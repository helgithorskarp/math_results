#!/usr/bin/env python3
"""Deterministically generate deletion-colouring witnesses for T375."""

from __future__ import annotations

import base64
import hashlib
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "hadwiger_nelson_small_triangle_forcer375"
sys.path.insert(0, str(PARENT))

from colour_check import solve  # noqa: E402
from geometry import graph  # noqa: E402


def pack(word: list[int]) -> bytes:
    out = bytearray((len(word) + 3) // 4)
    for i, colour in enumerate(word):
        if type(colour) is not int or not 0 <= colour < 4:
            raise ValueError("bad colour")
        out[i // 4] |= colour << (2 * (i % 4))
    return bytes(out)


def main() -> None:
    points, edges = graph()
    if len(points) != 375 or len(edges) != 1661:
        raise RuntimeError("parent graph mismatch")
    rows = []
    raw = bytearray()
    total_nodes = total_conflicts = maximum_nodes = 0
    for deleted in range(3, 375):
        active_edges = [edge for edge in edges if deleted not in edge]
        word, stats = solve(375, active_edges, [(0, 0), (1, 0), (2, 0)])
        if word is None:
            raise RuntimeError(f"deletion {deleted} still forces the marked relation")
        word[deleted] = 0  # canonical ignored slot
        data = pack(word)
        raw.extend(data)
        rows.append([deleted, base64.b64encode(data).decode("ascii")])
        total_nodes += stats["nodes"]
        total_conflicts += stats["conflicts"]
        maximum_nodes = max(maximum_nodes, stats["nodes"])
    certificate = {
        "schema": "t375-terminal-monochromatic-deletion-colourings-v1",
        "vertices": 375,
        "edges": 1661,
        "terminals": [0, 1, 2],
        "packing": "four 2-bit colours per byte, low vertex first; deleted slot is zero",
        "colourings": rows,
        "packed_words_sha256": hashlib.sha256(raw).hexdigest(),
        "producer_statistics": {
            "queries": len(rows),
            "total_nodes": total_nodes,
            "total_conflicts": total_conflicts,
            "maximum_nodes": maximum_nodes,
        },
    }
    (HERE / "certificate.json").write_text(
        json.dumps(certificate, sort_keys=True, separators=(",", ":")) + "\n"
    )
    print(json.dumps(certificate["producer_statistics"], sort_keys=True))
    print(certificate["packed_words_sha256"])


if __name__ == "__main__":
    main()
