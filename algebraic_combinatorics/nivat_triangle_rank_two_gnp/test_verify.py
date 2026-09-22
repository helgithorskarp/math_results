import unittest

import verify


class PeriodicMaskTests(unittest.TestCase):
    def test_trivial_norm(self):
        poly = {(0, 0): 2, (1, 0): -1, (0, 1): 3}
        self.assertEqual(verify.orbit_norm(poly, 1, 1), poly)

    def test_norm_support_and_factor(self):
        poly = {(0, 0): 1, (1, 0): -1, (0, 1): -1, (1, 1): 1}
        record = verify.norm_audit(poly, 2, 3)
        self.assertTrue(record["support_in_period_sublattice"])
        self.assertGreater(record["quotient_terms"], 0)

    def test_periodic_multiplier_transfer(self):
        record = verify.transfer_audit()
        self.assertTrue(record["periodic_multiplier_transfer"])
        self.assertEqual(record["commutation_entries"], 144)

    def test_triangle_component_identity(self):
        record = verify.triangle_audit()
        self.assertEqual(record["component_triples"], 32768)
        self.assertTrue(record["four_dot_plus_periodic_mask_identity"])

    def test_invalid_period(self):
        with self.assertRaises(ValueError):
            verify.orbit_norm({(0, 0): 1}, 0, 2)


if __name__ == "__main__":
    unittest.main()
