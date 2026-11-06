# C-08 | A free projection calibration restores merger-drag non-identifiability

**27 October 2026 · v1.0 · DERIVED / SIMULATION_RESULT / UNIDENTIFIABLE / DATA_INSUFFICIENT.** This is a small, expressly SIMULATED extension of [C-06](METHODS_RESULTS_v1.0.md) and [C-07](C07_PROJECTION_CORRECTION_2026-10-27.md), not an observational dark-matter constraint.

## Question and precise falsifiable statement

C-07 showed that using a *fixed*, nonzero radio-shock projection exponent can restore local rank at orbital turnaround. But in another cluster, what if that exponent has not been separately calibrated? In the same three-observable toy, **a freely varying projection exponent permits a continuous family of dark-drag parameters with identical predictions at turnaround**. A calibrated exponent or an independent angle/phase observable can break this constructed degeneracy.

[Jee, Park & Lee, arXiv:2605.00093v1, 30 April 2026, §II.3](https://arxiv.org/html/2605.00093v1) use projected shock separation proportional to cos^eta(alpha), with eta≈0.223 fitted in one illustrated simulation configuration and subsequently used in their interpolated analysis. This is a preprint; we have not obtained a cluster-dependent eta covariance or replicated their 11-cluster posterior. Their §II.6 likelihood actually fits two projected separations with astrophysical priors, **not the toy BCG-speed measurement** used below. Its published 68% upper limit of 0.22 cm²/g is their model-conditional reported inference, not challenged by this toy.

## Worked tool: inverse map and Jacobian

The SIMULATED model has measured coordinates R (shock separation, kpc), H (halo separation, kpc) and U (galaxy line-of-sight speed, km/s), and unknown parameters k (illustrative drag coefficient labelled cm²/g), t (Gyr), alpha (viewing angle in radians) and eta (dimensionless shock projection exponent). Adopt C-07's nonphysical benchmark dynamics:

$$
R=st\cos^\eta\alpha,\qquad
H=[H_0(t)-bk]\cos\alpha,\qquad
U=v(t)\sin\alpha,
$$

$$
H_0(t)=H_*-\tfrac12 A(t-t_*)^2,\qquad
v(t)=-A(t-t_*)/c_v.
$$

Here s is a speed in kpc/Gyr, H_* is a length, b converts k into a displacement, A has kpc/Gyr² units and c_v converts km/s to kpc/Gyr. At turnaround t=t_* and any nonzero inclination alpha strictly between 0° and 90°, U=0. For *any* admissible k,

$$
\cos\alpha(k)=\frac{H}{H_*-bk},\qquad
\eta(k)=\frac{\ln[R/(st_*)]}{\ln\cos\alpha(k)}
$$

reproduces the same R,H,U. This explicit family, rather than simply counting four unknowns and three observables, establishes the scoped non-identifiability.

The Jacobian's rows are the three observables and its columns are k,t,alpha,eta. The determinant of its nuisance columns (t,alpha,eta) at turnaround is

$$
\det J_{\mathrm{nuis}}=
R\,\ln(\cos\alpha)\,(H_*-bk)\,v'(t_*)\,\sin^2\alpha.
$$

It is nonzero in a generic inclined case, so nuisance adjustments can compensate a local change of k. In the face-on limit alpha=0, the log term vanishes and the formula for eta becomes undefined. With eta fixed, the C-07 rank-restoration result applies under its own assumptions.

## Actually executed SIMULATED example

One standard-library Python 3.13.5 process in a ChatGPT Linux container completed under a 20-second hard timeout, exit 0, deterministic (no seed). Inputs inherited from C-07: s=3600 km/s converted to kpc/Gyr, H_*=1200 kpc, b=150 kpc/(cm²/g), A=1400 kpc/Gyr² and t_*=0.8 Gyr. Generating truth: k=1, alpha=30°, eta=0.223.

| SIMULATED combination | k [cm²/g] | alpha [degrees] | eta |
|---|---:|---:|---:|
| Generating truth | 1 | 30 | 0.223 |
| Exact alternative | 0.5 | 36.07076865 | 0.15071166 |
| Unrestricted collisionless toy | 0 | 40.73180588 | 0.11564434 |

All give R=2852.4316096 kpc, H=909.3266740 kpc and U=0 km/s to numerical precision. The k=0 alternative **falls outside** the cited paper's fiducial viewing-angle prior alpha≤40°, so do not use it to dispute that paper's fiducial inference. The analytic nuisance minor is 1.474354654×10^8 in mixed units; an independent finite-difference approximation differs relatively by 9.78×10^-11. Seven scripted assertions passed, **at most six informative**: the check named "zero_drag_coefficient_removes_k_sensitivity" actually verifies only that R does not depend on k. This misnamed check is explicitly retained, not counted as independent corroboration.

Executed source SHA-256: 00e3e70947b96df18cb37abf60c84a8f86457e407444165173e103f1b23f308e. Raw SIMULATED JSON SHA-256: e2eafd3afc70208fc3e345e976eb89977c1263cd77d46be028f93f4ac54dc71b. The exact source and raw JSON are preserved as verified *ChatGPT run companion files*, **not uploaded in this compact repository note**. The external wall time was not independently measured; no external simulator, calibrated physical rate, observational likelihood or CI was run.

## Verdict, failure gate and next measurement

**C08-C1 DERIVED / UNIDENTIFIABLE** under free eta and declared toy. **C08-C2 SIMULATION_RESULT** for the matching numbers above. **C08-C3 DATA_INSUFFICIENT** for real clusters. A broad nuisance prior can mimic effects; a narrow independently justified calibration can rule out those mimics. Priors and selection affect the posterior, so this is not a refutation of Jee et al.'s inference.

The strongest conventional rival is a collisionless merger with different angle, phase and gas/shock response. The gate is a *publicly calibrated mass/phase/angle-dependent shock-projection response* and its residual/covariance, followed by matched independent CDM/SIDM merger holdouts and a joint radio/lensing/velocity likelihood. A mock mimic rejected by such calibrated inputs would invalidate this conditional counterexample for that physical population. Do not report cross-section sensitivity from uncalibrated toy measurements.

**AHA (explanation, not discovery):** an added observation can apparently resolve a particle-physics ambiguity but simultaneously introduce a new uncertain calibration. The observation helps only when the mapping between its signal and geometry is controlled.

**Research checkpoint:** C-06's eta=0 null, C-07's fixed-eta correction and C-08's free-eta degeneracy are different assumption domains, not conflicting empirical discoveries. C-05 collision-history non-identifiability remains, and C-03's unscreened long-range gravity model remains FAILED. **Learning checkpoint:** calibration and structural identifiability introduced, demonstrated understanding NOT_ASSESSED. No email, journal submission or new schedule was initiated by this study.
