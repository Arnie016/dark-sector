export const journalStatuses = {
  measurement: "Measurement",
  literature: "Paper review",
  proposal: "Study design",
  negative: "Negative result",
  blocked: "Blocked",
  "no-change": "No change",
};

export const journalId = /^[a-z0-9][a-z0-9-]{2,95}$/;
export const runId = /^\d{8}t\d{6}z-[a-z0-9][a-z0-9-]{2,60}$/;
const text = (value, limit) => typeof value === "string" && value.trim().length > 0 && value.length <= limit;
const list = (value, limit, test) => Array.isArray(value) && value.length > 0 && value.length <= limit && value.every(test);

function publicUrl(value) {
  if (!text(value, 850)) return false;
  try {
    const url = new URL(value);
    return url.protocol === "https:" && !url.username && !url.password;
  } catch {
    return false;
  }
}

function date(value) {
  if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const parsed = new Date(value);
  return Number.isFinite(parsed.valueOf()) && parsed.toISOString().slice(0, 10) === value;
}

export function verifyJournalEntry(post) {
  if (!post || post.version !== 1 || !text(post.id, 96) || !journalId.test(post.id) || !date(post.date)) {
    throw new TypeError("Use version 1, a valid entry ID and a YYYY-MM-DD date.");
  }
  if (!Object.hasOwn(journalStatuses, post.status) || !text(post.scope, 75) ||
      !text(post.title, 130) || !text(post.summary, 700) || !text(post.next, 650)) {
    throw new TypeError("Supply a title, summary, research scope, status and next test.");
  }
  if (!list(post.sections, 8, section => section && text(section.heading, 90) &&
        list(section.body, 6, paragraph => text(paragraph, 1500)))) {
    throw new TypeError("Supply sections with a heading and one or more paragraphs.");
  }
  if (!list(post.checks, 12, check => check && text(check.title, 140) && text(check.result, 1000) &&
        (check.command === undefined || text(check.command, 400)) &&
        (check.url === undefined || publicUrl(check.url)))) {
    throw new TypeError("Record a check and observed outcome. Evidence links use HTTPS.");
  }
  if (!Array.isArray(post.sources) || post.sources.length > 15 ||
      !post.sources.every(s => s && text(s.label, 150) && publicUrl(s.url))) {
    throw new TypeError("Supply a list of labeled HTTPS sources.");
  }
  if (post.action !== undefined && (!post.action || !text(post.action.label, 70) ||
      !text(post.action.href, 240) || !/^#(?:atlas|data|orbit|radio|desk|journal)(?:\?[\w&=%+.-]+)?$/.test(post.action.href))) {
    throw new TypeError("An atlas action must link to a supported in-site route.");
  }
  return post;
}
