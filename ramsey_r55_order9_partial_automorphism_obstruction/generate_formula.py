#!/usr/bin/env python3
"""Generate the power-filtered cyclic order-nine formulas."""

from __future__ import annotations

import argparse
import hashlib
import itertools
from pathlib import Path


ORDER = 43
CASES = tuple(
    (cycles9, cycles3, ORDER - 9 * cycles9 - 3 * cycles3)
    for cycles9 in (3, 4)
    for cycles3 in range((ORDER - 9 * cycles9) // 3 + 1)
)
CLOSED = {0: "direct", 1: "direct", 2: "direct", 3: "direct", 4: "direct",
          6: "direct", 7: "degree"}


def case_label(case: tuple[int, int, int]) -> str:
    return "a" + "_".join(map(str, case))


def vertex_cycles(case: tuple[int, int, int]) -> list[list[int]]:
    counts = dict(zip((9, 3, 1), case, strict=True))
    cycles = []
    top = 0
    for length in (9, 3, 1):
        for _ in range(counts[length]):
            cycles.append(list(range(top, top + length)))
            top += length
    if top != ORDER:
        raise AssertionError((case, top))
    return cycles


def edge_mapping(case: tuple[int, int, int]) -> tuple[dict[tuple[int, int], int], dict[int, int]]:
    successor = list(range(ORDER))
    for cycle in vertex_cycles(case):
        for position, vertex in enumerate(cycle):
            successor[vertex] = cycle[(position + 1) % len(cycle)]

    def key(left: int, right: int) -> tuple[int, int]:
        images = []
        for _ in range(9):
            images.append(tuple(sorted((left, right))))
            left, right = successor[left], successor[right]
        return min(images)

    representatives = sorted(
        {key(left, right) for left in range(ORDER) for right in range(left + 1, ORDER)}
    )
    index = {edge: position + 1 for position, edge in enumerate(representatives)}
    mapping = {
        (left, right): index[key(left, right)]
        for left in range(ORDER)
        for right in range(left + 1, ORDER)
    }
    orbit_sizes = {variable: 0 for variable in index.values()}
    for variable in mapping.values():
        orbit_sizes[variable] += 1
    distribution: dict[int, int] = {}
    for size in orbit_sizes.values():
        distribution[size] = distribution.get(size, 0) + 1
    return mapping, distribution


def insert(clauses: set[tuple[int, ...]], raw: tuple[int, ...]) -> None:
    literals = set(raw)
    if not any(-literal in literals for literal in literals):
        clauses.add(tuple(sorted(literals)))


def add_degree_network(
    clauses: set[tuple[int, ...]], inputs: list[int], top_id: int
) -> int:
    wires = inputs[:]
    for end in range(len(wires) - 1, 0, -1):
        for position in range(end):
            left, right = wires[position], wires[position + 1]
            high, low = top_id + 1, top_id + 2
            top_id = low
            for clause in (
                (-left, high), (-right, high), (left, right, -high),
                (left, -low), (right, -low), (-left, -right, low),
            ):
                insert(clauses, clause)
            wires[position], wires[position + 1] = high, low
    insert(clauses, (wires[17],))
    insert(clauses, (-wires[24],))
    return top_id


def build(
    case: tuple[int, int, int], degree: bool
) -> tuple[int, list[tuple[int, ...]], dict[int, int], int]:
    if case not in CASES:
        raise ValueError("case is not power-filtered")
    mapping, distribution = edge_mapping(case)
    clauses: set[tuple[int, ...]] = set()
    for vertices in itertools.combinations(range(ORDER), 5):
        variables = sorted({mapping[pair] for pair in itertools.combinations(vertices, 2)})
        clauses.add(tuple(variables))
        clauses.add(tuple(-variable for variable in reversed(variables)))
    base_clause_count = len(clauses)
    top_id = max(mapping.values())
    if degree:
        for cycle in vertex_cycles(case):
            vertex = cycle[0]
            inputs = [mapping[tuple(sorted((vertex, other)))]
                      for other in range(ORDER) if other != vertex]
            top_id = add_degree_network(clauses, inputs, top_id)
    return top_id, sorted(clauses, key=lambda c: (len(c), c)), distribution, base_clause_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, choices=range(len(CASES)), required=True)
    parser.add_argument("--degree", action="store_true")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    case = CASES[args.case]
    variables, clauses, distribution, base_clauses = build(case, args.degree)
    with args.output.open("w", encoding="ascii", newline="\n") as stream:
        stream.write(f"p cnf {variables} {len(clauses)}\n")
        for clause in clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    print(
        f"case={case} degree={args.degree} variables={variables} clauses={len(clauses)} "
        f"degree_clauses={len(clauses)-base_clauses} edge_orbit_sizes={distribution} "
        f"sha256={digest}"
    )


if __name__ == "__main__":
    main()
