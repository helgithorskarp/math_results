#!/usr/bin/env python3
"""Add exact orbit-union deficit and pair-overlap cuts to an exact-36 CNF."""

from __future__ import annotations

import argparse
import hashlib
from itertools import combinations
from math import gcd
from pathlib import Path

from pysat.pb import EncType, PBEnc

from fixed_link_extension import candidate_blocks, read_link, residual_targets
from fixed_link_invariant import cyclic_orbits

from augment_prime_exact import read_case
from split_capacity_orbits import read_permutation


def strengthen(
    link_path: Path, input_path: Path, output_path: Path, encoder_name: str
) -> None:
    link = read_link(link_path)
    comments, clauses, variables, orbit_sizes = read_case(input_path)
    generator = read_permutation(comments)
    block_orbits = cyclic_orbits(candidate_blocks(), generator)
    if [len(orbit) for orbit in block_orbits] != orbit_sizes:
        raise AssertionError("CNF orbit ordering disagrees with reconstruction")
    residual = set(map(frozenset, residual_targets(link)))
    coverage_sets: list[set[frozenset[int]]] = []
    deficits: list[int] = []
    for orbit in block_orbits:
        covered = {
            target
            for block in orbit
            for target in map(frozenset, combinations(block, 5))
            if target in residual
        }
        deficit = 16 * len(orbit) - len(covered)
        if deficit < 0:
            raise AssertionError("orbit covers more than 16 residual targets per block")
        coverage_sets.append(covered)
        deficits.append(deficit)

    divisor = 30
    for deficit in deficits:
        divisor = gcd(divisor, deficit)
    normalized_bound = 30 // divisor
    positive = [
        (i, deficit // divisor)
        for i, deficit in enumerate(deficits, 1)
        if deficit
    ]
    encoders = {"pb-bdd": EncType.bdd, "pb-binmerge": EncType.binmerge}
    encoded = PBEnc.atmost(
        lits=[variable for variable, _ in positive],
        weights=[weight for _, weight in positive],
        bound=normalized_bound,
        top_id=variables,
        encoding=encoders[encoder_name],
    )
    union_deficit_clauses = list(map(tuple, encoded.clauses))
    last_variable = max(variables, encoded.nv)
    conflict_clauses = []
    for left, right in combinations(range(len(block_orbits)), 2):
        overlap = len(coverage_sets[left] & coverage_sets[right])
        if deficits[left] + deficits[right] + overlap > 30:
            conflict_clauses.append((-(left + 1), -(right + 1)))
    all_clauses = clauses + union_deficit_clauses + conflict_clauses
    source_hash = hashlib.sha256(input_path.read_bytes()).hexdigest()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="ascii", newline="\n") as handle:
        for comment in comments:
            handle.write(comment + "\n")
        handle.write(f"c source exact-count CNF SHA-256: {source_hash}\n")
        handle.write(
            f"c exact orbit-union deficit at most 30, divided by gcd {divisor}; "
            f"{len(union_deficit_clauses)} {encoder_name} clauses\n"
        )
        handle.write(
            "c pair overlap plus the two union deficits at most 30; "
            f"{len(conflict_clauses)} binary incompatibility clauses\n"
        )
        handle.write(f"p cnf {last_variable} {len(all_clauses)}\n")
        for clause in all_clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")
    print(
        f"{output_path.name}: variables={last_variable} clauses={len(all_clauses)} "
        f"union_deficit_clauses={len(union_deficit_clauses)} "
        f"pair_conflicts={len(conflict_clauses)} "
        f"positive_deficits={len(positive)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("link", type=Path)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--encoder", choices=("pb-binmerge", "pb-bdd"), default="pb-binmerge"
    )
    args = parser.parse_args()
    strengthen(args.link, args.input, args.output, args.encoder)


if __name__ == "__main__":
    main()
