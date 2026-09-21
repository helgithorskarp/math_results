import argparse
import unittest

import verify


class FareyReductionTests(unittest.TestCase):
    def test_direction_normalization(self):
        self.assertEqual(verify.primitive_direction((-6, 9)), (2, -3))
        self.assertEqual(verify.primitive_direction((0, -5)), (0, 1))

    def test_zero_direction_rejected(self):
        with self.assertRaises(ValueError):
            verify.primitive_direction((0, 0))

    def test_characteristic_two_cancellation(self):
        factor = {(0, 0), (1, 0)}
        self.assertEqual(
            verify.multiply_mod2(factor, factor),
            {(0, 0), (2, 0)},
        )

    def test_triangle_support(self):
        self.assertEqual(
            verify.product_support([(1, 0), (0, 1), (1, 1)]),
            {(0, 0), (1, 0), (0, 1), (2, 1), (1, 2), (2, 2)},
        )

    def test_small_direction_audit(self):
        record = verify.direction_record(2)
        self.assertEqual(record["determinant_one_four_cliques"], 0)
        self.assertEqual(record["triangle_normal_forms"], 1)

    def test_odd_torus_dimensions(self):
        for size in (3, 5):
            record = verify.torus_record(size)
            self.assertEqual(record["triangle_kernel_dimension"], 3 * size - 2)
            self.assertEqual(
                record["direction_sum_dimension"],
                record["triangle_kernel_dimension"],
            )

    def test_bad_parameters_rejected(self):
        with self.assertRaises(ValueError):
            verify.direction_record(0)
        with self.assertRaises(ValueError):
            verify.torus_record(4)
        with self.assertRaises(argparse.ArgumentTypeError):
            verify.parse_sizes("3,4")


if __name__ == "__main__":
    unittest.main()
