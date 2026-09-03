#!/usr/bin/env python3
"""Regression and certificate-rejection tests for verify.py."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from verify import CertificateError, U, admissible, verify_case, verify_certificate

HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "certificate.json"


def generic_admissible(p: tuple[int, int, int]) -> bool:
    counts = dict(zip(U, p))
    v = sum(p) + 1
    if max(U) > v // 2:
        return False
    for d in range(1, v + 1):
        if v % d == 0:
            divisible = sum(c for x, c in counts.items() if x % d == 0)
            if divisible > v - d:
                return False
    return True


class VerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(CERTIFICATE.read_bytes())

    def test_full_certificate(self) -> None:
        summary = verify_certificate(CERTIFICATE)
        self.assertEqual(summary["cases"], 22)
        self.assertEqual(summary["witnesses"], 628)

    def test_admissibility_simplification(self) -> None:
        for a in range(1, 18):
            for b in range(1, 18):
                for c in range(1, 18):
                    p = (a, b, c)
                    self.assertEqual(admissible(p), generic_admissible(p), p)

    def test_rejects_corrupt_path(self) -> None:
        case = copy.deepcopy(self.data["cases"][0])
        case["witnesses"][0]["path"][0] = case["witnesses"][0]["path"][1]
        with self.assertRaises(CertificateError):
            verify_case(case)

    def test_rejects_corrupt_growth_position(self) -> None:
        case = copy.deepcopy(self.data["cases"][0])
        witness = next(w for w in case["witnesses"] if w["grow"])
        x = str(witness["grow"][0])
        witness["growth"][x] = -1
        with self.assertRaises(CertificateError):
            verify_case(case)

    def test_rejects_uncovered_infinite_region(self) -> None:
        case = copy.deepcopy(self.data["cases"][0])
        case["witnesses"] = [
            w
            for w in case["witnesses"]
            if tuple(w["counts"]) == tuple(case["cap"])
            and set(w["grow"]) == set(U)
        ]
        with self.assertRaises(CertificateError):
            verify_case(case)


if __name__ == "__main__":
    unittest.main()
