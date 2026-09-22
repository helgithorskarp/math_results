#!/usr/bin/env python3
"""Unit tests for the exact discriminant audit."""

from fractions import Fraction
import unittest

import verify


class DiscriminantAuditTests(unittest.TestCase):
    def test_quadratic_field_relation(self) -> None:
        rho = (Fraction(0), Fraction(1))
        self.assertEqual(
            verify.qmultiply(rho, rho),
            (Fraction(-1), Fraction(6)),
        )

    def test_quadratic_field_inverse(self) -> None:
        value = (Fraction(5), Fraction(-2))
        self.assertEqual(
            verify.qmultiply(value, verify.qinverse(value)),
            (Fraction(1), Fraction(0)),
        )

    def test_discriminant_specialization(self) -> None:
        self.assertEqual(
            verify.specialize_u_one(verify.construct_discriminant()),
            [1, -10, 31, -44, 31, -10, 1],
        )

    def test_complete_audit(self) -> None:
        result = verify.run()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["rho_prime"], "-rho/2")
        self.assertEqual(result["rho_second"], "(-1+7*rho)/2")
        self.assertTrue(result["variance_positive"])

    def test_mutated_discriminant_is_rejected(self) -> None:
        discriminant = verify.construct_discriminant()
        discriminant[(1, 0)] += 1
        self.assertNotEqual(
            verify.specialize_u_one(discriminant),
            [1, -10, 31, -44, 31, -10, 1],
        )


if __name__ == "__main__":
    unittest.main()
