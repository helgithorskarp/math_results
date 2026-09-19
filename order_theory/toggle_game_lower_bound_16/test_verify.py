#!/usr/bin/env python3
from __future__ import annotations

import unittest

from verify_small import mobius_to_top, parse_cats, transitive_order, winning_sequence


class ToggleVerifierTests(unittest.TestCase):
    def test_cats_decoder_order_four(self) -> None:
        # Positions are (2,1),(3,1),(3,2),(4,1),(4,2),(4,3).
        self.assertEqual(parse_cats("1.1.11", 4), [(1, 0), (2, 1), (3, 1), (3, 2)])

    def test_chain_is_winnable(self) -> None:
        covers = [(1, 0), (2, 1), (3, 2)]
        sequence = winning_sequence(4, covers, 0)
        self.assertIsNotNone(sequence)

    def test_diamond_is_winnable(self) -> None:
        # Catalogue orientation: (lower, upper), with vertex zero the top.
        covers = [(1, 0), (2, 0), (3, 1), (3, 2)]
        sequence = winning_sequence(4, covers, 0)
        self.assertIsNotNone(sequence)

    def test_diamond_mobius_values(self) -> None:
        covers = [(1, 0), (2, 0), (3, 1), (3, 2)]
        leq = transitive_order(4, covers)
        self.assertEqual(mobius_to_top(4, leq, 0), {0: 1, 1: -1, 2: -1, 3: 1})

    def test_malformed_cats_length(self) -> None:
        with self.assertRaises(AssertionError):
            parse_cats("1.1", 4)


if __name__ == "__main__":
    unittest.main()
