#!/usr/bin/env python3
"""Audit the sharp set-system signature in the two-high-P3 packing lemma.

This script is not a computational proof of the universal theorem.  It
checks its exact boundary construction and the arithmetic consequences
reported in README.md, using only Python sets and integers.
"""

from __future__ import annotations

import json
from itertools import combinations


def pairwise_disjoint(family: list[set[str]]) -> bool:
    return all(not (left & right) for left, right in combinations(family, 2))


def audit_families(
    rows: list[set[str]], columns: list[set[str]]
) -> dict[str, object]:
    if len(rows) != 3 or len(columns) != 3:
        raise ValueError("each path must supply exactly three neighborhoods")
    if [len(block) for block in rows] != [4, 5, 4]:
        raise ValueError("row sizes are not the sink P3 sizes 4,5,4")
    if [len(block) for block in columns] != [4, 5, 4]:
        raise ValueError("column sizes are not the sink P3 sizes 4,5,4")
    if not pairwise_disjoint(rows) or not pairwise_disjoint(columns):
        raise ValueError("neighborhoods within a P3 must be disjoint")

    cells = [[rows[i] & columns[j] for j in range(3)] for i in range(3)]
    if any(len(cell) > 1 for line in cells for cell in line):
        raise ValueError("a cross pair has two common neighbors")

    row_union = set().union(*rows)
    column_union = set().union(*columns)
    return {
        "row_sizes": [len(block) for block in rows],
        "column_sizes": [len(block) for block in columns],
        "cross_intersection_sizes": [
            [len(cells[i][j]) for j in range(3)] for i in range(3)
        ],
        "row_union": len(row_union),
        "column_union": len(column_union),
        "intersection": len(row_union & column_union),
        "ground_set": len(row_union | column_union),
        "minimum_z": len(row_union | column_union) - 4,
    }


def sharp_signature() -> tuple[list[set[str]], list[set[str]]]:
    grid = [[f"x{i + 1}{j + 1}" for j in range(3)] for i in range(3)]
    rows = [
        set(grid[0]) | {"r1"},
        set(grid[1]) | {"r2a", "r2b"},
        set(grid[2]) | {"r3"},
    ]
    columns = [
        {grid[i][0] for i in range(3)} | {"c1"},
        {grid[i][1] for i in range(3)} | {"c2a", "c2b"},
        {grid[i][2] for i in range(3)} | {"c3"},
    ]
    return rows, columns


def main() -> None:
    rows, columns = sharp_signature()
    report = audit_families(rows, columns)

    malformed = [set(block) for block in columns]
    malformed[0].remove("c1")
    malformed[0].add("r1")
    try:
        audit_families(rows, malformed)
    except ValueError as error:
        rejected = str(error)
    else:
        raise RuntimeError("malformed double intersection was not rejected")

    report["malformed_control"] = rejected
    report["consequence_z_le_12"] = "two vertex-disjoint P3s impossible"
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
