#!/usr/bin/env python3
"""Small direct and structurally independent checks."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import exact_covers as target


def continuant(entries: tuple[int, ...]) -> int:
    older, newer = 0, 1
    for entry in entries:
        older, newer = newer, entry * newer + older
    return newer


def independent_lagrange_square(path: tuple[int, ...]) -> Fraction:
    """Use four continuants, not the target's running 2x2 product."""
    base = (2,) + target.continued_fraction_entries(path)
    values = []
    for shift in range(len(base)):
        period = base[shift:] + base[:shift]
        p = continuant(period)
        r = continuant(period[:-1])
        q = continuant(period[1:])
        s = continuant(period[1:-1])
        values.append(Fraction((p - s) ** 2 + 4 * r * q, q * q))
    return max(values)


class ExactCoverTests(unittest.TestCase):
    def test_small_path_counts(self):
        self.assertEqual([len(list(target.rational_dyck_paths(n))) for n in range(2, 9)],
                         [1, 2, 5, 14, 42, 132, 429])

    def test_independent_lagrange_formula(self):
        for n in range(2, 9):
            for path in target.rational_dyck_paths(n):
                self.assertEqual(target.lagrange_data(path)[0],
                                 independent_lagrange_square(path))

    def test_small_cover_counts(self):
        expected = {
            2: (0, 0, 0),
            3: (1, 1, 1),
            4: (4, 5, 3),
            5: (13, 18, 2),
            6: (41, 67, 6),
            7: (132, 229, 15),
            8: (431, 793, 29),
        }
        for n, counts in expected.items():
            data = target.compute(n)
            actual = (
                len(data["matching_covers"]),
                len(data["lagrange_covers"]),
                len(data["common_covers"]),
            )
            self.assertEqual(actual, counts)

    def test_apruzzese_cong_example(self):
        target.verify_source_example()

    def test_lagrange_equality_classes_use_exact_square(self):
        data = target.compute(7)
        rebuilt = defaultdict(list)
        for path in data["paths"]:
            rebuilt[independent_lagrange_square(path)].append(path)
        self.assertEqual(dict(rebuilt), dict(data["lagrange_groups"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
