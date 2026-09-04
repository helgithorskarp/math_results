#!/usr/bin/env python3
"""Extract the deterministic L and S+ positive-colouring libraries."""

from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CRITICALITY = ROOT / "hadwiger_nelson_parts509_criticality" / "certificate.json"
FLEXIBILITY = ROOT / "hadwiger_nelson_parts509_splus_single_cross_flexibility" / "certificate.json"


def unpack_deletion_rows(encoded: str) -> list[list[int | None]]:
    data = base64.b64decode(encoded, validate=True)
    vertex_count = 509
    row_bytes = 127
    if len(data) != vertex_count * row_bytes:
        raise ValueError("bad packed deletion-colouring length")
    rows = []
    for deleted in range(vertex_count):
        block = data[deleted * row_bytes : (deleted + 1) * row_bytes]
        unpacked = [
            (byte >> shift) & 3
            for byte in block
            for shift in (0, 2, 4, 6)
        ]
        if len(unpacked) != vertex_count - 1:
            raise ValueError("bad deletion-colouring row length")
        iterator = iter(unpacked)
        rows.append([
            None if vertex == deleted else next(iterator)
            for vertex in range(vertex_count)
        ])
    return rows


def unpack_splus(encoded: str) -> list[int]:
    data = base64.b64decode(encoded, validate=True)
    if len(data) != 34:
        raise ValueError("bad packed S+ colouring length")
    return [(data[index // 4] >> (2 * (index % 4))) & 3 for index in range(136)]


def library_bytes() -> bytes:
    criticality = json.loads(CRITICALITY.read_text(encoding="utf-8"))
    flexibility = json.loads(FLEXIBILITY.read_text(encoding="utf-8"))
    deletion_rows = unpack_deletion_rows(criticality["deletion_colorings_base64"])
    lines = []
    for deleted in range(374, 509):
        row = deletion_rows[deleted][:374]
        if any(colour is None for colour in row):
            raise ValueError("L restriction contains the deleted vertex")
        lines.append("L:" + "".join(str(colour) for colour in row))
    lines.extend(
        "S:" + "".join(map(str, unpack_splus(encoded)))
        for encoded in flexibility["s_colorings"]
    )
    if len(lines) != 135 + 194:
        raise ValueError("colour-library census mismatch")
    return ("\n".join(lines) + "\n").encode("ascii")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", type=Path, default=Path("colour_libraries.txt"))
    args = parser.parse_args()
    args.output.write_bytes(library_bytes())
    print(f"L_colourings=135 Splus_colourings=194 output={args.output}")


if __name__ == "__main__":
    main()
