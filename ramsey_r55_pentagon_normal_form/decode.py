#!/usr/bin/env python3
"""Expand exactly 842 Boolean pair values into the complete 43-vertex graph."""
import argparse
import itertools as it
import json
from pathlib import Path


def decode(bits):
    if len(bits) != 842 or any(c not in "01" for c in bits):
        raise ValueError("expected exactly 842 binary values")
    red = []
    k = 0
    for u, v in it.combinations(range(43), 2):
        if u < 2 and v < 7:
            value = 1
        elif 2 <= u < v < 27 and (u - 2) // 5 == (v - 2) // 5:
            value = int(v - u in (1, 4))
        else:
            value = int(bits[k]); k += 1
        if value:
            red.append((u, v))
    if k != 842:
        raise ValueError("decoder coverage error")
    return red


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bits", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    edges = decode(args.bits.read_text().strip())
    args.output.write_text(f"43 {len(edges)}\n" + ''.join(f"{i} {j}\n" for i, j in edges))
    print(json.dumps({"status": "DECODED_FULL_GRAPH", "n": 43, "edges": len(edges),
                      "ramsey_status": "requires_physical_verification"}, sort_keys=True))
