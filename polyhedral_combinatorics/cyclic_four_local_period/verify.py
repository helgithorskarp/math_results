#!/usr/bin/env python3
"""Exact checks for the cyclic-index-four local Ehrhart formula."""

from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from math import comb, factorial
from pathlib import Path


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def trim(poly):
    out = list(poly)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_add(left, right, right_scale=1):
    out = [Fraction(0)] * max(len(left), len(right))
    for i in range(len(out)):
        if i < len(left):
            out[i] += left[i]
        if i < len(right):
            out[i] += Fraction(right_scale) * right[i]
    return trim(out)


def poly_mul(left, right):
    out = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return trim(out)


def poly_scale(scalar, poly):
    return trim([Fraction(scalar) * value for value in poly])


def poly_value(poly, x):
    value = Fraction(0)
    for coefficient in reversed(poly):
        value = value * x + coefficient
    return value


def interpolate(points):
    result = [Fraction(0)]
    for i, (x_i, y_i) in enumerate(points):
        basis = [Fraction(1)]
        denominator = 1
        for j, (x_j, _) in enumerate(points):
            if i != j:
                basis = poly_mul(basis, [Fraction(-x_j), Fraction(1)])
                denominator *= x_i - x_j
        result = poly_add(result, poly_scale(Fraction(y_i, denominator), basis))
    return trim(result)


def determinant(matrix):
    a = [[Fraction(value) for value in row] for row in matrix]
    value = Fraction(1)
    for col in range(len(a)):
        pivot = next((row for row in range(col, len(a)) if a[row][col]), None)
        if pivot is None:
            return 0
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            value = -value
        pivot_value = a[col][col]
        value *= pivot_value
        for j in range(col, len(a)):
            a[col][j] /= pivot_value
        for row in range(col + 1, len(a)):
            factor = a[row][col]
            for j in range(col, len(a)):
                a[row][j] -= factor * a[col][j]
    require(value.denominator == 1, "integral determinant became nonintegral")
    return value.numerator


def solve(matrix, rhs):
    n = len(matrix)
    a = [[Fraction(value) for value in row] + [Fraction(rhs[i])]
         for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if a[row][col])
        a[col], a[pivot] = a[pivot], a[col]
        pivot_value = a[col][col]
        a[col] = [value / pivot_value for value in a[col]]
        for row in range(n):
            if row == col:
                continue
            factor = a[row][col]
            a[row] = [a[row][j] - factor * a[col][j] for j in range(n + 1)]
    return tuple(a[i][-1] for i in range(n))


def kernel_matrix(profile):
    """Columns form a basis for {u:q.u=0 mod 4}."""
    g = len(profile)
    pivot = next(i for i, value in enumerate(profile) if value % 2)
    inverse = 1 if profile[pivot] == 1 else 3
    columns = []
    for j in range(g):
        if j == pivot:
            continue
        ratio = profile[j] * inverse % 4
        column = [0] * g
        column[j] = 1
        column[pivot] = -ratio
        columns.append(column)
    final = [0] * g
    final[pivot] = 4
    columns.append(final)
    return tuple(tuple(columns[j][i] for j in range(g)) for i in range(g)), pivot


def check_profile_lattice(profile):
    matrix, pivot = kernel_matrix(profile)
    require(abs(determinant(matrix)) == 4, "kernel basis does not have index four")
    for column in zip(*matrix):
        require(sum(q * u for q, u in zip(profile, column)) % 4 == 0,
                "kernel basis column violates the character")

    b = tuple(2 if i == pivot else 0 for i in range(len(profile)))
    vertex = solve(matrix, b)
    require(any(value.denominator == 2 for value in vertex), "apex is integral")
    require(all((2 * value).denominator == 1 for value in vertex),
            "apex is not half-integral")

    deletion_checks = 0
    for j, q in enumerate(profile):
        lam = 2 if q % 2 else 1
        endpoint_rhs = tuple(b[i] - (lam if i == j else 0)
                             for i in range(len(profile)))
        endpoint = solve(matrix, endpoint_rhs)
        require(all(value.denominator == 1 for value in endpoint),
                "proper subsystem has no integral endpoint")
        image = tuple(sum(matrix[i][r] * endpoint[r] for r in range(len(profile)))
                      for i in range(len(profile)))
        require(all(image[i] == b[i] for i in range(len(profile)) if i != j),
                "deleted-row witness failed")
        deletion_checks += 1
    return deletion_checks


def gaussian_multiply(left, right):
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c


def local_jump(profile):
    """Real part of prod_j (1-i^q_j)^(-1), exactly in Q."""
    numerator = (1, 0)
    for q in profile:
        if q == 1:
            numerator = gaussian_multiply(numerator, (1, 1))
        elif q == 2:
            numerator = gaussian_multiply(numerator, (1, 0))
        elif q == 3:
            numerator = gaussian_multiply(numerator, (1, -1))
        else:
            raise AssertionError("profile coordinate outside {1,2,3}")
    return Fraction(numerator[0], 2 ** len(profile))


@lru_cache(maxsize=None)
def slack_count(profile, n):
    """Count u>=0 with sum u_j/lambda_j<=n and q.u=2n mod 4."""
    limit = 2 * n
    dp = [[0] * 4 for _ in range(limit + 1)]
    dp[0][0] = 1
    for q in profile:
        weight = 1 if q % 2 else 2
        new = [[0] * 4 for _ in range(limit + 1)]
        for cost in range(limit + 1):
            for residue in range(4):
                if not dp[cost][residue]:
                    continue
                for u in range((limit - cost) // weight + 1):
                    new[cost + weight * u][(residue + q * u) % 4] += dp[cost][residue]
        dp = new
    target = 2 * n % 4
    return sum(dp[cost][target] for cost in range(limit + 1))


def literal_slack_count(profile, n):
    limit = 2 * n
    ranges = [range(limit // (1 if q % 2 else 2) + 1) for q in profile]
    total = 0
    for values in product(*ranges):
        cost = sum((1 if q % 2 else 2) * u for q, u in zip(profile, values))
        if cost <= limit and sum(q * u for q, u in zip(profile, values)) % 4 == 2 * n % 4:
            total += 1
    return total


def family_count(profile, free, n):
    return slack_count(profile, n) * (n + 1) ** free


def check_family(profile, free):
    d = len(profile) + free
    even = interpolate([(2 * j, family_count(profile, free, 2 * j))
                        for j in range(d + 1)])
    odd = interpolate([(2 * j + 1, family_count(profile, free, 2 * j + 1))
                       for j in range(d + 1)])
    alternating = poly_scale(Fraction(1, 2), poly_add(even, odd, -1))
    jump = local_jump(profile)
    expected = trim([jump * Fraction(comb(free, j), 2) for j in range(free + 1)])
    require(alternating == expected, f"alternating polynomial mismatch {(profile,free)}")
    for n in (2 * d + 2, 2 * d + 3):
        target = even if n % 2 == 0 else odd
        require(poly_value(target, n) == family_count(profile, free, n),
                f"holdout mismatch {(profile,free,n)}")
    return 2 * (d + 1) + 2


def run_checks():
    profiles = []
    lattice_checks = 0
    signs = {"negative": 0, "zero": 0, "positive": 0}
    for g in range(1, 7):
        for profile in product((1, 2, 3), repeat=g):
            if all(q == 2 for q in profile):
                continue
            lattice_checks += check_profile_lattice(profile)
            jump = local_jump(profile)
            signs["negative" if jump < 0 else "positive" if jump > 0 else "zero"] += 1
            profiles.append(profile)

    interpolation_checks = 0
    family_cases = 0
    records = []
    for profile in profiles:
        for free in range(3):
            interpolation_checks += check_family(profile, free)
            family_cases += 1
        records.append({
            "profile": "".join(map(str, profile)),
            "local_jump": str(local_jump(profile)),
        })

    literal_checks = 0
    for profile in ((1,), (1, 1), (1, 2), (1, 3), (1, 1, 1), (1, 2, 3)):
        for n in range(7):
            require(slack_count(profile, n) == literal_slack_count(profile, n),
                    f"literal count mismatch {(profile,n)}")
            literal_checks += 1

    require(local_jump((1, 3)) == Fraction(1, 2), "positive fixture failed")
    require(local_jump((1, 1)) == 0, "collapse fixture failed")
    require(local_jump((1, 1, 1)) == Fraction(-1, 4), "negative fixture failed")

    digest = sha256(json.dumps(records, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {
        "arithmetic": "exact Python int/Fraction; no floating point",
        "family_cases": family_cases,
        "interpolation_and_holdout_checks": interpolation_checks,
        "lattice_and_deletion_checks": lattice_checks,
        "literal_slack_counts": literal_checks,
        "profile_record_sha256": digest,
        "profiles": len(profiles),
        "sign_distribution": signs,
        "status": "PASS",
    }


def main():
    report = run_checks()
    expected = json.loads(Path(__file__).with_name("expected.json").read_text())
    require(report == expected, "report differs from expected.json")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
