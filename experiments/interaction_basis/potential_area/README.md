# N-06 | The potential-area gate for neutrino–dark-matter propagation

**21 October 2026 | DERIVED + SIMULATION_RESULT + DATA_INSUFFICIENT.** This experiment extends N-04's ideal two-mass-state mixing demonstration into a physical scale test. It is a **model calculation, not a detector fit or a new particle result.**

## Physical question
Can the accumulated dark matter along a path change neutrino flavor appreciably? Is the maximum density or the integrated density more important? For a specified vector-current contact interaction, the latter controls a rigorous **worst-case bound**. Lensing determines total mass, not net dark particle-antiparticle current.

## Derive the ceiling without choosing mixing angles
Let H_1(r)=H_0(r)+V(r) be the Hermitian propagation Hamiltonian, with arbitrary conventional H_0 and additional dark V. Their propagators U_0 and U_1 obey Duhamel's identity (natural units):
$$U_1(L)-U_0(L)=-i\int_0^L U_1(L,r)V(r)U_0(r,0)\,dr.$$
Since unitary norms are one,
$$\|U_1-U_0\|\le I_V=\int_0^L\|V(r)\|\,dr.$$
For the same initial density state and same effect operator 0<=E<=I, a conservative difference in any measured probability obeys
$$\boxed{|\Delta P|\le \min(1,2 I_V).}$$
This is a **ceiling**, not a predicted probability. A common identity potential produces no observable effect and can be removed to strengthen the bound. For an assumed Hermitian e–mu off-diagonal sigma_x interaction or one-flavor diagonal vector potential, \|V\|=|V_chi|. The microscopic theories and flavor phenomenologies still differ.

The illustrative EFT potential is
$$V_\chi=C\Delta n_\chi/\Lambda^2,\quad\Delta n_\chi=f_A\rho_\chi/m_\chi,\quad |f_A|\le1.$$
The density from gravity determines rho_chi but cannot determine f_A. At f_A=0 the vector effect vanishes **exactly**, even with arbitrarily massive dark halos. The source's spin/current structure and EFT/charged-lepton viability are not established by this parametrization.

## One bounded calculation: assumed profiles, not observations
The code uses the **2026 preprint's proposed** NGC 1068-like density spike, including the Schwarzschild factor, with its stated 10^7-solar-mass black hole, NFW scale 13 kpc, spike radius 0.7 kpc and neutrino-production start radius 1e-5 pc. It contrasts an expressly **SIMULATED** smooth 10-kpc halo of density 0.4 GeV cm^-3. Both use *illustrative* C=1, Lambda=1 TeV, m_chi=1 GeV, maximal asymmetry f_A=1. Nothing is fitted.

| Assumed path | Density column (GeV cm^-3 pc) | Norm integral (dimensionless) | Maximum absolute probability change |
|---|---:|---:|---:|
| Smooth 10-kpc halo | 4.0e3 | 4.8059968e-12 | **<= 9.6120e-12** |
| NGC 1068-like spike | 4.4526996e13 | 0.05349915 | **<= 0.1069983** |
| Identical mass, symmetric chi-antichi bath | any | 0 | **0**, for this vector-current potential |

The spike's **upper bound 0.107 is not a 10.7% signal prediction**. Its density profile, emission radius and maximally asymmetric charge are assumed rather than established by imaging. The line-of-sight calculation uses flat radial dr and omits near-horizon curved propagation, redshift, realistic flavor initial conditions and detector effects. For 100-TeV neutrinos and a chosen Delta m²=0.0025 eV², the local potential at the source is 2.13e-20 eV, compared with illustrative vacuum splitting scale 6.25e-18 eV. A **local energy comparison and path-integral ceiling are different checks**.

## Reproduction
Run **python run.py --output results.json** (Python standard library). The actual bounded 25-second CPU process, one worker, seed=null, passed 12 implementation/limiting tests with log-Simpson integration at 2048/4096/8192 steps and strict JSON readback. SHA-256 of executed Python source: **e7773794bddf7d039d33bc50b65fe31775d9e9597233012fa39f2d380929673d**. Re-running overwrites environment-dependent fields. The saved [result receipt](results.json) is **SIMULATED**; this is not an observed IceCube likelihood or reproduction of the source authors' flavor curves.

## Nulls, falsification and limitations
**N-06-C1 DERIVED:** with a fixed contact coefficient and net current, the upper bound is set by potential norm area, and a symmetric bath is blind. **N-06-C2 SIMULATION_RESULT:** the assumed smooth halo's maximum difference is below 1e-11 while the modeled spike's ceiling is larger. **N-06-C3 DATA_INSUFFICIENT:** no calibrated source asymmetry, physical coupling bounds, cosmological mass profile or measured detector probabilities were fitted.

Strongest conventional competitor: an unknown source flavor mixture, ordinary-electron NSI and detector calibration can produce the same measured flavor mixture. The previous Particle Physics Bridge also proves an exact degeneracy if ordinary-electron and dark-current profiles are proportional. The N-04 e–mu gauge-doublet operator necessarily includes charged-lepton partners: it is **not** a verified viable dark interaction. A large claimed smooth-halo flavor change inconsistent with the bound falsifies *these chosen EFT and halo assumptions*, not every dark model. If source asymmetry cannot be independently constrained, the vector interpretation is **UNIDENTIFIABLE**.

**Recommended next gate:** test charged-lepton bounds and a specific gauge-consistent operator before expensive three-flavor propagation. Only then build matched source-production and detector likelihoods with a held-out standard/ordinary-NSI competitor. Keep C-03's separately FAILED unscreened-gravity result intact.

## Sources and continuity
- **Primary paper:** Dev et al., *Resonant neutrino flavor conversion within dark matter spikes*, [arXiv:2609.26773v1](https://arxiv.org/html/2609.26773v1), submitted **22 September 2026**, preprint. Sections II–IV were inspected. It models a dense spike and explicitly distinguishes net current from gravitating density; its own three-flavor predictions are **not reproduced here**.
- **Ordinary NSI:** Krishnamoorthi et al., [arXiv:2512.22632v2](https://arxiv.org/html/2512.22632v2), revised **9 October 2026**, reanalyzes 7.5 years of older IceCube DeepCore exposure. Its mu–tau constraints cannot be directly applied to our off-diagonal e–mu coefficient.
- **Repo continuity:** main b6b85682f0843ae0d097b5f192d90b51b130788d and five open PRs #4–#8 read on this date. Previous N-04 PR #4 contains the ideal gate result; an independent **19 October lecture-bridge handoff** supplies the microscopic candidate and an electron-NSI identifiability calculation, but that code was not rerun. C-03's rejected gravity candidate remains rejected.
- **Learning checkpoint:** potential area, asymmetry versus total mass, unitary-norm bound, difference between maximum allowed change and actual transition fraction were introduced; reader understanding is **NOT_ASSESSED**. No new release, schedule, outreach or manuscript submission.
