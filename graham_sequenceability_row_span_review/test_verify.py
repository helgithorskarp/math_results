#!/usr/bin/env python3
import unittest

import verify


class RowSpanReviewTests(unittest.TestCase):
    def test_archived_branch_reconstruction(self):
        orderings, rows = verify.reconstruct_branch()
        self.assertEqual(rows, verify.ROWS)
        self.assertEqual(orderings[-1], (2, 1, 3, 5, 4, 6))

    def test_first_rational_terminal(self):
        self.assertEqual(
            [verify.rational_terminals(verify.ROWS[:d]) for d in range(1, 5)],
            [[], [], [], ["e5"]],
        )

    def test_saturation_index(self):
        nonzero = [value for value in verify.maximal_minors(verify.ROWS) if value]
        self.assertEqual(set(nonzero), {-2, 2})

    def test_claimed_group_assignment(self):
        self.assertTrue(verify.countermodel(verify.CLAIMED_LABELS))

    def test_exhaustive_group_assignments(self):
        self.assertEqual(len(verify.enumerate_countermodels()), 168)


if __name__ == "__main__":
    unittest.main(verbosity=2)
