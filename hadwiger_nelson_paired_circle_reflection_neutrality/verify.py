#!/usr/bin/env python3
"""Exact verifier for one reflection round of the paired-circle witness."""

from __future__ import annotations

import copy
import hashlib
import json
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


# Basis order is 1,sqrt(3),i,i*sqrt(3).
def add(x, y):
    return tuple(a + b for a, b in zip(x, y, strict=True))


def neg(x):
    return tuple(-a for a in x)


def sub(x, y):
    return add(x, neg(y))


def mul(x, y):
    out = [F(0)] * 4
    for m, a in enumerate(x):
        for n, b in enumerate(y):
            if not a or not b:
                continue
            radical = (m & 1) + (n & 1)
            imaginary = ((m >> 1) & 1) + ((n >> 1) & 1)
            coefficient = a * b
            if radical >= 2:
                coefficient *= 3
                radical -= 2
            if imaginary >= 2:
                coefficient = -coefficient
                imaginary -= 2
            out[radical + 2 * imaginary] += coefficient
    return tuple(out)


def conj(x):
    return x[0], x[1], -x[2], -x[3]


def norm(x):
    return mul(x, conj(x))


ZERO = (F(0),) * 4
ONE = (F(1), F(0), F(0), F(0))
II = (F(0), F(0), F(1), F(0))
OMEGA = (F(1, 2), F(0), F(0), F(1, 2))
ROOTS = [ONE]
for _ in range(5):
    ROOTS.append(mul(ROOTS[-1], OMEGA))
require(mul(ROOTS[-1], OMEGA) == ONE, "sixth-root relation failed")


def encode_number(x):
    return [x.numerator, x.denominator]


def encode_point(point):
    return [[encode_number(point[0]), encode_number(point[1])],
            [encode_number(point[2]), encode_number(point[3])]]


def digest(value):
    blob = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
    return hashlib.sha256(blob).hexdigest()


def source_geometry():
    w5 = ROOTS[5]
    from_a = (OMEGA, ONE, OMEGA, ONE)
    from_b = (II, II, mul(II, w5), mul(II, w5))
    displacements = [sub(a, b) for a, b in zip(from_a, from_b, strict=True)]
    centres = (ZERO, sub(displacements[0], displacements[2]),
               displacements[0], displacements[1])
    require(sub(centres[3], centres[1]) == displacements[3], "bad centre frame")
    require(norm(sub(centres[1], centres[0])) == ONE, "first segment not unit")
    require(norm(sub(centres[3], centres[2])) == ONE, "second segment not unit")
    require(len(set(centres)) == 4, "coincident centres")

    cross = ((0, 0), (0, 1), (1, 0), (1, 1))
    intersections = []
    for (i, j), u, v in zip(cross, from_a, from_b, strict=True):
        require(u not in (v, neg(v)), "nonregular centre pair")
        first = add(centres[i], u)
        second = sub(add(centres[i], centres[2 + j]), first)
        require(first != second, "tangent centre pair")
        for point in (first, second):
            require(norm(sub(point, centres[i])) == ONE, "bad first owner")
            require(norm(sub(point, centres[2 + j])) == ONE, "bad second owner")
        intersections.append((first, second))

    directions = [set(), set()]
    for group in range(2):
        seeds = [sub(centres[2 * group + 1], centres[2 * group])]
        for (i, j), roots in zip(cross, intersections, strict=True):
            owner = centres[i if group == 0 else 2 + j]
            seeds.extend(sub(point, owner) for point in roots)
        for seed in seeds:
            directions[group].update(mul(seed, root) for root in ROOTS)
    require([len(x) for x in directions] == [12, 12], "wrong direction orbits")

    support = set()
    for label, centre in enumerate(centres):
        support.update(add(centre, direction) for direction in directions[label // 2])
    points = sorted(support)
    require(len(points) == 39, "wrong source order")
    return centres, points


def complete_edges(points):
    return [(i, j) for i, j in combinations(range(len(points)), 2)
            if norm(sub(points[i], points[j])) == ONE]


def reflection_round(points, edges):
    neighbours = [set() for _ in points]
    for u, v in edges:
        neighbours[u].add(v)
        neighbours[v].add(u)
    support = set(points)
    labelled_routes = []
    for r in range(len(points)):
        for p, q in combinations(sorted(neighbours[r]), 2):
            reflected = sub(add(points[p], points[q]), points[r])
            require(norm(sub(reflected, points[p])) == ONE, "bad reflected contact")
            require(norm(sub(reflected, points[q])) == ONE, "bad reflected contact")
            support.add(reflected)
            labelled_routes.append((p, q, r, reflected))
    closure = sorted(support)
    index = {point: i for i, point in enumerate(closure)}
    routes = [(p, q, r, index[point]) for p, q, r, point in labelled_routes]
    return closure, routes


def restricted_growth_patterns(length):
    answer = []

    def visit(word, maximum):
        if len(word) == length:
            answer.append("".join(map(str, word)))
            return
        for colour in range(min(3, maximum + 1) + 1):
            visit(word + [colour], max(maximum, colour))

    visit([0], 0)
    return answer


def check_word(word, points, edges, terminals=None, pattern=None, colours=4):
    require(type(word) is str and len(word) == len(points), "malformed colour word")
    require(set(word) <= set("0123"[:colours]), "colour outside palette")
    require(all(word[u] != word[v] for u, v in edges), "monochromatic unit edge")
    if terminals is not None:
        require("".join(word[v] for v in terminals) == pattern,
                "wrong terminal pattern")


def verify(certificate):
    require(certificate.get("schema") == 1, "wrong schema")
    centres, source = source_geometry()
    source_edges = complete_edges(source)
    require(len(source_edges) == 102, "wrong source edge count")
    require(digest([encode_point(point) for point in source]) ==
            "866e7f8c58acb891be61935663f8d77fb02818835272d0532c90d845bbf14912",
            "wrong source point identity")
    require(digest(source_edges) ==
            "797b1e2d848a30cf2467b4b22b6772ed13ee0d13bf11aefb7efa0d2fb92b8ec3",
            "wrong source edge identity")

    closure, routes = reflection_round(source, source_edges)
    closure_edges = complete_edges(closure)
    require(len(closure) == 139 and len(closure_edges) == 492,
            "wrong closure census")
    source_index = {point: i for i, point in enumerate(source)}
    closure_index = {point: i for i, point in enumerate(closure)}
    require(all(point in closure_index for point in source), "source not embedded")
    require(len(routes) == 556, "wrong route count")
    edge_set = set(closure_edges)
    for p, q, _, new in routes:
        cp, cq = closure_index[source[p]], closure_index[source[q]]
        require(tuple(sorted((cp, new))) in edge_set, "missing route edge")
        require(tuple(sorted((cq, new))) in edge_set, "missing route edge")

    terminals = [closure_index[point] for point in centres]
    bare_edges = [(i, j) for i, j in combinations(range(4), 2)
                  if norm(sub(centres[i], centres[j])) == ONE]
    require(bare_edges == [(0, 1), (2, 3)], "wrong terminal graph")
    bare_relation = [pattern for pattern in restricted_growth_patterns(4)
                     if all(pattern[u] != pattern[v] for u, v in bare_edges)]
    require(bare_relation == ["0101", "0102", "0110", "0112",
                              "0120", "0121", "0123"],
            "wrong bare relation")

    common = neg(II)
    common_index = closure_index[common]
    require(all(tuple(sorted((common_index, terminal))) in edge_set
                for terminal in terminals), "missing four-centre common neighbour")
    triangle = (common_index, terminals[0], terminals[1])
    require(all(tuple(sorted(edge)) in edge_set for edge in combinations(triangle, 2)),
            "missing unit triangle")

    relation = ["0101", "0102", "0110", "0112", "0120", "0121"]
    extensions = certificate.get("terminal_extensions")
    require(type(extensions) is dict and sorted(extensions) == relation,
            "incomplete terminal certificate")
    for pattern in relation:
        check_word(extensions[pattern], closure, closure_edges, terminals, pattern)
    # Pattern 0123 is impossible already in the source: the common neighbour
    # would be adjacent to vertices of all four colours.  The six positive
    # words show that these are the complete source and closure relations.

    three_word = certificate.get("three_colour_word")
    check_word(three_word, closure, closure_edges, colours=3)
    require(len({three_word[v] for v in triangle}) == 3,
            "lower-bound triangle not three-coloured")
    return {
        "verified": True,
        "source_points": len(source),
        "source_edges": len(source_edges),
        "source_chromatic_number": 3,
        "source_terminal_relation": relation,
        "bare_terminal_relation": bare_relation,
        "unit_two_path_routes": len(routes),
        "new_points": len(closure) - len(source),
        "closure_points": len(closure),
        "closure_edges": len(closure_edges),
        "closure_chromatic_number": 3,
        "closure_terminal_relation": relation,
        "relation_strictly_stronger": False,
        "complete_pair_checks": len(closure) * (len(closure) - 1) // 2,
        "closure_point_sha256": digest([encode_point(point) for point in closure]),
        "closure_edge_sha256": digest(closure_edges),
        "route_sha256": digest(routes),
        "within_508": True,
        "record_candidate": False,
    }


def controls(certificate):
    bad = []
    damaged = copy.deepcopy(certificate)
    damaged["three_colour_word"] = "0" * 139
    bad.append(damaged)
    damaged = copy.deepcopy(certificate)
    damaged["terminal_extensions"].pop("0121")
    bad.append(damaged)
    damaged = copy.deepcopy(certificate)
    damaged["terminal_extensions"]["0101"] = "0" * 139
    bad.append(damaged)
    rejected = 0
    for item in bad:
        try:
            verify(item)
        except (ValueError, KeyError, IndexError):
            rejected += 1
    require(rejected == len(bad), "malformed certificate accepted")
    return rejected


def main():
    certificate = json.loads((HERE / "certificate.json").read_text())
    result = verify(certificate)
    result["malformed_controls_rejected"] = controls(certificate)
    expected_path = HERE / "expected.json"
    if expected_path.exists():
        require(result == json.loads(expected_path.read_text()), "expected result mismatch")
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    print("EXACT PAIRED-CIRCLE REFLECTION RELATION NEUTRALITY VERIFIED")


if __name__ == "__main__":
    main()
