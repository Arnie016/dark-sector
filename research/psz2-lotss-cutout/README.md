# PSZ2 G181.06+48.47: LoTSS image and redshift provenance

This directory generates a sky-registered view of an actual [LoTSS DR2 20-arcsecond radio cutout](https://lofar-surveys.org/cutout_api_details.html), with the two previously published radio-relic coordinates overlaid. The raw 1,272,960-byte FITS cutout and the VizieR source table are pinned by SHA-256 in `manifest.json` and stored in the private Azure archive alongside the analysis; the original data are not committed to GitHub. The image is a survey mosaic cutout, not the compact-source-subtracted image used in the original relic analysis. Bright sources and imaging artifacts are present. The map's FITS header gives a 20 × 20 arcsec beam, 143.65 MHz reference frequency and JY/BEAM brightness units. Both catalog coordinates land inside the image; markers are source catalog positions, **not positions independently measured from this cutout**. No source flux, shock front, lensing map, noise model or new detection is derived here.

## Cross-check: angular and physical separation

[Botteon et al. (2022)](https://www.aanda.org/articles/aa/pdf/2022/04/aa43020-21.pdf) list the cluster at redshift 0.240 in Table A.1 and give a flat cosmology with H0 = 70 km/s/Mpc, Ωm = 0.3. Their Table A.4 / the [VizieR table](https://vizier.cfa.harvard.edu/viz-bin/VizieR-3?-source=J%2FA%2BA%2F660%2FA78%2Frrsamp) list the rounded coordinates and a relic separation of 2694 ± 39 kpc. [Ahn et al. (2025)](https://arxiv.org/html/2501.09067) instead use z = 0.234 with the same H0 and Ωm. With Astropy spherical coordinates and angular-diameter distances, the published rounded coordinates are 11.8206 arcmin apart:

| Redshift used in conversion | Projected physical separation (kpc) |
| --- | ---: |
| 0.240 | 2691 |
| 0.234 | 2640 |

At z = 0.240 the calculation is 3.5 kpc below the tabulated 2694 kpc; this numerical agreement is consistent with the earlier redshift and cosmology, but the coordinates in the table are rounded and the unpublished details of the original calculation are not fully verified. Holding sky coordinates and cosmology fixed while changing only z shifts the derived separation by approximately 51 kpc. This is a convention sensitivity, not an independent change in the measured sky positions or a claim of inconsistency. Use the more recent redshift when comparing with quantities calculated at z = 0.234, while preserving the original published values and their own assumptions. The catalog's ±39 kpc is a reported measurement uncertainty, not a redshift or cross-catalog covariance estimate.

The prior [radius-sensitivity exercise](../psz2-radius-sensitivity/README.md) used the published 2694 kpc catalog value together with a radius calculated at z = 0.234. Replacing only the distance with the coordinate-derived 2640 kpc and retaining that illustrative 0.931 Mpc radius shifts the Lee line by approximately −0.030 Gyr. This is a bookkeeping sensitivity, not an updated age: radio positions and simulation relic-center definitions still differ, and uncertainties and covariances remain unmodeled.

## Reproduce and credit

Run `python analyze.py /path/to/cutout.fits /path/to/rrsamp.tsv` with NumPy, Astropy and matplotlib. If a machine has a broken matplotlib font cache, set `MPLCONFIGDIR` to a fresh writable directory. Both inputs are checked against the manifest; the image WCS, units and marker bounds are validated. A separate spherical trigonometry / numerical integration calculation verifies the angular separation and redshift conversions. The output `lotss-cutout.png` uses an asinh display stretch (mJy/beam), and `summary.json` records machine-readable values. The user can retrieve the FITS by the exact bounded request in `manifest.json`; survey updates may change the digest and must be inspected rather than silently accepted.

Credit the LOFAR Two-metre Sky Survey and cite the [DR2 release and acknowledgements](https://lofar-surveys.org/dr2_release.html), Botteon et al. and VizieR when reusing the data or image. No email was sent.
