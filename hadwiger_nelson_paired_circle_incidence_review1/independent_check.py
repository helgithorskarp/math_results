#!/usr/bin/env python3
"""Independent exact audit of the paired-circle incidence reduction.

This checker deliberately imports no target module.  In contrast to the
target's sparse producer and evaluation/interpolation verifier, it uses dense
7-by-7 coefficient arrays over Q(sqrt(3)).  It derives every incidence factor
twice: once from the displayed F formula and once from the undivided Cramer
determinant equation.  It then compares the complete coefficient arrays with
the published certificate.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TARGET = ROOT.parent / "hadwiger_nelson_paired_circle_incidence" / "certificate.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "ee51e8cf1517bd2885d3c74d7b5ccaa74418593e5e9910bf948bcab56021febb"
)
MAX_DEGREE = 6
SLOTS = ((0, 0), (0, 1), (1, 0), (1, 1))


# Elements of Q(sqrt(3)) are pairs (a,b), representing a+b sqrt(3).
def k(a=0, b=0):
    return (Q(a), Q(b))


K0 = k()
K1 = k(1)


def kadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def kneg(a):
    return (-a[0], -a[1])


def kmul(a, b):
    return (a[0] * b[0] + 3 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def pzero():
    return [[K0 for _ in range(MAX_DEGREE + 1)] for _ in range(MAX_DEGREE + 1)]


def pconst(a=0, b=0):
    out = pzero()
    out[0][0] = k(a, b)
    return out


def pvar(axis):
    out = pzero()
    out[1 if axis == "x" else 0][1 if axis == "y" else 0] = K1
    return out


PX = pvar("x")
PY = pvar("y")


def padd(*args):
    out = pzero()
    for p in args:
        for i in range(MAX_DEGREE + 1):
            for j in range(MAX_DEGREE + 1):
                out[i][j] = kadd(out[i][j], p[i][j])
    return out


def pneg(p):
    return [[kneg(c) for c in row] for row in p]


def psub(a, b):
    return padd(a, pneg(b))


def pscale(p, scalar):
    scalar = scalar if isinstance(scalar, tuple) else k(scalar)
    return [[kmul(c, scalar) for c in row] for row in p]


def pmul(a, b):
    out = pzero()
    for i, j, h, ell in product(range(MAX_DEGREE + 1), repeat=4):
        u = a[i][j]
        v = b[h][ell]
        if u == K0 or v == K0:
            continue
        if i + h > MAX_DEGREE or j + ell > MAX_DEGREE:
            raise AssertionError("unexpected polynomial degree above six")
        out[i + h][j + ell] = kadd(out[i + h][j + ell], kmul(u, v))
    return out


def psquare(p):
    return pmul(p, p)


def pdegree(p):
    return max(i + j for i in range(7) for j in range(7) if p[i][j] != K0)


def peval(p, x, y):
    out = K0
    for i in range(7):
        for j in range(7):
            out = kadd(out, pscale_value(p[i][j], Q(x) ** i * Q(y) ** j))
    return out


def pscale_value(value, scalar):
    return (value[0] * scalar, value[1] * scalar)


COS = (k(1), k(Q(1, 2)), k(Q(-1, 2)), k(-1), k(Q(-1, 2)), k(Q(1, 2)))
SIN = (k(), k(0, Q(1, 2)), k(0, Q(1, 2)), k(), k(0, Q(-1, 2)), k(0, Q(-1, 2)))


def displacement(slot):
    i, j = slot
    return (
        padd(PX, pconst(Q(3 * j, 5) - i)),
        padd(PY, pconst(Q(4 * j, 5))),
    )


def dot(a, b):
    return padd(pmul(a[0], b[0]), pmul(a[1], b[1]))


def det(a, b):
    return psub(pmul(a[0], b[1]), pmul(a[1], b[0]))


def rotate_minus(e, exponent):
    c, s = COS[exponent], SIN[exponent]
    return (
        padd(pscale(e[0], c), pscale(e[1], s)),
        padd(pscale(e[1], c), pscale(e[0], kneg(s))),
    )


def incidence_derivations(a, b, exponent):
    d = displacement(a)
    e = displacement(b)
    v = rotate_minus(e, exponent)
    q = dot(d, d)
    w = dot(e, e)
    h = dot(d, v)

    displayed = padd(
        pmul(pmul(q, w), padd(q, w, pscale(h, -2), pconst(-4))),
        pscale(psquare(h), 4),
    )

    # Cramer's numerators for 2 d.u=q and 2 v.u=w, without division.
    nx = psub(pmul(q, v[1]), pmul(w, d[1]))
    ny = psub(pmul(w, d[0]), pmul(q, v[0]))
    cramer = psub(padd(psquare(nx), psquare(ny)), pscale(psquare(det(d, v)), 4))
    assert displayed == cramer
    return displayed


def certificate_polynomial(entry):
    out = pzero()
    previous = None
    for term in entry["terms"]:
        assert isinstance(term, list) and len(term) == 5
        i, j, s, numerator, denominator = term
        assert all(type(x) is int for x in term)
        assert 0 <= i <= 6 and 0 <= j <= 6 and i + j <= 6
        assert s in (0, 1) and denominator > 0 and numerator != 0
        coefficient = Q(numerator, denominator)
        assert coefficient.numerator == numerator and coefficient.denominator == denominator
        index = (i, j, s)
        assert previous is None or previous < index
        previous = index
        out[i][j] = kadd(out[i][j], k(coefficient if s == 0 else 0, coefficient if s == 1 else 0))
    return out


def expected_leading(degree, scalar):
    out = pzero()
    m = degree // 2
    for j in range(m + 1):
        out[2 * j][2 * (m - j)] = k(scalar * comb(m, j))
    return out


def leading_part(p):
    degree = pdegree(p)
    out = pzero()
    for i in range(7):
        for j in range(7):
            if i + j == degree:
                out[i][j] = p[i][j]
    return out


def q_polynomial(slot):
    d = displacement(slot)
    return psub(dot(d, d), pconst(3))


def check_midpoint_control(data):
    control = data["midpoint_control"]
    assert control["translation"] == [[1, 5], [-2, 5]]
    assert control["a"] == [0, 0] and control["b"] == [1, 1] and control["k"] == 3

    # Elements of Q(sqrt(19)); the representation is again a rational pair.
    def decode(point):
        return tuple((Q(a, denominator), Q(b, denominator)) for a, b, denominator in point)

    def add19(a, b):
        return (a[0] + b[0], a[1] + b[1])

    def sub19(a, b):
        return (a[0] - b[0], a[1] - b[1])

    def mul19(a, b):
        return (a[0] * b[0] + 19 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])

    def norm19(point):
        return add19(mul19(point[0], point[0]), mul19(point[1], point[1]))

    x = decode(control["x"])
    y = decode(control["y"])
    zero19 = (Q(0), Q(0))
    centres = (
        (zero19, zero19),
        ((Q(1), Q(0)), zero19),
        ((Q(1, 5), Q(0)), (Q(-2, 5), Q(0))),
        ((Q(4, 5), Q(0)), (Q(2, 5), Q(0))),
    )
    for point, centre_index in ((x, 0), (x, 2), (y, 1), (y, 3)):
        delta = tuple(sub19(u, v) for u, v in zip(point, centres[centre_index]))
        assert norm19(delta) == (Q(1), Q(0))
    assert x not in centres and y not in centres
    assert tuple(add19(u, v) for u, v in zip(x, y)) == centres[1]
    assert (0 + 1 + 0 + 1 + 3) % 2 == 1
    return 4


def main():
    blob = TARGET.read_bytes()
    certificate_hash = sha256(blob).hexdigest()
    assert certificate_hash == EXPECTED_CERTIFICATE_SHA256
    data = json.loads(blob)
    assert data["orientation"] == [[3, 5], [4, 5]]
    assert Q(3, 5) ** 2 + Q(4, 5) ** 2 == 1
    assert data["factor_count"] == 22 and data["target_found"] is False

    expected_ids = []
    generated = {}
    for slot in SLOTS:
        ident = f"self_{slot[0]}{slot[1]}"
        expected_ids.append(ident)
        generated[ident] = q_polynomial(slot)
    for a_index, a in enumerate(SLOTS):
        for b in SLOTS[a_index + 1 :]:
            for exponent in range(6):
                if (sum(a) + sum(b) + exponent) % 2 == 1:
                    ident = f"pair_{a[0]}{a[1]}_{b[0]}{b[1]}_{exponent}"
                    expected_ids.append(ident)
                    generated[ident] = incidence_derivations(a, b, exponent)

    assert len(expected_ids) == 22
    assert [entry["id"] for entry in data["factors"]] == expected_ids

    degree_histogram = {2: 0, 4: 0, 6: 0}
    coefficient_terms = 0
    total_degree = 0
    leading_scalar = 1
    certified = {}
    for entry in data["factors"]:
        ident = entry["id"]
        certificate_poly = certificate_polynomial(entry)
        assert certificate_poly == generated[ident]
        degree = pdegree(certificate_poly)
        assert degree == entry["degree"]
        degree_histogram[degree] += 1
        coefficient_terms += len(entry["terms"])
        total_degree += degree

        exponent = entry.get("k")
        scalar = 1 if exponent in (None, 0, 1, 5) else 3 if exponent in (2, 4) else 4
        assert leading_part(certificate_poly) == expected_leading(degree, scalar)
        leading_scalar *= scalar
        certified[ident] = certificate_poly

    assert degree_histogram == {2: 4, 4: 4, 6: 14}
    assert coefficient_terms == 570
    assert total_degree == data["product_degree"] == 108
    assert leading_scalar == data["product_leading_scalar"] == 104976

    # Check the quotient of all 48 ordered odd-parity incidence slots by
    # reversal.  Self slots factor exactly as q^2(q-3) or 4q^3.
    ordered_conflicts = 0
    ordered_distinct = 0
    self_q_factors = 0
    self_impossible = 0
    factor_uses = {ident: 0 for ident in expected_ids if ident.startswith("pair_")}
    for a, b, exponent in product(SLOTS, SLOTS, range(6)):
        if (sum(a) + sum(b) + exponent) % 2 == 0:
            continue
        ordered_conflicts += 1

        # Directly re-derive the phase contradiction for both choices of the
        # otherwise irrelevant direction-orbit exponent.
        for base_exponent in (0, 1):
            i, j = a
            h, ell = b
            phase_a = (1 - j - i - base_exponent) % 2
            phase_b = (1 - ell - h - base_exponent - exponent) % 2
            assert phase_a != phase_b

        f = incidence_derivations(a, b, exponent)
        if a == b:
            qpoly = padd(q_polynomial(a), pconst(3))
            if exponent in (1, 5):
                assert f == pmul(psquare(qpoly), q_polynomial(a))
                self_q_factors += 1
            else:
                assert exponent == 3
                assert f == pscale(pmul(psquare(qpoly), qpoly), 4)
                self_impossible += 1
        else:
            ordered_distinct += 1
            if a < b:
                ident = f"pair_{a[0]}{a[1]}_{b[0]}{b[1]}_{exponent}"
            else:
                reverse = (-exponent) % 6
                ident = f"pair_{b[0]}{b[1]}_{a[0]}{a[1]}_{reverse}"
            assert f == certified[ident]
            factor_uses[ident] += 1

    assert ordered_conflicts == 48
    assert ordered_distinct == 36
    assert self_q_factors == 8 and self_impossible == 4
    assert set(factor_uses.values()) == {2}

    witness_x, witness_y = Q(1, 5), Q(2, 5)
    witness_distances = []
    for slot in SLOTS:
        value = peval(padd(q_polynomial(slot), pconst(3)), witness_x, witness_y)
        assert value[1] == 0 and 0 < value[0] < 4
        witness_distances.append([value[0].numerator, value[0].denominator])
    for entry in data["factors"]:
        value = peval(certified[entry["id"]], witness_x, witness_y)
        assert value != K0
        assert [[value[0].numerator, value[0].denominator], [value[1].numerator, value[1].denominator]] == entry["witness_value"]
    assert witness_distances == [[1, 5], [52, 25], [4, 5], [37, 25]]
    midpoint_distances = check_midpoint_control(data)

    result = {
        "status": "PASS",
        "certificate_sha256": certificate_hash,
        "complete_coefficient_matches": len(certified),
        "coefficient_terms": coefficient_terms,
        "cramer_formula_polynomial_matches": 18,
        "ordered_odd_parity_slots": ordered_conflicts,
        "ordered_distinct_slots": ordered_distinct,
        "self_slots_reduced_to_q_factor": self_q_factors,
        "self_slots_impossible_by_distinct_centres": self_impossible,
        "degree_histogram": {str(degree): count for degree, count in degree_histogram.items()},
        "product_degree": total_degree,
        "leading_scalar": leading_scalar,
        "witness_cross_squared_distances": witness_distances,
        "midpoint_control_unit_distances": midpoint_distances,
        "target_breakthrough": False,
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
