# C-31 | A global mass/radius column is not a merger-core SIDM scattering forecast

**2026-11-20 (Asia/Singapore) | DERIVED from SIMULATION-DERIVED CDM TNG-Cluster values.** No SIDM calculation was executed and no interaction cross-section was inferred.

## Bounded question and baseline

For the 11 previously selected strong-cool-core TNG-Cluster halos, what *conservative upper ceiling* follows for an idealized, single-pass scattering probability **averaged over uniformly sampled impact parameters** through a sphere truncated at `r500`, using only `M500` and `r500`? This checks whether a global surface-density proxy can stand in for a merger-core scattering rate. It cannot.

The strongest conventional explanation for much larger core effects is dark-matter concentration, dynamical residence time and the relative particle velocity distribution, not a force detectable through projected gas centroids alone. Stop at the mathematical ceiling without extrapolating to halo-halo drag.

## Source and provenance

- [Official TNG-Cluster properties catalog](https://www.tng-project.org/files/TNG-Cluster_Catalog.txt), last documented update **6 March 2025**, 352 `z=0` simulated halos. `mhalo_500c` is log10(M500/Msun) and `r500c` is Mpc. Eleven mass values below were manually copied and cross-checked. No full 352-row catalog was downloaded.
- Existing C-30 source excerpt, same 11 halo IDs/radii, input SHA-256 `bdd40aa776551aae0caf9560baf2bca0ef6003e481409584815641f96567d06a`. The halos were previously selected for strong cool cores and are **not** a random sample.
- [Lee et al., *TNGC-SIDM I*](https://arxiv.org/abs/2610.18957), submitted 13 October 2026, preprint (peer review not established), Methods §2.1 and §3.2. The authors use velocity-independent isotropic models at 0.5 and 1 cm²/g in **two separate matched merger simulations**, and estimate *local* collision rate with `rho_DM * v_rms * (sigma/m)`. Their reported central rates around 3/Gyr are not predictions for these eleven CDM halos.
- [Nelson et al. (2024)](https://doi.org/10.1051/0004-6361/202348608), peer-reviewed TNG-Cluster overview.

## Geometric derivation

Let `R=r500` (cm), `M=M500` (g) and `kappa=(sigma/m)` (cm²/g), constant. For an idealized test particle crossing an **r500-truncated stationary** target-DM sphere along impact parameter `b`, define `Sigma_DM(b)=integral_chord rho_DM dl` (g/cm²). Under an independent Poisson scattering assumption, `P(b)=1-exp(-kappa*Sigma_DM(b))`.

Across **area-uniform** impact parameters within a disk of radius R, `mean_area Sigma_DM = M_DM(<R)/(pi R²) <= M500/(pi R²)`. Because `1-exp(-x)` is concave, Jensen gives

```text
mean_area P(b) <= 1-exp[-kappa * mean_area Sigma_DM]
               <= 1-exp[-kappa * M500/(pi*r500^2)].
```

This ceiling applies to the stated *area-average*, **not** to a central chord or an orbiting particle's integrated exposure. `M500` includes baryons, so using it makes the mean column ceiling conservative. The scattering-coefficient interpretation of the paper's isotropic momentum-transfer cross-section is an explicit approximation, not a reproduced Monte Carlo scattering kernel.

## Published simulation-derived inputs and results

`M_sun=1.98847e33 g`, `Mpc=3.085677581491367e24 cm`.

| original halo ID | TNG haloID | log10 M500/Msun | r500 Mpc | M500/(pi r500²) g/cm² | probability ceiling at 1 cm²/g |
|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 15.13 | 1.711 | 0.030631 | 3.017% |
| 14 | 2507618 | 15.17 | 1.774 | 0.031244 | 3.076% |
| 19 | 3135769 | 14.97 | 1.515 | 0.027030 | 2.667% |
| 20 | 3238091 | 14.94 | 1.489 | 0.026114 | 2.578% |
| 24 | 3656685 | 14.92 | 1.462 | 0.025869 | 2.554% |
| 28 | 4054274 | 14.99 | 1.547 | 0.027145 | 2.678% |
| 34 | 4561713 | 14.98 | 1.531 | 0.027084 | 2.672% |
| 37 | 4854863 | 14.98 | 1.536 | 0.026908 | 2.655% |
| 38 | 4959833 | 15.02 | 1.577 | 0.027990 | 2.760% |
| 39 | 5059214 | 14.92 | 1.458 | 0.026011 | 2.568% |
| 46 | 5524229 | 14.95 | 1.492 | 0.026615 | 2.626% |

The 11 total-mass column ceilings span **0.025869–0.031244 g/cm²**, median **0.027030**. Thus area-mean **probability ceilings** at 1 cm²/g span **2.554%–3.076%**, median 2.667%; at 0.5 cm²/g the maximum ceiling is 1.550%. These are **not measured or simulated SIDM scattering frequencies**, and there is no population-level statistical significance.

Worked scale: halo 4561713 has `M500=10^14.98 Msun` and `r500=1.531 Mpc`; its total-mass area column is 0.0270843 g/cm². At `kappa=1 cm²/g`, `1-exp(-0.0270843)=0.0267208`. Printed mass ±0.005 dex and radius ±0.0005 Mpc give a rounding envelope **0.026757–0.027416 g/cm²**, not physical error bars. In the weak-opacity limit the bound is approximately `kappa*M500/(pi*R²)`.

## Reproducibility

One deterministic Python 3 standard-library worker; `timeout 20s python3 c31_area_mean_optical_depth.py`, exit **0**, measured external wall **1.06 seconds**, RNG seed none. Script SHA-256 `4a804c80838afd28bb6075ca8f52c2774208763961586a32b91da8da452e05a4`; local JSON output SHA-256 `157e9796afa82c6a11685cf8a8ed310a56e8c6ab4246fd8233f174430860fb33`. Exact 11 mass entries and radii are shown in this note; the locally archived script verifies the original C-30 CSV byte digest, converts each `10^logM` to grams and calculates `Sigma=M/(pi*R^2)` and `P_ceiling=-expm1(-kappa*Sigma)`. This note does not claim new HDF5 or map-level reproduction. No Azure access, GPU, paid API or bulk download.

## Decision and continuity

**AHA:** A few percent upper ceiling for uniformly selected one-pass chords can coexist with Lee et al.'s order-unity-per-Gyr **core** interaction rate. The former averages over area and assumes one transit; the latter depends on local dark matter density, particle velocities and residence time. The global area-mass proxy cannot decide SIDM drag or infer a cross-section. **DERIVED** measurement-domain restriction, no novelty claim.

**Next:** retrieve physically matched CDM/SIDM `rho_DM(r)` and `v_rms(r)` profiles from the primary simulation study, then integrate exposure on a declared set of physical merger trajectories, validating by independent merger initial conditions. Stop without local profiles and trajectory selection.

C-03 unscreened gravity **FAILED**; C-20 snapshot reweighting **FAILED**; C-23 velocity-group interpretation **UNIDENTIFIABLE**; C-25 through C-30 gas centroid and projection caveats unchanged. Merger-history `HaloID` is not automatically interchangeable with these z=0 `haloID` values. The 2026-06-26 `Mhistory_vel` correction is not implicated because velocity catalog fields were not used. Learning introduced: optical depth, area weighting and Jensen's inequality; understanding **NOT_ASSESSED**. No outreach, journal submission or approval implied.
