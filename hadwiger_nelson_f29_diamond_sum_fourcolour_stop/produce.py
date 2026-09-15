#!/usr/bin/env python3
"""Produce the literal four-colour certificate for the fixed exact sum."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from model import adjacency, build_geometry, colour, digest, flat


HERE = Path(__file__).resolve().parent


def build():
    _, _, points, edges, inherited, address_map = build_geometry()
    word = colour(adjacency(len(points), edges), 4)
    if word is None:
        raise RuntimeError("unexpected non-four signal")
    if not all(word[a] != word[b] for a, b in edges):
        raise RuntimeError("improper generated word")
    point_rows = [[flat(p[0]), flat(p[1])] for p in points]
    return {
        "format": "hn-f29-diamond-sum-fourcolour-v1",
        "proper_four_word": "".join(map(str, word)),
        "point_rows_sha256": digest(point_rows),
        "edge_rows_sha256": digest([list(e) for e in edges]),
        "address_map_sha256": digest(address_map),
        "physical_points": len(points),
        "complete_unit_edges": len(edges),
        "inherited_distinct_edges": len(inherited),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=HERE / "certificate.json")
    args = parser.parse_args()
    args.out.write_text(json.dumps(build(), indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()

