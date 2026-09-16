#!/usr/bin/env python3
"""Produce the compact exact certificate; output path must not exist."""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations, product
from pathlib import Path

from model import (
    build,
    cut_structure,
    degree_histogram,
    find_coloring,
    point_hash,
    proper,
    stream_hash,
    strict_edges,
)


def make_certificate():
    source_bytes, source, s0, a0, a1, a2, full_s2, first, second = build()
    e0 = strict_edges(a0)
    e1 = strict_edges(a1)
    e2 = strict_edges(a2)
    four = find_coloring(len(a2), e2, 4)
    if four is None:
        raise RuntimeError("unexpected non-four signal: certificate format needs extension")
    four_word = "".join(map(str, four))
    if not proper(four_word, len(a2), e2):
        raise RuntimeError("bad four-colour witness")

    moser = [a0.index((tuple(x), tuple(y))) for x, y in source["M"]]
    edge_set = set(e0)
    medges = [
        (i, j) for i, j in combinations(range(7), 2)
        if tuple(sorted((moser[i], moser[j]))) in edge_set
    ]
    proper3 = sum(
        all(word[a] != word[b] for a, b in medges)
        for word in product(range(3), repeat=7)
    )
    components, articulations, bridges = cut_structure(len(a2), e2)
    s2_intersection = len(set(a2) & set(full_s2))
    return {
        "schema": "hn-moser-mixeddepth-f4-stop-v1",
        "source_certificate_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "scale": 12,
        "basis": source["basis"],
        "operator": "A0=S1; A1=F4(A0); A2=F4(A1)",
        "threshold": 4,
        "first_step": first,
        "second_step": second,
        "supports": [
            {"name": "A0", "points": len(a0), "edges": len(e0),
             "point_sha256": point_hash(a0), "edge_sha256": stream_hash(e0)},
            {"name": "A1", "points": len(a1), "edges": len(e1),
             "point_sha256": point_hash(a1), "edge_sha256": stream_hash(e1)},
            {"name": "A2", "points": len(a2), "edges": len(e2),
             "point_sha256": point_hash(a2), "edge_sha256": stream_hash(e2)},
        ],
        "mixed_depth_audit": {
            "accepted_full_s2_points": len(full_s2),
            "a2_points_in_full_s2": s2_intersection,
            "a2_points_beyond_full_s2": len(a2) - s2_intersection,
            "full_s2_points_absent_from_a2": len(full_s2) - s2_intersection,
        },
        "graph_structure": {
            "components": components,
            "articulation_vertices": len(articulations),
            "bridges": len(bridges),
            "degree_histogram": degree_histogram(len(a2), e2),
        },
        "source_input_decision": {
            "zero_extensions": False,
            "surviving_source_word": four_word[:len(a0)],
            "surviving_full_word": four_word,
            "source_word_sha256": hashlib.sha256((four_word[:len(a0)] + "\n").encode()).hexdigest(),
            "full_word_sha256": hashlib.sha256((four_word + "\n").encode()).hexdigest(),
            "decision_method": "literal proper four-colouring of the complete A2 graph",
            "complete_source_relation_enumerated": False,
        },
        "moser_subgraph": {
            "indices_in_a0": moser,
            "edges": len(medges),
            "proper_named_three_colorings": proper3,
        },
        "chromatic_number": 4,
        "record_candidate": False,
        "status": "EXACT_MIXED_DEPTH_SUPPORT_HAS_SURVIVING_SOURCE_FOUR_COLOURING",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(args.out)
    args.out.write_text(json.dumps(make_certificate(), indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
