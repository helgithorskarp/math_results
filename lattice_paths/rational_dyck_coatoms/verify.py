#!/usr/bin/env python3
"""Exact finite corroboration of the rational-Dyck coatom theorem."""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def dyck_paths(a: int, b: int):
    """Yield all words in D(a,b), encoded by R=1 and U=0."""
    for up_positions in itertools.combinations(range(a + b), b):
        ups = set(up_positions)
        path = tuple(0 if index in ups else 1 for index in range(a + b))
        rights = ups_seen = 0
        for step in path:
            rights += step
            ups_seen += 1 - step
            if a * ups_seen > b * rights:
                break
        else:
            yield path


def cf_entries(path: tuple[int, ...]) -> tuple[int, ...]:
    entries: list[int] = []
    for left, right in zip(path, path[1:]):
        entries.extend((1, 1) if left == right else (2,))
    return tuple(entries)


def matrix(entries: tuple[int, ...]) -> tuple[int, int, int, int]:
    """Product of [[c,1],[1,0]], returned as (p,r,q,s)."""
    p, r, q, s = 1, 0, 0, 1
    for entry in entries:
        p, r, q, s = p * entry + r, p, q * entry + s, q
    return p, r, q, s


def matching_score(path: tuple[int, ...]) -> int:
    return matrix(cf_entries(path))[0]


def lagrange_square(path: tuple[int, ...]) -> Fraction:
    period = (2,) + cf_entries(path)
    scores = []
    for shift in range(len(period)):
        rotated = period[shift:] + period[:shift]
        p, r, q, s = matrix(rotated)
        scores.append(Fraction((p - s) ** 2 + 4 * r * q, q * q))
    return max(scores)


def word(path: tuple[int, ...]) -> str:
    return "".join("R" if step else "U" for step in path)


def named_paths(a: int, b: int):
    maximum = (1,) * a + (0,) * b
    matching_coatom = (1,) * (a - 1) + (0,) * (b - 1) + (1, 0)
    lagrange_mate = (1,) * (a - 1) + (0, 1) + (0,) * (b - 1)
    return maximum, matching_coatom, lagrange_mate


def fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def verify(max_a: int) -> dict[str, object]:
    table_digest = hashlib.sha256()
    endpoint_count = 0
    total_paths = 0
    largest_endpoint = 0

    for a in range(3, max_a + 1):
        for b in range(2, a):
            if math.gcd(a, b) != 1:
                continue
            endpoint_count += 1
            matching_levels: dict[int, list[tuple[int, ...]]] = defaultdict(list)
            lagrange_levels: dict[Fraction, list[tuple[int, ...]]] = defaultdict(list)

            paths = list(dyck_paths(a, b))
            total_paths += len(paths)
            largest_endpoint = max(largest_endpoint, len(paths))
            for path in paths:
                matching = matching_score(path)
                lagrange = lagrange_square(path)
                matching_levels[matching].append(path)
                lagrange_levels[lagrange].append(path)
                table_digest.update(
                    f"{a},{b};{word(path)};{matching};"
                    f"{lagrange.numerator}/{lagrange.denominator}\n".encode()
                )

            maximum, coatom, mate = named_paths(a, b)
            m_keys = sorted(matching_levels)
            l_keys = sorted(lagrange_levels)
            assert set(matching_levels[m_keys[-1]]) == {maximum}
            assert set(lagrange_levels[l_keys[-1]]) == {maximum}
            assert set(matching_levels[m_keys[-2]]) == {coatom}
            assert set(lagrange_levels[l_keys[-2]]) == {coatom, mate}
            assert lagrange_square(coatom) == lagrange_square(mate)
            assert matching_score(maximum) - matching_score(coatom) == (
                2 * fib(2 * b - 2) * fib(2 * a - 4)
            )

    return {
        "max_a": max_a,
        "coprime_endpoint_count": endpoint_count,
        "total_path_count": total_paths,
        "largest_endpoint_path_count": largest_endpoint,
        "score_table_sha256": table_digest.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-a", type=int, default=12)
    parser.add_argument("--print-summary", action="store_true")
    args = parser.parse_args()
    if args.max_a < 3:
        raise SystemExit("--max-a must be at least 3")

    actual = verify(args.max_a)
    if args.max_a == 12:
        expected = json.loads((ROOT / "expected.json").read_text())
        if actual != expected:
            raise SystemExit(
                "summary mismatch:\n"
                + json.dumps({"expected": expected, "actual": actual}, indent=2)
            )
    if args.print_summary:
        print(json.dumps(actual, indent=2, sort_keys=True))
    print("EXACT COATOM ENUMERATION VERIFIED")


if __name__ == "__main__":
    main()
