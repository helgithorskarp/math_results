#!/usr/bin/env python3
"""Exact symmetry and residual-capacity audit for a fixed C(12,6,4) link."""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path

from fixed_link_extension import candidate_blocks, read_link, residual_targets


def automorphisms(link: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    block_set = {frozenset(block) for block in link}
    degree = Counter(point for block in link for point in block)
    degree_classes = [
        tuple(point for point in range(1, 13) if degree[point] == value)
        for value in sorted(set(degree.values()))
    ]
    if tuple(map(len, degree_classes)) != (6, 6):
        raise ValueError(f"expected two six-point degree classes, got {degree_classes}")
    low, high = degree_classes
    result = []
    for low_image in permutations(low):
        partial = dict(zip(low, low_image))
        for high_image in permutations(high):
            mapping = partial | dict(zip(high, high_image))
            if all(
                frozenset(mapping[point] for point in block) in block_set
                for block in block_set
            ):
                result.append(tuple(mapping[point] for point in range(1, 13)))
    return result


def image(block: frozenset[int], permutation: tuple[int, ...]) -> frozenset[int]:
    return frozenset(permutation[point - 1] for point in block)


def analyze(link_path: Path) -> None:
    link = read_link(link_path)
    residual = residual_targets(link)
    covered = {
        frozenset(target)
        for block in link
        for target in combinations(block, 5)
    }
    if len(covered) != 246:
        raise AssertionError(f"expected 246 singly covered five-sets, got {len(covered)}")
    if len(residual) != 546:
        raise AssertionError(f"expected 546 residual five-sets, got {len(residual)}")

    group = automorphisms(link)
    if len(group) != 720 or len(set(group)) != 720:
        raise AssertionError(f"expected automorphism order 720, got {len(group)}")
    degree = Counter(point for block in link for point in block)
    low = tuple(point for point in range(1, 13) if degree[point] == 20)
    restrictions = {tuple(g[point - 1] for point in low) for g in group}
    if len(restrictions) != 720:
        raise AssertionError("restriction to the six degree-20 points is not faithful S_6")

    remaining = set(map(frozenset, candidate_blocks()))
    orbit_data = []
    while remaining:
        representative = min(remaining, key=lambda block: tuple(sorted(block)))
        orbit = {image(representative, g) for g in group}
        if not orbit <= remaining:
            raise AssertionError("computed orbit overlaps an earlier orbit")
        capacities = {
            sum(frozenset(target) not in covered for target in combinations(block, 5))
            for block in orbit
        }
        if len(capacities) != 1:
            raise AssertionError("residual capacity is not orbit-invariant")
        capacity = capacities.pop()
        orbit_data.append((len(orbit), capacity, tuple(sorted(representative))))
        remaining.difference_update(orbit)

    capacity_histogram = Counter()
    for size, capacity, _ in orbit_data:
        capacity_histogram[capacity] += size
    if sum(capacity_histogram.values()) != 792:
        raise AssertionError("candidate orbit partition is incomplete")
    capacity16 = [row for row in orbit_data if row[1] == 16]
    if len(capacity16) != 3:
        raise AssertionError(f"expected three capacity-16 orbits, got {len(capacity16)}")

    # If at most five of 36 blocks had capacity 16, aggregate capacity would
    # be at most 5*16+31*15=545, below the 546 residual targets.
    if 5 * 16 + 31 * 15 >= len(residual):
        raise AssertionError("capacity argument does not force six maximal blocks")

    print("fixed blocks: 41")
    print("fixed point degrees:", " ".join(f"{p}:{degree[p]}" for p in range(1, 13)))
    print("fixed-covered five-sets: 246 (all multiplicity one)")
    print("residual five-sets: 546")
    print("automorphism group order: 720")
    print("restriction to degree-20 points: faithful and onto S_6")
    print("candidate orbit count: 12")
    print("capacity histogram:", " ".join(f"{c}:{capacity_histogram[c]}" for c in sorted(capacity_histogram)))
    print("orbit  size  capacity  representative")
    for orbit_number, (size, capacity, representative) in enumerate(orbit_data):
        print(
            f"{orbit_number:>5} {size:>5} {capacity:>9}  "
            + " ".join(map(str, representative))
        )
    print("capacity lemma: every 36-block completion uses at least six capacity-16 blocks")
    print("exhaustive first-block branches:")
    for _, _, representative in capacity16:
        print(" ".join(map(str, representative)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("link", type=Path)
    args = parser.parse_args()
    analyze(args.link)


if __name__ == "__main__":
    main()
