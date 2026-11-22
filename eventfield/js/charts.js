import { norm, project } from "./engine.js";

const MINT = "#99dcd2";
const AMBER = "#ffb68f";
const PURPLE = "#c9b6ff";
const FAINT = "#aaa7bc";
const GRID = "#343548";
const MONO = '10px ui-monospace, Menlo, monospace';

function setup(canvas) {
  const { width, height } = canvas.getBoundingClientRect();
  if (!width || !height) return null;
  const density = Math.min(window.devicePixelRatio || 1, 2);
  if (canvas.width !== Math.round(width * density) || canvas.height !== Math.round(height * density)) {
    canvas.width = Math.round(width * density);
    canvas.height = Math.round(height * density);
  }
  const ctx = canvas.getContext("2d");
  ctx.setTransform(density, 0, 0, density, 0, 0);
  ctx.clearRect(0, 0, width, height);
  ctx.font = MONO;
  ctx.textBaseline = "middle";
  return { ctx, width, height };
}

function line(ctx, ax, ay, bx, by, color, width = 1) {
  ctx.beginPath();
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  ctx.moveTo(ax, ay);
  ctx.lineTo(bx, by);
  ctx.stroke();
}

function circle(ctx, x, y, r, color, fill = true) {
  ctx.beginPath();
  ctx.arc(x, y, r, 0, 2 * Math.PI);
  if (fill) {
    ctx.fillStyle = color;
    ctx.fill();
  } else {
    ctx.lineWidth = 1.05;
    ctx.strokeStyle = color;
    ctx.stroke();
  }
}

function label(ctx, value, x, y, color = FAINT, align = "left") {
  ctx.fillStyle = color;
  ctx.textAlign = align;
  ctx.fillText(value, x, y);
}

function niceStep(value) {
  const order = 10 ** Math.floor(Math.log10(Math.max(0.001, value)));
  const rounded = value / order;
  return (rounded < 1.5 ? 1 : rounded < 3 ? 2 : rounded < 7 ? 5 : 10) * order;
}

const formatted = (x, digits = 0) => x.toLocaleString("en-US", { maximumFractionDigits: digits });

function trace(ctx, points, color, width, dashed = []) {
  if (!points.length) return;
  ctx.beginPath();
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  ctx.lineJoin = "round";
  ctx.setLineDash(dashed);
  points.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y));
  ctx.stroke();
  ctx.setLineDash([]);
}

function halo(ctx, x, y, radius, color) {
  const light = ctx.createRadialGradient(x, y, 0, x, y, radius * 3);
  light.addColorStop(0, color);
  light.addColorStop(0.35, color + "5a");
  light.addColorStop(1, color + "00");
  circle(ctx, x, y, radius * 3, light);
  circle(ctx, x, y, radius * 1.45, color + "88", false);
  circle(ctx, x, y, radius * 0.52, color);
}

export function drawOrbit(canvas, frames, cursor, settings, marker, miniature = false) {
  const surface = setup(canvas);
  if (!surface || !frames.length) return;
  const { ctx, width, height } = surface;
  const { yaw, pitch, zoom, model } = settings;
  const origin = [width / 2, height * (miniature ? 0.5 : 0.52)];
  const projected = frames.map(({ position }) => project(position, yaw, pitch));
  const largest = Math.max(100, ...frames.map(({ position }) => norm(position)));
  const unit = Math.min(width, height) * 0.41 * zoom / largest;
  const point = ([x, y]) => [origin[0] + x * unit, origin[1] - y * unit];
  const step = niceStep(Math.min(width, height) / (unit * (miniature ? 4 : 6)));
  ctx.fillStyle = "#11131e";
  ctx.fillRect(0, 0, width, height);
  const glow = ctx.createRadialGradient(...origin, 0, ...origin, height * 0.57);
  glow.addColorStop(0, "#222434");
  glow.addColorStop(1, "#11131e");
  ctx.fillStyle = glow;
  ctx.fillRect(0, 0, width, height);
  const edgeX = Math.ceil(width / (2 * step * unit));
  const edgeY = Math.ceil(height / (2 * step * unit)) + 1;
  for (let i = -edgeX; i <= edgeX; i++) {
    const x = point([i * step, 0])[0];
    line(ctx, x, 0, x, height, i === 0 ? "#4b4d64" : GRID);
  }
  for (let i = -edgeY; i <= edgeY; i++) {
    const y = point([0, i * step])[1];
    line(ctx, 0, y, width, y, i === 0 ? "#4b4d64" : GRID);
  }
  if (!miniature) {
    const leg = step * unit;
    line(ctx, 16, height - 24, 16 + leg, height - 24, FAINT, 1.4);
    line(ctx, 16, height - 27, 16, height - 21, FAINT);
    line(ctx, 16 + leg, height - 27, 16 + leg, height - 21, FAINT);
    label(ctx, `${formatted(step)} kpc`, 16, height - 11);
  }
  const points = projected.map(point);
  const pathColor = model ? AMBER : MINT;
  trace(ctx, points.slice(cursor), pathColor + "56", 1.3, [4, 4]);
  trace(ctx, points.slice(0, cursor + 1), pathColor + "a9", 2);
  const stepDots = Math.max(1, Math.ceil(points.length / (miniature ? 25 : 66)));
  for (let i = 0; i < points.length; i += stepDots) {
    circle(ctx, ...points[i], 1.6, i <= cursor ? pathColor + "c7" : pathColor + "66");
  }
  if (marker >= 0 && points[marker]) {
    circle(ctx, ...points[marker], 7, AMBER + "a3", false);
  }
  const [x, y] = points[cursor];
  line(ctx, ...origin, x, y, "#d6bdff55");
  halo(ctx, ...origin, miniature ? 4 : 8, PURPLE);
  halo(ctx, x, y, miniature ? 3 : 6, pathColor);
  if (miniature) return;
  label(ctx, "Primary", origin[0] + 12, origin[1] - 12, PURPLE);
  if (x >= 5 && x <= width - 5 && y >= 5 && y <= height - 5) {
    label(ctx, "Secondary", x > width - 79 ? x - 10 : x + 10, y + 12, pathColor, x > width - 79 ? "right" : "left");
  } else {
    label(ctx, "Secondary outside zoomed view", width - 11, 19, MINT, "right");
  }
  const velocity = project(frames[cursor].velocity, yaw, pitch).slice(0, 2);
  const visibleSpeed = norm(velocity);
  if (visibleSpeed > 0.1) {
    const arrow = Math.min(72, visibleSpeed / 35);
    const dx = velocity[0] * arrow / visibleSpeed;
    const dy = -velocity[1] * arrow / visibleSpeed;
    trace(ctx, [[x, y], [x + dx, y + dy]], AMBER, 1.5);
    const theta = Math.atan2(dy, dx);
    for (const tip of [-0.5, 0.5]) {
      line(ctx, x + dx, y + dy, x + dx - 7 * Math.cos(theta + tip), y + dy - 7 * Math.sin(theta + tip), AMBER, 1.5);
    }
  }
}

export function drawSeries(canvas, frames, cursor, eventIndex) {
  const surface = setup(canvas);
  if (!surface || !frames.length) return;
  const { ctx, width, height } = surface;
  const left = 58, right = width - 59, top = 28, bottom = height - 36;
  const start = frames[0].t, duration = Math.max(1e-5, frames.at(-1).t - start);
  const distances = frames.map(({ position }) => norm(position));
  const speeds = frames.map(({ velocity }) => norm(velocity));
  const max = [distances, speeds].map(values => Math.max(1, ...values) * 1.1);
  const x = (t) => left + (t - start) / duration * (right - left);
  const y = (v, i) => bottom - v / max[i] * (bottom - top);
  label(ctx, "kpc", left, 13, MINT, "right");
  label(ctx, "km/s", right, 13, AMBER);
  for (let i = 0; i <= 4; i++) {
    const fraction = i / 4;
    const yy = bottom - fraction * (bottom - top);
    line(ctx, left, yy, right, yy, GRID);
    label(ctx, formatted(fraction * max[0]), left - 6, yy, MINT, "right");
    label(ctx, formatted(fraction * max[1]), right + 7, yy, AMBER);
  }
  for (let i = 0; i <= 4; i++) {
    const t = start + i * duration / 4;
    line(ctx, x(t), top, x(t), bottom, GRID + "6e");
    label(ctx, formatted(t, duration > 30 ? 0 : 2), x(t), bottom + 11, FAINT, "center");
  }
  label(ctx, eventIndex?.unit || "Gyr", (left + right) / 2, height - 8, FAINT, "center");
  if (eventIndex?.index >= 0 && frames[eventIndex.index]) {
    const xx = x(frames[eventIndex.index].t);
    ctx.setLineDash([3, 4]);
    line(ctx, xx, top, xx, bottom, AMBER + "9a");
    ctx.setLineDash([]);
  }
  trace(ctx, frames.map(({ t }, i) => [x(t), y(distances[i], 0)]), MINT, 1.9);
  trace(ctx, frames.map(({ t }, i) => [x(t), y(speeds[i], 1)]), AMBER, 1.9);
  const xx = x(frames[cursor].t);
  line(ctx, xx, top, xx, bottom, "#ffffff83");
  circle(ctx, xx, y(distances[cursor], 0), 4, MINT);
  circle(ctx, xx, y(speeds[cursor], 1), 4, AMBER);
}

const palette = [
  [17, 19, 33], [36, 26, 59], [81, 50, 106],
  [150, 57, 109], [216, 94, 88], [252, 158, 106], [255, 233, 177],
];
export const RADIO_MAX = 18;
const lookup = Array.from({ length: 256 }, (_, i) => {
  const index = Math.min(palette.length - 1.00001, i / 255 * (palette.length - 1));
  const low = Math.floor(index);
  return palette[low].map((v, j) => Math.round(v + (palette[low + 1][j] - v) * (index - low)));
});
const colorRange = Math.asinh(RADIO_MAX / 0.35);
const heatmaps = new WeakMap();

function radioHeatmap(values, side) {
  if (heatmaps.has(values)) return heatmaps.get(values);
  const tile = document.createElement("canvas");
  tile.width = side;
  tile.height = side;
  const ctx = tile.getContext("2d");
  const image = ctx.createImageData(side, side);
  for (let y = 0; y < side; y++) {
    for (let x = 0; x < side; x++) {
      const v = values[(side - 1 - y) * side + x];
      const t = Math.asinh(Math.max(0, Math.min(RADIO_MAX, v)) / 0.35) / colorRange;
      const rgb = Number.isFinite(v) ? lookup[Math.round(t * 255)] : [8, 10, 16];
      image.data.set([...rgb, 255], (y * side + x) * 4);
    }
  }
  ctx.putImageData(image, 0, 0);
  heatmaps.set(values, tile);
  return tile;
}

export function drawRadio(canvas, cutout, measurement, radius, channel, miniature = false) {
  const surface = setup(canvas);
  if (!surface) return;
  const { ctx, width, height } = surface;
  const { side } = cutout;
  const zoom = Math.max(width, height) / side;
  const left = (width - side * zoom) / 2, top = (height - side * zoom) / 2;
  const tile = radioHeatmap(channel ? cutout.after : cutout.before, side);
  ctx.imageSmoothingEnabled = true;
  ctx.drawImage(tile, left, top, side * zoom, side * zoom);
  const at = ([x, y]) => [left + (x + 0.5) * zoom, top + (side - 0.5 - y) * zoom];
  const [cx, cy] = at(cutout.center);
  ctx.setLineDash([4, 4]);
  circle(ctx, cx, cy, radius * zoom, "#efe9fcbb", false);
  ctx.setLineDash([]);
  if (miniature) return;
  if (measurement?.center) {
    ctx.fillStyle = "#ffdcaf56";
    for (const index of measurement.selected) {
      const [x, y] = at([index % side, Math.floor(index / side)]);
      ctx.fillRect(x - zoom / 2, y - zoom / 2, zoom, zoom);
    }
  }
  circle(ctx, cx, cy, 5, "#12141c");
  circle(ctx, cx, cy, 4, MINT, false);
  if (measurement?.center) {
    const [x, y] = at(measurement.center);
    const ink = "#1a1522";
    line(ctx, x - 7, y, x + 7, y, ink, 4);
    line(ctx, x, y - 7, x, y + 7, ink, 4);
    line(ctx, x - 6, y, x + 6, y, AMBER, 1.6);
    line(ctx, x, y - 6, x, y + 6, AMBER, 1.6);
  }
}

export function drawRadioCurve(canvas, readings) {
  const surface = setup(canvas);
  if (!surface) return;
  const { ctx, width, height } = surface;
  const finite = readings.filter(({ delta }) => Number.isFinite(delta));
  if (!finite.length) return;
  const left = 59, right = width - 35, top = 18, bottom = height - 36;
  const range = Math.max(25, ...finite.map(({ delta }) => Math.abs(delta))) * 1.12;
  const x = (r) => left + 12 + (r - 300) / 300 * (right - left - 24);
  const y = (v) => (top + bottom) / 2 - (bottom - top) * v / (2 * range);
  for (const value of [-range, -range / 2, 0, range / 2, range]) {
    line(ctx, left, y(value), right, y(value), value === 0 ? "#776e89" : GRID);
    label(ctx, formatted(value), left - 7, y(value), FAINT, "right");
  }
  for (const r of [300, 450, 600]) {
    line(ctx, x(r), top, x(r), bottom, GRID);
    label(ctx, `${r} kpc`, x(r), bottom + 15, FAINT, "center");
  }
  trace(ctx, finite.map(({ radius, delta }) => [x(radius), y(delta)]), AMBER, 1.8);
  for (const { radius, delta, cursor } of finite) {
    circle(ctx, x(radius), y(delta), cursor ? 5.5 : 4, cursor ? MINT : AMBER);
    if (cursor) circle(ctx, x(radius), y(delta), 8, MINT + "80", false);
  }
}
