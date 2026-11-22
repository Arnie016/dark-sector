import { byId, choose, downloadCsv, number, setText, signed, value } from "./dom.js";
import { getEvent } from "./data.js";
import { drawOrbit, drawSeries } from "./charts.js";
import { integrateOrbit, norm, project } from "./engine.js";

const state = { event: null, cursor: 0, modelCursor: 0, mode: "replay", seed: null, model: null, timer: null };
let latestRequest = 0;

function collisionIndex() {
  return state.event.frames.findIndex(frame => frame.snapshot === state.event.record.collision);
}

function isModel() {
  return state.mode === "model";
}

function camera() {
  return { yaw: value("yaw"), pitch: value("pitch"), zoom: value("zoom"), model: isModel() };
}

function seedFrom(frame) {
  if (!frame || !frame.m1 || !frame.m2) return false;
  state.seed = { ...frame, mass: (frame.m1 + frame.m2) * 1e14 };
  state.modelCursor = 0;
  return true;
}

function earliestApproach() {
  const frames = state.event.frames;
  const index = collisionIndex();
  const target = frames[Math.max(0, index)].t - 0.65;
  return frames.reduce((closest, next) => Math.abs(next.t - target) < Math.abs(closest.t - target) ? next : closest);
}

function computeModel() {
  const params = { massScale: value("mass-scale"), epsilon: value("softening"), sideways: value("sideways") };
  state.model = integrateOrbit(state.seed, params);
  setText("mass-out", `${params.massScale.toFixed(2)}×`);
  setText("soft-out", `${params.epsilon} kpc`);
  setText("side-out", `${params.sideways.toFixed(2)}×`);
  setText("model-seed", `Event ${state.event.record.row}, snapshot ${state.seed.snapshot}. Initial distance ${number(norm(state.seed.position), 1)} kpc. Catalog mass sum ${number(state.seed.mass / 1e14, 2)} × 10¹⁴ M☉.`);
  const { min, residual } = state.model;
  setText("model-report", `Smallest modeled separation is ${number(min.radius, 1)} kpc at ${min.t} Myr after the seed. Maximum normalized energy residual is ${(residual * 100).toPrecision(3)}% over 1.8 Gyr with a 1 Myr step.`);
}

export function stopOrbit() {
  clearInterval(state.timer);
  state.timer = null;
  const play = byId("play");
  play.textContent = "▶";
  play.setAttribute("aria-label", "Play snapshots");
  play.title = "Play snapshots";
}

function activeFrames() {
  return isModel() ? state.model.frames : state.event.frames;
}

function cursorIndex() {
  return isModel() ? state.modelCursor : state.cursor;
}

function updateCursor(index) {
  if (isModel()) state.modelCursor = index;
  else state.cursor = index;
}

function modelMinimumIndex() {
  return state.model.frames.findIndex(frame => frame.t === Math.round(state.model.min.t / 15) * 15);
}

function paint() {
  if (!state.event?.frames.length || byId("view-orbit").hidden) return;
  const model = isModel();
  const rows = activeFrames();
  const index = cursorIndex();
  const current = rows[index];
  const marker = model ? modelMinimumIndex() : collisionIndex();
  const settings = camera();
  const pos = project(current.position, settings.yaw, settings.pitch);
  const vel = project(current.velocity, settings.yaw, settings.pitch);
  const time = byId("time-input");
  time.max = rows.length - 1;
  time.value = index;
  time.setAttribute("aria-valuetext", model ? `${current.t} Myr after seed` : `Snapshot ${current.snapshot}`);
  setText("time-output", model ? `${current.t} Myr after seed` : `${current.snapshot} / ${rows.at(-1).snapshot} · z = ${current.redshift.toFixed(3)}`);
  setText("r3", number(norm(current.position), 1));
  setText("r2", number(Math.hypot(...pos.slice(0, 2)), 1));
  setText("v3", number(norm(current.velocity)));
  setText("vlos", signed(vel[2]));
  setText("yaw-out", `${settings.yaw}°`);
  setText("pitch-out", `${settings.pitch}°`);
  setText("zoom-out", `${settings.zoom.toFixed(1)}×`);
  const activePreset = `${settings.yaw},${settings.pitch}`;
  for (const button of document.querySelectorAll("[data-camera]")) {
    button.setAttribute("aria-pressed", String(button.dataset.camera === activePreset));
  }
  byId("orbit-canvas").setAttribute("aria-label", `Projected secondary position relative to primary. Separation ${number(Math.hypot(...pos.slice(0, 2)), 1)} kpc projected and ${number(norm(current.position), 1)} kpc in 3D.`);
  drawOrbit(byId("orbit-canvas"), rows, index, settings, marker);
  drawSeries(byId("series-canvas"), rows, index, { index: marker, unit: model ? "Myr after seed" : "Approximate cosmic age · Gyr" });
}

function describeMode() {
  const model = isModel();
  const { record, frames } = state.event;
  byId("model-settings").hidden = !model;
  const tag = byId("orbit-kind");
  tag.className = `kind ${model ? "model" : "simulation"}`;
  tag.textContent = model ? "Educational model" : "TNG-Cluster simulation";
  setText("event-title", model ? `Two-body orbit · Event ${record.row}` : `Halo ${record.halo} · Event ${record.row}`);
  setText("scene-mode", model ? "Modeled relative orbit" : "Primary halo frame");
  setText("orbit-hint", "Drag to rotate · amber arrow shows relative velocity");
  setText("time-label", model ? "Model time" : "Recorded snapshot");
  setText("jump", model ? "Closest model sample ↗" : "First passage ↗");
  const jump = byId("jump");
  jump.disabled = !model && collisionIndex() < 0;
  jump.title = model ? "Jump to the plotted model sample nearest closest approach" : "Jump to first stored snapshot after pericenter";
  setText("series-title", model ? "The modeled encounter" : "Separation and speed");
  setText("series-subtitle", model ? "Modeled samples every 15 Myr" : "Recorded samples in approximate cosmic time");
  setText("series-note", model
    ? "Fixed masses and softened Newtonian gravity. The dashed line marks the plotted sample nearest the modeled minimum."
    : "The dashed line marks the first stored snapshot after pericenter when it is present. Peculiar velocity excludes Hubble flow. The connecting lines guide the eye between samples.");
  const details = byId("event-detail");
  details.replaceChildren();
  for (const [title, body] of model ? [
    ["Seed", `Recorded snapshot ${state.seed.snapshot}`],
    ["Model", "Fixed masses with an adjustable softened force"],
  ] : [
    ["Primary / secondary", `${record.main} / ${record.secondary}`],
    ["History", `${frames.length} snapshots · ${frames[0].snapshot}–${frames.at(-1).snapshot}`],
    ["Mass ratio", record.ratio === null ? "Unavailable" : `${number(record.ratio, 3)} at peak secondary mass`],
  ]) {
    const p = document.createElement("p");
    const label = document.createElement("strong");
    label.textContent = title;
    p.append(label, ` · ${body}`);
    details.append(p);
  }
  choose("orbit-mode", "mode", state.mode);
  paint();
}

function setMode(mode) {
  if (!state.event?.frames.length) return;
  stopOrbit();
  if (mode === "model") {
    if (!state.seed && !seedFrom(earliestApproach())) {
      setText("orbit-status", "The model needs a sample with two positive subhalo masses. Try another row.");
      return;
    }
    computeModel();
  }
  setText("orbit-status", "");
  state.mode = mode;
  describeMode();
}

export async function loadOrbit(row = 5, mode = "replay", snapshot = null) {
  const id = ++latestRequest;
  const load = byId("event-form").querySelector("button");
  stopOrbit();
  if (state.event && state.event.record.row === row) {
    load.disabled = false;
    const target = state.event.frames.findIndex(frame => frame.snapshot === snapshot);
    if (target >= 0) state.cursor = target;
    setMode(mode);
    return;
  }
  load.disabled = true;
  setText("orbit-status", `Loading catalog row ${row}…`);
  try {
    const event = await getEvent(row);
    if (id !== latestRequest) return;
    if (!event.frames.length) {
      setText("orbit-status", `Row ${row} has no valid stored position and velocity samples. Choose another row.`);
      return;
    }
    state.event = event;
    state.mode = "replay";
    const target = event.frames.findIndex(frame => frame.snapshot === snapshot);
    state.cursor = target >= 0 ? target : Math.max(0, collisionIndex());
    state.seed = null;
    state.model = null;
    byId("event-number").value = row;
    byId("orbit-layout").hidden = false;
    byId("orbit-series").hidden = false;
    describeMode();
    setMode(mode);
  } catch (error) {
    if (id !== latestRequest) return;
    console.warn("Catalog read", error.message);
    setText("orbit-status", "The local catalog could not be read. Prepare the atlas data and try loading the row again.");
  } finally {
    if (id === latestRequest) load.disabled = false;
  }
}

function exportOrbit() {
  const settings = camera();
  const model = isModel();
  const { record } = state.event;
  const header = [
    "catalog_row", "halo_id", "primary_id", "secondary_id", "snapshot", "redshift", model ? "model_time_myr" : "cosmic_age_gyr",
    "delta_x_kpc", "delta_y_kpc", "delta_z_kpc", "delta_vx_kms", "delta_vy_kms", "delta_vz_kms", "separation_kpc",
    "projected_separation_kpc", "speed_kms", "line_of_sight_kms", "yaw_deg", "tilt_deg",
    "primary_subhalo_mass_1e14_msun", "secondary_subhalo_mass_1e14_msun",
    "model_mass_scale", "model_softening_kpc", "model_tangential_scale",
  ];
  const rows = activeFrames().map(frame => {
    const p = project(frame.position, settings.yaw, settings.pitch);
    const v = project(frame.velocity, settings.yaw, settings.pitch);
    return [
      record.row, record.halo, record.main, record.secondary, frame.snapshot ?? state.seed?.snapshot, frame.redshift ?? "",
      frame.t, ...frame.position, ...frame.velocity, norm(frame.position), Math.hypot(p[0], p[1]), norm(frame.velocity),
      v[2], settings.yaw, settings.pitch, frame.m1 ?? state.seed?.m1, frame.m2 ?? state.seed?.m2,
      ...(model ? [value("mass-scale"), value("softening"), value("sideways")] : ["", "", ""]),
    ];
  });
  downloadCsv(`eventfield-row-${record.row}-${state.mode}.csv`, [header, ...rows]);
}

function wireDrag() {
  const canvas = byId("orbit-canvas");
  let gesture = null;
  canvas.addEventListener("pointerdown", event => {
    if (!event.isPrimary || event.button !== 0) return;
    gesture = { x: event.clientX, y: event.clientY, ...camera() };
    canvas.setPointerCapture(event.pointerId);
    canvas.classList.add("dragging");
  });
  canvas.addEventListener("pointermove", event => {
    if (!event.isPrimary || !gesture) return;
    const yaw = gesture.yaw + (event.clientX - gesture.x) * 0.55;
    const pitch = gesture.pitch + (event.clientY - gesture.y) * 0.45;
    byId("yaw").value = Math.round(((yaw + 180) % 360 + 360) % 360 - 180);
    byId("pitch").value = Math.round(Math.max(-90, Math.min(90, pitch)));
    paint();
  });
  canvas.addEventListener("lostpointercapture", () => {
    gesture = null;
    canvas.classList.remove("dragging");
  });
}

export function wireOrbit() {
  byId("event-form").addEventListener("submit", (event) => {
    event.preventDefault();
    const row = value("event-number");
    const hash = `#orbit?event=${row}`;
    if (location.hash === hash) loadOrbit(row);
    else location.hash = hash;
  });
  byId("orbit-mode").addEventListener("click", event => {
    const mode = event.target.closest("button")?.dataset.mode;
    if (mode) setMode(mode);
  });
  byId("time-input").addEventListener("input", () => {
    stopOrbit();
    updateCursor(value("time-input"));
    paint();
  });
  byId("play").addEventListener("click", () => {
    if (state.timer) return stopOrbit();
    if (activeFrames().length < 2) return;
    if (cursorIndex() >= activeFrames().length - 1) updateCursor(0);
    paint();
    const play = byId("play");
    play.textContent = "Ⅱ";
    play.setAttribute("aria-label", "Pause playback");
    play.title = "Pause playback";
    state.timer = setInterval(() => {
      if (cursorIndex() >= activeFrames().length - 1) return stopOrbit();
      updateCursor(cursorIndex() + 1);
      paint();
    }, isModel() ? 48 : 125);
  });
  byId("jump").addEventListener("click", () => {
    stopOrbit();
    updateCursor(Math.max(0, isModel() ? modelMinimumIndex() : collisionIndex()));
    paint();
  });
  for (const key of ["yaw", "pitch", "zoom"]) byId(key).addEventListener("input", paint);
  for (const button of document.querySelectorAll("[data-camera]")) {
    button.addEventListener("click", () => {
      const [yaw, pitch] = button.dataset.camera.split(",");
      byId("yaw").value = yaw;
      byId("pitch").value = pitch;
      paint();
    });
  }
  for (const key of ["mass-scale", "softening", "sideways"]) {
    byId(key).addEventListener("input", () => { stopOrbit(); computeModel(); paint(); });
  }
  byId("seed-model").addEventListener("click", () => {
    if (!seedFrom(state.event.frames[state.cursor])) {
      setText("orbit-status", "Choose a replay sample with measured masses for both subhalos.");
      return;
    }
    setMode("model");
  });
  byId("orbit-export").addEventListener("click", exportOrbit);
  byId("orbit-question").addEventListener("click", () => {
    location.hash = isModel() ? "#desk?topic=model" : "#desk?topic=velocity";
  });
  wireDrag();
  new ResizeObserver(paint).observe(byId("orbit-canvas"));
}
