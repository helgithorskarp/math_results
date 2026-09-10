#!/usr/bin/env python3
"""Exact certificate checker for C(13,7,5)=78.

This standard-library checker verifies the new fixed-second-link
classification and the two terminal e0 completion contradictions.  It also
replays the earlier hard-e1 optimal-link certificates used to establish
uniqueness of the one surviving link extension.
"""

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


POINTS12 = tuple(range(1, 13))
R = tuple(range(2, 13))
LINK_CANDIDATES = tuple(combinations(R, 6))
D_CANDIDATES = tuple(combinations(R, 7))
GROUP_GENERATORS = (
    (2, 3, 4, 6, 5, 9, 8, 7, 10, 11, 12),
    (3, 4, 7, 9, 11, 2, 6, 5, 10, 12, 8),
)
SURVIVING_PROFILE_ORBIT = 142


@dataclass(frozen=True)
class Row:
    columns: tuple[int, ...]
    lower: int | None
    upper: int | None
    label: str


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_blocks(path: Path, size: int, allowed: set[int]) -> tuple[tuple[int, ...], ...]:
    blocks = []
    for raw in path.read_text(encoding="ascii").splitlines():
        text = raw.split("#", 1)[0].strip()
        if not text:
            continue
        block = tuple(sorted(map(int, text.split())))
        if len(block) != size or len(set(block)) != size or not set(block) <= allowed:
            raise ValueError(f"invalid block in {path}: {text}")
        blocks.append(block)
    if len(blocks) != len(set(blocks)):
        raise ValueError(f"duplicate block in {path}")
    return tuple(blocks)


def read_source(path: Path) -> tuple[tuple[int, ...], ...]:
    blocks = read_blocks(path, 6, set(POINTS12))
    if len(blocks) != 41:
        raise ValueError("source must have 41 blocks")
    sets = tuple(map(frozenset, blocks))
    for target in combinations(POINTS12, 4):
        if not any(frozenset(target) <= block for block in sets):
            raise ValueError(f"source misses quadruple {target}")
    if sum(1 in block for block in blocks) != 20:
        raise ValueError("source point 1 must have degree 20")
    return blocks


def second_link(source: Sequence[tuple[int, ...]]) -> tuple[tuple[int, ...], ...]:
    result = tuple(tuple(p for p in block if p != 1) for block in source if 1 in block)
    if len(result) != 20 or len(set(result)) != 20:
        raise AssertionError("second link must have 20 distinct blocks")
    sets = tuple(map(frozenset, result))
    for target in combinations(R, 3):
        if not any(frozenset(target) <= block for block in sets):
            raise AssertionError(f"second link misses triple {target}")
    return result


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[p - 2] - 2] for p in R)


def generated_group(second: Sequence[tuple[int, ...]]) -> tuple[tuple[int, ...], ...]:
    second_sets = set(map(frozenset, second))
    for generator in GROUP_GENERATORS:
        image = {
            frozenset(generator[p - 2] for p in block) for block in second_sets
        }
        if image != second_sets:
            raise AssertionError("generator does not preserve the second link")
    identity = R
    group = {identity}
    boundary = deque([identity])
    while boundary:
        current = boundary.popleft()
        for generator in GROUP_GENERATORS:
            product = compose(generator, current)
            if product not in group:
                group.add(product)
                boundary.append(product)
    if len(group) != 240:
        raise AssertionError(f"group order is {len(group)}, expected 240")
    return tuple(sorted(group))


def compositions(total: int, length: int, prefix=()):
    if length == 1:
        yield prefix + (total,)
        return
    for first in range(total + 1):
        yield from compositions(total - first, length - 1, prefix + (first,))


def profile_orbits(group: Sequence[tuple[int, ...]]):
    unseen = set(compositions(6, 11))
    result = []
    while unseen:
        representative = min(unseen)
        orbit = {
            tuple(representative[g[index] - 2] for index in range(11))
            for g in group
        }
        if not orbit <= unseen:
            raise AssertionError("profile orbits overlap")
        result.append((representative, len(orbit)))
        unseen.difference_update(orbit)
    if len(result) != 143 or sum(size for _, size in result) != math.comb(16, 10):
        raise AssertionError("profile orbit partition is not exhaustive")
    return result


def high_set_orbits(group: Sequence[tuple[int, ...]], representatives):
    seen = set()
    total = 0
    for representative in representatives:
        images = {
            frozenset(g[p - 2] for p in representative)
            for g in group
        }
        if seen & images:
            raise AssertionError("high-set representatives lie in overlapping orbits")
        seen.update(images)
        total += len(images)
    if total != math.comb(11, 6) or len(seen) != math.comb(11, 6):
        raise AssertionError("high-set orbits are not exhaustive")


def link_rows(
    second: Sequence[tuple[int, ...]],
    profile: tuple[int, ...],
    blocker: tuple[int, ...] | None = None,
) -> list[Row]:
    if len(profile) != 11 or min(profile) < 0 or sum(profile) != 6:
        raise ValueError("profile must be a weak composition of six")
    candidate_sets = tuple(map(frozenset, LINK_CANDIDATES))
    fixed_small = tuple(map(frozenset, second))
    fixed = tuple(frozenset((1, *block)) for block in second)
    rows = []
    residual = []
    for target in combinations(R, 4):
        target_set = frozenset(target)
        if any(target_set <= block for block in fixed_small):
            continue
        residual.append(target)
        rows.append(Row(
            tuple(i for i, block in enumerate(candidate_sets) if target_set <= block),
            1,
            None,
            "quadruple:" + "-".join(map(str, target)),
        ))
    if len(residual) != 230:
        raise AssertionError(len(residual))
    rows.append(Row(tuple(range(462)), 21, 21, "count"))
    fixed_degrees = Counter(p for block in second for p in block)
    for p, excess in zip(R, profile):
        target = 20 + excess - fixed_degrees[p]
        rows.append(Row(
            tuple(i for i, block in enumerate(candidate_sets) if p in block),
            target,
            target,
            f"degree:{p}",
        ))
    for size, lower in ((2, 9), (3, 3)):
        for subset in combinations(POINTS12, size):
            subset_set = frozenset(subset)
            fixed_count = sum(subset_set <= block for block in fixed)
            need = lower - fixed_count
            if need <= 0:
                continue
            columns = tuple(
                i for i, block in enumerate(candidate_sets) if subset_set <= block
            )
            if not columns:
                raise AssertionError((subset, need))
            rows.append(Row(columns, need, None, f"shadow{size}:" + "-".join(map(str, subset))))
    if blocker is not None:
        if len(blocker) != 21 or len(set(blocker)) != 21:
            raise AssertionError("bad extension blocker")
        rows.append(Row(blocker, None, 20, "known-extension-overlap<=20"))
    expected = 458 if blocker is not None else 457
    if len(rows) != expected:
        raise AssertionError((len(rows), expected))
    return rows


def verify_extension(
    second: Sequence[tuple[int, ...]], blocks: Sequence[tuple[int, ...]]
) -> tuple[int, ...]:
    if len(blocks) != 21 or len(set(blocks)) != 21:
        raise AssertionError("extension must contain 21 distinct blocks")
    if any(block not in LINK_CANDIDATES for block in blocks):
        raise AssertionError("extension has an invalid block")
    full = tuple((1, *block) for block in second) + tuple(blocks)
    full_sets = tuple(map(frozenset, full))
    for target in combinations(POINTS12, 4):
        if not any(frozenset(target) <= block for block in full_sets):
            raise AssertionError(f"extension misses quadruple {target}")
    degrees = Counter(p for block in full for p in block)
    if degrees[1] != 20:
        raise AssertionError("extension root degree is not 20")
    profile = tuple(degrees[p] - 20 for p in R)
    if min(profile) < 0 or sum(profile) != 6:
        raise AssertionError(f"bad extension profile {profile}")
    return profile


def completion_rows(
    second: Sequence[tuple[int, ...]],
    left: Sequence[tuple[int, ...]],
    right: Sequence[tuple[int, ...]],
) -> tuple[list[Row], int]:
    known = tuple(map(frozenset, second)) + tuple(map(frozenset, left)) + tuple(map(frozenset, right))
    candidates = tuple(map(frozenset, D_CANDIDATES))
    rows = []
    residual = []
    for target in combinations(R, 5):
        target_set = frozenset(target)
        if any(target_set <= block for block in known):
            continue
        residual.append(target)
        rows.append(Row(
            tuple(i for i, block in enumerate(candidates) if target_set <= block),
            1,
            None,
            "five:" + "-".join(map(str, target)),
        ))
    rows.append(Row(tuple(range(330)), 15, 15, "count"))
    return rows, len(residual)


def farkas_metrics(variable_count: int, rows: Sequence[Row], sparse) -> dict[str, int]:
    multipliers = [0] * len(rows)
    prior = -1
    for pair in sparse:
        if (
            not isinstance(pair, list)
            or len(pair) != 2
            or not isinstance(pair[0], int)
            or not isinstance(pair[1], int)
            or not pair[1]
            or not prior < pair[0] < len(rows)
        ):
            raise ValueError("invalid sparse multiplier")
        multipliers[pair[0]] = pair[1]
        prior = pair[0]
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
    maximum = sum(max(value, 0) for value in coefficients)
    return {
        "support": sum(value != 0 for value in multipliers),
        "max_abs_multiplier": max(map(abs, multipliers), default=0),
        "rhs": rhs,
        "max_box_lhs": maximum,
        "gap": rhs - maximum,
    }


def verify_case(case, variable_count: int, rows: Sequence[Row]):
    if case.get("row_count") != len(rows):
        raise ValueError("row-count mismatch")
    if case.get("matrix_nonzeros") != sum(len(row.columns) for row in rows):
        raise ValueError("matrix-nonzero mismatch")
    result = farkas_metrics(variable_count, rows, case.get("multipliers"))
    for field in ("support", "max_abs_multiplier", "rhs", "max_box_lhs", "gap"):
        if case.get(field) != result[field]:
            raise ValueError(f"{field} mismatch")
    if result["gap"] <= 0:
        raise ValueError("Farkas certificate has nonpositive gap")
    return result


def verify_prior_uniqueness(
    second,
    group,
    source_path: Path,
    witness_path: Path,
    prior_certificate_path: Path,
):
    witness_blocks = read_blocks(witness_path, 6, set(R))
    profile = verify_extension(second, witness_blocks)
    if tuple(sorted(profile)) != (0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1):
        raise AssertionError("prior witness does not have 20^6,21^6 degrees")
    witness = tuple(sorted(LINK_CANDIDATES.index(block) for block in witness_blocks))
    document = json.loads(prior_certificate_path.read_text(encoding="ascii"))
    if document.get("format") != "C1375-hard-e1-link-farkas-v1":
        raise ValueError("wrong prior certificate format")
    if document.get("source_link_sha256") != sha256(source_path):
        raise ValueError("prior source-link hash mismatch")
    if document.get("witness_sha256") != sha256(witness_path):
        raise ValueError("prior witness hash mismatch")
    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != 12:
        raise ValueError("prior certificate must have twelve cases")
    high_representatives = []
    results = []
    for orbit, case in enumerate(cases):
        if case.get("orbit") != orbit:
            raise ValueError("prior orbit index mismatch")
        high = tuple(case.get("high", ()))
        if len(high) != 6 or tuple(sorted(high)) != high or not set(high) <= set(R):
            raise ValueError("bad prior high-set representative")
        high_representatives.append(high)
        case_profile = tuple(int(p in high) for p in R)
        blocked = bool(case.get("known_blocker"))
        if blocked != (orbit == 11):
            raise ValueError("prior blocker metadata mismatch")
        rows = link_rows(second, case_profile, witness if blocked else None)
        results.append(verify_case(case, 462, rows))
        images = {frozenset(g[p - 2] for p in high) for g in group}
        if case.get("high_orbit_size") != len(images):
            raise ValueError("prior high-set orbit-size mismatch")
    high_set_orbits(group, high_representatives)
    if tuple(p for p, value in zip(R, profile) if value) != high_representatives[11]:
        raise AssertionError("witness does not match the blocked high-set representative")
    return witness_blocks, results


def verify_upper_78():
    v = 13
    line_base = (1, 2, 4, 10)
    cover_bases = (
        (1, 2, 3, 4, 5, 10, 11),
        (1, 2, 3, 4, 6, 10, 12),
        (1, 2, 3, 4, 7, 8, 10),
        (1, 2, 3, 5, 6, 8, 11),
        (1, 2, 3, 5, 7, 11, 12),
        (1, 2, 4, 5, 9, 10, 12),
    )
    translate = lambda block, shift: tuple(sorted(((p - 1 + shift) % v) + 1 for p in block))
    lines = {translate(line_base, shift) for shift in range(v)}
    if len(lines) != 13:
        raise AssertionError("line development failed")
    pair_counts = Counter(pair for line in lines for pair in combinations(line, 2))
    if len(pair_counts) != 78 or set(pair_counts.values()) != {1}:
        raise AssertionError("line orbit is not a projective plane")
    unions = {tuple(sorted(set(a) | set(b))) for a, b in combinations(lines, 2)}
    developed = {translate(base, shift) for base in cover_bases for shift in range(v)}
    if len(unions) != 78 or unions != developed:
        raise AssertionError("78-block construction mismatch")
    sets = tuple(map(frozenset, unions))
    histogram = Counter(sum(frozenset(target) <= block for block in sets) for target in combinations(range(1, 14), 5))
    if histogram != Counter({1: 1170, 4: 117}):
        raise AssertionError(f"unexpected upper-cover histogram {histogram}")
    return histogram


def verify_all(source_path, witness_path, prior_path, certificate_path):
    source = read_source(source_path)
    second = second_link(source)
    group = generated_group(second)
    profiles = profile_orbits(group)
    document = json.loads(certificate_path.read_text(encoding="ascii"))
    if document.get("format") != "C1375-exact-78-farkas-v1":
        raise ValueError("wrong new certificate format")
    if document.get("source_link_sha256") != sha256(source_path):
        raise ValueError("source hash mismatch")
    if document.get("prior_certificate_sha256") != sha256(prior_path):
        raise ValueError("prior certificate hash mismatch")
    if document.get("prior_witness_sha256") != sha256(witness_path):
        raise ValueError("prior witness hash mismatch")

    profile_cases = document.get("profile_cases")
    if not isinstance(profile_cases, list) or len(profile_cases) != 142:
        raise ValueError("new certificate must have 142 profile cases")
    expected_orbits = [i for i in range(143) if i != SURVIVING_PROFILE_ORBIT]
    profile_results = []
    for expected, case in zip(expected_orbits, profile_cases):
        profile, orbit_size = profiles[expected]
        if (
            case.get("orbit") != expected
            or case.get("representative") != list(profile)
            or case.get("orbit_size") != orbit_size
            or case.get("partition") != sorted((x for x in profile if x), reverse=True)
        ):
            raise ValueError(f"profile metadata mismatch at orbit {expected}")
        profile_results.append(verify_case(case, 462, link_rows(second, profile)))

    survivor, survivor_size = profiles[SURVIVING_PROFILE_ORBIT]
    if survivor_size != 2 or tuple(sorted(survivor)) != (0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1):
        raise AssertionError("unexpected surviving profile orbit")
    witness_blocks, prior_results = verify_prior_uniqueness(
        second, group, source_path, witness_path, prior_path
    )
    witness_profile = verify_extension(second, witness_blocks)
    survivor_orbit = {
        tuple(survivor[g[index] - 2] for index in range(11)) for g in group
    }
    if witness_profile not in survivor_orbit:
        raise AssertionError("prior unique extension is outside the surviving profile orbit")
    source_extension = tuple(block for block in source if 1 not in block)
    verify_extension(second, source_extension)
    extensions = {
        frozenset(tuple(sorted(g[p - 2] for p in block)) for block in witness_blocks)
        for g in group
    }
    if extensions != {frozenset(source_extension), frozenset(witness_blocks)} or len(extensions) != 2:
        raise AssertionError("surviving extension orbit does not have the expected two members")
    canonical = (tuple(sorted(source_extension)), tuple(sorted(witness_blocks)))

    completion_cases = document.get("completion_cases")
    if not isinstance(completion_cases, list) or len(completion_cases) != 2:
        raise ValueError("new certificate must have two completion cases")
    completion_results = []
    expected_pairs = ((0, 0), (0, 1))
    residual_counts = []
    for expected_pair, case in zip(expected_pairs, completion_cases):
        if tuple(case.get("pair", ())) != expected_pair:
            raise ValueError("completion-pair metadata mismatch")
        rows, residual = completion_rows(second, canonical[expected_pair[0]], canonical[expected_pair[1]])
        if case.get("residual_five_sets") != residual:
            raise ValueError("residual count mismatch")
        residual_counts.append(residual)
        completion_results.append(verify_case(case, 330, rows))

    upper_histogram = verify_upper_78()
    excluded_labeled = sum(profiles[i][1] for i in expected_orbits)
    if excluded_labeled != 8006:
        raise AssertionError(excluded_labeled)
    return {
        "profiles": profiles,
        "profile_results": profile_results,
        "excluded_labeled": excluded_labeled,
        "survivor": survivor,
        "prior_results": prior_results,
        "extensions": canonical,
        "residual_counts": residual_counts,
        "completion_results": completion_results,
        "upper_histogram": upper_histogram,
        "certificate_hash": sha256(certificate_path),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_link", type=Path)
    parser.add_argument("prior_witness", type=Path)
    parser.add_argument("prior_certificates", type=Path)
    parser.add_argument("certificates", type=Path)
    args = parser.parse_args()
    result = verify_all(
        args.source_link,
        args.prior_witness,
        args.prior_certificates,
        args.certificates,
    )
    print("exact_integer_farkas_check=PASS")
    print("second_link_blocks=20 group_order=240 profile_orbits=143 labeled_profiles=8008")
    print(
        f"profile_exclusions=142 excluded_labeled=8006 "
        f"min_gap={min(row['gap'] for row in result['profile_results'])} "
        f"max_support={max(row['support'] for row in result['profile_results'])}"
    )
    print(
        "surviving_profile=" + ",".join(map(str, result["survivor"]))
        + " orbit_size=2 prior_uniqueness_certificates=PASS extensions=2 stabilizer_order=120"
    )
    print(
        "terminal_e0_cases=same,different residual_five_sets="
        + ",".join(map(str, result["residual_counts"]))
        + " supports=" + ",".join(str(row["support"]) for row in result["completion_results"])
        + " strict_gaps=" + ",".join(str(row["gap"]) for row in result["completion_results"])
    )
    histogram = result["upper_histogram"]
    print("upper_cover_blocks=78 five_set_histogram=" + ",".join(f"{k}:{histogram[k]}" for k in sorted(histogram)))
    print(f"certificate_sha256={result['certificate_hash']}")
    print("conclusion=C(13,7,5)=78")


if __name__ == "__main__":
    main()
