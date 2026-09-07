#!/usr/bin/env python3
"""Generate the adaptive core-colouring cover for the target-sized family."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

from pysat.solvers import Cadical195


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "hadwiger_nelson_small_triangle_forcer375"
OVERLAP = HERE.parent / "hadwiger_nelson_overlapping_forcing_seed"
sys.path[:0] = [str(PARENT), str(OVERLAP)]

from geometry import graph  # noqa: E402
from lattice import directions, edges as lattice_edges  # noqa: E402


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def var(v: int, colour: int) -> int:
    return 4 * v + colour + 1


def main() -> None:
    base_points, base_edges = graph()
    base_points = [tuple(p) for p in base_points]
    unit_directions = directions(1)
    base_set = set(base_points)
    completion_set = {
        tuple(x + y for x, y in zip(point, displacement))
        for point in base_points
        for displacement in unit_directions
    } - base_set
    completion = sorted(completion_set)
    base_degree = [sum(tuple(x - y for x, y in zip(q, d)) in base_set for d in unit_directions) for q in completion]
    core_additions = [q for q, degree in zip(completion, base_degree) if degree >= 6]
    optional = [q for q, degree in zip(completion, base_degree) if degree == 5]
    points = base_points + core_additions + optional
    core_n = len(base_points) + len(core_additions)
    optional_n = len(optional)
    if (len(base_points), len(base_edges), len(unit_directions), len(completion), core_n, optional_n) != (375, 1661, 54, 12184, 506, 141):
        raise RuntimeError("construction count mismatch")
    edges = [tuple(edge) for edge in lattice_edges(points, 1)]
    core_edges = [(u, v) for u, v in edges if v < core_n]
    optional_core = [set() for _ in range(optional_n)]
    optional_edges = set()
    for u, v in edges:
        if u < core_n <= v:
            optional_core[v - core_n].add(u)
        elif core_n <= u:
            optional_edges.add((u - core_n, v - core_n))
    if (len(core_edges), sum(map(len, optional_core)), len(optional_edges)) != (2677, 868, 81):
        raise RuntimeError("support edge mismatch")

    selectors = [4 * len(points) + i + 1 for i in range(optional_n)]
    clauses = []
    for v in range(core_n):
        clauses.append([var(v, c) for c in range(4)])
        for c, d in combinations(range(4), 2):
            clauses.append([-var(v, c), -var(v, d)])
    for i in range(optional_n):
        v = core_n + i
        clauses.append([-selectors[i]] + [var(v, c) for c in range(4)])
        for c, d in combinations(range(4), 2):
            clauses.append([-selectors[i], -var(v, c), -var(v, d)])
    for u, v in edges:
        guards = []
        if u >= core_n:
            guards.append(-selectors[u - core_n])
        if v >= core_n:
            guards.append(-selectors[v - core_n])
        for c in range(4):
            clauses.append(guards + [-var(u, c), -var(v, c)])
    triangle = (0, 34, 36)
    edge_set = set(edges)
    if not all(tuple(sorted(pair)) in edge_set for pair in combinations(triangle, 2)):
        raise RuntimeError("pin is not a triangle")
    clauses.extend([[var(triangle[c], c)] for c in range(3)])

    pairs = list(combinations(range(optional_n), 2))
    full = (1 << len(pairs)) - 1

    def coverage(word: list[int]) -> int:
        available = [tuple(c for c in range(4) if c not in {word[v] for v in neighbours}) for neighbours in optional_core]
        bits = 0
        for k, (i, j) in enumerate(pairs):
            if available[i] and available[j] and (
                (i, j) not in optional_edges
                or any(a != b for a in available[i] for b in available[j])
            ):
                bits |= 1 << k
        return bits

    covered = 0
    library = []
    with Cadical195(bootstrap_with=clauses) as solver:
        while covered != full:
            missing = ~covered & full
            pair_index = (missing & -missing).bit_length() - 1
            i, j = pairs[pair_index]
            active = {i, j}
            assumptions = [selectors[q] if q in active else -selectors[q] for q in range(optional_n)]
            if not solver.solve(assumptions=assumptions):
                raise RuntimeError(f"non-four-colourable target candidate at optional pair {(i, j)}")
            positive = {literal for literal in solver.get_model() if literal > 0}
            word = [next(c for c in range(4) if var(v, c) in positive) for v in range(core_n)]
            bits = coverage(word)
            if not (bits >> pair_index) & 1:
                raise RuntimeError("solver model does not cover trigger pair")
            library.append(
                {
                    "trigger_pair": [i, j],
                    "core_colouring": "".join(map(str, word)),
                    "coverage_count": bits.bit_count(),
                    "new_coverage_count": (bits & ~covered).bit_count(),
                }
            )
            covered |= bits

    first_cover = []
    coverages = [coverage(list(map(int, row["core_colouring"]))) for row in library]
    for k in range(len(pairs)):
        first_cover.append(next(r for r, bits in enumerate(coverages) if bits >> k & 1))
    pair_edges = [
        len(core_edges) + len(optional_core[i]) + len(optional_core[j]) + ((i, j) in optional_edges)
        for i, j in pairs
    ]
    certificate = {
        "schema": "t375-high-contact-two-point-cover-v1",
        "construction": {
            "base_vertices": 375,
            "base_edges": 1661,
            "unit_directions": 54,
            "completion_vertices": len(completion),
            "base_degree_histogram": {str(k): v for k, v in sorted(Counter(base_degree).items())},
            "core_minimum_base_degree": 6,
            "core_vertices": core_n,
            "core_edges": len(core_edges),
            "optional_base_degree": 5,
            "optional_vertices": optional_n,
            "optional_core_edges": sum(map(len, optional_core)),
            "optional_internal_edges": len(optional_edges),
            "support_vertices": len(points),
            "support_edges": len(edges),
            "pair_members": len(pairs),
            "total_members_through_two_optional_points": 1 + optional_n + len(pairs),
            "target_vertices": core_n + 2,
            "target_edge_range": [min(pair_edges), max(pair_edges)],
            "triangle_pin": list(triangle),
        },
        "hashes": {
            "unit_directions_sha256": digest(unit_directions),
            "completion_points_sha256": digest(completion),
            "support_points_sha256": digest(points),
            "support_edges_sha256": digest(edges),
            "core_points_sha256": digest(points[:core_n]),
            "core_edges_sha256": digest(core_edges),
            "first_cover_rows_sha256": hashlib.sha256(bytes(first_cover)).hexdigest(),
        },
        "library": library,
        "target_found": False,
    }
    (HERE / "certificate.json").write_text(json.dumps(certificate, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps({"library_rows": len(library), **certificate["construction"], **certificate["hashes"]}, sort_keys=True))


if __name__ == "__main__":
    main()
