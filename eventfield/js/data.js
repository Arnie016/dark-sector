const base = new URL("../data/local/", import.meta.url);
const requests = new Map();

export function dataUrl(path) {
  return new URL(path, base);
}

function fetchLocal(path, type) {
  if (!requests.has(path)) {
    const request = fetch(dataUrl(path)).then(response => {
      if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
      return response[type]();
    }).catch(error => {
      requests.delete(path);
      throw error;
    });
    requests.set(path, request);
  }
  return requests.get(path);
}

export const getCatalog = () => fetchLocal("catalog.json", "json");

export async function getEvent(row) {
  const catalog = await getCatalog();
  if (!Number.isInteger(row) || !catalog.events[row]) throw new Error("Catalog row is out of range.");
  const shard = await fetchLocal(`tracks/${Math.floor(row / catalog.chunkSize)}.json`, "json");
  const record = Object.fromEntries(catalog.eventColumns.map((key, i) => [key, catalog.events[row][i]]));
  const frames = shard[row].map(([snapshot, x, y, z, vx, vy, vz, m1, m2]) => {
    const [, redshift, t] = catalog.snapshots[snapshot - 30];
    return { snapshot, redshift, t, position: [x, y, z], velocity: [vx, vy, vz], m1, m2 };
  });
  return { record, frames };
}

const littleEndian = new Uint8Array(new Uint32Array([1]).buffer)[0] === 1;

export function decodeCutout(bytes, side) {
  const count = side ** 2;
  if (bytes.byteLength !== count * 8) throw new Error("Unexpected radio cutout size.");
  const view = new DataView(bytes);
  const values = littleEndian ? new Float32Array(bytes) :
    Float32Array.from({ length: count * 2 }, (_, i) => view.getFloat32(i * 4, true));
  return { before: values.subarray(0, count), after: values.subarray(count) };
}

export async function getRadio(id) {
  if (!["macs", "g181", "g099"].includes(id)) throw new Error("Unknown radio field.");
  const metadata = await fetchLocal(`radio/${id}.json`, "json");
  const cutouts = await Promise.all(metadata.cutouts.map(async cut => {
    const buffer = await fetchLocal(`radio/${cut.file}`, "arrayBuffer");
    return { ...cut, ...decodeCutout(buffer, cut.side) };
  }));
  return { ...metadata, cutouts };
}
