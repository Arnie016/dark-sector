# N-06 Methods and results, version 1.0

## Smallest claim
A constant-density two-flavor neutrino oscillation channel that receives two potential contributions with the same flavor projector cannot identify their sources from oscillation probabilities at one independently fixed density when their amplitudes are both free.

## One model, two causal explanations
The flavor-basis Hamiltonian, after removing a scalar identity component, is the sum of the standard vacuum mixing Hamiltonian and the diagonal matter matrix diag(V,0). The ordinary electron potential is Ve = sqrt(2)*GF*ne. A hypothetical asymmetric fermionic dark medium with a flavor-aligned vector contact interaction can contribute Vx proportional to n_chi minus n_antichi. Symmetric dark fermions yield zero net current for this example. This is an illustrative low-energy interaction, not a tested ultraviolet-complete dark-matter theory.

Parameterize total V = Vref*(a*r+b), where r is independently fixed relative electron density, a is an ordinary-density normalization nuisance, b is an unknown hypothetical dark potential. For fixed vacuum mixing angle theta, mass-squared splitting dm2, energy E and path length L, define hx = dm2*sin(2*theta)/(4E), hz = -dm2*cos(2*theta)/(4E)+V/2 and h=sqrt(hx^2+hz^2). Constant-density appearance probability is P = hx^2/h^2 * sin(h*L/(hbar*c))^2.

The chain rule gives dP/da = (dP/dV)*Vref*r and dP/db = (dP/dV)*Vref. All rows of the sensitivity matrix are therefore collinear within one density, even if E and L vary. This is **structural non-identifiability**, not a weak-statistics issue. Two known distinct r values can break the degeneracy if derivatives are nonzero. Free, unmeasured densities can restore it.

## Executed numerical scope
One CPU process, standard-library Python, timeout 20 seconds, exit zero. 10 limiting and algebraic checks passed, including one nonindependent bookkeeping identity. No random draws or generated event counts. SIMULATED input truth: dm2=7.5e-5 eV^2; theta=33.4 degrees; a=1; b=.15; densities 3 and 5 g/cm^3; electron fraction=.50; E in {0.12,0.16,0.20,0.28,0.36} GeV; L in {800,1400,2200} km. Vref=1.1445e-13 eV. There are 30 evaluated expected probabilities, NOT measured observations. A null with a=1.15,b=0 matches the first density grid to machine precision. Keeping that null fixed at second density produces maximum absolute expected probability difference 0.024289958524238098. These are not significance estimates. Fictional independent-binomial trial weights were used only to illustrate information rank.

Local executed script SHA-256: ff138802be6ed99c67b326f8cfc2f7c7c42a67b8db4ac845ac1a608c604e3002. Raw execution code and output are downloadable from the companion ChatGPT artifact and are not committed here, so no remote reproduction is claimed.

## Strongest competing explanation and next gate
Ordinary density calibration, path-dependent flux/response and realistic matter radiative corrections can absorb or mimic the dark contribution. Stop any new-physics inference if those nuisances erase the held-out effect. First recover a realistic published 3-flavor oscillation likelihood with its response matrices and covariance.

Primary references: PDG 2025 Neutrino Masses, Mixing and Oscillations section 14.5 (https://pdg.lbl.gov/2025/reviews/rpp2025-rev-neutrino-mixing.pdf); Li et al. PRD 114 012009 (8 July 2026, https://doi.org/10.1103/twkz-l635); Huang et al. PRD 112 116014 (17 December 2025, https://doi.org/10.1103/3r2b-1hcc). Inspected prior art, not reproduced experiments.

User mastery: NOT_ASSESSED. N-04's arbitrary gate is not silently retroactively converted into this Hamiltonian. The previous C-03 unscreened failure remains unchanged.