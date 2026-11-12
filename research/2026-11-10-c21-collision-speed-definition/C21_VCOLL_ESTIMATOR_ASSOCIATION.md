# C-21: Collision-speed definition split and orbit-estimator discrepancy

**Date:** 2026-11-10 (Asia/Singapore)  
**Statuses:** SIMULATION_RESULT / DERIVED / DATA_INSUFFICIENT  
**Scope:** selected rows from TNG-Cluster **CDM simulation-derived** merger catalog, not observed cluster data or a SIDM constraint.

## Predeclared question and stopping rule

Do merger events where catalog first-pericenter `V_coll` differs from the instantaneous relative `Mhistory_vel` speed at `Snap_coll` also have a larger discrepancy between position-derived and `Mhistory_vel` relative velocities?

The strongest conventional explanation is **definition/cadence and estimator mismatch**, not exotic dark matter. `V_coll` is defined as a maximum velocity at the first pericenter, whereas `Snap_coll` is the nearest snapshot **after** first pericenter. The orbit finite-difference estimates motion of potential minima; `SubhaloVel` is a mass-weighted member velocity. Both diagnostics use the same `Mhistory_vel` source and therefore are **not independent tests**.

A threshold of `0.1 km/s` for catalog-speed agreement was fixed in the preceding collision-ensemble audit. For this bounded descriptive check, an absolute between-stratum mean discrepancy >50 km/s and an absolute median within-label mean difference >50 km/s were operational flags for a follow-up nuisance-control study, **not significance criteria**. Stop once these finite-table summaries and validation checks are completed.

## Source and reproduction boundary

- Selected source: [collision-comparison.csv](https://github.com/Arnie016/dark-sector/blob/533c705dd291301dac17878509b15a200dd4b4f3/research/merger-collision-ensemble/collision-comparison.csv), Git blob SHA-1 `95200eb824b9a93f3a7ba80bf9ae9306e1249e5a`, 1,977 rows.
- Input-producing script: [analyze.py](https://github.com/Arnie016/dark-sector/blob/533c705dd291301dac17878509b15a200dd4b4f3/research/merger-collision-ensemble/analyze.py), Git blob `2cbd4674af6cf87fe8d8e95c10a553b355f60d64`. Its input guard expects TNG merger HDF5 SHA-256 `d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d`. **This run did not reopen the HDF5.**
- Official [TNG merger field definitions](https://www.tng-project.org/data/cluster/), notably `Snap_coll`, `V_coll`, `Mhistory_vel`; [26 June 2026 correction](https://www.tng-project.org/data/forum/topic/2/changes-and-additions/) to `Mhistory_vel`.
- Literature context: [Lee et al. 2024](https://doi.org/10.1051/0004-6361/202348194), *A&A* 686 A55, published 29 May 2024, models complex collision geometry and radio-relic shocks in TNG-Cluster. No paper's observational or simulated results were reproduced.

Data were fetched through the connected GitHub file reader on 2026-11-10. A single deterministic JavaScript calculation parsed CSV columns by exact name, checked 1,977 unique row IDs, finite columns, nonnegative outcomes and `abs(catalog_speed_km_s-v_coll_km_s)` against the stored absolute difference (tolerance `1e-7 km/s`). No seed or external physical worker was used. Exit/return status SUCCESS; elapsed connector-fetch-plus-calculation wall time **869 ms**. No Azure access, paid compute, API credential, GPU or bulk download.

## Physical quantities and method

Let `v_snap = |v_secondary(Snap_coll)-v_main(Snap_coll)|` in km/s, read from corrected `Mhistory_vel`; let `v_peak=V_coll`. Define the *speed-definition mismatch* `A=|v_peak-v_snap|` (km/s), and the *orbit-estimator mismatch* `B=|v_center,finite_difference - (v_secondary-v_main)|` (km/s). Note `B` is a **3D vector norm**, while `A` is a **speed difference**. They are not interchangeable.

Two pre-existing strata: `A<0.1 km/s` and `A>=0.1 km/s`. Across the 337 stored `HaloID` labels, construct a second, conditional comparison using only labels with at least two records in each stratum. Report the median over labels of the difference in **within-label arithmetic means**, high-A minus low-A. Label identity is unverified against SubLink/FoF descendants and is **not** independently established host identity. Event rows share halos, so no iid confidence intervals or significance claims.

## Results: TNG simulation-derived catalog, not observations

| Quantity | `A<0.1 km/s` | `A>=0.1 km/s` |
|---|---:|---:|
| Event rows | 1,020 | 957 |
| Median `A` [km/s] | 0.00005148 | 140.8353 |
| Median `B` [km/s] | 357.1221 | 479.6459 |
| Mean `B` [km/s] | 418.3218 | 584.2118 |

Event-level high-minus-low difference in means: **+165.8900 km/s**. Event-level difference in medians: **+122.5238 km/s**.

Among **162 recorded labels** with at least two events in each stratum, the median high-minus-low *within-label mean* difference was **+68.3313 km/s**; 101/162 (62.35%) were positive. Median within-label difference of medians was +75.8625 km/s. The two predeclared >50 km/s descriptive flags were met.

These results are associations conditional on catalog selection. The labels are not demonstrably independent zoom histories; `A` and `B` share the same relative velocity; merger phase, collision speed, halo mass and sampling cadence may drive both. In particular, even 101/162 positive signs do not establish a significant population effect or independent replication.

## Interpretation and decision

The two diagnostics are **not redundant numeric copies**: the group with a collision-speed-definition mismatch >=0.1 km/s has larger position-versus-member-velocity discrepancies in this selected simulated catalog, including under the within-label descriptive control. This is a **pipeline diagnostic**, not evidence of SIDM, a velocity error or a confirmed causal relationship.

An independent discriminator requires a version-pinned same-particle or same-centroid velocity estimator sampled at the same times, a verified event-to-descendant map and ideally different initial-condition zooms. When building halo-aware validation, **never join merger `HaloIDs` to z=0 properties `haloID` by numeric equality** without a verified mapping. Existing C-20 snapshot-only standardization remains FAILED, C-03 globally unscreened gravity remains FAILED, and no physical SIDM likelihood exists here.

**Next experiment:** Use a matched-tracer velocity at the same three snapshots on one physically verified merger, then re-evaluate `B` after controlling measurement conventions. A failure to reduce it would motivate closer study of orbit integration/branch continuity, not an immediate new-force claim.
