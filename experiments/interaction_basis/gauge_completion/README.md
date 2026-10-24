# N-08 · Electroweak consistency gate for a neutrino–dark-matter potential

**24 October 2026 · v1.0 · DERIVED + SIMULATION_RESULT + DATA_INSUFFICIENT**

**Question.** The earlier N-06/N-07 studies assigned a vector-current potential to neutrinos crossing an assumed active-galactic-nucleus dark-matter spike. Can that potential arise from an electroweak-gauge-consistent particle model without an unavoidable charged-lepton counterpart? This note answers a narrow operator-level question before any further flavor simulations. The result is established prior art, **not a new theory or astrophysical inference**.

## AHA: selecting just the neutrino costs Higgs insertions

For Standard Model lepton doublet $L_\alpha=(\nu_{L\alpha},\ell_{L\alpha})^T$ and a gauge-singlet **Dirac** dark fermion $\chi$ with vector current $J_\chi^\mu=\bar\chi\gamma^\mu\chi$, a dimension-six gauge-invariant contact term is

$$
\mathcal L_6={C_6\over\Lambda^2}(\bar L_\alpha\gamma_\mu L_\beta)J_\chi^\mu+\mathrm{h.c.}
$$

Expanding the doublet gives **both** the neutrino current and the charged-lepton current with the same Wilson coefficient. For $\alpha\ne\beta$, a charged-lepton-flavor-changing dark interaction accompanies the neutrino term; for $\alpha=\beta$ the charged term is flavor-conserving. This is an operator relation, **not a claimed experimental rate or exclusion**.

The conjugate Higgs doublet $\widetilde H=i\sigma_2H^*$ has vacuum value $(v/\sqrt2,0)^T$, with $v=246.2$ GeV. Define the normalized two-component matrix

$$
P_\nu={\widetilde H\widetilde H^\dagger\over H^\dagger H}
\longrightarrow\begin{pmatrix}1&0\\0&0\end{pmatrix}.
$$

The rows and columns are the neutrino and charged-lepton positions in $L$. The projector satisfies $P_\nu^2=P_\nu$: it retains the upper component and eliminates the lower component. Its eigenvalues are **not detector probabilities**. The field-dependent contraction transforms covariantly before choosing a vacuum gauge.

The neutrino-selective gauge-invariant contact operator is instead possible at dimension eight:

$$
\mathcal L_8={C_8\over\Lambda^4}
(\bar L_\alpha\widetilde H)\gamma_\mu
(\widetilde H^\dagger L_\beta)J_\chi^\mu+\mathrm{h.c.}
$$

After symmetry breaking, its leading neutrino-only coefficient is $C_8v^2/(2\Lambda^4)$. No *tree-level charged-lepton bilinear from this operator* appears in the vacuum expression. This does **not** prove absence of loop effects, charged-lepton constraints, additional mediator couplings or neutrino-mass constraints. UV completions may have different allowed coefficients. For **Majorana** $\chi$, the Dirac-type vector bilinear vanishes identically; an axial-current interaction is a different model.

Prior art actually read: Babu, Dev and Thapa, *JHEP* **09 (2026) 046**, [arXiv:2512.25035v2](https://arxiv.org/html/2512.25035v2), Sec. 2 and Table 1, revised 8 September 2026 (journal published 3 September 2026). Historical context: Gavela et al., *PRD* 79, 013007 (2009), [arXiv:0809.3451](https://arxiv.org/abs/0809.3451). The benchmark AGN density is a source *assumption* from Dev et al., [arXiv:2609.26773v1](https://arxiv.org/html/2609.26773v1), submitted 22 September 2026.

## Numerical transfer of the previous **SIMULATED MODEL**, not a telescope fit

N-07 saved the fixed Schwarzschild-proper potential norm-area $A_7=0.05474432286434706$ using illustrative $C_6=1$ at $\Lambda=1$ TeV. Its code and summary were **read** at branch commit [1fadf2f](https://github.com/Arnie016/dark-sector/commit/1fadf2f89043b5fd45e8d4caa6399597014131e7); its integration was **not rerun** today. Independently choose $C_8=1$ and the same $\Lambda$, dark density and asymmetry. The electroweak matching factor is

$$
K={|C_8|\over|C_6|}{v^2\over2\Lambda^2}
=0.03030722,\qquad A_8=K A_7=0.0016591482368.
$$

This $3.030722\%$ reduction is a **hypothetical coupling-ratio comparison**, not a detector modulation fraction. To produce the same coefficient as the original dimension-six benchmark within this isolated dimension-eight parametrization, $|C_8|$ would need to be $32.9954$ when $C_6=1$. That does not itself rule out such a coefficient. Doubling $\Lambda$ with $C_8$ held fixed reduces this operator contribution by a factor of 16.

A separate, previously derived and standard **trace-distance contraction** tightens the original N-06/N-07 generic $2A$ ceilings: for an identical initial density matrix, purely unitary propagation with $H_1=H_0+V$ and the same complete detector channel, Duhamel gives $\|U_1-U_0\|\le A=\int\|V\|ds$. Hence propagated trace distance obeys $D\le A$, and **any fixed outcome** obeys $|\Delta P|\le\min(1,A)$. The N-07 bound for its original coefficient tightens from $0.109489$ to $0.0547443$; the N-08 matched-model bound is **at most $0.00165915$ (0.166 percentage points)**. These numbers are bounds, **not predicted flavor transitions** or detector sensitivities. If dark particle–antiparticle number densities match, this vector-current potential vanishes even if gravitationally inferred DM mass is huge.

**Execution:** One deterministic Python 3.13.5 standard-library audit, one worker, seed=null. 12/12 checks of matching, zero asymmetry, charge reversal, coupling/scale dependence, inherited geometry ratio and bound ordering passed. Source file [run.py](run.py) has local SHA-256 \`2b170663b8e7099d7747ce9cae6e0e94539a4a7ae5544e60337792c406452db9\`. [results.json](results.json) is the saved **SIMULATED MODEL** numerical receipt. Core wall time was measured in-process, not total scheduling time. The preflight equality-coefficient formula was corrected from inverse-square-root to inverse-linear before the final receipt. This audit does **not** symbolically prove gauge invariance or reproduce a detector likelihood.

## Stable claims, falsifiers and stopping rule

**N08-C1 | DERIVED / KNOWN.** The specified electroweak doublet operator includes a charged-lepton current; the Higgs-inserted dimension-eight contraction can isolate the neutrino current at leading vacuum order. Reject on a contradictory expansion of *these exact operators*. This is not a universal theorem about every UV completion.

**N08-C2 | SIMULATION_RESULT.** The toy fixed-column, fixed-$C$ rescaling produces $A_8=0.0016591482368$. Reject if independent units or matching checks disagree; do not interpret this as measured data.

**N08-C3 | DATA_INSUFFICIENT.** No mediator spectrum, independent dark asymmetry, source-flavor prior, charged-lepton bounds or calibrated event response has been fitted. The strongest null is a symmetric Dirac dark bath ($A=0$). Ordinary source-flavor variation and conventional matter NSI can imitate flavor changes.

**N08-C4 | UNIDENTIFIABLE (restricted).** If all observables depend only on the single product $C_8 f_A\int \rho_\chi ds/(m_\chi\Lambda^4)$ for one fixed path, a fitted propagation phase cannot identify each factor separately. Independent particle coupling/charge or mass-column constraints are needed.

## Checkpoints

**Research state.** N-06's October 21 absolute-asymmetry correction remains in its commit history. N-07's 2.327% Schwarzschild correction remains a specific **SIMULATED MODEL** result. N-08 introduces a gauge-consistency gate, a tighter established observable bound and a clear degeneracy. C-03's globally unscreened modified gravity candidate remains **FAILED** under Cassini. No dark-sector discovery or recovered IceCube likelihood.

**Learning state.** Introduced Higgs selection as a projection in lepton-doublet space; explained why a measured probability is not the same as a coupling coefficient or a bound. **USER UNDERSTANDING NOT ASSESSED.** Check: two Higgs fields supply two powers of $v$ with units GeV$^2$, converting a dimension-eight GeV$^{-4}$ coupling to an effective GeV$^{-2}$ coupling.

**Next recommended gate.** Map one specific UV-complete benchmark from Babu–Dev–Thapa into a physically allowed coefficient for the N-07 source potential, then compare an ordinary production-flavor competitor in the *same* likelihood. Do not optimize a candidate theory via AI until the evaluator rejects these known operator-level inconsistencies. Alternative decisive inputs are independent dark-current asymmetry constraints or a calibrated source-resolved flavor likelihood. No outreach, submission, user-device compute or schedule changes. Targeted primary-source coverage through 24 October 2026; not an exhaustive literature search.
