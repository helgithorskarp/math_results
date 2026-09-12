#!/usr/bin/env python3
"""Exact finite component and controls for proof.md; Python 3.11+ stdlib.

Coefficient lists are in ascending degree. No floating-point computation.
The infinite tail and the external vanishing-sum theorem are written premises,
not claims to have been exhaustively checked by this program.
"""
import argparse
from fractions import Fraction
import json
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
PHI = {5: [1, 1, 1, 1, 1], 6: [1, -1, 1], 12: [1, 0, -1, 0, 1]}
KNOWN = {(1, 2): [5], (1, 3): [5, 6], (3, 4): [5, 12]}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p or [0]


def add(p, q):
    r = [0] * max(len(p), len(q))
    for i, a in enumerate(p):
        r[i] += a
    for i, a in enumerate(q):
        r[i] += a
    return trim(r)


def mul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return trim(r)


def divide(p, q):
    r = trim([Fraction(a) for a in p])
    q = trim([Fraction(a) for a in q])
    require(q != [0], "polynomial division by zero")
    quotient = [Fraction(0)] * max(1, len(r) - len(q) + 1)
    while r != [0] and len(r) >= len(q):
        shift = len(r) - len(q)
        c = r[-1] / q[-1]
        quotient[shift] = c
        for i, a in enumerate(q):
            r[shift + i] -= c * a
        r = trim(r)
    return trim(quotient), r


def evaluate(p, x):
    value = 0
    for a in reversed(p):
        value = x * value + a
    return value


def sturm_count(p, left, right):
    """Number of distinct real roots in (left,right); neither endpoint a root."""
    require(evaluate(p, left) != 0 and evaluate(p, right) != 0,
            "Sturm endpoint is a root")
    seq = [trim(p), trim([i * p[i] for i in range(1, len(p))])]
    while seq[-1] != [0]:
        _, rem = divide(seq[-2], seq[-1])
        if rem == [0]:
            break
        seq.append([-a for a in rem])

    def variations(x):
        values = [evaluate(q, x) for q in seq]
        signs = [(a > 0) - (a < 0) for a in values if a != 0]
        return sum(a != b for a, b in zip(signs, signs[1:]))

    return variations(left) - variations(right)


def reciprocal_polynomial(u, v):
    p = [0] * (2 * v + 1)
    for exponent in (0, v - u, v, v + u, 2 * v):
        p[exponent] += 1
    return p


def cosine_polynomial(u, v):
    d = [[2], [0, 1]]
    for j in range(1, v):
        d.append(add([0] + d[j], [-a for a in d[j - 1]]))
    return add([1], add(d[u], d[v]))


def finite_box():
    rows = []
    for v in range(2, 10):
        for u in range(1, v):
            if gcd(u, v) != 1:
                continue
            p = reciprocal_polynomial(u, v)
            orders = [d for d, phi in PHI.items() if divide(p, phi)[1] == [0]]
            torsion_count = sum(len(PHI[d]) - 1 for d in orders)
            k = sum(v < 3 * ((u * (2 * j + 1)) % (2 * v)) < 5 * v
                    for j in range(v))
            circle_count = 2 * sturm_count(cosine_polynomial(u, v), -2, 2)
            require(circle_count >= 2 * k, "midpoint count contradicts Sturm")
            if (u, v) in KNOWN:
                product = [1]
                for d in KNOWN[u, v]:
                    product = mul(product, PHI[d])
                require(product == p, "known cyclotomic factorization failed")
                require(circle_count == torsion_count, "known circle count failed")
            else:
                require(2 * k > torsion_count, "midpoint exclusion failed")
                require(circle_count > torsion_count, "Sturm exclusion failed")
            rows.append({"u": u, "v": v, "midpoint_root_lower_bound": 2 * k,
                         "torsion_orders": orders, "distinct_torsion_roots": torsion_count,
                         "sturm_unit_circle_roots": circle_count,
                         "cyclotomic_product": (u, v) in KNOWN})
    require(len(rows) == 27, "finite box is incomplete")
    require(sum(r["cyclotomic_product"] for r in rows) == 3, "exception count")
    return rows


def bareiss(matrix):
    a = [list(row) for row in matrix]
    n, sign, previous = len(a), 1, 1
    require(all(len(row) == n for row in a), "nonsquare matrix")
    for k in range(n - 1):
        if a[k][k] == 0:
            j = next((j for j in range(k + 1, n) if a[j][k]), None)
            if j is None:
                return 0
            a[k], a[j] = a[j], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = pivot * a[i][j] - a[i][k] * a[k][j]
                quotient, remainder = divmod(numerator, previous)
                require(remainder == 0, "Bareiss division is not exact")
                a[i][j] = quotient
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def verify_bezout(cert):
    require((cert["N"], cert["u"], cert["v"]) == (41, 1, 9), "wrong certificate")
    p, u, v = (cert[k] for k in ("P", "U", "V"))
    require(all(type(a) is int for q in (p, u, v) for a in q),
            "noninteger certificate coefficient")
    require(p == reciprocal_polynomial(1, 9), "wrong certificate polynomial")
    require(add(mul(p, u), mul([1] * 41, v)) == [1], "Bezout identity failed")


def core(n, u, v):
    return {0, u % n, (-u) % n, v % n, (-v) % n}


def unit_orbit(n, values):
    return {tuple(sorted((t * x) % n for x in values))
            for t in range(1, n) if gcd(t, n) == 1}


def check_controls():
    cert = json.loads((HERE / "norm_counterexample.json").read_text())
    verify_bezout(cert)
    n, k = 41, core(41, 1, 9)
    det = bareiss([[int((j - i) % n in k) for j in range(n)] for i in range(n)])
    require(det == 5, "circulant determinant is not five")
    orbit = unit_orbit(n, k)
    known_orbits = [unit_orbit(n, core(n, u, v)) for u, v in KNOWN]
    require(all(orbit.isdisjoint(o) for o in known_orbits), "known orbit collision")
    require((n - 5) & (n - 6) != 0, "control is on selected modulus sequence")

    a = [1, 7, 11, 22, 24]
    sums = [0]
    for x in a:
        sums += [(y + x) % 37 for y in sums]
    require(len(sums) == len(set(sums)) == 32, "N=37 control not sum-distinct")
    holes = set(range(37)) - set(sums)
    total_half = (sum(a) * pow(2, -1, 37)) % 37
    centered = {(h - total_half) % 37 for h in holes}
    require(centered == core(37, 1, 12), "wrong centered holes")
    b1 = [1, 2, 4, 8, 17]
    require(sorted(24 * x % 37 for x in b1) == a, "B1 dilation control failed")
    require(unit_orbit(37, centered) == unit_orbit(37, core(37, 1, 3)),
            "no standard lift for known control")
    return {
        "N37": {"A": a, "distinct_subset_sums": len(set(sums)),
                "centered_holes": sorted(centered), "B1_multiplier": 24,
                "fixed_lift": [1, 12], "unit_equivalent_to_core": [1, 3]},
        "N41": {"core": sorted(k), "bareiss_determinant": det,
                "bezout_identity_verified": True,
                "max_abs_bezout_coefficient": max(abs(x) for key in ("U", "V") for x in cert[key]),
                "orbit_size": len(orbit), "known_orbit_sizes": [len(o) for o in known_orbits],
                "orbit_disjoint_from_all_known": True,
                "selected_modulus_sequence_member": False}}


def build():
    return {"schema": "cyclotomic-lifts-exact-controls-v1",
            "finite_box": finite_box(), "controls": check_controls()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="emit regenerated exact JSON")
    args = parser.parse_args()
    result = build()
    if args.emit:
        print(json.dumps(result, indent=2) + "\n", end="")
    else:
        expected = json.loads((HERE / "expected.json").read_text())
        require(result == expected, "regenerated result differs from expected.json")
        print("PASS: 27 primitive pairs; 24 non-torsion exclusions; 3 factorizations;")
        print("      independent Sturm counts; N37 subset-sum control;")
        print("      N41 Bezout identity, determinant 5, and complete unit-orbit separation.")
        print("Scope: polynomial theorem and method controls; modular residual unchanged.")


if __name__ == "__main__":
    main()
