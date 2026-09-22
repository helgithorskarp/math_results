import unittest
from fractions import Fraction

from verify import (
    audit,
    gaussian_product,
    gaussian_recurrence,
    is_exception,
    q_kneser_counts,
)


class QKneserAuditTests(unittest.TestCase):
    def test_gaussian_known_values_and_two_implementations(self) -> None:
        self.assertEqual(gaussian_recurrence(4, 2, 2), 35)
        self.assertEqual(gaussian_recurrence(5, 2, 2), 155)
        for q in range(2, 8):
            for n in range(1, 9):
                for k in range(n + 1):
                    self.assertEqual(
                        gaussian_recurrence(n, k, q),
                        gaussian_product(n, k, q),
                    )

    def test_named_instances(self) -> None:
        self.assertEqual(q_kneser_counts(2, 5, 2), (155, 112, 15, 140))
        self.assertEqual(q_kneser_counts(2, 4, 2), (35, 16, 7, 28))
        self.assertEqual(q_kneser_counts(3, 4, 2), (130, 81, 13, 117))

    def test_exact_ratio_product(self) -> None:
        for q in range(2, 6):
            for r in range(1, 6):
                for n in range(2 * r, 2 * r + 4):
                    N, d, _, _ = q_kneser_counts(q, n, r)
                    product = Fraction(1, 1)
                    for j in range(r):
                        product *= Fraction(
                            q ** (n - j) - q**r,
                            q ** (n - j) - 1,
                        )
                    self.assertEqual(Fraction(d, N), product)

    def test_density_classification(self) -> None:
        result = audit(max_q=10, max_r=7, max_excess=5)
        self.assertEqual(result["classification_failures"], 0)
        self.assertEqual(result["excluded_binary_middle_cases"], 6)
        self.assertFalse(is_exception(2, 2, 1))
        self.assertTrue(is_exception(2, 4, 2))

    def test_invalid_parameters(self) -> None:
        with self.assertRaises(ValueError):
            gaussian_recurrence(2, 3, 2)
        with self.assertRaises(ValueError):
            q_kneser_counts(2, 3, 2)
        with self.assertRaises(ValueError):
            audit(max_q=1, max_r=2, max_excess=0)


if __name__ == "__main__":
    unittest.main()
