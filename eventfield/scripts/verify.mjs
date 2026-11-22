import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { decodeCutout } from "../js/data.js";
import { integrateOrbit, measureRadio, norm, project } from "../js/engine.js";
import { search } from "../js/evidence.js";
import { parseMeasurement } from "../js/measurement-questions.js";

const base = new URL("../data/local/", import.meta.url);
const local = (path) => readFile(new URL(path, base));
const json = async (path) => JSON.parse(await local(path));
const catalog = await json("catalog.json");
assert.equal(catalog.events.length, 2083);
assert.deepEqual(catalog.fields.find(field => field.name === "Mhistory_vel").shape, [2083, 70, 6]);

let totalFrames = 0;
let eventFive;
for (let start = 0; start < catalog.events.length; start += catalog.chunkSize) {
  const shard = await json(`tracks/${start / catalog.chunkSize}.json`);
  for (const [key, frames] of Object.entries(shard)) {
    const row = Number(key);
    if (row === 5) eventFive = frames;
    assert.equal(frames.length, catalog.events[row].at(-1));
    totalFrames += frames.length;
    for (let i = 0; i < frames.length; i++) {
      const [snap] = frames[i];
      assert(snap >= 30 && snap <= 99 && (!i || snap > frames[i - 1][0]));
      assert(frames[i].slice(1, 7).every(Number.isFinite));
    }
  }
}
assert.equal(totalFrames, 133751);
const { baseline } = catalog;
const snapshot = eventFive.find(row => row[0] === baseline.Snap_coll);
assert(Math.abs(norm(snapshot.slice(1, 4)) - baseline.snapshot_collision_separation_proper_kpc) < 0.001);
assert(Math.abs(norm(snapshot.slice(4, 7)) - baseline.snapshot_collision_relative_speed_km_s) < 0.001);
for (const angles of [[0, 0], [0, 90], [35, 55]]) {
  const v = snapshot.slice(4, 7);
  assert(Math.abs(norm(v) - norm(project(v, ...angles))) < 1e-8);
}
const sample = eventFive.find(row => row[0] === 66);
const seed = { position: sample.slice(1, 4), velocity: sample.slice(4, 7), mass: (sample[7] + sample[8]) * 1e14 };
const params = { massScale: 1, epsilon: 150, sideways: 1 };
const orbit = integrateOrbit(seed, params);
assert.equal(orbit.frames.length, 121);
assert(orbit.residual < 0.005);
assert.notEqual(orbit.min.radius, integrateOrbit(seed, { ...params, sideways: 1.6 }).min.radius);

let checks = 0;
let maxError = 0;
for (const [key, targets] of Object.entries(await json("radio/validation.json"))) {
  const field = await json(`radio/${key}.json`);
  for (const cutout of field.cutouts) {
    const buffer = await local(`radio/${cutout.file}`);
    const bytes = buffer.buffer.slice(buffer.byteOffset, buffer.byteOffset + buffer.byteLength);
    Object.assign(cutout, decodeCutout(bytes, cutout.side));
  }
  for (const [radius, threshold, expected] of targets) {
    const observed = measureRadio(field, radius, threshold).delta;
    assert(Number.isFinite(observed));
    maxError = Math.max(maxError, Math.abs(observed - expected));
    checks++;
  }
}
assert.equal(checks, 27);
assert(maxError < 0.002);
assert.equal(search("What does weak lensing measure?")[0]?.id, "lensing");
assert.equal(search("can radio relics tell time since collision?")[0]?.id, "clock");
assert.equal(search("penguin cooking recipe").length, 0);
assert.deepEqual(parseMeasurement("Measure Abell 1925 at 450 kpc and 0.225 mJy"), { kind: "radio", id: "g099", radius: 450, threshold: 0.225 });
assert.deepEqual(parseMeasurement("How fast is row 5 at snapshot 70?"), { kind: "orbit", row: 5, snapshot: 70 });
console.log(`Verified ${catalog.events.length.toLocaleString()} events, ${totalFrames.toLocaleString()} frames, the gravity model, and ${checks} radio cases (max difference ${maxError.toExponential(2)} kpc).`);
