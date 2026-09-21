#!/usr/bin/env python3
"""Exact finite audits for the Farey-triangle directional-rank formulas."""

from __future__ import annotations

import json
from collections import Counter
from itertools import product


Point = tuple[int, int]
Poly = frozenset[Point]  # coefficients in F_2


def config(a: tuple[int, ...], b: tuple[int, ...], d: tuple[int, ...]) -> tuple[int, ...]:
    n = len(a)
    return tuple(a[j] ^ b[i] ^ d[(j - i) % n]
                 for j in range(n) for i in range(n))


def derivative(u: tuple[int, ...], t: int) -> tuple[int, ...]:
    n = len(u)
    return tuple(u[(k + t) % n] ^ u[k] for k in range(n))


def is_affine(u: tuple[int, ...], epsilon: int) -> tuple[bool, int]:
    constant = u[0]
    return (all(x == ((epsilon * k) & 1) ^ constant for k, x in enumerate(u)),
            constant)


def derivative_criterion(a: tuple[int, ...], b: tuple[int, ...], d: tuple[int, ...],
                         p: int, q: int) -> bool:
    # A homomorphism Z/n -> F_2 has slope 1 only when n is even.
    epsilons = (0, 1) if len(a) % 2 == 0 else (0,)
    for epsilon in epsilons:
        aa, ca = is_affine(derivative(a, q), epsilon)
        bb, cb = is_affine(derivative(b, p), epsilon)
        dd, cd = is_affine(derivative(d, q - p), epsilon)
        if aa and bb and dd and (ca ^ cb ^ cd) == 0:
            return True
    return False


def direct_period(c: tuple[int, ...], n: int, p: int, q: int) -> bool:
    return all(c[j * n + i] == c[((j + q) % n) * n + (i + p) % n]
               for j in range(n) for i in range(n))


def xor_poly(a: set[Point], b: set[Point]) -> set[Point]:
    return a.symmetric_difference(b)


def mul_poly(a: Poly, b: Poly) -> Poly:
    out: set[Point] = set()
    for (i, j), (k, ell) in product(a, b):
        out = xor_poly(out, {(i + k, j + ell)})
    return frozenset(out)


def factor(dx: int, dy: int, power: int = 1) -> Poly:
    return frozenset({(0, 0), (power * dx, power * dy)})


def apply_poly(poly: Poly, c: tuple[int, ...], n: int) -> tuple[int, ...]:
    return tuple(sum(c[((j + dy) % n) * n + (i + dx) % n]
                     for dx, dy in poly) & 1
                 for j in range(n) for i in range(n))


def avoids_x_plus_one(poly: Poly) -> bool:
    exponents = Counter(dy for _, dy in poly)
    return any(v & 1 for v in exponents.values())


def avoids_y_plus_one(poly: Poly) -> bool:
    exponents = Counter(dx for dx, _ in poly)
    return any(v & 1 for v in exponents.values())


def avoids_xy_plus_one(poly: Poly) -> bool:
    exponents = Counter(dy - dx for dx, dy in poly)
    return any(v & 1 for v in exponents.values())


def gauge_audit(n: int) -> dict[str, int]:
    sequences = list(product((0, 1), repeat=n))
    zero = (0,) * (n * n)
    kernel = 0
    fibers: Counter[tuple[int, ...]] = Counter()
    for a, b, d in product(sequences, repeat=3):
        c = config(a, b, d)
        fibers[c] += 1
        kernel += c == zero
    predicted = 8 if n % 2 == 0 else 4
    assert kernel == predicted
    assert set(fibers.values()) == {predicted}
    return {"n": n, "gauge_kernel": kernel, "image_size": len(fibers),
            "common_fiber_size": predicted}


def period_audit(n: int) -> dict[str, int]:
    sequences = list(product((0, 1), repeat=n))
    triples = 0
    tests = 0
    for a, b, d in product(sequences, repeat=3):
        c = config(a, b, d)
        triples += 1
        for p, q in product(range(n), repeat=2):
            tests += 1
            assert direct_period(c, n, p, q) == derivative_criterion(a, b, d, p, q)
    return {"n": n, "triples": triples, "translation_tests": tests}


def factor_avoidance_audit() -> dict[str, int | bool]:
    n = 4
    sequences = list(product((0, 1), repeat=n))
    period_two = [u for u in sequences if derivative(u, 2) == (0,) * n]
    one_x, one_y, one_xy = factor(1, 0), factor(0, 1), factor(1, 1)
    p_a = mul_poly(mul_poly(factor(0, 1, 2), one_y), one_xy)
    p_b = mul_poly(mul_poly(factor(1, 0, 2), one_x), one_xy)
    p_c = mul_poly(mul_poly(factor(1, 0, 2), one_x), one_y)
    checked = 0
    zero = (0,) * (n * n)
    for periodic, u, v in product(period_two, sequences, sequences):
        assert apply_poly(p_a, config(periodic, u, v), n) == zero
        assert apply_poly(p_b, config(u, periodic, v), n) == zero
        assert apply_poly(p_c, config(u, v, periodic), n) == zero
        checked += 3
    assert avoids_x_plus_one(p_a)
    assert avoids_y_plus_one(p_b)
    assert avoids_xy_plus_one(p_c)
    return {"torus_size": n, "annihilation_checks": checked,
            "p_A_avoids_1_plus_X": True, "p_B_avoids_1_plus_Y": True,
            "p_C_avoids_1_plus_XY": True}


def main() -> None:
    result = {
        "gauge_audits": [gauge_audit(3), gauge_audit(4)],
        "period_audits": [period_audit(3), period_audit(4)],
        "factor_avoidance": factor_avoidance_audit(),
        "scope": "finite cyclic audits only; universal claims use THEOREM.md",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
