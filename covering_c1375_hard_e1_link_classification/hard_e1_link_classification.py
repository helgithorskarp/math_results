#!/usr/bin/env python3
"""Exact checker for the hard-e1 optimal-link classification.

The floating-point LP solver is used only to discover multiplier vectors.
This checker uses Python integers to verify the published Farkas inequalities
directly, including the variable-box contribution.  It has no solver or
third-party dependency.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Sequence


POINTS = tuple(range(2, 13))
CANDIDATES = tuple(combinations(POINTS, 6))
CANDIDATE_INDEX = {block: index for index, block in enumerate(CANDIDATES)}
HIGH_ORBITS = (
    ((2, 3, 4, 5, 6, 7), 40),
    ((2, 3, 4, 5, 6, 10), 10),
    ((2, 3, 4, 5, 6, 12), 10),
    ((2, 3, 4, 5, 7, 8), 30),
    ((2, 3, 4, 5, 7, 10), 20),
    ((2, 3, 4, 5, 8, 9), 60),
    ((2, 3, 4, 5, 8, 10), 120),
    ((2, 3, 4, 5, 8, 12), 60),
    ((2, 3, 4, 5, 10, 12), 40),
    ((2, 3, 4, 8, 10, 11), 60),
    ((2, 3, 4, 8, 11, 12), 10),
    ((2, 4, 5, 6, 10, 12), 2),
)
SOURCE_TO_WITNESS = {
    1: 1,
    2: 3,
    3: 2,
    4: 7,
    5: 8,
    6: 9,
    7: 5,
    8: 6,
    9: 4,
    10: 10,
    11: 12,
    12: 11,
}


@dataclass(frozen=True)
class Row:
    columns: tuple[int, ...]
    lower: int | None
    upper: int | None
    label: str


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_blocks(path: Path, size: int, allowed: set[int]) -> list[tuple[int, ...]]:
    blocks: list[tuple[int, ...]] = []
    for raw in path.read_text(encoding="ascii").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            block = tuple(sorted(map(int, line.split())))
            if len(block) != size or len(set(block)) != size or not set(block) <= allowed:
                raise ValueError(f"invalid block in {path}: {line}")
            blocks.append(block)
    if len(blocks) != len(set(blocks)):
        raise ValueError(f"duplicate block in {path}")
    return blocks


def read_source(path: Path) -> list[tuple[int, ...]]:
    blocks = read_blocks(path, 6, set(range(1, 13)))
    if len(blocks) != 41:
        raise ValueError("source must contain 41 blocks")
    block_sets = tuple(map(frozenset, blocks))
    for target in combinations(range(1, 13), 4):
        if not any(frozenset(target) <= block for block in block_sets):
            raise ValueError(f"source misses quadruple {target}")
    if sum(1 in block for block in blocks) != 20:
        raise ValueError("source point 1 must have degree 20")
    return blocks


def second_link(source: Sequence[tuple[int, ...]]) -> list[tuple[int, ...]]:
    blocks = [tuple(point for point in block if point != 1) for block in source if 1 in block]
    if len(blocks) != 20 or len(set(blocks)) != 20:
        raise AssertionError("invalid second-link size")
    block_sets = tuple(map(frozenset, blocks))
    for target in combinations(POINTS, 3):
        if not any(frozenset(target) <= block for block in block_sets):
            raise AssertionError(f"second link misses triple {target}")
    return blocks


def read_witness(path: Path) -> tuple[int, ...]:
    blocks = read_blocks(path, 6, set(POINTS))
    if len(blocks) != 21:
        raise ValueError("witness must contain 21 blocks")
    return tuple(sorted(CANDIDATE_INDEX[block] for block in blocks))


def verify_witness(
    source: Sequence[tuple[int, ...]],
    second: Sequence[tuple[int, ...]],
    witness: tuple[int, ...],
) -> None:
    variable = [CANDIDATES[index] for index in witness]
    full = [(1, *block) for block in second] + variable
    if len(full) != 41 or len(set(full)) != 41:
        raise AssertionError("invalid full witness size")
    full_sets = tuple(map(frozenset, full))
    for target in combinations(range(1, 13), 4):
        if not any(frozenset(target) <= block for block in full_sets):
            raise AssertionError(f"witness misses quadruple {target}")
    degrees = Counter(point for block in full for point in block)
    high = tuple(point for point in POINTS if degrees[point] == 21)
    if degrees[1] != 20 or high != HIGH_ORBITS[11][0]:
        raise AssertionError(("witness degrees", degrees, high))
    if Counter(degrees.values()) != Counter({20: 6, 21: 6}):
        raise AssertionError(Counter(degrees.values()))
    mapped_source = {
        tuple(sorted(SOURCE_TO_WITNESS[point] for point in block)) for block in source
    }
    if mapped_source != set(full):
        raise AssertionError("witness is not the recorded source-cover image")


def build_rows(
    second: Sequence[tuple[int, ...]],
    high_tuple: tuple[int, ...],
    blocker: tuple[int, ...] | None,
) -> list[Row]:
    high = set(high_tuple)
    fixed_small = tuple(map(frozenset, second))
    fixed = tuple(frozenset((1, *block)) for block in second)
    candidate_sets = tuple(map(frozenset, CANDIDATES))
    rows: list[Row] = []
    residual = []
    for target in combinations(POINTS, 4):
        target_set = frozenset(target)
        if any(target_set <= block for block in fixed_small):
            continue
        residual.append(target)
        columns = tuple(
            index for index, block in enumerate(candidate_sets) if target_set <= block
        )
        rows.append(Row(columns, 1, None, "quadruple:" + "-".join(map(str, target))))
    if len(residual) != 230:
        raise AssertionError(len(residual))
    rows.append(Row(tuple(range(len(CANDIDATES))), 21, 21, "count"))

    degree = Counter(point for block in second for point in block)
    for point in POINTS:
        columns = tuple(
            index for index, block in enumerate(candidate_sets) if point in block
        )
        target = 20 + int(point in high) - degree[point]
        rows.append(Row(columns, target, target, f"degree:{point}"))

    for size, lower in ((2, 9), (3, 3)):
        for subset in combinations(range(1, 13), size):
            subset_set = frozenset(subset)
            fixed_count = sum(subset_set <= block for block in fixed)
            need = lower - fixed_count
            columns = tuple(
                index for index, block in enumerate(candidate_sets) if subset_set <= block
            )
            if need > 0:
                if not columns:
                    raise AssertionError((subset, fixed_count, need))
                rows.append(
                    Row(
                        columns,
                        need,
                        None,
                        f"shadow{size}:" + "-".join(map(str, subset)),
                    )
                )
            elif 1 in subset and columns:
                raise AssertionError("candidate unexpectedly contains point 1")

    if blocker is not None:
        if len(blocker) != 21 or len(set(blocker)) != 21:
            raise AssertionError("invalid known-witness blocker")
        rows.append(Row(blocker, None, 20, "known-witness-overlap<=20"))
    expected = 458 if blocker is not None else 457
    if len(rows) != expected:
        raise AssertionError((len(rows), expected))
    return rows


def farkas_metrics(
    rows: Sequence[Row], sparse_multipliers: Sequence[Sequence[int]]
) -> dict[str, int]:
    multipliers = [0] * len(rows)
    prior = -1
    for pair in sparse_multipliers:
        if len(pair) != 2:
            raise ValueError("each multiplier entry must be [row, value]")
        row_index, value = pair
        if not isinstance(row_index, int) or not isinstance(value, int) or not value:
            raise ValueError("multiplier indices and nonzero values must be integers")
        if not prior < row_index < len(rows):
            raise ValueError("multiplier row indices must be strictly increasing")
        multipliers[row_index] = value
        prior = row_index

    coefficients = [0] * len(CANDIDATES)
    right_hand_side = 0
    for multiplier, row in zip(multipliers, rows):
        if multiplier > 0:
            if row.lower is None:
                raise ValueError(f"positive multiplier has no lower bound: {row.label}")
            right_hand_side += multiplier * row.lower
        elif multiplier < 0:
            if row.upper is None:
                raise ValueError(f"negative multiplier has no upper bound: {row.label}")
            right_hand_side += multiplier * row.upper
        for column in row.columns:
            coefficients[column] += multiplier

    # Every variable lies in [0,1], so this is the exact maximum of c*x.
    maximum_box_lhs = sum(max(coefficient, 0) for coefficient in coefficients)
    gap = right_hand_side - maximum_box_lhs
    return {
        "support": sum(multiplier != 0 for multiplier in multipliers),
        "max_abs_multiplier": max(map(abs, multipliers), default=0),
        "rhs": right_hand_side,
        "max_box_lhs": maximum_box_lhs,
        "gap": gap,
    }


def verify_certificates(
    second: Sequence[tuple[int, ...]],
    witness: tuple[int, ...],
    certificate_path: Path,
) -> tuple[list[dict[str, int]], str]:
    document = json.loads(certificate_path.read_text(encoding="ascii"))
    if document.get("format") != "C1375-hard-e1-link-farkas-v1":
        raise ValueError("wrong certificate format")
    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != 12:
        raise ValueError("certificate must contain twelve cases")
    results: list[dict[str, int]] = []
    for orbit, case in enumerate(cases):
        high, orbit_size = HIGH_ORBITS[orbit]
        blocked = orbit == 11
        if (
            case.get("orbit") != orbit
            or case.get("high") != list(high)
            or case.get("high_orbit_size") != orbit_size
            or case.get("known_blocker") is not blocked
        ):
            raise ValueError(f"case metadata mismatch at orbit {orbit}")
        rows = build_rows(second, high, witness if blocked else None)
        if case.get("row_count") != len(rows):
            raise ValueError(f"row count mismatch at orbit {orbit}")
        if case.get("matrix_nonzeros") != sum(len(row.columns) for row in rows):
            raise ValueError(f"matrix size mismatch at orbit {orbit}")
        metrics = farkas_metrics(rows, case.get("multipliers", []))
        for field in ("support", "max_abs_multiplier", "rhs", "max_box_lhs", "gap"):
            if case.get(field) != metrics[field]:
                raise ValueError(f"{field} mismatch at orbit {orbit}")
        if metrics["gap"] <= 0:
            raise ValueError(f"nonpositive Farkas gap at orbit {orbit}")
        results.append(metrics)
    return results, sha256(certificate_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_link", type=Path)
    parser.add_argument("witness", type=Path)
    parser.add_argument("certificates", type=Path)
    args = parser.parse_args()

    source = read_source(args.source_link)
    second = second_link(source)
    witness = read_witness(args.witness)
    verify_witness(source, second, witness)
    metrics, certificate_hash = verify_certificates(second, witness, args.certificates)
    if sum(size for _, size in HIGH_ORBITS) != math.comb(11, 6):
        raise AssertionError("high-set orbit sizes do not cover the domain")

    print("exact_integer_farkas_check=PASS")
    print(
        "source_blocks=41 second_link_blocks=20 residual_quadruples=230 "
        "variables=462"
    )
    print("high_set_orbits=12 orbit_size_sum=462")
    print(
        "orbit11_witness=PASS variable_blocks=21 full_blocks=41 "
        "degree_profile=20^6,21^6 source_isomorphism=PASS"
    )
    print(
        "farkas_cases=12 empty_high_orbits=11 blocked_orbit11_alternatives=1 "
        "supports=" + ",".join(str(row["support"]) for row in metrics)
    )
    print("strict_gaps=" + ",".join(str(row["gap"]) for row in metrics))
    print(f"certificate_sha256={certificate_hash}")
    print("classification=hard-e1 optimal root link is unique up to isomorphism")


if __name__ == "__main__":
    main()
