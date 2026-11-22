import { getCatalog } from "./data.js";
import { byId, number, setText } from "./dom.js";

const PAGE_SIZE = 10;
let catalog = null;
let page = 0;

function paint() {
  if (!catalog) return;
  const raw = byId("browser-filter").value.trim();
  const sort = byId("browser-sort").value;
  const rows = catalog.filter(row => !raw || [row.row, row.halo, row.main, row.secondary].some(id => String(id) === raw));
  if (sort !== "row") rows.sort((a, b) => (b[sort] ?? -Infinity) - (a[sort] ?? -Infinity) || a.row - b.row);
  const start = page * PAGE_SIZE;
  const end = Math.min(start + PAGE_SIZE, rows.length);
  const pageRows = rows.slice(start, end);
  byId("browser-table").hidden = rows.length === 0;
  byId("browser-prev").disabled = page === 0;
  byId("browser-next").disabled = end >= rows.length;
  setText("browser-status", rows.length
    ? `Showing ${number(start + 1)}–${number(end)} of ${number(rows.length)} matching events`
    : "No matching event or halo ID. Clear the search to view the whole catalog.");
  const nodes = pageRows.map(row => {
    const tr = document.createElement("tr");
    for (const value of [row.row, row.halo, number(row.ratio, 3), number(row.speed), row.frames]) {
      const td = document.createElement("td");
      td.textContent = value;
      tr.append(td);
    }
    const td = document.createElement("td");
    const link = document.createElement("a");
    link.href = `#orbit?event=${row.row}`;
    link.className = "plain-link";
    link.textContent = "Replay ↗";
    link.setAttribute("aria-label", `Replay row ${row.row}`);
    td.append(link);
    tr.append(td);
    return tr;
  });
  byId("browser-rows").replaceChildren(...nodes);
}

export function wireCatalog() {
  const modal = byId("event-browser");
  for (const opener of document.querySelectorAll("[data-browse-events]")) {
    opener.addEventListener("click", async () => {
      modal.showModal();
      if (catalog) return paint();
      setText("browser-status", "Loading the catalog…");
      byId("browser-prev").disabled = true;
      byId("browser-next").disabled = true;
      try {
        const data = await getCatalog();
        catalog = data.events.map(row => Object.fromEntries(data.eventColumns.map((key, i) => [key, row[i]])))
          .filter(row => row.frames > 0);
        paint();
      } catch {
        setText("browser-status", "Prepare the local atlas data to browse the catalog.");
      }
    });
  }
  for (const [key, event] of [["browser-filter", "input"], ["browser-sort", "change"]]) {
    byId(key).addEventListener(event, () => { page = 0; paint(); });
  }
  byId("browser-prev").addEventListener("click", () => { page--; paint(); });
  byId("browser-next").addEventListener("click", () => { page++; paint(); });
  byId("browser-rows").addEventListener("click", event => {
    if (event.target.closest("a")) modal.close();
  });
}
