# C-09 | Published cluster-distance covariance gate

**28 October 2026, v1.0 | DERIVED, SOURCE_CORRECTION, DATA_INSUFFICIENT.** A bounded audit of **OBSERVED AS REPORTED**, rounded published marginal separations from Jee, Park & Lee, Table 2. No new observations, synthetic measurements, dark-matter constraint, or full-likelihood reproduction.

## Physical question

After C-08 established a conditional projection-calibration ambiguity in a **SIMULATED toy**, which missing statistical input is worth prioritizing? Here we isolate one precise issue: the unknown **within-cluster correlation** between two reported distances. This is not the simulation projection uncertainty shared across the eleven clusters.

## Source correction

Jee, Park & Lee, *A New Robust Constraint on the Self-interaction Cross Section of Dark Matter with Double Radio Relic Clusters*, was **published and peer reviewed** in *The Astrophysical Journal* **1007(1), 56, 10 August 2026**, DOI [10.3847/1538-4357/ae88fb](https://doi.org/10.3847/1538-4357/ae88fb), as shown by the [Yonsei University institutional record](https://yonsei.elsevierpure.com/en/publications/a-new-robust-constraint-on-the-self-interaction-cross-section-of-/). Earlier C-06/C-08 prose characterized it as a preprint without acknowledging the journal publication. Methods and data used here were inspected in accessible [arXiv:2605.00093 text](https://arxiv.org/abs/2605.00093), first submitted 30 April 2026. The exact latest arXiv revision and published-version differences were not independently audited.

The authors report 11 older observed clusters and a **model-conditional 68% upper limit of 0.22 cm²/g**. Neither those observations nor the published likelihood was independently reproduced here.

## Worked mathematical tool: a covariance matrix

Let `S` be reported shock separation [Mpc] and `H` reported halo separation [Mpc]. The dimensionless ratio is `Q=H/S`; `z=ln(Q)`. In `(S,H)` order the gradient is `g=(-1/S, 1/H)`. Write `a=sigma_S/S` and `b=sigma_H/H`, using the published marginal standard deviations. An unknown within-cluster correlation `rho` gives

```text
Sigma = [[sigma_S^2, rho*sigma_S*sigma_H],
         [rho*sigma_S*sigma_H, sigma_H^2]]
Var[ln(Q)] ≈ g^T Sigma g = a^2 + b^2 - 2 rho a b.
```

Therefore the **first-order fractional uncertainty** is bounded by `|b-a| <= sd[ln(Q)] <= a+b` for `-1<=rho<=1`. This is an analytic error-propagation identity, not an estimated covariance or a physical-potential Hessian. The `rho=±1` endpoints are limiting singular covariance matrices.

## Calculation using published rounded Table 2

| Cluster (OBSERVED AS REPORTED) | Q=H/S | Relative 1-sigma at rho=+1 | rho=0 | rho=-1 |
|---|---:|---:|---:|---:|
| MACS J1752.0+4440 | 0.5667 | 4.93% | 5.96% | 6.83% |
| PSZ2 G181.06+48.47 | 0.1852 | 23.26% | 24.01% | 24.74% |

For all 11 table entries, the **median increase in the possible uncertainty upper bound versus rho=0 is 6.28% of the error bar**, with maximum 14.70% for MACS J1752.0+4440. This is *not* a 14.70% change in the observed distance ratio, the SIDM posterior or its upper limit.

All 11 shock-distance fractional errors are at most 1.24%, whereas the smallest halo-distance fractional error is 5.88%. Thus under this **one-cluster, first-order log-ratio approximation** the marginal halo error dominates the within-cluster covariance contribution. ZWCL1447.2+2619 has 41.67% relative halo error, where this linearized approximation is especially weak. Do not interpret these envelopes as exact credible intervals.

One deterministic **ChatGPT Linux** standard-library Python process executed under a **20-second hard timeout**, exit 0, 8/8 finite implementation/limiting checks; seed null. No external wall time was measured. The complete executed source and raw result are in the ChatGPT C-09 companion, rather than uploaded by this compact GitHub note. Source SHA256 `b2b8cb412160888f19978eb66744ed9a54676c48ededcf175c505ba3a1198025`; raw JSON SHA256 `fbe0578462f5c996622ddd72588fa159235122fab56e8fece2b7d358c69e57a0`.

## Exact scope and next falsifier

**C09-C1 DERIVED:** The covariance envelope follows from the gradient and the two printed marginal errors under the linear expansion.

**C09-C2 SOURCE_CORRECTION:** The paper has an August peer-reviewed publication, so previous preprint-only attribution was incomplete.

**C09-C3 DATA_INSUFFICIENT:** We have not obtained correlated per-system lensing/radio likelihood products, the numerical merger emulator, shared projection-calibration covariance, sample selection or simulation-track holdouts. The authors' actual calculation fits the distances plus nuisance priors, **not merely the ratio**, so these diagnostic envelopes do not reproduce their 68% limit. The strongest competing possibility is a *shared projection or forward-model systematic across clusters*, which this calculation does not bound.

**Stop condition:** do not infer an SIDM cross-section from the ratio-envelope calculation. **Next discriminating step:** obtain joint separation/lensing covariance and projection-calibration residuals, then test whether shared simulation error is more important than the bounded within-cluster covariance effect using independent matched halos, not adjacent snapshots.

**AHA (explanation, not discovery):** an unknown covariance is not automatically the dominant uncertainty. Its effect depends on the marginal errors being linked. An unmeasured, shared simulation bias is a different problem.

**Research continuity:** C-06 turnaround null, C-07 fixed-projection correction, C-08 free-projection degeneracy, C-05 halo-history ambiguity and C-03 FAILED unscreened gravity remain recorded. **Learning:** gradients and covariance introduced, demonstrated understanding **NOT_ASSESSED**. No CI, independent review, outreach or scholarly submission is claimed here.
