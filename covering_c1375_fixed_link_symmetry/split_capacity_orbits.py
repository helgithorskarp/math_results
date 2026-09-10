#!/usr/bin/env python3
"""Split an exact prime-order invariant CNF by a capacity-16 orbit.

For a fixed link, every 36-block completion selects at least six capacity-16
blocks.  In a prime-order invariant completion these blocks occur in cyclic
orbits.  This script computes the centralizer of the chosen automorphism in the
link automorphism group and writes one forced-orbit CNF per centralizer orbit
of capacity-16 cyclic block orbits.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path

from analyze_fixed_link import image
from fixed_link_extension import candidate_blocks, read_link, residual_targets
from fixed_link_invariant import cyclic_orbits

from augment_prime_exact import read_case


PERMUTATION_RE = re.compile(
    r"^c permutation images of points 1,\.\.\.,12: ((?:[1-9]|1[0-2])(?: (?:[1-9]|1[0-2])){11})$"
)


def read_permutation(comments: list[str]) -> tuple[int, ...]:
    matches = [PERMUTATION_RE.match(comment) for comment in comments]
    payloads = [match.group(1) for match in matches if match]
    if len(payloads) != 1:
        raise ValueError(f"expected one permutation comment, got {len(payloads)}")
    permutation = tuple(map(int, payloads[0].split()))
    if sorted(permutation) != list(range(1, 13)):
        raise ValueError("permutation comment is not a permutation")
    return permutation


def commutes(left: tuple[int, ...], right: tuple[int, ...]) -> bool:
    return all(left[right[x - 1] - 1] == right[left[x - 1] - 1] for x in range(1, 13))


def centralizer_lifts(
    link: list[tuple[int, ...]], generator: tuple[int, ...]
) -> list[tuple[int, ...]]:
    degrees = Counter(point for block in link for point in block)
    low = tuple(point for point in range(1, 13) if degrees[point] == 20)
    high = tuple(point for point in range(1, 13) if degrees[point] != 20)
    if len(low) != 6 or len(high) != 6:
        raise ValueError("expected two six-point degree classes")
    link_set = set(map(frozenset, link))
    lifts: list[tuple[int, ...]] = []
    for low_images in permutations(low):
        partial = dict(zip(low, low_images))
        if any(
            partial[generator[x - 1]] != generator[partial[x] - 1]
            for x in low
        ):
            continue
        found: list[tuple[int, ...]] = []
        for high_images in permutations(high):
            mapping = {**partial, **dict(zip(high, high_images))}
            permutation = tuple(mapping[x] for x in range(1, 13))
            if {image(block, permutation) for block in link_set} == link_set:
                found.append(permutation)
        if len(found) != 1:
            raise AssertionError(
                f"low action {low_images} has {len(found)} lifts instead of one"
            )
        if not commutes(found[0], generator):
            raise AssertionError("faithful low-action centralizer did not lift centrally")
        lifts.extend(found)
    if not lifts or tuple(range(1, 13)) not in lifts:
        raise AssertionError("centralizer lift enumeration failed")
    return lifts


def capacity16_orbit_representatives(
    link: list[tuple[int, ...]], generator: tuple[int, ...]
) -> tuple[list[int], int, int]:
    block_orbits = cyclic_orbits(candidate_blocks(), generator)
    orbit_of = {
        block: variable
        for variable, orbit in enumerate(block_orbits, 1)
        for block in orbit
    }
    residual = set(map(frozenset, residual_targets(link)))
    capacity16 = []
    for variable, orbit in enumerate(block_orbits, 1):
        capacities = {
            sum(target <= block for target in residual)
            for block in orbit
        }
        if len(capacities) != 1:
            raise AssertionError("capacity is not constant on a cyclic orbit")
        if capacities.pop() == 16:
            capacity16.append(variable)
    centralizer = centralizer_lifts(link, generator)
    remaining = set(capacity16)
    representatives = []
    while remaining:
        start = min(remaining)
        block = min(block_orbits[start - 1], key=lambda item: tuple(sorted(item)))
        centralizer_orbit = {orbit_of[image(block, symmetry)] for symmetry in centralizer}
        if not centralizer_orbit <= set(capacity16):
            raise AssertionError("centralizer failed to preserve capacity 16")
        representatives.append(min(centralizer_orbit))
        remaining.difference_update(centralizer_orbit)
    return representatives, len(capacity16), len(centralizer)


def generate(link_path: Path, input_path: Path, output_dir: Path) -> None:
    link = read_link(link_path)
    comments, clauses, variables, orbit_sizes = read_case(input_path)
    generator = read_permutation(comments)
    block_orbits = cyclic_orbits(candidate_blocks(), generator)
    if len(block_orbits) != len(orbit_sizes):
        raise AssertionError("CNF orbit comments disagree with reconstructed orbits")
    if [len(orbit) for orbit in block_orbits] != orbit_sizes:
        raise AssertionError("CNF orbit ordering disagrees with reconstruction")
    representatives, capacity16_count, centralizer_order = (
        capacity16_orbit_representatives(link, generator)
    )
    source_hash = hashlib.sha256(input_path.read_bytes()).hexdigest()
    output_dir.mkdir(parents=True, exist_ok=True)
    print(
        f"centralizer_order={centralizer_order} capacity16_orbits={capacity16_count} "
        f"centralizer_classes={len(representatives)} representatives={representatives}"
    )
    for representative in representatives:
        output_path = output_dir / f"{input_path.stem}-cap16-orbit-{representative}.cnf"
        branch_clauses = clauses + [(representative,)]
        with output_path.open("w", encoding="ascii", newline="\n") as handle:
            for comment in comments:
                handle.write(comment + "\n")
            handle.write(f"c source exact-count CNF SHA-256: {source_hash}\n")
            handle.write(
                f"c force capacity-16 cyclic block orbit variable {representative}\n"
            )
            handle.write(
                f"c exhaustive under link centralizer of order {centralizer_order}; "
                f"{len(representatives)} branches\n"
            )
            handle.write(f"p cnf {variables} {len(branch_clauses)}\n")
            for clause in branch_clauses:
                handle.write(" ".join(map(str, clause)) + " 0\n")
        print(f"{output_path.name}: variables={variables} clauses={len(branch_clauses)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("link", type=Path)
    parser.add_argument("input", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    generate(args.link, args.input, args.output_dir)


if __name__ == "__main__":
    main()
