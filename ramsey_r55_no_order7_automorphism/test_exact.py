#!/usr/bin/env python3
"""Focused exact tests for the consolidated order-seven obstruction."""

import itertools
import unittest

import generate_formula as generator


def falsified(clause: tuple[int, ...], assignment: dict[int, int]) -> bool:
    return all(assignment[abs(literal)] != (literal > 0) for literal in clause)


class ExactTests(unittest.TestCase):
    def test_cycle_type_exhaustion(self) -> None:
        possible = [fixed for fixed in range(43) if (43 - fixed) % 7 == 0 and fixed < 43]
        self.assertEqual(possible, [1, 8, 15, 22, 29, 36])

    def test_single_cycle_degree_encoding(self) -> None:
        incidence = list(range(1, 37))
        internal = [37, 38, 39]
        clauses = generator.single_cycle_degree_clauses(incidence, internal)
        self.assertEqual(len(clauses), 16)
        for total in range(37):
            word = [0] * (36 - total) + [1] * total
            for internal_values in itertools.product((0, 1), repeat=3):
                assignment = dict(zip(incidence, word))
                assignment.update(zip(internal, internal_values))
                accepted = not any(falsified(clause, assignment) for clause in clauses)
                self.assertEqual(accepted, 18 <= total + 2 * sum(internal_values) <= 24)


if __name__ == "__main__":
    unittest.main()
