#!/usr/bin/env python3
"""Independent finite audits for the published orbit-51 CNF generator."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

from generate_dual_cnf import (
    Cnf,
    QFREE_TYPES,
    QPAIR_PATTERNS,
    build,
    qaway_values,
    qfree_representative,
    qthrough_types,
    render,
)


def sat(clauses: list[list[int]], assignment: dict[int, bool] | None = None) -> bool:
    """Tiny definition-level DPLL used only on primitive test formulas."""
    values = dict(assignment or {})

    def recurse(current: dict[int, bool]) -> bool:
        while True:
            unit = None
            all_satisfied = True
            for clause in clauses:
                unresolved = []
                satisfied = False
                for lit in clause:
                    value = current.get(abs(lit))
                    if value is None:
                        unresolved.append(lit)
                    elif value == (lit > 0):
                        satisfied = True
                        break
                if satisfied:
                    continue
                all_satisfied = False
                if not unresolved:
                    return False
                if len(unresolved) == 1:
                    unit = unresolved[0]
                    break
            if all_satisfied:
                return True
            if unit is None:
                break
            var, value = abs(unit), unit > 0
            if var in current and current[var] != value:
                return False
            current[var] = value
        for clause in clauses:
            for lit in clause:
                if abs(lit) not in current:
                    var = abs(lit)
                    return recurse(current | {var: False}) or recurse(current | {var: True})
        return False

    return recurse(values)


def audit_and() -> int:
    checks = 0
    for width in (2, 3):
        f = Cnf()
        inputs = [f.var() for _ in range(width)]
        out = f.and_var(inputs)
        for bits in itertools.product((False, True), repeat=width):
            for output in (False, True):
                fixed = {var: bit for var, bit in zip(inputs, bits)} | {out: output}
                assert sat(f.clauses, fixed) == (output == all(bits))
                checks += 1
    return checks


def audit_counts() -> int:
    checks = 0
    for size in range(0, 6):
        for cap in range(1, 4):
            for initial in range(cap + 1):
                f = Cnf()
                inputs = [f.var() for _ in range(size)]
                final = f.count_states(inputs, cap, initial)
                for bits in itertools.product((False, True), repeat=size):
                    expected = min(initial + sum(bits), cap)
                    fixed_inputs = {var: bit for var, bit in zip(inputs, bits)}
                    for state, var in enumerate(final):
                        possible = sat(f.clauses, fixed_inputs | {var: True})
                        assert possible == (state == expected)
                        checks += 1
    return checks


def audit_lex() -> int:
    checks = 0
    for width in range(1, 5):
        for strict in (False, True):
            f = Cnf()
            left = [f.var() for _ in range(width)]
            right = [f.var() for _ in range(width)]
            f.lex_le(left, right, strict)
            for a in itertools.product((False, True), repeat=width):
                for b in itertools.product((False, True), repeat=width):
                    fixed = {var: bit for var, bit in zip(left, a)}
                    fixed |= {var: bit for var, bit in zip(right, b)}
                    expected = a < b if strict else a <= b
                    assert sat(f.clauses, fixed) == expected
                    checks += 1
    return checks


def audit_qfree_orbits() -> dict[str, int]:
    s = set(range(3, 9))
    r = set(range(9, 12))
    edges = ({3, 4}, {5, 6}, {7, 8})
    counts = {kind: 0 for kind in QFREE_TYPES}
    invariant_to_kind = {value: kind for kind, value in QFREE_TYPES.items()}
    for block_tuple in itertools.combinations(range(3, 12), 5):
        block = set(block_tuple)
        c = len(block & r)
        doubled = sum(edge <= block for edge in edges)
        single = sum(len(edge & block) == 1 for edge in edges)
        kind = invariant_to_kind[doubled, single, c]
        counts[kind] += 1
    assert sum(counts.values()) == 126
    for kind, rep in ((kind, set(qfree_representative(kind))) for kind in QFREE_TYPES):
        doubled, single, c = QFREE_TYPES[kind]
        assert rep <= s | r and len(rep) == 5 and len(rep & r) == c
        assert sum(edge <= rep for edge in edges) == doubled
        assert sum(len(edge & rep) == 1 for edge in edges) == single
    return counts


def audit_qpair_orbits() -> dict[str, int]:
    counts = {kind: 0 for kind in QPAIR_PATTERNS}
    for flags in itertools.product((0, 1), repeat=3):
        kind = "".join(str(1 + bit) for bit in sorted(flags, reverse=True))
        counts[kind] += 1
    assert counts == {"111": 1, "211": 3, "221": 3, "222": 1}
    return counts


def audit_expected(expected_path: Path) -> list[dict[str, object]]:
    expected = json.loads(expected_path.read_text())
    rows = []
    observed_keys = set()
    for item in expected["cases"]:
        qthrough = tuple(item["qthrough_type"]) if item["qthrough_type"] else None
        f, meta = build(
            item["case"], item["qpair_pattern"], qthrough,
            item["qaway_triple_intersection"],
        )
        data = render(f)
        observed = {
            "case": item["case"],
            "variables": f.nvars,
            "clauses": len(f.clauses),
            "cnf_sha256": hashlib.sha256(data).hexdigest(),
        }
        assert observed == {key: item[key] for key in observed}
        assert meta["designated_qfree_residue"] == item["designated_qfree_residue"]
        observed_keys.add((item["case"], item["qpair_pattern"], qthrough,
                           item["qaway_triple_intersection"]))
        rows.append(observed)
    required_keys = set()
    for case in QFREE_TYPES:
        required_keys.add((case, "111", None, None))
        required_keys.add((case, "211", None, None))
        for qpattern in ("221", "222"):
            for qthrough in qthrough_types(qpattern):
                for qaway in qaway_values(qpattern, qthrough):
                    required_keys.add((case, qpattern, qthrough, qaway))
    assert observed_keys == required_keys and len(required_keys) == 91
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected", type=Path)
    args = parser.parse_args()
    result: dict[str, object] = {
        "and_checks": audit_and(),
        "count_checks": audit_counts(),
        "lex_checks": audit_lex(),
        "qfree_orbit_sizes": audit_qfree_orbits(),
        "qpair_orbit_sizes": audit_qpair_orbits(),
    }
    if args.expected:
        result["full_case_regenerations"] = audit_expected(args.expected)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
