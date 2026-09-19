#!/usr/bin/env python3
"""Exact q-Pascal, recurrence, and Lucas-Schur audit for the (5,6) ray."""

from __future__ import annotations

import argparse
import hashlib
import json
from functools import lru_cache


Polynomial = tuple[int, ...]
ZERO: Polynomial = ()
ONE: Polynomial = (1,)
EXPECTED_BASE_SHA256 = "a81cde2c90ed902f5e0f02012969e532e497a9bcc4496169fffa96540be84ea9"


def trim(values: list[int]) -> Polynomial:
    while values and values[-1] == 0:
        values.pop()
    return tuple(values)


def add(*polys: Polynomial) -> Polynomial:
    result = [0] * max((len(poly) for poly in polys), default=0)
    for poly in polys:
        for degree, coefficient in enumerate(poly):
            result[degree] += coefficient
    return trim(result)


def neg(poly: Polynomial) -> Polynomial:
    return tuple(-coefficient for coefficient in poly)


def shift(poly: Polynomial, degree: int) -> Polynomial:
    return (0,) * degree + poly if poly else ZERO


def shift_down(poly: Polynomial, degree: int) -> Polynomial:
    assert all(coefficient == 0 for coefficient in poly[:degree])
    return trim(list(poly[degree:]))


def value(poly: Polynomial | list[int], index: int) -> int:
    return poly[index] if 0 <= index < len(poly) else 0


@lru_cache(maxsize=None)
def gaussian(n: int, r: int) -> Polynomial:
    if r < 0 or r > n or n < 0:
        return ZERO
    r = min(r, n - r)
    if r == 0:
        return ONE
    return add(gaussian(n - 1, r), shift(gaussian(n - 1, r - 1), n - r))


def partition_table(parts: tuple[int, ...], limit: int) -> list[int]:
    values = [0] * (limit + 1)
    values[0] = 1
    for part in parts:
        for degree in range(part, limit + 1):
            values[degree] += values[degree - part]
    return values


def formula_h(k: int, i: int, p6: list[int], p5: list[int]) -> int:
    """Restricted-partition formula for the ordinary Schur layer."""
    return (
        value(p6, i)
        - sum(value(p6, i - 5 * k - nu) for nu in range(1, 7))
        + sum(
            value(p6, i - 10 * k - mu - nu)
            for mu in range(1, 7)
            for nu in range(mu + 1, 7)
        )
        - value(p5, i)
        + sum(value(p5, i - 6 * k - nu) for nu in range(1, 6))
        - sum(
            value(p5, i - 12 * k - mu - nu)
            for mu in range(1, 6)
            for nu in range(mu + 1, 6)
        )
    )


def ordinary_difference(k: int) -> Polynomial:
    return add(gaussian(5 * k + 6, 6), neg(gaussian(6 * k + 5, 5)))


def direct_h(k: int) -> list[int]:
    difference = ordinary_difference(k)
    return [value(difference, i) - value(difference, i - 1) for i in range(15 * k + 1)]


def ell_table(limit: int) -> list[list[int]]:
    """Schur coefficients ell(n,r) of the Lucas polynomial F_(n+1)."""
    rows: list[list[int]] = []
    for n in range(limit + 1):
        row = []
        for r in range(n // 2 + 1):
            coefficient = int(n == 0 and r == 0)
            if n >= 1 and r < len(rows[n - 1]):
                coefficient += rows[n - 1][r]
            if n >= 1 and r >= 1 and r - 1 < len(rows[n - 1]):
                coefficient += rows[n - 1][r - 1]
            if n >= 2 and r >= 1 and r - 1 < len(rows[n - 2]):
                coefficient += rows[n - 2][r - 1]
            row.append(coefficient)
        rows.append(row)
    return rows


def ell(rows: list[list[int]], n: int, r: int) -> int:
    if n < 0 or r < 0 or 2 * r > n:
        return 0
    return rows[n][r]


def lucas_schur_from_layers(
    layers: list[int], degree: int, rows: list[list[int]], leading_sign: int
) -> list[int]:
    """Apply e2 -> -e2 and expand in the two-row Schur basis."""
    return [
        sum(
            leading_sign * (-1) ** i * layers[i] * ell(rows, degree - 2 * i, r - i)
            for i in range(r + 1)
        )
        for r in range(degree // 2 + 1)
    ]


def paired_remainder(layers: list[int], degree: int, rows: list[list[int]]) -> list[int]:
    result = [0] * (degree // 2 + 1)
    for pair in range(len(layers) // 2):
        a = layers[2 * pair]
        b = layers[2 * pair + 1]
        c = 2 * a - b
        assert a >= 0 and c >= 0
        schur_shift = 2 * pair
        m = degree - 4 * pair + 1
        for r in range(len(result)):
            local = r - schur_shift
            kernel = (
                ell(rows, m - 2, local)
                + ell(rows, m - 3, local - 2)
                + ell(rows, m - 4, local - 2)
            )
            result[r] += a * kernel + c * ell(rows, m - 3, local - 1)
    if len(layers) % 2:
        endpoint = len(layers) - 1
        assert endpoint % 2 == 0 and layers[endpoint] >= 0
        result[endpoint] += layers[endpoint]
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=35)
    args = parser.parse_args()
    if args.max_k < 3:
        parser.error("need --max-k >= 3")

    p6 = partition_table((2, 3, 4, 5, 6), 15 * args.max_k)
    p5 = partition_table((2, 3, 4, 5), 15 * args.max_k)
    rows = ell_table(30 * args.max_k + 2)
    schur_rows: dict[int, list[int]] = {}
    least: tuple[int, int, int] | None = None

    assert ordinary_difference(1) == ZERO
    schur_rows[1] = [0] * 16
    for k in range(2, args.max_k + 1):
        layers = direct_h(k)
        assert layers == [formula_h(k, i, p6, p5) for i in range(15 * k + 1)]
        direct = lucas_schur_from_layers(layers, 30 * k, rows, 1)
        schur_rows[k] = direct
        assert direct[:6] == [0, 0, 0, 0, 0, 0]
        assert direct[6] == 1 and min(direct[6:]) > 0
        current = min((coefficient, k, r) for r, coefficient in enumerate(direct) if coefficient)
        least = current if least is None else min(least, current)

        if k < 3:
            continue
        previous_layers = direct_h(k - 2)
        remainder_layers = [
            layers[r + 6] - value(previous_layers, r - 24)
            for r in range(15 * k - 5)
        ]
        polynomial_remainder = shift_down(
            add(ordinary_difference(k), neg(shift(ordinary_difference(k - 2), 30))),
            6,
        )
        assert [
            value(polynomial_remainder, r) - value(polynomial_remainder, r - 1)
            for r in range(15 * k - 5)
        ] == remainder_layers

        for pair in range(len(remainder_layers) // 2):
            a = remainder_layers[2 * pair]
            c = 2 * a - remainder_layers[2 * pair + 1]
            assert a >= 0 and c >= 0, ("remainder layer sign", k, pair, a, c)
        if len(remainder_layers) % 2:
            assert remainder_layers[-1] >= 0

        remainder = lucas_schur_from_layers(remainder_layers, 30 * k - 12, rows, 1)
        assert remainder == paired_remainder(remainder_layers, 30 * k - 12, rows)
        assert min(remainder) > 0
        reconstructed = [0] * (15 * k + 1)
        for r, coefficient in enumerate(schur_rows[k - 2]):
            reconstructed[r + 30] += coefficient
        for r, coefficient in enumerate(remainder):
            reconstructed[r + 6] += coefficient
        assert reconstructed == direct

    base_record = [schur_rows[1], schur_rows[2]]
    base_digest = hashlib.sha256(
        json.dumps(base_record, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_BASE_SHA256:
        assert base_digest == EXPECTED_BASE_SHA256, base_digest

    print("exact q-Pascal/restricted-partition audit passed")
    print(f"two bases and Schur-layer recurrence checked through k={args.max_k}")
    print(f"paired and even-endpoint positivity checked through k={args.max_k}")
    print(f"least nonzero Lucas Schur coefficient: {least}")
    print(f"two-base Schur-row SHA-256: {base_digest}")


if __name__ == "__main__":
    main()
