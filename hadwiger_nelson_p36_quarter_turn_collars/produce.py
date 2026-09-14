#!/usr/bin/env python3
"""Generate positive four-colour certificates for residue-conflict orbits."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import model


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", type=Path,
                        default=Path("colourings.json"))
    args = parser.parse_args()
    started = time.monotonic()

    labels, points = model.patch(36)
    units = model.unit_vectors()
    centers = model.all_centers(points)
    representatives = sorted({model.canonical_center(center) for center in centers})
    triangle_indices = [labels.index(label) for label in ((0, 0), (1, 0), (0, 1))]
    certificates = []
    total_nodes = 0

    for number, center in enumerate(representatives):
        graph = model.build_graph(center, points, units)
        if model.residue_colouring(graph, labels) is not None:
            continue
        triangle = tuple(graph["where"][points[index]] for index in triangle_indices)
        if len(set(triangle)) != 3:
            raise AssertionError("pinned unit triangle collapsed")
        word, nodes = model.four_colouring(
            len(graph["physical"]), graph["edges"], triangle)
        if word is None:
            raise RuntimeError(f"non-four signal at center {center}")
        total_nodes += nodes
        certificates.append({
            "center": list(center),
            "vertices": len(graph["physical"]),
            "edges": len(graph["edges"]),
            "word": "".join(map(str, word)),
        })
        if number and number % 200 == 0:
            print(json.dumps({"orbit": number, "certificates": len(certificates),
                              "seconds": round(time.monotonic() - started, 3)}),
                  flush=True)

    payload = {
        "schema": "p36-quarter-turn-collar-positive-colourings-v1",
        "coordinate_order": "lexicographic integer quadruples representing axes in Q(sqrt(3))/4",
        "colour_names": "0123",
        "certificates": certificates,
    }
    args.output.write_text(
        json.dumps(payload, separators=(",", ":"), sort_keys=True) + "\n",
        encoding="utf-8")
    print(json.dumps({
        "status": "PASS",
        "raw_centers": len(centers),
        "dihedral_orbits": len(representatives),
        "certificates": len(certificates),
        "search_nodes": total_nodes,
        "seconds": round(time.monotonic() - started, 3),
        "output": str(args.output),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
