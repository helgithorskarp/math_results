#!/usr/bin/env python3
"""Definition-level exact verifier for the published certificate."""

import hashlib
import json
from pathlib import Path

from exact_model import (FIGURE_EDGES, adjacency, build, core_size,
                         find_coloring, graph_cuts, proper_coloring)


ROOT = Path(__file__).resolve().parent


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha256(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def verify_certificate(data, expected):
    model = build()
    points = model["points"]
    edges = model["edges"]
    encoded_points = [p.encode() for p in points]
    encoded_edges = [list(e) for e in edges]

    require(data["points"] == encoded_points, "coordinate list mismatch")
    require(data["unit_edges"] == encoded_edges, "complete edge list mismatch")
    require(data["point_sha256"] == sha256(encoded_points), "coordinate hash mismatch")
    require(data["edge_sha256"] == sha256(encoded_edges), "edge hash mismatch")
    require(data["point_sha256"] == expected["point_sha256"], "unexpected coordinate fingerprint")
    require(data["edge_sha256"] == expected["edge_sha256"], "unexpected edge fingerprint")

    require(len(model["source_points"]) == 10, "source order mismatch")
    require(len(model["source_edges"]) == 19, "source complete edge count mismatch")
    require(FIGURE_EDGES <= model["source_named_edges"], "displayed edge missing")
    require(model["source_incidental_edges"] == {("B", "F"), ("D", "H")},
            "source incidental contacts mismatch")
    moser_vertices = "ABFGHIJ"
    moser_edges = {tuple(sorted(e)) for e in
                   "AB AF AG BF BG FI FJ HI HJ IJ GH".split()}
    actual_moser = {e for e in model["source_named_edges"]
                    if e[0] in moser_vertices and e[1] in moser_vertices}
    require(actual_moser == moser_edges, "embedded Moser spindle mismatch")
    require(len(model["placements"]) == 38, "directed placement count mismatch")
    require(len({frozenset(image) for _, image in model["placements"]}) == 37,
            "distinct placement-support count mismatch")
    require(data["raw_vertex_upper_bound"] == 314, "raw cap mismatch")

    require(len(points) == data["vertices"] == expected["vertices"] == 188,
            "physical vertex count mismatch")
    require(len(edges) == data["edges"] == expected["edges"] == 765,
            "physical edge count mismatch")
    require(data["all_pairs_decided"] == 17578, "pair census mismatch")

    source_adj = adjacency(10, model["source_edges"])
    require(find_coloring(source_adj, 3) is None, "source unexpectedly three-colorable")
    source_word = tuple(data["source_four_word"])
    require(len(source_word) == 10 and proper_coloring(source_word, model["source_edges"], 4),
            "bad source four-word")

    adj = adjacency(len(points), edges)
    four_word = tuple(data["four_word"])
    require(len(four_word) == len(points), "four-word length mismatch")
    require(proper_coloring(four_word, edges, 4), "improper four-word")
    require(data["chromatic_number"] == 4, "wrong chromatic conclusion")

    source_index = {p: i for i, p in enumerate(points)}
    require(all(p in source_index for p in model["source_points"]),
            "source is not embedded in closure")
    embedded_source_edges = {
        tuple(sorted((source_index[model["source_points"][u]],
                      source_index[model["source_points"][v]])))
        for u, v in model["source_edges"]
    }
    require(embedded_source_edges <= set(edges), "embedded source edge missing")

    seen, articulations, bridges = graph_cuts(adj)
    require(seen == len(points) and data["connected"], "graph disconnected")
    require(not articulations and data["articulations"] == [], "articulation found")
    require(not bridges and data["bridges"] == [], "bridge found")
    require(min(map(len, adj)) == data["minimum_degree"] == 3, "minimum degree mismatch")
    require(max(map(len, adj)) == data["maximum_degree"] == 22, "maximum degree mismatch")
    require(core_size(adj, 4) == data["four_core_vertices"] == 184,
            "four-core size mismatch")
    return {
        "source": [10, 19],
        "closure": [188, 765],
        "pairs": 17578,
        "chromatic_number": 4,
        "articulations": 0,
        "bridges": 0,
        "four_core": 184,
        "point_sha256": data["point_sha256"],
        "edge_sha256": data["edge_sha256"],
    }


def main():
    data = json.loads((ROOT/"certificate.json").read_text())
    expected = json.loads((ROOT/"EXPECTED.json").read_text())
    print(json.dumps(verify_certificate(data, expected), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
