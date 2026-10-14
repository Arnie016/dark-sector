# Methods | from equations to reproducible tests

Every code-bearing research study should supply:

1. **Question and claim ID.** What single prediction is being tested?
2. **Generating truth / input origin.** Public observations, authors' data or explicitly **SIMULATED** inputs.
3. **Dimensions and units.** Coordinate definitions, axes, energies, times, distances and normalization.
4. **Exact dependencies.** Versions, immutable URLs/commit hashes, licenses and dataset splits.
5. **Reproduction command.** Single bounded CPU script or notebook with seed, runtime/worker ceiling and expected artifact names.
6. **Independent checks.** Analytic limiting cases, alternative implementation or baseline, covariance and nuisance identifiability.
7. **Failure ledger.** Exceptions, data gaps, rejected hypotheses and scope of any null result.
8. **What was not done.** No inference about observed physics when only an identity or simulation was checked.

### Minimal machine-readable manifest (example schema, not a run receipt)

```yaml
claim_id: DS-H02
status: DATA_INSUFFICIENT
data_type: SIMULATED # or OBSERVED
source_files: []
code_commit: null
seed: null
inputs_with_units: {}
command: null
environment: null
checks: []
failures: []
result_summary: "No validated experiment recorded in this template."
```

**Inference guardrails:** account for repeated looks, correlated samples and the model-selection process. Split halo simulation validation by independent initial condition, not adjacent snapshots. A symmetry-allowed response is not proof of a nonzero microscopic amplitude. An algebraic identity is not a reproduced likelihood.

Mathematical derivations should be readable in GitHub Markdown using LaTeX; formal Lean proofs must include toolchain pinning, the exact theorem, kernel run and axiom report. A draft containing `sorry` is not a verified theorem.
