#!/usr/bin/env python3
"""Definition-level and tampering tests for verify.py."""

import unittest

import verify


class BarrierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = verify.projective_plane_incidence_graph()
        self.arcs = verify.deterministic_euler_orientation(self.base)
        self.expansion, self.edge_vertex, self.matching = verify.eulerian_triangle_expansion(
            self.base, self.arcs
        )

    def test_projective_base(self) -> None:
        self.assertEqual(len(self.base), 26)
        self.assertEqual(len(verify.edges(self.base)), 52)
        self.assertEqual({len(neighbors) for neighbors in self.base.values()}, {4})
        self.assertEqual(verify.girth_at_most(self.base, 6), 6)

    def test_expansion_profile(self) -> None:
        self.assertEqual(len(self.expansion), 78)
        self.assertEqual(len(verify.edges(self.expansion)), 130)
        self.assertEqual({len(self.expansion[v]) for v in range(26)}, {4})
        self.assertEqual({len(self.expansion[v]) for v in range(26, 78)}, {3})
        self.assertEqual(len(self.matching), 26)

    def test_short_cycle_profile(self) -> None:
        counts = {
            length: len(verify.cycles_of_length(self.expansion, length))
            for length in range(3, 9)
        }
        self.assertEqual(counts, {3: 26, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0})

    def test_every_edge_deletion_destroys_the_three_core(self) -> None:
        self.assertEqual(verify.three_core_vertices(self.expansion), set(self.expansion))
        for edge in verify.edges(self.expansion):
            self.assertEqual(verify.three_core_vertices(self.expansion, edge), set())

    def test_unbalanced_orientation_is_rejected(self) -> None:
        tampered = list(self.arcs)
        tail, head = tampered[0]
        tampered[0] = (head, tail)
        with self.assertRaises(ValueError):
            verify.eulerian_triangle_expansion(self.base, tampered)

    def test_cycle_canonicalization(self) -> None:
        expected = (1, 2, 3, 4)
        self.assertEqual(verify.canonical_cycle((3, 4, 1, 2)), expected)
        self.assertEqual(verify.canonical_cycle((2, 1, 4, 3)), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
