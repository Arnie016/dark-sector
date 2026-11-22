export const byId = (id) => document.getElementById(id);
export const value = (id) => Number(byId(id).value);
export const setText = (id, text) => { byId(id).textContent = text; };

export const number = (n, digits = 0) => Number.isFinite(n)
  ? n.toLocaleString("en-US", { minimumFractionDigits: digits, maximumFractionDigits: digits })
  : "—";
export const signed = (n, digits = 0) => Number.isFinite(n)
  ? n.toLocaleString("en-US", { minimumFractionDigits: digits, maximumFractionDigits: digits, signDisplay: "exceptZero" }).replace("-", "−")
  : "—";

export function choose(container, key, selected) {
  for (const button of byId(container).querySelectorAll(`[data-${key}]`)) {
    button.setAttribute("aria-pressed", String(button.dataset[key] === String(selected)));
  }
}

export function downloadCsv(name, rows) {
  const url = URL.createObjectURL(new Blob([rows.map(row => row.join(",")).join("\n") + "\n"], { type: "text/csv;charset=utf-8" }));
  const link = document.createElement("a");
  link.download = name;
  link.href = url;
  document.body.append(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
}
