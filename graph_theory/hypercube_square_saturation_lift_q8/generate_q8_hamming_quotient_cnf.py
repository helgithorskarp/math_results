#!/usr/bin/env python3
"""Generate proof-producing CNFs for the H x {0}-invariant Q_8 lower bound."""

from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence


Edge = tuple[int, int]


def edge(x: int, y: int) -> Edge:
    assert x != y
    return min(x, y), max(x, y)


def quotient_edges() -> list[Edge]:
    result = [edge(x + 8 * layer, y + 8 * layer) for layer in range(2) for x in range(8) for y in range(x + 1, 8)]
    result.extend(edge(x, x + 8) for x in range(8))
    result = sorted(result)
    assert len(result) == 64 and len(set(result)) == 64
    return result


def quotient_cycles() -> list[frozenset[Edge]]:
    result: set[frozenset[Edge]] = set()
    # Squares using two of the first seven coordinates become affine-plane
    # 4-cycles in one of the two syndrome K_8 layers.
    for layer in range(2):
        for start in range(8):
            for first, second in itertools.combinations(range(1, 8), 2):
                vertices = (
                    start + 8 * layer,
                    (start ^ first) + 8 * layer,
                    (start ^ first ^ second) + 8 * layer,
                    (start ^ second) + 8 * layer,
                )
                result.add(
                    frozenset(edge(vertices[index], vertices[(index + 1) % 4]) for index in range(4))
                )
    # Squares using the eighth coordinate have two horizontal and two vertical
    # quotient edges.
    for start in range(8):
        for direction in range(1, 8):
            vertices = (start, start ^ direction, (start ^ direction) + 8, start + 8)
            result.add(
                frozenset(edge(vertices[index], vertices[(index + 1) % 4]) for index in range(4))
            )
    assert len(result) == 112
    return sorted(result, key=lambda cycle: sorted(cycle))


@dataclass
class CNF:
    next_variable: int = 1
    clauses: list[list[int]] = field(default_factory=list)

    def new_variable(self) -> int:
        result = self.next_variable
        self.next_variable += 1
        return result

    def add(self, *literals: int) -> None:
        self.clauses.append(list(literals))

    @property
    def variables(self) -> int:
        return self.next_variable - 1


def add_at_most(cnf: CNF, variables: Sequence[int], bound: int) -> None:
    """Sinz sequential counter encoding sum(variables) <= bound."""
    count = len(variables)
    assert 0 < bound < count
    sequential = [[cnf.new_variable() for _ in range(bound)] for _ in range(count - 1)]
    for index in range(count - 1):
        cnf.add(-variables[index], sequential[index][0])
    for index in range(1, count - 1):
        for level in range(bound):
            cnf.add(-sequential[index - 1][level], sequential[index][level])
        for level in range(1, bound):
            cnf.add(-variables[index], -sequential[index - 1][level - 1], sequential[index][level])
    for index in range(1, count):
        cnf.add(-variables[index], -sequential[index - 1][bound - 1])


def build_cnf(bound: int, fixed_type: str) -> tuple[CNF, dict[str, object]]:
    all_edges = quotient_edges()
    all_cycles = quotient_cycles()
    cnf = CNF()
    edge_variable = {host_edge: cnf.new_variable() for host_edge in all_edges}
    incident: dict[Edge, list[frozenset[Edge]]] = {host_edge: [] for host_edge in all_edges}

    for cycle in all_cycles:
        cnf.add(*(-edge_variable[host_edge] for host_edge in sorted(cycle)))
        for host_edge in cycle:
            incident[host_edge].append(cycle - {host_edge})
    assert all(len(witnesses) == 7 for witnesses in incident.values())

    for host_edge in all_edges:
        witness_variables = []
        for triple in incident[host_edge]:
            witness = cnf.new_variable()
            witness_variables.append(witness)
            for other in sorted(triple):
                cnf.add(-witness, edge_variable[other])
        cnf.add(edge_variable[host_edge], *witness_variables)

    add_at_most(cnf, [edge_variable[host_edge] for host_edge in all_edges], bound)
    if fixed_type == "horizontal":
        fixed_edge = edge(0, 1)
    elif fixed_type == "vertical":
        fixed_edge = edge(0, 8)
    else:
        raise ValueError(f"unknown fixed edge type: {fixed_type}")
    cnf.add(edge_variable[fixed_edge])
    metadata: dict[str, object] = {
        "bound_quotient_edges": bound,
        "fixed_edge": list(fixed_edge),
        "fixed_edge_type": fixed_type,
        "primary_variables": len(all_edges),
        "quotient_cycles": len(all_cycles),
        "quotient_edges": len(all_edges),
        "translation_group_order": 16,
    }
    return cnf, metadata


def write_dimacs(path: Path, cnf: CNF, metadata: dict[str, object]) -> None:
    with path.open("w", encoding="ascii") as output:
        output.write("c " + json.dumps(metadata, sort_keys=True) + "\n")
        output.write(f"p cnf {cnf.variables} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            output.write(" ".join(map(str, clause)) + " 0\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--bound", type=int, default=26)
    parser.add_argument("--fixed-type", choices=("horizontal", "vertical"), required=True)
    args = parser.parse_args()
    cnf, metadata = build_cnf(args.bound, args.fixed_type)
    write_dimacs(args.output, cnf, metadata)
    print(json.dumps(metadata | {"clauses": len(cnf.clauses), "variables": cnf.variables}, sort_keys=True))


if __name__ == "__main__":
    main()
