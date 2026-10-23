# D-07 | Solar versus sidereal aliasing under missing exposure

**23 October 2026 · DERIVED + SIMULATION_RESULT + DATA_INSUFFICIENT**

**Question.** Can an apparent daily dark-matter signal be a conventional 24-hour background when detector uptime is uneven? We used one deterministic, expressly **SIMULATED** hourly counting model. This is a bounded implementation of established time-series identifiability methods, **not an observed signal or a new physical theory**.

**AHA (explanatory, not novel).** A solar day takes 24 h; a sidereal day about 23 h 56 min. Their waveform phases separate by only ~3 min 56 s per calendar day. The same local hours, observed for only two weeks, do not span enough relative phase to determine whether a weak near-daily oscillation is solar or sidereal. A longer calendar baseline breaks that degeneracy in this ideal stationary model. More recorded counts within the same short phase window are not equivalent to new directional information.

## A testable mathematical tool

Each row of the observed design matrix is a **live one-hour interval**. Columns represent expected waveforms at that timestamp. For a time t in mean solar days define background B=(1, cos(2πt), sin(2πt)) and sidereal S=(cos(2π f*t), sin(2π f*t)), where f=1.00273790935 cycles per solar day. Background phase is freely fitted through the two solar columns. Sidereal phase is freely fitted through the two signal columns. With an expected Poisson background of mu counts per bin, the weight matrix is W=diag(1/mu). Profiling out the background gives the familiar *Schur complement*:

F_signal|background = S^T W S - S^T W B (B^T W B)^(-1) B^T W S.

This is the information that remains **after removing all parts of the sidereal shape that the background can imitate**. An exactly identical candidate signal and nuisance have zero remaining information, so that model is UNIDENTIFIABLE from these count times alone. Stable QR projections implement this without explicitly calculating the nuisance inverse. The generalized eigenvalues of this matrix relative to a constant-only background quantify *retained information fractions*. They are neither dark-matter modulation fractions nor discovery significance.

## Actual bounded execution

The generating truth is **SIMULATED**: a solar-only 10 counts/live-hour background with 18% sinusoidal modulation and a fixed phase 0.37 radians. **True sidereal amplitude = 0**. The schedule is deterministic: weekdays 07:00 to 18:59 only, with outages on days where day modulo 13 is 4 or day modulo 29 is 6. Continuous-uptime intervals are controls. Calendar spans are 14, 60, 180 and 365 days. No random Poisson draws; the code uses exact expected bin counts (Asimov data), plus Poisson weak-signal Fisher information.

| Calendar span | SIMULATED live hours | Worst retained information fraction | Poisson-Fisher 1σ worst-phase coefficient error (counts/live-h) | Fake fitted sidereal amplitude if solar background omitted (counts/live-h) |
|---:|---:|---:|---:|---:|
| 14 days | 108 | **0.00488** | **6.20** | **1.767** |
| 60 days | 456 | 0.0962 | 0.677 | 1.413 |
| 180 days | 1,380 | 0.613 | 0.150 | 0.719 |
| 365 days | 2,784 | 0.99993 | 0.0804 | 0.00961 |

A *correct* model that also fits the solar background returns zero sidereal coefficient to floating-point accuracy for all eight tested scenarios. One-hour continuous-uptime control at 14 days has a better absolute worst-phase uncertainty, **3.51** instead of **6.20**, although retained information fractions are similar. Thus maximizing a normalized information fraction alone can reward a poor observing strategy with less live time.

**Execution receipt:** one deterministic Linux Python 3.13.5 / NumPy 2.3.5 process, 7 implementation/limiting checks passed, saved output and JSON readback passed, exit 0. Numerical core 0.0321 s (not including process startup). Executed run.py SHA256: e8ea5eefa8e10394ecdfef9a14fbf7fa7d637a044ab56792a4d86decc15dc8c9. Full original raw output and execution log are in the separately delivered chat companion package. This repository file must be hash-checked before claiming it is byte-identical to the executed source.

## Claims and limitations

- **D07-C1 DERIVED / KNOWN:** Schur-complement nuisance projection removes background-explainable waveform components. Identical signal/nuisance spans are unidentifiable.
- **D07-C2 SIMULATION_RESULT:** in the specified toy exposure mask, a mis-specified solar-only dataset falsely returns a near-sidereal coefficient in a short span. Profiling the solar nuisance removes the fake coefficient but leaves severe uncertainty. A year-long idealized span separates the two frequencies.
- **D07-C3 DATA_INSUFFICIENT:** no actual detector event times, physical crystal response, cross-section constraint, sky direction, selection efficiency or measured calibration was provided. Nothing here is a new detection or a validated sensitivity forecast.

**Limits of the model:** no seasonality, higher harmonics, drifting laboratory phase, position-dependent scattering, crystal anisotropy or real timestamp/dead-time metadata. DAMIC-M Earth-attenuation modulation is not identical to a crystal phonon angular-response model. The 2026 methods below already provide the general likelihood framework; this is a transparent special-case run, not claimed novelty.

## Primary source checks as of 23 October 2026

- Blanco, Foster, Kahn and Lillard, *Statistics of Daily Modulation in Dark Matter Direct Detection Experiments*, arXiv:2602.15947v1 (**17 February 2026, preprint**), methods §§II, V, VI inspected. https://arxiv.org/html/2602.15947v1 . This is direct prior art for nuisance profiling and sidereal stacking; its unstacked likelihood already allows arbitrary exposure.
- DAMIC-M Collaboration, *Daily modulation constraints on light dark matter with DAMIC-M*, *Phys. Rev. D* 114, 032010 (**19 August 2026**, peer reviewed), https://doi.org/10.1103/c9fm-ymf2 ; preprint arXiv:2511.13962v1, 17 November 2025. Abstract and setup/data read. Their 1.257 kg-day analysis reports no significant 1-electron modulation and **reuses** the dataset of a 2025 multi-electron analysis: not independent new exposure.
- Li and Zhang, *Logarithmic Wavelets for Dark Matter--Phonon Scattering*, arXiv:2608.06452v1 (**6 August 2026, preprint**), https://arxiv.org/abs/2608.06452 . Their VectorPhonoDark method is a source-grounded candidate for computing real material-dependent modulation curves, not used or run here.

## Continuity and next discriminating gate

The main branch remains at its 14 October research snapshot; open PRs #4–#8 carry the later neutrino and gravity work. N-06's 21 October corrected asymmetry-sign norm test is retained. C-03's globally unscreened f(R) benchmark remains FAILED under Cassini; no dark-sector discovery is implied here. Older original directional studies remain inaccessible. Historical September archive titles were searched in Library without recovering them.

**Research checkpoint:** D07-C1/C2 supported within assumptions; D07-C3 unresolved. **Learning checkpoint:** concepts introduced are solar vs sidereal phase drift, statistical design matrices and nuisance profiling; reader understanding NOT_ASSESSED. **Next one bounded step:** obtain a material-specific rate curve and the corresponding publicly released live-time mask; reproduce the source paper's background-only likelihood with those same inputs before forecasting sensitivity. Halt or report UNIDENTIFIABLE if calibrated background variations can reproduce the proposed signal.
