# C-23: Coarsened joint-speed overlap gate for the collision-velocity association

**Research date:** 2026-11-12 (Asia/Singapore)  
**Statuses:** DERIVED / SIMULATION_RESULT / UNIDENTIFIABLE  
**Evidence:** selected event records from a **collisionless-CDM TNG-Cluster simulation-derived CSV**, not independent observed clusters or an SIDM measurement.

## Predeclared question and stopping condition

C-21 recorded a high-minus-low contrast of +165.8900 km/s in the orbit-estimator mismatch B when grouping by the speed-definition mismatch A. C-22 obtained +158.470 km/s after controlling coarsely for collision epoch and peak collision speed. Can this remain interpretable once the instantaneous relative speed, a variable used to construct **both A and B**, is included? Assess the available overlap rather than treating a non-overlap sample contrast as a causal effect. The test is **informative regardless of the sign**: inadequate common support, an unstable contrast or a mathematically deterministic exposure means no independent physical effect can be claimed.

## Physical quantities and exact identification gate

- `u` [km/s] = norm of the main-versus-subcluster member-weighted relative velocity at `Snap_coll`, exported as `catalog_speed_km_s`.
- `v` [km/s] = `V_coll`, the catalog maximum relative speed around first pericenter, exported as `v_coll_km_s`.
- `A = |v-u|` [km/s], stored as `vc_abs_difference_km_s`. The C-21 split is `A<0.1` versus `A>=0.1`.
- `B` [km/s] = 3D norm of the difference between a center-position finite-difference velocity and the member-weighted relative velocity, exported as `discrepancy_km_s`. It shares the velocity `u` with `A`, but is a vector norm rather than a scalar speed difference.

At exact fixed `(v,u)`, `A=|v-u|` is deterministic. There is **no possible joint support** for both C-21 A groups at the same exact `(v,u)`. An adjusted **causal effect of the A category at fixed generating speeds is UNIDENTIFIABLE** by construction. This does not prevent reporting descriptive contrasts in coarse bins, but it invalidates interpreting them as independent evidence for a new force.

## One bounded empirical check

Input: [collision-comparison.csv](https://github.com/Arnie016/dark-sector/blob/f8acd8362362446b91a84d0580581450f16d26fa/research/merger-collision-ensemble/collision-comparison.csv) in existing PR #14, **Git blob SHA-1 `95200eb824b9a93f3a7ba80bf9ae9306e1249e5a`**. The upstream [analyze.py](https://github.com/Arnie016/dark-sector/blob/f8acd8362362446b91a84d0580581450f16d26fa/research/merger-collision-ensemble/analyze.py) asserts original merger HDF5 SHA-256 `d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d`. This run did **not** reopen or validate that original HDF5, access private Azure, or download bulk data. The upstream code uses adjacent snapshots and a finite difference of comoving positions with a time conversion; it computes `B` rather than measuring an error against known physical truth.

Use the **same four collision snapshot bins** as C-20/C-22: [30,49], [50,69], [70,84], [85,99]. Add fixed **100 km/s bins** independently for `v` and `u`, each using `floor(value/100)` on nonnegative speed values. Let `s` index their joint cells. Keep cells with either (i) >=1 event in each A group, or (ii) >=2 in each group as a conservative descriptive robustness condition. Within eligible cell `s`, compute `delta_s = mean(B_high,s)-mean(B_low,s)` in km/s. Report `sum_s (n_s/N_selected) delta_s`, weighted by **total events in that selected cell**, not by inferred independent halos. It is explicitly a **selected-overlap descriptive contrast**, not a full-population effect estimate.

A deterministic JavaScript calculation fetched and parsed the entire 1,977-row CSV, validated 1,977 unique event row IDs, checked finite nonnegative input and B, and confirmed `abs(abs(v-u)-A) <= 1e-7 km/s` for every row. No random seed, GPU, paid service or HDF5 access. The tool returned successfully with calculated elapsed time **263 ms including GitHub read**. Only one new scientific calculation was executed.

## Results, simulation-derived finite table

| Quantity | Number |
|---|---:|
| All valid selected simulation event rows | 1,977 |
| Low A events (`A<0.1 km/s`) | 1,020 |
| High A events (`A>=0.1 km/s`) | 957 |
| Unadjusted high-minus-low mean B | +165.8900 km/s |
| Joint snapshot + v + u cells, 100-km/s speed widths | 544 |
| Cells with >=1 in both A categories | 69 |
| Events covered by those cells | 986 (207 high A, 779 low A) |
| Weighted within-cell contrast, cells with >=1 each | **-39.2795 km/s** |
| Cells with >=2 in both A categories | 44 |
| Events covered by >=2-each cells | **759 (180 high A, 579 low A)** |
| Weighted within-cell contrast, >=2-each cells | **-41.8046 km/s** |

For the >=1-each overlap set, the retained 986/1,977 events represent 49.9% of the selected data. However only 207/957 = 21.6% of the high-A category is retained, versus 779/1,020 = 76.4% of the low-A category. The stricter >=2-each gate retains 759/1,977 = 38.4%. Thus the apparent **sign reversal** occurs on a highly nonrepresentative, coarsened overlap set. It does not establish that a physically meaningful effect is negative, that a full-cohort correction equals -39 or -42 km/s, or that the remaining discrepancy is statistically significant.

The coarsened cells are broad compared with the C-21 threshold of 0.1 km/s. They do not condition on exact `(v,u)`, so substantial residual mathematical coupling, differential selection and within-bin imbalance remain. Exact conditioning has zero group overlap, not a well-defined adjusted contrast. No halo-clustered confidence interval was computed, and repeated events may share an initial condition.

## Conclusion and decision

**C23-VELOCITY-POSITIVITY-GATE: UNIDENTIFIABLE** as an independent A-category causal effect once the two source speeds are fixed. **C23-OVERLAP-COARSENING: SIMULATION_RESULT**, with large sample loss and a sign-unstable descriptive contrast. The source association from C-21/C-22 must not be interpreted as an SIDM drag force. The ordinary explanation is shared-input algebra plus differing velocity-estimator definitions, compounded by merger-phase selection and shared halo histories.

The **next discriminating step** is a same-tracer, same-snapshot comparison on a verified individual merger with matched center and member definitions, then host-independent validation by verified FoF/SubLink descendant IDs. That replaces deterministic comparisons of two functions of the same speed with independently specified physical observables. Neither the X-ray gas peak nor a radio-relic velocity proxy is equivalent to a weak-lensing mass peak.

## Provenance, publication boundary and references

- Official [TNG-Cluster Cluster Mergers documentation](https://www.tng-project.org/data/cluster/), including `V_coll`, `Snap_coll`, `Mhistory_vel` definitions and `-1` sentinel convention. Merger catalog published 25 March 2025.
- Official [TNG change log](https://www.tng-project.org/data/forum/topic/2/changes-and-additions/): correction to `Mhistory_vel` announced **26 June 2026**.
- Lee et al., [*Radio relics in massive galaxy cluster mergers in the TNG-Cluster simulation*](https://doi.org/10.1051/0004-6361/202348194), *Astronomy & Astrophysics* 686, A55 (2024), peer reviewed. Its shock/radio relic results were not reproduced here.
- Existing companion gates: C-20 snapshot-only reweighting FAILED; C-21/C-22 adjusted associations descriptive only; C-03 globally unscreened gravity FAILED. `HaloID` from this merger table **must not** be blindly joined to the z=0 properties catalog `haloID`.
- No novel particle-physics claim, independent observational replication or astrophysical likelihood. No researcher email sent.

### Reproduction pseudocode (not a separately executed artifact)

```js
// csvRows parsed with unique "row" identifiers, all numerical columns validated
const map = new Map();
for (const x of csvRows) {
  const s = x.snap_coll < 50 ? 0 : x.snap_coll < 70 ? 1 : x.snap_coll < 85 ? 2 : 3;
  const key = [s, Math.floor(x.v_coll_km_s/100),
    Math.floor(x.catalog_speed_km_s/100)].join("|");
  const cat = x.vc_abs_difference_km_s < 0.1 ? "low" : "high";
  if (!map.has(key)) map.set(key, {low:[],high:[]});
  map.get(key)[cat].push(x.discrepancy_km_s);
}
function contrast(minCount) {
  let numerator = 0, denominator = 0;
  for (const cell of map.values()) {
    if (Math.min(cell.low.length, cell.high.length) < minCount) continue;
    const mean = a => a.reduce((s,x)=>s+x,0)/a.length;
    const n=cell.low.length+cell.high.length;
    numerator += n * (mean(cell.high)-mean(cell.low));
    denominator += n;
  }
  return numerator/denominator;
}
// contrast(1): -39.2794858824 km/s; contrast(2): -41.8045955220 km/s.
```
