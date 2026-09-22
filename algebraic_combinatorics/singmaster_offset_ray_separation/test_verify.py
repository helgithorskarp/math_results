#!/usr/bin/env python3
"""Boundary and mutation tests for verify.py."""

from __future__ import annotations

import unittest
from fractions import Fraction

from verify import audit_ray, audit_value_sequence, factorial_ratio, ray_values


class RayTests(unittest.TestCase):
    def test_invalid_parameters(self) -> None:
        for args in ((3, 1, 0, 1), (3, 1, 1, 0), (1, 2, 1, 1)):
            with self.assertRaises(ValueError):
                ray_values(*args)

    def test_singleton_ray(self) -> None:
        self.assertEqual(ray_values(7, 6, 1, 1), [7])
        self.assertEqual(audit_ray(7, 6, 1, 1), (0, 0, 0))

    def test_ratio_formula(self) -> None:
        values = ray_values(31, 4, 3, 2)
        for r in range(len(values) - 1):
            self.assertEqual(factorial_ratio(31, 4, 3, 2, r),
                             Fraction(values[r + 1], values[r]))

    def test_strictness(self) -> None:
        values = ray_values(42, 3, 4, 3)
        self.assertTrue(all(values[r] * values[r] > values[r - 1] * values[r + 1]
                            for r in range(1, len(values) - 1)))

    def test_3003_sign_pattern(self) -> None:
        values = ray_values(15, 5, 1, 1)
        self.assertEqual(values[:2], [3003, 3003])
        self.assertTrue(all(value < 3003 for value in values[2:]))

    def test_reject_flat_mutation(self) -> None:
        # Repeating one term creates a forbidden threefold level/flat ratio.
        values = ray_values(24, 2, 2, 3)
        mutated = [values[0], values[0], values[0], *values[3:]]
        with self.assertRaises(AssertionError):
            audit_value_sequence(mutated)


if __name__ == "__main__":
    unittest.main()
