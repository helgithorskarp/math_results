#!/usr/bin/env python3
"""Deterministically discover the positive certificate with a SAT solver."""

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

from pysat.solvers import Cadical195

from model import fixed_case, require, serial_element
from two_factor import event_graph


def four_colour(edges):
    def variable(vertex, colour):
        return 4 * vertex + colour + 1

    solver = Cadical195()
    for vertex in range(343):
        solver.add_clause([variable(vertex, colour) for colour in range(4)])
        for c, d in itertools.combinations(range(4), 2):
            solver.add_clause([-variable(vertex, c), -variable(vertex, d)])
    for x, y in edges:
        for colour in range(4):
            solver.add_clause([-variable(x, colour), -variable(y, colour)])
    require(solver.solve(), "non-four-colourable exceptional support")
    model = {lit for lit in solver.get_model() if lit > 0}
    word = "".join(
        str(next(colour for colour in range(4) if variable(vertex, colour) in model))
        for vertex in range(343)
    )
    solver.delete()
    require(all(word[x] != word[y] for x, y in edges), "bad SAT word")
    return word


def generate():
    u, B, Db, Dm, groups, baseline, stats = fixed_case()
    words = []
    indices = {}
    assignment = []
    edge_counts = Counter()
    for index, (_, group) in enumerate(groups):
        edges = event_graph(Db, Dm, set(baseline), group)
        word = four_colour(edges)
        word_id = indices.setdefault(word, len(words))
        if word_id == len(words):
            words.append(word)
        assignment.append(word_id)
        edge_counts[len(edges)] += 1
        if (index + 1) % 250 == 0:
            print(f"SAT cases {index + 1}/{len(groups)}")
    return {
        "format": "fixed-eta3-circle-v1",
        "u": serial_element(u),
        "vertices": len(B) * 7,
        "baseline_edges": len(baseline),
        "filters": stats,
        "exceptional_quadratics": len(groups),
        "edge_counts": {str(k): edge_counts[k] for k in sorted(edge_counts)},
        "words": words,
        "assignment": assignment,
        "word_hashes": [hashlib.sha256(word.encode()).hexdigest() for word in words],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "certificate.json")
    args = parser.parse_args()
    args.output.write_text(json.dumps(generate(), indent=2, sort_keys=True) + "\n")
