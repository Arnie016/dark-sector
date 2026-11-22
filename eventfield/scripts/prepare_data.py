#!/usr/bin/env python3
"""Build the atlas's read-only data cache from verified local files."""
import argparse
import csv
import hashlib
import json
import warnings
from pathlib import Path

import astropy.units as u
import h5py
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.cosmology import FlatLambdaCDM
from astropy.io import fits
from astropy.wcs import WCS
from scipy.ndimage import map_coordinates
from scipy.signal import fftconvolve

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT.parent / "research"
CATALOG_HASH = "d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d"
RELIC_HASH = "4a46302883b9308a771eb2ebf914f8b0a22a22a10f6280f33477568689d70db9"
HOST_HASH = "9c5af9f24d8220228c58692b3b7d20777355e50f38ff484a50763a2c5afa39a2"
BOX_CKPC_H = 680000
H = 0.6774
BEAM_KPC = 135
SHARD_SIZE = 64

FIELDS = [
    ("macs", "MACS J1752", "PSZ2 G071.21+28.86", 0.366, "two-cluster-physical-beam"),
    ("g181", "PSZ2 G181", "PSZ2 G181.06+48.47", 0.234, "two-cluster-physical-beam"),
    ("g099", "PSZ2 G099", "PSZ2 G099.48+55.60", 0.105, "g099-paired-positions"),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_hash(path, expected):
    if digest(path) != expected:
        raise ValueError(f"Unexpected SHA-256 for {path.name}")


def write_json(path, obj):
    path.write_text(json.dumps(obj, separators=(",", ":"), allow_nan=False) + "\n")


def extract_catalog(inputs, out):
    path = inputs / "cluster_mergers.hdf5"
    require_hash(path, CATALOG_HASH)
    redshifts = {
        row["number"]: row["redshift"]
        for row in json.loads((inputs / "snapshot_redshifts.json").read_text())
    }
    scale = np.array([1 / (1 + redshifts[i]) for i in range(30, 100)])
    tng_cosmo = FlatLambdaCDM(H0=100 * H, Om0=0.3089)
    snapshots = [
        [i, redshifts[i], round(tng_cosmo.age(redshifts[i]).value, 7)]
        for i in range(30, 100)
    ]
    (out / "tracks").mkdir(exist_ok=True)
    with h5py.File(path) as catalog:
        if catalog["Mhistory_vel"].shape != (2083, 70, 6):
            raise ValueError("Unexpected velocity array shape")
        fields = []

        def add_field(key, value):
            if isinstance(value, h5py.Dataset):
                fields.append({"name": key, "shape": list(value.shape), "dtype": str(value.dtype)})

        catalog.visititems(add_field)
        snaps = catalog["Mhistory_snap"][:]
        positions = catalog["Mhistory_orbit"][:]
        velocities = catalog["Mhistory_vel"][:]
        masses = catalog["Mhistory_mass"][:]
        ids = [catalog[key][:] for key in ("HaloID", "MainclusterID", "SubclusterID", "Snap_coll")]
        measures = [catalog[key][:] for key in ("Mass_ratio", "V_coll", "M_Crit200_coll")]

    events = []
    for start in range(0, len(snaps), SHARD_SIZE):
        shard = {}
        for row in range(start, min(start + SHARD_SIZE, len(snaps))):
            valid = (snaps[row] >= 30) & (snaps[row] <= 99)
            valid &= np.all(np.isfinite(positions[row]) & np.isfinite(velocities[row]), axis=1)
            selected = snaps[row, valid].astype(int)
            order = np.argsort(selected)
            selected = selected[order]
            if len(selected) != len(set(selected)):
                raise ValueError(f"Duplicate snapshot in event {row}")
            pos = positions[row, valid][order].astype(float)
            vel = velocities[row, valid][order].astype(float)
            delta = (pos[:, 3:] - pos[:, :3] + BOX_CKPC_H / 2) % BOX_CKPC_H - BOX_CKPC_H / 2
            delta *= scale[selected - 30, None] / H
            relative_velocity = vel[:, 3:] - vel[:, :3]
            values = np.round(np.column_stack((delta, relative_velocity)), 4).tolist()
            mass = [
                [round(float(v), 7) if np.isfinite(v) and v > 0 else None for v in pair]
                for pair in masses[row, valid][order]
            ]
            shard[str(row)] = [[int(s), *vec, *pair] for s, vec, pair in zip(selected, values, mass)]
            metrics = [
                round(float(field[row]), 6) if np.isfinite(field[row]) and field[row] >= 0 else None
                for field in measures
            ]
            events.append([row, *(int(field[row]) for field in ids), *metrics, len(selected)])
        write_json(out / "tracks" / f"{start // SHARD_SIZE}.json", shard)

    base = json.loads((inputs / "event_summary.json").read_text())
    if base["catalog_sha256"] != CATALOG_HASH or len(events) != 2083:
        raise ValueError("Catalog baseline does not match")
    frames = json.loads((out / "tracks" / "0.json").read_text())["5"]
    row = next(frame for frame in frames if frame[0] == base["Snap_coll"])
    if abs(np.linalg.norm(row[1:4]) - base["snapshot_collision_separation_proper_kpc"]) > 0.001:
        raise ValueError("Baseline position was not reproduced")
    if abs(np.linalg.norm(row[4:7]) - base["snapshot_collision_relative_speed_km_s"]) > 0.001:
        raise ValueError("Baseline corrected velocity was not reproduced")
    write_json(out / "catalog.json", {
        "sha256": CATALOG_HASH,
        "size": path.stat().st_size,
        "targets": len({row[1] for row in events}),
        "chunkSize": SHARD_SIZE,
        "fields": fields,
        "snapshots": snapshots,
        "events": events,
        "eventColumns": ["row", "halo", "main", "secondary", "collision", "ratio", "speed", "mass200", "frames"],
        "baseline": base,
    })
    print(f"Catalog: {len(events)} events, {sum(row[-1] for row in events):,} valid frames")


def copy_gallery(gas, radio, out):
    gallery = out / "gallery"
    gallery.mkdir(exist_ok=True)
    for kind, source, manifest in [
        ("gas", gas, "multiwavelength-gallery-subhalo0"),
        ("radio", radio, "relic-gallery-subhalo0"),
    ]:
        items = json.loads((RESEARCH / manifest / "manifest.json").read_text())["images"]
        for row in items:
            name = row["filename"]
            dest = f"radio_{name}" if kind == "radio" else name
            frame = source / name
            require_hash(frame, row["sha256"])
            (gallery / dest).write_bytes(frame.read_bytes())


def extract_hosts(tng, out):
    path = tng / "additional-catalogs" / "TNG-Cluster_Catalog.hdf5"
    if not path.is_file():
        return
    require_hash(path, HOST_HASH)
    with h5py.File(path) as source:
        ids = source["haloID"][:].astype(int)
        fields = sorted(name for name, value in source.items() if isinstance(value, h5py.Dataset))
        radii = source["r500c"][:]
        if len(set(ids)) != 352 or radii.shape != (352,) or np.any(radii <= 0):
            raise ValueError("Unexpected cluster inventory")
        write_json(out / "hosts.json", {
            "bytes": path.stat().st_size, "sha256": HOST_HASH, "fields": fields,
            "halos": [[int(i), round(float(radius), 2)] for i, radius in zip(ids, radii)],
        })


def read_catalog_centers(path):
    require_hash(path, RELIC_HASH)
    lines = path.read_text().splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("recno\tName\t"))
    return list(csv.DictReader([lines[start], *lines[start + 3:]], delimiter="\t"))


def read_radio_map(path):
    with fits.open(path) as hdul:
        image = np.squeeze(hdul[0].data).astype(float)
        header = hdul[0].header.copy()
    if image.ndim != 2 or header.get("BUNIT", "").upper() != "JY/BEAM":
        raise ValueError(f"Unexpected units or dimensions in {path.name}")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wcs = WCS(header).celestial
    return image, header, wcs


def smooth_to_beam(image, header, wcs, target_deg):
    angle = np.radians(header["BPA"])
    major, minor = np.array([np.sin(angle), np.cos(angle)]), np.array([np.cos(angle), -np.sin(angle)])
    old_cov = header["BMAJ"]**2 * np.outer(major, major) + header["BMIN"]**2 * np.outer(minor, minor)
    inv_cd = np.linalg.inv(wcs.pixel_scale_matrix)
    cov = inv_cd @ (np.eye(2) * target_deg**2 - old_cov) @ inv_cd.T / (8 * np.log(2))
    eig = np.linalg.eigvalsh(cov)
    if eig[0] <= 0:
        raise ValueError("Requested beam is narrower than the native beam")
    width = int(np.ceil(6 * np.sqrt(eig[-1])))
    y, x = np.mgrid[-width:width + 1, -width:width + 1]
    coords = np.stack([x, y], axis=-1)
    kernel = np.exp(-0.5 * np.einsum("...i,ij,...j->...", coords, np.linalg.inv(cov), coords))
    kernel /= kernel.sum()
    vectors = coords.reshape(-1, 2)
    actual_cov = np.einsum("n,ni,nj->ij", kernel.ravel(), vectors, vectors)
    if not np.allclose(actual_cov, cov, rtol=1e-5, atol=1e-5):
        raise ValueError("Beam kernel covariance mismatch")
    valid = np.isfinite(image)
    result = fftconvolve(np.where(valid, image, 0), kernel, mode="same")
    result *= 1000 * target_deg**2 / (header["BMAJ"] * header["BMIN"])
    result[fftconvolve(valid.astype(float), kernel, mode="same") < 0.999] = np.nan
    return result


def repeated_checks(wcs, cutouts, data, kpc_arcsec, pixel_arcsec, study, name):
    with (RESEARCH / study / "variants.csv").open() as handle:
        refs = {
            (int(row["radius_kpc"]), float(row["threshold_mjy_per_beam"])): float(row["pair_difference_kpc"])
            for row in csv.DictReader(handle) if row["cluster"] == name
        }
    test = []
    for (radius, cut), expected in sorted(refs.items()):
        separations = []
        for image in range(2):
            centers = []
            for info, arrays in zip(cutouts, data):
                array = arrays[image]
                yy, xx = np.indices(array.shape)
                cx, cy = info["center"]
                inside = np.hypot(xx - cx, yy - cy) <= radius / (kpc_arcsec * pixel_arcsec)
                common = np.isfinite(arrays[0]) & np.isfinite(arrays[1])
                mask = inside & common & (array > cut)
                v = array[mask]
                selected = np.argsort(v, kind="stable")[-int(np.ceil(0.1 * len(v))):]
                x = np.average(xx[mask][selected], weights=v[selected]) + info["origin"][0]
                y = np.average(yy[mask][selected], weights=v[selected]) + info["origin"][1]
                centers.append(wcs.pixel_to_world(x, y))
            separations.append(centers[0].separation(centers[1]).arcsec * kpc_arcsec)
        actual = separations[0] - separations[1]
        if abs(expected - actual) > 0.002:
            raise ValueError(f"{name} {radius=} {cut=} separation difference {actual} vs {expected}")
        test.append([radius, cut, expected])
    if len(test) != 9:
        raise ValueError(f"Expected nine reference configurations for {name}")
    return test


def build_panorama(radio, key, native_data, matched, grids, cutouts, pixel_kpc):
    centers = [np.array(c["center"]) + np.array(c["origin"]) for c in cutouts]
    midpoint = (centers[0] + centers[1]) / 2
    direction = centers[1] - centers[0]
    length = np.linalg.norm(direction)
    along = direction / length
    up = np.array([-along[1], along[0]])
    margin = np.ceil(760 / pixel_kpc)
    width = int(np.ceil(length + 2 * margin)) + 1
    height = int(np.ceil(max(2 * margin, width * 0.45))) + 1
    cy, cx = (height - 1) / 2, (width - 1) / 2
    yy, xx = np.indices((height, width), dtype=float)
    plane_x = midpoint[0] + (xx - cx) * along[0] + (cy - yy) * up[0]
    plane_y = midpoint[1] + (xx - cx) * along[1] + (cy - yy) * up[1]
    native, grid = grids
    world = grid.pixel_to_world(plane_x, plane_y)
    px, py = native.world_to_pixel(world)
    north_end = grid.pixel_to_world(*midpoint).directional_offset_by(0 * u.deg, 30 * u.arcsec)
    north = np.asarray(grid.world_to_pixel(north_end)) - midpoint
    north /= np.linalg.norm(north)

    products = {}
    for mode, images in [("native", native_data), ("matched", matched)]:
        before = map_coordinates(images[0], [py, px], order=1, mode="constant", cval=np.nan)
        after = map_coordinates(images[1], [plane_y, plane_x], order=1, mode="constant", cval=np.nan)
        values = np.stack([before, after]).astype("<f4")
        noise = max(
            1.4826 * np.nanmedian(np.abs(plane - np.nanmedian(plane))) for plane in values
        )
        noise = max(0.001, float(noise))
        ceiling = max(10 * noise, float(np.nanpercentile(values, 99.7)))
        filename = f"{key}-field-{mode}.bin"
        (radio / filename).write_bytes(values.tobytes())
        products[mode] = {"file": filename, "noise": noise, "ceiling": ceiling}

    return {
        "width": width, "height": height, "pixelKpc": pixel_kpc, "midpoint": midpoint.tolist(),
        "along": along.tolist(), "up": up.tolist(), "north": [float(north @ along), float(-north @ up)],
        "layers": products,
    }


def extract_radio(folder, out):
    entries = read_catalog_centers(folder / "rrsamp.tsv")
    radio = out / "radio"
    radio.mkdir(exist_ok=True)
    cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
    all_checks = {}
    for key, name, identifier, z, study in FIELDS:
        ref = json.loads((RESEARCH / study / "summary.json").read_text())["clusters"][name]
        kpc_arcsec = cosmo.kpc_proper_per_arcmin(z).value / 60
        target_deg = BEAM_KPC / kpc_arcsec / 3600
        images, grids, native_data, beams = [], [], [], []
        for label in ("T50", "T50SUB"):
            path = folder / f"{key}-{label.lower()}.fits"
            require_hash(path, ref["input_sha256"][label])
            image, header, wcs = read_radio_map(path)
            images.append(smooth_to_beam(image, header, wcs, target_deg))
            grids.append(wcs)
            native_data.append(image * 1000)
            beams.append([round(header[name] * 3600, 2) for name in ("BMAJ", "BMIN")])
        native, wcs = grids
        cd = wcs.pixel_scale_matrix
        scales = np.sqrt(np.sum(cd**2, axis=0)) * 3600
        if not np.isclose(scales[0], scales[1], rtol=1e-4):
            raise ValueError("Expected square map pixels")
        pixel_arcsec = float(scales[0])
        ctype = [value.split("-")[-1] for value in wcs.wcs.ctype]
        if ctype != ["SIN", "SIN"] and ctype != ["TAN", "TAN"]:
            raise ValueError(f"Unsupported FITS projection: {ctype}")
        if wcs.has_distortion or wcs.wcs.get_pv():
            raise ValueError("Unexpected distortion or projection parameters")
        # Cut out a little more than the largest aperture while retaining the native sampling.
        pad = int(np.ceil(660 / (kpc_arcsec * pixel_arcsec)))
        cutouts, data = [], []
        for part in ("N", "S"):
            entry = next(row for row in entries if row["Name"].strip() == identifier and row["Pos"].strip() == part)
            # Keep the ICRS seed convention of the reference scripts. Astropy converts
            # these directions to the FK5 coordinates used by the map WCS.
            sky = SkyCoord(float(entry["RAJ2000"]) * u.deg, float(entry["DEJ2000"]) * u.deg)
            cx, cy = np.asarray(wcs.world_to_pixel(sky), dtype=float)
            x0, y0 = int(cx) - pad, int(cy) - pad
            side = 2 * pad + 1
            if min(x0, y0) < 0 or x0 + side > images[1].shape[1] or y0 + side > images[1].shape[0]:
                raise ValueError(f"{key} {part} cutout goes outside image")
            yy, xx = np.mgrid[y0:y0 + side, x0:x0 + side]
            ix, iy = native.world_to_pixel(wcs.pixel_to_world(xx, yy))
            before = map_coordinates(images[0], [iy, ix], order=1, mode="constant", cval=np.nan)
            after = images[1][y0:y0 + side, x0:x0 + side]
            both = np.stack([before, after]).astype("<f4")
            filename = f"{key}-{part}.bin"
            (radio / filename).write_bytes(both.tobytes())
            cutouts.append({
                "name": part, "file": filename, "side": side,
                "origin": [x0, y0], "center": [cx - x0, cy - y0],
                "catalogDegrees": [float(entry["RAJ2000"]), float(entry["DEJ2000"])],
            })
            data.append(both)
        all_checks[key] = repeated_checks(wcs, cutouts, data, kpc_arcsec, pixel_arcsec, study, name)
        panorama = build_panorama(radio, key, native_data, images, grids, cutouts, pixel_arcsec * kpc_arcsec)
        panorama["beamsArcsec"] = beams
        write_json(radio / f"{key}.json", {
            "id": key, "cluster": name, "psZ2": identifier, "z": z,
            "inputSha256": ref["input_sha256"], "sourceCatalogSha256": RELIC_HASH,
            "targetBeam": BEAM_KPC, "kpcArcsec": kpc_arcsec, "pixelArcsec": pixel_arcsec,
            "wcs": {
                "type": ctype[0], "frame": wcs.wcs.radesys, "equinox": wcs.wcs.equinox,
                "cd": cd.tolist(), "refPixel": (wcs.wcs.crpix - 1).tolist(),
                "refWorld": wcs.wcs.crval.tolist(),
            },
            "cutouts": cutouts,
            "panorama": panorama,
        })
        print(f"Radio: matched all nine {name} reference configurations")
    write_json(radio / "validation.json", all_checks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tng", required=True, type=Path, help="Directory with catalog and snapshot metadata")
    parser.add_argument("--gas-gallery", required=True, type=Path)
    parser.add_argument("--radio-gallery", required=True, type=Path)
    parser.add_argument("--fits", required=True, type=Path, help="Directory of six approved FITS maps and rrsamp.tsv")
    args = parser.parse_args()
    out = ROOT / "data" / "local"
    out.mkdir(parents=True, exist_ok=True)
    extract_catalog(args.tng, out)
    extract_hosts(args.tng, out)
    copy_gallery(args.gas_gallery, args.radio_gallery, out)
    extract_radio(args.fits, out)


if __name__ == "__main__":
    main()
