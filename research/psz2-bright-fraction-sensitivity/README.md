# PSZ2: bright-pixel fraction sensitivity

The [shared-pixel test](../psz2-shared-pixel-test/README.md) found that selecting the brightest 10% of jointly eligible sky pixels using T50 or T50SUB produced very different paired separations. Here we vary the fraction over 1%, 5%, 10%, 20%, 50% and 100%, using the same 135 kpc target beam, 600 kpc apertures, 0.2 mJy/target-beam cut, joint threshold eligibility and map-specific brightness weights. At each fraction the same sky pixels are used for both maps, chosen by one reference image. Both no-exclusion and the post-hoc 40-arcsecond peak exclusion are reported.

| Brightest fraction | T50 reference, no exclusion | T50SUB reference, no exclusion |
| --- | ---: | ---: |
| 1% | −1.34 kpc | +0.02 kpc |
| 5% | −300.36 kpc | +0.09 kpc |
| 10% | −213.46 kpc | −0.03 kpc |
| 20% | −153.24 kpc | −0.05 kpc |
| 50% | −105.55 kpc | −0.03 kpc |
| 100% | −92.79 kpc | −92.79 kpc |

These are signed T50 minus T50SUB pair-separation differences for an illustrative estimator. The T50-reference result is non-monotonic: selecting the very brightest 1% produces a small difference, while 5–50% produces a large one. The 100% rows are equal because both reference choices select the identical entire jointly eligible set, though each map retains its own weights. With the 40-arcsecond post-hoc exclusion, both 100% cases give −4.51 kpc and the other settings range from −2.00 to +0.11 kpc. This illustrates sensitivity to the fraction, reference ranking and selected sky region; it does not establish the correct physical center, original author selection, uncertainty, population bias, or merger-clock impact. The maps share observations and correlated pixels.

## Reproduce

Run `python research/psz2-bright-fraction-sensitivity/analyze.py /path/to/psz2-maps /path/to/rrsamp.tsv` with NumPy, SciPy, Astropy and Matplotlib. The script verifies the map/catalog hashes, beam kernel, finite support and four 10% baseline values, and checks that the 100% results agree between references. It writes `variants.csv`, `summary.json` and the figure. A separate Astropy calculation verified all 24 pair differences from the 96 recorded coordinate rows. Inputs are in private Azure. These fractions and the peak exclusion are exploratory, not a preregistered trial or uncertainty interval. Cite [Botteon et al.](https://arxiv.org/abs/2202.11720), [Shimwell et al.](https://arxiv.org/abs/2202.11733), and the [LoTSS release](https://lofar-surveys.org/planck_dr2.html).

A [pixel-weight decomposition](../psz2-selection-mechanism/README.md) explains why the T50-selected 1% and 5% choices behave differently: the former confines both map centers to the boundary region, while the latter mixes that region with other pixels weighted very differently in the two images.
