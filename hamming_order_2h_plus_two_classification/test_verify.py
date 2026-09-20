import unittest

import verify


class BoundaryAuditTests(unittest.TestCase):
    def test_profile_transition(self):
        self.assertEqual(
            verify.feasible_profiles(5),
            [(4, 1), (3, 2), (4, 2)],
        )
        self.assertEqual(verify.feasible_profiles(6), [(5, 1)])
        self.assertEqual(verify.feasible_profiles(10), [(9, 1)])

    def test_shell_bound_is_exact_rational(self):
        self.assertEqual(verify.shell_lower_bound(6, (5, 1)), 12)
        self.assertEqual(verify.shell_lower_bound(6, (4, 2)), 15)

    def test_skew_family(self):
        for h in (2, 6, 11):
            family = verify.skew_two_line_family(h)
            self.assertEqual(len(family), 2 * h + 2)
            self.assertEqual(verify.induced_min_degree(family), h)
            self.assertEqual(verify.essential_dimension(family), 3)

    def test_line_incidence_catalogue(self):
        audited, counts, covered = verify.audit_line_incidence()
        self.assertEqual(audited, 88074)
        self.assertEqual(
            counts,
            {"empty": 62478, "matching": 3240, "single": 19440, "star": 2916},
        )
        self.assertEqual(covered, 3726)

    def test_bad_range_rejected(self):
        with self.assertRaises(ValueError):
            verify.audit(5, 5)


if __name__ == "__main__":
    unittest.main()
