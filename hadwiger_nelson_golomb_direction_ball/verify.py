#!/usr/bin/env python3
"""Standard-library verifier for the exact Golomb direction radius-two ball."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
ZERO = (F(0),) * 4
ONE = (F(1), F(0), F(0), F(0))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add(x, y):
    return tuple(a + b for a, b in zip(x, y, strict=True))


def scale(x, scalar):
    return tuple(scalar * a for a in x)


def sub(x, y):
    return add(x, scale(y, -1))


def conjugate(x):
    return x[0], x[1], -x[2], -x[3]


def multiply(x, y):
    a, b, c, d = x
    A, B, C, D = y
    return (
        a * A + 33 * b * B - 3 * c * C - 11 * d * D,
        a * B + b * A - c * D - d * C,
        a * C + c * A + 11 * (b * D + d * B),
        a * D + d * A + 3 * (b * C + c * B),
    )


def norm(x):
    return multiply(x, conjugate(x))


def golomb():
    # (a,b,c,d) means (a+b*sqrt(33))/36 + i*sqrt(3)*(c+d*sqrt(33))/36.
    rows = [
        (0, 0, 0, 0), (36, 0, 0, 0), (18, 0, 18, 0),
        (-18, 0, 18, 0), (-36, 0, 0, 0), (-18, 0, -18, 0),
        (18, 0, -18, 0), (6, 0, 0, 2), (-3, -3, 3, -1),
        (-3, 3, -3, -1),
    ]
    return [(F(a, 36), F(b, 36), F(c, 36), F(d, 12))
            for a, b, c, d in rows]


def strict_edges(points):
    return [(u, v) for u, v in combinations(range(len(points)), 2)
            if norm(sub(points[u], points[v])) == ONE]


def construction():
    source = golomb()
    source_edges = strict_edges(source)
    directions = sorted({
        min(sub(source[v], source[u]), scale(sub(source[v], source[u]), -1))
        for u, v in source_edges
    })
    oriented = sorted(set(directions + [scale(direction, -1)
                                        for direction in directions]))
    alphabet = [ZERO] + oriented
    points = sorted({add(a, b) for a in alphabet for b in alphabet})
    edges = strict_edges(points)
    index = {point: i for i, point in enumerate(points)}
    source_vertices = tuple(index[point] for point in source)
    return source, source_edges, directions, points, edges, source_vertices


def proper(word, colours, vertices, edges):
    return (len(word) == vertices and set(word) <= set(map(str, range(colours)))
            and all(word[u] != word[v] for u, v in edges))


def source_patterns(source_edges):
    patterns = []
    for tail in product(range(4), repeat=7):
        word = (0, 1, 2) + tail
        if all(word[u] != word[v] for u, v in source_edges):
            patterns.append("".join(map(str, word)))
    return patterns


def stream_hash(rows):
    return hashlib.sha256(("\n".join(rows) + "\n").encode()).hexdigest()


def graph_hashes(points, edges):
    point_rows = ["|".join(map(str, point)) for point in points]
    edge_rows = [f"{u} {v}" for u, v in edges]
    return stream_hash(point_rows), stream_hash(edge_rows)


def verify(certificate):
    require(certificate.get("schema") == "golomb-direction-ball-neutrality-v1",
            "wrong certificate schema")
    source, source_edges, directions, points, edges, terminals = construction()
    require(len(source) == 10 and len(source_edges) == 18, "wrong Golomb source")
    require(len(directions) == 9, "wrong unit-direction count")
    require(len(points) == 163 and len(edges) == 648, "wrong physical graph")
    require(len(set(points)) == len(points), "point collision was not merged")
    require(all(tuple(sorted((terminals[u], terminals[v]))) in set(edges)
                for u, v in source_edges), "source edge missing from ball")

    # The triangle at source vertices 0,1,2 normalizes colour permutations.
    require(all(pair in source_edges for pair in ((0, 1), (0, 2), (1, 2))),
            "normalizing Golomb triangle missing")
    three_colourings = sum(
        all(word[u] != word[v] for u, v in source_edges)
        for tail in product(range(3), repeat=7)
        for word in [(0, 1, 2) + tail]
    )
    require(three_colourings == 0, "Golomb source unexpectedly three-colourable")

    expected_patterns = source_patterns(source_edges)
    extensions = certificate.get("source_extensions")
    require(isinstance(extensions, list), "missing source extensions")
    require([row.get("pattern") for row in extensions] == expected_patterns,
            "source extension patterns are incomplete or out of order")
    extension_words = []
    for row in extensions:
        word = row.get("word")
        require(isinstance(word, str) and proper(word, 4, len(points), edges),
                "improper source extension word")
        require("".join(word[v] for v in terminals) == row["pattern"],
                "source projection does not match claimed pattern")
        extension_words.append(word)

    edge_set = set(edges)
    nonedges = [pair for pair in combinations(range(len(points)), 2)
                if pair not in edge_set]
    equal_words = certificate.get("equal_cover_words")
    separating_words = certificate.get("separating_cover_words")
    require(isinstance(equal_words, list) and equal_words,
            "missing equality cover")
    require(isinstance(separating_words, list) and separating_words,
            "missing separation cover")
    require(all(isinstance(word, str) and proper(word, 4, len(points), edges)
                for word in equal_words), "improper equality-cover word")
    require(all(isinstance(word, str) and proper(word, 4, len(points), edges)
                for word in separating_words), "improper separation-cover word")
    require(all(any(word[u] == word[v] for word in equal_words)
                for u, v in nonedges), "some nonedge is never equal")
    require(all(any(word[u] != word[v] for word in separating_words)
                for u, v in nonedges), "some nonedge is never separated")

    point_hash, edge_hash = graph_hashes(points, edges)
    summary = {
        "unoriented_unit_directions": len(directions),
        "vertices": len(points),
        "edges": len(edges),
        "golomb_vertices": len(source),
        "golomb_edges": len(source_edges),
        "chromatic_number": 4,
        "canonical_golomb_patterns": len(expected_patterns),
        "extended_golomb_patterns": len(extension_words),
        "physical_nonedges": len(nonedges),
        "equality_cover_words": len(equal_words),
        "separation_cover_words": len(separating_words),
        "point_stream_sha256": point_hash,
        "edge_stream_sha256": edge_hash,
    }
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    summary = verify(certificate)
    if args.check_expected:
        require(summary == json.loads((HERE / "expected.json").read_text()),
                "summary differs from expected result")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
