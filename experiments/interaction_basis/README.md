# N-04 | Mass mixing after lost phase coherence

**16 October 2026 · DERIVED + SIMULATION_RESULT. Physical origin remains UNIDENTIFIABLE without additional observations.**

This bounded study extends [N-03](../phase_visibility/README.md). It is a one-logical-qubit teaching model, not a three-flavor neutrino fit, trained AI, quantum hardware demonstration or dark-matter detection.

## What the physicist is asking

A mass-diagonal phase interaction leaves an initially mass-diagonal ensemble unchanged. Does that mean every interaction is invisible after coherence is lost? **No.** Mixing can redistribute unequal populations. Whether a detector sees the change also depends on its measurement.

## Follow the intermediate mathematics

Start with an incoherent mass mixture

$$\rho=\begin{pmatrix}w&0\\0&1-w\end{pmatrix},\quad w=0.7.$$

Rows and columns label two mass states, not spatial coordinates. The zero off-diagonal terms mean incoherence in this basis. A diagonal phase gate preserves both populations. Instead, consider

$$R_x(\beta)=\begin{pmatrix}\cos(\beta/2)&-i\sin(\beta/2)\\-i\sin(\beta/2)&\cos(\beta/2)\end{pmatrix}.$$

For each input mass state, square the magnitude of its transition amplitude into mass state 1, then weight by that input state's population:

$$w'=w\cos^2(\beta/2)+(1-w)\sin^2(\beta/2)=\tfrac12+(w-\tfrac12)\cos\beta.$$

Now erase outgoing off-diagonal terms. This removes coherence but does not undo the changed populations. Define the ideal flavor channel $|\alpha\rangle=\cos\theta|1\rangle+\sin\theta|2\rangle$. Its probability is

$$P_\alpha=w'\cos^2\theta+(1-w')\sin^2\theta=\tfrac12+(w-\tfrac12)\cos(2\theta)\cos\beta.$$

For the assumed $\theta=30^\circ$, $P_\alpha=0.5+0.1\cos\beta$.

| Gate angle beta | SIMULATED probability |
|---|---:|
| 0 | 0.60 |
| pi/2 | 0.50 |
| pi | 0.40 |

**Explanatory insight, not a discovery:** loss of original coherence does not imply immunity to every later interaction. The input state, interaction basis and measurement jointly determine sensitivity.

## Two essential null cases

The exactly equal incoherent mixture $I/2$ is unchanged by every unitary. Also, an exactly 45-degree flavor projection after complete output dephasing cannot see diagonal population redistribution. A state change is therefore not sufficient to guarantee a measured signal.

A conventional and a dark-field mechanism implementing the same quantum channel, with the same input and measurement, remain indistinguishable. The same-map check in the code is a bookkeeping identity, not independent evidence that two realistic theories coincide.

## What ran

`run.py` is the actual executed NumPy implementation, not pseudocode. It checked 5,184 finite parameter combinations, generated a 241-point SIMULATED scan and passed 16 implementation/limiting checks. Complex density-matrix evolution agreed with an independently written real Bloch-coordinate formula to 2.22e-16. No random draws or observed events were used.

Numerical core: 0.205827764 s. Full scientific process: 1.125552345 s. One worker, 30-second timeout, exit code 0. Environment: Linux / Python 3.13.5 / NumPy 2.3.5. No processes remain. The script's SHA-256 is recorded in the results below. A small negative eigenvalue of order 2.5e-16 is floating-point roundoff within the declared 1e-12 tolerance, not a physical negative probability.

Reproduce in an environment with NumPy:

```sh
python run.py --output output
```

The code emits full JSON results, the scan CSV and 32 browser-kernel fixtures. Do not compare runtime as an invariant. The companion chat archive additionally contains a self-contained interactive HTML laboratory, graph files, JavaScript fixture checker and browser render receipts. Those larger interface artifacts are not part of this compact repository increment.

## Scope and interpretation

The propagation is explicitly sequential Rz then Rx, followed by independent dephasing. It is not the exponential of a simultaneous Galactic Hamiltonian. Beta is an assumed dimensionless angle; no mass, density, cross section or dark coupling is inferred. A two-state system omits the full measured three-flavor structure. A selectable ideal projection is a mathematical probe, not a knob on an actual neutrino detector.

Standard propagation and coherent forward scattering: [PDG neutrino review](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-neutrino-mixing.pdf), especially section 14.5. Related, not reproduced, dark-field prior art: [Brdar et al., arXiv:1705.09455](https://arxiv.org/abs/1705.09455). N-03 phase-only model: [Airoldi et al., arXiv:2603.02382v1](https://arxiv.org/html/2603.02382v1). These sources motivate the question; they do not calibrate our illustrative gates.

## Research and learning checkpoint

The actual main-branch parent was b6b85682f0843ae0d097b5f192d90b51b130788d. Its N-03 code, STATUS and checkpoint were read. A separate conversation N-03 archive with 15 checks was recovered with Files and inspected; it differs from the remote 12-check implementation. Neither was rerun here. Earlier permission/export failures remain in history. A graph-export permission failure in this run was resolved only within the newly created study directory; saved numerical data were rendered without rerunning the experiment.

New concepts introduced: interaction basis, population redistribution and measurement blindness. Reader understanding remains NOT_ASSESSED. No claim of novel physics, independent peer review or formal Lean proof is made. No scheduler change, outreach, paid compute or manuscript submission occurred.

**Next discriminating step:** specify one microscopic dark-field Hamiltonian and its ordinary-matter competitor, then test joint energy/direction/time predictions with independently constrained source and detector inputs. Stop with UNIDENTIFIABLE if their predictions coincide on the actual observed domain. Do not train a classifier to distinguish labels whose generating distributions are identical.
