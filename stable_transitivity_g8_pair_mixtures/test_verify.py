#!/usr/bin/env python3
"""Tamper-rejection tests for the G8 pair-mixture certificate."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from verify import verify

HERE = Path(__file__).resolve().parent


class VerifyTests(unittest.TestCase):
    def test_published_certificate(self) -> None:
        output = verify(HERE / "pair_profiles.txt")
        expected = (HERE / "EXPECTED_OUTPUT.txt").read_text(encoding="ascii").strip()
        self.assertEqual(output, expected)

    def test_changed_order_is_rejected(self) -> None:
        text = (HERE / "pair_profiles.txt").read_text(encoding="ascii")
        changed = text.replace("profile=9062,", "profile=9063,", 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.txt"
            path.write_text(changed, encoding="ascii")
            with self.assertRaises(ValueError):
                verify(path)

    def test_missing_target_is_rejected(self) -> None:
        lines = (HERE / "pair_profiles.txt").read_text(encoding="ascii").splitlines()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.txt"
            path.write_text("\n".join(lines[:-1]) + "\n", encoding="ascii")
            with self.assertRaises(ValueError):
                verify(path)


if __name__ == "__main__":
    unittest.main()
