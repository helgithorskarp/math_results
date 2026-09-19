#!/usr/bin/env python3
"""Fast regression tests for the gap-217 finite and rational reductions."""

from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent


def load(name):
    path = HERE / name
    spec = spec_from_file_location(f"gap217_test_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


verify = load("verify.py")
independent = load("independent_check.py")


class Gap217Tests(unittest.TestCase):
    def test_complete_cutoff(self):
        self.assertEqual((216 + 3 * 24) // 17, 16)
        self.assertEqual(17 * 17 - 3 * 24, 217)

    def test_frontier_totals(self):
        totals = [row[0] for row in verify.FRONTIER_SURVIVORS]
        self.assertEqual(totals, [203, 205, 208] + [210] * 8 + [215])
        self.assertEqual(independent.FRONTIER_SURVIVORS, verify.FRONTIER_SURVIVORS)

    def test_frontier_placement_counts(self):
        expected = {
            key: (row["profiles"], row["cases"])
            for key, row in verify.EXPECTED_FRONTIER_RESIDUALS.items()
        }
        self.assertEqual(expected, independent.EXPECTED_FRONTIER_CASES)
        self.assertEqual(sum(cases for _, cases in expected.values()), 28_470)

    def test_local_to_global_arithmetic(self):
        ratio = Fraction(12 * 56 + 217, 34 * 56)
        self.assertEqual(ratio, Fraction(127, 272))
        self.assertEqual(ratio / 12, Fraction(127, 3264))
        self.assertEqual(3264 - 127, 3137)
        self.assertEqual(7 * 3264 // 2, 11_424)

    def test_strengthened_bound(self):
        new = Fraction(5712, 3137)
        old = Fraction(4998, 2747)
        self.assertEqual(new - old, Fraction(12138, 8617339))
        self.assertGreater(new, old)
        self.assertEqual(verify.integer_bound(11), 3007)

    def test_equality_profile_correction_is_inherited(self):
        self.assertEqual(verify.P0, (0, 17, 0, 1))
        self.assertEqual(independent.P0, verify.P0)


if __name__ == "__main__":
    unittest.main()
