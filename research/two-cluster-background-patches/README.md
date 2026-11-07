# Geometry-selected local variation in the comparison maps

The published RMS values in the [noise provenance note](../lofar-noise-provenance/README.md) belong to different image products. As a first diagnostic on the actual 135 kpc-beam comparison products, we place a fixed 4 × 4 grid of approximately 250 kpc square patches across each SUB reference image. We reject patches whose bounds leave the image, whose center is close enough that the square could overlap a 600 kpc catalog-centered relic circle, or whose common finite-pixel coverage is below 99%. We apply identical accepted sky pixels to both T50 and T50SUB maps. This geometry-based rule is fixed in code and does **not** establish that the patches are free of compact sources, diffuse emission, calibration residuals or spatially varying backgrounds.

For each patch we compute `1.4826 × median(abs(pixel − median(pixel)))`, a robust dispersion diagnostic in mJy/target beam. Fifteen patches pass in MACS and twelve in PSZ2. Their medians and full ranges are:

| Field / product | Median patch MAD scale | Range across patches |
| --- | ---: | ---: |
| MACS T50 | 0.237 | 0.142–0.676 |
| MACS T50SUB | 0.241 | 0.148–0.337 |
| PSZ2 T50 | 0.256 | 0.106–1.256 |
| PSZ2 T50SUB | 0.209 | 0.115–0.276 |

Units are mJy/target beam. The nominal patch sides are roughly 252–261 kpc, only about 1.9 times the 135 kpc FWHM; pixels are highly correlated, so the many pixels in a patch are not many independent noise samples. The full ranges are sensitive to patch location and possible residual sources. These values are **not calibrated image RMS measurements, 2σ detection thresholds, error bars or uncertainty intervals**, and should not be substituted into the authors' relic procedure. They show why a source-masked, larger-area and spatial-covariance analysis is still required. The median across a handful of fixed patches is descriptive and not a population statistic.

## Reproduce

Run `python research/two-cluster-background-patches/analyze.py /path/to/macs-maps /path/to/psz2-maps /path/to/rrsamp.tsv` with NumPy, SciPy, Astropy and Matplotlib. Input hashes, FITS units, beam-kernel covariance and common finite coverage are checked; `patches.csv` includes accepted and rejected locations, and `summary.json` records the per-product ranges. An independent read of the CSV checked patch counts and all four medians. The patch selection is not the survey authors' region or a prevalidated noise mask. Cite [Botteon et al.](https://arxiv.org/abs/2202.11720), [Jones et al.](https://arxiv.org/abs/2301.07814), and the [LoTSS release](https://lofar-surveys.org/planck_dr2.html).
