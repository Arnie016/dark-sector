# C-28 | Orthogonal-projection closure for TNG-Cluster X-ray and SZ peaks

**Date:** 2026-11-17 (Asia/Singapore)  
**Status:** DERIVED from SIMULATION-DERIVED catalog values. **DATA_INSUFFICIENT** for exact pixel-map validation or SIDM inference.

## Question, ordinary explanation, stopping criterion

Can the three catalog offset radii for a given emission tracer and simulated cluster be the orthogonal projections of **one fixed physical point** relative to its central galaxy? The strongest ordinary explanation for failure is that peaks of separately integrated X-ray or thermal-SZ maps can correspond to different gas structures in different sightlines. Examine the pre-existing 11 nonrandom strong-cool-core halos from C-25/C-27. Stop after a rounded-data-robust geometric test, without model fitting.

## Geometric necessity

Let **d** = (dx,dy,dz) be a hypothesized *single fixed 3D displacement vector* from the galaxy to a tracer peak. For x-, y-, and z-axis sightlines, its projected scalar radii must obey

$$
R_x^2=d_y^2+d_z^2,\quad
R_y^2=d_x^2+d_z^2,\quad
R_z^2=d_x^2+d_y^2.
$$

Consequently, **each projected radius must satisfy** $R_i^2\leq R_j^2+R_k^2$. If even one inequality fails, these three scalars cannot arise from that one displacement vector. Passing is necessary but does not prove the existence of a physical 3D peak.

Catalog values are $q_i=\log_{10}(R_i/\mathrm{pkpc})$, so $R_i=10^{q_i}$ pkpc. Accounting conservatively for values printed to 0.01 dex, a *robust* violation requires

$$
10^{q_{\max}-0.005} >
\sqrt{10^{2(q_j+0.005)}+10^{2(q_k+0.005)}}.
$$

This conditional test assumes the x/y/z suffixes are orthogonal viewing directions, all reference the same galaxy center, and the projected distance magnitudes use the catalog-defined convention.

## Executed result on the selected simulated excerpt

A byte-verified copy of the C-27 selected CSV contained **11 halos** and **22 tracer triplets**, 11 X-ray plus 11 thermal SZ. **12 of 22** triplets fail the fixed-point closure gate robustly despite the rounding allowance: **6 of 11 X-ray** and **6 of 11 SZ**. This is not a prevalence measurement for the 352 simulated halos, much less for real observed clusters. Views and tracers from one halo are correlated.

**Worked example:** origID 34, TNG haloID 4561713, thermal SZ. The catalog's x/y/z logged offset magnitudes are (2.46, 2.31, 1.96), yielding (288.403, 204.174, 91.201) proper kpc. A single fixed 3D peak would require $R_x\leq\sqrt{R_y^2+R_z^2}=223.617$ pkpc, contradicted by the 288.403-pkpc reported radius. Conservative rounding still leaves $R_{x,\min}=285.102$ pkpc and $\sqrt{R_{y,\max}^2+R_{z,\max}^2}=226.206$ pkpc, a **58.895-pkpc closure margin**. This is an algebraic discrepancy, NOT an observed physical distance or extra dark-matter drag.

In the limiting case **d**=(d,0,0), radii are $(0,|d|,|d|)$ and the inequality is exactly satisfied. The gate tests cross-view consistency, not amplitude or significance.

## Physical interpretation and restrictions

The peak in a 2D image need not be the projection of an invariant 3D position. X-ray surface brightness depends on density-weighted gas emissivity integrated along a sightline; thermal SZ depends on integrated electron pressure. Distinct sightlines may maximize at different positions. Therefore an astrophysical world model should forward-project **the entire 3D gas field**, then apply each tracer's peak-selection procedure, rather than invent one fixed 3D SZ or X-ray maximum and project its location into all three images.

This conclusion is a simple mathematical consistency failure for a restricted observation model, **not a claim of novel astrophysics or self-interacting dark matter evidence**. The original HDF5 maps and pixel peak coordinates were not accessible. The exact suffix-to-view mapping, common center and map processing must still be verified against same-halo HDF5 metadata; public-map extents may differ from catalog peak-finding inputs. No independent pixel or observational reproduction, calibrated uncertainty or full-352-halo inference was performed.

## Provenance, code rule, run receipt

- Official TNG-Cluster properties catalog, 352 z=0 halos, **last updated 2025-03-06**, with log(pkpc) peakoffset_xray_{x,y,z} and peakoffset_sz_{x,y,z}: https://www.tng-project.org/files/TNG-Cluster_Catalog.txt .
- TNG-Cluster projection methods and three orthogonal viewing axes: https://www.tng-project.org/data/cluster/ ; author clarification of offsets and central SubhaloPos on **2025-08-18**: https://www.tng-project.org/data/forum/topic/997/tng-cluster-x-ray-offset-clarification/ . Simulation introduction: Nelson et al., A&A 686 A157 (2024), https://doi.org/10.1051/0004-6361/202348608 .
- This is a reanalysis of the same **11 preselected, manually transcribed halos** as C-25/C-27. Selected CSV SHA-256: **bdd40aa776551aae0caf9560baf2bca0ef6003e481409584815641f96567d06a**; local Python code SHA-256: **ede8538fff9da82561aed165a4fcbb6b86c415c0c493d2f0e242f9813ab69d4b**; JSON result SHA-256: **340d2322f4b9296b76facbc54fafeaed6443fd47fbd9e25f6cf9660e75375ddd**.
- Deterministic reproduction rule for each tracer-triplet: read $q_x,q_y,q_z$, find largest $q_i$, compare $10^{q_i-0.005}$ against the quadrature of upper-rounded other two radii. Count only strict positive margins. The executed local code verifies all 11 unique IDs and source SHA before the calculation.
- Execution: standard-library Python, command **timeout 20s python c28_projection_closure.py**, exit **0**, externally measured wall **0.87 seconds**; no RNG, paid API, GPU or Azure data. The official catalog web text was inspected for matching examples; a direct container fetch failed DNS, so the full 352-row file was **not** loaded.
- No merger catalog-to-property haloID joins. The 2026-06-26 Mhistory_vel correction concerns the different merger-velocity lane and did not enter this calculation.

## Checkpoint and falsifier

**C28 DERIVED:** single-fixed-3D-peak observation shortcut fails for 12/22 selected tracer triplets, conditional on stated source conventions. **C27 DERIVED** central-map containment remains true. **C26 DERIVED** public-map footprint mismatch remains. **C25 SIMULATION_RESULT** X-ray/SZ radial difference lower bound unchanged. **C23 UNIDENTIFIABLE** velocity-category causal interpretation, **C20 FAILED** snapshot-only standardization, **C03 FAILED** unscreened long-range gravity.

**Next discriminating measurement:** For halo 4561713 obtain actual x/y/z SZ map peak *pixel coordinates*, viewing-axis labels, consistent center/depth metadata and the original shrinking-circle implementation. This can separate intrinsic line-of-sight peak selection from column mapping or map-pipeline mismatch. No physicist was contacted, no journal submitted and no credentials or private correspondence were shared. The mathematical idea is introduced but user understanding has not been assessed.