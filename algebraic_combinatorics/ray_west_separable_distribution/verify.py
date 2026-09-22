#!/usr/bin/env python3
"""Exact audit of the Ray--West correction on separable permutations.

The audit has two independent layers:

1. solve the claimed algebraic generating-function equation coefficientwise;
2. enumerate permutations through a requested order, recover the canonical
   signed Schroeder decomposition, and compare its local statistic with the
   original Ray--West active-insertion definition.

Only Python arbitrary-precision integers and the standard library are used.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from functools import lru_cache
from itertools import combinations_with_replacement, permutations


Permutation = tuple[int, ...]
Poly = tuple[int, ...]  # coefficient k is [u^k]

ZERO: Poly = (0,)
ONE: Poly = (1,)


def trim(values: list[int] | tuple[int, ...]) -> Poly:
    values = list(values)
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values) if values else ZERO


def poly_add(left: Poly, right: Poly) -> Poly:
    return trim([
        (left[i] if i < len(left) else 0)
        + (right[i] if i < len(right) else 0)
        for i in range(max(len(left), len(right)))
    ])


def poly_neg(poly: Poly) -> Poly:
    return tuple(-coefficient for coefficient in poly)


def poly_scale(poly: Poly, scalar: int) -> Poly:
    return trim([scalar * coefficient for coefficient in poly])


def poly_mul(left: Poly, right: Poly) -> Poly:
    answer = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            answer[i + j] += x * y
    return trim(answer)


# H=(1-uz)(1+z-2uz), C=(1-u)z^2,
# B=(z-1)H-2C, E=zH-2C.
H_COEFFICIENTS: tuple[Poly, ...] = (ONE, (1, -3), (0, -1, 2))
C_COEFFICIENTS: tuple[Poly, ...] = (ZERO, ZERO, (1, -1))


def polynomial_data() -> tuple[list[Poly], list[Poly]]:
    b: list[Poly] = []
    e: list[Poly] = []
    for n in range(4):
        h_n = H_COEFFICIENTS[n] if n < len(H_COEFFICIENTS) else ZERO
        h_previous = H_COEFFICIENTS[n - 1] if 0 <= n - 1 < len(H_COEFFICIENTS) else ZERO
        c_n = C_COEFFICIENTS[n] if n < len(C_COEFFICIENTS) else ZERO
        b.append(poly_add(poly_add(h_previous, poly_neg(h_n)), poly_scale(c_n, -2)))
        e.append(poly_add(h_previous, poly_scale(c_n, -2)))
    if b[0] != (-1,):
        raise AssertionError("the formal equation must determine each coefficient uniquely")
    return b, e


def j_square_coefficient(series: list[Poly], degree: int) -> Poly:
    answer = ZERO
    for left_degree in range(1, degree):
        answer = poly_add(
            answer,
            poly_mul(series[left_degree], series[degree - left_degree]),
        )
    return answer


def residual_coefficient(series: list[Poly], degree: int) -> Poly:
    """Coefficient of z^degree in HJ^2+((z-1)H-2C)J+zH-2C."""
    b, e = polynomial_data()
    answer = ZERO
    for k, h_k in enumerate(H_COEFFICIENTS):
        if k <= degree:
            answer = poly_add(
                answer,
                poly_mul(h_k, j_square_coefficient(series, degree - k)),
            )
    for k, b_k in enumerate(b):
        if k <= degree:
            answer = poly_add(answer, poly_mul(b_k, series[degree - k]))
    if degree < len(e):
        answer = poly_add(answer, e[degree])
    return answer


def algebraic_coefficients(limit: int) -> list[Poly]:
    """Solve the quadratic recursively for its unique solution J in z*Z[u][[z]]."""
    if limit < 1:
        raise ValueError("limit must be positive")
    b, e = polynomial_data()
    series = [ZERO for _ in range(limit + 1)]
    for degree in range(1, limit + 1):
        # The only occurrence of the unknown coefficient is b[0]*J_degree=-J_degree.
        rest = ZERO
        for k, h_k in enumerate(H_COEFFICIENTS):
            if k <= degree:
                rest = poly_add(
                    rest,
                    poly_mul(h_k, j_square_coefficient(series, degree - k)),
                )
        for k in range(1, min(len(b), degree + 1)):
            rest = poly_add(rest, poly_mul(b[k], series[degree - k]))
        if degree < len(e):
            rest = poly_add(rest, e[degree])
        series[degree] = rest
        if residual_coefficient(series, degree) != ZERO:
            raise AssertionError((degree, residual_coefficient(series, degree)))
    return series


def standardize(word: Permutation) -> Permutation:
    ranks = {value: rank + 1 for rank, value in enumerate(sorted(word))}
    return tuple(ranks[value] for value in word)


@lru_cache(maxsize=None)
def canonical_tree_j(permutation: Permutation) -> int | None:
    """Return the local tree statistic, or None for a nonseparable permutation."""
    n = len(permutation)
    if n == 1:
        return 0
    direct_cuts = [
        k for k in range(1, n)
        if set(permutation[:k]) == set(range(1, k + 1))
    ]
    skew_cuts = [
        k for k in range(1, n)
        if set(permutation[:k]) == set(range(n - k + 1, n + 1))
    ]
    if direct_cuts and skew_cuts:
        raise AssertionError((permutation, direct_cuts, skew_cuts))
    cuts = direct_cuts or skew_cuts
    if not cuts:
        return None
    boundaries = [0, *cuts, n]
    children = [
        standardize(permutation[left:right])
        for left, right in zip(boundaries, boundaries[1:])
    ]
    child_values = [canonical_tree_j(child) for child in children]
    if any(value is None for value in child_values):
        return None
    if direct_cuts:
        marked_junctions = sum(
            left == tuple(range(len(left), 0, -1))
            and right == tuple(range(len(right), 0, -1))
            for left, right in zip(children, children[1:])
        )
    else:
        marked_junctions = sum(
            left == tuple(range(1, len(left) + 1))
            and right == tuple(range(1, len(right) + 1))
            for left, right in zip(children, children[1:])
        )
    return sum(value for value in child_values if value is not None) + marked_junctions


def active_site(permutation: Permutation, row: int, column: int) -> bool:
    n = len(permutation)
    return not (
        (column <= n and permutation[column - 1] == row)
        or (column > 1 and permutation[column - 2] == row)
    )


def insert_pair(
    permutation: Permutation,
    rho: tuple[int, int],
    rows: tuple[int, int],
    columns: tuple[int, int],
) -> Permutation:
    answer: list[int | None] = [None] * (len(permutation) + 2)
    for column_rank, row_rank in enumerate(rho, start=1):
        full_column = columns[column_rank - 1] + column_rank - 1
        full_row = rows[row_rank - 1] + row_rank - 1
        answer[full_column - 1] = full_row
    for old_column, old_row in enumerate(permutation, start=1):
        full_column = old_column + sum(c <= old_column for c in columns)
        full_row = old_row + sum(r <= old_row for r in rows)
        if answer[full_column - 1] is not None:
            raise AssertionError("insertion collision")
        answer[full_column - 1] = full_row
    result = tuple(value for value in answer if value is not None)
    if sorted(result) != list(range(1, len(permutation) + 3)):
        raise AssertionError("insertion did not produce a permutation")
    return result


@lru_cache(maxsize=None)
def active_insertion_j(permutation: Permutation) -> int:
    """Compute j from Ray--West's original codimension-two insertion definition."""
    sites = range(1, len(permutation) + 2)
    images: set[Permutation] = set()
    for rows in combinations_with_replacement(sites, 2):
        for columns in combinations_with_replacement(sites, 2):
            for rho in ((1, 2), (2, 1)):
                if all(
                    active_site(permutation, rows[rho[k] - 1], columns[k])
                    for k in range(2)
                ):
                    images.add(insert_pair(permutation, rho, rows, columns))
    n = len(permutation)
    active_total = (n**4 + 2 * n**3 + n**2 + 4 * n + 4) // 2
    return active_total - len(images)


def exhaustive_histograms(limit: int) -> tuple[list[Counter[int]], int]:
    """Compare canonical-tree and active-insertion values on all permutations."""
    if limit < 1:
        raise ValueError("limit must be positive")
    histograms: list[Counter[int]] = [Counter()]
    checked = 0
    for n in range(1, limit + 1):
        histogram: Counter[int] = Counter()
        for permutation in permutations(range(1, n + 1)):
            tree_value = canonical_tree_j(permutation)
            if tree_value is None:
                continue
            insertion_value = active_insertion_j(permutation)
            if tree_value != insertion_value:
                raise AssertionError((permutation, tree_value, insertion_value))
            histogram[tree_value] += 1
            checked += 1
        histograms.append(histogram)
    return histograms, checked


def integer_convolution(left: list[int], right: list[int], limit: int) -> list[int]:
    answer = [0] * (limit + 1)
    for i, x in enumerate(left):
        if i > limit:
            break
        for j, y in enumerate(right):
            if i + j > limit:
                break
            answer[i + j] += x * y
    return answer


def verify_first_moment_identity(series: list[Poly]) -> None:
    """Check (1-z)^2(1-z-2S)M=2z^2(S+1) coefficientwise."""
    limit = len(series) - 1
    counts = [sum(poly) for poly in series]
    moments = [sum(k * coefficient for k, coefficient in enumerate(poly)) for poly in series]
    one_minus_z_squared = [1, -2, 1] + [0] * max(0, limit - 2)
    discriminant_root = [0] * (limit + 1)
    discriminant_root[0] = 1
    if limit >= 1:
        discriminant_root[1] = -1
    for n in range(1, limit + 1):
        discriminant_root[n] -= 2 * counts[n]
    left = integer_convolution(
        integer_convolution(one_minus_z_squared, discriminant_root, limit),
        moments,
        limit,
    )
    right = [0] * (limit + 1)
    for n in range(2, limit + 1):
        right[n] = 2 * (counts[n - 2] + (1 if n == 2 else 0))
    if left != right:
        mismatch = next(i for i in range(limit + 1) if left[i] != right[i])
        raise AssertionError((mismatch, left[mismatch], right[mismatch]))


def histogram_dict(poly: Poly) -> dict[str, int]:
    return {str(k): coefficient for k, coefficient in enumerate(poly) if coefficient}


def run(max_series: int, max_exhaustive: int) -> dict[str, object]:
    if max_series < max_exhaustive:
        raise ValueError("max-series must be at least max-exhaustive")
    series = algebraic_coefficients(max_series)
    verify_first_moment_identity(series)
    exhaustive, checked = exhaustive_histograms(max_exhaustive)
    for n in range(1, max_exhaustive + 1):
        highest = max(exhaustive[n])
        expected = trim([exhaustive[n][k] for k in range(highest + 1)])
        if series[n] != expected:
            raise AssertionError((n, series[n], expected))
    displayed = min(10, max_series)
    result: dict[str, object] = {
        "status": "PASS",
        "series_degree": max_series,
        "quadratic_residual": f"zero through z^{max_series}",
        "moment_identity": f"zero through z^{max_series}",
        "independent_insertion_max_n": max_exhaustive,
        "independent_insertion_permutations": checked,
        "histograms": {
            str(n): histogram_dict(series[n]) for n in range(1, displayed + 1)
        },
    }
    for n in (20, 30):
        if n <= max_series:
            result[f"n{n}_count"] = sum(series[n])
            result[f"n{n}_first_moment"] = sum(
                k * coefficient for k, coefficient in enumerate(series[n])
            )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-series", type=int, default=30)
    parser.add_argument("--max-exhaustive", type=int, default=7)
    args = parser.parse_args()
    print(json.dumps(run(args.max_series, args.max_exhaustive), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
