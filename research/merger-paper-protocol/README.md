# Research protocol: robustness of a radio-relic merger clock

**State: INELIGIBLE_RESEARCH_NOTE_ONLY.** This is a prospective study design and reproducibility checkpoint, not a finished paper, preregistration, discovery, self-interacting-dark-matter constraint, or validation of published results. The frozen question below is a proposed scope; its feasibility depends on inputs not yet available. The physics-paper eligibility workflow requires source-complete evidence, a decisive result, controls, independent verification, known figure uncertainty and a bibliography before manuscript promotion. This note does not claim those gates are met.

## Question and claim boundary

For simulations with independently verified merger-event identities and measured radio relics, how do explicitly defined relic detection and position rules change the error of a published time-since-collision calibration on **held-out clusters**? The target is a sensitivity study for a measurement pipeline, not a claim that a catalog is erroneous, that existing work is invalid, or that self-interacting dark matter has been detected. A null result—no practically meaningful change over prespecified, justified perturbations—would be publishable only if the data, controls, uncertainty and novelty support it.

## What is already known

- [Lee et al. (2026)](https://arxiv.org/html/2510.21632) already fit a double-relic separation clock and examine projection, geometry, luminosity selection and merger complexity. They use 3D emissivity-weighted centers. The basic claim that double relics can trace merger age is therefore not novel.
- [Jee et al. (2026)](https://arxiv.org/html/2605.00093) already model an observational gold sample with masses, shock and lensing separations, phase and geometry priors. Their SIDM constraint belongs to their forward model. We have not reproduced its likelihood or tested how our catalog diagnostics affect it.
- [TNGC-SIDM I](https://arxiv.org/html/2610.18957) tests two cosmological cluster mergers; its data availability section says publication-related data are on request and a wider release is planned. Two cases do not establish a population selection function. Ask the user before any request email.
- [Nuza et al.](https://arxiv.org/html/2409.09422) model total shock radio power in The Three Hundred simulation as a function of phase and aperture. Our [formula evaluation](../three-hundred-radio-benchmark/README.md) uses published parameters only; it is not a relic detection model and cannot be substituted for individual TNG radio measurements.

## Current evidence and its limits

- The [corrected TNG-Cluster merger catalog](https://www.tng-project.org/data/cluster/) is locally pinned by SHA-256 `d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d`. Its 2,083 rows include repeated events and cannot be treated as independent clusters. The exact `d_peri` construction and event-to-present-day cluster mapping are unresolved. Our [collision-time association](../collision-time-quantization/README.md) is exploratory and does not demonstrate an error or a clock bias.
- The [PSZ2 observational case](../psz2-multiwavelength/README.md) combines a processed LOFAR map, Chandra image and published weak-lensing peak positions; the latter are coordinates, not a lensing map. A [centroid-shift check](../psz2-centroid-shift/README.md) agrees approximately with a published central number but lacks the original masks and counts-based uncertainty model. The [radio mask sensitivity test](../psz2-radio-region-sensitivity/README.md) uses artificial catalog-seeded circles and arbitrary cuts. Neither validates the simulation calibration.
- The [official radio-gallery and source audit](../relic-clock-source-audit/README.md) links previously archived present-day radio, gas and X-ray views to the source papers. They are rendered images, not the row-level 2026 relic sample or calibrated shock maps; they cannot reproduce the clock.
- The [observational sample transcription](../relic-gold-sample-data-check/README.md) contains selected published summaries, not underlying joint likelihoods, a random population sample, or independent data for the TNG calibration.

## Proposed analysis once inputs exist

1. **Freeze provenance and linkage.** Pin versions, hashes, cosmology, units, event definitions and sample-selection code. Verify each event's host and main branch with authoritative merger trees and match shock/relic entries and snapshot IDs. Audit selection and missingness before outcomes are inspected. Do not group clusters by unverified recorded labels.
2. **Reproduce a baseline.** Use the authors' data and code, or an explicitly documented independent implementation, to recover the published clock's fit and residual statistic within prespecified tolerances. The cited relation is TSC = 0.52 d/R500c − 0.24 Gyr over d/R500c 1–3.5, but exact reproduction requires the original selected data, fitting choices and uncertainty definitions. A formula evaluation alone is not baseline reproduction.
3. **Hold out at cluster level.** Before model fitting, assign entire independently identified clusters—including all events, snapshots and lines of sight—to either development or holdout sets; prevent duplicate progenitors, repeated viewpoints and related zooms from crossing the split. Record random seed, assignment and exclusions. Do not infer independent sample counts from event rows.
4. **Run one perturbation at a time.** On identical held-out systems, compare the source-defined reference pipeline with documented position definitions, viewing directions and survey-like brightness/noise/beam masks. Treat failures to detect or pair both relics explicitly as selection outcomes. Do not use the Three Hundred aggregate luminosity curves as detection probabilities. Only compare `d_peri` or alternate timing definitions once units and construction are source-verified.
5. **Measure impact and uncertainty.** Report cluster-level coverage/detection fraction, signed bias, median absolute error and interval coverage in prespecified separation/mass/phase bins, including sample sizes and excluded cases. Use cluster-level resampling or a hierarchical model, with the exact estimator and uncertainty chosen and frozen after inspecting input structure but before outcomes; account for within-cluster correlations. No significance test is valid before the matching and selection model exist.
6. **Compare observation cautiously.** PSZ2 is a case study with different radius, redshift and radio-center conventions, not an independent validation sample. Use source-level radio and weak-lensing likelihoods, masks, astrometry and covariance before making a quantitative comparison. SIDM inference requires the separate matched SIDM data and model, not ordinary TNG CDM alone.

## Reproducibility checkpoint

`replay.py` runs four existing calculations in a temporary workspace: the published The Three Hundred formula, the Chandra centroid-shift check, the artificial radio-region sensitivity test, and the catalog collision-time diagnostic. It verifies expected numerical summaries and each source script's pinned input hashes. This is an integrated **computational regression check**, not an independent scientific replication, an author-code reproduction, or a release-ready manuscript.

```sh
python research/merger-paper-protocol/replay.py \
  --mergers /path/cluster_mergers.hdf5 \
  --radio /path/PSZ2G181.06+48.47T50kpcSUB.fits \
  --chandra /path/PSZ2G181.06+48.47CHANDRA.fits \
  --catalog /path/rrsamp.tsv
```

Requires Python, NumPy, SciPy, Astropy, h5py and matplotlib. Existing source manifests identify the official inputs; the private Azure archive has the observational files and merger catalog. The helper does not download data or use credentials. Source-script warnings and caveats remain authoritative. The current user has not approved any email or paper submission.

## Decisions and missing evidence

The most direct path is to obtain the TNG credential through the existing secret helper and trace a small set of event descendants, and obtain the published shock/relic catalog, source code or documented equivalents for the same selected systems. The key was unavailable in the latest local presence check; no secret was printed. The authors' data/code availability must be checked rather than assumed. The existing question to the authors remains unsent. Original LOFAR masks, Chandra source/background inputs, and observational covariance are additional gaps. The user's per-email approval is required; no contact, Overleaf project, or journal submission is claimed.
