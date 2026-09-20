#!/usr/bin/env python3
"""Independent formula-level checks without importing the implementation."""

from __future__ import annotations

import argparse
import hashlib


def g(value: int) -> int:
    if value <= 1:
        return 2 * value - 3
    return value // 2 if value % 2 == 0 else (value - 3) // 2


def message(branch: tuple[int, ...]) -> int:
    occupied = False
    value = 0
    for pile in branch:
        occupied = occupied or pile > 0
        if occupied:
            value = g(pile + value)
    return value


def split(configuration: tuple[int, ...], cut: int, left: int) -> tuple[int, ...]:
    n = len(configuration)
    return (
        (left,)
        + tuple(configuration[(cut + offset) % n] for offset in range(1, n))
        + (configuration[cut] - left,)
    )


def score(path: tuple[int, ...], target: int) -> int:
    return path[target] + message(path[:target]) + message(path[:target:-1])


def configuration(k: int, a: int, b: int) -> tuple[int, ...]:
    values = [0] * (2 * k + 1)
    values[0] = 5 * (1 << (k - 1)) - 6
    values[a] = values[b] = 1
    return tuple(values)


def check(max_k: int) -> dict[str, int | str]:
    if max_k < 3:
        raise ValueError("max_k must be at least three")
    formula_checks = 0
    direct_checks = 0
    records: list[str] = []
    for k in range(3, max_k + 1):
        n = 2 * k + 1
        power = 1 << k
        heavy = 5 * (1 << (k - 1)) - 6

        # Two units on one clockwise arm, at distances a<b<=k.
        for a in range(1, k):
            for b in range(a + 1, k + 1):
                branch = (0,) + (0,) * (b - a - 1) + (1,) + (0,) * (a - 1)
                # The leading zero is ignored; replace it by the far unit.
                branch = (1,) + branch[1:]
                closed = 3 - (1 << a) * ((1 << (b - a + 1)) - 1)
                if message(branch) != closed:
                    raise AssertionError((k, a, b, message(branch), closed))
                if heavy + closed < 1:
                    raise AssertionError("same-arm inequality failed")
                formula_checks += 1

        # Units on opposite arms.  Exactly five central pairs fail at target 0.
        failed: list[tuple[int, int]] = []
        for x in range(1, k + 1):
            for y in range(1, k + 1):
                closed = 5 * power // 2 - (1 << (x + 1)) - (1 << (y + 1))
                if closed < 1:
                    failed.append((x, y))
                formula_checks += 1
        expected_failed = [(k - 2, k), (k - 1, k), (k, k - 2), (k, k - 1), (k, k)]
        if failed != expected_failed:
            raise AssertionError((k, failed, expected_failed))

        exceptional = (
            (k - 2, k + 1, 3 * (1 << (k - 2))),
            (k, k + 1, 0),
            (k, k + 3, 0),
        )
        for a, b, left in exceptional:
            path = split(configuration(k, a, b), 0, left)
            observed = score(path, k - 1)
            if observed != 1:
                raise AssertionError((k, a, b, observed))
            direct_checks += 1
            records.append(f"{k}|{a}|{b}|{left}|{observed}")

        # The two remaining failures are precisely the reflected stable pair.
        stable = {(k - 1, k + 1), (k, k + 2)}
        if {(x, n - y) for x, y in failed} - {
            (k - 2, k + 1), (k, k + 1), (k, k + 3)
        } != stable:
            raise AssertionError("exception partition failed")

    digest = hashlib.sha256(("\n".join(records) + "\n").encode("ascii")).hexdigest()
    return {
        "max_k": max_k,
        "formula_checks": formula_checks,
        "exceptional_direct_checks": direct_checks,
        "exception_sha256": digest,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=128)
    args = parser.parse_args()
    for key, value in check(args.max_k).items():
        print(f"{key}={value}")
    print("INDEPENDENT TRANSFER FORMULAS VERIFIED")


if __name__ == "__main__":
    main()
