# C-03 follow-up | A screened-shell closure test

**17 October 2026.** Status: DERIVED within a specified approximation; CONJECTURE for observational usefulness; DATA_INSUFFICIENT for a measurement. No numerical experiment was executed for this note. This is a research contract, not an announced result or new theory.

## Why change the question?

The preceding R + L^2 R^2/6 calculation is a known weak-field benchmark with a known failure when its long unscreened range is extended to the Solar System. Preserve it as a baseline. Repeating its solution with another numerical method will not supply novelty or observational evidence.

The next question is whether a physically screened scalar can produce a constrained radial relationship between motion and lensing that survives uncertainty about the mass distribution. Screening means suppression of the extra force in specified environments. It is not an arbitrary radius switch applied to the old quadratic theory. A candidate must ultimately predict its scalar profile, screening and local-test behavior using one consistent model.

## A specific real-data motivation

Pizzuti et al., arXiv:2604.23631v1, published in Universe 12 (2026) 124 on 26 April 2026, compare kinematics and lensing for nine previously observed CLASH/CLASH-VLT clusters. Their conclusions depend on the adopted density profile: cuspy profiles agree with GR, whereas a cored Burkert profile produces an apparent roughly 2-sigma combined deviation. The latter profile is disfavored by the lensing evidence, and cuts on disturbed systems reduce the apparent tension. This is the authors' analysis, not ours; it is not nine new 2026 exposures or independent confirmation of a force.

Read: theoretical Eqs. (5)-(10), screening approximation, kinematic modeling in Section 3, profile/systematics discussion in Section 4 and conclusions. No raw velocities, lensing posterior draws or covariance were recovered. https://arxiv.org/html/2604.23631v1 ; journal metadata https://doi.org/10.3390/universe12050124

Decision: do not chase the apparently most significant profile. Ask whether a physical force relation remains supported when mass-profile freedom is propagated consistently.

## Derive a restrictive prediction rather than fit an arbitrary extra curve

Let M(r) be total enclosed ordinary plus dark matter mass. Work in a spherical, quasi-static weak-field patch. Assume:

- The conformally coupled scalar has negligible direct leading lensing contribution, so the consistently deprojected lensing mass is M_lens(r) approximately M(r).
- A core r < r_s is screened, with negligible scalar gradient at r_s.
- In the active outer region, the scalar potential derivative and finite-range suppression are negligible compared with its matter source. This is the long-range screened-shell approximation, not the full nonlinear equation.
- The dynamical tracer responds without additional self-screening. Its inferred acceleration accounts for pressure/orbit support, equilibrium and projection uncertainties.

For a scalar coupling beta, define alpha=2 beta^2. Rewriting the shell field equation in SI force units gives

$$\frac{d}{dr}[r^2 g_\phi(r)]=\alpha G\frac{dM(r)}{dr},\qquad g_\phi(r_s)\simeq0.$$

Here g_phi is the positive inward extra acceleration. Integrating rather than prescribing its shape yields

$$g_\phi(r)=\frac{\alpha G}{r^2}[M(r)-M(r_s)]\quad(r>r_s).$$

Define the motion-inferred effective enclosed mass M_dyn=r^2 g_dyn/G. This definition does NOT assume circular orbits for observed cluster galaxies; g_dyn must come from an appropriate dynamical model. With g_dyn=G M/r^2+g_phi,

$$\boxed{\Delta M(r)\equiv M_{\rm dyn}(r)-M_{\rm lens}(r)\simeq\alpha[M_{\rm lens}(r)-M_{\rm lens}(r_s)]_+.}$$

The positive-part notation means zero inside the screened core for a nondecreasing enclosed-mass profile. In a plot of Delta M against M_lens, the ideal prediction is a flat segment followed by a straight segment of slope alpha. For the conventional f(R) scalar coupling beta=1/sqrt(6), that slope is 1/3. This is an elementary consequence of established screened-scalar equations, NOT a newly discovered force law.

Crucially, changing the screening radius moves the join; it does not independently change the outer slope when coupling and tracer response are fixed. A nonlinear field solution must determine whether the approximation holds over the observed range. A finite scalar range, a gradual transition or self-screened tracers can invalidate this simple broken-line form.

Adding more conventional dark matter in GR changes BOTH correctly inferred masses, and does not by itself generate Delta M. Incorrect deprojection or dynamical modeling can nonetheless produce apparent Delta M. This diagnostic is not immune to those systematics, and it must not be fitted by ordinary least squares: M_lens appears on both axes, making the errors correlated.

## Claim contract C-03-H2

**Target:** a joint forward model with flexible positive matter profiles and a single specified screened-scalar theory improves prediction of withheld kinematic observations relative to a GR model with the same mass-profile flexibility.

**Strongest null:** source/lens geometry, a restrictive mass-profile prior, velocity anisotropy, non-equilibrium or tracer self-screening creates or erases the apparent force. The 2026 source explicitly demonstrates reasons to take this null seriously.

**Required inputs:** lensing likelihood or posterior with selection and calibration; projected member positions and velocities with membership/completeness; tracer-density information; independent environmental information; consistent cross-probe covariance. The scalar's Solar-System behavior must be calculated or constrained using the same parameters, not claimed by invoking screening verbally.

**First work unit:** recover a real joint dataset or its sufficient likelihood inputs and reproduce one published GR baseline. Select the object for input completeness and independent dynamical quality, not the largest residual. If input access fails, report the exact missing files. Do not manufacture a data vector from a contour plot.

**Predictive test:** use identical flexible mass models and observation operators for GR and screened gravity; preserve errors on both mass functions and their covariance. Hold out independent observations or entire systems where possible. Binned radii are correlated, not independent replications. Selection based on dynamical disturbance must be modeled and must not use the desired outcome.

**Stopping rule:** if the apparent effect disappears with profile freedom, plausible orbital uncertainty or held-out predictions, reject the claimed discriminator for that dataset. A result that only occurs under the profile already disfavored by lensing is not support for new gravity.

## Nearby prior art and access boundary

Landim et al., arXiv:2407.08825v2, already compare gas and stellar kinematics with screened/unscreened controls. Sections 3-4 explain the MaNGA inputs, drift corrections and calibration. Its public NIRVANA repository was inspected at the root, but no fitted catalog or full likelihood was recovered. Do not present gas-versus-star comparison itself as novel. https://arxiv.org/html/2407.08825v2 ; https://github.com/ricardoclandim/NIRVANA

The novelty of an eventual profile-robust, environment-linked closure analysis remains PRIORITY_UNCHECKED. No forecast, significance, fit, new field solution or independently verified publication is reported by this note. A CCC connection would require deriving the same field and boundary conditions from that proposal; none is asserted.

## Continuity

C-03 methods were read through Files. Remote main and PR #8 were inspected; this note is appended to that existing branch without replacing its executed code or results. Research state: known unscreened benchmark parked, conditional observational target defined. Learning state: extra force as a mass-profile difference and shared-axis covariance introduced; learner understanding unassessed. No schedule change, external outreach, installation, payment or manuscript submission.
