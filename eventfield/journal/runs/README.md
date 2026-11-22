# Frontier physics run notes

Each research run can add one versioned journal entry. Use a unique UTC ID in the form `YYYYMMDDthhmmssz-task-slug`. The `date` field is the run’s date in Singapore.

The atlas reads entries from this directory on `research/cadence-control-20261107` in `Arnie016/dark-sector`. Each file is named exactly `<id>.json`. The journal checks new notes when opened, and Refresh checks again. Older run notes are available in batches. The named branch is the existing draft research branch in a public repository. Include shareable results and sources only.

## One entry per run

- Give the result first. Use one of `measurement`, `literature`, `proposal`, `negative`, `blocked` or `no-change` for `status`.
- Point to primary sources and input versions. Give the units and an equation when it changes the interpretation.
- Record what the verifier did, the observed verdict, and a link or command someone else can use. If a calculation was blocked, record the failed prerequisite in the check.
- Put one next discriminating test in `next`. If a data source matters, record what it adds, its access, expected size or size unknown, and the smallest useful product.
- Use your existing authorized connection to write the new file. If a hosted run lacks write access, include the JSON in its own output for the journal’s import form. The local form stores the entry in the current browser.

## Format

This is an example object for the schema.

```json
{
  "version": 1,
  "id": "20261122t010000z-dark-sector",
  "date": "2026-11-22",
  "scope": "Dark sector",
  "status": "blocked",
  "title": "The matched calibration rows are still needed",
  "summary": "The catalog describes halo orbits. The baseline fit also needs matched 3D relic centers.",
  "sections": [
    {"heading": "What was checked", "body": ["State the actual source listing, input version and result here."]}
  ],
  "checks": [
    {"title": "Calibration table access", "result": "State the observed access result here."}
  ],
  "sources": [
    {"label": "Lee et al. double-relic calibration", "url": "https://arxiv.org/html/2510.21632"}
  ],
  "next": "Locate the candidate table with snapshot IDs, R500c and measurement definitions."
}
```

Checks can add `url` and `command`. A command is published as a reproducibility recipe. The site renders it as text.

Use `node eventfield/scripts/check_journal.mjs /path/to/entry.json` to validate one entry, or run it without an argument to check the journal sources in the checkout.

## Task prompt addition

> After every run, add one short Eventfield journal entry, including runs with a negative result, blocker or no change. Preserve the current research remit and its approval gates. State the question, actual result, primary sources, material units or equation, the verifier and evidence, and one next test. Include one high-value bounded dataset lead when the evidence supports it. Use the version 1 format above. Give the file a unique UTC run ID and use the Singapore run date for the timeline. If your existing GitHub permission allows it, add one shareable JSON file to this directory on the existing draft research branch. If the write is unavailable or requires approval, include the JSON object in the task’s own output with the actual delivery status. Keep credentials, private paths, contact details and restricted data in their original locations.
