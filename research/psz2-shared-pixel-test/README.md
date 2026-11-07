# PSZ2: sensitivity to shared versus independently selected pixels

The [prior post-hoc exclusion](../psz2-boundary-ablation/README.md) allowed each image to select its own eligible and brightest pixels. This follow-up tests how the result changes with shared sky support. The same 135 kpc target beam, 600 kpc aperture and 0.2 mJy/target-beam cut are used for both related PSZ2 maps; the boundary mask, when applied, is the same 40-arcsecond circle in both maps. All four rules compute a separate brightness-weighted position for each map, so even the shared-pixel rules can yield different centers.

1. **Independent:** each image selects its own above-threshold pixels and its own brightest 10%.
2. **Joint eligibility, independent ranking:** retain only sky pixels above threshold in both images, then each image selects its own brightest 10% of that joint set.
3. **Shared T50 ranking:** use the brightest 10% of the joint set according to T50 for both maps.
4. **Shared T50SUB ranking:** use the brightest 10% of the joint set according to T50SUB for both maps.

| Position rule | No exclusion | Peak exclusion |
| --- | ---: | ---: |
| Independent | −270.58 kpc | +6.50 kpc |
| Joint eligibility, independent ranking | −232.66 kpc | −0.34 kpc |
| Shared T50 ranking | −213.46 kpc | −0.01 kpc |
| Shared T50SUB ranking | −0.03 kpc | −0.03 kpc |

The values are signed T50 minus T50SUB pair separations. For the southern relic without exclusion, independently selected sets overlap in 537 pixels out of a 968-pixel union; the images have strongly correlated pixels, so these are counts, not independent samples. Even with common eligible pixels, which map chooses the brightest pixels matters substantially: the T50-based shared selection retains a large difference, whereas the SUB-based selection does not. This is consistent with strong reference-selection dependence and with the local feature influencing the chosen estimator. It is not a determination that either selection is correct, an independent source detection, a noise or uncertainty estimate, a reproduction of author masks, or a published merger-clock bias. The peak and comparison choices are post-hoc, and the maps share observations.

## Reproduce

Run `python research/psz2-shared-pixel-test/analyze.py /path/to/psz2-maps /path/to/rrsamp.tsv` with NumPy, SciPy, Astropy and Matplotlib. The script validates the map and catalog hashes, matching beam kernels, finite coverage and the independent baseline against the prior analysis. It writes `variants.csv`, `summary.json` and `shared-selection.png`. An independent Astropy calculation verified all eight pair differences from the 32 saved coordinate rows. Inputs are already archived privately in Azure. See [Botteon et al.](https://arxiv.org/abs/2202.11720), [Shimwell et al.](https://arxiv.org/abs/2202.11733) and the [LoTSS cluster release](https://lofar-surveys.org/planck_dr2.html).

A [bright-fraction sweep](../psz2-bright-fraction-sensitivity/README.md) finds a non-monotonic response to the T50-selected fraction and a residual difference even on the full jointly eligible set. These choices remain post-hoc.
