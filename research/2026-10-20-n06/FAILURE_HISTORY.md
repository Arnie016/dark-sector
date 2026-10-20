# Failure retained

The first bounded N-06 execution finished the numerical core but raised \`AssertionError: strict_json_roundtrip\` because the saved check count was mistakenly compared against \`len(checks)-1\`. This was bookkeeping, not a physics discrepancy. The assertion was corrected to \`len(checks)\` and the same deterministic model rerun; all 14 implementation/readback checks passed. The corrected code and receipt are the only publishable version. An automated numerical audit is not independent peer review.
