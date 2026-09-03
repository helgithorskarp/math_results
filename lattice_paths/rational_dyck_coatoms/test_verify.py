#!/usr/bin/env python3
"""Independent continuant checks for verify.py."""

from __future__ import annotations

from fractions import Fraction
import importlib.util
import math
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().with_name("verify.py")
SPEC = importlib.util.spec_from_file_location("coatom_verify", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)

cf_entries = VERIFY.cf_entries
dyck_paths = VERIFY.dyck_paths
fib = VERIFY.fib
lagrange_square = VERIFY.lagrange_square
matching_score = VERIFY.matching_score
named_paths = VERIFY.named_paths


def continuant(entries: tuple[int, ...]) -> int:
    previous, current = 0, 1
    for entry in entries:
        previous, current = current, entry * current + previous
    return current


def reference_matching(path: tuple[int, ...]) -> int:
    return continuant(cf_entries(path))


def reference_lagrange_square(path: tuple[int, ...]) -> Fraction:
    period = (2,) + cf_entries(path)
    values = []
    for shift in range(len(period)):
        entries = period[shift:] + period[:shift]
        p = continuant(entries)
        r = continuant(entries[:-1])
        q = continuant(entries[1:])
        s = continuant(entries[1:-1])
        values.append(Fraction((p - s) ** 2 + 4 * r * q, q * q))
    return max(values)


class IndependentChecks(unittest.TestCase):
    def test_fibonacci_product_identity(self) -> None:
        for x in range(1, 30):
            for y in range(1, 30):
                self.assertEqual(
                    fib(2 * x) * fib(2 * y),
                    fib(2 * (x + y - 1)) + fib(2 * x - 2) * fib(2 * y - 2),
                )

    def test_four_block_deficit_formula(self) -> None:
        for r1 in range(1, 8):
            for u1 in range(1, 8):
                for r2 in range(1, 8):
                    for u2 in range(1, 8):
                        path = (1,) * r1 + (0,) * u1 + (1,) * r2 + (0,) * u2
                        maximum = (1,) * (r1 + r2) + (0,) * (u1 + u2)
                        expected_deficit = (
                            2
                            * fib(2 * u1)
                            * fib(2 * r2)
                            * (
                                fib(2 * r1 - 1) * fib(2 * u2 - 2)
                                + fib(2 * r1 - 2) * fib(2 * u2)
                            )
                        )
                        self.assertEqual(
                            matching_score(maximum) - matching_score(path),
                            expected_deficit,
                        )

    def test_independent_score_implementations(self) -> None:
        for a in range(3, 9):
            for b in range(2, a):
                if math.gcd(a, b) != 1:
                    continue
                for path in dyck_paths(a, b):
                    self.assertEqual(matching_score(path), reference_matching(path))
                    self.assertEqual(lagrange_square(path), reference_lagrange_square(path))

    def test_named_paths_and_gap(self) -> None:
        for a in range(3, 40):
            for b in range(2, a):
                if math.gcd(a, b) != 1:
                    continue
                maximum, coatom, mate = named_paths(a, b)
                self.assertEqual(lagrange_square(coatom), lagrange_square(mate))
                self.assertEqual(
                    matching_score(maximum) - matching_score(coatom),
                    2 * fib(2 * b - 2) * fib(2 * a - 4),
                )


if __name__ == "__main__":
    result = unittest.main(verbosity=2, exit=False).result
    if not result.wasSuccessful():
        raise SystemExit(1)
    print("INDEPENDENT CONTINUANT CHECKS PASSED")
