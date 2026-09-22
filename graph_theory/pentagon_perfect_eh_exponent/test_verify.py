#!/usr/bin/env python3

import unittest
from fractions import Fraction

import verify


class ExactAuditTests(unittest.TestCase):
    def test_cycle_polytope_vertices(self) -> None:
        for step in (1, 2):
            edges = verify.cycle_edges(step)
            self.assertEqual(
                set(verify.polytope_vertices(edges)), verify.expected_vertices(edges)
            )
            self.assertEqual(len(verify.polytope_vertices(edges)), 12)

    def test_all_vertex_pairs(self) -> None:
        original = set(verify.cycle_edges(1))
        a_vertices = verify.polytope_vertices(verify.cycle_edges(2))
        b_vertices = verify.polytope_vertices(verify.cycle_edges(1))
        certificates = [
            verify.certify_pair(a, b, original)
            for a in a_vertices
            for b in b_vertices
        ]
        self.assertEqual(len(certificates), 144)
        self.assertEqual(
            sum(row["category"] == "half_half" for row in certificates), 1
        )

    def test_infeasible_mutation_is_absent(self) -> None:
        mutation = (Fraction(2, 3),) * 5
        self.assertNotIn(mutation, verify.polytope_vertices(verify.cycle_edges(1)))
        self.assertTrue(
            any(mutation[i] + mutation[j] > 1 for i, j in verify.cycle_edges(1))
        )

    def test_sharp_family(self) -> None:
        rows = verify.lexicographic_power_rows(8)
        self.assertEqual(rows[0], {
            "k": 0,
            "order": 1,
            "alpha": 1,
            "omega": 1,
            "alpha_times_omega": 1,
        })
        for row in rows:
            self.assertEqual(row["order"], 5 ** row["k"])
            self.assertEqual(row["alpha"], 2 ** row["k"])
            self.assertEqual(row["omega"], 2 ** row["k"])
            self.assertEqual(row["alpha_times_omega"], 4 ** row["k"])

    def test_summary_counts(self) -> None:
        summary = verify.audit()
        self.assertEqual(summary["vertex_pairs_checked"], 144)
        self.assertEqual(summary["last_sharp_order"], 5**12)
        self.assertEqual(summary["last_sharp_alpha_omega"], 4**12)


if __name__ == "__main__":
    unittest.main()
