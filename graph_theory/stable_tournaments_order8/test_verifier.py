#!/usr/bin/env python3

import unittest

from verify_certificates import (
    check_m2,
    is_transitive,
    order_matrix,
    parse_order,
    tournament_matrix,
)


class VerifierTests(unittest.TestCase):
    def test_order_validation(self) -> None:
        self.assertEqual(parse_order("0,1,2,3,4,5,6,7"), tuple(range(8)))
        with self.assertRaises(ValueError):
            parse_order("0,1,2,3,4,5,6,6")

    def test_transitive_masks(self) -> None:
        self.assertTrue(is_transitive(tournament_matrix(0)))
        self.assertTrue(is_transitive(tournament_matrix((1 << 28) - 1)))
        self.assertFalse(is_transitive(tournament_matrix(251457479)))

    def test_first_m2_witness(self) -> None:
        orders = [
            (0, 1, 2, 3, 4, 5, 6, 7),
            (0, 1, 2, 3, 5, 6, 7, 4),
            (1, 2, 7, 3, 0, 6, 5, 4),
            (0, 5, 2, 6, 4, 1, 3, 7),
            (0, 3, 1, 4, 2, 5, 6, 7),
        ]
        check_m2(830, 251457479, orders)

    def test_order_matrix_scores(self) -> None:
        matrix = order_matrix((3, 0, 7, 2, 1, 6, 4, 5))
        self.assertEqual(sorted(map(sum, matrix)), list(range(8)))


if __name__ == "__main__":
    unittest.main()
