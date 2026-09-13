#!/usr/bin/env python3
"""Generate logically independent selectors for Q5 counts 0 through 6.

For a 134-element selection X from S union Q5, where |S|=135,

    |X intersect Q5| = q  iff  q Q5 points are selected and q+1 S points
    are deleted.

We encode those two small exact counts with a unary threshold recurrence,
not the reviewed package's binary ripple counters.  The killing-set clauses
are shared mathematical data: each clause says X intersects the deletion set
of one explicitly checked four-colourable complement.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BUDGET = ROOT / "hadwiger_nelson_parts509_s_replacement_budget"
TARGET = ROOT / "hadwiger_nelson_parts509_five_four_swap_search"


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


class CNF:
    def __init__(self, selectors: int):
        self.variables = selectors
        self.clauses: list[list[int]] = []

    def new(self) -> int:
        self.variables += 1
        return self.variables

    def conjunction(self, output: int, first: int, second: int) -> None:
        self.clauses.extend([
            [-output, first], [-output, second],
            [output, -first, -second],
        ])

    def disjunction(self, output: int, first: int, second: int) -> None:
        self.clauses.extend([
            [-first, output], [-second, output],
            [first, second, -output],
        ])

    def exact_threshold_count(self, literals: list[int], target: int) -> None:
        """Pin an insertion-style unary threshold network to an exact count."""
        need(0 <= target <= len(literals), "invalid exact-count target")
        if target == 0:
            self.clauses.extend([[-literal] for literal in literals])
            return
        limit = min(target + 1, len(literals))
        previous: list[int] = []
        for literal in literals:
            current: list[int] = []
            length = min(len(previous) + 1, limit)
            for index in range(length):
                if index == 0:
                    if not previous:
                        current.append(literal)
                    else:
                        output = self.new()
                        self.disjunction(output, previous[0], literal)
                        current.append(output)
                elif index == len(previous):
                    output = self.new()
                    self.conjunction(output, previous[index - 1], literal)
                    current.append(output)
                else:
                    product = self.new()
                    self.conjunction(product, previous[index - 1], literal)
                    output = self.new()
                    self.disjunction(output, previous[index], product)
                    current.append(output)
            previous = current
        self.clauses.append([previous[target - 1]])
        if len(previous) > target:
            self.clauses.append([-previous[target]])

    def dimacs(self) -> bytes:
        lines = [f"p cnf {self.variables} {len(self.clauses)}\n"]
        lines.extend(" ".join(map(str, clause)) + " 0\n"
                     for clause in self.clauses)
        return "".join(lines).encode()


def dpll(clauses: list[list[int]], assignment: dict[int, bool]) -> bool:
    clauses = [list(clause) for clause in clauses]
    assignment = dict(assignment)
    while True:
        changed = False
        for clause in clauses:
            if any(assignment.get(abs(lit)) == (lit > 0) for lit in clause):
                continue
            live = [lit for lit in clause if abs(lit) not in assignment]
            if not live:
                return False
            if len(live) == 1:
                literal = live[0]
                value = literal > 0
                old = assignment.get(abs(literal))
                if old is not None and old != value:
                    return False
                if old is None:
                    assignment[abs(literal)] = value
                    changed = True
        if not changed:
            break
    if all(any(assignment.get(abs(lit)) == (lit > 0) for lit in clause)
           for clause in clauses):
        return True
    variable = next(abs(lit) for clause in clauses for lit in clause
                    if abs(lit) not in assignment)
    return (dpll(clauses, assignment | {variable: False})
            or dpll(clauses, assignment | {variable: True}))


def controls() -> int:
    checks = 0
    # Positive and negative literals exercise both selector conventions.
    for size in range(1, 7):
        for signs in (1, -1):
            literals = [signs * (i + 1) for i in range(size)]
            for target in range(size + 1):
                cnf = CNF(size)
                cnf.exact_threshold_count(literals, target)
                for bits in itertools.product((False, True), repeat=size):
                    assignment = {i + 1: bits[i] for i in range(size)}
                    literal_sum = sum(
                        assignment[abs(literal)] == (literal > 0)
                        for literal in literals
                    )
                    need(dpll(cnf.clauses, assignment)
                         == (literal_sum == target),
                         "threshold-counter control failed")
                    checks += 1
    return checks


def build(pool: list[int], q5: list[int], killing: list[list[int]], q: int) -> CNF:
    index = {label: i + 1 for i, label in enumerate(pool)}
    need(len(index) == len(pool), "repeated pool label")
    s = list(range(374, 509))
    need(set(pool) == set(s) | set(q5) and not (set(s) & set(q5)),
         "pool is not S disjoint-union Q5")
    cnf = CNF(len(pool))
    cnf.exact_threshold_count([index[label] for label in q5], q)
    cnf.exact_threshold_count([-index[label] for label in s], q + 1)
    cnf.clauses.extend([[index[label] for label in row] for row in killing])
    return cnf


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    pool_data = json.loads((BUDGET / "pool_S.json").read_text())
    certificate = json.loads((TARGET / "certificate.json").read_text())
    pool = sorted(pool_data["W_S"])
    q5 = sorted(pool_data["Q5"])
    killing = [row["D"] for row in certificate["killing_sets"]]
    need(certificate["pool"] == pool and certificate["Q5"] == q5,
         "certificate does not match pool data")
    control_checks = controls()
    summaries = {}
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
    for q in range(7):
        dimacs = build(pool, q5, killing, q).dimacs()
        header = dimacs.splitlines()[0].split()
        digest = hashlib.sha256(dimacs).hexdigest()
        summaries[str(q)] = {
            "variables": int(header[2]),
            "clauses": int(header[3]),
            "bytes": len(dimacs),
            "sha256": digest,
        }
        if args.out:
            (args.out / f"independent_q{q}.cnf").write_bytes(dimacs)
    print(json.dumps({
        "status": "INDEPENDENT_SELECTORS_GENERATED",
        "encoding": "unary threshold counts on selected Q5 and deleted S",
        "counter_control_checks": control_checks,
        "selectors": summaries,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"independent selector generation failed: {error}")
        raise SystemExit(1)
