#!/usr/bin/env python3
"""Regenerate the positive colouring certificate; not part of the checker."""

import argparse
import json
from pathlib import Path

from verify import N, all_edges, build_geometry, canonical_words, find_colouring, sha_rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)

    source, w, points, maps = build_geometry()
    source_edges = all_edges(source)
    edges = all_edges(points)
    internal = {
        tuple(sorted((maps[c][a], maps[c][b])))
        for c in (0, 1) for a, b in source_edges
    }
    extras = [e for e in edges if tuple(e) not in internal]
    terminals = [maps[0][0], maps[1][0], maps[0][4], maps[0][1], maps[1][4], maps[1][1]]
    eset = {tuple(e) for e in edges}
    terminal_edges = [
        [a, b] for a in range(6) for b in range(a + 1, 6)
        if tuple(sorted((terminals[a], terminals[b]))) in eset
    ]
    witnesses = {}
    for pattern in canonical_words(6):
        if any(pattern[a] == pattern[b] for a, b in terminal_edges):
            continue
        key = "".join(map(str, pattern))
        word = find_colouring(58, edges, 4, {terminals[i]: pattern[i] for i in range(6)})
        if word is None:
            raise RuntimeError(f"bare pattern did not extend: {key}")
        witnesses[key] = "".join(map(str, word))
    whole = find_colouring(58, edges, 4, {0: 0})
    if whole is None:
        raise RuntimeError("unexpected four-colour obstruction")
    point_rows = [[x.row(), y.row()] for x, y in points]
    data = {
        "active_interface_bare_patterns": len(witnesses),
        "active_interface_edges": terminal_edges,
        "active_interface_extended_patterns": len(witnesses),
        "active_interface_extension_words": witnesses,
        "active_interface_neutral": True,
        "active_interface_rows": terminals,
        "architecture": "F29 half-turn edge-reversal through roles 4 and 1",
        "centre_rows": [maps[0][0], maps[1][0]],
        "collisions": [],
        "complete_edges": len(edges),
        "copy_terminal_palettes_in_four_word": [
            sorted({whole[maps[c][v]] for v in N}) for c in (0, 1)
        ],
        "edges_sha256": sha_rows(edges),
        "extra_edge_rows": extras,
        "extra_edges": len(extras),
        "formal_addresses": 58,
        "four_colour_word": "".join(map(str, whole)),
        "four_colourable": True,
        "internal_edge_union": len(internal),
        "physical_vertices": len(points),
        "points_sha256": sha_rows(point_rows),
        "prescribed_edge_rows": [[0, 29], [1, 33], [4, 30]],
        "q_squared": "7/5",
        "role_rows": {"copy0_role1": 1, "copy0_role4": 4, "copy1_role1": 30, "copy1_role4": 33},
        "source_edges": len(source_edges),
        "source_vertices": len(source),
        "three_colourable": False,
        "w": [w[0].row(), w[1].row()],
    }
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
