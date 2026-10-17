# S-01 | Can viewing angle imitate self-interacting dark matter?

**17 October 2026.** Status: **DERIVED** (Jacobian rank), **SIMULATION_RESULT** (deterministic mock), **UNIDENTIFIABLE** (halo plus an idealized stage reference), **DATA_INSUFFICIENT** (observed merger likelihood).

[Executable study](run.py) | [Numerical receipt](output/results.json) | [Research and learning checkpoint](CHECKPOINT.md)

## Physical question and the 2026 motivation

At the same merger stage, self-interacting dark matter (SIDM) can reduce the dark-halo separation. But viewing a collision axis at an inclination to the sky also shortens the *projected* separation. Does adding a radio-relic shock separation measurement distinguish the mechanisms?

Lee et al., [*TNGC-SIDM I*, arXiv:2610.18957v1](https://arxiv.org/html/2610.18957v1), was submitted **13 October 2026**. Their **preprint simulations**, not observed measurements, comprise two cosmological matched-CDM/SIDM cluster mergers, with benchmark sigma/m=1 cm²/g and another sigma/m=0.5 cm²/g run for the smaller cluster. Their ``4.1 and 5.2 show that double radio-relic separation approximately tracks time since collision, while halo separation changes with SIDM and inclination. They explicitly identify relative line-of-sight (LOS) BCG velocity as a complementary observable. Their `5.1 reports important resolution dependence in the lower-mass case. The **Data Availability** section says paper-level data are available upon reasonable request and the full TNGC-SIDM suite is planned for future release. No original track or measurement covariance was accessed.

The point of this bounded step is a checked *identifiability* limit, not to pretend the reported 100–270 kpc differences are an analytic linear law.

## AHA: Two explanations can produce the same image for different reasons

An apparent decrease in halo separation can come from **drag caused by self-interaction** or from **shortening due to inclination**. A shock distance can anchor approximate merger stage, but does not automatically determine orientation. To resolve the issue, the extra observable must respond *differently* to the unknown parameters.

### Worked model, all SIMULATED

At fixed stage, define the dimensionless strength `s=(sigma/m)/(1 cm²/g)` and viewing angle `theta` from the sky plane. Let `H0` be 1500 kpc, a deliberately linear interaction response `A` be 200 kpc per unit s, and relative physical speed `V` be 1800 km/s. The model predicts projected halo separation H in kpc and relative line-of-sight speed in km/s:

\[
H(s,\theta)=(H_0-As)\cos\theta,\qquad V_{\rm los}(\theta)=V\sin\theta.
\]

The idealized radio-relic distance is **fixed at 3000 kpc by construction**, to represent a known merger stage; *real* relic distance varies somewhat with interaction model, inclination, shocks and detection threshold. The assumed A is **not** a coefficient measured or fitted in TNGC-SIDM. Its validity does not extend to arbitrary stages, masses or cross sections.

Inject `s=0.8` at `theta=15°`, yielding **SIMULATED** H=1294.340607 kpc and LOS speed=465.874281 km/s. Exactly the same H arises from collisionless `s=0` at theta=30.356939°. The alternative predicts LOS speed=909.693710 km/s. Without LOS velocity, every s in [0, 1.028297] admits an exact H match for an inclination in the allowed [0°,50°] interval.

## The mathematical tool: Jacobian rank

A *Jacobian* is a table of local measurement sensitivities. Rows are measured channels (H in kpc, LOS speed in km/s); columns are parameters (dimensionless s and angle theta in radians). Differentiate the predictions:

\[
J=
\begin{pmatrix}
-A\cos\theta&-(H_0-As)\sin\theta\\
0&V\cos\theta
\end{pmatrix},
\quad
\det J=-AV\cos^2\theta.
\]

With H alone we have one row and two unknowns: structurally unidentifiable. The second row can restore local rank when A,V,cos(theta) are nonzero. At **apocenter**, where merger relative speed is near zero, V approaches zero, so even an accurate LOS velocity need not resolve the geometry. This matches the source authors' caveat. The Jacobian is **not** a lens-potential Hessian or a quantum operator.

## Actual deterministic audit and honest null

One Python-standard-library CPU process injected noiseless H and LOS velocity, assumed independent **illustrative** Gaussian errors sigma_H=70 kpc and sigma_V=200 km/s, and profiled a squared-residual function on 151 interaction strengths and 501 angles. No random draws or telescopes were involved. The grid is not 75,651 independent observations.

| Restriction | Result |
| --- | ---: |
| No LOS velocity, exactly matching H | s from 0 to 1.02830 |
| Joint best-fit s, inclination | 0.80, 15° |
| Joint profiled squared residual for collisionless s=0 | 2.93131 |
| Nominal delta-chi² ≤3.84 region within scanned s=[0,1.5] | **All of [0,1.5]** |
| Local linearized s uncertainty near truth | 0.41706, illustrative only |
| Checks | 15 passed + JSON readback |
| Source code SHA-256 | `74acf95719277d3066ccf2a7619b0709a0e8de5e1b21ebf3dc3fd5ec2eb84d71` |

**Result:** an extra velocity observable can remove an exact mathematical degeneracy, but under this deliberately optimistic, fixed-phase test it still fails to rule out a collisionless explanation at the nominal cutoff. **This is not a 95% observational limit**; nonlinear profiles, bounded parameters and survey selection have not been coverage-calibrated. No real likelihood or TNGC simulation was reproduced.

Run `python run.py --output output` with Python 3.11+ (standard library only). The command overwrites results.json and creates an explicitly SIMULATED profile CSV; runtime fields vary. The local companion package includes a high-resolution chart rendered from that saved CSV. No code from third-party papers was copied.

## Controls, alternative and next gate

**S-01-C1 (DERIVED):** under fixed stage/mass, inclination can exactly mimic the projected halo response. **S-01-C2 (SIMULATION_RESULT):** adding illustrative LOS errors gives collisionless squared residual 2.93131, not an exclusion. **S-01-C3 (DATA_INSUFFICIENT):** the published TNGC merger trajectories, observed halo/relic joint covariance and selection mask are not fitted.

The **strongest null** is collisionless CDM with adjusted inclination, impact parameter, merger phase or mass. Critically, the source authors show that after second pericenter and in minor mergers the sign of halo-separation differences can reverse. Resolution in the smaller cluster also substantially changes the predicted difference. These effects are not represented by our straight-line model.

**Next acceptance gate:** recover a real double-relic system or licensed paired merger track with source IDs, redshifts, weak-lensing centroid covariance, BCG velocity uncertainties and radio-relic selection. Fit a CDM nuisance baseline first, with held-out **entire clusters** rather than snapshots of one merger. Stop at UNIDENTIFIABLE if both physical explanations make the same held-out prediction.

Other prior art: [Silverman et al., *Mergers Matter*, arXiv:2606.02566v1, submitted 1 Jun 2026](https://arxiv.org/html/2606.02566v1) studies **dwarfs** at ~30–60 km/s using sigma/m=70 cm²/g. Those effective cross sections cannot be averaged with ~1000–3000 km/s cluster benchmarks without a consistent velocity-dependent interaction model. [SIDM Concerto Zenodo v1, 26 Feb 2025](https://zenodo.org/records/14933624) omits large Consistent-Trees tree*.dat files; it is not an automatically complete merger-history dataset.

**Research continuity:** main b6b85682f0843ae0d097b5f192d90b51b130788d inspected; prior open N-04/N-05/L-03/C-02/C-03 branches respected. C-03's globally unscreened gravity model remains FAILED by local tests. The 29 Sep Atlas was recovered through Files for historical context, not as current proof. **Learning checkpoint:** introduced the Jacobian as observable sensitivities and the rank loss at apocenter; learner understanding **NOT_ASSESSED**. Targeted primary coverage through 17 October 2026, not a comprehensive literature review.

No dark-matter detection, originality theorem, observer affiliation, manuscript submission, data contact or automation modification is claimed.
