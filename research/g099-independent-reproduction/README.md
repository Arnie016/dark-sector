# Computational replay of the Abell 1925 comparison

A second numerical implementation reproduces the [Abell 1925 paired-image analysis](../g099-paired-positions/README.md) using zero-padded NumPy FFT convolution and explicit bilinear interpolation, rather than its SciPy convolution and interpolation functions. The alternate convolution is checked against an impulse and a small directly summed example. It uses the same FITS members, catalog positions, Astropy WCS and cosmology, Gaussian beam approximation, masks, thresholds and center rule.

Across all nine radius/threshold configurations and 36 image/relic rows, eligible and selected-pixel counts match; the maximum position discrepancy is approximately **5.7 × 10⁻¹¹ arcseconds**, and paired separations agree at saved numerical precision. The replay compares WCS positions in their actual FK5 J2000 frame. This is a computational consistency check, not independent data or an independent analyst, validation of the original survey image-processing steps, a statistical uncertainty, a population result, or a published clock reproduction.

## Reproduce

Run `python research/g099-independent-reproduction/reproduce.py /path/g099-selected /path/rrsamp.tsv` with NumPy and Astropy. The script validates hashes, tests the alternate convolution, and compares the independently computed selections, centers and pair differences to the saved 36 rows. It writes `comparison.csv` and `summary.json`; the input FITS members are archived privately in Azure. The original archive was only partially streamed as documented in the [selection manifest](../third-cluster-selection/manifest.json). Cite [Botteon et al.](https://arxiv.org/abs/2202.11720) and the [LoTSS cluster release](https://lofar-surveys.org/planck_dr2.html).
