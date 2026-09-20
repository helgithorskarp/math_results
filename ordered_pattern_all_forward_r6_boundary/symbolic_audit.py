#!/usr/bin/env python3
"""Exact QF_LRA audit of the six paired-repair endpoint signatures."""

from __future__ import annotations

import hashlib
import json

import z3


def repair_formula(t: int, s_count: int):
    solver = z3.Solver()
    m = z3.Real("m")
    deficits = [z3.Real(f"d_{i}") for i in range(t)]
    points = [z3.Real(f"p_{j}") for j in range(s_count)]

    solver.add(m >= 2)
    for deficit in deficits:
        solver.add(deficit >= 0, deficit <= m - 1)
    solver.add(z3.Sum(deficits) == (t - 6) * m - 2)

    half = 3 * m + 1
    starts = [z3.IntVal(0)]
    for i in range(1, t):
        starts.append(i * m - z3.Sum(deficits[:i]))

    for point in points:
        solver.add(point >= 0, point < half)
    for left, right in zip(points, points[1:]):
        solver.add(left <= right)

    # K_i=[a_i-d_i,a_i] modulo M.  The shifts -1,0,1,2 contain every
    # possible lift because 0<=a_i<2M and -m<a_i-d_i<2M.
    for i in range(t):
        memberships = []
        for point in points:
            for shift in range(-1, 3):
                lifted = point + shift * half
                memberships.append(
                    z3.And(starts[i] - deficits[i] <= lifted, lifted <= starts[i])
                )
        solver.add(z3.Or(*memberships))
    return solver, m, deficits


def cases():
    solver, m, d = repair_formula(8, 5)
    solver.add(d[0] + d[1] >= m)
    yield "t8_intersecting_J_five_K_hits", solver

    solver, m, d = repair_formula(8, 4)
    for i in range(8):
        solver.add(d[i] + d[(i + 1) % 8] <= m - 1)
    solver.add(d[0] + d[1] + d[2] >= m)
    yield "t8_disjoint_J_four_K_hits_bad_triple", solver

    solver, m, d = repair_formula(9, 4)
    solver.add(d[0] + d[1] + d[2] >= 2 * m)
    yield "t9_J_triple_four_K_hits", solver

    for separation in (2, 3, 4):
        solver, m, d = repair_formula(9, 4)
        solver.add(d[0] + d[1] >= m)
        solver.add(d[separation] + d[separation + 1] >= m)
        yield f"t9_two_J_pairs_sep{separation}_four_K_hits", solver


def main():
    statuses = []
    formula_hashes = []
    for name, solver in cases():
        sexpr = solver.sexpr()
        formula_hashes.append((name, hashlib.sha256(sexpr.encode()).hexdigest()))
        status = solver.check()
        if status != z3.unsat:
            raise AssertionError(f"{name}: expected unsat, got {status}; model={solver.model()}")
        statuses.append((name, str(status)))
        print(f"{name}=unsat")
    record = {
        "z3_version": z3.get_version_string(),
        "statuses": statuses,
        "formula_hashes": formula_hashes,
    }
    digest = hashlib.sha256(
        json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print(f"formula_record_sha256={digest}")
    print("SYMBOLIC_VERIFIED")


if __name__ == "__main__":
    main()
