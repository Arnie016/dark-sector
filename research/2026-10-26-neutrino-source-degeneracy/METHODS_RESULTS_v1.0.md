# N-10 | Distinguishing dark and ordinary neutrino potentials

**26 October 2026 | v1.0 | DERIVED / SIMULATION_RESULT / UNIDENTIFIABLE / DATA_INSUFFICIENT**

**Physical question.** Can multiple neutrino paths distinguish a dark-matter forward potential from an ordinary-matter nonstandard interaction (NSI)? A forward potential is an energy correction from coherent scattering without a resolved collision. Here both mechanisms are *hypothetical* competing model terms.

**AHA (explanatory, not discovery).** If two explanations produce precisely the same Hamiltonian at every point, arbitrarily precise detectors cannot distinguish them. Better AI theory searching alone cannot fix a mathematically unidentifiable inverse problem.

## Primary sources and continuity

- Dev, Gaido, Ibarra & Porto, [arXiv:2609.26773v1](https://arxiv.org/abs/2609.26773), submitted 22 September 2026, preprint. Sections II–IV use a flavor-diagonal Dirac dark-vector current potential proportional to **net** particle minus antiparticle density and an **assumed** AGN spike; V–VI include source production choices and an AGN population assumption. Their spatially varying three-flavor calculation is not reproduced here.
- IceCube Collaboration, [Phys. Rev. D 104, 072006 (2021)](https://doi.org/10.1103/PhysRevD.104.072006), published 15 October 2021. Ordinary forward NSI constrained from three years of older DeepCore atmospheric exposure at 5.6–100 GeV. Neither these data nor a new AGN likelihood was fitted here.

Checked primary methods through 26 October 2026; no new observations. Earlier N-06 sign correction, N-07 curved-path scope, N-08 gauge-operator consistency and N-09 mediator-mass degeneracy are different retained studies. C-03's globally unscreened gravity model stays FAILED under its Solar System gate. Old named September ZIP archives not recovered. This is an additive study for existing open PR #4, not a merge.

## N10-C1: exact no-go theorem within a restricted model

Let the effective two-flavor propagation Hamiltonian on path j be

$$H_j(s)=H_{0,j}(s)+[\theta_\chi x_j(s)+\theta_e y_j(s)]T_j(s).$$

The flavor-state axes are electron and muon. Theta_chi and theta_e are effective interaction coefficients; x(s) is normalized **net** dark-current density, y(s) normalized ordinary current density. They have explicitly chosen *dimensionless* conventions here, not observed cm^-3. T is a Hermitian flavor-response matrix. Critically, this model assumes *both* mechanisms multiply the **same T**. Neither the Standard Model generally nor all gauge-complete UV theories must obey that assumption.

If x_j(s)=c y_j(s) **pointwise on every measured path**, the full Hamiltonian depends only on c theta_chi+theta_e. Therefore changing (theta_chi,theta_e) to (theta_chi+delta,theta_e-c delta) leaves the Hamiltonian everywhere identical. Even when H0 and T do **not commute**, the exact time-ordered quantum evolution and any fixed detector prediction agree. N10-C1 is **DERIVED / UNIDENTIFIABLE** under the stated condition. Equality of only the *integrated* columns would not suffice if spatial ordering affected the evolution.

Different ratios across sources remove this exact degeneracy, but may still fail because the detector has zero response or production conditions are unknown.

## Worked mathematical tool: a sensitivity Jacobian

For a transparent exact **SIMULATED** constant-density two-state example, take

$$H=\frac12\begin{pmatrix}v&\Delta\\\Delta&-v\end{pmatrix},
\quad v=\theta_\chi x+\theta_e y,\quad\Delta=1,\quad L=3.$$

The off-diagonal Delta creates flavor transitions. The diagonal ±v/2 shifts their relative energies. The lengths and energies are **dimensionless normalized products**, not real neutrino eV or astronomical distances. For initially pure electron flavor,

$$p(v)=P(e\to\mu)=\frac{\Delta^2}{\Delta^2+v^2}
\sin^2\left(\frac{L}{2}\sqrt{\Delta^2+v^2}\right).$$

A Jacobian matrix records each measured quantity's local sensitivity to each parameter. Its two rows represent paths, its two columns dark and electron matter couplings:

$$J_{j,\chi}=p'(v_j)x_j,\quad J_{j,e}=p'(v_j)y_j,$$
$$\det J=p'(v_1)p'(v_2)(x_1y_2-x_2y_1).$$

One zero determinant indicates a locally invisible parameter direction. Even with nonproportional profiles, p'(0)=0 because p is even in v, so geometry alone cannot guarantee measurable sensitivity. A **SIMULATED** Gaussian proxy with independent probability errors sigma=0.05 gives likelihood information F=J^T J/sigma². This is not a potential-energy Hessian, detector sensitivity or observational significance.

## One actual bounded CPU study

**Execution:** ChatGPT Linux container, one standard-library Python process under a hard 20 s timeout, exit 0; seed null. Reproduce with: python3 run.py results.json. Executed source SHA-256 **14eaab95fd8b02c3c83541be9ad6f16628eacaa1ccb02d25981165705457080e**; deterministic SIMULATED receipt SHA-256 **328a6746cb867b825e620401fa402fbdd58cdb9024b2fa5faff4db187a65fbbd**.

16 recorded assertions passed, but **one assertion is vacuous** (0==0, misleadingly named a zero-mixing check). Thus **15 nonvacuous implementation/limiting checks at most**, not 16 independent scientific tests. Keep this limitation visible. Finite-difference derivative and exact reweighted source mixture were executed. No physical baseline was reproduced.

Generating truth (theta_chi,theta_e)=(0.4,0.2); alternative (0.2,0.4). With source electron fractions fixed at w=0.7:

| SIMULATED path (x,y) | Truth P(e→mu) | Alternative P(e→mu) |
|---|---:|---:|
| Path 1: (1,1) | 0.7121165 | 0.7121165 |
| Path 2A: (2,2) | 0.2102943 | 0.2102943 |
| Path 2B: (2,0.5) | 0.4491473 | 0.7121165 |

**N10-C2 SIMULATION_RESULT:** the proportional pair has exactly the same Hamiltonian and outputs. The nonproportional pair separates at fixed production fractions and has conditional Fisher determinant 190080.262 in arbitrary proxy units. That number is not a significance, a forecast or an astrophysical measurement.

**The stronger null:** the source may produce a mixture. With source electron fraction w and muon fraction 1-w, the measured muon fraction is

$$z=(1-w)+(2w-1)p.$$

For SIMULATED path 2B, the true model produces z=0.4796589044 with w=0.7. The alternative interaction yields **exactly the same z** by setting w=0.4520520727, which is also physical. On path 1 both models use w=0.7. **N10-C3 UNIDENTIFIABLE**: independently free source mixtures erase the two-path coupling identification in this example. Generically the free w_j enters each independent observation when p_j differs from 1/2.

## Falsifier, constraints and next gate

**N10-C4 DATA_INSUFFICIENT:** No measured AGN source-resolved likelihoods, physical net dark-current columns, source mixture constraints, energy-dependent detector response, common selection or covariance, or physical electroweak-complete mediator constraints. Real three-flavor neutrinos travel through varying density and then often decohere. The two operators may be distinct; even the toy phase-sensitive probability is not automatically an astrophysical observable.

**Smallest falsifiable follow-up:** build the physically motivated three-flavor, phase-averaged *source-to-detector* Jacobian for at least two independently characterized AGN sources, allowing a matching ordinary NSI competitor and source nuisance profiling. Require the independent column profiles, measured likelihood and holdout. Stop as **UNIDENTIFIABLE** if the profiled Jacobian loses rank or as **DATA_INSUFFICIENT** if calibrated likelihood and response inputs are absent. A theory-proposing AI needs this fixed evaluator before optimization, otherwise it might reward an unknowable answer.

**Research checkpoint:** conditional structural null and a concrete source-mixture counterexample, not a dark matter discovery. **Learning checkpoint:** common Hamiltonian, matrix rank and nuisance profiling introduced; reader understanding **NOT_ASSESSED**. No outreach, submission, user-device execution, paid compute or schedule change.
