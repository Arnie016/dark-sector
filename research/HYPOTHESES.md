# Hypothesis tracker

IDs remain stable. Append dated evidence and change state explicitly; do not silently erase failed predictions.

| ID | Question | State | Next decisive test |
| --- | --- | --- | --- |
| L-01 | Does a compact halo predict independent lens observables better than a flexible host? | `DATA_INSUFFICIENT` | Fit joint flux/host posteriors; evaluate independent positions/arcs |
| L-02 | Does concentration-conditioned collapse matter after assembly history is included? | `HISTORICAL_REPORTED` | Recover code; test physically calibrated histories on held-out systems |
| S-01 | Do six same-flux log ratios supply six independent constraints? | `REJECTED` for exact same-flux construction | Rank-three result checked locally; revisit only if measurement definitions differ |
| N-01 | Can unmatched counts distinguish catalog loss from attenuation? | `CONDITIONAL` | Validate baseline; constrain background/source freedom |
| N-02 | Can coordinate/covariance errors mimic or miscalibrate structure? | `HISTORICAL_REPORTED` for toy simulations | Recover code; compare actual response kernels on identical inputs |
| D-01 | Can solar/sidereal modulation separate a directional dark-sector signal? | `NOT_EVALUATED` | Recover methods and material-specific response |

## L-01 · test conventional explanations

**Prediction:** a spatially varying halo improves held-out predictions. **Alternatives:** macro-lens complexity, source offsets/sizes, globular clusters, covariance, selection. **Reject or weaken:** predictive improvement disappears after those uncertainties are marginalized. An anomaly alone does not identify SIDM; Bayes factors depend on priors and models.

## L-02 · selection is not collapse history

**Prediction:** concentration adds held-out predictive value after assembly information. **Alternative:** merger-driven heat transport makes concentration selection misleading. **Reject:** selected and random-collapse predictions become indistinguishable under calibrated host/source uncertainty. The reported 500,000-halo population is synthetic.

## N-01 · nuisance freedom controls identifiability

**Prediction:** calibrated responses and independently constrained backgrounds separate catalog loss from attenuation in a specified model. **Alternatives:** background, source normalization/spectrum, galaxy selection. **Reject or weaken:** realistic uncertainty restores degeneracy. Idealized on/off controls are not automatically equivalent to real right-ascension scrambling.

## Evidence history

- **2026-10-14:** tracker initialized from recovered memos; S-01 audited locally. Other numerical tests remain historical reports, not new executions. See [checkpoints](checkpoints/README.md) and [sources](../docs/SOURCES.md).
