#!/usr/bin/env python3
"""Small exact regression cases for the generic square-membership oracle."""

from __future__ import annotations

import unittest
from fractions import Fraction

from independent_boundary_check import generic_square_in_k
import common


ZERO_TAIL = (Fraction(0),) * 7


class BoundaryTests(unittest.TestCase):
    def test_rational_square_with_radical_root(self):
        self.assertTrue(generic_square_in_k((Fraction(3),) + ZERO_TAIL))

    def test_rational_nonsquare_outside_k(self):
        self.assertFalse(generic_square_in_k((Fraction(2),) + ZERO_TAIL))

    def test_nontrivial_field_square(self):
        element = (Fraction(2), Fraction(1), Fraction(-1, 3)) + (Fraction(0),) * 5
        self.assertTrue(generic_square_in_k(common.f_sq(element)))


if __name__ == "__main__":
    unittest.main()
