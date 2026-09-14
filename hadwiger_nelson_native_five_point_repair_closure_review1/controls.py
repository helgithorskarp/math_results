#!/usr/bin/env python3
"""Small brute-force controls for the independent closure checker."""
from __future__ import annotations

import argparse
import itertools
import json
import random
from pathlib import Path

import independent_check as check


def connected(group, adjacency):
    selected = set(group)
    reached = {group[0]}
    while True:
        enlarged = reached | {u for v in reached for u in adjacency[v] & selected}
        if enlarged == reached:
            return reached == selected
        reached = enlarged


def brute_cover(singletons, pairs, width):
    masks = list(singletons) + list(pairs)
    weights = [1] * len(singletons) + [2] * len(pairs)
    full = (1 << width) - 1
    for chosen in range(1 << len(masks)):
        if sum(weights[i] for i in range(len(masks)) if chosen >> i & 1) > 5:
            continue
        union = 0
        for i, mask in enumerate(masks):
            if chosen >> i & 1:
                union |= mask
        if union == full:
            return True
    return False


def main(work):
    work.mkdir(parents=True, exist_ok=True)
    rng = random.Random(20260914017)
    connected_sets = 0
    for case in range(10):
        n = 7 + case % 3
        adjacency = [set() for _ in range(n)]
        for a in range(n):
            for b in range(a):
                if rng.randrange(5) < 2:
                    adjacency[a].add(b)
                    adjacency[b].add(a)
        base_degree = {v: rng.randrange(5) for v in range(n)}
        groups, stages = check.canonical_connected_growth(
            list(range(n)), {v: adjacency[v] for v in range(n)}, base_degree,
            {v: 0 for v in range(n)}, 1
        )
        for size in (3, 4, 5):
            expected = {
                group for group in itertools.combinations(range(n), size)
                if connected(group, adjacency)
                and all(base_degree[v] + len(adjacency[v] & set(group)) >= 4 for v in group)
            }
            connected_sets += len(expected)
            if size < 5:
                check.require(groups[size] == expected, "canonical growth/brute set mismatch")
            else:
                check.require(stages["5"]["degree_qualified"] == len(expected),
                              "canonical growth/brute count mismatch")

    feasible = infeasible = 0
    for case in range(80):
        width = 2 + case % 7
        h = 3 + case % 5
        p = case % 4
        singletons = [rng.randrange(1 << width) for _ in range(h)]
        pairs = [rng.randrange(1 << width) for _ in range(p)]
        expected = brute_cover(singletons, pairs, width)
        actual, _ = check.weighted_cover_after_dominance(singletons, pairs, width)
        check.require(actual == expected, "dominance cover/brute mismatch")
        if expected:
            feasible += 1
        else:
            infeasible += 1
    check.require(feasible and infeasible, "cover controls need both outcomes")

    masks = {0: 1, 1: 2, 2: 6}
    check.residual_completion_check([(0,)], [(1,)], masks, 3)
    rejected = 0
    try:
        check.residual_completion_check([(0,)], [(2,)], masks, 3)
    except ValueError:
        rejected += 1
    check.require(rejected == 1, "completion superset control accepted")

    result = {
        "status": "PASS",
        "random_graphs": 10,
        "qualified_connected_sets": connected_sets,
        "cover_instances": 80,
        "feasible_cover_instances": feasible,
        "infeasible_cover_instances": infeasible,
        "bad_completion_rejected": rejected,
    }
    (work / "controls.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()
    main(args.work.resolve())
