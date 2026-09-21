import unittest

from verify import (
    THREE_TORSION_ROWS,
    TWO_TORSION_ROWS,
    determinant,
    forbidden_targets,
    in_integer_row_lattice,
    least_separator_modulus,
    quotient_separates,
    row_subgroup_mod,
)


class SeparatorTests(unittest.TestCase):
    def test_bareiss_determinant(self):
        self.assertEqual(determinant(((1, 2), (3, 4))), -2)
        self.assertEqual(determinant(((2, 0, 0), (0, 3, 0), (0, 0, 5))), 30)
        self.assertEqual(determinant(((1, 2), (2, 4))), 0)

    def test_integer_membership_distinguishes_saturation(self):
        rows = ((2, 0),)
        self.assertFalse(in_integer_row_lattice(rows, (1, 0)))
        self.assertTrue(in_integer_row_lattice(rows, (2, 0)))
        self.assertFalse(in_integer_row_lattice(rows, (0, 1)))

    def test_characteristic_two_separator(self):
        targets = forbidden_targets(6)
        self.assertEqual(least_separator_modulus(TWO_TORSION_ROWS, targets, 8), 2)
        self.assertTrue(quotient_separates(TWO_TORSION_ROWS, targets, 2))
        self.assertEqual(len(row_subgroup_mod(TWO_TORSION_ROWS, 6, 2)), 8)

    def test_characteristic_three_separator(self):
        targets = forbidden_targets(6)
        self.assertFalse(quotient_separates(THREE_TORSION_ROWS, targets, 2))
        self.assertEqual(least_separator_modulus(THREE_TORSION_ROWS, targets, 8), 3)
        self.assertTrue(quotient_separates(THREE_TORSION_ROWS, targets, 3))
        self.assertEqual(len(row_subgroup_mod(THREE_TORSION_ROWS, 6, 3)), 81)

    def test_terminal_rejected(self):
        with self.assertRaises(ValueError):
            least_separator_modulus(((1, 0, 0),), forbidden_targets(3), 8)

    def test_malformed_inputs(self):
        with self.assertRaises(ValueError):
            row_subgroup_mod(((1, 0), (1,)), 2, 3)
        with self.assertRaises(ValueError):
            quotient_separates((), (), 2)
        with self.assertRaises(ValueError):
            row_subgroup_mod((), 2, 1)


if __name__ == "__main__":
    unittest.main()
