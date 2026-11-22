# PSZ2 G181.06+48.47: radius and geometry in a merger-clock comparison

This calculation tests the sensitivity of a published formula to input choices; it does not estimate a corrected merger age, reconcile two published analyses, or infer an SIDM cross-section. It follows the four-system [cross-paper comparison](../clock-crosspaper/README.md).

## Source measurements

- [Stroe et al. (2025)](https://arxiv.org/html/2501.07651), §IV.2, report an X-ray scaling-relation radius r500,X = 0.87 ± 0.04 Mpc and a Planck SZ radius r500,SZ = 1.06 ± 0.05 Mpc. They describe possible systematics including different assumed centers and background contamination.
- [Ahn et al. (2025)](https://arxiv.org/html/2501.09067) derive M500c = 2.90 (+0.75, -0.69) × 10^14 solar masses from a model superposing two NFW halos. They assume H0 = 70 km/s/Mpc, Ωm = 0.3 and z = 0.234. From the spherical overdensity definition, R500c = [3 M500c / (4π × 500 ρcrit(z))]^(1/3); using those values we obtain approximately **0.931 Mpc**. Ahn et al. also directly report R500c = 0.93 (+0.07, -0.08) Mpc in Table 1; our independent conversion agrees with their rounded central value. The source model and mass uncertainties still apply.
- The [LoTSS DR2 VizieR table](../clock-crosspaper/catalog-manifest.json) reports a projected separation of 2.694 Mpc between flux-weighted positions of the brightest 10% of each radio relic. [Lee et al. (2026)](https://arxiv.org/html/2510.21632), §IV.2, list an approximate normalized separation of 2.9 for this system and fit TSC = 0.52(d/R500c) − 0.24 Gyr over ratios 1–3.5. Their fitted simulation quantity is **3D emissivity-weighted-center separation**, not this projected LOFAR estimator.

## Controlled input substitution

Holding the 2.694 Mpc projected separation fixed and inserting each radius into the Lee line gives:

| Radius choice | Radius (Mpc) | Projected separation / radius | Formula output (Gyr) |
| --- | ---: | ---: | ---: |
| X-ray | 0.870 | 3.10 | 1.37 |
| Weak-lensing mass converted above | 0.931 | 2.90 | 1.27 |
| Planck SZ | 1.060 | 2.54 | 1.08 |

The two published radius choices change this algebraic output by about 0.29 Gyr, similar in scale to the roughly 0.3 Gyr scatter that Lee et al. discuss at large separations. This is not a comparison of independent Gaussian errors or a combined uncertainty: the radius measurements, chosen separation, fits, and selection all have systematic and potentially correlated errors. The numbers are not valid stand-alone age determinations. The lensing-derived radius and LOFAR distance happen to yield a ratio close to Lee et al.'s approximate 2.9, which is **consistent with** that combination but does not prove which exact inputs they used. This is a useful provenance check, not an independent reproduction of their fit.

## Geometry and interpretation

[Rajpurohit et al. (2025)](https://arxiv.org/html/2501.08390), §VI.3–4, discuss an approximately 45° inclination from radio analyses and emphasize that the geometry remains uncertain. [Jee et al. (2026)](https://arxiv.org/html/2605.00093), §§II.3 and IV.2, use a 0–40° fiducial angle prior, explicitly consider an expanded 0–70° prior including this system, and model projected shock positions as curved surfaces rather than treating them as a simple two-point cosine projection. Their 0.95 Gyr posterior median for this cluster and their joint sensitivity study depend on their full forward model; an approximate radio angle is not a proven conflict with that posterior or a demonstration of an erroneous SIDM result.

Next steps toward a defensible comparison: establish the exact distance estimator and mass inputs used for each published value; obtain corresponding radio maps, lensing posterior/covariance and the full clock calibration/likelihood; then construct common-definition mock observations and evaluate phase/geometry effects against held-out simulations. The studies share authors and some data or modeling, so agreement is not independent validation.

## Reproduce

Run `python analyze.py` using matplotlib. It writes the table, summary and plot and requires no network or credentials. Inputs are the source values above; the weak-lensing radius computation uses G = 4.30091 × 10^-9 Mpc (km/s)^2 / solar mass. An independent numerical check verified the derived radius and formula outputs. No additional observational data were downloaded, and no email was sent.

**Redshift provenance update:** The catalog separation used above was published using z = 0.240, whereas the weak-lensing radius was computed at z = 0.234. A [subsequent coordinate and FITS cross-check](../psz2-lotss-cutout/README.md) recomputes the same angular separation at both redshifts. At the same assumed cosmology, substituting its 2640 kpc value for 2694 kpc changes this exercise's lensing-radius formula output by about −0.030 Gyr. This remains an illustrative calculation, not a re-estimated merger age.
