import { getEvent, getRadio } from "./data.js";
import { number, signed } from "./dom.js";
import { measureRadio, norm } from "./engine.js";

export function parseMeasurement(question) {
  const orbit = question.match(/\b(?:row|event)\s*#?\s*(\d+)\b/i);
  const snapshot = question.match(/\bsnap(?:shot)?\s*#?\s*(\d+)\b/i);
  if (orbit && snapshot) return { kind: "orbit", row: Number(orbit[1]), snapshot: Number(snapshot[1]) };

  const field = [
    ["g099", /abell\s*1925|g\s*099/i],
    ["g181", /g\s*181/i],
    ["macs", /macs\s*j?\s*1752/i],
  ].find(([, pattern]) => pattern.test(question));
  const radius = question.match(/\b(\d+(?:\.\d+)?)\s*kpc\b/i);
  const threshold = question.match(/(?:^|\s)(\d*\.?\d+)\s*mjy\b/i);
  if (field && radius) {
    return { kind: "radio", id: field[0], radius: Number(radius[1]), threshold: threshold ? Number(threshold[1]) : 0.20 };
  }
  return null;
}

function note(tag, style, title, passage, refs, scope, action) {
  return { tag, style, title, passages: [[passage, refs]], scope, action };
}

async function orbitAnswer({ row, snapshot }) {
  if (row < 0 || row > 2082 || snapshot < 30 || snapshot > 99) {
    return note("Simulation catalog", "simulation", "Choose a row and snapshot in the catalog range.",
      "Catalog rows run from 0 to 2,082. The stored snapshot range is 30 through 99.", ["catalog"],
      "Row and snapshot are separate indices.", ["Browse the catalog", "#catalog"]);
  }
  const { record, frames } = await getEvent(row);
  const sample = frames.find(frame => frame.snapshot === snapshot);
  if (!sample) {
    const description = frames.length
      ? `Row ${row} has ${frames.length} valid samples between snapshots ${frames[0].snapshot} and ${frames.at(-1).snapshot}.`
      : `Row ${row} has no valid position and velocity pair in this release.`;
    return note("Simulation catalog", "simulation", `Snapshot ${snapshot} is missing from row ${row}.`, description,
      ["catalog"], "Select an available snapshot in the replay.", ["Open the row", `#orbit?event=${row}`]);
  }
  return note("Calculated from catalog", "simulation", `Row ${row}, snapshot ${snapshot}`,
    `The primary and secondary are ${number(norm(sample.position), 2)} proper kpc apart. Their relative peculiar speed is ${number(norm(sample.velocity), 2)} km/s. The snapshot has redshift ${sample.redshift.toFixed(3)}. TNG-Cluster records this event under primary halo ${record.halo}.`,
    ["catalog", "release"], "Calculated from the three-dimensional relative position and velocity vectors. Rotate the view in the orbit lab to measure projected components.",
    ["Open this snapshot", `#orbit?event=${row}&snap=${snapshot}`]);
}

async function radioAnswer({ id, radius, threshold }) {
  const step = (threshold - 0.1) / 0.025;
  if (radius < 300 || radius > 600 || radius % 25 !== 0 || step < -1e-8 || step > 8 + 1e-8 || Math.abs(step - Math.round(step)) > 1e-8) {
    return note("Survey measurement", "observation", "Choose a radius and flux threshold in the lab range.",
      "The radio lab uses radii from 300 to 600 kpc in steps of 25 kpc and flux thresholds from 0.100 to 0.300 mJy/beam in steps of 0.025.",
      ["g181", "g099"], "Example question · Measure Abell 1925 at 450 kpc and 0.200 mJy.", ["Open the radio lab", `#radio?field=${id}`]);
  }
  const field = await getRadio(id);
  const result = measureRadio(field, radius, threshold);
  const name = id === "g099" ? "Abell 1925" : field.cluster;
  const params = new URLSearchParams({ field: id, radius, cut: threshold, fraction: 10 });
  const summary = result.delta === null
    ? "One aperture has too few eligible pixels or too little common image coverage at these settings."
    : `The pair separation is ${number(result.separations[0], 2)} kpc in T50 and ${number(result.separations[1], 2)} kpc in T50SUB. The signed difference is ${signed(result.delta, 2)} kpc.`;
  return note("Calculated from survey pixels", "observation", `${name} at ${radius} kpc`, summary,
    ["lofar", id === "g099" ? "g099" : "g181"],
    `Radio maps use a common nominal 135 kpc beam. This calculation uses the brightest 10% above ${threshold.toFixed(3)} mJy/beam in each aperture.`,
    ["Open this measurement", `#radio?${params}`]);
}

export const answerMeasurement = (request) => request.kind === "orbit" ? orbitAnswer(request) : radioAnswer(request);
