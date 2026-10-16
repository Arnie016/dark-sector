# N-05 | Light and neutrinos share gravity

**16 October 2026. DERIVED.** This is established propagation physics plus SIMULATED numerical scale checks, not a new coupling, measured redshift or detector forecast.

## The physical connection

The matter distribution changes spacetime geometry; both photons and neutrinos propagate through it. Gravity is an interaction, but no new direct photon-neutrino coupling is required. The photons used to image a galaxy lens normally trace its gravity rather than provide the dominant gravitating energy. A lens measures total gravitational structure, so attributing part to dark matter still requires a visible-matter model.

Magnification changes collected flux, not each photon's energy. For a weak point-mass lens, photon deflection is 4GM/(bc^2), independent of photon energy in geometric optics. Static lensing, endpoint gravitational redshift and cosmic redshift must be distinguished.

## The indirect phase equation

Define rest energies mu_i=m_i*c^2 in eV. Expanding E_i=sqrt(p^2*c^2+mu_i^2) at high energy gives the local splitting Delta E_ij=Delta(mu^2)_ij/(2 E_local). Accumulating phase with dphi=Delta E*dt_local/hbar and c*dt_local=dell along the common near-null path yields

$$\Delta\varphi_{ij}[\mathcal C]=\frac{\Delta(\mu^2)_{ij}}{2\hbar c}\int_{\mathcal C}\frac{d\ell}{E_{\rm local}(\ell)}.$$

`dell` is locally measured path length; `dt_local` is the stationary local observer's time, not the neutrino's proper time. The geometry determines both the path and E_local. This leading-relativistic, static-background vacuum expression follows [Cardall & Fuller, Eqs. 31-35](https://arxiv.org/abs/hep-ph/9610494). It is not a full matter/spin solver.

**Cancellation check:** for radial Schwarzschild propagation, A=1-r_s/R, dell=dR/sqrt(A), E_local=E_infinity/sqrt(A). Thus dell/E_local=dR/E_infinity at fixed areal coordinates and asymptotic energy. This does not mean coordinate distance equals proper distance, or that all gravity effects vanish. It prevents adding a spurious separate gravitational phase.

Minimal vacuum gravity in this approximation is phase-only in the mass basis. It does not implement the Rx population-mixing gate from the separate N-04 study. An already mass-diagonal incoherent ensemble remains invariant under diagonal phases.

## Neutrino redshift and speed

For freely propagating particles in a homogeneous expanding universe,

$$p_0=\frac{p_{\rm em}}{1+z},\qquad E_0=\sqrt{\mu^2+\frac{p_{\rm em}^2c^2}{(1+z)^2}}.$$

Only the ultra-relativistic limit gives E_0 approximately E_em/(1+z). A single continuum neutrino does not identify z because its emitted energy is unknown. Host spectroscopy or an independently justified emission feature is needed.

Combining E(z)=E0*(1+z) with abs(dt/dz)=1/[(1+z)H(z)] gives

$$\Delta\varphi_{ij}=\frac{\Delta(\mu^2)_{ij}}{2\hbar E_0}\int_0^{z_s}\frac{dz}{(1+z)^2H(z)}.$$

Here H(z) is the cosmic expansion rate, not a quantum Hamiltonian. This homogeneous limit is distinct from a static-lens model. The eigenstate speed obeys v/c=sqrt(1-(mu/E)^2); light's local speed remains c.

**SIMULATED inputs:** mu=0.05 eV; mass-squared splitting 0.0025 eV^2; H0=67.4 km/s/Mpc; Omega_m=0.315; flat matter+Lambda, no radiation, z<=1.

| Quantity | Calculated value |
|---|---:|
| 1-v/c at 10 MeV | 1.25e-17 |
| 1-v/c at 100 TeV | 1.25e-31 |
| Mass-only delay at 10 MeV over 10 kpc, flat space | 12.866 microseconds |
| Cosmic phase kernel at z=1 | 5.922255 Gyr |
| Vacuum phase at 100 TeV, z=1 | 3.54924e15 radians |
| Fractional energy change for one radian | 2.81750e-16 |
| Mass-only delay at observed 100 TeV, z=1 | 2.33615e-14 seconds |

An enormous accumulated phase does not imply an observable oscillation pattern. Finite energy resolution and source averaging matter; see [PDG 2025, Eq. 14.42](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-neutrino-mixing.pdf). No sensitivity or physical parameter was inferred here.

## Testable null: repeated lensed transients

For two images A and B, define

$$\mathcal D=(t_{\nu,B}-t_{\nu,A})-(t_{\gamma,B}-t_{\gamma,A}).$$

A common intrinsic neutrino/photon emission offset cancels, assuming matched emission regions/features and a stable lens. The transparent massless common-path GR limit predicts zero. Mass, matter, source offsets and lens evolution require corrections; a residual is not automatically dark matter. This is established [Baker & Trodden](https://arxiv.org/abs/1612.02004) prior art, not a new test discovery. The timestamp example in the code checks algebra only, not a lens event simulation.

**Recommended next step:** forecast identified event counts with actual public response, source rates and exposure. Stop with DATA_INSUFFICIENT when those inputs are absent. Reject an observational design if sparse events or source uncertainty erase its discriminating power. Neutrino images need not be spatially resolved; temporal repetitions still require enough associated events.

## Detector dates and provenance

The explicit IceCube-Gen2 **2033** completion projection appears in an [18 August 2020 official announcement](https://icecube.wisc.edu/news/research/2020/08/icecube-gen2-will-open-new-window-on-universe/). Its [current homepage](https://icecube-gen2.wisc.edu/) describes a planned extension, not a newly confirmed completion commitment. JWST is already active, launched 25 December 2021 per [NASA](https://science.nasa.gov/mission/webb/). Photon telescopes constrain lenses and host redshifts, not neutrino quantum phases.

## Reproduction and checkpoints

Run `python run.py` with Python's standard library. This overwrites the local results.json with a new receipt. Eight finite numerical/algebraic checks passed, followed by strict JSON readback; these are not eight independent physics validations. One CPU process, 20-second timeout, no seed or random draws; numerical core 0.006858 s excluding startup. No real events, GPU, installation, payment or detector likelihood.

Frozen code SHA-256: `94c84cadd8679c36f1972bfc89bfa4bedf014a056ff17985991ae72162338290`. Runtime/environment fields may vary on rerun.

**Research continuity:** actual main HEAD and open PRs inspected; N-04 methods read through Files. N-04 stays in its separate PR; no previous experiment was rerun or retroactively repaired. This study supplies the standard-gravity baseline before adding speculative interactions.

**Learning state:** shared cause versus direct coupling, proper versus coordinate distance, momentum redshift and source-lag cancellation introduced. Learner understanding remains unassessed.

Sources [Cardall & Fuller] Sections III-V and [Baker & Trodden] propagation/delay methods read, not merely abstracts. PDG averaging section read. These are established 1996/1997, 2016/2017 and 2025 references, not new October observations. Some PDF screenshots failed but parsed equations were accessible. No inaccessible figure was treated as evidence. Extended explanation and a source-access log are retained in the chat companion archive. No schedule change, outreach or manuscript submission.
