# C-07 | Projection-corrected merger-clock identifiability

**27 October 2026 · v1.1 · DERIVED / SIMULATION_RESULT / UNIDENTIFIABLE / DATA_INSUFFICIENT**

## Scientific correction to C-06

The existing [C-06 result](METHODS_RESULTS_v1.0.md) uses an explicitly **SIMULATED** toy in which radio-relic shock separation is fully angle independent, \(R=st\), while halo separation \(H=[H_0(t)-bk]\cos\alpha\) is projected. It obtains an exact Jacobian rank loss at orbital apocenter. This is mathematically correct **for eta=0**, but is not a general result for radio-relic observations.

[Jee, Park and Lee, arXiv:2605.00093v1 (30 April 2026), Section II.3](https://arxiv.org/html/2605.00093v1) fit a weak *nonzero* shock projection, \(R=st\cos^\eta\alpha\) with \(\eta\approx0.223\), in an example cluster simulation. Their halos project as \(\cos\alpha\). This exponent is **case-dependent**, not a universal measured constant.

## Public derivation: what changes?

Parameters \(q=(k,t,\alpha)\) are a toy dark-drag coefficient in cm²/g, time in Gyr and viewing angle in radians. Observables \(y=(R,H,U)\) are two separations in kpc and a brightest-cluster-galaxy line-of-sight speed in km/s. Retain C-06's other artificial dynamics:

\[
R=st\cos^\eta\alpha,\quad H=[H_0(t)-bk]\cos\alpha,\quad U=v(t)\sin\alpha,
\]
\[
H_0(t)=H_*-\frac A2(t-t_*)^2,\quad v(t)=-A(t-t_*)/c_v.
\]

The Jacobian \(J_{ij}=\partial y_i/\partial q_j\) gives the sensitivity of output \(i\) to parameter \(j\). Differentiating and expanding its determinant gives

\[
\boxed{\det J=sb\cos^\eta\alpha\,[v(t)\cos^2\alpha+\eta t\,v'(t)\sin^2\alpha]}.
\]

**C07-C1 DERIVED:** eta=0 reduces to the recorded C-06 formula \(sbv\cos^2\alpha\). For nonzero eta and inclined mergers, the determinant can remain nonzero at apocenter \(v=0\), so the former unconditional-turnaround intuition must be restricted to C-06's assumption.

**C07-C2 DERIVED / SIMULATION_RESULT / UNIDENTIFIABLE:** A *new local rank-null surface* arises when the two bracketed terms cancel. For the stated linear orbital speed,

\[
\boxed{t_{\rm blind}= \frac{t_*\cos^2\alpha}{\cos^2\alpha+\eta\sin^2\alpha}}.
\]

At \(t_*=0.8\) Gyr, inclination \(30^\circ\) and eta=0.223, the **SIMULATED** null is \(0.744647843624\) Gyr, **before** apocenter. At exactly zero inclination, the old apocenter rank null still holds. A singular local Jacobian is not a global non-identifiability proof.

## Verified local CPU calculation (SIMULATED throughout)

One ChatGPT Linux standard-library Python 3.13.5 process with a 20-second timeout finished in 1.10 s, exit 0, deterministic, no random seed. Thirteen scripted assertions passed, some definitional rather than independent. Max finite-difference versus analytic Jacobian discrepancy: 1.215e-7 in mixed derivative units.

For inherited **SIMULATED** \(s=3600\) km/s converted to kpc/Gyr, \(H_*=1200\) kpc, \(A=1400\) kpc/Gyr², \(b=150\) kpc/(cm²/g), the previous exact C-06 mimic (\(k=1\), \(\alpha=30^\circ\) versus \(k=0.5\), \(\alpha=36.07077^\circ\)) produces radio-shock distances that now differ by **43.55 kpc** at eta=0.223. With an **invented 100-kpc shock standard deviation**, that is only 0.4355 of one sigma when other parameters are fixed. It is **not a measured significance**. At 0.8 Gyr the corrected toy has nonzero local determinant and a formal nuisance-profiled \(1\sigma\) width near **3.13 cm²/g**, which must not be interpreted as an observational bound. The local curvature vanishes at the newly identified blind phase.

Executed source SHA-256: 13c8d0e763d4f49d2403999bada0ef45a702b8c50965e05096945675c3ca6dc6.
Raw SIMULATED JSON SHA-256: e8cc0a15276cc084cb9e009c73b5ad82a850ed32b0c89f84dabb548d621f725d.

**The executable source and raw receipt are preserved in the ChatGPT run companion, NOT included in this small repo correction. No CI, external simulation or likelihood reproduction was run.** Results cannot be inferred to constrain real dark-matter cross-sections.

## Evidence gate and next research decision

The April 2026 preprint reports a model-conditional upper limit of 0.22 cm²/g (68%) from eleven observed cluster mergers, using 576 idealized grid simulations and marginalizing nuisance parameters. Those data were not reprocessed here. [Lee et al., TNGC-SIDM I, arXiv:2610.18957v1 (13 October 2026)](https://arxiv.org/abs/2610.18957) separately analyze **two independent simulated mergers**, not eleven additional observations. Its Data Availability says SIDM products are available on request pending a future public release. The publicly released ordinary [TNG-Cluster data](https://www.tng-project.org/data/) are **not** identical to the SIDM suite.

**C07-C3 DATA_INSUFFICIENT:** No mass/phase/angle-dependent projection calibration, joint radio/lensing/kinematic covariance, completeness or independent-halo holdouts were fitted. A collisionless merger with different geometry, dynamical state or baryonic response remains a strong ordinary competitor.

**Stopping criterion:** Do not issue sensitivity forecasts or public physical cross-section conclusions until projected CDM/SIDM trajectories and real selection/likelihood data are calibrated and tested on independent mergers. The first useful follow-up is a matched-tracks data request and a held-out angle/phase recovery check.

**AHA (explanatory, not a discovery):** an almost angle-independent measurement can still break a perfect mathematical degeneracy, yet be too weak to distinguish physical models in practice. The null can also migrate to a different orbital phase instead of vanishing.

**Learning checkpoint:** weak vs zero angular response, Jacobian rank and nuisance profiling were introduced; Arnav's demonstrated understanding remains **NOT_ASSESSED**. C-06's exact eta=0 construction is preserved in history. C-05's merger-history degeneracy and C-03's globally unscreened gravity **FAILED** case remain unchanged. No manuscript submission, outreach or new schedule is claimed for this contribution.
