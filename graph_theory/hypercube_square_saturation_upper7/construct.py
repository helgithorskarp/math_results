#!/usr/bin/env python3
"""Deterministic square-saturated cube construction; Python 3.11+, stdlib only.

The universal theorem is proved in proof.md. This program expands small
instances, audits the exceptional-set claim, and greedily completes them.
Generated edge lists belong outside the source directory.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction


def syndrome(vertex: int) -> int:
    answer = 0
    for bit in range(vertex.bit_length()):
        if vertex & (1 << bit):
            answer ^= bit + 1
    return answer


def template_edge(s: int, t: int) -> bool:
    if s == t:
        return False
    if s == 0 or t == 0 or {s, t} == {1, 3}:
        return True
    for hub, outer in ((s, t), (t, s)):
        if hub in (1, 2) and outer >= 4:
            return hub == (1 if (outer & 3).bit_count() % 2 == 0 else 2)
    return False


def choose_blocks(n: int) -> tuple[int, int, int]:
    if n < 6:
        raise ValueError("the construction requires n >= 6")
    q = 1 << (((n + 2) // 2).bit_length() - 1)
    p = q if n + 2 < 3 * q else 2 * q
    return p - 1, q - 1, n - p - q + 2


def bound(n: int, p: int, q: int) -> Fraction:
    return (Fraction(5, 2)
            + Fraction(3 * n - 13, 4) * (Fraction(1, p) + Fraction(1, q))
            + Fraction(9 * n, p * q))


def edge_hash(edges: list[list[int]]) -> str:
    encoded = "".join(f"{u} {v}\n" for u, v in edges).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def construct(a: int, b: int, r: int) -> dict:
    for length in (a, b):
        if length < 3 or (length + 1) & length:
            raise ValueError("block lengths must be 2^t-1 with t >= 2")
    if r < 0:
        raise ValueError("padding length must be nonnegative")
    n = a + b + r
    if n > 16:
        raise ValueError("expansion is capped at dimension 16; use --bound above it")
    mask_a = (1 << a) - 1
    mask_b = ((1 << b) - 1) << a
    labels = [syndrome(v) for v in range(1 << max(a, b))]
    states = [(labels[v & mask_a], labels[(v & mask_b) >> a])
              for v in range(1 << n)]
    exceptional = [s in (0, 1, 2) and t in (0, 1, 2) for s, t in states]
    host = [(u, i) for u in range(1 << n) for i in range(n)
            if not u & (1 << i)]
    index = {edge: k for k, edge in enumerate(host)}
    present = []
    for u, i in host:
        v = u ^ (1 << i)
        s, t = states[u]
        selected = False
        if i < a:
            selected = template_edge(s, s ^ (i + 1))
        elif i < a + b:
            selected = template_edge(t, t ^ (i - a + 1))
        if i >= a and s in (0, 1, 2):
            selected |= ((u & ~mask_a).bit_count() % 2 == (0 if s == 0 else 1))
        if not a <= i < a + b and t in (0, 1, 2):
            selected |= ((u & ~mask_b).bit_count() % 2 == (0 if t == 0 else 1))
        present.append(selected and not exceptional[u] and not exceptional[v])

    faces = []
    incident = [[] for _ in host]
    for u in range(1 << n):
        zeros = [i for i in range(n) if not u & (1 << i)]
        for i, j in itertools.combinations(zeros, 2):
            face = [index[u, i], index[u, j],
                    index[u ^ (1 << i), j], index[u ^ (1 << j), i]]
            for edge in face:
                incident[edge].append(len(faces))
            faces.append(face)
    counts = [sum(present[e] for e in face) for face in faces]
    if any(count == 4 for count in counts):
        raise AssertionError("initial construction contains a square")
    uncovered = [e for e in range(len(host)) if not present[e]
                 and not any(counts[f] == 3 for f in incident[e])]
    for e in uncovered:
        u, i = host[e]
        if not exceptional[u] and not exceptional[u ^ (1 << i)]:
            raise AssertionError("an uncovered edge avoids the exceptional set")
    initial = sum(present)
    for e in uncovered:  # host order is lexicographic (lower vertex, bit).
        if not any(counts[f] == 3 for f in incident[e]):
            present[e] = True
            for face in incident[e]:
                counts[face] += 1
    if any(count == 4 for count in counts):
        raise AssertionError("completion created a square")
    if not all(present[e] or any(counts[f] == 3 for f in incident[e])
               for e in range(len(host))):
        raise AssertionError("completion is not saturated")
    result_edges = [[u, u ^ (1 << i)] for e, (u, i) in enumerate(host) if present[e]]
    result_edges.sort()
    coefficient = bound(n, a + 1, b + 1)
    if len(result_edges) > coefficient * (1 << n):
        raise AssertionError("proved edge bound violated")
    if sum(exceptional) != 9 * (1 << n) // ((a + 1) * (b + 1)):
        raise AssertionError("exceptional-set cardinality mismatch")
    return {
        "dimension": n, "blocks": [a, b, r],
        "initial_edges": initial, "initial_uncovered_edges": len(uncovered),
        "uncovered_edges_away_from_exceptional_set": 0,
        "exceptional_vertices": sum(exceptional),
        "completion_edges": len(result_edges) - initial,
        "edge_count": len(result_edges), "edge_sha256": edge_hash(result_edges),
        "bound_coefficient": str(coefficient), "edges": result_edges,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dimension", type=int)
    group.add_argument("--blocks", nargs=3, type=int, metavar=("A", "B", "R"))
    parser.add_argument("--bound", action="store_true", help="exact bound without cube expansion")
    args = parser.parse_args()
    a, b, r = choose_blocks(args.dimension) if args.dimension is not None else args.blocks
    if args.bound:
        for length in (a, b):
            if length < 3 or (length + 1) & length:
                raise ValueError("invalid Hamming block length")
        if r < 0:
            raise ValueError("negative padding")
        n = a + b + r
        print(json.dumps({"dimension": n, "blocks": [a, b, r],
                          "bound_coefficient": str(bound(n, a + 1, b + 1))}, sort_keys=True))
    else:
        print(json.dumps(construct(a, b, r), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
