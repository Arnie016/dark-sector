# C-10 | The common-calibration identifiability gate

**29 October 2026 | v1.0 | C10-C1 DERIVED, C10-C2 SIMULATION_RESULT / UNIDENTIFIABLE, C10-C3 DATA_INSUFFICIENT.**

A bounded methodological check of whether eleven observed merger systems can still share an unconstrained forward-model error. Not an observed dark-matter signal, a reanalysis of the published posterior, or a new cross-section limit.

## What is actually in the sources

Jee, Park & Lee, *A New Robust Constraint on the Self-interaction Cross-section of Dark Matter with Double Radio Relic Clusters*, [arXiv:2605.00093v2](https://arxiv.org/html/2605.00093v2), dated **9 July 2026**, peer-reviewed as [ApJ 1007, 56](https://doi.org/10.3847/1538-4357/ae88fb) on **10 August 2026**. Table 2 prints rounded shock and halo separations for 11 observed clusters. Sections II.4/II.6 report **576** numerical merger-grid cases, **20** newly run off-grid cases for within-framework interpolation checks (agreement within 2%), and an eleven-system product of marginalized posteriors because only SIDM cross-section is shared in the specified likelihood. The **published** conditional limit is 0.22 (0.63) cm²/g at 68% (95%); **it is not reproduced here**.

Lee et al., *TNGC-SIDM I*, [arXiv:2610.18957v1](https://arxiv.org/html/2610.18957v1), **13 October 2026**: two independently selected cosmological cluster-merger systems at collisionless and SIDM cross-sections. Sections 5.1/5.2 describe resolution and projection sensitivity, including a 3D-cell radio-relic identity unavailable to ordinary observations when relics overlap. **Data availability** says simulation data directly related to the paper are on reasonable request; public simulation-suite release is planned, not established.

**A 2% interpolator error on 20 off-grid cases from the same simulation framework is not an observational/model-discrepancy bound on independent cluster formation histories.** This does not demonstrate that the published Bayesian analysis is wrong. It identifies a *different*, still-unmeasured validation contract.

## Physical observable and one mathematical tool

For each cluster, let S be the radio-shock separation and H the lensing-estimated halo separation, both in Mpc. The dimensionless logarithmic ratio is z=ln(H/S). Under the first-order delta method with no within-system error correlation, the **illustrative** marginal variance is

v_i = (sigma_Si/S_i)^2 + (sigma_Hi/H_i)^2.

The actual paper fits both distances jointly with physical parameters and mass priors. These derived variances do NOT reproduce its likelihood or even a true per-system joint covariance.

Now introduce a deliberately **SIMULATED** common-residual model:

y_i = delta + b + epsilon_i, where epsilon_i ~ N(0,v_i).

Here delta is an unknown *common dimensionless residual shift*, **not** the SIDM cross-section. b represents *shared model calibration error*, common to all clusters. We do not know the actual physical baselines, b distribution, or the response d(log H/S)/d(sigma/m).

Let W=sum(1/v_i). The likelihood-plus-Gaussian-calibration-prior (b ~ N(0,tau²)) information matrix for parameters (delta,b) is

F = ((W,W),(W,W+tau^-2)).

The diagonal is information curvature and the off-diagonal captures confounding. Profiling out b gives
I_delta = W - W²/(W+tau^-2), hence Var(delta)=W^-1+tau².

**AHA, explanatory not discovery:** Eleven distinct astronomical observations may share the same uncertain physical *calculation*. If delta and b enter in precisely the same direction, their likelihood columns coincide; without a calibrated prior, the model is **UNIDENTIFIABLE** however many objects are observed. If real parameter-response and calibration vectors are not aligned, this exact degeneracy need not apply.

## Reproducible single-CPU arithmetic

Run: python3 C10_common_calibration_run.py > results.json. Executed once in a ChatGPT Linux Python 3.13.5 process under 20-second hard timeout, exit 0, observed shell wall time **1.19 s**, seed none. All eleven *OBSERVED AS REPORTED* rounded Table 2 marginal values are transcribed into the script.

- Under the deliberately schematic common-offset model, independent-error standard deviation = **0.0355682** log-ratio units.
- Pure inverse-variance weight concentration N_eff=(sum w)^2/sum(w²) = **5.3146**. This is not a physical sample size or SIDM posterior effective count.
- With **SIMULATED** common calibration prior standard deviation tau=0.020, illustrative error rises to **0.0408056** (14.72% higher error bar). **The 2% is made up for the stress test; it is NOT the paper's 2% interpolation validation and not a new uncertainty estimate.**
- Nine checks passed, including scale invariance, Schur-complement algebra, rank-one null and limiting cases. Some are simple arithmetic/bookkeeping checks and do not validate astrophysics.

Executed original script SHA-256: 81b9be5b77cbc5cab4cdbbd6d2e5cf3dde37a4a8b14ed44e486c6e6ec9ba5469. Raw original result SHA-256: 41dd723a6f8cb65da31ca55ce232200d6b26596e08a43d98b7a9f2e3a5547fc8. The exact result receipt and expanded methods are in the corresponding ChatGPT research companion; this compact public commit adds the code and chapter, but does **not** claim to have uploaded the raw JSON or CI logs.

## Falsifier and decision

Strongest null: simulation-domain errors could be negligible in the relevant observational likelihood, or the true dark-matter response and shared error vectors may differ enough to be separable. A common additive log-ratio bias is *not* established by either source.

**Stop:** no new sigma/m limit, publication claim or critique of the published 0.22 cm²/g posterior without calibrated emulator outputs and selection/covariance. **Next:** recover physical per-cluster response vectors and independent matched-halo residuals, then use independent initial conditions as holdouts. Repeated snapshots are not independent simulations.

**Continuity:** C-09 covers within-cluster error correlations. C-10 covers conditional shared forward-model errors across clusters. Preserve C-06/C-08 identifiability nulls, C-03's FAILED globally unscreened gravity theory and N-06's corrected sign bound.

**Learning checkpoint:** Fisher curvature, shared calibration nuisance and exact rank-one unidentifiability introduced; **demonstrated understanding NOT_ASSESSED**. No new outreach or journal submission is claimed.
