import { byId, setText, number, signed } from "./dom.js";
import { projectionExample } from "./clock.js";
import { journalId, runId, journalStatuses, verifyJournalEntry } from "./journal-format.js";

const REPO = "Arnie016/dark-sector";
const BRANCH = "research/cadence-control-20261107";
const RUNS = "eventfield/journal/runs";
const LIST = `https://api.github.com/repos/${REPO}/contents/${RUNS}?ref=${encodeURIComponent(BRANCH)}`;
const RAW = `https://raw.githubusercontent.com/${REPO}/refs/heads/${BRANCH}/${RUNS}/`;
const STORAGE = "eventfield-journal-entry:";
const formatter = new Intl.DateTimeFormat("en-SG", { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" });
const entries = new Map();
let seeds;
let remoteIds = [];
let batch = 0;
let selected = null;
let pending = false;
let attempted = false;

const node = (tag, className, value) => {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (value !== undefined) el.textContent = value;
  return el;
};

function link(href, title, external = false) {
  const el = node("a", "plain-link", title);
  el.href = href;
  if (external) {
    el.target = "_blank";
    el.rel = "noopener noreferrer";
  }
  return el;
}

async function readJson(url, online = false) {
  const response = await fetch(url, online ? { signal: AbortSignal.timeout(6500), credentials: "omit", cache: "no-store" } : {});
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const body = await response.text();
  if (body.length > 1_000_000) throw new Error("Journal response is too large");
  return JSON.parse(body);
}

function remember(post) {
  const parsed = verifyJournalEntry(post);
  entries.set(parsed.id, parsed);
}

async function loadSeeds() {
  const ids = await readJson(new URL("../journal/index.json", import.meta.url));
  await Promise.all(ids.filter(id => journalId.test(id)).map(async id => {
    remember(await readJson(new URL(`../journal/entries/${id}.json`, import.meta.url)));
  }));
  try {
    for (const key of Object.keys(localStorage).filter(key => key.startsWith(STORAGE))) {
      try { remember(JSON.parse(localStorage.getItem(key))); } catch { /* ignore malformed imports */ }
    }
  } catch { /* site storage is optional */ }
}

function clockDemo() {
  const figure = node("section", "clock-demo");
  figure.append(node("h3", "", "Tilt the line between the relics"));
  const formula = node("div", "clock-formula", "T = (0.52 Gyr) × (d / R₅₀₀c) − 0.24 Gyr");
  figure.append(formula);

  function track(label) {
    const row = node("div", "clock-row");
    const title = node("span", "clock-track-name", label);
    const container = node("div", "clock-track");
    const length = node("span", "clock-length");
    const result = node("span", "clock-value");
    container.setAttribute("aria-hidden", "true");
    container.append(length);
    row.append(title, container, result);
    figure.append(row);
    return { length, result };
  }
  const ground = track("True separation");
  const shadow = track("Projected separation");
  const control = node("div", "clock-control");
  const slider = node("input");
  slider.type = "range";
  slider.id = "clock-tilt";
  slider.min = "0";
  slider.max = "75";
  slider.value = "30";
  const label = node("label", "", "Tilt out of the sky plane");
  label.htmlFor = slider.id;
  const output = node("output", "clock-angle");
  output.setAttribute("for", slider.id);
  const line = node("p", "data-note");
  const result = node("p", "clock-result");
  result.setAttribute("aria-live", "polite");
  const help = node("p", "data-note", "d / R₅₀₀c is the dimensionless ruler. The shadow uses d × cos(tilt). The fit covers ratios 1–3.5.");
  control.append(label, output, slider);
  figure.append(control, result, line, help);

  function update() {
    const angle = Number(slider.value);
    const estimate = projectionExample(angle);
    ground.length.style.width = `${estimate.ratio / 3.5 * 100}%`;
    shadow.length.style.width = `${estimate.projected / 3.5 * 100}%`;
    ground.result.textContent = `${number(estimate.ratio, 2)} R₅₀₀c`;
    shadow.result.textContent = `${number(estimate.projected, 2)} R₅₀₀c`;
    output.value = `${angle}°`;
    slider.setAttribute("aria-valuetext", `${angle} degrees`);
    result.textContent = estimate.shiftMyr === null ? "The projected ratio is outside the fitted interval."
      : `${signed(estimate.shiftMyr)} Myr apparent shift`;
    line.textContent = `True-separation fit ${number(estimate.reference, 3)} Gyr. ` +
      (estimate.projectedReading === null ? "A projected reading requires a ratio of at least 1."
        : `Projected-separation fit ${number(estimate.projectedReading, 3)} Gyr.`);
  }
  slider.addEventListener("input", update);
  update();
  return figure;
}

function renderPost(post) {
  const article = byId("journal-post");
  article.replaceChildren();
  if (!post) {
    article.append(node("p", "data-note", "Choose an available entry from the timeline."));
    return;
  }
  const meta = node("p", "kicker", `${post.scope} · ${journalStatuses[post.status]}`);
  const time = node("time", "journal-date", formatter.format(new Date(post.date)));
  time.dateTime = post.date;
  const title = node("h2", "journal-title", post.title);
  article.append(meta, title, time, node("p", "journal-dek", post.summary));

  for (const [i, section] of post.sections.entries()) {
    const part = node("section", "journal-copy");
    part.append(node("h3", "", section.heading), ...section.body.map(p => node("p", "", p)));
    article.append(part);
    if (i === 1 && post.demo === "relic-clock" && post.id === "relic-clock") article.append(clockDemo());
  }
  const verify = node("section", "journal-proof");
  verify.append(node("h3", "", "Reproduce the result"));
  for (const check of post.checks) {
    const item = node("div", "journal-check");
    item.append(node("strong", "", check.title), node("p", "", check.result));
    if (check.command) {
      const pre = node("pre");
      pre.append(node("code", "", check.command));
      item.append(pre);
    }
    if (check.url) item.append(link(check.url, "Open the evidence ↗", true));
    verify.append(item);
  }
  const next = node("section", "journal-next");
  next.append(node("h3", "", "What to test next"), node("p", "", post.next));
  if (post.action) next.append(link(post.action.href, post.action.label + " ↗"));
  article.append(verify, next);
  if (post.sources.length) {
    const sources = node("section", "journal-references");
    const list = node("ol");
    for (const source of post.sources) {
      const row = node("li");
      row.append(link(source.url, source.label, true));
      list.append(row);
    }
    sources.append(node("h3", "", "Sources"), list);
    article.append(sources);
  }
}

function showTimeline() {
  const sorted = [...entries.values()].sort((a, b) => {
    const day = b.date.localeCompare(a.date);
    const rank = (post) => runId.test(post.id) ? post.id : "";
    return day || rank(b).localeCompare(rank(a));
  });
  const showing = selected ? entries.get(selected) : sorted[0];
  const timeline = byId("journal-timeline");
  timeline.replaceChildren(...sorted.map(post => {
    const item = node("li");
    const route = link(`#journal?post=${post.id}`, "");
    route.className = "timeline-item";
    if (post.id === showing?.id) route.setAttribute("aria-current", "page");
    route.append(
      node("span", "timeline-date", formatter.format(new Date(post.date))),
      node("strong", "", post.title),
      node("span", "timeline-status", journalStatuses[post.status]),
    );
    item.append(route);
    return item;
  }));
  const article = byId("journal-post");
  if (article.dataset.rendered !== (showing?.id ?? "")) {
    article.dataset.rendered = showing?.id ?? "";
    renderPost(showing);
  }
}

async function loadRuns(reset = false) {
  if (pending) return;
  pending = true;
  attempted = true;
  const more = byId("journal-more");
  byId("journal-refresh").disabled = true;
  more.disabled = true;
  try {
    if (reset) {
      const files = await readJson(LIST, true);
      remoteIds = files.filter(item => item.type === "file" && item.name.endsWith(".json"))
        .map(item => item.name.slice(0, -5)).filter(id => runId.test(id)).sort().reverse();
      batch = 0;
    }
    const next = remoteIds.slice(batch, batch + 12);
    if (selected && !entries.has(selected) && remoteIds.includes(selected) && !next.includes(selected)) next.push(selected);
    const pulls = await Promise.allSettled(next.filter(id => !entries.has(id)).map(async id => {
      const post = await readJson(RAW + id + ".json", true);
      if (post.id !== id) throw new Error("Run ID differs from filename");
      remember(post);
    }));
    batch = Math.min(batch + 12, remoteIds.length);
    more.hidden = batch >= remoteIds.length;
    const failed = pulls.filter(result => result.status === "rejected").length;
    setText("journal-sync-status", failed ? `${failed} run file(s) could not be read. Refresh to retry.` :
      remoteIds.length ? "GitHub run notes up to date." : "Waiting for the first scheduled run note.");
  } catch {
    setText("journal-sync-status", "Showing saved entries. GitHub is currently unavailable.");
  } finally {
    pending = false;
    byId("journal-refresh").disabled = false;
    more.disabled = false;
    showTimeline();
  }
}

export async function showJournal(id) {
  selected = id && journalId.test(id) ? id : null;
  try {
    seeds ??= loadSeeds();
    await seeds;
    showTimeline();
    if (!attempted || (selected && runId.test(selected) && !entries.has(selected))) loadRuns(true);
  } catch {
    seeds = null;
    setText("journal-sync-status", "The saved journal could not be read. Reload to try again.");
  }
}

export function wireJournal() {
  byId("journal-refresh").addEventListener("click", () => loadRuns(true));
  byId("journal-more").addEventListener("click", () => loadRuns());
  byId("journal-import-form").addEventListener("submit", event => {
    event.preventDefault();
    const field = byId("journal-import-input");
    try {
      const raw = field.value.trim();
      const post = verifyJournalEntry(JSON.parse(raw));
      if (!runId.test(post.id)) throw new TypeError("Use the scheduled run’s timestamped ID.");
      const known = entries.get(post.id);
      if (known && JSON.stringify(known) !== JSON.stringify(post)) throw new TypeError("An entry already uses this run ID.");
      localStorage.setItem(STORAGE + post.id, JSON.stringify(post));
      remember(post);
      field.value = "";
      setText("journal-import-status", "Saved on this browser.");
      location.hash = `#journal?post=${post.id}`;
      showTimeline();
    } catch (error) {
      setText("journal-import-status", error instanceof SyntaxError ? "Paste one complete JSON entry." : error.message);
    }
  });
}
