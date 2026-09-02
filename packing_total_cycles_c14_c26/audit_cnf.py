#!/usr/bin/env python3
"""Audit a generated CNF against explicit distances in the total graph."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from generate_cnf import variable
from verify_witnesses import distances, total_graph


def parse_cnf(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    variables = clauses_declared = None
    clauses: list[tuple[int, ...]] = []
    with path.open(encoding="ascii") as handle:
        for raw in handle:
            fields = raw.split()
            if not fields or fields[0] == "c":
                continue
            if fields[0] == "p":
                if len(fields) != 4 or fields[1] != "cnf" or variables is not None:
                    raise AssertionError("invalid or duplicate DIMACS header")
                variables, clauses_declared = map(int, fields[2:])
                continue
            literals = tuple(map(int, fields))
            if not literals or literals[-1] != 0 or 0 in literals[:-1]:
                raise AssertionError("malformed DIMACS clause")
            clauses.append(literals[:-1])
    if variables is None or clauses_declared != len(clauses):
        raise AssertionError("DIMACS header mismatch")
    if any(abs(lit) > variables for clause in clauses for lit in clause):
        raise AssertionError("literal exceeds declared variable count")
    return variables, clauses


def expected_clauses(n: int, colors: int, symmetry: bool) -> list[tuple[int, ...]]:
    order = 2 * n
    expected: list[tuple[int, ...]] = []
    for position in range(order):
        expected.append(tuple(variable(position, color, colors) for color in range(1, colors + 1)))
    for position in range(order):
        for a in range(1, colors + 1):
            for b in range(a + 1, colors + 1):
                expected.append((-variable(position, a, colors), -variable(position, b, colors)))

    metric = distances(total_graph(n))
    for color in range(1, colors + 1):
        for a in range(order):
            for b in range(a + 1, order):
                if metric[a][b] <= color:
                    expected.append((-variable(a, color, colors), -variable(b, color, colors)))

    if symmetry:
        expected.append((variable(0, 1, colors),))
        diameter = max(max(row) for row in metric)
        for color in range(diameter + 1, colors + 1):
            for position in range(order):
                expected.append(
                    (-variable(position, color, colors),)
                    + tuple(variable(earlier, color - 1, colors) for earlier in range(position))
                )
    return expected


def audit(n: int, colors: int, path: Path, symmetry: bool) -> None:
    variables, actual = parse_cnf(path)
    if variables != 2 * n * colors:
        raise AssertionError("wrong variable count")
    expected = expected_clauses(n, colors, symmetry)
    if Counter(actual) != Counter(expected):
        missing = Counter(expected) - Counter(actual)
        extra = Counter(actual) - Counter(expected)
        raise AssertionError(f"CNF mismatch: {sum(missing.values())} missing, {sum(extra.values())} extra")
    print(f"audited C_{n}, k={colors}: {variables} variables, {len(actual)} clauses")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    parser.add_argument("colors", type=int)
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--symmetry", action="store_true")
    args = parser.parse_args()
    audit(args.n, args.colors, args.cnf, args.symmetry)


if __name__ == "__main__":
    main()
