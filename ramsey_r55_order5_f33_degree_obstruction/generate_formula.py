#!/usr/bin/env python3
"""Generate the degree-strengthened order-five fixed-count-33 formula."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import base_formula

ORDER = base_formula.ORDER
PRIME = 5
FIXED = 33


def edge_mapping(fixed: int) -> dict[tuple[int, int], int]:
    def image(vertex: int, power: int) -> int:
        if vertex < fixed:
            return vertex
        cycle, position = divmod(vertex - fixed, PRIME)
        return fixed + PRIME * cycle + (position + power) % PRIME

    def key(u: int, v: int) -> tuple[int, int]:
        return min(
            tuple(sorted((image(u, power), image(v, power))))
            for power in range(PRIME)
        )

    representatives = sorted(
        {key(u, v) for u in range(ORDER) for v in range(u + 1, ORDER)}
    )
    index = {edge: position + 1 for position, edge in enumerate(representatives)}
    return {
        (u, v): index[key(u, v)]
        for u in range(ORDER)
        for v in range(u + 1, ORDER)
    }


def edge(mapping: dict[tuple[int, int], int], u: int, v: int) -> int:
    return mapping[tuple(sorted((u, v)))]


def normalize(raw: list[int] | tuple[int, ...]) -> tuple[int, ...] | None:
    literals = set(raw)
    if any(-literal in literals for literal in literals):
        return None
    return tuple(sorted(literals))


def insert(formula: set[tuple[int, ...]], raw: list[int] | tuple[int, ...]) -> None:
    clause = normalize(raw)
    if clause is not None:
        formula.add(clause)


def comparator_clauses(
    left: int, right: int, high: int, low: int
) -> tuple[tuple[int, ...], ...]:
    """Encode high = left OR right and low = left AND right."""
    return (
        (-left, high),
        (-right, high),
        (left, right, -high),
        (left, -low),
        (right, -low),
        (-left, -right, low),
    )


def add_comparator(
    formula: set[tuple[int, ...]], left: int, right: int, top_id: int
) -> tuple[int, int, int]:
    high, low = top_id + 1, top_id + 2
    for clause in comparator_clauses(left, right, high, low):
        insert(formula, clause)
    return high, low, low


def add_degree_window(
    formula: set[tuple[int, ...]], inputs: list[int], top_id: int
) -> int:
    if len(inputs) != ORDER - 1:
        raise AssertionError("degree input must represent all 42 incident edges")
    wires = inputs[:]
    for end in range(len(wires) - 1, 0, -1):
        for position in range(end):
            high, low, top_id = add_comparator(
                formula, wires[position], wires[position + 1], top_id
            )
            wires[position], wires[position + 1] = high, low
    insert(formula, (wires[17],))
    insert(formula, (-wires[24],))
    return top_id


def degree_inputs(mapping: dict[tuple[int, int], int]) -> list[list[int]]:
    """Expand orbit colors to the 42 incident-edge colors per vertex orbit."""
    cycles = (ORDER - FIXED) // PRIME
    result = []
    for vertex in range(FIXED):
        inputs = [
            edge(mapping, vertex, other)
            for other in range(FIXED)
            if other != vertex
        ]
        for cycle in range(cycles):
            inputs.extend([edge(mapping, vertex, FIXED + PRIME * cycle)] * PRIME)
        result.append(inputs)

    for cycle in range(cycles):
        base = FIXED + PRIME * cycle
        inputs = [edge(mapping, vertex, base) for vertex in range(FIXED)]
        for distance in (1, 2):
            inputs.extend([edge(mapping, base, base + distance)] * 2)
        for other in range(cycles):
            if other == cycle:
                continue
            other_base = FIXED + PRIME * other
            inputs.extend(
                edge(mapping, base, other_base + offset)
                for offset in range(PRIME)
            )
        result.append(inputs)
    if len(result) != FIXED + cycles or any(len(row) != ORDER - 1 for row in result):
        raise AssertionError("degree expansion mismatch")
    return result


def build() -> tuple[int, list[tuple[int, ...]], int]:
    base_variables, base_clauses = base_formula.build(PRIME, FIXED)
    mapping = edge_mapping(FIXED)
    if max(mapping.values()) != base_variables:
        raise AssertionError("edge mapping disagrees with base formula")
    formula = set(base_clauses)
    base_clause_count = len(formula)
    top_id = base_variables
    for inputs in degree_inputs(mapping):
        top_id = add_degree_window(formula, inputs, top_id)
    return top_id, sorted(formula, key=lambda clause: (len(clause), clause)), base_clause_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    variables, clauses, base_clause_count = build()
    with args.output.open("w", encoding="ascii", newline="\n") as stream:
        stream.write(f"p cnf {variables} {len(clauses)}\n")
        for clause in clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    print(
        f"fixed={FIXED} cycles={(ORDER-FIXED)//PRIME} "
        f"edge_orbits=603 variables={variables} "
        f"clauses={len(clauses)} degree_clauses={len(clauses)-base_clause_count} "
        f"sha256={digest}",
        flush=True,
    )


if __name__ == "__main__":
    main()
