# D-02 | Rare charge patterns and the low-count evidence trap

**17 October 2026. Status: DERIVED (Poisson factorization), DATA_INSUFFICIENT (particle inference).** Published real summary counts, not simulated observations; original event-level data and signal templates were not recovered.

[Methods](METHODS_RESULTS_v1.0.md) | [Executable source](run.py) | [Actual result](results.json) | [Learning/research checkpoint](CHECKPOINT.md) | [Primary sources](SOURCES.md)

## Physical question and actual 2026 evidence

When a low-threshold silicon detector records an unusual few-electron event, is that evidence for dark matter? Only after considering all relevant response patterns and ordinary backgrounds.

The [DAMIC-M solar-reflection paper](https://arxiv.org/html/2607.09352v1), submitted 10 July 2026, was [accepted by Physical Review D on 2 October 2026](https://journals.aps.org/prd/accepted/10.1103/1h93-cx4x). The **observations were acquired October 2024 to January 2025**, not in October 2026. The collaboration used 1.257 kg-day of blind exposure, silicon skipper CCDs with about 0.16-electron charge noise and image exposures of 1668 seconds. A pattern named **31** means three electrons in one pixel next to one electron in another pixel, not a 31-eV recoil. The energy-to-charge conversion is stochastic.

## AHA | Rate and category are distinct information

Let independent count channels be Poisson with means mu_p. If N is the summed event count and mu is the sum of their means, their joint probability splits into a Poisson distribution for N times a multinomial distribution for the allocation of those N events across the channels. A particle hypothesis must predict how its energy deposits turn into the detector's **pixel-pattern distribution**, not just how many events occur.

## Source-grounded calculation

Published pattern labels: (11,21,111,31,22,211). Observed counts: (144,0,0,1,0,0). Nominal background: (141.439,0.150,0.058,0.071,0.011025,0.035058) events, summed from the paper's two background arrays at fixed radiogenic nuisance scale one. This is a transcription of the source [Eqs. (2), (5), (7)](https://arxiv.org/html/2607.09352v1).

The five rare categories excluding 11 contain **one observed event versus 0.325083 expected background events**. With that nominal background held fixed:
- P(at least one specifically in pattern 31) = **6.854%**.
- P(at least one in any of the five rare patterns) = **27.753%**.
- Given exactly one rare event, P(it lands in 31) = **21.841%**.

Thus one noteworthy-looking category is not evidence of a particle by itself. The five-channel probability is *not* a comprehensive search-trials correction.

A restricted fixed-background one-sided 90% upper bound on **additional expected events confined to those five categories** is 3.564637. This **cannot be converted to a dark-matter cross section** without flux, silicon response, acceptance and the profiled nuisance likelihood. Do not attach an asymptotic p-value to the all-channel deviance of 3.9864: most non-dominant channels have much less than one expected event.

## Reproducibility, strongest null and next gate

One deterministic Python standard-library process, no random seed and six finite checks plus strict JSON readback. Script SHA-256: 7de9752611bb186c87f9fb9ba80b41823643f360f36e7f3aa560487024b3f867. No full DAMIC-M likelihood was reproduced. Their control sample has 98 observed higher-energy events, and their particle fit uses a separate auxiliary Poisson term with low-count Monte Carlo calibration.

**D-02-C1 DERIVED:** the published low-count summary is compatible with ordinary nominal background at this fixed-input diagnostic level. **D-02-C2 DATA_INSUFFICIENT:** a microscopic dark-matter signal cannot be identified from the channel aggregates alone. **Strongest null:** accidental coincidences and radiogenic charge depositions with the source's nuisance model. Stop at no detection claim.

The newly accepted paper reuses earlier DAMIC-M pattern-exposure data. Its separate [August 2026 daily-modulation publication](https://arxiv.org/html/2511.13962) uses the same LBC campaign with a different single-electron time observable. These are **not independent new exposures**. Joint inference needs shared exposure, selections and nuisance correlations.

**Recommended next bounded step:** recover one published benchmark vector of six particle signal counts, along with the control-region expectation and detector-response setup; only then reproduce the profiled low-count likelihood for one mass/cross-section point. If unavailable, record DATA_INSUFFICIENT rather than fabricate sensitivity.

**Continuity:** previous D-01 solar/sidereal mask study, S-01 cluster projection study and failed C-03 unscreened long-range gravity model remain unchanged. Learning: introduced Poisson-vs-category information; understanding NOT_ASSESSED.
