#!/usr/bin/env python3
"""Definition-level controls for the independent H510 exact-507 checker."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_checker():
    spec = importlib.util.spec_from_file_location("h510_exact507_review", HERE / "independent_verify.py")
    if spec is None or spec.loader is None:
        raise ValueError("checker import")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def brute_k23(adjacency):
    for a, b in combinations(range(len(adjacency)), 2):
        if (adjacency[a] & adjacency[b]).bit_count() >= 3:
            return True
    return False


def main():
    checker = load_checker()
    stream = sha256()

    radicands = (1, 3, 5, 15, 11, 33, 55, 165)
    radical_products = 0
    for first in range(8):
        for second in range(8):
            radical, factor = checker.radical_product_factor(first, second)
            checker.require(
                radicands[first] * radicands[second] == factor * factor * radicands[radical],
                "radical multiplication",
            )
            radical_products += 1
            stream.update(f"r:{first}:{second}:{radical}:{factor}\n".encode())

    pairs = list(combinations(range(4), 2))
    dense_graphs = 0
    triangle_graphs = 0
    c4_graphs = 0
    for word in range(1 << len(pairs)):
        edges = {pair for bit, pair in enumerate(pairs) if word & (1 << bit)}
        if len(edges) < 4:
            continue
        dense_graphs += 1
        triangles = [
            triple for triple in combinations(range(4), 3)
            if all(pair in edges for pair in combinations(triple, 2))
        ]
        if triangles:
            triangle_graphs += 1
            kind = "triangle"
        else:
            degrees = [sum(vertex in pair for pair in edges) for vertex in range(4)]
            checker.require(len(edges) == 4 and degrees == [2, 2, 2, 2], "triangle-free dense graph")
            c4_graphs += 1
            kind = "c4"
        stream.update(f"g:{word}:{kind}\n".encode())

    k23 = [0] * 5
    for centre in (0, 1):
        for leaf in (2, 3, 4):
            k23[centre] |= 1 << leaf
            k23[leaf] |= 1 << centre
    checker.require(brute_k23(k23), "brute K2,3 positive")
    checker.require(checker.first_new_k23(k23, [0]) is not None, "local K2,3 positive")
    path = [0] * 5
    for u, v in zip(range(4), range(1, 5)):
        path[u] |= 1 << v
        path[v] |= 1 << u
    checker.require(not brute_k23(path), "brute K2,3 negative")
    checker.require(checker.first_new_k23(path, [0]) is None, "local K2,3 negative")

    shapes = [
        checker.canonical_groups(((0, 1, 2, 3),)),
        checker.canonical_groups(((0, 1, 2), (3, 4))),
        checker.canonical_groups(((0, 1), (2, 3), (4, 5))),
    ]
    checker.require([sorted(map(len, shape)) for shape in shapes] == [[4], [2, 3], [2, 2, 2]], "fibre shapes")

    result = {
        "status": "INDEPENDENT_CONTROLS_OK",
        "radical_products": radical_products,
        "four_vertex_graphs_with_at_least_four_edges": dense_graphs,
        "dense_graphs_with_triangle": triangle_graphs,
        "triangle_free_dense_graphs": c4_graphs,
        "k23_positive_and_negative_controls": 2,
        "fibre_shapes": [sorted(map(len, shape)) for shape in shapes],
        "control_stream_sha256": stream.hexdigest(),
    }
    expected_path = HERE / "controls_expected.json"
    if expected_path.exists():
        checker.require(result == json.loads(expected_path.read_text()), "control expected output")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
