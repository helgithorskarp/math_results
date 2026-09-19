#!/usr/bin/env python3
"""Exact run-matrix audit for nonlocal matching covers in D(a,3).

The universal proof is in PROOF.md.  This program checks the closed score-gap
identity and every singleton-cover assertion on the reduced partition/run
carrier over a configurable finite range.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from math import gcd

Run = tuple[int, int, int]
Matrix = tuple[tuple[int, int], tuple[int, int]]


def fibonacci(index: int) -> int:
    if index == -1:
        return 1
    if index < -1:
        raise ValueError("Fibonacci index must be at least -1")
    older, old = 0, 1
    for _ in range(index):
        older, old = old, older + old
    return older


def lucas(index: int) -> int:
    if index < 0:
        raise ValueError("Lucas index must be nonnegative")
    older, old = 2, 1
    for _ in range(index):
        older, old = old, older + old
    return older


def multiply(left: Matrix, right: Matrix) -> Matrix:
    return (
        (
            left[0][0] * right[0][0] + left[0][1] * right[1][0],
            left[0][0] * right[0][1] + left[0][1] * right[1][1],
        ),
        (
            left[1][0] * right[0][0] + left[1][1] * right[1][0],
            left[1][0] * right[0][1] + left[1][1] * right[1][1],
        ),
    )


def k_matrix(run: int) -> Matrix:
    if run < 0:
        raise ValueError("run length must be nonnegative")
    return (
        (fibonacci(2 * run + 3), fibonacci(2 * run + 1)),
        (fibonacci(2 * run + 1), fibonacci(2 * run - 1)),
    )


def matching_score(runs: Run) -> int:
    product = multiply(multiply(k_matrix(runs[0]), k_matrix(runs[1])), k_matrix(runs[2]))
    return product[1][0]


def partitions(a: int) -> list[Run]:
    output = []
    for z in range(a // 3 + 1):
        for y in range(z, (a - z) // 2 + 1):
            output.append((a - y - z, y, z))
    return output


def valid_runs(part: Run, a: int) -> tuple[Run, ...]:
    x, y, z = part
    h = a - 3 * y
    if h == 0 or gcd(a, 3) != 1:
        raise ValueError("requires a coprime height-three endpoint")
    candidates = (part, (x, z, y) if h > 0 else (y, x, z))
    return tuple(dict.fromkeys(candidates))


def candidate_pair(a: int, z: int) -> tuple[Run, Run, int, int, int]:
    m, epsilon = divmod(a, 3)
    if epsilon not in (1, 2) or not 0 <= z <= m - 1:
        raise ValueError("not a family parameter")
    n = m - z
    x_path = (a - 1 - 2 * z, z + 1, z)
    y_path = (2 * m + epsilon - z, z, m)
    return x_path, y_path, m, epsilon, n


def gap_formula(z: int, epsilon: int, n: int) -> int:
    five_gap = (
        2
        * fibonacci(2 * z + 1)
        * (4 * lucas(6 * n + 2 * epsilon - 5) + 3 * lucas(2 * n + 2 * epsilon - 2))
        + 10 * fibonacci(2 * z) * fibonacci(6 * n + 2 * epsilon - 4)
    )
    quotient, remainder = divmod(five_gap, 5)
    if remainder:
        raise AssertionError("closed gap numerator is not divisible by five")
    return quotient


def audit(max_a: int) -> dict[str, int | str]:
    if max_a < 4:
        raise ValueError("max_a must be at least 4")
    digest = hashlib.sha256()
    endpoints = paths = covers = max_distance = 0
    for a in range(4, max_a + 1):
        if gcd(a, 3) != 1:
            continue
        rows: list[tuple[int, Run, Run, int]] = []
        part_index: dict[Run, int] = {}
        for index, part in enumerate(partitions(a)):
            part_index[part] = index
            for run in valid_runs(part, a):
                rows.append((matching_score(run), part, run, index))
        levels: dict[int, list[tuple[Run, Run, int]]] = defaultdict(list)
        for score, part, run, index in rows:
            levels[score].append((part, run, index))
        values = sorted(levels)
        rank = {score: index for index, score in enumerate(values)}
        m = a // 3
        for z in range(m):
            x_path, y_path, _, epsilon, n = candidate_pair(a, z)
            x_score, y_score = matching_score(x_path), matching_score(y_path)
            formula = gap_formula(z, epsilon, n)
            if y_score - x_score != formula or formula <= 0:
                raise AssertionError((a, z, x_score, y_score, formula))
            if rank[y_score] != rank[x_score] + 1:
                raise AssertionError((a, z, "not adjacent matching levels"))
            if len(levels[x_score]) != 1 or len(levels[y_score]) != 1:
                raise AssertionError((a, z, "endpoint level is not a singleton"))
            x_part = tuple(sorted(x_path, reverse=True))
            y_part = tuple(sorted(y_path, reverse=True))
            distance = abs(part_index[x_part] - part_index[y_part])
            if distance != n - 1:
                raise AssertionError((a, z, distance, n - 1))
            record = [a, z, epsilon, n, list(x_path), list(y_path), x_score, y_score, formula, distance]
            digest.update(json.dumps(record, separators=(",", ":")).encode() + b"\n")
            covers += 1
            max_distance = max(max_distance, distance)
        endpoints += 1
        paths += len(rows)
    return {
        "endpoints": endpoints,
        "paths": paths,
        "covers": covers,
        "max_fibre_distance": max_distance,
        "row_sha256": digest.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-a", type=int, default=180)
    args = parser.parse_args()
    result = audit(args.max_a)
    fields = "; ".join(f"{key}={value}" for key, value in result.items())
    print(f"EXACT VERIFIED D(a,3) NONLOCAL MATCHING COVERS; 4<=a<={args.max_a}; {fields}")


if __name__ == "__main__":
    main()
