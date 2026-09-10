#!/usr/bin/env python3
"""Independent bit-mask checker for the hard-e1 weighted certificate.

This implementation does not import the primary checker.  It represents
subsets as integers, constructs the generated permutation group independently,
and checks all 792 candidate blocks directly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path


N = 12
ALL_POINTS = tuple(range(1, N + 1))


def mask(points) -> int:
    result = 0
    for point in points:
        result |= 1 << (point - 1)
    return result


def points(block: int) -> tuple[int, ...]:
    return tuple(index + 1 for index in range(N) if block & (1 << index))


def contained(small: int, large: int) -> bool:
    return small & large == small


def read_masks(path: Path) -> list[int]:
    result = []
    for raw in path.read_text(encoding="ascii").splitlines():
        text = raw.split("#", 1)[0].strip()
        if not text:
            continue
        values = tuple(map(int, text.split()))
        if len(values) != 6 or len(set(values)) != 6 or not set(values) <= set(ALL_POINTS):
            raise ValueError(f"bad source block: {text}")
        result.append(mask(values))
    if len(result) != 41 or len(set(result)) != 41:
        raise ValueError("source link must have 41 distinct blocks")
    return result


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(N))


def closure(generators: tuple[tuple[int, ...], ...]) -> set[tuple[int, ...]]:
    identity = tuple(range(N))
    result = {identity}
    boundary = [identity]
    while boundary:
        current = boundary.pop()
        for generator in generators:
            product = compose(current, generator)
            if product not in result:
                result.add(product)
                boundary.append(product)
    return result


def permute(block: int, permutation: tuple[int, ...]) -> int:
    result = 0
    for source in range(N):
        if block & (1 << source):
            result |= 1 << permutation[source]
    return result


def check(link_path: Path, certificate_path: Path):
    link = read_masks(link_path)
    link_set = set(link)
    quadruples = tuple(mask(target) for target in combinations(ALL_POINTS, 4))
    if not all(any(contained(target, block) for block in link) for target in quadruples):
        raise ValueError("source is not a C(12,6,4) cover")

    document = json.loads(certificate_path.read_text(encoding="ascii"))
    if document["format"] != "C1375-hard-e1-weighted-orbit-certificate-v1":
        raise ValueError("certificate format")
    digest = hashlib.sha256(link_path.read_bytes()).hexdigest()
    if digest != document["source_link_sha256"]:
        raise ValueError("source hash")

    degree = Counter()
    for block in link:
        for point_index in range(N):
            degree[point_index + 1] += bool(block & (1 << point_index))
    if Counter(degree.values()) != Counter({20: 6, 21: 6}):
        raise ValueError("source degree profile")
    degree20 = tuple(point for point in ALL_POINTS if degree[point] == 20)
    if list(degree20) != document["link_degree_20_points"]:
        raise ValueError("degree-20 metadata")
    degree20_mask = mask(degree20)

    generators = tuple(
        tuple(value - 1 for value in generator)
        for generator in document["automorphism_generators"]
    )
    if len(generators) != 2 or any(set(generator) != set(range(N)) for generator in generators):
        raise ValueError("bad generators")
    for generator in generators:
        if {permute(block, generator) for block in link} != link_set:
            raise ValueError("non-automorphism generator")
    group = closure(generators)
    if len(group) != document["generated_group_order"]:
        raise ValueError("group order")

    all_five = {mask(target) for target in combinations(ALL_POINTS, 5)}
    residual = {
        target for target in all_five
        if not any(contained(target, block) for block in link)
    }
    if len(residual) != 546:
        raise ValueError("residual size")

    target_weight: dict[int, int] = {}
    residual_orbit_sizes = []
    for row in document["residual_orbits"]:
        representative = mask(row["representative"])
        orbit = {permute(representative, permutation) for permutation in group}
        if representative not in residual or not orbit <= residual:
            raise ValueError("bad residual representative")
        if len(orbit) != row["size"] or target_weight.keys() & orbit:
            raise ValueError("bad or overlapping residual orbit")
        weight = row["weight"]
        if not isinstance(weight, int) or weight < 0:
            raise ValueError("bad residual weight")
        target_weight.update((target, weight) for target in orbit)
        residual_orbit_sizes.append(len(orbit))
    if set(target_weight) != residual:
        raise ValueError("residual orbits are not exhaustive")

    candidates = {mask(block) for block in combinations(ALL_POINTS, 7)}
    seen_candidates: set[int] = set()
    scores = Counter()
    bound = document["per_block_bound"]
    for row in document["candidate_orbits"]:
        representative = mask(row["representative"])
        orbit = {permute(representative, permutation) for permutation in group}
        if representative not in candidates or not orbit <= candidates:
            raise ValueError("bad candidate representative")
        if len(orbit) != row["size"] or seen_candidates & orbit:
            raise ValueError("bad or overlapping candidate orbit")
        for block in orbit:
            weighted_containment = sum(
                target_weight.get(mask(target), 0)
                for target in combinations(points(block), 5)
            )
            low_count = (block & degree20_mask).bit_count()
            score = weighted_containment + 8 * low_count
            if score > bound:
                raise ValueError("per-block inequality fails")
            scores[score] += 1
        representative_weight = sum(
            target_weight.get(mask(target), 0)
            for target in combinations(points(representative), 5)
        )
        representative_low = (representative & degree20_mask).bit_count()
        if (
            representative_weight != row["contained_weight"]
            or representative_low != row["link_low_count"]
            or representative_weight + 8 * representative_low != row["score"]
        ):
            raise ValueError("candidate row metadata")
        seen_candidates.update(orbit)
    if seen_candidates != candidates:
        raise ValueError("candidate orbits are not exhaustive")

    weighted_requirement = sum(target_weight.values())
    count = document["completion_blocks"]
    variable_degree = document["variable_degree_on_link_degree_20_points"]
    weighted_upper = bound * count - 8 * len(degree20) * variable_degree
    gap = weighted_requirement - weighted_upper
    if document["arithmetic"] != {
        "weighted_requirement": weighted_requirement,
        "weighted_upper": weighted_upper,
        "strict_gap": gap,
    } or gap <= 0:
        raise ValueError("contradiction arithmetic")
    return digest, len(group), residual_orbit_sizes, scores, weighted_requirement, weighted_upper, gap


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_link", type=Path)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    digest, group_order, residual_sizes, scores, lower, upper, gap = check(
        args.source_link, args.certificate
    )
    print("independent_bitmask_certificate_check=PASS")
    print(f"source_link_sha256={digest}")
    print(f"generated_group_order={group_order} residual_orbit_sizes=" + ",".join(map(str, residual_sizes)))
    print("all_792_candidates_checked=PASS score_histogram=" + ",".join(f"{score}:{scores[score]}" for score in sorted(scores)))
    print(f"weighted_requirement={lower} weighted_upper={upper} strict_integer_gap={gap}")
    print("fractional_hard_e1_completion=INFEASIBLE")


if __name__ == "__main__":
    main()
