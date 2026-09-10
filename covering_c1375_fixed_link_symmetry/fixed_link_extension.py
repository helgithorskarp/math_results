#!/usr/bin/env python3
"""Test whether a fixed 41-block C(12,6,4) cover extends to C(13,7,5).

Point 0 is added to every fixed six-block.  The remaining variables are all
seven-blocks on points 1,...,12.  Only five-sets not already covered by a
fixed six-block need coverage clauses, and at most 36 variable blocks may be
selected to obtain a 77-block cover.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
from pathlib import Path

from c1375_sat import forward_at_most_clauses, parse_model


def read_link(path: Path) -> list[tuple[int, ...]]:
    blocks = []
    for raw in path.read_text(encoding="ascii").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            blocks.append(tuple(sorted(map(int, line.split()))))
    if len(blocks) != 41 or len(set(blocks)) != 41:
        raise ValueError("fixed link must have 41 distinct blocks")
    if any(len(block) != 6 or not set(block) <= set(range(1, 13)) for block in blocks):
        raise ValueError("fixed link blocks must be six-subsets of 1,...,12")
    for target in combinations(range(1, 13), 4):
        if not any(set(target) <= set(block) for block in blocks):
            raise ValueError(f"fixed link misses quadruple {target}")
    return blocks


def residual_targets(link: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    link_sets = [set(block) for block in link]
    return [
        target
        for target in combinations(range(1, 13), 5)
        if not any(set(target) <= block for block in link_sets)
    ]


def candidate_blocks() -> list[tuple[int, ...]]:
    return list(combinations(range(1, 13), 7))


def generate(
    link_path: Path,
    cnf_path: Path,
    degree_bounds: bool,
    capacity_bound: bool,
    force_block: tuple[int, ...] | None,
) -> None:
    link = read_link(link_path)
    residual = residual_targets(link)
    candidates = candidate_blocks()
    index = {block: i + 1 for i, block in enumerate(candidates)}
    coverage = []
    points = set(range(1, 13))
    for target in residual:
        rest = sorted(points.difference(target))
        coverage.append(
            tuple(
                index[tuple(sorted(target + extra))]
                for extra in combinations(rest, 2)
            )
        )
    last, global_counter = forward_at_most_clauses(
        list(range(1, len(candidates) + 1)), 36, len(candidates) + 1
    )
    extra_counters: list[tuple[int, ...]] = []
    if degree_bounds:
        fixed_degree = Counter(point for block in link for point in block)
        for point in range(1, 13):
            # A completed cover has exactly 77 blocks and every point degree is
            # at least 41.  If d fixed blocks contain this point, at most d-5
            # of the 36 variable blocks can avoid it.
            avoiding = [
                i + 1 for i, block in enumerate(candidates) if point not in block
            ]
            last, point_counter = forward_at_most_clauses(
                avoiding, fixed_degree[point] - 5, last + 1
            )
            extra_counters.extend(point_counter)
    if capacity_bound:
        # A variable seven-block covers at most 16 of the 546 residual
        # five-sets for this fixed link.  Exactly 36 variable blocks are
        # necessary, so their aggregate deficit from 36*16=576 is at most
        # 576-546=30.  Repeated literals encode the small integer weights.
        target_set = set(residual)
        weighted_primaries: list[int] = []
        for i, block in enumerate(candidates, 1):
            capacity = sum(target in target_set for target in combinations(block, 5))
            weighted_primaries.extend([i] * (16 - capacity))
        last, capacity_counter = forward_at_most_clauses(
            weighted_primaries, 30, last + 1
        )
        extra_counters.extend(capacity_counter)
    forced_clause: tuple[tuple[int, ...], ...] = ()
    if force_block is not None:
        canonical_force = tuple(sorted(force_block))
        if canonical_force not in index:
            raise ValueError("--force-block must be a seven-subset of 1,...,12")
        forced_clause = ((index[canonical_force],),)
    clauses = (*coverage, *forced_clause, *global_counter, *extra_counters)
    with cnf_path.open("w", encoding="ascii", newline="\n") as handle:
        handle.write("c extension of a fixed 41-block C(12,6,4) link\n")
        handle.write("c primary variables are lexicographic 7-subsets of 1,...,12\n")
        handle.write("c at most 36 variable blocks; fixed blocks all contain point 0\n")
        if degree_bounds:
            handle.write(
                "c point-degree bounds use C(12,6,4)=41 and C(13,7,5)>=77\n"
            )
        if capacity_bound:
            handle.write("c aggregate residual-capacity deficit is at most 30\n")
        if force_block is not None:
            handle.write("c forced variable block: " + " ".join(map(str, force_block)) + "\n")
        handle.write(f"p cnf {last} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")
    print(
        f"wrote {cnf_path}: fixed=41, residual_targets={len(residual)}, "
        f"candidates={len(candidates)}, variables={last}, clauses={len(clauses)}"
    )


def check(link_path: Path, model_path: Path) -> None:
    link = read_link(link_path)
    candidates = candidate_blocks()
    positives = parse_model(model_path)
    selected = [block for i, block in enumerate(candidates, 1) if i in positives]
    if len(selected) > 36:
        raise ValueError(f"selected {len(selected)} variable blocks")
    full = [(0, *block) for block in link] + selected
    if len(set(full)) != len(full):
        raise ValueError("duplicate full blocks")
    multiplicity = Counter()
    uncovered = []
    full_sets = [set(block) for block in full]
    for target in combinations(range(13), 5):
        count = sum(set(target) <= block for block in full_sets)
        multiplicity[count] += 1
        if count == 0:
            uncovered.append(target)
    if uncovered:
        raise ValueError(f"{len(uncovered)} uncovered targets; first={uncovered[0]}")
    degrees = Counter(point for block in full for point in block)
    print(f"verified full cover with {len(full)} distinct blocks")
    print("point degrees:", tuple(degrees[p] for p in range(13)))
    print("5-set multiplicities:", dict(sorted(multiplicity.items())))
    print("variable blocks:")
    for block in selected:
        print(" ".join(map(str, block)))


def main() -> None:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    gen = commands.add_parser("generate")
    gen.add_argument("link", type=Path)
    gen.add_argument("cnf", type=Path)
    gen.add_argument(
        "--degree-bounds",
        action="store_true",
        help="add sound lower point-degree consequences via avoidance counters",
    )
    gen.add_argument(
        "--capacity-bound",
        action="store_true",
        help="add the implied weighted residual-capacity deficit bound",
    )
    gen.add_argument(
        "--force-block",
        nargs=7,
        type=int,
        metavar=("A", "B", "C", "D", "E", "F", "G"),
        help="force one seven-block (for an explicitly justified symmetry branch)",
    )
    chk = commands.add_parser("check-model")
    chk.add_argument("link", type=Path)
    chk.add_argument("model", type=Path)
    args = parser.parse_args()
    if args.command == "generate":
        generate(
            args.link,
            args.cnf,
            args.degree_bounds,
            args.capacity_bound,
            tuple(args.force_block) if args.force_block is not None else None,
        )
    else:
        check(args.link, args.model)


if __name__ == "__main__":
    main()
