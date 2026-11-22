# PSZ2 G181: post-hoc boundary-feature exclusion

The [matched-physical-beam analysis](../two-cluster-physical-beam/README.md) found a large T50–T50SUB separation difference in a 600 kpc catalog-centered region and a bright difference peak near the southern aperture boundary. Here we repeat its exact 135 kpc Gaussian-beam, 600 kpc-aperture, 0.2 mJy/target-beam, brightest-10% rule and exclude a circle around the **post-hoc selected difference peak from both maps** before selecting pixels. The baseline matches the previous calculation to better than 10⁻⁶ kpc.

| Exclusion around peak | T50 minus T50SUB pair separation | Southern center difference |
| --- | ---: | ---: |
| None | −270.58 kpc | 74.53 arcsec |
| 20 arcsec | −92.36 kpc | 26.37 arcsec |
| 40 arcsec | +6.50 kpc | 0.79 arcsec |
| 60 arcsec | +5.50 kpc | 0.37 arcsec |

The 40-arcsecond exclusion removes 605 of 8,000 eligible southern T50 pixels and 239 of 7,046 eligible southern T50SUB pixels; it also changes which pixels enter each image's brightest 10%. These are not independent samples. The northern center remains unchanged by this particular exclusion and still differs between maps. The result shows that this **selected region strongly influences this particular estimator**, not that a cataloged source caused the difference, that the mask is the correct author mask, or that any published merger separation or age should be changed.

For context, we placed circles at three other positions on the same nominal radius from the southern catalog coordinate: the opposite side and rotations by ±90° in image-pixel coordinates. At 40 arcseconds, the resulting signed pair changes are −270.58, −271.26 and −282.60 kpc, respectively. These are convenience comparisons, not matched statistical controls: in particular, the reflected circle removed no threshold-eligible southern pixels in either map. The locations have different emission, differ in which eligible pixels they remove, and were not randomized or prespecified. They do not establish significance or a physical mechanism. A published LoTSS catalog source is nearby but remains a [positional association](../two-cluster-physical-beam/README.md).

## Reproduce

Run `python research/psz2-boundary-ablation/analyze.py /path/to/psz2-maps /path/to/rrsamp.tsv` with NumPy, SciPy, Astropy and Matplotlib. The maps and catalog are pinned by hashes and archived privately in Azure. The program checks beam-kernel covariance, coverage and the previous baseline; it writes all 52 center rows, `summary.json` and `ablation.png`. An independent Astropy calculation verified all 13 pair differences from the saved coordinates. Images share observations; noise covariance, original region selection, source subtraction and cluster membership remain unverified. Cite [Botteon et al.](https://arxiv.org/abs/2202.11720), [Shimwell et al.](https://arxiv.org/abs/2202.11733) and the [LoTSS release](https://lofar-surveys.org/planck_dr2.html).

A [36-location rotated-mask sweep](../psz2-rotated-mask-sweep/README.md) extends the control check. Only one alternate mask has similar eligible-pixel counts in both maps, and it overlaps the selected mask, so an independent matched control remains unavailable.

A [shared-pixel comparison](../psz2-shared-pixel-test/README.md) shows strong dependence on whether T50 or T50SUB selects the common bright pixels, even before the post-hoc peak exclusion.
