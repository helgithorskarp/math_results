#!/usr/bin/env python3
"""Verify the weighted mixed-orbit quotient/physical-support gap.

The finite quotient is abstract.  The physical graph is reconstructed from
exact coordinates in Q(sqrt(13), i*sqrt(3)).  This checker never infers a
chromatic lower bound from a solver answer: its only lower bound on the
physical graph is the displayed unit triangle.  The optional emitted CNF is
the input whose transient DRAT refutation certifies the auxiliary quotient's
non-five-colourability.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ZERO = (F(0),) * 4
ONE = (F(1), F(0), F(0), F(0))
EXPECTED = {
    "quotient_vertices": 256,
    "quotient_directions": 21,
    "quotient_edges": 2688,
    "quotient_five_cnf_variables": 1280,
    "quotient_five_cnf_clauses": 16259,
    "quotient_five_cnf_sha256": "c5b0faf45916cef4f2e65b025c93d16f4b27bef696da814df56e23b09f3b8525",
    "one_mixed_directions": 17,
    "one_mixed_edges": 2176,
    "physical_directions": 24,
    "physical_raw_addresses": 576,
    "physical_points": 289,
    "physical_edges": 1032,
    "physical_generator_edges": 1032,
    "physical_incidental_edges": 0,
    "physical_point_sha256": "764ab9a0e1de2441d4028c47c678b47a0a66852b4c2d5aa1c41541451689224f",
    "physical_edge_sha256": "2c90fad7388ce64a4e7f3c2df6f210b479d211c9076bd6f3b8c76e838e25e659",
}

QUOTIENT_SIX_WORD = (
    "0124524343502501053454012014312524014352504301253405401353520241314042051352501454312305401231404031054252131450315405231240403143502501012452435012312502431450504301252401435212532540413153041352501431404205401231405431230552131450403105421240403131540523"
)
ONE_MIXED_FOUR_WORD = (
    "0101323210102323323201012323101032320101232310100101323210102323010123231010323201012323101032323232101023230101323210102323010123231010323201011010232301013232101023230101323223231010323201012323010132321010232301013232101010103232010123231010323201012323"
)
PHYSICAL_THREE_WORD = (
    "0101120112121200111111101112201101122011201112201220220011101121100200110121122010111220010122220011112220022222001111121111220011121212212200111102210102200001111111220000010011111122010101212110121122010111222010100000211120022220221101101200111200011212001111211211111112201010112011212"
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


# Q(sqrt(13), alpha), alpha=i*sqrt(3), in basis 1,s,alpha,s*alpha.
def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def scale(x, q):
    return tuple(q * a for a in x)


def subtract(x, y):
    return add(x, scale(y, -1))


def multiply(x, y):
    a, b, c, d = x
    A, B, C, D = y
    return (
        a * A + 13 * b * B - 3 * c * C - 39 * d * D,
        a * B + b * A - 3 * c * D - 3 * d * C,
        a * C + c * A + 13 * b * D + 13 * d * B,
        a * D + d * A + b * C + c * B,
    )


def conjugate(x):
    return x[0], x[1], -x[2], -x[3]


def norm(x):
    return multiply(x, conjugate(x))


def ring_multiply(x, y):
    """Multiply in (Z/4)[w]/(w^2+w+1)."""
    a, b = x
    c, d = y
    return ((a * c - b * d) % 4, (a * d + b * c - b * d) % 4)


def quotient_data():
    residues = list(product(range(4), repeat=2))
    unit = {
        (a, b)
        for a, b in residues
        if (a * a - a * b + b * b) % 4 == 1
    }
    require(
        unit == {(0, 1), (0, 3), (1, 0), (1, 1), (3, 0), (3, 3)},
        "unit residues",
    )
    vertical = {(2, 0), (0, 2), (2, 2)}
    base = (
        {(0, 0, a, b) for a, b in unit}
        | {(a, b, a, b) for a, b in unit}
        | {(a, b, 0, 0) for a, b in vertical}
    )
    escaped = (2, 1)
    mixed = {ring_multiply(e, escaped) for e in unit}
    require(
        mixed == {(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)},
        "mixed orbit",
    )
    full = base | {(a, b, a, b) for a, b in mixed}
    one_mixed = base | {
        (2, 1, 2, 1),
        (2, 3, 2, 3),
    }
    return unit, vertical, mixed, base, full, one_mixed


def cayley_edges(directions):
    labels = list(product(range(4), repeat=4))
    index = {z: i for i, z in enumerate(labels)}
    edges = set()
    for i, z in enumerate(labels):
        for direction in directions:
            target = tuple((a + b) % 4 for a, b in zip(z, direction))
            j = index[target]
            require(i != j, "loop in quotient")
            edges.add(tuple(sorted((i, j))))
    return labels, sorted(edges)


def check_word(word, n, k, edges, name):
    require(
        isinstance(word, str)
        and len(word) == n
        and all(c in "0123456789" and int(c) < k for c in word),
        name + " format",
    )
    colours = tuple(map(int, word))
    require(all(colours[u] != colours[v] for u, v in edges), name + " edge")
    return colours


def quotient_five_cnf(edges):
    n, k = 256, 5
    clauses = [[k * v + c + 1 for c in range(k)] for v in range(n)]
    clauses += [
        [-k * v - c - 1, -k * v - d - 1]
        for v in range(n)
        for c in range(k)
        for d in range(c + 1, k)
    ]
    clauses += [
        [-k * u - c - 1, -k * v - c - 1]
        for u, v in edges
        for c in range(k)
    ]
    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    triangle = next(
        (u, v, min(adjacency[u] & adjacency[v]))
        for u, v in edges
        if adjacency[u] & adjacency[v]
    )
    require(triangle == (0, 1, 5), "quotient triangle")
    clauses += [[k * triangle[c] + c + 1] for c in range(3)]
    body = f"p cnf {n*k} {len(clauses)}\n" + "".join(
        " ".join(map(str, clause)) + " 0\n" for clause in clauses
    )
    return body.encode(), triangle


def point_key(p):
    return tuple((q.numerator, q.denominator) for q in p)


def stream_sha(rows):
    digest = sha256()
    for row in rows:
        digest.update((" ".join(map(str, row)) + "\n").encode())
    return digest.hexdigest()


def physical_data():
    alpha = (F(0), F(0), F(1), F(0))
    rho = (F(1, 2), F(0), F(1, 2), F(0))
    phases = [
        ONE,
        (F(5, 8), F(0), F(0), F(1, 8)),
        (F(0), F(1, 4), F(1, 4), F(0)),
        (F(0), F(-1, 5), F(2, 5), F(0)),
    ]
    require(norm(alpha) == (F(3), F(0), F(0), F(0)), "alpha norm")
    require(norm(rho) == ONE and all(norm(z) == ONE for z in phases), "phase norm")

    # Definition-level representatives from W(a,p)=(1-u)a+u*p.
    u = phases[1]
    v = scale(alpha, F(2, 3))
    d = scale(alpha, F(1, 15))
    r = scale(alpha, F(3, 5))
    require(add(multiply(subtract(ONE, u), v), multiply(u, ZERO)) == phases[2], "vertical representative")
    require(add(multiply(subtract(ONE, u), d), multiply(u, r)) == phases[3], "mixed representative")

    directions = []
    for phase in phases:
        current = phase
        for _ in range(6):
            directions.append(current)
            current = multiply(current, rho)
        require(current == phase, "sixfold orbit")
    require(len(set(directions)) == 24, "direction collision")

    raw = [add(a, b) for a in directions for b in directions]
    points = sorted(set(raw), key=point_key)
    index = {p: i for i, p in enumerate(points)}
    multiplicities = Counter(index[p] for p in raw)
    edges = [
        (i, j)
        for i, j in combinations(range(len(points)), 2)
        if norm(subtract(points[i], points[j])) == ONE
    ]
    generator_edges = {
        tuple(sorted((index[p], index[add(p, direction)])))
        for p in points
        for direction in directions
        if add(p, direction) in index
    }
    require(generator_edges <= set(edges), "false generator edge")
    return phases, directions, points, edges, multiplicities, generator_edges


def run(emit_cnf=None):
    unit, vertical, mixed, base, full, one_mixed = quotient_data()
    labels, quotient_edges = cayley_edges(full)
    require(len(full) == EXPECTED["quotient_directions"], "quotient direction count")
    require(len(quotient_edges) == EXPECTED["quotient_edges"], "quotient edge count")
    check_word(QUOTIENT_SIX_WORD, len(labels), 6, quotient_edges, "quotient six-colouring")

    _, one_edges = cayley_edges(one_mixed)
    require(len(one_mixed) == EXPECTED["one_mixed_directions"], "one-mixed direction count")
    require(len(one_edges) == EXPECTED["one_mixed_edges"], "one-mixed edge count")
    check_word(ONE_MIXED_FOUR_WORD, len(labels), 4, one_edges, "one-mixed four-colouring")

    cnf, quotient_triangle = quotient_five_cnf(quotient_edges)
    require(len(cnf.splitlines()) - 1 == EXPECTED["quotient_five_cnf_clauses"], "CNF clauses")
    require(sha256(cnf).hexdigest() == EXPECTED["quotient_five_cnf_sha256"], "CNF hash")
    if emit_cnf is not None:
        Path(emit_cnf).write_bytes(cnf)

    phases, directions, points, edges, multiplicities, generator_edges = physical_data()
    require(len(points) == EXPECTED["physical_points"], "physical point count")
    require(len(edges) == EXPECTED["physical_edges"], "physical edge count")
    require(len(generator_edges) == EXPECTED["physical_generator_edges"], "generator edge count")
    require(set(edges) == generator_edges, "incidental physical unit contact")
    require(Counter(multiplicities.values()) == {1: 24, 2: 264, 24: 1}, "address multiplicities")
    point_hash = stream_sha(
        tuple(q for x in p for q in (x.numerator, x.denominator))
        for p in points
    )
    edge_hash = stream_sha(edges)
    require(point_hash == EXPECTED["physical_point_sha256"], "physical point hash")
    require(edge_hash == EXPECTED["physical_edge_sha256"], "physical edge hash")
    check_word(PHYSICAL_THREE_WORD, len(points), 3, edges, "physical three-colouring")
    adjacency = [set() for _ in points]
    degrees = [0] * len(points)
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
        degrees[u] += 1
        degrees[v] += 1
    triangle = next(
        (u, v, min(adjacency[u] & adjacency[v]))
        for u, v in edges
        if adjacency[u] & adjacency[v]
    )
    require(triangle == (0, 1, 62), "physical triangle")
    degree_histogram = dict(sorted(Counter(degrees).items()))
    require(degree_histogram == {3: 24, 4: 24, 6: 216, 24: 25}, "physical degrees")

    result = dict(EXPECTED)
    result.update(
        {
            "quotient_unit_residues": len(unit),
            "quotient_vertical_residues": len(vertical),
            "quotient_mixed_orbit": len(mixed),
            "quotient_triangle": list(quotient_triangle),
            "quotient_six_colouring_checked": True,
            "one_mixed_four_colouring_checked": True,
            "physical_address_multiplicity_histogram": {
                str(k): v for k, v in sorted(Counter(multiplicities.values()).items())
            },
            "physical_degree_histogram": {
                str(k): v for k, v in degree_histogram.items()
            },
            "physical_triangle": list(triangle),
            "physical_three_colouring_checked": True,
            "physical_chromatic_number": 3,
            "record_candidate": False,
        }
    )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-cnf", help="write the deterministic five-colour quotient CNF")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    answer = run(args.emit_cnf)
    if args.check_expected:
        expected_path = Path(__file__).with_name("EXPECTED.json")
        require(answer == json.loads(expected_path.read_text()), "EXPECTED.json mismatch")
    print(json.dumps(answer, indent=2, sort_keys=True))
