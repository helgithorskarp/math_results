#!/usr/bin/env python3
"""Compare fresh one-parent solver outputs with the committed radius-six map."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


MAP_SHA256 = "ea3dd948e333153f0bf844e279d7df2788849dfe676d6e45af1aaf74e1e29e72"
COUNT_SHA256 = "04913efaaeda358e58b33f8eab437637804ad1be05cf18808bfbd94078cea2f8"
PARENTS = (0, 23, 190, 241)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_graph6(record: str) -> list[int]:
    assert record and ord(record[0]) - 63 == 42
    bits = []
    for character in record[1:]:
        value = ord(character) - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    assert len(bits) >= 861
    return bits[:861]


def encode_graph6(bits: list[int]) -> str:
    output = [chr(42 + 63)]
    for start in range(0, 861, 6):
        chunk = bits[start:start + 6]
        chunk += [0] * (6 - len(chunk))
        value = sum(bit << (5 - index) for index, bit in enumerate(chunk))
        output.append(chr(value + 63))
    return "".join(output)


def edge_index(encoded: str) -> int:
    low, high = map(int, encoded.split(","))
    assert 0 <= low < high < 42
    return high * (high - 1) // 2 + low


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("sample_directory", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    target = root / "ramsey_r55_catalog_edge_radius6_classification"
    map_path = target / "EDGE_RADIUS6_MAP.tsv"
    count_path = target / "EXPECTED_PARENT_COUNTS.txt"
    assert sha256(map_path) == MAP_SHA256 and sha256(count_path) == COUNT_SHA256
    catalog = (target / "r55_42some.g6").read_text(encoding="ascii").splitlines()

    expected: dict[int, set[tuple[int, ...]]] = {parent: set() for parent in PARENTS}
    for line in map_path.read_text(encoding="ascii").splitlines()[1:]:
        if line.startswith("# SUMMARY "):
            break
        fields = line.split("\t")
        parent = int(fields[0])
        if parent in expected:
            expected[parent].add(tuple(edge_index(value) for value in fields[1:7]))

    logged = {}
    for line in count_path.read_text(encoding="ascii").splitlines():
        fields = dict(item.split("=", 1) for item in line.split())
        logged[int(fields["parent"])] = (int(fields["exact6"]), int(fields["lower_models"]))

    total = 0
    for parent in PARENTS:
        actual = set()
        for line in (args.sample_directory / f"parent-{parent}.tsv").read_text(encoding="ascii").splitlines():
            fields = line.split("\t")
            assert len(fields) == 8 and int(fields[0]) == parent
            edges = tuple(edge_index(value) for value in fields[1:7])
            assert edges == tuple(sorted(edges)) and len(set(edges)) == 6
            assert edges not in actual
            actual.add(edges)
            bits = decode_graph6(catalog[parent])
            for edge in edges:
                bits[edge] ^= 1
            assert encode_graph6(bits) == fields[7]
        assert actual == expected[parent]
        log = (args.sample_directory / f"parent-{parent}.log").read_text(encoding="ascii")
        match = re.search(rf"parent={parent} exact6=(\d+) lower_models=(\d+)", log)
        assert match and tuple(map(int, match.groups())) == logged[parent]
        total += len(actual)

    print(json.dumps({
        "all_checks": True,
        "exact_set_match": True,
        "parents": list(PARENTS),
        "raw_graph6_match": True,
        "sample_transitions": total,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
