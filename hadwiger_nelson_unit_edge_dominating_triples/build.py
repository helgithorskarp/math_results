#!/usr/bin/env python3
"""Generate the finite parity-conflict certificate used in the proof."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import product
from pathlib import Path


PAIRS4 = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PAIRS3 = ((0, 1), (0, 2), (1, 2))


def set_partitions(n: int):
    """Restricted-growth encodings of all set partitions."""
    word = [0] * n

    def visit(i: int, top: int):
        if i == n:
            yield tuple(word)
            return
        for value in range(top + 2):
            word[i] = value
            yield from visit(i + 1, max(top, value))

    yield from visit(1, 0)


def conflict_mask(partition, labels, pairs) -> int:
    mask = 0
    for bit, (i, j) in enumerate(pairs):
        if partition[i] == partition[j] and labels[i] != labels[j]:
            mask |= 1 << bit
    return mask


def valid_allocations(n: int, a_mask: int, c_mask: int, pairs, forced_a=()):
    answers = []
    for word in product((0, 1), repeat=n):  # 1 means palette A; 0 means C.
        if any(word[v] != 1 for v in forced_a):
            continue
        if any((a_mask >> k & 1) and word[i] == word[j] == 1 for k, (i, j) in enumerate(pairs)):
            continue
        if any((c_mask >> k & 1) and word[i] == word[j] == 0 for k, (i, j) in enumerate(pairs)):
            continue
        answers.append("".join(map(str, word)))
    return answers


def produce():
    parity_graphs = set()
    encodings = 0
    for partition in set_partitions(4):
        for labels in product((0, 1), repeat=4):
            parity_graphs.add(conflict_mask(partition, labels, PAIRS4))
            encodings += 1

    histogram = Counter()
    unsat = []
    admissible = 0
    internal_bits = (0, 5)  # pairs 01 and 23
    for a_mask in sorted(parity_graphs):
        for c_mask in sorted(parity_graphs):
            if any(bool(a_mask >> k & 1) != bool(c_mask >> k & 1) for k in internal_bits):
                continue
            admissible += 1
            allocations = valid_allocations(4, a_mask, c_mask, PAIRS4)
            histogram[len(allocations)] += 1
            if not allocations:
                unsat.append({"a_mask": a_mask, "c_mask": c_mask})

    triple_histogram = Counter()
    triple_unsat = []
    # Vertex 0 is triple-owned and forced to A.  It cannot use C, so the
    # only possible C-conflict is the pair (1,2), mask bit 2.
    for a_mask in range(8):
        for c_mask in (0, 4):
            allocations = valid_allocations(3, a_mask, c_mask, PAIRS3, forced_a=(0,))
            triple_histogram[len(allocations)] += 1
            if not allocations:
                triple_unsat.append({"a_mask": a_mask, "c_mask": c_mask})

    return {
        "schema": "unit-edge-dominating-triples-parity-v1",
        "pair_order_4": [list(p) for p in PAIRS4],
        "partition_label_encodings": encodings,
        "distinct_parity_conflict_graphs_4": len(parity_graphs),
        "admissible_no_triple_graph_pairs": admissible,
        "allocation_count_histogram": {str(k): histogram[k] for k in sorted(histogram)},
        "unsat_no_triple": unsat,
        "pair_order_3": [list(p) for p in PAIRS3],
        "triple_systems": 16,
        "triple_allocation_count_histogram": {
            str(k): triple_histogram[k] for k in sorted(triple_histogram)
        },
        "unsat_one_triple": triple_unsat,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    payload = produce()
    target = out / "certificate.json"
    target.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
