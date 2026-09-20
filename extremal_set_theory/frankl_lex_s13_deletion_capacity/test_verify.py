#!/usr/bin/env python3
"""Boundary and mutation tests for verify.py."""

import unittest

import verify


def block(*items):
    return frozenset(items)


class CapacityTests(unittest.TestCase):
    def test_easy_singleton_is_rejected(self):
        # Omitting 8 produces the twelfth block avoiding 8.
        self.assertFalse(verify.respects_capacity((block(1, 2, 3, 9),)))

    def test_all_hard_singletons_survive(self):
        hard = [x for x in verify.REMAINING if {8, 9} <= x]
        self.assertEqual(len(hard), 21)
        self.assertTrue(all(verify.respects_capacity((x,)) for x in hard))

    def test_valid_triple_boundary(self):
        extra = (block(1, 6, 8, 9), block(5, 7, 8, 9), block(6, 7, 8, 9))
        self.assertTrue(verify.respects_capacity(extra))

    def test_missing_67_fails_at_distance_three(self):
        extra = (block(1, 6, 8, 9), block(2, 6, 8, 9), block(5, 7, 8, 9))
        self.assertFalse(verify.respects_capacity(extra))

    def test_four_edges_cannot_survive(self):
        hard = [x for x in verify.REMAINING if {8, 9} <= x]
        self.assertFalse(any(verify.respects_capacity(x) for x in __import__("itertools").combinations(hard, 4)))

    def test_subgroup_preserves_base(self):
        for permutation in verify.GROUP:
            image = {verify.act_block(permutation, x) for x in verify.L13}
            self.assertEqual(image, set(verify.L13))


if __name__ == "__main__":
    unittest.main(verbosity=2)
