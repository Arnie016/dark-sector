"""D-02: published DAMIC-M six-pattern fixed-background audit, NOT a DM fit.
Inputs: arXiv:2607.09352v1 Eqs. 2, 5, 7. Python stdlib only.
"""
import json
import math
import hashlib
from pathlib import Path

labels = ("11", "21", "111", "31", "22", "211")
observed = (144, 0, 0, 1, 0, 0)
accidental = (141.4, .111, .042, .019, .000025, .000058)
radiogenic = (.039, .039, .016, .052, .011, .035)
background = tuple(a + b for a, b in zip(accidental, radiogenic))
rare_background = sum(background[1:])
rare_count = sum(observed[1:])


def cdf_le_one(x):
    return (1 + x) * math.exp(-x)


def deviance(data, mean):
    return 2 * sum(m - n + (n * math.log(n / m) if n else 0)
                   for n, m in zip(data, mean))


lo, hi = 0., 20.
for _ in range(80):
    mid = (lo + hi) / 2
    if cdf_le_one(rare_background + mid) > 0.1:
        lo = mid
    else:
        hi = mid
limit = (lo + hi) / 2
checks = {
    "six_unique_channels": len(set(labels)) == 6,
    "valid_counts": all(isinstance(n, int) and n >= 0 for n in observed),
    "positive_means": all(x > 0 for x in background),
    "one_rare_event": rare_count == 1,
    "exact_bound_root": abs(cdf_le_one(rare_background + limit) - .1) < 1e-13,
    "pattern_probabilities_sum_one": abs(sum(x / rare_background for x in background[1:]) - 1) < 1e-12,
}
assert all(checks.values())
result = {
    "id": "D-02", "as_of": "2026-10-17",
    "status": ["DERIVED", "DATA_INSUFFICIENT"],
    "source": "https://arxiv.org/html/2607.09352v1", "kind": "PUBLISHED summary counts, fixed nominal background",
    "labels": labels, "observed": observed, "accidental": accidental,
    "radiogenic": radiogenic, "background": background,
    "all_observed": sum(observed), "all_background": sum(background),
    "rare_observed": rare_count, "rare_background": rare_background,
    "p_31_at_least_one": -math.expm1(-background[3]),
    "p_any_rare_at_least_one": -math.expm1(-rare_background),
    "p_31_given_one_rare": background[3] / rare_background,
    "p_exactly_one_rare": rare_background * math.exp(-rare_background),
    "one_sided_90pct_extra_count_bound_fixed_background": limit,
    "six_channel_deviance_no_p_value": deviance(observed, background),
    "checks": checks, "seed": None, "random_draws": 0,
    "not_claimed": ["collaboration likelihood reproduction", "DM cross-section bound", "detection significance", "independent new experimental dataset"],
    "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
path = Path(__file__).with_name("results.json")
path.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
assert json.loads(path.read_text())["rare_observed"] == 1
print(json.dumps(result, indent=2))
