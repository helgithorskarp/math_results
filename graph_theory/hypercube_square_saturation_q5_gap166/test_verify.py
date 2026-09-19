#!/usr/bin/env python3

from collections import Counter
from fractions import Fraction
from pathlib import Path
import sys
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify


class Gap166Tests(unittest.TestCase):
    def test_incidence_sizes(self) -> None:
        self.assertEqual(len(verify.EDGES), 32)
        self.assertEqual(len(verify.SQUARES), 24)
        self.assertEqual(len(verify.FACETS), 8)
        multiplicities = Counter(
            edge for facet in verify.FACETS for edge in verify.FACET_EDGES[facet]
        )
        self.assertEqual(set(multiplicities.values()), {3})

    def test_representative_statistics(self) -> None:
        expected = {
            0x07FF2332: (17, 3, 0),
            0x0FFF163C: (19, 5, 28),
            0x18BB77EE: (20, 6, 42),
            0x07FF2336: (18, 6, 48),
        }
        for mask, (edges, slack, deficit) in expected.items():
            statistics = verify.direct_q4_statistics(mask)
            self.assertEqual((statistics[0], statistics[3]), (edges, slack))
            self.assertEqual(17 * slack - 3 * edges, deficit)

    def test_live_facet_capacity_maxima(self) -> None:
        maxima = [
            max(verify.live_support_distribution(live)) for live in range(1, 11)
        ]
        self.assertEqual(maxima, [0, 0, 0, 1, 5, 9, 16, 28, 48, 80])

    def test_zero_deficit_profiles(self) -> None:
        cases = []
        for live in range(1, 11):
            if 17 * live % 4 == 0:
                cases.append(
                    (
                        live,
                        17 * live // 4,
                        max(verify.live_support_distribution(live)),
                    )
                )
        self.assertEqual(cases, [(4, 17, 1), (8, 34, 28)])

    def test_global_arithmetic(self) -> None:
        q5_ratio = Fraction(12 * 56 + 166, 34 * 56)
        self.assertEqual(q5_ratio, Fraction(419, 952))
        self.assertEqual(q5_ratio / 12, Fraction(419, 11_424))
        self.assertEqual(1 - q5_ratio / 12, Fraction(11_005, 11_424))
        new_constant = Fraction(19_992, 11_005)
        old_constant = Fraction(204, 113)
        self.assertEqual(new_constant - old_constant, Fraction(14_076, 1_243_565))
        self.assertEqual(
            19_992 * (113 * 8 + 295) - 204 * (11_005 * 8 + 28_979),
            14_076 * (8 - 1),
        )


if __name__ == "__main__":
    unittest.main()
