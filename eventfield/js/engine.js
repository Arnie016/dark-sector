const DEG = Math.PI / 180;
const KPC_PER_MYR_PER_KM_S = 0.001022712165;
const G = 4.30091727e-6 * KPC_PER_MYR_PER_KM_S ** 2;

export const norm = (v) => Math.hypot(...v);
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const scale = (v, amount) => v.map((x) => x * amount);
const add = (a, b) => a.map((x, i) => x + b[i]);

export function project(v, yaw, pitch) {
  const a = yaw * DEG;
  const b = pitch * DEG;
  const right = [Math.cos(a), Math.sin(a), 0];
  const up = [-Math.sin(a) * Math.sin(b), Math.cos(a) * Math.sin(b), Math.cos(b)];
  const depth = [Math.sin(a) * Math.cos(b), -Math.cos(a) * Math.cos(b), Math.sin(b)];
  return [dot(v, right), dot(v, up), dot(v, depth)];
}

export function integrateOrbit(seed, { massScale, epsilon, sideways }) {
  let r = [...seed.position];
  const initialV = scale(seed.velocity, KPC_PER_MYR_PER_KM_S);
  const radius = norm(r);
  const radial = radius ? scale(r, dot(initialV, r) / radius ** 2) : [0, 0, 0];
  const tangent = add(initialV, scale(radial, -1));
  let v = add(radial, scale(tangent, sideways));
  const mu = G * seed.mass * massScale;
  const softenedRadius = (pos) => Math.hypot(...pos, epsilon);
  const accel = (pos) => scale(pos, -mu / softenedRadius(pos) ** 3);
  const potential = (pos) => -mu / softenedRadius(pos);
  const energy = (pos, vel) => 0.5 * norm(vel) ** 2 + potential(pos);
  const initialEnergy = energy(r, v);
  const normalization = 0.5 * norm(v) ** 2 - potential(r);
  let residual = 0;
  let min = { radius, t: 0 };
  let a = accel(r);
  const frames = [];
  // Kick-drift-kick velocity Verlet with a fixed one-Myr step.
  for (let t = 0; t <= 1800; t++) {
    const distance = norm(r);
    if (distance < min.radius) min = { radius: distance, t };
    residual = Math.max(residual, Math.abs(energy(r, v) - initialEnergy) / normalization);
    if (t % 15 === 0) {
      frames.push({ t, position: r, velocity: scale(v, 1 / KPC_PER_MYR_PER_KM_S) });
    }
    if (t === 1800) break;
    const half = add(v, scale(a, 0.5));
    r = add(r, half);
    a = accel(r);
    v = add(half, scale(a, 0.5));
  }
  return { frames, min, residual };
}

function pixelToDirection(x, y, wcs) {
  const dx = x - wcs.refPixel[0];
  const dy = y - wcs.refPixel[1];
  const east = (wcs.cd[0][0] * dx + wcs.cd[0][1] * dy) * DEG;
  const north = (wcs.cd[1][0] * dx + wcs.cd[1][1] * dy) * DEG;
  const depth = wcs.type === "SIN" ? Math.sqrt(1 - east ** 2 - north ** 2) : 1;
  const [ra, dec] = wcs.refWorld.map((v) => v * DEG);
  const localEast = [-Math.sin(ra), Math.cos(ra), 0];
  const localNorth = [-Math.cos(ra) * Math.sin(dec), -Math.sin(ra) * Math.sin(dec), Math.cos(dec)];
  const center = [Math.cos(ra) * Math.cos(dec), Math.sin(ra) * Math.cos(dec), Math.sin(dec)];
  return add(add(scale(localEast, east), scale(localNorth, north)), scale(center, depth));
}

function angularDistance(a, b) {
  const cross = [
    a[1] * b[2] - a[2] * b[1],
    a[2] * b[0] - a[0] * b[2],
    a[0] * b[1] - a[1] * b[0],
  ];
  return Math.atan2(norm(cross), dot(a, b)) / DEG * 3600;
}

function brightestCenter(cutout, radius, threshold, fraction) {
  const { side, center, before, after } = cutout;
  const eligible = [[], []];
  let disk = 0;
  let common = 0;
  for (let y = Math.max(0, Math.ceil(center[1] - radius)); y < Math.min(side, center[1] + radius + 1); y++) {
    for (let x = Math.max(0, Math.ceil(center[0] - radius)); x < Math.min(side, center[0] + radius + 1); x++) {
      if ((x - center[0]) ** 2 + (y - center[1]) ** 2 > radius ** 2) continue;
      disk++;
      const index = y * side + x;
      if (!Number.isFinite(before[index]) || !Number.isFinite(after[index])) continue;
      common++;
      if (before[index] > threshold) eligible[0].push(index);
      if (after[index] > threshold) eligible[1].push(index);
    }
  }
  return eligible.map((list, i) => {
    const coverage = disk ? common / disk : 0;
    if (coverage < 0.99 || list.length < 10) return { eligible: list.length, coverage, center: null };
    const image = i === 0 ? before : after;
    list.sort((a, b) => image[a] - image[b]);
    const selected = list.slice(-Math.ceil(list.length * fraction));
    let weight = 0;
    let sx = 0;
    let sy = 0;
    for (const index of selected) {
      const flux = image[index];
      sx += flux * (index % side);
      sy += flux * Math.floor(index / side);
      weight += flux;
    }
    return { eligible: list.length, selected, coverage, center: [sx / weight, sy / weight] };
  });
}

export function measureRadio(field, radius, threshold, fraction = 0.10) {
  const radiusPixels = radius / (field.kpcArcsec * field.pixelArcsec);
  const points = field.cutouts.map((cutout) => brightestCenter(cutout, radiusPixels, threshold, fraction));
  const separations = [0, 1].map((i) => {
    if (points.some((item) => !item[i].center)) return null;
    const directions = points.map((pair, j) => {
      const [x, y] = pair[i].center;
      const [ox, oy] = field.cutouts[j].origin;
      return pixelToDirection(x + ox, y + oy, field.wcs);
    });
    return angularDistance(...directions) * field.kpcArcsec;
  });
  const delta = separations.every(Number.isFinite) ? separations[0] - separations[1] : null;
  return { points, separations, delta, radiusPixels };
}
