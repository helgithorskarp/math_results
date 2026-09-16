#!/usr/bin/env python3
"""Self-contained exact verifier for the frozen C11 spindle-round stop."""

from __future__ import annotations

import json
from pathlib import Path

from model import (
    canonical_colorings,
    check_word,
    construction,
    coordinate_hash,
    edge_hash,
    find_coloring,
    induced_edges,
    word_hash,
)


HERE = Path(__file__).resolve().parent


class VerificationError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def cut_structure(vertex_count, edges):
    """Return component count, articulation vertices and bridges (Tarjan)."""
    adj = [set() for _ in range(vertex_count)]
    for a, b in edges:
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
    return components, tuple(sorted(articulations)), tuple(sorted(bridges))


def compute():
    points, edges, labels, source = construction()
    require(sum(map(len, labels)) == 90, "formal-address census failed")
    require(len(points) <= 508, "campaign point cap failed")
    require(len(set(source)) == 7, "source spindle collided")
    source_edges = induced_edges(source, edges)
    require(len(source_edges) == 11, "unexpected source-spindle edge count")
    require(find_coloring(7, source_edges, 3) is None, "source is three-colourable")
    require(find_coloring(7, source_edges, 4) is not None, "source is not four-colourable")

    source_words = canonical_colorings(7, source_edges, 4)
    require(len(source_words) == 16, "source colouring census failed")
    extensions = []
    for source_word in source_words:
        pins = {source[i]: source_word[i] for i in range(7)}
        extension = find_coloring(len(points), edges, 4, pins)
        if extension is not None:
            extensions.append(extension)

    collision_groups = [group for group in labels if len(group) > 1]
    components, articulations, bridges = cut_structure(len(points), edges)
    actual = {
        "field": {
            "cyclotomic_order": 66,
            "degree": 20,
        },
        "source_spindle": {
            "points": 7,
            "edges": len(source_edges),
            "canonical_four_colorings": len(source_words),
            "three_colorable": False,
            "edge_sha256": edge_hash(source_edges),
        },
        "full_c11_round": {
            "formal_addresses": 90,
            "points": len(points),
            "edges": len(edges),
            "components": components,
            "articulation_vertices": len(articulations),
            "bridges": len(bridges),
            "collision_classes": len(collision_groups),
            "maximum_collision_multiplicity": max(map(len, labels)),
            "source_fibre": list(source),
            "source_inputs_blocked": len(source_words) - len(extensions),
            "source_inputs_surviving": len(extensions),
            "source_relation_sha256": word_hash(source_words),
            "extension_sha256": word_hash(extensions),
            "coordinate_sha256": coordinate_hash(points),
            "edge_sha256": edge_hash(edges),
            "four_colorable": bool(extensions),
            "three_colorable": False,
        },
    }
    return actual, (points, edges, source, source_words, tuple(extensions))


def validate_certificate(certificate, context):
    points, edges, source, source_words, extensions = context
    require(certificate["schema"] == "hendecagon-c11-spindle-round-v1", "wrong schema")
    records = certificate["source_extensions"]
    require(len(records) == len(source_words) == len(extensions), "wrong certificate census")
    for index, record in enumerate(records):
        source_word = tuple(map(int, record["source_word"]))
        require(source_word == source_words[index], "source word order differs")
        colors = check_word(record["extension"], len(points), edges)
        require(colors == extensions[index], "extension differs from deterministic witness")
        require(
            all(colors[source[i]] == source_word[i] for i in range(7)),
            "extension does not restrict to its source word",
        )


def main():
    expected = json.loads((HERE / "expected.json").read_text())
    certificate = json.loads((HERE / "certificate.json").read_text())
    actual, context = compute()
    print(json.dumps(actual, sort_keys=True, separators=(",", ":")))
    require(actual == expected, "result differs from expected.json")
    validate_certificate(certificate, context)
    print("VERIFIED_HENDECAGON_C11_SPINDLE_ROUND_FOUR_CHROMATIC_STOP")


if __name__ == "__main__":
    main()
