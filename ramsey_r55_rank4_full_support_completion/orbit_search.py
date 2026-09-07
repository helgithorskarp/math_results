#!/usr/bin/env python3
"""Enumerate GL(4,2) orbits of a broad retained cut stratum and solve them.

Rows contain every nonzero F_2^4 label once and five labels twice. Columns
contain every nonzero label once and eight labels twice. Column-double affine
hyperplanes are omitted because the complete corresponding family is already
excluded. Vertex permutations within each side and dual GL factor changes
preserve physical completion, so one representative per orbit is complete for
this stratum.
"""

from __future__ import annotations

import argparse
from collections import deque
from itertools import combinations
import json
from pathlib import Path
import subprocess
import tempfile
import time

import probe


def linear_map(images: tuple[int, int, int, int], x: int) -> int:
    value = 0
    for i, image in enumerate(images):
        if (x >> i) & 1:
            value ^= image
    return value


def dual_images(images: tuple[int, int, int, int]) -> tuple[int, ...]:
    dual = []
    for y in (1, 2, 4, 8):
        matches = [z for z in range(16)
                   if all(probe.dot(linear_map(images, 1 << i), z) ==
                          probe.dot(1 << i, y) for i in range(4))]
        if len(matches) != 1:
            raise RuntimeError("noninvertible generator")
        dual.append(matches[0])
    return tuple(dual)


def generators() -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    result = []
    for i in range(3):
        basis = [1, 2, 4, 8]
        basis[i], basis[i + 1] = basis[i + 1], basis[i]
        row = tuple(basis)
        result.append((row, dual_images(row)))
    row = (3, 2, 4, 8)
    result.append((row, dual_images(row)))
    return result


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(linear_map(left, linear_map(right, 1 << i)) for i in range(4))


def generated_group_size(gens) -> int:
    identity = (1, 2, 4, 8)
    seen = {identity}
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for row, _ in gens:
            nxt = compose(row, current)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return len(seen)


def subset_mask(values) -> int:
    return sum(1 << (x - 1) for x in values)


def mask_values(mask: int) -> tuple[int, ...]:
    return tuple(x for x in range(1, 16) if (mask >> (x - 1)) & 1)


def mask_action_table(images: tuple[int, ...]) -> list[int]:
    label_image = [linear_map(images, x) for x in range(16)]
    table = [0] * (1 << 15)
    for mask in range(1, 1 << 15):
        bit = mask & -mask
        label = bit.bit_length()
        table[mask] = table[mask ^ bit] | (1 << (label_image[label] - 1))
    return table


def orbit_representatives() -> tuple[list[tuple[tuple[int, ...], tuple[int, ...]]], dict]:
    gens = generators()
    group_size = generated_group_size(gens)
    if group_size != 20160:
        raise RuntimeError(f"generators span {group_size}, expected 20160")
    rows = [subset_mask(c) for c in combinations(range(1, 16), 5)]
    columns = [subset_mask(c) for c in combinations(range(1, 16), 8)
               if not probe.affine_hyperplane(set(c))]
    row_index = {mask: i for i, mask in enumerate(rows)}
    column_index = {mask: i for i, mask in enumerate(columns)}
    tables = [(mask_action_table(row), mask_action_table(column))
              for row, column in gens]
    width = len(columns)
    visited = bytearray(len(rows) * width)
    representatives = []
    orbit_sizes = []
    for ri, row_mask in enumerate(rows):
        base = ri * width
        for ci, column_mask in enumerate(columns):
            key = base + ci
            if visited[key]:
                continue
            visited[key] = 1
            queue = deque([(row_mask, column_mask)])
            size = 0
            while queue:
                rm, cm = queue.popleft()
                size += 1
                for row_table, column_table in tables:
                    nr = row_table[rm]
                    nc = column_table[cm]
                    nk = row_index[nr] * width + column_index[nc]
                    if not visited[nk]:
                        visited[nk] = 1
                        queue.append((nr, nc))
            representatives.append((mask_values(row_mask), mask_values(column_mask)))
            orbit_sizes.append(size)
    if sum(orbit_sizes) != len(rows) * len(columns):
        raise RuntimeError("orbit partition does not cover the complete stratum")
    return representatives, {
        "gl4_size": group_size,
        "row_sets": len(rows),
        "column_sets_nonaffine": len(columns),
        "pairs": len(rows) * len(columns),
        "orbits": len(representatives),
        "orbit_size_min": min(orbit_sizes),
        "orbit_size_max": max(orbit_sizes),
        "orbit_size_sum": sum(orbit_sizes),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", required=True)
    parser.add_argument("--seconds", type=int, default=10)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--limit", type=int, default=16)
    parser.add_argument("--stride", type=int, default=1)
    parser.add_argument("--progress-every", type=int, default=1)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--scratch", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    reps, census = orbit_representatives()
    enumeration_seconds = time.monotonic() - started
    if not 0 <= args.start < len(reps) or not 1 <= args.limit <= len(reps):
        raise ValueError("invalid orbit schedule")
    indices = []
    seen = set()
    index = args.start
    for _ in range(args.limit):
        if index in seen:
            raise ValueError("stride repeats before requested limit")
        seen.add(index)
        indices.append(index)
        index = (index + args.stride) % len(reps)
    results = []
    with tempfile.TemporaryDirectory(dir=args.scratch) as tmp:
        for position, index in enumerate(indices, 1):
            row, column = reps[index]
            result = probe.solve_one(args.solver, args.seconds, row, column, Path(tmp))
            result["orbit_index"] = index
            results.append(result)
            if position % args.progress_every == 0 or result["status"] != "UNSAT":
                progress = {"position": position, "result": result}
                print(json.dumps(progress, sort_keys=True), flush=True)
            if result["status"] == "SAT_GOOD43":
                break
    payload = {
        "schema": "rank4-full-support-orbit-search-v1",
        "census": census,
        "enumeration_seconds": enumeration_seconds,
        "schedule": {"start": args.start, "stride": args.stride,
                     "limit": args.limit, "indices": indices},
        "seconds_per_instance": args.seconds,
        "solver": subprocess.run([args.solver, "--version"], capture_output=True,
                                 text=True, check=True).stdout.strip(),
        "results": results,
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print(json.dumps({"census": census, "tested": len(results)}, sort_keys=True))


if __name__ == "__main__":
    main()
