# N-06 | Multimessenger dark-asymmetry identifiability

**19 October 2026 | DERIVED + SIMULATION_RESULT + UNIDENTIFIABLE | Observational DATA_INSUFFICIENT.** Every numerical result is SIMULATED. No IceCube event fit, gamma-ray measurement, or novel particle claim is made.

## Question and explanatory AHA

If neutrino oscillations and gamma-ray annihilation both probe one dark-matter spike, do we know the dark-matter particle–antiparticle asymmetry? **Not without additional input.** A vector-current neutrino potential responds to the **difference** of particle and antiparticle number densities. A hypothetical pair-annihilation photon rate responds to their **product**. Two complementary measurements need not identify three unknown microscopic parameters.

Our primary physical starting point is Dev, Gaido, Ibarra & Porto, [arXiv:2609.26773v1](https://arxiv.org/html/2609.26773), submitted **22 September 2026**, a preprint. Sections II–IV assume a Dirac dark-matter fermion with a flavor-dependent effective vector coupling, derive Vα=2√2 G_F εα(nχ−nχbar) and numerically propagate three neutrino flavors through an assumed AGN dark-matter spike. The assumed dense spike and maximally asymmetric background are inputs, not established measurements.

Define total mass density ρ=mχ(nχ+nχbar) and net asymmetry f=(nχ−nχbar)/(nχ+nχbar), constrained to −1≤f≤1. Hence nχ=(ρ/mχ)(1+f)/2 and nχbar=(ρ/mχ)(1−f)/2. At fixed mass density, neutrino vector potential is proportional to ε f. A separately *hypothesized* χχbar annihilation channel with fixed photon yield gives emissivity proportional to s(1−f²)ρ²/mχ². The coefficient s includes unknown annihilation rate and photon yield. Its existence does not follow from the neutrino operator.

Normalize away **assumed known** spatial density and detector geometry to define two *theoretical amplitudes*, not measured rates: 
Aν=ε f and Aγ=s(1−f²).

## Mathematical tool: the observation Jacobian

The Jacobian is a 2×3 sensitivity matrix. Rows represent the predicted neutrino and gamma amplitudes. Columns represent (ε,f,s). An entry quantifies how an observable changes when a parameter changes:

J = [[f, ε, 0], [0, −2sf, 1−f²]].

For ε=0.8, f=0.75, s=0.8 it is [[0.75,0.8,0],[0,−1.2,0.4375]], with **rank 2** and one invisible parameter direction. Specifically (δε,δf,δs)=t(−ε/f,1,2sf/(1−f²)) has J·δ=0. The exact nonlinear family is ε(f)=Aν/f, s(f)=Aγ/(1−f²) on the allowed interior domain.

**Smallest claim N-06-C1 (DERIVED; UNIDENTIFIABLE):** two idealized amplitudes cannot recover the three unknown parameters. This is an algebraic property even if these two amplitudes were noiseless; the numerical audit is not a discovery.

## Actual SIMULATED result

| Quantity | Model A | Model B |
| --- | ---: | ---: |
| ε | 0.80 | 1.20 |
| f | 0.75 | 0.50 |
| s | 0.8000 | 0.4667 |
| Aν | 0.6000 | 0.6000 |
| Aγ | 0.3500 | 0.3500 |

At the original paper's illustrative production-radius density 3×10¹⁸ GeV/cm³, and assumed mχ=1 GeV, both give V≈4.5×10⁻¹⁹ eV. For a separate **SIMULATED** constant-density two-flavor toy with mixing θ=33°, Δm²=7.5×10⁻⁵ eV², path length 10⁻⁴ pc, the flavor-conversion probabilities at E=50,100,200 TeV were approximately 0.499799, 0.088849, 0.000919 for **both** models. This does **not** reproduce the paper's radially varying three-flavor calculation. Identical net potentials along any common path analytically imply identical neutrino evolution for fixed source and detector inputs, including antineutrino sign changes.

**N-06-C2 (SIMULATION_RESULT):** one deterministic standard-library Python CPU run passed 17 algebraic, numerical and limiting-case checks plus JSON readback. No random draws, paid compute, user-device installation or observed events. Executed run.py SHA256: 6a647039e5622e924f77d3ba4b1c905e7cd2316f89f3d0749aa7da39c852e1ed. Full original result SHA256: 210544e1f71b0cdd65659e804db145ed3dcea66b5b41114c0f60d58a41ce2d9b. Companion archive contains exact generated JSON; the repository code regenerates it.

## Physics boundaries and competing model

The [2025 PDG dark-matter review](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-dark-matter.pdf), Sec. 27.7, gives the standard annihilation density-squared production and photon line-of-sight integrals. The **added** gamma channel is conditional. The spike paper itself considers nonannihilating DM for its density benchmark: large annihilation could alter that spike. For mχ=1 GeV, annihilation photon energies cannot be 100 TeV; astrophysical 100-TeV neutrinos instead come from source acceleration and pion/muon processes.

The [IceCube collaboration flavor analysis](https://arxiv.org/html/2510.24957), its manuscript dated **24 August 2026**, analyzes **11.4 years of existing exposure** across 5 TeV–10 PeV and constrains an *all-sky diffuse mixture*, not a named AGN's dark spike. The 2026 analysis is not an independent new exposure. Dev et al. assume common AGN production/spike properties to compare their prediction with diffuse flavor contours. We obtained no full calibrated source-resolved likelihood or annihilation photon measurements.

**Strongest conventional alternative:** astrophysical pion/muon production and source averaging explain neutrino flavors while gas, cosmic rays or accretion explain photons. Unknown dark density shapes, production fractions and detector calibration introduce further nuisance directions. **Failure gate:** do not infer f or ε from the two amplitudes without independent s or an alternative asymmetry-sensitive observable, and do not infer annihilation from gamma brightness alone. Exact vector-current cancellation at f=0 does not imply every other possible dark operator vanishes.

**Recommended next step:** inspect feasibility of a source-resolved AGN neutrino likelihood, with flavor confusion matrices, effective areas and source count rates, before developing full radial three-flavor fits. If those inputs remain absent, stop at DATA_INSUFFICIENT. Future independent s constraints could reduce the continuous ambiguity to at most a discrete sign, provided photon origin and model are controlled.

**Continuity:** main was inspected at b6b85682f0843ae0d097b5f192d90b51b130788d, plus existing PRs #4–#8 and unmerged C-04 and DIR-20261019 branches. Earlier N-03 origin ambiguity is preserved, C-03 constant unscreened f(R) remains FAILED. Neither experiment was rerun. **Learning:** introduced net versus total density, pair-emission rate, Jacobian null direction. Arnav's understanding remains **NOT_ASSESSED**. No publication venue submission, outreach, schedule adjustment or repository setting change.
