#!/usr/bin/env python3
"""Positive and negative controls for the independent D31 review."""

import json

from independent_check import (
    CheckError,
    SOURCE_EDGE_TEXT,
    build_spindle,
    canonical_colouring_census,
    find_colouring,
    parse_edge_text,
    poly_add,
    poly_multiply,
    verify_static_source,
)


def must_reject(label, action):
    try:
        action()
    except (CheckError, RuntimeError):
        return label
    raise RuntimeError(f"control was not rejected: {label}")


def main():
    source = parse_edge_text(SOURCE_EDGE_TEXT)
    rejected = []
    rejected.append(must_reject(
        "duplicate_source_edge",
        lambda: parse_edge_text(SOURCE_EDGE_TEXT + " 1-2"),
    ))
    rejected.append(must_reject(
        "source_edge_deletion",
        lambda: verify_static_source(source[1:]),
    ))
    rejected.append(must_reject(
        "source_edge_substitution",
        lambda: verify_static_source(tuple(sorted(set(source[1:]) | {(0, 2)}))),
    ))
    rejected.append(must_reject(
        "self_loop",
        lambda: parse_edge_text("1-1"),
    ))

    k4 = tuple((a, b) for a in range(4) for b in range(a + 1, 4))
    k4_three = canonical_colouring_census(4, k4, 3)
    k4_four = canonical_colouring_census(4, k4, 4)
    if k4_three["leaves"] != 0 or k4_four["leaves"] != 1:
        raise RuntimeError("K4 colouring control failed")

    spindle, _second, bridge = build_spindle(source)
    without_bridge = tuple(edge for edge in spindle if edge != bridge)
    four_word, four_nodes = find_colouring(61, without_bridge, 4)
    if four_word is None:
        raise RuntimeError("bridge-deletion positive control is not four-colourable")

    f = [1, 0, -2, 1]
    g = [-1, -2, 1, 1]
    broken = poly_add(poly_multiply([1, -3, -2], f),
                      poly_multiply([0, -3, 3], g))
    if broken == [1]:
        raise RuntimeError("mutated Bezout multiplier was accepted")
    rejected.append("bezout_multiplier_mutation")

    output = {
        "status": "PASS",
        "rejected_mutations": rejected,
        "k4_canonical_three_colourings": k4_three["leaves"],
        "k4_canonical_four_colourings": k4_four["leaves"],
        "spindle_without_bridge_four_colourable": True,
        "spindle_without_bridge_search_nodes": four_nodes,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
