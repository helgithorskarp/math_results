#!/usr/bin/env python3
"""Focused tests for the standalone multi-instance DRUP checker."""

from __future__ import annotations

import unittest

from verify_proofs import RupChecker, parse_line


class RupTests(unittest.TestCase):
    def test_rejects_empty_for_satisfiable_formula(self) -> None:
        self.assertFalse(RupChecker(2, [(1, 2)]).rup(()))

    def test_nontrivial_rup_step(self) -> None:
        checker = RupChecker(2, [(1, 2), (1, -2)])
        self.assertTrue(checker.rup((1,)))
        checker.add_clause((1,))
        self.assertFalse(checker.rup(()))

    def test_unit_conflict(self) -> None:
        self.assertTrue(RupChecker(2, [(1,), (-1, 2), (-2,)]).rup(()))

    def test_parse(self) -> None:
        self.assertEqual(parse_line("1 -2 0"), (False, (1, -2)))
        self.assertEqual(parse_line("d 1 -2 0"), (True, (1, -2)))
        with self.assertRaises(ValueError):
            parse_line("1 -2")


if __name__ == "__main__":
    unittest.main()
