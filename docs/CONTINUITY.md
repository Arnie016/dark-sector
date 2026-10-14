# Continuity without schedule changes

The existing daily morning **Asia/Singapore** research schedule is outside this repository. No schedule, prompt, account setting, or automation was edited in this setup. Its execution state and exact cadence were not inspected; the preservation claim means no scheduler mutation occurred.

Automatic export from the existing morning chat to this repository is **not verified**. Do not infer continuous GitHub updates from the existence of a schedule or this documentation.

## After a morning run

1. Retrieve only the relevant memo/artifacts. Inspect existing work and preserve unrelated changes.
2. Create a dated branch, such as `research/YYYY-MM-DD-topic`.
3. Use the [checkpoint template](../research/templates/checkpoint.md). Distinguish external claims, recovered reports, derived math, simulations, and locally verified results.
4. Save permitted inputs, code, dependency versions, seeds, numerical output, and hashes. Keep private/raw files out of Git unless separately authorized.
5. Update stable hypothesis IDs, learning state, and research status. Record null/failure outcomes.
6. Run the narrow verifier, inspect rendered Markdown, and open a PR with proof and blockers. Merge is an owner/reviewer decision.

This procedure enables versioned updates without adding a second scheduler. Connecting automated delivery would require inspecting the actual scheduler/export mechanism and recording a successful end-to-end receipt; that integration is not claimed complete here.
