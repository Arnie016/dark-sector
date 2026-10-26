# N-11 | When does another neutrino-energy bin add information?

**26 October 2026 | Methods and results v1.0 | DERIVED / SIMULATION_RESULT / UNIDENTIFIABLE / DATA_INSUFFICIENT**

## The physical question

The 26 October N-10 study showed that dark-current and ordinary-matter couplings can be confused when the neutrino production mixture is freely adjustable per source. **Can measurements in two energy bins at each of two sources break that ambiguity?**

**AHA (explanatory insight, not discovery):** an additional energy bin adds identifying information only if physics constrains its source-production nuisance parameter *relative to the first bin*. With a new free production mixture in every bin, the extra observation can be absorbed by the extra unknown.

## Source and prior-art gate

Dev, Gaido, Ibarra & Porto, [*Resonant neutrino flavor conversion within dark matter spikes*, arXiv:2609.26773v1](https://arxiv.org/html/2609.26773v1), 22 September 2026, **preprint**, sections II, IV–VI and Appendix B, model a forward potential that competes with vacuum terms scaling as inverse energy. They calculate spatially varying, three-flavor propagation with redshift, production-model assumptions and long-baseline phase averaging. None of that external analysis was reproduced here.

Liu et al., [*Identifying energy-dependent flavor transitions in high-energy astrophysical neutrino measurements*, PRD 112, 043019](https://doi.org/10.1103/vrjj-h27p), published 13 August 2025, report no transition in an analysis of **7.5 years of earlier IceCube HESE observations**. This is not new independent exposure or evidence that an individual AGN's production fractions stay fixed across energies. Only the accessible publisher abstract, not the gated likelihood, was checked.

ALBERT's original [30 March 2026 preprint](https://arxiv.org/html/2603.28935v1) motivates an eventual physically constrained theory evaluator; no neural training or discovery model was executed. Literature novelty is not asserted.

## Exactly specified normalized two-flavor model

Everything calculated below is **SIMULATED** and dimensionless: no inferred astrophysical column densities, physical TeV bins or calibrated cross sections. In the electron/muon flavor basis, choose the constant Hamiltonian

\[
H_j(E)=\frac12
\begin{pmatrix}v_j&E^{-1}\\ E^{-1}&-v_j\end{pmatrix},
\qquad v_j=\theta_\chi x_j+\theta_e y_j,\qquad L=3.
\]

The diagonal entries encode a relative energy correction while off-diagonal entries mix flavors. Here \(x_j,y_j\) are assumed normalized environmental column templates, not measured dark or electron currents. The effective interaction coefficients are \(\theta_\chi,\theta_e\). For a pure initial electron flavor, exact coherent evolution gives

\[
p_j(E)=P(e\rightarrow\mu)=\frac{E^{-2}}{E^{-2}+v_j^2}
\sin^2\!\left[\frac L2\sqrt{E^{-2}+v_j^2}\right].
\]

An incoherent production source with electron fraction \(w_j\) and muon fraction \(1-w_j\) produces the final muon fraction

\[
z_j(E)=1-w_j+(2w_j-1)p_j(E).
\]

The conditional identification test assumes that each source's \(w_j\) stays the same at energies 1 and 2. This is a strong hypothesis to test, not an observational fact.

## Worked mathematical tool: the sensitivity Jacobian

A Jacobian matrix has one row per predicted observable and one column per unknown model parameter. Here four rows correspond to source/energy pairs (1,1), (1,2), (2,1), (2,2). Four columns correspond to \((\theta_\chi,\theta_e,w_1,w_2)\). Each entry answers how strongly that bin's predicted muon fraction changes if one parameter changes slightly.

\[
\frac{\partial z_j}{\partial\theta_\chi}=(2w_j-1)p'_j(v_j)x_j,\quad
\frac{\partial z_j}{\partial\theta_e}=(2w_j-1)p'_j(v_j)y_j,\quad
\frac{\partial z_j}{\partial w_j}=2p_j(E)-1 .
\]

The derivative with respect to the other source's \(w\) is zero. Define each source's two-energy sensitivity determinant

\[
D_j=(2w_j-1)\left[
p'_{j,1}(2p_{j,2}-1)-p'_{j,2}(2p_{j,1}-1)
\right].
\]

A block-matrix calculation produces an **exact model identity**:

\[
\boxed{|\det J|=|x_1y_2-x_2y_1|\,|D_1D_2|}.
\]

Thus one needs both nonproportional environment columns and within-source spectral variation that separates potential sensitivity from source-mixture sensitivity. A zero determinant means at least one locally invisible parameter direction. A nonzero determinant gives local invertibility in this noiseless model, **not** measured sensitivity, significance, or global uniqueness. In particular the probability is even in \(v\), so simultaneously reversing both couplings changes no prediction. At \(w=1/2\), output is constant irrespective of the potential.

## Actual bounded calculation and negative control

SIMULATED generating truth: \((\theta_\chi,\theta_e)=(0.4,0.2)\); \(w_1=w_2=0.7\); environment columns \((x_1,y_1)=(1,1)\), \((x_2,y_2)=(2,0.5)\); normalized energy bins 1 and 2; holdout energy 3. Alternative couplings are \((0.2,0.4)\).

| SIMULATED source and energy | Truth muon fraction | Alternative with a single adjusted production mixture per source |
|---|---:|---:|
| Source 1, E=1 | 0.58484661 | 0.58484661 |
| Source 1, E=2 | 0.43916141 | 0.43916141 |
| Source 2, E=1 | 0.47965890 | 0.47965890 |
| Source 2, E=2 | **0.39427363** | **0.51458542** |
| Source 2, held-out E=3 | **0.34742537** | **0.53133407** |

The alternative fits the first source-2 bin with \(w'_2=0.45205207\), but misses its second by **0.12031179**. The full four-by-four Jacobian determinant is **0.04068651416** in arbitrary normalized units, with no calibrated error model. Letting production instead vary independently between bins yields \(w'_2(E=1)=0.45205207\) and \(w'_2(E=2)=0.84756354\): both are physical fractions and **exactly mimic both observations**. This is an explicit **UNIDENTIFIABLE** null.

**Execution and provenance:** Two sequential bounded attempts on the ChatGPT Linux CPU with Python 3.13.5, no paid services and no RNG. The first implementation's zero-path test was vacuous; it was replaced before the final run by a genuine zero-path forward-model check. Final single worker had a 20-second hard timeout, exit 0, wall 1.03 s, and **15/15 passing implementation/limiting checks**. These are not observational likelihood validation, independent peer review or a reproduction of the cited AGN paper.

- Executed source SHA-256: **08cf78770bf2d52edd9c6e887babf810fc3e0b806308140e98e2aaac584f70ba**
- Raw result SHA-256: **78744205b072305b68b607dcf3fae2e14ec09e129688bd9a264de8bb740edba8**
- Original Git blob hashes checked before publication: source **f38f3e28c36f849a0c97d84acd2b5948384cd9d1**, results **ae5e5bd91dbdc61a1b68a9f5fa877a18f8488cdc**.
- Rerun with: python3 run.py results.json. Regeneration reflects the executing Python version in the result receipt.

Checks cover physical probability ranges, finite-difference derivatives, determinant factorization, source-column and half-mixture nulls, zero potential, sign inversion, zero length, exact nuisance mimicry and a held-out bin. The constant two-state evolution deliberately omits real three-flavor phase averaging, energy-dependent production, detector tagging and efficiency, covariance, redshift, selection, spatial density profiles and electroweak consistency.

## Claims, falsifier and next contract

**N11-C1 DERIVED:** Under fixed \(w_j\), the determinant identity is a local identifiability criterion. Falsify by a correct counter-derivation of the exact toy equations. **N11-C2 SIMULATION_RESULT:** The specific alternative fits E=1 but misses E=2 and held-out E=3 when constrained to one \(w_j\). Rerun code to challenge the numbers. **N11-C3 UNIDENTIFIABLE:** Energy-dependent free production fractions or global coupling sign flip reproduce the designated observables without unique dark inference. **N11-C4 DATA_INSUFFICIENT:** No actual detector likelihood, independent AGN production constraints or calibrated columns were fitted.

**Recommended next bounded gate:** build and validate a three-flavor, phase-averaged source-to-detector baseline with realistic energy response, ordinary NSI, production priors and joint covariance before training a theory proposer. Stop on nuisance-rank failure or inaccessible likelihood inputs. Alternatives are independent spectral production constraints or non-neutrino mediator bounds. Do not infer particles, submit a manuscript or silently merge this idealized check.
