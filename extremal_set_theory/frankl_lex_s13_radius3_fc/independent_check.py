#!/usr/bin/env python3
"""Independent direct SCIP formulation of the three Poonen inequalities."""

from __future__ import annotations

import argparse
import json

from pyscipopt import Model, quicksum

import verify


def check(name: str) -> dict[str, object]:
    added, weights = verify.REPRESENTATIVES[name]
    model = Model(f"poonen_{name}")
    model.hideOutput()
    model.setIntParam("parallel/maxnthreads", 1)
    variables = [model.addVar(vtype="B", name=f"x_{subset}") for subset in verify.SUBSETS]

    stability = 0
    for subset in verify.SUBSETS:
        for generator in verify.L13 + added:
            target = subset | generator
            if target != subset:
                model.addCons(variables[subset] <= variables[target])
                stability += 1

    unions = 0
    for left in verify.SUBSETS:
        for right in range(left + 1, 1 << verify.N):
            union = left | right
            if union != right:
                model.addCons(
                    variables[left] + variables[right] <= 1 + variables[union]
                )
                unions += 1

    coefficients = verify.poonen_coefficients(weights)
    model.addCons(
        quicksum(coefficients[subset] * variables[subset] for subset in verify.SUBSETS)
        <= -1
    )
    model.setObjective(0)
    model.optimize()
    status = str(model.getStatus())
    if status != "infeasible":
        raise AssertionError(f"{name}: expected infeasible, got {status}")
    return {
        "case": name,
        "nodes": int(model.getNNodes()),
        "status": status,
        "stability_constraints": stability,
        "union_constraints": unions,
        "weights": list(weights),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=tuple(verify.REPRESENTATIVES))
    args = parser.parse_args()
    verify.verify_structure()
    names = (args.case,) if args.case else tuple(verify.REPRESENTATIVES)
    print(json.dumps([check(name) for name in names], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
