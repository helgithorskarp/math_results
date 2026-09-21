import unittest

import verify


class DirectionalRankTests(unittest.TestCase):
    def test_gauge_parity_boundary(self):
        self.assertEqual(verify.gauge_audit(1)["gauge_kernel"], 4)
        self.assertEqual(verify.gauge_audit(2)["gauge_kernel"], 8)

    def test_period_criterion_small(self):
        self.assertEqual(verify.period_audit(2)["translation_tests"], 256)

    def test_polynomial_divisibility_substitutions(self):
        x = verify.factor(1, 0)
        y = verify.factor(0, 1)
        xy = verify.factor(1, 1)
        f = verify.mul_poly(verify.mul_poly(x, y), xy)
        self.assertFalse(verify.avoids_x_plus_one(f))
        self.assertFalse(verify.avoids_y_plus_one(f))
        self.assertFalse(verify.avoids_xy_plus_one(f))

    def test_factor_avoiding_annihilators(self):
        result = verify.factor_avoidance_audit()
        self.assertEqual(result["annihilation_checks"], 3072)


if __name__ == "__main__":
    unittest.main()
