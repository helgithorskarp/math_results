#!/usr/bin/env python3
"""Exact verifier for the E457 paired-hexagon connector stop."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
RADICANDS = (3, 47)
ZERO = (F(0),) * 4
ONE = (F(1), F(0), F(0), F(0))
SQRT3 = (F(0), F(1), F(0), F(0))
SQRT47 = (F(0), F(0), F(1), F(0))
SQRT141 = (F(0), F(0), F(0), F(1))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b, strict=True))


def neg(a):
    return tuple(-x for x in a)


def sub(a, b):
    return add(a, neg(b))


def scale(a, q):
    return tuple(q * x for x in a)


def mul(a, b):
    out = [F(0)] * 4
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            factor = 1
            common = i & j
            for bit, radicand in enumerate(RADICANDS):
                if common & (1 << bit):
                    factor *= radicand
            out[i ^ j] += factor * x * y
    return tuple(out)


def point_add(p, q):
    return add(p[0], q[0]), add(p[1], q[1])


def point_sub(p, q):
    return sub(p[0], q[0]), sub(p[1], q[1])


def point_scale(p, q):
    return scale(p[0], q), scale(p[1], q)


def norm2(p):
    return add(mul(p[0], p[0]), mul(p[1], p[1]))


def rotate60(p):
    # (x,y) -> ((x-sqrt(3)y)/2, (sqrt(3)x+y)/2)
    x, y = p
    return (
        scale(sub(x, mul(SQRT3, y)), F(1, 2)),
        scale(add(mul(SQRT3, x), y), F(1, 2)),
    )


def connector_points():
    origin = (ZERO, ZERO)
    terminal = (scale(ONE, F(8, 3)), ZERO)
    left_seed = (scale(ONE, F(23, 24)), scale(SQRT47, F(1, 24)))
    right_vector = (
        add(scale(ONE, F(-123, 144)), scale(SQRT141, F(-1, 144))),
        add(scale(SQRT3, F(-41, 144)), scale(SQRT47, F(3, 144))),
    )

    left, right_vectors = [], []
    p = left_seed
    q = right_vector
    for _ in range(6):
        left.append(p)
        right_vectors.append(q)
        p, q = rotate60(p), rotate60(q)
    need(p == left_seed and q == right_vector, "sixfold rotation did not close")
    right = [point_add(terminal, vector) for vector in right_vectors]
    return [origin, terminal] + left + right


def complete_edges(points):
    return [
        (u, v)
        for u, v in itertools.combinations(range(len(points)), 2)
        if norm2(point_sub(points[u], points[v])) == ONE
    ]


def proper(word, edges, colours):
    return (
        len(word) == 14
        and set(word) <= set(map(str, range(colours)))
        and all(word[u] != word[v] for u, v in edges)
    )


def k_colourable(vertices, edges, colours):
    adjacent = [set() for _ in range(vertices)]
    for u, v in edges:
        adjacent[u].add(v)
        adjacent[v].add(u)
    word = [-1] * vertices

    def visit(done):
        if done == vertices:
            return True
        vertex = max(
            (v for v in range(vertices) if word[v] < 0),
            key=lambda v: (
                len({word[w] for w in adjacent[v] if word[w] >= 0}),
                len(adjacent[v]),
                -v,
            ),
        )
        forbidden = {word[w] for w in adjacent[vertex] if word[w] >= 0}
        for colour in range(colours):
            if colour not in forbidden:
                word[vertex] = colour
                if visit(done + 1):
                    return True
        word[vertex] = -1
        return False

    return visit(0)


def encode_scalar(value):
    return [
        [coefficient.numerator, coefficient.denominator]
        for coefficient in value
    ]


def digest_rows(rows):
    stream = "\n".join(rows) + "\n"
    return hashlib.sha256(stream.encode()).hexdigest()


def verify():
    points = connector_points()
    need(len(points) == len(set(points)) == 14, "point collision")
    edges = complete_edges(points)
    expected_edges = set()
    expected_edges.update((0, vertex) for vertex in range(2, 8))
    expected_edges.update((1, vertex) for vertex in range(8, 14))
    expected_edges.update(
        tuple(sorted((2 + j, 2 + (j + 1) % 6))) for j in range(6)
    )
    expected_edges.update(
        tuple(sorted((8 + j, 8 + (j + 1) % 6))) for j in range(6)
    )
    expected_edges.update(((2, 8), (2, 13)))
    need(set(edges) == expected_edges, "complete edge set differs from construction")

    equal_four_word = "33" + "010101" + "121212"
    different_three_word = "01" + "121212" + "020202"
    need(proper(equal_four_word, edges, 4), "bad equal-terminal four-colouring")
    need(equal_four_word[0] == equal_four_word[1], "four-word terminals differ")
    need(proper(different_three_word, edges, 3), "bad three-colouring")
    need(different_three_word[0] != different_three_word[1], "three-word terminals agree")
    need(not k_colourable(14, edges, 2), "fixed connector unexpectedly bipartite")

    # Stronger abstract audit used after the geometric at-most-two-cross-edge
    # lemma: every union of two C6 rims and at most two cross edges is
    # three-colourable.  The centres can then share a fourth colour.
    rims = {
        tuple(sorted((j, (j + 1) % 6))) for j in range(6)
    } | {
        tuple(sorted((6 + j, 6 + (j + 1) % 6))) for j in range(6)
    }
    cross = [(j, 6 + k) for j in range(6) for k in range(6)]
    abstract_cases = 0
    for count in range(3):
        for selected in itertools.combinations(cross, count):
            abstract_cases += 1
            need(
                k_colourable(12, sorted(rims | set(selected)), 3),
                "at-most-two-cross-edge core is not three-colourable",
            )
    need(abstract_cases == 667, "wrong abstract case count")

    point_rows = [
        json.dumps([encode_scalar(point[0]), encode_scalar(point[1])], separators=(",", ":"))
        for point in points
    ]
    edge_rows = [f"{u} {v}" for u, v in edges]
    return {
        "schema": "e457-paired-hexagon-connector-stop-v1",
        "terminal_squared_distance": "64/9",
        "vertices": len(points),
        "complete_unit_edges": len(edges),
        "left_spokes": 6,
        "right_spokes": 6,
        "left_rim_edges": 6,
        "right_rim_edges": 6,
        "cross_edges": [[2, 8], [2, 13]],
        "chromatic_number": 3,
        "equal_terminal_four_colouring": equal_four_word,
        "different_terminal_three_colouring": different_three_word,
        "abstract_at_most_two_cross_edge_cases_checked": abstract_cases,
        "e457_raw_union_bound": 457 + len(points) - 2,
        "outside_field_witness_after_quarter_turn": "(-sqrt(47)/24,23/24)",
        "point_hash": digest_rows(point_rows),
        "edge_hash": digest_rows(edge_rows),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = verify()
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n"
    if args.check_expected:
        expected = (HERE / "expected.json").read_text()
        need(encoded == expected, "expected result mismatch")
    print(encoded, end="")


if __name__ == "__main__":
    main()
