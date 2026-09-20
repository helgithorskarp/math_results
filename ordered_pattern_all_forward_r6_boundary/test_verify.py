#!/usr/bin/env python3
"""Small hand-checkable tests for verify.py."""

import unittest

import verify


class RankSixBoundaryTests(unittest.TestCase):
    def test_occurrence_classification_small(self):
        for m in (2, 3):
            self.assertEqual(
                set(verify.direct_occurrences(m).values()),
                set(verify.modeled_occurrences(m).values()),
            )

    def test_type_counts(self):
        for m in (2, 5):
            n = 6 * m + 2
            half = n // 2
            modeled = verify.modeled_occurrences(m)
            self.assertEqual(
                [sum(kind == band for kind, _ in modeled) for band in range(4)],
                [n, n, n, half],
            )

    def test_blocker(self):
        for m in (2, 3, 6):
            blocker = verify.blocker_edges(m)
            self.assertEqual(len(blocker), 28)
            self.assertTrue(all(copy & blocker for _, copy in verify.canonical_copies(m)))

    def test_transversal_number(self):
        intervals = (0b0011, 0b0110, 0b1100)
        self.assertEqual(verify.transversal_number(intervals), 2)
        disjoint = (0b0001, 0b0010, 0b0100, 0b1000)
        self.assertEqual(verify.transversal_number(disjoint), 4)

    def test_tight_propagation_example(self):
        m = 3
        deficits = (0, 0, 0, 0, 2, 0, 0, 2)
        js, ks, _ = verify.repair_intervals(m, deficits)
        self.assertEqual(verify.transversal_number(js), 8)
        self.assertEqual(verify.transversal_number(ks), 4)
        self.assertTrue(
            all(
                sum(deficits[(i + offset) % 8] for offset in range(3)) <= m - 1
                for i in range(8)
            )
        )


if __name__ == "__main__":
    unittest.main()
