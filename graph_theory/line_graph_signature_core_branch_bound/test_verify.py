#!/usr/bin/env python3

import unittest
from fractions import Fraction

import verify


class ExactAuditTests(unittest.TestCase):
    def test_inertia_pivots(self) -> None:
        self.assertEqual(verify.inertia([[0, 1], [1, 0]]), (1, 0, 1))
        self.assertEqual(verify.inertia([[2, 1], [1, 2]]), (2, 0, 0))
        self.assertEqual(verify.inertia([[0, 0], [0, 0]]), (0, 2, 0))

    def test_rooted_states(self) -> None:
        singleton = ()
        edge_rooted_at_end = (singleton,)
        path_three_rooted_at_end = (edge_rooted_at_end,)
        self.assertEqual(verify.rooted_state(singleton), (-1, Fraction(-1)))
        self.assertEqual(verify.rooted_state(edge_rooted_at_end), (0, Fraction(1)))
        self.assertEqual(verify.rooted_state(path_three_rooted_at_end), (-1, Fraction(-1)))
        audit = verify.audit_rooted_trees(8)
        self.assertEqual(audit["counts"], [1, 1, 2, 4, 9, 20, 48, 115])

    def test_path_core_principal_signature(self) -> None:
        # A path adjacency matrix is bipartite and has signature zero.
        adj = verify.adjacency(5, ((0, 1), (1, 2), (2, 3), (3, 4)))
        self.assertEqual(verify.signature(verify.shifted_signless(adj)), -1)
        path_adjacency = [
            [0, 1, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 1, 0],
        ]
        self.assertEqual(verify.signature(path_adjacency), 0)

    def test_graph6_witnesses(self) -> None:
        witnesses = verify.audit_witnesses()
        self.assertEqual(witnesses["c2"]["line_inertia"], (6, 1, 5))
        self.assertEqual(witnesses["c3"]["line_inertia"], (9, 0, 7))

    def test_small_graph_audit(self) -> None:
        audit = verify.audit_graphs(4, 4)
        self.assertEqual(audit["connected"], 44)
        self.assertEqual(audit["c_ge_2"], 7)


if __name__ == "__main__":
    unittest.main()
