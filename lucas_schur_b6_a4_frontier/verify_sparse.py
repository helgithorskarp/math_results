#!/usr/bin/env python3
"""Definition-level sparse Z[e1,e2] audit for the canonical Lucas (4,6) ray."""

from __future__ import annotations

import argparse
from functools import lru_cache
import math


Monomial = tuple[int, int]
Polynomial = dict[Monomial, int]
QPolynomial = tuple[int, ...]
ZERO: Polynomial = {}
ONE: Polynomial = {(0, 0): 1}
E1: Polynomial = {(1, 0): 1}


def clean(poly: Polynomial) -> Polynomial:
    return {monomial: coefficient for monomial, coefficient in poly.items() if coefficient}


def add(*polys: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return clean(result)


def neg(poly: Polynomial) -> Polynomial:
    return {monomial: -coefficient for monomial, coefficient in poly.items()}


def mul(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for (a1, a2), x in left.items():
        for (b1, b2), y in right.items():
            monomial = (a1 + b1, a2 + b2)
            result[monomial] = result.get(monomial, 0) + x * y
    return clean(result)


def e2_shift(poly: Polynomial, power: int, scale: int = 1) -> Polynomial:
    return {
        (e1_degree, e2_degree + power): scale * coefficient
        for (e1_degree, e2_degree), coefficient in poly.items()
        if scale * coefficient
    }


def lucas_table(limit: int) -> list[Polynomial]:
    values = [ZERO, ONE]
    for _ in range(1, limit):
        values.append(add(mul(E1, values[-1]), e2_shift(values[-2], 1)))
    return values


def lucas_binomial_table(values: list[Polynomial], limit: int, max_bottom: int) -> list[list[Polynomial]]:
    choose = [[ZERO for _ in range(max_bottom + 1)] for _ in range(limit + 1)]
    for n in range(limit + 1):
        choose[n][0] = ONE
        if n <= max_bottom:
            choose[n][n] = ONE
        for k in range(1, min(max_bottom, n - 1) + 1):
            choose[n][k] = add(
                mul(values[k + 1], choose[n - 1][k]),
                e2_shift(mul(values[n - k - 1], choose[n - 1][k - 1]), 1),
            )
    return choose


def q_trim(values: list[int]) -> QPolynomial:
    while values and values[-1] == 0:
        values.pop()
    return tuple(values)


def q_add(*polys: QPolynomial) -> QPolynomial:
    result = [0] * max((len(poly) for poly in polys), default=0)
    for poly in polys:
        for degree, coefficient in enumerate(poly):
            result[degree] += coefficient
    return q_trim(result)


def q_neg(poly: QPolynomial) -> QPolynomial:
    return tuple(-coefficient for coefficient in poly)


def q_shift(poly: QPolynomial, degree: int) -> QPolynomial:
    return (0,) * degree + poly if poly else ()


def q_value(poly: QPolynomial | list[int], index: int) -> int:
    return poly[index] if 0 <= index < len(poly) else 0


@lru_cache(maxsize=None)
def gaussian(n: int, r: int) -> QPolynomial:
    if r < 0 or r > n or n < 0:
        return ()
    r = min(r, n - r)
    if r == 0:
        return (1,)
    return q_add(gaussian(n - 1, r), q_shift(gaussian(n - 1, r - 1), n - r))


def gaussian_layers(k: int) -> list[int]:
    difference = q_add(gaussian(2 * k + 6, 6), q_neg(gaussian(3 * k + 4, 4)))
    return [q_value(difference, i) - q_value(difference, i - 1) for i in range(6 * k + 1)]


def schur_coefficients(poly: Polynomial, degree: int) -> list[int]:
    monomial = []
    for r in range(degree // 2 + 1):
        coefficient = 0
        for (e1_degree, e2_degree), value in poly.items():
            choice = r - e2_degree
            if 0 <= choice <= e1_degree:
                coefficient += value * math.comb(e1_degree, choice)
        monomial.append(coefficient)
    return [
        coefficient - (monomial[index - 1] if index else 0)
        for index, coefficient in enumerate(monomial)
    ]


def lucas_image(layers: list[int], degree: int, lucas: list[Polynomial], leading_sign: int) -> Polynomial:
    return add(*(
        e2_shift(
            lucas[degree - 2 * index + 1],
            index,
            leading_sign * (-1) ** index * coefficient,
        )
        for index, coefficient in enumerate(layers)
    ))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=40)
    args = parser.parse_args()
    if args.max_k < 13:
        parser.error("need --max-k >= 13")

    lucas = lucas_table(12 * args.max_k + 2)
    choose = lucas_binomial_table(lucas, 3 * args.max_k + 4, 6)
    assert choose[10][4] == choose[10][6]
    differences: dict[int, Polynomial] = {}

    for k in range(3, args.max_k + 1):
        degree = 12 * k
        direct = add(choose[3 * k + 4][4], neg(choose[2 * k + 6][6]))
        differences[k] = direct
        layers = gaussian_layers(k)
        expansion = lucas_image(layers, degree, lucas, -1)
        assert direct == expansion, ("literal Gaussian-layer expansion", k)
        coefficients = schur_coefficients(direct, degree)
        assert coefficients[:5] == [0, 0, 0, 0, 0]
        assert coefficients[5] == 1 and min(coefficients[5:]) > 0

        if k < 13:
            continue
        previous = gaussian_layers(k - 10)
        remainder_layers = [
            layers[r + 5] - q_value(previous, r - 55)
            for r in range(6 * k - 4)
        ]
        remainder = lucas_image(remainder_layers, degree - 10, lucas, 1)
        recurrence = add(e2_shift(differences[k - 10], 60), e2_shift(remainder, 5))
        assert direct == recurrence, ("literal recurrence", k)
        assert min(schur_coefficients(remainder, degree - 10)) > 0

    print("independent sparse Z[e1,e2] verification passed")
    print(f"literal expansions and recurrence checked for 3 <= k <= {args.max_k}")
    print(f"strict Lucas-Schur positivity checked for 3 <= k <= {args.max_k}")


if __name__ == "__main__":
    main()
