#!/usr/bin/env python3
"""Exact orphan-local Q7 size-29 SAT encoding with the D>=18 bounds."""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys
import time

from pysat.card import CardEnc, EncType
from pysat.pb import PBEnc
from pysat.solvers import Solver

PREDECESSOR = pathlib.Path(__file__).resolve().parents[1] / "q7_ld29_family_reduction"
sys.path.insert(0, str(PREDECESSOR))

from local_graphs import local_graph_assumptions, local_graph_representatives  # noqa: E402
from search_q7_ld29 import (  # noqa: E402
    DIMENSION,
    VERTEX_COUNT,
    add_nonisolated_variables,
    add_pair_indicators,
    add_singleton_variables,
    build,
    dimacs_bytes,
)


def strengthened(*, pair_bounds: bool, dynamic_pair_bound: bool):
    cnf = build(
        lex=False,
        structural=False,
        pair_bounds=False,
        dynamic_pair_bound=False,
    )
    nonisolated = add_nonisolated_variables(cnf)
    singleton = add_singleton_variables(cnf)
    edges = add_pair_indicators(cnf, 1)
    distance_two_pairs = add_pair_indicators(cnf, 2) if pair_bounds else []

    cnf.extend(
        CardEnc.atmost(
            lits=nonisolated,
            bound=16,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atleast(
            lits=singleton,
            bound=42,
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
            bound=32,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    if pair_bounds:
        cnf.extend(
            CardEnc.atleast(
                lits=distance_two_pairs,
                bound=26,
                top_id=cnf.nv,
                encoding=EncType.totalizer,
            ).clauses
        )
    if pair_bounds and dynamic_pair_bound:
        cnf.extend(
            PBEnc.atleast(
                lits=[*distance_two_pairs, *(-literal for literal in singleton)],
                weights=[*[1] * len(distance_two_pairs), *[2] * len(singleton)],
                bound=198,
                top_id=cnf.nv,
            ).clauses
        )
    return cnf


def scratch_path(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("solver artifacts must stay under /scratch")
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local-graph-index", type=int, required=True)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--pair-bounds", action="store_true")
    parser.add_argument("--dynamic-pair-bound", action="store_true")
    parser.add_argument("--write-cnf")
    parser.add_argument("--build-only", action="store_true")
    args = parser.parse_args()
    if args.dynamic_pair_bound and not args.pair_bounds:
        raise ValueError("--dynamic-pair-bound requires --pair-bounds")

    representatives = local_graph_representatives()
    if not 0 <= args.local_graph_index < len(representatives):
        raise ValueError(f"local graph index must lie in 0..{len(representatives)-1}")

    started = time.monotonic()
    cnf = strengthened(
        pair_bounds=args.pair_bounds,
        dynamic_pair_bound=args.dynamic_pair_bound,
    )
    mask = representatives[args.local_graph_index]
    cnf.extend([[literal] for literal in local_graph_assumptions(mask)])
    payload = dimacs_bytes(cnf)
    print(
        f"local_graph={args.local_graph_index}/{len(representatives)} "
        f"edges={mask.bit_count()} mask={mask}",
        flush=True,
    )
    print(
        f"variables={cnf.nv} clauses={len(cnf.clauses)} "
        f"sha256={hashlib.sha256(payload).hexdigest()}",
        flush=True,
    )
    if args.write_cnf:
        scratch_path(args.write_cnf).write_bytes(payload)
    print(f"built_seconds={time.monotonic() - started:.3f}", flush=True)
    if args.build_only:
        return

    solve_started = time.monotonic()
    with Solver(name=args.solver, bootstrap_with=cnf.clauses) as solver:
        satisfiable = solver.solve()
        model = solver.get_model() if satisfiable else None
    print(
        f"{args.solver}={'SAT' if satisfiable else 'UNSAT'} "
        f"solve_seconds={time.monotonic() - solve_started:.3f}",
        flush=True,
    )
    if model is not None:
        positive = {literal for literal in model if literal > 0}
        code = [v for v in range(VERTEX_COUNT) if v + 1 in positive]
        print("code:", " ".join(f"{vertex:0{DIMENSION}b}" for vertex in code))


if __name__ == "__main__":
    main()
