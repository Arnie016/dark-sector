# C-02 | Uneven acceleration, lensing and conformal-only limits

**16 October 2026. DERIVED + SIMULATION_RESULT; observational DATA_INSUFFICIENT.**

[Executed code](run.py) · [Actual result receipt](output/results.json) · [Identity/provenance](IDENTITY.json)

## Question

Does spatially different lensing require spatially different dark energy or a different initial cosmic era? No: the foreground matter arrangement and geometric distances already change the prediction. The physically interesting question is what remains after those effects are independently constrained.

Local acceleration g_i=-partial_i Psi varies across a structured matter field. A small separation s gives delta g_i=-sum_j(partial_i partial_j Psi)s_j. That second-derivative matrix is the tidal field. A constant local gradient has no differential term. This statement concerns a local weak-field bundle, not every measurement in an accelerated coordinate system.

The homogeneous background obeys ddot(a)/a=-(4*pi*G/3)sum(rho+3p/c^2), with rho a mass-equivalent density. It is not an independent Friedmann equation at each position. A constant positive Lambda can drive expansion without being a population of annihilating particles. A microscopic dark-matter annihilation model needs an actual rate and consistent energy transfer; products remain gravitating energy.

## An exact null for the proposed interpretation

Einstein's equation with explicit Lambda is R_ab-R*g_ab/2+Lambda*g_ab=8*pi*G*T_ab/c^4. Contract with a light-ray tangent k, which satisfies g_ab k^a k^b=0:

$$R_{ab}k^ak^b=\frac{8\pi G}{c^4}T_{ab}k^ak^b.$$

A pure Lambda term contributes zero to this **direct null Ricci focusing**. It can still change cosmological distances and growth, so this is not a claim that observed lensing is Lambda-independent. The optical focusing equation is D_A''=-[R_ab k^a k^b/2+|sigma|^2]D_A for a twist-free bundle before a caustic; sigma denotes optical shear, not a cross section.

## The line-of-sight equation

For weak scalar perturbations define Phi_W=(Phi+Psi)/2, where Phi and Psi have velocity-squared units and encode spatial curvature and the time-time potential. In a flat background at Born order,

$$\kappa(\mathbf n,z_s)=\frac1{c^2}\int_0^{\chi_s}d\chi\,\frac{\chi(\chi_s-\chi)}{\chi_s}\nabla_\perp^2\Phi_W.$$

For GR, negligible anisotropic stress and the usual subhorizon density projection,

$$\kappa=\frac{3H_0^2\Omega_m}{2c^2}\int_0^{\chi_s}d\chi\,\frac{\chi(\chi_s-\chi)}{\chi_s a(\chi)}\delta_m(\chi\mathbf n,z).$$

chi is comoving distance, a=1/(1+z), and delta_m is the fractional matter excess relative to the mean. Matter includes ordinary matter and dark matter. The units cancel: (H0/c)^2 is inverse-length squared, the geometric factor is a length and dchi is a length. Longitudinal/end-point terms are neglected in the standard density-projection step. This is not an exact horizon-scale or strong-lens equation. Smooth-background focusing is in the distance relation; delta_m=0 means zero *perturbative* convergence, not zero total cosmological focusing. The L-03 higher-order lens-lens term is deliberately omitted here.

## Worked matrix example: SIMULATED

Two thin excess-density planes lie at zl=(.3,.8). Two source distances have zs=(1,2). Adopt flat illustrative H0=67.4 km/s/Mpc, Omega_m=.315, Omega_Lambda=.685, radiation omitted and 0<=z<=3. Define q_i=4*pi*G*D_i*DeltaSigma_i/c^2, dimensionless physical surface-density strengths. Then

$$\boldsymbol\kappa=W\mathbf q,\qquad W_{si}=\max(0,1-\chi_i/\chi_s),$$

$$W=\begin{pmatrix}.636474944&.155162905\\.767238941&.459060185\end{pmatrix}.$$

Each row is a source redshift. Each column gives the weight of one foreground plane. Model A has q=(.02,.01). Model B has q=(.0214627086915546,.004), chosen to match the first source exactly, not fitted to data.

| Source redshift | SIMULATED convergence A | SIMULATED convergence B |
|---|---:|---:|
| 1 | .01428112793 | .01428112793 |
| 2 | .01993538067 | .01830326663 |

At the second, prespecified source redshift, the absolute difference is .00163211404. This is not a significance or sensitivity forecast.

For both sources behind both lenses,

$$\det W=(\chi_2-\chi_1)(1/\chi_{s1}-1/\chi_{s2})=.1731332821.$$

Thus two exact calibrated convergences identify two amplitudes in this restricted geometry. Coincident lens distances or duplicate source distances make the matrix singular. Real shear has additional source/mass-sheet freedom; this study assumes absolute convergence calibration instead of solving that problem. No noise, selection, redshift-error covariance or arbitrary radial mass reconstruction was included.

## A restriction on conformal-only explanations

For a smooth nonzero conformal rescaling in four dimensions,

$$\tilde g_{ab}=\Omega^2g_{ab},\qquad \tilde C^a{}_{bcd}=C^a{}_{bcd}.$$

C is the Weyl curvature tensor, which supplies the trace-free optical tidal source. If C=0, conformal rescaling alone cannot make it nonzero. An initially shear-free, twist-free beam gains no new Weyl-driven shear in such a conformally flat metric. Ricci focusing, redshift and distances may nevertheless change. The formula must not be naively applied at a singular crossover boundary.

At linear order a pure rescaling adds +c^2*omega to Psi and -c^2*omega to Phi, preserving Phi+Psi. Therefore a variable scale factor alone is not an extra shear source. Meissner-Penrose already introduce weak Weyl perturbations; this restriction is not an innovation over their work and does not disprove CCC.

A genuine extension must specify the perturbation, its crossover matching, species content and transfer to actual observables. Identical complete initial states followed by identical well-posed dynamics cannot be distinguished by assigning different historical labels. A fitted residual alone is not evidence of a prior aeon. Anthropically selected parameter ranges likewise require a prior and observer-selection model; lensing variations do not establish spatially varying constants.

## What ran and what did not

One deterministic standard-library CPU process, 20-second timeout, exit 0; total elapsed 2.014862 s, numerical core 0.0784703 s. Sixteen finite algebraic/implementation checks plus strict JSON readback. The same-distance null, foreground-source null, coincident-plane null and matrix inversion passed. No random seed, new dataset, paid service, installation or physical likelihood. The exact executed code hash is recorded in the result. No previous calculation was rerun.

The canonical ID is C-02. The executed code/result retain their provisional C-01 label because a final remote catalogue check discovered an independent existing C-01 initial-growth/bias branch. IDENTITY.json preserves that correction rather than silently rewriting execution evidence. The existing study was read and left untouched. More redshift bins cannot automatically overcome unrestricted bias or calibration functions.

## Checkpoints and next test

Research continuity: Files recovered L-03 README/conceptual note. The L-03 archive was inspected including complete code/results, not rerun. Main HEAD and README, branch catalogue and open PRs were inspected. Existing C-01 at f2dc1c17500f6abfe29903bf0d6c72d484120851 concerns galaxy tracer bias, not this two-plane geometry. N-04/N-05/L-03 branches were not modified. Earlier failures remain documented.

Learning: spatially different force versus tidal distortion versus homogeneous acceleration; distance weighting and rank; scale rescaling versus Weyl perturbations. These were introduced, not assessed as learner mastery.

Next: derive one boundary-normalized, gauge-consistent crossover perturbation and compare its lensing/redshift predictions against an ordinary primordial-feature model. In parallel planning only, the observational prerequisite is one calibrated redshift-binned likelihood with covariance. Stop with DATA_INSUFFICIENT without it; report UNIDENTIFIABLE if source freedom or initial-condition freedom makes the candidate identical to its null. No schedule changes, outreach, affiliation claim or manuscript submission.

## Primary methods and coverage

- Bartelmann & Schneider, arXiv:astro-ph/9912508v1 (23 Dec 1999), Physics Reports 340 (2001), Eqs.6.14-6.20 and projection caveats read. https://arxiv.org/pdf/astro-ph/9912508
- PDG Dark Energy, revised Aug 2025, Sections28.1-28.2 read; first-page screenshot inspected. https://pdg.lbl.gov/2025/reviews/rpp2025-rev-dark-energy.pdf
- Meissner & Penrose, arXiv:2503.24263v1 (31 March 2025), Sec.II assumptions/Eqs.6-7,15,23-28 and Sec.III conditional argument read. Accessible record lists v1; no later journal/version established. Full proof not independently verified. https://arxiv.org/html/2503.24263v1
- Hu, Heavens & Bacon, arXiv:2109.09785 (20 Sept2021), observable-conversion methods and Sec.3 read. https://arxiv.org/pdf/2109.09785
- Hu, arXiv:astro-ph/9904153 (1999), metadata/abstract prior-art lead for tomography, no forecast reproduced.

Targeted primary-source coverage as of 16 October 2026, not an exhaustive news survey or new exposure. The lensing-review screenshot failed; parsed equations were readable. No unread figure supplied evidence. The companion chat archive contains the long derivation, full CSV, high-resolution plot, frozen claim contract and run receipt; those extra assets are not uploaded in this compact contribution.
