#!/usr/bin/env python3
"""Regression tests for the star--triangle subdivision checker."""

import unittest

import verify


class StructuralCertificateTests(unittest.TestCase):
    def test_small_instances(self) -> None:
        for m in range(1, 31):
            verify.audit_instance(m, explicit=True)

    def test_formula_values(self) -> None:
        self.assertEqual(
            [verify.crossing_formula(m) for m in range(1, 11)],
            [0, 0, 1, 2, 4, 6, 9, 12, 16, 20],
        )

    def test_path_lengths(self) -> None:
        paths = verify.subdivision_paths(7)
        lengths = sorted(len(path) - 1 for path in paths.values())
        self.assertEqual(lengths.count(1), 7)
        self.assertEqual(lengths.count(2), 14)

    def test_invalid_parameters(self) -> None:
        for function in (
            verify.product_graph,
            verify.subdivision_paths,
            verify.crossing_formula,
            verify.audit_instance,
        ):
            with self.assertRaises(ValueError):
                function(0)

    def test_loop_rejected(self) -> None:
        with self.assertRaises(ValueError):
            verify.canonical_edge(verify.centre(0), verify.centre(0))


if __name__ == "__main__":
    unittest.main()
