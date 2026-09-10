#!/usr/bin/env python3
"""Incidence-graph audit of the hard-e1 weighted contradiction.

This checker does not import either submitted checker.  It enumerates the
full automorphism group of the archived link through NetworkX's generic
colored-graph isomorphism machinery, reconstructs the residual orbit weights,
and tests the certificate inequality on all 792 candidate seven-blocks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, deque
from itertools import combinations
from pathlib import Path

import networkx as nx


POINTS = tuple(range(1, 13))


def read_link(path: Path) -> list[tuple[int, ...]]:
    blocks: list[tuple[int, ...]] = []
    for raw in path.read_text(encoding="ascii").splitlines():
        text = raw.split("#", 1)[0].strip()
        if text:
            block = tuple(sorted(map(int, text.split())))
            assert len(block) == len(set(block)) == 6 and set(block) <= set(POINTS)
            blocks.append(block)
    assert len(blocks) == len(set(blocks)) == 41
    block_sets = tuple(map(frozenset, blocks))
    assert all(
        any(frozenset(target) <= block for block in block_sets)
        for target in combinations(POINTS, 4)
    )
    return blocks


def incidence_automorphisms(blocks: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    graph = nx.Graph()
    for point in POINTS:
        graph.add_node(("p", point), color="point")
    for index, block in enumerate(blocks):
        vertex = ("b", index)
        graph.add_node(vertex, color="block")
        graph.add_edges_from((vertex, ("p", point)) for point in block)
    matcher = nx.algorithms.isomorphism.GraphMatcher(
        graph,
        graph,
        node_match=nx.algorithms.isomorphism.categorical_node_match("color", None),
    )
    result = {
        tuple(mapping[("p", point)][1] for point in POINTS)
        for mapping in matcher.isomorphisms_iter()
    }
    assert len(result) == 720
    return result


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[point - 1] - 1] for point in POINTS)


def generator_closure(generators: tuple[tuple[int, ...], ...]) -> set[tuple[int, ...]]:
    identity = POINTS
    result = {identity}
    boundary = deque([identity])
    while boundary:
        current = boundary.popleft()
        for generator in generators:
            image = compose(generator, current)
            if image not in result:
                result.add(image)
                boundary.append(image)
    return result


def image(block: frozenset[int], permutation: tuple[int, ...]) -> frozenset[int]:
    return frozenset(permutation[point - 1] for point in block)


def orbits(
    domain: set[frozenset[int]], group: set[tuple[int, ...]]
) -> list[tuple[frozenset[int], set[frozenset[int]]]]:
    unseen = set(domain)
    result = []
    while unseen:
        seed = min(unseen, key=lambda row: tuple(sorted(row)))
        orbit = {image(seed, permutation) for permutation in group}
        assert orbit <= unseen
        result.append((seed, orbit))
        unseen -= orbit
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("link", type=Path)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()

    blocks = read_link(args.link)
    block_sets = tuple(map(frozenset, blocks))
    certificate = json.loads(args.certificate.read_text(encoding="ascii"))
    assert certificate["format"] == "C1375-hard-e1-weighted-orbit-certificate-v1"
    link_sha = hashlib.sha256(args.link.read_bytes()).hexdigest()
    assert certificate["source_link_sha256"] == link_sha

    full_group = incidence_automorphisms(blocks)
    generators = tuple(tuple(row) for row in certificate["automorphism_generators"])
    generated = generator_closure(generators)
    assert generated == full_group and len(generated) == certificate["generated_group_order"]

    degrees = Counter(point for block in blocks for point in block)
    low = tuple(point for point in POINTS if degrees[point] == 20)
    assert Counter(degrees.values()) == Counter({20: 6, 21: 6})
    assert list(low) == certificate["link_degree_20_points"]

    residual = {
        frozenset(target)
        for target in combinations(POINTS, 5)
        if not any(frozenset(target) <= block for block in block_sets)
    }
    assert len(residual) == 546
    residual_orbits = orbits(residual, full_group)
    rows_by_rep = {
        tuple(row["representative"]): row for row in certificate["residual_orbits"]
    }
    target_weight: dict[frozenset[int], int] = {}
    for representative, orbit in residual_orbits:
        key = tuple(sorted(representative))
        row = rows_by_rep[key]
        assert len(orbit) == row["size"] and isinstance(row["weight"], int)
        assert row["weight"] >= 0
        target_weight.update((target, row["weight"]) for target in orbit)
    assert set(target_weight) == residual and len(residual_orbits) == 6

    low_set = set(low)
    candidates = tuple(map(frozenset, combinations(POINTS, 7)))
    bound = certificate["per_block_bound"]
    scores: Counter[int] = Counter()
    for block in candidates:
        contained = sum(weight for target, weight in target_weight.items() if target <= block)
        score = contained + 8 * len(block & low_set)
        assert score <= bound
        scores[score] += 1
    assert len(candidates) == 792
    assert scores == Counter({39: 30, 41: 60, 44: 120, 45: 60, 46: 96, 47: 60, 48: 366})

    weighted_requirement = sum(target_weight.values())
    weighted_upper = (
        bound * certificate["completion_blocks"]
        - 8 * len(low) * certificate["variable_degree_on_link_degree_20_points"]
    )
    gap = weighted_requirement - weighted_upper
    assert certificate["arithmetic"] == {
        "weighted_requirement": weighted_requirement,
        "weighted_upper": weighted_upper,
        "strict_gap": gap,
    }
    assert (weighted_requirement, weighted_upper, gap) == (678, 672, 6)

    print("independent_incidence_graph_double_count=PASS")
    print(f"networkx={nx.__version__} source_link_sha256={link_sha}")
    print("source_blocks=41 quadruple_cover=PASS degree_profile=20^6,21^6")
    print("full_link_automorphisms=720 certificate_generated_group=720 groups_equal=true")
    print("residual_targets=546 residual_orbits=6 weighted_requirement=678")
    print("candidate_blocks=792 all_directly_checked=true")
    print("score_histogram=39:30,41:60,44:120,45:60,46:96,47:60,48:366")
    print("weighted_upper=672 strict_gap=6 fractional_hard_e1_completion=INFEASIBLE")


if __name__ == "__main__":
    main()
