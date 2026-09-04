#!/usr/bin/env python3
"""Exhaust target-degree radius-five moves from the known Ramsey-42 catalog.

This is deliberately target-specific.  Saturating the degree-sequence edit
lower bound forces additions to join only vertices whose degrees rise and
deletions to join only vertices whose degrees fall.  The required endpoint
degrees are at most two.  We enumerate those small degree-realizing flip
graphs, rather than all 5-subsets of the 861 possible edges.
"""

from __future__ import annotations

from functools import cache
import hashlib
import itertools

from verify_known_r42_bridge import (
    CATALOG_PATH,
    CATALOG_SHA256,
    TARGET_DEGREES,
    complement_adjacency,
    decode_short_graph6,
    degree_multiset,
)


ORDER = 42
TARGET_EDGES = 430


def bit_adjacency(adjacency) -> list[int]:
    return [
        sum(1 << other for other, adjacent in enumerate(row) if adjacent)
        for row in adjacency
    ]


def contains_clique(adjacency: list[int], wanted: int = 5) -> bool:
    def search(candidates: int, remaining: int) -> bool:
        if candidates.bit_count() < remaining:
            return False
        if remaining == 1:
            return bool(candidates)
        while candidates.bit_count() >= remaining:
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length() - 1
            if search(candidates & adjacency[vertex], remaining - 1):
                return True
        return False

    return search((1 << len(adjacency)) - 1, wanted)


def flip_graph_generator(adjacency, want_edge: bool):
    """Return a cached enumerator for prescribed flip-endpoint degrees."""

    @cache
    def realizations(requirements: tuple[int, ...]):
        if not any(requirements):
            return ((),)
        if sum(requirements) % 2:
            return ()
        first = next(
            vertex for vertex, requirement in enumerate(requirements) if requirement
        )
        needed = requirements[first]
        candidates = [
            vertex
            for vertex, requirement in enumerate(requirements)
            if vertex != first
            and requirement
            and bool(adjacency[first][vertex]) == want_edge
        ]
        if len(candidates) < needed:
            return ()
        answers = []
        for neighbors in itertools.combinations(candidates, needed):
            following = list(requirements)
            following[first] = 0
            for neighbor in neighbors:
                following[neighbor] -= 1
            if min(following) < 0:
                continue
            edges = tuple((min(first, other), max(first, other)) for other in neighbors)
            answers.extend((*edges, *tail) for tail in realizations(tuple(following)))
        return tuple(answers)

    return realizations


def is_ramsey_after(base_bits: list[int], flips) -> bool:
    adjacency = base_bits.copy()
    for first, second in flips:
        adjacency[first] ^= 1 << second
        adjacency[second] ^= 1 << first
    if tuple(sorted(row.bit_count() for row in adjacency)) != TARGET_DEGREES:
        raise AssertionError("matching reduction produced wrong target degrees")
    if contains_clique(adjacency):
        return False
    mask = (1 << ORDER) - 1
    complement = [
        mask ^ (1 << vertex) ^ row for vertex, row in enumerate(adjacency)
    ]
    return not contains_clique(complement)


def self_test() -> None:
    # Compare the recursive degree-realization generator with literal subset
    # enumeration on a six-vertex graph, for both edge colors.
    order = 6
    adjacency = [[False] * order for _ in range(order)]
    for first, second in itertools.combinations(range(order), 2):
        value = (first + 2 * second) % 3 == 0
        adjacency[first][second] = adjacency[second][first] = value
    for want_edge in (False, True):
        available = tuple(
            (first, second)
            for first, second in itertools.combinations(range(order), 2)
            if adjacency[first][second] == want_edge
        )
        expected = {}
        for mask in range(1 << len(available)):
            edges = tuple(
                edge for index, edge in enumerate(available) if mask & (1 << index)
            )
            requirements = [0] * order
            for first, second in edges:
                requirements[first] += 1
                requirements[second] += 1
            expected.setdefault(tuple(requirements), set()).add(edges)
        generator = flip_graph_generator(adjacency, want_edge)
        for requirements, edge_sets in expected.items():
            actual = {tuple(sorted(edges)) for edges in generator(requirements)}
            if actual != edge_sets:
                raise AssertionError((want_edge, requirements, actual, edge_sets))

    # Cross-check the bitset clique search against direct subset inspection.
    edges = tuple(itertools.combinations(range(7), 2))
    for sample in range(64):
        adjacency = [0] * 7
        for index, (first, second) in enumerate(edges):
            if ((sample * 0x9E3779B1 + index * 0x85EBCA77) >> (index % 13)) & 1:
                adjacency[first] |= 1 << second
                adjacency[second] |= 1 << first
        for wanted in range(1, 6):
            direct = any(
                all(
                    adjacency[first] & (1 << second)
                    for first, second in itertools.combinations(vertices, 2)
                )
                for vertices in itertools.combinations(range(7), wanted)
            )
            if contains_clique(adjacency, wanted) != direct:
                raise AssertionError((sample, wanted))


def enumerate_orientation(adjacency) -> tuple[int, int]:
    degrees = [sum(row) for row in adjacency]
    if any(degree not in range(19, 23) for degree in degrees):
        raise AssertionError("unexpected degree outside 19,...,22")

    # An optimal assignment of twenty target-degree-21 labels takes all
    # current degree-21/22 vertices if there are too few of them, or chooses
    # twenty among them if there are too many.  The degree-19/20 vertices are
    # tied in the former choice, and degree-21/22 vertices are tied in the
    # latter; retaining these ties is essential because changes of magnitude
    # two can occur at degree 19 or 22.
    high = tuple(vertex for vertex, degree in enumerate(degrees) if degree >= 21)
    low = tuple(vertex for vertex, degree in enumerate(degrees) if degree <= 20)
    if len(high) <= 20:
        target21_sets = (
            frozenset((*high, *extra))
            for extra in itertools.combinations(low, 20 - len(high))
        )
    else:
        target21_sets = (
            frozenset(chosen) for chosen in itertools.combinations(high, 20)
        )

    upward_realizations = flip_graph_generator(adjacency, False)
    downward_realizations = flip_graph_generator(adjacency, True)
    base_bits = bit_adjacency(adjacency)
    candidate_count = ramsey_count = 0
    seen_candidates = set()

    for target21 in target21_sets:
        changes = tuple(
            (21 if vertex in target21 else 20) - degree
            for vertex, degree in enumerate(degrees)
        )
        if sum(abs(change) for change in changes) != 10:
            raise AssertionError("nonoptimal target-degree assignment")
        up_requirements = tuple(max(change, 0) for change in changes)
        down_requirements = tuple(max(-change, 0) for change in changes)
        up_options = upward_realizations(up_requirements)
        down_options = downward_realizations(down_requirements)
        for additions in up_options:
            for deletions in down_options:
                if len(additions) + len(deletions) != 5:
                    raise AssertionError("wrong number of saturated flips")
                key = tuple(sorted((*additions, *deletions)))
                if key in seen_candidates:
                    raise AssertionError(f"duplicate flip set: {key}")
                seen_candidates.add(key)
                candidate_count += 1
                if is_ramsey_after(base_bits, (*additions, *deletions)):
                    ramsey_count += 1
    return candidate_count, ramsey_count


def main() -> None:
    self_test()
    raw_catalog = CATALOG_PATH.read_bytes()
    if hashlib.sha256(raw_catalog).hexdigest() != CATALOG_SHA256:
        raise AssertionError("known R(5,5;42) catalog digest changed")
    catalog = [
        decode_short_graph6(line)
        for line in raw_catalog.decode("ascii").splitlines()
    ]
    if len(catalog) != 328:
        raise AssertionError("wrong catalog record count")
    for base in catalog:
        adjacency = bit_adjacency(base)
        mask = (1 << ORDER) - 1
        complement = [
            mask ^ (1 << vertex) ^ row for vertex, row in enumerate(adjacency)
        ]
        if contains_clique(adjacency) or contains_clique(complement):
            raise AssertionError("catalog input has a homogeneous five-set")

    eligible = []
    total_candidates = total_ramsey = 0
    for index, base in enumerate(catalog):
        for orientation, adjacency in (
            ("base", base),
            ("complement", complement_adjacency(base)),
        ):
            degrees = degree_multiset(adjacency)
            l1 = sum(
                abs(observed - target)
                for observed, target in zip(degrees, TARGET_DEGREES, strict=True)
            )
            if l1 % 2:
                raise AssertionError("nonintegral degree edit bound")
            lower_bound = l1 // 2
            edge_count = sum(degrees) // 2
            if lower_bound > 5:
                continue
            # Five flips reverse edge-count parity.  The sole lower-bound-four
            # orientation and five lower-bound-five orientations fail this
            # necessary test.
            if (TARGET_EDGES - edge_count) % 2 == 0:
                continue
            if lower_bound != 5:
                raise AssertionError("unexpected sub-five parity-compatible parent")
            candidates, ramsey = enumerate_orientation(adjacency)
            eligible.append((index, orientation, edge_count, candidates, ramsey))
            total_candidates += candidates
            total_ramsey += ramsey
            print(
                f"parent={index} orientation={orientation} edges={edge_count} "
                f"degree_saturated_candidates={candidates} "
                f"ramsey_survivors={ramsey}"
            )

    expected_orientations = [
        (9, "base"),
        (79, "base"),
        (88, "base"),
        (93, "complement"),
        (94, "base"),
        (95, "base"),
        (132, "base"),
        (135, "base"),
        (138, "base"),
        (140, "base"),
        (167, "base"),
        (212, "base"),
    ]
    if [(index, orientation) for index, orientation, *_ in eligible] != expected_orientations:
        raise AssertionError(eligible)
    if total_ramsey:
        raise AssertionError(f"found {total_ramsey} radius-five target graphs")
    print(
        f"PASS radius-five eligible orientations={len(eligible)} "
        f"degree-saturated-candidates={total_candidates} Ramsey-survivors=0"
    )
    print("PASS singleton-deletion catalog edge distance is at least 6")


if __name__ == "__main__":
    main()
