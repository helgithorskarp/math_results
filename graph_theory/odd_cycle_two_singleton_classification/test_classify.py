#!/usr/bin/env python3

from __future__ import annotations

import unittest

from classify import Witness, explicit_witness, stable_pair, verify_witness


class ClassificationTests(unittest.TestCase):
    def test_stable_orbit_has_no_positive_witness(self) -> None:
        for k in range(3, 18):
            for pair in ((k - 1, k + 1), (k, k + 2)):
                self.assertTrue(stable_pair(k, *pair))
                self.assertIsNone(explicit_witness(k, *pair))

    def test_three_central_recoveries_have_score_one(self) -> None:
        for k in range(3, 18):
            for pair in ((k - 2, k + 1), (k, k + 1), (k, k + 3)):
                witness = explicit_witness(k, *pair)
                self.assertIsNotNone(witness)
                assert witness is not None
                self.assertEqual(witness.root_score, 1)
                self.assertTrue(verify_witness(k, *pair, witness))

    def test_reject_mutations_and_bad_inputs(self) -> None:
        witness = explicit_witness(7, 2, 11)
        self.assertIsNotNone(witness)
        assert witness is not None
        self.assertFalse(
            verify_witness(
                7,
                2,
                11,
                Witness(witness.cut, witness.left_pile, witness.target, witness.root_score + 1),
            )
        )
        self.assertFalse(verify_witness(7, 2, 11, {"cut": witness.cut}))
        with self.assertRaises(ValueError):
            explicit_witness(2, 1, 3)
        with self.assertRaises(ValueError):
            explicit_witness(5, 0, 4)
        with self.assertRaises(ValueError):
            explicit_witness(5, 4, 4)


if __name__ == "__main__":
    unittest.main()
