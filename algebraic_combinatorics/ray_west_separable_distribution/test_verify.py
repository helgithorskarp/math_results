import itertools
import unittest

import verify


class RayWestSeparableTests(unittest.TestCase):
    def test_first_coefficients(self) -> None:
        series = verify.algebraic_coefficients(7)
        self.assertEqual(series[1], (1,))
        self.assertEqual(series[2], (0, 2))
        self.assertEqual(series[3], (0, 0, 6))
        self.assertEqual(series[4], (0, 0, 8, 14))
        self.assertEqual(series[7], (0, 0, 116, 432, 692, 440, 126))

    def test_quadratic_residual(self) -> None:
        series = verify.algebraic_coefficients(20)
        for degree in range(21):
            self.assertEqual(verify.residual_coefficient(series, degree), verify.ZERO)

    def test_original_insertion_definition_through_five(self) -> None:
        counts = []
        for n in range(1, 6):
            count = 0
            for permutation in itertools.permutations(range(1, n + 1)):
                tree_value = verify.canonical_tree_j(permutation)
                if tree_value is None:
                    continue
                self.assertEqual(tree_value, verify.active_insertion_j(permutation))
                count += 1
            counts.append(count)
        self.assertEqual(counts, [1, 2, 6, 22, 90])

    def test_nonseparable_basis(self) -> None:
        self.assertIsNone(verify.canonical_tree_j((2, 4, 1, 3)))
        self.assertIsNone(verify.canonical_tree_j((3, 1, 4, 2)))

    def test_monotone_values(self) -> None:
        for n in range(1, 9):
            increasing = tuple(range(1, n + 1))
            decreasing = tuple(range(n, 0, -1))
            self.assertEqual(verify.canonical_tree_j(increasing), n - 1)
            self.assertEqual(verify.canonical_tree_j(decreasing), n - 1)

    def test_first_moment_identity(self) -> None:
        verify.verify_first_moment_identity(verify.algebraic_coefficients(30))

    def test_argument_validation(self) -> None:
        with self.assertRaises(ValueError):
            verify.algebraic_coefficients(0)
        with self.assertRaises(ValueError):
            verify.exhaustive_histograms(0)
        with self.assertRaises(ValueError):
            verify.run(5, 6)


if __name__ == "__main__":
    unittest.main()
