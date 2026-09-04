#!/usr/bin/env python3
"""Focused exact tests for the order-seven, eight-fixed-point encoding."""

import collections
import itertools
import unittest

import generate_formula as generator


def falsified(clause: tuple[int, ...], assignment: dict[int, int]) -> bool:
    return all(assignment[abs(literal)] != (literal > 0) for literal in clause)


class ExactTests(unittest.TestCase):
    def test_edge_partition(self) -> None:
        mapping = generator.edge_variables()
        self.assertEqual(len(mapping), 903)
        self.assertEqual(len(set(mapping.values())), 153)
        self.assertEqual(
            collections.Counter(collections.Counter(mapping.values()).values()),
            {1: 28, 7: 125},
        )

    def test_blocking_clause(self) -> None:
        variables = [3, 8, 11, 20]
        for values in itertools.product((0, 1), repeat=4):
            clause = generator.blocking_clause(variables, values)
            for candidate in itertools.product((0, 1), repeat=4):
                assignment = dict(zip(variables, candidate))
                self.assertEqual(falsified(clause, assignment), candidate == values)

    def test_necklace_representatives(self) -> None:
        accepted = [
            word
            for word in itertools.product((0, 1), repeat=7)
            if word == min(generator.rotations(word))
        ]
        self.assertEqual(len(accepted), 20)
        for word in accepted:
            self.assertLessEqual(word, min(generator.rotations(word)))


if __name__ == "__main__":
    unittest.main()
