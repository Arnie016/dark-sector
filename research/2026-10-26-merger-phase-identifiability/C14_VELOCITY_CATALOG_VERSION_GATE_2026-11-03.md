# C-14 version gate | corrected TNG-Cluster merger velocities (2026-11-03)

**Status:** DATA_INSUFFICIENT for observational/simulation reproduction; **VERIFIED SOURCE CORRECTION** for the data provenance. This is not a new SIDM result or re-run of C-14's numerical illustration.

## Bounded question and decision

**Question:** Can the previously proposed consistency test between TNG-Cluster merger orbits and catalog relative velocities be interpreted before verifying the catalog version?

**Decision: no.** The TNG project's own chronological change log states that on **26 June 2026** Wonki Lee corrected an error in the **`Mhistory_vel`** field of the **Cluster Mergers** supplementary catalogs for both **TNG-Cluster and TNG300-1**. The notice confirms that older `Mhistory_vel` values were incorrect but does **not** specify the numerical error, its distribution, or which events were affected. We therefore cannot calculate its effect on any merger from documentation alone.

Primary source: [IllustrisTNG chronological change log](https://www.tng-project.org/data/forum/topic/2/changes-and-additions/) (entry dated 26 June 2026). Cross-check: [TNG-Cluster supplementary catalog documentation, section 5(g)](https://www.tng-project.org/data/cluster/), which defines `Mhistory_vel` as the main and secondary subhalo velocities, with shape `[N,70,6]`, in km/s. Its corresponding `Mhistory_orbit` has comoving positions in ckpc/h, while `Mhistory_snap` identifies the snapshots.

The related documentation describes **2,083 merger events** in TNG-Cluster and **289** in TNG300-1. These are catalog entries, not independent observational detections.

## Why this changes our scientific decision

C-14 proposed checking whether the finite-difference derivative of the *proper* halo separation,
`R(t)=a(t)|x_s(t)-x_m(t)|/(1000 h)` Mpc, is consistent with the physical radial rate
`dR/dt = H(z)R + n·(v_s-v_m)`, where `n` points from main to secondary, `v` is the peculiar catalog velocity in km/s, and `H(z)` is in km/s/Mpc.

The equation is an exact frame-conversion identity in the declared coordinate convention, but evaluating a velocity residual with an **uncorrected** `Mhistory_vel` could produce apparent discrepancies that are entirely due to the published catalog error. Even with the corrected field, finite-snapshot derivatives, velocity interpolation, subhalo identification, and accelerating orbits must be handled before interpreting a residual.

**Strongest ordinary explanations for a large residual:** stale catalog; snapshot mismatch; finite-difference truncation; coordinate/velocity unit error; incorrectly selected subhalos or invalid `-1` history entries. No residual is presently measured, so none of these is diagnosed.

## New gate, with explicit stop rule

1. Download the current `cluster_mergers.hdf5` **after account activation** through the legitimate TNG data interface. Record download timestamp, source URL, raw SHA-256, size, and any server `Last-Modified` metadata. Do not assume a local filename or older cached copy is current.
2. Open with HDF5 tooling, verify `Mhistory_snap`, `Mhistory_orbit`, and `Mhistory_vel` shapes, units, invalid-entry conventions, and exact event identifiers. Preserve dataset hashes and source metadata.
3. Validate a **single independently selected merger** against direct subhalo snapshot fields for a few valid matching `Mhistory_snap` values. This is more diagnostic than directly testing finite differences and blaming physics.
4. Only after a catalog-to-snapshot value match, compute a frame-consistent, time-centered finite-difference residual with explicit cadence/truncation uncertainty. Do **not** use uncalibrated discrepancies as SIDM evidence, or treat catalog halo motion as radio-relic shock motion.

**Stop:** if the corrected catalog cannot be read or matched to at least one original snapshot, status remains DATA_INSUFFICIENT, with no halo-orbit baseline reproduction claimed. Catalog and snapshots are correlated outputs of the same simulation, so this is a consistency check, not independent physical validation.

## Execution, continuity and learning

No scientific worker, new fit, observation, or synthetic data were run on 3 November. The official source correction was read directly and compared with the C-14 note at PR #11 head `6abc47c5502d2ac09d36382f7e709dcfdfeab18f`. Neither the catalog bytes nor the alleged pre-correction error magnitude were accessible, so no quantitative bias can honestly be assigned. C-03 globally unscreened gravity remains FAILED. C-12/C-13 gas-flow and projection ambiguities remain distinct. Learning: source versioning versus physical model error **INTRODUCED**, user comprehension **NOT_ASSESSED**.

This is a correction to the prerequisites of C-14, not a discovery or independent peer review.
