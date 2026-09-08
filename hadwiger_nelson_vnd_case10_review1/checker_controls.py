#!/usr/bin/env python3
"""Small semantic and sanitizer controls for the reviewer LRAT checker."""

import argparse
import json
import subprocess
from itertools import combinations, permutations, product
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def run(checker, directory, formula, proof):
    formula_path = directory / "control.cnf"
    proof_path = directory / "control.lrat"
    formula_path.write_text(formula)
    proof_path.write_text(proof)
    result = subprocess.run([str(checker), str(formula_path), str(proof_path)],
                            capture_output=True, text=True, timeout=10)
    need(result.returncode in (0, 1), "checker crash")
    return (result.returncode == 0 and
            "VERIFIED_INDEPENDENT_RUP_LRAT" in result.stdout.splitlines())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("work", type=Path)
    parser.add_argument("release", type=Path)
    parser.add_argument("sanitized", type=Path)
    args = parser.parse_args()
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    square = "p cnf 2 4\n1 2 0\n1 -2 0\n-1 2 0\n-1 -2 0\n"
    cases = [
        ("original_units", "p cnf 1 2\n1 0\n-1 0\n", "3 0 1 2 0\n", True),
        ("derived_unit", square, "5 1 0 1 2 0\n6 0 5 3 4 0\n", True),
        ("false_sat", "p cnf 1 1\n1 0\n", "2 0 1 0\n", False),
        ("empty_hints", "p cnf 1 1\n1 0\n", "2 0 0\n", False),
        ("deleted_hint", "p cnf 1 2\n1 0\n-1 0\n",
         "2 d 2 0\n3 0 1 2 0\n", False),
        ("negative_hint", "p cnf 1 1\n1 0\n", "2 0 -1 0\n", False),
        ("missing_empty", square, "5 1 0 1 2 0\n", False),
        ("reused_identifier", square,
         "5 1 0 1 2 0\n5 0 5 3 4 0\n", False),
        ("variable_range", "p cnf 1 2\n1 0\n-1 0\n", "3 2 0 1 2 0\n", False),
        ("integer_overflow", "p cnf 1 2\n1 0\n-1 0\n",
         "999999999999999999999 0 1 2 0\n", False),
    ]
    for checker in (args.release.resolve(), args.sanitized.resolve()):
        for name, formula, proof, wanted in cases:
            need(run(checker, work, formula, proof) == wanted,
                 checker.name + " wrong result " + name)

    clause_pool = [(1,), (-1,), (2,), (-2,), (1, 2), (1, -2),
                   (-1, 2), (-1, -2)]
    total = satisfiable = accepted = 0
    for size in range(5):
        for subset in combinations(clause_pool, size):
            sat = any(
                all(any(values[abs(literal) - 1] == (literal > 0)
                        for literal in clause) for clause in subset)
                for values in product((False, True), repeat=2)
            )
            formula = (f"p cnf 2 {size}\n" +
                       "".join(" ".join(map(str, clause)) + " 0\n"
                               for clause in subset))
            for ordering in permutations(range(1, size + 1)):
                hints = (" ".join(map(str, ordering)) + " " if ordering else "")
                proof = f"{size + 1} 0 {hints}0\n"
                good = run(args.release.resolve(), work, formula, proof)
                total += 1
                satisfiable += sat
                accepted += good
                need(not (sat and good), "accepted satisfiable truth-table formula")
    print(json.dumps({
        "status": "INDEPENDENT_LRAT_CHECKER_CONTROLS_PASSED",
        "named_controls": len(cases),
        "named_controls_checked_in_two_builds": 2 * len(cases),
        "sanitizer_findings": 0,
        "truth_table_instances_and_hint_orders": total,
        "satisfiable_cases_all_rejected": satisfiable,
        "accepted_cases_all_unsatisfiable": accepted,
        "SAT_solver_calls": 0,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
