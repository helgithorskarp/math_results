#!/usr/bin/env python3

import itertools
import unittest

import verify


class ConsecutivePackingTests(unittest.TestCase):
    def test_named_example(self):
        plan = verify.make_plan(2, (10, 9, 8))
        self.assertEqual(plan.q_base, 18)
        self.assertEqual(plan.multipliers, (19, 20, 21))
        self.assertEqual(plan.minimum_leaves, 164)
        self.assertEqual(plan.total_edges_at_threshold, 193)
        self.assertTrue(verify.check_graceful(verify.construct(plan)))

    def test_ratio_gate(self):
        for largest in range(2, 40):
            for r in range(1, 25):
                q = max(1, (largest - 1) * r - largest + 1)
                self.assertLess(
                    (q + r) * (largest - 1),
                    (q + 1) * largest,
                )

    def test_exchange_assignment_is_optimal(self):
        for lengths in ((9, 7, 2), (8, 8, 3, 2), (6, 5, 4, 3, 2)):
            multipliers = tuple(range(11, 11 + len(lengths)))
            aligned = max(a * q for a, q in zip(sorted(lengths, reverse=True), multipliers))
            brute = min(
                max(a * q for a, q in zip(permutation, multipliers))
                for permutation in itertools.permutations(lengths)
            )
            self.assertEqual(aligned, brute)

    def test_closure_and_multiplicative_paths(self):
        for c in range(2, 20):
            _, minimum_m = verify.closure_parameters(c)
            for extra in (0, 1, 17):
                m = minimum_m + extra
                self.assertTrue(verify.is_self_matched(verify.closure_path(c, m), m))
        for length in range(2, 25):
            for q in (1, 2, 7, 31):
                m = length * q + 1
                path = verify.multiplicative_path(length, q, m)
                self.assertTrue(verify.is_self_matched(path, m))

    def test_threshold_boundary_and_monotonicity(self):
        for c, lengths in ((2, (10, 9, 8)), (4, (7, 7, 3)), (9, (12, 5, 2, 2))):
            plan = verify.make_plan(c, lengths)
            with self.assertRaises(ValueError):
                verify.construct(plan, plan.minimum_leaves - 1)
            for extra in (0, 1, 20):
                self.assertTrue(
                    verify.check_graceful(
                        verify.construct(plan, plan.minimum_leaves + extra)
                    )
                )

    def test_best_plan_checks_every_closure_choice(self):
        arms = (12, 8, 3, 2)
        index, best = verify.best_plan(arms)
        all_plans = [
            verify.make_plan(c, arms[:i] + arms[i + 1 :])
            for i, c in enumerate(arms)
        ]
        self.assertEqual(best.minimum_leaves, min(plan.minimum_leaves for plan in all_plans))
        self.assertEqual(best.closure_length, arms[index])

    def test_checker_rejects_tampering(self):
        plan = verify.make_plan(3, (8, 5, 2))
        construction = verify.construct(plan)
        self.assertTrue(verify.check_graceful(construction))
        bad_leaves = list(construction["leaf_labels"])
        bad_leaves[-1] = bad_leaves[-2]
        tampered = dict(construction)
        tampered["leaf_labels"] = tuple(bad_leaves)
        self.assertFalse(verify.check_graceful(tampered))


if __name__ == "__main__":
    unittest.main()
