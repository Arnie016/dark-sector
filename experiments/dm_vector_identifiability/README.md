# N-06 | Dark density and dark number asymmetry are not the same observable

**2026-10-21 · DERIVED + SIMULATION_RESULT + UNIDENTIFIABLE**

**Question.** Can an intense gravitationally inferred dark-matter spike fail to change neutrino flavor? Yes, in a specified Dirac-dark-matter vector-current model if particle and antiparticle number densities match. This result is established within that interaction class, not a discovery or evidence of a particle. It is the physical Hamiltonian replacement N-04's abstract mixing gate was missing.

## Physical source and derivation

Dev, Gaido, Ibarra and Porto, *Resonant neutrino flavor conversion within dark matter spikes*, arXiv:2609.26773 (first posted 2026-09-22), derive an effective flavor-dependent vector contact interaction (their Eqs. 1-4). For a nonrelativistic Dirac-dark-particle medium, coherent forward scattering contributes

\[
V_\alpha=2\sqrt2 G_F \epsilon_\alpha(n_\chi-n_{\bar\chi}).
\]

Here \(\alpha\) labels a neutrino flavor, \(G_F\) is the Fermi constant, and the dimensionless \(\epsilon_\alpha\) measures a coupling relative to weak interactions. The expectation of the **vector charge current** is the difference in dark particle and antiparticle number densities. The gravitational mass density is instead their **sum** times particle mass:

\[
\rho_\chi=m_\chi(n_\chi+n_{\bar\chi}),\qquad
\eta=\frac{n_\chi-n_{\bar\chi}}{n_\chi+n_{\bar\chi}},\quad -1\leq\eta\leq1.
\]

Thus, using consistent natural units,

\[
\boxed{V_\alpha=2\sqrt2G_F\,\rho_\chi\,\frac{\epsilon_\alpha\eta}{m_\chi}.}
\]

**AHA (explanatory, not novel):** lensing responds to gravitational mass-energy, whereas this neutrino interaction responds to signed dark particle abundance. Increasing the former cannot guarantee increasing the latter. At \(\eta=0\), the potential vanishes even in a very dense spike. This is an exact null for this vector interaction; it is not a universal statement about every scalar or axial dark coupling.

## A rank-one parameter map

Hold \(\rho_\chi(r)\) fixed independently. Every outcome from this vector correction depends on the combination \(q=\epsilon_\alpha\eta/m_\chi\). For a prediction \(P(E,q)\), its sensitivity to the logarithms of the three positive parameters obeys

\[
(\partial_{\ln\epsilon}P,\partial_{\ln\eta}P,\partial_{\ln m}P)
=\frac{\partial P}{\partial\ln q}(1,1,-1).
\]

The rows from any number of energies are proportional to one direction, so the parameter sensitivity matrix has rank at most one, and the two independent orthogonal directions are **UNIDENTIFIABLE**. Constraints from a different observable or justified external particle-mass/asymmetry information are necessary. Neutrino-antineutrino asymmetry may help determine the sign of \(q\) but not independently resolve \(\epsilon,\eta,m\).

An additional exact null is \(\epsilon_e=\epsilon_\mu=\epsilon_\tau\): a flavor-universal vector potential is proportional to the identity, changing only a common phase. Ordinary electron matter induces \(V_e=\sqrt2 G_F n_e\) as reviewed by PDG §14.5. If ordinary and dark contributions yield the same total flavor Hamiltonian along observed paths, the labels cannot be identified from oscillations alone.

## SIMULATED numerical limiting example

The cited paper conditionally assumes a **nonannihilating** NGC 1068 spike density about \(3\times10^{18}\) GeV/cm³ near its production radius \(10^{-5}\) pc. This density is *model-assumed, not measured*. For \((\epsilon,\eta,m_\chi/\mathrm{GeV})=(1,0.5,1)\), the model potential is \(V=3.8022025\times10^{-19}\) eV. Units are converted using \(1\ \mathrm{cm}^{-3}=(\hbar c)^3\ \mathrm{eV}^3\) when \(\hbar c\) is supplied in eV cm.

To show an observable consequence but not misrepresent the full AGN calculation, use the **two-flavor adiabatic endpoint** with vacuum \(\theta=33^\circ\), \(\Delta m^2=7.5\times10^{-5}\) eV², production of pure electron flavor and complete later vacuum phase averaging:

\[
P_{ee}=\tfrac12[1+\cos2\theta\,\cos2\theta_m],\quad
\cos2\theta_m=\frac{\Delta\cos2\theta-V}{\sqrt{(\Delta\cos2\theta-V)^2+(\Delta\sin2\theta)^2}},\quad
\Delta=\frac{\Delta m^2}{2E}.
\]

For antineutrinos reverse the potential sign. At **40 TeV**, the SIMULATED predictions are \(P_{ee}^\nu=0.50026\), \(P_{ee}^{\bar\nu}=0.63514\); the symmetric-DM null is \(0.58272\). In this ideal model resonance occurs around **40.115 TeV**. These numbers assume adiabatic escape; no radial propagation, nonadiabatic transition, detector selection, source redshift or three-flavor physics was simulated.

Three different parameter choices, \((1,0.5,1),(2,0.5,2),(5,0.2,2)\), all yield \(q=0.5/\mathrm{GeV}\) and numerically identical energy predictions. A finite-difference log-sensitivity audit confirms \(\nabla_{\ln\eta}P=\nabla_{\ln\epsilon}P=-\nabla_{\ln m}P\), within numerical tolerances.

One bounded single-process standard-library run passed **17** deterministic implementation and limiting checks and wrote the actual SIMULATED CSV. This is not baseline reproduction of the 2026 preprint; its published calculations require three flavors and numerical propagation through a spike. Run [run.py](run.py) to regenerate [SIMULATED_energy_scan.csv](SIMULATED_energy_scan.csv) and results.json. Frozen local executable SHA-256: 32d777c8cdab8136b475935588022c443dffab184946b80b076ae49a52782076. The complete conversation companion package also preserves the chart, full receipt and a standalone plot renderer; binaries are not pushed in this compact PR.

## Evidence and decision boundaries

The [IceCube three-flavor result](https://doi.org/10.1103/vntd-m133), Phys. Rev. Lett. 137, 081002, **published 18 August 2026**, is based on **11.4 years of earlier exposure**. It reports a diffuse 5 TeV–10 PeV flavor fit near (0.30, 0.37, 0.33), not a calibrated flavor measurement for each AGN. Its summary contours are not treated here as detector event files or a likelihood. The spike preprint explicitly assumes a representative AGN population when comparing with that diffuse result. No independent new observation or significance calculation is claimed.

**Smallest falsifiable claim N-06-C1 (DERIVED):** for the specified asymmetry-sensitive vector interaction, a symmetric dark background contributes zero to the oscillation Hamiltonian, and independent observations are needed to resolve \(\epsilon,\eta,m_\chi\) individually at fixed mass-density profile.

**Strongest null:** ordinary matter, source-flavor freedom and/or \(\eta=0\) explain the flavor information without a detectable dark vector potential. **Stopping rule:** reject any claim that flavor data alone identify the separate three parameters unless an actual additional channel breaks the rank-one map. A two-flavor adiabatic curve cannot establish an IceCube sensitivity forecast.

**Research checkpoint:** N-03 phase-averaging remains in main, N-04's abstract rotation source is still unassigned, C-03's unscreened gravitational candidate remains FAILED. This chapter introduces a concrete interaction and an exact identifiability limit. PRs #4-#8 remain separate. **Learning checkpoint:** vector-current charge vs mass density, matter eigenstate mixing and log-sensitivity rank INTRODUCED; user understanding NOT_ASSESSED.

**Recommended next gate:** pin the published spike and full three-flavor Hamiltonian, independently solve radial propagation with nonadiabatic transitions, then compare its vacuum and strongly coupled limiting predictions against the authors' stated tables/figures. Only after a physics baseline matches should a real source/detector likelihood be attempted.

**Source coverage (as of 2026-10-21):** arXiv:2609.26773 Sections II–IV and Appendix A, first posted 2026-09-22, accessible preprint not independently peer reviewed here; PDG 2025 neutrino review §14.5; IceCube PRL 137 (2026) 081002 and arXiv:2510.24957, original exposure 11.4 years. No source-paper files or figures redistributed. No outreach, manuscript submission or schedule modification.
