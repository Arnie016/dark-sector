# D-01 | Sidereal versus solar-time alias under masked exposure

17 October 2026. `DERIVED` + `SIMULATION_RESULT`; experimental inference `DATA_INSUFFICIENT`.

**Question:** A daily event-rate modulation can arise from a Galactic sidereal pattern or a mundane solar-clock background. When only certain hours are observed, how well can we separate the two?

The sidereal day is about 86,164.09 seconds, versus 86,400 seconds for the solar day. In a background-dominated Poisson model, the time-template Fisher matrix has entries F_ab = sum_i (e_i/b0) X_ia X_ib, where e_i is the live kg-day exposure and X columns are constant, solar cosine/sine and sidereal cosine/sine. Fitting unknown solar background rates leaves a sidereal Fisher matrix equal to **F_SS - F_SN F_NN^{-1} F_NS**, the Schur complement. This is a projection of nuisance-shaped variations, not a physical scattering calculation.

**SIMULATED:** one executed deterministic process compared continuous 1-kg exposure and an invented 21:00-05:00 solar-clock window with every 11th day offline, at 15-minute time steps. Generating baseline 100 events/(kg day), solar amplitude 15 and sidereal amplitude 8 events/(kg day), both phases fixed. No random events were drawn. These are noiseless Asimov expected-rate templates, not measurements.

| Elapsed days | Full uptime, worst sidereal information retained | Window + downtime, worst information retained |
|---:|---:|---:|
| 30 | 2.19% | 0.88% |
| 90 | 18.37% | 8.65% |
| 180 | 58.19% | 40.69% |
| 365 | ~100% | ~100% |

Percentages normalize to the **same observation mask before solar-background profiling**. The 365-day restricted window still collects only 110.33 kg days rather than 365 kg days, so it does not have equal detection power. Ignoring the solar component in a solar-only injected 90-day continuous run yields a spurious 13.54 events/(kg day) sidereal amplitude. Including both harmonics removes it from noiseless expected rates, but large statistical uncertainty remains for close frequencies. The code passed 10 algebraic and limiting checks, including exact-frequency unidentifiability. It did not compute a p-value, material response or actual experimental sensitivity.

**Claim D-01-C1 (`DERIVED`):** the sidereal Fisher information after fitting the solar harmonic nuisance is the Schur complement. **D-01-C2 (`SIMULATION_RESULT`):** 90-day invented night window retains 8.6461% of worst-phase relative information. **D-01-C3 (`DATA_INSUFFICIENT`):** real calibrated timestamps, effective exposure and temperature covariates have not been recovered; no DAMIC-M limit is reproduced.

**Primary sources inspected:** Blanco et al., [arXiv:2602.15947v1, 17 February 2026](https://arxiv.org/html/2602.15947v1), Sections II-III, V-VI; DAMIC-M [arXiv:2511.13962v1](https://arxiv.org/html/2511.13962v1), Sections II-III, peer-reviewed [19 August 2026](https://journals.aps.org/prd/abstract/10.1103/c9fm-ymf2). DAMIC-M used 1.257 kg days acquired Oct 2024-Jan 2025, a ~77-day blinded search with temperature-correlated background and interruptions. Its model-dependent signal is Earth shielding, not the crystal-orientation mechanism. Its published absence of significant 1e- modulation over 1-48 h is **their** result, not our simulated data.

**Strongest null:** temperature-linked solar background plus time-dependent detection efficiency. **Stop** without a real observation mask and calibrated background model. Next work unit: independently reproduce one official background-only time-domain result before any cross-section calculation. Original executable [run.py](run.py), identical to the locally verified source SHA-256 `0de9ba4678add9af7ead5d510a69d1a982a1568d85cd7d37b3c266fca7b1d437`. The extended methods and high-resolution SIMULATED plot are in the chat research archive. No prior experiment, failure or PR was overwritten.
