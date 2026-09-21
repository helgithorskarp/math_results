#!/usr/bin/env python3
"""Focused tests for verify.py."""

import unittest

import verify


class LocalOrderAuditTests(unittest.TestCase):
    def test_directed_triangle(self) -> None:
        triangle = (1, 0, 1)  # 0->1->2->0 in pairs (01,02,12)
        self.assertTrue(verify.is_locally_transitive(triangle, 3))
        self.assertFalse(verify.is_transitive(triangle, 3))
        for root in range(3):
            verify.rooted_witness(triangle, 3, root)

    def test_forbidden_four_vertex_shapes_fail_locality(self) -> None:
        triangle = (1, 0, 1)
        for source in (True, False):
            profile = []
            for u, v in verify.pairs(4):
                if u == 0:
                    profile.append(int(source))
                else:
                    profile.append(triangle[verify.pair_index(3)[(u - 1, v - 1)]])
            self.assertFalse(verify.is_locally_transitive(tuple(profile), 4))

    def test_cut_switch_converse(self) -> None:
        base = verify.order_profile(tuple(range(7)))
        switched = verify.switch_cut(base, 7, {0, 2, 3, 6})
        self.assertTrue(verify.is_locally_transitive(switched, 7))

    def test_carousel_formula(self) -> None:
        for q in range(1, 20):
            profile = verify.carousel(q)
            p, a, b = verify.carousel_orders(q)
            lhs = tuple(x + y for x, y in zip(profile, verify.order_profile(p)))
            rhs = tuple(x + y for x, y in zip(verify.order_profile(a), verify.order_profile(b)))
            self.assertEqual(lhs, rhs)

    def test_small_exhaustive_totals(self) -> None:
        total, local, transitive, rooted = verify.audit_all_tournaments(max_n=4)
        self.assertEqual(total, 75)
        self.assertEqual(transitive, 33)
        self.assertGreaterEqual(local, transitive)
        self.assertGreaterEqual(rooted, local)


if __name__ == "__main__":
    unittest.main()
