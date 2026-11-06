# C-14 | TNG-Cluster orbit frame-consistency gate (2026-11-02)

**Claims:** C14-C1 DERIVED; C14-C2 SIMULATION_RESULT (arithmetic check, invented state); C14-C3 DATA_INSUFFICIENT (no actual simulation arrays accessed). **Not** an observational SIDM constraint, tracked shock-front simulation, or new theory.

## Decision: can the public merger catalog directly supply a shock clock?

The [official TNG-Cluster supplementary catalog](https://www.tng-project.org/data/cluster/) records 2,083 merger events, with collision-axis vectors, merger timestamps `T_coll` and `TSC_full`, plus 70-snapshot `Mhistory_orbit` and `Mhistory_vel` arrays. It describes **halo-orbit trajectories**, not a tracked radio shock surface. A direct request for `cluster_mergers.hdf5` could not be authenticated: the web request returned 403 and the separate direct download failed. No source data were downloaded, parsed, fitted or simulated here. The [official data downloads page](https://www.tng-project.org/data/downloads/TNG-Cluster/) states that access requires login. These public fiducial-TNG halos are not a matched SIDM/CDM sample.

The concrete methodological issue is that `Mhistory_orbit` stores comoving subhalo positions in `ckpc/h`, while `SubhaloVel` is **peculiar velocity** in km/s. The latter does not contain the expansion contribution to the time derivative of *proper* pair separation. The [TNG field specifications](https://www.tng-project.org/data/docs/specifications/) explicitly distinguish these conventions.

## Physical derivation

Let `a=1/(1+z)` and `h=0.6774`. Let `Delta x` be the comoving separation vector in ckpc/h. The proper physical vector in Mpc is:

`r = a Delta x / (1000 h).`

Write its radial magnitude as `R=|r|` and its unit vector `n=r/R`. Differentiating the scale-factor product gives, in consistent physical units:

`dR/dt = H(z) R + dot(n, v_pec,secondary - v_pec,main).`

The first term is the apparent separation rate arising from expansion of the coordinate scale. The second is peculiar radial relative motion. `H(z) = H0 sqrt(Omega_m(1+z)^3 + Omega_Lambda)` for flat matter-plus-Lambda cosmology at low redshift, using the official TNG-Cluster parameters `H0=67.74 km/s/Mpc`, `Omega_m=0.3089` and `Omega_Lambda=0.6911`. This is coordinate kinematics, **not** an extra physical force on bound cluster halos; do not add it to proper-position finite differences twice.

## Bounded numerical illustration

**All positions and velocities in this example are SIMULATED assumptions**, not observations or sampled TNG outputs: at `z=0.3`, let the proper separation be `R=2 Mpc` and outward radial *peculiar* relative speed `v_pec,r=1500 km/s`. The calculation gives:

| Quantity | Calculated |
|---|---:|
| Scale factor | 0.7692307692 |
| Comoving catalog-style separation | 1761.240 ckpc/h |
| Hubble rate `H(z)` | 79.280498 km/s/Mpc |
| Expansion contribution `H(z)R` | 158.560996 km/s |
| Physical radial separation rate | 1658.560996 km/s |
| Instantaneous `R/v_pec,r` proxy | 1.303723 Gyr |
| Instantaneous `R/(dR/dt)` proxy | 1.179085 Gyr |

Omitting the coordinate term underestimates the **instantaneous proper separation rate** by about **9.56%** of that rate in this numerical illustration. The difference between the crossing-time proxies is about 0.124638 Gyr, **not** a merger age estimate: trajectories accelerate, shock surfaces evolve separately, and true time since pericenter is available as a different catalog quantity.

Limiting checks: at `z=0`, `H=H0`; a pair fixed in comoving coordinates still separates in physical coordinates as `HR`; a sufficiently large negative peculiar radial speed produces physical infall.

## Execution receipt and provenance

One ChatGPT Linux Python 3 standard-library process under a hard 20-second timeout exited **0**; **10 implementation and limiting assertions passed**. No random seed. Executed source SHA-256: `168c900b2a05a83e08363489565b1b89631ae3eab3538c757d13106d1bcaccce`. Raw results SHA-256: `862beac5aac809668c66f0286bbcc746d81a7d91174061258286da4bbc2ef4d0`. Original executed `C14_frame_consistency.py`, `C14_results.json` and companion methods were locally archived; this GitHub note contains the full derivation and key outputs, **not the executable**. No CI or independent reproduction is claimed.

## Falsifier and next gate

Acquire the authenticated, relatively small merger-orbit supplement using a legitimate TNG account. Validate sentinel values, snapshot times, original zoom IDs and contamination. For one independently selected merger, compare finite differences in `a Delta x/h` against `HR+dot(n,Delta vpec)`, allowing for finite snapshot cadence. Nontrivial residuals after alignment indicate either a wrong unit convention, timestep mismatch or other missing catalog physics. This must be resolved before training a world model on the orbit catalog. **Only later** reconstruct actual shock fronts from appropriate gas-cell snapshots, compare them to the orbital history, and consider matched CDM/SIDM simulations. Do not treat tracer `SHOCKMACHNUM_MAX`, a maximum since the previous full snapshot, as an instantaneous shock trajectory.

**Research continuity:** C-03 globally unscreened gravity FAILED; C-06/C-08 geometry degeneracies, C-09/C-10 calibration, C-11 bounded clock mismatch, C-12 gas velocity reference frame and C-13 LOS projection remain separate. **Learning:** comoving vs proper coordinates introduced, mastery NOT_ASSESSED. **Digestibility self-score** 9/10 (user-facing sketch, definitions, one scale, limiting cases, truth labels; real orbit visualization missing), not a scientific validity score.

