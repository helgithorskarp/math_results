#!/usr/bin/env python3
"""Unit tests including malformed input and corrupted-certificate rejection."""
from __future__ import annotations

import json
import unittest
from unittest.mock import patch

import direct
import layers
import verify


class Checks(unittest.TestCase):
    def test_known_gaussian_and_lucas_values(self):
        self.assertEqual(layers.gaussian(4,2), (1,1,2,1,1))
        self.assertEqual(direct.lucas(4), (1,5,5,1))

    def test_boundary_two_algorithms(self):
        report, actual = verify.audit_boundary()
        self.assertEqual(report["cases"], 6)
        self.assertEqual(len(actual), 6)

    def test_structural_audits(self):
        self.assertLessEqual(verify.audit_partition_map()["maximum_fibre"], 2)
        self.assertEqual(verify.audit_rectangle_decomposition()["identities"], 3280)
        self.assertGreater(verify.audit_kernel()["threefold_coefficients"], 1000)

    def test_rational_budget(self):
        self.assertEqual(layers.tail_budget()["uniform_margin"], "1/6")

    def test_regression_independence(self):
        self.assertEqual(verify.audit_regressions()["cases"], 463)

    def test_invalid_parameters(self):
        for args in ((0,2,2),(2,2,3),(3,4,5),(1.0,2,2)):
            with self.assertRaises(ValueError):
                layers.parameters(*args)
            with self.assertRaises(ValueError):
                direct.validate(*args)

    def test_nonexact_division_rejected(self):
        with self.assertRaises(ArithmeticError):
            direct.divide_exact((1,0,1), (1,1))

    def test_corrupted_boundary_rejected(self):
        good = json.loads((verify.HERE / "BOUNDARY.json").read_text())
        bad = json.loads(json.dumps(good))
        bad[0]["margin_coefficients"][0] += 1
        with patch("verify.json.loads", side_effect=[bad]):
            with self.assertRaises(ArithmeticError):
                verify.audit_boundary()


if __name__ == "__main__":
    unittest.main()
