#!/usr/bin/env python3

import unittest

import verify


class LocalIrregularityTests(unittest.TestCase):
    def test_initial_zigzag_values_by_two_methods(self) -> None:
        expected = [1, 1, 1, 2, 5, 16, 61, 272, 1385, 7936]
        for p in (43, 67):
            self.assertEqual(
                verify.zigzag_mod_ode(p, len(expected) - 1),
                [value % p for value in expected],
            )
            self.assertEqual(
                verify.zigzag_mod_entringer(p, len(expected) - 1),
                [value % p for value in expected],
            )

    def test_small_bernoulli_values(self) -> None:
        for p in (7, 11, 43):
            values = verify.bernoulli_mod(p)
            self.assertEqual(values[1], -pow(2, -1, p) % p)
            self.assertEqual(values[2], pow(6, -1, p))
            self.assertEqual(values[3], 0)
            self.assertEqual(values[4], -pow(30, -1, p) % p)

    def test_strict_mixed_irregular_example(self) -> None:
        p = 67
        zigzag = verify.zigzag_mod_ode(p)
        bernoulli = verify.bernoulli_mod(p)
        e_set, b_set, _, order, wieferich = verify.irregular_data(
            p, zigzag, bernoulli
        )
        self.assertEqual(e_set, {26})
        self.assertEqual(b_set, {58})
        self.assertEqual(order, 66)
        self.assertFalse(wieferich)
        self.assertEqual(verify.actual_triple_starts(p, zigzag), set())
        self.assertEqual(verify.predicted_triple_starts(p, zigzag, bernoulli), set())

    def test_near_miss_at_43(self) -> None:
        p = 43
        zigzag = verify.zigzag_mod_ode(p)
        bernoulli = verify.bernoulli_mod(p)
        self.assertIn(12, verify.consecutive_pair_starts(p, zigzag))
        self.assertNotEqual(zigzag[14], 0)
        self.assertEqual(verify.actual_triple_starts(p, zigzag), set())
        self.assertEqual(verify.predicted_triple_starts(p, zigzag, bernoulli), set())

    def test_wieferich_boundary_pair_not_triple(self) -> None:
        p = 1093
        zigzag = verify.zigzag_mod_ode(p)
        bernoulli = verify.bernoulli_mod(p)
        self.assertEqual(pow(2, p - 1, p * p), 1)
        self.assertEqual(zigzag[p - 2], 0)
        self.assertEqual(zigzag[p - 1], 0)
        self.assertEqual(zigzag[1], 1)
        self.assertEqual(verify.actual_triple_starts(p, zigzag), set())
        self.assertEqual(verify.predicted_triple_starts(p, zigzag, bernoulli), set())

    def test_reject_bad_inputs(self) -> None:
        with self.assertRaises(ValueError):
            verify.zigzag_mod_ode(2)
        with self.assertRaises(ValueError):
            verify.zigzag_mod_entringer(5, -1)
        with self.assertRaises(ValueError):
            verify.positive_residue(0, 5)


if __name__ == "__main__":
    unittest.main()
