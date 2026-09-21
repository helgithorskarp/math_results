#!/usr/bin/env python3

import unittest

from verify import (
    contains_2143,
    dilate,
    direct_flagged_count,
    flagged_count,
    inflate_identity,
    lehmer_code,
    transition_upsilon,
    vexillary_data,
)


class VexillaryDilationTests(unittest.TestCase):
    def test_pattern_closure_examples(self):
        vexillary = (2, 0, 3, 1)  # 3142
        nonvexillary = (1, 0, 3, 2)  # 2143
        self.assertFalse(contains_2143(vexillary))
        self.assertFalse(contains_2143(inflate_identity(vexillary, 3)))
        self.assertTrue(contains_2143(nonvexillary))
        self.assertTrue(contains_2143(inflate_identity(nonvexillary, 3)))

    def test_code_dilation(self):
        w = (7, 0, 1, 5, 8, 6, 2, 4, 3)
        for k in (1, 2, 3, 4):
            self.assertEqual(lehmer_code(inflate_identity(w, k)), dilate(lehmer_code(w), k))

    def test_shape_flag_dilation(self):
        w = (2, 0, 3, 1)
        lam, flag = vexillary_data(w)
        self.assertEqual((lam, flag), ((2, 1), (1, 3)))
        for k in (1, 2, 3, 4):
            self.assertEqual(vexillary_data(inflate_identity(w, k)), (dilate(lam, k), dilate(flag, k)))

    def test_flagged_determinant_directly(self):
        cases = [((2, 1), (1, 3)), ((3, 2), (2, 4)), ((2, 2, 1), (2, 3, 5))]
        for lam, flag in cases:
            self.assertEqual(flagged_count(lam, flag), direct_flagged_count(lam, flag))

    def test_schubert_bridge(self):
        examples = [(0,), (1, 0, 2), (2, 0, 3, 1), (2, 3, 0, 1)]
        for w in examples:
            lam, flag = vexillary_data(w)
            self.assertEqual(flagged_count(lam, flag), transition_upsilon(w))

    def test_frontier_example(self):
        lam, flag = (2, 1), (1, 3)
        self.assertEqual(flagged_count(lam, flag), 2)
        self.assertEqual(flagged_count(dilate(lam, 2), dilate(flag, 2)), 20)
        self.assertGreater(20, 2**4)


if __name__ == "__main__":
    unittest.main()
