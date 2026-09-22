#!/usr/bin/env python3

import unittest

import verify


class ParityKernelTests(unittest.TestCase):
    def test_path_residue_matrices(self):
        paths = ((0, 1, 1), (0, 1, 2), (0, 1, 3))
        data = verify.reduction(paths, 2)
        self.assertEqual(data["P"], [[1, 0], [0, 1]])
        self.assertEqual(data["V"], [[1, 1]])
        self.assertEqual(data["rank"], 1)

    def test_even_signed_component_rank(self):
        balanced = ((0, 1, 4), (1, 2, 2), (0, 2, 2))
        unbalanced = ((0, 1, 4), (1, 2, 4), (0, 2, 2))
        self.assertEqual(verify.balanced_even_components(balanced, 3), 1)
        self.assertEqual(verify.balanced_even_components(unbalanced, 3), 0)
        for paths in (balanced, unbalanced):
            data = verify.reduction(paths, 3)
            self.assertEqual(
                verify.balanced_even_components(paths, 3),
                3 - data["rank"],
            )

    def test_loop_residues(self):
        paths = ((0, 0, 3), (0, 1, 1), (1, 1, 4))
        data = verify.reduction(paths, 2)
        self.assertEqual(data["P"][0][0], -1)
        self.assertEqual(data["V"], [[0, 0]])
        self.assertEqual(data["rank"], 0)

    def test_theta_formula(self):
        graph = verify.build_core(2, ((0, 1, 2), (0, 1, 3), (0, 1, 5)))
        stats = verify.audit_one(graph, check_line_graph=True)
        self.assertEqual(stats["branch"], 2)
        self.assertEqual(stats["cyclomatic"], 2)

    def test_four_subdivision_periodicity(self):
        base = ((0, 1, 1), (0, 1, 2), (0, 1, 3))
        lifted = ((0, 1, 5), (0, 1, 2), (0, 1, 3))
        g0 = verify.build_core(2, base)
        g1 = verify.build_core(2, lifted)
        i0 = verify.inertia(verify.shifted_signless(g0))
        i1 = verify.inertia(verify.shifted_signless(g1))
        self.assertEqual(i1, (i0[0] + 2, i0[1], i0[2] + 2))
        self.assertEqual(
            verify.signature(verify.line_adjacency(g0)),
            verify.signature(verify.line_adjacency(g1)),
        )

    def test_invalid_core_rejected(self):
        cycle = verify.adjacency(4, ((0, 1), (1, 2), (2, 3), (0, 3)))
        with self.assertRaises(ValueError):
            verify.branch_paths(cycle)
        with self.assertRaises(ValueError):
            verify.build_core(2, ((0, 0, 2), (0, 1, 1), (1, 1, 3)))


if __name__ == "__main__":
    unittest.main()
