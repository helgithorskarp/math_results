#!/usr/bin/env python3
"""Enumerate spanning nonzero column-support orbits for one row stabilizer."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from joint_completion import dual_map, edge_rank, image_mask, row_orbits, stabilizer


def valid(mask: int) -> bool:
    labels = [value for value in range(1, 16) if mask & (1 << (value - 1))]
    return len(labels) >= 5 and edge_rank(labels, 4) == 4


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--masks", type=Path, required=True)
    args = parser.parse_args()
    rows, row_census = row_orbits()
    row = rows[args.orbit]
    row_group = stabilizer(row)
    group = [dual_map(transformation) for transformation in row_group]
    remaining = {mask for mask in range(1 << 15) if valid(mask)}
    valid_count = len(remaining)
    records = []
    while remaining:
        seed = min(remaining)
        orbit = {image_mask(seed, transformation) for transformation in group}
        if not orbit <= remaining | {item["mask"] for item in records}:
            raise RuntimeError("support orbit left the valid family")
        members = orbit & remaining
        representative = min(orbit)
        if seed != representative:
            raise RuntimeError("minimum remaining support was not canonical")
        remaining -= members
        records.append({
            "mask": representative,
            "labels": [value for value in range(1, 16)
                       if representative & (1 << (value - 1))],
            "orbit_size": len(orbit),
            "support_size": representative.bit_count(),
        })
    if sum(record["orbit_size"] for record in records) != valid_count:
        raise RuntimeError("support orbits do not cover all valid masks")
    by_size = Counter(record["support_size"] for record in records)
    result = {
        "schema": "rank4-row-full-support-orbits-v1",
        "row_orbit": row,
        "row_orbit_census": row_census,
        "row_stabilizer_size": len(row_group),
        "column_action": "inverse-transpose of row stabilizer",
        "valid_support_masks": valid_count,
        "support_orbits": len(records),
        "support_orbits_by_size": dict(sorted(by_size.items())),
        "orbit_size_sum": sum(record["orbit_size"] for record in records),
        "records": records,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    args.masks.write_text("".join(f"{record['mask']}\n" for record in records))
    print(json.dumps({key: value for key, value in result.items()
                      if key != "records"}, sort_keys=True))


if __name__ == "__main__":
    main()
