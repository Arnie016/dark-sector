# N-04: A vanishing mean can hide a time-varying neutrino signal

**16 October 2026 | v1.0 | Claim N-04 | DERIVED + SIMULATION_RESULT + conditional UNIDENTIFIABLE.**
Observational data: **DATA_INSUFFICIENT**. All numbers are explicitly **SIMULATED**, with no real neutrino events or calibrated instrument response.

## AHA: temporal information can disappear in an ordinary average

The earlier [N-03 phase-averaging study](../../../experiments/phase_visibility/README.md) showed how sampling an unknown scalar-field phase creates a Bessel interference factor, and how different physical phase ensembles can yield identical averaged probabilities. N-04 asks whether one interval of *time-resolved* data contains extra distinguishing information.

A source that has **unchanged full-cycle probability** can still have a strong **periodic modulation**. A detector that operates for only part of that cycle need not measure the full-cycle average. These are established consequences of Fourier analysis and sampling, not newly discovered dark-sector phenomena.

## Physical system and the worked tool

For two orthogonal neutrino mass states, use the initial density matrix

$$\rho_0=\frac12\begin{pmatrix}1&c\\c&1\end{pmatrix},\quad 0\leq c\leq1.$$

Its diagonal entries are mass-state probabilities. The off-diagonal entries retain phase coherence, with visibility parameter $c$. The phase transformation is

$$D(t)=\operatorname{diag}(1,e^{i[\Delta+a\cos(\omega t+\theta)]}).$$

Here $\Delta$ is the vacuum phase, $a$ is the field-induced relative phase amplitude (radians), $\omega$ is angular frequency and $\theta$ the field's unknown initial phase. Projecting the evolved matrix onto the ideal plus flavor state gives

$$P_+(t)=\frac12[1+c\cos(\Delta+a\cos(\omega t+\theta))].$$

The Fourier coefficient

$$b_k=\frac2T\int_0^T P_+(t)\cos(k\omega t)\,dt,\quad k\ge1$$

extracts the size of the probability modulation at a particular integer multiple of the field frequency. We set $\theta=0$ for a worked example. With unknown phase, analysis must use **both sine and cosine** coefficients, not assume a known time zero.

For $\Delta=\pi/2$, the ordinary vacuum plus probability is $1/2$. Expanding the sine of a cosine:

$$P_+(t)=\frac12-\frac c2\sin(a\cos\omega t),$$
$$\boxed{\langle P_+\rangle_T=\frac12,\qquad b_1=-cJ_1(a)\simeq-\frac{ca}{2}.}$$

For $\Delta=0$, the cosine of a cosine has **even** harmonics:

$$\langle P_+\rangle_T=\frac{1+cJ_0(a)}2,\quad b_1=0,\quad b_2=-cJ_2(a)\simeq-\frac{ca^2}{8}.$$

The terms *odd* and *even* here describe time harmonics, **not CP-odd or CP-even neutrino interactions**. $J_n$ are ordinary Bessel functions, calculated by convergent power series in the accompanying script.

## Bounded CPU result

An executed single-worker standard-library Python program simulated **12 cycles**, 96 time bins per 24-hour cycle, with $a=0.30$ radians and $c=0.8$. One deterministic calculation completed all **12/12 checks**. No random observations or event counts were generated, so there is no stochastic seed. The 24-hour period is chosen *only* to stress-test an overlap with detector downtime.

| SIMULATED quantity | Result |
|---|---:|
| Mean of plus channel, $\Delta=\pi/2$ | 0.500000000 |
| First cosine harmonic, $\Delta=\pi/2$ | **−0.1186550530** |
| Mean of plus channel, $\Delta=0$ | 0.8910504986 |
| Second cosine harmonic, $\Delta=0$ | **−0.0089326896** |
| Plus mean when detector live only for $\cos(\omega t)>0$ | **0.4243531886** |
| Hypothetical scalar Compton energy $h/T$ for $T=24$ hours | **4.78665 × 10⁻²⁰ eV** |

The fifth result comes from a **SIMULATED 50% uptime mask** that is deliberately phase-locked to the hypothesized field. Real uptime was not measured. At an illustrative 50 km neutrino baseline, propagation time is approximately 0.17 milliseconds, far below 24 hours, supporting only the quasi-static-during-flight **limit**. The experiment is not a three-flavor matter propagation calculation, a sensitivity forecast, or a particle constraint.

**Local execution provenance:** Script SHA-256 d7fed431e38b21aa869731c1db08345347280767bf1b2eac2860601d8a3e2d28. Generated CSV SHA-256 a15da1daaa9e36ff1e0ba0418a8592123fa5e42391a2cd12cbe1887daf705a4c. Checks cover Bessel/Fourier agreement, forbidden harmonics, normalizations, positivity, zero-coherence limit, no-field limit and a conventional countermodel. Roundoff precision is not an observational error bar.

## Strongest conventional explanation and exact null

If a hypothetical scalar gives channel probabilities $P(t)$ and $1-P(t)$, both detected with constant efficiency $\epsilon=0.4$, its observed rates are proportional to $\epsilon P(t)$ and $\epsilon[1-P(t)]$. Consider a null with fixed true probabilities $1/2$, but independently time-varying channel efficiencies

$$\epsilon_+(t)=2\epsilon P(t),\qquad\epsilon_-(t)=2\epsilon[1-P(t)].$$

The observed count rates are **identical at every timestamp** under these two descriptions. Both efficiencies remain between zero and 0.8 in the toy, so the construction does not require an efficiency exceeding one. When channel efficiencies have no independent constraint, particle origin is **UNIDENTIFIABLE**, even from time-resolved counts.

**Falsifiable claim:** this precisely specified two-state, coherent, diagonal-phase model can produce a first time harmonic with zero full-cycle mean shift. **Rejection/stop conditions:** if realistic incoming coherence vanishes, or calibrated flux, energy response, live time and efficiency nuisance models absorb the effect on held-out data, do not infer a dark field. Event timing alone cannot settle the physical origin.

## Research and learning checkpoint

**Research:** one N-03 extension completed, without claiming recovery of earlier missing simulations. Previously found D-01 solar/sidereal, C-01 cosmological-bias and L-03 lens-core branches were left untouched. The physical detector-level problem remains DATA_INSUFFICIENT.

**Learning:** new tools introduced are Fourier projection, phase-correlation across events, exposure-weighted estimands and structural instrument-response degeneracy. Earlier mass-basis coherence and phase averaging remain prior concepts. **Actual learner understanding: NOT_ASSESSED.**

**Next recommended gate:** check for a public reactor-neutrino release containing time-tagged events, a detector live-time record, calibrated energy response and independent channel-efficiency constraints. If none are available, perform only a labeled feasibility forecast. Long-baseline fully mass-incoherent input has no signal from a purely mass-diagonal phase perturbation.

## Primary sources and coverage

**As of 16 October 2026. Targeted source-method inspection, not an exhaustive literature survey.**

* [Airoldi et al., Physical Review D 114, 015043](https://journals.aps.org/prd/abstract/10.1103/rh5j-fvry), published 28 July 2026. [ArXiv 2603.02382v1](https://arxiv.org/html/2603.02382v1), posted 2 March 2026, section III.1 explicitly averages phase-dependent density matrices.
* [Losada et al., JHEP 04 (2022) 030](https://link.springer.com/article/10.1007/JHEP04(2022)030), published 7 April 2022, examines time-averaged and time-resolved scalar-neutrino effects. [Losada et al., Physical Review D 108, 055004](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.108.055004), published 6 September 2023, studies time-dependent signatures in another field-frequency regime. These are explicit **prior art**: the temporal concept is not original here.
* [Centers et al., Nature Communications 12, 7321](https://www.nature.com/articles/s41467-021-27632-7), published 16 December 2021, explains coherent intervals and stochastic bosonic-field amplitudes. One observation interval does not necessarily sample the complete field ensemble.

No actual neutrino events, detector masks, likelihood fits, novelty claims, research outreach, or journal submissions were produced.
