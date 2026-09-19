#!/usr/bin/env python3

from fractions import Fraction
from pathlib import Path
import sys
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify


class Gap200Tests(unittest.TestCase):
    def test_cutoff(self) -> None:
        self.assertEqual(17 * 16 - 3 * 24, 200)

    def test_survivor_totals(self) -> None:
        self.assertEqual(
            [row[0] for row in verify.EXPECTED_SURVIVORS],
            [42, 84, 132, 144, 161, 166, 174, 186, 188, 190, 195, 196, 198],
        )

    def test_parity_counterexample(self) -> None:
        selected = {(0, 0), (0, 1), (1, 1)}
        global_mask = sum(
            1 << verify.base.Q5_EDGE_INDEX[edge] for edge in selected
        )
        total_deficit = 0
        for facet in verify.base.Q5_FACETS:
            local_mask = 0
            for edge in range(len(verify.base.EDGES)):
                if verify.base.embed_q4(1 << edge, facet) & global_mask:
                    local_mask |= 1 << edge
            edges, _, _, slack = verify.base.direct_q4_statistics(local_mask)
            total_deficit += 17 * slack - 3 * edges
        self.assertEqual(total_deficit, 831)
        self.assertEqual(total_deficit % 2, 1)

    def test_residual_placement_counts(self) -> None:
        expected = {
            "42": 9,
            "84": 9,
            "132": 252,
            "144": 252,
            "161": 504,
            "166": 72,
            "174": 84,
            "186": 84,
            "188": 504,
            "190": 252,
            "195": 72,
            "196": 84,
            "198": 252,
        }
        self.assertEqual(
            {key: value["cases"] for key, value in verify.EXPECTED_RESIDUALS.items()},
            expected,
        )

    def test_local_to_global_arithmetic(self) -> None:
        ratio = Fraction(12 * 56 + 200, 34 * 56)
        self.assertEqual(ratio, Fraction(109, 238))
        self.assertEqual(ratio / 12, Fraction(109, 2856))
        self.assertEqual(1 - ratio / 12, Fraction(2747, 2856))
        self.assertEqual(Fraction(7, 2) * 2856, 9996)

    def test_improvement_and_integer_bounds(self) -> None:
        new = Fraction(4998, 2747)
        old = Fraction(19992, 11005)
        self.assertEqual(new - old, Fraction(84966, 30230735))
        for dimension, expected in ((7, 170), (8, 351)):
            value = Fraction(
                4998 * dimension * 2**dimension,
                2747 * dimension + 7249,
            )
            self.assertEqual(
                (value.numerator + value.denominator - 1) // value.denominator,
                expected,
            )


if __name__ == "__main__":
    unittest.main()
