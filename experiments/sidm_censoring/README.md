# C-04: Endpoint censoring in SIDM halo collapse
**18 October 2026 | DERIVED / UNIDENTIFIABLE / DATA_INSUFFICIENT**
**Source:** Silverman et al., *Mergers Matter*, arXiv:2606.02566v1 (1 June 2026), Tables 1–3: https://arxiv.org/html/2606.02566v1

**Question:** Does an SIDM halo that has not collapsed by the end of a simulation demonstrate that mergers permanently prevent collapse? No. A run's endpoint is a **censoring time**, not a physical lifetime.

Let T be the age when the core first reaches the authors' 10-times-minimum-density criterion, C the last simulated age, and P the CDM-based fluid model's **predicted cosmic age**. Observing no event establishes only T>C; it does not establish T=infinity.

| Halo | P (Gyr) | C (Gyr) | Reached 10x by C | C-P (Gyr) |
|---|---:|---:|---|---:|
| m10q | 7.33 | 10.4 | yes | +3.07 |
| m10d | 5.37 | 9.5 | yes | +4.13 |
| m10i | 2.28 | 5.2 | yes | +2.92 |
| m10b | 10.12 | 9.0 | no | -1.12 |
| m10f | 7.18 | 6.4 | no | -0.78 |
| m10j | 2.28 | 4.9 | no | +2.62 |

**C-04-C1, DERIVED:** Two of the three non-reaching runs stopped *before* their predicted epochs. Only m10j had 2.62 Gyr of continued non-crossing after its forecast. This is evidence of mismatch with a simple **approximate** model time, not a hard falsification of the complete theory.

**C-04-C2, UNIDENTIFIABLE:** At an illustrative 13.8-Gyr target, these six selected runs' endpoint flags alone permit between 3 and 6 halos to have reached threshold: 3 <= N <= 6. For each of the three censored non-events, both a subsequent crossing before 13.8 and a crossing after 13.8 are logically compatible. The range **[50%,100%] is a logical bound on this selected set, not a confidence interval or cosmic population fraction**.

The strongest null is ordinary merger-history heterogeneity, model approximation, numerical resolution and variable run duration. The simulations are dark-matter-only and have a high constant interaction benchmark of 70 cm²/g; extrapolation to observed galaxies requires additional physics. Table 3's *interval since each halo's core minimum* must not be confused with Table 1's *absolute cosmic age*. Published stopping rules may be informative because collapse elsewhere in the simulation volume makes later snapshots costly. The authors report 300–770 Myr snapshot gaps.

**What ran:** One deterministic local Python table audit (13 checks passed) on manually transcribed published summaries. This was **not** an N-body reproduction, new measurement or calibrated likelihood. Full executed code and raw JSON receipt are retained in the companion local research package; the small independent reconstruction below is not asserted to be byte-identical with that executed file. Source SHA256 of locally executed program: 6ef9a503c43a430aa3101d7b079a6dbac296e990b63597eb6a6d5739d760f34c.

**Next bounded test:** Obtain m10j's time-resolved core-density and termination metadata, then reapply the published 10x criterion and compare a matched CDM control. Stop if inputs are unavailable. Do not treat digitized plots as independent snapshots.

See [reference calculation](audit.py), [checkpoint](CHECKPOINT.md), [input table](table.csv) and [result receipt](RESULT.json).
