#!/usr/bin/env python3
"""Definition-level controls for the compact physical/DRAT certificate checker."""
import argparse
from itertools import product
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from check_certificate import physical_core, require, rup, verify_proof


def satisfying(database, n):
    for values in product((False, True), repeat=n):
        if all(any(values[abs(x) - 1] == (x > 0) for x in row) for row in database):
            yield values


def reject(function):
    try:
        function()
    except ValueError:
        return
    raise RuntimeError("A deliberately invalid certificate was accepted")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("core", type=Path)
    parser.add_argument("proof", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    possible = [frozenset((i + 1) * sign for i, sign in enumerate(signs) if sign)
                for signs in product((-1, 0, 1), repeat=2)]
    candidates = []
    for signs in product((-1, 0, 1), repeat=3):
        row = frozenset((i + 1) * sign for i, sign in enumerate(signs) if sign)
        for pivot in row:
            candidates.append((row, pivot))
    rup_checks = rat_checks = accepted_rat = 0
    for mask in range(1 << len(possible)):
        database = {row for j, row in enumerate(possible) if mask >> j & 1}
        models = list(satisfying(database, 3))
        for row, pivot in candidates:
            if rup(database, row):
                require(all(any(values[abs(x)-1] == (x > 0) for x in row) for values in models),
                        "RUP accepted a non-implication")
            rup_checks += 1
            is_rat = all(rup(database, row | (other - {-pivot}))
                         for other in database if -pivot in other)
            if is_rat:
                accepted_rat += 1
                require(not models or bool(list(satisfying(database | {row}, 3))),
                        "RAT failed satisfiability preservation")
            rat_checks += 1
    with TemporaryDirectory(prefix="paley-certificate-controls-") as tmp:
        damaged = Path(tmp) / "input"
        # Multiplicity matters: one of two identical added unit clauses remains.
        square = {frozenset(row) for row in ((1, 2), (-1, 2), (1, -2), (-1, -2))}
        damaged.write_text("1 0\n1 0\nd 1 0\n0\n")
        require(verify_proof(square, damaged)["additions"] == 3, "Multiset regression failed")
        # A RAT-only first step with a new pivot, then a genuinely RUP refutation.
        damaged.write_text("3 0\n1 0\n0\n")
        require(verify_proof(square, damaged)["rat_additions"] == 1, "Fresh-variable RAT failed")
        damaged.write_text("0\n")
        reject(lambda: verify_proof({frozenset((1, 2))}, damaged))
        damaged.write_text("1 0\n")
        reject(lambda: verify_proof(square, damaged))  # Missing the empty clause.
        damaged.write_text(args.proof.read_text().rsplit("\n0\n", 1)[0] + "\n")
        database, _ = physical_core(args.core)
        reject(lambda: verify_proof(database, damaged))
        damaged.write_text("0\n" + args.proof.read_text())
        reject(lambda: verify_proof(database, damaged))
        # Corrupt each of the first six physical clauses by moving a variable
        # outside the core. These are independent of the downstream proof.
        lines = args.core.read_text().splitlines()
        for i in range(1, 7):
            altered = lines.copy()
            words = altered[i].split()
            words[0] = "41"
            altered[i] = " ".join(words)
            damaged.write_text("\n".join(altered) + "\n")
            reject(lambda: physical_core(damaged))
        # A well-formed but false physical condition, not just malformed syntax.
        # On vertices 0,1,2,3,4 the all-zero spin is not monochromatic in Paley41.
        damaged.write_text("p cnf 123 1\n1 2 3 4 0\n")
        reject(lambda: physical_core(damaged))
    report = {"status": "PASS", "two_variable_formulas": 512,
              "rup_semantic_checks": rup_checks, "rat_semantic_checks": rat_checks,
              "accepted_rat_cases": accepted_rat, "negative_tests_rejected": 11,
              "positive_proof_tests": 2}
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
