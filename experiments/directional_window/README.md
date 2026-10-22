# D-01 | Can a sidereal dark-matter signal survive an ordinary daily background?

**22 October 2026. Claim D-01-F1: DERIVED + SIMULATION_RESULT; detector inference DATA_INSUFFICIENT.**

[Executable study](run.py) | [Research and learning checkpoint](CHECKPOINT.md)

## The question and AHA

A Galactic-direction-dependent dark-matter signal could repeat every **sidereal day** (approximately 23 h 56 min), while temperature or laboratory operations often repeat every **mean solar day** (24 h). These periods differ by just 0.2738%.

**AHA, an explanatory insight rather than a discovery:** Two different physical clocks can be mathematically distinguishable yet observationally nearly identical during a short or interrupted run. Calendar duration is not a measure of *identifiable* signal information.

## One mathematical tool: nuisance projection

For live hourly bin centers at time t (mean solar days), describe an unknown-phase sidereal rate through two columns S = [cos(omega_sid t), sin(omega_sid t)]. Describe ordinary nuisance rates through X = [1, cos(omega_sol t), sin(omega_sol t)]. Rows represent time bins, not quantum states, crystal tensor components or event probabilities.

The frequencies are omega_sol = 2*pi radians/mean-solar-day and omega_sid = 2*pi*1.00273790935 radians/mean-solar-day. The two sine/cosine coefficients represent a freely chosen phase and amplitude. The actual rate remains positive because this audit assumes modulation amplitudes small compared with the mean count rate.

In the high-count Poisson approximation at constant background per live hour, the nuisance-fit projection is

\[
P_X=X(X^T W X)^{-1}X^T W .
\]

Here W is diagonal with live-time/exposure weights. The information about sidereal rate amplitudes remaining after fitting the ordinary solar modulation is H = S^T W (I-P_X) S. The ideal information with a known solar background is G = S^T W S. The two eigenvalues of G^(-1/2) H G^(-1/2) are the **worst and best fractions of retained Fisher information over signal phases**. A Fisher matrix measures the likelihood's sensitivity to parameters, not a gravitational tidal potential or material response. The code uses numerically stable QR projection, without forming the large projection matrix.

## Bounded deterministic SIMULATED calculation

| Calendar span | Full-time live: information fraction range | Invented outages: fraction range |
|---|---:|---:|
| 30 days | 0.021861 to 0.022119 | 0.015035 to 0.034979 |
| 77 days | 0.137274 to 0.138569 | 0.091884 to 0.190615 |
| 180 days | 0.581895 to 0.584174 | 0.484361 to 0.661832 |
| 365 days | approximately 1.000000 | 0.999968 to 0.999979 |

For 77 days of uninterrupted hypothetical observations, **only ~13.7% of the idealized sidereal Fisher information remains** after profiling a free-phase solar-day background plus constant rate. The corresponding relative amplitude signal-to-noise for a fixed observing window is sqrt(0.1373) = 0.371. This is **not** a 13.7% modulation, a particle cross-section limit or a discovery significance.

The invented outages retain hours 01:00-18:59 each day and remove days where d mod 17 is 6,7,8 or d mod 31 is 15. They are NOT an approximation to a real detector's run log. No event counts were generated. The solar/sidereal beat period is approximately 365.24 mean solar days, which explains why a longer span helps distinguish the frequencies. Intermittent uptime also makes sensitivity depend on unknown signal phase.

The exact local NumPy script ran as one CPU process under a 25-second timeout with one worker, no random seed and 8 implementation/limiting checks passed. It writes a full JSON receipt containing software versions, units, generating assumptions, results and source/CSV SHA-256; it also emits an eight-row CSV. This is not an independent peer review, published signal forecast or event likelihood reproduction.

## Primary evidence checked

**Statistical theory:** Blanco, Foster, Kahn and Lillard, [arXiv:2602.15947v1](https://arxiv.org/html/2602.15947v1), **17 February 2026 preprint**, Secs. II, IV and V. Methods include inhomogeneous Poisson rate models, nuisance fitting and sidereal stacking. The present design matrix does NOT reproduce their trans-stilbene material response, Monte Carlo runs or claimed orientation improvements.

**Detector:** DAMIC-M, [arXiv:2511.13962v1](https://arxiv.org/html/2511.13962v1), **17 November 2025 preprint**, published [Phys. Rev. D 114, 032010](https://doi.org/10.1103/c9fm-ymf2) on **19 August 2026**. Its actual observations are from **October 2024 to January 2025**; methods report approximately 7 days developing cuts and approximately 77 days of blinded analysis, with 1.257 kg-day integrated exposure. CCD availability changes and temperature/segment background parameters matter. DAMIC-M reported no significant daily modulation. Its live-time vector, measured events and covariance were not retrieved or fitted. Choosing a 77-day synthetic span does NOT recreate the DAMIC-M likelihood or provide independent evidence.

## Falsifier and next gate

**Smallest claim:** under the stated rate and nuisance model, free-phase solar-day backgrounds can dramatically reduce information for a sidereal amplitude. **Strongest conventional null:** ordinary local 24h variability coupled to real exposure masks or an additional sidereal-linked systematic. **Reject a proposed detection** if the sidereal model fails to improve held-out prediction relative to conventional nuisances or if the actual exposure makes it unidentifiable.

**Required next measurement:** a publicly reproducible exposure/time-mask vector with temperature/background covariates, plus a material-specific energy-and-direction-dependent scattering model. Without these the conclusion remains DATA_INSUFFICIENT, not a dark particle detection. No purchase, outreach, publication submission or schedule change was made.
