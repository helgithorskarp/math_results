#!/usr/bin/env python3
"""Brute-force controls for the independent DPLL decision procedure."""
from itertools import product
import json

from dpll_check import decide


def all_clauses(n):
    clauses = []
    for states in product((-1, 0, 1), repeat=n):
        if all(x == 0 for x in states):
            continue
        pos = sum(1 << i for i, x in enumerate(states) if x == 1)
        neg = sum(1 << i for i, x in enumerate(states) if x == -1)
        clauses.append((pos, neg))
    return clauses


def brute(n, clauses):
    for assignment in range(1 << n):
        if all((pos & assignment) or (neg & ~assignment) for pos, neg in clauses):
            return True
    return False


def main():
    tested = 0
    # Exhaust 4096 clause-subsets from three differently ordered 12-clause pools.
    universe = all_clauses(3)
    for offset in (0, 7, 14):
        pool = tuple(universe[(offset + i) % len(universe)] for i in range(12))
        for mask in range(1 << len(pool)):
            clauses = tuple(pool[i] for i in range(len(pool)) if mask >> i & 1)
            got, _ = decide(3, clauses)
            want = brute(3, clauses)
            if got != want:
                raise AssertionError((offset, mask, got, want, clauses))
            tested += 1
    # Empty clause and the complete eight-assignment blocker are explicit UNSAT controls.
    for clauses in (((0, 0),), tuple((0, 0) for _ in range(2))):
        got, _ = decide(3, clauses)
        if got:
            raise AssertionError("empty-clause control")
        tested += 1
    blockers = []
    for assignment in range(8):
        pos = sum(1 << i for i in range(3) if not (assignment >> i & 1))
        neg = sum(1 << i for i in range(3) if assignment >> i & 1)
        blockers.append((pos, neg))
    got, _ = decide(3, tuple(blockers))
    if got:
        raise AssertionError("complete assignment blocker")
    tested += 1
    print(json.dumps({"status": "DPLL_CONTROLS_PASSED",
                      "three_variable_formulas_checked": tested,
                      "literal_assignments_per_bruteforce": 8},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
