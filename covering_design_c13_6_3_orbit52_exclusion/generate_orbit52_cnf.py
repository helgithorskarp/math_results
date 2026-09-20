#!/usr/bin/env python3
"""Generate exact CNFs for the orbit-52 P3+K2 exclusion.

This deliberately reuses only the primitive CNF and Venn routines from the
published orbit-51 package.  The normal form, residual automorphisms, and
column degrees below are specific to orbit 52.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "covering_design_c13_6_3_orbit51_exclusion" / "generate_dual_cnf.py"
SPEC = importlib.util.spec_from_file_location("orbit51_primitives", PARENT)
assert SPEC is not None and SPEC.loader is not None
parent = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(parent)

Cnf = parent.Cnf
QPAIR_PATTERNS = parent.QPAIR_PATTERNS
qthrough_types = parent.qthrough_types
qaway_values = parent.qaway_values
qthrough_rows = parent.qthrough_rows
venn_rows = parent.venn_rows
render = parent.render

N = 12
FIXED = (
    frozenset((0, 1, 2, 3, 4)),
    frozenset((0, 1, 2, 4, 5)),
    frozenset((0, 1, 2, 6, 7)),
)

# A Q-free row is classified under Aut(P3+K2) x S4 by
# (path-center chosen, number of path endpoints, number of K2 vertices,
#  number of R vertices).  The entries must sum to five.
QFREE_TYPES = {
    f"c{center}_e{endpoints}_k{edge}_r{rest}": (center, endpoints, edge, rest)
    for center in range(2)
    for endpoints in range(3)
    for edge in range(3)
    for rest in (5 - center - endpoints - edge,)
    if 0 <= rest <= 4
}


def qfree_representative(kind: str) -> tuple[int, ...]:
    center, endpoints, edge, rest = QFREE_TYPES[kind]
    points = ([4] if center else [])
    points += [3, 5][:endpoints]
    points += [6, 7][:edge]
    points += [8, 9, 10, 11][:rest]
    assert len(points) == 5
    return tuple(sorted(points))


def build(case: str, qpattern: str,
          qthrough: tuple[int, int, int, int] | None = None,
          qaway: int | None = None) -> tuple[Cnf, dict[str, object]]:
    f = Cnf()
    y = [[f.var() for _ in range(N)] for _ in range(9)]
    z = [[f.var() for _ in range(N)] for _ in range(8)]
    primary_end = f.nvars

    for row in y:
        f.exactly(row, 5)
    for row in z:
        f.exactly(row, 6)
    through_degrees = (2, 2, 2, 4, 3, 4, 4, 4, 5, 5, 5, 5)
    for point, degree in enumerate(through_degrees):
        f.exactly([row[point] for row in y], degree)
        f.exactly([row[point] for row in z], 4)

    representative = qfree_representative(case)
    for point, lit in enumerate(y[0]):
        f.clauses.append([lit if point in representative else -lit])
    for row in y[1:]:
        f.clauses.append([
            -row[point] if point in representative else row[point]
            for point in range(N)
        ])

    if qthrough is not None:
        assert qpattern in ("221", "222")
        assert qthrough in qthrough_types(qpattern)
        q_rows = qthrough_rows(qthrough)
        for row_index, pattern in enumerate(q_rows, start=1):
            for q, value in enumerate(pattern):
                f.clauses.append([y[row_index][q] if value else -y[row_index][q]])
        start = 0
        while start < len(q_rows):
            end = start + 1
            while end < len(q_rows) and q_rows[end] == q_rows[start]:
                end += 1
            for first, second in itertools.pairwise(y[1 + start:1 + end]):
                f.lex_le(list(reversed(first[3:])), list(reversed(second[3:])), strict=True)
            start = end
    else:
        for first, second in itertools.pairwise(y[1:]):
            f.lex_le(list(reversed(first)), list(reversed(second)), strict=True)

    if qaway is not None:
        assert qthrough is not None
        limits = tuple(1 + bit for bit in QPAIR_PATTERNS[qpattern])
        z_pairs = tuple(limits[index] - qthrough[index] for index in range(3))
        z_rows = venn_rows(4, z_pairs + (qaway,))
        for row_index, pattern in enumerate(z_rows):
            for q, value in enumerate(pattern):
                f.clauses.append([z[row_index][q] if value else -z[row_index][q]])
        start = 0
        while start < len(z_rows):
            end = start + 1
            while end < len(z_rows) and z_rows[end] == z_rows[start]:
                end += 1
            for first, second in itertools.pairwise(z[start:end]):
                f.lex_le(list(reversed(first[3:])), list(reversed(second[3:])), strict=True)
            start = end
    else:
        for first, second in itertools.pairwise(z):
            f.lex_le(list(reversed(first)), list(reversed(second)), strict=True)

    for row in y:
        for fixed in FIXED:
            f.clauses.append([
                -row[point] if point in fixed else row[point]
                for point in range(N)
            ])

    pair_vars: dict[tuple[str, int, int, int], int] = {}
    for name, matrix in (("y", y), ("z", z)):
        for p, q in itertools.combinations(range(N), 2):
            for row_index, row in enumerate(matrix):
                pair_vars[name, row_index, p, q] = f.and_var([row[p], row[q]])

    high_pair: dict[tuple[int, int], int] = {}
    for p, q in itertools.combinations(range(N), 2):
        fixed_count = sum({p, q} <= block for block in FIXED)
        through_pairs = [pair_vars["y", r, p, q] for r in range(9)]
        away_pairs = [pair_vars["z", r, p, q] for r in range(8)]
        if fixed_count == 0:
            f.clauses.append(through_pairs)
        final = f.count_states(through_pairs + away_pairs, cap=6, initial=fixed_count)
        f.clauses.append([final[3], final[4], final[5]])
        high_pair[p, q] = final[5]

    for point in range(N):
        flags = [
            high_pair[min(point, other), max(point, other)]
            for other in range(N) if other != point
        ]
        final = f.count_states(flags, cap=3)
        f.clauses.append([-final[3]])

    for pair, flag_value in zip(
        ((0, 1), (0, 2), (1, 2)), QPAIR_PATTERNS[qpattern]
    ):
        f.clauses.append([high_pair[pair] if flag_value else -high_pair[pair]])

    fixed_covered = {
        triple for block in FIXED
        for triple in itertools.combinations(sorted(block), 3)
    }
    uncovered_fixed = 0
    for triple in itertools.combinations(range(N), 3):
        if triple in fixed_covered:
            continue
        uncovered_fixed += 1
        witnesses = []
        for matrix in (y, z):
            for row in matrix:
                witnesses.append(f.and_var([row[point] for point in triple]))
        f.clauses.append(witnesses)

    meta: dict[str, object] = {
        "primary_variables": primary_end,
        "variables": f.nvars,
        "clauses": len(f.clauses),
        "fixed_through_residues": [sorted(block) for block in FIXED],
        "remaining_through_column_sums": list(through_degrees),
        "away_column_sums": [4] * N,
        "triple_constraints_not_fixed": uncovered_fixed,
        "qfree_case": case,
        "qpair_pattern": qpattern,
        "qthrough_type": list(qthrough) if qthrough is not None else None,
        "qaway_triple_intersection": qaway,
        "designated_qfree_residue": list(representative),
    }
    return f, meta


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("metadata", type=Path)
    parser.add_argument("--case", required=True, choices=sorted(QFREE_TYPES))
    parser.add_argument("--qpattern", required=True, choices=sorted(QPAIR_PATTERNS))
    parser.add_argument("--qthrough")
    parser.add_argument("--qaway", type=int)
    args = parser.parse_args()
    qthrough = tuple(map(int, args.qthrough)) if args.qthrough else None
    f, meta = build(args.case, args.qpattern, qthrough, args.qaway)
    data = render(f)
    meta["cnf_sha256"] = hashlib.sha256(data).hexdigest()
    args.cnf.write_bytes(data)
    args.metadata.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n")
    print(json.dumps(meta, sort_keys=True))


if __name__ == "__main__":
    main()
