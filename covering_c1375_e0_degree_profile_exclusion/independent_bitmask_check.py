#!/usr/bin/env python3
"""Independent bit-mask replay of the twenty e0 Farkas certificates."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from itertools import combinations
from pathlib import Path


GROUND = tuple(range(13))
R = tuple(range(2, 13))
EXPECTED_EXCLUDED = (0, 1, 2, 3, 4, 7, 10, 12, 13, 14, 15, 16, 19, 20, 30, 33, 37, 67, 75, 110)


def mask(points) -> int:
    result = 0
    for point in points:
        result |= 1 << point
    return result


def contained(small: int, large: int) -> bool:
    return small & large == small


def read_source(path: Path) -> list[int]:
    result = []
    for raw in path.read_text(encoding="ascii").splitlines():
        text = raw.split("#", 1)[0].strip()
        if not text:
            continue
        block = tuple(map(int, text.split()))
        if len(block) != 6 or len(set(block)) != 6 or not set(block) <= set(range(1, 13)):
            raise ValueError(f"invalid source row: {text}")
        result.append(mask(block))
    if len(result) != 41 or len(set(result)) != 41:
        raise ValueError("source size")
    targets = tuple(mask(target) for target in combinations(range(1, 13), 4))
    if not all(any(contained(target, block) for block in result) for target in targets):
        raise ValueError("source quadruple coverage")
    return result


def second_link(source: list[int]) -> list[int]:
    point1 = 1 << 1
    result = [block & ~point1 for block in source if block & point1]
    if len(result) != 20 or len(set(result)) != 20:
        raise ValueError("second-link size")
    for target in combinations(R, 3):
        target_mask = mask(target)
        if not any(contained(target_mask, block) for block in result):
            raise ValueError("second-link triple coverage")
    return result


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index] - 2] for index in range(11))


def permute(block: int, permutation: tuple[int, ...]) -> int:
    result = 0
    for index, point in enumerate(R):
        if block & (1 << point):
            result |= 1 << permutation[index]
    return result


def group_closure(second: list[int], raw_generators) -> set[tuple[int, ...]]:
    generators = tuple(tuple(row) for row in raw_generators)
    if any(len(row) != 11 or set(row) != set(R) for row in generators):
        raise ValueError("invalid group generators")
    second_set = set(second)
    for generator in generators:
        if {permute(block, generator) for block in second} != second_set:
            raise ValueError("generator is not an automorphism")
    identity = R
    group = {identity}
    boundary = [identity]
    while boundary:
        current = boundary.pop()
        for generator in generators:
            product = compose(current, generator)
            if product not in group:
                group.add(product)
                boundary.append(product)
    return group


def weak_compositions(total: int, length: int, prefix=()):
    if length == 1:
        yield prefix + (total,)
    else:
        for value in range(total + 1):
            yield from weak_compositions(total - value, length - 1, prefix + (value,))


def profile_orbits(group):
    unseen = set(weak_compositions(6, 11))
    result = []
    while unseen:
        representative = min(unseen)
        orbit = {
            tuple(representative[permutation[index] - 2] for index in range(11))
            for permutation in group
        }
        if not orbit <= unseen:
            raise ValueError("profile orbit overlap")
        result.append((representative, len(orbit)))
        unseen -= orbit
    if sum(size for _, size in result) != math.comb(16, 6):
        raise ValueError("profile orbit coverage")
    return result


def primary_blocks():
    family_b = tuple(mask((0, *block)) for block in combinations(R, 6))
    family_c = tuple(mask((1, *block)) for block in combinations(R, 6))
    family_d = tuple(mask(block) for block in combinations(R, 7))
    return family_b, family_c, family_d


def row_support(primary: tuple[int, ...], subset: int) -> int:
    result = 0
    for index, block in enumerate(primary):
        if contained(subset, block):
            result |= 1 << index
    return result


def matrix(second: list[int], profile: tuple[int, ...]):
    fixed = tuple(block | (1 << 0) | (1 << 1) for block in second)
    families = primary_blocks()
    primary = families[0] + families[1] + families[2]
    result: list[tuple[int, int | None, int | None]] = []
    residual_count = 0
    for target in combinations(GROUND, 5):
        target_mask = mask(target)
        if any(contained(target_mask, block) for block in fixed):
            continue
        residual_count += 1
        result.append((row_support(primary, target_mask), 1, None))
    if residual_count != 902:
        raise ValueError("residual count")

    offset = 0
    for family, count in zip(families, (21, 21, 15)):
        result.append((((1 << len(family)) - 1) << offset, count, count))
        offset += len(family)

    fixed_degree = Counter()
    for block in second:
        for point in R:
            fixed_degree[point] += bool(block & (1 << point))
    lower_by_size = {1: 41, 2: 20, 3: 9}
    for size in range(1, 4):
        for subset in combinations(GROUND, size):
            subset_mask = mask(subset)
            fixed_count = sum(contained(subset_mask, block) for block in fixed)
            need = lower_by_size[size] - fixed_count
            upper = None
            if size == 1 and subset[0] in R:
                need = 41 + profile[subset[0] - 2] - fixed_degree[subset[0]]
                upper = need
            if need > 0:
                support = row_support(primary, subset_mask)
                if not support:
                    raise ValueError((subset, need))
                result.append((support, need, upper))
    if len(result) != 1270:
        raise ValueError("matrix row count")
    return primary, result


def metrics(matrix_rows, sparse):
    multipliers = [0] * len(matrix_rows)
    prior = -1
    for index, value in sparse:
        if not isinstance(index, int) or not isinstance(value, int) or not value or not prior < index < len(matrix_rows):
            raise ValueError("invalid multiplier")
        multipliers[index] = value
        prior = index
    coefficients = [0] * 1254
    rhs = 0
    for multiplier, (support, lower, upper) in zip(multipliers, matrix_rows):
        if multiplier > 0:
            if lower is None:
                raise ValueError("positive multiplier without lower bound")
            rhs += multiplier * lower
        elif multiplier < 0:
            if upper is None:
                raise ValueError("negative multiplier without upper bound")
            rhs += multiplier * upper
        bits = support
        while bits:
            least = bits & -bits
            coefficients[least.bit_length() - 1] += multiplier
            bits -= least
    maximum = sum(value for value in coefficients if value > 0)
    return (
        sum(value != 0 for value in multipliers),
        max(map(abs, multipliers), default=0),
        rhs,
        maximum,
        rhs - maximum,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_link", type=Path)
    parser.add_argument("certificates", type=Path)
    args = parser.parse_args()
    source = read_source(args.source_link)
    second = second_link(source)
    document = json.loads(args.certificates.read_text(encoding="ascii"))
    if document["format"] != "C1375-e0-degree-profile-farkas-v1":
        raise ValueError("format")
    source_digest = hashlib.sha256(args.source_link.read_bytes()).hexdigest()
    if document["source_link_sha256"] != source_digest:
        raise ValueError("source hash")
    second_text = "".join(" ".join(map(str, (point for point in R if block & (1 << point)))) + "\n" for block in second)
    if document["second_link_sha256"] != hashlib.sha256(second_text.encode("ascii")).hexdigest():
        raise ValueError("second-link hash")
    group = group_closure(second, document["group_generators"])
    if len(group) != document["group_order"] or len(group) != 240:
        raise ValueError("group order")
    orbits = profile_orbits(group)
    if len(orbits) != document["profile_orbits"] or len(orbits) != 143:
        raise ValueError("profile orbits")
    if tuple(document["excluded_orbits"]) != EXPECTED_EXCLUDED:
        raise ValueError("excluded orbit list")
    if len(document["cases"]) != 20:
        raise ValueError("case count")

    outputs = []
    excluded_labeled = 0
    for expected_orbit, case in zip(EXPECTED_EXCLUDED, document["cases"]):
        profile, orbit_size = orbits[expected_orbit]
        partition = sorted((value for value in profile if value), reverse=True)
        if (
            case["orbit"] != expected_orbit
            or case["representative"] != list(profile)
            or case["orbit_size"] != orbit_size
            or case["partition"] != partition
        ):
            raise ValueError("case metadata")
        primary, rows = matrix(second, profile)
        if len(primary) != 1254 or case["row_count"] != len(rows):
            raise ValueError("matrix dimensions")
        if case["matrix_nonzeros"] != sum(support.bit_count() for support, _, _ in rows):
            raise ValueError("matrix nonzeros")
        actual = metrics(rows, case["multipliers"])
        expected = tuple(case[field] for field in ("support", "max_abs_multiplier", "rhs", "max_box_lhs", "gap"))
        if actual != expected or actual[-1] <= 0:
            raise ValueError((expected_orbit, actual, expected))
        outputs.append(actual)
        excluded_labeled += orbit_size
    if excluded_labeled != 536:
        raise ValueError("excluded labeled count")
    digest = hashlib.sha256(args.certificates.read_bytes()).hexdigest()
    print("independent_bitmask_farkas_check=PASS")
    print(f"source_link_sha256={source_digest} second_link_blocks=20 triple_cover=PASS")
    print("generated_group_order=240 profile_orbits=143 labeled_profiles=8008")
    print("cases=20 variables=1254 rows_per_case=1270 excluded_labeled_profiles=536")
    print("all_strict_integer_contradictions=PASS min_gap=" + str(min(row[-1] for row in outputs)))
    print("supports=" + ",".join(str(row[0]) for row in outputs))
    print("certificate_sha256=" + digest)


if __name__ == "__main__":
    main()
