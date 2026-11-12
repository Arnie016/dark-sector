# MACS J1752: velocity context for the matched optical object

The [Keck cross-match](../macs1752-keck-crossmatch/README.md) identifies a galaxy at z = 0.3708639 close to the LoTSS-associated optical position. Figure 29 of the [Golovich et al. panchromatic atlas](https://arxiv.org/html/1806.10619#S5.SS21) reports two fitted subcluster means and dispersions: z = 0.36482 ± 0.00046 and σ = 1006 ± 68 km/s (93 galaxies), and z = 0.36430 ± 0.00055 and σ = 1038 ± 77 km/s (69 galaxies). These numbers were read from the figure in the arXiv v1 rendering. The paper notes that a two-subcluster model is only slightly preferred and that a bright star limits spectroscopic completeness near one core.

Using Δv = c(z_gal − z_sub)/(1 + z_sub), the galaxy is approximately **+1328 km/s (1.32 σ)** relative to component 1 and **+1442 km/s (1.39 σ)** relative to component 2. These are descriptive offsets based on published central values; the script does not propagate uncertainties in the fitted means or dispersions. The [illustrative plot](velocity_context.png) shows normalized Gaussian shapes with these published dispersions, not newly fitted distributions.

This comparison is not an independent confirmation of cluster membership: the atlas used the same Keck survey, so the matched spectrum may have contributed to the fitted population, and the spatial selection, interlopers and merger structure matter. It provides no probability of membership or assignment to a subcluster. The optical-to-radio association and the origin of the image difference remain unresolved.

## Reproduce

Run `python research/macs1752-keck-velocity-context/analyze.py` from the repository root with NumPy and Matplotlib. It reads the archived cross-match summary, calculates the two offsets, and writes the machine-readable `summary.json` and `velocity_context.png`. The figure values are manually transcribed from the paper; verify the cited figure if updating them. No new spectra, membership fit, or radio-image morphology measurement is claimed.
