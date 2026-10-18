# D-01A | Solar-day background aliasing with a sidereal signal

**18 October 2026.** Claim D-01A-C1: DERIVED. Window comparison: SIMULATION_RESULT. Physical particle sensitivity: DATA_INSUFFICIENT. No actual event data, detector-response calculation, observation or discovery is claimed.

## Physical question
Will a 24-hour detector background masquerade as a sidereal dark-matter modulation when live times cover only part of the year? Sidereal rotation is 86,164.0905 s versus the defined solar day 86,400 s. The phase difference is only 235.9095 s per day. A 77-day contiguous campaign spans barely five hours of accumulated phase drift; this can leave very similar timed predictions despite different frequencies.

## Primary sources, status and overlap
- Blanco, Foster, Kahn and Lillard, *Statistics of Daily Modulation in Dark Matter Direct Detection Experiments*, [arXiv:2602.15947v1](https://arxiv.org/html/2602.15947), posted 2026-02-17. Sections II, III and V examined; known Poisson likelihood, Fisher forecasting, background harmonics and **shifted sidereal stacking**. Their material response is not reproduced. The wind phase itself varies annually.
- DAMIC-M Collaboration, *Daily Modulation Constraints on Light Dark Matter with DAMIC-M*, [arXiv:2511.13962v1](https://arxiv.org/html/2511.13962), posted 2025-11-17; published 2026-08-19 in Phys. Rev. D, DOI [10.1103/c9fm-ymf2](https://doi.org/10.1103/c9fm-ymf2). Sections II-III examined. Existing 2024-10 to 2025-01 exposure is reused, not new 2026 data. About 77 search days and a 28-minute charge-image cadence were described. The experiment reports temperature-correlated single-electron backgrounds plus hardware changes. Its physical DM mechanism is Earth attenuation, not the same as intrinsic anisotropic-crystal scattering. No timestamps or likelihood were recovered or fitted.

## Mathematical tool: weighted nuisance projection
In time bin i let s_i be the sidereal fractional template, b_i the solar fractional template, w_i the expected background count. A template is a vector of **predicted count changes**, not a quantum state.

Define <s,b>_w = sum_i w_i s_i b_i. The solar nuisance consumes the component of s parallel to b:
s_perp = s - (<s,b>_w / <b,b>_w) b.
For a known phase, Fisher information after profiling is
I = <s_perp,s_perp>_w = I0 (1-rho^2).
This follows by directly expanding the weighted square. Here rho is the normalized overlap of predicted patterns, not a particle-detection probability.

Real unknown phases need two columns each for cosine and sine. Seven segment baseline offsets are also nuisances. With X_s as two sidereal columns, X_n as nine nuisance columns and W as expected-count weights, the profiled Fisher matrix is

F = X_s^T W X_s - X_s^T W X_n (X_n^T W X_n)^(-1) X_n^T W X_s.

The implementation computes the same Schur complement via QR, avoiding an explicit inverse. F0 first profiles only the seven segment means. The smallest eigenvalue of F0^(-1/2) F F0^(-1/2) gives the worst retained information fraction for any sidereal phase direction. Exactly coincident solar and sidereal frequencies make the sidereal columns lie in the solar nuisance span, yielding zero information, UNIDENTIFIABLE in this restricted model.

## One deterministic SIMULATED study
Seven windows of 11 nominal days. Contiguous starts: days [0,11,22,33,44,55,66]. Season-spread starts: days [0,52,104,156,208,260,312]. Both omit 02:00-04:00 daily and two extra days in the fourth window. Each yields 3,300 live half-hour bins, equal to 68.75 uninterrupted days. Expected synthetic background count sum is 82,445. Arbitrary per-segment baseline factors [.97,1.05,.94,1.08,1,.95,1.02] are used. These are NOT DAMIC-M exposure masks or counts.

| Metric | Contiguous | Season-spread |
| --- | ---: | ---: |
| Calendar span (days) | 77 | 323 |
| Worst retained Fisher information | 0.119865 | 0.999641 |
| Maximum solar/sidereal overlap | 0.938155 | 0.018958 |
| Formal weakest-direction sigma inflation | 2.69446 | 1.000174 |
| Naively fitted sidereal amplitude from a 4% solar-only Asimov truth | 0.037965 | 0.000793 |
| Jointly fitted sidereal amplitude from solar-only truth | < 1e-12 | < 1e-12 |
| Recovered 2% sidereal-plus-solar Asimov injected amplitude | 0.020000 | 0.020000 |

The solar-only Asimov data contain zero true sidereal component. This is **not** a significance estimate, a false discovery probability or a material sensitivity curve. Exact joint-model recovery in a noiseless Asimov dataset does not establish statistical power with real counts.

Source: [run.py](run.py), frozen [results.json](results.json). NumPy implementation was executed in one CPU process with finite checks and no stochastic samples. SHA-256 of executed source bytes: 80ecbe76e1b1ebc0d6bd19eb57bbc639be4577d584ca61fecdc19ed2aac55547. Two initial prototype JSON serialization errors were corrected before publishing the canonical result. The compact code was executed and matched the prototype's physical numbers. Automated checks are not independent scientific validation.

## Falsifier and controls
Strongest null: solar-linked temperature or IR leakage plus acquisition changes and exposure timing produce the apparent sidereal pattern. A correctly specified joint fit removes it in the synthetic null. The sinusoidal toy is not a substitute for an observed background response. Real dark-matter winds vary annually, and fixed phase is inadequate for a multi-season detector likelihood.

The next useful dataset must contain true time stamps, masks, temperature/threshold logs, per-channel event counts and a calibrated material/time response. Fit full nuisance terms, then hold out independent seasons. If sidereal excess vanishes after nuisance profiling, reject the claimed discriminator. Without real detector response or exposure logs, stop with DATA_INSUFFICIENT. Do not infer a cross section, modulating detector capability or particle discovery.

## Continuity and learner checkpoint
Repo main inspected at b6b85682 with open PRs #4-#8; no PR overwritten. Previous C-03 constant-range unscreened gravity benchmark remains FAILED at Solar-System tests. D-01 was NOT_EVALUATED. This D-01A addition gives a bounded synthetic timing diagnostic only. Old named September archives were searched via Files but not recovered. Relevant primary methods coverage inspected through the 2026-08-19 DAMIC-M publication. Learning concepts introduced: nuisance projection, phase degeneracy, live-time weighted information. Learner demonstration remains NOT_ASSESSED. No schedule change, external outreach or manuscript submission.
