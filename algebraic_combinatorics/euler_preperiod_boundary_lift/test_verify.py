#!/usr/bin/env python3
"""Regression tests for the exact boundary-lift audit."""

import unittest

import verify


class BoundaryLiftTests(unittest.TestCase):
    def test_entringer_normalization(self) -> None:
        self.assertEqual(
            verify.euler_up_down_through(9),
            [1, 1, 1, 2, 5, 16, 61, 272, 1385, 7936],
        )

    def test_prime_sieve(self) -> None:
        self.assertEqual(verify.primes_through(13), [3, 5, 7, 11, 13])

    def test_zero_valuation_rejected(self) -> None:
        with self.assertRaises(ValueError):
            verify.valuation(0, 3)

    def test_q_divisible_by_p_cancellation(self) -> None:
        values = verify.euler_up_down_through(19)
        for p, q in ((3, 3), (5, 5)):
            index = q * (p - 1) - 1
            self.assertEqual(
                verify.valuation(values[index], p),
                verify.wieferich_order(p) - 1,
            )

    def test_classical_wieferich_orders(self) -> None:
        self.assertEqual(verify.wieferich_order(1093), 2)
        self.assertEqual(verify.wieferich_order(3511), 2)
        self.assertEqual(verify.second_fermat_quotient_mod_p(1093), 487)
        self.assertEqual(verify.second_fermat_quotient_mod_p(3511), 51)

    def test_limit_guard(self) -> None:
        with self.assertRaises(ValueError):
            verify.run(100)


if __name__ == "__main__":
    unittest.main()
