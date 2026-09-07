#!/usr/bin/env python3
"""Independent exact audit of the de Grey 1581 residue-section theorem.

No code is imported from the reviewed package. SymPy reconstructs the point
set and supplies exact primitive-number-field arithmetic. Affine hyperplanes
are enumerated as scalar-equivalence classes of all nonzero equations.
"""

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path

import sympy as sp


SEED_SHA256 = "69b9c1c2ab221c2d3df92f1fd800be51e812f268b58e145793ff56e6b1d37806"
CERTIFICATE_SHA256 = "b4ff0d1a41f3353be1777247a6606191c1b2876acb4fec9888b8e272e64fb067"
SCALE = 3072
LIMIT = 508
RADICAND_VALUES = (1, 3, 5, 15, 11, 33, 55, 165,
                    7, 21, 35, 105, 77, 231, 385, 1155)
MODULAR_EMBEDDINGS = (
    (3061, {3: 601, 5: 367, 7: 166, 11: 866}),
    (3251, {3: 788, 5: 255, 7: 419, 11: 1550}),
)

# Independently transcribed from Section 6 of arXiv:1804.02385v2. A row
# (a,b,c,d) means ((a+b*sqrt(33))/12,(c*sqrt(3)+d*sqrt(11))/12).
SEED_ROWS = (
    (0, 0, 0, 0), (4, 0, 0, 0), (12, 0, 0, 0), (24, 0, 0, 0),
    (-6, 2, 0, 0), (6, 0, 2, 0), (12, 0, 4, 0), (18, 0, 6, 0),
    (14, 0, 0, 2), (2, 0, 4, -2), (10, 0, 4, -2), (8, 0, -2, 2),
    (8, 0, 6, -2), (0, 2, 2, 0), (6, 2, 4, 0), (2, 2, 6, -2),
    (-2, 2, 6, -2), (2, 2, -2, 2), (-2, 2, -2, 2), (-4, 2, 4, -2),
    (-8, 2, 4, -2), (13, 1, -1, 1), (11, 1, 1, 1), (9, 1, -3, 3),
    (9, 1, 3, 1), (7, 1, 1, 1), (7, 1, 3, -1), (5, 1, 5, -1),
    (5, 1, -1, 1), (3, 1, -5, 3), (3, 1, 1, 1), (3, 1, 3, -1),
    (1, 1, -1, 1), (-1, 1, 3, -1), (-3, 1, -1, 1), (15, -1, -3, 3),
    (15, -1, 7, -3), (13, -1, 3, -1), (11, -1, -1, 1),
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def turn(point, phase):
    """Complex multiplication on pairs (real, imaginary)."""
    x, y = point
    a, b = phase
    return sp.expand(x*a-y*b), sp.expand(x*b+y*a)


def coefficient_vector(value, radicals):
    simplified = sp.expand(sp.radsimp(value))
    terms = sp.collect(simplified, radicals[1:], evaluate=False)
    require(set(terms).issubset(set(radicals)), "unexpected radical")
    coefficients = tuple(sp.Rational(terms.get(radical, 0)) for radical in radicals)
    require(all(coefficient.is_Rational for coefficient in coefficients),
            "nonrational coefficient")
    require(sp.expand(simplified-sum(c*r for c, r in zip(coefficients, radicals))) == 0,
            "basis reconstruction")
    scaled = tuple(SCALE*coefficient for coefficient in coefficients)
    require(all(coefficient.q == 1 for coefficient in scaled), "coordinate scale")
    return tuple(int(coefficient) for coefficient in scaled)


def check_seed_file(target):
    raw = (target / "seeds.json").read_bytes()
    require(sha256(raw) == SEED_SHA256, "seed-file digest")
    parsed = json.loads(raw)
    require(parsed.get("scale") == 12, "seed scale")
    require(tuple(map(tuple, parsed.get("points", ()))) == SEED_ROWS,
            "seed transcription differs from independent table")


def construct(target):
    check_seed_file(target)
    root3, root5, root7, root11 = map(sp.sqrt, (3, 5, 7, 11))
    radicals = (sp.Integer(1), root3, root5, sp.sqrt(15), root11, sp.sqrt(33),
                sp.sqrt(55), sp.sqrt(165), root7, sp.sqrt(21), sp.sqrt(35),
                sp.sqrt(105), sp.sqrt(77), sp.sqrt(231), sp.sqrt(385),
                sp.sqrt(1155))

    omega = (sp.Rational(1, 2), root3/2)
    rotations = [(sp.Integer(1), sp.Integer(0))]
    for _ in range(5):
        rotations.append(turn(rotations[-1], omega))
    sb = set()
    for a, b, c, d in SEED_ROWS:
        point = ((a+b*sp.sqrt(33))/12, (c*root3+d*root11)/12)
        for reflected in (point, (point[0], -point[1])):
            for phase in rotations:
                sb.add(turn(reflected, phase))
    require(len(sb) == 397, "Sb order")

    third = sp.Rational(1, 3)
    sa = sb - {(third, sp.Integer(0)), (-third, sp.Integer(0))}
    require(len(sa) == 395, "Sa order")
    inner_phase = (sp.Rational(7, 8), sp.sqrt(15)/8)
    require(sp.expand(inner_phase[0]**2+inner_phase[1]**2) == 1,
            "inner phase norm")
    half = sa | {turn(point, inner_phase) for point in sb}
    require(len(half) == 791, "half order")

    outer_phase = (sp.Rational(31, 32), 3*root7/32)
    require(sp.expand(outer_phase[0]**2+outer_phase[1]**2) == 1,
            "outer phase norm")
    image = set()
    for x, y in half:
        qx, qy = turn((x+2, y), outer_phase)
        image.add((sp.expand(qx-2), sp.expand(qy)))
    require(len(image) == 791, "outer image order")
    require(half & image == {(-sp.Integer(2), sp.Integer(0))}, "outer intersection")

    expressions = half | image
    points = sorted(coefficient_vector(x, radicals)+coefficient_vector(y, radicals)
                    for x, y in expressions)
    require(len(points) == 1581 and len(set(points)) == 1581, "host order")
    return points, radicals


def modular_basis_images(modulus, prime_roots):
    require(all(root*root % modulus == prime % modulus
                for prime, root in prime_roots.items()), "invalid modular root")
    images = []
    for radicand in RADICAND_VALUES:
        value, remainder = 1, radicand
        for prime in (3, 5, 7, 11):
            if remainder % prime == 0:
                value = value*prime_roots[prime] % modulus
                remainder //= prime
        require(remainder == 1, "radicand outside four-prime basis")
        images.append(value)
    return tuple(images)


def field_value(coefficients, basis, field):
    value = field.zero
    for coefficient, monomial in zip(coefficients, basis):
        if coefficient:
            value += field.convert(coefficient)*monomial
    return value


def exact_edges(points, radicals):
    projections = []
    for modulus, roots in MODULAR_EMBEDDINGS:
        images = modular_basis_images(modulus, roots)
        projections.append(tuple(
            (sum(a*b for a, b in zip(point[:16], images)) % modulus,
             sum(a*b for a, b in zip(point[16:], images)) % modulus)
            for point in points))

    survivors = []
    for v in range(len(points)):
        for u in range(v):
            for (modulus, _), projection in zip(MODULAR_EMBEDDINGS, projections):
                dx = projection[v][0]-projection[u][0]
                dy = projection[v][1]-projection[u][1]
                if (dx*dx+dy*dy-SCALE*SCALE) % modulus:
                    break
            else:
                survivors.append((u, v))

    field = sp.QQ.algebraic_field(sp.sqrt(3), sp.sqrt(5), sp.sqrt(7), sp.sqrt(11))
    basis = tuple(field.from_sympy(radical) for radical in radicals)
    values = tuple((field_value(point[:16], basis, field),
                    field_value(point[16:], basis, field)) for point in points)
    unit = field.convert(SCALE*SCALE)
    edges = []
    for u, v in survivors:
        dx = values[v][0]-values[u][0]
        dy = values[v][1]-values[u][1]
        if dx*dx+dy*dy == unit:
            edges.append((u, v))
    edges.sort()
    require(len(edges) == 7877, "unit-edge count")
    return edges, len(survivors)


def residue_projection(points):
    columns = tuple(i for i in range(16) if any(point[i] for point in points))
    divisors = tuple(math.gcd(*(abs(point[i]) for point in points)) for i in columns)
    require(columns == (0, 2, 5, 7, 9, 11, 12, 14), "x columns")
    require(divisors == (1, 3, 1, 1, 3, 3, 3, 9), "x divisors")
    residues = tuple(tuple((point[i]//divisor) % 3
                           for i, divisor in zip(columns, divisors))
                     for point in points)
    require(len(set(residues)) == 205, "residue fibres")
    return columns, divisors, residues


def equation_classes(dimension):
    """Quotient all nonzero affine equations by simultaneous scalar 2."""
    representatives = set()
    descriptions = 0
    for normal in itertools.product(range(3), repeat=dimension):
        if not any(normal):
            continue
        for level in range(3):
            descriptions += 1
            equation = normal+(level,)
            doubled = tuple(2*x % 3 for x in equation)
            representatives.add(min(equation, doubled))
    require(descriptions == 19_680, "raw equation count")
    require(len(representatives) == 9_840, "affine equation quotient")
    return tuple(sorted((equation[:-1], equation[-1]) for equation in representatives))


def hyperplanes(residues):
    fibres = {}
    for vertex, residue in enumerate(residues):
        fibres[residue] = fibres.get(residue, 0) | (1 << vertex)
    records = []
    for normal, level in equation_classes(8):
        support = 0
        for residue, mask in fibres.items():
            if sum(a*b for a, b in zip(normal, residue)) % 3 == level:
                support |= mask
        records.append((normal, level, support))
    admissible = tuple(record for record in records if record[2].bit_count() <= LIMIT)
    require(len(records) == 9_840, "hyperplane count")
    require(len(admissible) == 2_118, "admissible hyperplanes")
    require(len({support for _, _, support in admissible}) == 2_100,
            "distinct admissible supports")
    return tuple(records), admissible


def check_certificate(target, points, edges, residues, admissible):
    raw = (target / "certificate.json").read_bytes()
    require(sha256(raw) == CERTIFICATE_SHA256, "certificate digest")
    certificate = json.loads(raw)
    require(certificate.get("version") == "degrey-residue-hyperplanes-v1", "version")
    require(type(certificate.get("target")) is int and certificate["target"] == LIMIT,
            "target")
    deleted = certificate.get("deleted")
    require(type(deleted) is int and deleted == 1580, "deleted label")
    require(points[deleted] == (2*SCALE,)+(0,)*31, "deleted endpoint")
    require(not any(residues[deleted]), "endpoint residue")

    base = certificate.get("base_word")
    require(isinstance(base, str) and len(base) == len(points), "base word")
    require(all(character in ("-" if vertex == deleted else "0123")
                for vertex, character in enumerate(base)), "base support")
    base_checks = 0
    for u, v in edges:
        if u != deleted and v != deleted:
            require(base[u] != base[v], "base monochromatic edge")
            base_checks += 1

    zero_supports = {support for _, level, support in admissible if level == 0}
    supplied = set()
    exception_checks = 0
    exceptions = certificate.get("exceptions")
    require(isinstance(exceptions, list), "exceptions")
    for entry in exceptions:
        normal_text, word = entry.get("normal"), entry.get("word")
        require(isinstance(normal_text, str) and len(normal_text) == 8 and
                set(normal_text) <= set("012") and "1" in normal_text,
                "exception normal")
        normal = tuple(map(int, normal_text))
        first = next(value for value in normal if value)
        require(first == 1, "unnormalized exception normal")
        support = sum(1 << vertex for vertex, residue in enumerate(residues)
                      if sum(a*b for a, b in zip(normal, residue)) % 3 == 0)
        require(support in zero_supports and support not in supplied,
                "invalid or duplicate exception support")
        supplied.add(support)
        vertices = tuple(v for v in range(len(points)) if support & (1 << v))
        require(isinstance(word, str) and len(word) == len(vertices) and
                set(word) <= set("0123"), "exception word")
        colours = dict(zip(vertices, word))
        for u, v in edges:
            if u in colours and v in colours:
                require(colours[u] != colours[v], "exception monochromatic edge")
                exception_checks += 1
    require(supplied == zero_supports, "incomplete zero-level support cover")
    require(all(not (support & (1 << deleted))
                for _, level, support in admissible if level != 0),
            "base does not cover nonzero section")
    return deleted, len(exceptions), base_checks, exception_checks


def run(target):
    points, radicals = construct(target)
    edges, survivors = exact_edges(points, radicals)
    columns, divisors, residues = residue_projection(points)
    records, admissible = hyperplanes(residues)
    deleted, exceptions, base_checks, exception_checks = check_certificate(
        target, points, edges, residues, admissible)

    coordinate_stream = "".join(" ".join(map(str, point))+"\n" for point in points).encode()
    edge_stream = "".join(f"{u} {v}\n" for u, v in edges).encode()
    hyperplane_stream = "".join(
        "".join(map(str, normal))+f" {level} {support:x}\n"
        for normal, level, support in sorted(records)).encode()
    multiplicities = Counter(support for _, _, support in admissible)
    return {
        "accepted": True,
        "arbitrary_target_subsets_classified": False,
        "seed_rows": len(SEED_ROWS),
        "construction_orders": [397, 395, 791, len(points)],
        "vertices": len(points),
        "edges": len(edges),
        "pair_checks": len(points)*(len(points)-1)//2,
        "modular_survivors": survivors,
        "moduli": [modulus for modulus, _ in MODULAR_EMBEDDINGS],
        "coordinate_sha256": sha256(coordinate_stream),
        "edge_sha256": sha256(edge_stream),
        "x_columns": list(columns),
        "x_divisors": list(divisors),
        "residue_fibres": len(set(residues)),
        "raw_affine_equations": 19_680,
        "affine_hyperplanes": len(records),
        "admissible_hyperplanes": len(admissible),
        "distinct_admissible_supports": len(multiplicities),
        "duplicate_descriptions": sum(count-1 for count in multiplicities.values()),
        "admissible_by_level": [sum(level == b for _, level, _ in admissible)
                                for b in range(3)],
        "exact_target_sections": sum(support.bit_count() == LIMIT
                                     for _, _, support in admissible),
        "admissible_order_range": [min(s.bit_count() for _, _, s in admissible),
                                   max(s.bit_count() for _, _, s in admissible)],
        "zero_level_distinct_supports": len({s for _, b, s in admissible if b == 0}),
        "zero_level_order_range": [min(s.bit_count() for _, b, s in admissible if b == 0),
                                   max(s.bit_count() for _, b, s in admissible if b == 0)],
        "hyperplane_stream_sha256": sha256(hyperplane_stream),
        "deleted": deleted,
        "exception_words": exceptions,
        "base_edge_checks": base_checks,
        "exception_edge_checks": exception_checks,
        "total_colour_edge_checks": base_checks+exception_checks,
        "seed_sha256": SEED_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "geometry_engine": "SymPy exact symbolic construction and AlgebraicField/ANP",
        "family_engine": "all equations modulo nonzero scalar equivalence",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--expected", type=Path)
    arguments = parser.parse_args()
    result = run(arguments.target)
    if arguments.expected:
        require(result == json.loads(arguments.expected.read_text()),
                "expected report mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))
