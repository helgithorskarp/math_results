#!/usr/bin/env python3
"""Generate exact cases for fixed-link completions with a nontrivial symmetry."""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
from pathlib import Path

from analyze_fixed_link import automorphisms, image
from c1375_sat import forward_at_most_clauses
from fixed_link_extension import candidate_blocks, read_link, residual_targets


def cycle_type(permutation: tuple[int, ...], domain: tuple[int, ...]) -> tuple[int, ...]:
    remaining = set(domain)
    lengths = []
    while remaining:
        start = min(remaining)
        current = start
        length = 0
        while True:
            remaining.remove(current)
            length += 1
            current = permutation[current - 1]
            if current == start:
                break
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def cyclic_orbits(
    blocks: list[tuple[int, ...]], permutation: tuple[int, ...]
) -> list[set[frozenset[int]]]:
    remaining = set(map(frozenset, blocks))
    result = []
    while remaining:
        start = min(remaining, key=lambda block: tuple(sorted(block)))
        orbit = set()
        current = start
        while current not in orbit:
            orbit.add(current)
            current = image(current, permutation)
        if current != start or not orbit <= remaining:
            raise AssertionError("cyclic orbit construction failed")
        result.append(orbit)
        remaining.difference_update(orbit)
    return result


def append_counter(
    clauses: list[tuple[int, ...]],
    weighted_variables: list[int],
    limit: int,
    last_variable: int,
) -> int:
    last_variable, generated = forward_at_most_clauses(
        weighted_variables, limit, last_variable + 1
    )
    clauses.extend(generated)
    return last_variable


def append_weighted_bound(
    clauses: list[tuple[int, ...]],
    variables: list[int],
    weights: list[int],
    limit: int,
    last_variable: int,
    encoder: str,
) -> int:
    positive = [(variable, weight) for variable, weight in zip(variables, weights) if weight]
    if encoder == "unary":
        expanded = [variable for variable, weight in positive for _ in range(weight)]
        return append_counter(clauses, expanded, limit, last_variable)
    from pysat.pb import EncType, PBEnc

    pb_encoding = EncType.bdd if encoder == "pb-bdd" else EncType.binmerge

    encoded = PBEnc.atmost(
        lits=[variable for variable, _ in positive],
        weights=[weight for _, weight in positive],
        bound=limit,
        top_id=last_variable,
        encoding=pb_encoding,
    )
    clauses.extend(map(tuple, encoded.clauses))
    return max(last_variable, encoded.nv)


def write_case(
    path: Path,
    link: list[tuple[int, ...]],
    permutation: tuple[int, ...],
    kind: tuple[int, ...],
    encoder: str,
) -> None:
    residual = residual_targets(link)
    residual_sets = list(map(frozenset, residual))
    residual_set = set(residual_sets)
    orbits = cyclic_orbits(candidate_blocks(), permutation)
    variables = list(range(1, len(orbits) + 1))
    orbit_coverage = []
    orbit_capacity = []
    for orbit in orbits:
        covered = {
            target
            for block in orbit
            for target in map(frozenset, combinations(block, 5))
            if target in residual_set
        }
        orbit_coverage.append(covered)
        per_block = {len(covered & set(map(frozenset, combinations(block, 5)))) for block in orbit}
        if len(per_block) != 1:
            raise AssertionError("capacity differs within a cyclic orbit")
        orbit_capacity.append(per_block.pop())

    clauses = []
    for target in residual_sets:
        clause = tuple(
            variable
            for variable, covered in zip(variables, orbit_coverage)
            if target in covered
        )
        if not clause:
            raise AssertionError(f"no orbit can cover residual target {target}")
        clauses.append(clause)

    last = len(orbits)
    last = append_weighted_bound(
        clauses,
        variables,
        [len(orbit) for orbit in orbits],
        36,
        last,
        encoder,
    )

    last = append_weighted_bound(
        clauses,
        variables,
        [len(orbit) * (16 - capacity) for orbit, capacity in zip(orbits, orbit_capacity)],
        30,
        last,
        encoder,
    )

    fixed_degree = Counter(point for block in link for point in block)
    for point in range(1, 13):
        last = append_weighted_bound(
            clauses,
            variables,
            [sum(point not in block for block in orbit) for orbit in orbits],
            fixed_degree[point] - 5,
            last,
            encoder,
        )

    with path.open("w", encoding="ascii", newline="\n") as handle:
        handle.write("c nontrivial-symmetry case for a fixed C(12,6,4) link\n")
        handle.write(f"c weighted-cardinality encoder: {encoder}\n")
        handle.write("c cycle type on degree-20 points: " + "-".join(map(str, kind)) + "\n")
        handle.write("c permutation images of points 1,...,12: " + " ".join(map(str, permutation)) + "\n")
        for variable, orbit, capacity in zip(variables, orbits, orbit_capacity):
            representative = min(orbit, key=lambda block: tuple(sorted(block)))
            handle.write(
                f"c orbit {variable} size={len(orbit)} capacity={capacity} rep="
                + " ".join(map(str, sorted(representative)))
                + "\n"
            )
        handle.write(f"p cnf {last} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")
    print(
        f"{path.name}: type={'-'.join(map(str, kind))} orbit_vars={len(orbits)} "
        f"variables={last} clauses={len(clauses)}"
    )


def generate_all(link_path: Path, output_dir: Path, encoder: str) -> None:
    link = read_link(link_path)
    degree = Counter(point for block in link for point in block)
    low = tuple(point for point in range(1, 13) if degree[point] == 20)
    representatives: dict[tuple[int, ...], tuple[int, ...]] = {}
    for permutation in automorphisms(link):
        kind = cycle_type(permutation, low)
        representatives[kind] = min(permutation, representatives.get(kind, permutation))
    if len(representatives) != 11 or (1, 1, 1, 1, 1, 1) not in representatives:
        raise AssertionError(f"unexpected S_6 cycle types: {sorted(representatives)}")
    output_dir.mkdir(parents=True, exist_ok=True)
    for kind in sorted(representatives):
        if kind == (1, 1, 1, 1, 1, 1):
            continue
        stem = "cycle-" + "-".join(map(str, kind))
        write_case(
            output_dir / f"{stem}.cnf",
            link,
            representatives[kind],
            kind,
            encoder,
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("link", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument(
        "--encoder",
        choices=("pb-binmerge", "pb-bdd", "unary"),
        default="pb-binmerge",
    )
    args = parser.parse_args()
    generate_all(args.link, args.output_dir, args.encoder)


if __name__ == "__main__":
    main()
