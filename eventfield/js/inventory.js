import { byId, number, setText } from "./dom.js";
import { getHostCatalog } from "./data.js";

const tng = "https://www.tng-project.org/data/cluster/";
const products = [
  ["Cluster Mergers", "In the atlas", "Positions, peculiar velocities, masses and passage flags for 2,083 events. Open any row and replay the two-halo history.", "#orbit", "Browse trajectories"],
  ["Cluster properties", "In the archive", "A separate z = 0 HDF5 has masses, radii, cooling, magnetic fields, stellar content and projected offsets for 352 targets. IDs need a verified crosswalk to join histories.", tng, "Official catalog"],
  ["LoTSS-DR2 radio maps", "In the atlas", "Three observed cluster fields with paired FITS maps. The wide viewer uses native-resolution data and can switch to the matched beam to measure separation.", "#radio", "Open the radio sky"],
  ["Gas, X-ray and radio gallery", "In the atlas", "The illustrated z = 0 target is halo 0. Atlas projections show rendered emission or column density from three directions.", "#atlas", "Open the gallery"],
  ["Numerical cluster projections", "Listed by TNG", "Files around 16 GB each combine targets and sightlines for quantities such as gas column density, X-ray and SZ. Confirm one useful field of view and epoch first.", tng, "Projection specs"],
  ["Particle snapshots and trees", "Listed by TNG", "The larger release has gas cells, dark matter, stars, black holes, halo catalogs and histories. Use the smallest valid cutout and verify coverage before joining.", "https://www.tng-project.org/data/docs/api/", "Cutout documentation"],
  ["Clock calibration sample", "Needed for replication", "The Lee et al. fit used 3D relic centers across selected snapshots. Seek the matched event list, exclusions, R500c values and original measurement definition.", "https://arxiv.org/html/2510.21632", "Read the calibration paper"],
  ["Matched dark-matter models", "Watch the release", "TNGC-SIDM I describes CDM/SIDM comparisons and a planned public suite. Start with matched IDs and identical sightlines to test any separation difference.", "https://arxiv.org/html/2610.18957", "Read the availability statement"],
];

function item(tag, className, value) {
  const el = document.createElement(tag);
  el.className = className;
  el.textContent = value;
  return el;
}

export function wireInventory() {
  const container = byId("data-inventory");
  for (const [title, label, caption, href, action] of products) {
    const card = item("article", "panel inventory-card", "");
    const proof = item("span", "kind " + (label === "In the atlas" ? "observation" : "literature"), label);
    const go = item("a", "plain-link", action + " ↗");
    go.href = href;
    if (!href.startsWith("#")) {
      go.target = "_blank";
      go.rel = "noopener";
    }
    card.append(proof, item("h2", "", title), item("p", "", caption), go);
    container.append(card);
  }
  getHostCatalog().then(host => {
    setText("host-caption", `${number(host.halos.length)} unique host IDs · ${number(host.fields.length)} datasets · ${number(host.bytes)} bytes`);
    byId("host-hash").append("SHA-256 ", item("code", "", host.sha256));
    for (const field of host.fields) {
      const row = item("li", "", "");
      row.append(item("code", "", field));
      byId("host-fields").append(row);
    }
  }).catch(() => {
    setText("host-caption", "Rebuild the local cache with the archived cluster properties file to inspect it here.");
  });
}
