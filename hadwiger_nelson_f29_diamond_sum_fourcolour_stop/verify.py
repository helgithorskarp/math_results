#!/usr/bin/env python3
"""Replay exact geometry, input forcing features, and the positive stop word."""

from __future__ import annotations

import json
from pathlib import Path

from model import adjacency, build_geometry, colour, digest, edges, flat


HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def run(certificate_path: Path = HERE / "certificate.json"):
    cert = json.loads(certificate_path.read_text())
    need(set(cert) == {
        "format", "proper_four_word", "point_rows_sha256", "edge_rows_sha256",
        "address_map_sha256", "physical_points", "complete_unit_edges",
        "inherited_distinct_edges",
    }, "certificate fields")
    need(cert["format"] == "hn-f29-diamond-sum-fourcolour-v1", "certificate format")

    f29, core, points, complete_edges, inherited, address_map = build_geometry()
    need(len(points) == len(address_map) == 232, "unexpected point collision")
    need(len(complete_edges) == 994 and len(inherited) == 919, "graph census")
    need(len(set(complete_edges) - inherited) == 75, "incidental edge census")

    # Recheck the two forcing inputs rather than infer them from package names.
    f_edges = edges(f29)
    f_adj = adjacency(len(f29), f_edges)
    centre_neighbours = sorted(f_adj[0])
    need(len(centre_neighbours) == 14, "F29 centre neighbourhood")
    deleted_edges = [(a - 1, b - 1) for a, b in f_edges if a and b]
    allowed = [set(range(4)) for _ in range(28)]
    for v in centre_neighbours:
        allowed[v - 1] = {0, 1}
    need(colour(adjacency(28, deleted_edges), 4, allowed) is None,
         "F29 palette obstruction failed")
    need(colour(f_adj, 4) is not None and colour(f_adj, 3) is None,
         "F29 chromatic gate")

    d_edges = set(edges(core))
    need(d_edges == {
        (0, 2), (0, 3), (0, 4), (0, 5),
        (1, 4), (1, 5), (1, 6), (1, 7),
        (2, 3), (4, 5), (6, 7),
    }, "eight-point palette core graph")
    need(colour(adjacency(8, sorted(d_edges)), 3) is not None,
         "palette core positive gate")

    point_rows = [[flat(p[0]), flat(p[1])] for p in points]
    need(cert["point_rows_sha256"] == digest(point_rows), "point hash")
    need(cert["edge_rows_sha256"] == digest([list(e) for e in complete_edges]), "edge hash")
    need(cert["address_map_sha256"] == digest(address_map), "address-map hash")
    need((cert["physical_points"], cert["complete_unit_edges"],
          cert["inherited_distinct_edges"]) == (232, 994, 919), "certificate census")

    word = cert["proper_four_word"]
    need(isinstance(word, str) and len(word) == 232 and set(word) <= set("0123"),
         "four-word format")
    need(all(word[a] != word[b] for a, b in complete_edges), "monochromatic unit edge")

    result = {
        "status": "EXACT_F29_DIAMOND_SUM_FOUR_COLOUR_STOP_VERIFIED",
        "raw_addresses": 232,
        "physical_points": 232,
        "collisions_removed": 0,
        "complete_pair_checks": 26796,
        "complete_unit_edges": 994,
        "inherited_distinct_edges": 919,
        "incidental_unit_edges": 75,
        "f29_neighbour_palette_minimum": 3,
        "diamond_core_palette_intersections": 2,
        "chromatic_number": 4,
        "point_rows_sha256": cert["point_rows_sha256"],
        "edge_rows_sha256": cert["edge_rows_sha256"],
        "address_map_sha256": cert["address_map_sha256"],
    }
    expected = json.loads((HERE / "expected.json").read_text())
    need(result == expected, "expected result mismatch")
    return result


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))

