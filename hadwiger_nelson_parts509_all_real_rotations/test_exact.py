#!/usr/bin/env python3
"""Fast boundary tests for exact arithmetic and certificate serialization."""

from __future__ import annotations

import unittest
from fractions import Fraction

from common import ONE, ZERO, f_add, f_inv, f_mul, f_sign, line_digest, pack_coloring, unpack_coloring
from verify import mq_mul, mq_sqrt


class ExactTests(unittest.TestCase):
    def test_sign_bounds(self):
        sqrt3_minus_17_over_10 = (Fraction(-17, 10), Fraction(1)) + (Fraction(0),) * 6
        self.assertEqual(f_sign(sqrt3_minus_17_over_10), 1)
        self.assertEqual(f_sign(tuple(-x for x in sqrt3_minus_17_over_10)), -1)
        self.assertEqual(f_sign(ZERO), 0)

    def test_field_inverse(self):
        value = (Fraction(2), Fraction(1), Fraction(-1, 3)) + (Fraction(0),) * 5
        self.assertEqual(f_mul(value, f_inv(value)), ONE)

    def test_recursive_square_membership(self):
        value = (Fraction(2), Fraction(1), Fraction(-1, 3)) + (Fraction(0),) * 5
        square = mq_mul(value, value)
        root = mq_sqrt(square)
        self.assertIsNotNone(root)
        self.assertEqual(mq_mul(root, root), square)
        self.assertIsNone(mq_sqrt((Fraction(2),) + (Fraction(0),) * 7))

    def test_coloring_round_trip(self):
        colors = [index % 4 for index in range(509)]
        self.assertEqual(unpack_coloring(pack_coloring(colors)), colors)

    def test_line_digest_order_independent(self):
        key1 = (ONE, ZERO, ONE)
        key2 = (ZERO, ONE, ONE)
        self.assertEqual(line_digest([key1, key2]), line_digest([key2, key1]))
        self.assertNotEqual(line_digest([key1]), line_digest([key2]))


if __name__ == "__main__":
    unittest.main()
