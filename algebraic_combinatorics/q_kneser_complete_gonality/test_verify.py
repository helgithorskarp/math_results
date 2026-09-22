"""Small exact tests, including rejection of corrupted audit inputs."""

import unittest

import verify as v


class AuditTests(unittest.TestCase):
    def test_gaussian_values_and_boundaries(self):
        self.assertEqual(v.gaussian(4, 2), 35)
        self.assertEqual(v.gaussian(6, 3), 1395)
        self.assertEqual(v.gaussian(4, 2, 3), 130)
        self.assertEqual(v.gaussian(0, 0), 1)
        self.assertEqual(v.gaussian(3, -1), 0)
        self.assertEqual(v.gaussian(3, 4), 0)
        for q in (2, 3, 4):
            for n in range(9):
                for k in range(n + 1):
                    self.assertEqual(v.gaussian(n, k, q), v.gaussian_product(n, k, q))

    def test_small_component_matrices(self):
        self.assertEqual(v.gf2_rank([2, 1]), 2)  # edge
        self.assertEqual(v.gf2_rank([2, 5, 2]), 2)  # path
        self.assertEqual(v.gf2_rank([6, 5, 3]), 2)  # triangle
        self.assertEqual(v.audit_small_components(), 11)

    def test_independent_generators(self):
        for n in range(1, 5):
            for k in range(n + 1):
                direct = [v.span_mask(b) for b in v.rref_bases(n, k)]
                self.assertEqual(len(direct), v.gaussian(n, k))
                self.assertEqual(set(direct), v.extension_subspaces(n, k))

    def test_plucker_basis_invariance(self):
        basis = (1, 2, 4)
        changed = (1 ^ 2, 2 ^ 4, 4)
        self.assertEqual(v.span_mask(basis), v.span_mask(changed))
        self.assertEqual(v.plucker_coordinates(basis, 6), v.plucker_coordinates(changed, 6))

    def test_exact_binary_rank_two(self):
        report = v.audit_binary_graph(2)
        self.assertEqual(report["binary_adjacency_rank"], 6)
        self.assertEqual(report["degree"], 16)
        self.assertEqual(report["star_size"], 7)

    def test_tampered_adjacency_rejected(self):
        bases = v.rref_bases(4, 2)
        rows = v.adjacency_masks([v.span_mask(b) for b in bases])
        plucker = [v.plucker_coordinates(b, 4) for b in bases]
        rows[0] ^= 1 << 1
        rows[1] ^= 1 << 0
        with self.assertRaises(ValueError):
            v.check_factorization(rows, plucker, 2)

    def test_tampered_plucker_rejected(self):
        bases = v.rref_bases(4, 2)
        rows = v.adjacency_masks([v.span_mask(b) for b in bases])
        plucker = [v.plucker_coordinates(b, 4) for b in bases]
        plucker[0] ^= 1
        with self.assertRaises(ValueError):
            v.check_factorization(rows, plucker, 2)

    def test_invalid_inputs_rejected(self):
        bad_calls = (
            lambda: v.gaussian(-1, 0),
            lambda: v.gaussian(4, 2, 1),
            lambda: v.rref_bases(3, 4),
            lambda: v.span_mask((1, 1)),
            lambda: v.plucker_coordinates((1, 1), 4),
            lambda: v.plucker_coordinates((1, 16), 4),
            lambda: v.gf2_rank([-1]),
            lambda: v.adjacency_masks([3, 3]),
            lambda: v.complement_permutation(5, 2),
            lambda: v.check_factorization([0], [], 1),
            lambda: v.audit_binary_graph(4),
        )
        for call in bad_calls:
            with self.assertRaises(ValueError):
                call()


if __name__ == "__main__":
    unittest.main()
