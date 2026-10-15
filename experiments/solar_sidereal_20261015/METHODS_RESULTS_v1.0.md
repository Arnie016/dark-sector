# D-01: Solar versus sidereal modulation | 15 October 2026

**Version 1.0.0. Status: DERIVED + SIMULATION_RESULT; observational DATA_INSUFFICIENT.**
**All observations and masks in this study are SIMULATED.** No particle inference or DAMIC-M data reproduction.

## Question and sources

The mean solar day is 24 hours; the sidereal day is about 23 h 56 min 4 s. Their nearly coincident frequencies produce an approximately annual beat. Official definitions: [USNO](https://aa.usno.navy.mil/data/siderealtime), [NASA](https://www.grc.nasa.gov/www/K-12/Numbers/Math/Mathematical_Thinking/telling_time_by_the_stars.htm).

Blanco et al., [arXiv:2602.15947v1](https://arxiv.org/html/2602.15947), submitted 17 February 2026, derive Poisson/nuisance modulation likelihoods and sidereal stacking: the statistical principle is not new. DAMIC-M [Phys. Rev. D 114, 032010](https://journals.aps.org/prd/abstract/10.1103/c9fm-ymf2), published 19 August 2026, analyzed 1.257 kg-day in a roughly 77-day search sample taken October 2024 to January 2025; its [methods](https://arxiv.org/html/2511.13962) describe temperature-linked background and downtime. That publication reuses an older search dataset and models Earth attenuation in silicon, not anisotropic crystal excitations. No event timestamps or live-time are imported from DAMIC-M.

## Explanatory AHA: a modulation must survive nuisance projection

For bins indexed by i, let each row of the nuisance matrix N contain (1, cos 2πt_i, sin 2πt_i) where t_i is in solar days. Let S contain (cos ω_sid t_i, sin ω_sid t_i), where ω_sid=2π(1+1/365.2422). Let W be a diagonal expected-count weight including live time.

The profile Fisher information for two unknown-phase sidereal coefficients is

$$I_{\rm prof}=S^TWS-S^TWN(N^TWN)^{-1}N^TWS.$$

This subtracts candidate patterns that a free solar background can imitate. Eigenvectors label candidate phases, eigenvalues their local distinguishability. Example: s=(1,0) and constant nuisance n=(1,1) leave s_perp=(1/2,-1/2), halving squared norm under equal noise. If both clocks are exactly equal, all S columns lie in the nuisance span: I_prof=0, an **UNIDENTIFIABLE** limit.

## Bounded SIMULATED result

One deterministic NumPy calculation, 10 checks passed, no random seed. Hourly bins; 30, 77, 180, 365 days; uniform or invented gapped live time. Generating truth: 4% solar cosine, zero sidereal modulation, arbitrary 100 baseline counts per live hour. False sidereal amplitude is a deliberately misspecified fit *omitting* solar terms. Retained info is the weakest eigenvalue fraction relative to fitting only a constant nuisance.

| Days | Invented mask | Retained sidereal information | False sidereal amplitude |
| ---: | --- | ---: | ---: |
| 30 | uniform | 2.19% | 3.95% |
| 77 | uniform | **13.73%** | **3.71%** |
| 77 | gapped | **12.45%** | **3.69%** |
| 180 | uniform | 58.19% | 2.59% |
| 365 | uniform | approximately 100% | 0.003% |

The correct solar+sidereal Asimov fit recovers sidereal amplitude below 1e-11, but that does not establish real detector sensitivity. The gapped mask drops 02:00-04:00 daily plus predetermined multiday and weekly interruptions. It is **not** DAMIC-M uptime.

**Falsifiable claim:** ordinary 24 h background can mimic sidereal modulation over short runs when omitted from the likelihood. **Strongest null:** thermal/readout cycling with uneven uptime. **Stop:** no dark-matter cross section, significance or physical forecast without real exposure/temperature streams and calibrated particle/material response. If the nuisance-inclusive likelihood stays degenerate, report UNIDENTIFIABLE.

Next: check whether data products include time-stamped exposure and temperature measurements, then evaluate held-out full likelihood with justified response.

Code and generated output are included in this experiment folder. No external contact, manuscript submission or scheduling change.
