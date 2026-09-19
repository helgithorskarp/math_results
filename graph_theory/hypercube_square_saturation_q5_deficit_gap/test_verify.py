#!/usr/bin/env python3

from collections import Counter
from fractions import Fraction
from itertools import permutations
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify


class DeficitGapTests(unittest.TestCase):
    def test_incidence_sizes(self) -> None:
        self.assertEqual(len(verify.EDGES), 32)
        self.assertEqual(len(verify.SQUARES), 24)
        self.assertEqual(len(verify.FACETS), 8)
        self.assertEqual({len(verify.FACET_EDGES[facet]) for facet in verify.FACETS}, {12})
        multiplicities = Counter(
            edge
            for facet in verify.FACETS
            for edge in verify.FACET_EDGES[facet]
        )
        self.assertEqual(set(multiplicities.values()), {3})

    def test_empty_and_defect_witness(self) -> None:
        self.assertEqual(verify.direct_q4_statistics(0), (0, 0, 0, 0))
        self.assertEqual(verify.direct_q4_statistics(0x0FFF163C), (19, 17, 5, 5))
        self.assertEqual(17 * 5 - 3 * 19, 28)

    def test_square_rejection(self) -> None:
        completed_square = sum(1 << edge for edge in verify.SQUARES[0])
        with self.assertRaises(ValueError):
            verify.direct_q4_statistics(completed_square)

    def test_witness_orbit(self) -> None:
        witness = 0x0FFF163C
        orbit = {
            verify.transform(witness, translation, permutation)
            for translation in verify.VERTICES
            for permutation in permutations(range(verify.DIM))
        }
        self.assertEqual(len(orbit), 192)
        self.assertIn(witness, orbit)

    def test_global_arithmetic(self) -> None:
        q5_ratio = Fraction(12 * 56 + 28, 34 * 56)
        self.assertEqual(q5_ratio, Fraction(25, 68))
        self.assertEqual(q5_ratio / 12, Fraction(25, 816))
        self.assertEqual(1 - q5_ratio / 12, Fraction(791, 816))
        self.assertEqual(Fraction(204, 113) - Fraction(5_183_640, 2_874_791), Fraction(706_044, 324_851_383))


if __name__ == "__main__":
    unittest.main()
