"""Exact standard-library certificate for a 53-edit S(6) baseline obstruction.

The 51 disjoint mandatory groups leave at most one slack edit at distance 52.
A short unit refutation for the no-slack case rules out most slack positions.
The remaining cases are checked by exhaustive binary branching.
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

from saturation_check import certificate_groups, require, unit_refutes

COLORS = range(1, 7)


def variable(v: int, d: int) -> int:
    return (v - 1) * 6 + d


def mandatory_groups(pairs: dict[int, list[tuple[int, int]]],
                     supports: dict[int, list[list[int]]],
                     c: int) -> list[list[int]]:
    groups = [list(pair) for pair in pairs[c]] + supports[c]
    require(len(groups) == 51, f"wrong group count for colour {c}")
    require(len({v for group in groups for v in group}) ==
            sum(map(len, groups)), "mandatory groups overlap")
    return groups


def clauses_for(baseline: list[int], c: int, groups: list[list[int]],
                slack: int | None) -> tuple[list[list[int]], list[tuple[int, ...]]]:
    """Return exact Schur clauses and dependencies on a possible slack edit.

    With slack=None, every group has exactly one edit and all other positions
    are fixed. With slack=j, j is edited in addition to one member of every
    group; if j is inside a group, the group's other member is still required.
    The metadata identifies positions whose slack status can remove a clause.
    """
    require(slack is None or 1 <= slack <= 536, "bad slack position")
    free = {v for group in groups for v in group}
    if slack is not None:
        free.add(slack)
    colour = baseline + [c]
    clauses: list[list[int]] = []
    dependencies: list[tuple[int, ...]] = []

    def add(clause: list[int], deps: tuple[int, ...] = ()) -> None:
        clauses.append(clause)
        dependencies.append(deps)

    for v in sorted(free):
        add([variable(v, d) for d in COLORS])
        for d in COLORS:
            for e in range(1, d):
                add([-variable(v, d), -variable(v, e)])

    if slack is not None:
        add([-variable(slack, baseline[slack])])
    for group in groups:
        # The original group's at-least-one clause remains valid even when
        # slack belongs to the group. This helps compare the two formulas.
        add([-variable(v, baseline[v]) for v in group])
        for i, v in enumerate(group):
            for w in group[:i]:
                if slack in (v, w):
                    continue
                add([variable(v, baseline[v]),
                     variable(w, baseline[w])], (v, w))
        if slack in group:
            add([-variable(v, baseline[v]) for v in group if v != slack])

    # Fixed colours are substituted into every Schur triple on [1,537].
    # A repeated summand gives two distinct positions, not three.
    for x in range(1, 538):
        for y in range(x, 538 - x):
            vertices = {x, y, x + y}
            fixed = vertices - free
            for d in COLORS:
                if any(colour[v] != d for v in fixed):
                    continue
                clause = sorted(-variable(v, d) for v in vertices & free)
                require(clause, f"fixed monochromatic triple {(x, y, x + y)}")
                add(clause, tuple(v for v in fixed if v <= 536))
    return clauses, dependencies


def unit_core(clauses: list[list[int]]) -> set[int]:
    """Trace one unit contradiction back to its premise clauses."""
    assignment: dict[int, bool] = {}
    reason: dict[int, int] = {}
    while True:
        changed = False
        for index, clause in enumerate(clauses):
            pending: list[int] = []
            satisfied = False
            for literal in clause:
                value = assignment.get(abs(literal))
                if value is None:
                    pending.append(literal)
                elif value == (literal > 0):
                    satisfied = True
                    break
            if satisfied:
                continue
            if not pending:
                core: set[int] = set()
                stack = [index]
                while stack:
                    current = stack.pop()
                    if current in core:
                        continue
                    core.add(current)
                    for literal in clauses[current]:
                        antecedent = reason.get(abs(literal))
                        if antecedent is not None:
                            stack.append(antecedent)
                require(unit_refutes([clauses[i] for i in sorted(core)])[0],
                        "extracted core does not refute")
                return core
            if len(pending) == 1:
                literal = pending[0]
                assignment[abs(literal)] = literal > 0
                reason[abs(literal)] = index
                changed = True
        require(changed, "no unit contradiction in 51-edit case")


def simplify(clauses: list[list[int]], assignment: dict[int, bool]
             ) -> list[list[int]] | None:
    """Unit propagation. None denotes a contradictory clause."""
    while True:
        reduced: list[list[int]] = []
        units: dict[int, bool] = {}
        for clause in clauses:
            pending: list[int] = []
            satisfied = False
            for literal in clause:
                value = assignment.get(abs(literal))
                if value is None:
                    pending.append(literal)
                elif value == (literal > 0):
                    satisfied = True
                    break
            if satisfied:
                continue
            if not pending:
                return None
            if len(pending) == 1:
                literal = pending[0]
                v, value = abs(literal), literal > 0
                if v in units and units[v] != value:
                    return None
                units[v] = value
            else:
                reduced.append(pending)
        if not units:
            return reduced
        assignment.update(units)
        clauses = reduced


def choose_variable(clauses: list[list[int]]) -> tuple[int, bool]:
    score: Counter[int] = Counter()
    sign: Counter[int] = Counter()
    for clause in clauses:
        weight = 16 if len(clause) == 2 else 4 if len(clause) == 3 else 1
        for literal in clause:
            score[abs(literal)] += weight
            sign[literal] += weight
    v = max(score, key=lambda candidate: (score[candidate], -candidate))
    return v, sign[v] >= sign[-v]


class ExhaustiveCheck:
    def __init__(self) -> None:
        self.nodes = 0
        self.maximum_depth = 0

    def satisfiable(self, clauses: list[list[int]],
                    assignment: dict[int, bool] | None = None,
                    depth: int = 0) -> bool:
        self.nodes += 1
        self.maximum_depth = max(self.maximum_depth, depth)
        if assignment is None:
            assignment = {}
        residual = simplify(clauses, assignment)
        if residual is None:
            return False
        if not residual:
            return True
        v, preferred = choose_variable(residual)
        for value in (preferred, not preferred):
            if self.satisfiable(residual, {**assignment, v: value}, depth + 1):
                return True
        return False


def dpll_controls() -> None:
    """Compare the checker with direct truth tables for every two-var CNF."""
    universe = [[1], [-1], [2], [-2], [1, 2], [1, -2],
                [-1, 2], [-1, -2]]
    for mask in range(1 << len(universe)):
        clauses = [clause for i, clause in enumerate(universe)
                   if mask & (1 << i)]
        expected = any(all(any((literal > 0) == values[abs(literal)]
                                   for literal in clause) for clause in clauses)
                       for values in ({1: a, 2: b}
                                      for a in (False, True)
                                      for b in (False, True)))
        require(ExhaustiveCheck().satisfiable(clauses) == expected,
                f"DPLL disagrees with truth table for mask {mask}")


_WORKER_DATA: tuple[list[int], dict[int, list[tuple[int, int]]],
                    dict[int, list[list[int]]]] | None = None


def worker_init() -> None:
    global _WORKER_DATA
    _WORKER_DATA = certificate_groups()


def check_case(case: tuple[int, int]) -> tuple[int, int, int, int]:
    require(_WORKER_DATA is not None, "worker was not initialized")
    baseline, pairs, supports = _WORKER_DATA
    c, j = case
    groups = mandatory_groups(pairs, supports, c)
    clauses, _ = clauses_for(baseline, c, groups, j)
    search = ExhaustiveCheck()
    require(not search.satisfiable(clauses),
            f"possible 537-colouring with colour {c}, slack {j}")
    return c, j, search.nodes, search.maximum_depth


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if not 1 <= args.workers <= 16:
        parser.error("--workers must be in 1..16")
    dpll_controls()
    baseline, pairs, supports = certificate_groups()
    require({c: len(pairs[c]) + len(supports[c]) for c in COLORS} ==
            {1: 64, 2: 51, 3: 55, 4: 51, 5: 51, 6: 51},
            "unexpected first-stage distance bounds")
    cases: list[tuple[int, int]] = []
    for c in (2, 4, 5, 6):
        groups = mandatory_groups(pairs, supports, c)
        clauses, metadata = clauses_for(baseline, c, groups, None)
        core = unit_core(clauses)
        sensitive = {v for index in core for v in metadata[index]}
        require(all(1 <= v <= 536 for v in sensitive), "bad core metadata")
        print(f"colour={c} unit_core_clauses={len(core)} "
              f"slack_cases={len(sensitive)}", flush=True)
        cases.extend((c, j) for j in sorted(sensitive))

    results: list[tuple[int, int, int, int]] = []
    with ProcessPoolExecutor(max_workers=args.workers,
                             initializer=worker_init) as pool:
        for row in pool.map(check_case, cases):
            results.append(row)
    for c in (2, 4, 5, 6):
        rows = [row for row in results if row[0] == c]
        print(f"colour={c} checked_slack={len(rows)} "
              f"branching_cases={sum(row[2] > 1 for row in rows)} "
              f"max_nodes={max(row[2] for row in rows)}", flush=True)
    print("PASS distance_at_least=53", flush=True)


if __name__ == "__main__":
    main()
