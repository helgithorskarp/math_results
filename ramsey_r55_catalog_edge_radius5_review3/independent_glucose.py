#!/usr/bin/env python3
"""Independent exact-five Ramsey perturbation enumeration with PySAT/Glucose."""

from __future__ import annotations

import hashlib
import itertools
import sys
from pathlib import Path

import pysat
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver


ORDER = 42
PRIMARY = ORDER * (ORDER - 1) // 2


def edge_index(low: int, high: int) -> int:
    if low > high:
        low, high = high, low
    return high * (high - 1) // 2 + low


def decode_graph6(record: str) -> list[int]:
    if not record or ord(record[0]) - 63 != ORDER:
        raise ValueError("expected a short graph6 record of order 42")
    bits = []
    for char in record[1:]:
        value = ord(char) - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 byte")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adjacency = [0] * ORDER
    at = 0
    for high in range(1, ORDER):
        for low in range(high):
            if bits[at]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            at += 1
    return adjacency


def expected_sets(map_path: Path, parent: int) -> set[tuple[int, ...]]:
    answer = set()
    with map_path.open(encoding="ascii") as source:
        header = source.readline().rstrip("\n")
        if not header.startswith("parent\tedge_1\tedge_2\tedge_3\tedge_4\tedge_5\t"):
            raise ValueError("unexpected map header")
        for line in source:
            if line.startswith("# SUMMARY"):
                break
            fields = line.rstrip("\n").split("\t")
            if int(fields[0]) != parent:
                continue
            indices = []
            for edge in fields[1:6]:
                low, high = map(int, edge.split(","))
                indices.append(edge_index(low, high))
            answer.add(tuple(sorted(indices)))
    return answer


def canonical_bytes(sets: set[tuple[int, ...]]) -> bytes:
    return "".join(
        " ".join(map(str, selected)) + "\n" for selected in sorted(sets)
    ).encode("ascii")


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: independent_glucose.py CATALOG MAP PARENT")
    catalog_path = Path(sys.argv[1])
    map_path = Path(sys.argv[2])
    parent = int(sys.argv[3])
    records = catalog_path.read_text(encoding="ascii").splitlines()
    if len(records) != 328 or not 0 <= parent < len(records):
        raise ValueError("catalog or parent index is out of range")
    adjacency = decode_graph6(records[parent])

    # This uses a separate, bidirectional sequential encoding of exactly five,
    # rather than the submitted one-way at-most-five threshold counter.
    cardinality = CardEnc.equals(
        lits=list(range(1, PRIMARY + 1)),
        bound=5,
        top_id=PRIMARY,
        encoding=EncType.seqcounter,
    )
    ramsey_clauses = 0
    with Solver(name="g42", bootstrap_with=cardinality.clauses) as solver:
        for vertices in itertools.combinations(range(ORDER), 5):
            present = []
            absent = []
            for low, high in itertools.combinations(vertices, 2):
                variable = edge_index(low, high) + 1
                if adjacency[low] & (1 << high):
                    present.append(variable)
                else:
                    absent.append(variable)
            if len(absent) <= 5:
                solver.add_clause([*present, *(-variable for variable in absent)])
                ramsey_clauses += 1
            if len(present) <= 5:
                solver.add_clause([*(-variable for variable in present), *absent])
                ramsey_clauses += 1

        actual = set()
        while solver.solve():
            positive = {literal for literal in solver.get_model() if literal > 0}
            selected = tuple(
                edge for edge in range(PRIMARY) if edge + 1 in positive
            )
            if len(selected) != 5 or selected in actual:
                raise AssertionError((len(selected), selected in actual))
            actual.add(selected)
            selected_set = set(selected)
            solver.add_clause(
                [
                    -(edge + 1) if edge in selected_set else edge + 1
                    for edge in range(PRIMARY)
                ]
            )

        expected = expected_sets(map_path, parent)
        if actual != expected:
            raise AssertionError(
                f"parent {parent}: missing={sorted(expected - actual)} "
                f"extra={sorted(actual - expected)}"
            )
        digest = hashlib.sha256(canonical_bytes(actual)).hexdigest()
        stats = solver.accum_stats()

    print(f"pysat_version={pysat.__version__}")
    print("solver=Glucose4.2")
    print(f"parent={parent}")
    print(f"primary_variables={PRIMARY}")
    print(f"total_variables={cardinality.nv}")
    print(f"cardinality_clauses={len(cardinality.clauses)}")
    print(f"ramsey_clauses={ramsey_clauses}")
    print(f"exact5_models={len(actual)}")
    print(f"canonical_sets_sha256={digest}")
    print(f"conflicts={stats.get('conflicts', -1)}")
    print("glucose_exact_check=true")


if __name__ == "__main__":
    main()
