#!/usr/bin/env python3
"""Exact geometry + nonrigorous high-precision corroboration of PROOF.md.

Run with Python 3.11 and mpmath==1.3.0. No network or external input.
The numerical integrations do not constitute a proof or an error enclosure.
"""
import argparse
from fractions import Fraction as F
from functools import lru_cache
import json
from pathlib import Path

import mpmath as mp


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def neg(a):
    return (-a[0], -a[1])


def hull(points):
    """Strict CCW convex hull; all input coordinates become exact rationals."""
    points = sorted(set(tuple(map(F, v)) for v in points))
    chains = []
    for seq in (points, points[::-1]):
        chain = []
        for v in seq:
            while len(chain) >= 2 and det(sub(chain[-1], chain[-2]),
                                          sub(v, chain[-1])) <= 0:
                chain.pop()
            chain.append(v)
        chains.append(chain[:-1])
    return chains[0] + chains[1]


def geometry(points, x):
    poly = hull(points)
    x = tuple(map(F, x))
    if len(poly) < 3 or set(poly) != {neg(v) for v in poly}:
        raise ValueError("C must be a full-dimensional origin-symmetric polygon")
    facets = []
    for a, b in zip(poly, poly[1:] + poly[:1]):
        edge = sub(b, a)
        n = (edge[1], -edge[0])  # unnormalized outward normal
        mass = dot(a, n)         # h_C(unit n) times edge length
        if mass <= 0 or abs(dot(x, n)) > mass:
            raise ValueError("invalid origin or x outside C")
        facets.append((n, mass, dot(x, n) / mass))
    area = sum(det(a, b) for a, b in zip(poly, poly[1:] + poly[:1])) / 2
    moment = sum(abs(dot(x, n)) for n, _, _ in facets) / 2
    twice_x = (2 * x[0], 2 * x[1])
    maximum = max(abs(det(v, twice_x)) for v in poly)
    assert moment == maximum and maximum <= area
    assert sum(mass for _, mass, _ in facets) / 2 == area
    v = max(poly, key=lambda v: abs(det(v, twice_x)))
    y = add(v, x)
    para = hull([(0, 0), y, twice_x, sub(twice_x, y)])
    para_area = sum(det(a, b) for a, b in zip(para, para[1:] + para[:1])) / 2
    assert para_area == maximum
    for point in para:
        assert all(dot(sub(point, x), n) <= mass for n, mass, _ in facets)
    equality = all(abs(t) in (0, 1) for _, _, t in facets)
    return poly, x, facets, area, maximum, equality


def num(r):
    r = F(r)
    return mp.mpf(r.numerator) / r.denominator


def f(t, p):
    return ((1 + t) ** p + (1 - t) ** p) ** (1 / p)


def fp(t, p):
    return ((1 + t) ** (p - 1) - (1 - t) ** (p - 1)) / f(t, p) ** (p - 1)


@lru_cache(None)
def psi(t, p):
    # Deliberately do not substitute the claimed endpoint beta integral.
    t, p = abs(num(t)), num(p)
    return f(t, p) ** 2 - t * mp.quad(lambda r: fp(r, p) ** 2, [0, t])


def constants(p):
    p = num(p)
    q = p / (p - 1)
    cq = 2 * mp.gamma(1 + 1 / q) ** 2 / mp.gamma(1 + 2 / q)
    base = 2 ** (2 / p)
    return cq, base, 2 + cq - base


def transformed_area(data, p):
    return sum(num(mass) * psi(t, p) for _, mass, t in data[2]) / 2


def direct_area(data, p):
    """Original Firey support and Green integral, split at facet normals.

    This route does not call psi, transformed_area, or the stability bound.
    At each open normal cone the supporting vertex of C is constant.
    """
    poly, x, facets = data[:3]
    p = num(p)
    angles = sorted(mp.atan2(num(n[1]), num(n[0])) % (2 * mp.pi)
                    for n, _, _ in facets)
    angles.append(angles[0] + 2 * mp.pi)
    result = mp.mpf(0)
    for left, right in zip(angles, angles[1:]):
        mid = (left + right) / 2
        v = max(poly, key=lambda v: num(v[0]) * mp.cos(mid)
                                     + num(v[1]) * mp.sin(mid))
        va, vb = add(v, x), sub(v, x)

        def integrand(theta):
            n = (mp.cos(theta), mp.sin(theta))
            tangent = (-n[1], n[0])
            a, b = [num(w[0]) * n[0] + num(w[1]) * n[1] for w in (va, vb)]
            # Only roundoff at exact zeros can be negative; reject larger errors.
            if min(a, b) < -mp.mpf("1e-40"):
                raise ArithmeticError("negative support on a normal cone")
            a, b = max(a, 0), max(b, 0)
            da, db = [num(w[0]) * tangent[0] + num(w[1]) * tangent[1]
                      for w in (va, vb)]
            support = (a ** p + b ** p) ** (1 / p)
            deriv = (a ** (p - 1) * da + b ** (p - 1) * db) / support ** (p - 1)
            return (support ** 2 - deriv ** 2) / 2

        result += mp.quad(integrand, [left, (left + right) / 2, right])
    return result


def family(t):
    return [(0, 1), (0, -1)] + [(a, b * t) for a in (-1, 1) for b in (-1, 1)]


def hexagon(a, b):
    points = [(0, 0), (1, 0), (1 + a, b), (1 + a, 1 + b),
              (a, 1 + b), (0, 1)]
    x = (F(1 + a) / 2, F(1 + b) / 2)
    return [sub(v, x) for v in points], x


def transform(matrix, v):
    return (dot(matrix[0], v), dot(matrix[1], v))


def run():
    assert mp.__version__ == "1.3.0", "Install the pinned dependency"
    mp.mp.dps = 50
    tolerance = mp.mpf("1e-28")  # comparison threshold, not certified error
    fixtures = [(f"T_{t}", family(t), (0, 1), True)
                for t in (F(0), F(1, 3), F(3, 4), F(1))]
    for a, b in [(F(1), F(1)), (F(1), F(3)), (F(1, 5), F(7, 3))]:
        points, x = hexagon(a, b)
        data = geometry(points, x)
        assert data[3] == 1 + a + b
        assert data[4] == 1 + max(a, b)
        fixtures.append((f"hex_{a}_{b}", points, x, a == b))
    octagon = [(2, 0), (2, 1), (0, 2), (-1, 2), (-2, 0),
               (-2, -1), (0, -2), (1, -2)]
    fixtures += [("octagon_boundary", octagon, (2, 0), False),
                 ("octagon_interior", octagon, (F(1, 2), F(1, 3)), False),
                 ("octagon_center", octagon, (0, 0), True),
                 ("square_off_midpoint", family(F(1)), (F(1, 3), 1), False)]
    rejected = 0
    for points, x in [(family(F(1)), (0, 2)), ([(0, 0), (1, 0), (0, 1)], (0, 0)),
                      ([(0, -1), (0, 1)], (0, 0))]:
        try:
            geometry(points, x)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("malformed fixture accepted")
    matrices = [((2, 1), (1, 3)), ((0, 2), (3, 1)), ((1, 4), (0, 1))]
    parameters = [F(5, 4), F(3, 2), F(2), F(3), F(6)]
    checks = []
    for name, points, x, expected_equality in fixtures:
        data = geometry(points, x)
        poly, x, facets, area, maximum, equality = data
        assert equality == expected_equality
        for matrix in matrices:
            changed = geometry([transform(matrix, v) for v in poly], transform(matrix, x))
            factor = abs(det(matrix[0], matrix[1]))
            assert changed[3:5] == (factor * area, factor * maximum)
            assert changed[5] == equality
            assert sorted(abs(t) for _, _, t in changed[2]) == sorted(abs(t) for _, _, t in facets)
        row = {"fixture": name, "area": str(area), "M": str(maximum),
               "equality": equality, "direct_areas": {}}
        for p in parameters:
            cq, base, constant = constants(p)
            original = direct_area(data, p)
            transformed = transformed_area(data, p)
            assert abs(original - transformed) < tolerance * (1 + abs(original))
            gap = base * num(area) + constant * num(maximum) - original
            if equality:
                assert abs(gap) < tolerance * (1 + abs(original))
            else:
                assert gap > tolerance
            row["direct_areas"][str(p)] = mp.nstr(original, 18)
        checks.append(row)

    # Endpoint beta integral, strict scalar chord, and p=2 closed formula.
    for p in parameters:
        cq, base, constant = constants(p)
        assert constant > 0
        assert abs(psi(F(1), p) - (2 + cq)) < tolerance
        for t in (F(1, 9), F(1, 2), F(9, 10)):
            assert psi(t, p) < base + constant * num(t)
    for t in (F(0), F(1, 7), F(3, 4), F(1)):
        assert abs(psi(t, F(2)) - (2 + 2 * num(t) * mp.atan(num(t)))) < tolerance

    # Nonpolygonal controls: a translated unit disk at p=2 gives an ellipse.
    disk_checks = []
    for r in (F(0), F(1, 3), F(1)):
        rho = num(r)
        value = mp.quad(lambda theta: 1 + rho * mp.sin(theta)
                        * mp.atan(rho * mp.sin(theta)),
                        [0, mp.pi / 2, mp.pi, 3 * mp.pi / 2, 2 * mp.pi])
        ellipse = 2 * mp.pi * mp.sqrt(1 + rho ** 2)
        assert abs(value - ellipse) < tolerance
        disk_checks.append({"translation": str(r), "area": mp.nstr(value, 18)})

    # Exact hexagon deficit formula, with an independent area integral.
    hex_checks = 0
    for a, b in [(F(1), F(1)), (F(1), F(3)), (F(1, 5), F(7, 3))]:
        data = geometry(*hexagon(a, b))
        r = abs(a - b) / (a + b)
        for p in parameters:
            cq, _, constant = constants(p)
            deficit = (2 + cq) * num(data[3]) - direct_area(data, p)
            expected = num(a + b) / 2 * (psi(F(1), p) - psi(r, p))
            assert abs(deficit - expected) < tolerance * (1 + abs(deficit))
            assert deficit + tolerance >= constant * num(min(a, b))
            assert deficit < (1 + cq) * num(min(a, b))
            hex_checks += 1
    return {"status": "PASS", "arithmetic": "Fraction geometry; 50-digit mpmath corroboration",
            "tolerance": "1e-28 comparison threshold, not an error enclosure",
            "polygon_cases": len(fixtures) * len(parameters),
            "exact_linear_transform_cases": len(fixtures) * len(matrices),
            "rejected_invalid_inputs": rejected, "hexagon_formula_cases": hex_checks,
            "polygons": checks, "disk_controls": disk_checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare against adjacent EXPECTED.json")
    args = parser.parse_args()
    result = run()
    if args.check:
        expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
        assert result == expected, "computed results differ from EXPECTED.json"
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
