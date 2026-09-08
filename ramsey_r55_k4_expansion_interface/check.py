#!/usr/bin/env python3
"""Independent exact controls for the compact K4 expansion interface."""
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json
import random
import subprocess
import sys
import tempfile
import audit

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def holds(clause, values):
    return any(values.get(abs(literal)) == (literal > 0) for literal in clause)


def gadget_controls():
    cases = 0
    # Exact CNFs used by the recurrence: OR, AND, and a OR (b AND x).
    for a, x, out in product((False, True), repeat=3):
        clauses = [(-1, 3), (-2, 3), (-3, 1, 2)]
        values = {1: a, 2: x, 3: out}
        need(all(holds(c, values) for c in clauses) == (out == (a or x)), "OR gadget")
        clauses = [(-3, 1), (-3, 2), (3, -1, -2)]
        need(all(holds(c, values) for c in clauses) == (out == (a and x)), "AND gadget")
        cases += 2
    for a, b, x, out in product((False, True), repeat=4):
        clauses = [(-1, 4), (-2, -3, 4), (-4, 1, 2), (-4, 1, 3)]
        values = {1: a, 2: b, 3: x, 4: out}
        need(all(holds(c, values) for c in clauses) ==
             (out == (a or (b and x))), "mixed recurrence gadget")
        cases += 1
    # The five contact clauses define z iff all same-color literals are false.
    for bits in product((False, True), repeat=4):
        admitted = []
        for z in (False, True):
            values = {1: z, **{i + 2: bit for i, bit in enumerate(bits)}}
            clauses = [(-1, -(i + 2)) for i in range(4)] + [(1, 2, 3, 4, 5)]
            if all(holds(c, values) for c in clauses):
                admitted.append(z)
        need(admitted == [not any(bits)], "contact indicator")
        cases += 2
    return cases


def abstract_counter(n, maximum):
    level = maximum + 1
    z = list(range(1, n + 1))
    states = {}
    next_variable = n + 1
    for i in range(1, n + 1):
        for j in range(1, min(i, level) + 1):
            states[i, j] = next_variable
            next_variable += 1
    clauses = [(-states[1, 1], z[0]), (states[1, 1], -z[0])]
    for i in range(2, n + 1):
        x = z[i - 1]
        old, new = states[i - 1, 1], states[i, 1]
        clauses += [(-old, new), (-x, new), (-new, old, x)]
        for j in range(2, min(i, level) + 1):
            diagonal, new = states[i - 1, j - 1], states[i, j]
            if i == j:
                clauses += [(-new, diagonal), (-new, x), (new, -diagonal, -x)]
            else:
                old = states[i - 1, j]
                clauses += [(-old, new), (-diagonal, -x, new),
                            (-new, old, diagonal), (-new, old, x)]
    clauses.append((-states[n, level],))
    return z, states, clauses


def exact_counter_controls():
    assignments = 0
    for n in range(2, 10):
        for maximum in range(1, n):
            z, states, clauses = abstract_counter(n, maximum)
            for bits in product((False, True), repeat=n):
                values = dict(zip(z, bits))
                for (i, j), variable in states.items():
                    values[variable] = sum(bits[:i]) >= j
                need(all(holds(c, values) for c in clauses) ==
                     (sum(bits) <= maximum), "counter semantics")
                assignments += 1
    return assignments


def unit_propagate(clauses, initial):
    values = dict(initial)
    changed = True
    while changed:
        changed = False
        for clause in clauses:
            if holds(clause, values):
                continue
            unknown = [literal for literal in clause if abs(literal) not in values]
            if not unknown:
                return None
            if len(unknown) == 1:
                literal = unknown[0]
                variable, value = abs(literal), literal > 0
                if variable in values and values[variable] != value:
                    return None
                if variable not in values:
                    values[variable] = value
                    changed = True
    return values


def propagation_controls():
    z, _, clauses = abstract_counter(39, 20)
    rng = random.Random(202609080500)
    subsets = [tuple(range(20)), tuple(range(19, 39)), tuple(range(0, 39, 2))]
    subsets += [tuple(sorted(rng.sample(range(39), 20))) for _ in range(29)]
    checked = 0
    for subset in subsets:
        subset = subset[:20]
        values = unit_propagate(clauses, {z[i]: True for i in subset})
        need(values is not None, "twenty noncontacts rejected")
        need(all(values[z[i]] is False for i in range(39) if i not in subset),
             "twenty-noncontact propagation")
        extra = next(i for i in range(39) if i not in subset)
        need(unit_propagate(clauses,
             {z[i]: True for i in tuple(subset) + (extra,)}) is None,
             "twenty-one-noncontact conflict")
        checked += 2
    return checked


def suffix_controls():
    rows = []
    with tempfile.TemporaryDirectory(prefix="r55-k4-expansion-") as directory:
        for q in range(7, 11):
            for r in range(5, q + 1):
                base = 9000 + 100 * q + r
                path = Path(directory) / f"q{q}-r{r}.cnf"
                command = [sys.executable, "-B", str(HERE / "interface.py"),
                           "--q", str(q), "--r", str(r),
                           "--base-variables", str(base), "--cnf", str(path)]
                produced = json.loads(subprocess.check_output(command, text=True))
                checked = audit.audit_suffix(q, r, base, path)
                for key in ("variables", "clauses", "bytes", "max_width", "sha256"):
                    need(produced[key] == checked[key], "producer/auditor mismatch")
                rows.append({key: checked[key] for key in
                             ("q", "r", "variables", "clauses", "bytes", "sha256")})
    return rows


def main():
    rows = suffix_controls()
    result = {
        "status": "VERIFIED_K4_EXPANSION_INTERFACE",
        "macro_classes": len(rows),
        "all_qr_suffixes_entrywise_audited": True,
        "gadget_truth_table_cases": gadget_controls(),
        "small_counter_assignments": exact_counter_controls(),
        "boundary_propagation_controls": propagation_controls(),
        "minimum_cut_clauses_per_block": comb(39, 21),
        "all_cut_clauses_per_block": sum(comb(39, k) for k in range(21, 40)),
        "compact_variables_per_block": 648,
        "compact_clauses_per_block": 2572,
        "compact_max_width": 5,
        "tasks_covered": 2189178,
        "physical_tasks_decided": 0,
        "solver_calls": 0,
        "good43_found": False,
        "suffix_rows_sha256": hashlib.sha256(
            (json.dumps(rows, sort_keys=True, separators=(",", ":")) + "\n").encode()
        ).hexdigest(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
