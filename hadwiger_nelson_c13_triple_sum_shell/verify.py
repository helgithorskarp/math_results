#!/usr/bin/env python3
"""Exact verifier for the C13 triple-sum one-step shell theorem.

Coordinates are elements of Q[t,r,s]/(t^2-5,r^2+3,s^2+11), embedded by
t=sqrt(5), r=i sqrt(3), s=i sqrt(11), and stored in the Cartesian numerator
basis described in README.md with common denominator 96.
"""
from fractions import Fraction as F
from itertools import product
import argparse
import collections
import hashlib
import json
from pathlib import Path

SQUARES = (5, -3, -11)
ZERO = (0,) * 8
ONE = (1, 0, 0, 0, 0, 0, 0, 0)
DENOMINATOR = 96
TARGET = DENOMINATOR ** 2

TABLE = []
for i in range(8):
    row = []
    for j in range(8):
        coefficient = 1
        for k, square in enumerate(SQUARES):
            if (i & j) & (1 << k):
                coefficient *= square
        row.append((i ^ j, coefficient))
    TABLE.append(row)


def plus(x, y):
    return tuple(a + b for a, b in zip(x, y))


def minus(x, y):
    return tuple(a - b for a, b in zip(x, y))


def scale(x, coefficient):
    return tuple(coefficient * a for a in x)


def conjugate(x):
    return tuple(-a if bool(i & 2) ^ bool(i & 4) else a
                 for i, a in enumerate(x))


def multiply(x, y):
    z = [0] * 8
    for i, a in enumerate(x):
        if a:
            for j, b in enumerate(y):
                if b:
                    k, coefficient = TABLE[i][j]
                    z[k] += a * b * coefficient
    return tuple(z)


def power(x, exponent):
    if exponent < 0:
        return power(conjugate(x), -exponent)
    z = ONE
    for _ in range(exponent):
        z = multiply(z, x)
    return z


def cartesian_key(x):
    """Convert tensor order 1,t,r,tr,s,ts,rs,trs to x/y radical order."""
    a, b, e, f, g, h, minus_c, minus_d = x
    return a, b, -minus_c, -minus_d, e, f, g, h


def numerator(x):
    z = scale(x, DENOMINATOR)
    if any(F(a).denominator != 1 for a in z):
        raise ValueError("nonintegral coordinate numerator")
    return tuple(map(int, cartesian_key(z)))


def base_geometry():
    omega = (F(1, 2), 0, F(1, 2), 0, 0, 0, 0, 0)
    v = (0, 0, F(1, 6), 0, 0, 0, F(-1, 6), 0)
    rho = (F(7, 8), 0, 0, F(1, 8), 0, 0, 0, 0)
    if power(omega, 6) != ONE:
        raise ValueError("omega is not a sixth root of unity")
    if multiply(v, conjugate(v)) != ONE or multiply(rho, conjugate(rho)) != ONE:
        raise ValueError("a defining direction is not a unit")

    direction_set = set()
    for j, k in product(range(6), range(-2, 3)):
        z = multiply(power(omega, j), power(v, k))
        direction_set.add(numerator(z))
        direction_set.add(numerator(multiply(rho, z)))
    directions = tuple(sorted(direction_set))

    u = power(v, 2)
    spindle = (ZERO, ONE, omega, plus(ONE, omega), u,
               multiply(u, omega), multiply(u, plus(ONE, omega)))
    c13 = tuple(numerator(z) for z in spindle +
                tuple(multiply(rho, z) for z in spindle[1:]))
    if len(directions) != 60 or len(set(c13)) != 13:
        raise ValueError("wrong direction or C13 cardinality")
    return directions, c13


def unit_delta(d):
    a, b, c, d0, e, f, g, h = d
    constant = (a*a + 5*b*b + 33*c*c + 165*d0*d0 +
                3*e*e + 15*f*f + 11*g*g + 55*h*h)
    if constant != TARGET:
        return False
    sqrt5 = 2 * (a*b + 33*c*d0 + 3*e*f + 11*g*h)
    sqrt33 = 2 * (a*c + 5*b*d0 + e*g + 5*f*h)
    sqrt165 = 2 * (a*d0 + b*c + e*h + f*g)
    return sqrt5 == sqrt33 == sqrt165 == 0


def is_unit(x, y):
    return unit_delta(minus(x, y))


def reconstruct(minimum_contacts=2):
    directions, c13 = base_geometry()
    if not all(unit_delta(z) for z in directions):
        raise ValueError("nonunit direction")
    triple_sum = tuple(sorted({plus(plus(a, b), c)
                               for a, b, c in product(c13, repeat=3)}))
    candidates = set()
    triple_set = set(triple_sum)
    for b, direction in product(triple_sum, directions):
        z = plus(b, direction)
        if z not in triple_set:
            candidates.add(z)
    contact_counts = {}
    for z in candidates:
        count = sum(is_unit(z, b) for b in triple_sum)
        if count >= minimum_contacts:
            contact_counts[z] = count
    shell = tuple(sorted(contact_counts))
    points = tuple(sorted(triple_set | set(shell)))
    return directions, c13, triple_sum, shell, contact_counts, points


def strict_edges(points):
    return tuple((i, j) for j in range(len(points)) for i in range(j)
                 if is_unit(points[i], points[j]))


def proper(word, edges, vertex_count):
    if (type(word) is not str or len(word) != vertex_count or
            set(word) - set("0123")):
        raise ValueError("malformed four-colour word")
    if any(word[a] == word[b] for a, b in edges):
        raise ValueError("monochromatic unit edge")


def compact_hash(value):
    data = json.dumps(value, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def check(certificate):
    required = {
        "format": 1,
        "denominator": DENOMINATOR,
        "directions": 60,
        "motif_vertices": 13,
        "base_operation": "C13+C13+C13",
        "minimum_base_contacts": 2,
    }
    if any(certificate.get(k) != value for k, value in required.items()):
        raise ValueError("wrong construction parameters")

    directions, c13, triple_sum, shell, contacts, points = reconstruct()
    if len(triple_sum) != 403 or len(shell) != 2940 or len(points) != 3343:
        raise ValueError("wrong exact construction cardinality")
    edges = strict_edges(points)
    if len(edges) != 21044:
        raise ValueError("wrong strict unit-edge count")
    contact_histogram = dict(sorted(collections.Counter(contacts.values()).items()))
    expected_histogram = {2: 2108, 3: 576, 4: 156, 5: 80, 6: 18, 8: 2}
    if contact_histogram != expected_histogram:
        raise ValueError("wrong base-contact histogram")
    if any(certificate.get(k) != value for k, value in {
            "base_vertices": 403, "shell_vertices": 2940,
            "host_vertices": 3343, "host_edges": 21044,
            "base_contact_histogram": {str(k): v for k, v in expected_histogram.items()},
            "coordinate_sha256": compact_hash(points),
            "edge_sha256": compact_hash(edges)}.items()):
        raise ValueError("certificate receipt mismatch")
    proper(certificate.get("colouring"), edges, len(points))

    point_index = {z: i for i, z in enumerate(points)}
    if not set(c13).issubset(point_index):
        raise ValueError("C13 is not contained in the triple sum")
    spindle_indices = [point_index[z] for z in c13[:7]]
    spindle_edges = tuple((i, j) for j in range(7) for i in range(j)
                           if is_unit(c13[i], c13[j]))
    proper3 = sum(all(word[i] != word[j] for i, j in spindle_edges)
                  for word in product(range(3), repeat=7))
    if len(spindle_edges) != 11 or proper3 != 0:
        raise ValueError("Moser-spindle lower-bound check failed")

    return {
        "verified": True,
        "base_vertices": len(triple_sum),
        "shell_vertices": len(shell),
        "host_vertices": len(points),
        "host_edges": len(edges),
        "base_contact_histogram": contact_histogram,
        "four_colour_word_verified": True,
        "moser_spindle_edges": len(spindle_edges),
        "moser_spindle_three_colourings_checked": 3 ** 7,
        "moser_spindle_proper_three_colourings": proper3,
        "chromatic_number": 4,
        "classified_subsets": "2^2940",
        "target_order_additions": 508 - len(triple_sum),
        "record_improvement": False,
        "coordinate_sha256": compact_hash(points),
        "edge_sha256": compact_hash(edges),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=Path(__file__).with_name("certificate.json"))
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    result = check(json.loads(raw))
    result["certificate_sha256"] = hashlib.sha256(raw).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
