# DIR-20261019 | Sidereal versus solar attribution with interrupted exposure

**19 October 2026. DERIVED + SIMULATION_RESULT; DATA_INSUFFICIENT for actual dark matter.** No particle candidate, detector events, background measurement or cross-section bound is claimed.

## Question and AHA

If a detector's counts oscillate once per day, how could we distinguish a sky-fixed dark matter wind from temperature or another 24-hour laboratory background? The sidereal day is 86,164.09 seconds, 235.91 seconds shorter than a solar day. The phase difference accumulates one cycle per tropical year. A short run therefore has little statistical leverage, even when both mathematical frequencies are distinct.

Our deliberately minimal five-column time-design matrix has rows indexed by exposed hours:

\[
X_i=[1,\cos(\omega_\odot t_i),\sin(\omega_\odot t_i),\cos(\omega_*t_i),\sin(\omega_*t_i)].
\]

The first three columns are nuisance templates: baseline count rate and unknown-phase solar daily modulation. The last two form a sidereal first harmonic of unknown phase. Entries are unitless mathematical functions, not dark-matter rates or quantum amplitudes. When the detector is off, the row is removed. The Gram matrix measures overlap in these sampled template directions. It is a surrogate for equal-noise Gaussian information, **not** a calibrated detector likelihood.

Let S hold the last two columns, B hold the first three, and P_B project onto the column space of B. Compare the sidereal Gram after profiling solar nuisance, Gp = S^T(I-P_B)S, to G0, obtained after profiling only a constant. The smallest generalized eigenvalue is the worst-phase *information fraction*. Its inverse square root is the relative standard-error inflation at the same observed times under the assumed noise model.

## Executed SIMULATED demonstration

[Source code](run.py) and [numerical result receipt](results.json). One deterministic Python/NumPy CPU calculation, 20-second timeout, exit 0, ten checks plus JSON readback; one worker; no randomness, installs or paid services. The local source SHA-256 is 8c1cfd1e8c03f00a3c87f1bdbfb1da1f8a1ba86255d0c49a150112668b4d3558.

The modeled operating mask is 18:00–06:00 during the first five days of each seven-day week, with all other hours offline. Solar and sidereal sin/cos phases are fitted freely.

| Elapsed time | Live hours | Worst-phase fraction | Inflation relative to fixed solar nuisance |
| --- | ---: | ---: | ---: |
| 7 days | 60 | 0.000638924 | 39.56 |
| 30 days | 264 | 0.023479863 | 6.53 |
| 90 days | 780 | 0.190216834 | 2.29 |
| 365 days | 3132 | 0.999999813 | 1.00 |

These are **conditional fractions**, not an exposure-normalized sensitivity comparison: a detector live 36% of the time has fewer observations. The full-time schedule has seven-day fraction 0.001181 and full-year fraction 0.99999956. The five columns are full rank even after seven days, so the short-run issue is poor *practical* identifiability rather than exactly equal frequencies.

### Holdout check

Generate exact, noise-free **SIMULATED solar-only relative rate** 1+0.05 cos(2 pi t/86400+0.4), with **zero sidereal component**. Fit a constant plus sidereal sin/cos on the first seven days' live hours. The wrong model's training RMS residual is just 0.000865 in relative-rate units; on an unseen week starting day 180 its RMS error becomes 0.070997. A correctly specified solar model predicts the held-out week to ~3e-15 floating point. No Poisson event counts or p-values were simulated.

## Stronger exact null: annual drift can restore non-identifiability

The apparent full-year solution above assumes the solar background has constant amplitude and phase over the year. Set \(\Omega=\omega_*-\omega_\odot\). Then

\[
\cos[(\omega_\odot+\Omega)t]
=\cos(\omega_\odot t)\cos(\Omega t)
-\sin(\omega_\odot t)\sin(\Omega t).
\]

If the two coefficients of the 24-hour background may independently vary annually, the sidereal cosine is **exactly** in the nuisance span. The sidereal sine has an analogous identity. Under this enlarged model, the origin is **UNIDENTIFIABLE from the timing harmonic alone at any exposure duration**. This is a mathematical limiting case, not a finding that laboratory backgrounds truly vary that way. Environmental controls, constrained seasonal nuisance evolution or multiple detector orientations with jointly predicted material responses could restore identification. An anti-sidereal control diagnoses some seasonal artifacts, not all.

## Nearest prior art and new evidence

- [Blanco et al., arXiv:2602.15947](https://arxiv.org/html/2602.15947), submitted 17 February 2026 (the accessed HTML also displays an August manuscript date). Sections II, IV and V reviewed 19 October 2026. This work already formulates Poisson statistics with unknown 24-hour backgrounds, profile inference and shifted-sidereal stacking. Our deterministic masked time-design audit does **not** reproduce that likelihood or claim novelty.
- [DAMIC-M Collaboration, arXiv:2607.09352v1](https://arxiv.org/html/2607.09352), submitted 10 July 2026; [Physical Review D acceptance 2 October 2026](https://journals.aps.org/prd/accepted/10.1103/1h93-cx4x). Checked detector/data methods: a silicon skipper CCD prototype at roughly 130 K, 1668-second image readouts and 84 days of exposure acquisition from October 2024 to January 2025. The October acceptance is **not independent new detector exposure**. Their **solar-reflected DM** analysis is not a calibrated anisotropic-crystal sidereal search. No image-level live-time mask or event likelihood was retrieved here.
- [NASA sidereal clock explanation](https://www.grc.nasa.gov/www/K-12/Numbers/Math/Mathematical_Thinking/telling_time_by_the_stars.htm). The mean sidereal day differs from the solar day by about four minutes.

## Claims, controls, boundaries

**DIR-20261019-C1 (SIMULATION_RESULT).** For the stated deterministic mask and equal-noise first-harmonic design, a seven-day study retains 0.000639 of the worst sidereal-phase information after profiling the unknown solar sinusoid. A solar-only generating process nearly matches a short-run sidereal-only fit but decisively fails a distant holdout. Falsifier: an independently implemented calculation using the identical samples and assumptions disagrees beyond numerical tolerance.

**DIR-20261019-C2 (DERIVED / UNIDENTIFIABLE).** Unknown annual solar coefficient modulation exactly contains the sidereal first harmonic. Falsifier: a counterexample to the displayed identity under the same definitions.

**Strongest null:** an environmental solar-day process with unconstrained seasonal phase and amplitude. **Required additional observations:** calibrated environmental time series, timestamped events and per-readout live/dead time, realistic material response plus multiple orientations or energy channels. **Stop:** do not infer a dark-matter rate or significance from generic harmonics.

**Research checkpoint:** C-03's long-range unscreened scalar remains FAILED by Solar-System constraints; N-03's averaged phase origin remains UNIDENTIFIABLE. This run adds a detector-data identifiability gate only. **Learning checkpoint:** measurement-design matrices and nuisance projection introduced; understanding NOT_ASSESSED. **Recommended next step:** obtain an actual anisotropic-material response and real operational mask before performing a response-weighted Poisson injection/recovery against solar plus seasonal backgrounds. No schedule or prior PR changed.
