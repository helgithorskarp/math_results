#!/usr/bin/env python3
import unittest

import verify


class BlockerAuditTests(unittest.TestCase):
    def test_disjoint_orbit_criterion(self):
        caps = verify.capacities(3, 4, 5)
        self.assertTrue(
            verify.disjoint_representatives_exist(
                (1, 1, 0, 2, 0, 1), (0, 1, 1, 1, 1, 2), caps
            )
        )
        self.assertFalse(
            verify.disjoint_representatives_exist(
                (1, 1, 0, 2, 0, 1), (1, 0, 0, 0, 0, 0), caps
            )
        )

    def test_startup_asymmetric_large_widths(self):
        result = verify.assert_startup(4, 7, 11)
        self.assertEqual(result["type_box"], 2464)

    def test_full_boundary_orbit(self):
        result = verify.assert_full_orbit(3, 3, 3)
        self.assertEqual(result["period"], 11)

    def test_full_asymmetric_orbit(self):
        result = verify.assert_full_orbit(3, 4, 5)
        self.assertEqual(result["period"], 14)

    def test_direct_boolean_lattice_cross_check(self):
        result = verify.assert_labeled_333()
        self.assertEqual(result["states"], 11)


if __name__ == "__main__":
    unittest.main(verbosity=2)
