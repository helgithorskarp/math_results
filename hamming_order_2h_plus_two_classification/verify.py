#!/usr/bin/env python3
"""Exact finite audits for the order-(2h+2) Hamming-core theorem."""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations, product


Vertex = tuple[int, ...]


def partitions(total: int, cap: int, previous: int | None = None):
    """Yield nonincreasing positive partitions of total with parts <= cap."""
    if total == 0:
        yield ()
        return
    upper = min(total, cap, previous if previous is not None else total)
    for first in range(upper, 0, -1):
        for tail in partitions(total - first, cap, first):
            yield (first,) + tail


def shell_lower_bound(h: int, profile: tuple[int, ...]) -> Fraction:
    total = sum(profile)
    penalty = sum(a * (h - a) for a in profile)
    return Fraction(1 + total, 1) + Fraction(penalty, 2)


def feasible_profiles(h: int) -> list[tuple[int, ...]]:
    result = []
    for total in range(h, 2 * h + 2):
        for profile in partitions(total, h - 1):
            if shell_lower_bound(h, profile) <= 2 * h + 2:
                result.append(profile)
    return result


def adjacent(x: Vertex, y: Vertex) -> bool:
    return sum(a != b for a, b in zip(x, y)) == 1


def induced_min_degree(vertices: set[Vertex]) -> int:
    return min(sum(adjacent(x, y) for y in vertices) for x in vertices)


def essential_dimension(vertices: set[Vertex]) -> int:
    dimension = len(next(iter(vertices)))
    return sum(len({v[i] for v in vertices}) > 1 for i in range(dimension))


def geometric_lines(dimension: int, alphabet: int):
    for direction in range(dimension):
        other = [i for i in range(dimension) if i != direction]
        for fixed_values in product(range(alphabet), repeat=dimension - 1):
            fixed = dict(zip(other, fixed_values))
            line = tuple(
                tuple(symbol if i == direction else fixed[i] for i in range(dimension))
                for symbol in range(alphabet)
            )
            yield direction, line


def nontrivial_line_subsets(dimension: int = 4, alphabet: int = 3):
    for direction, line in geometric_lines(dimension, alphabet):
        for size in range(2, alphabet + 1):
            for subset in combinations(line, size):
                yield direction, frozenset(subset)


def audit_line_incidence() -> tuple[int, dict[str, int], int]:
    objects = list(nontrivial_line_subsets())
    counts = {"empty": 0, "matching": 0, "single": 0, "star": 0}
    covered_pairs = 0
    audited = 0

    for (direction_a, a), (direction_b, b) in combinations(objects, 2):
        if a & b:
            continue
        audited += 1
        edges = [(x, y) for x in a for y in b if adjacent(x, y)]
        if not edges:
            counts["empty"] += 1
            continue

        degree_a = {x: sum(x == u for u, _ in edges) for x in a}
        degree_b = {y: sum(y == v for _, v in edges) for y in b}
        if len(edges) == 1:
            counts["single"] += 1
            if direction_a != direction_b:
                assert essential_dimension(set(a | b)) == 3
        elif max(degree_a.values()) <= 1 and max(degree_b.values()) <= 1:
            counts["matching"] += 1
            assert direction_a == direction_b
            assert essential_dimension(set(a | b)) == 2
        else:
            counts["star"] += 1
            assert direction_a != direction_b
            assert essential_dimension(set(a | b)) == 2
            assert (
                sum(value > 0 for value in degree_a.values()) == 1
                or sum(value > 0 for value in degree_b.values()) == 1
            )

        if all(value >= 1 for value in degree_b.values()):
            covered_pairs += 1
            assert essential_dimension(set(a | b)) <= 2

    assert all(counts.values())
    return audited, counts, covered_pairs


def skew_two_line_family(h: int) -> set[Vertex]:
    return {(a, 0, 0) for a in range(h + 1)} | {
        (0, b, 1) for b in range(h + 1)
    }


def audit(max_h: int, profile_max_h: int) -> None:
    if not 6 <= profile_max_h <= max_h:
        raise ValueError("require 6 <= profile_max_h <= max_h")

    profile_count = 0
    for h in range(6, profile_max_h + 1):
        profiles = feasible_profiles(h)
        profile_count += len(profiles)
        assert profiles == [(h - 1, 1)], (h, profiles)

    algebra_count = 0
    for h in range(6, max_h + 1):
        assert min(t * (h - t) for t in range(1, h - 1)) >= 5
        assert 3 * h - 3 > 2 * h + 2
        algebra_count += 2

        family = skew_two_line_family(h)
        assert len(family) == 2 * h + 2
        assert induced_min_degree(family) == h
        assert essential_dimension(family) == 3
        first = {(a, 0, 0) for a in range(h + 1)}
        second = {(0, b, 1) for b in range(h + 1)}
        cross_edges = [(x, y) for x in first for y in second if adjacent(x, y)]
        assert cross_edges == [((0, 0, 0), (0, 0, 1))]

    grid = {(a, b) for a in range(4) for b in range(3)}
    assert len(grid) == 12
    assert induced_min_degree(grid) == 5
    maximum_line = max(
        sum(1 for x in grid if all(x[j] == v[j] for j in range(2) if j != i))
        for v in grid
        for i in range(2)
    )
    assert maximum_line == 4

    line_pairs, pattern_counts, covered_pairs = audit_line_incidence()
    print(f"exhaustive profile range: h=6..{profile_max_h}")
    print(f"feasible capped profiles checked: {profile_count}")
    print(f"symbolic inequality instances checked: {algebra_count}")
    print(f"skew two-line witnesses checked: {max_h - 5}")
    print("h=5 sharp grid: order=12 minimum_degree=5 maximum_line=4")
    print(f"disjoint ternary line-subset pairs checked: {line_pairs}")
    print(
        "cross-pattern counts: "
        + ", ".join(f"{name}={pattern_counts[name]}" for name in sorted(pattern_counts))
    )
    print(f"one-side-covered cross patterns checked: {covered_pairs}")
    print("all exact checks passed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-h", type=int, default=60)
    parser.add_argument("--profile-max-h", type=int, default=15)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    audit(arguments.max_h, arguments.profile_max_h)
