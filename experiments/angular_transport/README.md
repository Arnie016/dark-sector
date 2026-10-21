# S-02 | Counting collisions is not measuring transport

**21 October 2026** | S-02-C1 **DERIVED**; S-02-C2 **MODEL_CALCULATED**; observational inference **DATA_INSUFFICIENT**. This is an original worked calculation of established scattering physics, not a new particle or halo simulation.

## Physical question

Can a dark-matter model produce many scattering events but relatively little transfer of directions or heat? Yes. At high velocity, a forward-peaked differential cross section counts many small-angle deflections. Such events must not all be treated as equally effective at changing halo trajectories.

**AHA, explanation rather than discovery:** event counts and transport are different angular moments of the *same scattering law*. The distinction grows dramatically with relative speed.

## Equation and worked angular integral

Nadler et al. [*SIDM Concerto*, arXiv:2503.10748v2, section II Eq. 1](https://arxiv.org/html/2503.10748v2) specify a differential cross section as a function of relative speed \`v\` and deflection angle \`theta\`:

$$\frac{d\sigma}{d\mu}=\frac{\sigma_0}{2[1+(v/w)^2(1-\mu)/2]^2},\qquad \mu=\cos\theta.$$

The angle cosine \`mu\` varies from -1 (backward) to +1 (forward), \`w\` is the transition velocity in km/s and \`sigma0\` is the low-speed cross-section scale. Integrate over \`mu\` to count scattering events. Weight instead by \`(3/2)(1-mu²)\` for the explicitly normalized **viscosity moment**, which downweights small direction changes. The factor 3/2 makes the moment equal the total cross section when scattering is isotropic.

With \`y=(v/w)²\`, substitute \`x=(1-mu)/2\`, then integrate:

$$\boxed{\frac{\sigma_{\mathrm{tot}}}{\sigma_0}=\frac{1}{1+y}},\qquad
\boxed{\frac{\sigma_V}{\sigma_0}=6\frac{(y+2)\ln(1+y)-2y}{y^3}}.$$

At small \`y\`, both approach 1, as isotropy requires. At large \`y\`, total scattering falls roughly as \`v^-2\`, but viscosity-weighted scattering falls approximately as \`v^-4 ln v\`. This is established mathematics. The precise normalization is stated because viscosity-moment conventions vary.

## MODEL-CALCULATED values, not observations

Published inputs in Section II of Concerto: GroupSIDM uses \`sigma0/m=147.1 cm²/g\`, \`w=120 km/s\`; MilkyWaySIDM uses the same amplitude with \`w=24.3 km/s\`. Both models also have different N-body histories; these numbers are **fixed-speed cross sections, not halo density predictions**.

| Model | Relative speed | Total / mass | Normalized viscosity / mass |
|---|---:|---:|---:|
| GroupSIDM | 30 km/s | 138.447 cm²/g | 138.396 cm²/g |
| GroupSIDM | 1000 km/s | 2.08817 cm²/g | **0.435095 cm²/g** |
| MilkyWaySIDM | 30 km/s | 58.2769 cm²/g | 53.5259 cm²/g |
| MilkyWaySIDM | 1000 km/s | 0.0868098 cm²/g | **0.00167533 cm²/g** |

At 1000 km/s, angular transport weighting retains 20.8% of GroupSIDM total collision area, but only 1.93% of MilkyWaySIDM. It does not mean particles did not scatter. At an *illustrative* fixed density \`1e-25 g/cm³\`, GroupSIDM gives 0.659 counted events/Gyr versus 0.137 angular-weighted rate units/Gyr. Those are rate proxies, **not halo core-collapse times**.

## What ran

\`python run.py --output results.json\` ran on one bounded CPU process (1.339 seconds including startup), no RNG or external datasets, 100000-interval independent Simpson integration directly over \`cos(theta)\`. Forty implementation and limiting-case checks passed. Largest absolute dimensionless discrepancy between closed form and quadrature: \`6.47e-12\`. Code SHA-256: \`b18ee464ed82f5d8b9ee456738d44eb40b8f3f164089892a36e744dde8bc7070\`. These are implementation checks, not 40 independent physics validations. Full raw JSON and high-resolution figure accompany the ChatGPT research report; the script regenerates the receipt.

## Scientific contract and prior art

**S-02-C1 DERIVED:** for the cited angular law and explicitly defined viscosity normalization, total and transport cross sections diverge at high relative speed. **S-02-C2 MODEL_CALCULATED:** the cited Concerto parameters yield the table. **S-02-H1 CONJECTURE:** particle models that look comparable in one collision-count regime may predict distinct transport in another regime, once velocity distributions and dynamical histories are controlled.

**Strongest null:** changes in halo cores could instead arise from merger histories, gas physics, orientation or inference freedom. Two models with the same effective transport response over the observed velocity distribution can remain indistinguishable even if their microscopic scattering law differs. Stop at **DATA_INSUFFICIENT** without independent velocity distributions and calibrated halo-response likelihoods.

This does not reproduce Concerto's N-body simulations, its actual effective heat-conduction kernels or published constraints. [Yang & Yu, JCAP 2022](https://doi.org/10.1088/1475-7516/2022/09/077) already investigate angular-weighted thermal evolution: no new-physics priority is claimed. The [13 October 2026 TNGC-SIDM I preprint](https://arxiv.org/abs/2610.18957) instead uses constant-cross-section cluster experiments, so one must not equate its cross-section benchmark with the total of a forward-peaked model.

**Recommended next gate:** verify actual velocity-distribution and matched-halo identities in the released Concerto Halo004 files, using held-out independent halos rather than multiple snapshots as independent samples. The historical release lacks some Consistent-Trees files. Do not claim a matched-halo reproduction without those inputs.

**Research checkpoint:** main \`b6b85682\` and PRs #4-#8 checked; C-04 endpoint censoring, S-01 projection ambiguity, D-04 sidereal aliasing and C-03 failed global unscreened model remain separate. **Learning checkpoint:** angular moment and normalization introduced, isotropic limiting case shown; user understanding **NOT_ASSESSED**. No schedule change, outreach or scholarly submission.
