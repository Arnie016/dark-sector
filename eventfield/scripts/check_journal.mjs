import assert from "node:assert/strict";
import { readFile, readdir } from "node:fs/promises";
import { basename } from "node:path";
import { clockFit, projectionExample, clockSensitivityMyr } from "../js/clock.js";
import { verifyJournalEntry, runId } from "../js/journal-format.js";

const base = new URL("../journal/", import.meta.url);
const json = async (file) => JSON.parse(await readFile(file, "utf8"));
const close = (a, b) => assert(Math.abs(a - b) < 1e-6);
if (process.argv[2]) {
  const post = verifyJournalEntry(await json(process.argv[2]));
  assert(runId.test(post.id), "Expected a timestamped run ID");
  console.log(`Valid journal run: ${post.id}`);
} else {
  const ids = await json(new URL("index.json", base));
  assert.equal(new Set(ids).size, ids.length);
  for (const id of ids) {
    const post = verifyJournalEntry(await json(new URL(`entries/${id}.json`, base)));
    assert.equal(post.id, id);
  }
  const files = (await readdir(new URL("runs/", base))).filter(file => file.endsWith(".json"));
  for (const file of files) {
    const post = verifyJournalEntry(await json(new URL(`runs/${file}`, base)));
    assert(runId.test(post.id));
    assert.equal(post.id, basename(file, ".json"));
  }
  close(clockFit(2.4), 1.008);
  close(projectionExample(30).shiftMyr, -167.2002960770);
  close(projectionExample(0).shiftMyr, 0);
  assert.equal(projectionExample(75).projectedReading, null);
  close(clockSensitivityMyr(-270.584433, 1000), -140.70390516);
  console.log(`Valid journal: ${ids.length} reference entries, ${files.length} run notes, clock arithmetic checked.`);
}
