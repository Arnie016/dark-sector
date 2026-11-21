# C-30 | A pixel-count stopping rule is not a fixed physical aperture

**2026-11-19 (Asia/Singapore)**. **DERIVED** method gate, **SIMULATION_RESULT** from reused z=0 TNG-Cluster simulated-catalog values, **DATA_INSUFFICIENT** for map-level validation and released-HDF5 provenance. Not a dark-matter detection, novel method, or sensitivity estimate.

## Question and stopping rule

Does the public shrinking-circle estimator's `npx <= 100` stopping criterion impose a fixed proper-kpc analysis aperture across cluster masses or map resolutions? **No.** The ordinary explanation for offsets much smaller than one pixel is a continuous weighted-centroid estimator, not necessarily a spatially compact emitting knot. Audit the pinned code and compute only the nominal physical support scale for the already source-checked 11 strong-cool-core halos. Stop before any claim to reproduce pixel maps.

## Evidence: exact version and independent sources

- [dnelson/temet `maps.py` at `b13665712db3a6eaf95835d5bd1d837ebd9972a0`](https://github.com/dnelson/temet/blob/b13665712db3a6eaf95835d5bd1d837ebd9972a0/temet/catalog/maps.py). The `_find_peak(..., method="shrinking_circle")` loop recomputes a **linear-brightness-weighted** centroid, shrinks the pixel-radius by 0.95 each step, and exits at `npx<=100` or 500 iterations. `summarize_projection_2d` converts logged input maps to linear flux (`10**proj`) and sets the reference `SubhaloPos` at map center. The source's config 2 uses 2000 pixels across a total width of `r500` (±0.5 r500).
- [Official public TNG-Cluster z=0 catalog](https://www.tng-project.org/files/TNG-Cluster_Catalog.txt), last documented change **2025-03-06**, reports offsets in log proper kpc for 352 original zoom targets.
- [Author's 2025-08-18 clarification](https://www.tng-project.org/data/forum/topic/997/tng-cluster-x-ray-offset-clarification/) confirms shrinking-circle and `SubhaloPos`, but describes an X-ray map spanning **±r500**, unlike the pinned source's ±0.5 r500. The exact binary-catalog generation code and footprint remain **unverified**.
- Nelson et al. (2024), *A&A* 686 A157, [DOI 10.1051/0004-6361/202348608](https://doi.org/10.1051/0004-6361/202348608), provides peer-reviewed cosmological-simulation context; this run introduces no observed clusters.

## Calculation and measured inputs

For a map `N` pixels across, total width `r500` in Mpc, define the physical pixel scale `s=1000*r500/N` proper kpc/pixel. A near-circular area with 100 pixels has **nominal** radius

$$
r_{100,\mathrm{nom}}=s\sqrt{100/\pi}\simeq5.642s.
$$

**Important:** this is a continuum-area *proxy*, **not** the observed final support radius. The code uses an integer mask, moving center and pixel-count stopping test, so the final actual radius need not equal the proxy; there is no tolerance on centroid convergence. An aperture's physical support is **not** a centroid uncertainty.

Input: the C-29 byte-verified, **nonrandom 11-halo strong-cool-core subset**, SHA-256 `bdd40aa776551aae0caf9560baf2bca0ef6003e481409584815641f96567d06a`. Three correlated x/y/z views per halo, two gas tracers. For each logged offset `q`, its simulated-catalog radius is `R=10**q` pkpc. To account for 0.01-dex printed rounding, a radius is robustly below the nominal aperture if `10**(q+0.005)<r100_nom`.

**DERIVED and SIMULATION-DERIVED, conditional on the inspected source configuration:**

| Map width | Min nominal radius | Median nominal radius | Max nominal radius |
|---|---:|---:|---:|
| 1000 px (counterfactual) | 8.226 pkpc | 8.638 pkpc | 10.009 pkpc |
| 2000 px (source config) | 4.113 pkpc | 4.319 pkpc | 5.004 pkpc |
| 4000 px (counterfactual) | 2.056 pkpc | 2.159 pkpc | 2.502 pkpc |

At 2000 px, **27/33** X-ray centroid offsets and **25/33** SZ centroid offsets fall below the nominal stopping-aperture radius, **robust to catalog rounding**. These are repeated views from 11 halos, **not 66 independent systems or a population prevalence estimate**. No actual image was rerendered at the counterfactual resolutions.

For original halo 34, TNG haloID **4561713**, `r500=1.531 Mpc` gives `s=0.7655 pkpc/px`, hence `r100_nom=4.319 pkpc`. Its x-projection X-ray offset is `10**0.11=1.288 pkpc`, or **0.298 times** that nominal aperture radius. The same-view SZ offset is `10**2.46=288.403 pkpc`. At the hypothetical 4000-px grid, the nominal radius would be **2.159 pkpc**, half as large. As `N→∞` at fixed footprint with the 100-pixel criterion, nominal physical scale tends to zero, **without guaranteeing centroid convergence to a physical gas clump**.

## Decision and evidence limits

**AHA:** A centroid can be close to the central galaxy while averaging emission across a region much wider than the centroid-to-galaxy separation. C-29's continuous-coordinate finding does **not** certify subpixel physical accuracy or fixed proper-length resolution. This code convention is a concrete calibration requirement for the gas observation operator, not evidence for SIDM.

**Next discriminating step:** obtain one source-identified original X-ray/SZ projection map for halo 4561713, its code version, footprint and `SubhaloPos`. Reproduce the centroid at native resolution, rerender the same physical field at another pixel count, and quantify any offset change using exactly the same physical extent. Compare to released offsets only after source-version provenance is established. Do not treat projected gas centroids as lensing mass peaks.

## Reproducibility and checkpoints

One deterministic Python standard-library worker, `timeout 20s python3 c30_aperture_scale.py`, exit **0**, external wall **1.22 s**, seed **none**. Source script SHA-256 `4a47e767f4aca1178dc1b6975d97146fa60edb6894cb7eb86d3828d281673c92`; result JSON SHA-256 `e4fb1887cddfe635a922cc7c4d6f202dd9d11af24648bb68974b3beea72cb745`. CSV, original script and receipt retained in the run's local release package. The private Azure catalog was not accessible; a direct local download of the full public catalog failed DNS resolution. No HDF5 maps, new simulations, GPUs, paid APIs or cloud resources were used.

C-03 globally unscreened gravity **FAILED**, C-20 snapshot reweighting **FAILED**, C-23 velocity category **UNIDENTIFIABLE**. C-25 separation bounds and C-28 projection-closure results remain mathematical diagnostics of the **reported centroids**, conditional on source conventions. C-29 method audit remains **DERIVED**. Reader comprehension **NOT_ASSESSED**. No outreach or independent scientific peer review.
