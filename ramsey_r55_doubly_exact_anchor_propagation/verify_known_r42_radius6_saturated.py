#!/usr/bin/env python3
"""Exclude the degree-bound-saturated part of catalog edge radius six.

For a parent whose sorted degree distance from the target multiset is exactly
six edge edits, every endpoint action is forced to move monotonically toward
its assigned target degree.  This script exhausts those assignments and the
small prescribed-degree addition/deletion graphs.  Parents with lower degree
distance need cancellation endpoint actions and are deliberately not covered.
"""

from __future__ import annotations

import argparse
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
from verify_known_r42_radius5 import (
    bit_adjacency,
    contains_clique,
    flip_graph_generator,
    self_test,
)


TARGET_EDGES = 430
RADIUS = 6
CACHE_ASSIGNMENT_BLOCK = 256


def contains_triangle(adjacency: list[int], candidates: int) -> bool:
    """Test whether the indicated vertices contain a triangle."""
    while candidates:
        vertex_bit = candidates & -candidates
        candidates ^= vertex_bit
        vertex = vertex_bit.bit_length() - 1
        neighbors = candidates & adjacency[vertex]
        while neighbors:
            neighbor_bit = neighbors & -neighbors
            neighbors ^= neighbor_bit
            neighbor = neighbor_bit.bit_length() - 1
            if adjacency[neighbor] & neighbors:
                return True
    return False


def is_ramsey_after_local(
    base_bits: list[int], additions, deletions, target_degrees=None
) -> bool:
    """Check a repair through final common neighborhoods of changed edges."""
    adjacency = base_bits.copy()
    for first, second in (*additions, *deletions):
        adjacency[first] ^= 1 << second
        adjacency[second] ^= 1 << first
    if target_degrees is not None:
        actual = tuple(sorted(row.bit_count() for row in adjacency))
        if actual != tuple(target_degrees):
            raise AssertionError(("wrong target degrees", actual))

    # The parent has no red K5.  Therefore any red K5 in the repaired graph
    # contains an added edge, whose final common neighborhood contains a K3.
    for first, second in additions:
        common = adjacency[first] & adjacency[second]
        if contains_triangle(adjacency, common):
            return False

    mask = (1 << len(adjacency)) - 1
    blue = [
        mask ^ (1 << vertex) ^ row for vertex, row in enumerate(adjacency)
    ]
    # Dually, every new blue K5 contains an edge deleted from the red parent.
    for first, second in deletions:
        common = blue[first] & blue[second]
        if contains_triangle(blue, common):
            return False
    return True


def local_repair_self_test() -> None:
    """Compare the changed-edge criterion with global K5 search on K7."""
    order = 7
    edges = tuple(itertools.combinations(range(order), 2))
    mask = (1 << order) - 1
    tested = 0
    for sample in range(64):
        base = [0] * order
        for index, (first, second) in enumerate(edges):
            value = ((sample + 5) * 0x9E3779B1 + index * 0x85EBCA77) >> (
                index % 13
            ) & 1
            if value:
                base[first] |= 1 << second
                base[second] |= 1 << first
        base_blue = [
            mask ^ (1 << vertex) ^ row for vertex, row in enumerate(base)
        ]
        if contains_clique(base) or contains_clique(base_blue):
            continue
        for flip_count in range(3):
            for flips in itertools.combinations(edges, flip_count):
                additions = tuple(
                    edge
                    for edge in flips
                    if not (base[edge[0]] & (1 << edge[1]))
                )
                deletions = tuple(edge for edge in flips if edge not in additions)
                repaired = base.copy()
                for first, second in flips:
                    repaired[first] ^= 1 << second
                    repaired[second] ^= 1 << first
                repaired_blue = [
                    mask ^ (1 << vertex) ^ row
                    for vertex, row in enumerate(repaired)
                ]
                expected = not contains_clique(repaired) and not contains_clique(
                    repaired_blue
                )
                actual = is_ramsey_after_local(base, additions, deletions)
                if actual != expected:
                    raise AssertionError((sample, flips, actual, expected))
                tested += 1
    if not tested:
        raise AssertionError("local repair self-test was vacuous")


def optimal_high_target_sets(
    degrees, high_target: int, high_count: int
):
    """Generate all minimum-L1 assignments of two consecutive targets."""
    high = tuple(
        vertex for vertex, degree in enumerate(degrees) if degree >= high_target
    )
    low = tuple(
        vertex for vertex, degree in enumerate(degrees) if degree < high_target
    )
    if len(high) <= high_count:
        return (
            frozenset((*high, *extra))
            for extra in itertools.combinations(low, high_count - len(high))
        )
    return (
        frozenset(chosen) for chosen in itertools.combinations(high, high_count)
    )


def assignment_self_test() -> None:
    """Compare the threshold rule with literal target assignment search."""
    order = 6
    low_target = 2
    high_target = low_target + 1
    high_count = 3
    for degrees in itertools.product(range(5), repeat=order):
        actual = set(
            optimal_high_target_sets(degrees, high_target, high_count)
        )
        all_sets = [
            frozenset(chosen)
            for chosen in itertools.combinations(range(order), high_count)
        ]
        costs = {
            chosen: sum(
                abs(
                    (high_target if vertex in chosen else low_target) - degree
                )
                for vertex, degree in enumerate(degrees)
            )
            for chosen in all_sets
        }
        optimum = min(costs.values())
        expected = {chosen for chosen, cost in costs.items() if cost == optimum}
        if actual != expected:
            raise AssertionError((degrees, actual, expected))


def enumerate_orientation(adjacency) -> tuple[int, int]:
    """Count all target-degree six-flip graphs at saturated degree distance."""
    degrees = [sum(row) for row in adjacency]
    if any(degree not in range(19, 23) for degree in degrees):
        raise AssertionError("unexpected degree outside 19,...,22")

    # Assign exactly twenty vertices target degree 21.  At an L1-optimal
    # assignment, all vertices currently on the scarcer side of the 20/21
    # threshold are retained, and all choices within a side are genuine ties.
    target21_sets = optimal_high_target_sets(degrees, 21, 20)

    upward_realizations = flip_graph_generator(adjacency, False)
    downward_realizations = flip_graph_generator(adjacency, True)
    base_bits = bit_adjacency(adjacency)
    candidate_count = ramsey_count = 0

    for assignment_index, target21 in enumerate(target21_sets):
        # Some degree profiles have hundreds of thousands of tied target
        # assignments.  Recursive subproblems are useful within a nearby
        # block, but retaining every outer requirement is unnecessary and can
        # dominate memory.  Clearing at deterministic block boundaries keeps
        # the proof computation bounded without changing the enumeration.
        if assignment_index and assignment_index % CACHE_ASSIGNMENT_BLOCK == 0:
            upward_realizations.cache_clear()
            downward_realizations.cache_clear()
        changes = tuple(
            (21 if vertex in target21 else 20) - degree
            for vertex, degree in enumerate(degrees)
        )
        if sum(abs(change) for change in changes) != 2 * RADIUS:
            raise AssertionError("non-saturated target-degree assignment")
        additions_options = upward_realizations(
            tuple(max(change, 0) for change in changes)
        )
        deletions_options = downward_realizations(
            tuple(max(-change, 0) for change in changes)
        )
        for additions in additions_options:
            for deletions in deletions_options:
                flips = (*additions, *deletions)
                if len(flips) != RADIUS:
                    raise AssertionError("wrong number of saturated flips")
                # No duplicate set is possible: its final labeled degrees
                # recover target21, its edge colors separate additions from
                # deletions, and each degree-realization generator is unique.
                candidate_count += 1
                if is_ramsey_after_local(
                    base_bits, additions, deletions, TARGET_DEGREES
                ):
                    ramsey_count += 1
    return candidate_count, ramsey_count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--only-parent",
        type=int,
        action="append",
        help="diagnostic restriction to a zero-based catalog parent index",
    )
    args = parser.parse_args()

    self_test()
    assignment_self_test()
    local_repair_self_test()
    raw_catalog = CATALOG_PATH.read_bytes()
    if hashlib.sha256(raw_catalog).hexdigest() != CATALOG_SHA256:
        raise AssertionError("known R(5,5;42) catalog digest changed")
    catalog = [
        decode_short_graph6(line)
        for line in raw_catalog.decode("ascii").splitlines()
    ]
    if len(catalog) != 328:
        raise AssertionError("wrong catalog record count")

    eligible = []
    slack_eligible = []
    total_candidates = total_ramsey = 0
    selected = None if args.only_parent is None else set(args.only_parent)
    for index, base in enumerate(catalog):
        if selected is not None and index not in selected:
            continue
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
            if lower_bound > RADIUS:
                continue
            if abs(TARGET_EDGES - edge_count) > RADIUS:
                continue
            if (TARGET_EDGES - edge_count) % 2 != RADIUS % 2:
                continue
            if lower_bound < RADIUS:
                slack_eligible.append(
                    (index, orientation, edge_count, lower_bound)
                )
                continue
            candidates, ramsey = enumerate_orientation(adjacency)
            eligible.append((index, orientation, edge_count, candidates, ramsey))
            total_candidates += candidates
            total_ramsey += ramsey
            print(
                f"parent={index} orientation={orientation} edges={edge_count} "
                f"degree_saturated_candidates={candidates} "
                f"ramsey_survivors={ramsey}",
                flush=True,
            )

    if selected is not None:
        print(
            f"DIAGNOSTIC selected orientations={len(eligible)} "
            f"degree-saturated-candidates={total_candidates} "
            f"Ramsey-survivors={total_ramsey}"
        )
        return
    if len(eligible) != 47:
        raise AssertionError(("eligible orientations", len(eligible)))
    expected_slack = [
        (87, "base", 428, 5),
        (89, "base", 428, 5),
        (91, "base", 430, 5),
        (93, "base", 428, 4),
        (137, "base", 428, 5),
        (143, "base", 430, 5),
    ]
    if slack_eligible != expected_slack:
        raise AssertionError(("slack orientations", slack_eligible))
    if total_ramsey:
        raise AssertionError(f"found {total_ramsey} saturated radius-six graphs")
    print(
        "PASS radius-six degree/parity-compatible orientations=53 "
        "saturated=47 slack=6"
    )
    print(
        f"PASS radius-six saturated orientations={len(eligible)} "
        f"degree-saturated-candidates={total_candidates} Ramsey-survivors=0"
    )
    print("PASS any radius-six target must use a lower-bound-four/five parent")


if __name__ == "__main__":
    main()
