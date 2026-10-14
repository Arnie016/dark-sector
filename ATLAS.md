# Atlas | choose a trail through the physics

**New to the subject?** Start with the physical question. **Auditing a result?** Start with the claim and run record.

| Trail | Question | Key observable | Primary challenge |
|---|---|---|---|
| **1. Dark halos** | Do dark-matter particles exchange heat through self-interactions? | Halo density profiles; image-position and flux perturbations | Merger history, baryons, host lens model |
| **2. Ultra-low-energy scattering** | Can electrons or lattice vibrations reveal light dark matter? | Time/energy-resolved event rates | Real material response, cryogenic backgrounds, uneven exposure |
| **3. Cosmic origins** | Was structure suppressed at birth or altered during evolution? | Scale-dependent clustering and redshift evolution | Initial-condition/late-time degeneracy |
| **4. Neutrino sky** | Do apparent disappearances come from propagation or missing source associations? | Energy, direction, event categories, detector responses | Flux/population/background identifiability |

## The template for every scientific chapter

**At a glance:** question · why it matters · smallest falsifiable claim · verdict and confidence boundaries.

**Physics:** relevant scales (with units), one worked derivation, limiting cases and the competing explanation.

**Evidence:** primary citations with exact version dates and data overlaps; observed inputs distinguished from assumptions.

**Methods:** runnable code, dependency versions, seeds, hashes and unit tests when executed; exact CLI and hardware/runtime footprint.

**Results:** figures labeled by provenance and honest nulls. *No experimental run? State that explicitly.*

**Next gate:** what measurement or calculation would overturn the interpretation.

## Interpretation rules

- `DERIVED` means the stated mathematical result follows from identified assumptions. It does **not** imply a measured physical effect.
- `SIMULATION_RESULT` is generated from declared truth. Always label axes, units and generating process.
- `BASELINE_REPRODUCED` requires actual source data plus a recorded execution matching an independently specified baseline.
- `UNIDENTIFIABLE` means the proposed observations cannot distinguish at least two specified models under explicit assumptions.
- `DATA_INSUFFICIENT` is a useful conclusion. Missing covariance or exposure masks are not invitation to invent them.

Use GitHub History and pull requests to see how a claim was corrected. Later revisions must **retain the failure and why the conclusion changed**.
