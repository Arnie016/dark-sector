# Audit of `V_coll` against adjacent merger-history speeds

This exploratory check follows `merger-collision-ensemble`; it takes the same selected 1,977 event rows and independently recomputes the magnitude of secondary-minus-main `Mhistory_vel` at the catalog's `Snap_coll` and the immediately preceding and following snapshot. A match means absolute difference from `V_coll` less than 0.1 km/s. The corrected input HDF5 is SHA-256 checked, and the selected CSV hash is recorded in `summary.json`. Run `python analyze.py /path/to/cluster_mergers.hdf5`. Same-event results are correlated and halo IDs repeat.

The [official documentation](https://www.tng-project.org/data/cluster/) defines `Snap_coll` as the closest snapshot after first pericenter and `V_coll` as the maximum relative velocity at first pericenter; it does not assert equality with the after-pericenter speed. The previous statement that approximately 52% match is a description, not a failure rate.

| Selected rows | N | Match at collision snapshot | Match at previous | Match at next | Match at any of the three |
|---|---:|---:|---:|---:|---:|
| All | 1,977 | 1,020 | 565 | 88 | 1,673 |
| Collision and full-collision snapshots equal | 239 | 126 | 70 | 11 | 207 |
| Different snapshot numbers | 1,738 | 894 | 495 | 77 | 1,466 |

The current-snapshot agreement fractions are 52.7% and 51.4%, respectively; this split does not show a substantial difference in these descriptive data. The additional preceding-snapshot matches are consistent with (but do not prove) a pericenter timing/maximum-speed explanation. There are 304 rows with no match among the three snapshots. Neither group comparison is causal; the selection was based on available adjacent histories and not independent clusters. Other snapshots, interpolation, construction choices, and numerical details have not been checked. These results do not establish a bug in the corrected velocity field.

An independent numerical check in the script verifies every collision-snapshot difference against the previous analysis's saved result. Required next: consult the Lee et al. catalog construction method, verify specific event branches and history against provider data, and examine a matched-tracer trajectory before attributing the discrepancies. Citation: [Lee et al. (2024)](https://doi.org/10.1051/0004-6361/202348194), and the TNG-Cluster source citations specified in its documentation. No SIDM or observational claim is made.
