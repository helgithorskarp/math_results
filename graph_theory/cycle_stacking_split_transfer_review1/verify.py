#!/usr/bin/env python3
"""Definition-level audit of the cycle split-path theorem.

This program is independent of the submitted signed-transfer implementation.
It recursively enumerates legal pebbling moves and, separately, checks every
branch of the proof's inverse-move construction on a finite exhaustive domain.
"""

from __future__ import annotations

import argparse
import itertools
import json
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parent


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def compositions(total: int, parts: int) -> Iterable[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            yield (first,) + tail


def support_size(configuration: Sequence[int]) -> int:
    return sum(value > 0 for value in configuration)


@lru_cache(None)
def path_stackable(configuration: tuple[int, ...]) -> bool:
    """Direct reachability oracle using only the definition of a path move."""
    if support_size(configuration) == 1:
        return True
    for source, value in enumerate(configuration):
        if value < 2:
            continue
        for target in (source - 1, source + 1):
            if not 0 <= target < len(configuration):
                continue
            child = list(configuration)
            child[source] -= 2
            child[target] += 1
            if path_stackable(tuple(child)):
                return True
    return False


@lru_cache(None)
def cycle_stackable(configuration: tuple[int, ...]) -> bool:
    """Direct reachability oracle using only the definition of a cycle move."""
    if support_size(configuration) == 1:
        return True
    order = len(configuration)
    for source, value in enumerate(configuration):
        if value < 2:
            continue
        for target in ((source - 1) % order, (source + 1) % order):
            child = list(configuration)
            child[source] -= 2
            child[target] += 1
            if cycle_stackable(tuple(child)):
                return True
    return False


def split_lift(
    configuration: Sequence[int], cut: int, left_pile: int
) -> tuple[int, ...]:
    """Open at cut in order cut_left, cut+1, ..., cut-1, cut_right."""
    order = len(configuration)
    require(order >= 3, ("short cycle", configuration))
    require(0 <= cut < order, ("bad cut", cut))
    require(0 <= left_pile <= configuration[cut], ("bad split", left_pile))
    interior = tuple(configuration[(cut + offset) % order] for offset in range(1, order))
    return (left_pile,) + interior + (configuration[cut] - left_pile,)


def cycle_vertex_position(vertex: int, cut: int, order: int) -> int:
    """Unique path position for a cycle vertex other than the cut."""
    require(vertex != cut, ("cut has two positions", vertex, cut))
    position = (vertex - cut) % order
    require(1 <= position < order, (vertex, cut, order, position))
    return position


def incident_endpoint(cut: int, neighbor: int, order: int) -> int:
    if neighbor == (cut + 1) % order:
        return 0
    if neighbor == (cut - 1) % order:
        return order
    raise AssertionError(("not adjacent", cut, neighbor, order))


def path_move(
    configuration: Sequence[int], source: int, target: int
) -> tuple[int, ...]:
    require(abs(source - target) == 1, ("nonedge", source, target))
    require(configuration[source] >= 2, ("insufficient source", configuration, source))
    child = list(configuration)
    child[source] -= 2
    child[target] += 1
    return tuple(child)


def inverse_move_transform(
    child: tuple[int, ...],
    source: int,
    target: int,
    cut: int,
    left_pile: int,
) -> tuple[tuple[int, ...], int, int, tuple[int, ...], int, int, str]:
    """Implement all cases of the proof's inverse-move construction.

    The directed cycle move is source -> target.  ``child`` is the
    post-move configuration.  The returned parent split makes one path move
    to the returned (possibly changed) stackable child split.
    """
    order = len(child)
    require(target in ((source - 1) % order, (source + 1) % order), "nonedge")
    require(child[target] >= 1, ("no pebble to undo", child, target))
    original_child_lift = split_lift(child, cut, left_pile)
    require(path_stackable(original_child_lift), "input lift must stack")

    parent = list(child)
    parent[source] += 2
    parent[target] -= 1
    parent_tuple = tuple(parent)

    if cut not in (source, target):
        parent_cut = child_cut = cut
        parent_left = child_left = left_pile
        move_source = cycle_vertex_position(source, cut, order)
        move_target = cycle_vertex_position(target, cut, order)
        case = "cut_elsewhere"
    elif cut == source:
        endpoint = incident_endpoint(source, target, order)
        parent_cut = child_cut = cut
        parent_left = left_pile + 2 if endpoint == 0 else left_pile
        child_left = left_pile
        move_source = endpoint
        move_target = cycle_vertex_position(target, cut, order)
        case = "cut_at_source"
    else:
        endpoint = incident_endpoint(target, source, order)
        endpoint_pile = (
            left_pile if endpoint == 0 else child[target] - left_pile
        )
        if endpoint_pile > 0:
            parent_cut = child_cut = cut
            parent_left = left_pile - 1 if endpoint == 0 else left_pile
            child_left = left_pile
            move_source = cycle_vertex_position(source, cut, order)
            move_target = endpoint
            case = "cut_at_target_positive"
        else:
            # Delete the empty target endpoint.  The remaining spanning path
            # is re-expressed by cutting at source and adjoining a new empty
            # source endpoint across the source-target edge.
            parent_cut = child_cut = source
            if source == (target + 1) % order:
                # The retained source endpoint is left; the new endpoint is right.
                child_left = child[source]
                parent_left = child[source]
                move_source = order
            else:
                # The new endpoint is left; the retained source endpoint is right.
                child_left = 0
                parent_left = 2
                move_source = 0
            move_target = cycle_vertex_position(target, source, order)
            case = "cut_at_target_empty"

    parent_lift = split_lift(parent_tuple, parent_cut, parent_left)
    designated_child_lift = split_lift(child, child_cut, child_left)
    require(
        path_move(parent_lift, move_source, move_target) == designated_child_lift,
        (
            "inverse move does not recover child",
            child,
            source,
            target,
            cut,
            left_pile,
            case,
        ),
    )
    require(
        path_stackable(designated_child_lift),
        ("replacement child lift does not stack", child, case),
    )
    require(
        path_stackable(parent_lift),
        ("constructed parent lift does not stack", parent_tuple, case),
    )
    return (
        parent_tuple,
        parent_cut,
        parent_left,
        child,
        child_cut,
        child_left,
        case,
    )


def full_equivalence_audit() -> dict[str, object]:
    domains = ((3, 8), (4, 8), (5, 7), (6, 7))
    configurations = 0
    split_tests = 0
    stackable = 0
    rows = []
    for order, maximum_mass in domains:
        local_configurations = 0
        local_split_tests = 0
        local_stackable = 0
        for mass in range(maximum_mass + 1):
            for configuration in compositions(mass, order):
                cycle_truth = cycle_stackable(configuration)
                split_truth = False
                for cut in range(order):
                    for left_pile in range(configuration[cut] + 1):
                        local_split_tests += 1
                        if path_stackable(split_lift(configuration, cut, left_pile)):
                            split_truth = True
                require(
                    cycle_truth == split_truth,
                    ("equivalence failure", configuration, cycle_truth, split_truth),
                )
                local_configurations += 1
                local_stackable += cycle_truth
        configurations += local_configurations
        split_tests += local_split_tests
        stackable += local_stackable
        rows.append(
            {
                "order": order,
                "maximum_mass": maximum_mass,
                "configurations": local_configurations,
                "split_tests": local_split_tests,
                "stackable": local_stackable,
            }
        )
    return {
        "domains": rows,
        "configurations": configurations,
        "split_tests": split_tests,
        "stackable": stackable,
        "nonstackable": configurations - stackable,
    }


def induction_audit() -> dict[str, object]:
    domains = ((3, 7), (4, 7), (5, 6), (6, 6))
    case_counts = {
        "cut_elsewhere": 0,
        "cut_at_source": 0,
        "cut_at_target_positive": 0,
        "cut_at_target_empty": 0,
    }
    first_examples: dict[str, object] = {}
    transformations = 0
    target_was_one = 0
    stackable_child_lifts = 0
    nontrivial_empty_endpoint_cases = 0
    first_nontrivial_empty_endpoint = None

    for order, maximum_mass in domains:
        directed_edges = [
            (source, target)
            for source in range(order)
            for target in ((source - 1) % order, (source + 1) % order)
        ]
        for mass in range(1, maximum_mass + 1):
            for child in compositions(mass, order):
                for cut in range(order):
                    for left_pile in range(child[cut] + 1):
                        if not path_stackable(split_lift(child, cut, left_pile)):
                            continue
                        stackable_child_lifts += 1
                        for source, target in directed_edges:
                            if child[target] == 0:
                                continue
                            transformed = inverse_move_transform(
                                child, source, target, cut, left_pile
                            )
                            case = transformed[-1]
                            case_counts[case] += 1
                            transformations += 1
                            target_was_one += child[target] == 1
                            first_examples.setdefault(
                                case,
                                {
                                    "child": list(child),
                                    "move": [source, target],
                                    "original_split": [cut, left_pile],
                                    "parent": list(transformed[0]),
                                    "parent_split": [transformed[1], transformed[2]],
                                    "designated_child_split": [
                                        transformed[4],
                                        transformed[5],
                                    ],
                                },
                            )
                            if (
                                case == "cut_at_target_empty"
                                and support_size(split_lift(child, cut, left_pile)) > 1
                            ):
                                nontrivial_empty_endpoint_cases += 1
                                if first_nontrivial_empty_endpoint is None:
                                    first_nontrivial_empty_endpoint = {
                                        "child": list(child),
                                        "move": [source, target],
                                        "original_split": [cut, left_pile],
                                        "original_lift": list(
                                            split_lift(child, cut, left_pile)
                                        ),
                                        "parent": list(transformed[0]),
                                        "parent_split": [
                                            transformed[1],
                                            transformed[2],
                                        ],
                                        "replacement_child_split": [
                                            transformed[4],
                                            transformed[5],
                                        ],
                                    }
    require(all(case_counts.values()), ("unexercised proof case", case_counts))
    require(
        nontrivial_empty_endpoint_cases > 0,
        "empty-endpoint case was exercised only on already stacked lifts",
    )
    return {
        "stackable_child_lifts": stackable_child_lifts,
        "transformations": transformations,
        "post_move_target_equal_to_one": target_was_one,
        "case_counts": case_counts,
        "first_examples": first_examples,
        "nontrivial_empty_endpoint_cases": nontrivial_empty_endpoint_cases,
        "first_nontrivial_empty_endpoint": first_nontrivial_empty_endpoint,
    }


def empty_leaf_audit() -> dict[str, int]:
    configurations = 0
    implications = 0
    for order in range(2, 9):
        for mass in range(9):
            for configuration in compositions(mass, order):
                configurations += 1
                if configuration[0] == 0 and path_stackable(configuration):
                    require(path_stackable(configuration[1:]), ("left leaf", configuration))
                    implications += 1
                if configuration[-1] == 0 and path_stackable(configuration):
                    require(path_stackable(configuration[:-1]), ("right leaf", configuration))
                    implications += 1
    return {"configurations": configurations, "verified_implications": implications}


def quotient_edge_audit() -> dict[str, int]:
    edges = 0
    for order in range(3, 21):
        for cut in range(order):
            mapped = [cut] + [
                (cut + position) % order for position in range(1, order)
            ] + [cut]
            require(len(mapped) == order + 1, (order, cut))
            for left, right in itertools.pairwise(mapped):
                require(left != right, ("collapsed loop", order, cut, left))
                require(
                    right in ((left - 1) % order, (left + 1) % order),
                    ("collapsed nonedge", order, cut, left, right),
                )
                edges += 1
    return {"orders": 18, "cut_path_edges": edges}


def spanning_path_stackable(configuration: tuple[int, ...]) -> bool:
    order = len(configuration)
    return any(
        path_stackable(
            tuple(configuration[(first + offset) % order] for offset in range(order))
        )
        for first in range(order)
    )


def strict_gain_audit() -> list[dict[str, object]]:
    result = []
    for configuration in ((0, 1, 1, 0, 6), (0, 0, 1, 1, 0, 0, 15)):
        require(cycle_stackable(configuration), ("cycle should stack", configuration))
        require(
            not spanning_path_stackable(configuration),
            ("ordinary spanning path unexpectedly works", configuration),
        )
        successful_splits = 0
        for cut in range(len(configuration)):
            for left_pile in range(configuration[cut] + 1):
                successful_splits += path_stackable(
                    split_lift(configuration, cut, left_pile)
                )
        require(successful_splits > 0, ("no split succeeds", configuration))
        result.append(
            {
                "configuration": list(configuration),
                "successful_splits": successful_splits,
                "ordinary_spanning_paths_all_fail": True,
            }
        )
    return result


def run() -> dict[str, object]:
    equivalence = full_equivalence_audit()
    induction = induction_audit()
    empty_leaf = empty_leaf_audit()
    quotient = quotient_edge_audit()
    strict_gain = strict_gain_audit()
    return {
        "status": "PASS",
        "method": "direct legal-move recursion plus exhaustive inverse-move proof audit",
        "full_equivalence": equivalence,
        "induction": induction,
        "empty_leaf": empty_leaf,
        "quotient": quotient,
        "strict_gain": strict_gain,
        "path_oracle_states": path_stackable.cache_info().currsize,
        "cycle_oracle_states": cycle_stackable.cache_info().currsize,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = run()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check:
        expected = (ROOT / "EXPECTED.json").read_text(encoding="utf-8")
        require(rendered == expected, "computed output differs from EXPECTED.json")
    print(rendered, end="")


if __name__ == "__main__":
    main()
