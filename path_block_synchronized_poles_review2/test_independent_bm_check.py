"""Tests for the independent synchronized-pole checker."""

from fractions import Fraction
import unittest

import independent_bm_check as audit


class IndependentPoleAuditTests(unittest.TestCase):
    def test_berlekamp_massey_on_fibonacci(self) -> None:
        sequence = [0, 1]
        for _ in range(18):
            sequence.append(sequence[-1] + sequence[-2])
        self.assertEqual(
            audit.berlekamp_massey(sequence),
            [Fraction(1), Fraction(-1), Fraction(-1)],
        )

    def test_preimage_root_orders(self) -> None:
        self.assertEqual(audit.preimage_root_orders(2, 2), (4,))
        self.assertEqual(audit.preimage_root_orders(6, 2), (4, 12))

    def test_least_nonrectangular_fractions(self) -> None:
        self.assertEqual(
            audit.reconstruct_fraction((2, 1)),
            ([1, 2, 6, 2, 1], [1, 1]),
        )
        self.assertEqual(
            audit.reconstruct_fraction((4, 2)),
            ([1, 0, 2, 0, 6, 0, 2, 0, 1], [1, 0, 1]),
        )

    def test_rectangular_formula(self) -> None:
        self.assertIsNone(audit.check_partition((3, 3, 3)))

    def test_width_eight_grid(self) -> None:
        report = audit.verify(8)
        self.assertEqual(report["partitions_checked"], 66)
        self.assertEqual(report["nonrectangular_checked"], 46)
        self.assertEqual(report["maximizing_preimage_orders_checked"], 66)
        self.assertEqual(
            report["sha256"],
            "af28a8a610b9aaa1521e017c5aa41c209bbda20f5aac27ca6aed072f443b240b",
        )


if __name__ == "__main__":
    unittest.main()
