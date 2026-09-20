#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import audit_coverage
import verify

HERE = Path(__file__).resolve().parent
COVERAGE = HERE.parent / "bhr_1_2_11_a1_completion" / "coverage_data.json"


class CertificateTests(unittest.TestCase):
    def test_reference(self) -> None:
        summary = verify.verify_certificate(HERE / "certificate.json", 2)
        self.assertEqual(summary["seeds"], 3)
        coverage = audit_coverage.audit(COVERAGE, HERE / "certificate.json")
        self.assertEqual(coverage["final_residual_patterns"], 0)

    def test_duplicate_vertex_rejected(self) -> None:
        data = json.loads((HERE / "certificate.json").read_text())
        data["seeds"][0]["path"][0] = data["seeds"][0]["path"][1]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                verify.verify_certificate(path, 1)

    def test_overlapping_cut_rejected(self) -> None:
        data = json.loads((HERE / "certificate.json").read_text())
        data["seeds"][0]["growth"]["2"] = data["seeds"][0]["growth"]["11"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                verify.verify_certificate(path, 1)

    def test_missing_seed_rejected_by_coverage(self) -> None:
        data = json.loads((HERE / "certificate.json").read_text())
        data["seeds"].pop()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                audit_coverage.audit(COVERAGE, path)


if __name__ == "__main__":
    unittest.main()
