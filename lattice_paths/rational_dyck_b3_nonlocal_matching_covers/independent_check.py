#!/usr/bin/env python3
"""Definition-level independent audit of the D(a,3) matching-cover family.

This file deliberately does not import verify.py or use its run matrices.
It generates binary paths, applies the literal adjacency encoding, and uses
a scalar continuant for every matching score.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from itertools import combinations
import hashlib
import json
from math import gcd

Path = tuple[int, ...]  # R=1, U=0


def dyck_paths(a: int):
    for up_positions in combinations(range(a + 3), 3):
        ups = set(up_positions)
        path = tuple(0 if index in ups else 1 for index in range(a + 3))
        rights = up_count = 0
        for step in path:
            rights += step
            up_count += 1 - step
            if a * up_count > 3 * rights:
                break
        else:
            yield path


def continued_fraction_entries(path: Path) -> tuple[int, ...]:
    entries: list[int] = []
    for left, right in zip(path, path[1:]):
        entries.extend((1, 1) if left == right else (2,))
    return tuple(entries)


def continuant(entries: tuple[int, ...]) -> int:
    older, old = 0, 1
    for entry in entries:
        older, old = old, entry * old + older
    return old


def matching_score(path: Path) -> int:
    return continuant(continued_fraction_entries(path))


def from_runs(runs: tuple[int, int, int]) -> Path:
    output: list[int] = []
    for run in runs:
        output.extend((1,) * run)
        output.append(0)
    return tuple(output)


def run_triple(path: Path) -> tuple[int, int, int]:
    runs: list[int] = []
    count = 0
    for step in path:
        if step:
            count += 1
        else:
            runs.append(count)
            count = 0
    if len(runs) != 3 or count:
        raise AssertionError("unexpected height-three path")
    return tuple(runs)  # type: ignore[return-value]


def audit(max_a: int) -> dict[str, int | str]:
    if max_a < 4:
        raise ValueError("max_a must be at least 4")
    digest = hashlib.sha256()
    endpoints = paths_checked = covers = max_distance = 0
    for a in range(4, max_a + 1):
        if gcd(a, 3) != 1:
            continue
        paths = list(dyck_paths(a))
        levels: dict[int, list[Path]] = defaultdict(list)
        parts = set()
        for path in paths:
            levels[matching_score(path)].append(path)
            parts.add(tuple(sorted(run_triple(path), reverse=True)))
        ordered_parts = sorted(parts, key=lambda part: (part[2], -part[0]))
        part_index = {part: index for index, part in enumerate(ordered_parts)}
        values = sorted(levels)
        rank = {score: index for index, score in enumerate(values)}
        m, epsilon = divmod(a, 3)
        for z in range(m):
            n = m - z
            x_runs = (a - 1 - 2 * z, z + 1, z)
            y_runs = (2 * m + epsilon - z, z, m)
            x_path, y_path = from_runs(x_runs), from_runs(y_runs)
            if x_path not in paths or y_path not in paths:
                raise AssertionError((a, z, "candidate absent from carrier"))
            x_score, y_score = matching_score(x_path), matching_score(y_path)
            if rank[y_score] != rank[x_score] + 1:
                raise AssertionError((a, z, "not a definition-level cover"))
            if levels[x_score] != [x_path] or levels[y_score] != [y_path]:
                raise AssertionError((a, z, "definition-level score tie"))
            distance = abs(
                part_index[tuple(sorted(x_runs, reverse=True))]
                - part_index[tuple(sorted(y_runs, reverse=True))]
            )
            if distance != n - 1:
                raise AssertionError((a, z, distance, n - 1))
            record = [a, z, x_score, y_score, distance]
            digest.update(json.dumps(record, separators=(",", ":")).encode() + b"\n")
            covers += 1
            max_distance = max(max_distance, distance)
        endpoints += 1
        paths_checked += len(paths)
    return {
        "endpoints": endpoints,
        "paths": paths_checked,
        "covers": covers,
        "max_fibre_distance": max_distance,
        "row_sha256": digest.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-a", type=int, default=60)
    args = parser.parse_args()
    result = audit(args.max_a)
    fields = "; ".join(f"{key}={value}" for key, value in result.items())
    print(f"INDEPENDENT VERIFIED D(a,3) NONLOCAL MATCHING COVERS; 4<=a<={args.max_a}; {fields}")


if __name__ == "__main__":
    main()
