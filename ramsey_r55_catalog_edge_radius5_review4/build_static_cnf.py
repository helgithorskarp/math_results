#!/usr/bin/env python3
"""Build one static radius-five CNF with all known models blocked.

The resulting UNSAT formula certifies that the saved radius-one-through-five
maps contain every Ramsey-preserving flip set for the selected parent.  This
is a standard-library implementation and imports no submitted module.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
from pathlib import Path


ORDER = 42
EDGE_COUNT = ORDER * (ORDER - 1) // 2
VARIABLES = EDGE_COUNT + 6 * EDGE_COUNT
MAP_HASHES = {
    2: "5e1cafc6ba00cdf2bd48c8e4c45748ef29cc88328b1119dbda8898c58215afe5",
    3: "d2e3e2a88be4af996bc27f8740945ce73684c9a0e1c62cb7aea9def1c012372d",
    4: "b7265672d34b876ceb1f371ab8b8a6cde7c970a0d0fbf4daed1d783a860a9b3b",
    5: "46efec29ef9e4bcf326fd530d3ebbf43d3adb7687ee68ce356eadfe3a8c991da",
}
CATALOG_SHA256 = "067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge_index(low: int, high: int) -> int:
    if low > high:
        low, high = high, low
    return high * (high - 1) // 2 + low


def parse_edge(text: str) -> int:
    low, high = map(int, text.split(","))
    if not 0 <= low < high < ORDER:
        raise ValueError(f"bad edge {text!r}")
    return edge_index(low, high)


def decode_graph6(record: str) -> list[int]:
    if not record or ord(record[0]) - 63 != ORDER:
        raise ValueError("expected a graph6 record of order 42")
    bits = []
    for character in record[1:]:
        value = ord(character) - 63
        if not 0 <= value < 64:
            raise ValueError("bad graph6 byte")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    if len(bits) < EDGE_COUNT:
        raise ValueError("truncated graph6 record")
    return bits[:EDGE_COUNT]


def known_assignments(root: Path, parent: int) -> set[tuple[int, ...]]:
    result = {()}
    for radius in range(2, 6):
        path = root / f"ramsey_r55_catalog_edge_radius{radius}_classification" / f"EDGE_RADIUS{radius}_MAP.tsv"
        if sha256(path) != MAP_HASHES[radius]:
            raise AssertionError(f"unexpected radius-{radius} map bytes")
        for line in path.read_text(encoding="ascii").splitlines()[1:]:
            if line.startswith("# SUMMARY "):
                break
            fields = line.split("\t")
            if radius == 2:
                row_radius, row_parent = map(int, fields[:2])
                if row_parent != parent:
                    continue
                selected = tuple(parse_edge(text) for text in fields[2 : 2 + row_radius])
            else:
                row_parent = int(fields[0])
                if row_parent != parent:
                    continue
                selected = tuple(parse_edge(text) for text in fields[1 : 1 + radius])
            if selected != tuple(sorted(selected)) or len(set(selected)) != len(selected):
                raise AssertionError("noncanonical saved assignment")
            if selected in result:
                raise AssertionError("duplicate saved assignment")
            result.add(selected)
    return result


def counter_variable(edge: int, level: int) -> int:
    return EDGE_COUNT + 1 + 6 * edge + (level - 1)


def ramsey_clauses(adjacency: list[int]):
    for vertices in itertools.combinations(range(ORDER), 5):
        present = []
        absent = []
        for low, high in itertools.combinations(vertices, 2):
            variable = edge_index(low, high) + 1
            (present if adjacency[variable - 1] else absent).append(variable)
        if len(absent) <= 5:
            yield present + [-variable for variable in absent]
        if len(present) <= 5:
            yield [-variable for variable in present] + absent


def counter_clauses():
    for edge in range(EDGE_COUNT):
        flip = edge + 1
        yield [-flip, counter_variable(edge, 1)]
        if edge:
            for level in range(1, 7):
                yield [-counter_variable(edge - 1, level), counter_variable(edge, level)]
            for level in range(2, 7):
                yield [
                    -flip,
                    -counter_variable(edge - 1, level - 1),
                    counter_variable(edge, level),
                ]
    yield [-counter_variable(EDGE_COUNT - 1, 6)]


def blocking_clause(selected: tuple[int, ...]) -> list[int]:
    chosen = set(selected)
    return [-(edge + 1) if edge in chosen else edge + 1 for edge in range(EDGE_COUNT)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("parent", type=int)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if not 0 <= args.parent < 328:
        raise ValueError("parent must be in 0,...,327")

    here = Path(__file__).resolve().parent
    root = here.parent
    artifact = root / "ramsey_r55_catalog_edge_radius5_classification"
    catalog_path = artifact / "r55_42some.g6"
    if sha256(catalog_path) != CATALOG_SHA256:
        raise AssertionError("unexpected catalog bytes")
    records = catalog_path.read_text(encoding="ascii").splitlines()
    if len(records) != 328:
        raise AssertionError("unexpected catalog census")
    adjacency = decode_graph6(records[args.parent])
    assignments = known_assignments(root, args.parent)
    ramsey_count = sum(1 for _ in ramsey_clauses(adjacency))
    counter_count = sum(1 for _ in counter_clauses())
    clause_count = counter_count + ramsey_count + len(assignments)

    with args.output.open("w", encoding="ascii", buffering=1024 * 1024) as output:
        output.write(f"p cnf {VARIABLES} {clause_count}\n")
        for clause in counter_clauses():
            output.write(" ".join(map(str, clause)) + " 0\n")
        for clause in ramsey_clauses(adjacency):
            output.write(" ".join(map(str, clause)) + " 0\n")
        for selected in sorted(assignments, key=lambda value: (len(value), value)):
            output.write(" ".join(map(str, blocking_clause(selected))) + " 0\n")

    print(
        f"parent={args.parent} variables={VARIABLES} clauses={clause_count} "
        f"counter_clauses={counter_count} ramsey_clauses={ramsey_count} "
        f"blocked_known_models={len(assignments)}"
    )


if __name__ == "__main__":
    main()
