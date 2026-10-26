# C-06 | When a merger clock stops identifying dark drag

**26 October 2026 | v1.0 | DERIVED · SIMULATION_RESULT · UNIDENTIFIABLE · DATA_INSUFFICIENT**

## Research question and source context

Would adding radio-shock separation and a galaxy line-of-sight velocity always distinguish self-interacting dark matter (SIDM) from a tilted, conventional cluster merger? **No.** A simple counterexample occurs at orbital turnaround (apocenter), where the galaxy velocity approaches zero. This is a necessary identifiability gate, not a new cluster measurement or dark-particle constraint.

**Sources checked:** Lee et al., *TNGC-SIDM I*, [arXiv:2610.18957v1](https://arxiv.org/html/2610.18957v1), submitted **13 October 2026**, preprint, sections 2.1–2.2, 4.1 and 5.2. Matched CDM/SIDM cosmological magnetohydrodynamical zoom-ins of **two independent cluster mergers** at approximately **2×10^14** and **9×10^14 solar masses** explore constant elastic cross sections **0, 0.5 and 1 cm²/g**. The authors show that double-radio-relic separation approximately tracks time after collision while halo separation changes with SIDM, but the former is not exactly interaction-invariant (early slopes can differ by about 20%). Their analysis warns that viewing-angle constraints from BCG line-of-sight velocities weaken near apocenter. Simulation data are **available on request**, not a public event-level likelihood.

**Prior art:** Jee, Park & Lee, [arXiv:2605.00093v1](https://arxiv.org/html/2605.00093v1), submitted **30 April 2026**, preprint, sections II.3, II.6, III.1–III.2 and IV.2. The authors already proposed radio-relic distances as merger clocks and analyzed **11 observed clusters**, reporting a **68% upper limit of 0.22 cm²/g** under their simulator, selections and priors. That reported observational result was **not reproduced here**. The 2026 TNGC-SIDM paper re-examines the physical tracer in more complex matched simulations; these are not eleven new observed clusters.

## AHA (explanation, not discovery)

An observable that ordinarily breaks a degeneracy can cease to help **at a special physical stage**. Shock separation may still tell us the merger epoch. But when the galaxy orbit turns around, its line-of-sight velocity is zero regardless of the inclination. A shorter *projected* dark-halo distance can then be explained by either stronger effective dark drag or a larger viewing angle. The issue is not weak AI or low numerical precision. The measured quantities do not contain the missing direction of information.

## Worked tool: Jacobian as a local response map

The following is a strictly **SIMULATED**, phenomenological toy, not the TNGC-SIDM simulator. Let parameters be q=(k,t,a), where k is an illustrative cross-section proxy [cm²/g], t is time since collision [Gyr] and a the viewing angle measured from the sky plane [radians]. Let outputs be y=(R,H,U) for projected double-relic distance [kpc], halo-to-halo distance [kpc] and relative BCG line-of-sight speed [km/s]. Define

$$
R=st,\qquad H=[H_0(t)-bk]\cos a,\qquad U=v(t)\sin a,
$$
$$
H_0(t)=H_*-\tfrac12 A(t-t_*)^2,\qquad v(t)=-A(t-t_*)/c_v.
$$

Here s=3600 km/s = 3681.76 kpc/Gyr is a **chosen constant shock-speed proxy**, H*=1200 kpc, A=1400 kpc/Gyr², t*=0.8 Gyr, b=150 kpc/(cm²/g) and c_v=1.022712165 (kpc/Gyr)/(km/s) converts speed units. **Only the rough speed scale is source-motivated; every calibration coefficient, noise assumption and generating truth is invented.** In reality shock speed, halo acceleration and gas selection depend on the merger.

The sensitivity matrix J_ij=∂y_i/∂q_j records how each output (row) changes when each unknown (column) shifts:

$$
J=\begin{pmatrix}
0&s&0\\
-b\cos a&H'_0(t)\cos a&-[H_0(t)-bk]\sin a\\
0&v'(t)\sin a&v(t)\cos a
\end{pmatrix}.
$$

Expanding along the first row,

$$
\boxed{\det J=s b\,v(t)\cos^2a}.
$$

Therefore at **apocenter**, v(t*)=0 and det J=0. This is a **local** identifiability warning, not a proof every real cluster model is globally degenerate. This identity also vanishes if b=0, s=0 or a=90°. At t=t*=0.8 Gyr, k=1 cm²/g and a=30°, the **SIMULATED** observables are (2945.411 kpc, 909.327 kpc, 0 km/s). An alternative k=0.5 cm²/g, a=36.07077° gives **exactly the same outputs**.

## What ran and how much it means

A single deterministic standard-library Python 3.13.5 process in the **ChatGPT Linux container**, 20-second hard timeout, exited 0 in 1.10 seconds externally measured. [Code](run.py) and [raw SIMULATED results](results.json) are included. RNG seed null. Executed code SHA-256: **451d50bf3fbcfb22d5ef0e9ca02a55e7a97ea00af3e7a39b91a6c0f5c106df41**; raw JSON SHA-256: **6a9f73a9f82f2b2bdbddb1b63242a2eb7a84c59816b0bf74ef1da7711acaef44**. Reruns print new receipts with the local Python version; actual observations were never processed.

For **SIMULATED independent Gaussian standard deviations** (100 kpc, 80 kpc, 50 km/s), the profile information after fitting t and a predicts a *formal local* uncertainty on k of 1.065 cm²/g at 0.60 Gyr, 18.19 cm²/g at 0.79 Gyr and undefined at 0.80 Gyr because information vanishes. These are **not detector forecasts or observed uncertainties**; an inverse-Hessian approximation is unreliable near singularities and physical boundaries.

The script reports 11 passing assertions. One, unfortunately named zero_drag_no_k_sensitivity, is tautological and merely rechecks the own derivative formula: count **at most 10 substantive implementation checks**. Other finite-difference and determinant checks passed with maximum absolute derivative discrepancy 9.18e-8. No external simulation or likelihood was reproduced.

## Claims, failure gates and continuation

**C06-C1 DERIVED:** toy response Jacobian loses rank at apocenter. **C06-C2 SIMULATION_RESULT / UNIDENTIFIABLE:** distinct k and angle reproduce all three exact SIMULATED outputs. **C06-C3 DATA_INSUFFICIENT:** no machine-readable TNGC-SIDM profiles, galaxy velocities, observational likelihood, selection, covariance, lensing-center posterior or inclination priors were fitted.

Strongest conventional competitor: **collisionless dark matter with a different viewing angle, initial geometry or baryonic response**. Needed: an independent inclination observable, a joint calibrated radio+lensing+spectroscopic likelihood and matched-halo train/test validation. Reject any constraint if nuisance-profiling remains rank deficient or actual calibration inputs cannot be obtained. Do not count multiple snapshots of one halo as independent samples.

**Recommended next bounded step:** retrieve matched CDM/SIDM trajectories and completeness/covariance metadata from the simulation release (currently stated as available on request), then test whether the phase/angle near-singularity survives. No author contacted, no manuscript submitted or schedule changed.

**Research checkpoint:** C06-C1/C2 hold only in the declared analytic and SIMULATED toy; C06-C3 remains DATA_INSUFFICIENT. Prior C-05 halo-history counterexamples and the C-03 FAILED globally unscreened model remain unchanged.

**Learning checkpoint:** apocenter, projected geometry, Jacobian rank and nuisance profiling were introduced. User demonstration **NOT_ASSESSED**.
