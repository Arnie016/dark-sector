# C-05 | Research and learning checkpoint

**As of 2026-10-25 | v1.0.0 | independent run, not an external reproduction**

## Research state

- `C05-C1 DERIVED`: for fixed `v`, `sigma/m`, and synthetic prescribed history, expected event count equals `(sigma/m)∫rho(t)vdt`; present-day density does not fix this integral. A and B share the endpoint but not the underlying collision exposure.
- `C05-C2 SIMULATION_RESULT`: A (`a=0,k=1`) and B (`a=1,k=2/3`) have equal `lambda=0.640755922891` with `P(N>=1)=0.473106017756`; same `k` in B gives `lambda=0.961133884337`. SIMULATED imposed histories only. Executed source SHA-256 `9df0d40f07d9b26a8ba9dd1b65289fc1daf4df4d742702ec51c1eb2d302474a3`; 11/11 checks, exit 0, 20s timeout, seed null.
- `C05-C3 UNIDENTIFIABLE`: a single integrated count has rank-one sensitivity in `(ln k,a)`, despite fixed final density; early/late ratio would differentiate these histories if independently available.
- `C05-C4 DATA_INSUFFICIENT`: no actual simulation tracks, scattering/heat response or observed density-history likelihood; no particle detection. A collision count is *not* a collapse-time estimator. Need CDM/SIDM matched halo initial conditions, trajectory provenance, velocity dependence, covariance and selection rules.
- State preserved: main `b6b8568` (14 Oct) with open PRs #4-#9 at inspection; D-01 dated 24 Oct remains an unmerged simulated nuisance-identifiability study. C-04 censored-collapse endpoint limitation and C-03 `FAILED` unscreened-gravity candidate preserved. Existing Sept archives searched in Files by name, not recovered. Prior N-06/07/08/09 neutrino tests remain separate and are not reproduced here.
- Primary inputs checked on 25 Oct: Mergers Matter arXiv:2606.02566v1 (2026-06-01) sections II, III and V; SIDM Concerto arXiv:2503.10748v2 (2025-09-29) §III.2; Zenodo 14933624 v1 (2025-02-26), missing large tree*.dat confirmed. None was used as numerical observational input.

## Learning state

- **Newly introduced, NOT_ASSESSED:** scattering rate and collision optical depth, units of `(sigma/m)∫rho vdt`, fixed-trajectory versus self-consistent gravothermal dynamics, likelihood-Hessian rank deficiency and history-shape discriminator.
- **Demonstrated user understanding:** none observed in this run. Do not promote introduced concepts to mastered.
- Optional self-check with available answer: does observing the same `rho(T)` force equal scattering histories? **No.** A and B have the same final density but have `∫rho dt` in ratio `1:1.5`; matching `lambda` requires adjusting `sigma/m` by `1:2/3`.

## Next gate

Inspect public low-volume SIDM Concerto prediction products and read file schemas/licenses, then test a one-halo-per-group held-out baseline with declared calibration and selection. Do not treat snapshots of one halo as multiple independent cases. If the requisite histories cannot be reconstructed, mark `DATA_INSUFFICIENT`, rather than manufacture a particle cross-section constraint.
