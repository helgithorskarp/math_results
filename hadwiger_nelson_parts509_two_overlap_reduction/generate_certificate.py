#!/usr/bin/env python3
"""Discover a compact S-pair flexibility witness library with CaDiCaL."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pysat.solvers import Solver

from verify import (
    FORMAT,
    GRAPH_CERTIFICATE,
    POINTS,
    S_SIZE,
    VTX,
    build_edges,
    distance_histogram,
    exceptional_difference_counts,
    pack_coloring,
    read_points,
    sha256,
)


def clauses(n, edges):
    result = []
    for vertex in range(n):
        variables = [4 * vertex + color + 1 for color in range(4)]
        result.append(variables)
        result.extend(
            [-variables[c], -variables[d]]
            for c in range(4)
            for d in range(c + 1, 4)
        )
    result.extend(
        [-4 * u - color - 1, -4 * v - color - 1]
        for u, v in edges
        for color in range(4)
    )
    # The first lexicographic S triangle is (0,24,26).
    result.extend([[4 * vertex + color + 1] for color, vertex in enumerate((0, 24, 26))])
    return result


def decode(model):
    positive = {literal for literal in model if literal > 0}
    return tuple(
        next(color for color in range(4) if 4 * vertex + color + 1 in positive)
        for vertex in range(S_SIZE)
    )


def covered(witnesses, pair, same):
    u, v = pair
    return any((colors[u] == colors[v]) == same for colors in witnesses)


def generate(output: Path) -> None:
    points = read_points()
    L = points[:374]
    S = [points[0]] + points[374:]
    edges = build_edges(S)
    edge_set = set(edges)
    nonedges = [
        (u, v)
        for u in range(S_SIZE)
        for v in range(u + 1, S_SIZE)
        if (u, v) not in edge_set
    ]
    formula = clauses(S_SIZE, edges)
    witnesses = []
    next_variable = 4 * S_SIZE + 1
    with Solver(name="cadical195", bootstrap_with=formula) as solver:
        if not solver.solve():
            raise RuntimeError("S unexpectedly not 4-colourable")
        witnesses.append(decode(solver.get_model()))
        while True:
            target = next(
                ((pair, relation) for relation in (True, False) for pair in nonedges if not covered(witnesses, pair, relation)),
                None,
            )
            if target is None:
                break
            (u, v), same = target
            selector = next_variable
            next_variable += 1
            for color in range(4):
                xu, xv = 4 * u + color + 1, 4 * v + color + 1
                if same:
                    solver.add_clause([-selector, -xu, xv])
                    solver.add_clause([-selector, -xv, xu])
                else:
                    solver.add_clause([-selector, -xu, -xv])
            if not solver.solve(assumptions=[selector]):
                raise RuntimeError(f"S pair {(u, v)} lacks relation same={same}")
            witnesses.append(decode(solver.get_model()))

    # Delete any witness made redundant by later discoveries.
    changed = True
    while changed:
        changed = False
        for index in range(len(witnesses) - 1, -1, -1):
            trial = witnesses[:index] + witnesses[index + 1 :]
            if all(covered(trial, pair, relation) for relation in (True, False) for pair in nonedges):
                witnesses = trial
                changed = True
                break

    l_hist = distance_histogram(L)
    s_hist = distance_histogram(S)
    common = set(l_hist) & set(s_hist)
    matching = sum(l_hist[length] * s_hist[length] for length in common)
    differences = exceptional_difference_counts(L, S)
    certificate = {
        "format": FORMAT,
        "source_sha256": {
            "points.tsv": sha256(POINTS),
            "parts509.vtx": sha256(VTX),
            "parts509_certificate.json": sha256(GRAPH_CERTIFICATE),
        },
        "counts": {
            "L_vertices": len(L),
            "S_vertices_including_center": len(S),
            "total_labels": len(L) + len(S),
            "L_segments": sum(l_hist.values()),
            "S_segments": sum(s_hist.values()),
            "L_squared_distance_classes": len(l_hist),
            "S_squared_distance_classes": len(s_hist),
            "common_squared_distance_classes": len(common),
            "matching_unordered_segment_pairs": matching,
            "orientation_preserving_overlap_pair_certificates": 2 * matching,
            "orientation_reversing_overlap_pair_certificates": 2 * matching,
            "all_overlap_pair_certificates": 4 * matching,
            "S_edges": len(edges),
            "S_nonedges": len(nonedges),
            "S_pair_flexibility_witnesses": len(witnesses),
            "exceptional_orientations": len(differences),
            "cross_differences_per_exceptional_orientation": 374 * 136,
        },
        "s_colorings": [pack_coloring(list(colors)) for colors in witnesses],
    }
    output.write_text(json.dumps(certificate, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps(certificate["counts"], indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", type=Path, default=Path("certificate.json"))
    args = parser.parse_args()
    generate(args.output)


if __name__ == "__main__":
    main()
