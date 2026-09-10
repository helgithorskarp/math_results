#!/usr/bin/env python3
"""Independent bit-mask replay of the hard-e1 Farkas certificates.

This checker does not import the generator or the primary checker.  It builds
the covering rows from point-set bit masks, stores each row's candidate support
as one Python integer, and recomputes every certificate inequality exactly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path


R = tuple(range(2, 13))
CANDIDATE_TUPLES = tuple(combinations(R, 6))

HIGH = (
    ((2, 3, 4, 5, 6, 7), 40), ((2, 3, 4, 5, 6, 10), 10),
    ((2, 3, 4, 5, 6, 12), 10), ((2, 3, 4, 5, 7, 8), 30),
    ((2, 3, 4, 5, 7, 10), 20), ((2, 3, 4, 5, 8, 9), 60),
    ((2, 3, 4, 5, 8, 10), 120), ((2, 3, 4, 5, 8, 12), 60),
    ((2, 3, 4, 5, 10, 12), 40), ((2, 3, 4, 8, 10, 11), 60),
    ((2, 3, 4, 8, 11, 12), 10), ((2, 4, 5, 6, 10, 12), 2),
)


def mask(points) -> int:
    value = 0
    for point in points:
        value |= 1 << (point - 1)
    return value


CANDIDATES = tuple(map(mask, CANDIDATE_TUPLES))
CANDIDATE_INDEX = {value: index for index, value in enumerate(CANDIDATES)}


def is_subset(small: int, large: int) -> bool:
    return small & large == small


def read_masks(path: Path, size: int, allowed: set[int]) -> list[int]:
    result = []
    for raw in path.read_text(encoding="ascii").splitlines():
        text = raw.split("#", 1)[0].strip()
        if not text:
            continue
        points = tuple(map(int, text.split()))
        if len(points) != size or len(set(points)) != size or not set(points) <= allowed:
            raise ValueError(f"bad row in {path}: {text}")
        result.append(mask(points))
    if len(result) != len(set(result)):
        raise ValueError(f"duplicate rows in {path}")
    return result


def support(predicate) -> int:
    value = 0
    for index, candidate in enumerate(CANDIDATES):
        if predicate(candidate):
            value |= 1 << index
    return value


def rows(second: list[int], high_tuple: tuple[int, ...], blocker: list[int] | None):
    fixed = [(1 << 0) | block for block in second]
    result: list[tuple[int, int | None, int | None]] = []
    residual = []
    for target_tuple in combinations(R, 4):
        target = mask(target_tuple)
        if any(is_subset(target, block) for block in second):
            continue
        residual.append(target)
        result.append((support(lambda block, target=target: is_subset(target, block)), 1, None))
    if len(residual) != 230:
        raise AssertionError(len(residual))
    result.append(((1 << len(CANDIDATES)) - 1, 21, 21))
    second_degrees = Counter()
    for block in second:
        for point in R:
            second_degrees[point] += bool(block & (1 << (point - 1)))
    high = set(high_tuple)
    for point in R:
        bit = 1 << (point - 1)
        target = 20 + (point in high) - second_degrees[point]
        result.append((support(lambda block, bit=bit: bool(block & bit)), target, target))
    for size, lower in ((2, 9), (3, 3)):
        for subset_tuple in combinations(range(1, 13), size):
            subset = mask(subset_tuple)
            fixed_count = sum(is_subset(subset, block) for block in fixed)
            need = lower - fixed_count
            if need > 0:
                row_support = support(lambda block, subset=subset: is_subset(subset, block))
                if not row_support:
                    raise AssertionError((subset_tuple, need))
                result.append((row_support, need, None))
    if blocker is not None:
        blocker_support = sum(1 << index for index in blocker)
        result.append((blocker_support, None, 20))
    if len(result) != (458 if blocker is not None else 457):
        raise AssertionError(len(result))
    return result


def metrics(matrix, sparse):
    multipliers = [0] * len(matrix)
    last = -1
    for index, value in sparse:
        if not isinstance(index, int) or not isinstance(value, int) or not value:
            raise ValueError("bad sparse multiplier")
        if index <= last or index >= len(matrix):
            raise ValueError("bad sparse multiplier order")
        multipliers[index] = value
        last = index
    coefficients = [0] * len(CANDIDATES)
    rhs = 0
    for multiplier, (row_support, lower, upper) in zip(multipliers, matrix):
        if multiplier > 0:
            if lower is None:
                raise ValueError("positive multiplier on upper-only row")
            rhs += multiplier * lower
        elif multiplier < 0:
            if upper is None:
                raise ValueError("negative multiplier on lower-only row")
            rhs += multiplier * upper
        bits = row_support
        while bits:
            least = bits & -bits
            column = least.bit_length() - 1
            coefficients[column] += multiplier
            bits -= least
    maximum = sum(value for value in coefficients if value > 0)
    return (sum(value != 0 for value in multipliers), max(map(abs, multipliers)), rhs, maximum, rhs - maximum)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_link", type=Path)
    parser.add_argument("witness", type=Path)
    parser.add_argument("certificates", type=Path)
    args = parser.parse_args()

    source = read_masks(args.source_link, 6, set(range(1, 13)))
    if len(source) != 41:
        raise ValueError("source size")
    targets = tuple(map(mask, combinations(range(1, 13), 4)))
    if not all(any(is_subset(target, block) for block in source) for target in targets):
        raise ValueError("source is not a cover")
    second = [block & ~(1 << 0) for block in source if block & 1]
    if len(second) != 20:
        raise ValueError("second-link size")
    if not all(
        any(is_subset(mask(target), block) for block in second)
        for target in combinations(R, 3)
    ):
        raise ValueError("second link is not a triple cover")
    witness_masks = read_masks(args.witness, 6, set(R))
    witness = sorted(CANDIDATE_INDEX[block] for block in witness_masks)
    if len(witness) != 21:
        raise ValueError("witness size")
    full = [(1 << 0) | block for block in second] + witness_masks
    if not all(any(is_subset(target, block) for block in full) for target in targets):
        raise ValueError("witness is not a quadruple cover")
    degrees = Counter()
    for block in full:
        for point in range(1, 13):
            degrees[point] += bool(block & (1 << (point - 1)))
    if Counter(degrees.values()) != Counter({20: 6, 21: 6}):
        raise ValueError("witness degree profile")

    document = json.loads(args.certificates.read_text(encoding="ascii"))
    cases = document["cases"]
    outputs = []
    for orbit, case in enumerate(cases):
        if case["high"] != list(HIGH[orbit][0]) or case["high_orbit_size"] != HIGH[orbit][1]:
            raise ValueError("orbit metadata")
        matrix = rows(second, HIGH[orbit][0], witness if orbit == 11 else None)
        actual = metrics(matrix, case["multipliers"])
        expected = tuple(
            case[field]
            for field in ("support", "max_abs_multiplier", "rhs", "max_box_lhs", "gap")
        )
        if actual != expected or actual[-1] <= 0:
            raise ValueError((orbit, actual, expected))
        if sum(value.bit_count() for value, _, _ in matrix) != case["matrix_nonzeros"]:
            raise ValueError("matrix nonzero count")
        outputs.append(actual)

    digest = hashlib.sha256(args.certificates.read_bytes()).hexdigest()
    print("independent_bitmask_farkas_check=PASS")
    print("source_cover=PASS second_link=PASS orbit11_witness=PASS")
    print("cases=12 strict_integer_contradictions=12 min_gap=" + str(min(row[-1] for row in outputs)))
    print("supports=" + ",".join(str(row[0]) for row in outputs))
    print("certificate_sha256=" + digest)


if __name__ == "__main__":
    main()
