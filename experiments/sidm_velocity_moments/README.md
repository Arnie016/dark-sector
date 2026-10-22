# S-03 | Velocity-weighted self-interacting dark matter

**22 October 2026 | DERIVED + SIMULATION_RESULT + UNIDENTIFIABLE (single speed moment).** No observational halo or detector inputs were used. This is an original numerical audit of established kinetic theory, not a new particle interaction or an N-body reproduction.

## Question and explanatory AHA

When particles have a distribution of relative speeds, which "effective cross section" should describe them? It depends on what the experiment measures. The **AHA** is that a collision-rate proxy and a conductivity-motivated proxy emphasize different speeds, even for exactly the same microscopic scattering law. An effective value obtained for one observable is not automatically transferable to another.

[S-02](https://github.com/Arnie016/dark-sector/tree/research/s02-angular-transport-2026-10-21/experiments/angular_transport) calculated the angular moments at a fixed velocity. Here we perform the missing speed average. This is not the actual heat flux, which also depends on temperature gradients and transport regime.

## One mathematical tool: a weighted expectation

[Nadler et al., SIDM Concerto, arXiv:2503.10748v2 (29 September 2025), Eq. 1](https://arxiv.org/html/2503.10748v2) specify the angular scattering law. Set relative speed \(v\), transition speed \(w\), scattering-angle cosine \(\mu=\cos\theta\), and \(y=(v/w)^2\):

\[
\frac{d\sigma}{d\mu}
 =\frac{\sigma_0}{2[1+y(1-\mu)/2]^2},
\qquad
\frac{\sigma_V(v)}{\sigma_0}
 =6\frac{(y+2)\ln(1+y)-2y}{y^3}.
\]

The second expression integrates the first with an explicitly **3/2-normalized** angular factor \(1-\mu^2\), to downweight weakly deflecting encounters. Its small-\(y\) limit is \(1-y+0.9y^2+\cdots\). Angular normalization conventions must be checked when comparing papers.

For **SIMULATED independent isotropic Gaussian** one-particle velocities with component standard deviation \(s\) km/s, the relative-speed density is

\[
f_s(v)=\frac{v^2}{2\sqrt{\pi}\,s^3}e^{-v^2/(4s^2)},
\quad\langle v\rangle=\frac{4s}{\sqrt{\pi}}.
\]

Define \(R_p=\langle v^p\sigma_V(v)\rangle/\langle v^p\rangle\), where brackets mean integration with this distribution. \(R_1\) is a normalized **viscosity-weighted rate-like proxy**, not total collision counting. \(R_5\) is a **conductivity-motivated cross-section proxy**, supported by [Fischer et al., MNRAS 529 (2024), Eq. 9](https://academic.oup.com/mnras/article/529/3/2327/7624679) following Yang & Yu (2022). Neither is the physical heat flux or gravothermal collapse time.

For small \(s/w\), the Maxwell moments give

\[
\boxed{\frac{R_p}{\sigma_0}
 =1-2(p+3)(s/w)^2+O((s/w)^4).}
\]

Thus the first corrections are \(1-8(s/w)^2\) for \(R_1\), and \(1-16(s/w)^2\) for \(R_5\). This expansion is not reliable when \(s\) approaches or exceeds \(w\); the numerical calculation integrates the full formula.

## MODEL-CALCULATED, not observed

Use the published \(\sigma_0/m=147.1\) cm²/g for both models, with GroupSIDM \(w=120\) km/s and MilkyWaySIDM \(w=24.3\) km/s. Each \(s\) below is an invented **one-particle 1D dispersion**, not an empirical halo velocity distribution.

| Model | \(s\) (km/s) | \(R_1/m\) (cm²/g) | \(R_5/m\) (cm²/g) |
|---|---:|---:|---:|
| GroupSIDM | 30 | 101.1964 | 74.6756 |
| GroupSIDM | 100 | 26.05595 | 9.71664 |
| GroupSIDM | 300 | 2.43759 | 0.447729 |
| MilkyWaySIDM | 30 | 12.4551 | 3.57660 |
| MilkyWaySIDM | 100 | 0.639002 | 0.0885479 |
| MilkyWaySIDM | 300 | 0.0230913 | 0.00192201 |

At \(s=100\) km/s, the mean relative speed is about **225.7 km/s**, not 100 km/s.

### The identifiability control

A *deliberately artificial* alternative with \(w=24.3\) km/s and adjustable \(\sigma_0/m=5998.149\) cm²/g exactly matches the GroupSIDM \(R_1/m=26.05595\) cm²/g at \(s=100\). Yet the alternative's \(R_5/m=3.61063\) differs from the reference \(9.71664\). At a held-out \(s=30\), their \(R_1/m\) values are **507.87** versus **101.20**; at \(s=300\) the values are **0.942** versus **2.438**.

A single \(R_1(s;\sigma_0,w)=\sigma_0F(s/w)\) fixes only a parameter combination. Other speed regimes may distinguish these restricted laws if the actual velocity distributions and nuisance uncertainties are controlled. The altered normalization is **not** asserted to satisfy any particle-physics bound.

## Actual execution and stopping rule

One standard-library CPU run, deterministic Simpson integration of \(u=v/(2s)\) over \([0,10]\), coarse and fine grids of 6,000 and 12,000 intervals. **26 internal numerical/limiting checks passed**; maximum dimensionless grid difference \(5.07\times10^{-13}\). No RNG, paid compute, observations, N-body simulations, background covariance or particle-response fit. The executed \`run.py\` has SHA-256 \`cc069fd4b835c7527f0b45113ccf8e15fc957f8b6ef0886b9558b78a9361e1e3\`. Run \`python3 run.py\` to regenerate full \`results.json\`; see [summary](summary.json). Internal checks are not independent observational validation.

**Strongest null:** merger and accretion histories, uncertain halo velocity anisotropy, baryonic feedback or lens/velocity inference freedom explain apparent halo differences. A viscosity-weighted cross section is not a complete conductivity prediction; increasing or decreasing it need not produce a proportional change in real halo heat transport.

**Recommended next test:** recover public SIDM Concerto matched Halo004 particle velocities and masks, verify units and identities, measure the actual \(f(v,r)\), then hold out independent halos rather than nearby snapshots. Stop at **DATA_INSUFFICIENT** without those inputs. [Mergers Matter, June 2026](https://arxiv.org/html/2606.02566v1) demonstrates history sensitivity. [TNGC-SIDM I, October 13 2026](https://arxiv.org/abs/2610.18957) instead uses velocity-independent cluster benchmarks and is not reproduction of this work. A Zenodo release redirect was not accessible during this run; that does not establish permanent absence.

**Research checkpoint:** main at \`b6b85682\`, open PRs #4–#8 inspected, S-02 source read. Existing C-03 FAILED unscreened-gravity result is preserved. **Learning checkpoint:** weighted speed expectation, relative versus individual dispersion and structural non-identifiability introduced; actual user understanding **NOT_ASSESSED**. No scheduler changes, outreach or scholarly submission.
