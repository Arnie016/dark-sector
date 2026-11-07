# Published radio-light-curve benchmark from The Three Hundred

This is a reproduction of an **analytic formula using published rounded fit parameters**, not a reanalysis of simulation particles, a refit of light curves, or a TNG-Cluster merger-clock calibration. [Nuza et al., arXiv:2409.09422v1](https://arxiv.org/html/2409.09422), Eq. 3 and Table 1, report a skewed Gaussian plus linear background for median 1.4 GHz luminosity relative to core passage. `parameters.csv` transcribes the group and cluster rows for radiation inside R200 and 2R200. These are aggregate power from shocked gas in 3D spherical apertures; they are not the luminosity of a single identified relic or directly comparable with a survey image aperture.

Evaluating the paper's formula over 0–1.5 Gyr after core passage gives the following central rounded-parameter results:

| Sample and radius | Maximum within this interval | Output at 1 Gyr |
| --- | ---: | ---: |
| Groups, R200 | 0.293 Gyr | 1.03 × 10²² W/Hz |
| Groups, 2R200 | 0.515 Gyr | 2.98 × 10²² W/Hz |
| Clusters, R200 | 0.617 Gyr | 4.10 × 10²³ W/Hz |
| Clusters, 2R200 | 0.673 Gyr | 8.43 × 10²³ W/Hz |

At 1 Gyr, the fitted cluster curve in the larger aperture is approximately 2.05 times the R200 curve. That arithmetic illustrates the paper's point that including a larger volume can collect more late-time emission, including shocks unrelated to the target merger; it does not measure an observational aperture correction or an uncertainty. The maxima are bounded to our chosen 0–1.5 Gyr interval and use rounded central parameters; no covariance, fit errors or individual-merger dispersion are propagated. The paper cautions that later luminosity bumps can come from other mergers and discusses model assumptions for cosmic-ray electrons and emission.

## Relation to the merger-clock candidate

[Lee et al. (2026)](https://arxiv.org/html/2510.21632), §§II–IV, use TNG-Cluster/TNG300, identify radio relic structures with a luminosity and morphology selection, and fit a time-since-collision relation to their separations. Their sample and definitions differ from Nuza et al.'s total shock-emission-in-spheres curves. The comparison motivates a testable question: **how does selection on detected relic features change the phase distribution and clock residuals relative to a fixed underlying merger sample?** It does not supply a detection probability, prove such a bias in Lee et al., reproduce their relation, or imply that total radio luminosity tracks the visible second relic. A defensible test still needs source-verified event/relic identities, time-resolved 3D and projected relic measurements, consistent detection models, cluster-level splits, a baseline, and uncertainty propagation. The original TNG key remains unavailable in the local secret helper; no key is recorded here.

`python analyze.py` uses NumPy, SciPy and matplotlib to regenerate the figure and `summary.json`; it checks the four transcribed rows and optimizes each curve within the stated interval. A separate standard-library implementation of the paper's equation checked all four outputs at 1 Gyr. The parameter values are a small attributed transcription, not the underlying proprietary code or simulation data. This benchmark and figure are archived privately in Azure and versioned in the GitHub draft. No email was sent.
