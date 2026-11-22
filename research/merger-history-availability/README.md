# Collision-time association with snapshot-99 history availability

This exploratory diagnostic intersects the previously produced collision comparison and snapshot-99 phase-space fingerprint tables by event row. It reproduces their totals: 1,977 selected events, of which 1,475 have an eligible final-snapshot fingerprint and 502 do not. `analyze.py` records input SHA-256 digests and can be run with NumPy and Matplotlib after the two upstream analyses. A fingerprint requires one snapshot-99 history record and finite, in-box main position plus finite velocity; it is not a verified merger-tree identity.

| Collision snapshot | Events | Fingerprint available | Unavailable | Median discrepancy available / unavailable (km/s) |
|---|---:|---:|---:|---:|
| 30–49 | 135 | 22 (16.3%) | 113 | 376 / 538 |
| 50–69 | 684 | 366 (53.5%) | 318 | 335 / 560 |
| 70–84 | 568 | 504 (88.7%) | 64 | 333 / 693 |
| 85–98 | 590 | 583 (98.8%) | 7 | 384 / 690 |

The probability of an eligible final-snapshot fingerprint rises sharply with collision snapshot (later cosmic time). The [official catalog documentation](https://www.tng-project.org/data/cluster/) states that orbit histories are marked `-1` after merger completion; this is consistent with a time-related selection mechanism, but we have not established a reason for each excluded row. Unavailability includes the numerical validity filter, not just absent history. The last bin has only seven unavailable events: its median is unstable. These are selected event rows, not independent halos, and the bins were chosen exploratorily. A within-bin difference does not establish the cause or correct the full-sample bias.

The discrepancy is between potential-center position derivatives and member-weighted catalog velocities. It is not a measurement error or evidence of dark-matter physics. A physical paper would require verified tree identities, matched tracers and completeness-aware selection, together with reproduction of a relevant published benchmark such as [Lee et al. (2024)](https://doi.org/10.1051/0004-6361/202348194).
