#!/usr/bin/env python3
"""Small mathematical controls and deliberate invalid-certificate rejection."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from check import replay


class DeductionChecks(unittest.TestCase):
    def test_two_colour_schur_obstruction(self):
        # Starting from c(1)=1, these five deductions prove S(2)<5.
        steps = [[2, 1, 1, 1], [4, 2, 2, 2], [3, 1, 1, 3],
                 [5, 1, 1, 4], [5, 2, 2, 3]]
        self.assertEqual(replay(5, 2, {1: 1}, steps), (5, 2))

    def test_missing_doubling_deduction_fails(self):
        with self.assertRaises(ValueError):
            replay(5, 2, {1: 1}, [[4, 2, 2, 2]])

    def test_invalid_sum_fails(self):
        with self.assertRaises(ValueError):
            replay(5, 2, {1: 1}, [[4, 1, 1, 1]])

    def test_prefix_certificate_and_mutations(self):
        here = Path(__file__).resolve().parent
        word = (here / "baseline.txt").read_text().strip()
        seeds = {x: int(word[x - 1]) for x in range(1, 82)}
        steps = json.loads((here / "prefix81_proof.json").read_text())["steps"]
        self.assertEqual(replay(537, 6, seeds, steps)[0], 537)
        with self.assertRaises(ValueError):
            replay(537, 6, seeds, steps[:-1])
        bad = deepcopy(steps)
        bad[0][1] = 1 + bad[0][1] % 6
        with self.assertRaises(ValueError):
            replay(537, 6, seeds, bad)
        seeds[81] = 3
        with self.assertRaises(ValueError):
            replay(537, 6, seeds, steps)


if __name__ == "__main__":
    unittest.main()
