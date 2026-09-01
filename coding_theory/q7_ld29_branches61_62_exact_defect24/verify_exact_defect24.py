#!/usr/bin/env python3
"""Build and verify the D>=25 exclusions for Q7 LD29 branches 61 and 62."""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

from pysat.card import CardEnc, EncType


SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1]
PREDECESSOR_PATH = (
    SOURCE_ROOT
    / "q7_ld29_branches61_62_split"
    / "verify_branches61_62_split.py"
)
EXPECTED_PREDECESSOR_SHA256 = "c91531e6cc12c993a2a59a8e83b2bcede8fba8fc50d4589eac415b28670456c9"
assert hashlib.sha256(PREDECESSOR_PATH.read_bytes()).hexdigest() == EXPECTED_PREDECESSOR_SHA256
sys.path.insert(0, str(SOURCE_ROOT / "q7_ld29_family_reduction"))

from local_graphs import local_graph_assumptions, local_graph_representatives  # noqa: E402
from search_q7_ld29 import (  # noqa: E402
    add_nonisolated_variables,
    add_pair_indicators,
    add_singleton_variables,
    build as base_build,
    dimacs_bytes,
)


MASKS = {61: 5941, 62: 5948}
EXPECTED_DIGESTS = {
    61: "bc3e7209f890eb96f370a8df089d66d8c279a2a0e0ab645c19cb8ddecd6267d7",
    62: "571a3d012d5e0f84731967f7b345b2fee137a11e51cc0ee49ffcb068687a0360",
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
            bound=9,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atleast(
            lits=singleton,
            bound=49,
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
            bound=13,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    representatives = local_graph_representatives()
    assert len(representatives) == 115
    mask = representatives[branch]
    assert mask == MASKS[branch]
    cnf.extend([[literal] for literal in local_graph_assumptions(mask)])
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]
    return cnf, mask


def scratch_directory(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("CNF output must remain under /scratch")
    path.mkdir(parents=True, exist_ok=True)
    return path


def solve_kissat(cnf, name: str) -> None:
    from pysat.solvers import Solver

    with Solver(name="kissat404", bootstrap_with=cnf.clauses) as solver:
        assert not solver.solve()
    print(f"PASS formula={name} Kissat-4.0.4=UNSAT")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    parser.add_argument("--solve-kissat", action="store_true")
    args = parser.parse_args()
    output = scratch_directory(args.write_directory) if args.write_directory else None

    for branch in sorted(MASKS):
        cnf, mask = build(branch)
        payload = dimacs_bytes(cnf)
        digest = hashlib.sha256(payload).hexdigest()
        assert cnf.nv == EXPECTED_VARIABLES
        assert len(cnf.clauses) == EXPECTED_CLAUSES
        assert digest == EXPECTED_DIGESTS[branch]
        name = f"branch{branch}-d25"
        if output is not None:
            (output / f"{name}.cnf").write_bytes(payload)
        print(
            f"PASS formula={name} mask={mask} variables={cnf.nv} "
            f"clauses={len(cnf.clauses)} bytes={len(payload)} sha256={digest}"
        )
        if args.solve_kissat:
            solve_kissat(cnf, name)


if __name__ == "__main__":
    main()
