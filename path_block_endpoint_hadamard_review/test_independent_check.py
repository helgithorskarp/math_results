import unittest

import independent_check as audit


class EndpointHadamardAuditTests(unittest.TestCase):
    def test_definition_level_counts(self) -> None:
        self.assertEqual(audit.verify_definition_level_counts(), 168)

    def test_rectangular_heterogeneous_formula(self) -> None:
        left = (3, 3)
        right = (3, 3, 3)
        self.assertEqual(
            audit.endpoint_hstar_polynomial(left, right),
            [1, 0, 0, 6, 0, 0, 3],
        )

    def test_nonmatching_rectangles_fail(self) -> None:
        self.assertIsNone(audit.endpoint_hstar_polynomial((2, 2, 2), (3, 3)))

    def test_one_sided_exact_pole(self) -> None:
        numerator, denominator = audit.endpoint_hstar_fraction((4, 2), (1,) * 6)
        for root_order in (2, 4):
            factor = list(audit.cyclotomic(root_order))
            residual = audit.polynomial_valuation(
                denominator, factor
            ) - audit.polynomial_valuation(numerator, factor)
            self.assertEqual(residual, 6)

    def test_scaling_identity(self) -> None:
        left = (2, 1)
        right = (3,)
        base_num, base_den = audit.endpoint_hstar_fraction(left, right)
        scaled_num, scaled_den = audit.endpoint_hstar_fraction((8, 4), (12,))
        expected_num = audit.poly_substitute_power(base_num, 4)
        expected_den = audit.poly_substitute_power(base_den, 4)
        self.assertEqual(
            audit.poly_mul(scaled_num, expected_den),
            audit.poly_mul(expected_num, scaled_den),
        )

    def test_full_report(self) -> None:
        report = audit.verify()
        self.assertEqual(report["equal_width_pairs"], 6718)
        self.assertEqual(report["equal_width_polynomial_pairs"], 29)
        self.assertEqual(report["heterogeneous_pairs"], 4356)


if __name__ == "__main__":
    unittest.main()
