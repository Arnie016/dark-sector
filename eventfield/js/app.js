import { byId, choose, number, setText } from "./dom.js";
import { dataUrl, getCatalog, getEvent, getRadio } from "./data.js";
import { drawOrbit, drawRadio } from "./charts.js";
import { measureRadio } from "./engine.js";
import { loadOrbit, stopOrbit, wireOrbit } from "./orbit.js";
import { loadRadio, wireRadio } from "./radio.js";
import { renderAnswer, search, topics } from "./evidence.js";
import { wireCatalog } from "./catalog.js";
import { answerMeasurement, parseMeasurement } from "./measurement-questions.js";

const atlas = {
  band: "gas",
  views: {
    gas: ["Gas column density", "nelson23", "A bright central cluster surrounded by diffuse filaments."],
    xray: ["X-ray emission · 0.5–5 keV", "nelson23xray", "Bright X-ray emission traces the densest hot gas."],
    radio: ["Simulated radio · 1.4 GHz", "lee23", "Radio synchrotron structures surround the simulated galaxy cluster."],
  },
  preview: null,
  radio: null,
};
let active = null;
let questionVersion = 0;

function gallery() {
  const axis = byId("gallery-axis").value;
  const [label, source, info] = atlas.views[atlas.band];
  choose("gallery-mode", "band", atlas.band);
  setText("hero-view-label", `${axis}-axis · z = 0`);
  setText("hero-band-label", label);
  byId("gallery-source").href = `https://www.tng-project.org/cluster/gallery/${source}/`;
  const render = byId("hero-render");
  render.alt = `TNG-Cluster halo 0, ${label.toLowerCase()}, viewed along the ${axis}-axis. ${info}`;
  render.src = dataUrl(`gallery/${atlas.band}_${axis}.png`);
}

function paintPreviews() {
  if (active !== "atlas") return;
  if (atlas.preview) {
    const { frames, record } = atlas.preview;
    const index = Math.max(0, frames.findIndex(frame => frame.snapshot === record.collision));
    drawOrbit(byId("atlas-track"), frames, index, { yaw: 65, pitch: 40, zoom: 2.3, model: false }, index, true);
  }
  if (atlas.radio) {
    const result = measureRadio(atlas.radio, 600, 0.2);
    drawRadio(byId("atlas-radio"), atlas.radio.cutouts[1], result.points[1][0], result.radiusPixels, 0, true);
  }
}

function describeCatalog(catalog) {
  setText("atlas-count", number(catalog.events.length));
  byId("event-number").max = catalog.events.length - 1;
  const details = byId("catalog-file");
  const digest = document.createElement("code");
  digest.textContent = catalog.sha256;
  details.replaceChildren(
    `${number(catalog.size)} bytes. ${number(catalog.targets)} primary halo IDs appear in this release. SHA-256 `, digest,
  );
  const nodes = catalog.fields.map(({ name, shape, dtype }) => {
    const li = document.createElement("li");
    const key = document.createElement("code");
    key.textContent = name;
    li.append(key, ` · ${shape.map(x => number(x)).join(" × ") || "scalar"} · ${dtype}`);
    return li;
  });
  byId("catalog-fields").replaceChildren(...nodes);
}

async function showDesk(params) {
  const version = ++questionVersion;
  const query = params.get("ask")?.slice(0, 240) ?? "";
  const topic = topics.find(item => item.id === params.get("topic"));
  if (query) {
    byId("query").value = query;
    const calculation = parseMeasurement(query);
    if (calculation) {
      setText("desk-results", "Reading local data for your measurement…");
      try {
        const answer = await answerMeasurement(calculation);
        if (version === questionVersion) renderAnswer(byId("desk-results"), answer);
      } catch {
        if (version === questionVersion) setText("desk-results", "The local files for this measurement could not be read. Open the data guide to prepare the atlas.");
      }
      return;
    }
    const [result, ...related] = search(query);
    renderAnswer(byId("desk-results"), result, related);
    return;
  }
  const result = topic || topics.find(item => item.id === "clock");
  byId("query").value = topic ? result.question : "";
  renderAnswer(byId("desk-results"), result);
}

function route({ focus = false } = {}) {
  const [part, qs] = window.location.hash.slice(1).split("?");
  if (part === "main") return;
  const params = new URLSearchParams(qs);
  const next = ["orbit", "radio", "desk"].includes(part) ? part : "atlas";
  const changed = next !== active;
  if (active === "orbit" && changed) stopOrbit();
  active = next;
  document.querySelectorAll("[data-view]").forEach(view => { view.hidden = view.dataset.view !== active; });
  for (const tab of document.querySelectorAll("[data-nav]")) {
    if (tab.dataset.nav === active) tab.setAttribute("aria-current", "page");
    else tab.removeAttribute("aria-current");
  }
  if (part === "catalog") {
    byId("catalog").scrollIntoView({ block: "start" });
  } else if (changed) {
    window.scrollTo(0, 0);
    if (focus) {
      const heading = byId(`view-${active}`).querySelector("h1");
      heading.tabIndex = -1;
      heading.focus({ preventScroll: true });
    }
  }
  if (active === "orbit") {
    const raw = params.get("event");
    const snap = params.has("snap") ? Number(params.get("snap")) : null;
    loadOrbit(raw === null ? 5 : Number(raw), params.get("mode") === "model" ? "model" : "replay", snap);
  } else if (active === "radio") {
    const id = params.get("field");
    const settings = [
      ["aperture", "radius"], ["threshold", "cut"], ["bright-fraction", "fraction"],
    ];
    for (const [input, key] of settings) {
      if (params.has(key) && Number.isFinite(Number(params.get(key)))) byId(input).value = params.get(key);
    }
    loadRadio(["g181", "macs", "g099"].includes(id) ? id : "g181");
  } else if (active === "desk") {
    showDesk(params);
  } else {
    paintPreviews();
  }
}

function wireDesk() {
  for (const id of ["catalog", "clock", "radio", "lensing", "world", "model"]) {
    const topic = topics.find(item => item.id === id);
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = topic.question;
    button.addEventListener("click", () => {
      const hash = `#desk?topic=${id}`;
      if (location.hash === hash) showDesk(new URLSearchParams(`topic=${id}`));
      else location.hash = hash;
    });
    byId("suggestions").append(button);
  }
  for (const query of ["Measure Abell 1925 at 450 kpc", "How fast is row 5 at snapshot 70?"]) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = query;
    button.addEventListener("click", () => {
      byId("query").value = query;
      byId("search-form").requestSubmit();
    });
    byId("suggestions").append(button);
  }
  byId("search-form").addEventListener("submit", (event) => {
    event.preventDefault();
    const query = byId("query").value.trim();
    if (!query) return;
    const params = new URLSearchParams({ ask: query });
    const hash = `#desk?${params}`;
    if (location.hash === hash) showDesk(params);
    else location.hash = hash;
  });
}

byId("gallery-mode").addEventListener("click", event => {
  const band = event.target.closest("button")?.dataset.band;
  if (!band) return;
  atlas.band = band;
  gallery();
});
byId("gallery-axis").addEventListener("change", gallery);
byId("hero-render").addEventListener("error", () => {
  byId("hero-render").hidden = true;
  byId("hero-empty").hidden = false;
});
byId("hero-render").addEventListener("load", () => {
  byId("hero-render").hidden = false;
  byId("hero-empty").hidden = true;
});

wireOrbit();
wireRadio();
wireDesk();
wireCatalog();
gallery();
route();
window.addEventListener("hashchange", () => route({ focus: true }));
getCatalog().then(describeCatalog).catch(() => {
  setText("catalog-file", "Prepare the atlas data to see the verified file fingerprint and field inventory.");
});
getEvent(5).then(event => { atlas.preview = event; paintPreviews(); }).catch(() => {});
getRadio("g181").then(field => { atlas.radio = field; paintPreviews(); }).catch(() => {});
const observer = new ResizeObserver(paintPreviews);
observer.observe(byId("atlas-track"));
observer.observe(byId("atlas-radio"));
