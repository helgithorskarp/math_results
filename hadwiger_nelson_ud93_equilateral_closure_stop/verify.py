#!/usr/bin/env python3
"""Exact standard-library verifier for the maximal capped UD9-3 closure.

The source is the unique zero in a certified rational box of a four-equation
quadratic system written in the basis ``1,rho``, where ``rho^2-rho+1=0``.
Every closure address is an exact affine expression over three source
generators.  The verifier reconstructs all points and all unit edges, excludes
every other pair by rational interval bounds, and checks the positive colour
word directly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "certificate.json"
EXPECTED = HERE / "EXPECTED.json"
SOURCE_EDGES = (
    (0, 1), (0, 2), (0, 4), (1, 3), (1, 8), (2, 4), (2, 6),
    (2, 7), (3, 5), (3, 6), (3, 7), (3, 8), (4, 5), (5, 8),
    (6, 7),
)
ROOTS = ((Q(1), Q(0)), (Q(0), Q(1)), (Q(-1), Q(1)),
         (Q(-1), Q(0)), (Q(0), Q(-1)), (Q(1), Q(-1)))
EXPECTED_ROWS = ((9, 15), (24, 45), (50, 108), (91, 209),
                 (140, 333), (196, 486), (267, 677), (346, 891),
                 (432, 1134), (533, 1415))
ZERO_EXP = (0, 0, 0, 0)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def clean(poly):
    return {exponent: coefficient for exponent, coefficient in poly.items()
            if coefficient}


def pconst(value):
    value = Q(value)
    return {} if not value else {ZERO_EXP: value}


def pvar(index):
    exponent = [0] * 4
    exponent[index] = 1
    return {tuple(exponent): Q(1)}


def padd(left, right):
    answer = dict(left)
    for exponent, coefficient in right.items():
        answer[exponent] = answer.get(exponent, Q(0)) + coefficient
    return clean(answer)


def pneg(poly):
    return {exponent: -coefficient for exponent, coefficient in poly.items()}


def psub(left, right):
    return padd(left, pneg(right))


def pscale(poly, scalar):
    scalar = Q(scalar)
    return clean({exponent: scalar * coefficient
                  for exponent, coefficient in poly.items()})


def pmul(left, right):
    answer = {}
    for a, x in left.items():
        for b, y in right.items():
            exponent = tuple(i + j for i, j in zip(a, b))
            answer[exponent] = answer.get(exponent, Q(0)) + x * y
    return clean(answer)


def pdiff(poly, index):
    answer = {}
    for exponent, coefficient in poly.items():
        if exponent[index]:
            reduced = list(exponent)
            reduced[index] -= 1
            key = tuple(reduced)
            answer[key] = answer.get(key, Q(0)) + coefficient * exponent[index]
    return clean(answer)


def peval(poly, point):
    answer = Q(0)
    for exponent, coefficient in poly.items():
        term = coefficient
        for value, power in zip(point, exponent):
            term *= value**power
        answer += term
    return answer


def pkey(poly):
    return tuple(sorted(poly.items()))


def kadd(left, right):
    return padd(left[0], right[0]), padd(left[1], right[1])


def kneg(value):
    return pneg(value[0]), pneg(value[1])


def ksub(left, right):
    return kadd(left, kneg(right))


def kmul(left, right):
    a, b = left
    c, d = right
    return (psub(pmul(a, c), pmul(b, d)),
            padd(padd(pmul(a, d), pmul(b, c)), pmul(b, d)))


def knorm(value):
    a, b = value
    return padd(padd(pmul(a, a), pmul(a, b)), pmul(b, b))


def cpair(a=0, b=0):
    return pconst(a), pconst(b)


def equations():
    x, y, u, v = (pvar(i) for i in range(4))
    z = (x, y)
    w = (u, v)
    one = cpair(1, 0)
    rho = cpair(0, 1)
    p2 = kmul(cpair(1, -1), z)
    q = ksub(kmul(cpair(1, 1), w), rho)
    return (
        psub(knorm(z), pconst(1)),
        psub(knorm(ksub(w, one)), pconst(1)),
        psub(knorm(ksub(w, z)), pconst(3)),
        psub(knorm(ksub(q, p2)), pconst(1)),
    )


def qkadd(x, y):
    return x[0] + y[0], x[1] + y[1]


def qkmul(x, y):
    a, b = x
    c, d = y
    return a * c - b * d, a * d + b * c + b * d


def qvadd(x, y):
    return tuple(qkadd(a, b) for a, b in zip(x, y))


def qvsub(x, y):
    return tuple((a[0] - b[0], a[1] - b[1]) for a, b in zip(x, y))


def qvscale(x, scalar):
    return tuple(qkmul(scalar, a) for a in x)


def formal_source():
    zero = ((Q(0), Q(0)),) * 3

    def basis(index):
        row = list(zero)
        row[index] = (Q(1), Q(0))
        return tuple(row)

    def combination(*terms):
        value = zero
        for scalar, vector in terms:
            value = qvadd(value, qvscale(vector, scalar))
        return value

    one, z, w = (basis(i) for i in range(3))
    rho = (Q(0), Q(1))
    rhobar = (Q(1), Q(-1))
    alpha = (Q(1, 3), Q(1, 3))
    one_minus_alpha = (Q(2, 3), Q(-1, 3))
    p3 = combination(((Q(0), Q(-1)), one),
                     ((Q(1), Q(1)), w))
    return (
        zero, one, z, w, qvscale(z, rhobar), p3,
        combination((one_minus_alpha, z), (alpha, w)),
        combination((alpha, z), (one_minus_alpha, w)),
        combination((rhobar, w), (rho, p3)),
    )


def closure_graph(completed_round=8):
    source = formal_source()
    signatures = {
        qvscale(qvsub(source[b], source[a]), root)
        for a, b in SOURCE_EDGES for root in ROOTS
    }
    points = set(source)
    rows = []
    target = None
    next_graph = None
    for round_index in range(completed_round + 2):
        ordered = sorted(points)
        edges = [
            (left, right)
            for right in range(len(ordered))
            for left in range(right)
            if qvsub(ordered[right], ordered[left]) in signatures
        ]
        rows.append((len(ordered), len(edges)))
        if round_index == completed_round:
            target = ordered, edges
        if round_index == completed_round + 1:
            next_graph = ordered, edges
            break
        enlarged = set(points)
        for left, right in edges:
            delta = qvsub(ordered[right], ordered[left])
            enlarged.add(qvadd(ordered[left], qvscale(delta, ROOTS[1])))
            enlarged.add(qvadd(ordered[left], qvscale(delta, ROOTS[5])))
        points = enlarged
    need(target is not None and next_graph is not None, "target generation")
    return (target[0], target[1], next_graph[0], next_graph[1],
            tuple(rows), source, signatures)


def point_polynomial(formal):
    bases = (cpair(1, 0), (pvar(0), pvar(1)), (pvar(2), pvar(3)))
    answer = cpair(0, 0)
    for coefficient, base in zip(formal, bases):
        answer = kadd(answer, kmul((pconst(coefficient[0]),
                                   pconst(coefficient[1])), base))
    return answer


def interval_multiply(left, right):
    products = [a * b for a in left for b in right]
    return min(products), max(products)


def interval_add(left, right):
    return left[0] + right[0], left[1] + right[1]


def norm_interval(a, ea, b, eb):
    ia = (a - ea, a + ea)
    ib = (b - eb, b + eb)
    return interval_add(interval_add(interval_multiply(ia, ia),
                                     interval_multiply(ia, ib)),
                        interval_multiply(ib, ib))


def proper(word, vertex_count, edges, colours=4):
    return (len(word) == vertex_count
            and set(word) <= set(map(str, range(colours)))
            and all(word[a] != word[b] for a, b in edges))


def colourable(vertex_count, edges, colours):
    adjacency = [set() for _ in range(vertex_count)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    assignment = [-1] * vertex_count
    assignment[0] = 0
    nodes = 0

    def visit(left):
        nonlocal nodes
        nodes += 1
        if not left:
            return True
        vertex = max(left, key=lambda v: (
            len({assignment[w] for w in adjacency[v] if assignment[w] >= 0}),
            len(adjacency[v]), -v))
        forbidden = {assignment[w] for w in adjacency[vertex]
                     if assignment[w] >= 0}
        for colour in range(colours):
            if colour not in forbidden:
                assignment[vertex] = colour
                if visit(left - {vertex}):
                    return True
        assignment[vertex] = -1
        return False

    return visit(set(range(1, vertex_count))), nodes


def stream_formal_points(points):
    return "".join(
        f"{index}:" + ";".join(
            f"{a.numerator}/{a.denominator},{b.numerator}/{b.denominator}"
            for a, b in point) + "\n"
        for index, point in enumerate(points)
    )


def physical_audit(points, declared_edges, midpoint, radius):
    """Exclude every collision and undeclared unit pair by rational intervals."""
    point_polynomials = [point_polynomial(point) for point in points]
    midpoint_points = [tuple(peval(coordinate, midpoint) for coordinate in point)
                       for point in point_polynomials]
    sensitivity = [
        tuple(radius * sum(abs(peval(pdiff(coordinate, variable), midpoint))
                           for variable in range(4))
              for coordinate in point)
        for point in point_polynomials
    ]
    edge_set = set(declared_edges)
    separation_lower = None
    nonedge_unit_gap_lower = None
    pair_checks = 0
    for right in range(len(points)):
        for left in range(right):
            pair_checks += 1
            a = midpoint_points[right][0] - midpoint_points[left][0]
            b = midpoint_points[right][1] - midpoint_points[left][1]
            ea = sensitivity[right][0] + sensitivity[left][0]
            eb = sensitivity[right][1] + sensitivity[left][1]
            lower, upper = norm_interval(a, ea, b, eb)
            need(lower > 0, f"unresolved collision {(left, right)}")
            separation_lower = lower if separation_lower is None else min(
                separation_lower, lower)
            if (left, right) in edge_set:
                need(lower <= 1 <= upper, f"edge interval {(left, right)}")
            else:
                need(upper < 1 or lower > 1,
                     f"unresolved unit pair {(left, right)}")
                gap = min(abs(lower - 1), abs(upper - 1))
                nonedge_unit_gap_lower = gap if nonedge_unit_gap_lower is None else min(
                    nonedge_unit_gap_lower, gap)
    return pair_checks, separation_lower, nonedge_unit_gap_lower


def verify(certificate_path=CERTIFICATE, check_expected=True):
    certificate_path = Path(certificate_path)
    certificate = json.loads(certificate_path.read_text())
    need(certificate.get("schema") ==
         "ud93-maximal-capped-equilateral-closure-v1", "certificate schema")
    early_word = certificate.get("four_colour_word")
    need(type(early_word) is str and len(early_word) == 432
         and set(early_word) <= set("0123"), "four-colour word syntax")
    provenance = certificate.get("provenance", {})
    need(provenance.get("commit") ==
         "218097c9971db2b60ab94a0b8dae20d76741cc43", "source commit")
    h = certificate["midpoint_denominator"]
    d = certificate["inverse_denominator"]
    radius_denominator = certificate["radius_denominator"]
    need(all(type(value) is int and value > 0
             for value in (h, d, radius_denominator)), "denominators")
    midpoint_numerators = certificate["midpoint_numerators"]
    inverse_numerators = certificate["inverse_numerators"]
    need(len(midpoint_numerators) == 4
         and all(type(value) is int for value in midpoint_numerators),
         "midpoint")
    need(len(inverse_numerators) == 4
         and all(len(row) == 4 for row in inverse_numerators)
         and all(type(value) is int for row in inverse_numerators for value in row),
         "inverse")
    midpoint = tuple(Q(value, h) for value in midpoint_numerators)
    inverse = [[Q(value, d) for value in row] for row in inverse_numerators]
    radius = Q(1, radius_denominator)
    system = equations()
    jacobian_polys = [[pdiff(row, column) for column in range(4)]
                      for row in system]
    jacobian = [[peval(value, midpoint) for value in row]
                for row in jacobian_polys]
    residual = [peval(row, midpoint) for row in system]
    defect = [[Q(i == j) - sum(inverse[i][k] * jacobian[k][j]
                                for k in range(4))
               for j in range(4)] for i in range(4)]
    beta = max(sum(abs(value) for value in row) for row in defect)
    inverse_norm = max(sum(abs(value) for value in row) for row in inverse)
    hessian_row_bound = max(
        sum(abs(peval(pdiff(jacobian_polys[i][j], k), midpoint))
            for j in range(4) for k in range(4))
        for i in range(4)
    )
    eta = beta + inverse_norm * hessian_row_bound * radius
    residual_image = max(abs(sum(inverse[i][k] * residual[k]
                                     for k in range(4)))
                         for i in range(4))
    displacement = residual_image + eta * radius
    need(beta < 1 and eta < 1 and displacement < radius,
         "root contraction")

    points, edges, next_points, next_edges, rows, source, signatures = closure_graph(8)
    need(rows == EXPECTED_ROWS, "round census")
    need(certificate["completed_round"] == 8, "completed round")
    need(tuple(map(tuple, certificate["round_vertex_edge_counts"])) == rows,
         "certificate round census")
    need(rows[8][0] <= 508 < rows[9][0], "maximal capped round")

    # Exactly five source direction orbits occur.  Their squared norms are
    # respectively 1, 1+F0, 1+F1, 1+F2/3 and 1+F3.
    norm_polynomials = {pkey(knorm(ksub(point_polynomial(source[b]),
                                        point_polynomial(source[a]))))
                        for a, b in SOURCE_EDGES}
    targets = {
        pkey(pconst(1)), pkey(padd(pconst(1), system[0])),
        pkey(padd(pconst(1), system[1])),
        pkey(padd(pconst(1), pscale(system[2], Q(1, 3)))),
        pkey(padd(pconst(1), system[3])),
    }
    need(norm_polynomials == targets and len(targets) == 5,
         "source unit direction proof")
    for signature in signatures:
        need(pkey(knorm(point_polynomial(signature))) in targets,
             "rotated signature norm")

    audit = physical_audit(points, edges, midpoint, radius)
    next_audit = physical_audit(next_points, next_edges, midpoint, radius)
    pair_checks = audit[0] + next_audit[0]
    separation_lower = min(audit[1], next_audit[1])
    nonedge_unit_gap_lower = min(audit[2], next_audit[2])
    edge_set = set(edges)

    word = early_word
    need(proper(word, 432, edges), "four-colour word")
    source_three, source_search_nodes = colourable(9, SOURCE_EDGES, 3)
    need(not source_three, "source unexpectedly three-colourable")
    source_positions = {point: index for index, point in enumerate(points)}
    need(all(point in source_positions for point in source), "source embedding")
    need(all(tuple(sorted((source_positions[source[a]], source_positions[source[b]])))
             in edge_set for a, b in SOURCE_EDGES), "source edge embedding")

    point_stream = stream_formal_points(points)
    edge_stream = "".join(f"{a} {b}\n" for a, b in edges)
    next_point_stream = stream_formal_points(next_points)
    next_edge_stream = "".join(f"{a} {b}\n" for a, b in next_edges)
    need(beta < Q(1, 10**64), "reported beta bound")
    need(eta < Q(1, 10**33), "reported eta bound")
    need(displacement < Q(1, 10**68), "reported displacement bound")
    need(separation_lower > Q(1, 10000), "reported separation bound")
    need(nonedge_unit_gap_lower > Q(1, 1000), "reported nonedge bound")
    summary = {
        "status": "EXACT MAXIMAL CAPPED UD9-3 EQUILATERAL CLOSURE VERIFIED",
        "scope": "the displayed rigid UD9-3 source and complete closure rounds 0 through 9",
        "completed_round": 8,
        "vertices": 432,
        "complete_unit_edges": 1134,
        "chromatic_number": 4,
        "proper_four_colouring": True,
        "embedded_source_vertices": 9,
        "embedded_source_edges": 15,
        "source_chromatic_number": 4,
        "source_three_colour_search_nodes": source_search_nodes,
        "next_complete_round_vertices": 533,
        "next_complete_round_edges": 1415,
        "formal_point_pair_checks": pair_checks,
        "source_direction_orbits": 5,
        "root_radius": str(radius),
        "contraction_beta_upper": "1/10^64",
        "contraction_eta_upper": "1/10^33",
        "self_map_displacement_upper": "1/10^68",
        "squared_separation_lower": "1/10000",
        "nonedge_squared_unit_gap_lower": "1/1000",
        "point_stream_sha256": hashlib.sha256(point_stream.encode()).hexdigest(),
        "edge_stream_sha256": hashlib.sha256(edge_stream.encode()).hexdigest(),
        "next_point_stream_sha256": hashlib.sha256(
            next_point_stream.encode()).hexdigest(),
        "next_edge_stream_sha256": hashlib.sha256(
            next_edge_stream.encode()).hexdigest(),
        "certificate_sha256": hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
        "record_candidate": False,
    }
    if check_expected:
        need(summary == json.loads(EXPECTED.read_text()), "expected summary")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path, default=CERTIFICATE)
    parser.add_argument("--no-expected", action="store_true")
    args = parser.parse_args()
    print(json.dumps(verify(args.certificate, not args.no_expected),
                     indent=2, sort_keys=True))
