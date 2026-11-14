# C-25 | Cool core does not guarantee X-ray/SZ peak co-location

**Dated:** 2026-11-14 (Singapore). **Claim C25-CC-TRACER-COLOCATION:** DERIVED geometry; SIMULATION_RESULT using published TNG-Cluster z=0 catalog values; population rate DATA_INSUFFICIENT. **Not an observational measurement, dark-matter signal, SIDM constraint, or novelty claim.**

## Question and stopping criterion

**Question.** Does a **strong cool core** (central cooling time < 1 Gyr) guarantee that the projected X-ray and thermal Sunyaev–Zeldovich (SZ) brightness peaks are within **0.05 r500** of one another for all three orthogonal projections?

**Strongest ordinary explanation for a counterexample:** X-ray emission weights the square of electron density and a temperature-dependent emissivity; SZ measures line-of-sight electron pressure. Gas dynamics, AGN feedback, projection and image peak finders can thus select different features. This is not a measurement of lensing dark-matter displacement.

**Stopping criterion:** One strong cool-core halo with a **rounding-conservative geometry-only lower bound** greater than 0.05 r500 in an individual matched projection is enough to reject the *universal proxy*. The 0.05 threshold is an exploratory diagnostic, not a detector-resolution or observed-data uncertainty model.

## Primary data, methods, dates and prior art

- Official [TNG-Cluster public properties catalog](https://www.tng-project.org/files/TNG-Cluster_Catalog.txt), public 352-target z=0 table last updated **2025-03-06**; fields 23-24, 31-36; source lines 43–86 for rows used here. The **11 strong cool-core entries with original IDs ≤46** were manually transcribed from this public text, **not** downloaded as a machine-verified full catalog. They are not a random sample. This work uses published **simulated** halos, not astronomical observations.
- Official [catalog documentation](https://www.tng-project.org/data/cluster/) and Dylan Nelson's [2025-08-18 clarification](https://www.tng-project.org/data/forum/topic/997/tng-cluster-x-ray-offset-clarification/): projected X-ray and SZ peaks use a shrinking-circle algorithm and the central-galaxy position is `SubhaloPos`; the positive offset magnitudes are stored as log10(pkpc). Both peaks must share that center and projection for the bound below to apply.
- Nelson et al., [A&A 686, A157 (2024), DOI 10.1051/0004-6361/202348608](https://doi.org/10.1051/0004-6361/202348608): TNG-Cluster overview, simulation and forward-modelled gas observables.
- **Crucial prior art:** Zhang, Yu & Lu, [ApJ 796, 138 (2014), DOI 10.1088/0004-637X/796/2/138](https://doi.org/10.1088/0004-637X/796/2/138), already simulated large X-ray/SZ peak offsets under conventional gas dynamics. This calculation is a catalog-specific quality gate, not a new phenomenon.

## Exact geometry and result

For viewing axis `i`, let `qX_i`, `qSZ_i` denote the catalog logarithms, and let `G` be the common projected galaxy position. Set `RX_i = 10**qX_i pkpc = |X_i-G|` and `RSZ_i = 10**qSZ_i pkpc = |SZ_i-G|`. Because their relative directions are unknown, the reverse triangle inequality gives

`D_i = |X_i-SZ_i| >= |RX_i-RSZ_i|`.

To protect against printed logarithms rounded to 0.01 dex, lower each large radius by 0.005 dex and raise each smaller radius by 0.005 dex, clipping the resulting separation lower bound at zero. This is a **printing precision allowance only**, not map/pixel/model uncertainty.

**Highlighted result: z=0 halo `origID=34`, `haloID=4561713`, cooling time 0.78 Gyr, `r500=1.531 Mpc`.**

| Projected view | X-ray-to-galaxy radius (pkpc) | SZ-to-galaxy radius (pkpc) | Minimum X-ray/SZ separation (pkpc) | Rounding-conservative lower bound / r500 |
|---|---:|---:|---:|---:|
| x | 1.288 | 288.403 | 287.115 | **18.54%** |
| y | 1.549 | 204.174 | 202.625 | **13.08%** |
| z | 1.148 | 91.201 | 90.053 | **5.81%** |

All **three** projected views for that single halo exceed the exploratory 5% r500 threshold even under printing-rounding allowance. Of the 11 manually selected strong-cool-core rows in the excerpt, exactly **one** had any such bound above 5% r500. This is **1/11 in a nonrandom selected excerpt**, **not** a prevalence estimate. Three views of one halo are not independent halos.

### Pinned input values for independent checking

Table columns: origID, haloID, r500 Mpc, central t_cool Gyr, X-ray log10(pkpc) x/y/z, SZ log10(pkpc) x/y/z. Negative logs are positive offsets below 1 pkpc, never negative distances.

```csv
origID,haloID,r500_Mpc,tcool_Gyr,xray_x,xray_y,xray_z,sz_x,sz_y,sz_z
0,0,1.711,0.45,0.23,0.67,0.55,0.60,0.45,0.72
14,2507618,1.774,0.55,1.61,0.84,0.69,0.40,0.53,0.66
19,3135769,1.515,0.26,0.47,0.30,0.30,0.62,0.57,0.54
20,3238091,1.489,0.96,0.26,0.20,0.09,0.02,0.02,0.02
24,3656685,1.462,0.13,0.59,-0.04,0.04,0.73,0.45,0.76
28,4054274,1.547,0.63,0.24,1.16,0.11,-0.13,0.03,-0.68
34,4561713,1.531,0.78,0.11,0.19,0.06,2.46,2.31,1.96
37,4854863,1.536,0.38,0.89,0.78,0.97,0.24,-0.02,0.20
38,4959833,1.577,0.31,0.60,0.57,0.63,0.27,0.35,0.01
39,5059214,1.458,0.74,0.13,0.41,0.22,0.87,1.20,0.57
46,5524229,1.492,0.58,-0.07,-0.31,-0.17,-0.10,-0.18,-0.20
```

**Reproduction:** For each row and projection, `x=10**xray_i; s=10**sz_i; lower=max(0,10**(xray_i-0.005)-10**(sz_i+0.005),10**(sz_i-0.005)-10**(xray_i+0.005))`; flag if `lower/(1000*r500_Mpc)>0.05`. Source CSV SHA-256 `bdd40aa776551aae0caf9560baf2bca0ef6003e481409584815641f96567d06a`. Actual standard-library Python worker under 20-second timeout, exit 0, observed external wall time 0.751 s, code SHA-256 `aac52f89dfdad9160a6138d91f8dde08daaeba12134f78708c5d6ce2c2e72c74`, deterministic, no RNG. This Markdown contains data and algorithm; the executed standalone script was not uploaded in this one-file contribution.

## What changes and what remains unproven

**Practical constraint:** A cool-core flag and a nearly central X-ray peak are not sufficient to force an SZ peak within 5% r500. A future forward model should generate X-ray and SZ images separately before extracting peaks. Do not force both to follow a common gas-center latent coordinate.

**Unresolved:** Exact 2D peak coordinates and their directions, map-selection choices, full 352-halo data, calibration/selection effects, independent control of halo dynamical state. The bound is not the actual X-ray/SZ separation. There is no lensing mass map, observed likelihood or SIDM cross-section. Halo `haloID` in this z=0 catalog must not be joined directly to Cluster Merger `HaloID`.

C-03 globally unscreened gravity stays **FAILED**; C-20 time-only selection baseline stays **FAILED**; C-23 constructed-velocity contrast stays **UNIDENTIFIABLE**. The 2026-06-26 merger-`Mhistory_vel` correction does not apply because this calculation uses no velocities.

**Next discriminating step:** retrieve this halo's same-projection X-ray and SZ map pixels/peak coordinates and confirm the peak finder, common BCG center and the separation against the geometry bound. Then analyze the complete independently identified 352-halo sample without treating three projections as independent objects.

No email, peer review, Azure operations, novel physics, paid compute or manuscript submission claimed.
