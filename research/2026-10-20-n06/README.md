# N-06 | Why an ordinary electron density can perfectly mimic a dark neutrino potential

**20 October 2026.** States: **DERIVED**, **SIMULATION_RESULT**, **UNIDENTIFIABLE** (under free electron-density nuisance), **DATA_INSUFFICIENT** (for detector inference). This is an additive companion to open N-04 PR #4, not its replacement.

## Physical question and model

Can a neutrino oscillation spectrum distinguish a flavor-diagonal dark-matter forward potential from uncertainty in ordinary electron density? Not when both act through the same flavor projector and share a proportional spatial profile.

For coherent two-flavor propagation, after removing an unobservable identity term,

\[
H=\frac12\begin{pmatrix}
V-\delta\cos2\theta&\delta\sin2\theta\\
\delta\sin2\theta&\delta\cos2\theta-V
\end{pmatrix},\qquad \delta=\frac{\Delta m^2}{2E},\quad V=V_e+V_\chi.
\]

All matrix entries are energies, in eV. Rows are **flavor states**. Standard coherent forward scattering gives \(V_e=\sqrt2G_Fn_e\) for neutrinos and a reversed sign for antineutrinos. A hypothetical asymmetric Dirac dark-fermion vector contact current may yield \(V_\chi\propto G_\chi(n_\chi-n_{\bar\chi})\). A **symmetric** particle/antiparticle vector current cancels. No electroweak gauge completion or allowed coupling region is established here.

In the mass basis, the flavor projector is \(U^\dagger P_eU=\begin{pmatrix}\cos^2\theta&\sin\theta\cos\theta\\\sin\theta\cos\theta&\sin^2\theta\end{pmatrix}\), making this a defined alternative to the assumed rotation gate in N-04. It is NOT a reproduction of the N-04 dephased-source model.

For a constant medium over \(\ell\), let \(h_x=\delta\sin2\theta\), \(h_z=V-\delta\cos2\theta\), \(\Omega=\sqrt{h_x^2+h_z^2}\). Then

\[
P_{e\to x}=\frac{h_x^2}{\Omega^2}\sin^2\left(\frac{\Omega\ell}{2\hbar c}\right).
\]

This is an ideal probability, **not an observed event rate**.

## AHA | The missing direction of the measurement

On one path set \(V=V_0(a+q)\), where \(a\) is uncertain ordinary electron-density normalization and \(q\) an extra dark coefficient. Then \(\partial P/\partial a=\partial P/\partial q\) for every energy. The sensitivity **Jacobian**, a matrix whose rows are observed channels and columns are parameters, has two identical columns. It constrains \(a+q\) only, no matter how many energy channels one adds.

For multiple paths \(V_j=V_0(e_ja+d_jq)\), differing known ratios \(e_j/d_j\) can restore conditional rank two. But granting each path its own free electron normalization \(a_j\) makes the dark column equal to \(\sum_j(d_j/e_j)\) times the path-specific nuisance columns. Without outside matter information, the dark parameter is again UNIDENTIFIABLE.

## Executed SIMULATED results

One deterministic Python standard-library CPU process, two constant-density paths of equal illustrative length 1300 km, five energies 0.8–3 GeV, both neutrino signs. Parameters: \(\theta=8.6^\circ\), \(\Delta m^2=2.5\times10^{-3}\,{\rm eV}^2\), \(V_0=1.07\times10^{-13}\,\rm eV\). Truth \((a,q)=(1,0.1)\). Path A electron/dark ratios (1,1), B (1.5,1).

| Control | Result |
| --- | ---: |
| One-path probability change under \((1,0.1)\to(1.1,0)\) | 0 exactly on tested grid |
| One-path smaller Gram eigenvalue | 0 at recorded precision |
| Two-path maximum probability separation under that relabeling | **0.00363119** |
| Two-path smaller/larger Gram eigenvalues, with **one shared** electron calibration | **0.000520753 / 0.05701594** |
| Free per-path electron nuisances: Jacobian null residual | **3.47e-12** |

Gram eigenvalues are unweighted sensitivity diagnostics, **not significance**. Fourteen implementation/limiting/readback checks passed. The first process raised an off-by-one results-count **bookkeeping** assertion after the physics checks; the corrected run passed and the failure is [preserved](FAILURE_HISTORY.md). Deterministic seeds: none. Executed source SHA-256 is \`6a44c12ba92831194797142ba76aea45dbc4945cfd9d4f975a42681206f10767\`; the corrected original run's receipt and CSV are in the chat companion package. Run this source: \`python run.py --out output\`. No external data/likelihood were fitted.

**Feasibility warning:** for illustrative local DM density 0.4 GeV/cm³ and 1-GeV asymmetric fermions, dark particle density is 0.4 cm⁻³. At ordinary density 2.8 g/cm³ and \(Y_e=0.5\), electron density is about \(8.37\times10^{23}\) cm⁻³. A 10% extra matter potential needs \(G_\chi/(\sqrt2G_F)\sim2.1\times10^{23}\) in this naive heavy-mediator contact model. The benchmark \(q=0.1\) is NOT demonstrated physically viable.

## Prior art, scope and stopping rule

The 2025 PDG neutrino review, Sec. 14.5, provides the standard coherent forward potential and Hamiltonian: https://pdg.lbl.gov/2025/reviews/rpp2025-rev-neutrino-mixing.pdf . The 2026 preprint arXiv:2601.04802 studies a **different complex-scalar dark medium**, correcting the mass-squared Hamiltonian; do not silently identify it with our vector-current case: https://arxiv.org/abs/2601.04802 . The 2016 Coloma-Schwetz generalized NSI degeneracy is more established prior art, but is NOT the same narrow reparameterization as N-06: https://arxiv.org/abs/1604.05772 .

**Strongest null:** uncertain electron densities exactly absorb the added flavor-diagonal potential. **Falsifier of identifiable-dark claim:** a joint nuisance fit remains rank deficient. **Next gate:** test an energy- or geometry-dependent physically consistent interaction versus standard matter, including calibrated profiles and detector response, before any significance estimate.

[Checkpoint](CHECKPOINT.md) · [Methods and full mathematical contract](METHODS_RESULTS_v1.0.md) · [Run code](run.py) · [Actual limited numerical receipt](RESULTS.md)
