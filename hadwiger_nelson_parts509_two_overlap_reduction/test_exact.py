#!/usr/bin/env python3

import unittest

import verify


class ExactTests(unittest.TestCase):
    def test_radical_products(self):
        sqrt3 = (0, 1, 0, 0, 0, 0, 0, 0)
        sqrt5 = (0, 0, 1, 0, 0, 0, 0, 0)
        self.assertEqual(verify.field_multiply(sqrt3, sqrt3), (3, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(verify.field_multiply(sqrt3, sqrt5), (0, 0, 0, 1, 0, 0, 0, 0))

    def test_coloring_packing_round_trip(self):
        colors = [(7 * index + 2) % 4 for index in range(verify.S_SIZE)]
        self.assertEqual(verify.unpack_coloring(verify.pack_coloring(colors)), colors)

    def test_exceptional_parameters_are_unit(self):
        one = (64 * 64,) + (0,) * 7
        for c, s in verify.EXCEPTIONAL_ROTATIONS:
            norm = verify.field_add(verify.field_multiply(c, c), verify.field_multiply(s, s))
            self.assertEqual(norm, one)


if __name__ == "__main__":
    unittest.main()
