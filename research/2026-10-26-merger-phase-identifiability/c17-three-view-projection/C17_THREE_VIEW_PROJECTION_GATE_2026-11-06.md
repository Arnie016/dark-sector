# C-17 | Three-view projected-peak consistency gate (2026-11-06)

**Status: DERIVED + SIMULATION_RESULT (published TNG-Cluster simulation catalog entries) + DATA_INSUFFICIENT for SIDM.** No observed astronomical data, trained AI, cosmological N-body reproduction, novelty claim or cross-section constraint.

## Exact question, ordinary explanation and stopping rule

Could the three positive, log-encoded X-ray peak-to-central-galaxy offsets (or the three SZ offsets) in the public TNG-Cluster properties catalog be the orthogonal 2D projections of **one fixed 3D displacement vector**? We find **NO for each tracer in the first three catalog rows, including rounding tolerance**. The most direct ordinary explanation is that projected gas-emission peaks are defined separately on three line-of-sight-integrated maps using a peak-finding algorithm. Projection, varying emitting structures and nonlinear peak selection can shift which location is brightest. This is a data-semantics/inference gate, not evidence of particle interactions.

**Inputs and source dates:** [official public TNG-Cluster catalog](https://www.tng-project.org/files/TNG-Cluster_Catalog.txt), original parent IDs 0, 1, 2 at lines 43-45; available catalog version last updated **2025-03-06**, inspected **2026-11-06**. Columns 31-36 are `peakoffset_xray_{x,y,z}` and `peakoffset_sz_{x,y,z}`. [Dylan Nelson's 18–20 Aug 2025 field clarification](https://www.tng-project.org/data/forum/topic/997/tng-cluster-x-ray-offset-clarification/) says these are positive **magnitudes** between the X-ray/SZ peak and `SubhaloPos`, found by a shrinking-circle procedure; the input X-ray map is soft band 0.5–2 keV. See also [TNG-Cluster methods/documentation](https://www.tng-project.org/data/cluster/) and Nelson et al., *A&A* 2024, DOI [10.1051/0004-6361/202348608](https://doi.org/10.1051/0004-6361/202348608). The work uses existing published simulation values, not independent new observations.

## Geometry and falsifier

Suppose an actual single spatial offset is `v=(a,b,c)` in proper kpc, and the viewing axes are exactly orthogonal. Its projected scalar lengths would have to satisfy

```text
Rx² = b² + c²
Ry² = a² + c²
Rz² = a² + b²
a² = (Ry² + Rz² - Rx²)/2 >= 0
b² = (Rx² + Rz² - Ry²)/2 >= 0
c² = (Rx² + Ry² - Rz²)/2 >= 0
```

Thus a necessary and sufficient condition for **some single fixed vector** is `max(Rx²,Ry²,Rz²) <= sum(other two squared radii)`. Reported log offsets `q_i` give `R_i = 10**q_i pkpc`. This theorem would be invalid if the three maps use different peak locations or coordinate definitions. **That distinction is precisely the claim being checked, not a demonstration of an erroneous TNG catalog.**

For `origID=1, haloID=252455`, X-ray log radii `(1.91,2.81,1.84)` imply `(81.283,645.654,69.183) pkpc`. A fixed 3D peak requires `Ry <= sqrt(Rx²+Rz²)=106.74 pkpc`, yet `Ry=645.65 pkpc`. The ratio is **6.0489**, or at least **5.9112** under the deliberately conservative ±0.005 dex rounding variation on all three printed entries. No physical measurement precision is asserted.

## One bounded empirical check

**Deterministic selection:** first three original parent IDs **0,1,2**, corresponding to catalog `haloID=0,252455,476245`. The order is not random, and the three projections per halo are not independent halos.

| parent origID | tracer | dominant view | reported fixed-vector violation factor | conservative rounded lower factor |
|---|---|---|---:|---:|
| 0 | X-ray | y | 1.189074 | 1.162007 |
| 0 | SZ | z | 1.075926 | 1.051435 |
| 1 | X-ray | y | **6.048901** | **5.911211** |
| 1 | SZ | z | 1.406222 | 1.374213 |
| 2 | X-ray | y | 1.135224 | 1.109383 |
| 2 | SZ | z | 2.007889 | 1.962184 |

Here factor = `max(Ri) / sqrt(sum(other two radii squared))`; feasibility requires factor <= 1. All six deliberately selected tracer/halo checks fail that fixed-vector assumption, robust to 2-decimal log rounding. **This is not a population frequency or evidence that all 352 halos behave this way.**

## Execution receipt and boundaries

One standard-library Python worker: `timeout 20s python run.py`, exit **0**, measured external wall **0.79 s**. Deterministic, seed null; checks confirm parent IDs, converted negative log value, geometric identity, rounding robustness and a mathematically feasible limiting control. Verified output was read back. Input CSV SHA-256 `8e23e9faa3de48716d7a332fa9f1e69efbf929f9fb782dc9f81a9be42f5f9a07`, executed script SHA-256 `a3e1080015d32be7c79e5be94453fb23471f63902af2b9fc3cac24e781e7b7ed`, resulting JSON SHA-256 `27ba38dc68feb0a2acda63751a70b45ce667129e5a66440f8b4259343630cd43`. Input was **manually transcribed** from the public HTML-text view, not the entire TXT file downloaded. Public catalog sandbox access failed due to DNS; private Azure blobs not mounted.

Do **not** assume the TNG merger `HaloID` and properties `haloID` share a direct join key. No merger histories, 3D peak positions, X-ray/SZ maps, lensing mass reconstructions, likelihood, covariance or selection function were retrieved. Corrected `Mhistory_vel` (official change notice 2026-06-26) was not used. The C-03 globally unscreened gravity candidate remains **FAILED**; prior C-12 through C-16 shock/geometry gates remain open.

## Scientific decision / next step

Obtain same-halo, same-view **projected X-ray and SZ pixel-level peak coordinates** together with physical pixel scales and exact peak-finding conventions. Test whether different viewing directions select different emitting structures or whether other map-construction details explain the incompatibility. Only later compare with matched lensing mass maps and a calibrated ordinary-CDM baseline before contemplating SIDM inference. A multi-view observation of *the same 3D point* would satisfy the algebra by construction; a projection-dependent brightness peak need not.

Learning introduced: square-radius consistency is stronger than an unknown azimuth bound; **understanding NOT_ASSESSED**. This is an established geometrical test applied to simulation outputs, not new cosmology.
