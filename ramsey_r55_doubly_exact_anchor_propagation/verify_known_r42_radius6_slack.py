#!/usr/bin/env python3
"""Exhaust the six lower-degree-bound slack cases at catalog radius six.

For a fixed target-degree assignment let delta_v be target minus parent
degree.  If a_v and d_v are the numbers of added and deleted flip edges at
v, then a_v-d_v=delta_v.  Hence uniquely

    a_v=max(delta_v,0)+q_v,  d_v=max(-delta_v,0)+q_v,

where q_v is nonnegative.  Six flips give

    sum_v q_v = (12-sum_v |delta_v|)/2.

The only parity-compatible catalog orientations below degree bound six have
bound four or five, so the right side is at most two.  This script exhausts
all target assignments, weak compositions q, and prescribed-degree flip
graphs for precisely those six orientations.
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
    flip_graph_generator,
    self_test,
)
from verify_known_r42_radius6_saturated import (
    assignment_self_test,
    is_ramsey_after_local,
    local_repair_self_test,
)


TARGET_EDGES = 430
RADIUS = 6
CACHE_REQUIREMENT_BLOCK = 256


def target_high_sets_through_cost(
    degrees, low_target: int, high_count: int, endpoint_budget: int
):
    """Generate every two-consecutive-degree assignment within L1 budget."""
    high_target = low_target + 1
    high = tuple(
        vertex for vertex, degree in enumerate(degrees) if degree >= high_target
    )
    low = tuple(
        vertex for vertex, degree in enumerate(degrees) if degree < high_target
    )
    all_low_cost = sum(abs(low_target - degree) for degree in degrees)
    min_low_chosen = max(0, high_count - len(high))
    max_low_chosen = min(len(low), high_count)
    for low_chosen in range(min_low_chosen, max_low_chosen + 1):
        high_chosen = high_count - low_chosen
        # Assigning a low-side vertex the high target raises cost by one;
        # assigning a high-side vertex the high target lowers it by one.
        endpoint_cost = all_low_cost + low_chosen - high_chosen
        if endpoint_cost > endpoint_budget:
            break
        for chosen_high in itertools.combinations(high, high_chosen):
            for chosen_low in itertools.combinations(low, low_chosen):
                chosen = frozenset((*chosen_high, *chosen_low))
                changes = tuple(
                    (high_target if vertex in chosen else low_target) - degree
                    for vertex, degree in enumerate(degrees)
                )
                if sum(abs(change) for change in changes) != endpoint_cost:
                    raise AssertionError("target-assignment cost formula")
                if (endpoint_budget - endpoint_cost) % 2:
                    raise AssertionError("endpoint parity mismatch")
                yield chosen, changes, endpoint_cost


def weak_compositions(total: int, length: int):
    """Generate weak compositions for total at most two, canonically."""
    if not 0 <= total <= 2:
        raise ValueError(total)
    for support in itertools.combinations_with_replacement(range(length), total):
        answer = [0] * length
        for vertex in support:
            answer[vertex] += 1
        yield tuple(answer)


def degree_compatible_flip_sets(
    adjacency,
    low_target: int,
    high_count: int,
    flip_count: int,
    endpoint_cost_filter: int | None = None,
):
    """Yield every flip set reaching the requested two-degree multiset once."""
    degrees = tuple(sum(row) for row in adjacency)
    additions_for = flip_graph_generator(adjacency, False)
    deletions_for = flip_graph_generator(adjacency, True)
    requirement_index = 0
    for _, changes, endpoint_cost in target_high_sets_through_cost(
        degrees, low_target, high_count, 2 * flip_count
    ):
        if (
            endpoint_cost_filter is not None
            and endpoint_cost != endpoint_cost_filter
        ):
            continue
        cancellation_total = (2 * flip_count - endpoint_cost) // 2
        for cancellations in weak_compositions(cancellation_total, len(degrees)):
            if (
                requirement_index
                and requirement_index % CACHE_REQUIREMENT_BLOCK == 0
            ):
                additions_for.cache_clear()
                deletions_for.cache_clear()
            requirement_index += 1
            addition_requirements = tuple(
                max(change, 0) + cancellation
                for change, cancellation in zip(
                    changes, cancellations, strict=True
                )
            )
            deletion_requirements = tuple(
                max(-change, 0) + cancellation
                for change, cancellation in zip(
                    changes, cancellations, strict=True
                )
            )
            for additions in additions_for(addition_requirements):
                for deletions in deletions_for(deletion_requirements):
                    if len(additions) + len(deletions) != flip_count:
                        raise AssertionError("wrong number of flips")
                    yield additions, deletions


def slack_self_test() -> None:
    """Compare the whole decomposition with literal flip subsets on K6."""
    order = 6
    edges = tuple(itertools.combinations(range(order), 2))
    target = tuple(sorted((2,) * 4 + (3,) * 2))
    for sample in range(12):
        adjacency = [[False] * order for _ in range(order)]
        for index, (first, second) in enumerate(edges):
            value = ((sample + 3) * 0x9E3779B1 + index * 0x85EBCA77) >> (
                index % 11
            ) & 1
            adjacency[first][second] = adjacency[second][first] = bool(value)
        for flip_count in range(4):
            expected = set()
            for flips in itertools.combinations(edges, flip_count):
                degrees = [sum(row) for row in adjacency]
                for first, second in flips:
                    change = -1 if adjacency[first][second] else 1
                    degrees[first] += change
                    degrees[second] += change
                if tuple(sorted(degrees)) == target:
                    expected.add(flips)
            generated_pairs = list(
                degree_compatible_flip_sets(adjacency, 2, 2, flip_count)
            )
            generated = [
                tuple(sorted((*additions, *deletions)))
                for additions, deletions in generated_pairs
            ]
            actual = set(generated)
            if len(actual) != len(generated):
                raise AssertionError(("duplicate", sample, flip_count))
            if actual != expected:
                raise AssertionError((sample, flip_count, actual, expected))


def enumerate_orientation(
    adjacency, endpoint_cost_filter: int | None = None
) -> tuple[int, int]:
    base_bits = bit_adjacency(adjacency)
    candidate_count = ramsey_count = 0
    for additions, deletions in degree_compatible_flip_sets(
        adjacency, 20, 20, RADIUS, endpoint_cost_filter
    ):
        candidate_count += 1
        if is_ramsey_after_local(
            base_bits, additions, deletions, TARGET_DEGREES
        ):
            ramsey_count += 1
            flips = tuple(sorted((*additions, *deletions)))
            print(f"UNEXPECTED Ramsey survivor flips={flips}", flush=True)
    return candidate_count, ramsey_count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--only-parent",
        type=int,
        action="append",
        help="diagnostic restriction to a zero-based catalog parent index",
    )
    parser.add_argument(
        "--endpoint-cost",
        type=int,
        choices=(8, 10, 12),
        help="diagnostic restriction by sum of absolute target degree changes",
    )
    args = parser.parse_args()
    if args.endpoint_cost is not None and args.only_parent is None:
        parser.error("--endpoint-cost requires --only-parent")

    self_test()
    assignment_self_test()
    local_repair_self_test()
    slack_self_test()
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
            lower_bound = sum(
                abs(observed - target)
                for observed, target in zip(degrees, TARGET_DEGREES, strict=True)
            ) // 2
            edge_count = sum(degrees) // 2
            if not 0 <= lower_bound < RADIUS:
                continue
            if abs(TARGET_EDGES - edge_count) > RADIUS:
                continue
            if (TARGET_EDGES - edge_count) % 2 != RADIUS % 2:
                continue
            candidates, ramsey = enumerate_orientation(
                adjacency, args.endpoint_cost
            )
            eligible.append((index, orientation, edge_count, lower_bound))
            total_candidates += candidates
            total_ramsey += ramsey
            print(
                f"parent={index} orientation={orientation} edges={edge_count} "
                f"degree_lower_bound={lower_bound} candidates={candidates} "
                f"ramsey_survivors={ramsey}",
                flush=True,
            )

    if selected is not None:
        print(
            f"DIAGNOSTIC selected orientations={len(eligible)} "
            f"endpoint_cost={args.endpoint_cost or 'all'} "
            f"degree-compatible-candidates={total_candidates} "
            f"Ramsey-survivors={total_ramsey}"
        )
        return
    expected = [
        (87, "base", 428, 5),
        (89, "base", 428, 5),
        (91, "base", 430, 5),
        (93, "base", 428, 4),
        (137, "base", 428, 5),
        (143, "base", 430, 5),
    ]
    if eligible != expected:
        raise AssertionError(("slack orientations", eligible))
    if total_ramsey:
        raise AssertionError(f"found {total_ramsey} slack radius-six graphs")
    print(
        f"PASS radius-six slack orientations={len(eligible)} "
        f"degree-compatible-candidates={total_candidates} Ramsey-survivors=0"
    )


if __name__ == "__main__":
    main()
