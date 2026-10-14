# Learning checkpoints

**All concepts: `NOT_ASSESSED`.** An explanation or successful computation does not demonstrate the reader's mastery. Record an actual worked answer before changing the state.

## The educated-reader layer

**Added at the user's request, 14 October 2026.** Every research chapter should include a genuine explanation for an educated reader who is not yet a specialist. Keep the mathematics; supply the missing bridges.

Start with what the physical system is doing and what is actually measured. Introduce each mathematical object when it becomes necessary, identify its entries or axes, then show the intermediate operation that produces the next equation. Explain why that operation is physically appropriate. A symbol glossary alone is not an explanation.

Use this sequence: physical question → defined quantities → intermediate algebra → a small worked example → observable consequence → assumptions and failure case. Provide sensible units and scales where relevant. Explain a matrix's role before discussing its entries: a state vector, evolution matrix and density matrix describe different things even when their dimensions match. Explain new notation such as a complex conjugate before relying on it.

Do not substitute metaphors for mechanisms, remove important qualifications to make prose smoother or equate a prediction with a measurement. Use diagrams when they clarify an actual relationship. Separate a quick orientation from the optional full derivation so experienced readers can navigate directly to the part they need.

For every claimed signature, finish the chain: what changes in the underlying physics, how it changes the predicted observation, which conventional effect can imitate it, and which independent test distinguishes them. Do not require a quiz every run. Never mark an AI-written answer as the user's demonstrated understanding.

## Concept ledger

| Concept | Recovered memo | Assessment exercise |
| --- | --- | --- |
| Profile likelihood | 9 October | Derive the nonnegative background optimum and explain $r=0$ |
| Solid angle and response matrices | 10 October | Derive $d\Omega=d(\sin\delta)d\alpha$ and column-sum conservation |
| Covariance propagation | 11 October | Explain why weighted observed counts are not independent Poisson samples |
| Lensing Jacobian | 12 October | Derive the orientation term; distinguish signed/absolute magnification |
| Finite-source fold lensing | 13 October | Identify degenerate shifts and what curvature adds |
| Matrix rank | 14 October | Construct the six-by-four matrix and its null vector; choose three contrasts |
| Amplitudes, relative phase and density matrices | 14 October, analytical explainer below | Explain how equal mass probabilities can produce different flavor probabilities |
| Oscillations, redshift, gravothermal transport | Earlier work mentioned | Recover teaching notes, then define a concrete exercise |

Start with $F=(1,0.45,0.35,0.07)$. Write six log ratios, rescale every flux by 10, and explain the invariant. Explain why rounded posterior summaries need not close exactly even when sample-wise ratios do.

An assessment entry records date, question, worked answer, correction, and remaining gap. Do not label an AI answer as the user's answer.

---

## Worked bridge: how a neutrino phase becomes a probability

**Area:** quantum mechanics / particle astrophysics. **Status:** `DERIVED` under an explicitly idealized two-state model. This is established mathematics, not a new particle claim or a reproduced experiment.

### 1. The physical distinction comes first

A neutrino flavor state produced in a weak interaction is a superposition of mass states. The mass components acquire different phases during propagation. A flavor-sensitive detection combines their contributions to one outcome. The standard relation between mass states, propagation and detection is given in the [Particle Data Group review, section 14.4](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-neutrino-mixing.pdf), especially Eqs. (14.35)-(14.39).

For a small example, retain only two orthogonal mass states, $|1\rangle$ and $|2\rangle$, and choose two idealized flavor channels

$$|+\rangle=\frac{|1\rangle+|2\rangle}{\sqrt2},\qquad |-\rangle=\frac{|1\rangle-|2\rangle}{\sqrt2}.$$

This is maximal mixing in a two-state teaching model. It is not the measured three-flavor mixing matrix. The ket symbols label state vectors, not trajectories or little particles inside one particle.

### 2. Why the initial column contains square roots

Produce the plus state. In the mass basis its amplitude column is

$$\psi(0)=\frac1{\sqrt2}\begin{pmatrix}1\\1\end{pmatrix}.$$

The rows refer to mass states 1 and 2. Squaring each amplitude's magnitude gives $1/2$; the probabilities sum to one. This explains the normalization. The coherent state is not merely a classical list of two probabilities because the relative phase is also retained.

### 3. What phase means

Write a complex amplitude as $z=r e^{i\phi}=r(\cos\phi+i\sin\phi)$. The magnitude $r$ fixes its isolated probability contribution $r^2$. The angle $\phi$ determines how it adds to other amplitudes for the same outcome. The complex-plane angle is not the neutrino's position, travel direction or physical rotation.

Multiplying every component by the same phase is unobservable in this setup: every measured amplitude receives that common factor, whose squared magnitude is one. A **relative** phase need not cancel.

For constant energies, time evolution gives component factors $e^{-iE_jt/\hbar}$. Removing the common factor leaves a relative phase $\phi=-(E_2-E_1)t/\hbar$ in the equal-momentum, plane-wave teaching approximation. The full relativistic oscillation treatment relates this to the mass-squared splitting and $L/E$; it does not require literal spinning clocks.

### 4. Read an evolution matrix as an operation

A phase-only evolution is

$$D(\phi)=\begin{pmatrix}1&0\\0&e^{i\phi}\end{pmatrix},\qquad D(\phi)\psi(0)=\frac1{\sqrt2}\begin{pmatrix}1\\e^{i\phi}\end{pmatrix}.$$

Multiplication leaves the first amplitude unchanged and multiplies the second by $e^{i\phi}$. The zero off-diagonal entries mean this operation transfers no amplitude from one mass component into the other. Consequently both mass-state probabilities remain $1/2$. That does **not** imply that flavor probabilities remain unchanged.

### 5. The detector question changes the calculation

For detection in the plus channel, take the overlap with its row vector, $(1,1)/\sqrt2$:

$$A_+=\frac1{\sqrt2}(1,1)\frac1{\sqrt2}\begin{pmatrix}1\\e^{i\phi}\end{pmatrix}=\frac{1+e^{i\phi}}2.$$

This combines the two mass components' contributions to the **same detection outcome**. It is not interference between two separate neutrinos. To get the probability, multiply the amplitude by its complex conjugate; conjugation changes $i$ to $-i$:

$$P_+=A_+A_+^*=\frac{(1+e^{i\phi})(1+e^{-i\phi})}{4}=\frac{2+e^{i\phi}+e^{-i\phi}}4=\frac{1+\cos\phi}{2}.$$

The last step uses $e^{i\phi}+e^{-i\phi}=2\cos\phi$. This is the interference term that would disappear if one added the probabilities too early.

| Relative phase | Plus-channel amplitude | Plus-channel probability |
| --- | --- | --- |
| $0$ | $1$ | $1$ |
| $\pi/2$ | $(1+i)/2$ | $1/2$ |
| $\pi$ | $0$ | $0$ |

At $\phi=\pi$ the neutrino has not vanished: in this ideal two-channel system $P_-=1-P_+=1$. There are no observed event counts in this table.

### 6. Why a density matrix is useful

The outer product of the amplitude column and its conjugate row is

$$\rho(\phi)=\psi\psi^\dagger=\frac12\begin{pmatrix}1&e^{-i\phi}\\e^{i\phi}&1\end{pmatrix}.$$

The dagger means transpose and complex conjugation. Every entry is $\rho_{ij}=a_i a_j^*$. The diagonal entries are the probabilities for mass measurements in this basis. The off-diagonal entries retain relative-phase coherence. These are not the transition entries of the evolution matrix $D$; the two matrices have different jobs.

Multiplying out $(1,1)\rho(1,1)^T/2$ gives $P_+=(\rho_{11}+\rho_{22}+\rho_{12}+\rho_{21})/2$. This explicitly shows where the off-diagonal information enters the detector probability.

Suppose the incoming ensemble has phases uniformly spread around a complete cycle. Then $\langle e^{i\phi}\rangle=0$ and its averaged state is

$$\overline\rho=\frac12\begin{pmatrix}1&0\\0&1\end{pmatrix}.$$

The equal mass probabilities are unchanged, but the ensemble has no phase-sensitive cross term. Every subsequent phase-only shift $D(\delta)$ obeys

$$D(\delta)\overline\rho D(\delta)^\dagger=\overline\rho.$$

More generally this invariance holds for any mass-diagonal input $\operatorname{diag}(w_i)$ under any diagonal phase operation: each diagonal factor multiplies its complex conjugate to one, and every zero off-diagonal entry stays zero. Every fixed flavor projection is therefore unchanged.

**Scope matters:** this assumes genuinely mass-diagonal input or independent prior dephasing, not unresolved correlated phases that a later operation might refocus. It assumes phase-only propagation and fixed production/detection and energy distributions. Interactions with mass transitions, extra states or altered source/detector physics are not covered. The special equal mixture above is proportional to the identity and is invariant under any unitary; do not use it as a generic example of population redistribution.

### 7. Connect the algebra to a dark-sector hypothesis

[Airoldi et al., arXiv:2603.02382v1](https://arxiv.org/html/2603.02382v1), submitted 2 March 2026, studies a scalar coupling diagonal in the mass basis. Sections II-III explicitly distinguish diagonal evolution from phase averaging. This motivates checking what coherence remains before predicting a detectable phase signature. The cited work is a preprint model, not evidence of a detected scalar field.

The decisive question is not merely whether a proposed interaction changes a phase. It is whether that change survives the source ensemble, energy/baseline averaging and the calibrated detector response, and differs from conventional explanations. A measured flavor fraction is also not automatically a detector event-type fraction; efficiencies and interaction cross sections matter.

### Execution and continuity boundary

The preceding interrupted N-03 calculation encountered an output-permission failure followed by a JSON-serialization failure. The prior tool transcript reports intermediate CSV/figure output, but those working files are not accessible in the resumed runtime. No completed numerical package is published or claimed by this guide. Recover the actual files and execution receipt before promoting the numerical result or claiming a repaired pipeline passed. This update adds an inspectable analytical explanation and the teaching standard, not a new simulation run.
