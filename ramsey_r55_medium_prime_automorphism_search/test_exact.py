#!/usr/bin/env python3
"""Exhaustive tests for every single-cycle degree encoding."""

from __future__ import annotations

import itertools
import unittest

from generate_formula import CASES, ORDER, single_cycle_degree_clauses
from verify import RupChecker, parse_line


def satisfied(clause: tuple[int, ...], assignment: dict[int, bool]) -> bool:
    return any(assignment[abs(literal)] == (literal > 0) for literal in clause)


class DegreeEncodingTests(unittest.TestCase):
    def test_all_single_cycle_cases(self) -> None:
        assignments_checked = 0
        for prime in CASES:
            fixed = ORDER - prime
            incidence = list(range(1, fixed + 1))
            internal = list(range(fixed + 1, fixed + 1 + (prime - 1) // 2))
            clauses = single_cycle_degree_clauses(fixed, incidence, internal)
            for ones in range(fixed + 1):
                incidence_values = [False] * (fixed - ones) + [True] * ones
                for internal_values in itertools.product((False, True), repeat=len(internal)):
                    assignment = dict(zip(incidence, incidence_values, strict=True))
                    assignment.update(dict(zip(internal, internal_values, strict=True)))
                    actual = all(satisfied(clause, assignment) for clause in clauses)
                    expected = 18 <= ones + 2 * sum(internal_values) <= 24
                    self.assertEqual(actual, expected, (prime, ones, internal_values))
                    assignments_checked += 1
        self.assertEqual(assignments_checked, 64_704)


class RupCheckerTests(unittest.TestCase):
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
