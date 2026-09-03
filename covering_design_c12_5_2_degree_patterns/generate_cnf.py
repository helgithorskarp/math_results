#!/usr/bin/env python3
"""Generate the proof-checkable incidence CNF for degree pattern (5^4,4,3^7)."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


class Builder:
    def __init__(self) -> None:
        self.nvars = 0
        self.clauses: list[list[int]] = []

    def var(self) -> int:
        self.nvars += 1
        return self.nvars

    def at_most(self, literals: list[int], bound: int) -> None:
        """Add the Sinz sequential-counter encoding of sum(literals) <= bound."""
        if bound >= len(literals):
            return
        if bound < 0:
            self.clauses.append([])
            return
        if bound == 0:
            self.clauses.extend([[-literal] for literal in literals])
            return
        size = len(literals)
        counter = [[self.var() for _ in range(bound)] for _ in range(size - 1)]
        self.clauses.append([-literals[0], counter[0][0]])
        self.clauses.extend([[-counter[0][column]] for column in range(1, bound)])
        for row in range(1, size - 1):
            self.clauses.append([-literals[row], counter[row][0]])
            self.clauses.append([-counter[row - 1][0], counter[row][0]])
            for column in range(1, bound):
                self.clauses.append(
                    [-literals[row], -counter[row - 1][column - 1], counter[row][column]]
                )
                self.clauses.append([-counter[row - 1][column], counter[row][column]])
            self.clauses.append([-literals[row], -counter[row - 1][bound - 1]])
        self.clauses.append([-literals[-1], -counter[size - 2][bound - 1]])

    def exactly(self, literals: list[int], value: int) -> None:
        self.at_most(literals, value)
        self.at_most([-literal for literal in literals], len(literals) - value)

    def lex_le(self, left: list[int], right: list[int]) -> None:
        """Add an equisatisfiable encoding of left <=_lex right with 0 < 1."""
        assert len(left) == len(right)
        prefix_equal = self.var()
        self.clauses.append([prefix_equal])
        for first, second in zip(left, right):
            self.clauses.append([-prefix_equal, -first, second])
            next_prefix = self.var()
            self.clauses.append([-next_prefix, prefix_equal])
            self.clauses.append([-next_prefix, -first, second])
            self.clauses.append([-next_prefix, first, -second])
            self.clauses.append([-prefix_equal, -first, -second, next_prefix])
            self.clauses.append([-prefix_equal, first, second, next_prefix])
            prefix_equal = next_prefix


def build() -> Builder:
    degrees = (5, 5, 5, 5, 4, 3, 3, 3, 3, 3, 3, 3)
    formula = Builder()
    incidence = [[formula.var() for _ in range(9)] for _ in range(12)]

    for row, degree in zip(incidence, degrees):
        formula.exactly(row, degree)
    for column in range(9):
        formula.exactly([incidence[row][column] for row in range(12)], 5)

    for first in range(12):
        for second in range(first + 1, 12):
            together = []
            for column in range(9):
                conjunction = formula.var()
                formula.clauses.append([-conjunction, incidence[first][column]])
                formula.clauses.append([-conjunction, incidence[second][column]])
                formula.clauses.append(
                    [conjunction, -incidence[first][column], -incidence[second][column]]
                )
                together.append(conjunction)
            formula.clauses.append(together)

    for column in range(8):
        formula.lex_le([incidence[row][column] for row in range(12)],
                       [incidence[row][column + 1] for row in range(12)])
    for first, last in ((0, 4), (5, 12)):
        for row in range(first, last - 1):
            formula.lex_le(incidence[row], incidence[row + 1])
    return formula


def render(formula: Builder) -> bytes:
    lines = [f"p cnf {formula.nvars} {len(formula.clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in formula.clauses)
    return "".join(lines).encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path, help="CNF path under /scratch")
    args = parser.parse_args()
    formula = build()
    data = render(formula)
    args.output.write_bytes(data)
    print(json.dumps({"variables": formula.nvars, "clauses": len(formula.clauses),
                      "sha256": hashlib.sha256(data).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
