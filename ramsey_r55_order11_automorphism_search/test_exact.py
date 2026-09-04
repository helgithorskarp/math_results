#!/usr/bin/env python3
"""Focused exhaustive test for the single-cycle degree encoding."""

from __future__ import annotations

import itertools
import unittest

from generate_formula import single_cycle_degree_clauses


def satisfied(clause: tuple[int, ...], assignment: dict[int, bool]) -> bool:
    return any(assignment[abs(literal)] == (literal > 0) for literal in clause)


class DegreeEncodingTests(unittest.TestCase):
    def test_all_threshold_internal_profiles(self) -> None:
        incidence = list(range(1, 33))
        internal = list(range(33, 38))
        clauses = single_cycle_degree_clauses(incidence, internal)
        self.assertEqual(len(clauses), 64)
        for ones in range(33):
            incidence_values = [False] * (32 - ones) + [True] * ones
            for internal_values in itertools.product((False, True), repeat=5):
                assignment = dict(zip(incidence, incidence_values, strict=True))
                assignment.update(dict(zip(internal, internal_values, strict=True)))
                actual = all(satisfied(clause, assignment) for clause in clauses)
                expected = 18 <= ones + 2 * sum(internal_values) <= 24
                self.assertEqual(actual, expected, (ones, internal_values))


if __name__ == "__main__":
    unittest.main()
