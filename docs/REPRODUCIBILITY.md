# Reproducibility guide

## Included and runnable

The new ratio audit runs offline once NumPy is installed. Use Python 3.11+ with `numpy==2.4.3`; the run receipt records the actual interpreter. This is a numeric/table audit, not observational lensing reproduction.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python experiments/ratio_closure/run.py --output /tmp/dark-sector-ratio-audit.json
python experiments/ratio_closure/run.py --check
```

The last command recalculates results and compares them to the committed output: numeric tolerance $10^{-10}$, identical inputs/code hashes. It exits nonzero on mismatch without overwriting the reference. Inputs use the same flux convention as Table 2. No randomness or seed is needed. `--output` writes a result only when explicitly requested.

Tests cover rank/null normalization, displayed-precision closure, covariance positive semidefiniteness/rank, shared-flux correlations, global rescaling, and invalid/changed inputs. Display agreement uses half a unit at the published decimal place, not a statistical confidence interval.

## What the output proves

- Same-flux exact log contrasts have rank three.
- Reconstructed rounded central ratios agree at displayed precision.
- An assumed independent 0.03 log-flux standard deviation induces correlated, singular ratio covariance.

It does not verify a spectral posterior, a physical halo model, a measured covariance, or any author's Bayes factor. The original six-check script is not recovered; this implementation has its own independent tests.

## External baseline still pending

For neutrinos, start from [SkyLLH's versioned tutorial index](https://icecube.github.io/skyllh/v26.1.0/html/tutorials/index.html). Pin the software and explicit `IceTracks-DR2-v2` input. Record actual hashes, configuration, expected published output, tolerances, and differences before running. The public tutorial results belong to IceCube. No real-event baseline or data-host availability check ran during this setup.

For lensing, recover joint flux samples, source-size/offset assumptions, host posterior, and independent constraints. Do not multiply six independent likelihoods using only marginal errors. Record licensing and retrieval provenance before adding any larger data product.

## Recovered archives

All previous executable archive claims remain pending; see [inventory](RECOVERY.md). A newly rebuilt toy script must have a new run ID and label. Do not relabel it as recovery of an old result.
