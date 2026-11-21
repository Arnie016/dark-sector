# C-16 | X-ray versus SZ peak geometry in one TNG-Cluster halo (2026-11-05)

**Status:** DERIVED + SIMULATION_RESULT (one publicly documented simulated halo) + UNIDENTIFIABLE (exact separation) + DATA_INSUFFICIENT (SIDM). Not an observational measurement, cross-section bound or claimed discovery.

## Question and decision

Can the positive, log-encoded X-ray and thermal Sunyaev-Zeldovich (SZ) peak offsets from a galaxy determine the actual X-ray-to-SZ peak distance? **No.** Their azimuths are absent. Yet the two magnitudes impose exact triangle-inequality bounds. The strongest ordinary explanation for discrepant peaks is the different gas response of the tracers, plus projection and peak-finder definitions. Neither tracer locates a gravitational-lensing dark-matter mass peak.

**Source and provenance:** Official public [z=0 TNG-Cluster Catalog](https://www.tng-project.org/files/TNG-Cluster_Catalog.txt), checked 2026-11-05, line 44, `origID=1`, `haloID=252455`, `r500c=1.912 Mpc`. The complete 352-row file was NOT downloaded; only a verified, manually transcribed source row was evaluated. The team [clarified the offset conventions](https://www.tng-project.org/data/forum/topic/997/tng-cluster-x-ray-offset-clarification/) on August 18 and 20, 2025: these are positive projected peak-to-`SubhaloPos` distance magnitudes, given as log10(pkpc), **not Cartesian vectors**. See also the [TNG-Cluster documentation](https://www.tng-project.org/data/cluster/), citing Nelson et al. (2024), for projections and selection.

## Derivation and actual catalog-based calculation

Let G denote central galaxy position and X and S the projected X-ray and thermal SZ peaks on the same sightline. Each recorded scalar is `dX=10**qX pkpc` and `dS=10**qS pkpc`, measured relative to G. With an unknown relative position angle `theta in [0, pi]`, the separation `D=|X-S|` satisfies:

```
D**2 = dX**2 + dS**2 - 2*dX*dS*cos(theta)
abs(dX-dS) <= D <= dX+dS
```

Both endpoints are geometrically attainable, so the exact distance is **UNIDENTIFIABLE** from the two scalars. The q-values and results for one SIMULATED TNG-Cluster halo (NOT telescope observations) are:

| Viewing axis | qX log10(pkpc) | qSZ log10(pkpc) | dX (pkpc) | dSZ (pkpc) | D range (pkpc) |
|---|---:|---:|---:|---:|---:|
| x | 1.91 | 1.35 | 81.283 | 22.387 | 58.896–103.670 |
| y | 2.81 | 1.75 | 645.654 | 56.234 | **589.420–701.888** |
| z | 1.84 | 1.93 | 69.183 | 85.114 | 15.931–154.297 |

For the y projection the lower bound is **0.3083 r500**. Allowing ±0.005 dex roundoff on the two printed log values conservatively lowers it to **581.378 pkpc**, or 0.3041 r500. This is not a measurement error estimate. x/y/z indicate three dependent viewing orientations of one halo, not three independent objects.

## Execution and limits

One Python standard-library worker with `timeout 20s` returned exit **0**, wall **0.86 seconds** (max RSS 95,632 KB), deterministic with no seed. Verified column count/IDs, radius conversion and triangle extrema. Executed script SHA-256 `0df9717dd61dc4cc177a55fd036373ed2e7722367e84b0740e4ef06ea73a7865`; manually transcribed one-row input SHA-256 `27bc30251b96d95f8c7f82a78c02c197fffdd8bfb72de23c3ced278fb3a5bd81`; results SHA-256 `a6182a7e6ae58d142373ac780da97fe1d9136879966d4935b0f4582155e24777`. The companion executable/output were validated locally, but not committed in this note. The calculations can be independently repeated using q-values and the formula above.

Public catalog download to sandbox failed; an alternate attempt failed DNS. Private Azure blob contents were NOT accessed. No merger trajectories or halo-ID joins, and no use of the separately corrected `Mhistory_vel` field (June 26, 2026). No whole-population rate, p-value, observational interpretation or SIDM sensitivity is inferred.

**Required next discriminator:** recover same-view map pixel coordinates of X-ray and SZ peaks for this one actual simulated halo, on a verified common pixel scale and peak-finder convention. Compare true projected separation to the predicted bounded interval. A mismatch would motivate a catalog/pipeline audit before speculation about new physics. Lensing mass peaks and fully specified uncertainties remain additional requirements for SIDM inference. Prior C-03 globally unscreened long-range gravity remains **FAILED**.

**Learning checkpoint:** angle versus distance and different gas tracers INTRODUCED; user comprehension NOT_ASSESSED.