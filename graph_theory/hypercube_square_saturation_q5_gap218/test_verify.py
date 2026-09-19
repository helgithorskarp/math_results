#!/usr/bin/env python3
"""Fast regression tests for the Q5 gap-218 package."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent


def load(name, filename):
    spec = spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {filename}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Gap218Tests(unittest.TestCase):
    def test_profile_certificate(self):
        rows = json.loads((HERE / "PROFILE_CLASSES.json").read_text())
        digest = sha256(
            json.dumps(rows, separators=(",", ":")).encode("ascii")
        ).hexdigest()
        self.assertEqual(len(rows), 182)
        self.assertEqual(
            digest,
            "9dc4c10874d87acd730ab6fb0741b23da45c13a4d01ba29149dcc11e8f4aefbb",
        )
        self.assertEqual(rows[-2:], [[217, 7, 5, 2, 192], [217, 7, 7, 1, 192]])

    def test_extremal_boundary(self):
        verify = load("gap218_target_tests", "verify.py")
        count, spectrum = verify.extremal_q4_exact_covers()
        self.assertEqual(count, 8)
        self.assertEqual(dict(spectrum), {(24, 24, 24, 24, 336): 8})

    def test_global_algebra(self):
        ratio = Fraction(12 * 56 + 218, 34 * 56)
        self.assertEqual(ratio, Fraction(445, 952))
        self.assertEqual(ratio / 12, Fraction(445, 11424))
        self.assertEqual(
            Fraction(19992, 10979) - Fraction(5712, 3137),
            Fraction(2856, 34441123),
        )

    def test_compact_independent_replay(self):
        independent = load("gap218_independent_tests", "independent_check.py")
        result = independent.check()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["total_cases"], 5040)
        self.assertEqual(result["total_solutions"], 0)


if __name__ == "__main__":
    unittest.main()
