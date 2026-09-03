#!/usr/bin/env python3
"""Independent scalar-continuant checks for the D(a,2) classification."""

from __future__ import annotations

from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().with_name("verify.py")
SPEC = importlib.util.spec_from_file_location("b2_verify", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


def scalar_continuant(entries: tuple[int, ...]) -> int:
    previous, current = 0, 1
    for entry in entries:
        previous, current = current, entry * current + previous
    return current


def reference_matching(path: tuple[int, ...]) -> int:
    return scalar_continuant(VERIFY.cf_entries(path))


def reference_lagrange_square(path: tuple[int, ...]) -> Fraction:
    period = (2,) + VERIFY.cf_entries(path)
    values: list[Fraction] = []
    for shift in range(len(period)):
        entries = period[shift:] + period[:shift]
        p = scalar_continuant(entries)
        r = scalar_continuant(entries[:-1])
        q = scalar_continuant(entries[1:])
        s = scalar_continuant(entries[1:-1])
        values.append(Fraction((p - s) ** 2 + 4 * r * q, q * q))
    return max(values)


class IndependentChecks(unittest.TestCase):
    def test_d_ocagne_specializations(self) -> None:
        for r in range(2, 70):
            for s in range(1, r):
                self.assertEqual(
                    VERIFY.fib(2 * r - 2) * VERIFY.fib(2 * s - 3)
                    - VERIFY.fib(2 * r - 3) * VERIFY.fib(2 * s - 2),
                    VERIFY.fib(2 * (r - s)),
                )
                self.assertEqual(
                    VERIFY.fib(2 * r - 2) * VERIFY.fib(2 * s - 1)
                    - VERIFY.fib(2 * r - 3) * VERIFY.fib(2 * s),
                    VERIFY.fib(2 * (r - s) - 2),
                )

    def test_independent_scores_and_strict_order(self) -> None:
        for a in range(3, 32, 2):
            paths = [
                VERIFY.split_path(a, r)
                for r in range((a + 1) // 2, a)
            ] + [VERIFY.maximum_path(a)]
            matching = [reference_matching(path) for path in paths]
            lagrange = [reference_lagrange_square(path) for path in paths]
            self.assertTrue(all(x < y for x, y in zip(matching, matching[1:])))
            self.assertTrue(all(x < y for x, y in zip(lagrange, lagrange[1:])))

    def test_exhaustive_path_classification(self) -> None:
        for a in range(3, 102, 2):
            expected = {VERIFY.maximum_path(a)} | {
                VERIFY.split_path(a, r)
                for r in range((a + 1) // 2, a)
            }
            self.assertEqual(set(VERIFY.dyck_paths(a)), expected)

    def test_reference_agrees_with_matrix_implementation(self) -> None:
        for a in range(3, 32, 2):
            for path in VERIFY.dyck_paths(a):
                self.assertEqual(VERIFY.matching_score(path), reference_matching(path))
                self.assertEqual(VERIFY.lagrange_data(path)[0], reference_lagrange_square(path))


if __name__ == "__main__":
    result = unittest.main(verbosity=2, exit=False).result
    if not result.wasSuccessful():
        raise SystemExit(1)
    print("INDEPENDENT D(a,2) CONTINUANT CHECKS PASSED")

