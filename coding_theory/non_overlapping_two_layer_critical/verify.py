#!/usr/bin/env python3
"""Independent checks for the last-two-layer SQN critical-set theorem.

The reference path uses Python arbitrary-precision integers.  It obtains each
bivariate objective by six definition-level evaluations, enumerates every
feasible pair on complete small trees, and compares that maximum with the
critical set.  It does not call the C++ symbolic routines.
"""

from __future__ import annotations

import argparse
from itertools import product
import json
import subprocess


KNOWN = {8: 8, 10: 24, 12: 81, 14: 274, 16: 927, 18: 3160, 20: 11272}

EXPECTED_CPP = {
    8: (8, 1, 4, 2, 2),
    10: (24, 2, 10, 3, 2),
    12: (81, 4, 31, 7, 3),
    14: (274, 10, 142, 20, 4),
    16: (927, 31, 967, 67, 5),
    18: (3160, 142, 10723, 308, 5),
    20: (11272, 967, 192656, 2176, 5),
    22: (40202, 10723, 6001931, 23642, 5),
    24: (147312, 192656, 321286030, 430794, 5),
}


def conv(left: list[int], right: list[int], index: int) -> int:
    return sum(left[j] * right[index - 1 - j] for j in range(index))


def conditions(left: list[int], right: list[int], n: int) -> list[int]:
    values = [0] * n
    sides = [0] * n
    parameter = [[0] * (i + 1) for i in range((n + 1) // 2)]
    for i in range(len(parameter)):
        parameter[i][i] = 1
    for index in range(len(left)):
        for j in range(index):
            for k in range(j - 1, -1, -1):
                parameter[j][k] = sum(
                    (right[j - ell - 1] if sides[n - index + ell - 1]
                     else left[j - ell - 1]) * parameter[ell][k]
                    for ell in range(k, j)
                )
        pos = n - index - 2
        value = right[index] - left[index]
        for j in range(index):
            inner = sum(
                parameter[j][ell] * (right[ell] - left[ell])
                for ell in range(j + 1)
            )
            factor = (right[index - j - 1] if sides[n - index + j - 1]
                      else left[index - j - 1])
            value += inner * factor
        values[pos] = value
        sides[pos] = int(value >= 0)
    return values


def score(prefix_l: list[int], prefix_r: list[int], n: int,
          u: int, t: int, force_m1_left: bool | None = None) -> int:
    m = n // 2
    left = prefix_l + [u] + [0] * (n - 2 - len(prefix_l))
    right = prefix_r + [conv(prefix_l, prefix_r, m - 2) - u] + [0] * (
        n - 2 - len(prefix_r)
    )
    cond = conditions(left[:m - 1], right[:m - 1], n)
    sm = conv(left, right, m - 1)
    left[m - 1] = t
    right[m - 1] = sm - t
    for index in range(m, n - 1):
        total = conv(left, right, index)
        choose_left = cond[index] > 0
        if index == m and force_m1_left is not None:
            choose_left = force_m1_left
        if choose_left:
            left[index] = total
        else:
            right[index] = total
    return conv(left, right, n - 1)


def interpolate(prefix_l: list[int], prefix_r: list[int], n: int,
                side: bool) -> tuple[int, int, int, int, int, int]:
    f00 = score(prefix_l, prefix_r, n, 0, 0, side)
    f10 = score(prefix_l, prefix_r, n, 1, 0, side)
    f20 = score(prefix_l, prefix_r, n, 2, 0, side)
    f01 = score(prefix_l, prefix_r, n, 0, 1, side)
    f02 = score(prefix_l, prefix_r, n, 0, 2, side)
    f11 = score(prefix_l, prefix_r, n, 1, 1, side)
    c20_num = f20 - 2 * f10 + f00
    c02_num = f02 - 2 * f01 + f00
    assert c20_num % 2 == c02_num % 2 == 0
    c20 = c20_num // 2
    c02 = c02_num // 2
    c10 = f10 - f00 - c20
    c01 = f01 - f00 - c02
    c11 = f11 - f00 - c10 - c01 - c20 - c02
    assert c02 == -1
    return c20, c11, c02, c10, c01, f00


def restrict_le(interval: tuple[int, int] | None, a: int, b: int,
                rhs: int) -> tuple[int, int] | None:
    if interval is None:
        return None
    lo, hi = interval
    target = rhs - b
    if a > 0:
        hi = min(hi, target // a)
    elif a < 0:
        lo = max(lo, -((-target) // a))
    elif b > rhs:
        return None
    return (lo, hi) if lo <= hi else None


def restrict_ge(interval: tuple[int, int] | None, a: int, b: int,
                rhs: int) -> tuple[int, int] | None:
    return restrict_le(interval, -a, -b, -rhs)


def quadratic_points(a: int, b: int, lo: int, hi: int,
                     residue: int = 0, step: int = 1) -> set[int]:
    first = lo + ((residue - lo) % step)
    if first > hi:
        return set()
    last = hi - ((hi - residue) % step)
    count = (last - first) // step
    if a >= 0:
        return {first, last}
    az = a * step * step
    bz = (2 * a * first + b) * step
    z0 = (-bz) // (2 * az)
    return {first + step * min(count, max(0, z)) for z in (z0, z0 + 1)}


def critical_pairs(coeff: tuple[int, int, int, int, int, int],
                   sm: tuple[int, int], interval: tuple[int, int]) -> set[tuple[int, int]]:
    c20, c11, c02, c10, c01, c00 = coeff
    assert c02 == -1
    p, r = sm
    # Q=-t^2+B(u)t+C(u).
    ba, bb = c11, c01
    out: set[tuple[int, int]] = set()

    lower = restrict_le(interval, ba, bb, 0)
    if lower:
        for u in quadratic_points(c20, c10, *lower):
            out.add((u, 0))

    interior = restrict_ge(interval, ba, bb, 1)
    interior = restrict_le(interior, ba - 2 * p, bb - 2 * r, -1)
    if interior:
        h2 = 4 * c20 + ba * ba
        h1 = 4 * c10 + 2 * ba * bb
        if ba % 2 == 0:
            parity = bb & 1
            for u in quadratic_points(h2, h1, *interior):
                assert ((ba * u + bb) & 1) == parity
                out.add((u, (ba * u + bb) // 2))
        else:
            for residue in (0, 1):
                for u in quadratic_points(h2, h1, *interior, residue, 2):
                    out.add((u, (ba * u + bb) // 2))

    upper = restrict_ge(interval, ba, bb, 1)
    upper = restrict_ge(upper, ba - 2 * p, bb - 2 * r, 0)
    if upper:
        a2 = c20 - p * p + ba * p
        a1 = c10 - 2 * p * r + ba * r + bb * p
        for u in quadratic_points(a2, a1, *upper):
            out.add((u, p * u + r))
    return out


def verify_n(n: int) -> dict[str, int]:
    m = n // 2
    best_brute = -1
    best_critical = -1
    prefixes = 0
    leaves = 0
    candidates = 0
    polynomial_checks = 0
    condition_checks = 0

    def visit(left: list[int], right: list[int]) -> None:
        nonlocal best_brute, best_critical, prefixes, leaves, candidates
        nonlocal polynomial_checks, condition_checks
        level = len(left)
        if level == m - 2:
            prefixes += 1
            a_total = conv(left, right, m - 2)
            sm0 = conv(left + [0], right + [a_total], m - 1)
            sm1 = conv(left + [1], right + [a_total - 1], m - 1)
            p, r = sm1 - sm0, sm0
            cond0 = conditions(left + [0], right + [a_total], n)[m]
            cond1 = conditions(left + [1], right + [a_total - 1], n)[m]
            assert cond1 - cond0 == -2
            condition_checks += 1

            actual: dict[tuple[int, int], int] = {}
            for u in range(a_total + 1):
                smu = p * u + r
                assert smu >= 0
                for t in range(smu + 1):
                    actual[u, t] = score(left, right, n, u, t)
            leaves += len(actual)
            best_brute = max(best_brute, *actual.values())

            selected: set[tuple[int, int]] = set()
            for side in (False, True):
                coeff = interpolate(left, right, n, side)
                for u, t in actual:
                    forced = score(left, right, n, u, t, side)
                    c20, c11, c02, c10, c01, c00 = coeff
                    predicted = (c20*u*u + c11*u*t + c02*t*t +
                                 c10*u + c01*t + c00)
                    assert forced == predicted
                    polynomial_checks += 1
                interval = (0, a_total)
                if side:
                    interval = restrict_ge(interval, -2, cond0, 1)
                else:
                    interval = restrict_le(interval, -2, cond0, 0)
                if interval:
                    selected |= critical_pairs(coeff, (p, r), interval)
            assert selected
            for u, t in selected:
                assert 0 <= u <= a_total and 0 <= t <= p * u + r
            candidate_best = max(actual[pair] for pair in selected)
            assert candidate_best == max(actual.values())
            candidates += len(selected)
            best_critical = max(best_critical, candidate_best)
            return

        total = 2 if level == 0 else conv(left, right, level)
        minimum = 1 if level == 0 else 0
        maximum = total
        if all(x == y for x, y in zip(left, right)):
            maximum //= 2
        for x in range(minimum, maximum + 1):
            visit(left + [x], right + [total - x])

    visit([], [])
    assert best_brute == best_critical == KNOWN[n]
    return {
        "n": n, "best": best_brute, "prefixes": prefixes,
        "raw_two_layer_leaves": leaves, "critical_pairs": candidates,
        "polynomial_checks": polynomial_checks,
        "condition_slope_checks": condition_checks,
    }


def test_optimizer() -> int:
    checked = 0
    for c20, c11, c10, c01, p, r, hi in product(
        range(-3, 4), range(-3, 4), range(-3, 4), range(-3, 4),
        range(-2, 3), range(0, 5), range(0, 7)
    ):
        if min(r, p * hi + r) < 0:
            continue
        checked += 1
        coeff = (c20, c11, -1, c10, c01, 0)
        points = critical_pairs(coeff, (p, r), (0, hi))
        brute = {(u, t): c20*u*u+c11*u*t-t*t+c10*u+c01*t
                 for u in range(hi + 1) for t in range(p*u+r+1)}
        assert points, (coeff, p, r, hi)
        assert max(brute[pair] for pair in points) == max(brute.values()), (
            coeff, p, r, hi, points
        )
    assert checked == 309729
    return checked


def verify_cpp(binary: str) -> list[dict[str, int]]:
    """Check scalable summaries and definition-check displayed witnesses."""
    records = []
    for n, expected in EXPECTED_CPP.items():
        completed = subprocess.run(
            [binary, str(n)], check=True, capture_output=True, text=True
        )
        fields: dict[str, str] = {}
        for line in completed.stdout.splitlines():
            key, _, value = line.partition(" ")
            fields[key] = value
        keys = (
            "best",
            "prefixes",
            "raw_two_layer_leaves",
            "critical_pairs",
            "maximum_candidates_per_prefix",
        )
        actual = tuple(int(fields[key]) for key in keys)
        assert actual == expected, (n, actual, expected)
        assert int(fields["condition_slope_checks"]) == actual[1]
        assert actual[3] <= 16 * actual[1]

        left = tuple(map(int, fields["L"].split()))
        right = tuple(map(int, fields["R"].split()))
        assert len(left) == len(right) == n - 1
        assert left[0] + right[0] == 2 and left[0] > 0 and right[0] > 0
        for index in range(1, n - 1):
            total = sum(left[j] * right[index - 1 - j] for j in range(index))
            assert left[index] + right[index] == total
        objective = sum(left[j] * right[n - 2 - j] for j in range(n - 1))
        assert objective == actual[0]
        assert all(
            left[index] == 0 or right[index] == 0
            for index in range(n // 2, n - 1)
        )
        records.append({"n": n, **dict(zip(keys, actual))})
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", help="also verify the compiled C++ enumerator")
    parser.add_argument("--reference-max", type=int, default=18)
    args = parser.parse_args()
    if args.reference_max not in KNOWN:
        raise SystemExit("--reference-max must be a known even length from 8 to 20")

    checked = test_optimizer()
    references = [
        verify_n(n) for n in sorted(KNOWN) if n <= args.reference_max
    ]
    result: dict[str, object] = {
        "status": "PASS",
        "generic_quadratics_checked": checked,
        "reference_records": references,
    }
    if args.binary:
        result["cpp_records"] = verify_cpp(args.binary)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
