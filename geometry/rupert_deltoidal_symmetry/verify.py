#!/usr/bin/env python3
"""Exact invariants for symmetry-axis shadows of the deltoidal hexecontahedron.

Python 3.11+, standard library only. No floating-point decisions or solvers.
The analytic angular-covering argument is in proof.md.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import isqrt
import json


@dataclass(frozen=True)
class Q5:
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, "a", F(self.a))
        object.__setattr__(self, "b", F(self.b))

    @staticmethod
    def coerce(x):
        return x if isinstance(x, Q5) else Q5(x)

    def __add__(self, x):
        x = self.coerce(x)
        return Q5(self.a + x.a, self.b + x.b)

    __radd__ = __add__

    def __neg__(self):
        return Q5(-self.a, -self.b)

    def __sub__(self, x):
        return self + (-self.coerce(x))

    def __rsub__(self, x):
        return self.coerce(x) - self

    def __mul__(self, x):
        x = self.coerce(x)
        return Q5(self.a * x.a + 5 * self.b * x.b,
                  self.a * x.b + self.b * x.a)

    __rmul__ = __mul__

    def __truediv__(self, x):
        x = self.coerce(x)
        den = x.a * x.a - 5 * x.b * x.b
        if den == 0:
            raise ZeroDivisionError("zero field element")
        return self * Q5(x.a / den, -x.b / den)

    def __rtruediv__(self, x):
        return self.coerce(x) / self

    def __pow__(self, n):
        if n < 0:
            return (1 / self) ** (-n)
        result, base = Q5(1), self
        while n:
            if n & 1:
                result *= base
            base *= base
            n //= 2
        return result

    def sign(self):
        a, b = self.a, self.b
        if b == 0:
            return (a > 0) - (a < 0)
        if a == 0:
            return (b > 0) - (b < 0)
        if a > 0 and b > 0:
            return 1
        if a < 0 and b < 0:
            return -1
        d = a * a - 5 * b * b
        if d == 0:
            raise ArithmeticError("irrational square root represented as rational")
        return ((d > 0) - (d < 0)) * ((a > 0) - (a < 0))

    def __lt__(self, x):
        return (self - x).sign() < 0

    def __le__(self, x):
        return (self - x).sign() <= 0

    def __str__(self):
        return f"({self.a}) + ({self.b})*sqrt(5)"


S = Q5(0, 1)
PHI = (1 + S) / 2
ZERO = Q5(0)


def vec(x):
    return tuple(Q5.coerce(y) for y in x)


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def mul(c, x):
    return tuple(c * a for a in x)


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), ZERO)


def cross(x, y):
    return (x[1] * y[2] - x[2] * y[1],
            x[2] * y[0] - x[0] * y[2],
            x[0] * y[1] - x[1] * y[0])


def project(v, u):
    return sub(v, mul(dot(v, u) / dot(u, u), u))


def cyclic_signed(x):
    result = set()
    for k in range(3):
        t = x[k:] + x[:k]
        for signs in product((-1, 1), repeat=3):
            result.add(tuple(s * a for s, a in zip(signs, t)))
    return result


def vertices():
    # McCooey's exact coordinates, generated from five cyclic signed families.
    c0 = (5 - S) / 4
    c1 = (15 + S) / 22
    c2 = S / 2
    c3 = (5 + S) / 6
    c4 = (5 + 4 * S) / 11
    c5 = (5 + S) / 4
    c6 = (5 + 3 * S) / 6
    c7 = (25 + 9 * S) / 22
    families = [vec((S, 0, 0)), vec((0, c1, c7)), vec((c3, 0, c6)),
                vec((c0, c2, c5)), vec((c4, c4, c4))]
    points = set().union(*(cyclic_signed(t) for t in families))
    if len(points) != 62:
        raise AssertionError("incorrect solid")
    return sorted(points)


def convex_hull_2d(points):
    points = sorted(set(points))
    if len(points) < 3:
        raise ValueError("degenerate input")

    def turn(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    def half(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and turn(out[-2], out[-1], p).sign() <= 0:
                out.pop()
            out.append(p)
        return out

    return half(points)[:-1] + half(reversed(points))[:-1]


def shadow(V, u):
    # These coordinates preserve orientation, without introducing square roots
    # from normalization. Euclidean metrics are computed in 3D below.
    e1 = vec((0, 1, 0)) if u[1] == ZERO else vec((1, -1, 0))
    e2 = cross(u, e1)
    assert dot(e1, u) == ZERO and dot(e2, u) == ZERO
    assert dot(cross(e1, e2), u).sign() > 0
    mapping = {}
    for v in V:
        key = (dot(v, e1), dot(v, e2))
        mapping.setdefault(key, []).append(v)
    H = [mapping[p][0] for p in convex_hull_2d(mapping)]
    P = [project(v, u) for v in H]
    constraints = []
    area_num = ZERO
    for i, v in enumerate(H):
        w = H[(i + 1) % len(H)]
        n = cross(sub(w, v), u)
        b = dot(n, v)
        assert b.sign() > 0 and dot(n, n).sign() > 0
        assert all((b - dot(n, x)).sign() >= 0 for x in V)
        constraints.append((n, b))
        area_num += dot(u, cross(v, w)) / 2
    assert area_num.sign() > 0
    radii_sq = [dot(p, p) for p in P]
    all_radii_sq = [dot(project(v, u), project(v, u)) for v in V]
    inradius_sq = min(b * b / dot(n, n) for n, b in constraints)
    return {
        "u": u, "hull": P, "constraints": constraints,
        "vertices": len(H), "radii_sq": radii_sq,
        "radius_sq": max(all_radii_sq), "inradius_sq": inradius_sq,
        "area_num": area_num, "area_sq": area_num ** 2 / dot(u, u),
    }


def sqrt_fraction_bounds(q, digits=18):
    if q < 0:
        raise ValueError("negative radicand")
    scale = 10 ** digits
    k = isqrt((q.numerator * scale * scale) // q.denominator)
    lo, hi = F(k, scale), F(k + 1, scale)
    assert lo * lo <= q < hi * hi
    return lo, hi


def field_bounds(q):
    lo, hi = sqrt_fraction_bounds(F(5))
    if q.b >= 0:
        return q.a + q.b * lo, q.a + q.b * hi
    return q.a + q.b * hi, q.a + q.b * lo


def field_sqrt_bounds(q):
    lo, hi = field_bounds(q)
    assert lo >= 0
    return sqrt_fraction_bounds(lo)[0], sqrt_fraction_bounds(hi)[1]


def decimal_bounds(lo, hi, digits=12):
    scale = 10 ** digits
    a = (lo.numerator * scale) // lo.denominator
    b = -((-hi.numerator * scale) // hi.denominator)
    return [f"{a // scale}.{a % scale:0{digits}d}",
            f"{b // scale}.{b % scale:0{digits}d}"]


def self_check():
    assert (S - 2).sign() > 0 and (S - 3).sign() < 0
    assert (2 - S).sign() < 0 and (3 - S).sign() > 0
    assert 1 / (S - 2) == S + 2
    assert (S * S) == Q5(5)
    cube = [vec(p) for p in product((-1, 1), repeat=3)]
    c = shadow(cube, vec((0, 0, 1)))
    assert c["vertices"] == 4 and c["area_sq"] == Q5(16)
    assert c["radius_sq"] == Q5(2) and c["inradius_sq"] == Q5(1)


def verify():
    self_check()
    V = vertices()
    assert all(mul(-1, v) in V for v in V)
    R2 = (25 + 10 * S) / 9
    assert max(dot(v, v) for v in V) == R2
    assert sum(dot(v, v) == R2 for v in V) == 12
    assert R2 < Q5(F(53, 10))
    # Explicit order-3 and order-5 symmetries. Order 2 follows from sign changes.
    u5 = vec((1, 0, PHI))
    c72 = (S - 1) / 4

    def rot5(v):
        return add(add(mul(c72, v),
                       mul((1 - c72) * dot(u5, v) / dot(u5, u5), u5)),
                   mul(F(1, 2), cross(u5, v)))

    assert all((v[1], v[2], v[0]) in V for v in V)
    assert all(rot5(v) in V for v in V)
    assert all(dot(v, u5) == dot(rot5(v), u5) for v in V)
    for v in V:
        w = v
        for _ in range(5):
            w = rot5(w)
        assert w == v

    H2 = shadow(V, vec((0, 0, 1)))
    H3 = shadow(V, vec((1, 1, 1)))
    H5 = shadow(V, u5)
    assert [h["vertices"] for h in (H2, H3, H5)] == [12, 12, 20]
    r3_sq = (70 + 30 * S) / 27
    assert H2["radius_sq"] == R2
    assert H3["radius_sq"] == r3_sq
    assert H5["radius_sq"] == Q5(5)

    # The threefold shadow is an alternating-radius, equiangular dodecagon.
    assert set(H3["radii_sq"]) == {Q5(5), r3_sq}
    for i, p in enumerate(H3["hull"]):
        q = H3["hull"][(i + 1) % 12]
        assert dot(p, p) != dot(q, q)
        assert dot(p, q).sign() > 0
        assert 4 * dot(p, q) ** 2 == 3 * dot(p, p) * dot(q, q)
    d = PHI ** (-4)
    b3_sq = 5 / (1 + 3 * d * d)
    assert all(b * b / dot(n, n) == b3_sq for n, b in H3["constraints"])

    # The fivefold shadow contains a regular decagon of radius sqrt(5).
    # Its ten remaining vertices have smaller radius, alternating every 18 deg.
    rho_sq = next(r for r in H5["radii_sq"] if r != Q5(5))
    assert set(H5["radii_sq"]) == {Q5(5), rho_sq}
    assert rho_sq < Q5(5 * F(99, 100) ** 2)
    for i, p in enumerate(H5["hull"]):
        q = H5["hull"][(i + 1) % 20]
        assert dot(p, p) != dot(q, q)
        assert dot(p, q).sign() > 0
        assert dot(p, q) ** 2 == (5 + S) / 8 * dot(p, p) * dot(q, q)
    decagon = [p for p in H5["hull"] if dot(p, p) == Q5(5)]
    assert len(decagon) == 10
    for i, p in enumerate(decagon):
        assert dot(p, decagon[(i + 1) % 10]) == 5 * (1 + S) / 4

    # All six off-diagonal cases. The remaining cases are congruent polygons.
    assert R2 > r3_sq > Q5(5)
    assert H3["area_sq"] > H2["area_sq"]
    assert H5["inradius_sq"] > H2["inradius_sq"]
    # delta = arctan(sqrt(3)/phi^4) lies between 12 and 15 degrees.
    assert 3 * d * d > Q5(F(1, 16))  # tan(delta) > 1/4 > tan(12 deg)
    assert 3 * (1 + d) ** 2 < Q5(4)  # tan(delta) < 2 - sqrt(3)
    # kappa^{-1} = cos(18 deg) + sqrt(3)*(5*sqrt(5)-11)/4.
    # Each lower bound is strict, so kappa < 40/41 < 1.
    cos18_sq = (5 + S) / 8
    other_sq = 3 * ((5 * S - 11) / 4) ** 2
    assert (5 * S - 11).sign() > 0
    assert d * (S - 1) == 5 * S - 11
    assert cos18_sq > Q5(F(19, 20) ** 2)
    assert other_sq > Q5(F(3, 40) ** 2)

    # Rationally verified margins for perturbing both axes by <= 1/1000 rad.
    # Circumradius differences exceed .039 and .016; 2 R eps < .0046.
    assert R2 > Q5(F(2293, 1000) ** 2)
    assert r3_sq < Q5(F(2254, 1000) ** 2)
    assert r3_sq > Q5(F(2253, 1000) ** 2)
    assert Q5(5) < Q5(F(2237, 1000) ** 2)
    assert R2 < Q5(F(23, 10) ** 2)
    assert H5["inradius_sq"] > Q5(F(2154, 1000) ** 2)
    assert H2["inradius_sq"] < Q5(F(2122, 1000) ** 2)
    assert H3["area_sq"] > Q5(F(1511, 100) ** 2)
    assert H2["area_sq"] < Q5(F(1502, 100) ** 2)
    eps = F(1, 1000)
    area_error = (4 * F(22, 7) * eps + 2 * F(22, 7) * eps * eps) * F(53, 10)
    assert area_error < F(9, 100)
    assert b3_sq < Q5(F(2168, 1000) ** 2)
    assert Q5(5) > Q5(F(2236, 1000) ** 2)
    assert F(99, 100) * F(2236, 1000) - F(2168, 1000) > 2 * F(23, 10) * eps

    a_lo, a_hi = field_sqrt_bounds(cos18_sq)
    b_lo, b_hi = field_sqrt_bounds(other_sq)
    kappa_lo, kappa_hi = 1 / (a_hi + b_hi), 1 / (a_lo + b_lo)
    assert F(971679451840, 10 ** 12) < kappa_lo
    assert kappa_hi < F(971679451841, 10 ** 12)
    summary = {
        "agent": "six-rupert-1", "role": "researcher", "arithmetic": "Q(sqrt(5)), exact",
        "solid_vertices": len(V), "circumradius_squared": str(R2),
        "shadows": {},
        "five_to_three_optimal_closed_scale": "4/(sqrt(10+2*sqrt(5))+sqrt(3)*(5*sqrt(5)-11))",
        "five_to_three_scale_enclosure": decimal_bounds(kappa_lo, kappa_hi),
        "cross_order_axis_neighborhood_radius_radians": "1/1000",
        "excluded_exact_axis_order_pairs": [[a, b] for a in [2, 3, 5] for b in [2, 3, 5]],
        "excluded_neighborhood_order_pairs": [[a, b] for a in [2, 3, 5] for b in [2, 3, 5] if a != b],
        "scope": "restricted passage exclusions; no global non-Rupert conclusion",
    }
    for order, h in [(2, H2), (3, H3), (5, H5)]:
        summary["shadows"][str(order)] = {
            "vertices": h["vertices"], "radius_squared": str(h["radius_sq"]),
            "inradius_squared": str(h["inradius_sq"]), "area_squared": str(h["area_sq"]),
        }
    return summary


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("verification requires assertions; do not use python -O")
    print(json.dumps(verify(), indent=2, sort_keys=True))
