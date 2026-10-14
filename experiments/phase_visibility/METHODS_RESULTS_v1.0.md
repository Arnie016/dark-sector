# N-03 | Methods and results v1.0

## Physical question and sources

Can an oscillation pattern distinguish dark-sector physics from the way unresolved phases and field amplitudes were averaged?

Two perturbation ensembles inducing the same averaged density matrix give the same probabilities for every fixed measurement of that state. Their event timing or correlations may still differ.

Airoldi et al., [arXiv:2603.02382v1](https://arxiv.org/html/2603.02382v1), submitted 2 March 2026, derive a Bessel interference factor for a fixed-amplitude scalar with phase sampled uniformly. Sections II-IV, Eqs. (18)-(25) and (39), distinguish that exact average from a second-order weak-coupling description. This is established prior art, not our newly discovered signature. Their scalar coupling is diagonal in mass, with a small fractional mass shift and an approximately static field during each flight. That does not require the accumulated phase to be small.

Centers et al., [Nature Communications 12, 7321](https://www.nature.com/articles/s41467-021-27632-7), published 16 December 2021, discuss Rayleigh-distributed bosonic-field amplitudes and observation time relative to coherence time. We use Eq. (2) to motivate an alternative ensemble, not to import their experimental limits or conflate their entire model with a neutrino interaction.

**Coverage, 14 October 2026:** the above methods and version dates were read. A search surfaced arXiv:2610.08547 on stochastic polarization signals, but its primary full text failed to load and is not evidence for this calculation. No new October observations were ingested; this is not exhaustive literature coverage.

## Worked tool: average the phase factor

Use two mass states with an ideal equal-weight flavor projection, not measured three-flavor parameters. The initial density matrix is

$$\rho_0=\frac12\begin{pmatrix}1&c\\c&1\end{pmatrix},\qquad 0\leq c\leq1.$$

Diagonal entries are mass populations; off-diagonal entries retain relative-phase coherence. Here $c$ is incoming coherence, not a coupling or event probability. $c=1$ is the coherent plus superposition; $c=0$ an equal incoherent mixture.

The phase operation $D(\Phi)=\operatorname{diag}(1,e^{i\Phi})$ gives

$$D\rho_0D^\dagger=\frac12\begin{pmatrix}1&c e^{-i\Phi}\\c e^{i\Phi}&1\end{pmatrix}.$$

The dagger means transpose and complex conjugation. Populations remain unchanged; cross terms acquire phase factors. The plus-channel probability is half the sum of all four entries:

$$P_+(\Phi)=\frac{1+c\cos\Phi}{2}.$$

Separate the ordinary phase $\Phi_0$ and added perturbation $\delta$. Across different sampled perturbations,

$$C=\langle e^{i\delta}\rangle,\qquad \overline P_+=\frac{1+c\,\operatorname{Re}(e^{i\Phi_0}C)}{2}.$$

Angle brackets are a probability-weighted average. $C$ is a characteristic function evaluated at unit argument: it describes the distribution's effect on interference. It is **not** a probability; it can be negative or complex. Physical probabilities remain bounded because $|C|\leq1$. Average independently sampled neutrinos' density matrices or probabilities, not their amplitudes as though the beam were one coherent particle.

### Fixed amplitude, sampled cycle phase

Let $\delta=a\cos\xi$, with $\xi$ uniform on $[0,2\pi)$. $a$ is an added neutrino phase scale in radians, not the scalar amplitude itself. Then

$$C_{\rm fixed}(a)=\frac1{2\pi}\int_0^{2\pi}e^{ia\cos\xi}\,d\xi=J_0(a).$$

The integral defines the relevant zeroth-order Bessel function; its imaginary part cancels by symmetry. Using $\langle\cos\xi\rangle=0$, $\langle\cos^2\xi\rangle=1/2$ and $\langle\cos^4\xi\rangle=3/8$ gives

$$C_{\rm fixed}=1-\frac{a^2}{4}+\frac{a^4}{64}+O(a^6).$$

Zero mean phase perturbation therefore does not imply zero effect on probabilities.

### Sampled amplitudes as well as phases

Let $\delta=ar\cos\xi$, where $r\geq0$ has density $p(r)=2r e^{-r^2}$, hence $\langle r^2\rangle=1$. This is a Rayleigh distribution normalized by root-mean-square amplitude. Both ensembles have phase variance $a^2/2$.

Write $X=r\cos\xi$, $Y=r\sin\xi$. The area element is $dX\,dY=r\,dr\,d\xi$. The joint density is $e^{-(X^2+Y^2)}/\pi$. Integrating over $Y$ gives $p(X)=e^{-X^2}/\sqrt\pi$, a Gaussian with variance $1/2$. Therefore

$$C_{\rm sampled}(a)=\int_0^\infty2r e^{-r^2}J_0(ar)\,dr
=\int_{-\infty}^\infty\frac{e^{-X^2}}{\sqrt\pi}e^{iaX}\,dX=e^{-a^2/4}.$$

Ordinary Gaussian phase noise with variance $a^2/2$ gives exactly the same averaged channel under these assumptions. For small $a$,

$$e^{-a^2/4}=1-\frac{a^2}{4}+\frac{a^4}{32}+O(a^6).$$

The fixed- and sampled-amplitude models first differ at fourth order. Leading variance alone cannot distinguish them.

**Do not confuse regimes:** many sampled oscillation cycles need not mean many independent amplitudes. Within one coherence interval the amplitude may be constant but unknown. Marginalizing that shared amplitude in a joint likelihood is not equivalent to redrawing it independently for each event. Our Rayleigh curve is an ensemble/long-run expectation, not an event-independence assumption or a short-run likelihood.

## Calculation and results

One bounded deterministic study used two sequential process launches. The first failed on output permissions; the retry passed after repair. No random draws, package installations, paid services or surviving background workers.

Domain: 61 points $a\in[0,6]$, 2,048 uniform-phase nodes, 64-point Gauss-Laguerre integration after $u=r^2$, plus independent 160-point Gauss-Legendre Gaussian integration on $[-10,10]$ (tail below $3\times10^{-45}$). Lower-resolution convergence checks belong to the same calculation.

Twelve checks passed: analytic agreement, convergence, normalization, positivity, fourth-order behavior, diagonal-state invariance for **unequal** populations $(0.8,0.2)$, a mass-mixing negative control, and NumPy-boolean JSON conversion. Strict JSON was parsed back and saved atomically.

Largest absolute integration errors: fixed versus $J_0$, $2.29\times10^{-16}$; Rayleigh versus exponential, $1.42\times10^{-15}$; Gaussian versus exponential, $3.44\times10^{-15}$. These are numerical checks, not measured-physics uncertainties.

**SIMULATED MODEL**, $c=1$, $\Phi_0=0$:

| Phase scale | Fixed amplitude | Sampled amplitude or Gaussian phase noise |
|---:|---:|---:|
| 1 rad | 0.882599 | 0.889400 |
| 2 rad | 0.611945 | 0.683940 |
| 3 rad | 0.369974 | 0.552700 |
| 4 rad | 0.301425 | 0.509158 |
| 6 rad | 0.575323 | 0.500062 |

$J_0$ first crosses zero at $2.40482556$ rad. Negative $J_0$ reverses interference; it is not negative probability or particle disappearance. No measured events are in this table.

## Scope, scales and falsification

Any genuinely mass-diagonal incoming state is invariant under diagonal phase evolution: $D\rho D^\dagger=\rho$. This covers unequal populations. It assumes true dephasing or independent unresolved input phases; it does not forbid refocusing correlated phases, mass transitions or changed source/detector physics. In our equal-population example, $c=0$ gives $P_+=1/2$ for every $a$.

For scale only, a 50 km flight lasts about $1.7\times10^{-4}$ s; a hypothetical scalar rest energy $10^{-16}$ eV gives a period about 41 s from $2\pi\hbar/(m_\phi c^2)$. These are illustrative assumptions. Field coherence time is a separate scale controlling amplitude sampling.

The strongest conventional competitor is matched phase dispersion from uncertain source or detector quantities. Small fractional energy errors can yield Gaussian phase dispersion after linearizing a phase proportional to $L/E$. That approximation is not a full detector-response equivalence. We have no calibrated event likelihood, sensitivity forecast, cross-section limit or full three-flavor matter calculation.

**Stop rule:** no unique dark-field claim from a time-integrated damping curve until conventional dispersion and the correct field ensemble are constrained. These known identities establish no novelty claim.

## Recommended next bounded step

Construct one time-resolved conditional likelihood with field amplitude shared within each finite coherence interval and explicit exposure. Compare with a matched, time-independent instrumental phase-noise null. A predictable time correlation could discriminate mechanisms with identical integrated curves; if timing/exposure erases it, report `UNIDENTIFIABLE`.

Alternative: apply a calibrated energy-response kernel. Survival of the shape can justify later injection/recovery; disappearance rejects a practical discriminator. Neither branch was launched here.
