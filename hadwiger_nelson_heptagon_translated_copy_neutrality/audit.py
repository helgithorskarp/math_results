#!/usr/bin/env python3
"""Independent tensor-basis audit of the translated-heptagon interaction."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path


ZERO = (0,) * 12
ONE = (1,) + (0,) * 11
Z = (0, 1) + (0,) * 10
W = (0,) * 6 + (1,) + (0,) * 5


def need(ok, message):
    if not ok:
        raise ValueError(message)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(a, c):
    return tuple(c * x for x in a)


def mul(a, b):
    # Tensor basis z^i*w^j, 0<=i<6, 0<=j<2; z^7=1,
    # 1+z+...+z^6=0, and w^2=w-1.
    values = [0] * 14
    for i, x in enumerate(a):
        if not x:
            continue
        for j, y in enumerate(b):
            if not y:
                continue
            z_degree = (i % 6 + j % 6) % 7
            w_degree = i // 6 + j // 6
            coefficient = x * y
            if w_degree == 2:
                values[z_degree] -= coefficient
                values[7 + z_degree] += coefficient
            else:
                values[7 * w_degree + z_degree] += coefficient
    return tuple(values[7 * j + i] - values[7 * j + 6]
                 for j in range(2) for i in range(6))


def power(a, exponent):
    answer = ONE
    for _ in range(exponent):
        answer = mul(answer, a)
    return answer


ZPOW = tuple(power(Z, i) for i in range(7))
CONJUGATE_BASIS = tuple(
    mul(ZPOW[-i % 7], ONE if j == 0 else sub(ONE, W))
    for j in range(2) for i in range(6)
)


def conjugate(a):
    answer = ZERO
    for coefficient, basis_value in zip(a, CONJUGATE_BASIS):
        answer = add(answer, scale(basis_value, coefficient))
    return answer


def norm(a):
    return mul(a, conjugate(a))


def inverse_times_seven(x):
    # For primitive seventh-root x:
    # (x-x^-1)*x*sum(k*x^(2k), k=0..6)=7.
    answer = ZERO
    for k in range(7):
        answer = add(answer, scale(power(x, 2 * k), k))
    answer = mul(x, answer)
    need(mul(sub(x, conjugate(x)), answer) == scale(ONE, 7), "inverse identity")
    return answer


def seed_scaled_by_seven():
    p = inverse_times_seven(ZPOW[4])
    q = scale(mul(conjugate(W), inverse_times_seven(Z)), -1)
    r = scale(mul(W, inverse_times_seven(ZPOW[2])), -1)
    return tuple(mul(a, ZPOW[j]) for a in (p, q, r) for j in range(7))


def build_graph():
    seed = seed_scaled_by_seven()
    moved = tuple(add(seed[0], mul(ZPOW[6], sub(point, seed[0]))) for point in seed)
    addresses = seed + moved
    points = []
    groups = []
    for address, point in enumerate(addresses):
        if point in points:
            index = points.index(point)
        else:
            index = len(points)
            points.append(point)
            groups.append([])
        groups[index].append(address)
    classes = tuple(map(tuple, groups))
    class_of = {address: index for index, group in enumerate(classes) for address in group}
    edges = tuple((i, j) for i, j in combinations(range(len(points)), 2)
                  if norm(sub(points[i], points[j])) == scale(ONE, 49))
    fixed = tuple(class_of[i] for i in range(21))
    moved_labels = tuple(class_of[21 + i] for i in range(21))
    return seed, classes, tuple(points), edges, fixed, moved_labels


def adjacency(order, edges):
    answer = [set() for _ in range(order)]
    for i, j in edges:
        answer[i].add(j)
        answer[j].add(i)
    return answer


def patterns_in_label_order(seed_edges):
    graph = adjacency(21, seed_edges)
    colours = [-1] * 21
    colours[0], colours[7], colours[14] = 0, 1, 2

    def visit(vertex):
        while vertex < 21 and colours[vertex] != -1:
            vertex += 1
        if vertex == 21:
            yield tuple(colours)
            return
        for colour in range(4):
            if all(colours[w] != colour for w in graph[vertex]):
                colours[vertex] = colour
                yield from visit(vertex + 1)
        colours[vertex] = -1

    yield from visit(0)


def extend_label_order(order, edges, graph, terminals=(), pattern=()):
    colours = [-1] * order
    for vertex, colour in zip(terminals, pattern):
        if colours[vertex] not in (-1, colour):
            return None
        colours[vertex] = colour
    if any(colours[i] == colours[j] != -1 for i, j in edges):
        return None

    def search(vertex):
        while vertex < order and colours[vertex] != -1:
            vertex += 1
        if vertex == order:
            return True
        used = {colours[w] for w in graph[vertex] if colours[w] != -1}
        for colour in range(4):
            if colour not in used:
                colours[vertex] = colour
                if search(vertex + 1):
                    return True
        colours[vertex] = -1
        return False

    if not search(0):
        return None
    answer = tuple(colours)
    need(all(answer[i] != answer[j] for i, j in edges), "improper audit word")
    return answer


def audit():
    seed, classes, points, edges, fixed, moved = build_graph()
    need(len(points) == 41 and len(edges) == 105, "geometry dimensions")
    need([group for group in classes if len(group) > 1] == [(0, 21)], "collision")
    seed_edges = tuple((i, j) for i, j in combinations(range(21), 2)
                       if norm(sub(seed[i], seed[j])) == scale(ONE, 49))
    need(len(seed_edges) == 42, "seed edges")
    graph = adjacency(len(points), edges)
    projection_hashes = {}
    pattern_count = None
    for name, terminals in (("fixed", fixed), ("moved", moved)):
        count = 0
        digest = hashlib.sha256()
        for pattern in patterns_in_label_order(seed_edges):
            count += 1
            word = extend_label_order(len(points), edges, graph, terminals, pattern)
            need(word is not None, f"audit {name} projection restriction")
            need(tuple(word[v] for v in terminals) == pattern,
                 f"audit {name} terminal mismatch")
            digest.update(bytes(word))
        need(count == 327_180, f"audit {name} pattern count")
        pattern_count = count if pattern_count is None else pattern_count
        need(pattern_count == count, "audit component counts disagree")
        projection_hashes[name] = digest.hexdigest()
    pair_counts = Counter()
    edge_set = set(edges)
    pair_digest = hashlib.sha256()
    for i, j in combinations(range(len(points)), 2):
        if (i, j) in edge_set:
            pair_counts["unit_forced_different"] += 1
            continue
        equal = extend_label_order(len(points), edges, graph, (i, j), (0, 0))
        different = extend_label_order(len(points), edges, graph, (i, j), (0, 1))
        need(equal is not None and different is not None, "audit pair restriction")
        pair_counts["nonunit_both_states"] += 1
        pair_digest.update(bytes(equal) + bytes(different))
    graph_digest = hashlib.sha256((json.dumps({
        "classes": classes,
        "edges": edges,
    }, separators=(",", ":")) + "\n").encode()).hexdigest()
    return {
        "verified": True,
        "vertices": len(points),
        "edges": len(edges),
        "normalized_component_patterns_each": pattern_count,
        "component_projection_queries": 2 * pattern_count,
        "pair_relation_counts": dict(sorted(pair_counts.items())),
        "graph_sha256": graph_digest,
        "label_order_extension_stream_sha256": projection_hashes,
        "label_order_pair_stream_sha256": pair_digest.hexdigest(),
        "both_complete_projections_surjective": True,
        "complete_nonedge_pair_relation_neutral": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.check_expected:
        expected = json.loads(Path(__file__).with_name("AUDIT_EXPECTED.json").read_text())
        need(json.loads(json.dumps(result)) == expected, "AUDIT_EXPECTED.json mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
