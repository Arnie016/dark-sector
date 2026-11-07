# Published noise values and their image provenance

The [survey table](https://lofar-surveys.org/planck_dr2.html) lists RMS values of **0.101 mJy/beam** for MACS J1752 (`PSZ2 G071.21+28.86`) and **0.066 mJy/beam** for PSZ2 G181. [Botteon et al.](https://arxiv.org/html/2202.11720#S3.SS3) define these table entries for their **reference image**, made with robust −0.5 and no uv taper. Twice these reference RMS values is 0.202 and 0.132 mJy/beam, respectively; those are arithmetic values for those reference products, **not validated 2σ thresholds for our maps**.

The archived T50SUB maps have FITS restoring beams of approximately **14.73 × 10.64 arcseconds** for MACS and **19.56 × 19.19 arcseconds** for PSZ2. Our comparison further convolves and resamples them to a 135 kpc physical beam. The reference-image RMS cannot simply be transferred to either product: restoring beam, uv weighting, source subtraction, resampling, correlated noise and spatial background can change it. Our 0.1–0.3 mJy/target-beam cuts were exploratory absolute thresholds and should not be described as 2σ measurements.

For context, [Rajpurohit et al. (2025), Table 2](https://arxiv.org/html/2501.08390) report RMS values for **different PSZ2 LOFAR products**: 70 μJy/beam for an 8.1 × 5.3 arcsecond map, and 200 and 210 μJy/beam for two distinct 20 × 20 arcsecond maps. The entries are manually transcribed from that paper. Similar dimensions or frequency do not establish that those maps are identical to our archived T50SUB image, or provide the noise covariance after our additional smoothing.

The next defensible measurement requires source-free regions and an RMS/covariance estimate for each actual comparison product, plus the original relic regions. No noise significance, author-pipeline reproduction or merger-age uncertainty follows from the reference values above.

## Reproduce

Run `python research/lofar-noise-provenance/analyze.py /path/planck-dr2-snapshot.html /path/macs-T50kpcSUB.fits /path/psz2-T50kpcSUB.fits` with Beautiful Soup, NumPy and Astropy. The official table snapshot is archived privately in Azure. The script checks image hashes and exact table labels, extracts the two reference RMS values and records archived FITS beam sizes. The later-paper entries are transcriptions requiring source review, not independently estimated values. `summary.json` includes the table snapshot hash and provenance. Cite [Botteon et al.](https://arxiv.org/abs/2202.11720), [Rajpurohit et al.](https://arxiv.org/abs/2501.08390) and the [survey release](https://lofar-surveys.org/planck_dr2.html).

An initial [geometry-selected patch diagnostic](../two-cluster-background-patches/README.md) measures spatial variation on the actual smoothed products, but the patches are small and not verified source-free; the results are not calibrated RMS values.
