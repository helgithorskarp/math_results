#!/usr/bin/env python3
"""Focused exact tests for the circulant K_43 classification verifier."""

from __future__ import annotations

import itertools
import unittest

import verify_classification as verify


class ClassificationTests(unittest.TestCase):
    def test_translation_and_multiplier_preserve_distance_masks(self) -> None:
        vertices = (0, 1, 2, 22, 23)
        expected = verify.distance_mask(vertices)
        for shift in range(verify.ORDER):
            translated = tuple((x + shift) % verify.ORDER for x in vertices)
            self.assertEqual(verify.distance_mask(translated), expected)
        for multiplier in range(1, verify.ORDER):
            image_vertices = tuple(multiplier * x % verify.ORDER for x in vertices)
            self.assertEqual(
                verify.distance_mask(image_vertices),
                verify.multiplier_image(expected, multiplier),
            )

    def test_each_canonical_five_set_has_free_orbit(self) -> None:
        sample = (0, 3, 13, 23, 33)
        images = {
            tuple(sorted((x + shift) % verify.ORDER for x in sample))
            for shift in range(verify.ORDER)
        }
        self.assertEqual(len(images), verify.ORDER)
        anchored = [image for image in images if 0 in image]
        self.assertEqual(len(anchored), 5)
        self.assertEqual(verify.canonical_translate(sample), sample)

    def test_exoo_clique_orbit_from_definitions(self) -> None:
        red = verify.mask_from_lengths(verify.EXOO_LENGTHS)
        red_witness = (0, 1, 2, 22, 23)
        self.assertEqual(verify.distance_mask(red_witness) & ~red, 0)
        for shift in range(verify.ORDER):
            witness = tuple((x + shift) % verify.ORDER for x in red_witness)
            self.assertEqual(verify.distance_mask(witness) & ~red, 0)

        # A complete direct five-set count independently checks the familiar
        # 43-red, zero-blue Cyclic(43) objective.
        red_count = blue_count = 0
        for vertices in itertools.combinations(range(verify.ORDER), 5):
            mask = verify.distance_mask(vertices)
            red_count += mask & ~red == 0
            blue_count += mask & red == 0
        self.assertEqual((red_count, blue_count), (43, 0))


if __name__ == "__main__":
    unittest.main()
