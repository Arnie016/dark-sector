# N-09 | One forward potential, multiple mediator explanations

**24 October 2026 · v1.0.0 · DERIVED / SIMULATION_RESULT / UNIDENTIFIABLE / DATA_INSUFFICIENT**

**Physical question.** If the flavor of a cosmic neutrino were affected by a dark-matter forward-scattering potential, would that establish which heavy mediator caused the interaction? **No.** Zero-momentum-transfer propagation measures an effective coefficient, whereas hard scattering can sample the momentum dependence of the mediator. This is established scattering mathematics, not a new discovery.

## Continuity and external evidence

The earlier branch studies remain distinct: N-06 supplied a hypothetical AGN potential-area ceiling and corrected its dark-charge sign; N-07 added a conditional curved-path factor; N-08 checked electroweak operator consistency and obtained a more restrictive neutrino-selective dimensional coefficient. The N-08 code and saved receipt were inspected at branch head 7265ba5 (24 October). C-03's unscreened long-range gravity candidate remains **FAILED** under its Solar System assumption.

Read these primary sources through 24 October:

- P. S. Bhupal Dev et al., [arXiv:2609.26773v1](https://arxiv.org/abs/2609.26773), submitted **22 September 2026**. Section II explicitly defines a Dirac-DM vector-current potential proportional to the *net* particle-antiparticle number density. Section IV models an AGN spike. Their analysis explicitly sets aside hard-scattering attenuation and regeneration.
- K. S. Babu, P. S. Bhupal Dev and A. Thapa, [JHEP 09 (2026) 046](https://doi.org/10.1007/JHEP09(2026)046), published **3 September 2026**, [arXiv:2512.25035](https://arxiv.org/abs/2512.25035). Sections 2–4 explain how one low-energy operator admits different ultraviolet completions and why charged-lepton limits matter.
- S. Abbaslu, Y. Farzan and A. Maleki, [arXiv:2607.08833](https://arxiv.org/abs/2607.08833), submitted **9 July 2026**, also study AGN neutrinos with an explicit inelastic-scattering channel. Their model is not equivalent to our illustrative elastic vector exchange.

No joint source-flavor data, calibrated attenuation likelihood, covariance or source-specific dark-number density was obtained. These papers are **prior art**, not independent evidence of our toy's physical viability.

## AHA: the sum and the difference are different measurements

Let a nonrelativistic Dirac dark population contain particle and antiparticle number densities n_chi and n_antichi. Define total n = n_chi + n_antichi and asymmetry f = (n_chi - n_antichi)/n, with |f| <= 1. For a schematic single t-channel vector mediator of mass M [GeV] and dimensionless coupling product g, factor out common spin/current kinematics:

\[
K(Q)=\frac{g}{M^2+Q^2}\quad [\mathrm{GeV}^{-2}],\qquad Q^2=-t\ge 0.
\]

The coherent **forward** vector potential has V0 proportional to (g/M^2) f n. Under a clearly simplified equal-spin-kernel model, the **hard** differential scattering rate is proportional to n times |K(Q)|^2 because both particles and antiparticles can scatter. The hard rate is not generically proportional to the net dark charge. Spin-dependent differences and interference require a real UV calculation. With f=0, the vector forward potential is exactly zero, while hard scattering need not vanish.

A leading Standard Model lepton-doublet dimension-six interaction also contains a charged-lepton current. This illustrative mediator is **not** an electroweak/anomaly-complete UV realization of N-08's neutrino-selective dimension-eight interaction. Its mediator mass M must not be silently identified with N-08's EFT scale Lambda.

## A matched forward null, then a discriminating finite-Q prediction

All values below are **SIMULATED MODEL** parameters, not measured events. Compare A: M=1000 GeV, g=1 with B: M=100 GeV, g=0.01. Both give K(0)=1e-6 GeV^-2 and, at the same net density, exactly equal forward potentials. But at Q=100 GeV:

- A has K(Q)=9.9009901e-7 GeV^-2.
- B has K(Q)=5.0e-7 GeV^-2.
- B/A reduced amplitude ratio = **0.505**. Squared-kernel ratio = **0.255025**.

These are not cross sections or rates until target abundance, scattering phase space, transport, detector efficiency and other amplitudes are included. A stationary 1-GeV dark target and a hypothetical local 100-TeV neutrino give s=m_chi^2+2m_chi E_nu and Q_max=(s-m_chi^2)/sqrt(s)=**447.21248 GeV**; thus Q=100 GeV is kinematically possible, not observationally accessible by assertion. The beam energy alone does not specify momentum transfer.

## Worked mathematical tool: a sensitivity Jacobian

For positive g, nonzero |f| and independently known n, use three idealized log-observation types y=(log|V0|, log R(0), log R(Q)), where R(0) denotes the limiting *differential rate density*, not a count at a zero-width Q bin. Their sensitivity to theta=(log g, log M, log|f|) is

\[
J=\begin{pmatrix}
1 & -2 & 1\\
2 & -4 & 0\\
2 & -4M^2/(M^2+Q^2) & 0
\end{pmatrix},\quad
\det J=\frac{8Q^2}{M^2+Q^2}.
\]

At Q=0 the determinant vanishes: perfect forward information does not recover M. For the stated Q=100 GeV, it is **0.07920792** with M=1000 GeV and **4.0** with M=100 GeV. These dimensionless determinants only diagnose algebraic rank; they are **not significances or Fisher-information bounds**. When Q is much smaller than M, the distinction remains poorly conditioned.

Now admit an *unknown* total dark number density n. The Jacobian has four parameter columns but only three observation rows, and has an exact null direction (delta log g, delta log M, delta log|f|, delta log n)=(1,0,1,-2). Even finite-Q information cannot separate coupling from target density and asymmetry without external information. The asymmetry fraction must lie strictly between zero and one for this logarithmic local argument. At f=0 the forward observable vanishes and the logarithm is undefined.

## Claim ledger, actual validation and limitations

**N09-C1 | DERIVED, KNOWN:** g/M^2 fixed produces identical forward kernels despite different mediator masses. Falsifier: the declared single-mediator kernel algebra fails, or the actual UV model does not realize the declared current.

**N09-C2 | SIMULATION_RESULT:** the specified numerical hypotheses have ratio 0.505 in reduced amplitude and 0.255025 in squared kernel at Q=100 GeV. These values follow from illustrative inputs.

**N09-C3 | UNIDENTIFIABLE:** a free total dark-number density leaves the explicit exact null direction even when two hard-scattering Q bins and a forward potential are added. Independent target-number calibration or a different coupling observable would change the conclusion.

**N09-C4 | DATA_INSUFFICIENT:** no real source/detector likelihood, actual cross section, charged-lepton bound, propagation flux loss or statistical claim was evaluated. Conventional source-flavor uncertainty and ordinary-matter interactions remain competing explanations.

A deterministic standard-library Python implementation was actually executed in a **Linux ChatGPT container**, one worker, no RNG, under a 25-second hard timeout. Final run **exit 0, 18/18 checks passed**. Executed source SHA-256: **d77c77e3c337d8ced9702e7d9ef890ae407ddcd83796e816a4ff92ccc074642e**. Saved results JSON SHA-256: **217a2ef218efaf06ab0d2720f93592d4f6b1e6be9b9ca08675fbde4d110499a8**. A discarded preflight had incorrectly treated hard scattering as a net-current rate; the released model corrects this to a total-target rate under the specified spin assumption. No prior N-06/07/08 code was rerun. The **full executed source plus raw JSON receipt are supplied as a separate downloadable ChatGPT companion**, not included as source files in this GitHub-only methods note. Therefore this note is not by itself a complete executable repository release.

**Research checkpoint.** Keep the N-06 sign correction, N-07 fixed-model path result, N-08 operator gate and failed C-03 gravity candidate unchanged. N-09 adds a falsifiable mediator-identifiability gate, not evidence for a particle.

**Learning checkpoint.** Introduced invariant momentum transfer versus lab beam energy, sum versus net number density, sensitivity matrices and null directions. **Reader understanding: NOT_ASSESSED**, not silently marked as mastered.

**Recommended next bounded step.** Select **one gauge-consistent mediator model from primary literature**, derive its actual hard-scattering response and charged-lepton companion, and test whether a measured, source-resolved spectrum could distinguish it from production-flavor uncertainty. Stop at **DATA_INSUFFICIENT** until calibrated event/selection/covariance inputs are available.