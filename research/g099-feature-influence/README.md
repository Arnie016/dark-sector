# Abell 1925: influence of northern and southern difference regions

Starting from the [600 kpc, 0.2 mJy/target-beam Abell 1925 configuration](../g099-paired-positions/README.md), we identify the largest positive T50 minus T50SUB pixel within each catalog-centered relic circle. We then repeat the same brightest-10% estimator after excluding circles of radius **one target-beam FWHM (70.11 arcseconds)** around the selected northern peak, the southern peak, or both. Every exclusion is applied to both maps before selecting pixels. The peaks and masks were chosen after the images were examined; they are not author-supplied regions or source identifications.

| Exclusion | Signed T50 minus T50SUB pair separation |
| --- | ---: |
| None | −197.08 kpc |
| Northern peak | −30.68 kpc |
| Southern peak | −362.36 kpc |
| Both peaks | −190.28 kpc |

The two single-region changes have opposite signs, while the combined change nearly cancels in the scalar pair separation. This does not mean the underlying center positions or images are unchanged. It shows that, for this post-hoc estimator, the pair separation can conceal substantial individual-position changes. The center rule is nonlinear because eligible and brightest pixels are reselected; the table is not an additive decomposition or a causal estimate of source subtraction.

The selected northern and southern difference maxima lie approximately 271.09 and 192.64 arcseconds from their respective catalog centers and have pixel values 269.24 and 47.08 mJy/target beam. The [diagnostic map](difference-regions.png) is clipped at ±5 mJy/beam, so it saturates those peaks; values come from the unclipped arrays. Both images share observations, pixels are correlated, and an image-difference maximum does not identify a physical source or artifact. The sky coordinates in `summary.json` are FK5 J2000. No published separation, merger clock or dark-matter conclusion is corrected.

## Reproduce

Run `python research/g099-feature-influence/analyze.py /path/g099-selected /path/rrsamp.tsv` with NumPy, SciPy, Astropy and Matplotlib. The code checks input hashes, target beam and coverage, reproduces the saved 600 kpc/0.2 baseline, and writes the 16 center rows and diagnostic plot. A separate Astropy calculation verified all four pair differences from the saved FK5 positions. The input FITS members and analysis are archived privately in Azure; the full source archive was only partially streamed. Source masks, per-image noise covariance and independent data remain necessary for a calibrated inference. Cite [Botteon et al.](https://arxiv.org/abs/2202.11720) and the [LoTSS release](https://lofar-surveys.org/planck_dr2.html).

A [LoTSS catalog cross-match](../g099-radio-source-crossmatch/README.md) finds nearby radio entries for both selected peaks; the same-survey positional matches do not establish physical identities.
