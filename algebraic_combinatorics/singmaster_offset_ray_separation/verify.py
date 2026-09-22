#!/usr/bin/env python3
"""Exact audit for strict inward Pascal rays and offset-curve separation.

The universal theorem is proved in README.md.  This standard-library checker
uses arbitrary-precision integers and Fraction arithmetic to audit the ratio
formula, strict log-concavity, level multiplicity, and sign corollaries on a
finite parameter box.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from math import comb


def ray_values(x: int, y: int, a: int, b: int) -> list[int]:
    """Return binom(x-ar,y+br) over its complete natural-number domain."""
    if not (a >= 1 and b >= 1 and x >= y >= 0):
        raise ValueError("require a,b>=1 and x>=y>=0")
    d_max = (x - y) // (a + b)
    return [comb(x - a * r, y + b * r) for r in range(d_max + 1)]


def factorial_ratio(x: int, y: int, a: int, b: int, r: int) -> Fraction:
    """Equation (1), independently from consecutive math.comb values."""
    n = x - a * r
    k = y + b * r
    ell = n - k
    if not (0 <= r < (x - y) // (a + b)):
        raise ValueError("r must have a successor on the ray")

    ratio = Fraction(1, 1)
    for i in range(a):
        ratio *= Fraction(ell - i, n - i)
    for j in range(b):
        ratio *= Fraction(ell - a - j, k + j + 1)
    return ratio


def audit_value_sequence(values: list[int]) -> tuple[int, int]:
    """Check strict log-concavity and its level/sign consequences."""
    if not values or any(value <= 0 for value in values):
        raise ValueError("values must be a nonempty positive sequence")

    strict_lc = 0
    for r in range(1, len(values) - 1):
        if not values[r] * values[r] > values[r - 1] * values[r + 1]:
            raise AssertionError(("strict LC", r, values))
        strict_lc += 1

    multiplicities = Counter(values)
    if max(multiplicities.values(), default=0) > 2:
        raise AssertionError(("threefold level", values))

    for m in range(1, len(values)):
        if values[m] != values[0]:
            continue
        if not all(values[r] > values[0] for r in range(1, m)):
            raise AssertionError(("inner sign", m, values))
        if not all(values[r] < values[0] for r in range(m + 1, len(values))):
            raise AssertionError(("outer sign", m, values))

    return strict_lc, sum(count == 2 for count in multiplicities.values())


def audit_ray(x: int, y: int, a: int, b: int) -> tuple[int, int, int]:
    """Audit one ray; return ratio, strict-LC, and repeated-level counts."""
    values = ray_values(x, y, a, b)
    ratios = [Fraction(values[r + 1], values[r]) for r in range(len(values) - 1)]

    for r, ratio in enumerate(ratios):
        if ratio != factorial_ratio(x, y, a, b, r):
            raise AssertionError(("ratio formula", x, y, a, b, r, ratio))

    for r in range(len(ratios) - 1):
        if not ratios[r] > ratios[r + 1]:
            raise AssertionError(("ratio descent", x, y, a, b, r, ratios))

    try:
        strict_lc, repeated_levels = audit_value_sequence(values)
    except (ValueError, AssertionError) as exc:
        raise AssertionError(("ray consequence", x, y, a, b, exc)) from exc

    return len(ratios), strict_lc, repeated_levels


def bounded_audit(max_x: int, max_step: int) -> dict[str, int]:
    totals = {
        "rays": 0,
        "ratio_checks": 0,
        "strict_lc_checks": 0,
        "repeated_levels": 0,
    }
    for x in range(max_x + 1):
        for y in range(x + 1):
            gap = x - y
            for a in range(1, min(max_step, gap - 1) + 1):
                for b in range(1, min(max_step, gap - a) + 1):
                    ratios, strict_lc, repeats = audit_ray(x, y, a, b)
                    totals["rays"] += 1
                    totals["ratio_checks"] += ratios
                    totals["strict_lc_checks"] += strict_lc
                    totals["repeated_levels"] += repeats
    return totals


def known_examples() -> None:
    # The nontrivial equal-offset collision 3003=C(15,5)=C(14,6).
    values = ray_values(15, 5, 1, 1)
    if values[:2] != [3003, 3003]:
        raise AssertionError(("3003 collision", values))
    if not all(value < 3003 for value in values[2:]):
        raise AssertionError(("3003 sign tail", values))

    # A ray with a strict interior peak and no repeated level.
    values = ray_values(24, 2, 2, 3)
    if not all(values[r] * values[r] > values[r - 1] * values[r + 1]
               for r in range(1, len(values) - 1)):
        raise AssertionError(("hand ray", values))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-x", type=int, default=100)
    parser.add_argument("--max-step", type=int, default=8)
    args = parser.parse_args()
    if args.max_x < 4 or args.max_step < 1:
        parser.error("require max-x>=4 and max-step>=1")

    known_examples()
    totals = bounded_audit(args.max_x, args.max_step)
    print(f"max_x={args.max_x}")
    print(f"max_step={args.max_step}")
    for key in ("rays", "ratio_checks", "strict_lc_checks", "repeated_levels"):
        print(f"{key}={totals[key]}")
    print("known_3003_collision=PASS")
    print("all_checks=PASS")


if __name__ == "__main__":
    main()
