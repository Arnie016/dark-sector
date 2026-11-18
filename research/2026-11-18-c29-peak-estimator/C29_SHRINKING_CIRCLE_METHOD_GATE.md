# C-29 | The TNG-Cluster 'peak offset' is not necessarily a brightest-pixel location

**Date:** 2026-11-18 (Asia/Singapore). **Status:** DERIVED source-code audit; SIMULATION_RESULT for a reused, nonrandom 11-halo excerpt; DATA_INSUFFICIENT for exact published-HDF5 provenance and full-catalog inference.

## Question, baseline, stop condition

Does it make sense to model the released X-ray/SZ peakoffset scalars as distances to a single brightest pixel, or does the documented implementation find a different kind of 2D position? The ordinary explanation is a shrinking-circle flux centroid. Inspect the code chain, then make one bounded pixel-scale consistency check on the already verified 11 simulated halos. Stop without claiming to reproduce the actual released maps.

## Code evidence, pinned to a specific upstream version

At [dnelson/temet commit b136657](https://github.com/dnelson/temet/commit/b13665712db3a6eaf95835d5bd1d837ebd9972a0):

- [temet/catalog/maps.py](https://github.com/dnelson/temet/blob/b13665712db3a6eaf95835d5bd1d837ebd9972a0/temet/catalog/maps.py) distinguishes an explicit `max_pixel` finder from `_find_peak(..., method='shrinking_circle')`. The latter is called by `summarize_projection_2d(..., op='peak_offset')`. It iteratively computes a linear-flux-weighted centroid inside a contracting circular aperture, multiplies the aperture radius by **0.95** per iteration and stops at at most 100 enclosed pixels or 500 iterations. The result is a continuous coordinate in pixels, not constrained to a brightest pixel's integer coordinates.
- The same code's configuration 2 specifies three orthogonal views, **2000 × 2000 pixels**, total image width **r500** (half-width ±0.5 r500), and projection half-depth **3 r200**.
- [temet/projects/tngcluster.py](https://github.com/dnelson/temet/blob/b13665712db3a6eaf95835d5bd1d837ebd9972a0/temet/projects/tngcluster.py) wires X-ray and SZ offset auxiliary fields to the shrinking-circle summary with configuration `0.5r500_d=3r200`, then exports base-ten logarithms as the six peakoffset columns.
- [temet/load/groupcat_fields_post.py](https://github.com/dnelson/temet/blob/b13665712db3a6eaf95835d5bd1d837ebd9972a0/temet/load/groupcat_fields_post.py) reads separate *released* XrayOffsets/SZOffsets HDF5 arrays, converts code length to proper kpc, and chooses the x/y/z column before export. **The binary released arrays were not reopened or matched to this particular code revision.** The author's [August 18, 2025 forum response](https://www.tng-project.org/data/forum/topic/997/tng-cluster-x-ray-offset-clarification/) also confirms shrinking-circle and `SubhaloPos`, but describes an X-ray map spanning ±r500, different from this source's auxiliary-map footprint. That version/footprint gap remains open.

## Executed finite-domain pixel-scale check

Input: the already source-checked 11 nonrandom strong-cool-core halos of C-28, exactly 33 X-ray and 33 SZ projection offset magnitudes. Input SHA-256: `bdd40aa776551aae0caf9560baf2bca0ef6003e481409584815641f96567d06a`. These are actual TNG-Cluster simulated-catalog values, not observations, newly generated simulations or additional independent halos.

For each published log radius q (log proper kpc) and r500 (Mpc), **conditional on the public code's config-2 map width**, use pixel scale `s = 1000*r500/2000 pkpc/pixel` and pixel radius `p = 10^q/s`. To call an offset robustly subpixel, require the upper-rounded q+0.005 dex estimate of p to be strictly below 1.

**Result:** 2/33 X-ray offsets and 4/33 SZ offsets are strictly between zero and one pixel, robust to printed-value rounding. 22/33 per tracer are within five pixels. Pixel scales across the 11 halos range from **0.729 to 0.887 pkpc/pixel**.

**Worked example:** For original halo 34 / TNG halo 4561713, r500=1.531 Mpc gives 0.7655 pkpc/pixel. Its x-view X-ray radius is 10^0.11=1.28825 pkpc = **1.68289 pixels**; its x-view SZ radius is 10^2.46=288.403 pkpc = **376.751 pixels**. These are radial offsets from the shared reference galaxy, not directly measured peak-to-peak distances.

Under the source's image-center convention (integer coordinate 1000,1000), a noncentral brightest integer pixel cannot have a positive radial offset smaller than one pixel. A continuous weighted centroid can. This is a **conditional consistency check** supporting the code-level correction, not proof the same code revision generated all released catalog numbers.

## Correction to earlier physical interpretations

C-25's geometric reverse-triangle separation lower bound still applies to the two *reported estimator positions* if referenced to the same galaxy in the same 2D projection. C-28's orthogonal-projection closure failures remain a rejection of the simplification that all three reported 2D radii are projections of one fixed 3D position. But **they do not prove that different sightlines select different global-brightest pixels or different individual 3D gas knots**. The measurement may be a line-of-sight-dependent **weighted centroid**. The correct forward operator is 3D gas emission or pressure → integrated 2D map → calibrated shrinking-circle centroid → scalar offset.

## Reproducibility, explicit gaps, next discriminating measurement

Executed one standard-library Python calculation: `timeout 20s python c29_pixel_gate.py`, exit 0, external wall 0.85 s, internal 0.000419 s. Code SHA-256 `cd349a7d2ceb222ec309d40448dcf9e90fcdb912d182aeaa9700bb7d4dee565e`; results JSON SHA-256 `ac82168fd33773fe61af37395aa1df5902530649da7e51513c64b89fc22b143a`. Deterministic, no RNG, remote HPC, paid API, GPU or cloud modification. Local script and full receipt retained outside this public repository; the reproducibility rule and necessary inputs are stated here.

Private Azure catalogs were not mounted. Direct download of the official public 352-row text file failed local DNS; this run processed only the 11 byte-verified local rows. No map pixels, released offset HDF5 or full 352-halo sample was loaded. Merger-catalog `Mhistory_vel` was not used. Existing C-03 unscreened gravity FAILED, C-20 snapshot correction FAILED and C-23 velocity effect UNIDENTIFIABLE remain unchanged.

**Next test:** For TNG halo 4561713, retrieve one actual source-identified X-ray/SZ x-view pixel-map pair and corresponding released offsets, confirm projection box/depth and SubhaloPos, rerun the exact peak-finder version and compare to published values within 0.01 dex. If the released map differs from the public code's input configuration, version the observation operator before physical interpretation. No new physics or population prevalence is claimed.
