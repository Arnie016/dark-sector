# C-03 | Solve the field equations before interpreting a lensing anomaly

**16 October 2026 · DERIVED + SIMULATION_RESULT.** Known metric f(R) gravity, implemented as a bounded weak-field boundary-value solve. No new particle, CCC crossover solution or observational fit.

[Executed code](run.py) · [Actual result receipt](output/results.json) · [Identity mapping](IDENTITY.json)

## What changed

The earlier C-01 conformal metrics had no supporting field-equation solution. Here we explicitly choose metric f(R)=R+L^2 R^2/6 gravity with matter minimally coupled to its physical metric. This is a controlled dynamical completion of the geometry question, NOT a theory derived from Penrose's conformal cyclic cosmology. With a prescribed weak source, the extra attraction and leading lensing cancellation follow from solved equations instead of arbitrary potential shifts.

## Derive the equation and its solution

Use signature (-,+,+,+), R in m^-2 and potentials Psi,Phi in m^2/s^2. Set F=df/dR=1+L^2 R/3. The metric field equation is

$$F R_{\mu\nu}-\frac12f g_{\mu\nu}+(g_{\mu\nu}\Box-\nabla_\mu\nabla_\nu)F=\frac{8\pi G}{c^4}T_{\mu\nu}.$$

Tracing means contracting with the inverse metric. It produces

$$FR-2f+3\Box F=\frac{8\pi G}{c^4}T.$$

In this quadratic theory the R^2 terms cancel, yielding the exact trace equation

$$L^2\Box R-R=\frac{8\pi G}{c^4}T.$$

Now make the stated weak, static, nonrelativistic approximations: T approximately -rho*c^2, Box approximately the spatial Laplacian. For u=F-1, the coupled linearized equations reduce to

$$(\nabla^2-L^{-2})u=-\frac{8\pi G}{3c^2}\rho,\quad \nabla^2\Phi_N=4\pi G\rho,$$

$$\Psi=\Phi_N-\frac{c^2u}{2},\qquad\Phi=\Phi_N+\frac{c^2u}{2}.$$

The sum Phi+Psi=2Phi_N determines leading lensing at fixed source geometry. Slow-body motion depends on -gradient(Psi). The scalar field's range L determines where the extra contribution decays; it is not a fitted lensing coefficient.

For a pointlike source, asymptotic decay and the source normalization give

$$u=\frac{2GM}{3c^2r}e^{-r/L},$$

$$\Psi=-\frac{GM}{r}(1+e^{-r/L}/3),\qquad\Phi=-\frac{GM}{r}(1-e^{-r/L}/3).$$

Differentiate the potential, rather than equating potential and acceleration ratios:

$$\frac{|g|}{GM/r^2}=1+\frac13(1+r/L)e^{-r/L}.$$

These equations and their known weak-source interpretation follow the field-equation treatment in [De Felice & Tsujikawa, 2010, Secs. 2 and 5.1](https://doi.org/10.12942/lrr-2010-3). This is an independent implementation of established mathematics, not an original law.

## Finite-source boundary problem actually solved

Use a uniform sphere with M=10^11 solar masses and radius Rs=10 kpc, with L=100 kpc. These are SIMULATED inputs. Define x=r/L, a=Rs/L=0.1, epsilon=GM/(Lc^2), q=u/epsilon, S=2/a^3. Inside, q''+2q'/x-q=-S; outside the right side is zero.

Require regularity at the center, continuity of q and q' at the surface, and decay at infinity. Analytic matching gives

$$q_{in}=S\left[1-(1+a)e^{-a}\frac{\sinh x}{x}\right],$$

$$q_{out}=\frac23\mathcal F(a)\frac{e^{-x}}x,\qquad\mathcal F(a)=\frac{3(a\cosh a-\sinh a)}{a^3}.$$

An independent finite-difference solver evolves y=xq as a boundary-value problem without calling the analytic profile. Two grids have 4000 and 8000 intervals over x in [0,10]. The analytic form factor is 1.0010003572, not silently set to one. Leading hydrostatic support p(r)=rho[Psi(Rs)-Psi(r)] is positive and small, with central p/(rho*c^2)=3.187e-7. Pressure corrections to the gravitational source are beyond retained order. No stability claim for the uniform sphere is made.

| Radius | SIMULATED attraction / Newtonian value | Fixed-source leading lensing ratio |
|---|---:|---:|
| 10 kpc | 1.332106 | 1.000000 |
| 100 kpc | 1.245498 | 1.000000 |
| 300 kpc | 1.066449 | 1.000000 |
| 1000 kpc | 1.000167 | 1.000000 |

## The observational gate this benchmark fails

If the same constant 100-kpc range applies in the Solar System without suppression, the post-Newtonian potential ratio is

$$\gamma=\Phi/\Psi=(1-e^{-r/L}/3)/(1+e^{-r/L}/3)\simeq1/2.$$

[Cassini's published result](https://doi.org/10.1038/nature01997) is gamma=1+(2.1 +/- 2.3)*10^-5. This 2003 result used the 2002 solar conjunction. Its published measurement was checked, not its raw likelihood rerun. Therefore the constant long-range globally unscreened candidate is FAILED as a viable interpretation. No new sigma level is calculated.

Finite range is not environmental screening: 100 kpc remains effectively long throughout the Solar System. A surviving scalar theory must justify suppression locally, typically by changing its action and solving its environment-dependent field profile. It cannot repair this failure by ignoring it or fitting a cosmological summary instead.

## Recent-data check

[DES Y6 arXiv:2601.14559v2](https://arxiv.org/html/2601.14559v2) was posted 29 January 2026 after v1 on 21 January; its observations were taken in 2013-2019 and overlap earlier releases. Data, covariance, scale cuts and availability sections were read. Its linear-bias analysis keeps 602 vector entries after cuts and excludes lens bin 2; galaxy-galaxy lensing uses a 6 Mpc/h lower separation cut. Our 100-kpc static prediction cannot be substituted directly for this cosmological likelihood.

The official release pointer https://des.ncsa.illinois.edu/releases/y6a2 returned no parsed data in web access, and direct container retrieval failed DNS. No joint data-vector/covariance pair was recovered or fitted. The accessible paper says products would be released upon journal acceptance; current global availability or journal acceptance was not established here. Missing access is not proof that the data do not exist.

A September 2026 lead arXiv:2609.04419 was found in secondary indexing but primary abstract/HTML/PDF retrieval failed. No conclusion relies on that inaccessible paper. [Meissner & Penrose v1](https://arxiv.org/html/2503.24263v1) was revisited for crossover assumptions; it does not supply this R^2 action. No conformal crossover is solved here.

## Execution and next step

Run `python run.py --output output` with Python's standard library. One CPU process, 25-second timeout, exit 0. Eighteen finite implementation/limiting checks plus JSON readback passed. The fine-grid maximum profile error, normalized to the analytic central scalar, is 5.0366e-5; halving spacing reduces it by a factor of 3.999996. Numerical core 0.02110124 s; total process 1.13877857 s. These are discretization errors, not experimental confidence intervals.

This solves only the STATIC LINEARIZED field equations, not the full nonlinear cosmology. Fixed-source leading lensing cancellation does not imply identical cosmological lensing maps after growth and distance effects. G denotes the action's gravitational coefficient, not a silently recalibrated locally measured constant.

**Research checkpoint:** C-01 archive/code/results were read and hashed, not rerun. Remote C-02 tomography PR #7 was identified and left untouched. This study is C-03; raw execution retains its provisional C-02 ID with an explicit mapping. Older failures remain historical. No schedule change, external outreach or manuscript submission.

**Learning checkpoint:** introduced action versus chosen metric, tracing equations, regular boundary solutions, force versus potential and local-versus-cosmological validation. Learner understanding remains unassessed.

**Recommended next bounded test:** solve one specified screened model in both a low-density and Solar-System environment. Reject it if its local scalar charge remains inconsistent with local constraints. For a CCC-specific branch, derive the actual permitted perturbation and matching conditions instead of importing this unrelated action. No observed-data fit should precede these validity gates.
