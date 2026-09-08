#!/usr/bin/env python3
"""Replay the minimum-deletion search that selected the positive repair."""
import argparse
import itertools
import json
import pathlib

from pysat.solvers import Cadical153

import verify

D = pathlib.Path(__file__).resolve().parent
UP = D.parent / "hadwiger_nelson_h516_degree4_surgeries"


def four_colourable(labels, edges):
    pos = {v: i for i, v in enumerate(labels)}

    def var(v, c):
        return 4 * pos[v] + c + 1

    with Cadical153() as solver:
        for v in labels:
            solver.add_clause([var(v, c) for c in range(4)])
        for u, v in edges:
            for c in range(4):
                solver.add_clause([-var(u, c), -var(v, c)])
        return solver.solve()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", type=pathlib.Path, required=True)
    args = ap.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    source = json.loads((UP / "SOURCE.json").read_text())
    candidate = json.loads((D / "parent508.json").read_text())
    labels, original = verify.quotient(source, candidate["surgeries"])
    k23, k4 = verify.forbidden(labels, original)
    verify.need(len(k23) == 6 and not k4, "frozen case-24 profile")
    constraints = set()
    for u, v, common in k23:
        for triple in itertools.combinations(common, 3):
            constraints.add(frozenset(tuple(sorted((a, b)))
                                      for a in (u, v) for b in triple))
    universe = sorted(set().union(*constraints))
    minimum = []
    for size in range(7):
        minimum = [frozenset(h) for h in itertools.combinations(universe, size)
                   if all(c & frozenset(h) for c in constraints)]
        if minimum:
            break
    verify.need(size == 6 and len(minimum) == 14400, "minimum hitting sets")
    answers = []
    selected = None
    for rank, deleted in enumerate(minimum):
        edges = sorted(set(original) - deleted)
        sat = four_colourable(labels, edges)
        answers.append("SAT" if sat else "UNSAT")
        if not sat:
            selected = deleted
            break
    want = frozenset(tuple(e) for e in candidate["deleted_edges"])
    verify.need(selected == want and rank == 11, "first positive repair")
    receipt = {
        "minimum_deletions": size,
        "minimum_hitting_sets": len(minimum),
        "queries": len(answers),
        "answers": answers,
        "first_UNSAT_rank_zero_based": rank,
        "deleted_edges": [list(e) for e in sorted(selected)],
        "candidate_matches": True,
    }
    expected = json.loads((D / "expected.json").read_text())["producer"]
    verify.need(receipt == expected, "expected producer receipt")
    (args.work / "producer.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
