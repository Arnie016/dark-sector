# S-03 | Velocity averages are not interchangeable

**22 October 2026. S-03-C1: DERIVED. S-03-C2: SIMULATION_RESULT. S-03-C3: UNIDENTIFIABLE for a restricted single moment.** This is a worked computational check of known SIDM kinetic theory, **not** observed dark matter, an N-body baseline reproduction, or a new particle claim.

## Question and explanatory AHA

Does one representative halo speed determine its heat transport response when self-interaction strength falls sharply with relative speed? No. The outcome depends on **which velocity-weighted expectation** an observable probes. The rate of angular deflection and a conductivity-motivated response weigh the same interaction differently.

[Nadler et al., SIDM Concerto, arXiv:2503.10748v2, Section II Eq. (1), 29 September 2025](https://arxiv.org/html/2503.10748v2) use
[
rac{dsigma}{dmu}=rac{sigma_0}{2[1+(v/w)^2(1-mu)/2]^2},quadmu=cos	heta.
]
Here v is the relative speed in km/s, w the transition velocity and mu the cosine of the deflection angle. Our (3/2)-normalized angular viscosity cross section is
[
sigma_V(v)=rac32int_{-1}^{1}(1-mu^2)rac{dsigma}{dmu}dmu
=sigma_0,6rac{(y+2)ln(1+y)-2y}{y^3},quad y=(v/w)^2.
]
The small-y limit is sigma_V/sigma0 = 1-y+0.9y²+..., not a numerically safe direct subtraction at small y.

With two independently sampled, isotropic Gaussian velocity vectors of one-particle 1D dispersion s, the relative-speed probability density is
[
f_s(v)=rac{v^2}{2sqrtpi,s^3}e^{-v^2/(4s^2)},quad
langle vangle=4s/sqrtpi.
]
For p=1 versus p=5 define
[
R_p(s)=rac{int_0^infty dv,f_s(v)v^psigma_V(v)}
             {int_0^infty dv,f_s(v)v^p}.
]
R1 is a viscosity-weighted encounter-rate **proxy**, not total collision count. R5 is a literature-motivated heat-conduction effective cross section, *not* the heat flux or a gravothermal collapse time. The p=5 effective weight is already in [Fischer et al., MNRAS 529 (2024), Section 3.2.1 Eq. (9)](https://academic.oup.com/mnras/article/529/3/2327/7624679), based on Yang & Yu (2022). Neither this weighting nor the SIDM angular model is a novelty claim.

The normalized radial Maxwell moment is
[
langle v^pangle=(2s)^prac{2}{sqrtpi}Gamma((p+3)/2).
]
Consequently, for s/w small,
[
R_p/sigma_0=1-2(p+3)(s/w)^2+O((s/w)^4).
]
At first correction order, R5 decreases twice as fast as R1.

## MODEL-CALCULATED output (not observed)

Published GroupSIDM parameters: sigma0/m=147.1 cm²/g, w=120 km/s. Published MilkyWaySIDM parameters: same sigma0/m, w=24.3 km/s. For s=100 km/s, GroupSIDM yields R1/m = **26.05595** cm²/g and R5/m = **9.71664** cm²/g. The MilkyWaySIDM model gives R1/m = **0.639002** and R5/m = **0.0885479** cm²/g. The R5/R1 ratios are **0.3729** and **0.1386** respectively.

**Exact single-rate degeneracy control, SIMULATED:** Hold the first GroupSIDM R1 at 26.05595 by resetting the second model's otherwise-free sigma0/m to 5998.15 cm²/g. This is not a physically permitted coupling fit. Its R5/m is 3.61063 versus 9.71664. A held-out s=30 km/s environment predicts R1/m=507.87 versus 101.20; at s=300 km/s, 0.942 versus 2.438. One scalar R1 observation fixes only sigma0*F(s/w), not sigma0 and w individually. A second calibrated speed regime can separate *these restricted models*.

## Execution and falsifiability

One Python standard-library CPU process on a deterministic 0..10 transformed Maxwell integration interval using Simpson quadrature (6000 and 12000 subdivisions). **26 checks passed**, including small-speed limits, exact rate match, held-out separation, positivity and refinement. Largest coarse/fine difference in dimensionless response **5.07e-13**. No RNG, paid service, Mac or N-body data. SHA-256 of **actually executed** run.py: `cc069fd4b835c7527f0b45113ccf8e15fc957f8b6ef0886b9558b78a9361e1e3`. Run `python3 run.py` to regenerate full output `results.json`. This repository contribution includes the executable source and compact results summary; the complete numerical JSON/figure is in the ChatGPT companion package.

**Strongest null:** merger histories, baryonic feedback, speed-distribution uncertainty and simulated-halo selection explain differences. The Maxwell assumption does not apply automatically to merging or anisotropic halos. Actual heat flow also depends on gradients and long- versus short-mean-free-path conductivity: a smaller R5 does **not** universally imply smaller heat flow.

**Decision gate:** acquire actual released matched Halo004 velocities, verify particle IDs/units, measure f(v,r) under the same spatial mask for independent CDM/SIDM halos. Stop with DATA_INSUFFICIENT if those particle-level inputs cannot be retrieved. [Mergers Matter, June 2026 v1](https://arxiv.org/html/2606.02566v1) shows histories alter collapse even with constant scattering. [TNGC-SIDM I, 13 October 2026 v1](https://arxiv.org/abs/2610.18957) uses isotropic velocity-independent scattering, so it is not a reproduction of this velocity-dependent check.

**Research checkpoint:** S-02 fixed-speed angular audit on independent branch read; main HEAD b6b85682, PRs #4–#8 inspected. Preserve S-01/C-04/D-04/N-06 and the C-03 unscreened-gravity FAILED result. Old ZIP names were searched in Library without exact match; October 19 particle-physics bridge context was read.

**Learning checkpoint:** velocity distribution versus representative speed, relative versus one-particle dispersion, kinetic weight and observable identifiability introduced. Understanding: NOT_ASSESSED. No public scientific authorship claim, outreach or schedule change.
