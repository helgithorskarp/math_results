"""Tests for the reviewed Albertson r=27 dependency-chain checker."""

from copy import deepcopy
import unittest

import verify_chain as audit


class ReviewedChainTests(unittest.TestCase):
    def test_dependency_hashes(self) -> None:
        manifest = audit.read_json("dependency_manifest.json")
        self.assertEqual(audit.check_manifest(manifest), (9, 18))

    def test_local_disk(self) -> None:
        rotation = audit.read_json("rotation_system.json")
        certificate = audit.local_disk(rotation)
        self.assertEqual(certificate["euler_characteristic"], 1)
        self.assertEqual(certificate["boundary"], ["u", "z", "t", "r", "w"])

    def test_orientation_rejection(self) -> None:
        rotation = deepcopy(audit.read_json("rotation_system.json"))
        rotation["faces"][1] = ["z", "w", "x"]
        with self.assertRaises(AssertionError):
            audit.local_disk(rotation)

    def test_frontier_arithmetic(self) -> None:
        certificate = audit.arithmetic_chain()
        self.assertEqual(certificate["Z(27)"], 6084)
        self.assertEqual(
            certificate["terminal_planarizations"],
            [("A", 41, 117, 78), ("B", 40, 114, 76)],
        )
        self.assertEqual(
            certificate["row_bounds"],
            {"53,713": 6089, "53,714": 6100, "53,715": 6129, "54,726": 6084},
        )


if __name__ == "__main__":
    unittest.main()
