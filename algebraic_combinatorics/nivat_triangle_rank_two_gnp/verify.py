#!/usr/bin/env python3
"""Exact symbolic audits for periodic-mask annihilator transfer.

The universal statements are proved in THEOREM.md.  This checker constructs
small orbit norms by an exact regular-representation determinant, verifies
their period-sublattice support and factorization, and checks the resulting
operator identities entry by entry on finite tori.
"""

from __future__ import annotations

import hashlib
import json
from itertools import product


Exponent = tuple[int, int]
Poly = dict[Exponent, int]
Array = tuple[tuple[int, ...], ...]


def clean(poly: Poly) -> Poly:
    return {e: a for e, a in poly.items() if a}


def add(left: Poly, right: Poly, scale: int = 1) -> Poly:
    out = dict(left)
    for exponent, coefficient in right.items():
        out[exponent] = out.get(exponent, 0) + scale * coefficient
    return clean(out)


def multiply(left: Poly, right: Poly) -> Poly:
    out: Poly = {}
    for (a, b), x in left.items():
        for (c, d), y in right.items():
            exponent = (a + c, b + d)
            out[exponent] = out.get(exponent, 0) + x * y
    return clean(out)


def monomial_multiple(poly: Poly, exponent: Exponent, coefficient: int) -> Poly:
    a, b = exponent
    return clean({(i + a, j + b): coefficient * x
                  for (i, j), x in poly.items()})


def leading(poly: Poly) -> tuple[Exponent, int]:
    if not poly:
        raise ValueError("zero polynomial has no leading term")
    exponent = max(poly)
    return exponent, poly[exponent]


def exact_divide(dividend: Poly, divisor: Poly) -> Poly:
    """Exact lexicographic division for the monic fixtures used below."""
    if not divisor:
        raise ValueError("division by zero polynomial")
    divisor_exponent, divisor_coefficient = leading(divisor)
    if abs(divisor_coefficient) != 1:
        raise ValueError("checker division requires a unit leading coefficient")
    quotient: Poly = {}
    remainder = dict(dividend)
    while remainder:
        exponent, coefficient = leading(remainder)
        shift = (exponent[0] - divisor_exponent[0],
                 exponent[1] - divisor_exponent[1])
        if shift[0] < 0 or shift[1] < 0:
            raise AssertionError("nonzero remainder in exact division")
        factor = coefficient // divisor_coefficient
        quotient[shift] = quotient.get(shift, 0) + factor
        remainder = add(remainder, monomial_multiple(divisor, shift, factor), -1)
    return clean(quotient)


def permutation_matrix_polynomial(poly: Poly, m: int, n: int) -> list[list[Poly]]:
    """Regular representation of p(X e_(1,0),Y e_(0,1)) on Z[C_m x C_n]."""
    if m <= 0 or n <= 0:
        raise ValueError("periods must be positive")
    size = m * n
    matrix = [[{} for _ in range(size)] for _ in range(size)]
    for source_r, source_s in product(range(m), range(n)):
        source = source_r * n + source_s
        for (a, b), coefficient in poly.items():
            target_r = (source_r + a) % m
            target_s = (source_s + b) % n
            target = target_r * n + target_s
            term = {(a, b): coefficient}
            matrix[target][source] = add(matrix[target][source], term)
    return matrix


def determinant(matrix: list[list[Poly]]) -> Poly:
    """Subset dynamic program for the exact determinant over Z[X^+-1,Y^+-1]."""
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError("matrix must be square")
    states: dict[int, Poly] = {0: {(0, 0): 1}}
    for row in range(size):
        new: dict[int, Poly] = {}
        for mask, subtotal in states.items():
            for column in range(size):
                if (mask >> column) & 1 or not matrix[row][column]:
                    continue
                # Adding column to the right of earlier rows creates one
                # inversion for every earlier chosen column larger than it.
                inversions = (mask >> (column + 1)).bit_count()
                term = multiply(subtotal, matrix[row][column])
                if inversions & 1:
                    term = {e: -a for e, a in term.items()}
                next_mask = mask | (1 << column)
                new[next_mask] = add(new.get(next_mask, {}), term)
        states = new
    return states.get((1 << size) - 1, {})


def orbit_norm(poly: Poly, m: int, n: int) -> Poly:
    """Return product_(zeta^m=eta^n=1) p(zeta X,eta Y), exactly over Z."""
    result = determinant(permutation_matrix_polynomial(poly, m, n))
    if not result:
        raise AssertionError("a nonzero polynomial must have nonzero orbit norm")
    return result


def canonical(poly: Poly) -> str:
    return ";".join(f"{i},{j}:{poly[(i, j)]}" for i, j in sorted(poly))


def digest(poly: Poly) -> str:
    return hashlib.sha256(canonical(poly).encode()).hexdigest()


def apply(poly: Poly, array: Array, modulus: int | None = None) -> Array:
    height = len(array)
    width = len(array[0])
    if not height or any(len(row) != width for row in array):
        raise ValueError("array must be a nonempty rectangle")
    rows = []
    for y in range(height):
        row = []
        for x in range(width):
            value = sum(coefficient * array[(y + b) % height][(x + a) % width]
                        for (a, b), coefficient in poly.items())
            row.append(value if modulus is None else value % modulus)
        rows.append(tuple(row))
    return tuple(rows)


def pointwise(left: Array, right: Array) -> Array:
    return tuple(tuple(a * b for a, b in zip(x, y))
                 for x, y in zip(left, right))


def zero_like(array: Array) -> Array:
    return tuple(tuple(0 for _ in row) for row in array)


def norm_audit(poly: Poly, m: int, n: int) -> dict[str, int | str | bool]:
    norm = orbit_norm(poly, m, n)
    quotient = exact_divide(norm, poly)
    assert multiply(poly, quotient) == norm
    assert all(i % m == 0 and j % n == 0 for i, j in norm)
    return {
        "m": m,
        "n": n,
        "norm_terms": len(norm),
        "quotient_terms": len(quotient),
        "max_abs_coefficient": max(abs(x) for x in norm.values()),
        "support_in_period_sublattice": True,
        "norm_sha256": digest(norm),
    }


def transfer_audit() -> dict[str, int | str | bool]:
    m, n = 2, 3
    poly = {(0, 0): 1, (1, 0): -1, (0, 1): -1, (1, 1): 1}
    norm = orbit_norm(poly, m, n)
    width = height = 12
    base = tuple(tuple(((x * x + 3 * y + x * y) % 7) - 3
                       for x in range(width)) for y in range(height))
    mask_tile = ((0, 1), (1, 1), (0, 1))
    mask = tuple(tuple(mask_tile[y % n][x % m] for x in range(width))
                 for y in range(height))
    left = apply(norm, pointwise(mask, base))
    right = pointwise(mask, apply(norm, base))
    assert left == right

    # A(x)+B(y) is annihilated by (1-X)(1-Y), so both it and its
    # pointwise product with the periodic mask are killed by the norm.
    separated = tuple(tuple(((x * x + x) % 5) + ((2 * y + y * y) % 7)
                            for x in range(width)) for y in range(height))
    masked = pointwise(mask, separated)
    zero = zero_like(separated)
    assert apply(poly, separated) == zero
    assert apply(norm, separated) == zero
    assert apply(norm, masked) == zero
    return {
        "m": m,
        "n": n,
        "torus_cells": width * height,
        "commutation_entries": width * height,
        "annihilation_entries": 3 * width * height,
        "norm_sha256": digest(norm),
        "periodic_multiplier_transfer": True,
    }


def triangle_audit() -> dict[str, int | bool]:
    size = 6
    one_x = {(0, 0): 1, (1, 0): 1}
    one_y = {(0, 0): 1, (0, 1): 1}
    one_xy = {(0, 0): 1, (1, 1): 1}
    four_dot = multiply(one_x, one_y)
    triangle = multiply(four_dot, one_xy)
    sequences = list(product((0, 1), repeat=size))
    masks = list(product((0, 1), repeat=3))
    zero = tuple(tuple(0 for _ in range(size)) for _ in range(size))
    triples = 0
    entry_checks = 0
    for a, b, phase in product(sequences, sequences, masks):
        s = tuple(tuple(a[y] ^ b[x] for x in range(size)) for y in range(size))
        q = tuple(tuple(phase[(y - x) % 3] for x in range(size))
                  for y in range(size))
        c = tuple(tuple(s[y][x] ^ q[y][x] for x in range(size))
                  for y in range(size))
        assert apply(four_dot, s, 2) == zero
        assert apply(one_xy, q, 2) == zero
        assert apply(triangle, c, 2) == zero
        assert all(q[y][x] == q[y][(x + 3) % size] == q[(y + 3) % size][x]
                   for y in range(size) for x in range(size))
        triples += 1
        entry_checks += 4 * size * size
    return {
        "torus_size": size,
        "component_triples": triples,
        "entry_checks": entry_checks,
        "four_dot_plus_periodic_mask_identity": True,
    }


def main() -> None:
    generic = {(0, 0): 2, (1, 0): 1, (0, 1): -1, (1, 1): 1}
    difference = {(0, 0): 1, (1, 0): -1, (0, 1): -1, (1, 1): 1}
    result = {
        "orbit_norms": [
            norm_audit(generic, 2, 2),
            norm_audit(difference, 2, 3),
        ],
        "periodic_multiplier": transfer_audit(),
        "triangle_rank_two": triangle_audit(),
        "scope": "exact finite symbolic audits; universal claims use THEOREM.md",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
