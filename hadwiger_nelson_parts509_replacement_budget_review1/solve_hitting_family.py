#!/usr/bin/env python3
"""Independently solve the published S-killing-set hitting family.

The target used PySAT RC2.  This review model instead supports OR-Tools CP-SAT,
SciPy/HiGHS, or OR-Tools' SCIP/SoPlex backend.  Solver optimality remains an
explicitly imported trust boundary; every returned integer witness is checked
directly against the JSON family before it is reported.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from pathlib import Path

from verify_hitting_witness import DEFAULT_CERTIFICATE, minimal_family


def validate(selected: list[int], family: list[frozenset[int]], universe: list[int]) -> str:
    chosen = frozenset(selected)
    assert len(chosen) == len(selected)
    assert chosen <= set(universe)
    assert all(item & chosen for item in family)
    canonical = " ".join(map(str, sorted(chosen))) + "\n"
    return hashlib.sha256(canonical.encode()).hexdigest()


def solve_cpsat(
    universe: list[int], family: list[frozenset[int]], workers: int, seed: int
) -> tuple[str, int, list[int], float]:
    from ortools.sat.python import cp_model

    model = cp_model.CpModel()
    variables = {vertex: model.NewBoolVar(f"x_{vertex}") for vertex in universe}
    for item in family:
        model.Add(sum(variables[vertex] for vertex in item) >= 1)
    model.Minimize(sum(variables.values()))
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = seed
    start = time.time()
    status = solver.Solve(model)
    elapsed = time.time() - start
    name = solver.StatusName(status)
    selected = [vertex for vertex in universe if solver.BooleanValue(variables[vertex])]
    value = int(round(solver.ObjectiveValue()))
    return name, value, selected, elapsed


def solve_highs(
    universe: list[int], family: list[frozenset[int]]
) -> tuple[str, int, list[int], float]:
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import lil_matrix

    index = {vertex: column for column, vertex in enumerate(universe)}
    matrix = lil_matrix((len(family), len(universe)))
    for row, item in enumerate(family):
        for vertex in item:
            matrix[row, index[vertex]] = 1
    start = time.time()
    result = milp(
        c=np.ones(len(universe)),
        integrality=np.ones(len(universe)),
        bounds=Bounds(0, 1),
        constraints=LinearConstraint(matrix.tocsr(), lb=np.ones(len(family))),
        options={"mip_rel_gap": 0.0},
    )
    elapsed = time.time() - start
    status = "OPTIMAL" if result.status == 0 else f"STATUS_{result.status}"
    selected = [vertex for vertex in universe if result.x[index[vertex]] > 0.5]
    value = int(round(result.fun))
    return status, value, selected, elapsed


def solve_scip(
    universe: list[int], family: list[frozenset[int]]
) -> tuple[str, int, list[int], float]:
    from ortools.linear_solver import pywraplp

    solver = pywraplp.Solver.CreateSolver("SCIP")
    assert solver is not None
    solver.SetNumThreads(1)
    variables = {vertex: solver.BoolVar(f"x_{vertex}") for vertex in universe}
    for item in family:
        solver.Add(sum(variables[vertex] for vertex in item) >= 1)
    solver.Minimize(sum(variables.values()))
    start = time.time()
    result = solver.Solve()
    elapsed = time.time() - start
    status = "OPTIMAL" if result == pywraplp.Solver.OPTIMAL else f"STATUS_{result}"
    selected = [vertex for vertex in universe if variables[vertex].solution_value() > 0.5]
    value = int(round(solver.Objective().Value()))
    return status, value, selected, elapsed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--solver", choices=("cpsat", "highs", "scip"), required=True)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--seed", type=int, default=20260904)
    args = parser.parse_args()
    assert args.workers >= 1

    certificate = json.loads(args.certificate.read_text())
    universe = list(map(int, certificate["S"]))
    family = minimal_family(certificate["killing_sets"])
    if args.solver == "cpsat":
        status, value, selected, elapsed = solve_cpsat(
            universe, family, args.workers, args.seed
        )
    elif args.solver == "highs":
        status, value, selected, elapsed = solve_highs(universe, family)
    else:
        status, value, selected, elapsed = solve_scip(universe, family)

    assert status == "OPTIMAL", status
    assert value == len(selected)
    digest = validate(selected, family, universe)
    print(
        json.dumps(
            {
                "solver": args.solver,
                "status": status,
                "minimum_hitting_set": value,
                "selected_sha256": digest,
                "seconds": round(elapsed, 3),
                "workers": args.workers if args.solver == "cpsat" else 1,
                "thread_limits": {
                    key: os.environ.get(key)
                    for key in (
                        "OMP_NUM_THREADS",
                        "OPENBLAS_NUM_THREADS",
                        "MKL_NUM_THREADS",
                    )
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
