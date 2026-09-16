#!/usr/bin/env python3
"""Exact standard-library verifier for the frozen Pegg12 triple-sum stop."""

from __future__ import annotations

import json
from pathlib import Path

from model import (
    all_source_four_colorings,
    check_word,
    coordinate_hash,
    edge_hash,
    find_coloring,
    inherited_edges,
    source_edges,
    source_points,
    triple_sum,
    word_hash,
)


HERE = Path(__file__).resolve().parent


class VerificationError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def compute():
    source = source_points()
    source_graph = source_edges()
    require(len(source) == len(set(source)) == 12, "bad source order")
    require(len(source_graph) == 21, "bad source edge count")
    require(find_coloring(12, source_graph, 3) is None, "source is three-colourable")
    require(find_coloring(12, source_graph, 4) is not None, "source is not four-colourable")

    points, edges, labels, fibre = triple_sum()
    require(sum(map(len, labels)) == 364, "formal address census failed")
    require(len(points) <= 508, "point cap failed")
    require(len(set(fibre)) == 12, "source fibre collided")
    edge_set = set(edges)
    require(
        all(tuple(sorted((fibre[a], fibre[b]))) in edge_set for a, b in source_graph),
        "source fibre lost an edge",
    )

    inherited = inherited_edges(points)
    require(set(inherited) <= edge_set, "an inherited unit edge is absent")
    source_words = all_source_four_colorings()
    require(len(source_words) == 756, "source colouring census failed")
    survivors = []
    first_extension = None
    for word in source_words:
        pins = {fibre[i]: int(word[i]) for i in range(12)}
        extension = find_coloring(len(points), edges, 4, pins)
        if extension is not None:
            survivors.append(word)
            if first_extension is None:
                first_extension = "".join(map(str, extension))

    require(first_extension is not None, "no four-colour extension was found")
    three_word = find_coloring(len(points), edges, 3)
    actual = {
        "source": {
            "points": 12,
            "edges": 21,
            "canonical_four_colorings": len(source_words),
            "coordinate_sha256": coordinate_hash(source),
            "edge_sha256": edge_hash(source_graph),
        },
        "triple_sum": {
            "formal_addresses": 364,
            "points": len(points),
            "edges": len(edges),
            "collision_classes": sum(len(group) > 1 for group in labels),
            "maximum_collision_multiplicity": max(map(len, labels)),
            "source_fibre": list(fibre),
            "translated_source_edges": len(inherited),
            "additional_complete_graph_edges": len(edge_set - set(inherited)),
            "source_inputs_blocked": len(source_words) - len(survivors),
            "source_inputs_surviving": len(survivors),
            "surviving_relation_sha256": word_hash(survivors),
            "coordinate_sha256": coordinate_hash(points),
            "edge_sha256": edge_hash(edges),
            "four_colorable": True,
            "three_colorable": three_word is not None,
        },
    }
    context = (points, edges, fibre, tuple(survivors), first_extension)
    return actual, context


def validate_certificate(certificate, context):
    points, edges, fibre, survivors, first_extension = context
    require(certificate["schema"] == "pegg12-commutative-triplesum-v1", "wrong schema")
    require(
        certificate["architecture"] == "p_i+p_j+p_k for 0<=i<=j<=k<12",
        "wrong architecture",
    )
    source_word = certificate["first_surviving_source_word"]
    require(source_word == survivors[0], "wrong first survivor")
    word = certificate["four_color_word"]
    require(word == first_extension, "wrong deterministic extension")
    colors = check_word(word, len(points), edges)
    require(
        all(colors[fibre[i]] == int(source_word[i]) for i in range(12)),
        "extension does not restrict to source word",
    )


def main():
    certificate = json.loads((HERE / "certificate.json").read_text())
    expected = json.loads((HERE / "expected.json").read_text())
    actual, context = compute()
    validate_certificate(certificate, context)
    print(json.dumps(actual, sort_keys=True, separators=(",", ":")))
    require(actual == expected, "reconstructed result differs from expected.json")
    print("VERIFIED_PEGG12_TRIPLESUM_FOUR_CHROMATIC_STOP")


if __name__ == "__main__":
    main()
