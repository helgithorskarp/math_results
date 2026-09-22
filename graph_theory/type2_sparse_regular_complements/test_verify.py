#!/usr/bin/env python3

import unittest

import verify


class FamilyAuditTests(unittest.TestCase):
    def test_first_member(self) -> None:
        row = verify.audit(4)
        self.assertEqual(row["order"], 28)
        self.assertEqual(row["edges"], 42)
        self.assertEqual(row["complement_degree"], 24)
        self.assertEqual(row["claimed_total_chromatic_number"], 26)
        self.assertTrue(row["cubic"])
        self.assertTrue(row["triangle_free"])

    def test_formula_sample(self) -> None:
        for m in (4, 5, 9, 20):
            row = verify.audit(m)
            self.assertEqual(row["order"], 6 * m + 4)
            self.assertEqual(row["edges"], 9 * m + 6)
            self.assertTrue(row["three_central_bridges"])
            self.assertTrue(row["bridge_lobes_odd"])

    def test_rejects_too_small_parameter(self) -> None:
        with self.assertRaises(ValueError):
            verify.build_h(3)

    def test_triangle_mutation_is_detected(self) -> None:
        graph, centre, subdivisions = verify.build_h(4)
        verify.add_edge(graph, subdivisions[0], subdivisions[1])
        self.assertFalse(verify.triangle_free(graph))


if __name__ == "__main__":
    unittest.main()
