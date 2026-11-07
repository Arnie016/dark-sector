# Collision-epoch stratification of time–distance association

This check extends `../pericenter-time-distance-association`: among 1,977 selected TNG-Cluster merger events, distinguish the 1,428 whose catalog `d_peri` number matches one of three nearby proper-scaled separations and the 549 that do not. For each event, compare `T_coll` with the nearest of the same three snapshot ages, using the previous flat matter-plus-Lambda age approximation and a 0.01 Gyr diagnostic threshold. The catalog's exact `T_coll` convention remains unverified. Both classifications are computed from the same simulation release and related snapshots; this is not independent corroboration.

| `Snap_coll` range | Distance-match group: time within threshold | Distance-nonmatch group: time within threshold |
|---|---:|---:|
| 30–49 | 99 / 112 (88.4%) | 1 / 23 (4.3%) |
| 50–69 | 445 / 521 (85.4%) | 4 / 163 (2.5%) |
| 70–84 | 332 / 401 (82.8%) | 8 / 167 (4.8%) |
| 85–98 | 323 / 394 (82.0%) | 13 / 196 (6.6%) |

The qualitative association appears in all four chosen snapshot ranges. These bins were selected for exploration, not preregistered. Rows can share a cluster or trajectory, event inclusion depends on history availability, and no inference or uncertainty intervals are calculated. Similar rates across bins do not resolve cosmology/time convention, units, sample selection, unobserved subhalo switching, or the release's exact algorithm. The [official catalog](https://www.tng-project.org/data/cluster/) calls `T_coll` the pericenter time and labels `d_peri` ckpc/h; [Lee et al. (2024)](https://arxiv.org/html/2311.06340) describes a five-point fit. We do not conclude which field convention is correct, that either source is wrong, or that the pattern is new physics.

Run `python analyze.py` with NumPy/Matplotlib after generating the adjacent time–distance comparison. It records that input's SHA-256 and outputs the summary and figure. A separate check confirms the strata sum to the original group counts and threshold counts. Exact construction code or an approved author clarification, followed by independent branch and selection validation, remains necessary for manuscript-level interpretation.
