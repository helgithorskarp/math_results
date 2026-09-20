#!/usr/bin/env python3

import unittest

import verify


class InverseGrassmannianTests(unittest.TestCase):
    def test_inverse_and_inflation_commute(self) -> None:
        w = (2, 0, 3, 1)
        self.assertEqual(
            verify.inverse(verify.inflate_identity(w, 3)),
            verify.inflate_identity(verify.inverse(w), 3),
        )

    def test_non_grassmannian_inverse_grassmannian(self) -> None:
        w = verify.alternating_inverse_grassmannian(4)
        self.assertEqual(verify.descents(w), (0, 2, 4, 6))
        self.assertTrue(verify.is_inverse_grassmannian(w))
        self.assertEqual(
            verify.grassmannian_partition(verify.inverse(w)), (4, 3, 2, 1)
        )

    def test_known_small_value(self) -> None:
        w = (2, 0, 3, 1)  # 3142, inverse of the Grassmannian 2413.
        self.assertEqual(verify.transition_upsilon(w), 2)
        self.assertEqual(verify.transition_upsilon(verify.inflate_identity(w, 2)), 20)

    def test_weyl_strictness_and_equality(self) -> None:
        self.assertGreater(verify.weyl_dimension((4, 4, 2, 2)), 2**4)
        lam = (3, 3)
        self.assertEqual(
            verify.weyl_dimension(verify.inflated_partition(lam, 4)),
            verify.weyl_dimension(lam) ** 16,
        )

    def test_partition_enumerator(self) -> None:
        values = list(verify.partitions_in_box(2, 2))
        self.assertEqual(values, [(2, 2), (2, 1), (2, 0), (1, 1), (1, 0), (0, 0)])


if __name__ == "__main__":
    unittest.main()
