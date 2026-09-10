#!/usr/bin/env python3
"""Exact checker for the compact hard-e1 fixed-link contradiction.

The certificate is a weighted double count.  This program validates the
archived link, the displayed automorphisms and their orbits, every entry of
the twelve-row candidate table, and the final strict integer gap.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, deque
from itertools import combinations
from pathlib import Path
from typing import Iterable, Sequence


POINTS = tuple(range(1, 13))
CANDIDATES = tuple(combinations(POINTS, 7))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_link(path: Path) -> tuple[frozenset[int], ...]:
    blocks = []
    for raw in path.read_text(encoding="ascii").splitlines():
        text = raw.split("#", 1)[0].strip()
        if not text:
            continue
        points = tuple(map(int, text.split()))
        if len(points) != 6 or len(set(points)) != 6 or not set(points) <= set(POINTS):
            raise ValueError(f"invalid link block: {text}")
        blocks.append(frozenset(points))
    if len(blocks) != 41 or len(set(blocks)) != 41:
        raise ValueError("link must contain 41 distinct blocks")
    for target in combinations(POINTS, 4):
        if not any(set(target) <= block for block in blocks):
            raise ValueError(f"link misses quadruple {target}")
    return tuple(blocks)


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Return left after right, with permutations stored as point images."""
    return tuple(left[right[point - 1] - 1] for point in POINTS)


def generated_group(generators: Sequence[tuple[int, ...]]) -> set[tuple[int, ...]]:
    identity = POINTS
    group = {identity}
    queue = deque([identity])
    while queue:
        permutation = queue.popleft()
        for generator in generators:
            product = compose(generator, permutation)
            if product not in group:
                group.add(product)
                queue.append(product)
    return group


def image(block: frozenset[int], permutation: tuple[int, ...]) -> frozenset[int]:
    return frozenset(permutation[point - 1] for point in block)


def set_orbits(
    domain: Iterable[frozenset[int]], group: set[tuple[int, ...]]
) -> list[tuple[frozenset[int], set[frozenset[int]]]]:
    unseen = set(domain)
    result = []
    while unseen:
        representative = min(unseen, key=lambda block: tuple(sorted(block)))
        orbit = {image(representative, permutation) for permutation in group}
        if not orbit <= unseen:
            raise AssertionError("group images do not form a fresh orbit")
        result.append((representative, orbit))
        unseen.difference_update(orbit)
    return result


def parse_permutation(values: object) -> tuple[int, ...]:
    if not isinstance(values, list) or len(values) != 12:
        raise ValueError("each generator must list twelve images")
    permutation = tuple(values)
    if any(not isinstance(value, int) for value in permutation) or set(permutation) != set(POINTS):
        raise ValueError("invalid permutation")
    return permutation


def parse_block(values: object, size: int) -> tuple[int, ...]:
    if not isinstance(values, list) or len(values) != size:
        raise ValueError(f"expected a {size}-set")
    block = tuple(values)
    if any(not isinstance(value, int) for value in block) or tuple(sorted(set(block))) != block:
        raise ValueError(f"invalid sorted {size}-set")
    if not set(block) <= set(POINTS):
        raise ValueError("block leaves the point set")
    return block


def check(link_path: Path, certificate_path: Path) -> dict[str, int | tuple[int, ...]]:
    link = read_link(link_path)
    link_set = set(link)
    document = json.loads(certificate_path.read_text(encoding="ascii"))
    if document.get("format") != "C1375-hard-e1-weighted-orbit-certificate-v1":
        raise ValueError("wrong certificate format")
    if document.get("source_link_sha256") != sha256(link_path):
        raise ValueError("source-link hash mismatch")

    degrees = Counter(point for block in link for point in block)
    if Counter(degrees.values()) != Counter({20: 6, 21: 6}):
        raise ValueError(f"wrong link degree profile: {Counter(degrees.values())}")
    link_low = tuple(point for point in POINTS if degrees[point] == 20)
    if document.get("link_degree_20_points") != list(link_low):
        raise ValueError("degree-20 point metadata mismatch")

    raw_generators = document.get("automorphism_generators")
    if not isinstance(raw_generators, list) or len(raw_generators) != 2:
        raise ValueError("certificate must contain two generators")
    generators = tuple(parse_permutation(values) for values in raw_generators)
    for generator in generators:
        if {image(block, generator) for block in link} != link_set:
            raise ValueError("displayed generator is not a link automorphism")
    group = generated_group(generators)
    if len(group) != document.get("generated_group_order"):
        raise ValueError("generated-group order mismatch")

    residual = {
        frozenset(target)
        for target in combinations(POINTS, 5)
        if not any(set(target) <= block for block in link)
    }
    if len(residual) != 546:
        raise AssertionError(f"expected 546 residual targets, got {len(residual)}")
    residual_orbits = set_orbits(residual, group)
    raw_residual = document.get("residual_orbits")
    if not isinstance(raw_residual, list) or len(raw_residual) != len(residual_orbits):
        raise ValueError("residual-orbit count mismatch")
    target_weight: dict[frozenset[int], int] = {}
    residual_rows = []
    for (representative, orbit), row in zip(residual_orbits, raw_residual):
        expected_rep = parse_block(row.get("representative"), 5)
        size = row.get("size")
        weight = row.get("weight")
        if tuple(sorted(representative)) != expected_rep or len(orbit) != size:
            raise ValueError("residual-orbit metadata mismatch")
        if not isinstance(weight, int) or weight < 0:
            raise ValueError("residual weight must be a nonnegative integer")
        for target in orbit:
            target_weight[target] = weight
        residual_rows.append((expected_rep, size, weight))
    if set(target_weight) != residual:
        raise AssertionError("weighted target orbits do not partition the residual targets")

    weighted_requirement = sum(target_weight.values())
    candidates = tuple(map(frozenset, CANDIDATES))
    candidate_orbits = set_orbits(candidates, group)
    raw_candidates = document.get("candidate_orbits")
    if not isinstance(raw_candidates, list) or len(raw_candidates) != len(candidate_orbits):
        raise ValueError("candidate-orbit count mismatch")
    candidate_rows = []
    per_block_bound = document.get("per_block_bound")
    if not isinstance(per_block_bound, int):
        raise ValueError("per-block bound must be an integer")
    for (representative, orbit), row in zip(candidate_orbits, raw_candidates):
        expected_rep = parse_block(row.get("representative"), 7)
        link_low_count = len(representative.intersection(link_low))
        contained_weight = sum(
            weight for target, weight in target_weight.items() if target <= representative
        )
        score = contained_weight + 8 * link_low_count
        actual = {
            "representative": list(sorted(representative)),
            "size": len(orbit),
            "link_low_count": link_low_count,
            "contained_weight": contained_weight,
            "score": score,
        }
        if row != actual:
            raise ValueError(f"candidate-orbit row mismatch: expected {actual}, got {row}")
        for block in orbit:
            block_weight = sum(
                weight for target, weight in target_weight.items() if target <= block
            )
            if block_weight + 8 * len(block.intersection(link_low)) != score:
                raise AssertionError("candidate score is not orbit-invariant")
        if score > per_block_bound:
            raise ValueError("claimed per-block bound fails")
        candidate_rows.append((expected_rep, len(orbit), link_low_count, contained_weight, score))
    if sum(len(orbit) for _, orbit in candidate_orbits) != len(CANDIDATES):
        raise AssertionError("candidate orbits do not partition all candidates")

    completion_blocks = document.get("completion_blocks")
    variable_degree = document.get("variable_degree_on_link_degree_20_points")
    if completion_blocks != 36 or variable_degree != 22:
        raise ValueError("hard-e1 completion parameters must be 36 and 22")
    weighted_upper = per_block_bound * completion_blocks - 8 * len(link_low) * variable_degree
    strict_gap = weighted_requirement - weighted_upper
    expected_arithmetic = document.get("arithmetic")
    actual_arithmetic = {
        "weighted_requirement": weighted_requirement,
        "weighted_upper": weighted_upper,
        "strict_gap": strict_gap,
    }
    if expected_arithmetic != actual_arithmetic or strict_gap <= 0:
        raise ValueError(f"final contradiction mismatch: {actual_arithmetic}")

    return {
        "group_order": len(group),
        "residual_orbits": len(residual_orbits),
        "candidate_orbits": len(candidate_orbits),
        "weighted_requirement": weighted_requirement,
        "weighted_upper": weighted_upper,
        "strict_gap": strict_gap,
        "link_low": link_low,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_link", type=Path)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    result = check(args.source_link, args.certificate)
    print("exact_compact_certificate_check=PASS")
    print(f"source_link_sha256={sha256(args.source_link)}")
    print("link_blocks=41 link_degree_profile=20^6,21^6")
    print(f"automorphism_generators=2 generated_group_order={result['group_order']}")
    print(
        f"residual_targets=546 residual_orbits={result['residual_orbits']} "
        f"weighted_requirement={result['weighted_requirement']}"
    )
    print(
        f"candidate_blocks=792 candidate_orbits={result['candidate_orbits']} "
        "per_block_score_at_most=48"
    )
    print(
        "completion_blocks=36 link_degree_20_points="
        + ",".join(map(str, result["link_low"]))
        + f" variable_degree=22 weighted_upper={result['weighted_upper']}"
    )
    print(f"strict_integer_gap={result['strict_gap']} fractional_relaxation=INFEASIBLE")
    print("conclusion=archived link has no hard-e1 36-block completion")


if __name__ == "__main__":
    main()
