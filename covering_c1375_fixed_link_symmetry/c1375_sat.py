#!/usr/bin/env python3
"""Generate and check a direct SAT encoding for a 77-block (13,7,5) cover.

The primary variables are all 7-subsets of range(13), in lexicographic order.
Coverage clauses require every 5-subset to lie in a selected block.  A unary
forward counter imposes at most 77 selected blocks.  We also force the first
block {0,...,6}: this is sound because any nonempty cover can be relabelled so
that any one of its blocks is the first block.

Only Python's standard library is used.  All combinatorics use exact integers.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from typing import Iterable, Iterator, Sequence


V = 13
K = 7
T = 5
LIMIT = 77


def all_blocks() -> list[tuple[int, ...]]:
    return list(combinations(range(V), K))


def coverage_clauses(
    blocks: Sequence[tuple[int, ...]],
) -> Iterator[tuple[int, ...]]:
    block_index = {block: i + 1 for i, block in enumerate(blocks)}
    points = set(range(V))
    for target in combinations(range(V), T):
        rest = sorted(points.difference(target))
        yield tuple(
            block_index[tuple(sorted(target + extra))]
            for extra in combinations(rest, K - T)
        )


def forward_at_most_clauses(
    primary_vars: Sequence[int], limit: int, first_aux: int
) -> tuple[int, Iterator[tuple[int, ...]]]:
    """Return last variable and a forward unary at-most-limit encoding.

    s(i,j) means that at least j of x[0],...,x[i] are true.  Only implications
    needed to propagate actual counts are encoded.  Requiring not s(n-1,k+1)
    therefore rejects every assignment with more than k true x variables.
    """
    n = len(primary_vars)
    width = limit + 1
    if not 0 <= limit < n:
        raise ValueError("forward counter requires 0 <= limit < n")

    def s(i: int, j: int) -> int:
        if not (0 <= i < n and 1 <= j <= width):
            raise IndexError((i, j))
        return first_aux + i * width + (j - 1)

    def clauses() -> Iterator[tuple[int, ...]]:
        # A selected x_i forces the first unary bit.
        for i, x_i in enumerate(primary_vars):
            yield (-x_i, s(i, 1))

        for i in range(1, n):
            x_i = primary_vars[i]
            # Counts already reached remain reached.
            for j in range(1, width + 1):
                yield (-s(i - 1, j), s(i, j))
            # Selecting x_i advances every count already reached.
            for j in range(2, width + 1):
                yield (-x_i, -s(i - 1, j - 1), s(i, j))

        yield (-s(n - 1, width),)

    return first_aux + n * width - 1, clauses()


def write_cnf(path: Path, point0_minimum: bool) -> None:
    blocks = all_blocks()
    primaries = list(range(1, len(blocks) + 1))
    last_var, global_counter = forward_at_most_clauses(
        primaries, LIMIT, len(blocks) + 1
    )
    cover = list(coverage_clauses(blocks))
    extra_counters: list[tuple[int, ...]] = []
    if point0_minimum:
        # Every point occurs in at least C(12,6,4)=41 blocks.  For a putative
        # 77-block cover, sum(r_x-41)=77*7-13*41=6, so some point has degree
        # exactly 41.  Relabel such a point as 0 and impose the upper half of
        # that equality here; the cited lower bound supplies the lower half.
        through_zero = [i + 1 for i, block in enumerate(blocks) if 0 in block]
        last_var, point_counter = forward_at_most_clauses(
            through_zero, 41, last_var + 1
        )
        extra_counters.extend(point_counter)
    # Forcing the lexicographically first block is a sound S_13 symmetry break.
    clauses: Iterable[tuple[int, ...]] = (
        *cover,
        (1,),
        *global_counter,
        *extra_counters,
    )
    clauses = tuple(clauses)
    with path.open("w", encoding="ascii", newline="\n") as handle:
        header_comments = (
            f"c C(13,7,5) cover with at most {LIMIT} distinct blocks\n"
            "c primary variables are lexicographic 7-subsets of 0,...,12\n"
            "c variable 1 ({0,...,6}) is forced by point-permutation symmetry\n"
        )
        if point0_minimum:
            header_comments += (
                "c point 0 has degree at most 41 (sound using C(12,6,4)=41)\n"
            )
        handle.write(header_comments)
        handle.write(f"p cnf {last_var} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")
    print(
        f"wrote {path}: {last_var} variables, {len(clauses)} clauses, "
        f"{len(blocks)} primary variables"
    )


def parse_model(path: Path) -> set[int]:
    positives: set[int] = set()
    saw_sat = False
    with path.open("r", encoding="ascii", errors="strict") as handle:
        for raw in handle:
            line = raw.strip()
            if line in {"s SATISFIABLE", "SAT"}:
                saw_sat = True
            if line.startswith("v "):
                for token in line.split()[1:]:
                    literal = int(token)
                    if literal > 0:
                        positives.add(literal)
    if not saw_sat:
        raise ValueError(f"no SAT status in {path}")
    return positives


def verify_selected(selected: Sequence[tuple[int, ...]]) -> None:
    if len(set(selected)) != len(selected):
        raise ValueError("selected block list contains duplicates")
    if len(selected) > LIMIT:
        raise ValueError(f"selected {len(selected)} blocks, exceeding {LIMIT}")
    uncovered = []
    block_sets = [set(block) for block in selected]
    multiplicities = []
    for target in combinations(range(V), T):
        target_set = set(target)
        multiplicity = sum(target_set <= block for block in block_sets)
        multiplicities.append(multiplicity)
        if multiplicity == 0:
            uncovered.append(target)
    if uncovered:
        raise ValueError(f"{len(uncovered)} uncovered 5-sets; first={uncovered[0]}")
    degree = Counter(point for block in selected for point in block)
    print(f"verified {len(selected)} distinct blocks and complete 5-coverage")
    print("point degrees:", tuple(degree[p] for p in range(V)))
    print("5-set multiplicities:", dict(sorted(Counter(multiplicities).items())))


def check_model(path: Path) -> None:
    positives = parse_model(path)
    blocks = all_blocks()
    selected = [block for var, block in enumerate(blocks, 1) if var in positives]
    verify_selected(selected)
    for block in selected:
        print(" ".join(map(str, block)))


def self_test() -> None:
    # Definition-level checks on a tiny counter: for each primary assignment,
    # brute-force all auxiliary assignments and compare satisfiability with <= k.
    for n, limit in ((1, 0), (3, 1), (4, 2)):
        xs = list(range(1, n + 1))
        last, generated = forward_at_most_clauses(xs, limit, n + 1)
        clauses = tuple(generated)
        aux = tuple(range(n + 1, last + 1))
        for primary_values in product((False, True), repeat=n):
            extendible = False
            for aux_values in product((False, True), repeat=len(aux)):
                assignment = {
                    **dict(zip(xs, primary_values)),
                    **dict(zip(aux, aux_values)),
                }
                if all(
                    any(
                        assignment[abs(literal)] == (literal > 0)
                        for literal in clause
                    )
                    for clause in clauses
                ):
                    extendible = True
                    break
            expected = sum(primary_values) <= limit
            if extendible != expected:
                raise AssertionError((n, limit, primary_values, extendible, expected))
    # Repeated input literals are used as integer weights in derived cases.
    weighted = [1, 1, 2]
    last, generated = forward_at_most_clauses(weighted, 1, 3)
    clauses = tuple(generated)
    for x1, x2 in product((False, True), repeat=2):
        extendible = False
        for aux_values in product((False, True), repeat=last - 2):
            assignment = {1: x1, 2: x2, **dict(zip(range(3, last + 1), aux_values))}
            if all(
                any(assignment[abs(literal)] == (literal > 0) for literal in clause)
                for clause in clauses
            ):
                extendible = True
                break
        if extendible != (2 * x1 + x2 <= 1):
            raise AssertionError(("weighted", x1, x2, extendible))
    blocks = all_blocks()
    cover = tuple(coverage_clauses(blocks))
    assert len(blocks) == 1716
    assert len(cover) == 1287
    assert all(len(clause) == 28 for clause in cover)
    print("self-test passed: tiny counters, repeated-literal weights, and incidence dimensions")


def main() -> None:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    generate = commands.add_parser("generate")
    generate.add_argument("cnf", type=Path)
    generate.add_argument(
        "--point0-minimum",
        action="store_true",
        help="symmetry-break at a degree-41 point using C(12,6,4)=41",
    )
    check = commands.add_parser("check-model")
    check.add_argument("model", type=Path)
    commands.add_parser("self-test")
    args = parser.parse_args()
    if args.command == "generate":
        write_cnf(args.cnf, args.point0_minimum)
    elif args.command == "check-model":
        check_model(args.model)
    else:
        self_test()


if __name__ == "__main__":
    main()
