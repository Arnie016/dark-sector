import { byId, choose, downloadCsv, number, setText, signed, value } from "./dom.js";
import { getRadio } from "./data.js";
import { drawRadio, drawRadioCurve, RADIO_MAX } from "./charts.js";
import { measureRadio } from "./engine.js";

let field = null;
let channel = 0;
let request = 0;
let measurement = null;
let readings = [];
let renderHandle = 0;

const settings = () => ({
  radius: value("aperture"),
  threshold: value("threshold"),
  fraction: value("bright-fraction") / 100,
});

function paint() {
  if (!field || !measurement || byId("view-radio").hidden) return;
  field.cutouts.forEach((cut, i) => {
    const result = measurement.points[i][channel];
    const canvas = byId(i === 0 ? "radio-n" : "radio-s");
    const label = i ? "Southern relic" : "Northern relic";
    canvas.setAttribute("aria-label", `${label}, ${channel ? "T50SUB" : "T50"}. ${result.selected?.length ?? 0} bright pixels used to estimate its position.`);
    drawRadio(canvas, cut, result, measurement.radiusPixels, channel);
  });
  drawRadioCurve(byId("radio-curve"), readings);
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
  choose("radio-field", "field", id);
  try {
    const next = await getRadio(id);
    if (ticket !== request) return;
    field = next;
    setText("radio-id", `${field.psZ2} · z = ${field.z.toFixed(3)}`);
    setText("radio-cluster", id === "g099" ? "Abell 1925" : field.cluster);
    setText("radio-color-label", `Flux 0–${RADIO_MAX} mJy/beam · asinh`);
    byId("radio-layout").hidden = false;
    byId("radio-series").hidden = false;
    update();
  } catch (error) {
    if (ticket !== request) return;
    console.warn("Radio read", error.message);
    if (field) choose("radio-field", "field", field.id);
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
  byId("radio-field").addEventListener("click", event => {
    const id = event.target.closest("button")?.dataset.field;
    if (!id) return;
    const hash = `#radio?field=${id}`;
    if (location.hash === hash) loadRadio(id);
    else location.hash = hash;
  });
  byId("radio-image-mode").addEventListener("click", event => {
    const image = event.target.closest("button")?.dataset.image;
    if (image === undefined) return;
    channel = Number(image);
    choose("radio-image-mode", "image", channel);
    paint();
  });
  for (const key of ["aperture", "threshold", "bright-fraction"]) byId(key).addEventListener("input", queueUpdate);
  byId("aperture-presets").addEventListener("click", event => {
    const radius = event.target.closest("button")?.dataset.radius;
    if (!radius) return;
    byId("aperture").value = radius;
    queueUpdate();
  });
  byId("radio-export").addEventListener("click", exportMeasurement);
  byId("radio-question").addEventListener("click", () => { location.hash = "#desk?topic=radio"; });
  const observer = new ResizeObserver(paint);
  observer.observe(byId("radio-n"));
  observer.observe(byId("radio-curve"));
}
