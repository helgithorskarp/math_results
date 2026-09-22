import unittest

import verify


class RegularResidueLiftTests(unittest.TestCase):
    def test_first_euler_numbers(self):
        targets = set(range(9))
        got = verify.entringer_targets_mod(targets, 10**9)
        self.assertEqual(
            [got[n] for n in range(9)],
            [1, 1, 1, 2, 5, 16, 61, 272, 1385],
        )

    def test_irregular_residues(self):
        self.assertEqual(verify.bernoulli_mod_prime(37)[32], 0)
        self.assertEqual(verify.bernoulli_mod_prime(59)[44], 0)
        self.assertEqual(verify.bernoulli_mod_prime(67)[58], 0)

    def test_first_order_only_profile(self):
        prime = 17
        bernoulli = verify.bernoulli_mod_prime(prime)
        order = verify.order_of_two(prime)
        residues = [
            j
            for j in range(2, prime - 2, 2)
            if bernoulli[j] and j % order == 0
        ]
        self.assertEqual(order, 8)
        self.assertEqual(residues, [8])

    def test_v_p_m_term_is_essential(self):
        prime, j, q = 17, 8, 8
        m = j + q * (prime - 1)
        value = verify.entringer_targets_mod({m - 1}, prime**6)[m - 1]
        actual = verify.valuation_from_residue(value, prime, 6)
        self.assertEqual(m, 8 * prime)
        self.assertEqual(actual, 2)
        self.assertNotEqual(actual, verify.valuation(pow(2, prime - 1) - 1, prime))

    def test_p_squared_divides_m(self):
        prime, j, q = 17, 8, 8 * 18
        m = j + q * (prime - 1)
        value = verify.entringer_targets_mod({m - 1}, prime**6)[m - 1]
        actual = verify.valuation_from_residue(value, prime, 6)
        self.assertEqual(m, 8 * prime**2)
        self.assertEqual(actual, 3)

    def test_wieferich_and_boundary_are_distinct(self):
        audit = verify.audit_wieferich_prime()
        self.assertEqual(audit["w_p"], 2)
        self.assertEqual(set(audit["interior_valuations"].values()), {2})
        self.assertEqual(audit["boundary_v_p_A_p_minus_2"], 1)

    def test_irregular_hypothesis_cannot_be_removed(self):
        audit = verify.audit_irregular_boundary()
        self.assertEqual(audit["v_p_A_j_minus_1"], 1)
        self.assertEqual(audit["v_p_2_to_j_minus_1"], 0)

    def test_rejects_invalid_residue(self):
        with self.assertRaises(ValueError):
            verify.valuation_from_residue(17**6, 17, 6)


if __name__ == "__main__":
    unittest.main()
