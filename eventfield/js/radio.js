import { byId, choose, downloadCsv, number, setText, signed, value } from "./dom.js";
import { getRadio, getRadioPanorama } from "./data.js";
import { drawRadio, drawRadioCurve, drawRadioPanorama } from "./charts.js";
import { measureRadio } from "./engine.js";

let field = null;
let channel = 1;
let request = 0;
let mapRequest = 0;
let measurement = null;
let readings = [];
let renderHandle = 0;
let panorama = null;
let faint = false;

const settings = () => ({
  radius: value("aperture"),
  threshold: value("threshold"),
  fraction: value("bright-fraction") / 100,
});

function paint() {
  if (!field || !measurement || byId("view-radio").hidden) return;
  const canvas = byId("radio-sky");
  const activeMeasurement = byId("radio-measure").open ? measurement : null;
  if (panorama) {
    const marker = panorama.mode === "matched" ? activeMeasurement : null;
    drawRadioPanorama(canvas, panorama, field, marker, channel, faint);
    const mode = channel ? "T50SUB" : "T50";
    const pair = marker ? ` Measured separation ${number(measurement.separations[channel], 1)} kiloparsecs.` : "";
    canvas.setAttribute("aria-label", `${field.cluster} wide LoTSS field, ${mode}. Northern catalog relic on the left and southern relic on the right.${pair}`);
  } else {
    canvas.setAttribute("aria-label", `${field.cluster}, southern relic cutout`);
    drawRadio(canvas, field.cutouts[1], activeMeasurement?.points[1][channel], measurement.radiusPixels, channel);
  }
  if (activeMeasurement) drawRadioCurve(byId("radio-curve"), readings);
}

function describeImage() {
  if (!panorama) {
    setText("radio-color-label", "Southern cutout · prepare the current data cache for a wide field");
    return;
  }
  const matched = byId("radio-measure").open;
  const beam = panorama.beamsArcsec[channel].join(" × ");
  setText("radio-color-label", matched
    ? "135 kpc matched beam · measurement overlay"
    : `Native release beam ${beam}″ · regridded along the relic pair`);
}

async function loadMap() {
  if (!field) return;
  const ticket = ++mapRequest;
  const mode = byId("radio-measure").open ? "matched" : "native";
  try {
    const loaded = await getRadioPanorama(field, mode);
    if (ticket !== mapRequest) return;
    panorama = loaded;
    byId("radio-sky").style.aspectRatio = loaded ? `${loaded.width} / ${loaded.height}` : "2 / 1";
  } catch (error) {
    if (ticket !== mapRequest) return;
    console.warn("Wide radio map", error.message);
    panorama = null;
  }
  describeImage();
  paint();
}

function update() {
  if (!field) return;
  const { radius, threshold, fraction } = settings();
  setText("aperture-out", `${radius} kpc`);
  byId("aperture").setAttribute("aria-valuetext", `${radius} kiloparsecs`);
  setText("threshold-out", `${number(threshold, 3).replace(/0$/, "")} mJy/beam`);
  setText("fraction-out", `${Math.round(fraction * 100)}%`);
  choose("aperture-presets", "radius", radius);
  measurement = measureRadio(field, radius, threshold, fraction);
  const ids = [...new Set([300, 450, 600, radius])].sort((a, b) => a - b);
  readings = ids.map(r => ({
    radius: r, cursor: r === radius,
    delta: r === radius ? measurement.delta : measureRadio(field, r, threshold, fraction).delta,
  }));
  setText("radio-delta", signed(measurement.delta, 2));
  setText("radio-before", `${number(measurement.separations[0], 1)} kpc`);
  setText("radio-after", `${number(measurement.separations[1], 1)} kpc`);
  const note = readings.map(sample => `${sample.radius} kpc → ${signed(sample.delta, 2)} kpc`).join("  ·  ");
  setText("radio-curve-note", note);
  setText("radio-status", measurement.delta === null ? "One aperture has too few eligible pixels or insufficient common coverage. Try a wider circle or a lower threshold." : "");
  byId("radio-export").disabled = measurement.delta === null;
  paint();
}

function queueUpdate() {
  cancelAnimationFrame(renderHandle);
  renderHandle = requestAnimationFrame(update);
}

export async function loadRadio(id = "g181") {
  const ticket = ++request;
  if (field?.id === id) {
    update();
    return;
  }
  setText("radio-status", "Loading the paired radio maps…");
  byId("radio-field").value = id;
  try {
    const next = await getRadio(id);
    if (ticket !== request) return;
    field = next;
    panorama = null;
    setText("radio-id", `${field.psZ2} · z = ${field.z.toFixed(3)}`);
    setText("radio-cluster", id === "g099" ? "Abell 1925" : field.cluster);
    byId("radio-layout").hidden = false;
    update();
    loadMap();
  } catch (error) {
    if (ticket !== request) return;
    console.warn("Radio read", error.message);
    if (field) byId("radio-field").value = field.id;
    setText("radio-status", "The requested cutouts could not be read. Prepare the local atlas data and select the field again.");
  }
}

function exportMeasurement() {
  const { radius, threshold, fraction } = settings();
  const header = [
    "field", "redshift", "beam_fwhm_kpc", "radius_kpc", "threshold_mjy_per_beam", "brightest_fraction", "map", "relic",
    "eligible_pixels", "selected_pixels", "coverage_fraction", "centroid_x_parent_px", "centroid_y_parent_px",
    "pair_separation_kpc", "t50_minus_t50sub_kpc", "input_sha256", "relic_catalog_sha256",
  ];
  const rows = measurement.points.flatMap((pair, index) => pair.map((point, map) => {
    const cut = field.cutouts[index];
    const label = map ? "T50SUB" : "T50";
    return [
      field.psZ2, field.z, field.targetBeam, radius, threshold, fraction, label, cut.name,
      point.eligible, point.selected?.length ?? 0, point.coverage,
      ...point.center?.map((v, j) => cut.origin[j] + v) ?? ["", ""],
      measurement.separations[map], measurement.delta, field.inputSha256[label], field.sourceCatalogSha256,
    ];
  }));
  downloadCsv(`eventfield-${field.id}-radio-${radius}kpc.csv`, [header, ...rows]);
}

export function wireRadio() {
  byId("radio-field").addEventListener("change", event => {
    const id = event.target.value;
    const hash = `#radio?field=${id}`;
    if (location.hash === hash) loadRadio(id);
    else location.hash = hash;
  });
  byId("radio-image-mode").addEventListener("click", event => {
    const image = event.target.closest("button")?.dataset.image;
    if (image === undefined) return;
    channel = Number(image);
    choose("radio-image-mode", "image", channel);
    describeImage();
    paint();
  });
  byId("radio-measure").addEventListener("toggle", loadMap);
  byId("radio-faint").addEventListener("click", event => {
    faint = !faint;
    event.currentTarget.setAttribute("aria-pressed", String(faint));
    event.currentTarget.textContent = faint ? "Hide faint signal" : "Show faint signal";
    paint();
  });
  const fullscreen = byId("radio-fullscreen");
  fullscreen.addEventListener("click", async () => {
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else await fullscreen.parentElement.requestFullscreen();
    } catch {
      fullscreen.parentElement.classList.toggle("expanded");
      updateFullscreen();
    }
  });
  function updateFullscreen() {
    const expanded = document.fullscreenElement !== null || fullscreen.parentElement.classList.contains("expanded");
    fullscreen.ariaLabel = expanded ? "Exit full screen" : "Enter full screen";
    fullscreen.title = fullscreen.ariaLabel;
    fullscreen.textContent = expanded ? "×" : "⤢";
    paint();
  }
  document.addEventListener("fullscreenchange", updateFullscreen);
  document.addEventListener("keydown", event => {
    if (event.key !== "Escape" || !fullscreen.parentElement.classList.contains("expanded")) return;
    fullscreen.parentElement.classList.remove("expanded");
    updateFullscreen();
  });
  for (const key of ["aperture", "threshold", "bright-fraction"]) byId(key).addEventListener("input", queueUpdate);
  byId("aperture-presets").addEventListener("click", event => {
    const radius = event.target.closest("button")?.dataset.radius;
    if (!radius) return;
    byId("aperture").value = radius;
    queueUpdate();
  });
  byId("radio-export").addEventListener("click", exportMeasurement);
  const observer = new ResizeObserver(paint);
  observer.observe(byId("radio-sky"));
  observer.observe(byId("radio-curve"));
}
