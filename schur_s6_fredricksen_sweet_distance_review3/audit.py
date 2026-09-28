#!/usr/bin/env python3
"""Independent one-slack audit for the 53-edit S(6) local obstruction."""

import importlib.util
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "schur_s6_fredricksen_sweet_distance"
PRIOR = HERE.parent / "schur_s6_fredricksen_sweet_distance_review2" / "audit.py"
spec = importlib.util.spec_from_file_location("prior_distance_audit", PRIOR)
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def var(v, colour):
    return 6 * (v - 1) + colour


def read_input():
    digits = (SOURCE / "baseline.txt").read_text(encoding="ascii").strip()
    require(len(digits) == 536 and set(digits) == set("123456"),
            "bad baseline")
    base = [0] + list(map(int, digits))
    data = json.loads((SOURCE / "certificate.json").read_text())
    require(data["target"] == 537, "wrong target")
    edges = prior.schur_edges()
    for edge in edges:
        if edge[-1] <= 536:
            require(len({base[v] for v in edge}) > 1,
                    "baseline is not sum-free")
    return base, data, edges


def groups_for(base, data, colour):
    groups, free, witnesses = prior.groups_for(
        base, data["selected_by_color"][str(colour)], colour)
    require(len(groups) == 51 and len(free) == sum(map(len, groups)),
            "wrong disjoint mandatory groups")
    return groups, free, witnesses


def clauses_for(base, edges, colour, groups, free, slack=None):
    """Exact constraints; core dependencies are valid for one-slack changes."""
    require(slack is None or 1 <= slack <= 536, "bad slack position")
    free = free | ({slack} if slack is not None else set())
    assigned = base + [colour]
    rows = []

    def add(clause, sensitive=()):
        rows.append((tuple(clause), tuple(sensitive)))

    for v in sorted(free):
        add([var(v, d) for d in range(1, 7)])
        for d in range(1, 7):
            for e in range(1, d):
                add([-var(v, d), -var(v, e)])
    if slack is not None:
        add([-var(slack, base[slack])])
    for group in groups:
        active = [v for v in group if v != slack]
        # A slack edit inside a group is its second edit. Among the other
        # vertices there must be exactly one edit, just as in every other group.
        if not active:
            add([])
            continue
        add([-var(v, base[v]) for v in active])
        for i, v in enumerate(active):
            for w in active[:i]:
                add([var(v, base[v]), var(w, base[w])], (v, w))
    for edge in edges:
        fixed = [v for v in edge if v not in free]
        changing = [v for v in edge if v in free]
        for d in range(1, 7):
            if any(assigned[v] != d for v in fixed):
                continue
            require(changing, "fixed monochromatic triple")
            add([-var(v, d) for v in changing],
                (v for v in fixed if v <= 536))
    return rows


def unit_core(rows):
    assignment = {}
    reason = {}
    while True:
        changed = False
        for index, (clause, _) in enumerate(rows):
            if any(assignment.get(abs(lit)) == (lit > 0)
                   for lit in clause):
                continue
            pending = [lit for lit in clause if abs(lit) not in assignment]
            if not pending:
                core = set()
                stack = [index]
                while stack:
                    i = stack.pop()
                    if i in core:
                        continue
                    core.add(i)
                    stack.extend(reason[abs(lit)] for lit in rows[i][0]
                                 if abs(lit) in reason)
                require(unit_refutes([rows[i][0] for i in sorted(core)]),
                        "unit core does not refute")
                return core
            if len(pending) == 1:
                lit = pending[0]
                assignment[abs(lit)] = lit > 0
                reason[abs(lit)] = index
                changed = True
        require(changed, "no no-slack unit contradiction")


def unit_refutes(clauses):
    assignment = {}
    while True:
        changes = {}
        for clause in clauses:
            if any(assignment.get(abs(lit)) == (lit > 0)
                   for lit in clause):
                continue
            pending = [lit for lit in clause if abs(lit) not in assignment]
            if not pending:
                return True
            if len(pending) == 1:
                lit = pending[0]
                old = changes.get(abs(lit))
                if old is not None and old != (lit > 0):
                    return True
                changes[abs(lit)] = lit > 0
        if not changes:
            return False
        assignment.update(changes)


def simplify(clauses, assignment):
    while True:
        residual = []
        units = {}
        for clause in clauses:
            if any(assignment.get(abs(lit)) == (lit > 0)
                   for lit in clause):
                continue
            pending = tuple(lit for lit in clause
                            if abs(lit) not in assignment)
            if not pending:
                return None
            if len(pending) == 1:
                lit = pending[0]
                old = units.get(abs(lit))
                if old is not None and old != (lit > 0):
                    return None
                units[abs(lit)] = lit > 0
            else:
                residual.append(pending)
        if not units:
            return residual
        assignment.update(units)
        clauses = residual


def choose_literal(clauses):
    scores = Counter()
    signs = Counter()
    for clause in clauses:
        weight = 16 if len(clause) == 2 else 4 if len(clause) == 3 else 1
        for lit in clause:
            scores[abs(lit)] += weight
            signs[lit] += weight
    v = max(scores, key=lambda x: (scores[x], -x))
    return v, signs[v] >= signs[-v]


def satisfiable(clauses, assignment=None, stats=None, depth=0):
    if assignment is None:
        assignment = {}
    if stats is None:
        stats = [0, 0]
    stats[0] += 1
    stats[1] = max(stats[1], depth)
    residual = simplify(clauses, assignment)
    if residual is None:
        return False
    if not residual:
        return True
    v, first = choose_literal(residual)
    for value in (first, not first):
        if satisfiable(residual, {**assignment, v: value}, stats, depth + 1):
            return True
    return False


def dpll_controls():
    universe = ((1,), (-1,), (2,), (-2,),
                (1, 2), (1, -2), (-1, 2), (-1, -2))
    for mask in range(1 << len(universe)):
        clauses = [clause for i, clause in enumerate(universe)
                   if mask & (1 << i)]
        expected = any(
            all(any(values[abs(lit)] == (lit > 0) for lit in clause)
                for clause in clauses)
            for values in ({1: a, 2: b} for a in (False, True)
                           for b in (False, True)))
        require(satisfiable(clauses) == expected,
                f"DPLL disagrees with truth table at mask {mask}")


def main():
    dpll_controls()
    base, data, edges = read_input()
    total_cases = total_witnesses = 0
    expected_clauses = {2: 57349, 4: 97660, 5: 169996, 6: 131512}
    for colour in (2, 4, 5, 6):
        groups, free, witnesses = groups_for(base, data, colour)
        total_witnesses += witnesses
        rows = clauses_for(base, edges, colour, groups, free)
        require(len(rows) == expected_clauses[colour],
                "no-slack encoding disagrees in clause count")
        core = unit_core(rows)
        sensitive = {v for i in core for v in rows[i][1]}
        require(len(sensitive) <= 536, "invalid sensitivity count")
        # Every core clause has a specific origin: one-hot and group-need
        # clauses persist; group pair clauses can disappear only when slack
        # is an endpoint; Schur clauses can weaken only when slack was fixed.
        # The recorded dependency sets therefore cover all ways to remove
        # the verified no-slack contradiction.
        print(f"colour={colour} core={len(core)} sensitive={len(sensitive)}",
              flush=True)
        branch_cases = max_nodes = 0
        for slack in sorted(sensitive):
            case = clauses_for(base, edges, colour, groups, free, slack)
            stats = [0, 0]
            require(not satisfiable([clause for clause, _ in case],
                                    stats=stats),
                    f"colourable one-slack case {(colour, slack)}")
            branch_cases += stats[0] > 1
            max_nodes = max(max_nodes, stats[0])
        total_cases += len(sensitive)
        print(f"colour={colour} checked={len(sensitive)} "
              f"branching={branch_cases} max_nodes={max_nodes}", flush=True)
    require(total_witnesses == 560, "witness count mismatch")
    print(f"PASS independent_distance_at_least=53 checked_cases={total_cases}")


if __name__ == "__main__":
    main()
