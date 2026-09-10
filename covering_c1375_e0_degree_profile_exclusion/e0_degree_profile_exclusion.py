#!/usr/bin/env python3
"""Exact checker for twenty excluded e0 point-degree profile orbits."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, deque
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Sequence


GROUND = tuple(range(13))
R = tuple(range(2, 13))
GROUP_GENERATORS = (
    (2, 3, 4, 6, 5, 9, 8, 7, 10, 11, 12),
    (3, 4, 7, 9, 11, 2, 6, 5, 10, 12, 8),
)
EXCLUDED_ORBITS = (0, 1, 2, 3, 4, 7, 10, 12, 13, 14, 15, 16, 19, 20, 30, 33, 37, 67, 75, 110)
PARTITION_COUNTS = {
    (6,): (2, 2),
    (5, 1): (5, 5),
    (4, 2): (5, 4),
    (4, 1, 1): (12, 6),
    (3, 3): (4, 3),
    (3, 2, 1): (19, 0),
    (3, 1, 1, 1): (19, 0),
    (2, 2, 2): (6, 0),
    (2, 2, 1, 1): (28, 0),
    (2, 1, 1, 1, 1): (31, 0),
    (1, 1, 1, 1, 1, 1): (12, 0),
}
SHADOW_LOWER = {1: 41, 2: 20, 3: 9}


@dataclass(frozen=True)
class Row:
    columns: tuple[int, ...]
    lower: int | None
    upper: int | None
    label: str


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_source(path: Path) -> tuple[tuple[int, ...], ...]:
    blocks = []
    for raw in path.read_text(encoding="ascii").splitlines():
        text = raw.split("#", 1)[0].strip()
        if not text:
            continue
        block = tuple(sorted(map(int, text.split())))
        if len(block) != 6 or len(set(block)) != 6 or not set(block) <= set(range(1, 13)):
            raise ValueError(f"invalid source block: {text}")
        blocks.append(block)
    if len(blocks) != 41 or len(set(blocks)) != 41:
        raise ValueError("source must have 41 distinct blocks")
    block_sets = tuple(map(frozenset, blocks))
    for target in combinations(range(1, 13), 4):
        if not any(frozenset(target) <= block for block in block_sets):
            raise ValueError(f"source misses quadruple {target}")
    if sum(1 in block for block in blocks) != 20:
        raise ValueError("source point 1 must have degree 20")
    return tuple(blocks)


def second_link(source: Sequence[tuple[int, ...]]) -> tuple[tuple[int, ...], ...]:
    result = tuple(
        tuple(point for point in block if point != 1)
        for block in source
        if 1 in block
    )
    if len(result) != 20 or len(set(result)) != 20:
        raise AssertionError("second link must have twenty distinct blocks")
    result_sets = tuple(map(frozenset, result))
    for target in combinations(R, 3):
        if not any(frozenset(target) <= block for block in result_sets):
            raise AssertionError(f"second link misses triple {target}")
    return result


def second_link_sha256(blocks: Sequence[tuple[int, ...]]) -> str:
    text = "".join(" ".join(map(str, block)) + "\n" for block in blocks)
    return hashlib.sha256(text.encode("ascii")).hexdigest()


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[point - 2] - 2] for point in R)


def generated_group(
    second: Sequence[tuple[int, ...]], generators: Sequence[tuple[int, ...]]
) -> set[tuple[int, ...]]:
    second_sets = set(map(frozenset, second))
    for generator in generators:
        if len(generator) != 11 or set(generator) != set(R):
            raise ValueError("invalid group generator")
        image = {
            frozenset(generator[point - 2] for point in block) for block in second_sets
        }
        if image != second_sets:
            raise ValueError("group generator is not a second-link automorphism")
    identity = R
    result = {identity}
    boundary = deque([identity])
    while boundary:
        current = boundary.popleft()
        for generator in generators:
            product = compose(generator, current)
            if product not in result:
                result.add(product)
                boundary.append(product)
    return result


def compositions(total: int, length: int, prefix=()):
    if length == 1:
        yield prefix + (total,)
        return
    for first in range(total + 1):
        yield from compositions(total - first, length - 1, prefix + (first,))


def profile_orbits(group: set[tuple[int, ...]]):
    unseen = set(compositions(6, 11))
    result = []
    while unseen:
        representative = min(unseen)
        orbit = {
            tuple(representative[permutation[index] - 2] for index in range(11))
            for permutation in group
        }
        if not orbit <= unseen:
            raise AssertionError("profile orbits overlap")
        result.append((representative, len(orbit)))
        unseen.difference_update(orbit)
    if sum(size for _, size in result) != math.comb(16, 10):
        raise AssertionError("profile orbits do not cover all weak compositions")
    return result


def primary_families():
    family_b = tuple(frozenset((0, *block)) for block in combinations(R, 6))
    family_c = tuple(frozenset((1, *block)) for block in combinations(R, 6))
    family_d = tuple(frozenset(block) for block in combinations(R, 7))
    if tuple(map(len, (family_b, family_c, family_d))) != (462, 462, 330):
        raise AssertionError("primary family sizes")
    return family_b, family_c, family_d


def build_rows(
    second: Sequence[tuple[int, ...]], profile: tuple[int, ...]
) -> tuple[tuple[frozenset[int], ...], list[Row]]:
    if len(profile) != 11 or min(profile) < 0 or sum(profile) != 6:
        raise ValueError("profile must be an eleven-part weak composition of six")
    fixed = tuple(frozenset((0, 1, *block)) for block in second)
    families = primary_families()
    primary = families[0] + families[1] + families[2]

    def support(subset: frozenset[int]) -> tuple[int, ...]:
        return tuple(index for index, block in enumerate(primary) if subset <= block)

    rows = []
    residual = []
    for target in combinations(GROUND, 5):
        target_set = frozenset(target)
        if any(target_set <= block for block in fixed):
            continue
        residual.append(target)
        rows.append(
            Row(support(target_set), 1, None, "five:" + "-".join(map(str, target)))
        )
    if len(residual) != 902:
        raise AssertionError(f"expected 902 residual five-sets, got {len(residual)}")

    offset = 0
    for name, family, count in (
        ("B", families[0], 21),
        ("C", families[1], 21),
        ("D", families[2], 15),
    ):
        columns = tuple(range(offset, offset + len(family)))
        rows.append(Row(columns, count, count, f"category:{name}"))
        offset += len(family)

    fixed_degree = Counter(point for block in second for point in block)
    for size in range(1, 4):
        lower = SHADOW_LOWER[size]
        for subset in combinations(GROUND, size):
            subset_set = frozenset(subset)
            fixed_count = sum(subset_set <= block for block in fixed)
            need = lower - fixed_count
            upper = None
            if size == 1 and subset[0] in R:
                need = 41 + profile[subset[0] - 2] - fixed_degree[subset[0]]
                upper = need
            if need > 0:
                columns = support(subset_set)
                if not columns:
                    raise AssertionError((subset, need))
                rows.append(
                    Row(
                        columns,
                        need,
                        upper,
                        f"shadow{size}:" + "-".join(map(str, subset)),
                    )
                )
    if len(rows) != 1270:
        raise AssertionError(f"expected 1270 rows, got {len(rows)}")
    return primary, rows


def farkas_metrics(
    variable_count: int, rows: Sequence[Row], sparse_multipliers: Sequence[Sequence[int]]
) -> dict[str, int]:
    multipliers = [0] * len(rows)
    prior = -1
    for pair in sparse_multipliers:
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError("each multiplier must be [row,value]")
        index, value = pair
        if (
            not isinstance(index, int)
            or not isinstance(value, int)
            or not value
            or not prior < index < len(rows)
        ):
            raise ValueError("invalid sparse multiplier")
        multipliers[index] = value
        prior = index

    coefficients = [0] * variable_count
    rhs = 0
    for multiplier, row in zip(multipliers, rows):
        if multiplier > 0:
            if row.lower is None:
                raise ValueError(f"positive multiplier has no lower bound: {row.label}")
            rhs += multiplier * row.lower
        elif multiplier < 0:
            if row.upper is None:
                raise ValueError(f"negative multiplier has no upper bound: {row.label}")
            rhs += multiplier * row.upper
        for column in row.columns:
            coefficients[column] += multiplier
    maximum = sum(max(coefficient, 0) for coefficient in coefficients)
    return {
        "support": sum(multiplier != 0 for multiplier in multipliers),
        "max_abs_multiplier": max(map(abs, multipliers), default=0),
        "rhs": rhs,
        "max_box_lhs": maximum,
        "gap": rhs - maximum,
    }


def verify(source_path: Path, certificate_path: Path):
    source = read_source(source_path)
    second = second_link(source)
    document = json.loads(certificate_path.read_text(encoding="ascii"))
    if document.get("format") != "C1375-e0-degree-profile-farkas-v1":
        raise ValueError("wrong certificate format")
    if document.get("source_link_sha256") != sha256(source_path):
        raise ValueError("source-link hash mismatch")
    if document.get("second_link_sha256") != second_link_sha256(second):
        raise ValueError("second-link hash mismatch")
    if document.get("group_generators") != [list(row) for row in GROUP_GENERATORS]:
        raise ValueError("group-generator metadata mismatch")
    group = generated_group(second, GROUP_GENERATORS)
    if len(group) != document.get("group_order") or len(group) != 240:
        raise ValueError("generated-group order mismatch")
    orbits = profile_orbits(group)
    if len(orbits) != document.get("profile_orbits") or len(orbits) != 143:
        raise ValueError("profile-orbit count mismatch")
    if document.get("labeled_profiles") != 8008:
        raise ValueError("labeled-profile count mismatch")
    if document.get("excluded_orbits") != list(EXCLUDED_ORBITS):
        raise ValueError("excluded-orbit list mismatch")

    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != len(EXCLUDED_ORBITS):
        raise ValueError("certificate must contain twenty cases")
    results = []
    for expected_orbit, case in zip(EXCLUDED_ORBITS, cases):
        profile, orbit_size = orbits[expected_orbit]
        partition = tuple(sorted((value for value in profile if value), reverse=True))
        if (
            case.get("orbit") != expected_orbit
            or case.get("representative") != list(profile)
            or case.get("orbit_size") != orbit_size
            or case.get("partition") != list(partition)
        ):
            raise ValueError(f"case metadata mismatch at orbit {expected_orbit}")
        primary, rows = build_rows(second, profile)
        if case.get("row_count") != len(rows):
            raise ValueError("row count mismatch")
        if case.get("matrix_nonzeros") != sum(len(row.columns) for row in rows):
            raise ValueError("matrix nonzero count mismatch")
        result = farkas_metrics(len(primary), rows, case.get("multipliers", []))
        for field in ("support", "max_abs_multiplier", "rhs", "max_box_lhs", "gap"):
            if case.get(field) != result[field]:
                raise ValueError(f"{field} mismatch at orbit {expected_orbit}")
        if result["gap"] <= 0:
            raise ValueError(f"nonpositive exact gap at orbit {expected_orbit}")
        results.append(result)

    actual_partition_counts = Counter(
        tuple(sorted((value for value in profile if value), reverse=True))
        for profile, _ in orbits
    )
    actual_excluded_counts = Counter(
        tuple(sorted((value for value in orbits[index][0] if value), reverse=True))
        for index in EXCLUDED_ORBITS
    )
    for partition, (total, excluded) in PARTITION_COUNTS.items():
        if actual_partition_counts[partition] != total or actual_excluded_counts[partition] != excluded:
            raise AssertionError((partition, actual_partition_counts[partition], actual_excluded_counts[partition]))
    high_excess_orbits = {
        index for index, (profile, _) in enumerate(orbits) if max(profile) >= 5
    }
    if not high_excess_orbits <= set(EXCLUDED_ORBITS):
        raise AssertionError("degree-cap corollary is not covered")
    excluded_labeled = sum(orbits[index][1] for index in EXCLUDED_ORBITS)
    if excluded_labeled != 536:
        raise AssertionError(excluded_labeled)
    return group, orbits, results, excluded_labeled, sha256(certificate_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_link", type=Path)
    parser.add_argument("certificates", type=Path)
    args = parser.parse_args()
    group, orbits, results, excluded_labeled, digest = verify(
        args.source_link, args.certificates
    )
    print("exact_integer_farkas_check=PASS")
    print(f"source_link_sha256={sha256(args.source_link)}")
    print("fixed_second_link_blocks=20 primary_variables=1254 rows_per_case=1270")
    print(f"generated_group_order={len(group)} profile_orbits={len(orbits)} labeled_profiles=8008")
    print(f"excluded_profile_orbits=20 excluded_labeled_profiles={excluded_labeled} remaining_orbits=123")
    print("excluded_by_partition=6:2/2,5+1:5/5,4+2:4/5,4+1+1:6/12,3+3:3/4")
    print("global_corollary=max_point_degree_at_most_45")
    print("supports=" + ",".join(str(result["support"]) for result in results))
    print("strict_gaps=" + ",".join(str(result["gap"]) for result in results))
    print(f"certificate_sha256={digest}")


if __name__ == "__main__":
    main()
