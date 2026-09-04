#!/usr/bin/env python3
"""Focused exact tests for the C7 encoding and decision tree."""

import collections
import itertools
import unittest

import generate_formula as generator
import proof_tree


def falsified(clause: tuple[int, ...], assignment: dict[int, int]) -> bool:
    return all(assignment[abs(literal)] != (literal > 0) for literal in clause)


class ExactTests(unittest.TestCase):
    def test_edge_partition(self) -> None:
        mapping = generator.edge_variables()
        self.assertEqual(len(mapping), 903)
        self.assertEqual(len(set(mapping.values())), 129)
        self.assertEqual(set(collections.Counter(mapping.values()).values()), {7})

    def test_fixed_degree_encoding(self) -> None:
        mapping = generator.edge_variables()
        clauses: set[tuple[int, ...]] = set()
        generator.add_fixed_degree(clauses, mapping)
        variables = [mapping[(0, 1 + 7 * cycle)] for cycle in range(6)]
        self.assertEqual(len(clauses), 30)
        for values in itertools.product((0, 1), repeat=6):
            assignment = dict(zip(variables, values))
            accepted = not any(falsified(clause, assignment) for clause in clauses)
            self.assertEqual(accepted, sum(values) == 3)

    def test_tree_partition(self) -> None:
        leaves = proof_tree.leaves()
        self.assertEqual(len(leaves), 65)
        self.assertEqual(
            collections.Counter(leaf.name[:2] for leaf in leaves),
            {"l0": 14, "l1": 14, "l2": 9, "l3": 28},
        )
        proof_tree.check_partition()


if __name__ == "__main__":
    unittest.main()
