#!/usr/bin/env python3
"""Exact audit for the second equal-offset binomial curve.

The universal result is proved in README.md.  This script provides a
definition-level finite check, an algebraic identity audit, and a fast exact
stress test based on independently solving the relevant quadratic equations.
It uses only arbitrary-precision integers from Python's standard library.
"""

from __future__ import annotations

import argparse
import json
import math


def factorization_residual(a: int, b: int) -> tuple[int, int]:
    """Return both sides of the residual identity before imposing equality."""
    A = a * (a + b + 1)
    U = b * (b + 1)
    low = 2 * A + b - 2 * U + 2
    high = 2 * A + b + 2 * U - 2
    return low * high - (b * b - 4), 4 * (A * (A + b) - U * (U - 2))


def check_identity_grid(limit: int) -> None:
    for a in range(1, limit + 1):
        for b in range(2, limit + 2):
            lhs, rhs = factorization_residual(a, b)
            if lhs != rhs:
                raise AssertionError((a, b, lhs, rhs))


def definition_scan(max_x: int) -> list[list[int]]:
    """Use math.comb directly, without the product/factor transformation."""
    solutions: list[list[int]] = []
    for x in range(4, max_x + 1):
        for y in range(0, x - 3):
            if math.comb(x, y) == math.comb(x - 2, y + 2):
                solutions.append([x, y])
    return solutions


def exact_quadratic_solutions(max_b: int) -> list[list[int]]:
    """Solve the two quadratic discriminant conditions exactly for each b."""
    solutions: list[list[int]] = []
    for b in range(2, max_b + 1):
        U = b * (b + 1)
        target = U * (U - 2)

        # A(A+b)=target.
        disc_A = b * b + 4 * target
        root_A = math.isqrt(disc_A)
        if root_A * root_A != disc_A or (root_A - b) % 2:
            continue
        A = (root_A - b) // 2
        if A <= 0 or A * (A + b) != target:
            continue

        # a(a+b+1)=A.
        disc_a = (b + 1) * (b + 1) + 4 * A
        root_a = math.isqrt(disc_a)
        if root_a * root_a != disc_a or (root_a - b - 1) % 2:
            continue
        a = (root_a - b - 1) // 2
        if a >= 1 and a * (a + b + 1) == A:
            solutions.append([a, b])
    return solutions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--identity-limit", type=int, default=100)
    parser.add_argument("--definition-max-x", type=int, default=1000)
    parser.add_argument("--stress-max-b", type=int, default=1_000_000)
    args = parser.parse_args()
    if args.identity_limit < 1 or args.definition_max_x < 4 or args.stress_max_b < 2:
        parser.error("limits must satisfy identity>=1, x>=4, and b>=2")

    check_identity_grid(args.identity_limit)
    direct = definition_scan(args.definition_max_x)
    stress = exact_quadratic_solutions(args.stress_max_b)
    if direct != [[4, 0]]:
        raise AssertionError(f"unexpected direct solutions: {direct}")
    if stress != [[1, 2]]:
        raise AssertionError(f"unexpected (a,b) stress solutions: {stress}")

    print(
        json.dumps(
            {
                "definition_scan": {
                    "max_x": args.definition_max_x,
                    "solutions_xy": direct,
                },
                "factorization_identity_grid": {
                    "a_max": args.identity_limit,
                    "b_min": 2,
                    "b_max": args.identity_limit + 1,
                    "status": "PASS",
                },
                "quadratic_discriminant_scan": {
                    "b_min": 2,
                    "b_max": args.stress_max_b,
                    "solutions_ab": stress,
                },
                "status": "PASS",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
