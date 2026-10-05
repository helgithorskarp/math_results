#!/usr/bin/env python3
"""Exact weighted tree-state recurrence, with independently enumerated small fibers."""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import platform
import resource
from time import perf_counter

from tree_dynamics import (cartesian_shape, clear_caches, insert_maximum_shape,
                           shape_legal_gaps, tree_word)
from verify_kernel import direct_occurrences


def require(condition, description):
    if not condition:
        raise RuntimeError(description)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=11)
    parser.add_argument("--check-fibers-through", type=int, default=7)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    require(0 <= args.max_n <= 12, "bounded experimental scope is n<=12")
    require(0 <= args.check_fibers_through <= min(7, args.max_n),
            "definition-level fiber comparison bound is n<=7")
    start = perf_counter()
    weights = {(): 1}
    records = []
    transitions = 0
    for n in range(args.max_n + 1):
        level_start = perf_counter()
        literal_fibers_checked = False
        if n <= args.check_fibers_through:
            definition_fibers = defaultdict(int)
            for p in permutations(range(1, n + 1)):
                if not direct_occurrences(p):
                    definition_fibers[cartesian_shape(p)] += 1
            require(weights == dict(definition_fibers),
                    f"complete weighted-state comparison failed at n={n}")
            literal_fibers_checked = True
        digest = sha256()
        for t, w in sorted(weights.items(), key=lambda pair: tree_word(pair[0])):
            digest.update((tree_word(t) + ":" + str(w) + "\n").encode())
        max_weight = max(weights.values())
        max_trees = [tree_word(t) for t, w in weights.items() if w == max_weight]
        record = {
            "n": n, "states": len(weights), "avoiders": sum(weights.values()),
            "max_avoiding_single_tree_fiber": max_weight,
            "max_fiber_shapes": sorted(max_trees),
            "state_weight_stream_sha256": digest.hexdigest(),
            "all_weights_compared_to_literal_definition": literal_fibers_checked,
            "seconds_this_level_before_transition": perf_counter() - level_start,
            "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        }
        records.append(record)
        print(json.dumps(record), flush=True)
        if n != args.max_n:
            children = defaultdict(int)
            for tree, weight in weights.items():
                for gap in shape_legal_gaps(tree):
                    children[insert_maximum_shape(tree, gap)] += weight
                    transitions += 1
            weights = dict(children)
            clear_caches()
    payload = {
        "actor": "literature-researcher-3",
        "status": "exact finite weighted-state calculation; no growth conclusion",
        "full_growth_target_solved": False,
        "scope_n": [0, args.max_n],
        "all_state_weights_definition_checked_through": args.check_fibers_through,
        "legal_shape_transitions_processed": transitions,
        "records": records,
        "python": platform.python_version(),
        "native_threads": 1,
        "processes": 1,
        "seconds": perf_counter() - start,
        "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({k: v for k, v in payload.items() if k != "records"}), flush=True)


if __name__ == "__main__":
    main()
