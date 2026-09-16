#!/usr/bin/env python3
"""Exact checker for the native-frame S343--EI21 mixed-source stop.

The two reviewed sources are reconstructed from their pinned public inputs.
S343 has exact multiquadratic coordinates.  EI21 is the unique real root in
the rational box certified by its contraction proof.  Rational outward
intervals exclude every collision and unit contact between their private
vertices, proving that the mixed union is a one-vertex sum at the origin.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from fractions import Fraction as Q
from itertools import product
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED = HERE / "EXPECTED.json"

S_DIR = ROOT / "hadwiger_nelson_golomb_opposed_b214_stop"
EI_DIR = ROOT / "hadwiger_nelson_ei21_contact_selfsum_fourcolour_stop"
S_VERIFY = S_DIR / "verify.py"
S_CERT = S_DIR / "certificate.json"
B214 = ROOT / "hadwiger_nelson_nonmono159_214_lowden2/points214.tsv"
EI_VERIFY = EI_DIR / "verify.py"
EI_CERT = EI_DIR / "geometry_certificate.json"

PINNED = {
    S_VERIFY: "3520b0e61bf1115c237d2c657dac06205eb194a97bd6975fa5c73847686bc00b",
    S_CERT: "3f6a4a13ead37de71ceb3cd1818d21a9036ea0273e151461fc54d9df1a8c2e19",
    B214: "97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f",
    EI_VERIFY: "d20e82ad161e66e620be78dd2a26649b399cb5119c1ef0ffda8500fc30f47efb",
    EI_CERT: "4e94704ca1f96743f1bb950393ff4fadd6377d8a33697f0debb484722d8cd162",
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_module(name, path):
    old = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        need(spec is not None and spec.loader is not None, "module spec")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.dont_write_bytecode = old


def add_interval(a, b):
    return a[0] + b[0], a[1] + b[1]


def scale_interval(c, a):
    if c >= 0:
        return c * a[0], c * a[1]
    return c * a[1], c * a[0]


def square_interval(a):
    lo, hi = a
    if lo <= 0 <= hi:
        return Q(0), max(lo * lo, hi * hi)
    x, y = lo * lo, hi * hi
    return min(x, y), max(x, y)


def squared_distance_interval(p, q):
    dx = p[0][0] - q[0][1], p[0][1] - q[0][0]
    dy = p[1][0] - q[1][1], p[1][1] - q[1][0]
    return add_interval(square_interval(dx), square_interval(dy))


def sqrt_interval(n, denominator=10**80):
    target = n * denominator * denominator
    floor = math.isqrt(target)
    need(floor * floor < target < (floor + 1) * (floor + 1),
         "unexpected rational square")
    return Q(floor, denominator), Q(floor + 1, denominator)


def radical_point_boxes(points):
    roots = {
        1: (Q(1), Q(1)),
        3: sqrt_interval(3),
        11: sqrt_interval(11),
        33: sqrt_interval(33),
    }
    radicands = (1, 3, 11, 33)

    def coordinate(coefficients):
        out = (Q(0), Q(0))
        for coefficient, radicand in zip(coefficients, radicands):
            out = add_interval(out, scale_interval(coefficient, roots[radicand]))
        return out[0] / 36, out[1] / 36

    return [(coordinate(x), coordinate(y)) for x, y in points]


def rational_point_boxes(points, radius, fixed):
    boxes = []
    for index, (x, y) in enumerate(points):
        error = Q(0) if index in fixed else radius
        boxes.append(((x - error, x + error), (y - error, y + error)))
    return boxes


def private_cross_margins(s_boxes, e_boxes):
    checks = 0
    minimum_separation = None
    minimum_unit_gap = None
    for si, sp in enumerate(s_boxes):
        for ej, ep in enumerate(e_boxes):
            lo, hi = squared_distance_interval(sp, ep)
            checks += 1
            need(lo > 0, f"unresolved private collision {(si, ej)}")
            need(not (lo <= 1 <= hi), f"unresolved private unit pair {(si, ej)}")
            gap = 1 - hi if hi < 1 else lo - 1
            need(gap > 0, "nonpositive unit gap")
            minimum_separation = lo if minimum_separation is None else min(
                minimum_separation, lo)
            minimum_unit_gap = gap if minimum_unit_gap is None else min(
                minimum_unit_gap, gap)
    return checks, minimum_separation, minimum_unit_gap


def proper(word, n, edges, colours=4):
    return (len(word) == n and set(word) <= set(map(str, range(colours)))
            and all(word[a] != word[b] for a, b in edges))


def connected(n, edges, removed=None):
    adjacency = [set() for _ in range(n)]
    for a, b in edges:
        if a == removed or b == removed:
            continue
        adjacency[a].add(b)
        adjacency[b].add(a)
    vertices = [v for v in range(n) if v != removed]
    seen = {vertices[0]}
    stack = [vertices[0]]
    while stack:
        v = stack.pop()
        for w in adjacency[v] - seen:
            seen.add(w)
            stack.append(w)
    return len(seen) == len(vertices)


def component_sizes(n, edges, removed=None):
    adjacency = [set() for _ in range(n)]
    for a, b in edges:
        if a == removed or b == removed:
            continue
        adjacency[a].add(b)
        adjacency[b].add(a)
    unseen = set(range(n))
    if removed is not None:
        unseen.remove(removed)
    sizes = []
    while unseen:
        start = min(unseen)
        seen = {start}
        stack = [start]
        while stack:
            v = stack.pop()
            for w in adjacency[v] - seen:
                seen.add(w)
                stack.append(w)
        unseen -= seen
        sizes.append(len(seen))
    return sorted(sizes, reverse=True)


def stream_hash(rows):
    return hashlib.sha256(("\n".join(rows) + "\n").encode()).hexdigest()


def verify(check_expected=True):
    for path, expected in PINNED.items():
        need(digest(path) == expected, f"dependency hash: {path.name}")

    smod = load_module("hn_s343_source", S_VERIFY)
    eimod = load_module("hn_ei21_source", EI_VERIFY)

    b_source = smod.read_parts(smod.B_SOURCE, smod.B_SHA256)
    golomb = smod.golomb()
    s_points, _ = smod.merge(
        golomb + smod.shifted_b(b_source, 0) + smod.shifted_b(b_source, 1))
    s_edges = smod.strict_edges(s_points)
    need((len(s_points), len(s_edges)) == (343, 1782), "S343 graph")
    need(s_points[0] == ((0, 0, 0, 0), (0, 0, 0, 0)), "S343 origin")
    need(all(point != s_points[0] for point in s_points[1:]), "S343 second origin")

    s_certificate = json.loads(S_CERT.read_text())
    pattern = min(s_certificate["surviving_patterns"])
    s_word = s_certificate["s343_words"][pattern]
    need(proper(s_word, 343, s_edges), "S343 positive word")

    e_points, e_radius, e_edges, _ = eimod.source_replay(EI_CERT)
    need((len(e_points), len(e_edges)) == (21, 39), "EI21 graph")
    need(e_points[0] == (Q(0), Q(0)), "EI21 origin")
    e_certificate = json.loads(EI_CERT.read_text())
    e_word = e_certificate["surviving_complete_word"]
    need(proper(e_word, 21, e_edges), "EI21 positive word")

    s_boxes = radical_point_boxes(s_points)
    e_boxes = rational_point_boxes(e_points, e_radius, set(eimod.FIXED))
    # The common origin is removed from both sides of this Cartesian product.
    cross_checks, separation, unit_gap = private_cross_margins(
        s_boxes[1:], e_boxes[1:])
    need(cross_checks == 342 * 20 == 6840, "private cross count")
    reported_margin = Q(1, 100000)
    need(separation > reported_margin and unit_gap > reported_margin,
         "reported cross margin")

    # Merge EI21 vertex zero with S343 vertex zero and append EI21 vertices 1..20.
    e_image = [0] + [342 + j for j in range(1, 21)]
    union_edges = sorted(set(s_edges) | {
        tuple(sorted((e_image[a], e_image[b]))) for a, b in e_edges
    })
    need((len(union_edges), max(max(edge) for edge in union_edges) + 1)
         == (1821, 363), "union graph")

    # Align the EI21 origin colour with the S343 origin colour.
    old0, new0 = int(e_word[0]), int(s_word[0])
    old_rest = [c for c in range(4) if c != old0]
    new_rest = [c for c in range(4) if c != new0]
    permutation = {old0: new0, **dict(zip(old_rest, new_rest))}
    remapped_e = "".join(str(permutation[int(c)]) for c in e_word)
    union_word = s_word + remapped_e[1:]
    need(proper(union_word, 363, union_edges), "union four-colouring")

    # The first ten S343 vertices are Golomb.  With its unit triangle pinned
    # to 0,1,2, all 3^7 remaining assignments fail.
    g_edges = smod.strict_edges(golomb)
    need(len(g_edges) == 18, "Golomb edge count")
    three_words = 0
    for tail in product(range(3), repeat=7):
        word = (0, 1, 2) + tail
        three_words += all(word[a] != word[b] for a, b in g_edges)
    need(three_words == 0, "Golomb unexpectedly three-colourable")

    need(connected(363, union_edges), "union disconnected")
    need(not connected(363, union_edges, removed=0), "origin is not articulation")
    components_without_origin = component_sizes(363, union_edges, removed=0)
    need(components_without_origin == [342, 20], "component orders")
    articulations = [v for v in range(363)
                     if not connected(363, union_edges, removed=v)]
    need(articulations == [0], "unexpected articulation structure")

    pair_count = 363 * 362 // 2
    need(pair_count == 343 * 342 // 2 + 21 * 20 // 2 + cross_checks,
         "all-pairs partition")
    result = {
        "status": "EXACT S343--EI21 NATIVE WEDGE FOUR-COLOUR STOP VERIFIED",
        "scope": "displayed native frames with their unique common origin",
        "vertices": 363,
        "complete_unit_edges": 1821,
        "all_physical_pairs_reconstructed": pair_count,
        "private_cross_pairs_excluded": cross_checks,
        "private_cross_collisions": 0,
        "private_cross_unit_edges": 0,
        "shared_points": 1,
        "shared_point": "origin",
        "articulation_vertices": articulations,
        "component_orders_after_origin_deletion": components_without_origin,
        "chromatic_number": 4,
        "s343_word_pattern": pattern,
        "edge_stream_sha256": stream_hash(f"{a} {b}" for a, b in union_edges),
        "four_word_sha256": hashlib.sha256(union_word.encode()).hexdigest(),
        "certified_private_cross_squared_separation_lower": str(reported_margin),
        "certified_private_cross_squared_unit_gap_lower": str(reported_margin),
        "record_candidate": False,
    }
    if check_expected:
        need(result == json.loads(EXPECTED.read_text()), "expected summary")
    return result


if __name__ == "__main__":
    print(json.dumps(verify(EXPECTED.exists()), indent=2, sort_keys=True))
