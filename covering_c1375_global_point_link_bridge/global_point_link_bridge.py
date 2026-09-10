#!/usr/bin/env python3
"""Exact global point-pair reduction for a 77-block C(13,7,5) cover.

The generator has two exhaustive cases.  Case e0 fixes two degree-41 points
of pair multiplicity 20.  Case e1 is the complementary situation: the point
degrees are 41^7,42^6, pairs within the degree-41 class have multiplicity 21,
and cross-pairs have multiplicity 20.  In both cases the 20 blocks through
the distinguished pair are the unique optimal C(11,5,3) second link.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from typing import Sequence

from pysat.formula import CNF
from pysat.pb import EncType, PBEnc
from pysat.solvers import Solver


GROUND = tuple(range(13))
REMAINDER = tuple(range(2, 13))
SHADOW_LOWER = {1: 41, 2: 20, 3: 9, 4: 3}


def read_source_link(path: Path) -> list[tuple[int, ...]]:
    blocks = []
    for raw in path.read_text(encoding="ascii").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            blocks.append(tuple(sorted(map(int, line.split()))))
    if len(blocks) != 41 or len(set(blocks)) != 41:
        raise ValueError("source link must have 41 distinct blocks")
    if any(len(block) != 6 or not set(block) <= set(range(1, 13)) for block in blocks):
        raise ValueError("source blocks must be six-subsets of 1,...,12")
    block_sets = tuple(map(frozenset, blocks))
    for target in combinations(range(1, 13), 4):
        if not any(frozenset(target) <= block for block in block_sets):
            raise ValueError(f"source link misses quadruple {target}")
    if sum(1 in block for block in blocks) != 20:
        raise ValueError("point 1 must have source-link degree 20")
    return blocks


def second_link(path: Path) -> list[tuple[int, ...]]:
    source = read_source_link(path)
    blocks = [tuple(point for point in block if point != 1) for block in source if 1 in block]
    if len(blocks) != 20 or len(set(blocks)) != 20:
        raise AssertionError("second link is not a 20-block simple family")
    block_sets = tuple(map(frozenset, blocks))
    for target in combinations(REMAINDER, 3):
        if not any(frozenset(target) <= block for block in block_sets):
            raise AssertionError(f"second link misses triple {target}")
    return blocks


def second_link_text(blocks: Sequence[tuple[int, ...]]) -> str:
    return "".join(" ".join(map(str, block)) + "\n" for block in blocks)


def append_pb(
    clauses: list[tuple[int, ...]],
    top: int,
    relation: str,
    literals: Sequence[int],
    bound: int,
) -> tuple[int, int]:
    function = {
        "atleast": PBEnc.atleast,
        "equals": PBEnc.equals,
    }[relation]
    encoded = function(
        lits=list(literals), bound=bound, top_id=top, encoding=EncType.bdd
    )
    clauses.extend(map(tuple, encoded.clauses))
    return max(top, encoded.nv), len(encoded.clauses)


def primary_families() -> tuple[
    list[tuple[int, ...]], list[tuple[int, ...]], list[tuple[int, ...]]
]:
    b_blocks = [(0, *block) for block in combinations(REMAINDER, 6)]
    c_blocks = [(1, *block) for block in combinations(REMAINDER, 6)]
    d_blocks = list(combinations(REMAINDER, 7))
    assert (len(b_blocks), len(c_blocks), len(d_blocks)) == (462, 462, 330)
    return b_blocks, c_blocks, d_blocks


def automorphisms(blocks: Sequence[tuple[int, ...]]) -> list[tuple[int, ...]]:
    """Exhaustively search a pair-multiplicity supergroup of Aut(blocks)."""
    point_degree = Counter(point for block in blocks for point in block)
    pair_degree = Counter(pair for block in blocks for pair in combinations(block, 2))
    block_set = set(map(frozenset, blocks))
    order = sorted(REMAINDER, key=lambda point: (-point_degree[point], point))
    candidates = {
        point: tuple(q for q in REMAINDER if point_degree[q] == point_degree[point])
        for point in REMAINDER
    }
    mapping: dict[int, int] = {}
    used: set[int] = set()
    found: list[tuple[int, ...]] = []

    def recurse(position: int) -> None:
        if position == len(order):
            image = {frozenset(mapping[p] for p in block) for block in blocks}
            if image == block_set:
                found.append(tuple(mapping[p] for p in REMAINDER))
            return
        point = order[position]
        for image_point in candidates[point]:
            if image_point in used:
                continue
            if any(
                pair_degree[tuple(sorted((point, prior)))]
                != pair_degree[tuple(sorted((image_point, mapping[prior])))]
                for prior in mapping
            ):
                continue
            mapping[point] = image_point
            used.add(image_point)
            recurse(position + 1)
            used.remove(image_point)
            del mapping[point]

    recurse(0)
    if len(found) != len(set(found)):
        raise AssertionError("duplicate automorphisms")
    return found


def high_set_orbits(blocks: Sequence[tuple[int, ...]]) -> list[tuple[tuple[int, ...], int]]:
    group = automorphisms(blocks)
    domain = set(combinations(REMAINDER, 6))
    unseen = set(domain)
    rows = []
    while unseen:
        representative = min(unseen)
        orbit = {
            tuple(sorted(permutation[point - 2] for point in representative))
            for permutation in group
        }
        if not orbit <= domain:
            raise AssertionError("orbit leaves the six-subset domain")
        unseen.difference_update(orbit)
        rows.append((representative, len(orbit)))
    if sum(size for _, size in rows) != len(domain):
        raise AssertionError("orbits do not partition the domain")
    return rows


def generate(
    source_path: Path,
    output_path: Path,
    case: str,
    high_tuple: tuple[int, ...] | None,
    max_shadow: int,
) -> None:
    if case not in {"e0", "e1"}:
        raise ValueError("case must be e0 or e1")
    if not 0 <= max_shadow <= 4:
        raise ValueError("--max-shadow must lie in 0,...,4")
    if case == "e0" and high_tuple is not None:
        raise ValueError("--high-set is only valid in case e1")
    if case == "e1":
        if high_tuple is None:
            raise ValueError("case e1 requires --high-set")
        high_tuple = tuple(sorted(high_tuple))
        if len(high_tuple) != 6 or len(set(high_tuple)) != 6:
            raise ValueError("--high-set needs six distinct points")
        if not set(high_tuple) <= set(REMAINDER):
            raise ValueError("--high-set points must lie in 2,...,12")

    second = second_link(source_path)
    fixed = [(0, 1, *block) for block in second]
    fixed_sets = tuple(map(frozenset, fixed))
    b_blocks, c_blocks, d_blocks = primary_families()
    primary = b_blocks + c_blocks + d_blocks
    primary_sets = tuple(map(frozenset, primary))
    b_vars = list(range(1, 463))
    c_vars = list(range(463, 925))
    d_vars = list(range(925, 1255))
    excess = 0 if case == "e0" else 1

    clauses: list[tuple[int, ...]] = []
    width_hist: Counter[int] = Counter()
    for target in combinations(GROUND, 5):
        target_set = frozenset(target)
        if any(target_set <= block for block in fixed_sets):
            continue
        clause = tuple(
            variable
            for variable, block in enumerate(primary_sets, 1)
            if target_set <= block
        )
        if not clause:
            raise AssertionError(f"no primary block covers {target}")
        clauses.append(clause)
        width_hist[len(clause)] += 1
    coverage_clauses = len(clauses)

    top = len(primary)
    exact_rows = []
    for name, variables, count in (
        ("B", b_vars, 21),
        ("C", c_vars, 21 + excess),
        ("D", d_vars, 15 - excess),
    ):
        top, added = append_pb(clauses, top, "equals", variables, count)
        exact_rows.append(f"{name}:{count}:{added}")

    shadow_rows = []
    for size in range(1, max_shadow + 1):
        lower = SHADOW_LOWER[size]
        added_clauses = constraints = 0
        for subset in combinations(GROUND, size):
            subset_set = frozenset(subset)
            fixed_count = sum(subset_set <= block for block in fixed_sets)
            need = max(0, lower - fixed_count)
            variables = [
                variable
                for variable, block in enumerate(primary_sets, 1)
                if subset_set <= block
            ]
            if need:
                top, added = append_pb(clauses, top, "atleast", variables, need)
                constraints += 1
                added_clauses += added
        shadow_rows.append(f"{size}:{constraints}:{added_clauses}")

    hard_rows = []
    pair_row = ""
    if case == "e1":
        assert high_tuple is not None
        high = set(high_tuple)
        second_degree = Counter(point for block in second for point in block)
        for point in REMAINDER:
            b_containing = [
                variable for variable, block in zip(b_vars, b_blocks) if point in block
            ]
            b_target = 20 + int(point in high) - second_degree[point]
            top, b_added = append_pb(clauses, top, "equals", b_containing, b_target)
            all_containing = [
                variable
                for variable, block in enumerate(primary, 1)
                if point in block
            ]
            full_target = 41 + int(point not in high) - second_degree[point]
            top, full_added = append_pb(
                clauses, top, "equals", all_containing, full_target
            )
            hard_rows.append(
                f"{point}:B={b_target}:{b_added}:all={full_target}:{full_added}"
            )

        degree_41 = {0, *high}
        relation_hist: Counter[str] = Counter()
        pair_clauses = 0
        for left, right in combinations(GROUND, 2):
            pair = frozenset((left, right))
            fixed_count = sum(pair <= block for block in fixed_sets)
            variables = [
                variable
                for variable, block in enumerate(primary_sets, 1)
                if pair <= block
            ]
            if left in degree_41 and right in degree_41:
                relation, total, label = "equals", 21, "A-A=21"
            elif (left in degree_41) != (right in degree_41):
                relation, total, label = "equals", 20, "A-B=20"
            else:
                relation, total, label = "atleast", 20, "B-B>=20"
            target = total - fixed_count
            if variables or target:
                top, added = append_pb(clauses, top, relation, variables, target)
                pair_clauses += added
            relation_hist[label] += 1
        pair_row = " ".join(
            f"{label}:{relation_hist[label]}"
            for label in ("A-A=21", "A-B=20", "B-B>=20")
        ) + f" clauses={pair_clauses}"

    source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    second_hash = hashlib.sha256(second_link_text(second).encode("ascii")).hexdigest()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="ascii", newline="\n") as handle:
        handle.write("c exact global point-pair bridge for C(13,7,5) <= 77\n")
        handle.write(f"c case={case} source_link_sha256={source_hash}\n")
        handle.write(f"c canonical_second_link_sha256={second_hash}\n")
        handle.write("c primary ranges B=1..462 C=463..924 D=925..1254\n")
        handle.write(
            f"c fixed=20 coverage_clauses={coverage_clauses} width_hist="
            + ",".join(f"{width}:{width_hist[width]}" for width in sorted(width_hist))
            + "\n"
        )
        handle.write("c exact categories " + " ".join(exact_rows) + "\n")
        if shadow_rows:
            handle.write("c shadows size:constraints:clauses " + " ".join(shadow_rows) + "\n")
        if case == "e1":
            handle.write("c hard-e1 high set " + " ".join(map(str, high_tuple or ())) + "\n")
            handle.write("c hard-e1 point constraints " + " ".join(hard_rows) + "\n")
            handle.write("c hard-e1 pair constraints " + pair_row + "\n")
        handle.write(f"p cnf {top} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")
    print(
        f"case={case} variables={top} clauses={len(clauses)} "
        f"coverage={coverage_clauses} exact={' '.join(exact_rows)}"
    )


def parse_model(path: Path) -> set[int]:
    positives: set[int] = set()
    saw_sat = False
    for raw in path.read_text(encoding="ascii", errors="strict").splitlines():
        line = raw.strip()
        if line in {"s SATISFIABLE", "SAT"}:
            saw_sat = True
        if line.startswith("v "):
            for token in line.split()[1:]:
                literal = int(token)
                if literal > 0:
                    positives.add(literal)
    if not saw_sat:
        raise ValueError("model has no SAT status")
    return positives


def check_model(
    source_path: Path,
    model_path: Path,
    case: str,
    high_tuple: tuple[int, ...] | None,
) -> None:
    if case == "e1" and high_tuple is None:
        raise ValueError("case e1 needs --high-set")
    second = second_link(source_path)
    fixed = [(0, 1, *block) for block in second]
    families = primary_families()
    primary = families[0] + families[1] + families[2]
    positives = parse_model(model_path)
    chosen = [variable for variable in range(1, 1255) if variable in positives]
    excess = 0 if case == "e0" else 1
    counts = (
        sum(variable <= 462 for variable in chosen),
        sum(463 <= variable <= 924 for variable in chosen),
        sum(variable >= 925 for variable in chosen),
    )
    if counts != (21, 21 + excess, 15 - excess):
        raise ValueError(f"category counts {counts}")
    selected = fixed + [primary[variable - 1] for variable in chosen]
    if len(selected) != 77 or len(set(selected)) != 77:
        raise ValueError("model does not select 77 distinct blocks")
    selected_sets = tuple(map(frozenset, selected))
    for target in combinations(GROUND, 5):
        if not any(frozenset(target) <= block for block in selected_sets):
            raise ValueError(f"uncovered five-set {target}")
    degrees = tuple(sum(point in block for block in selected) for point in GROUND)
    if degrees[0] != 41 or degrees[1] != 41 + excess:
        raise ValueError(f"root degrees {degrees[:2]}")
    if case == "e1":
        high = set(high_tuple or ())
        degree_41 = {0, *high}
        if any(degrees[p] != (41 if p in degree_41 else 42) for p in GROUND):
            raise ValueError(f"hard-e1 point degrees {degrees}")
        pair_degree = Counter(pair for block in selected for pair in combinations(block, 2))
        for left, right in combinations(GROUND, 2):
            value = pair_degree[(left, right)]
            if left in degree_41 and right in degree_41 and value != 21:
                raise ValueError((left, right, value, "expected 21"))
            if (left in degree_41) != (right in degree_41) and value != 20:
                raise ValueError((left, right, value, "expected 20"))
            if left not in degree_41 and right not in degree_41 and value < 20:
                raise ValueError((left, right, value, "expected at least 20"))
    print(f"verified case={case} blocks=77 categories={counts} degrees={degrees}")


def print_orbits(source_path: Path) -> None:
    second = second_link(source_path)
    group = automorphisms(second)
    rows = high_set_orbits(second)
    print(f"automorphisms={len(group)}")
    print(f"six_subset_orbits={len(rows)} domain=462")
    print("orbit\tsize\trepresentative")
    for index, (representative, size) in enumerate(rows):
        print(f"{index}\t{size}\t" + " ".join(map(str, representative)))


def self_test(source_path: Path) -> None:
    second = second_link(source_path)
    degree = Counter(point for block in second for point in block)
    if sorted(degree.values()) != [9] * 10 + [10]:
        raise AssertionError(f"unexpected second-link degrees {degree}")
    group = automorphisms(second)
    rows = high_set_orbits(second)
    if len(group) != 240 or len(rows) != 12 or sum(size for _, size in rows) != 462:
        raise AssertionError((len(group), len(rows), sum(size for _, size in rows)))
    for n in range(1, 7):
        variables = list(range(1, n + 1))
        for relation in ("atleast", "equals"):
            for bound in range(n + 1):
                clauses: list[tuple[int, ...]] = []
                append_pb(clauses, n, relation, variables, bound)
                with Solver(name="cadical195", bootstrap_with=CNF(from_clauses=clauses)) as solver:
                    for values in product((False, True), repeat=n):
                        assumptions = [
                            variable if value else -variable
                            for variable, value in zip(variables, values)
                        ]
                        weight = sum(values)
                        expected = weight >= bound if relation == "atleast" else weight == bound
                        if solver.solve(assumptions=assumptions) != expected:
                            raise AssertionError((n, relation, bound, values))
    print(
        "self-test passed: second link, group=240, 12 orbits covering 462 sets, "
        "and PB truth tables"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    test = commands.add_parser("self-test")
    test.add_argument("source_link", type=Path)
    orbit = commands.add_parser("orbits")
    orbit.add_argument("source_link", type=Path)
    generate_parser = commands.add_parser("generate")
    generate_parser.add_argument("source_link", type=Path)
    generate_parser.add_argument("output", type=Path)
    generate_parser.add_argument("--case", choices=("e0", "e1"), required=True)
    generate_parser.add_argument("--high-set", nargs=6, type=int)
    generate_parser.add_argument("--max-shadow", type=int, default=0)
    check = commands.add_parser("check-model")
    check.add_argument("source_link", type=Path)
    check.add_argument("model", type=Path)
    check.add_argument("--case", choices=("e0", "e1"), required=True)
    check.add_argument("--high-set", nargs=6, type=int)
    args = parser.parse_args()
    if args.command == "self-test":
        self_test(args.source_link)
    elif args.command == "orbits":
        print_orbits(args.source_link)
    elif args.command == "generate":
        generate(
            args.source_link,
            args.output,
            args.case,
            tuple(args.high_set) if args.high_set is not None else None,
            args.max_shadow,
        )
    else:
        check_model(
            args.source_link,
            args.model,
            args.case,
            tuple(args.high_set) if args.high_set is not None else None,
        )


if __name__ == "__main__":
    main()
