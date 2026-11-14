# C-13 | LOS gas velocity does not close a sky-plane shock clock

**Run date:** 2026-11-01. **Claim:** C13-LOS-CLOCK. **Statuses:** DERIVED / SIMULATION_RESULT / UNIDENTIFIABLE for the declared toy / DATA_INSUFFICIENT for observational inference. This is established kinematics applied to an identifiability gate, not new dark-matter physics.

## Physical question

C-12 showed that an X-ray density jump and gas temperature determine shock speed relative to the **upstream gas**, not necessarily the speed relative to the cluster. Does measuring that gas's Doppler velocity fix a radio-relic shock clock? Not in general. A spectrometer measures the gas's **line-of-sight (LOS)** velocity, while merger shocks often propagate partly across the plane of the sky. Unmeasured sky-plane flow can be traded against merger time.

**AHA (explanatory):** another measurement is useful only when it constrains the *missing component* of the physical state.

## Source audit (as accessed 2026-11-01)

- Heinrich et al., [*The major cluster merger in Abell 2034 as seen by XRISM*](https://doi.org/10.33232/001c.168514), *Open Journal of Astrophysics*, published **2026-08-26**; [arXiv:2604.27161v2](https://arxiv.org/abs/2604.27161v2) dated **2026-08-20**. **Journal metadata and abstract only; methods not independently audited.** Its authors report a ~380 km/s LOS gas velocity gradient with sign opposite to a galaxy velocity gradient. This is **OBSERVED AS REPORTED** for Abell 2034, not a flow measurement for the Abell 115 shock used in the numerical example.
- [Official TNG-Cluster data documentation](https://www.tng-project.org/data/cluster/) describes 352 original high-mass zoom simulations and 100 snapshots (20 full, 80 mini). Its gas-tracer \`SHOCKMACHNUM_MAX\` is a **maximum since the previous full snapshot**, not the instantaneous speed or location of a particular shock front. Gas cells must be loaded from the appropriate original zoom; low-resolution PartType2 contamination must be excluded. Data access requires a login. This public CDM baseline is **not** the unreleased matched TNGC-SIDM merger suite.
- Carry-forward: [C-12 source and math checkpoint](https://github.com/Arnie016/dark-sector/blob/b7a54de743f892bcf4acafa5d1971fdd8a3de30f/research/2026-10-26-merger-phase-identifiability/C12_XRAY_SHOCK_FRAME_GATE_2026-10-31.md), with a **rounded derived** relative shock speed \`w = 1852.68 km/s\` obtained from a different cluster, Abell 115. No telescope events or simulation arrays were processed in C-13.

## Derivation

Take \`x\` across the sky along the projected shock propagation and \`z\` along the observer's line of sight. The unit shock-normal vector is \`n = (cos i, sin i)\`, where inclination \`i\` is assumed *known*. Let upstream gas flow be \`u=(u_x,u_z)\` km/s, relative shock-normal speed be \`w\` km/s and elapsed time be \`t\` Gyr. For a constant-speed planar shock starting at the reference origin,

\`\`\`text
R_projected(Mpc) = t(Gyr) * [w + u_x cos(i) + u_z sin(i)] * cos(i) / K
K = 977.792... km/s per (Mpc/Gyr)
\`\`\`

A hypothetical X-ray measurement fixes \`u_z\` and a compression/temperature model fixes \`w\`. Even with fixed inclination and projected distance \`R\`, the exact inverse relation

\`\`\`text
t(u_x) = K R / ([w + u_x cos(i) + u_z sin(i)] cos(i))
\`\`\`

leaves a continuous one-parameter family of indistinguishable ages. The single-row Jacobian of \`R\` with respect to \`(t,u_x)\` has rank one, so extra precision in \`R\` cannot determine both unknowns. In the \`i=0\` limit, LOS gas velocity contributes **nothing** to normal shock speed. When the normal points exactly along LOS, projected radius is zero and this particular sky-plane clock ceases to work.

## Exact SIMULATED example and execution receipt

Use **SIMULATED** projected shock travel \`R=1 Mpc\`, angle \`i=20°\`, LOS flow \`u_z=+200 km/s\`; carry forward the rounded \`w=1852.68 km/s\` from C-12 purely as an input. The three hypothetical sky-plane flows give:

| SIMULATED \`u_x\` (km/s) | Projected speed (km/s) | SIMULATED inferred age (Gyr) |
|---:|---:|---:|
| -500 | 1363.7174 | 0.717005 |
| 0 | 1805.2285 | 0.541645 |
| +500 | 2246.7396 | 0.435205 |

All reproduce the same mock projected 1-Mpc distance, same mock LOS flow and same relative shock speed. **None is a measurement of Abell 115 or Abell 2034.** This is a forward-model identity, not a fitted observational SIDM signal.

One original Python 3 standard-library process ran in a ChatGPT Linux container with a 20-second hard timeout and exit **0**. Internal computation time reported **0.000727 s**, excluding Python startup. Seven assertions passed; **one was tautological**, therefore *at most six useful implementation checks*. Executed script SHA-256: \`77091b38cae8e2284ce8d39d46e851c87f66de42ffee5b8cb115995568b21094\`. Raw SIMULATED JSON SHA-256: \`db36d36e9f78ca4e4ab03eb366e9936d35765e6734e11e39c167c5dd23b298d0\`. No random seed. Executed source and output are in the verified user-facing companion archive; they are **not uploaded in this GitHub commit**. No external numerical simulation, full likelihood, CI or independent peer review was run.

## Falsifier, checkpoint and next gate

**Competing explanation / resolution:** independent physical information about \`u_x\` or upstream speed *along the shock normal* could constrain the age. A mere LOS gas map generally cannot determine it without dynamical or geometric assumptions. An additional galaxy LOS velocity cannot simply be equated with upstream gas flow; Abell 2034's reported opposing gradients emphasize why.

**Stopping rule:** no SIDM fitting from this idealized example. Next retrieve one physically tracked shock trajectory and upstream vector velocities from a contamination-safe *single* TNG-Cluster zoom, use full-snapshot times and actual shock geometry, then compare instantaneous relative Mach-derived speeds against shock displacement; do not mistake tracer **maximum Mach since previous snapshot** for instantaneous shock motion. Only if matched CDM/SIDM halos and appropriate selection/covariance become accessible should dark-interaction inference proceed. Independent halos, not neighboring snapshots, define validation splits.

**Research checkpoint:** C-13 DERIVED + SIMULATION_RESULT (toy) + UNIDENTIFIABLE (with named observations) + DATA_INSUFFICIENT (real inference). Preserve C-03 globally unscreened gravity **FAILED**, C-06/C-08 geometry nulls, C-09/C-10 covariance gates, C-11 finite shock-bias example and C-12 frame ambiguity.

**Learning checkpoint:** sky-plane versus LOS velocity projections **INTRODUCED**, understanding **NOT_ASSESSED**. **Digestibility self-check:** physical picture 2/2 (user-facing schematic), symbols 2/2, worked scale and limit 2/2, discriminator 2/2, empirical/synthetic boundary 2/2: **10/10 self-rated only**. Gap: no measured or simulated 3D shock trajectory has yet been visualized.
