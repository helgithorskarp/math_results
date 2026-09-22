"""Boundary, hand-checkable, and rejection tests; active under python -O."""

from fractions import Fraction
import unittest

import direct
import layers
import verify


class ExactTests(unittest.TestCase):
    def test_gaussian_normalization(self):
        self.assertEqual(layers.gaussian(0,0), (1,))
        self.assertEqual(layers.gaussian(4,2), (1,1,2,1,1))
        self.assertEqual(layers.gaussian(5,2), (1,1,2,2,2,1,1))

    def test_lucas_initial_values(self):
        self.assertEqual(direct.lucas(0), (0,))
        self.assertEqual(direct.lucas(1), (1,))
        self.assertEqual(direct.lucas(3), (1,3,1))
        self.assertEqual(layers.lucas_schur(2), (1,2))
        self.assertEqual(layers.lucas_schur(4), (1,6,6))

    def test_first_case(self):
        # D_(3,4)=e2^3 F_7; F_7=e1^6+5e1^4 e2+6e1^2 e2^2+e2^3.
        self.assertEqual(layers.comparison(3,4), (0,0,0,1,10,30,22))
        self.assertEqual(direct.comparison(3,4), (0,0,0,1,10,30,22))

    def test_exact_degenerate_family(self):
        for c in range(2,15):
            self.assertEqual(layers.comparison(2,c), (0,)*(c+1))
            self.assertEqual(direct.comparison(2,c), (0,)*(c+1))

    def test_threshold_and_parity(self):
        for pair in ((3,10),(4,10),(4,11),(3,12),(11,12)):
            self.assertTrue(all(v > 0 for v in verify.audit_case(*pair)[3:]))
        for pair in ((3,3),(3,11),(4,3),(1,12),(True,4),(4.0,6)):
            for implementation in (direct.comparison, layers.comparison):
                with self.assertRaises(ValueError):
                    implementation(*pair)

    def test_bad_algebra_inputs(self):
        with self.assertRaises(ArithmeticError):
            direct.divide_exact((1,0,1), (1,1))
        with self.assertRaises(ValueError):
            direct.divide_exact((1,1), (1,2))
        with self.assertRaises(ValueError):
            direct.to_schur((1,2))
        with self.assertRaises(ValueError):
            layers.gaussian(4,5)
        with self.assertRaises(ValueError):
            layers.lucas_schur(-1)
        with self.assertRaises(ValueError):
            direct.lucas(-1)

    def test_tail_budget(self):
        report = layers.tail_budget()
        self.assertEqual(Fraction(report['schur_margin']), Fraction(31,960))
        self.assertLess(Fraction(report['euler_product_upper']), Fraction(52,15))

    def test_base_digest(self):
        report = verify.run()
        self.assertEqual(report['finite_base_cases'], 26)
        self.assertEqual(report['finite_base_schur_coefficients'], 612)
        self.assertEqual(report['finite_base_records_sha256'],
                         '1e1751f231acf03752aa07866d11690eec18673233985e10c391462839d84910')


if __name__ == '__main__':
    unittest.main()
