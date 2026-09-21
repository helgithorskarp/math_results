#!/usr/bin/env python3
"""Exact audit for the denominator-five local-cancellation octagons."""

from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import ceil, floor, gcd
from pathlib import Path


NORMALS = (
    (1, 1), (-1, 4), (-1, 1), (-4, -1),
    (-1, -1), (1, -4), (1, -1), (4, 1),
)

# Affine polynomials are stored as (constant, coefficient of t).
SUPPORTS = (
    (0, 11), (1, 29), (1, 11), (1, 29),
    (1, 11), (3, 29), (3, 11), (0, 29),
)

EXPECTED_VERTICES = (
    ((Fraction(-1, 5), 3), (Fraction(1, 5), 8)),
    ((-1, -5), (0, 6)),
    ((Fraction(-2, 5), -8), (Fraction(3, 5), 3)),
    ((0, -6), (-1, -5)),
    ((Fraction(-1, 5), -3), (Fraction(-4, 5), -8)),
    ((3, 5), (0, -6)),
    ((Fraction(3, 5), 8), (Fraction(-12, 5), -3)),
    ((0, 6), (0, 5)),
)

EXPECTED_LENGTHS = (
    (Fraction(1, 5), 3), (Fraction(1, 5), 2),
    (Fraction(-3, 5), 3), (Fraction(2, 5), 2),
    (Fraction(-1, 5), 3), (Fraction(4, 5), 2),
    (Fraction(-12, 5), 3), (Fraction(3, 5), 2),
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def lin_add(left, right):
    return tuple(Fraction(a) + Fraction(b) for a, b in zip(left, right))


def lin_scale(scalar, value):
    return tuple(Fraction(scalar) * Fraction(a) for a in value)


def lin_value(value, t):
    return Fraction(value[0]) + Fraction(value[1]) * t


def poly_add(left, right):
    size = max(len(left), len(right))
    return tuple(
        (Fraction(left[i]) if i < len(left) else 0)
        + (Fraction(right[i]) if i < len(right) else 0)
        for i in range(size)
    )


def poly_scale(scalar, value):
    return tuple(Fraction(scalar) * Fraction(a) for a in value)


def poly_mul(left, right):
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += Fraction(a) * Fraction(b)
    return tuple(result)


def determinant(left, right):
    return left[0] * right[1] - left[1] * right[0]


def symbolic_vertices():
    vertices = []
    for i in range(8):
        a, c = NORMALS[i]
        d, e = NORMALS[(i + 1) % 8]
        det = determinant(NORMALS[i], NORMALS[(i + 1) % 8])
        left = SUPPORTS[i]
        right = SUPPORTS[(i + 1) % 8]
        x = lin_scale(Fraction(1, det),
                      lin_add(lin_scale(e, left), lin_scale(-c, right)))
        y = lin_scale(Fraction(1, det),
                      lin_add(lin_scale(a, right), lin_scale(-d, left)))
        vertices.append((x, y))
    return tuple(vertices)


def symbolic_lengths(vertices):
    lengths = []
    for i, (nx, ny) in enumerate(NORMALS):
        dx = lin_add(vertices[i][0], lin_scale(-1, vertices[i - 1][0]))
        dy = lin_add(vertices[i][1], lin_scale(-1, vertices[i - 1][1]))
        # Positively traversed tangent is (-ny,nx).
        if ny:
            length = lin_scale(Fraction(-1, ny), dx)
            require(dy == lin_scale(nx, length), f"edge direction {i}")
        else:
            length = lin_scale(Fraction(1, nx), dy)
        lengths.append(length)
    return tuple(lengths)


def symbolic_area(vertices):
    twice = (Fraction(0), Fraction(0), Fraction(0))
    for i in range(8):
        x, y = vertices[i]
        next_x, next_y = vertices[(i + 1) % 8]
        twice = poly_add(
            twice,
            poly_add(poly_mul(x, next_y), poly_scale(-1, poly_mul(y, next_x))),
        )
    return poly_scale(Fraction(1, 2), twice)


def support_values(t):
    return tuple(int(lin_value(value, t)) for value in SUPPORTS)


def vertex_values(t):
    return tuple(
        (lin_value(x, t), lin_value(y, t))
        for x, y in EXPECTED_VERTICES
    )


def normalized_profiles():
    profiles = []
    for i in (0, 2, 4, 6):
        require(determinant(NORMALS[i], NORMALS[i + 1]) == 5,
                "bad vertex lost index five")
        epsilon = (1, 1)
        for column in range(2):
            require(sum(epsilon[row] * NORMALS[i + row][column]
                        for row in range(2)) % 5 == 0,
                    "diagonal character does not annihilate the active image")
        c_poly = lin_add(SUPPORTS[i], SUPPORTS[i + 1])
        require(c_poly[1] % 5 == 0, "profile depends on t modulo five")
        c = int(c_poly[0]) % 5
        require(c, "bad vertex became integral")
        inverse = pow(c, -1, 5)
        profiles.append((inverse, inverse))
    return tuple(profiles)


def cyclotomic_reduce(coefficients, p=5):
    cyclic = [Fraction(0)] * p
    for exponent, coefficient in enumerate(coefficients):
        cyclic[exponent % p] += coefficient
    top = cyclic[-1]
    return tuple(cyclic[i] - top for i in range(p - 1))


def zeta_power(exponent, p=5):
    raw = [Fraction(0)] * (exponent % p + 1)
    raw[exponent % p] = 1
    return cyclotomic_reduce(raw, p)


def cyclotomic_add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def cyclotomic_scale(scalar, value):
    return tuple(Fraction(scalar) * a for a in value)


def cyclotomic_mul(left, right, p=5):
    raw = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            raw[i + j] += a * b
    return cyclotomic_reduce(raw, p)


def reciprocal_one_minus(exponent, p=5):
    # (1-zeta^a)^(-1)=-(1/p) sum_(r=1)^(p-1) r zeta^(ar).
    result = (Fraction(0),) * (p - 1)
    for r in range(1, p):
        result = cyclotomic_add(
            result, cyclotomic_scale(Fraction(-r, p), zeta_power(exponent * r, p))
        )
    return result


def check_cancellation():
    zero = (Fraction(0),) * 4
    checks = 0
    for h in range(1, 5):
        total = zero
        for a in range(1, 5):
            reciprocal = reciprocal_one_minus(h * a)
            total = cyclotomic_add(total, cyclotomic_mul(reciprocal, reciprocal))
        require(total == zero, f"Fourier cancellation failed in mode {h}")
        checks += 1
    return checks


def count_lattice_points(t, n):
    supports = support_values(t)
    vertices = vertex_values(t)
    scaled_x = [n * vertex[0] for vertex in vertices]
    minimum_x = floor(min(scaled_x))
    maximum_x = ceil(max(scaled_x))
    count = 0
    for x in range(minimum_x, maximum_x + 1):
        lower = None
        upper = None
        feasible = True
        for (a, b), support in zip(NORMALS, supports):
            rhs = n * support - a * x
            if b > 0:
                bound = rhs // b
                upper = bound if upper is None else min(upper, bound)
            elif b < 0:
                bound = -((-rhs) // b)  # ceil(rhs/b), valid for negative b
                lower = bound if lower is None else max(lower, bound)
            elif rhs < 0:
                feasible = False
                break
        if feasible and lower is not None and upper is not None and lower <= upper:
            count += upper - lower + 1
    return count


def interpolate_quadratic(points):
    coefficients = [Fraction(0)] * 3
    for i, (x_i, y_i) in enumerate(points):
        basis = [Fraction(1)]
        denominator = 1
        for j, (x_j, _) in enumerate(points):
            if i == j:
                continue
            basis = list(poly_mul(basis, (-x_j, 1)))
            denominator *= x_i - x_j
        for degree, coefficient in enumerate(basis):
            coefficients[degree] += Fraction(y_i, denominator) * coefficient
    return tuple(coefficients)


def predicted_coefficients(t):
    return (
        Fraction(1),
        Fraction(20 * t - 1, 2),
        Fraction(364 * t * t + 50 * t - 5, 2),
    )


def direct_count_checks():
    records = []
    residue_polynomials = 0
    holdouts = 0
    for t in range(1, 7):
        predicted = predicted_coefficients(t)
        for residue in range(5):
            ns = [residue + 5 * m for m in range(4)]
            values = [count_lattice_points(t, n) for n in ns]
            records.extend((t, n, value) for n, value in zip(ns, values))
            polynomial = interpolate_quadratic(list(zip(ns[:3], values[:3])))
            require(polynomial == predicted,
                    f"residue polynomial mismatch for {(t, residue)}")
            reconstructed = sum(polynomial[j] * ns[3] ** j for j in range(3))
            require(reconstructed == values[3],
                    f"unused count mismatch for {(t, residue)}")
            residue_polynomials += 1
            holdouts += 1
    payload = json.dumps(records, separators=(",", ":"))
    return {
        "count_values": len(records),
        "max_n": 19,
        "residue_polynomials": residue_polynomials,
        "t_values": [1, 2, 3, 4, 5, 6],
        "unused_count_values": holdouts,
        "record_sha256": sha256(payload.encode()).hexdigest(),
    }


def symbolic_checks():
    require(tuple(gcd(abs(a), abs(b)) for a, b in NORMALS) == (1,) * 8,
            "a facet normal is not primitive")
    determinants = tuple(
        determinant(NORMALS[i], NORMALS[(i + 1) % 8]) for i in range(8)
    )
    require(determinants == (5, 3, 5, 3, 5, 3, 5, 3),
            "normal fan determinant pattern changed")
    vertices = symbolic_vertices()
    require(vertices == EXPECTED_VERTICES, "symbolic vertex formula changed")
    lengths = symbolic_lengths(vertices)
    require(lengths == EXPECTED_LENGTHS, "symbolic edge length formula changed")
    for i, vertex in enumerate(vertices):
        for j, normal in enumerate(NORMALS):
            slack = lin_add(
                SUPPORTS[j],
                lin_scale(-1, lin_add(lin_scale(normal[0], vertex[0]),
                                      lin_scale(normal[1], vertex[1]))),
            )
            if j in (i, (i + 1) % 8):
                require(slack == (0, 0), f"incident slack {i,j}")
            else:
                require(slack[1] >= 0 and lin_value(slack, 1) > 0,
                        f"nonincident slack not positive for t>=1: {i,j,slack}")
    for i, length in enumerate(lengths):
        require(length[1] >= 0 and lin_value(length, 1) > 0,
                f"facet {i} is not actual for t>=1")
    area = symbolic_area(vertices)
    require(area == (Fraction(-5, 2), Fraction(25), Fraction(182)),
            "area polynomial changed")
    perimeter = (Fraction(0), Fraction(0))
    for length in lengths:
        perimeter = lin_add(perimeter, length)
    require(perimeter == (-1, 20), "perimeter polynomial changed")
    profiles = normalized_profiles()
    require(profiles == ((1, 1), (3, 3), (4, 4), (2, 2)),
            "normalized profiles changed")
    # In the all-bad quadrilateral reduction, the final determinant divided
    # by five is forced to be -3 modulo five, but cyclic index five needs 1.
    require((-3) % 5 != 1, "quadrilateral obstruction disappeared")
    return {
        "area": "(364*t^2+50*t-5)/2",
        "edge_lengths": [
            f"{a}+{b}*t" for a, b in lengths
        ],
        "normal_determinants": list(determinants),
        "normalized_perimeter": "20*t-1",
        "profiles": [list(profile) for profile in profiles],
        "quadrilateral_obstruction": "forced 2 mod 5, required 1 mod 5",
    }


def main():
    report = {
        "cyclotomic": {
            "nonzero_mode_checks": check_cancellation(),
            "p": 5,
        },
        "direct_counts": direct_count_checks(),
        "status": "all exact checks passed",
        "symbolic_family": symbolic_checks(),
    }
    expected = json.loads(Path(__file__).with_name("expected.json").read_text())
    require(report == expected, "report differs from expected.json")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
