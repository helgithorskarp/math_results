#!/usr/bin/env python3
"""Definition-level audit of the P84 exclusion ledger and generated traces.

This file does not import the reviewed Python or C++ code.  With --work it
also parses every nonempty-query trace record independently and checks it
against the regenerated heavy catalog.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import struct
from collections import Counter
from pathlib import Path


EXPECTED = {
    "packings": 62_861_452,
    "calls1": 2,
    "calls2": 11_698,
    "calls3": 4_048_536,
    "calls4": 62_861_452,
    "candidates1": 0,
    "candidates2": 2,
    "candidates3": 11_698,
    "candidates4": 4_048_536,
    "found": 0,
}
CAP = 2_000_000
TOTAL_WEIGHT = 15_685_948
THRESHOLD = TOTAL_WEIGHT - 4 * CAP
CUTOFF = (THRESHOLD - 2 * CAP + 1) // 2
UNIVERSE = (1 << 84) - 1


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def sidon(row: tuple[int, ...] | list[int]) -> bool:
    sums = [a + b for i, a in enumerate(row) for b in row[i:]]
    return len(sums) == len(set(sums))


def as_mask(row: tuple[int, ...] | list[int]) -> int:
    return sum(1 << point for point in row)


def load_weights(path: Path) -> tuple[list[int], list[list[int]]]:
    weights = list(map(int, path.read_text(encoding="ascii").split()))
    assert len(weights) == 84
    assert weights == weights[::-1]
    assert sum(weights) == TOTAL_WEIGHT
    tables: list[list[int]] = []
    for chunk in range(7):
        local = weights[12 * chunk : 12 * (chunk + 1)]
        table = [0] * 4096
        for mask in range(1, 4096):
            bit = mask & -mask
            table[mask] = table[mask ^ bit] + local[bit.bit_length() - 1]
        tables.append(table)
    return weights, tables


def mask_weight(mask: int, tables: list[list[int]]) -> int:
    return sum(table[(mask >> (12 * chunk)) & 4095] for chunk, table in enumerate(tables))


def audit_cases(path: Path, prior_path: Path) -> list[dict[str, int]]:
    with path.open(encoding="ascii", newline="") as stream:
        rows = [{key: int(value) for key, value in row.items()} for row in csv.DictReader(stream)]
    assert len(rows) == 1488
    assert [row["orbit"] for row in rows] == list(range(1488))
    totals = {key: sum(row[key] for row in rows) for key in EXPECTED}
    assert totals == EXPECTED
    assert sum(row["packings"] == 0 for row in rows) == 64
    assert [row["orbit"] for row in rows if row["calls1"]] == [2, 23]
    for row in rows:
        assert row["found"] == row["candidates1"] == 0
        assert row["calls4"] == row["packings"]
        assert row["calls3"] == row["candidates4"]
        assert row["calls2"] == row["candidates3"]
        assert row["calls1"] == row["candidates2"]
    with prior_path.open(encoding="ascii", newline="") as stream:
        prior = list(csv.DictReader(stream))
    assert len(prior) == len(rows)
    assert all(row["packings"] == int(old["anchored_packings"]) for row, old in zip(rows, prior))
    return rows


def audit_terminal_basic(path: Path) -> list[dict[str, object]]:
    terminals = json.loads(path.read_text(encoding="ascii"))
    assert len(terminals) == 2
    assert [row["eleven_ids"][0] // 2 for row in terminals] == [2, 23]
    for row in terminals:
        chosen = row["chosen_tens"]
        residual = row["residual"]
        assert len(chosen) == 3
        assert all(len(block) == 10 and sidon(block) for block in chosen)
        assert len(residual) == 10 and not sidon(residual) and row["sidon"] is False
        left, right = row["collision"]
        assert sum(left) == sum(right)
        assert left != right
    return terminals


def audit_terminal_full(
    terminals: list[dict[str, object]], orbit_path: Path, weights: list[int]
) -> None:
    orbit_rows = [
        tuple(map(int, line.split()))
        for line in orbit_path.read_text(encoding="ascii").splitlines()
    ]
    assert len(orbit_rows) == 30_510
    for terminal in terminals:
        ids = terminal["eleven_ids"]
        assert ids[0] % 2 == 0 and ids == sorted(ids) and all(i >= ids[0] for i in ids)
        elevens = [orbit_rows[index] for index in ids]
        assert all(len(block) == 11 and sidon(block) for block in elevens)
        assert sum(sum(weights[x] for x in block) for block in elevens) >= THRESHOLD
        blocks = [*elevens, *terminal["chosen_tens"], terminal["residual"]]
        points = [point for block in blocks for point in block]
        assert sorted(points) == list(range(84)) and len(set(points)) == 84

        domain = UNIVERSE
        for block in elevens:
            domain ^= as_mask(block)
        upper = CAP
        for k, block in zip((4, 3, 2), terminal["chosen_tens"]):
            block_mask = as_mask(block)
            block_weight = sum(weights[x] for x in block)
            lower = (mask_weight(domain, _weight_tables) + k - 1) // k
            assert block_mask & domain == block_mask
            assert lower >= CUTOFF and lower <= block_weight <= upper
            domain ^= block_mask
            upper = block_weight
        residual = as_mask(terminal["residual"])
        assert domain == residual and mask_weight(domain, _weight_tables) <= upper


def load_heavy(path: Path, weights: list[int]) -> dict[int, int]:
    raw = path.read_bytes()
    assert len(raw) == 901_286 * 10
    catalog: dict[int, int] = {}
    previous = -1
    for offset in range(0, len(raw), 10):
        row = tuple(raw[offset : offset + 10])
        assert len(set(row)) == 10 and list(row) == sorted(row) and row[-1] < 84
        mask = as_mask(row)
        assert mask > previous and sidon(row)
        value = sum(weights[x] for x in row)
        assert CUTOFF <= value <= CAP
        catalog[mask] = value
        previous = mask
    assert len(catalog) == 901_286
    return catalog


def audit_trace(path: Path, catalog: dict[int, int], tables: list[list[int]]) -> tuple[Counter, Counter]:
    raw = path.read_bytes()
    view = memoryview(raw)
    offset = 0
    records: Counter[int] = Counter()
    options: Counter[int] = Counter()
    while offset < len(view):
        assert offset + 40 <= len(view)
        low, high, k, upper, count = struct.unpack_from("<QQQQQ", view, offset)
        offset += 40
        domain = low | (high << 64)
        assert domain <= UNIVERSE and k in (2, 3, 4) and domain.bit_count() == 10 * k
        lower = (mask_weight(domain, tables) + k - 1) // k
        assert lower >= CUTOFF and lower <= upper <= CAP and count > 0
        records[k] += 1
        options[k] += count
        previous = -1
        assert offset + 16 * count <= len(view)
        for _ in range(count):
            lo, hi = struct.unpack_from("<QQ", view, offset)
            offset += 16
            candidate = lo | (hi << 64)
            assert candidate > previous
            assert candidate & domain == candidate and candidate.bit_count() == 10
            value = catalog[candidate]
            assert lower <= value <= upper
            previous = candidate
    assert offset == len(view)
    return records, options


def same_bytes(left: Path, right: Path) -> None:
    assert left.stat().st_size == right.stat().st_size
    assert digest(left) == digest(right)


def audit_work(work: Path, weights: list[int], tables: list[list[int]]) -> None:
    assert (work / "verification.json").exists()
    same_bytes(work / "full_0.bin", work / "full_1.bin")
    same_bytes(work / "heavy_0.bin", work / "heavy_1.bin")
    catalog = load_heavy(work / "heavy_0.bin", weights)
    combined_records: Counter[int] = Counter()
    combined_options: Counter[int] = Counter()
    for shard in range(4):
        left = work / f"sweep_0_{shard}.bin"
        right = work / f"sweep_1_{shard}.bin"
        same_bytes(left, right)
        same_bytes(work / f"sweep_0_{shard}.jsonl", work / f"sweep_1_{shard}.jsonl")
        assert (work / f"sweep_0_{shard}.done").read_text() == "complete\n"
        assert (work / f"sweep_1_{shard}.done").read_text() == "complete\n"
        records, options = audit_trace(left, catalog, tables)
        combined_records.update(records)
        combined_options.update(options)
    assert combined_options == Counter({4: 4_048_536, 3: 11_698, 2: 2})
    print("trace_records=" + ",".join(f"k{k}:{combined_records[k]}" for k in (4, 3, 2)))
    print("trace_options=k4:4048536,k3:11698,k2:2")


_weight_tables: list[list[int]]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--prior-cases", type=Path, required=True)
    parser.add_argument("--terminal", type=Path, required=True)
    parser.add_argument("--weights", type=Path, required=True)
    parser.add_argument("--work", type=Path)
    args = parser.parse_args()

    global _weight_tables
    weights, _weight_tables = load_weights(args.weights)
    audit_cases(args.cases, args.prior_cases)
    terminals = audit_terminal_basic(args.terminal)
    if args.work is not None:
        same_bytes(args.cases, args.work / "cases.csv")
        same_bytes(args.terminal, args.work / "terminal_checks.json")
        audit_terminal_full(terminals, args.work / "orbit_catalog.txt", weights)
        audit_work(args.work, weights, _weight_tables)
    print("independent_p84_exclusion_audit=PASS")
    print("cases=1488 packing_empty_cases=64 packings=62861452 found=0")
    print("calls=k4:62861452,k3:4048536,k2:11698,k1:2")
    print("candidate_occurrences=k4:4048536,k3:11698,k2:2")
    print("terminal_anchor_cases=2,23 terminal_residuals_nonsidon=2")
    print(f"cases_sha256={digest(args.cases)}")
    print(f"terminal_sha256={digest(args.terminal)}")
    if args.work is not None:
        print("heavy_catalog=901286 full_and_heavy_catalog_pairs_byte_equal=true")
        print("query_method_trace_pairs_byte_equal=true terminal_partitions=PASS")


if __name__ == "__main__":
    main()
