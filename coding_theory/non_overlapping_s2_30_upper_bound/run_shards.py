#!/usr/bin/env python3
"""Run and validate deterministic quadratic-box proof shards."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess


SCALAR_KEYS = (
    "n",
    "free_layers",
    "start_level",
    "upper_bound",
    "shard",
    "shards",
    "prefixes_seen",
    "prefixes_evaluated",
    "orientation_polynomials",
    "positive_cross_terms",
    "maximizing_mask",
    "constant",
)
VECTOR_KEYS = ("prefix_L", "prefix_R", "highs", "linear", "quadratic")


def run_one(binary: str, n: int, free_layers: int,
            shard: int, shards: int) -> dict[str, object]:
    completed = subprocess.run(
        [binary, str(n), str(free_layers), str(shard), str(shards)],
        check=True,
        capture_output=True,
        text=True,
    )
    fields: dict[str, object] = {}
    for line in completed.stdout.splitlines():
        key, _, value = line.partition(" ")
        if key == "elapsed_seconds":
            fields[key] = float(value)
        elif key in VECTOR_KEYS:
            fields[key] = [int(part) for part in value.split()]
        elif key in SCALAR_KEYS:
            fields[key] = int(value)
    missing = set(SCALAR_KEYS + VECTOR_KEYS + ("elapsed_seconds",)) - fields.keys()
    if missing:
        raise AssertionError(f"shard {shard} omitted fields {sorted(missing)}")
    return fields


def merge(records: list[dict[str, object]], n: int,
          free_layers: int, shards: int) -> dict[str, object]:
    assert len(records) == shards
    records.sort(key=lambda record: int(record["shard"]))
    assert [record["shard"] for record in records] == list(range(shards))
    assert all(record["n"] == n for record in records)
    assert all(record["free_layers"] == free_layers for record in records)
    assert all(record["shards"] == shards for record in records)
    starts = {int(record["start_level"]) for record in records}
    seen = {int(record["prefixes_seen"]) for record in records}
    assert len(starts) == len(seen) == 1
    start_level = starts.pop()
    prefixes_seen = seen.pop()

    counts = [int(record["prefixes_evaluated"]) for record in records]
    assert sum(counts) == prefixes_seen
    assert max(counts) - min(counts) <= 1
    polynomial_total = sum(
        int(record["orientation_polynomials"]) for record in records
    )
    assert polynomial_total == prefixes_seen * (1 << (free_layers - 1))
    assert all(
        int(record["orientation_polynomials"])
        == int(record["prefixes_evaluated"]) * (1 << (free_layers - 1))
        for record in records
    )

    bounds = [int(record["upper_bound"]) for record in records]
    winner = max(range(shards), key=lambda index: bounds[index])
    winning = records[winner]
    return {
        "status": "PASS",
        "n": n,
        "free_layers": free_layers,
        "start_level": start_level,
        "shards": shards,
        "upper_bound": bounds[winner],
        "prefixes_seen": prefixes_seen,
        "prefixes_evaluated": sum(counts),
        "orientation_polynomials": polynomial_total,
        "positive_cross_terms": sum(
            int(record["positive_cross_terms"]) for record in records
        ),
        "shard_prefix_counts": counts,
        "shard_upper_bounds": bounds,
        "maximizing_shard": winner,
        "maximizing_mask": winning["maximizing_mask"],
        "prefix_L": winning["prefix_L"],
        "prefix_R": winning["prefix_R"],
        "highs": winning["highs"],
        "constant": winning["constant"],
        "linear": winning["linear"],
        "quadratic": winning["quadratic"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--free-layers", type=int, required=True)
    parser.add_argument("--shards", type=int, required=True)
    parser.add_argument("--expected", type=Path)
    args = parser.parse_args()

    with ThreadPoolExecutor(max_workers=args.shards) as executor:
        records = list(executor.map(
            lambda shard: run_one(
                args.binary, args.n, args.free_layers, shard, args.shards
            ),
            range(args.shards),
        ))
    result = merge(records, args.n, args.free_layers, args.shards)
    if args.expected:
        expected = json.loads(args.expected.read_text())
        assert result == expected, (result, expected)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
