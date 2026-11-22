# Cluster-merger collision velocity estimator comparison

Exploratory simulation diagnostic, not a measurement of a velocity error or dark matter. Reproduce with `python analyze.py /path/to/cluster_mergers.hdf5` using h5py, NumPy and Matplotlib; the script checks the corrected catalog SHA-256. Snapshot redshifts are saved alongside the script. TNG-Cluster's documentation requests citations of Nelson et al. (2024), Nelson et al. (2019) and [Lee et al. (2024)](https://doi.org/10.1051/0004-6361/202348194) for this supplementary catalog.

## Selection and method

From 2,083 event rows, retain an event only when exactly one valid record exists for each of the collision snapshot and the immediately preceding and following numbered snapshots (all 30–99), with finite velocities and finite positions inside the periodic 680,000 ckpc/h box. This yields 1,977 events, spanning 337 recorded HaloID values (not verified as distinct present-day clusters); 68 fail the snapshot requirement and 38 fail the numerical position/velocity requirement. These are event-level counts, not 1,977 independent clusters. Branch continuity, particle membership and selection biases are not independently checked.

Use the periodic nearest-image main-to-secondary position, unwrap the three-point sequence, take a nonuniform centered derivative using the flat matter-plus-Lambda cosmology h=0.6774, Omega_m=0.3089, and convert to peculiar km/s with the scale factor at the central snapshot. Compare it to secondary-minus-main `Mhistory_vel` at the same snapshot. Radiation is neglected. The median magnitude of this 3D difference is 407.4 km/s, and the 90th percentile is 974.6 km/s. The plotted histogram omits values at or above 4,000 km/s and gives the count omitted. These summary statistics describe the selected event rows, not a cosmic distribution or error bar.

The fundamental comparison is between different estimators: `SubhaloPos` traces the potential minimum while `SubhaloVel` is member-mass weighted. Cadence, center changes, membership, and unresolved orbital evolution can all contribute. Neither the direction nor contribution of each effect is measured here. The prior synthetic cadence experiment is a sensitivity demonstration rather than an event-specific bound. A matched-particle or matched-centroid control and independent branch validation remain necessary.

## Collision field caution

The median absolute difference between the relative speed at `Snap_coll` and `V_coll` is approximately 0.0002 km/s; about 51.6% of selected rows agree within 0.1 km/s. The [official catalog](https://www.tng-project.org/data/cluster/) describes `Snap_coll` as the first snapshot after pericenter and `V_coll` as the maximum relative velocity at first pericenter; equality at every row is not guaranteed by those definitions. This diagnostic does not establish a catalog bug or explain the remaining differences. Earlier single-event validation should not be generalized to every event.

## Next study

Use matched tracers and independently verified tree IDs, group repeated events by halo, estimate sensitivity to timing and validity cuts, and replicate a published merger benchmark. The [TNG gas-motion atlas](https://doi.org/10.1051/0004-6361/202348612) emphasizes that projected gas velocities do not directly determine radial gas motion; halo-relative velocities are likewise not interchangeable with gas or X-ray observables. No lensing, SIDM contrast, or observational likelihood is evaluated in this diagnostic.
