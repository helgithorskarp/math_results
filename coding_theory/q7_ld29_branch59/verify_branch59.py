#!/usr/bin/env python3
"""Regenerate and hash the exact D>=24 CNF for Q7 LD29 branch 59."""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

from pysat.card import CardEnc, EncType


SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE_ROOT / "q7_ld29_family_reduction"))

from local_graphs import local_graph_assumptions, local_graph_representatives  # noqa: E402
from search_q7_ld29 import (  # noqa: E402
    add_nonisolated_variables,
    add_pair_indicators,
    add_singleton_variables,
    build as base_build,
    dimacs_bytes,
)


BRANCH = 59
EXPECTED_MASK = 5873
EXPECTED_DIGEST = "a548059e35430ff142b1a4cc719c401a945f24e9041c91626460525c521cfddf"
EXPECTED_VARIABLES = 10432
EXPECTED_CLAUSES = 183619


def build():
    cnf = base_build(
        lex=False,
        structural=False,
        pair_bounds=False,
        dynamic_pair_bound=False,
    )
    nonisolated = add_nonisolated_variables(cnf)
    singleton = add_singleton_variables(cnf)
    edges = add_pair_indicators(cnf, 1)
    cnf.extend(
        CardEnc.atmost(
            lits=nonisolated,
            bound=10,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atleast(
            lits=singleton,
            bound=48,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atmost(
            lits=[*nonisolated, *singleton],
            bound=58,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atmost(
            lits=edges,
            bound=15,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    mask = local_graph_representatives()[BRANCH]
    cnf.extend([[literal] for literal in local_graph_assumptions(mask)])
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]
    return cnf, mask


def scratch_path(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("CNF output must remain under /scratch")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-cnf")
    parser.add_argument("--learn-digest", action="store_true")
    parser.add_argument("--solve-kissat", action="store_true")
    args = parser.parse_args()

    cnf, mask = build()
    payload = dimacs_bytes(cnf)
    digest = hashlib.sha256(payload).hexdigest()
    assert mask == EXPECTED_MASK
    assert mask.bit_count() == 8
    assert cnf.nv == EXPECTED_VARIABLES
    assert len(cnf.clauses) == EXPECTED_CLAUSES
    if not args.learn_digest:
        assert digest == EXPECTED_DIGEST
    if args.write_cnf:
        scratch_path(args.write_cnf).write_bytes(payload)
    if args.solve_kissat:
        from pysat.solvers import Solver

        with Solver(name="kissat404", bootstrap_with=cnf.clauses) as solver:
            assert not solver.solve()
        print("PASS Kissat 4.0.4 returned UNSAT")
    print(
        f"PASS branch={BRANCH} mask={mask} variables={cnf.nv} "
        f"clauses={len(cnf.clauses)} sha256={digest}"
    )


if __name__ == "__main__":
    main()
