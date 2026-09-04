#!/usr/bin/env python3
import unittest

from independent_check import (
    compose,
    exact_rectangle_partition,
    explicit_hamming_witness,
    family_arithmetic,
    validate_partition,
)


class ModularSlabReviewTests(unittest.TestCase):
    def test_independent_rectangle_search(self) -> None:
        parts = exact_rectangle_partition(8, 7, 5)
        validate_partition(parts, (8, 7), 5)
        self.assertEqual(len(parts), 11)

    def test_composition_beyond_old_criterion(self) -> None:
        base = exact_rectangle_partition(8, 7, 5)
        parts = compose(base, (8, 7), 7, 5)
        self.assertEqual(len(parts), 78)

    def test_failed_residue_condition_is_rejected(self) -> None:
        base = exact_rectangle_partition(7, 7, 5)
        with self.assertRaises(ValueError):
            compose(base, (7, 7), 4, 5)

    def test_explicit_family_and_hamming_witness(self) -> None:
        self.assertEqual(family_arithmetic(20), 19)
        self.assertEqual(explicit_hamming_witness(), (4704, 78, 15, 16))


if __name__ == "__main__":
    unittest.main()
