#!/usr/bin/env python3
"""Independent exact checker using nested quadratic-pair arithmetic."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_moser_all_terminal_contacts/certificate.json"
ONE = ((144, 0), (0, 0))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def qadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def qsub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def qmul(a, b):
    return (a[0] * b[0] + 3 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def kadd(a, b):
    return (qadd(a[0], b[0]), qadd(a[1], b[1]))


def ksub(a, b):
    return (qsub(a[0], b[0]), qsub(a[1], b[1]))


def kmul(a, b):
    return (
        qadd(qmul(a[0], b[0]), tuple(11 * x for x in qmul(a[1], b[1]))),
        qadd(qmul(a[0], b[1]), qmul(a[1], b[0])),
    )


def convert(value):
    return ((value[0], value[1]), (value[2], value[3]))


def flatten(value):
    return value[0] + value[1]


def squared_distance(a, b):
    x = ksub(a[0], b[0])
    y = ksub(a[1], b[1])
    return kadd(kmul(x, x), kmul(y, y))


def edges(points):
    return tuple(
        (a, b) for a, b in combinations(range(len(points)), 2)
        if squared_distance(points[a], points[b]) == ONE
    )


def reflection_candidates(points):
    graph = edges(points)
    neighbors = [[] for _ in points]
    for a, b in graph:
        neighbors[a].append(b)
        neighbors[b].append(a)
    old = set(points)
    candidates = set()
    routes = 0
    for centre, ns in enumerate(neighbors):
        for a, b in combinations(ns, 2):
            routes += 1
            point = (
                ksub(kadd(points[a][0], points[b][0]), points[centre][0]),
                ksub(kadd(points[a][1], points[b][1]), points[centre][1]),
            )
            # Check the two route contacts directly.
            need(squared_distance(point, points[a]) == ONE, "first route contact failed")
            need(squared_distance(point, points[b]) == ONE, "second route contact failed")
            if point not in old:
                candidates.add(point)
    return graph, candidates, routes


def f4(points):
    graph, candidates, routes = reflection_candidates(points)
    old_degrees = {
        point: sum(squared_distance(point, old) == ONE for old in points)
        for point in candidates
    }
    kept = tuple(sorted(point for point in candidates if old_degrees[point] >= 4))
    output = tuple(points) + kept
    return output, {
        "input_points": len(points),
        "input_edges": len(graph),
        "unit_two_path_routes": routes,
        "distinct_new_candidates": len(candidates),
        "old_degree_histogram": {
            str(k): v for k, v in sorted(Counter(old_degrees.values()).items())
        },
        "kept_points": len(kept),
        "output_points": len(output),
    }


def full_closure(points):
    _, candidates, _ = reflection_candidates(points)
    return tuple(points) + tuple(sorted(candidates))


def accepted_closure(points):
    """Independently reproduce the target source's route-order closure."""
    graph = edges(points)
    neighbors = [[] for _ in points]
    for a, b in graph:
        neighbors[a].append(b)
        neighbors[b].append(a)
    output = list(points)
    index = {point: i for i, point in enumerate(output)}
    for centre, ns in enumerate(neighbors):
        for a, b in combinations(ns, 2):
            point = (
                ksub(kadd(points[a][0], points[b][0]), points[centre][0]),
                ksub(kadd(points[a][1], points[b][1]), points[centre][1]),
            )
            need(squared_distance(point, points[a]) == ONE, "accepted first route contact failed")
            need(squared_distance(point, points[b]) == ONE, "accepted second route contact failed")
            if point not in index:
                index[point] = len(output)
                output.append(point)
    return tuple(output)


def sha_rows(rows):
    text = "".join(",".join(map(str, row)) + "\n" for row in rows)
    return hashlib.sha256(text.encode()).hexdigest()


def point_hash(points):
    return sha_rows([flatten(p[0]) + flatten(p[1]) for p in points])


def proper(word, vertex_count, graph, colors=4):
    need(type(word) is str and len(word) == vertex_count, "wrong word length")
    need(set(word) <= set("0123456789"[:colors]), "colour outside domain")
    need(all(word[a] != word[b] for a, b in graph), "monochromatic edge")


def cut_structure(vertex_count, graph):
    adj = [set() for _ in range(vertex_count)]
    for a, b in graph:
        adj[a].add(b)
        adj[b].add(a)
    discovered = [-1] * vertex_count
    low = [0] * vertex_count
    parent = [-1] * vertex_count
    clock = 0
    articulations = set()
    bridges = set()

    def visit(vertex):
        nonlocal clock
        discovered[vertex] = low[vertex] = clock
        clock += 1
        children = 0
        for neighbor in adj[vertex]:
            if discovered[neighbor] < 0:
                parent[neighbor] = vertex
                children += 1
                visit(neighbor)
                low[vertex] = min(low[vertex], low[neighbor])
                if parent[vertex] < 0 and children > 1:
                    articulations.add(vertex)
                if parent[vertex] >= 0 and low[neighbor] >= discovered[vertex]:
                    articulations.add(vertex)
                if low[neighbor] > discovered[vertex]:
                    bridges.add(tuple(sorted((vertex, neighbor))))
            elif neighbor != parent[vertex]:
                low[vertex] = min(low[vertex], discovered[neighbor])

    components = 0
    for vertex in range(vertex_count):
        if discovered[vertex] < 0:
            components += 1
            visit(vertex)
    degrees = Counter(len(a) for a in adj)
    return {
        "components": components,
        "articulation_vertices": len(articulations),
        "bridges": len(bridges),
        "degree_histogram": {str(k): v for k, v in sorted(degrees.items())},
    }


def audit(certificate):
    need(certificate["schema"] == "hn-moser-mixeddepth-f4-stop-v1", "wrong schema")
    source_bytes = SOURCE.read_bytes()
    need(hashlib.sha256(source_bytes).hexdigest() == certificate["source_certificate_sha256"], "source hash mismatch")
    source = json.loads(source_bytes)
    need(certificate["scale"] == source["scale"] == 12, "wrong scale")
    need(certificate["basis"] == source["basis"] == ["1", "sqrt3", "sqrt11", "sqrt33"], "wrong basis")
    need(certificate["operator"] == "A0=S1; A1=F4(A0); A2=F4(A1)", "wrong operator")
    need(certificate["threshold"] == 4, "wrong threshold")

    s0 = tuple((convert(x), convert(y)) for x, y in source["C"])
    a0 = accepted_closure(s0)
    a1, first = f4(a0)
    a2, second = f4(a1)
    full_s2 = accepted_closure(a0)
    need(len(a2) <= 508, "point cap failed")
    need(first == certificate["first_step"], "first selective round differs")
    need(second == certificate["second_step"], "second selective round differs")

    graphs = [edges(support) for support in (a0, a1, a2)]
    summaries = []
    for name, support, graph in zip(("A0", "A1", "A2"), (a0, a1, a2), graphs):
        summaries.append({
            "name": name,
            "points": len(support),
            "edges": len(graph),
            "point_sha256": point_hash(support),
            "edge_sha256": sha_rows(graph),
        })
    need(summaries == certificate["supports"], "support census/hash mismatch")
    need([len(a0), len(a1), len(a2)] == [115, 214, 382], "unexpected support sizes")
    need([len(x) for x in graphs] == [447, 1019, 2026], "unexpected edge counts")

    intersection = len(set(a2) & set(full_s2))
    mixed = {
        "accepted_full_s2_points": len(full_s2),
        "a2_points_in_full_s2": intersection,
        "a2_points_beyond_full_s2": len(a2) - intersection,
        "full_s2_points_absent_from_a2": len(full_s2) - intersection,
    }
    need(mixed == certificate["mixed_depth_audit"], "mixed-depth audit mismatch")
    need(mixed == {
        "accepted_full_s2_points": 398,
        "a2_points_in_full_s2": 342,
        "a2_points_beyond_full_s2": 40,
        "full_s2_points_absent_from_a2": 56,
    }, "construction reduced to the accepted full round")

    structure = cut_structure(len(a2), graphs[2])
    need(structure == certificate["graph_structure"], "cut/degree structure mismatch")
    decision = certificate["source_input_decision"]
    need(decision["zero_extensions"] is False, "incorrect zero-extension verdict")
    need(decision["complete_source_relation_enumerated"] is False, "unsupported relation census")
    proper(decision["surviving_source_word"], len(a0), graphs[0])
    proper(decision["surviving_full_word"], len(a2), graphs[2])
    need(decision["surviving_full_word"][:len(a0)] == decision["surviving_source_word"], "word is not an extension")
    need(hashlib.sha256((decision["surviving_source_word"] + "\n").encode()).hexdigest() == decision["source_word_sha256"], "source-word hash mismatch")
    need(hashlib.sha256((decision["surviving_full_word"] + "\n").encode()).hexdigest() == decision["full_word_sha256"], "full-word hash mismatch")

    moser_indices = [a0.index((convert(x), convert(y))) for x, y in source["M"]]
    edge_set = set(graphs[0])
    medges = [(i, j) for i, j in combinations(range(7), 2)
              if tuple(sorted((moser_indices[i], moser_indices[j]))) in edge_set]
    proper3 = sum(all(word[a] != word[b] for a, b in medges)
                  for word in product(range(3), repeat=7))
    need(certificate["moser_subgraph"] == {
        "indices_in_a0": moser_indices,
        "edges": len(medges),
        "proper_named_three_colorings": proper3,
    }, "Moser lower-bound audit mismatch")
    need(len(medges) == 11 and proper3 == 0, "Moser lower bound failed")
    need(certificate["chromatic_number"] == 4, "wrong chromatic number")
    need(certificate["record_candidate"] is False, "incorrect candidate status")
    need(certificate["status"] == "EXACT_MIXED_DEPTH_SUPPORT_HAS_SURVIVING_SOURCE_FOUR_COLOURING", "wrong status")
    return {
        "support_points": [115, 214, 382],
        "support_edges": [447, 1019, 2026],
        "cap_ok": True,
        "mixed_depth_beyond_full_s2": 40,
        "mixed_depth_missing_from_full_s2": 56,
        "complete_graph_four_word_checked": True,
        "surviving_source_input_checked": True,
        "zero_extensions": False,
        "chromatic_number": 4,
        "record_candidate": False,
        "status": "PASS",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    result = audit(certificate)
    if args.check_expected:
        need(result == json.loads((HERE / "EXPECTED.json").read_text()), "expected output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
