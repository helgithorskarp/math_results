#!/usr/bin/env python3
"""Generate a SAT instance for small maximal partial Latin hypercubes.

A filled entry is a word in [q]^dimension.  Two entries are compatible exactly
when their Hamming distance is at least two.  Maximality says that every word
outside the selected set has a selected word at Hamming distance one.  Thus the
selected entries are an independent dominating set of the Hamming graph.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence


Word = tuple[int, ...]


def words(q: int, dimension: int) -> list[Word]:
    return list(itertools.product(range(q), repeat=dimension))


def closed_neighborhood(word: Word, q: int) -> list[Word]:
    result = [word]
    for coordinate, old_value in enumerate(word):
        for new_value in range(q):
            if new_value != old_value:
                neighbor = list(word)
                neighbor[coordinate] = new_value
                result.append(tuple(neighbor))
    return result


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
    def variable_count(self) -> int:
        return self.next_variable - 1


def add_at_most(cnf: CNF, variables: Sequence[int], bound: int) -> None:
    """Sinz sequential counter for sum(variables) <= bound."""
    n = len(variables)
    if bound < 0:
        cnf.add()
        return
    if bound >= n:
        return
    if bound == 0:
        for variable in variables:
            cnf.add(-variable)
        return

    s = [[cnf.new_variable() for _ in range(bound)] for _ in range(n - 1)]
    for i in range(n - 1):
        cnf.add(-variables[i], s[i][0])
    for i in range(1, n - 1):
        for j in range(bound):
            cnf.add(-s[i - 1][j], s[i][j])
        for j in range(1, bound):
            cnf.add(-variables[i], -s[i - 1][j - 1], s[i][j])
    for i in range(1, n):
        cnf.add(-variables[i], -s[i - 1][bound - 1])


def add_cardinality_range(
    cnf: CNF,
    variables: Sequence[int],
    lower_bound: int,
    upper_bound: int,
) -> None:
    """Exact unary recurrence for lower_bound <= sum(variables) <= upper_bound."""
    if not 0 <= lower_bound <= upper_bound <= len(variables):
        raise ValueError("invalid cardinality range")
    limit = min(len(variables), upper_bound + 1)
    count = [[cnf.new_variable() for _ in range(limit + 1)] for _ in range(len(variables) + 1)]
    for i in range(len(variables) + 1):
        cnf.add(count[i][0])
    for j in range(1, limit + 1):
        cnf.add(-count[0][j])
    for i, variable in enumerate(variables, start=1):
        for j in range(1, limit + 1):
            previous_same = count[i - 1][j]
            previous_lower = count[i - 1][j - 1]
            current = count[i][j]
            cnf.add(-previous_same, current)
            cnf.add(-previous_lower, -variable, current)
            cnf.add(-current, previous_same, previous_lower)
            cnf.add(-current, previous_same, variable)
    cnf.add(count[len(variables)][lower_bound])
    if upper_bound < len(variables):
        cnf.add(-count[len(variables)][upper_bound + 1])


def build(
    q: int,
    dimension: int,
    bound: int,
    lower_bound: int | None,
    fix_zero: bool,
    fixed_words: Sequence[Word] = (),
) -> tuple[CNF, list[Word]]:
    universe = words(q, dimension)
    cnf = CNF()
    selected = {word: cnf.new_variable() for word in universe}

    index = {word: i for i, word in enumerate(universe)}
    for word in universe:
        for neighbor in closed_neighborhood(word, q)[1:]:
            if index[word] < index[neighbor]:
                cnf.add(-selected[word], -selected[neighbor])
    for word in universe:
        cnf.add(*(selected[neighbor] for neighbor in closed_neighborhood(word, q)))

    primary_variables = [selected[word] for word in universe]
    if lower_bound is None:
        add_at_most(cnf, primary_variables, bound)
    else:
        add_cardinality_range(cnf, primary_variables, lower_bound, bound)
    if fix_zero:
        cnf.add(selected[(0,) * dimension])
    for word in fixed_words:
        if word not in selected:
            raise ValueError(f"fixed word outside universe: {word}")
        cnf.add(selected[word])
    return cnf, universe


def write_dimacs(path: Path, cnf: CNF, metadata: dict[str, object]) -> None:
    with path.open("w", encoding="ascii") as handle:
        handle.write("c " + json.dumps(metadata, sort_keys=True) + "\n")
        handle.write(f"p cnf {cnf.variable_count} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--order", type=int, default=4)
    parser.add_argument("--dimension", type=int, default=4)
    parser.add_argument("--bound", type=int, default=30)
    parser.add_argument("--lower-bound", type=int)
    parser.add_argument("--no-fix-zero", action="store_true")
    parser.add_argument("--fix-word", action="append", default=[])
    args = parser.parse_args()
    if args.order < 2 or args.dimension < 2:
        parser.error("order and dimension must both be at least two")
    if args.lower_bound is not None and not 0 <= args.lower_bound <= args.bound:
        parser.error("lower-bound must be between zero and bound")

    fixed_words = [tuple(map(int, text.split(","))) for text in args.fix_word]
    if any(len(word) != args.dimension for word in fixed_words):
        parser.error("each fixed word must have exactly dimension comma-separated entries")
    try:
        cnf, universe = build(
            args.order,
            args.dimension,
            args.bound,
            args.lower_bound,
            not args.no_fix_zero,
            fixed_words,
        )
    except ValueError as exc:
        parser.error(str(exc))
    metadata = {
        "claim": "independent dominating set of the Hamming graph with bounded size",
        "order": args.order,
        "dimension": args.dimension,
        "primary_variables": len(universe),
        "primary_order": "lexicographic words in range(order)^dimension",
        "bound": args.bound,
        "lower_bound": args.lower_bound,
        "fix_zero": not args.no_fix_zero,
        "fixed_words": [list(word) for word in fixed_words],
    }
    write_dimacs(args.output, cnf, metadata)
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    print(json.dumps({
        **metadata,
        "variables": cnf.variable_count,
        "clauses": len(cnf.clauses),
        "sha256": digest,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
