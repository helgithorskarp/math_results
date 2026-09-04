"""Tests for the independent terminal triangle--kite audit."""

from fractions import Fraction
import unittest

import verify_local_map as audit


class TerminalTriangulationTests(unittest.TestCase):
    def test_union_boundary(self) -> None:
        certificate = audit.local_map_certificate()
        self.assertEqual(len(certificate["outer_boundary"]), 5)
        self.assertEqual(certificate["crossing_degrees"], [2, 2, 2, 2, 2])

    def test_forced_restoration(self) -> None:
        certificate = audit.local_map_certificate()
        self.assertEqual(certificate["restored_b"], ["u", "r"])
        self.assertEqual(certificate["restored_c"], ["u", "t"])

    def test_profiles(self) -> None:
        rows = audit.profile_certificate()
        self.assertEqual(
            tuple((row["c5"], row["reported_full"]) for row in rows),
            ((10, 9), (12, 11)),
        )
        self.assertEqual(
            tuple((row["terminal_edges"], row["terminal_crossings"]) for row in rows),
            ((83, 17), (82, 16)),
        )

    def test_order54_sampling(self) -> None:
        self.assertEqual(audit.order54_sampling(), Fraction(1965795, 322))


if __name__ == "__main__":
    unittest.main()
