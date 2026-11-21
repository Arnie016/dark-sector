# C-15 | TNG-Cluster X-ray offset semantics and projection gate (2026-11-04)

**Status: DERIVED + SIMULATION_RESULT (official simulated-catalog excerpt) + DATA_INSUFFICIENT. Not a SIDM detection or population inference.**

## Question and verified correction

Can the public z=0 TNG-Cluster catalog fields `peakoffset_xray_x/y/z` be treated as signed Cartesian components of a 3D gas–dark-matter displacement? **No.** These are three viewing-direction measurements of the *magnitude* of the projected X-ray-peak-to-galaxy positional separation, stored as log10(proper kpc). The TNG team specifies a 0.5–2 keV X-ray map, +/-r500 aperture, 3r200c projection depth, shrinking-circle peak finder, and galaxy location from `SubhaloPos`. A negative logged value is a small **positive** distance, not a negative offset. This does **not** measure the weak-lensing mass peak.

**Primary references:** [TNG team clarification (18–20 Aug 2025)](https://www.tng-project.org/data/forum/topic/997/tng-cluster-x-ray-offset-clarification/); [official z=0 property table](https://www.tng-project.org/files/TNG-Cluster_Catalog.txt), header lines 36–41 and rows 43,44,45,50; [documentation](https://www.tng-project.org/data/cluster/); [Nelson et al. (2024), arXiv:2311.06338v2](https://arxiv.org/html/2311.06338v2). The public catalog lists last update **6 March 2025**.

## Single reproducible small calculation

A deliberately selected excerpt was manually transcribed from the *public HTML text view* of the official tabular catalog, **not** a downloaded complete file. First three parent IDs 0,1,2 plus parent 7 for a negative-log control. Convert each `q=log10(d/pkpc)` to projected positive scalar distance `d=10**q pkpc`.

| Parent ID | z=0 properties haloID | (x,y,z) log10(pkpc) | (x,y,z) pkpc, rounded | max/min across views |
| --- | ---: | --- | --- | ---: |
| 0 | 0 | 0.23, 0.67, 0.55 | 1.70, 4.68, 3.55 | 2.754 |
| 1 | 252455 | 1.91, 2.81, 1.84 | 81.28, 645.65, 69.18 | 9.333 |
| 2 | 476245 | 1.41, 2.29, 2.23 | 25.70, 194.98, 169.82 | 7.586 |
| 7 | 1431487 | -0.05, -0.29, -0.09 | 0.891, 0.513, 0.813 | 1.738 |

For parent ID 1, the maximum/minimum ratio is `10**(2.81-1.84)=9.33`. Different views of **the same simulated halo** must not be treated as independent halos or combined as a Cartesian norm. Negative `-0.29` corresponds to **+0.513 pkpc**. These four chosen entries are SIMULATED astrophysical model outputs, not telescope observations. They are neither a representative population estimate nor a direct SIDM test.

## Execution and limits

One local Python 3 standard-library worker, hard 20-second timeout, exit 0, external wall 1.302 s, deterministic/no seed; tests for row IDs, log-ratio identity, positivity and negative logs passed. SHA-256: script `e68b61e0cba672e04a97c8f12825f92560c7fa971e2d19511e641e73f43a0d37`; transcribed input CSV `741273effa69ae476ffbf13c00a1f0da575000cc9408f1c00682764086a68b7b`; generated JSON `0ef35bff3c18a41dcfd711284b49f17e0b46a235965d12ba7713020533b6e7ab`. Executable and output are in a local companion only; not published by this commit. Full catalog bytes, private Azure catalogs, independent X-ray and lensing maps, and a calibrated likelihood were NOT loaded.

**Stop rule:** never interpret these X-ray-to-galaxy offsets as lensing mass–gas offsets or a dark-matter cross-section signal. Next load and hash the full official catalog, establish independent halo/progenitor mapping before joining merger `HaloIDs` to property `haloID`, and obtain matched simulated lensing maps under identical sightlines and selection. Alternative ordinary causes include projected gas structure, mergers, and feedback. The June 26 2026 `Mhistory_vel` correction is a separate version gate. C-03 globally unscreened gravity remains **FAILED**. No novelty claim: TNG's 2025 forum already clarified the field semantics.

Learning checkpoint: projected scalar versus vector, log magnitude versus negative distance, X-ray peak versus gravitational mass peak **INTRODUCED; comprehension NOT_ASSESSED**.
