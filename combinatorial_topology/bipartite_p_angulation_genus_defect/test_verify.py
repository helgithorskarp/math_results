import unittest

import verify


class ParityGapTests(unittest.TestCase):
    def test_cube_audit_has_all_rotations(self):
        report = verify.cube_audit()
        self.assertEqual(report["rotation_systems"], 256)
        self.assertEqual(sum(row["count"] for row in report["profiles"]), 256)

    def test_cube_attains_quadrangulation_endpoint(self):
        profiles = verify.cube_audit()["profiles"]
        endpoint = [row for row in profiles
                    if row["genus_excess"] == 1
                    and row["missing_faces"] == 6]
        self.assertEqual(endpoint, [{
            "genus_excess": 1,
            "missing_faces": 6,
            "nonreference_face_lengths": [6, 6, 6, 6],
            "count": 8,
        }])

    def test_valid_abstract_record(self):
        verify.audit_defect(4, 1, 5, (6, 6, 8), 20)

    def test_odd_face_rejected(self):
        with self.assertRaisesRegex(ValueError, "odd length"):
            verify.audit_defect(4, 1, 5, (5, 7, 8), 20)

    def test_inconsistent_endpoint_rejected(self):
        with self.assertRaisesRegex(ValueError, "dart-count"):
            verify.audit_defect(4, 1, 6, (6, 6, 6, 8), 20)


if __name__ == "__main__":
    unittest.main()
