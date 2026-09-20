#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import verify


HERE = Path(__file__).resolve().parent


class CertificateTests(unittest.TestCase):
    def test_reference(self) -> None:
        summary = verify.verify_certificate(HERE / "certificate.json", 2)
        self.assertEqual(summary["seeds"], 5)

    def test_duplicate_vertex_rejected(self) -> None:
        data = json.loads((HERE / "certificate.json").read_text())
        data["seeds"][0]["path"][0] = data["seeds"][0]["path"][1]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                verify.verify_certificate(path, 1)

    def test_shifted_cut_rejected(self) -> None:
        data = json.loads((HERE / "certificate.json").read_text())
        data["seeds"][0]["growth"]["11"] = 0
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                verify.verify_certificate(path, 1)

    def test_missing_seed_rejected_by_coverage(self) -> None:
        data = json.loads((HERE / "certificate.json").read_text())
        data["seeds"].pop(0)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps(data))
            result = subprocess.run(
                [sys.executable, str(HERE / "audit_coverage.py"), str(HERE / "coverage_data.json"), str(path)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
