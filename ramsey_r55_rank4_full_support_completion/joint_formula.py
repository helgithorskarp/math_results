#!/usr/bin/env python3
"""One SAT formula for every full-support doubled rank-four cut at once."""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


N = 43
ROW_BASE = range(0, 15)
ROW_EXTRA = range(15, 20)
COLUMN_BASE = range(20, 35)
COLUMN_EXTRA = range(35, 43)
PAIRS = list(combinations(range(N), 2))
EDGE = {pair: i + 1 for i, pair in enumerate(PAIRS)}
FIRST_SELECTOR = len(PAIRS) + 1
ROW_SELECT = {(i, x): FIRST_SELECTOR + i * 15 + x - 1
              for i in range(5) for x in range(1, 16)}
FIRST_COLUMN_SELECTOR = FIRST_SELECTOR + 5 * 15
COLUMN_SELECT = {(j, y): FIRST_COLUMN_SELECTOR + j * 15 + y - 1
                 for j in range(8) for y in range(1, 16)}
VARIABLES = len(PAIRS) + 5 * 15 + 8 * 15


def dot(x: int, y: int) -> int:
    return (x & y).bit_count() & 1


def exactly_one(selectors):
    selectors = list(selectors)
    yield selectors
    for a, b in combinations(selectors, 2):
        yield [-a, -b]


def clauses():
    # Full physical Ramsey constraints.
    for vertices in combinations(range(N), 5):
        edges = [EDGE[pair] for pair in combinations(vertices, 2)]
        yield [-e for e in edges]
        yield edges

    # The 15-by-15 core contains every nonzero label exactly once.
    for i in ROW_BASE:
        x = i + 1
        for j in COLUMN_BASE:
            y = j - 19
            edge = EDGE[(i, j)]
            yield [edge if dot(x, y) else -edge]

    # Each extra row/column gets one distinct label, listed increasingly.
    for i in range(5):
        yield from exactly_one(ROW_SELECT[(i, x)] for x in range(1, 16))
    for j in range(8):
        yield from exactly_one(COLUMN_SELECT[(j, y)] for y in range(1, 16))
    for i in range(4):
        for x in range(1, 16):
            for y in range(1, x + 1):
                yield [-ROW_SELECT[(i, x)], -ROW_SELECT[(i + 1, y)]]
    for j in range(7):
        for x in range(1, 16):
            for y in range(1, x + 1):
                yield [-COLUMN_SELECT[(j, x)], -COLUMN_SELECT[(j + 1, y)]]

    # Conditional cross colors involving selected duplicate labels.
    for i, vertex in enumerate(ROW_EXTRA):
        for x in range(1, 16):
            selector = ROW_SELECT[(i, x)]
            for column_vertex in COLUMN_BASE:
                y = column_vertex - 19
                edge = EDGE[(vertex, column_vertex)]
                yield [-selector, edge if dot(x, y) else -edge]
    for row_vertex in ROW_BASE:
        x = row_vertex + 1
        for j, vertex in enumerate(COLUMN_EXTRA):
            for y in range(1, 16):
                selector = COLUMN_SELECT[(j, y)]
                edge = EDGE[(row_vertex, vertex)]
                yield [-selector, edge if dot(x, y) else -edge]
    for i, row_vertex in enumerate(ROW_EXTRA):
        for j, column_vertex in enumerate(COLUMN_EXTRA):
            edge = EDGE[(row_vertex, column_vertex)]
            for x in range(1, 16):
                rs = ROW_SELECT[(i, x)]
                for y in range(1, 16):
                    cs = COLUMN_SELECT[(j, y)]
                    yield [-rs, -cs, edge if dot(x, y) else -edge]


def write_formula(path: Path) -> dict:
    expected_clauses = (2 * 962598 + 225 + 5 * 106 + 8 * 106 +
                        4 * 120 + 7 * 120 + 5 * 15 * 15 +
                        15 * 8 * 15 + 5 * 8 * 15 * 15)
    digest = sha256()
    count = 0
    with path.open("wb") as output:
        header = f"p cnf {VARIABLES} {expected_clauses}\n".encode("ascii")
        output.write(header)
        digest.update(header)
        for clause in clauses():
            raw = (" ".join(map(str, clause)) + " 0\n").encode("ascii")
            output.write(raw)
            digest.update(raw)
            count += 1
    if count != expected_clauses:
        raise RuntimeError(f"clause count {count} != {expected_clauses}")
    return {"variables": VARIABLES, "clauses": count,
            "bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--metadata", type=Path)
    args = parser.parse_args()
    result = write_formula(args.output)
    if args.metadata:
        args.metadata.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
