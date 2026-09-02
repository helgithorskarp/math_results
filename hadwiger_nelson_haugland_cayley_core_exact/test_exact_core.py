#!/usr/bin/env python3
"""Small rejection and algebra tests for the exact Cayley-core certificate."""

from __future__ import annotations

import copy
import unittest

from exact_cayley_core import SPECIALIZATIONS, evaluate_element, verify_result
from exact_field import ONE, ZERO, field_constants, point_add, squared_norm


class ExactCoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sqrt3, cls.vectors = field_constants()

    def test_unit_vectors_and_antipodes(self) -> None:
        self.assertEqual(len(set(self.vectors)), 84)
        for index, vector in enumerate(self.vectors):
            self.assertEqual(squared_norm(vector), ONE)
            self.assertEqual(point_add(vector, self.vectors[(index + 42) % 84]), (ZERO, ZERO))

    def test_two_step_endpoint_walk(self) -> None:
        target = (ZERO, self.sqrt3)
        self.assertEqual(
            point_add(point_add(target, self.vectors[56]), self.vectors[70]),
            (ZERO, ZERO),
        )

    def test_modular_sieve_keeps_exact_unit_vectors(self) -> None:
        for prime, zeta_image in SPECIALIZATIONS:
            for x, y in self.vectors:
                x_image = evaluate_element(x, prime, zeta_image)
                y_image = evaluate_element(y, prime, zeta_image)
                self.assertEqual((x_image * x_image + y_image * y_image) % prime, 1)

    def test_certificate_comparison_rejects_mutation(self) -> None:
        actual = {"T6": {"vertices": 12856}}
        verify_result(actual, copy.deepcopy(actual))
        corrupted = copy.deepcopy(actual)
        corrupted["T6"]["vertices"] -= 1
        with self.assertRaises(AssertionError):
            verify_result(actual, corrupted)


if __name__ == "__main__":
    unittest.main()
