# C-32 | Baryons tighten the area-mean SIDM scattering ceiling

**2026-11-21 | DERIVED from TNG-Cluster CDM simulation catalog data | no SIDM inference.**

## Question and comparison

C-31 bounded one-pass scattering through a sphere of radius r500, using **total** mass M500 even though baryons are not dark-matter scattering targets. Does subtracting catalogued gas and a guaranteed central stellar component materially tighten that ceiling? The conventional explanation is the baryonic mass budget, not any additional DM force. Stop without a local dark-matter density profile or actual merger trajectories.

**Source:** [Official TNG-Cluster 352-halo z=0 text catalog](https://www.tng-project.org/files/TNG-Cluster_Catalog.txt) (updated 2025-03-06). Fields 1, 2, 4, 6, 8, 11: origID, haloID, log M500/Msun, r500 Mpc, log Mstar100kpc/Msun, fgas_r500. [TNG team clarification](https://www.tng-project.org/data/forum/topic/1020/gas-fraction-in-tng-cluster/) (2025-10-23) verifies fgas=Mgas(<r500)/M500. [Nelson et al. 2024](https://doi.org/10.1051/0004-6361/202348608) is peer reviewed. [Lee et al. TNGC-SIDM I](https://arxiv.org/abs/2610.18957) (submitted 2026-10-13, preprint) uses two **different** matched mergers, not these eleven CDM halos.

## Physics and finite-domain assumption

Mstar100 is central stellar mass within 100 pkpc. Assuming this central aperture lies entirely inside r500,

`M_DM(<r500) <= M500*(1 - fgas_r500) - Mstar100`.

Stars outside 100 pkpc and other non-DM mass are **not** subtracted. This is therefore a mass **upper** bound, not a DM-mass measurement. For test particles with impact parameters uniformly distributed over the disk of radius r500, constant kappa=(sigma/m)=1 cm²/g and independent Poisson collisions through an r500-**truncated** stationary DM target sphere, Jensen's inequality gives

`<P>_area <= 1-exp[-kappa*(M500*(1-fgas)-Mstar100)/(pi*r500^2)]`.

It is **not** a bound on any individual core chord, bound orbit or realistic merger history; no self-consistent SIDM evolution was simulated.

## Eleven selected real simulated catalog entries and calculated conditional ceilings

| origID | haloID | logM500 | r500 (Mpc) | fgas | logMstar100 | C-31 total ceiling % | C-32 upper ceiling % |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 15.13 | 1.711 | .145 | 12.76 | 3.017 | 2.572 |
| 14 | 2507618 | 15.17 | 1.774 | .151 | 12.64 | 3.076 | 2.609 |
| 19 | 3135769 | 14.97 | 1.515 | .152 | 12.63 | 2.667 | 2.254 |
| 20 | 3238091 | 14.94 | 1.489 | .146 | 12.62 | 2.578 | 2.193 |
| 24 | 3656685 | 14.92 | 1.462 | .146 | 12.76 | 2.554 | 2.167 |
| 28 | 4054274 | 14.99 | 1.547 | .142 | 12.47 | 2.678 | 2.294 |
| 34 | 4561713 | 14.98 | 1.531 | .140 | 12.41 | 2.672 | 2.295 |
| 37 | 4854863 | 14.98 | 1.536 | .148 | 12.71 | 2.655 | 2.252 |
| 38 | 4959833 | 15.02 | 1.577 | .141 | 12.66 | 2.760 | 2.364 |
| 39 | 5059214 | 14.92 | 1.458 | .143 | 12.61 | 2.568 | 2.192 |
| 46 | 5524229 | 14.95 | 1.492 | .143 | 13.00 | 2.626 | 2.226 |

**Result:** Baryon-corrected ceiling 2.167–2.609%, median 2.254% versus total-mass 2.554–3.076%, median 2.667%. Median paired reduction 0.396 percentage points. These eleven previously selected strong cool cores are **not a random sample** of 352 clusters, and no prevalence or significance is inferred.

**Worked example, original ID 34:** Gas 14.0% and central stars at least 0.269% of M500, giving M_DM/M500 <=85.731%. Total-mass column 0.027084305 g/cm² becomes DM-column ceiling 0.023219604 g/cm². Conditional P ceiling changes 2.672% to **2.295%**, or 2.3245% under maximally conservative independent source-number rounding. This rounding test is not a statistical error bar.

## Verification and stop rule

One deterministic Python 3 standard-library calculation `timeout 20s python3 c32_baryon_column.py`, exit **0**, measured wall **0.814446 s**, seed none. It checked all 11 C-31 IDs, masses and radii, finite-domain fractions and monotonicity. Local script SHA-256 `b6a580badcf6b6e1bc3b61a8d9c9270c8a03e52f3b50edab0d7e2dc9c51998e3`; six-field manual source CSV SHA-256 `f79cee92db352ca135ad9391e7f008cab4c8e70937f535184780b5182552c523`; raw JSON SHA-256 `bdeb87bb9a056b7fd675a30594091eb0ef23a6bcc7085bfab88522a4befd40ce`. Local execution files were preserved for the user; not represented as uploaded to GitHub.

Full catalog direct download failed local DNS, although text was available via a web viewer. Private Azure unavailable. SIMULATION-DERIVED inputs, mathematical DERIVED ceilings, **DATA_INSUFFICIENT** for real SIDM rates and cross sections. Source original halo IDs are **not** merger-catalog identifiers. 2026-06-26 Mhistory_vel correction irrelevant to today's mass-only calculation.

**Next discriminating test:** Matched CDM/SIDM dark-matter density and velocity profiles on one independently verified merger history, with declared trajectories. Repeated global ceilings cannot identify heat transport or drag. C-03 unscreened gravity FAILED; C-20 selection correction FAILED; C-23 velocity group effect UNIDENTIFIABLE. No outreach or publication outside the approved repository. Learning introduced; understanding NOT_ASSESSED.
