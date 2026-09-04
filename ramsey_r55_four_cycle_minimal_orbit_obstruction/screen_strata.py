#!/usr/bin/env python3
"""Exploratory one-core SAT screen for selected four-cycle edge-orbit strata."""

import argparse
import itertools
import json
from pathlib import Path

from pysat.solvers import Solver

from generate_proofs import (
    ORDER,
    clauses_from_masks,
    degree_feasible,
    edge_orbits,
    five_set_masks,
    orbit_count,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbits", type=int, nargs="+", required=True)
    parser.add_argument("--candidate", type=Path, default=Path("candidate.json"))
    args = parser.parse_args()
    strata = set(args.orbits)
    types = [
        parts
        for parts in itertools.combinations_with_replacement(range(1, ORDER + 1), 4)
        if sum(parts) == ORDER and orbit_count(parts) in strata and degree_feasible(parts)
    ]
    print(f"screen_strata={','.join(map(str, sorted(strata)))} feasible_types={len(types)}", flush=True)
    for index, parts in enumerate(types, start=1):
        orbits = edge_orbits(parts)
        masks = five_set_masks(orbits)
        clauses = clauses_from_masks(masks, len(orbits))
        with Solver(name="glucose42", bootstrap_with=clauses) as solver:
            satisfiable = solver.solve()
            model = solver.get_model() if satisfiable else None
        print(
            f"case={index}/{len(types)} cycle_type={'+'.join(map(str, parts))} "
            f"variables={len(orbits)} clauses={len(clauses)} "
            f"result={'SAT' if satisfiable else 'UNSAT'}",
            flush=True,
        )
        if satisfiable:
            if model is None:
                raise AssertionError("SAT result omitted model")
            truth = {abs(literal): literal > 0 for literal in model}
            if any(
                not any((literal > 0) == truth[abs(literal)] for literal in clause)
                for clause in clauses
            ):
                raise AssertionError("model does not satisfy reconstructed CNF")
            red_edges = [
                list(edge)
                for variable, orbit in enumerate(orbits)
                if truth[variable + 1]
                for edge in orbit
            ]
            args.candidate.write_text(
                json.dumps(
                    {"cycle_type": list(parts), "order": ORDER, "red_edges": red_edges},
                    indent=2,
                    sort_keys=True,
                )
                + "\n"
            )
            print(f"TARGET_CANDIDATE={args.candidate}", flush=True)
            raise SystemExit(10)
    print(f"PASS all {len(types)} selected feasible types returned UNSAT", flush=True)


if __name__ == "__main__":
    main()
