# C-01 | Initial amplitude, late growth, and galaxy bias

**16 October 2026 (Singapore) | version 1.0**
**Statuses: DERIVED + SIMULATION_RESULT; conditional UNIDENTIFIABLE; observational DATA_INSUFFICIENT.**

## Physical question

A small early density fluctuation grows under gravity. An unusual galaxy clustering amplitude might be caused by a different *initial* fluctuation or by modified *later* growth. A galaxy survey observes galaxies, not the matter distribution directly. The relation between galaxy and matter clustering is described by a redshift-dependent tracer bias.

**Explanatory AHA (not a discovery):** adding redshift bins is useful only if the relation between what the survey measures and the underlying matter is constrained. A smooth change in bias can perfectly mimic a change in growth.

## Worked model and assumptions

Consider one fixed comoving wavenumber k = 0.05 h/Mpc, a wavelength of 125.66 h^-1 Mpc (approximately 186.4 Mpc if h=0.674). This is a synthetic large-scale illustration, not a physical particle forecast, survey likelihood or halo simulation. Divide all powers by one common arbitrary power unit, so the following logarithms are dimensionless. Let the scale factor a(z)=1/(1+z) and define

$$
P_m(k,z)/P_{\rm unit}=P_* [a(z)/a(1)]^{2g}.
$$

P_* is the normalized matter power at redshift 1; g is a phenomenological constant growth exponent only over 1 <= z <= 3. The matter-dominated limit g=1 is not a complete Lambda-CDM growth model over all redshifts. We choose SIMULATED P_*=0.8, g_true=0.9 and g_alternative=1.0.

At z=1 the models agree. At z=3 the two matter predictions are, respectively, 0.22973967099940698 and 0.2, differing by 14.8698% relative to the latter.

### Mathematical tool: the Jacobian and its null directions

With A=ln(P_*), y_i=ln(P_m(z_i)/P_unit), the sensitivity matrix for matter at z1=1 and z2=3 is

$$
\begin{pmatrix}y_1\\y_2\end{pmatrix}=
\underbrace{\begin{pmatrix}1&0\\1&-2\ln2\end{pmatrix}}_{X_m}
\begin{pmatrix}A\\g\end{pmatrix}.
$$

Each row is a measured epoch. The first column is the response to earlier amplitude; the second is the response to later growth. The determinant is -2 ln 2, so both unknowns are identified from exact **matter** power at these two epochs, under the stated model and known relative calibration.

A galaxy clustering survey approximately measures P_g=b(z)^2 P_m on appropriate large scales. With beta_i=ln b(z_i), its Jacobian is

$$
\begin{pmatrix}y^g_1\\y^g_2\end{pmatrix}=
\underbrace{\begin{pmatrix}1&0&2&0\\1&-2\ln2&0&2\end{pmatrix}}_{X_g}
\begin{pmatrix}A\\g\\\beta_1\\\beta_2\end{pmatrix}.
$$

This 2x4 matrix has rank 2, with two explicit independent null vectors:

$$
X_g(2,0,-1,-1)^T=0,\quad X_g(0,1,0,\ln2)^T=0.
$$

A null vector is a change to the unknown parameters that leaves **all the specified measurements unchanged**. It is therefore a structural ambiguity that noiseless precision cannot resolve. The second null exchanges growth with higher-redshift tracer bias.

For all z in this model, set

$$
b_{\rm alt}(z)=[a(z)/a(1)]^{g_{\rm true}-g_{\rm alt}}=[a(z)/a(1)]^{-0.1}.
$$

Then b_alt(z)^2 P_m,alt(z) = P_m,true(z) **identically**. At z=3, b_alt=1.0717734625362931, a 7.1773% bias change. The alternative and true galaxy powers are exactly the same, even though the dark-matter powers differ. Interpolated redshift samples do not constitute independent observations.

## Falsification and limits

**Claim C-01:** the two-epoch matter Jacobian is invertible with the stated known calibration, while the galaxy Jacobian remains rank-deficient if tracer biases at both redshifts are unrestricted. The explicit bias function is a concrete counterexample to interpreting a growth discrepancy as automatically new physics.

**Strongest conventional explanation:** ordinary redshift evolution of galaxy selection or halo occupation. **Stop rule:** if nuisance functions allow two growth histories to yield identical measured predictions, report UNIDENTIFIABLE. Do not infer dark matter microphysics, cross section, discovery significance or a posterior from this synthetic identity.

No CMB or galaxy data, likelihood, selection function, instrumental covariance, survey window, transfer function, nonlinear power or weak-lensing kernel was loaded. The 0.05 h/Mpc illustrative mode does not certify a real survey scale as linear.

## Execution and provenance

One bounded deterministic Python-standard-library computation generated a full 81-point **SIMULATED** CSV trace and an SVG from the same equations, checking 14/14 identities. Full generator SHA-256: c49b45279c1542985efa5d54094c636a871a8b8c2554229aa2c2d6950c589a93. This repository also includes a smaller executable verifier of the core result: **8/8 assertions**. Its code is not the same as the full plotting generator. No random seed was used. No experimental data were simulated with a detector response, and neither calculation reproduces an external cosmology baseline.

**Source coverage verified 16 October 2026 (primary methods):**

1. Novell-Masot et al., [arXiv:2503.09714v2, 6 June 2025](https://arxiv.org/html/2503.09714), published JCAP06(2025)005 on 6 June 2025. Methods sections 2 and 3 model DESI DR1 galaxy power and bispectrum with nuisance bias, noise and covariance. Joint power-plus-bispectrum partly breaks growth-amplitude degeneracy. These are statistics from overlapping DR1 galaxy observations, not independent telescope exposures.
2. Andrews et al., Euclid Consortium, [arXiv:2412.11945v1, 16 December 2024](https://arxiv.org/html/2412.11945), [A&A 711 A94, July 2026](https://www.ipac.caltech.edu/publication/2026A%26A...711A..94A). Inspected arXiv v1 methods sections 2.1, 2.3 and 3.3: primordial conditions are propagated into a biased selected mock galaxy field. The same forward model is used for simulation generation and inference. The July peer-reviewed article has not been line-by-line compared to preprint v1.
3. Ivanov et al., [PRD 114, 063526, published 17 September 2026](https://journals.aps.org/prd/abstract/10.1103/sjff-yj2t). Metadata and abstract checked, full subscriber-only methods not inspected. Its DESI DR1 clustering sample overlaps earlier DR1 work. Not new independent exposure.

These sources are established prior art and do not provide empirical inputs for the simulated values here.

## Research and learning checkpoints

**Research state:** this C-01 result is independent of N-03 neutrino phase averaging on main. D-01 solar-versus-sidereal and L-03 lens-core null existed on other unmerged branches at intake and were left unchanged. Earlier failed phase-export executions remain documented. Actual DESI/Euclid likelihoods, bias calibration and lens flux posteriors remain unavailable in this run.

**Learning state:** introduced the log-power sensitivity Jacobian, its zero-response null directions, tracer bias and the distinction between initial amplitude and later growth. Reader mastery is NOT_ASSESSED.

**Recommended next:** recover a single version-locked multi-probe data product that constrains galaxy bias independently, such as galaxy clustering plus lensing cross-correlations or validated power-plus-bispectrum likelihood and cross-covariance. Only then compare held-out growth predictions. No outreach, paid compute, journal submission or schedule change.
