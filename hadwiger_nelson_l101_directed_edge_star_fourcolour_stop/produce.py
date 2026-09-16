#!/usr/bin/env python3
"""Produce the exact certificate for the frozen directed-edge-star closure."""

import argparse
import hashlib
import json
import platform
from pathlib import Path

from exact_model import (FIGURE_EDGES, adjacency, build, core_size,
                         find_coloring, graph_cuts, proper_coloring)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha256(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def make_certificate():
    model = build()
    points = model["points"]
    edges = model["edges"]
    adj = adjacency(len(points), edges)
    source_adj = adjacency(len(model["source_points"]), model["source_edges"])
    source_three = find_coloring(source_adj, 3)
    source_four = find_coloring(source_adj, 4)
    four_word = find_coloring(adj, 4)
    if source_three is not None or source_four is None or four_word is None:
        raise AssertionError("unexpected chromatic decision")
    if not proper_coloring(four_word, edges, 4):
        raise AssertionError("bad producer coloring")
    seen, articulations, bridges = graph_cuts(adj)
    encoded_points = [p.encode() for p in points]
    encoded_edges = [list(e) for e in edges]
    return {
        "schema": 1,
        "title": "Exact four-colour stop for the L10,1 directed-edge-star closure",
        "field": "Q(sqrt(3),sqrt(11)); coefficient basis [1,sqrt(3),sqrt(11),sqrt(33)]",
        "operation": "for every directed physical source unit edge (u,v), z maps to u+(v-u)z",
        "raw_vertex_upper_bound": 314,
        "source_vertices": 10,
        "source_displayed_edges": len(FIGURE_EDGES),
        "source_complete_edges": len(model["source_edges"]),
        "source_incidental_edges": [list(e) for e in sorted(model["source_incidental_edges"])],
        "source_three_colorable": False,
        "source_four_word": list(source_four),
        "directed_placements": len(model["placements"]),
        "distinct_placement_supports": len({frozenset(image) for _, image in model["placements"]}),
        "vertices": len(points),
        "edges": len(edges),
        "all_pairs_decided": len(points)*(len(points)-1)//2,
        "connected": seen == len(points),
        "articulations": sorted(articulations),
        "bridges": [list(e) for e in bridges],
        "minimum_degree": min(map(len, adj)),
        "maximum_degree": max(map(len, adj)),
        "four_core_vertices": core_size(adj, 4),
        "chromatic_number": 4,
        "four_word": list(four_word),
        "points": encoded_points,
        "unit_edges": encoded_edges,
        "point_sha256": sha256(encoded_points),
        "edge_sha256": sha256(encoded_edges),
        "python": platform.python_version(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="certificate.json")
    args = parser.parse_args()
    certificate = make_certificate()
    Path(args.output).write_text(json.dumps(certificate, indent=2, sort_keys=True)+"\n")
    summary = {k: certificate[k] for k in (
        "source_vertices", "source_complete_edges", "directed_placements",
        "vertices", "edges", "all_pairs_decided", "connected",
        "minimum_degree", "maximum_degree", "four_core_vertices",
        "chromatic_number", "point_sha256", "edge_sha256")}
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
