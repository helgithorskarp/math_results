#!/usr/bin/env python3
"""Truth-table and propagation controls for the degree stratifier."""
from itertools import product
import json
import stratify


def need(ok, message):
    if not ok:
        raise ValueError(message)


def satisfied(clause, values):
    return any(values[abs(lit)] == (lit > 0) for lit in clause)


def propagate(clauses, initial):
    values = dict(initial)
    while True:
        changed = False
        for clause in clauses:
            if any(abs(lit) in values and values[abs(lit)] == (lit > 0)
                   for lit in clause):
                continue
            open_literals = [lit for lit in clause if abs(lit) not in values]
            if not open_literals:
                return None
            if len(open_literals) == 1:
                lit = open_literals[0]
                value = lit > 0
                variable = abs(lit)
                if variable in values and values[variable] != value:
                    return None
                if variable not in values:
                    values[variable] = value
                    changed = True
        if not changed:
            return values


def local_counter(n, level):
    inputs = list(range(1, n + 1))
    nxt = n + 1
    states = {}
    for i in range(1, n + 1):
        for j in range(1, min(i, level) + 1):
            states[i, j] = nxt
            nxt += 1
    clauses = []
    clauses.extend([(-states[1, 1], inputs[0]),
                    (states[1, 1], -inputs[0])])
    for i in range(2, n + 1):
        x, out, before = inputs[i - 1], states[i, 1], states[i - 1, 1]
        clauses.extend([(-before, out), (-x, out), (-out, before, x)])
        for j in range(2, min(i, level) + 1):
            out, diagonal = states[i, j], states[i - 1, j - 1]
            if j == i:
                clauses.extend([(-out, diagonal), (-out, x),
                                (out, -diagonal, -x)])
            else:
                before = states[i - 1, j]
                clauses.extend([(-before, out), (-diagonal, -x, out),
                                (-out, before, diagonal),
                                (-out, before, x)])
    return inputs, states, clauses, nxt


def gate_truth_tables():
    checked = 0
    # First state iff the first input.
    clauses = [(-2, 1), (2, -1)]
    for x, out in product((False, True), repeat=2):
        values = {1: x, 2: out}
        need(all(satisfied(c, values) for c in clauses) == (out == x),
             "initial counter truth table")
        checked += 1
    # First threshold out iff previous OR input.
    clauses = [(-1, 3), (-2, 3), (-3, 1, 2)]
    for previous, x, out in product((False, True), repeat=3):
        values = {1: previous, 2: x, 3: out}
        need(all(satisfied(c, values) for c in clauses) ==
             (out == (previous or x)), "OR truth table")
        checked += 1
    # out iff left AND right, including signed input positions by symmetry.
    clauses = [(-3, 1), (-3, 2), (3, -1, -2)]
    for a, b, out in product((False, True), repeat=3):
        values = {1: a, 2: b, 3: out}
        need(all(satisfied(c, values) for c in clauses) == (out == (a and b)),
             "AND truth table")
        checked += 1
    # out iff previous OR (diagonal AND input), the four-clause recurrence.
    clauses = [(-1, 4), (-2, -3, 4), (-4, 1, 2), (-4, 1, 3)]
    for previous, diagonal, x, out in product((False, True), repeat=4):
        values = {1: previous, 2: diagonal, 3: x, 4: out}
        need(all(satisfied(c, values) for c in clauses) ==
             (out == (previous or (diagonal and x))), "counter truth table")
        checked += 1
    return checked


def contact_propagation():
    inputs, states, base, nxt = local_counter(39, 21)
    records = []
    for degree in range(18, 25):
        bound = 53 - 2 * degree
        guard = nxt
        clauses = list(base)
        if degree == 18:
            clauses.append((-states[39, bound + 1],))
            active = {}
        else:
            clauses.extend([(-states[39, 18],),
                            (-guard, -states[39, bound + 1])])
            active = {guard: True}
        conflict = propagate(clauses, {**active,
                                      **{v: True for v in inputs[:bound + 1]}})
        need(conflict is None, "contact excess must conflict")
        forced = propagate(clauses, {**active,
                                    **{v: True for v in inputs[:bound]}})
        need(forced is not None and all(forced.get(v) is False for v in inputs[bound:]),
             "contact boundary must force remaining contacts")
        if degree > 18:
            inactive = propagate(clauses, {guard: False,
                                           **{v: True for v in inputs[:bound + 1]}})
            need(inactive is not None, "inactive degree guard")
        records.append({"minimum_color_degree": degree,
                        "maximum_noncontacts": bound,
                        "conflict_at_noncontacts": bound + 1,
                        "boundary_forces_remaining_contacts": 39 - bound})
    return records


def degree_window_propagation():
    inputs, states, clauses, _ = local_counter(42, 25)
    clauses.extend([(states[42, 18],), (-states[42, 25],)])
    need(propagate(clauses, {v: True for v in inputs[:25]}) is None,
         "degree 25 conflict")
    high = propagate(clauses, {v: True for v in inputs[:24]})
    need(high is not None and all(high.get(v) is False for v in inputs[24:]),
         "degree 24 forces remaining opposite")
    need(propagate(clauses, {v: False for v in inputs[:25]}) is None,
         "degree 17 conflict")
    low = propagate(clauses, {v: False for v in inputs[:24]})
    need(low is not None and all(low.get(v) is True for v in inputs[24:]),
         "degree 18 forces remaining same")
    return {"conflict_above": 24, "conflict_below": 18,
            "upper_boundary_forced_literals": 18,
            "lower_boundary_forced_literals": 18}


def guard_propagation():
    literals = list(range(1, 44))
    nxt = 44
    clauses = []
    previous = literals[0]
    prefixes = []
    for literal in literals[1:]:
        out = nxt
        nxt += 1
        prefixes.append(out)
        clauses.extend(stratify.and_gate(out, previous, literal))
        previous = out
    final = prefixes[-1]
    all_true = propagate(clauses, {v: True for v in literals})
    need(all_true is not None and all_true.get(final) is True, "all-degree guard")
    forced = propagate(clauses, {final: True})
    need(forced is not None and all(forced.get(v) is True for v in literals),
         "active guard forces every degree predicate")
    one_false = propagate(clauses, {17: False})
    need(one_false is not None and one_false.get(final) is False,
         "one low degree disables global guard")
    almost = {v: True for v in literals if v != 17}
    almost[final] = False
    forced_low = propagate(clauses, almost)
    need(forced_low is not None and forced_low.get(17) is False,
         "failed guard with other degrees high identifies low predicate")
    return {"degree_predicates": 43, "and_gates": 42,
            "propagation_cases": 4}


def run():
    return {
        "status": "VERIFIED_K4_DEGREE_STRATIFIER_CONTROLS",
        "gate_truth_assignments": gate_truth_tables(),
        "contact_strata": contact_propagation(),
        "degree_window": degree_window_propagation(),
        "global_guard": guard_propagation(),
        "solver_calls": 0,
        "target43_found": False,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
