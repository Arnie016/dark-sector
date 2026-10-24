# N-07 | Schwarzschild path weighting in an assumed neutrino-dark-matter spike

**23 October 2026. DERIVED + SIMULATION_RESULT; observational DATA_INSUFFICIENT.** This is a methodological extension of N-06's retained **SIMULATED** density spike, not new event data, an IceCube fit, a fully curved Einstein-matter solution or a discovery.

## Physical question and AHA

Does the black-hole gravitational field change the neutrino forward-potential phase area? The leading radial *vacuum* mass-splitting phase at fixed conserved energy cancels the static metric factor because local energy redshifts while radial proper distance stretches. A *local medium-induced forward potential* accumulates with proper distance and therefore does not cancel in the same way. This established difference is the explanatory AHA, not a novel neutrino law.

Take Schwarzschild f(r)=1-r_S/r and locally static matter, outward radial propagation. The proper-distance element is dℓ=dr/sqrt(f) while E_loc=E_infinity/sqrt(f). Consequently

$$d\phi_{\rm vac}=\frac{\Delta m^2}{2E_{\rm loc}}d\ell
=\frac{\Delta m^2}{2E_\infty}dr,$$

$$I_\chi^{\rm proper}=\frac1{\hbar c}
\int_{r_p}^{R_{\rm sp}}\frac{\|V_{\chi,\rm loc}(r)\|}{\sqrt{1-r_S/r}}dr.$$

For the same static local density and nonnegative potential norm, monotonicity supplies an exact integral bound:

$$1\le I_\chi^{\rm proper}/I_\chi^{\rm flat}\le(1-r_S/r_p)^{-1/2}.$$

If the dark vector charge is symmetric, I=0, and this ratio is undefined rather than unity. A strictly flavor-universal potential drops out of observable oscillations; a norm bound need not be saturated. For fixed *local emission* energy instead of fixed energy at infinity, the vacuum-phase comparison changes because E_infinity itself depends on gravitational redshift.

## Bounded computation

Reused Dev et al.'s explicitly assumed NGC 1068-like profile from the N-06 code: 10^7 solar-mass Schwarzschild black hole, emission at 10^-5 pc, spike boundary 700 pc, NFW scale 13 kpc, NFW scale density 0.35 GeV/cm^3, density proportional to (1-4r_S/r)^3 r^(-7/3). The numerical correction holds this local profile fixed as a test input. Assumed contact parameters: |C|=1, Lambda=1 TeV, m_chi=1 GeV, |asymmetry|=1.

| Model-calculated quantity | Value |
|---|---:|
| Schwarzschild radius [pc] | 9.5711211041e-7 |
| Flat radial N-06 phase-norm area | 0.05349915044 |
| Schwarzschild proper-distance phase-norm area | **0.05474432286** |
| Relative increase | **2.32746%** |
| Analytic ratio ceiling | 1.0515899494 |
| Prior maximum absolute probability-change bound | <= 0.10699830 |
| Updated conservative bound | **<= 0.10948865** |
| Column formed within 10^-4 pc | 91.35% flat; 91.52% proper |

The last two probability numbers are ceilings from 2I, **not measured probabilities or predicted flavor transitions**. One bounded Python 3.13.5 standard-library process under a 25-second timeout, no random draws, one worker; 11 implementation and limiting controls passed with strict JSON readback. Source SHA-256 **a7528d69a57f9bccb681c4d8788fcea267b9a2f2d37ac1915f2c6b6635ed470c**. Run **python3 run.py** to regenerate full results.json and its receipt. Log-radius Simpson integration used 2048/4096/8192 intervals. The exact executed source and full numerical receipt are in the chat companion package.

## Stable claims and falsifiers

**N07-C1 DERIVED / KNOWN:** leading radial vacuum phase cancels explicit static f at fixed E_infinity, while local medium potential is weighted by f^(-1/2). Stop if a covariant derivation under identical assumptions violates either statement.

**N07-C2 SIMULATION_RESULT:** this specified profile gives a 2.327% correction; the flat baseline recovers N-06's earlier integrated density column. Independent quadrature outside tolerance would refute this numerical implementation result.

**N07-C3 DATA_INSUFFICIENT:** the spike, source radius, asymmetry and coupling are not calibrated observations; neither the PMNS three-flavor evolution, lensing geodesics, dark-matter gravity backreaction, detector likelihood nor charged-lepton constraints were calculated. The strongest null remains zero net vector charge or ordinary source/matter effects. This small fixed-model correction cannot establish a dark particle.

## Sources and continuity

- [Dev et al., arXiv:2609.26773v1](https://arxiv.org/html/2609.26773v1), posted **22 September 2026**. Read Sections II–IV; provides the assumed particle current and density profile.
- [Mannobova et al., arXiv:2610.25053v1](https://arxiv.org/html/2610.25053v1), posted **18 October 2026**. Read Section IV.1; leading radial vacuum cancellation. Its *perfect-fluid dark-matter geometry* and multi-path lensing are distinct from Dev et al.'s particle-current potential and **not** simulated here.
- Cardall & Fuller, *Physical Review D* 55, 7960 (1997), doi:10.1103/PhysRevD.55.7960, earlier gravity-and-matter neutrino prior art.

**Research checkpoint:** a documented omission in N-06 is bounded for one explicit benchmark, with little change in its practical interpretation. C-03's unscreened long-range gravity candidate remains FAILED. **Learning checkpoint:** local vs conserved energy, proper vs areal radial distance and norm-bound interpretation introduced; actual reader mastery **NOT_ASSESSED**.

**Recommended next gate:** before heavier curved-space propagation, require a gauge-consistent particle interaction and data products sufficient to separate unknown source flavor from ordinary matter/NSI. The geometric correction is only 2.3% here, while the unmeasured dark asymmetry can set this vector effect to exactly zero.
