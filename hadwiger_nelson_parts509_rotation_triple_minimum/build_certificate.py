#!/usr/bin/env python3
"""Compact raw search checkpoints into the solver-free theorem certificate."""

from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path


EXPECTED_EDGE_SHA256 = "cc3f6ad98f3d1198b6bde17628326d690b17789bd880f84303a2c6ff58be454f"
EXPECTED_FREE = [
    374, 375, 376, 383, 385, 387, 389, 390, 391, 392, 393, 394, 395,
    396, 412, 413, 414, 415, 416, 429, 431, 433, 453, 454, 455, 456,
    457, 458, 471, 472, 473, 474, 475, 477, 479, 493, 494, 495, 496,
    509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521,
    522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532,
]


def pack_colors(text: str) -> str:
    if any(color not in "0123" for color in text):
        raise ValueError("a colouring uses a symbol outside 0,1,2,3")
    data = bytearray((len(text) + 3) // 4)
    for index, color in enumerate(text):
        data[index // 4] |= int(color) << (2 * (index % 4))
    return base64.b64encode(data).decode("ascii")


def minimal_rows(rows: list[dict]) -> list[dict]:
    """Keep one witness for every inclusion-minimal deletion set."""
    kept: list[dict] = []
    kept_sets: list[frozenset[int]] = []
    seen: set[frozenset[int]] = set()
    for row in sorted(rows, key=lambda item: (len(item["D"]), item["D"])):
        deleted = frozenset(row["D"])
        if not deleted or deleted in seen:
            continue
        seen.add(deleted)
        if any(old <= deleted for old in kept_sets):
            continue
        kept_sets.append(deleted)
        kept.append(row)
    return kept


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("forced_checkpoint", type=Path)
    parser.add_argument("ihs_checkpoint", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    forced_data = json.loads(args.forced_checkpoint.read_text(encoding="utf-8"))
    ihs_data = json.loads(args.ihs_checkpoint.read_text(encoding="utf-8"))
    for data in (forced_data, ihs_data):
        if data["union_edge_sha256"] != EXPECTED_EDGE_SHA256:
            raise ValueError("checkpoint edge digest mismatch")
        if data["events"] != [108, 109, 789]:
            raise ValueError("checkpoint event mismatch")
    forced = forced_data["forced"]
    if forced != ihs_data["forced"] or forced != sorted(set(forced)) or len(forced) != 470:
        raise ValueError("forced lists disagree")
    free = forced_data["unforced"]
    if free != EXPECTED_FREE or free != sorted(set(range(533)) - set(forced)):
        raise ValueError("free list mismatch")
    if ihs_data["status"] != "theorem" or ihs_data["target_optional"] != 38:
        raise ValueError("target-cardinality search did not prove the target")

    forced_witnesses = []
    for vertex in forced:
        row = forced_data["results"][str(vertex)]
        witness = row["witness"]
        if row["status"] != "SAT" or not isinstance(witness, str) or len(witness) != 532:
            raise ValueError(f"missing deletion witness for vertex {vertex}")
        forced_witnesses.append(witness)

    rows = minimal_rows(ihs_data["family"])
    if len(rows) != 330:
        raise ValueError(f"expected 330 inclusion-minimal killing sets, got {len(rows)}")
    killing_sets = []
    for row in rows:
        deleted = sorted(row["D"])
        witness = row["witness"]
        if not set(deleted) <= set(free) or len(witness) != 533 - len(deleted):
            raise ValueError("malformed killing-set witness")
        killing_sets.append({"deleted": deleted, "coloring_base64": pack_colors(witness)})

    certificate = {
        "format": "parts509-exceptional-rotation-triple-minimum-v1",
        "claim": "The strict 108/109/789 and 215/216/690 placement unions have identical canonical edge arrays, and each has minimum non-4-colourable induced order 509.",
        "events": [108, 109, 789],
        "equivalent_events": [215, 216, 690],
        "vertices": 533,
        "edges": 2607,
        "edge_sha256": EXPECTED_EDGE_SHA256,
        "forced_vertices": forced,
        "free_vertices": free,
        "forced_colorings_base64": pack_colors("".join(forced_witnesses)),
        "forced_coloring_row_length": 532,
        "killing_sets": killing_sets,
        "transversal_search_nodes": 73946,
        "certificate_generation": {
            "initial_ihs_seed": 1,
            "target_cegar_seed": 3,
            "raw_killing_sets": len(ihs_data["family"]),
            "target_cegar_rounds": len(ihs_data["history"]),
        },
    }
    args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
