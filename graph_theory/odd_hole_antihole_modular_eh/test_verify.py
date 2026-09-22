#!/usr/bin/env python3
"""Mutation-sensitive unit tests for verify.py."""

from __future__ import annotations

import unittest

import verify


class AuditTests(unittest.TestCase):
    def test_stable_set_counts(self) -> None:
        self.assertEqual(len(verify.stable_sets(5)), 11)
        self.assertEqual(len(verify.stable_sets(7)), 29)
        self.assertEqual(len(verify.stable_sets(9)), 76)

    def test_maximum_sets(self) -> None:
        for r in range(2, 9):
            sets = verify.maximum_cycle_stable_sets(r)
            self.assertEqual(len(sets), 2 * r + 1)
            self.assertTrue(all(len(stable) == r for stable in sets))
            self.assertTrue(all(verify.is_stable(sum(1 << i for i in s), 2 * r + 1) for s in sets))

    def test_incidence_identity(self) -> None:
        self.assertEqual(
            verify.audit_incidence_identity(4),
            {"stable_sets": 76, "incidences": 684},
        )

    def test_pair_boundary(self) -> None:
        row = verify.audit_vertex_pair_types(3)
        self.assertEqual(row["uniform_half"], 1)
        self.assertEqual(row["integral_half"], 15)
        self.assertEqual(row["uniform_integral"], 29)

    def test_kept_index_mutation_is_detected(self) -> None:
        r = 4
        n = 2 * r + 1
        stable = frozenset({0, 3, 6})
        correct = verify.kept_indices(stable, n)
        mutated = frozenset((j + 1) % n for j in correct)
        max_sets = verify.maximum_cycle_stable_sets(r)
        correct_counts = tuple(sum(i in max_sets[j] for j in correct) for i in range(n))
        mutated_counts = tuple(sum(i in max_sets[j] for j in mutated) for i in range(n))
        self.assertEqual(correct_counts, tuple(r - len(stable) + int(i in stable) for i in range(n)))
        self.assertNotEqual(mutated_counts, correct_counts)

    def test_sharp_recurrence(self) -> None:
        row = verify.sharp_rows(last_h=3, last_k=2)[-1]
        self.assertEqual(row, {"h": 3, "k": 2, "order": 2401, "alpha": 36, "omega": 36, "product": 1296})


if __name__ == "__main__":
    unittest.main()

