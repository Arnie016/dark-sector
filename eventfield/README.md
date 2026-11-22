# Eventfield

Eventfield is a local astronomy atlas for TNG-Cluster merger histories and paired LoTSS-DR2 images. It runs as a static site with a generated read-only cache.

| View | What you can do |
| --- | --- |
| Atlas | Inspect present-day gas, X-ray and radio gallery views and browse actual HDF5 fields and event IDs. |
| Orbit lab | Replay catalog events, project relative positions and peculiar velocities, or seed an educational two-body orbit. Export measured and modeled series as CSV. |
| Radio lab | View a wide native-resolution radio field. Open the analysis to switch to a common beam, vary the settings and export a measurement. |
| Data library | Read the 352-cluster catalog inventory and see which larger numerical products would test the next hypothesis. |
| Journal | Read a timeline of research, proofs, and proposals. Try the interactive relic clock or import a scheduled run note. |
| Research desk | Search nine cited notes or ask for a calculation such as “Measure Abell 1925 at 450 kpc” or “How fast is row 5 at snapshot 70?” Open the exact settings in a lab. |

## Run locally

From the repository root, serve the folder on loopback and open [the atlas](http://127.0.0.1:8769/).

```sh
python3 -m http.server 8769 --bind 127.0.0.1 --directory eventfield
```

The local cache lives under `eventfield/data/local/`. Use the private Eventfield bundle if available. For a fresh cache, prepare the inputs below and run the exporter with Python 3.12 and `h5py numpy scipy astropy`. The static site itself needs only a recent browser and a local HTTP server.

```sh
python eventfield/scripts/prepare_data.py \
  --tng "$EVENTFIELD_TNG_DIR" \
  --gas-gallery "$EVENTFIELD_GAS_DIR" \
  --radio-gallery "$EVENTFIELD_RADIO_DIR" \
  --fits "$EVENTFIELD_FITS_DIR"
node eventfield/scripts/verify.mjs
python3 eventfield/scripts/clock_probe.py
node eventfield/scripts/check_journal.mjs
```

### Input layout

| Directory | Required files |
| --- | --- |
| TNG | `cluster_mergers.hdf5`, `snapshot_redshifts.json` and the reproduced row-5 `event_summary.json` |
| Gas gallery | `gas_{x,y,z}.png` and `xray_{x,y,z}.png` as defined in the [manifest](../research/multiwavelength-gallery-subhalo0/manifest.json) |
| Radio gallery | `{x,y,z}.png` as defined in the [manifest](../research/relic-gallery-subhalo0/manifest.json) |
| FITS | `{macs,g181,g099}-{t50,t50sub}.fits` and `rrsamp.tsv` |

The FITS inputs come from the [LoTSS Planck-cluster release](https://lofar-surveys.org/planck_dr2.html). Use the exact two members for each field pinned in the [two-field methods](../research/two-cluster-physical-beam/README.md) and [Abell 1925 methods](../research/g099-paired-positions/README.md), with these short local filenames. The exporter checks all six image hashes and the relic table hash. The survey cutouts, original gallery images and complete catalog tracks stay in the git-ignored local cache.

If present, `additional-catalogs/TNG-Cluster_Catalog.hdf5` under the TNG input folder adds the 352-cluster field inventory. Wide radio views use the same source maps as the original estimator. The exporter rotates the local grid along the two relic seeds at the native pixel spacing. The quiet display stretch changes appearance only.

The [journal run format](journal/runs/README.md) explains evidence receipts and the GitHub file convention. The journal shows local entries offline and can read new run notes from the draft research branch. The clock probe uses versioned CSV tables and runs with the Python standard library.

## Measurement conventions

- **Catalog.** The corrected HDF5 input has 2,083 rows, 346 distinct primary halo IDs with recorded events, and 133,751 valid position and velocity frames. The parent simulation has 352 target zooms. Relative positions use the shortest periodic displacement in the 680,000 ckpc/h box, then scale by `a/h` to proper kpc. Velocities use secondary minus primary peculiar velocity in km/s. Cosmic ages use the snapshot redshifts and a flat matter-plus-Λ cosmology with H₀ = 67.74 km/s/Mpc and Ωₘ = 0.3089.
- **Frame.** The primary is fixed at the origin for the relative view. The sign of line-of-sight velocity follows the camera depth axis. First passage jumps to `Snap_coll`, the stored snapshot following first pericenter. The site reports the separation recomputed from the relative position history.
- **Gravity experiment.** The initial relative vectors and sum of the two subhalo masses come from one snapshot. The softened potential is `−G M / sqrt(r² + ε²)` per unit reduced mass. Velocity Verlet advances the system at 1 Myr steps for 1.8 Gyr. The residual is normalized to the sum of the magnitudes of the seed kinetic and potential energies. This fixed-mass model is an educational comparison.
- **Radio.** The exporter brings each radio map to a common nominal 135 kpc beam, resamples T50 onto T50SUB and retains both native-grid cutouts. It reads the catalog center seeds as ICRS, matching the reference scripts, and transforms them to FK5 J2000 map coordinates. The browser estimates flux-weighted centers for each map and converts spherical separation to proper kpc with H₀ = 70 km/s/Mpc and Ωₘ = 0.3. The display stretches flux with asinh. Measurements use the linear image values. The signed difference is T50 minus T50SUB, a processing sensitivity on shared observations.
- **Gallery.** The hero crops rendered images of snapshot 99 halo 0 for display. The original image and color scale are available from the gallery link. Relating visible emission to a particular passage requires a registered time series.

The reference-row check reproduces 95.4061 proper kpc and 3,689.6624 km/s at snapshot 70 of row 5. The radio verifier checks all 27 reference settings across the three fields against saved research tables. The browser uses the same engine for those settings and for intermediate settings.

## Browser verification

Chromium checks on 22 November 2026 exercised the gallery, event search and sorting, orbit playback and camera controls, gravity parameters, both CSV exports, radio settings, research citations and measurement links. Layout checks covered 1,440, 390 and 320 px widths. A human comprehension review remains pending.

The expanded radio and journal views were also checked at those widths. The 30° clock example returned to the exact same reading after a change to 0°. The projected reading stopped beyond the calibrated interval. A test note persisted through reloading in an isolated browser.

## Sources

- [TNG-Cluster overview](https://arxiv.org/abs/2311.06338), [IllustrisTNG data release](https://arxiv.org/abs/1812.05609), and [Cluster Mergers catalog and specification](https://www.tng-project.org/data/cluster/). The catalog accompanies the [Lee et al. radio relic analysis](https://arxiv.org/abs/2311.06340).
- [Botteon et al. observation and imaging methods](https://arxiv.org/html/2202.11720), [Jones et al. relic measurements](https://arxiv.org/html/2301.07814), and the [LoTSS-DR2 cluster release](https://lofar-surveys.org/planck_dr2.html).
- [Lee et al. simulated merger clock](https://arxiv.org/html/2510.21632), [Stroe et al. X-ray analysis](https://arxiv.org/html/2501.07651), and [Ahn et al. weak lensing](https://arxiv.org/html/2501.09067) provide the forward-model references.
