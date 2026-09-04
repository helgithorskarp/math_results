#!/usr/bin/env python3
"""Focused tests for the standalone RUP proof checker."""

from __future__ import annotations

import unittest

from verify_drup import RupChecker, parse_proof_line


class RupCheckerTests(unittest.TestCase):
    def test_rejects_empty_clause_for_satisfiable_formula(self) -> None:
        checker = RupChecker(2, [(1, 2)])
        self.assertFalse(checker.rup(()))

    def test_accepts_nontrivial_rup_step(self) -> None:
        checker = RupChecker(2, [(1, 2), (1, -2)])
        self.assertTrue(checker.rup((1,)))
        checker.add_clause((1,))
        self.assertFalse(checker.rup(()))

    def test_accepts_empty_clause_after_unit_conflict(self) -> None:
        checker = RupChecker(2, [(1,), (-1, 2), (-2,)])
        self.assertTrue(checker.rup(()))

    def test_parse_addition_and_deletion(self) -> None:
        self.assertEqual(parse_proof_line("1 -2 0"), (False, (1, -2)))
        self.assertEqual(parse_proof_line("d 1 -2 0"), (True, (1, -2)))
        with self.assertRaises(ValueError):
            parse_proof_line("1 -2")


if __name__ == "__main__":
    unittest.main()
