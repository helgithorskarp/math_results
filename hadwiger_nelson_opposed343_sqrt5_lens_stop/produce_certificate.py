#!/usr/bin/env python3
"""Regenerate positive words; requires python-sat and writes only the requested path."""

from __future__ import annotations

from itertools import combinations
import argparse
import json
from pathlib import Path

from pysat.solvers import Cadical195

import verify as V


def variable(vertex, colour):
    return 4 * vertex + colour + 1


def solve_words(geometry, patterns):
    solver = Cadical195()
    for vertex in range(451):
        solver.add_clause([variable(vertex, colour) for colour in range(4)])
        for a, b in combinations(range(4), 2):
            solver.add_clause([-variable(vertex, a), -variable(vertex, b)])
    for a, b in geometry["edges"]:
        for colour in range(4):
            solver.add_clause([-variable(a, colour), -variable(b, colour)])

    words = {}
    for pattern in patterns:
        assumptions = [variable(vertex, int(colour)) for vertex, colour in enumerate(pattern)]
        V.need(solver.solve(assumptions=assumptions), f"unexpected UNSAT pattern {pattern}")
        model = set(solver.get_model())
        word = "".join(str(next(colour for colour in range(4)
                                if variable(vertex, colour) in model))
                       for vertex in range(451))
        V.need(V.proper(word, 451, geometry["edges"]), "solver returned improper word")
        V.need(word[:10] == pattern, "solver returned wrong projection")
        words[pattern] = word
    solver.delete()
    return words


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    geometry = V.build_geometry()
    source = json.loads((V.SOURCE / "certificate.json").read_text())
    certificate = {
        "schema": "opposed343-sqrt5-lens-stop-v1",
        "point_sha256": V.point_hash(geometry["points"]),
        "edge_sha256": V.edge_hash(geometry["edges"]),
        "centre_pair_sha256": V.pair_hash(geometry["centre_pairs"]),
        "words": solve_words(geometry, source["surviving_patterns"]),
    }
    args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
