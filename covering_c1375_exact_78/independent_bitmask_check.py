#!/usr/bin/env python3
"""Independent bit-mask audit of the exact C(13,7,5)=78 certificates.

This script does not import the primary checker or the certificate generator.
It reconstructs all incidence rows using integer masks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, deque
from itertools import combinations
from pathlib import Path


GENERATOR_IMAGES = (
    (2, 3, 4, 6, 5, 9, 8, 7, 10, 11, 12),
    (3, 4, 7, 9, 11, 2, 6, 5, 10, 12, 8),
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse(path, block_size, minimum, maximum):
    rows = []
    for raw in path.read_text(encoding="ascii").splitlines():
        text = raw.partition("#")[0].strip()
        if not text:
            continue
        points = tuple(sorted(map(int, text.split())))
        if len(points) != block_size or len(set(points)) != block_size:
            raise ValueError(f"malformed block in {path}")
        if points[0] < minimum or points[-1] > maximum:
            raise ValueError(f"out-of-range block in {path}")
        rows.append(points)
    if len(rows) != len(set(rows)):
        raise ValueError(f"repeated block in {path}")
    return tuple(rows)


def subset(a, b):
    return a & b == a


def mask_r(points):
    return sum(1 << (point - 2) for point in points)


def mask_12(points):
    return sum(1 << (point - 1) for point in points)


def k_masks(n, k):
    return tuple(sum(1 << i for i in row) for row in combinations(range(n), k))


def compose(a, b):
    return tuple(a[b[i]] for i in range(11))


def make_group(m_blocks):
    generators = tuple(tuple(value - 2 for value in row) for row in GENERATOR_IMAGES)
    for generator in generators:
        images = {
            sum(1 << generator[i] for i in range(11) if block >> i & 1)
            for block in m_blocks
        }
        if images != set(m_blocks):
            raise AssertionError("independent generator check failed")
    identity = tuple(range(11))
    group = {identity}
    todo = deque([identity])
    while todo:
        current = todo.popleft()
        for generator in generators:
            result = compose(generator, current)
            if result not in group:
                group.add(result)
                todo.append(result)
    if len(group) != 240:
        raise AssertionError(f"independent group order {len(group)}")
    return tuple(sorted(group))


def permute_mask(block, permutation):
    return sum(1 << permutation[i] for i in range(11) if block >> i & 1)


def weak_compositions(total, length, prefix=()):
    if length == 1:
        yield prefix + (total,)
    else:
        for value in range(total + 1):
            yield from weak_compositions(total - value, length - 1, prefix + (value,))


def independent_profile_orbits(group):
    remaining = set(weak_compositions(6, 11))
    answer = []
    while remaining:
        representative = min(remaining)
        orbit = set()
        for permutation in group:
            inverse = [0] * 11
            for old, new in enumerate(permutation):
                inverse[new] = old
            orbit.add(tuple(representative[inverse[new]] for new in range(11)))
        if not orbit <= remaining:
            raise AssertionError("independent profile orbit overlap")
        answer.append((representative, len(orbit)))
        remaining -= orbit
    if len(answer) != 143 or sum(size for _, size in answer) != 8008:
        raise AssertionError("independent profile orbit census failed")
    return answer


def link_matrix(m_blocks, profile, link_candidates, blocker=None):
    rows = []
    for target in k_masks(11, 4):
        if any(subset(target, block) for block in m_blocks):
            continue
        rows.append(([i for i, block in enumerate(link_candidates) if subset(target, block)], 1, None))
    if len(rows) != 230:
        raise AssertionError("independent residual-quadruple count")
    rows.append((list(range(462)), 21, 21))
    fixed_degree = [sum(block >> i & 1 for block in m_blocks) for i in range(11)]
    for i in range(11):
        target = 20 + profile[i] - fixed_degree[i]
        rows.append(([j for j, block in enumerate(link_candidates) if block >> i & 1], target, target))
    # Full point set is indexed 0..11, with root point 1 at bit 0 and R at bits 1..11.
    fixed_full = tuple(1 | (block << 1) for block in m_blocks)
    candidate_full = tuple(block << 1 for block in link_candidates)
    for size, lower in ((2, 9), (3, 3)):
        for target in k_masks(12, size):
            fixed_count = sum(subset(target, block) for block in fixed_full)
            need = lower - fixed_count
            if need <= 0:
                continue
            columns = [i for i, block in enumerate(candidate_full) if subset(target, block)]
            if not columns:
                raise AssertionError("independent empty shadow support")
            rows.append((columns, need, None))
    if blocker is not None:
        rows.append((list(blocker), None, 20))
    if len(rows) != (458 if blocker is not None else 457):
        raise AssertionError("independent link-row count")
    return rows


def replay(case, variable_count, rows):
    if case["row_count"] != len(rows) or case["matrix_nonzeros"] != sum(len(row[0]) for row in rows):
        raise AssertionError("independent matrix metadata mismatch")
    multipliers = [0] * len(rows)
    last = -1
    for index, value in case["multipliers"]:
        if not last < index < len(rows) or not isinstance(value, int) or value == 0:
            raise AssertionError("independent sparse-vector check failed")
        multipliers[index] = value
        last = index
    coefficients = [0] * variable_count
    rhs = 0
    for multiplier, (columns, lower, upper) in zip(multipliers, rows):
        if multiplier > 0:
            if lower is None:
                raise AssertionError("positive multiplier lacks lower bound")
            rhs += multiplier * lower
        elif multiplier < 0:
            if upper is None:
                raise AssertionError("negative multiplier lacks upper bound")
            rhs += multiplier * upper
        for column in columns:
            coefficients[column] += multiplier
    maximum = sum(max(value, 0) for value in coefficients)
    result = {
        "support": sum(value != 0 for value in multipliers),
        "max_abs_multiplier": max(map(abs, multipliers), default=0),
        "rhs": rhs,
        "max_box_lhs": maximum,
        "gap": rhs - maximum,
    }
    if any(case[key] != value for key, value in result.items()) or result["gap"] <= 0:
        raise AssertionError("independent Farkas replay failed")
    return result


def check_extension(m_blocks, extension):
    if len(extension) != 21 or len(set(extension)) != 21:
        raise AssertionError("independent extension-size check")
    fixed = tuple(1 | (block << 1) for block in m_blocks)
    variable = tuple(block << 1 for block in extension)
    full = fixed + variable
    for target in k_masks(12, 4):
        if not any(subset(target, block) for block in full):
            raise AssertionError("independent extension-coverage check")
    degrees = [sum(block >> i & 1 for block in full) for i in range(12)]
    if degrees[0] != 20 or min(degrees[1:]) < 20 or sum(value - 20 for value in degrees[1:]) != 6:
        raise AssertionError("independent extension-degree check")
    return tuple(value - 20 for value in degrees[1:])


def completion_matrix(m_blocks, left, right, d_candidates):
    known = tuple(m_blocks) + tuple(left) + tuple(right)
    rows = []
    for target in k_masks(11, 5):
        if any(subset(target, block) for block in known):
            continue
        rows.append(([i for i, block in enumerate(d_candidates) if subset(target, block)], 1, None))
    residual = len(rows)
    rows.append((list(range(330)), 15, 15))
    return rows, residual


def check_upper():
    modulus = 13
    line = (1, 2, 4, 10)
    bases = (
        (1, 2, 3, 4, 5, 10, 11),
        (1, 2, 3, 4, 6, 10, 12),
        (1, 2, 3, 4, 7, 8, 10),
        (1, 2, 3, 5, 6, 8, 11),
        (1, 2, 3, 5, 7, 11, 12),
        (1, 2, 4, 5, 9, 10, 12),
    )
    shift = lambda row, amount: frozenset((point - 1 + amount) % modulus for point in row)
    lines = {shift(line, amount) for amount in range(modulus)}
    pairs = Counter(frozenset(pair) for row in lines for pair in combinations(row, 2))
    if len(lines) != 13 or len(pairs) != 78 or set(pairs.values()) != {1}:
        raise AssertionError("independent projective-plane check")
    unions = {a | b for a, b in combinations(lines, 2)}
    developed = {shift(base, amount) for base in bases for amount in range(modulus)}
    if len(unions) != 78 or unions != developed:
        raise AssertionError("independent upper-cover development check")
    histogram = Counter(sum(set(target) <= block for block in unions) for target in combinations(range(13), 5))
    if histogram != Counter({1: 1170, 4: 117}):
        raise AssertionError("independent upper-cover incidence check")
    return histogram


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_link", type=Path)
    parser.add_argument("prior_witness", type=Path)
    parser.add_argument("prior_certificates", type=Path)
    parser.add_argument("certificates", type=Path)
    args = parser.parse_args()

    source_points = parse(args.source_link, 6, 1, 12)
    if len(source_points) != 41:
        raise AssertionError("independent source-size check")
    source_masks = tuple(map(mask_12, source_points))
    for target in k_masks(12, 4):
        if not any(subset(target, block) for block in source_masks):
            raise AssertionError("independent source-cover check")
    m_blocks = tuple(mask_r(tuple(p for p in block if p != 1)) for block in source_points if 1 in block)
    if len(m_blocks) != 20 or len(set(m_blocks)) != 20:
        raise AssertionError("independent second-link size check")
    for target in k_masks(11, 3):
        if not any(subset(target, block) for block in m_blocks):
            raise AssertionError("independent second-link coverage check")

    link_candidates = k_masks(11, 6)
    d_candidates = k_masks(11, 7)
    link_index = {block: i for i, block in enumerate(link_candidates)}
    group = make_group(m_blocks)
    profiles = independent_profile_orbits(group)

    new_document = json.loads(args.certificates.read_text(encoding="ascii"))
    if new_document.get("format") != "C1375-exact-78-farkas-v1":
        raise AssertionError("independent new-format check")
    if new_document["source_link_sha256"] != digest(args.source_link):
        raise AssertionError("independent source-hash check")
    if new_document["prior_witness_sha256"] != digest(args.prior_witness):
        raise AssertionError("independent prior-witness-hash check")
    if new_document["prior_certificate_sha256"] != digest(args.prior_certificates):
        raise AssertionError("independent prior-certificate-hash check")
    expected_indices = list(range(142))
    profile_results = []
    if len(new_document["profile_cases"]) != 142:
        raise AssertionError("independent profile-case count")
    for orbit, case in zip(expected_indices, new_document["profile_cases"]):
        profile, orbit_size = profiles[orbit]
        if case["orbit"] != orbit or case["representative"] != list(profile) or case["orbit_size"] != orbit_size:
            raise AssertionError("independent profile metadata check")
        if case["partition"] != sorted((x for x in profile if x), reverse=True):
            raise AssertionError("independent partition metadata check")
        profile_results.append(replay(case, 462, link_matrix(m_blocks, profile, link_candidates)))

    survivor, survivor_size = profiles[142]
    if survivor_size != 2 or sorted(survivor) != [0] * 5 + [1] * 6:
        raise AssertionError("independent survivor check")

    witness_points = parse(args.prior_witness, 6, 2, 12)
    witness = tuple(mask_r(block) for block in witness_points)
    witness_profile = check_extension(m_blocks, witness)
    prior = json.loads(args.prior_certificates.read_text(encoding="ascii"))
    if prior.get("format") != "C1375-hard-e1-link-farkas-v1" or prior["witness_sha256"] != digest(args.prior_witness):
        raise AssertionError("independent prior-certificate metadata check")
    if prior["source_link_sha256"] != digest(args.source_link):
        raise AssertionError("independent prior source-hash check")
    if len(prior["cases"]) != 12:
        raise AssertionError("independent prior-case count")
    seen_high_sets = set()
    prior_results = []
    for orbit, case in enumerate(prior["cases"]):
        high = tuple(point - 2 for point in case["high"])
        high_mask = sum(1 << point for point in high)
        images = {permute_mask(high_mask, permutation) for permutation in group}
        if seen_high_sets & images:
            raise AssertionError("independent prior high-orbit overlap")
        seen_high_sets |= images
        if case["orbit"] != orbit or case["high_orbit_size"] != len(images):
            raise AssertionError("independent prior high-orbit metadata")
        blocked = orbit == 11
        if case["known_blocker"] != blocked:
            raise AssertionError("independent prior blocker metadata")
        profile = tuple(int(high_mask >> i & 1) for i in range(11))
        blocker = tuple(sorted(link_index[block] for block in witness)) if blocked else None
        prior_results.append(replay(case, 462, link_matrix(m_blocks, profile, link_candidates, blocker)))
    if len(seen_high_sets) != math.comb(11, 6):
        raise AssertionError("independent prior high-orbit exhaustiveness")
    witness_high = sum((witness_profile[i] == 1) << i for i in range(11))
    survivor_high = sum((survivor[i] == 1) << i for i in range(11))
    if witness_high not in {permute_mask(survivor_high, permutation) for permutation in group}:
        raise AssertionError("independent survivor-to-witness orbit check")
    last_high = sum(1 << (point - 2) for point in prior["cases"][11]["high"])
    if witness_high != last_high:
        raise AssertionError("independent blocked-witness high-set check")

    source_extension = tuple(mask_r(block) for block in source_points if 1 not in block)
    check_extension(m_blocks, source_extension)
    extension_orbit = {
        frozenset(permute_mask(block, permutation) for block in witness)
        for permutation in group
    }
    if extension_orbit != {frozenset(source_extension), frozenset(witness)}:
        raise AssertionError("independent two-extension orbit check")
    canonical = (tuple(sorted(source_extension)), tuple(sorted(witness)))

    completion_results = []
    residual_counts = []
    for pair, case in zip(((0, 0), (0, 1)), new_document["completion_cases"]):
        if tuple(case["pair"]) != pair:
            raise AssertionError("independent terminal-pair metadata")
        rows, residual = completion_matrix(m_blocks, canonical[pair[0]], canonical[pair[1]], d_candidates)
        if case["residual_five_sets"] != residual:
            raise AssertionError("independent terminal residual count")
        residual_counts.append(residual)
        completion_results.append(replay(case, 330, rows))

    histogram = check_upper()
    print("independent_bitmask_farkas_check=PASS")
    print("group_order=240 profile_orbits=143 excluded_orbits=142 excluded_labeled=8006")
    print(f"profile_min_gap={min(row['gap'] for row in profile_results)} profile_max_support={max(row['support'] for row in profile_results)}")
    print(f"prior_uniqueness_cases={len(prior_results)} surviving_extensions={len(extension_orbit)}")
    print(
        "terminal_cases=2 residual_five_sets=" + ",".join(map(str, residual_counts))
        + " strict_gaps=" + ",".join(str(row["gap"]) for row in completion_results)
    )
    print("upper_cover_blocks=78 five_set_histogram=" + ",".join(f"{k}:{histogram[k]}" for k in sorted(histogram)))
    print(f"certificate_sha256={digest(args.certificates)}")
    print("conclusion=C(13,7,5)=78")


if __name__ == "__main__":
    main()
