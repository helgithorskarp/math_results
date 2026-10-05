#!/usr/bin/env python3
"""Finite controls for the written structural reductions; not a growth proof."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import time

from rectangle_checker import boxed_occurrences, validate_permutation


def standardize(values: tuple[int, ...]) -> tuple[int, ...]:
    ranks = {x: i + 1 for i, x in enumerate(sorted(values))}
    return tuple(ranks[x] for x in values)


def skew_components(values: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    p = validate_permutation(values)
    pieces = []
    start = 0
    prefix_min = len(p) + 1
    for i, x in enumerate(p):
        prefix_min = min(prefix_min, x)
        if prefix_min == len(p) - i:
            pieces.append(standardize(p[start:i + 1]))
            start = i + 1
    if start != len(p):
        raise RuntimeError("Skew decomposition omitted entries")
    return tuple(pieces)


def inflate_increasing(values: tuple[int, ...], sizes: tuple[int, ...]) -> tuple[int, ...]:
    p = validate_permutation(values)
    if len(sizes) != len(p) or any(type(s) is not int or s <= 0 for s in sizes):
        raise ValueError("Inflation needs one positive integer size per entry")
    size_by_value = {x: sizes[i] for i, x in enumerate(p)}
    first_by_value = {}
    next_value = 1
    for x in range(1, len(p) + 1):
        first_by_value[x] = next_value
        next_value += size_by_value[x]
    return tuple(y for x in p for y in range(first_by_value[x], first_by_value[x] + size_by_value[x]))


def forced_lifts(occurrences: tuple[tuple[int, ...], ...], sizes: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    offsets = []
    pos = 0
    for size in sizes:
        offsets.append(pos)
        pos += size
    return tuple(sorted(
        (offsets[a] + sizes[a] - 1, offsets[b] + sizes[b] - 1, offsets[c], offsets[d])
        for a, b, c, d in occurrences
    ))


def run(max_n: int, inflation_max_n: int) -> dict:
    if not 0 <= max_n <= 8 or not 0 <= inflation_max_n <= 5:
        raise ValueError("Finite controls capped at n=8 and inflation base n=5")
    started = time.perf_counter()
    a = []
    b = [0]
    component_comparisons = 0
    stream = hashlib.sha256()
    for n in range(max_n + 1):
        avoiders = indecomposable_avoiders = 0
        for p in itertools.permutations(range(1, n + 1)):
            actual = boxed_occurrences(p)
            components = skew_components(p)
            expected = []
            offset = 0
            for c in components:
                expected.extend(tuple(i + offset for i in occ) for occ in boxed_occurrences(c))
                offset += len(c)
            if tuple(sorted(expected)) != actual:
                raise RuntimeError(f"Component occurrence mismatch for {p}")
            component_comparisons += 1
            avoiders += not actual
            indecomposable_avoiders += not actual and len(components) == 1
            stream.update((json.dumps([p, components, actual], separators=(",", ":")) + "\n").encode())
        a.append(avoiders)
        if n:
            b.append(indecomposable_avoiders)
            if sum(b[k] * a[n-k] for k in range(1, n+1)) != a[n]:
                raise RuntimeError(f"Skew counting identity mismatch at {n}")
    inflation_comparisons = 0
    inflation_hash = hashlib.sha256()
    for n in range(inflation_max_n + 1):
        for p in itertools.permutations(range(1, n+1)):
            occurrences = boxed_occurrences(p)
            for sizes in itertools.product((1, 2), repeat=n):
                inflated = inflate_increasing(p, sizes)
                actual = boxed_occurrences(inflated)
                expected = forced_lifts(occurrences, sizes)
                if actual != expected:
                    raise RuntimeError(f"Inflation occurrence mismatch for {p}, {sizes}")
                inflation_comparisons += 1
                inflation_hash.update((json.dumps([p, sizes, actual], separators=(",", ":")) + "\n").encode())
    fixture = (2, 1, 4, 3)
    sizes = (1, 2, 3, 4)
    if boxed_occurrences(inflate_increasing(fixture, sizes)) != forced_lifts(boxed_occurrences(fixture), sizes):
        raise RuntimeError("Unequal-size inflation fixture failed")
    try:
        inflate_increasing((1, 2), (1, 0))
    except ValueError:
        pass
    else:
        raise RuntimeError("Nonpositive inflation accepted")
    # Extending the claim to arbitrary block orientations is false.
    if boxed_occurrences((1, 2)) or not boxed_occurrences((2, 1, 4, 3)):
        raise RuntimeError("Decreasing-block negative control failed")
    return {
        "actor": "literature-researcher-4",
        "decision_message_id": 410,
        "claim_status": "finite controls for written lemmas awaiting independent check",
        "full_target_solved": False,
        "python": platform.python_version(),
        "skew_scope_max_n": max_n,
        "component_occurrence_comparisons": component_comparisons,
        "a_n": a,
        "b_n_with_b0_zero": b,
        "component_stream_sha256": stream.hexdigest(),
        "inflation_scope_max_base_n": inflation_max_n,
        "inflation_sizes": [1, 2],
        "inflation_occurrence_comparisons": inflation_comparisons,
        "inflation_stream_sha256": inflation_hash.hexdigest(),
        "unequal_size_fixture": {"permutation": fixture, "sizes": sizes},
        "seconds": time.perf_counter() - started,
        "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=7)
    parser.add_argument("--inflation-max-n", type=int, default=5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.max_n, args.inflation_max_n)
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
