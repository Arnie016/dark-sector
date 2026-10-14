"""New offline summary-table audit; not the recovered ChatGPT script or a lens fit."""

import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data/published/rxj1131_narrow_line.csv"
REFERENCE = Path(__file__).with_name("results.json")
PAIRS = [("B", "A"), ("C", "A"), ("C", "B"),
         ("D", "A"), ("D", "B"), ("D", "C")]
IMAGES = ["A", "B", "C", "D"]
RANK_TOLERANCE = 1e-12


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_rows(path=INPUT):
    with path.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    if len(rows) != 6:
        raise ValueError("Expected exactly six published rows")
    for row, (num, den) in zip(rows, PAIRS):
        if (row["ratio"], row["numerator"], row["denominator"]) != (f"{num}/{den}", num, den):
            raise ValueError("Unexpected ratio direction or row order")
        row["value"] = float(row["value"])
        row["marginal_error"] = float(row["marginal_error"])
        row["display_decimals"] = int(row["display_decimals"])
        if not all(np.isfinite(row[k]) and row[k] > 0 for k in ("value", "marginal_error")):
            raise ValueError("Flux ratios and marginal errors must be positive and finite")
        if not 0 <= row["display_decimals"] <= 12:
            raise ValueError("Invalid displayed precision")
    return rows


def incidence_matrix():
    matrix = np.zeros((6, 4))
    for row, (num, den) in enumerate(PAIRS):
        matrix[row, IMAGES.index(num)] = 1
        matrix[row, IMAGES.index(den)] = -1
    return matrix


def contrasts(flux):
    flux = np.asarray(flux, dtype=float)
    if flux.shape != (4,) or not np.all(np.isfinite(flux)) or np.any(flux <= 0):
        raise ValueError("Four positive finite fluxes required")
    return incidence_matrix() @ np.log(flux)


def calculate(rows=None):
    rows = load_rows() if rows is None else rows
    by_ratio = {r["ratio"]: r["value"] for r in rows}
    flux = np.array([1, by_ratio["B/A"], by_ratio["C/A"], by_ratio["D/A"]])
    matrix = incidence_matrix()
    reconstructed = np.exp(contrasts(flux))
    closure = []
    for row, value in zip(rows, reconstructed):
        tolerance = 0.5 * 10 ** (-row["display_decimals"])
        residual = float(value - row["value"])
        closure.append({"ratio": row["ratio"], "published": row["value"],
                        "reconstructed": float(value), "residual": residual,
                        "display_tolerance": tolerance,
                        "agrees_at_display_precision": abs(residual) <= tolerance + 1e-12})
    # This assumption is intentionally independent of the table's marginal errors.
    assumed_log_flux_sd = 0.03
    covariance = matrix @ (assumed_log_flux_sd ** 2 * np.eye(4)) @ matrix.T
    sd = np.sqrt(np.diag(covariance))
    correlation = covariance / np.outer(sd, sd)
    return {
        "run_id": "2026-10-14-ratio-closure-new-implementation-v1",
        "input_kind": "PUBLISHED_ROUNDED_SUMMARY",
        "covariance_kind": "ILLUSTRATIVE_NOT_MEASURED",
        "source": "https://arxiv.org/html/2606.23808v1#S4.T2",
        "row_order": [r["ratio"] for r in rows],
        "incidence_matrix": matrix.tolist(),
        "matrix_rank": int(np.linalg.matrix_rank(matrix, tol=RANK_TOLERANCE)),
        "normalization_null_residual": float(np.max(np.abs(matrix @ np.ones(4)))),
        "closure": closure,
        "illustrative_log_flux_sd": assumed_log_flux_sd,
        "illustrative_log_ratio_covariance": covariance.tolist(),
        "illustrative_log_ratio_correlation": correlation.tolist(),
        "illustrative_covariance_rank": int(np.linalg.matrix_rank(covariance, tol=RANK_TOLERANCE)),
        "rank_tolerance": RANK_TOLERANCE,
        "seed": None,
        "observational_likelihood_reproduced": False,
        "sha256": {str(path.relative_to(ROOT)): sha256(path) for path in
                   (INPUT, Path(__file__).resolve(), ROOT / "requirements.txt")},
    }


def equivalent(actual, expected):
    """Strict shape/metadata comparison with portable floating point tolerance."""
    if isinstance(actual, dict) and isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(equivalent(actual[k], expected[k]) for k in actual)
    if isinstance(actual, list) and isinstance(expected, list):
        return len(actual) == len(expected) and all(equivalent(a, b) for a, b in zip(actual, expected))
    if type(actual) is not type(expected):
        return False
    if isinstance(actual, float):
        return bool(np.isclose(actual, expected, rtol=1e-10, atol=1e-10))
    return actual == expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--output", type=Path, help="Write new audit output to this path")
    group.add_argument("--check", action="store_true", help="Compare with committed reference without writing")
    args = parser.parse_args()
    result = calculate()
    if not all(r["agrees_at_display_precision"] for r in result["closure"]):
        raise SystemExit("FAIL: rounded central-value closure outside displayed precision")
    if args.check:
        if not equivalent(result, json.loads(REFERENCE.read_text())):
            raise SystemExit("FAIL: recalculation differs from committed reference")
        print("PASS: committed audit matches recalculation; observational inference not reproduced")
    elif args.output:
        args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
        print(f"Wrote summary-table audit: {args.output}")
    else:
        print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
