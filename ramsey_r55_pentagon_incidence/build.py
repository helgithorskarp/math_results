#!/usr/bin/env python3
"""Produce literal second-pentagon witnesses; no external graph catalog."""
import argparse
import itertools as it
import json
from pathlib import Path


def independent(a, vertices, size):
    if size == 0:
        return True
    while vertices.bit_count() >= size:
        bit = vertices & -vertices
        vertices ^= bit
        if independent(a, vertices & ~a[bit.bit_length() - 1], size - 1):
            return True
    return False


def graph(word, mask):
    a = [0] * 10
    edges = [(i, (i + 1) % 5) for i in range(5)]
    edges += [(i + 5, x - 1) for i, x in enumerate(word) if x]
    edges += [(i + 5, j + 5) for k, (i, j) in
              enumerate(it.combinations(range(5), 2)) if mask >> k & 1]
    for i, j in edges:
        a[i] |= 1 << j
        a[j] |= 1 << i
    return a


def build():
    records = []
    words = list(it.combinations_with_replacement(range(6), 5))
    for wi, word in enumerate(words):
        for mask in range(1024):
            a = graph(word, mask)
            if any(a[i] & a[j] for i in range(10)
                   for j in range(i) if a[i] >> j & 1):
                continue
            if independent(a, 1023, 5):
                continue
            for s in it.combinations(range(10), 5):
                sm = sum(1 << x for x in s)
                if sm != 31 and all((a[x] & sm).bit_count() == 2 for x in s):
                    records.append([wi, mask, sm])
                    break
            else:
                raise RuntimeError(f"Unique-pentagon counterexample: {word}, {mask}")
    return {"schema": "r55-two-pentagons-v1", "records": records}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = build()
    args.output.write_text(json.dumps(result, separators=(",", ":")) + "\n")
    print(json.dumps({"status": "PRODUCED_SECOND_PENTAGONS",
                      "records": len(result["records"])}))
