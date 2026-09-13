#!/usr/bin/env python3
"""Clean-room exact checks for the triple-phase collar review.

This file imports no code or data from the target package.  It checks the
algebra and finite combinatorial lemmas that are most exposed to silent sign,
boundary, or colouring errors.  The continuum reduction remains a written-
proof obligation and is audited in README.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations
import json


@dataclass(frozen=True)
class S3:
    """The exact real number a+b*sqrt(3)."""

    a: F
    b: F

    def __init__(self, a: int | F = 0, b: int | F = 0) -> None:
        object.__setattr__(self, "a", F(a))
        object.__setattr__(self, "b", F(b))

    def __add__(self, other: S3) -> S3:
        return S3(self.a + other.a, self.b + other.b)

    def __sub__(self, other: S3) -> S3:
        return S3(self.a - other.a, self.b - other.b)

    def __mul__(self, other: S3) -> S3:
        return S3(self.a * other.a + 3 * self.b * other.b,
                  self.a * other.b + self.b * other.a)

    def square(self) -> S3:
        return self * self


def sign_s3(z: S3) -> int:
    """Exact sign, using only rational comparisons."""
    if z.a == 0:
        return (z.b > 0) - (z.b < 0)
    if z.b == 0 or (z.a > 0) == (z.b > 0):
        return (z.a > 0) - (z.a < 0)
    rational_comparison = z.a * z.a - 3 * z.b * z.b
    if rational_comparison == 0:
        return 0
    if rational_comparison > 0:
        return (z.a > 0) - (z.a < 0)
    return (z.b > 0) - (z.b < 0)


def dist2(p: tuple[S3, S3], q: tuple[S3, S3]) -> S3:
    dx, dy = p[0] - q[0], p[1] - q[1]
    return dx.square() + dy.square()


def poly_add(*polys: tuple[F, ...]) -> tuple[F, ...]:
    degree = max(map(len, polys))
    return tuple(sum((p[i] if i < len(p) else F(0)) for p in polys)
                 for i in range(degree))


def poly_scale(p: tuple[F, ...], scalar: F) -> tuple[F, ...]:
    return tuple(scalar * coefficient for coefficient in p)


def poly_mul(p: tuple[F, ...], q: tuple[F, ...]) -> tuple[F, ...]:
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, left in enumerate(p):
        for j, right in enumerate(q):
            out[i + j] += left * right
    return tuple(out)


def has_undirected_cycle(n: int, directed: dict[int, int]) -> bool:
    parent = list(range(n))

    def root(v: int) -> int:
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    seen_edges: set[tuple[int, int]] = set()
    for left, right in directed.items():
        if left == right:
            return True
        edge = tuple(sorted((left, right)))
        if edge in seen_edges:
            # The only possible duplicate is a directed two-cycle.  It is a
            # periodic orbit and must not occur for an increasing map.
            return True
        seen_edges.add(edge)
        rleft, rright = root(left), root(right)
        if rleft == rright:
            return True
        parent[rleft] = rright
    return False


def audit_order_lemma(max_n: int = 7) -> tuple[list[dict[str, int]], int]:
    """Enumerate every increasing partial injection on [n]."""
    rows: list[dict[str, int]] = []
    total_loop_free = 0
    for n in range(1, max_n + 1):
        maps = 0
        loop_free = 0
        for size in range(n + 1):
            for domain in combinations(range(n), size):
                for image in combinations(range(n), size):
                    maps += 1
                    mapping = dict(zip(domain, image))
                    if any(left == right for left, right in mapping.items()):
                        continue
                    loop_free += 1
                    assert not has_undirected_cycle(n, mapping)
        # Vandermonde's identity supplies an independent count oracle.
        from math import comb
        assert maps == comb(2 * n, n)
        rows.append({"n": n, "maps": maps, "loop_free_maps": loop_free})
        total_loop_free += loop_free
    return rows, total_loop_free


def audit_orbit_extension() -> int:
    """Check every allowed active precolouring of the six-cycle."""
    alternating = [tuple((phase + i) % 2 for i in range(6))
                   for phase in (0, 1)]
    cases: list[dict[int, int]] = [{}]
    for vertex in range(6):
        for colour in (0, 1):
            cases.append({vertex: colour})
    for vertex in range(6):
        neighbour = (vertex + 1) % 6
        for colour in (0, 1):
            cases.append({vertex: colour, neighbour: 1 - colour})
    assert len(cases) == 25
    for precolouring in cases:
        extensions = [colouring for colouring in alternating
                      if all(colouring[v] == c
                             for v, c in precolouring.items())]
        assert len(extensions) == (2 if not precolouring else 1)
    return len(cases)


def main() -> None:
    one = S3(1)
    zero = S3()
    sqrt3 = S3(0, 1)
    d0 = one + sqrt3

    # The exact threshold is inside the claimed strict fixture interval.
    assert sign_s3(d0 - S3(2)) > 0
    assert sign_s3(S3(F(11, 4)) - d0) > 0
    assert sign_s3(S3(3) - S3(F(11, 4))) > 0
    assert d0.square() == S3(4, 2)
    assert sign_s3(d0.square() - S3(7)) > 0

    # Sharp boundary triangle and membership in the two owner circles.
    first = (zero, zero)
    second = (d0, zero)
    u_minus = (S3(0, F(1, 2)), S3(F(-1, 2)))
    u_plus = (S3(0, F(1, 2)), S3(F(1, 2)))
    v = (sqrt3, zero)
    assert dist2(first, u_minus) == one
    assert dist2(first, u_plus) == one
    assert dist2(second, v) == one
    assert dist2(u_minus, u_plus) == one
    assert dist2(u_minus, v) == one
    assert dist2(u_plus, v) == one

    # The open equilateral fixture has side 11/4 exactly.
    a0 = (zero, zero)
    a1 = (S3(F(11, 4)), zero)
    b = (S3(F(11, 8)), S3(0, F(11, 8)))
    side2 = S3(F(121, 16))
    assert dist2(a0, a1) == side2
    assert dist2(a0, b) == side2
    assert dist2(a1, b) == side2

    # Independent cross-triple at d=11/4:
    # (7/8 +/- i*sqrt(15)/8) + 1 = 11/4, with each term unit
    # and conjugate product one.  All checks reduce to Q.
    cross_unit_norm2 = F(7, 8) ** 2 + F(15, 64)
    cross_real_sum = 2 * F(7, 8) + 1
    cross_product = F(7, 8) ** 2 + F(15, 64)
    assert (cross_unit_norm2, cross_real_sum, cross_product) == (1, F(11, 4), 1)

    # Re-derive the threshold identities over Q[x].  Common denominator for
    # A^2+B^2-AB-3/4 is 16*x.
    x_minus_3 = (F(-3), F(1))
    x_plus_3 = (F(3), F(1))
    x2_minus_9 = (F(-9), F(0), F(1))
    numerator = poly_add(
        poly_scale(poly_mul(x_minus_3, x_minus_3), F(4)),
        poly_mul(x_plus_3, x_plus_3),
        poly_scale(x2_minus_9, F(-2)),
        (F(0), F(-12)),
    )
    expected_gap = poly_scale(poly_mul(x_minus_3, (F(-7), F(1))), F(3))
    assert numerator == expected_gap == (F(63), F(-30), F(3))
    # AB-1/2=(x^2-4x-9)/(8x), positive for x>7: its value at
    # 7 is 12 and its derivative 2x-4 is then positive.
    ab_gap = (F(-9), F(-4), F(1))
    assert sum(coefficient * F(7) ** degree
               for degree, coefficient in enumerate(ab_gap)) == 12
    assert 2 * 7 - 4 > 0

    # Direct quotient-rule derivation of sigma': if
    # D=d^2+1-2*d*c, then 1+2*(1-d*c)/D has numerator
    # d^2+3-4*d*c.  Compare coefficients in (1,d*c,d^2).
    derivative_numerator = tuple(
        left + twice_arg
        for left, twice_arg in zip((F(1), F(-2), F(1)),
                                    (F(2), F(-2), F(0)))
    )
    assert derivative_numerator == (F(3), F(-4), F(1))

    order_rows, loop_free_total = audit_order_lemma()
    orbit_cases = audit_orbit_extension()

    # Palette constraints used by the three-centre lift.
    paired_rim = {0, 1}
    third_rim = {2, 3}
    paired_centre_colour = 2
    third_centre_colour = 0
    assert paired_rim.isdisjoint(third_rim)
    assert paired_centre_colour not in paired_rim
    assert third_centre_colour not in third_rim

    result = {
        "cross_triple_exact_checks": 3,
        "finite_order_lemma": order_rows,
        "fixture_squared_distances": 3,
        "loop_free_partial_maps_checked": loop_free_total,
        "orbit_precolourings_checked": orbit_cases,
        "palette_set_checks": 3,
        "sharp_boundary_checks": 6,
        "status": "PASS",
        "symbolic_identity_checks": 4,
        "threshold_order_checks": 5,
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
