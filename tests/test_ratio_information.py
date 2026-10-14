import copy
import csv
import importlib.util
from pathlib import Path
import tempfile
import unittest

import numpy as np

SCRIPT = Path(__file__).resolve().parents[1] / "experiments/ratio_closure/run.py"
spec = importlib.util.spec_from_file_location("ratio_audit", SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class RatioInformationTests(unittest.TestCase):
    def test_rank_and_independent_reference_basis(self):
        b = audit.incidence_matrix()
        self.assertEqual(np.linalg.matrix_rank(b), 3)
        self.assertEqual(np.linalg.matrix_rank(b[[0, 1, 3]]), 3)
        np.testing.assert_array_equal(b[2], b[1] - b[0])
        np.testing.assert_array_equal(b[4], b[3] - b[0])
        np.testing.assert_array_equal(b[5], b[3] - b[1])

    def test_common_normalization_is_invisible(self):
        f = np.array([2.3, 0.87, 1.2, 0.06])
        np.testing.assert_allclose(audit.contrasts(f), audit.contrasts(f * 123), atol=1e-12)

    def test_published_closure_at_display_precision(self):
        result = audit.calculate()
        self.assertTrue(all(r["agrees_at_display_precision"] for r in result["closure"]))
        values = {r["ratio"]: r["reconstructed"] for r in result["closure"]}
        self.assertAlmostEqual(values["C/B"], 7 / 9)
        self.assertAlmostEqual(values["D/B"], 7 / 45)
        self.assertAlmostEqual(values["D/C"], 1 / 5)

    def test_changed_ratio_fails_closure(self):
        rows = copy.deepcopy(audit.load_rows())
        rows[2]["value"] = 0.9
        self.assertFalse(audit.calculate(rows)["closure"][2]["agrees_at_display_precision"])

    def test_covariance_is_singular_positive_semidefinite(self):
        cov = np.array(audit.calculate()["illustrative_log_ratio_covariance"])
        np.testing.assert_allclose(cov, cov.T)
        self.assertEqual(np.linalg.matrix_rank(cov, tol=1e-12), 3)
        self.assertGreaterEqual(np.linalg.eigvalsh(cov).min(), -1e-12)

    def test_shared_and_disjoint_flux_correlations(self):
        corr = np.array(audit.calculate()["illustrative_log_ratio_correlation"])
        self.assertAlmostEqual(corr[0, 1], 0.5)  # shared denominator A
        self.assertAlmostEqual(corr[0, 2], -0.5)  # B enters with opposite signs
        self.assertAlmostEqual(corr[0, 5], 0)  # disjoint images

    def test_invalid_flux_is_rejected(self):
        for f in ([1, 0, 2, 3], [1, -1, 2, 3], [1, np.nan, 2, 3], [1, 2]):
            with self.assertRaises(ValueError):
                audit.contrasts(f)

    def test_csv_direction_and_positive_values_are_checked(self):
        with audit.INPUT.open() as source:
            raw = list(csv.DictReader(source))
        for key, value in (("value", "nan"), ("marginal_error", "-1"), ("numerator", "A")):
            rows = copy.deepcopy(raw)
            rows[0][key] = value
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "input.csv"
                with path.open("w", newline="") as target:
                    writer = csv.DictWriter(target, fieldnames=raw[0].keys())
                    writer.writeheader()
                    writer.writerows(rows)
                with self.assertRaises(ValueError):
                    audit.load_rows(path)

    def test_reference_comparison_detects_changed_provenance(self):
        result = audit.calculate()
        changed = copy.deepcopy(result)
        changed["covariance_kind"] = "MEASURED"
        self.assertFalse(audit.equivalent(result, changed))
        changed = copy.deepcopy(result)
        changed["sha256"] = {}
        self.assertFalse(audit.equivalent(result, changed))


if __name__ == "__main__":
    unittest.main()
