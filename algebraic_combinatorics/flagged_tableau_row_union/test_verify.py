#!/usr/bin/env python3

import unittest

import verify


class RowUnionTests(unittest.TestCase):
    def test_nontrivial_distinct_shapes(self) -> None:
        shapes = ((2, 1), (1, 1))
        flag = (2, 3)
        first = verify.tableaux(shapes[0], flag)[-1]
        second = verify.tableaux(shapes[1], flag)[0]
        image = verify.merge((first, second))
        self.assertTrue(verify.is_flagged_tableau(image, (3, 2), (4, 6)))
        self.assertEqual(verify.split(image, shapes), (first, second))
        self.assertEqual(verify.weight(image), verify.transformed_weight((first, second)))

    def test_column_matching_survives_sorting(self) -> None:
        shapes = ((3, 2), (2, 1), (1, 1))
        flag = (3, 5)
        source = tuple(verify.tableaux(shape, flag)[-1] for shape in shapes)
        image = verify.merge(source)
        self.assertTrue(verify.is_flagged_tableau(image, (6, 4), (9, 15)))
        self.assertEqual(verify.split(image, shapes), source)

    def test_wrong_residue_multiplicity_rejected(self) -> None:
        with self.assertRaises(AssertionError):
            verify.split(((1, 1),), ((1,), (1,)))

    def test_vertical_monotonicity_boundary_failure(self) -> None:
        self.assertEqual(verify.audit_boundary(), {"base": 1, "horizontal": 3, "full_dilation": 1})

    def test_determinant_matches_direct_count(self) -> None:
        shape = (3, 2, 1)
        flag = (2, 4, 5)
        self.assertEqual(verify.flagged_count(shape, flag), len(verify.tableaux(shape, flag)))


if __name__ == "__main__":
    unittest.main()
