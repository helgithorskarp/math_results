import unittest

from verify import audit_instance, majority_threshold, make_instance


class SecondCarryArithmeticTests(unittest.TestCase):
    def test_first_family_member(self) -> None:
        instance = make_instance(8, 2)
        self.assertEqual(
            (instance.n1, instance.m, instance.n, instance.p, instance.h, instance.Q),
            (33, 25, 20, 4, 39, 248),
        )
        audit_instance(instance)

    def test_larger_family_member(self) -> None:
        instance = make_instance(14, 7)
        self.assertEqual(instance.h - (instance.n1 - 1) + 1, 14)
        self.assertEqual((instance.m % 14) * (instance.n % 14) * instance.p, 28)
        audit_instance(instance)

    def test_threshold_rounding(self) -> None:
        self.assertEqual(majority_threshold(33, 25, 20, 4), 39)
        self.assertEqual(majority_threshold(47, 37, 28, 6), 57)

    def test_reject_odd_s(self) -> None:
        with self.assertRaisesRegex(ValueError, "even"):
            make_instance(9, 2)

    def test_reject_small_A(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least 2"):
            make_instance(8, 1)


if __name__ == "__main__":
    unittest.main()
