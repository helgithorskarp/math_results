#!/usr/bin/env python3
"""Verify the deterministic row stream and its complete edge-stratified census."""

from __future__ import annotations

import hashlib
import sys
from collections import defaultdict
from pathlib import Path


CATALOGUE_SHA256 = "83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0"
ROWS_SHA256 = "0620bc947873e32c8eb7aa9dd3e0c78af3426552e3f177fc1d1870aaac8da628"
EXPECTED = {
    116: (9, -2364, -2048),
    117: (90, -2350, -1968),
    118: (806, -2324, -1748),
    119: (4358, -2304, -1660),
    120: (16346, -2284, -1522),
    121: (43457, -2155, -1420),
    122: (79678, -2026, -1302),
    123: (92504, -1800, -1203),
    124: (67209, -1704, -1104),
    125: (31996, -1478, -1016),
    126: (11485, -1356, -918),
    127: (3401, -1209, -864),
    128: (843, -1062, -748),
    129: (147, -915, -626),
    130: (32, -768, -590),
    131: (3, -636, -636),
    132: (2, -528, -528),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: verify.py CATALOGUE.g6 ROWS")
    catalogue, rows = map(Path, sys.argv[1:])
    assert sha256(catalogue) == CATALOGUE_SHA256, "unexpected catalogue SHA-256"
    assert sha256(rows) == ROWS_SHA256, "unexpected row-stream SHA-256"
    summary: dict[int, list[int]] = defaultdict(lambda: [0, 10**18, -10**18])
    total = 0
    with rows.open() as stream:
        for expected_index, line in enumerate(stream):
            fields = list(map(int, line.split()))
            assert len(fields) == 6, "wrong row width"
            index, edges, triangles, t31, t32, r12 = fields
            assert index == expected_index, "nonconsecutive row index"
            assert r12 == -129 * triangles + 6 * t31 + 16 * t32
            assert r12 < 0, "nonnegative fourth-order summand"
            record = summary[edges]
            record[0] += 1
            record[1] = min(record[1], r12)
            record[2] = max(record[2], r12)
            total += 1
    observed = {edges: tuple(values) for edges, values in summary.items()}
    assert total == 352366
    assert observed == EXPECTED
    print("verified=1 records=352366 min_r12=-2364 max_r12=-528")


if __name__ == "__main__":
    main()
