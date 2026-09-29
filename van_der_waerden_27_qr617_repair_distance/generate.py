#!/usr/bin/env python3
"""Discover and write an elimination certificate; a separate verifier proves it.

No solver, floating point, parallelism, or external input is used. A stalled
search is an incomplete proof attempt, never mathematical nonexistence.
"""

import argparse
import json
from pathlib import Path


P = 617
N = 6 * P + 1


def critical_progressions():
    squares = {i * i % P for i in range(1, P)}
    color = [int(x % P not in squares) for x in range(N)]
    edges = [[] for _ in range(N)]
    for d in range(1, (N - 1) // 6 + 1):
        for a in range(N - 6 * d):
            points = [a + j * d for j in range(7)]
            if any(x % P == 0 for x in points):
                continue
            values = [color[x] for x in points]
            total = sum(values)
            if total in (1, 6):
                v = points[values.index(int(total == 1))]
                edges[v].append((sum(1 << x for x in points if x != v), a, d))
    return edges


def select_witness(edges, radius):
    for mask, a, d in edges:
        if mask == 0:
            return [[a, d]]
    if len(edges) < radius:
        return None
    m = len(edges)
    conflicts = [0] * m
    for i in range(m):
        for j in range(i):
            if edges[i][0] & edges[j][0]:
                conflicts[i] |= 1 << j
                conflicts[j] |= 1 << i
    available = (1 << m) - 1
    selected = []
    while available:
        indices = []
        bits = available
        while bits:
            bit = bits & -bits
            indices.append(bit.bit_length() - 1)
            bits ^= bit
        i = min(indices, key=lambda i: (
            (conflicts[i] & available).bit_count(),
            edges[i][0].bit_count(), edges[i][2], edges[i][1]))
        selected.append([edges[i][1], edges[i][2]])
        if len(selected) == radius:
            return selected
        available &= ~(conflicts[i] | (1 << i))
    return None


def generate(radius):
    edges = critical_progressions()
    vertices = [x for x in range(N) if x % P]
    allowed = sum(1 << x for x in vertices)
    full_records = []
    rounds = []
    while allowed:
        removed = []
        for v in vertices:
            if not (allowed & (1 << v)):
                continue
            pairs = select_witness([(mask & allowed, a, d) for mask, a, d in edges[v]], radius)
            if pairs is not None:
                removed.append(v)
                full_records.append([v, pairs])
        rounds.append(len(removed))
        if not removed:
            raise RuntimeError(f"Proof search stalled with {allowed.bit_count()} positions; no exclusion established")
        allowed &= ~sum(1 << v for v in removed)

    # Reflecting each deduction preserves its validity and halves coverage.
    # Remove redundant later records; shorten a packing if one petal is empty.
    allowed_set = set(vertices)
    records = []
    for v, pairs in full_records:
        if v not in allowed_set:
            continue
        for a, d in pairs:
            if not ({a + j * d for j in range(7)} - {v}) & allowed_set:
                pairs = [[a, d]]
                break
        records.append([v, pairs])
        allowed_set.remove(v)
        allowed_set.remove(N - 1 - v)
    if allowed_set:
        raise RuntimeError("Incomplete reflection coverage")
    data = {
        "format": "qr617-critical-petals-v1", "radius": radius,
        "prime": P, "prefix_length": N, "reflect_each_record": True,
        "records": records, "extension_obstructions": [[1, 617], [3421, 47]],
    }
    return data, {"critical_progressions": sum(map(len, edges)), "round_eliminations": rounds}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--radius", type=int, default=28)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.radius <= 100:
        parser.error("radius must lie in [1,100]")
    data, summary = generate(args.radius)
    encoded = json.dumps(data, separators=(",", ":")) + "\n"
    temporary = args.output.with_name(args.output.name + ".tmp")
    temporary.write_text(encoded)
    temporary.replace(args.output)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
