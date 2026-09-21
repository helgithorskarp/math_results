#!/usr/bin/env python3

import unittest

import verify


class BarycentricTuzaTests(unittest.TestCase):
    def test_primary_exception_frustrations(self) -> None:
        expected = {"Gamma1": 2, "Gamma2": 2, "Gamma3": 3, "Gamma4": 3, "Gamma5": 3}
        for name, spec in verify.EXCEPTIONS.items():
            n, positive, negative, _ = verify.normalize_graph(spec)
            self.assertEqual(verify.edge_frustration(n, positive | negative, negative), expected[name])

    def test_boundary_parity(self) -> None:
        for facets in (verify.TETRAHEDRON, verify.MOBIUS, verify.PROJECTIVE_PLANE):
            self.assertTrue(verify.boundary_even(facets))
        _, _, _, boundary = verify.facet_data(verify.MOBIUS)
        self.assertEqual(len(boundary), 5)

    def test_topological_lower_bound(self) -> None:
        self.assertEqual(verify.minimum_surface_bound(), 10)

    def test_negative_gluing_controls(self) -> None:
        for name in ("Gamma1", "Gamma2"):
            raw, canonical, accepted = verify.canonical_gluing_scan(verify.EXCEPTIONS[name])
            self.assertEqual(raw, 6 ** verify.EXCEPTIONS[name]["n"])
            self.assertEqual(canonical, 2 ** verify.EXCEPTIONS[name]["n"])
            self.assertEqual(accepted, 0)

    def test_positive_gluing_controls(self) -> None:
        for facets in (verify.TETRAHEDRON, verify.MOBIUS):
            _, _, accepted = verify.canonical_gluing_scan(verify.spec_from_facets(facets))
            self.assertGreater(accepted, 0)


if __name__ == "__main__":
    unittest.main()
