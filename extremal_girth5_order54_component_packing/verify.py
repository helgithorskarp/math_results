#!/usr/bin/env python3
"""Audit the sharp equality signatures for high path-component packing.

The checker covers the six unordered pairs P_r,P_s with 1 <= r <= s <= 3.
It is a finite audit of the table and sharp set systems, not a computational
proof of the universal graph theorem in README.md.
"""

from __future__ import annotations

import json
from itertools import combinations


def path_degrees(order: int) -> list[int]:
    if not 1 <= order <= 3:
        raise ValueError("path order must lie in 1..3")
    if order == 1:
        return [0]
    return [1] + [2] * (order - 2) + [1]


def pairwise_disjoint(family: list[set[str]]) -> bool:
    return all(not (left & right) for left, right in combinations(family, 2))


def threshold(r: int, s: int) -> int:
    return 5 * (r + s) - r * s - 8


def sharp_signature(r: int, s: int) -> tuple[list[set[str]], list[set[str]]]:
    """Construct the canonical grid-plus-private-points equality system."""
    grid = [[f"x_{i}_{j}" for j in range(s)] for i in range(r)]
    rows: list[set[str]] = []
    for i, degree in enumerate(path_degrees(r)):
        private_count = 3 + degree - s
        if private_count < 0:
            raise RuntimeError("negative row-private count")
        rows.append(
            set(grid[i]) | {f"row_{i}_private_{k}" for k in range(private_count)}
        )

    columns: list[set[str]] = []
    for j, degree in enumerate(path_degrees(s)):
        private_count = 3 + degree - r
        if private_count < 0:
            raise RuntimeError("negative column-private count")
        columns.append(
            {grid[i][j] for i in range(r)}
            | {f"column_{j}_private_{k}" for k in range(private_count)}
        )
    return rows, columns


def audit_pair(r: int, s: int, rows: list[set[str]], columns: list[set[str]]) -> dict:
    if len(rows) != r or len(columns) != s:
        raise ValueError("wrong number of component neighborhoods")
    expected_rows = [3 + degree for degree in path_degrees(r)]
    expected_columns = [3 + degree for degree in path_degrees(s)]
    if [len(block) for block in rows] != expected_rows:
        raise ValueError("wrong row neighborhood sizes")
    if [len(block) for block in columns] != expected_columns:
        raise ValueError("wrong column neighborhood sizes")
    if not pairwise_disjoint(rows) or not pairwise_disjoint(columns):
        raise ValueError("component neighborhoods are not internally disjoint")

    cells = [[rows[i] & columns[j] for j in range(s)] for i in range(r)]
    if any(len(cell) > 1 for line in cells for cell in line):
        raise ValueError("a cross pair has two common neighbors")

    row_union = set().union(*rows)
    column_union = set().union(*columns)
    ground = row_union | column_union
    expected_ground = threshold(r, s) + 4
    if len(ground) != expected_ground:
        raise ValueError("sharp signature has the wrong ground-set size")
    if any(len(cell) != 1 for line in cells for cell in line):
        raise ValueError("sharp signature is missing a cross-grid point")

    return {
        "components": [r, s],
        "threshold_z": threshold(r, s),
        "structural_minimum_z": max(r + s, threshold(r, s)),
        "ground_size": len(ground),
        "row_sizes": expected_rows,
        "column_sizes": expected_columns,
        "row_private": [len(block - column_union) for block in rows],
        "column_private": [len(block - row_union) for block in columns],
        "cross_cells": sum(len(cell) for line in cells for cell in line),
    }


def main() -> None:
    table = []
    for r in range(1, 4):
        for s in range(r, 4):
            rows, columns = sharp_signature(r, s)
            table.append(audit_pair(r, s, rows, columns))

    rows, columns = sharp_signature(2, 3)
    malformed = [set(block) for block in columns]
    stolen = next(iter(rows[0] - set().union(*columns)))
    replaced = next(iter(malformed[0] - set().union(*rows)))
    malformed[0].remove(replaced)
    malformed[0].add(stolen)
    try:
        audit_pair(2, 3, rows, malformed)
    except ValueError as error:
        malformed_control = str(error)
    else:
        raise RuntimeError("malformed double intersection was not rejected")

    report = {
        "single_component_thresholds": {"P1": -1, "P2": 4, "P3": 9},
        "pair_signatures": table,
        "corollaries": {
            "z_le_4": "high graph edgeless",
            "z_5_to_7": "at most one high edge",
            "z_9_to_10_with_P3": "all other high vertices isolated",
            "z_11_with_P3_and_P2": "deficit-free 3-by-2 equality signature",
        },
        "malformed_control": malformed_control,
    }
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
