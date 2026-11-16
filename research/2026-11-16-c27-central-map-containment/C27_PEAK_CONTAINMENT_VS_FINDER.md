# C-27 | Peak containment does not make TNG map pipelines equivalent

**Date:** 2026-11-16 (Asia/Singapore)  
**Status:** DERIVED using SIMULATION-DERIVED TNG-Cluster catalog data; 352-halo population DATA_INSUFFICIENT. This corrects one possible interpretation of C-26 but does not reproduce X-ray or SZ maps, show a new physical interaction, or give an SIDM constraint.

## Claim, ordinary alternative, stopping condition

For the 11 manually transcribed strong-cool-core halos analyzed in C-25, ask whether the X-ray or SZ *catalog-reported* projected peak positions could be outside the published central projection square merely because that map covers only ±0.5 r500. Test all three projections and both tracers, with 0.005-dex upper rounding allowance. If all reported peak radii are below 0.5 r500, peak-exclusion-by-cropping is not an explanation **for these selected locations**.

The strongest conventional alternative remains that shrinking-circle peak selection depends on the map's full field, depth, smoothing and search algorithm. **A coordinate lying inside two fields does not mean both peak finders will select it.** The C-26 factual input-footprint mismatch remains.

## Data provenance and primary sources

- [Official TNG-Cluster Catalog](https://www.tng-project.org/files/TNG-Cluster_Catalog.txt), last updated **2025-03-06**, 352 simulated z=0 halo targets. Original IDs used: 0,14,19,20,24,28,34,37,38,39,46. Published catalog columns: r500c [Mpc], coolcore_tcool [Gyr], peakoffset_xray_x/y/z and peakoffset_sz_x/y/z [log10(pkpc)]. These eleven rows are a previously manually transcribed *nonrandom excerpt*, not a newly downloaded 352-halo table. C-25's verified input CSV SHA-256: **bdd40aa776551aae0caf9560baf2bca0ef6003e481409584815641f96567d06a**.
- [Official TNG projection documentation](https://www.tng-project.org/data/cluster/): both public 0.5r500 central map variants span ±0.5r500 in each sky coordinate, 2000×2000 pixels; HDF5 maps record box_center/box_size/axes_set. Different central-map variants have different line-of-sight depths.
- [Dylan Nelson's 2025-08-18 offset clarification](https://www.tng-project.org/data/forum/topic/997/tng-cluster-x-ray-offset-clarification/): positive offsets are relative to SubhaloPos, shrinking-circle peak positions are used, and the catalog X-ray input map spans ±r500 with stated projection depth 3r200c. It does not explicitly establish an equivalent public-map SZ peak finder. See Nelson et al., [A&A 686 A157 (2024)](https://doi.org/10.1051/0004-6361/202348608) for the underlying TNG-Cluster simulation.

## DERIVED geometry and bounded SIMULATION-DERIVED result

Let R = 10^q pkpc be the projected distance from the common central galaxy to a peak, with q = log10(R/pkpc). For published hundredth-dex values take R_upper = 10^(q+0.005) pkpc. The public central square has half-width H = 500*r500_Mpc pkpc. If R_upper < H, then for *any position angle*, |x| <= R_upper and |y| <= R_upper, so the reported peak coordinate is guaranteed inside the ±H square. This is a sufficient, not a necessary, condition.

**Executed result: 66/66 projected catalog peak radii fit**, across 11 halos × 3 axes × 2 tracers, with the upper rounding allowance. These are 66 correlated data values within just 11 simulated halo targets, not independent cluster observations. The largest R_upper/H is **0.381114**.

The tightest containment margin occurs for halo origID=34, haloID=4561713, x-view SZ peak. Here r500 = 1.531 Mpc, so H=765.5 pkpc; q_SZ=2.46 gives R=288.403 pkpc and R_upper=291.743 pkpc. Therefore the guaranteed margin from the peak to each map edge is at least **473.757 pkpc**, or **618.9 central-map pixels** assuming 0.7655 pkpc/pixel. The x-view X-ray radius is only 1.288 pkpc. The previously established C-25 X-ray-to-SZ separation lower bound remains 283.799 pkpc after logarithmic rounding.

**Interpretation:** For these original catalog peak coordinates, the public central map is not too small to contain them. This does **not** establish that peak-finding on a differently cropped field would return the same coordinates. Nothing was measured on actual HDF5 image pixels.

## Execution receipt, scope and checkpoints

One standard-library Python worker, command: timeout 20s python c27_containment.py. **Exit 0; measured shell-side wall time 0.89 s**, deterministic with no random seed. Checks: exact 11 unique IDs, coolcore_tcool < 1 Gyr, finite units and log offsets, all 66 inequalities, source SHA-256 matches C-25.

- Input CSV SHA-256: bdd40aa776551aae0caf9560baf2bca0ef6003e481409584815641f96567d06a
- Executed code SHA-256: 16b1df0b6ad2b7dc6515c9963f0ca614476fc8ac8bf8b5c1d5790725c94180d2
- Results JSON SHA-256: 208630a693431eeb696753a0aebb61765243d00eddb765a0b4e9a8fd688d4ef6

To independently reproduce the geometric test using C-25's 11-row CSV, evaluate 10^(log_offset+0.005) < 500*r500_Mpc for every axis and both tracer columns. The exact executed Python, CSV, JSON results and stdout/stderr are retained in the local release package; this one-file contribution does **not** claim code upload to GitHub or independent peer review.

The full 352-row official table remained accessible via web text view, but a Python download failed DNS resolution. No Azure paths were mounted or used. No paid compute or bulk download. No merger/property halo-ID join. The 2026-06-26 Mhistory_vel correction is irrelevant here because no velocities were read.

**C27: DERIVED** peak containment for a limited simulated excerpt; **C26: DERIVED** map-input provenance mismatch remains; **C25: SIMULATION_RESULT** catalog lower-bound non-co-location remains; **C20: FAILED** snapshot-only selection correction; **C23: UNIDENTIFIABLE** constructed exposure comparison; **C03: FAILED** globally unscreened long-range gravity. No new dark-matter evidence.

**Next discriminating input:** Same-halo X-ray/SZ pixel maps or peak coordinates with validated HDF5 box_center, box_size and axes_set, matched depth and precise shrinking-circle implementation. The peak reproducibility gate comes before expansion to a halo-level full-catalog and observational likelihood. Learning: radial inclusion versus actual peak-selection equivalence introduced; user understanding NOT_ASSESSED. No physicist outreach or manuscript action.

