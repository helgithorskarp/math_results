#!/usr/bin/env python3
"""Exact conservative-colouring proof for the Golomb/A159 connector family."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
INTERVAL_SOURCE = ROOT / "hadwiger_nelson_moser_terminal_connector" / "intervals.py"
A_SOURCE = ROOT / "hadwiger_nelson_nonmono159_214_lowden2"
EXTENSION_SOURCE = ROOT / "hadwiger_nelson_long_terminal_gluing" / "certificate.json"
DEPENDENCIES = {
    INTERVAL_SOURCE: "45a24b415df20e80341c7a1e8b91878dfc4f8c504653e083fc45a9b8bdba48cf",
    A_SOURCE / "enumerate_lowden.py": "182f752e8f0354e5a91a3fc1569d717fb8654c16b5127bc5281dfc7141da6322",
    A_SOURCE / "points159.tsv": "4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02",
    EXTENSION_SOURCE: "26206782c1937d481d06e05ed95284405a188c66c1073a48a8d30dd537b0a830",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def load_dependencies():
    for path, expected in DEPENDENCIES.items():
        require(hashlib.sha256(path.read_bytes()).hexdigest() == expected,
                f"changed dependency: {path.name}")
    return (load_module("golomb_a159_intervals", INTERVAL_SOURCE),
            load_module("golomb_a159_field", A_SOURCE / "enumerate_lowden.py"))


def verify_a159_extension(field):
    points = field.points(A_SOURCE / "points159.tsv")
    require(len(points) == 159, "wrong A159 order")

    def distance(i, j):
        dx, dy = [tuple(a - b for a, b in zip(left, right, strict=True))
                  for left, right in zip(points[i], points[j], strict=True)]
        return field.add(field.mul(dx, dx), field.mul(dy, dy))

    edges = [pair for pair in combinations(range(159), 2)
             if distance(*pair) == (144,) + (0,) * 7]
    require(len(edges) == 646, "wrong A159 edge count")
    terminals = (141, 142, 144)
    require(all(distance(*pair) == (1008,) + (0,) * 7
                for pair in combinations(terminals, 2)),
            "wrong A159 terminal geometry")
    certificate = json.loads(EXTENSION_SOURCE.read_text())["159"]
    require(tuple(certificate["terminals"]) == terminals, "wrong A159 terminals")
    rows = certificate["extensions"]
    require([row["pattern"] for row in rows] == ["001", "010", "011", "012"],
            "incomplete A159 nonmonochromatic pattern cover")
    for row in rows:
        word = row["colours"]
        require(len(word) == 159 and set(word) <= set("0123"), "bad A159 word")
        require("".join(word[i] for i in terminals) == row["pattern"],
                "wrong A159 terminal word")
        require(all(word[u] != word[v] for u, v in edges),
                "improper A159 extension")
    return {"vertices": 159, "edges": len(edges), "terminals": len(terminals),
            "canonical_nonmonochromatic_extensions": len(rows)}


def golomb_rows():
    return [
        (0, 0, 0, 0), (36, 0, 0, 0), (18, 0, 18, 0),
        (-18, 0, 18, 0), (-36, 0, 0, 0), (-18, 0, -18, 0),
        (18, 0, -18, 0), (6, 0, 0, 2), (-3, -3, 3, -1),
        (-3, 3, -3, -1),
    ]


def golomb_exact_graph():
    rows = golomb_rows()
    require(len(rows) == len(set(rows)) == 10, "bad Golomb rows")

    def squared(i, j):
        a, b, c, d = (rows[i][k] - rows[j][k] for k in range(4))
        return a * a + 33 * b * b + 3 * c * c + 99 * d * d, 2 * a * b + 6 * c * d

    edges = [pair for pair in combinations(range(10), 2)
             if squared(*pair) == (1296, 0)]
    require(len(edges) == 18, "wrong Golomb edge count")
    require(all(edge in edges for edge in ((0, 1), (0, 2), (1, 2))),
            "missing Golomb reference triangle")
    three_colourings = 0
    for tail in product(range(3), repeat=7):
        word = (0, 1, 2) + tail
        three_colourings += all(word[u] != word[v] for u, v in edges)
    require(three_colourings == 0, "Golomb graph unexpectedly three-colourable")
    return edges


def golomb_squared_coefficients(i, j):
    rows = golomb_rows()
    a, b, c, d = (rows[i][k] - rows[j][k] for k in range(4))
    return a * a + 33 * b * b + 3 * c * c + 99 * d * d, 2 * a * b + 6 * c * d


def golomb_boxes(intervals):
    Q = intervals.Q
    sqrt3, sqrt11, sqrt33 = Q(3).sqrt(), Q(11).sqrt(), Q(33).sqrt()
    return [((Q(a) + Q(b) * sqrt33) / Q(36),
             Q(c) * sqrt3 / Q(36) + Q(d) * sqrt11 / Q(12))
            for a, b, c, d in golomb_rows()]


def enumerate_boxes(intervals):
    Q, S = intervals.Q, intervals.S
    add, sub = intervals.add, intervals.sub
    scale, turn, norm, mul = intervals.scale, intervals.turn, intervals.norm, intervals.mul
    golomb = golomb_boxes(intervals)
    omega = (Q(1, 2), Q(3).sqrt() / Q(2))
    points = list(golomb)
    labels = [["G", i] for i in range(10)]
    triangles = []
    first_branches = []
    second_branches = []
    for i, j in combinations(range(10), 2):
        delta = sub(golomb[j], golomb[i])
        d2 = norm(delta)
        label = [i, j]
        midpoint = scale(add(golomb[i], golomb[j]), Q(1, 2))
        exact_d2 = golomb_squared_coefficients(i, j)
        if exact_d2 == (4 * 1296, 0):
            first_branches.append([label, "tangent"])
            centres = [(0, midpoint)]
        elif d2.lo > 4 * S:
            first_branches.append([label, "excluded_gt_2"])
            continue
        else:
            require(d2.hi < 4 * S and d2.lo > 0,
                    f"unresolved first-circle branch {label}")
            first_branches.append([label, "two"])
            offset = scale(turn(delta), (Q(4) / d2 - Q(1)).sqrt() / Q(2))
            centres = [(side, add(midpoint, scale(offset, Q(side))))
                       for side in (-1, 1)]
        for first_side, a in centres:
            for k in range(10):
                delta = sub(golomb[k], a)
                r = norm(delta)
                discriminant = Q(16) * r - r.square() - Q(36)
                full_label = [i, j, first_side, k]
                if discriminant.hi < 0:
                    second_branches.append([full_label, "absent"])
                    continue
                require(discriminant.lo > 0 and r.lo > 0,
                        f"unresolved second-circle branch {full_label}")
                second_branches.append([full_label, "two"])
                foot = add(a, scale(delta, (r + Q(6)) / (Q(2) * r)))
                offset = scale(turn(delta), discriminant.sqrt() / (Q(2) * r))
                for second_side in (-1, 1):
                    b = add(foot, scale(offset, Q(second_side)))
                    for orientation in (-1, 1):
                        rotation = (omega[0], omega[1] * Q(orientation))
                        c = add(a, mul(sub(b, a), rotation))
                        ids = list(range(len(points), len(points) + 3))
                        triangles.append(ids)
                        points.extend((a, b, c))
                        labels.extend([full_label + [second_side, orientation, t]
                                       for t in range(3)])
    return points, labels, triangles, first_branches, second_branches


def conservative_graph(intervals, points, triangles):
    I, S, norm, sub = intervals.I, intervals.S, intervals.norm, intervals.sub
    parent = list(range(len(points)))

    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    possible_collision_pairs = 0
    for i, j in combinations(range(len(points)), 2):
        if all(points[i][coordinate].meets(points[j][coordinate])
               for coordinate in (0, 1)):
            possible_collision_pairs += 1
            a, b = root(i), root(j)
            if a != b:
                parent[max(a, b)] = min(a, b)
    roots = sorted({root(i) for i in range(len(points))})
    renumber = {value: i for i, value in enumerate(roots)}
    group_of = [renumber[root(i)] for i in range(len(points))]
    groups = [[i for i, value in enumerate(group_of) if value == group]
              for group in range(len(roots))]
    hulls = []
    internal_unit_margin = None
    for members in groups:
        hull = tuple(I(min(points[i][coordinate].lo for i in members),
                       max(points[i][coordinate].hi for i in members))
                     for coordinate in (0, 1))
        hulls.append(hull)
        diameter2_upper = sum((hull[c].hi - hull[c].lo) ** 2 for c in (0, 1))
        require(diameter2_upper < S * S, "possible unit edge inside one colour group")
        margin = S * S - diameter2_upper
        internal_unit_margin = margin if internal_unit_margin is None else min(internal_unit_margin, margin)

    edges = []
    nonedge_margin = None
    for i, j in combinations(range(len(hulls)), 2):
        d2 = norm(sub(hulls[i], hulls[j]))
        if d2.lo <= S <= d2.hi:
            edges.append((i, j))
        else:
            margin = min(abs(d2.lo - S), abs(d2.hi - S))
            nonedge_margin = margin if nonedge_margin is None else min(nonedge_margin, margin)
    triples = sorted({tuple(sorted(group_of[i] for i in triangle))
                      for triangle in triangles})
    require(all(len(set(triple)) == 3 for triple in triples),
            "a certified terminal triangle collapsed")
    return {
        "groups": groups,
        "group_of": group_of,
        "hulls": hulls,
        "edges": edges,
        "triples": triples,
        "possible_collision_pairs": possible_collision_pairs,
        "internal_unit_margin": internal_unit_margin,
        "nonedge_margin": nonedge_margin,
    }


def check_word(certificate, graph):
    word = certificate.get("four_colour_word")
    require(certificate.get("schema") == 1 and type(word) is str,
            "malformed certificate")
    require(len(word) == len(graph["groups"]) and set(word) <= set("0123"),
            "malformed colour word")
    require(all(word[u] != word[v] for u, v in graph["edges"]),
            "monochromatic possible unit edge")
    require(all(len({word[i] for i in triple}) > 1 for triple in graph["triples"]),
            "monochromatic candidate terminal triangle")


def verify(certificate):
    intervals, field = load_dependencies()
    a159 = verify_a159_extension(field)
    golomb_edges = golomb_exact_graph()
    points, labels, triangles, first, second = enumerate_boxes(intervals)
    graph = conservative_graph(intervals, points, triangles)
    check_word(certificate, graph)
    group_of = graph["group_of"]
    golomb_groups = [group_of[i] for i in range(10)]
    require(len(set(golomb_groups)) == 10, "Golomb source collision")
    edge_set = set(graph["edges"])
    require(all(tuple(sorted((golomb_groups[u], golomb_groups[v]))) in edge_set
                for u, v in golomb_edges), "Golomb edge absent from supergraph")
    sizes = Counter(map(len, graph["groups"]))
    S = intervals.S
    return {
        "verified": True,
        "golomb_vertices": 10,
        "golomb_edges": len(golomb_edges),
        "golomb_chromatic_number": 4,
        "golomb_pairs": len(first),
        "secant_first_pairs": sum(row[1] == "two" for row in first),
        "tangent_first_pairs": sum(row[1] == "tangent" for row in first),
        "excluded_first_pairs": sum(row[1] == "excluded_gt_2" for row in first),
        "second_anchor_cases": len(second),
        "eligible_second_anchor_cases": sum(row[1] == "two" for row in second),
        "labelled_triangles": len(triangles),
        "labelled_points": len(points),
        "possible_collision_pairs": graph["possible_collision_pairs"],
        "possible_equality_colour_groups": len(graph["groups"]),
        "class_size_histogram": {str(k): sizes[k] for k in sorted(sizes)},
        "conservative_possible_unit_edges": len(graph["edges"]),
        "distinct_cluster_triples": len(graph["triples"]),
        "constraint_graph_sha256": digest({
            "groups": graph["groups"], "edges": graph["edges"],
            "triples": graph["triples"]}),
        "internal_squared_diameter_gap_lower": str(Fraction(graph["internal_unit_margin"], S * S)),
        "nonedge_squared_unit_gap_lower": str(Fraction(graph["nonedge_margin"], S)),
        "a159_source": a159,
        "maximum_full_A159_copies_under_508": 3,
        "raw_three_A159_plus_Golomb_bound": 487,
        "all_candidate_triangles_simultaneously_nonmonochromatic": True,
        "all_covered_full_assemblies_four_colourable": True,
        "record_candidate": False,
    }


def malformed_control(certificate):
    intervals, _ = load_dependencies()
    points, _, triangles, _, _ = enumerate_boxes(intervals)
    graph = conservative_graph(intervals, points, triangles)
    word = list(certificate["four_colour_word"])
    u, v = graph["edges"][0]
    word[v] = word[u]
    bad = {"schema": 1, "four_colour_word": "".join(word)}
    try:
        check_word(bad, graph)
    except ValueError:
        return 1
    raise RuntimeError("corrupted colouring accepted")


def main():
    certificate = json.loads((HERE / "certificate.json").read_text())
    result = verify(certificate)
    result["malformed_controls_rejected"] = malformed_control(certificate)
    expected = json.loads((HERE / "expected.json").read_text())
    require(result == expected, "expected result mismatch")
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    print("EXACT GOLOMB--A159 CONNECTOR FAMILY FOUR-COLOUR STOP VERIFIED")


if __name__ == "__main__":
    main()
