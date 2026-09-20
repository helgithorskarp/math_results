import copy
import unittest

import verify


class VerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = verify.load_certificate()

    def test_classification(self):
        self.assertEqual(verify.branch_patterns(), {(2, 1), (1, 1, 1)})
        self.assertEqual(
            {name: dict(counts) for name, counts in verify.classified_types().items()},
            verify.EXPECTED_TYPES,
        )

    def test_countermodel(self):
        result = verify.verify_countermodel(self.data, count_cycles=False)
        self.assertEqual(result["perfect_matchings"], 276)
        self.assertEqual(result["equations"], 1344)

    def test_reject_duplicate_permutation_value(self):
        bad = copy.deepcopy(self.data)
        bad["permutations"]["0,1"][0] = bad["permutations"]["0,1"][1]
        with self.assertRaises(AssertionError):
            verify.verify_countermodel(bad, count_cycles=False)

    def test_reject_balance_corruption(self):
        bad = copy.deepcopy(self.data)
        p = bad["permutations"]["0,3"]
        p[0], p[7] = p[7], p[0]
        with self.assertRaises(AssertionError):
            verify.verify_countermodel(bad, count_cycles=False)


if __name__ == "__main__":
    unittest.main()

