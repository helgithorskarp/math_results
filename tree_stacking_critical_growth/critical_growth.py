#!/usr/bin/env python3
"""Critical tree-stacking multiplicity for double brooms and caterpillars.

The counting layer uses the sibling-leaf classification of critical
tree-stacking configurations.  It computes the excess of a leaf z directly as

    X(z) = sum(deg(v) * 2**(dist(z, v) - 1) for internal vertices v),

which is independent of the directed-deficit implementation in the earlier
classification artifact.
"""

from __future__ import annotations

import argparse
import json
import platform
import time
from collections import deque
from itertools import combinations
from math import comb
from typing import Iterator, Sequence


Tree = tuple[tuple[int, ...], ...]


EXPECTED_TREE_MAXIMA = {
    2: (1, 1),
    3: (3, 1),
    4: (10, 2),
    5: (35, 3),
    6: (126, 6),
    7: (462, 11),
    8: (1716, 23),
    9: (6435, 47),
    10: (24310, 106),
    11: (92378, 235),
    12: (352716, 551),
    13: (1352078, 1301),
    14: (5200300, 3159),
    15: (30577800, 7741),
    16: (383736990, 19320),
    17: (5930563870, 48629),
    18: (93247009310, 123867),
    19: (1478942057502, 317955),
}


EXPECTED_CATERPILLAR_MAXIMA = {
    **{n: value for n, (value, _) in EXPECTED_TREE_MAXIMA.items() if n <= 19},
    20: 34704830468464,
    21: 1096246556385904,
    22: 34852713682289776,
}


def validate_tree(adjacency: Sequence[Sequence[int]]) -> Tree:
    """Normalize and validate an undirected finite tree."""

    tree = tuple(tuple(sorted(neighbors)) for neighbors in adjacency)
    n = len(tree)
    if n < 2:
        raise ValueError("at least two vertices are required")
    for vertex, neighbors in enumerate(tree):
        if len(set(neighbors)) != len(neighbors):
            raise ValueError("duplicate neighbor")
        for neighbor in neighbors:
            if neighbor < 0 or neighbor >= n or neighbor == vertex:
                raise ValueError("invalid endpoint")
            if vertex not in tree[neighbor]:
                raise ValueError("asymmetric adjacency")
    if sum(map(len, tree)) != 2 * (n - 1):
        raise ValueError("the graph does not have n-1 edges")
    reached = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for neighbor in tree[vertex]:
            if neighbor not in reached:
                reached.add(neighbor)
                queue.append(neighbor)
    if len(reached) != n:
        raise ValueError("the graph is disconnected")
    return tree


def distances(tree: Tree, source: int) -> tuple[int, ...]:
    """Return graph distances from source in a tree."""

    result = [-1] * len(tree)
    result[source] = 0
    queue = deque([source])
    while queue:
        vertex = queue.popleft()
        for neighbor in tree[vertex]:
            if result[neighbor] < 0:
                result[neighbor] = result[vertex] + 1
                queue.append(neighbor)
    return tuple(result)


def leaf_excesses(adjacency: Sequence[Sequence[int]]) -> dict[int, int]:
    """Compute X(z)=(H(z)-1)/2 from distance-degree sums."""

    tree = validate_tree(adjacency)
    if len(tree) == 2:
        return {0: 0, 1: 0}
    internal = [vertex for vertex, neighbors in enumerate(tree) if len(neighbors) > 1]
    result = {}
    for leaf, neighbors in enumerate(tree):
        if len(neighbors) != 1:
            continue
        distance = distances(tree, leaf)
        result[leaf] = sum(
            len(tree[vertex]) * (1 << (distance[vertex] - 1)) for vertex in internal
        )
    return result


def critical_count(adjacency: Sequence[Sequence[int]]) -> int:
    """Count critical configurations using the sibling-leaf theorem."""

    tree = validate_tree(adjacency)
    if len(tree) == 2:
        return 1
    excess = leaf_excesses(tree)
    maximum = max(excess.values())
    maximizing_parents = {tree[leaf][0] for leaf, value in excess.items() if value == maximum}
    total = 0
    for parent in maximizing_parents:
        siblings = [
            leaf
            for leaf, neighbors in enumerate(tree)
            if len(neighbors) == 1 and neighbors[0] == parent
        ]
        sibling_excesses = {excess[leaf] for leaf in siblings}
        if len(sibling_excesses) != 1:
            raise AssertionError("sibling leaves must have the same excess")
        value = sibling_excesses.pop()
        total += comb(value + len(siblings) - 1, len(siblings) - 1)
    return total


def double_broom(d: int, e: int, ell: int) -> Tree:
    """Build B(d,e,ell): d and e leaves on endpoints of an ell-edge path."""

    if d < 1 or e < 1 or ell < 1:
        raise ValueError("d, e, and ell must be positive")
    adjacency = [[] for _ in range(ell + 1 + d + e)]
    for vertex in range(ell):
        adjacency[vertex].append(vertex + 1)
        adjacency[vertex + 1].append(vertex)
    next_vertex = ell + 1
    for _ in range(d):
        adjacency[0].append(next_vertex)
        adjacency[next_vertex].append(0)
        next_vertex += 1
    for _ in range(e):
        adjacency[ell].append(next_vertex)
        adjacency[next_vertex].append(ell)
        next_vertex += 1
    return validate_tree(adjacency)


def double_broom_formula(d: int, e: int, ell: int) -> dict[str, int | str]:
    """Return the exact maximizing side, excess, and critical count."""

    if d < 1 or e < 1 or ell < 1:
        raise ValueError("d, e, and ell must be positive")
    if d > e:
        d, e = e, d
        side = "right"
    else:
        side = "both" if d == e else "left"
    excess = (1 << ell) * (e + 3) + d - 3
    one_class = comb(excess + d - 1, d - 1)
    return {
        "smaller_local_leaf_class": d,
        "opposite_leaf_class": e,
        "hub_distance": ell,
        "maximizing_side": side,
        "maximizing_excess": excess,
        "critical_count": one_class * (2 if d == e else 1),
    }


def caterpillar(leaf_profile: Sequence[int]) -> Tree:
    """Build a caterpillar from pendant-leaf counts along its nonleaf core."""

    profile = tuple(leaf_profile)
    if len(profile) == 1:
        if profile[0] < 2:
            raise ValueError("a one-vertex core must describe a nontrivial star")
    elif len(profile) < 2 or profile[0] < 1 or profile[-1] < 1:
        raise ValueError("a path core must have a pendant leaf at each endpoint")
    if any(value < 0 for value in profile):
        raise ValueError("leaf counts must be nonnegative")
    core_order = len(profile)
    adjacency = [[] for _ in range(core_order + sum(profile))]
    for vertex in range(core_order - 1):
        adjacency[vertex].append(vertex + 1)
        adjacency[vertex + 1].append(vertex)
    next_vertex = core_order
    for core, count in enumerate(profile):
        for _ in range(count):
            adjacency[core].append(next_vertex)
            adjacency[next_vertex].append(core)
            next_vertex += 1
    return validate_tree(adjacency)


def caterpillar_profile_count(leaf_profile: Sequence[int]) -> int:
    """Count directly from the two endpoint excesses of a caterpillar."""

    profile = tuple(leaf_profile)
    if len(profile) == 1:
        d = profile[0]
        return comb(2 * d - 1, d - 1)
    if len(profile) < 2 or profile[0] < 1 or profile[-1] < 1:
        raise ValueError("invalid caterpillar profile")
    degrees = tuple(
        leaves + (1 if index in (0, len(profile) - 1) else 2)
        for index, leaves in enumerate(profile)
    )
    left = sum(degree * (1 << index) for index, degree in enumerate(degrees))
    right = sum(
        degree * (1 << (len(profile) - 1 - index))
        for index, degree in enumerate(degrees)
    )
    maximum = max(left, right)
    total = 0
    if left == maximum:
        total += comb(left + profile[0] - 1, profile[0] - 1)
    if right == maximum:
        total += comb(right + profile[-1] - 1, profile[-1] - 1)
    return total


def weak_compositions(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    """Yield weak compositions in deterministic bar order."""

    if parts == 1:
        yield (total,)
        return
    for bars in combinations(range(total + parts - 1), parts - 1):
        values = []
        previous = -1
        for bar in bars + (total + parts - 1,):
            values.append(bar - previous - 1)
            previous = bar
        yield tuple(values)


def caterpillar_profiles(order: int) -> Iterator[tuple[int, ...]]:
    """Yield the star and every oriented nonstar caterpillar profile of an order."""

    if order < 3:
        return
    yield (order - 1,)
    for core_order in range(2, order - 1):
        free_leaves = order - core_order - 2
        if free_leaves < 0:
            continue
        for free_profile in weak_compositions(free_leaves, core_order):
            profile = list(free_profile)
            profile[0] += 1
            profile[-1] += 1
            yield tuple(profile)


def caterpillar_census(order: int) -> dict[str, object]:
    """Exhaust every oriented core profile and return the exact maximum."""

    best = -1
    maximizers: set[tuple[int, ...]] = set()
    checked = 0
    for profile in caterpillar_profiles(order):
        checked += 1
        value = caterpillar_profile_count(profile)
        canonical = min(profile, tuple(reversed(profile)))
        if value > best:
            best = value
            maximizers = {canonical}
        elif value == best:
            maximizers.add(canonical)
    return {
        "order": order,
        "oriented_profiles_checked": checked,
        "maximum": best,
        "maximizing_profiles_up_to_reversal": [list(item) for item in sorted(maximizers)],
    }


def identify_family(graph: object) -> dict[str, int | str]:
    """Recognize the star or a symmetric double broom in a NetworkX graph."""

    import networkx as nx

    degrees = dict(graph.degree())
    order = len(graph)
    if max(degrees.values()) == order - 1:
        return {"family": "star", "leaves": order - 1}
    hubs = [vertex for vertex, degree in degrees.items() if degree > 2]
    if len(hubs) != 2 or degrees[hubs[0]] != degrees[hubs[1]]:
        return {"family": "other"}
    if any(degree not in (1, 2, degrees[hubs[0]]) for degree in degrees.values()):
        return {"family": "other"}
    d = degrees[hubs[0]] - 1
    for hub in hubs:
        if sum(degrees[neighbor] == 1 for neighbor in graph.neighbors(hub)) != d:
            return {"family": "other"}
    return {
        "family": "symmetric_double_broom",
        "leaves_per_hub": d,
        "hub_distance": nx.shortest_path_length(graph, hubs[0], hubs[1]),
    }


def all_tree_census(order: int) -> dict[str, object]:
    """Exhaust NetworkX's nonisomorphic trees at one order."""

    import networkx as nx

    start = time.monotonic()
    best = -1
    maximizers = []
    checked = 0
    for graph in nx.nonisomorphic_trees(order):
        checked += 1
        adjacency = tuple(tuple(graph.neighbors(vertex)) for vertex in range(order))
        value = critical_count(adjacency)
        if value > best:
            best = value
            maximizers = [graph.copy()]
        elif value == best:
            maximizers.append(graph.copy())
    expected_best, expected_checked = EXPECTED_TREE_MAXIMA[order]
    if (best, checked) != (expected_best, expected_checked):
        raise AssertionError(
            f"order {order}: got {(best, checked)}, expected {(expected_best, expected_checked)}"
        )
    records = []
    for graph in maximizers:
        records.append(
            {
                "graph6": nx.to_graph6_bytes(graph, header=False).strip().decode("ascii"),
                "degree_sequence": sorted(dict(graph.degree()).values()),
                **identify_family(graph),
            }
        )
    return {
        "order": order,
        "trees_checked": checked,
        "maximum": best,
        "maximizer_count": len(maximizers),
        "maximizers": records,
        "elapsed_seconds": round(time.monotonic() - start, 6),
    }


def run_checks(max_caterpillar_order: int, max_tree_order: int) -> dict[str, object]:
    """Run symbolic-family, caterpillar, and optional all-tree checks."""

    formula_cases = 0
    for d in range(1, 9):
        for e in range(1, 9):
            for ell in range(1, 9):
                formula_cases += 1
                direct = critical_count(double_broom(d, e, ell))
                closed = int(double_broom_formula(d, e, ell)["critical_count"])
                if direct != closed:
                    raise AssertionError((d, e, ell, direct, closed))

    profile_graph_cases = 0
    for order in range(4, min(max_caterpillar_order, 12) + 1):
        for profile in caterpillar_profiles(order):
            profile_graph_cases += 1
            direct = critical_count(caterpillar(profile))
            compressed = caterpillar_profile_count(profile)
            if direct != compressed:
                raise AssertionError((profile, direct, compressed))

    caterpillar_records = []
    for order in range(3, max_caterpillar_order + 1):
        record = caterpillar_census(order)
        expected = EXPECTED_CATERPILLAR_MAXIMA.get(order)
        if expected is not None and record["maximum"] != expected:
            raise AssertionError((order, record["maximum"], expected))
        caterpillar_records.append(record)

    tree_records = []
    if max_tree_order:
        if max_tree_order > max(EXPECTED_TREE_MAXIMA):
            raise ValueError("no pinned all-tree expectation above order 19")
        import networkx as nx

        for order in range(2, max_tree_order + 1):
            tree_records.append(all_tree_census(order))
        networkx_version = nx.__version__
    else:
        networkx_version = None

    return {
        "python": platform.python_version(),
        "networkx": networkx_version,
        "double_broom_formula_cases": formula_cases,
        "profile_vs_graph_cases": profile_graph_cases,
        "caterpillar_census": caterpillar_records,
        "all_tree_census": tree_records,
        "all_checks": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-caterpillar-order", type=int, default=22)
    parser.add_argument(
        "--max-tree-order",
        type=int,
        default=0,
        help="exhaust all nonisomorphic trees through this order; 0 skips it",
    )
    args = parser.parse_args()
    record = run_checks(args.max_caterpillar_order, args.max_tree_order)
    print(json.dumps(record, sort_keys=True))


if __name__ == "__main__":
    main()
