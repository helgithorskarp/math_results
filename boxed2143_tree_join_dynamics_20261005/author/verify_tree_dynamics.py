#!/usr/bin/env python3
"""Falsify tree-state claims with all small permutations and exact fibers."""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import platform
from time import perf_counter

from kernel import blockers, insert_maximum, legal_maximum_gaps
from tree_dynamics import (cartesian_shape, clear_caches,
                           insert_maximum_shape, shape_blockers,
                           shape_legal_gaps, tree_word)
from verify_kernel import direct_occurrences


def require(condition, description):
    if not condition:
        raise RuntimeError(description)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=7)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    require(0 <= args.max_n <= 8, "explicit bounded replay scope is 0..8")
    start = perf_counter()
    checked = 0
    transitions = 0
    records = []
    digest = sha256()
    for n in range(args.max_n + 1):
        fibers = defaultdict(lambda: [0, 0])
        for p in permutations(range(1, n + 1)):
            tree = cartesian_shape(p)
            expected = blockers(p)
            actual = shape_blockers(tree)
            require(actual == expected, f"blocker shape disagreement {p}")
            gaps = shape_legal_gaps(tree)
            require(gaps == legal_maximum_gaps(p), f"gap disagreement {p}")
            avoiding = not direct_occurrences(p)
            fibers[tree][0] += 1
            fibers[tree][1] += int(avoiding)
            for gap in range(n + 1):
                require(insert_maximum_shape(tree, gap) ==
                        cartesian_shape(insert_maximum(p, gap)),
                        f"split update disagreement {p} gap {gap}")
                transitions += 1
            digest.update(json.dumps([p, tree_word(tree), gaps, avoiding],
                                     separators=(",", ":")).encode())
            digest.update(b"\n")
            checked += 1
        records.append({
            "n": n, "permutations": sum(a for a, _ in fibers.values()),
            "shape_states": len(fibers),
            "avoiders": sum(b for _, b in fibers.values()),
            "max_avoiding_shape_fiber": max(b for _, b in fibers.values()),
            "max_heap_labeling_shape_fiber": max(a for a, _ in fibers.values()),
            "mixed_avoidance_shapes": sum(0 < b < a for a, b in fibers.values()),
        })
        clear_caches()
    p, q = (2, 1, 4, 3), (3, 1, 4, 2)
    require(cartesian_shape(p) == cartesian_shape(q), "expected shape collision")
    require(bool(direct_occurrences(p)) and not direct_occurrences(q),
            "expected avoidance status collision")
    payload = {
        "status": "finite replay passed; not an asymptotic theorem",
        "scope": {"all_permutations_n": [0, args.max_n],
                  "all_maximum_gaps_for_every_parent": True},
        "permutations_checked": checked,
        "maximum_insertions_checked": transitions,
        "stream_sha256": digest.hexdigest(),
        "records": records,
        "same_shape_different_avoidance": {
            "containing": p, "avoiding": q,
            "tree": tree_word(cartesian_shape(p)),
            "occurrences": direct_occurrences(p),
        },
        "python": platform.python_version(),
        "seconds": perf_counter() - start,
    }
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
