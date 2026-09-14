#!/usr/bin/env python3
"""Exact geometry and complete component-relation check for two H motifs."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path


PHI = (1, 1, 0, -1, -1, 0, 1, 0, -1, -1, 0, 1, 1)
ZERO = (Q(0),) * 12
ONE = (Q(1),) + ZERO[1:]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def sub(a, b):
    return add(a, neg(b))


def scale(a, c):
    return tuple(c * x for x in a)


def reduce_polynomial(values):
    values = list(values) + [Q(0)] * max(0, 12 - len(values))
    for degree in range(len(values) - 1, 11, -1):
        coefficient = values[degree]
        if coefficient:
            for index in range(12):
                values[degree - 12 + index] -= coefficient * PHI[index]
    return tuple(values[:12])


def mul(a, b):
    values = [Q(0)] * 23
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    values[i + j] += x * y
    return reduce_polynomial(values)


def power(n):
    return reduce_polynomial([Q(0)] * (n % 42) + [Q(1)])


POWERS = tuple(power(n) for n in range(42))


def conjugate(a):
    out = ZERO
    for index, coefficient in enumerate(a):
        out = add(out, scale(POWERS[-index % 42], coefficient))
    return out


def norm(a):
    return mul(a, conjugate(a))


def inverse(a):
    columns = [mul(a, POWERS[j]) for j in range(12)]
    rows = [[columns[j][i] for j in range(12)] + [Q(i == 0)]
            for i in range(12)]
    for column in range(12):
        pivot = next((row for row in range(column, 12) if rows[row][column]), None)
        need(pivot is not None, "field inverse pivot")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        leading = rows[column][column]
        rows[column] = [value / leading for value in rows[column]]
        for row in range(12):
            if row != column and rows[row][column]:
                leading = rows[row][column]
                rows[row] = [a - leading * b
                             for a, b in zip(rows[row], rows[column])]
    answer = tuple(row[-1] for row in rows)
    need(mul(a, answer) == ONE, "field inverse identity")
    return answer


def seed():
    p = inverse(sub(POWERS[24], POWERS[-24 % 42]))
    q = neg(mul(POWERS[-7 % 42], inverse(sub(POWERS[6], POWERS[-6 % 42]))))
    r = neg(mul(POWERS[7], inverse(sub(POWERS[12], POWERS[-12 % 42]))))
    return tuple(mul(a, POWERS[6 * j % 42]) for a in (p, q, r) for j in range(7))


def build_graph():
    fixed_points = seed()
    rotation = POWERS[-6 % 42]
    moved_points = tuple(add(fixed_points[0], mul(rotation, sub(point, fixed_points[0])))
                         for point in fixed_points)
    addresses = fixed_points + moved_points
    unique = []
    groups = []
    for address, point in enumerate(addresses):
        if point in unique:
            index = unique.index(point)
        else:
            index = len(unique)
            unique.append(point)
            groups.append([])
        groups[index].append(address)
    classes = tuple(map(tuple, groups))
    class_of = {address: index for index, group in enumerate(classes) for address in group}
    edges = tuple((i, j) for i, j in combinations(range(len(unique)), 2)
                  if norm(sub(unique[i], unique[j])) == ONE)
    fixed = tuple(class_of[i] for i in range(21))
    moved = tuple(class_of[21 + i] for i in range(21))
    need(len(unique) == 41 and len(edges) == 105, "unexpected union geometry")
    need([group for group in classes if len(group) > 1] == [(0, 21)],
         "unexpected collision")
    return fixed_points, classes, tuple(unique), edges, fixed, moved


def adjacency(order, edges):
    answer = [set() for _ in range(order)]
    for i, j in edges:
        answer[i].add(j)
        answer[j].add(i)
    return answer


def enumerate_patterns(seed_edges):
    graph = adjacency(21, seed_edges)
    colours = [-1] * 21
    colours[0], colours[7], colours[14] = 0, 1, 2

    def search():
        choice = None
        for vertex, colour in enumerate(colours):
            if colour != -1:
                continue
            allowed = tuple(c for c in range(4)
                            if all(colours[w] != c for w in graph[vertex]))
            if not allowed:
                return
            key = len(allowed), -len(graph[vertex]), vertex
            if choice is None or key < choice[0]:
                choice = key, vertex, allowed
        if choice is None:
            yield tuple(colours)
            return
        _, vertex, allowed = choice
        for colour in allowed:
            colours[vertex] = colour
            yield from search()
        colours[vertex] = -1

    yield from search()


def extend(order, edges, graph, terminals=(), pattern=()):
    colours = [-1] * order
    for vertex, colour in zip(terminals, pattern):
        if colours[vertex] not in (-1, colour):
            return None
        colours[vertex] = colour
    if any(colours[i] == colours[j] != -1 for i, j in edges):
        return None

    def search():
        vertex = next((v for v, colour in enumerate(colours) if colour == -1), None)
        if vertex is None:
            return True
        used = {colours[w] for w in graph[vertex] if colours[w] != -1}
        for colour in range(4):
            if colour in used:
                continue
            colours[vertex] = colour
            if search():
                return True
        colours[vertex] = -1
        return False

    if not search():
        return None
    answer = tuple(colours)
    need(all(answer[i] != answer[j] for i, j in edges), "improper search word")
    need(tuple(answer[v] for v in terminals) == tuple(pattern), "pin mismatch")
    return answer


def verify():
    points, classes, union_points, edges, fixed, moved = build_graph()
    seed_edges = tuple((i, j) for i, j in combinations(range(21), 2)
                       if norm(sub(points[i], points[j])) == ONE)
    need(len(seed_edges) == 42, "seed edge count")
    attempts = valid_three = 0
    three_word = [-1] * 21
    three_word[0], three_word[7], three_word[14] = 0, 1, 2
    for states in product(tuple(permutations(range(3))), repeat=6):
        for j, state in enumerate(states, 1):
            three_word[j], three_word[j + 7], three_word[j + 14] = state
        attempts += 1
        valid_three += all(three_word[i] != three_word[j] for i, j in seed_edges)
    need((attempts, valid_three) == (46_656, 0), "seed three-colour census")

    graph = adjacency(len(union_points), edges)
    projection_hashes = {}
    pattern_count = None
    for name, terminals in (("fixed", fixed), ("moved", moved)):
        witness_digest = hashlib.sha256()
        count = 0
        for pattern in enumerate_patterns(seed_edges):
            count += 1
            union_word = extend(len(union_points), edges, graph, terminals, pattern)
            need(union_word is not None, f"{name} projection restriction found")
            witness_digest.update(bytes(union_word))
        need(count == 327_180, f"{name} normalized pattern count")
        pattern_count = count if pattern_count is None else pattern_count
        need(pattern_count == count, "component pattern counts disagree")
        projection_hashes[name] = witness_digest.hexdigest()

    edge_set = set(edges)
    pair_states = Counter()
    pair_digest = hashlib.sha256()
    for i, j in combinations(range(len(union_points)), 2):
        if (i, j) in edge_set:
            pair_states["unit_forced_different"] += 1
            continue
        equal_word = extend(len(union_points), edges, graph, (i, j), (0, 0))
        different_word = extend(len(union_points), edges, graph, (i, j), (0, 1))
        need(equal_word is not None and different_word is not None,
             f"nonedge pair relation at {i},{j}")
        pair_states["nonunit_both_states"] += 1
        pair_digest.update(bytes(equal_word) + bytes(different_word))

    factor_edges = {
        tuple(sorted((fixed[i], fixed[j]))) for i, j in seed_edges
    } | {
        tuple(sorted((moved[i], moved[j]))) for i, j in seed_edges
    }
    need(factor_edges <= edge_set and len(factor_edges) == 84, "factor edge image")
    extra_edges = tuple(sorted(edge_set - factor_edges))
    need(len(extra_edges) == 21, "nonfactor edge count")
    graph_digest = hashlib.sha256((json.dumps({
        "classes": classes,
        "edges": edges,
    }, separators=(",", ":")) + "\n").encode()).hexdigest()
    return {
        "verified": True,
        "seed_vertices": len(points),
        "seed_edges": len(seed_edges),
        "seed_chromatic_number": 4,
        "normalized_three_colour_assignments": attempts,
        "valid_three_colourings": valid_three,
        "vertices": len(union_points),
        "edges": len(edges),
        "factor_edges": len(factor_edges),
        "nonfactor_edges": len(extra_edges),
        "normalized_component_patterns_each": pattern_count,
        "component_projection_queries": 2 * pattern_count,
        "collision_classes": [list(group) for group in classes if len(group) > 1],
        "pair_relation_counts": dict(sorted(pair_states.items())),
        "graph_sha256": graph_digest,
        "extension_witness_stream_sha256": projection_hashes,
        "pair_witness_stream_sha256": pair_digest.hexdigest(),
        "every_four_colouring_of_either_component_extends": True,
        "every_nonunit_pair_admits_both_states": True,
        "union_chromatic_number": 4,
        "record_improvement": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    summary = verify()
    if args.check_expected:
        expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
        need(json.loads(json.dumps(summary)) == expected, "EXPECTED.json mismatch")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
