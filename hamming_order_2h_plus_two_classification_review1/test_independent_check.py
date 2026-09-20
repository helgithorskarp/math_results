import unittest

import independent_check as check


class IndependentAuditTests(unittest.TestCase):
    def test_two_row_boundary(self):
        self.assertEqual(
            check.enumerate_host((2, 8), 6),
            {"subsets": 120, "cores": 120, "L": 0, "E": 64, "U": 56,
             "overlaps": 0},
        )

    def test_explicit_witnesses(self):
        records = check.witness_records()
        self.assertEqual(len(records), 7)
        self.assertEqual(
            {tuple(row["forms"]) for row in records},
            {("L",), ("E",), ("U",), ("E", "U")},
        )
        skew = next(row for row in records if row["name"] == "third_direction_unique_edge")
        self.assertEqual((skew["dimension"], skew["cross_edges"]), (3, 1))

    def test_sharp_threshold_control(self):
        self.assertEqual(
            check.sharp_h5_record(),
            {"host": [4, 3], "order": 12, "minimum_degree": 5,
             "forms": [], "profiles": [[3, 2]]},
        )

    def test_line_facts(self):
        self.assertEqual(
            check.elementary_line_facts(),
            {"triangles": 27, "outside_point_line_checks": 648},
        )

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            check.make_host(())
        with self.assertRaises(ValueError):
            check.enumerate_host((2, 2), 6)


if __name__ == "__main__":
    unittest.main()
