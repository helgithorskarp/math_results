import unittest

import verify


class MooreBoundaryTests(unittest.TestCase):
    def test_branch_types(self):
        self.assertEqual(
            set(verify.BRANCH_TYPES),
            {
                (7, 0, 0), (5, 1, 0), (3, 2, 0), (1, 3, 0),
                (4, 0, 1), (2, 1, 1), (0, 2, 1), (1, 0, 2),
            },
        )
        for a, b, c in verify.BRANCH_TYPES:
            self.assertEqual(a + 2 * b + 3 * c, 7)

    def test_signature_counts(self):
        self.assertEqual([len(verify.branch_multisets(t)) for t in range(4)], [12, 16, 11, 2])
        self.assertEqual([len(verify.surviving_signatures(t)) for t in range(4)], [12, 16, 8, 2])

    def test_uniform_degree_57(self):
        verify.audit_uniform_extension(7)
        p = verify.uniform_parameters(7)
        self.assertEqual((p["k"], p["v"], p["alpha"]), (57, 3250, 400))

    def test_uniform_range(self):
        for r in range(5, 50):
            verify.audit_uniform_extension(r)

    def test_boundary_sizes(self):
        self.assertEqual(
            [verify.boundary_summary(t)["code_weight"] for t in range(4)],
            [184, 188, 192, 196],
        )

    def test_odd_partition_minimum(self):
        self.assertEqual(verify.odd_partition_min_pairs(150, 24), 405)
        self.assertEqual(verify.odd_partition_min_pairs(150, 56), 141)
        with self.assertRaises(ValueError):
            verify.odd_partition_min_pairs(151, 24)

    def test_bad_parameters(self):
        with self.assertRaises(ValueError):
            verify.uniform_parameters(0)
        with self.assertRaises(ValueError):
            verify.branch_multisets(4)


if __name__ == "__main__":
    unittest.main()
