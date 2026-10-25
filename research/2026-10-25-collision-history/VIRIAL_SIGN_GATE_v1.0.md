# C-05-V | Virial sign gate: why a gravitating core can heat as it loses energy

**25 October 2026 · v1.0 · `DERIVED` / `DATA_INSUFFICIENT`**  
**Classification:** established mechanics, new-to-this-repository interpretation gate. No new dark-matter particle constraint, simulation reproduction, astronomical inference or claim of scientific novelty.

## Physical question and AHA

The [C-05-H supplement](HEAT_ORDER_v1.0.md) evolves two *fixed, equal positive-heat-capacity* reservoirs. It correctly finds, **within that declared model**, that an earlier outer heat impulse produces a larger final inner specific kinetic energy. Does that directly tell us whether a self-gravitating dark-matter core expands or collapses? **No.**

**AHA, explanatory rather than a discovery:** after an isolated gravitational system re-equilibrates, losing **total** energy can *raise* its random particle speeds. Heating the kinetic motions and increasing the system's mechanical energy are different operations. Therefore the sum of two zones' kinetic energies, conserved in the C-05-H exchange matrix, is *not* a legitimate replacement for the conserved kinetic-plus-gravitational energy of a restructuring halo.

This sign distinction is central to gravothermal collapse, not an invented effect: see Lynden-Bell & Wood, *MNRAS* **138** (1968), 495–525, [doi:10.1093/mnras/138.4.495](https://doi.org/10.1093/mnras/138.4.495). For modern SIDM with cosmological mergers see Silverman et al., *Mergers Matter*, [arXiv:2606.02566v1](https://arxiv.org/abs/2606.02566v1), posted **1 June 2026**, Sec. I and III. The latter explicitly reports that merger-associated energy redistribution changes core evolution in six dark-matter-only simulations. Its model and results were not reproduced here.

## One worked tool: the virial theorem

Take an **isolated, stationary, self-gravitating uniform sphere** with fixed total mass `M` [solar masses] and radius `R` [kpc]. Assume Newtonian gravity, negligible surface pressure, isotropic random velocities and a virialized equilibrium. The gravitational potential energy of this uniform sphere is

\[
W=-\frac{3GM^2}{5R},\qquad 2K+W=0,
\]

where `G` is Newton's constant and `K` is kinetic energy. The second equality is the *virial theorem*, a relation for a relaxed state, **not** an instantaneous law during a merger. Combining the two gives

\[
K=\frac{3GM^2}{10R},\quad
E_{\mathrm{total}}=K+W=-\frac{3GM^2}{10R}=-K.
\]

For one-dimensional velocity dispersion `s` [km/s] in three isotropic directions, `K=3Ms^2/2`. Thus

\[
\boxed{s^2=\frac{GM}{5R}},\qquad
\boxed{E_{\mathrm{total}}=-\frac32 M s^2}.
\]

The minus sign is the relevant physical test. Along this *fixed-mass family of equilibria*, `dE_total/d(s^2)=-3M/2 < 0`. It is a negative kinetic-temperature response of this idealized whole sphere. It is **not** a universal statement that all spatially selected halo cores have negative heat capacity.

### Exact numerical-scale illustration, not data

Set `M=10^8 M_sun`, `R_0=1.0 kpc` and `G=4.30091×10⁻⁶ kpc (km/s)² / M_sun`. Then `s_0²=86.0182 (km/s)²`, `s_0≈9.275 km/s`. Suppose the sphere **re-virializes** at the same mass but at `R_1=0.8 kpc`:

\[
\frac{K_1}{K_0}=\frac{R_0}{R_1}=1.25,\quad
\frac{s_1}{s_0}=\sqrt{1.25}\approx1.118,\quad
E_1-E_0=-0.25K_0<0.
\]

**Result C05-V1 `DERIVED / KNOWN`:** in this declared virial family, a 20% smaller radius accompanies 25% higher kinetic energy **and 25% greater magnitude of negative total binding energy**. Energy has left the idealized bound sphere while the particles move faster. Every number comes from the displayed formulae; **no numerical code, astronomical dataset or CPU experiment was run for this supplement**. Seed: not applicable.

### Limits that actively test the claim

For `R_1=R_0` the increments vanish. For `R_1>R_0` the signs reverse: a higher total energy accompanies lower kinetic dispersion in the re-virialized fixed-mass family. At fixed `M` and `R`, the uniform-sphere model cannot make kinetic energy arbitrary while preserving equilibrium. These limiting checks are analytic, not independent simulation validation.

If a core exchanges mass with the outer halo, experiences external gravitational fields, has important boundary pressure, undergoes time-dependent tidal disturbance, or has not re-virialized, the simple `2K+W=0` and uniform self-gravitating `W` do not apply. Observed line-of-sight stellar velocities are also not automatically the dark particles' `s`; projection and tracer dynamics need calibration.

## Contract and falsification

**Smallest claim, C05-V1:** within the *fixed-mass isolated virialized uniform-sphere approximation*, loss of total energy implies higher isotropic kinetic dispersion along the homologous contraction family. **Falsifier:** a correct derivation of the stated virial equilibrium under the same assumptions yielding `E_total≠-K`, or inconsistent ratio/units checks.

**Strongest competitor:** the **positive-capacity reservoir** is correct as a deliberately nongravitating transport model; the virial sign gate does not refute its algebra. A dark halo with external tidal forcing, baryonic feedback, changing core mass or appreciable pressure work need not follow either simple family. Neither model can on its own predict SIDM collapse.

**Required observables for physical use:** joint time-resolved gravitational potential or density profile, DM velocity-dispersion profile from calibrated simulations, mass flux across core boundaries, surface-pressure/tidal terms, merger heating history, numerical-energy-conservation receipts and independent initial-condition groupings. For galaxy observations, stellar-tracer selection, projection and covariance must be modeled. **Stop** if these terms are unavailable or the measured/resolved virial residual is too large for the quasi-equilibrium approximation. Do not infer `sigma/m` or collapse status from these teaching models.

**C05-V2 `DATA_INSUFFICIENT`:** no such calibrated joint history or virial residual was calculated here. A low-volume SIDM Concerto parametric tar exists in its [Zenodo v1 file inventory](https://zenodo.org/records/14933624) (published 26 February 2025), but downloading its 348.2-kB LMC_Halo104 file failed in this environment. Its contents and suitability for this test were **not** audited. The release separately omits large `tree*.dat` files, which must not be assumed present. Relevant primary source inspection: through 25 October 2026.

## Compact continuation checkpoints

**Research:** preserve C-05's fixed-trajectory scattering-history degeneracy and C-05-H's valid positive-capacity impulse-timing result without treating either as a gravothermal collapse simulation. Add this **virial sign/energy-accounting gate** before attempting any core-heating surrogate. C-03's globally unscreened `f(R)` model remains `FAILED`; all observational inference remains `DATA_INSUFFICIENT`. No external physics baseline reproduced, no source code executed, no outreach/manuscript/schedule action.

**Learning:** introduced the virial theorem as an equilibrium constraint, `K` versus `K+W`, and negative kinetic-temperature response in a self-gravitating toy. **User understanding: NOT_ASSESSED**, no mastery claim. Optional check: if a fixed-mass isolated sphere shrinks while remaining virialized, does its *total* energy increase? **No: it becomes more negative, even as its velocity dispersion grows.**

**Next bounded gate (recommended):** obtain a matched CDM/SIDM halo profile time series with known gravitational potential, mass flux and solver conventions; calculate `2K+W` with correct boundary terms on *independent halo tracks* before interpreting heat flow. An inadequate virial residual or missing terms would reject the simple closure rather than be dressed up as a SIDM cross-section measurement.
