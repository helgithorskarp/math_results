#!/usr/bin/env python3
"""Pack raw six-bridge deletion colorings into the compact certificate."""

from __future__ import annotations

import argparse
import base64
import json
from fractions import Fraction
from pathlib import Path


SCALE = 96
BASE_SIZE = 509
TOTAL_SIZE = 515
EXPECTED_EDGE_SHA256 = "f665c9a30ed9e8691a0c2ffceb32bbe47e369ae74491b1aa2bba9e44496df20d"
BRIDGE_COORDINATES = [
    [[0, 0, 0, 0, 0, 0, 0, 0], [0, -16, 0, 0, 48, 0, 0, 0]],
    [[0, 0, 0, 0, 0, 0, 0, 0], [0, 16, 0, 0, 48, 0, 0, 0]],
    [[24, 0, 0, 0, 0, 24, 0, 0], [0, -8, 0, 0, -24, 0, 0, 0]],
    [[-24, 0, 0, 0, 0, -24, 0, 0], [0, -8, 0, 0, -24, 0, 0, 0]],
    [[-24, 0, 0, 0, 0, 24, 0, 0], [0, 8, 0, 0, -24, 0, 0, 0]],
    [[24, 0, 0, 0, 0, -24, 0, 0], [0, 8, 0, 0, -24, 0, 0, 0]],
]
BRIDGE_NEIGHBORS = [
    [40, 51, 151, 168, 217, 220, 475],
    [149, 170, 262, 273, 298, 303, 429],
    [154, 157, 265, 266, 299, 300, 431],
    [162, 165, 269, 270, 301, 302, 433],
    [43, 44, 152, 159, 218, 477],
    [47, 48, 160, 167, 219, 479],
]


def pack_colors(text: str) -> bytes:
    if any(color not in "0123" for color in text):
        raise ValueError("a coloring uses a symbol outside 0,1,2,3")
    payload = bytearray((len(text) + 3) // 4)
    for index, color in enumerate(text):
        payload[index // 4] |= int(color) << (2 * (index % 4))
    return bytes(payload)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_witnesses", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    raw = json.loads(args.raw_witnesses.read_text(encoding="utf-8"))
    if raw["vertices"] != TOTAL_SIZE or raw["edges"] != 2482 or raw["base_vertices"] != BASE_SIZE:
        raise ValueError("raw graph census mismatch")
    if raw["edge_sha256"] != EXPECTED_EDGE_SHA256:
        raise ValueError("raw graph edge digest mismatch")
    scaled = []
    for row in raw["bridge_rows"]:
        point = []
        for coordinate in row["candidate"]:
            values = [Fraction(value) * SCALE for value in coordinate]
            if any(value.denominator != 1 for value in values):
                raise ValueError("a bridge coordinate is not integral at scale 96")
            point.append([int(value) for value in values])
        scaled.append(point)
    if scaled != BRIDGE_COORDINATES:
        raise ValueError("unexpected bridge coordinates")
    witnesses = raw["witnesses"]
    if len(witnesses) != BASE_SIZE or any(len(row) != TOTAL_SIZE - 1 for row in witnesses):
        raise ValueError("raw deletion-witness dimensions mismatch")
    payload = b"".join(pack_colors(row) for row in witnesses)
    certificate = {
        "format": "parts509-six-bridge-augmentation-minimum-v1",
        "claim": "For every subset C of the six listed bridge points, the strict graph on the Parts points union C has minimum non-4-colourable induced order 509.",
        "scale": SCALE,
        "basis_radicands": [1, 3, 5, 15, 11, 33, 55, 165],
        "base_vertices": BASE_SIZE,
        "bridge_vertices": 6,
        "vertices": TOTAL_SIZE,
        "edges": 2482,
        "edge_sha256": EXPECTED_EDGE_SHA256,
        "bridge_coordinates_scaled96": BRIDGE_COORDINATES,
        "bridge_neighbors": BRIDGE_NEIGHBORS,
        "bridge_degrees": [len(row) for row in BRIDGE_NEIGHBORS],
        "bridge_internal_edges": [],
        "base_deletion_colorings_base64": base64.b64encode(payload).decode("ascii"),
        "coloring_rows": BASE_SIZE,
        "coloring_row_length": TOTAL_SIZE - 1,
        "minimum_non_four_colorable_order": BASE_SIZE,
        "augmentation_subsets_closed": 64,
    }
    args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
