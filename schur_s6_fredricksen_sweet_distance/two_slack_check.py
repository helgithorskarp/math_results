"""Exact standard-library checker for a 54-edit S(6) baseline obstruction.

The original certificate supplies 51 disjoint mandatory edit groups. The
51-edit and 52-edit cases are already excluded. At 53 edits, choose two slack
positions. Nested refutation cores reduce the possible pairs to a finite
list, whose exact Schur instances are checked by exhaustive branching.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor

from one_slack_check import (
    COLORS,
    ExhaustiveCheck,
    certificate_groups,
    choose_variable,
    clauses_for,
    dpll_controls,
    mandatory_groups,
    require,
    unit_core,
    variable,
)


def propagate_with_reasons(clauses: list[list[int]],
                           assumptions: dict[int, bool]
                           ) -> tuple[set[int] | None, list[list[int]] | None]:
    """Return a unit-conflict core, or the residual clauses if open."""
    assignment = dict(assumptions)
    reason: dict[int, int] = {}
    while True:
        changes = 0
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
                return core, None
            if len(pending) == 1:
                literal = pending[0]
                assignment[abs(literal)] = literal > 0
                reason[abs(literal)] = index
                changes += 1
        if changes == 0:
            residual = []
            for clause in clauses:
                if any(assignment.get(abs(literal)) == (literal > 0)
                       for literal in clause):
                    continue
                residual.append([literal for literal in clause
                                 if abs(literal) not in assignment])
            return None, residual


def branching_core(clauses: list[list[int]],
                   assumptions: dict[int, bool] | None = None) -> set[int]:
    """Union the unit-conflict cores of both sides of every binary branch."""
    if assumptions is None:
        assumptions = {}
    core, residual = propagate_with_reasons(clauses, assumptions)
    if core is not None:
        return core
    require(residual is not None and residual, "one-slack case is satisfiable")
    v, preferred = choose_variable(residual)
    left = branching_core(clauses, {**assumptions, v: preferred})
    right = branching_core(clauses, {**assumptions, v: not preferred})
    return left | right


def verified_core(clauses: list[list[int]]) -> tuple[set[int], bool]:
    try:
        return unit_core(clauses), False
    except ValueError as error:
        if str(error) != "no unit contradiction in 51-edit case":
            raise
    core = branching_core(clauses)
    require(not ExhaustiveCheck().satisfiable(
        [clauses[index] for index in sorted(core)]),
        "extracted branching core does not refute")
    return core, True


def two_slack_clauses(baseline: list[int], c: int,
                      groups: list[list[int]], j: int, k: int
                      ) -> list[list[int]]:
    require(1 <= j < k <= 536, "bad slack pair")
    slack = {j, k}
    free = {v for group in groups for v in group} | slack
    colour = baseline + [c]
    clauses: list[list[int]] = []
    for v in sorted(free):
        clauses.append([variable(v, d) for d in COLORS])
        for d in COLORS:
            for e in range(1, d):
                clauses.append([-variable(v, d), -variable(v, e)])
    for v in sorted(slack):
        clauses.append([-variable(v, baseline[v])])
    for group in groups:
        # Keep both the original at-least-one clause and, for either slack
        # position in the group, the one-slack clause. Thus a core from a
        # one-slack case survives literally unless a tagged dependency moves.
        clauses.append([-variable(v, baseline[v]) for v in group])
        for s in sorted(slack & set(group)):
            clauses.append([-variable(v, baseline[v])
                            for v in group if v != s])
        regular = [v for v in group if v not in slack]
        if len(regular) < len(group):
            clauses.append([-variable(v, baseline[v]) for v in regular])
        for i, v in enumerate(regular):
            for w in regular[:i]:
                clauses.append([variable(v, baseline[v]),
                                variable(w, baseline[w])])

    # Substitute fixed colours in every classical Schur triple, including
    # x=y. A repeated summand contributes two distinct vertices.
    for x in range(1, 538):
        for y in range(x, 538 - x):
            vertices = {x, y, x + y}
            fixed = vertices - free
            for d in COLORS:
                if any(colour[v] != d for v in fixed):
                    continue
                clause = sorted(-variable(v, d) for v in vertices & free)
                require(clause, f"fixed monochromatic triple {(x, y, x + y)}")
                clauses.append(clause)
    return clauses


_WORKER_DATA: tuple[list[int], dict[int, list[tuple[int, int]]],
                    dict[int, list[list[int]]]] | None = None


def worker_init() -> None:
    global _WORKER_DATA
    _WORKER_DATA = certificate_groups()


def check_pair(case: tuple[int, int, int]) -> tuple[int, int, int, int, int]:
    require(_WORKER_DATA is not None, "worker was not initialized")
    baseline, pairs, supports = _WORKER_DATA
    c, j, k = case
    groups = mandatory_groups(pairs, supports, c)
    clauses = two_slack_clauses(baseline, c, groups, j, k)
    search = ExhaustiveCheck()
    require(not search.satisfiable(clauses),
            f"possible 537-colouring with colour {c}, slack {j},{k}")
    return c, j, k, search.nodes, search.maximum_depth


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    if not 1 <= args.workers <= 16:
        parser.error("--workers must be in 1..16")
    dpll_controls()
    baseline, pairs, supports = certificate_groups()
    require({c: len(pairs[c]) + len(supports[c]) for c in COLORS} ==
            {1: 64, 2: 51, 3: 55, 4: 51, 5: 51, 6: 51},
            "unexpected first-stage distance bounds")
    cases: list[tuple[int, int, int]] = []
    for c in (2, 4, 5, 6):
        groups = mandatory_groups(pairs, supports, c)
        original, metadata = clauses_for(baseline, c, groups, None)
        first_core = unit_core(original)
        first = sorted({v for index in first_core for v in metadata[index]})
        pairs_to_check: set[tuple[int, int]] = set()
        branching_first = 0
        for j in first:
            one_slack, tags = clauses_for(baseline, c, groups, j)
            core, branched = verified_core(one_slack)
            branching_first += branched
            for k in {v for index in core for v in tags[index]}:
                if k != j:
                    pairs_to_check.add(tuple(sorted((j, k))))
        print(f"colour={c} first_slack={len(first)} "
              f"branching_first={branching_first} "
              f"candidate_pairs={len(pairs_to_check)}", flush=True)
        cases.extend((c, j, k) for j, k in sorted(pairs_to_check))

    results: list[tuple[int, int, int, int, int]] = []
    with ProcessPoolExecutor(max_workers=args.workers,
                             initializer=worker_init) as pool:
        for row in pool.map(check_pair, cases):
            results.append(row)
            if len(results) % 200 == 0:
                print(f"checked={len(results)}/{len(cases)}", flush=True)
    for c in (2, 4, 5, 6):
        rows = [row for row in results if row[0] == c]
        print(f"colour={c} checked_pairs={len(rows)} "
              f"branching_cases={sum(row[3] > 1 for row in rows)} "
              f"max_nodes={max(row[3] for row in rows)}", flush=True)
    print("PASS distance_at_least=54", flush=True)


if __name__ == "__main__":
    main()
