#!/usr/bin/env python3
"""Check library failure for every residual; reconstruct selected geometries.

For geometry, derive the isometry directly from the two overlap pairs.  Work
with an algebraic common denominator rather than the C++ normalized rotation
and rational translation.  No spatial buckets or numerical intervals are used.
"""
from itertools import permutations
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / "hadwiger_nelson_parts509_two_overlap_cross_census"
POINTS = HERE.parent / "hadwiger_nelson_parts509_completion_census_degree9/points.tsv"
RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
ZERO = (0,) * 8
UNIT = (96 * 96,) + (0,) * 7


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(a, b):
    result = [0] * 8
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    result[i ^ j] += x * y * RADICANDS[i & j]
    return tuple(result)


def norm(x, y):
    return add(mul(x, x), mul(y, y))


def points():
    all_points = []
    for line in POINTS.read_text().splitlines():
        if line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        if len(row) != 16:
            raise ValueError("bad point row")
        all_points.append((row[:8], row[8:]))
    if len(all_points) != 509 or len(set(all_points)) != 509:
        raise ValueError("point census mismatch")
    return all_points[:374], [all_points[0]] + all_points[374:]


def internal_edges(vertices):
    return {(a, b) for a in range(len(vertices)) for b in range(a + 1, len(vertices))
            if norm(sub(vertices[a][0], vertices[b][0]),
                    sub(vertices[a][1], vertices[b][1])) == UNIT}


def check_geometry(case, large, small, large_edges, small_edges):
    overlaps = [divmod(encoded, 136) for encoded in case["overlaps"]]
    (p0, q0), (p1, q1) = overlaps
    if p0 == p1 or q0 == q1:
        raise ValueError("degenerate overlap seed")
    reflected = case["orientation"] >= 1420
    source = [(x, tuple(-v for v in y) if reflected else y) for x, y in small]
    ux, uy = sub(source[q1][0], source[q0][0]), sub(source[q1][1], source[q0][1])
    vx, vy = sub(large[p1][0], large[p0][0]), sub(large[p1][1], large[p0][1])
    denominator = norm(ux, uy)
    if denominator == ZERO or denominator != norm(vx, vy):
        raise ValueError("overlap segments have unequal squared lengths")
    cosine = add(mul(ux, vx), mul(uy, vy))
    sine = sub(mul(ux, vy), mul(uy, vx))
    # All points now share denominator 96*denominator.  Translate p0 to zero.
    left_numerators = [
        (mul(denominator, sub(x, large[p0][0])),
         mul(denominator, sub(y, large[p0][1]))) for x, y in large
    ]
    small_numerators = []
    for x, y in source:
        dx, dy = sub(x, source[q0][0]), sub(y, source[q0][1])
        small_numerators.append((sub(mul(cosine, dx), mul(sine, dy)),
                                 add(mul(sine, dx), mul(cosine, dy))))
    target = tuple(96 * 96 * v for v in mul(denominator, denominator))
    coincidences = []
    cross_edges = set()
    label = {q: p for p, q in overlaps}
    for p, (x, y) in enumerate(left_numerators):
        for q, (u, v) in enumerate(small_numerators):
            dx, dy = sub(x, u), sub(y, v)
            if dx == ZERO and dy == ZERO:
                coincidences.append((p, q))
            if norm(dx, dy) == target:
                cross_edges.add(tuple(sorted((p, label.get(q, 374 + q)))))
    if coincidences != overlaps:
        raise ValueError("overlap list mismatch in direct reconstruction")
    if len(set(left_numerators + small_numerators)) != 508:
        raise ValueError("strict union order mismatch")
    inherited = large_edges | {
        tuple(sorted((label.get(a, 374 + a), label.get(b, 374 + b))))
        for a, b in small_edges
    }
    new_edges = sorted(510 * a + b for a, b in cross_edges - inherited)
    if new_edges != case["edges"]:
        raise ValueError("direct geometry disagrees with residual edges")


def reverse_masks():
    """Fix original S colours; bits index all colour permutations of L rows."""
    large, small = [], []
    for line in (PRIOR / "colour_libraries.txt").read_text().splitlines():
        kind, row = line.split(":")
        (large if kind == "L" else small).append(tuple(map(int, row)))
    if len(large) != 135 or len(small) != 194:
        raise ValueError("library row count mismatch")
    expanded = [tuple(p[c] for c in row) for row in large
                for p in permutations(range(4))]
    equality = [[0] * 4 for _ in range(374)]
    for index, row in enumerate(expanded):
        bit = 1 << index
        for vertex, colour in enumerate(row):
            equality[vertex][colour] |= bit
    return small, equality, (1 << len(expanded)) - 1


def main():
    if len(sys.argv) != 2:
        raise ValueError("usage: python3 check_residual.py RESIDUAL.jsonl")
    cases = [json.loads(line) for line in Path(sys.argv[1]).read_text().splitlines()]
    if not cases:
        print("residual_cases=0")
        return
    small_colours, equality, full = reverse_masks()
    for case in cases:
        overlaps = [divmod(pair, 136) for pair in case["overlaps"]]
        edges = [(edge // 510, edge % 510 - 374) for edge in case["edges"]]
        for small in small_colours:
            allowed = full
            for p, q in overlaps:
                allowed &= equality[p][small[q]]
            for p, q in edges:
                allowed &= full ^ equality[p][small[q]]
                if not allowed:
                    break
            if allowed:
                raise ValueError("reported residual has a compatible library pair")
    print(f"residual_cases={len(cases)}")
    print("all_residuals_fail_reversed_library_intersection=true")
    # Up to eight deterministic samples: shortest, longest, first and last
    # residual in each orientation parity. This is explicitly sample coverage.
    chosen = {}
    for reflected in (False, True):
        subset = [c for c in cases if (c["orientation"] >= 1420) == reflected]
        if not subset:
            continue
        for case in (subset[0], subset[-1],
                     min(subset, key=lambda c: (len(c["edges"]), c["orientation"], c["overlaps"])),
                     max(subset, key=lambda c: (len(c["edges"]), c["orientation"], c["overlaps"]))):
            key = (case["orientation"], tuple(case["overlaps"]))
            chosen[key] = case
    large, small = points()
    large_edges, small_edges = internal_edges(large), internal_edges(small)
    if (len(large_edges), len(small_edges)) != (1860, 564):
        raise ValueError("independent internal edge census mismatch")
    for key, case in sorted(chosen.items()):
        check_geometry(case, large, small, large_edges, small_edges)
        print(f"direct_geometry_orientation={key[0]} overlaps={list(key[1])} "
              f"new_edges={len(case['edges'])}")
    print(f"independent_direct_geometry_samples={len(chosen)}")


if __name__ == "__main__":
    main()
