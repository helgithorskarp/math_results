#!/usr/bin/env python3
"""Exact boxed-pattern occurrences by canonical value rectangles.

This is groundwork for decision410, not a growth proof. Returned occurrence
indices are zero based; permutation values are 1,...,n. Python integers and
standard-library enumeration only. No other researcher's module is imported.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import resource
import time
from typing import Iterable


def validate_permutation(values: Iterable[int]) -> tuple[int, ...]:
    p = tuple(values)
    if any(type(x) is not int for x in p):
        raise ValueError("Permutation entries must be integers, excluding bool")
    if sorted(p) != list(range(1, len(p) + 1)):
        raise ValueError("Expected a permutation of 1,...,n")
    return p


def boxed_occurrences(values: Iterable[int], pattern: str = "2143") -> tuple[tuple[int, ...], ...]:
    """Return every occurrence once, ordered lexicographically by indices.

    For each possible pair of vertical rectangle boundaries lo,hi, read the
    points in that value interval in position order. A run of four points is a
    canonical rectangle exactly when its minimum and maximum are lo and hi.
    Check that run's order. This avoids choosing index quadruples and then
    scanning their interiors, the representation used by the other checker.
    """
    p = validate_permutation(values)
    if pattern not in ("2143", "2413"):
        raise ValueError("Only 2143 and the independently sourced 2413 baseline are supported")
    result = []
    for lo in range(1, len(p) - 2):
        for hi in range(lo + 3, len(p) + 1):
            interval = tuple((i, x) for i, x in enumerate(p) if lo <= x <= hi)
            for start in range(len(interval) - 3):
                window = interval[start:start + 4]
                a, b, c, d = (point[1] for point in window)
                if pattern == "2143":
                    matches = b == lo and c == hi and b < a < d < c
                else:
                    matches = c == lo and b == hi and c < a < d < b
                if matches:
                    result.append(tuple(point[0] for point in window))
    result.sort()
    if len(result) != len(set(result)):
        raise RuntimeError("Canonical rectangle produced a duplicate occurrence")
    return tuple(result)


def controls() -> None:
    fixtures = (
        ((2, 1, 4, 3), "2143", ((0, 1, 2, 3),)),
        ((2, 4, 1, 3), "2413", ((0, 1, 2, 3),)),
        ((2, 4, 1, 5, 3), "2143", ()),
        ((1, 3, 2, 5, 4), "2143", ((1, 2, 3, 4),)),
        ((3, 2, 5, 4, 1), "2143", ((0, 1, 2, 3),)),
        ((), "2143", ()),
        ((1, 2, 3), "2143", ()),
    )
    for p, pattern, expected in fixtures:
        actual = boxed_occurrences(p, pattern)
        if actual != expected:
            raise RuntimeError(f"Fixture mismatch: {p}, {pattern}, {actual}, {expected}")
    for malformed in ((1, 1), (0, 1), (1, 3), (True,), (1.0,)):
        try:
            boxed_occurrences(malformed)
        except ValueError:
            pass
        else:
            raise RuntimeError(f"Malformed permutation accepted: {malformed}")
    try:
        boxed_occurrences((1, 2, 3, 4), "1234")
    except ValueError:
        pass
    else:
        raise RuntimeError("Unsupported baseline accepted")


def census(max_n: int) -> dict:
    if not 0 <= max_n <= 8:
        raise ValueError("Groundwork census is intentionally limited to 0 <= n <= 8")
    controls()
    baseline = {
        "2143": (1, 1, 2, 6, 23, 106),
        "2413": (1, 1, 2, 6, 23, 104),
    }
    rows = []
    started = time.perf_counter()
    for n in range(max_n + 1):
        n_started = time.perf_counter()
        hashes = {pattern: hashlib.sha256() for pattern in baseline}
        counts = {pattern: 0 for pattern in baseline}
        tested = 0
        for p in itertools.permutations(range(1, n + 1)):
            tested += 1
            for pattern in baseline:
                occurrences = boxed_occurrences(p, pattern)
                counts[pattern] += not occurrences
                entry = json.dumps([p, occurrences], separators=(",", ":")) + "\n"
                hashes[pattern].update(entry.encode("ascii"))
        if tested != math.factorial(n):
            raise RuntimeError("Incomplete enumeration")
        for pattern, expected in baseline.items():
            if n < len(expected) and counts[pattern] != expected[n]:
                raise RuntimeError(f"Published baseline mismatch at n={n}, {pattern}")
        rows.append({
            "n": n,
            "permutations_tested": tested,
            "avoiders": counts,
            "ordered_occurrence_stream_sha256": {p: h.hexdigest() for p, h in hashes.items()},
            "seconds": time.perf_counter() - n_started,
        })
    return {
        "actor": "literature-researcher-4",
        "decision_message_id": 410,
        "claim_status": "definition-level baseline reproduction and finite observation only",
        "full_target_solved": False,
        "representation": "canonical closed value rectangles / consecutive interval factors",
        "indices": "zero based; stream entries are [permutation, sorted occurrence index tuples]",
        "python": platform.python_version(),
        "external_dependencies": [],
        "rows": rows,
        "seconds": time.perf_counter() - started,
        "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=7)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = census(args.max_n)
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
