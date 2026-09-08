#!/usr/bin/env python3
"""Merge deterministic certifier shard summaries."""

from __future__ import annotations

import argparse
from pathlib import Path


def merge(inputs: list[Path], output: Path) -> None:
    records: dict[int, tuple[int, int, int, int]] = {}
    for path in inputs:
        lines = path.read_text().splitlines()
        if not lines or lines[0] != "record\troots\tunsat\tclauses\tproof_bytes":
            raise ValueError(f"bad header: {path}")
        if not lines[-1].startswith("TOTAL\t"):
            raise ValueError(f"incomplete shard: {path}")
        for line in lines[1:-1]:
            record, roots, unsat, clauses, proof_bytes = map(int, line.split("\t"))
            if record in records:
                raise ValueError(f"duplicate record {record}")
            records[record] = roots, unsat, clauses, proof_bytes
    if sorted(records) != list(range(2178)):
        raise ValueError("shards do not cover records 0..2177 exactly")
    rows = [(record, *records[record]) for record in sorted(records)]
    totals = tuple(sum(row[column] for row in rows) for column in range(1, 5))
    with output.open("w") as result:
        result.write("record\troots\tunsat\tclauses\tproof_bytes\n")
        for row in rows:
            result.write("\t".join(map(str, row)) + "\n")
        result.write("TOTAL\t" + "\t".join(map(str, totals)) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("inputs", type=Path, nargs="+")
    args = parser.parse_args()
    merge(args.inputs, args.output)


if __name__ == "__main__":
    main()
