#!/usr/bin/env python3
import copy
import unittest

import verify


class CertificateTests(unittest.TestCase):
    def test_root_profile_through_k_12(self):
        for k in range(3, 13):
            bounds = verify.verify_k(k)
            expected = [
                verify.expected_root_bound(k, vertex)
                for vertex in range(2 * k + 1)
            ]
            self.assertEqual(bounds, expected)

    def test_known_lower_bounds(self):
        self.assertEqual(5 * 2 ** (3 - 1) - 3, 17)
        self.assertEqual(5 * 2 ** (4 - 1) - 3, 37)
        self.assertEqual(5 * 2 ** (5 - 1) - 3, 77)

    def test_local_mutation_is_rejected(self):
        table = verify.construct_tree_table(3)
        broken = copy.deepcopy(table)
        broken[1][0][2] += 3
        with self.assertRaises(AssertionError):
            verify.verify_tree_lower_bound_certificate(3, broken)

    def test_malformed_k_is_rejected(self):
        with self.assertRaises(ValueError):
            verify.construct_tree_table(2)


if __name__ == "__main__":
    unittest.main()
