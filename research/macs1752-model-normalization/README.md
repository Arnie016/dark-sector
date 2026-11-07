# MACS J1752: testing model-image normalization hypotheses

The earlier [compact-model comparison](../macs1752-compact-model-check/README.md) treated the official `compact-model.fits` as a restored Jy/source-beam image, consistent with its `BUNIT=JY/BEAM` header, and found a peak 10.5 times smaller than the T50 − T50SUB difference. This test evaluates a second **post-hoc hypothesis**: the model represents unconvolved Jy/pixel components. Some imaging software uses such a convention for CLEAN models; see the [CASA documentation](https://casadocs.readthedocs.io/en/latest/_modules/casatasks/imaging/ft.html) and [WSClean release notes](https://wsclean.readthedocs.io/en/latest/changelogs/v2.7.html). The [survey paper](../radio-processing-provenance/README.md) identifies WSClean 2.8 for its general imaging workflow, supporting this hypothesis, but the released file’s exact provenance and convention remain unverified; its header says Jy/beam.

On the same selected 30-arcsecond region:

| Assumption | Predicted peak | Difference-image peak | RMS residual over region |
| --- | ---: | ---: | ---: |
| Restored source beam, convolved to target | 2.523 mJy/target beam | 26.548 mJy/beam | 5.326 mJy/beam |
| Unconvolved per-pixel components, restored with unit-peak target Gaussian | 26.489 mJy/target beam | 26.548 mJy/beam | 0.069 mJy/beam |

The second model's peak is within approximately 0.23% of the difference peak and its local residual is smaller. This is **consistent with**, but does not prove, the unconvolved-component hypothesis. The selected region was identified after inspecting the difference; the images and model are related products with correlated pixels, and Gaussian beams, interpolation, local selection and image processing are approximate. RMS is a descriptive image residual, not a noise or statistical-significance estimate. No conclusion is made about the physical source, published fluxes, catalog correctness, merger age, or dark matter. The header's stated Jy/beam, actual construction, units, and subtraction procedure require authoritative documentation or author clarification before this model is used quantitatively.

Run `python research/macs1752-model-normalization/analyze.py /path/to/selected-maps` with NumPy, SciPy and Astropy. It checks source hashes, FITS units, sampled WCS agreement, beam compatibility and source-grid scale; a separate direct local kernel sum checks the FFT convolution at the selected difference peak. Inputs are in the previously archived official FITS package and compact-model archive. Cite the [LoTSS cluster release](https://lofar-surveys.org/planck_dr2.html) and [Botteon et al.](https://arxiv.org/html/2202.11720) when reusing data. No email was sent.
