# Collision-time repeats and the pericenter-distance diagnostic

This exploratory check asks whether catalog collision times concentrate at the same numerical value for events assigned the same collision snapshot, and whether that concentration differs between the two previously defined pericenter-distance groups. It uses the corrected, SHA-256-pinned TNG-Cluster merger catalog and the row-level output of the [earlier distance/time check](../pericenter-time-distance-association/README.md). It is not a merger-clock calibration or an observational result.

Of all 2,083 rows, 1,686 share an exact `T_coll` value with at least one other row; 635 distinct values occur. For each `Snap_coll`, we choose the most frequent exact `T_coll` value across *all* catalog rows (in an exact frequency tie, the lower value). Among the 1,977 rows selected in the prior audit:

| Previously defined distance group | Events | Equal to modal `T_coll` for the same `Snap_coll` | Distinct recorded halo labels |
| --- | ---: | ---: | ---: |
| Nearby proper-scaled numerical separation match | 1,428 | 1,193 (83.5%) | 330 |
| No such nearby match | 549 | 16 (2.9%) | 238 |

The modal value is an empirical property of these event rows; it is **not independently shown to equal the actual snapshot age**. This result is consistent with differing time/position sampling or interpolation conventions, but does not establish their cause, the correct `d_peri` units, a defect, or any effect on a published radio-relic calibration. Both group definitions use related catalog fields and the same simulation; the pattern is not independent evidence. Selection excludes 106 rows, groups can share halo labels, and repeated events are not independent clusters. There is no confidence interval, population inference, or corrected measurement here. The documentation calls `T_coll` a pericenter time and `d_peri` ckpc/h; the [original radio-relic paper](https://arxiv.org/html/2311.06340) describes fitting the separation near pericenter. The exact released implementation and its conventions remain to be verified.

Run `python analyze.py /path/to/cluster_mergers.hdf5` with Python, NumPy, h5py and matplotlib; the adjacent prior CSV must be present. The output is `event_diagnostic.csv`, `summary.json`, and `collision-time-modes.png`. The script checks the catalog digest, checks row uniqueness, and verifies collision times and snapshot numbers against the prior table. A separate standard-library count of the output reproduced the group totals and modal counts. Resolve event-to-descendant matching and obtain source code or author clarification before interpreting this as a physical clock or submitting a paper. Any author email requires the user's approval.
