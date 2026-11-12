# C-20: Snapshot standardization does not repair fingerprint-selection bias

**Date:** 2026-11-09 (Asia/Singapore)  
**Statuses:** DERIVED / SIMULATION_RESULT / DATA_INSUFFICIENT  
**Scope:** finite, selected **TNG-Cluster simulation-derived** event table; not observed velocities, independent halos, SIDM signals, or evidence of new physics.

## Question and stopping rule

Would reweighting the 1,475 merger events with valid final-snapshot phase-space fingerprints by four pre-existing collision-snapshot bins recover the mean velocity-estimator discrepancy among all 1,977 collision-quality events? The predeclared operational tolerance was an absolute residual no greater than **5 km/s**. This is a pipeline sanity threshold, not physical precision, a confidence interval, or a test of dark matter.

The strongest conventional explanation is selection: fingerprint validity requires an eligible snapshot-99 trajectory record, whereas historical merger events can be represented with -1 after merger completion. Collision epoch and other merger/measurement characteristics can therefore be related to eligibility. Further, potential-center positional derivatives and mass-weighted SubhaloVel are different estimators, not a known truth and a noisy measurement.

## Provenance

Read through the GitHub connector from [PR #14](https://github.com/Arnie016/dark-sector/pull/14), pinned at branch head `514745cd67934c4991a92e4f05ef3ca66c6188d0` **before this note was created**.

- `research/merger-collision-ensemble/collision-comparison.csv`, Git blob SHA-1 `95200eb824b9a93f3a7ba80bf9ae9306e1249e5a`, 1,977 unique event rows. The upstream production script checks the TNG merger HDF5 SHA-256 `d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d`; **the HDF5 was not reopened in C-20**.
- `research/trajectory-grouping-audit/grouping.csv`, Git blob SHA-1 `2d4fa2f4545bf5c8475b5356e32bebbc9d0b34fa`, 1,530 eligible event rows by *provisional* snapshot-99 fingerprint.
- Intersection: 1,475 event rows; the other 502 collision-quality events have no eligible fingerprint. The 55 grouped-only records do not have a velocity-discrepancy result in the collision-quality table.
- C-20 execution: one deterministic JavaScript calculation, return status 0, measured tool-side elapsed time 443 ms including GitHub reads; no RNG, paid resources, GPU or local HDF5 access. It verified total and unique IDs, finite nonnegative outcome values and cohort intersection before calculation.

The official TNG documentation describes 2,083 cluster-merger catalog events and the snapshot 30–99 trajectories, including -1 entries after completed mergers; `Mhistory_vel` is in km/s and was officially corrected on 2026-06-26. See [catalog documentation](https://www.tng-project.org/data/cluster/) and [2026 changelog](https://www.tng-project.org/data/forum/topic/2/changes-and-additions/). The 2024 peer-reviewed radio-relic methods context is [Lee et al., A&A 2024](https://doi.org/10.1051/0004-6361/202348194).

## Fixed-bin calculation

Let `Y_i` be the nonnegative norm of the difference between the two velocity estimators, in km/s. Let `R_i=1` if event `i` has an eligible snapshot-99 fingerprint. Let `b` be one of the already-defined collision-snapshot bins 30–49, 50–69, 70–84 or 85–98. With `N_b` all collision-quality rows in bin `b`, the *snapshot-standardized complete-case* mean is

```math
\hat\mu_{\rm std}=\sum_b (N_b/N)\,\overline{Y}_{b,R=1}.
```

It recovers the full-table mean only when the observed subset's conditional outcome mean is representative **within** each bin. The full-table mean is directly available in this diagnostic because the velocity outcome was calculated even when the endpoint fingerprint was not.

| Collision snapshot | N | Fingerprint eligible | Eligible mean [km/s] | Ineligible mean [km/s] | Weight N / eligible |
|---|---:|---:|---:|---:|---:|
| 30–49 | 135 | 22 | 412.079 | 606.435 | 6.136 |
| 50–69 | 684 | 366 | 404.981 | 623.324 | 1.869 |
| 70–84 | 568 | 504 | 431.109 | 719.322 | 1.127 |
| 85–98 | 590 | 583 | 503.241 | 720.089 | 1.012 |

**Calculated results:**

- Mean over all 1,977 selected collision-quality events: **498.624 km/s**.
- Complete-case fingerprint-eligible mean: **452.853 km/s**, residual **−45.771 km/s** relative to the full table.
- Four-bin snapshot-standardized eligible mean: **442.296 km/s**, residual **−56.327 km/s** relative to the full table. **Fails** the stated 5 km/s tolerance.
- Ineligible-event mean: **633.110 km/s**.

The snapshot-bin reweighting not only fails to repair the discrepancy, it **increases its magnitude** (45.8 to 56.3 km/s) in this finite sample. Eligibility is associated with the outcome within each broad bin, so using bin alone as a missing-at-random adjustment is unsupported for this outcome and cohort. The largest 30–49 inverse-eligibility weight is 6.14, another warning about representation. These are finite-table differences, **not statistical significance values**.

## Reproduction outline

At the pinned parent commit, load the two listed CSVs. Require unique `row` and `event_row` keys. Intersect by integer event ID. Compute arithmetic means of `discrepancy_km_s` over all and eligible records. For each pre-existing bin, compute `N_b/N` and its eligible-only outcome mean, then sum these products. Reject missing, negative or non-finite outcomes. **Do not** infer physical descendant identity from exact phase-space fingerprints. No random seed is needed.

## Interpretation and next decision

This is a **failed selection adjustment**, not an independent reanalysis of raw simulations, a validation of the position-derived velocity, or evidence for SIDM. Already-published TNG-Cluster conventional CDM simulations and merger-physics modeling can produce complex shock/radio structure. The 2024 Lee et al. paper reports that additional mergers complicate radio-relic appearance. Before an SIDM comparison: verify true event-to-descendant membership, clarify missingness pathways, use matched physical velocity estimators, reproduce a collisionless benchmark, and split held-out tests by independent zoom halo/initial condition, not event rows or snapshots. No astrophysical selection function or covariance was recovered here. The globally unscreened C-03 gravity model remains FAILED.

**One discriminating next test:** recompute the discrepancy from independently verified same-tracer orbital measurements for host-grouped events, with a selection model trained on measured covariates rather than the collision-snapshot bin alone. A physical SIDM interpretation remains DATA_INSUFFICIENT.
