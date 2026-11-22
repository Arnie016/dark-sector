# MACS J1752: spatial check of model normalization

The previous [normalization test](../macs1752-model-normalization/README.md) found that treating the nominal compact model as unconvolved per-pixel components reproduced a selected image-difference patch much better than treating it as an already restored Jy/beam image. The FITS header says Jy/beam, and the true model construction and units are not established.

Here the two existing, fixed calculations are evaluated in a ring **45–240 arcseconds from the original difference peak**, with a 15-arcsecond gap from the previously examined 30-arcsecond region. This is spatially separate, not statistically independent: it uses the same maps, observations, model, beam and correlated pixels. The bounds and two selection rules were set before inspecting this diagnostic's output; the unit hypotheses were proposed after seeing the original patch. No model parameters are fitted here.

| Region | Pixels | Restored-beam assumption: RMS residual | Unconvolved-component assumption: RMS residual |
| --- | ---: | ---: | ---: |
| All finite pixels in ring | 77,567 | 0.299 mJy/beam | 0.028 mJy/beam |
| Pixels where the unconvolved-component prediction exceeds 0.5 mJy/beam | 991 | 2.607 mJy/beam | 0.036 mJy/beam |

Both RMS values are descriptive image residuals, not noise estimates, error bars or significance tests. The signal-selected subset is conditioned on one of the two predictions, so the all-pixel result is included as a separate check; neither is a representative sample of unrelated clusters. Spatial filtering, beam approximations, background, image-generation steps and model normalization still need documentation. The results strengthen the working hypothesis that a per-pixel component convention may describe this file, but do not override the FITS header or establish how the survey produced it. No physical source identification, merger-age correction or dark-matter constraint follows.

Run `python research/macs1752-model-holdout/analyze.py /path/to/selected-maps` with NumPy, SciPy and Astropy. The program invokes the preceding normalization script, which checks input hashes, beam and WCS and regenerates its summary, before evaluating the spatial ring. The official raw images and nominal model are already in private Azure. Cite the [survey release](https://lofar-surveys.org/planck_dr2.html) and [Botteon et al.](https://arxiv.org/html/2202.11720). No email was sent.
