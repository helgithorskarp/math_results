#!/usr/bin/env python3

from __future__ import annotations

import unittest
from collections import Counter

import verify


class ModuleIndependenceTests(unittest.TestCase):
    def test_three_element_sharp_witness(self) -> None:
        record = verify.audit_sharpness()
        self.assertEqual(record["ambient_restriction_counts"], [2, 1])

    def test_whole_poset_is_a_module(self) -> None:
        order = (0b110, 0b100, 0)
        self.assertTrue(verify.is_module(order, 0b111))

    def test_nonautonomous_subset_detected(self) -> None:
        order = (0b100, 0, 0)
        self.assertFalse(verify.is_module(order, 0b011))

    def test_module_fibres_equal(self) -> None:
        # Lexicographic sum of the two-element antichain with C2 and A2.
        skeleton = (0, 0)
        blocks = ((0b10, 0), (0, 0))
        order, vertices = verify.lexicographic_sum(skeleton, blocks)
        words = verify.extensions_on(order, 0b1111)
        fibres = Counter(verify.restrict_word(word, 0b0011) for word in words)
        self.assertEqual(fibres, Counter({(0, 1): 12}))
        coordinates = [verify.block_coordinates(word, vertices) for word in words]
        self.assertEqual(len(coordinates), len(set(coordinates)))

    def test_comparable_blocks_do_not_interleave(self) -> None:
        skeleton = (0b10, 0)
        words = verify.admissible_block_words(skeleton, (2, 2))
        self.assertEqual(words, ((0, 0, 1, 1),))


if __name__ == "__main__":
    unittest.main()
