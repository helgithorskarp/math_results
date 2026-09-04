#!/usr/bin/env python3
"""Focused exact tests for the middle order-five obstruction."""

from __future__ import annotations

import unittest

from generate_formula import CASES, ORDER


class ExactTests(unittest.TestCase):
    def test_cycle_type_exhaustion_and_scope(self) -> None:
        possible = [
            fixed
            for fixed in range(ORDER)
            if (ORDER - fixed) % 5 == 0 and fixed < ORDER
        ]
        self.assertEqual(possible, [3, 8, 13, 18, 23, 28, 33, 38])
        self.assertEqual(CASES, {5: (13, 18, 23, 28)})

    def test_edge_orbit_formula(self) -> None:
        expected = {13: 243, 18: 303, 23: 383, 28: 483}
        for fixed, edge_orbits in expected.items():
            cycles = (ORDER - fixed) // 5
            actual = (
                fixed * (fixed - 1) // 2
                + fixed * cycles
                + 2 * cycles
                + 5 * cycles * (cycles - 1) // 2
            )
            self.assertEqual(actual, edge_orbits)


if __name__ == "__main__":
    unittest.main()
