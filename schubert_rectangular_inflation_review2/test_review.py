#!/usr/bin/env python3

import unittest

import verify_independent as check


class IndependentReviewTests(unittest.TestCase):
    def test_permutation_shape_and_inflation(self) -> None:
        w = check.rectangular_permutation(2, 3, 1)
        self.assertEqual(w, (1, 5, 6, 2, 3, 4))
        self.assertEqual(check.descents(w), (3,))
        self.assertEqual(check.grassmannian_shape(w), (3, 3))
        self.assertEqual(check.tensor_identity(w, 2), check.rectangular_permutation(4, 6, 2))

    def test_jacobi_trudi_and_hyperfactorial_values(self) -> None:
        expected = {(1, 1, 0): 1, (1, 1, 3): 4, (2, 2, 2): 20, (4, 4, 4): 232848}
        for (a, b, c), value in expected.items():
            self.assertEqual(check.boxed_plane_partitions(a, b, c), value)
            self.assertEqual(check.schur_rectangle_jacobi_trudi(a, b, a + c), value)

    def test_exact_equality_cases(self) -> None:
        for a, b, c, k in [(2, 3, 0, 4), (2, 3, 2, 1), (2, 3, 2, 3)]:
            base = check.boxed_plane_partitions(a, b, c)
            large = check.boxed_plane_partitions(k * a, k * b, k * c)
            self.assertEqual(large == base ** (k * k), c == 0 or k == 1)

    def test_central_antidiagonal_is_not_pointwise_fixed(self) -> None:
        # For k=2 both t=k subcells are swapped, although both factors equal R.
        self.assertEqual(check.reflect((1, 2), 2), (2, 1))
        self.assertNotEqual(check.reflect((1, 2), 2), (1, 2))
        check.verify_reflected_factor_identity(q=3, c=2, k=2)

    def test_all_grassmannian_strengthening(self) -> None:
        partition = (5, 3, 3, 0)
        self.assertEqual(check.schur_partition_jacobi_trudi(partition), check.weyl_dimension(partition))
        base = check.weyl_dimension(partition)
        for k in range(1, 5):
            large = check.weyl_dimension(check.inflate_partition(partition, k))
            self.assertGreaterEqual(large, base ** (k * k))
            self.assertEqual(large == base ** (k * k), k == 1)

        constant_partition = (4, 4, 4)
        self.assertEqual(check.weyl_dimension(constant_partition), 1)
        self.assertEqual(check.weyl_dimension(check.inflate_partition(constant_partition, 3)), 1)


if __name__ == "__main__":
    unittest.main()
