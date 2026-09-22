#!/usr/bin/env python3

import unittest

import verify


class ConstructionTests(unittest.TestCase):
    def test_small_matching_formulas(self):
        self.assertEqual(
            verify.rainbow_matching(3),
            ((0, 5), (1, 2), (3, 4)),
        )
        self.assertEqual(
            verify.rainbow_matching(4),
            ((0, 7), (1, 3), (2, 6), (4, 5)),
        )
        self.assertEqual(
            verify.rainbow_matching(6),
            ((0, 11), (1, 2), (3, 4), (5, 7), (6, 10), (8, 9)),
        )

    def test_factorization_and_rainbow_properties(self):
        for r in range(3, 101):
            verify.verify_one_factorization(r)
            verify.verify_rainbow_matching(r)

    def test_thick_spider_degree_and_coloring(self):
        for r in range(3, 31):
            edges = verify.thick_spider_edges(r)
            vertex_colors, edge_colors = verify.transferred_coloring(r, edges)
            self.assertTrue(
                verify.check_total_coloring(
                    verify.vertices(r), edges, vertex_colors, edge_colors
                )
            )
            self.assertEqual(max(verify.degrees(verify.vertices(r), edges).values()), 2 * r - 2)

    def test_checker_rejects_vertex_conflict(self):
        r = 5
        edges = verify.allowed_edges(r)
        vertex_colors, edge_colors = verify.transferred_coloring(r, edges)
        matching = verify.rainbow_matching(r)
        vertex_colors[matching[1][0]] = vertex_colors[matching[0][0]]
        self.assertFalse(
            verify.check_total_coloring(
                verify.vertices(r), edges, vertex_colors, edge_colors
            )
        )

    def test_checker_rejects_incidence_conflict(self):
        r = 5
        edges = verify.allowed_edges(r)
        vertex_colors, edge_colors = verify.transferred_coloring(r, edges)
        first = edges[0]
        edge_colors[first] = vertex_colors[first[0]]
        self.assertFalse(
            verify.check_total_coloring(
                verify.vertices(r), edges, vertex_colors, edge_colors
            )
        )

    def test_rank_two_boundary(self):
        verify.check_rank_two_boundary()


if __name__ == "__main__":
    unittest.main()
