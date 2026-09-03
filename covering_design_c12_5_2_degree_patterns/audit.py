#!/usr/bin/env python3
"""Independent compact audits of witnesses and the custom CNF encoders."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

from generate_cnf import Builder, build, render
from verify_witnesses import verify


ROOT = Path(__file__).resolve().parent
EXPECTED_CNF_SHA256 = "45d89f7dab2972df4786a806bf67380af5cd7faf93e9125b7516a4332d637def"


def simplify(clauses: list[list[int]], assignment: dict[int, bool]) -> list[list[int]] | None:
    remaining = []
    for clause in clauses:
        if any((literal > 0) == assignment.get(abs(literal))
               for literal in clause if abs(literal) in assignment):
            continue
        reduced = [literal for literal in clause if abs(literal) not in assignment]
        if not reduced:
            return None
        remaining.append(reduced)
    return remaining


def satisfiable(clauses: list[list[int]], assignment: dict[int, bool]) -> bool:
    clauses = [list(clause) for clause in clauses]
    assignment = dict(assignment)
    while True:
        reduced = simplify(clauses, assignment)
        if reduced is None:
            return False
        if not reduced:
            return True
        units = [clause[0] for clause in reduced if len(clause) == 1]
        if not units:
            clauses = reduced
            break
        for literal in units:
            variable, value = abs(literal), literal > 0
            if variable in assignment and assignment[variable] != value:
                return False
            assignment[variable] = value
        clauses = reduced
    variable = abs(min(clauses, key=len)[0])
    return any(satisfiable(clauses, assignment | {variable: value}) for value in (False, True))


def audit_at_most() -> None:
    for size in range(1, 7):
        for bound in range(size + 1):
            formula = Builder()
            primary = [formula.var() for _ in range(size)]
            formula.at_most(primary, bound)
            for bits in itertools.product((False, True), repeat=size):
                actual = satisfiable(formula.clauses, dict(zip(primary, bits)))
                assert actual == (sum(bits) <= bound), (size, bound, bits, actual)


def audit_lex() -> None:
    for size in range(1, 6):
        formula = Builder()
        left = [formula.var() for _ in range(size)]
        right = [formula.var() for _ in range(size)]
        formula.lex_le(left, right)
        for first in itertools.product((False, True), repeat=size):
            for second in itertools.product((False, True), repeat=size):
                assignment = dict(zip(left + right, first + second))
                actual = satisfiable(formula.clauses, assignment)
                assert actual == (first <= second), (size, first, second, actual)


def audit_witnesses() -> None:
    payload = json.loads((ROOT / "witnesses.json").read_text())
    for a in range(4):
        verify(a, payload[str(a)])


def main() -> None:
    audit_at_most()
    audit_lex()
    audit_witnesses()
    data = render(build())
    assert len(data) > 0
    assert hashlib.sha256(data).hexdigest() == EXPECTED_CNF_SHA256
    print(json.dumps({"cnf_sha256": EXPECTED_CNF_SHA256,
                      "small_counter_instances": sum((size + 1) * (1 << size)
                                                     for size in range(1, 7)),
                      "small_lex_pairs": sum(4 ** size for size in range(1, 6)),
                      "witnesses": 4}, sort_keys=True))
    print("audit=PASS")


if __name__ == "__main__":
    main()
