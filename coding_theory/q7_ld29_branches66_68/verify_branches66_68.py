#!/usr/bin/env python3
"""Build exact Q7 LD29 branch 66--68 CNFs with the proved D>=24 bounds."""

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


EXPECTED = {
    66: (1022, "a1114814daf11367f5f0de7523307ec0990c529f0f3814f2fe49e1ded4002ace"),
    67: (1759, "c8df988078649ad8b7613a13a647c63ba91da7f1170612de34671e086d14db71"),
    68: (1783, "f1114e5860c93de7730218e9f96f1bb8aa293e6e79b2d1362be59b2ea902c737"),
}
EXPECTED_VARIABLES = 10432
EXPECTED_CLAUSES = 183619


def build(branch: int):
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
    mask = local_graph_representatives()[branch]
    cnf.extend([[literal] for literal in local_graph_assumptions(mask)])
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]
    return cnf, mask


def scratch_directory(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("CNF output must remain under /scratch")
    path.mkdir(parents=True, exist_ok=True)
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    parser.add_argument("--solve-kissat", action="store_true")
    parser.add_argument("--branch", type=int, choices=sorted(EXPECTED))
    args = parser.parse_args()
    output = scratch_directory(args.write_directory) if args.write_directory else None
    branches = [args.branch] if args.branch is not None else sorted(EXPECTED)

    for branch in branches:
        cnf, mask = build(branch)
        payload = dimacs_bytes(cnf)
        digest = hashlib.sha256(payload).hexdigest()
        expected_mask, expected_digest = EXPECTED[branch]
        assert mask == expected_mask
        assert mask.bit_count() == 9
        assert cnf.nv == EXPECTED_VARIABLES
        assert len(cnf.clauses) == EXPECTED_CLAUSES
        assert digest == expected_digest
        if output is not None:
            (output / f"branch-{branch}.cnf").write_bytes(payload)
        print(
            f"PASS branch={branch} mask={mask} D>=24 variables={cnf.nv} "
            f"clauses={len(cnf.clauses)} sha256={digest}",
            flush=True,
        )
        if args.solve_kissat:
            from pysat.solvers import Solver

            with Solver(name="kissat404", bootstrap_with=cnf.clauses) as solver:
                assert not solver.solve()
            print(f"PASS branch={branch} Kissat-4.0.4=UNSAT", flush=True)


if __name__ == "__main__":
    main()
