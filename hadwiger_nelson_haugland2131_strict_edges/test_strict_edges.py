#!/usr/bin/env python3
"""Small, fast tests for the independent cyclotomic implementation."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import independent_check as exact


DIRECTORY = Path(__file__).resolve().parent


class ExactFieldTests(unittest.TestCase):
    def test_cyclotomic_relation_and_order(self) -> None:
        expected_x24 = exact.pad(-value for value in exact.MODULUS[:-1])
        self.assertEqual(exact.multiply(exact.power(exact.ZETA, 23), exact.ZETA), expected_x24)
        self.assertEqual(exact.power(exact.ZETA, 84), exact.ONE)
        for proper_exponent in (42, 28, 12):
            self.assertNotEqual(exact.power(exact.ZETA, proper_exponent), exact.ONE)

    def test_inverse(self) -> None:
        value = exact.add(exact.ONE, exact.ZETA)
        self.assertEqual(exact.multiply(value, exact.inverse(value)), exact.ONE)

    def test_modular_sieve_has_no_small_false_negatives(self) -> None:
        certificate = json.loads((DIRECTORY / "certificate.json").read_text())
        specializations = certificate["independent_specializations"]
        for parameters in specializations:
            exact.check_specialization(parameters)
        _, vectors = exact.field_constants()
        points = [(exact.ZERO, exact.ZERO), *vectors[:12]]
        tables = [
            (parameters["prime"], exact.point_images(points, parameters))
            for parameters in specializations
        ]
        candidates = exact.sieve_intersection(tables)
        exact_edges = exact.confirm_base(points, candidates)
        all_exact_edges = exact.confirm_base(
            points,
            [(u, v) for u in range(len(points)) for v in range(u + 1, len(points))],
        )
        self.assertEqual(exact_edges, all_exact_edges)
        self.assertTrue(all((0, vertex) in exact_edges for vertex in range(1, 13)))


if __name__ == "__main__":
    unittest.main()
