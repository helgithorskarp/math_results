#!/usr/bin/env python3
"""Exact checks for the complete D(a,2) matching/Lagrange classification."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def fib(n: int) -> int:
    """Fibonacci number, including the convenient convention F_{-1}=1."""
    if n == -1:
        return 1
    if n < -1:
        raise ValueError("Fibonacci index must be at least -1")
    previous, current = 0, 1
    for _ in range(n):
        previous, current = current, previous + current
    return previous


def continuant_matrix(entries: tuple[int, ...]) -> tuple[int, int, int, int]:
    """Product of [[c,1],[1,0]], returned as (p,r,q,s)."""
    p, r, q, s = 1, 0, 0, 1
    for entry in entries:
        p, r, q, s = p * entry + r, p, q * entry + s, q
    return p, r, q, s


def cf_entries(path: tuple[int, ...]) -> tuple[int, ...]:
    entries: list[int] = []
    for left, right in zip(path, path[1:]):
        entries.extend((1, 1) if left == right else (2,))
    return tuple(entries)


def matching_score(path: tuple[int, ...]) -> int:
    return continuant_matrix(cf_entries(path))[0]


def lagrange_data(path: tuple[int, ...]) -> tuple[Fraction, int, tuple[int, ...]]:
    """Return exact L^2, common period trace, and q values at all 2-cuts."""
    period = (2,) + cf_entries(path)
    trace = None
    squares: list[Fraction] = []
    q_at_two: list[int] = []
    for shift, digit in enumerate(period):
        rotated = period[shift:] + period[:shift]
        p, r, q, s = continuant_matrix(rotated)
        this_trace = p + s
        if trace is None:
            trace = this_trace
        else:
            assert this_trace == trace
        squares.append(Fraction((p - s) ** 2 + 4 * r * q, q * q))
        if digit == 2:
            q_at_two.append(q)
    assert trace is not None
    return max(squares), trace, tuple(q_at_two)


def is_dyck(path: tuple[int, ...], a: int) -> bool:
    rights = ups = 0
    for step in path:
        rights += step
        ups += 1 - step
        if a * ups > 2 * rights:
            return False
    return rights == a and ups == 2


def dyck_paths(a: int):
    """Enumerate D(a,2) directly from the two up-step positions."""
    length = a + 2
    for up_positions in itertools.combinations(range(length), 2):
        up_set = set(up_positions)
        path = tuple(0 if index in up_set else 1 for index in range(length))
        if is_dyck(path, a):
            yield path


def split_path(a: int, r: int) -> tuple[int, ...]:
    return (1,) * r + (0,) + (1,) * (a - r) + (0,)


def maximum_path(a: int) -> tuple[int, ...]:
    return (1,) * a + (0, 0)


def word(path: tuple[int, ...]) -> str:
    return "".join("R" if step else "U" for step in path)


def verify(max_a: int) -> dict[str, object]:
    if max_a < 3:
        raise ValueError("max_a must be at least 3")
    if max_a % 2 == 0:
        max_a -= 1

    digest = hashlib.sha256()
    endpoint_count = 0
    path_count = 0
    identity_count = 0

    for a in range(3, max_a + 1, 2):
        endpoint_count += 1
        middle = (a + 1) // 2
        split_paths = [split_path(a, r) for r in range(middle, a)]
        maximum = maximum_path(a)
        ascending = split_paths + [maximum]

        enumerated = set(dyck_paths(a))
        assert enumerated == set(ascending)
        assert len(enumerated) == (a + 1) // 2
        path_count += len(enumerated)

        matching_scores = [matching_score(path) for path in ascending]
        lagrange_squares = [lagrange_data(path)[0] for path in ascending]
        assert all(left < right for left, right in zip(matching_scores, matching_scores[1:]))
        assert all(left < right for left, right in zip(lagrange_squares, lagrange_squares[1:]))

        maximum_matching = matching_scores[-1]
        previous_matching = None
        previous_lagrange = None
        for r, path in zip(range(middle, a), split_paths, strict=True):
            s = a - r
            d = r - s
            matching = matching_score(path)
            lagrange_square, trace, q_at_two = lagrange_data(path)

            assert maximum_matching - matching == 2 * fib(2 * s) * fib(2 * r - 2)
            assert trace == 3 * matching + 2 * fib(2 * d - 2)
            assert sorted(q_at_two) == sorted(
                (matching, matching, matching + 2 * fib(2 * d), matching + 2 * fib(2 * d))
            )
            assert lagrange_square == Fraction(trace * trace - 4, matching * matching)
            assert matching >= fib(2 * a)

            if previous_matching is not None:
                previous_d = d - 2
                assert matching - previous_matching == 2 * fib(2 * previous_d)
                assert lagrange_square > previous_lagrange
            previous_matching = matching
            previous_lagrange = lagrange_square
            identity_count += 5

            digest.update(
                (
                    f"{a};{r};{word(path)};{matching};{trace};"
                    f"{lagrange_square.numerator}/{lagrange_square.denominator};"
                    f"{','.join(map(str, q_at_two))}\n"
                ).encode()
            )

    return {
        "max_a": max_a,
        "odd_endpoint_count": endpoint_count,
        "classified_path_count": path_count,
        "checked_identity_count": identity_count,
        "score_table_sha256": digest.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-a", type=int, default=101)
    parser.add_argument("--print-summary", action="store_true")
    args = parser.parse_args()

    actual = verify(args.max_a)
    if actual["max_a"] == 101:
        expected = json.loads((ROOT / "expected.json").read_text())
        if actual != expected:
            raise SystemExit(
                "summary mismatch:\n"
                + json.dumps({"expected": expected, "actual": actual}, indent=2)
            )
    if args.print_summary:
        print(json.dumps(actual, indent=2, sort_keys=True))
    print("D(a,2) COMPLETE ORDER CLASSIFICATION VERIFIED")


if __name__ == "__main__":
    main()

