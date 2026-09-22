"""Small independent checks of the checker, not a second proof of the theorem."""
import unittest
from itertools import combinations, combinations_with_replacement
import verify as v


class ExactChecks(unittest.TestCase):
    def test_cyclotomic_known(self):
        self.assertEqual(v.phi(6), (1, -1, 1))
        self.assertEqual(v.phi(12), (1, 0, -1, 0, 1))
        self.assertEqual(v.phi(8), (1, 0, 0, 0, 1))

    def test_independent_zero_tests(self):
        for n in range(1, 13):
            for k in range(5):
                for exponents in combinations_with_replacement(range(n), k):
                    self.assertEqual(v.zero(n, exponents), v.trace_zero(n, exponents))

    def test_clique_against_literal_all_spectra(self):
        for n in range(2, 9):
            for k in range(1, n + 1):
                for points in v.normalized_subsets(n, k):
                    brute = any(v.spectral_pair(n, points, spectrum, v.trace_zero)
                                for spectrum in v.normalized_subsets(n, k))
                    self.assertEqual(v.find_spectrum(n, points) is not None, brute)

    def test_all_pair_valuations(self):
        for n in (2, 4, 6, 8, 12, 16):
            for t in range(v.v2(n)):
                pairs = [a for a in combinations(range(n), 2)
                         if v.v2(a[1] - a[0]) == t]
                self.assertEqual(len(pairs), n * n // 2 ** (t + 2))

    def test_extraction_and_mutations(self):
        pairs = [(0, 3), (4, 7), (8, 11)]
        result = v.extract_paired(12, 3, pairs, [2, 10, 3, 9])
        self.assertEqual(result['points'], [0, 4, 8])
        with self.assertRaises(ValueError):
            v.extract_paired(12, 3, [(0, 0), (4, 7), (8, 11)], [2, 10, 3, 9])
        with self.assertRaises(ValueError):
            v.extract_paired(12, 3, pairs, [2, 10, 3, 3])
        with self.assertRaises(ValueError):
            v.extract_paired(12, 3, pairs, [2, 10, 3, 8])

    def test_input_rejections(self):
        self.assertEqual(v.audit_bad_inputs(), 6)

    def test_mixed_valuations_rejected(self):
        self.assertIsNone(v.binary_valuation(8, [[0, 1], [0, 2], [0, 3]]))
        self.assertIsNone(v.binary_valuation(8, [[0], [0, 1, 2], [0, 3]]))

    def test_translation_normalization_count(self):
        for n, p in ((4, 3), (8, 3), (4, 5)):
            total = sum((n * n // 2 ** (t + 2)) ** p for t in range(v.v2(n)))
            containing_zero = sum((n // 2 ** (t + 1)) *
                                  (n * n // 2 ** (t + 2)) ** (p - 1)
                                  for t in range(v.v2(n)))
            self.assertEqual(total * 2, containing_zero * n)


if __name__ == '__main__':
    unittest.main()
