#!/usr/bin/env python3
"""Exact/ball audits for PROOF.md, not an exhaustive proof of majorisation."""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from itertools import product
from math import comb, factorial
from pathlib import Path
from random import Random

from flint import arb, ctx, fmpq


ROOT = Path(__file__).resolve().parent
PRECISION = 256


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ArithmeticError(message)


def ball(q: F | int) -> arb:
    q = F(q)
    return arb(fmpq(q.numerator, q.denominator))


def dimension_factor(m: int, n: int) -> arb:
    return arb(m) ** (n // 2) * (arb(m).sqrt() if n % 2 else arb(1))


def constant(n: int, p: int, q: int) -> arb:
    return ball(F(q - 1, p - 1)) * dimension_factor(p, n) / dimension_factor(q, n)


def two_atom_gap(n: int, m: int, source: F, target: F) -> arb:
    """Variance s=1; stable difference of exact binomial moment formulas."""
    require(source > target >= 0, "separations must strictly contract")
    value = arb(0)
    for j in range(1, m):
        rate = F(j * (m - j), 2 * m)
        e = ball(rate * target * target)
        loss = ball(rate * (source * source - target * target))
        value += comb(m, j) * (-e).exp() * (-(-loss).expm1())
    return value / (2 ** m * dimension_factor(m, n))


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def norm2(x):
    return dot(x, x)


def variance(points):
    m = len(points)
    mean = tuple(sum(x[j] for x in points) / m for j in range(len(points[0])))
    return sum(norm2(tuple(a - b for a, b in zip(x, mean))) for x in points)


def exact_variance_audit() -> tuple[int, str]:
    rng = Random(20260926)
    digest = hashlib.sha256()
    for case in range(300):
        m = 2 + case % 11
        dimension = 1 + case % 7
        points = [tuple(F(rng.randrange(-8, 9), rng.randrange(1, 8))
                        for _ in range(dimension)) for _ in range(m + 1)]
        old = variance(points[:-1])
        mean = tuple(sum(x[j] for x in points[:-1]) / m for j in range(dimension))
        increment = F(m, m + 1) * norm2(tuple(a - b for a, b in zip(points[-1], mean)))
        new = variance(points)
        require(new == old + increment and increment >= 0, "variance update failed")
        pair_sum = sum(norm2(tuple(a - b for a, b in zip(points[i], points[j])))
                       for i in range(m + 1) for j in range(i))
        require(pair_sum == (m + 1) * new, "pair variance formula failed")
        digest.update(f"{case}|{m}|{dimension}|{old}|{increment}|{new}\n".encode())
    return 300, digest.hexdigest()


def ordered_replica_gap(n: int, m: int, source: F, target: F) -> arb:
    """Independent ordered Bernoulli tuples, without binomial multiplicities."""
    value = arb(0)
    for row in product((0, 1), repeat=m):
        pairs = sum((row[i] - row[j]) ** 2 for i in range(m) for j in range(i))
        ex = ball(F(pairs, 2 * m) * source * source)
        ey = ball(F(pairs, 2 * m) * target * target)
        value += (-ey).exp() - (-ex).exp()
    return value / (2 ** m * dimension_factor(m, n))


def audit() -> dict:
    ctx.prec = PRECISION
    variance_count, variance_hash = exact_variance_audit()
    comparisons = 0
    ordered_checks = 0
    regimes = ((F(1, 10), F(0)), (F(1), F(1, 2)),
               (F(3), F(2)), (F(11), F(10)))
    for n in (1, 2, 3, 7, 20):
        for source, target in regimes:
            gaps = {m: two_atom_gap(n, m, source, target) for m in range(2, 10)}
            require(all(g > 0 for g in gaps.values()), "unresolved moment positivity")
            for p in range(2, 9):
                for q in range(p + 1, 10):
                    require(constant(n, p, q) * gaps[p] - gaps[q] > 0,
                            "relative moment bound failed or was not enclosed")
                    comparisons += 1
            if n in (1, 3):
                for m in range(2, 9):
                    direct = ordered_replica_gap(n, m, source, target)
                    require(direct.overlaps(gaps[m]), "replica normalizations disagree")
                    ordered_checks += 1

    # Finite calibrations of both limiting sharpness mechanisms.
    k23 = constant(3, 2, 3)
    eps = F(1, 10 ** 6)
    near_ratio = two_atom_gap(3, 3, eps, F(0)) / two_atom_gap(3, 2, eps, F(0))
    require(k23 - near_ratio > 0 and k23 - near_ratio < ball(F(1, 10 ** 12)),
            "near-point calibration failed")
    far_ratio = two_atom_gap(3, 3, F(21), F(20)) / two_atom_gap(3, 2, F(21), F(20))
    require(far_ratio > 0 and far_ratio < ball(F(1, 10 ** 12)),
            "far-separated calibration failed")
    # These deliberately NONCONVEX energies test necessity of the cone.
    first_gap = two_atom_gap(3, 2, F(1, 10), F(0)) - two_atom_gap(3, 3, F(1, 10), F(0))
    second_gap = -two_atom_gap(3, 2, F(11), F(10)) + two_atom_gap(3, 3, F(11), F(10))
    require(first_gap < 0 and second_gap < 0, "two-power necessity fixtures failed")

    endpoint = ball(F(243, 32)).sqrt()
    require(endpoint > ball(F(5, 2)) and endpoint < 3, "exponential endpoint failed")
    prefix = arb(0)
    prefixes = 0
    for m in range(2, 81):
        prefix += ball(F((-5) ** m * (m - 1), 2 ** m * factorial(m))) / dimension_factor(m, 3)
        require(prefix > 0, "positive exponential prefix not enclosed")
        prefixes += 1
    # At a=5/2 and z=9/10 the second Euler pressure derivative is negative.
    a, z = F(5, 2), F(9, 10)
    pressure_second = ball(a * a * z * z * (2 - a * z)) * (-ball(a * z)).exp()
    require(pressure_second < 0, "PC2 exclusion not enclosed")

    result = {
        "precision_bits": PRECISION,
        "exact_variance_cases": variance_count,
        "exact_variance_sha256": variance_hash,
        "strict_relative_gap_enclosures": comparisons,
        "ordered_replica_crosschecks": ordered_checks,
        "exponential_positive_prefixes": prefixes,
        "near_point_ratio_distance_to_sharp_constant": "strictly between 0 and 10^-12",
        "far_separated_ratio": "strictly between 0 and 10^-12",
        "nonconvex_necessity_fixture_signs": [-1, -1],
        "exponential_endpoint_squared": "243/32",
        "a_5_over_2_pc2_witness_sign": -1,
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["audit_sha256"] = hashlib.sha256(encoded).hexdigest()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.check:
        expected = json.loads((ROOT / "EXPECTED.json").read_text())
        require(result == expected, "audit does not match EXPECTED.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
