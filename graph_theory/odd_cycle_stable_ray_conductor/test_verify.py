#!/usr/bin/env python3
"""Mutation and boundary tests for the stable-ray certificate checker."""

from __future__ import annotations

import unittest

from verify import (
    Witness,
    conductor,
    explicit_witness,
    stable_configuration,
    verify_witness,
)


class StableRayTests(unittest.TestCase):
    def test_boundary_witnesses(self) -> None:
        for k in range(3, 18):
            base = conductor(k)
            for excess in range(9):
                witness = explicit_witness(k, base + excess)
                self.assertTrue(verify_witness(k, base + excess, witness))

    def test_known_first_case(self) -> None:
        self.assertEqual(stable_configuration(3, conductor(3)), (15, 0, 0, 1, 0, 1, 0))
        self.assertEqual(explicit_witness(3, conductor(3)), Witness(0, 0, 2, 1))

    def test_reject_score_mutation(self) -> None:
        k = 8
        heavy = conductor(k)
        witness = explicit_witness(k, heavy)
        changed = Witness(
            witness.cut, witness.left_pile, witness.target, witness.root_score + 1
        )
        self.assertFalse(verify_witness(k, heavy, changed))

    def test_reject_split_mutation(self) -> None:
        k = 7
        heavy = conductor(k) + 1
        witness = explicit_witness(k, heavy)
        changed = Witness(
            witness.cut, witness.left_pile + 1, witness.target, witness.root_score
        )
        self.assertFalse(verify_witness(k, heavy, changed))

    def test_reject_malformed(self) -> None:
        self.assertFalse(verify_witness(5, conductor(5), {"cut": 0}))
        with self.assertRaises(ValueError):
            conductor(2)
        with self.assertRaises(ValueError):
            explicit_witness(5, conductor(5) - 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
