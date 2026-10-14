# Setup verification receipt

**14 October 2026 · checked at 12:27 Singapore time (04:27 UTC)**

## Outcome

Evidence-linked research foundation prepared on `research/repository-foundation`. The only direct main-branch change was a minimal initialization README so an empty repository could support a PR. Research content remains reviewable on the branch.

## Numeric proof

- Clean virtual environment: Python 3.14.8, NumPy 2.4.3, matching `requirements.txt`.
- `python -m unittest discover -s tests -v`: **9 tests passed**.
- `python experiments/ratio_closure/run.py --check`: **passed**, including input/code/dependency hashes and numeric comparison to committed output.
- A changed central ratio and invalid flux inputs are rejected by the verifier/tests.
- No spectral fit, telescope event fit, SIDM population likelihood, or external baseline reproduction ran.
- Python 3.11–3.13 and other machines have not been tested. The declared lower Python version is a compatibility target, not proof of a cross-version test matrix.

## Documentation and render

Internal file links checked with no missing targets; whitespace check passed. GitHub rendered the banner and equation. README inspected at desktop width 1440 and phone width 390. The crowded three-column overview was replaced with lane paragraphs; the remaining navigation table is shorter and readable. The primary “Run the audit” link opened the correct guide; browser Back returned to the README.

Copy presents published ratios, historical toy runs, and new local calculations distinctly. Original artwork has descriptive alt text and a conceptual-data boundary. No motion is used. Human comprehension remains **`NOT_TESTED`**; screenshot inspection is an agent review, not human acceptance.

Two browser automation retries were needed: a screenshot met a changing page, and a link selector matched two links. A stable screenshot and an exact link label resolved them. GitHub initially blocked a push for author-email privacy; the local commits were amended to the account's public GitHub noreply identity before publication. No email setting changed.

## Continuity and cost

- Morning Singapore scheduler: **no tool or file mutation**. No extra scheduler or workflow was created.
- Morning-to-GitHub automatic delivery: **not verified**.
- Planned scope: 20–30 minutes, estimated 12–20k tokens, external spend $0.
- Actual elapsed: full intake was not timed; the measured checkout-to-render portion was 8.5 minutes at the timestamp above. This excludes earlier retrieval and later PR handoff.
- Actual tokens and model cost: not surfaced. External paid-service spend: $0. Local dependency download used no paid compute.
- Impact: **`IMPROVED :)`** for organization and independently executable algebra; no increase in physical discovery evidence claimed.
- Nearest blocker: joint observed flux/lens posterior and missing original archives.
- Next safe action: review this foundation, then recover permitted joint samples or original archives with provenance before extending inference.
