#!/usr/bin/env python3
"""Cross-check the independent colour-compatibility predicate."""

import itertools
import unittest

import independent_dense_orientation as checked


def brute_compatible(left, small):
    return any(
        permutation[small[0]] == left[0]
        and permutation[small[1]] == left[1]
        and all(permutation[small[index]] != left[index] for index in range(2, 8))
        for permutation in itertools.permutations(range(4))
    )


class CompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.partitions = sorted({
            checked.canonical(pattern)
            for pattern in itertools.product(range(4), repeat=8)
        })

    def test_partition_count(self):
        self.assertEqual(len(self.partitions), 2795)

    def test_deterministic_pairs_against_all_permutations(self):
        count = len(self.partitions)
        for index in range(100_000):
            # The quotient/remainder map makes these 100,000 ordered pairs distinct.
            left = self.partitions[index // count]
            small = self.partitions[index % count]
            self.assertEqual(
                checked.compatible(left, small),
                brute_compatible(left, small),
                (left, small),
            )


if __name__ == "__main__":
    unittest.main()
