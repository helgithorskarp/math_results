#!/usr/bin/env python3
"""Independent SAT encoding of the six certified Parts-509 pool shapes.

This checker deliberately imports no module from the target contribution.  It
reads only its two JSON certificates, translates each killing set into the
corresponding candidate-hitting clause, uses PySAT's totalizer rather than the
target's custom encoder, and solves the resulting alternate CNFs.
"""

from __future__ import annotations

import json
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Solver


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "hadwiger_nelson_parts509_pool_shape_closure"


def main() -> None:
    killing = json.loads((TARGET / "killing_sets.json").read_text())
    closure = json.loads((TARGET / "closures.json").read_text())
    s_vertices = closure["S"]
    q_vertices = closure["Q5"]
    s_set, q_set = set(s_vertices), set(q_vertices)
    removed = {v: i + 1 for i, v in enumerate(s_vertices)}
    added = {v: len(s_vertices) + i + 1 for i, v in enumerate(q_vertices)}

    assert killing["U"] == sorted(s_vertices + q_vertices)
    assert sorted(map(int, closure["closures"])) == list(range(6))

    for a in range(6):
        info = closure["closures"][str(a)]
        cnf = CNF()
        for index in info["sets"]:
            deleted = killing["sets"][index]["D"]
            clause = (
                [-removed[v] for v in deleted if v in s_set]
                + [added[v] for v in deleted if v in q_set]
            )
            assert clause
            cnf.append(clause)

        top = len(s_vertices) + len(q_vertices)
        first = CardEnc.equals(
            lits=list(removed.values()),
            bound=a + 1,
            top_id=top,
            encoding=EncType.totalizer,
        )
        cnf.extend(first.clauses)
        second = CardEnc.equals(
            lits=list(added.values()),
            bound=a,
            top_id=first.nv,
            encoding=EncType.totalizer,
        )
        cnf.extend(second.clauses)

        with Solver(name="cadical195", bootstrap_with=cnf.clauses) as solver:
            satisfiable = solver.solve()
        result = "SAT" if satisfiable else "UNSAT"
        print(
            f'a={a} sets={len(info["sets"])} alt_vars={cnf.nv} '
            f'alt_clauses={len(cnf.clauses)} result={result}',
            flush=True,
        )
        assert not satisfiable

    print("alternate_master_check=true")


if __name__ == "__main__":
    main()
