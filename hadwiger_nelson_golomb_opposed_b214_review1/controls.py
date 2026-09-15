#!/usr/bin/env python3
"""Deterministic controls for the independent opposed-B214 review."""

from __future__ import annotations

import json
from itertools import product

import verify


def slow_rup(variables, clauses, candidate):
    values = [0] * (variables + 1)

    def assign(lit):
        variable = abs(lit)
        value = 1 if lit > 0 else -1
        if values[variable]:
            return values[variable] == value
        values[variable] = value
        return True

    for lit in candidate:
        if not assign(-lit):
            return True
    while True:
        changed = False
        for clause in clauses:
            unassigned = []
            satisfied = False
            for lit in clause:
                value = values[abs(lit)]
                signed = value if lit > 0 else -value
                if signed == 1:
                    satisfied = True
                    break
                if not value:
                    unassigned.append(lit)
            if satisfied:
                continue
            if not unassigned:
                return True
            if len(unassigned) == 1:
                before = values[abs(unassigned[0])]
                if not assign(unassigned[0]):
                    return True
                changed |= not before
        if not changed:
            return False


def radical_oracle_cases():
    cases = 0
    vectors = []
    for digits in product((-1, 0, 1), repeat=4):
        vectors.append((digits[0], digits[1], 0, 0,
                        digits[2], digits[3], 0, 0))
    for a in vectors:
        for b in vectors:
            direct = [0] * 8
            for i, x in enumerate(a):
                for j, y in enumerate(b):
                    if not x or not y:
                        continue
                    common = i & j
                    coefficient = 1
                    if common & 1:
                        coefficient *= 3
                    if common & 2:
                        coefficient *= 5
                    if common & 4:
                        coefficient *= 11
                    direct[i ^ j] += coefficient * x * y
            if verify.multiply(a, b) != tuple(direct):
                raise AssertionError("radical product oracle mismatch")
            cases += 1
    return cases


def rup_oracle_cases():
    pool = (
        (1,), (-1,), (2,), (-2,), (3,),
        (1, 2), (-1, 2), (1, -2), (-1, -2), (2, -3),
    )
    candidates = ((), (1,), (-1,), (2,), (-2,), (3,), (-3,),
                  (1, 2), (-1, 3), (1, -2, 3))
    cases = 0
    for mask in range(1 << len(pool)):
        clauses = [pool[i] for i in range(len(pool)) if mask & (1 << i)]
        checker = verify.OccurrenceRup(3, clauses)
        for candidate in candidates:
            observed = checker.is_rup(candidate)
            expected = slow_rup(3, clauses, candidate)
            if observed != expected:
                raise AssertionError((mask, candidate, observed, expected))
            cases += 1
    return cases


def main():
    result = verify.run()
    expected = json.loads((verify.HERE / "EXPECTED.json").read_text())
    if result != expected:
        raise AssertionError("baseline differs from EXPECTED.json")

    # A normalized base clause fixes variable 1 true, so the contrary unit
    # clause [-1] is not RUP: its negation is consistent with the base CNF.
    cert = json.loads((verify.TARGET / "certificate.json").read_text())
    b_source = verify.read_parts(verify.B_SOURCE)
    g = verify.golomb()
    s343, _ = verify.merge(g + verify.shifted_b(b_source, False)
                           + verify.shifted_b(b_source, True))
    edges343 = verify.exact_edges(s343)
    variables, clauses = verify.build_cnf(
        len(s343), edges343, cert["excluded_patterns"]
    )
    corrupted_first_lemma_rejected = not verify.OccurrenceRup(
        variables, clauses
    ).is_rup((-1,))
    if not corrupted_first_lemma_rejected:
        raise AssertionError("corrupted first RUP lemma accepted")

    first_pattern = cert["surviving_patterns"][0]
    bad_word = "0" * len(s343)
    colour_corruption_rejected = not verify.proper(bad_word, len(s343), edges343)
    if not colour_corruption_rejected:
        raise AssertionError("bad colour word accepted")

    path, digest = next(iter(verify.PINNED.items()))
    hash_corruption_rejected = verify.sha256_bytes(path.read_bytes() + b"x") != digest
    if not hash_corruption_rejected:
        raise AssertionError("hash corruption accepted")

    if verify.cut_structure(3, ((0, 1), (1, 2))) != {
        "articulation_vertices": [1], "bridges": [(0, 1), (1, 2)],
        "components": 1, "minimum_degree": 1,
    }:
        raise AssertionError("path cut-structure control")
    if verify.cut_structure(3, ((0, 1), (0, 2), (1, 2))) != {
        "articulation_vertices": [], "bridges": [],
        "components": 1, "minimum_degree": 2,
    }:
        raise AssertionError("triangle cut-structure control")

    output = {
        "baseline_passed": True,
        "colour_corruption_rejected": colour_corruption_rejected,
        "corrupted_first_rup_lemma_rejected": corrupted_first_lemma_rejected,
        "cut_structure_controls": 2,
        "hash_corruption_rejected": hash_corruption_rejected,
        "radical_product_oracle_cases": radical_oracle_cases(),
        "rup_oracle_cases": rup_oracle_cases(),
        "surviving_pattern_control": first_pattern,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
