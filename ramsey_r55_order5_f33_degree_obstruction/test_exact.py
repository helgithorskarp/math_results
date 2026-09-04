#!/usr/bin/env python3
"""Exact local tests for the degree-network encoding."""

from __future__ import annotations

import itertools
import unittest
from collections import Counter

from generate_formula import (
    comparator_clauses,
    degree_inputs,
    edge_mapping,
)


def satisfied(clause: tuple[int, ...], assignment: dict[int, bool]) -> bool:
    return any(assignment[abs(literal)] == (literal > 0) for literal in clause)


class ExactTests(unittest.TestCase):
    def test_order_five_cycle_types_and_scope(self) -> None:
        possible = [fixed for fixed in range(43) if fixed < 43 and (43 - fixed) % 5 == 0]
        self.assertEqual(possible, [3, 8, 13, 18, 23, 28, 33, 38])

    def test_comparator_truth_table(self) -> None:
        clauses = comparator_clauses(1, 2, 3, 4)
        for left, right, high, low in itertools.product((False, True), repeat=4):
            assignment = {1: left, 2: right, 3: high, 4: low}
            actual = all(satisfied(clause, assignment) for clause in clauses)
            expected = high == (left or right) and low == (left and right)
            self.assertEqual(actual, expected, (left, right, high, low))

    def test_bubble_network_sorts_all_eight_bit_words(self) -> None:
        for word in itertools.product((False, True), repeat=8):
            wires = list(word)
            for end in range(len(wires) - 1, 0, -1):
                for position in range(end):
                    left, right = wires[position], wires[position + 1]
                    wires[position], wires[position + 1] = left or right, left and right
            self.assertEqual(wires, sorted(word, reverse=True))

    def test_degree_expansion(self) -> None:
        rows = degree_inputs(edge_mapping(33))
        self.assertEqual(len(rows), 35)
        self.assertTrue(all(len(row) == 42 for row in rows))
        for row in rows[:33]:
            self.assertEqual(Counter(Counter(row).values()), Counter({1: 32, 5: 2}))
        for row in rows[33:]:
            self.assertEqual(Counter(Counter(row).values()), Counter({1: 38, 2: 2}))

    def test_sorted_output_degree_window(self) -> None:
        for degree in range(43):
            wires = [True] * degree + [False] * (42 - degree)
            self.assertEqual(wires[17] and not wires[24], 18 <= degree <= 24)


if __name__ == "__main__":
    unittest.main()
