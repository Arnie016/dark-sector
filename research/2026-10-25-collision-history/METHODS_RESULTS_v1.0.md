# C-05 | A scattering clock that remembers the halo's past

**25 October 2026 | v1.0.0 | `DERIVED`, `SIMULATION_RESULT`, `UNIDENTIFIABLE`, `DATA_INSUFFICIENT`**

**Scope:** New-to-this-project worked identifiability gate for **SIMULATED FIXED TRAJECTORIES**, not an observational measurement, SIDM N-body replication, or new astrophysical theory. See [`run.py`](run.py), [`results.json`](results.json), and [`CHECKPOINT.md`](CHECKPOINT.md).

## Physical question

If two dwarf halos have the same present-day local dark-matter density, can we infer how often dark particles scattered during the preceding ten billion years? **No, even when the cross section is constant**, because scattering depends on the density *experienced over time*. Conversely, the same integrated scattering budget can arise from different cross sections and density histories.

**AHA (explanatory, not a discovery):** a particle's collision clock counts the matter it passed *through*, not merely what its halo looks like today. But this collision clock is **not** the gravothermal clock: mergers also carry energy, change orbits and heat-flow gradients. Equal scattering counts do not entail equal density cores or collapse times.

## Prior work, source method and release limits

- Silverman et al., *Mergers Matter: Gravothermal Collapse in Dwarf Halos with Self-Interacting Dark Matter*, [arXiv:2606.02566v1](https://arxiv.org/html/2606.02566v1), **posted 1 June 2026, preprint**. Read sections II.1, III.1–III.2 and V. The GIZMO Monte Carlo pair rate is `Gamma_ij=(sigma/m) m_particle v_rel g_ij`; timestep probability is controlled by `kappa`. Six dark-matter-only dwarf zoom-ins use **70 cm²/g**, and three reach the stated core-collapse threshold before their simulation endpoints. Merger energy transport changes collapse outcomes. Our continuous local-rate approximation is **not** their kernel algorithm.
- Nadler et al., *SIDM Concerto*, [arXiv:2503.10748v2](https://arxiv.org/html/2503.10748v2), **revised 29 September 2025** (initial preprint March 2025). Read section III.2 and source dataset entry. [Zenodo record 14933624 v1](https://zenodo.org/records/14933624), **26 February 2025**, makes catalogs, selected snapshots and parametric predictions available. It explicitly **omits `tree*.dat` files** due size. Its main SIDM models have **velocity-dependent** cross sections and cannot simply use today's constant-sigma example as physical calibration.
- Continuity: main HEAD `b6b85682f0843ae0d097b5f192d90b51b130788d` (14 October), open PRs #4–#9 inspected on 25 October. In particular, C-04 already audited six **censored collapse endpoints**; S-01 already derived **merger projection/inclination** non-identifiability. D-04 already identified exact seasonal **solar/sidereal** aliasing, and the 24 October D-01 PR #9 studied free-phase solar/sidereal nuisance information. This C-05 model instead addresses **collision-exposure versus unknown density history**. The older named 29 September Library archives were sought but were not recovered. C-03's globally unscreened long-range `f(R)` candidate remains `FAILED`, not silently resumed.

No new astronomical exposure or calibrated halo trajectory was retrieved. The two papers are **prior art** for why assembly/merger history matters; no novelty claim is made. Relevant accessible primary coverage was rechecked through 25 October 2026, not an exhaustive literature census.

## One mathematical tool: the likelihood Hessian as local identifiability

Assume a nonrelativistic tracer moving through an **externally imposed** mass-density history `rho(t)` [g/cm³], with constant relative velocity `v` [cm/s] and velocity-independent cross section per dark mass `k=sigma/m` [cm²/g]. In a simplified Poisson-scattering picture the instantaneous interaction rate is

\[
\Gamma(t)=k\,\rho(t)\,v \quad [\mathrm{s}^{-1}],\qquad
\lambda=\int_0^T\Gamma(t)\,dt.
\]

`lambda` is the **dimensionless expected collision count**, not a number of observed detector events. With fixed independent-scattering rates, `P(N>=1)=1-exp(-lambda)`; this probability is *conditional on the toy trajectory*, not a probability of halo collapse.

Let `x=t/T` run from the start (`0`) to present (`1`), and define **SIMULATED** linear density histories

\[
\rho(x;a)=\rho_f[1+a(1-x)],\quad a\ge0,\qquad
\lambda(k,a)=k\rho_f vT(1+a/2).
\]

Both histories have the **same present density** `rho_f`, even if their past differs. The quantity `a` measures how much denser the start was: `a=1` means twice today's density. We are *not* asserting a halo evolves linearly; the imposed histories are counterexamples to endpoint identifiability.

Take `rho_f=0.01 M_sun/pc³ = 6.76810998e-25 g/cm³`, `v=30 km/s`, `T=10 Gyr`, `1 M_sun=1.98847e33 g`, `1 pc=3.0856775814913673e18 cm`, a Julian year `365.25 days`, and `k=1 cm²/g` as a declared **illustration**. The uniform history `A: a=0, k=1` gives `lambda_A=0.6407559229`. Another history `B: a=1, k=2/3 cm²/g` has 50% more integrated mass exposure but the same `lambda_B=0.6407559229` to machine precision. Both give `P(N>=1)=0.4731060`. If B's cross section instead remained `1 cm²/g`, it would give `lambda=0.9611338843`, `P(N>=1)=0.6175410`. These are **SIMULATED MODEL RESULTS**, not halo statistics.

An idealized scalar observation `y=lambda` cannot distinguish the two pairs, even if measured perfectly. To see this locally, use parameters `theta=(ln(k/k_ref), a)` at `k_ref=1 cm²/g`. Its derivative row, or *sensitivity Jacobian*, is

\[
J=\left(\frac{\partial\lambda}{\partial\ln k},\frac{\partial\lambda}{\partial a}\right)=
\left(\lambda,\frac{k\rho_f vT}{2}\right).
\]

If one modeled `y` with **illustrative independent Gaussian uncertainty** `s` in collision-count units, the Hessian of the negative log-likelihood at an exact fit is `F=J^T J/s²` (a 2-by-2 *parameter-curvature* matrix, **not** a gravitational-potential Hessian). Rows and columns correspond to changes in `ln(k/k_ref)` and `a`; at `a=0,k=1`, `J=(0.640756,0.320378)` and `det(F)=0` **for every positive s**. One eigenvalue is exactly zero: there is a locally flat parameter direction. Globally all positive pairs satisfying `k(1+a/2)=constant` are indistinguishable to this scalar statistic.

An additional **independently calibrated history-sensitive statistic** would help. For the same linear toy, the ratio of collision exposure in the first half to the second half is

\[
R_{\rm early/late}=\frac{1+3a/4}{1+a/4},
\]

which is `1` for A and `1.4` for B regardless of `k`. This suggests the *kind* of discriminating observable we need. Such time-resolved collision counts are not currently available from astronomical observation. A validated merger/halo history reconstruction could constrain `a`, but realistic heat-flow modeling must replace the toy before identifying dark-particle physics.

## Falsifier, actual run and stopping rule

**C05-C1 `DERIVED` / known:** fixing final density is insufficient to fix collision exposure for the prescribed histories. The counterexample is explicit; reject it if integration or units are wrong.

**C05-C2 `SIMULATION_RESULT`:** A and B have matched expected counts and Poisson at-least-one probabilities while B at fixed `k` does not. Test by rerunning the single included standard-library Python source and checking the JSON receipt.

**C05-C3 `UNIDENTIFIABLE`:** with only the integrated scalar summary, the two-dimensional `(ln k,a)` parameter map has rank one. An additional genuinely independent history observable changes this conclusion in the declared family; repeating endpoint density does not.

**C05-C4 `DATA_INSUFFICIENT`:** no calibrated `rho(t)`, relative-velocity distribution, halo-specific merger-tree trajectory, full scattering transport, baryonic feedback, observational selection or joint covariance was fitted. The collision count does **not** imply equal gravothermal heat flux. Halo response to changing `k` is frozen out by construction, so the degeneracy does not prove a degeneracy in a self-consistent dynamical solution.

**Exact execution:** single Python-standard-library process in the ChatGPT Linux container under a **20-second hard timeout**, exit `0`, **11/11 predeclared limiting/implementation checks**, strict JSON round-trip. Wall time **1.21 s** reported by `/usr/bin/time`, numerical core **0.00137 s**. Seed `null`, no random draws. Executed `run.py` SHA-256 `9df0d40f07d9b26a8ba9dd1b65289fc1daf4df4d742702ec51c1eb2d302474a3`. Method includes analytic integration and independent midpoint quadrature at 32, 256, 4096 steps; those checks are *not* an N-body reproduction. `results.json` contains the precise floats, generating truth and limitations. A source hash and a numeric receipt do not certify an astrophysical forward model.

**Stop condition:** Do not infer `sigma/m` from an endpoint density or a toy `lambda` without independent merger/assembly calibration and a self-consistent evolution model. Preserve the C-04 censoring rule and halo-level holdouts: snapshots from one initial condition are correlated, not independent systems.

## The next discriminating step

**Recommended:** inspect the *small public SIDM Concerto parametric products and catalog schema* without assuming the omitted `tree*.dat` files exist. Test whether a **separate halo-level** history indicator can be measured and checked for predictive improvement on held-out halo initial conditions. **Acceptance:** a matched-CDM/SIDM baseline plus a truly independent history covariate improves held-out density/profile predictions beyond observational/selection uncertainty; **failure:** missing trajectories, non-identifiable nuisances, calibration failures or no improvement. No large Zenodo file was downloaded in this run.

Other possible branches (not executed): calibrate the half-epoch density exposure against simulation time series if legally available, or test how velocity-dependent `sigma(v)` invalidates a single scalar collision-clock parametrization. Neither is established here.
