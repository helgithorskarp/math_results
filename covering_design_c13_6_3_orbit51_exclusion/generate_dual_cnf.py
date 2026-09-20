#!/usr/bin/env python3
"""Generate proof-checkable dual-incidence CNFs for the orbit-51 exclusion.

Unlike the exploratory CP-SAT model, this generator uses only the manifestly
sound symmetry break obtained by sorting the unordered rows inside the two
block families.  It exposes every cardinality state and every pair/triple
conjunction to make the mathematical encoding auditable.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


N = 12
FIXED = (
    frozenset((0, 1, 2, 3, 4)),
    frozenset((0, 1, 2, 5, 6)),
    frozenset((0, 1, 2, 7, 8)),
)

QFREE_TYPES = {
    "c0_21": (2, 1, 0),
    "c1_12": (1, 2, 1),
    "c1_20": (2, 0, 1),
    "c2_03": (0, 3, 2),
    "c2_11": (1, 1, 2),
    "c3_02": (0, 2, 3),
    "c3_10": (1, 0, 3),
}

QPAIR_PATTERNS = {
    "111": (0, 0, 0),
    "211": (1, 0, 0),
    "221": (1, 1, 0),
    "222": (1, 1, 1),
}


def qthrough_types(qpattern: str) -> tuple[tuple[int, int, int, int], ...]:
    """Row-permutation orbits of three 2-subsets compatible with qpattern."""
    seen: set[tuple[int, int, int, int]] = set()
    pairs = tuple(itertools.combinations(range(8), 2))
    limits = tuple(1 + bit for bit in QPAIR_PATTERNS[qpattern])
    for first, second, third in itertools.product(pairs, repeat=3):
        sets = tuple(map(set, (first, second, third)))
        value = (
            len(sets[0] & sets[1]),
            len(sets[0] & sets[2]),
            len(sets[1] & sets[2]),
            len(sets[0] & sets[1] & sets[2]),
        )
        if any(value[i] > limits[i] for i in range(3)):
            continue
        if qpattern == "221":
            value = min(value, (value[1], value[0], value[2], value[3]))
        elif qpattern == "222":
            value = tuple(sorted(value[:3])) + (value[3],)
        seen.add(value)
    return tuple(sorted(seen))


def venn_rows(size: int, value: tuple[int, int, int, int]) -> tuple[tuple[int, int, int], ...]:
    """Canonical eight-row realization of three equal-size column sets."""
    a, b, c, t = value
    counts = {
        (1, 1, 1): t,
        (1, 1, 0): a - t,
        (1, 0, 1): b - t,
        (0, 1, 1): c - t,
        (1, 0, 0): size - a - b + t,
        (0, 1, 0): size - a - c + t,
        (0, 0, 1): size - b - c + t,
    }
    used = sum(counts.values())
    counts[(0, 0, 0)] = 8 - used
    assert all(count >= 0 for count in counts.values())
    rows = tuple(pattern for pattern in sorted(counts, reverse=True)
                 for _ in range(counts[pattern]))
    assert len(rows) == 8
    assert all(sum(row[q] for row in rows) == size for q in range(3))
    return rows


def qthrough_rows(value: tuple[int, int, int, int]) -> tuple[tuple[int, int, int], ...]:
    return venn_rows(2, value)


def qaway_values(qpattern: str, qthrough: tuple[int, int, int, int]) -> tuple[int, ...]:
    limits = tuple(1 + bit for bit in QPAIR_PATTERNS[qpattern])
    a, b, c = (limits[i] - qthrough[i] for i in range(3))
    feasible = []
    for t in range(5):
        try:
            venn_rows(4, (a, b, c, t))
        except AssertionError:
            continue
        feasible.append(t)
    return tuple(feasible)


class Cnf:
    def __init__(self) -> None:
        self.nvars = 0
        self.clauses: list[list[int]] = []

    def var(self) -> int:
        self.nvars += 1
        return self.nvars

    def and_var(self, lits: list[int]) -> int:
        out = self.var()
        self.clauses.extend([[-out, lit] for lit in lits])
        self.clauses.append([out] + [-lit for lit in lits])
        return out

    def count_states(self, lits: list[int], cap: int, initial: int = 0) -> list[int]:
        """Return exact saturated-count states after all literals.

        State j means the count equals j for j < cap; state cap means the
        count is at least cap.  Each row is one-hot and transitions are exact.
        """
        assert 0 <= initial <= cap
        states = [[self.var() for _ in range(cap + 1)]
                  for _ in range(len(lits) + 1)]
        for row in states:
            self.clauses.append(row)
            for a, b in itertools.combinations(row, 2):
                self.clauses.append([-a, -b])
        self.clauses.append([states[0][initial]])
        for i, lit in enumerate(lits):
            for j in range(cap + 1):
                self.clauses.append([-states[i][j], lit, states[i + 1][j]])
                nxt = min(j + 1, cap)
                self.clauses.append([-states[i][j], -lit, states[i + 1][nxt]])
        return states[-1]

    def exactly(self, lits: list[int], value: int) -> None:
        final = self.count_states(lits, value + 1)
        self.clauses.append([final[value]])

    def lex_le(self, left: list[int], right: list[int], strict: bool = False) -> None:
        """Enforce Boolean lex order left <= right with 0 < 1."""
        assert len(left) == len(right)
        prefix = self.var()
        self.clauses.append([prefix])
        for a, b in zip(left, right):
            self.clauses.append([-prefix, -a, b])
            following = self.var()
            self.clauses.append([-following, prefix])
            self.clauses.append([-following, -a, b])
            self.clauses.append([-following, a, -b])
            self.clauses.append([-prefix, -a, -b, following])
            self.clauses.append([-prefix, a, b, following])
            prefix = following
        if strict:
            self.clauses.append([-prefix])


def qfree_representative(kind: str) -> tuple[int, ...]:
    doubled, single, r_count = QFREE_TYPES[kind]
    edges = ((3, 4), (5, 6), (7, 8))
    points: list[int] = []
    for edge in edges[:doubled]:
        points.extend(edge)
    for edge in edges[doubled:doubled + single]:
        points.append(edge[0])
    points.extend((9, 10, 11)[:r_count])
    assert len(points) == 5
    return tuple(sorted(points))


def build(case: str | None = None, qpattern: str | None = None,
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
    through_degrees = (2,) * 3 + (4,) * 6 + (5,) * 3
    for p, degree in enumerate(through_degrees):
        f.exactly([row[p] for row in y], degree)
        f.exactly([row[p] for row in z], 4)

    # Binary row signatures increase strictly; compare the most significant
    # point first because signature(row)=sum 2^p row[p].
    if case is not None:
        representative = qfree_representative(case)
        for p, lit in enumerate(y[0]):
            f.clauses.append([lit if p in representative else -lit])
        for row in y[1:]:
            f.clauses.append([
                (-row[p] if p in representative else row[p]) for p in range(N)
            ])
        y_sort_rows = y[1:]
    else:
        representative = None
        y_sort_rows = y
    if qthrough is not None:
        assert qpattern in ("221", "222")
        assert qthrough in qthrough_types(qpattern)
        q_rows = qthrough_rows(qthrough)
        for r, pattern in enumerate(q_rows, start=1):
            for q, value in enumerate(pattern):
                f.clauses.append([y[r][q] if value else -y[r][q]])
        # Row permutations were used to normalize the three Q columns.  The
        # residual row symmetry consists exactly of permutations within equal
        # Q-membership cells; sort those cells by their S+R tails.
        start = 0
        while start < len(q_rows):
            end = start + 1
            while end < len(q_rows) and q_rows[end] == q_rows[start]:
                end += 1
            cell_rows = y[1 + start:1 + end]
            for first, second in itertools.pairwise(cell_rows):
                f.lex_le(list(reversed(first[3:])), list(reversed(second[3:])), strict=True)
            start = end
    else:
        for first, second in itertools.pairwise(y_sort_rows):
            f.lex_le(list(reversed(first)), list(reversed(second)), strict=True)
    if qaway is not None:
        assert qpattern is not None and qthrough is not None
        assert qaway in qaway_values(qpattern, qthrough)
        limits = tuple(1 + bit for bit in QPAIR_PATTERNS[qpattern])
        z_pairs = tuple(limits[i] - qthrough[i] for i in range(3))
        z_rows = venn_rows(4, z_pairs + (qaway,))
        for r, pattern in enumerate(z_rows):
            for q, value in enumerate(pattern):
                f.clauses.append([z[r][q] if value else -z[r][q]])
        start = 0
        while start < len(z_rows):
            end = start + 1
            while end < len(z_rows) and z_rows[end] == z_rows[start]:
                end += 1
            cell_rows = z[start:end]
            for first, second in itertools.pairwise(cell_rows):
                f.lex_le(list(reversed(first[3:])), list(reversed(second[3:])), strict=True)
            start = end
    else:
        for first, second in itertools.pairwise(z):
            f.lex_le(list(reversed(first)), list(reversed(second)), strict=True)

    # No remaining through row repeats one of the three fixed residues.
    for row in y:
        for fixed in FIXED:
            f.clauses.append([(-row[p] if p in fixed else row[p]) for p in range(N)])

    pair_vars: dict[tuple[str, int, int, int], int] = {}
    for name, matrix in (("y", y), ("z", z)):
        for p, q in itertools.combinations(range(N), 2):
            for r, row in enumerate(matrix):
                pair_vars[name, r, p, q] = f.and_var([row[p], row[q]])

    high_pair: dict[tuple[int, int], int] = {}
    for p, q in itertools.combinations(range(N), 2):
        fixed_count = sum({p, q} <= block for block in FIXED)
        yp = [pair_vars["y", r, p, q] for r in range(9)]
        zp = [pair_vars["z", r, p, q] for r in range(8)]
        if fixed_count == 0:
            f.clauses.append(yp)
        final = f.count_states(yp + zp, cap=6, initial=fixed_count)
        f.clauses.append([final[3], final[4], final[5]])
        high_pair[p, q] = final[5]

    # At most two codegree-five low neighbors at each point.  Since the flags
    # are exact count states, this is a direct encoding of the imported link
    # profile classification.
    for p in range(N):
        flags = [high_pair[min(p, q), max(p, q)] for q in range(N) if q != p]
        final = f.count_states(flags, cap=3)
        f.clauses.append([-final[3]])

    if qpattern is not None:
        # The fixed blocks contribute three to every pair inside Q.  Covering
        # the triples with each point of R forces at least one further block,
        # while the imported link bound gives total codegree at most five.
        # Thus these three flags (total codegree five versus four) classify
        # the four S3(Q)-orbits 111, 211, 221, 222.
        for pair, flag_value in zip(((0, 1), (0, 2), (1, 2)),
                                    QPAIR_PATTERNS[qpattern]):
            f.clauses.append([high_pair[pair] if flag_value else -high_pair[pair]])

    fixed_covered = {triple for block in FIXED
                     for triple in itertools.combinations(sorted(block), 3)}
    uncovered_fixed = 0
    for triple in itertools.combinations(range(N), 3):
        if triple in fixed_covered:
            continue
        uncovered_fixed += 1
        witnesses = []
        for matrix in (y, z):
            for row in matrix:
                witnesses.append(f.and_var([row[p] for p in triple]))
        f.clauses.append(witnesses)

    meta: dict[str, object] = {
        "primary_variables": primary_end,
        "variables": f.nvars,
        "clauses": len(f.clauses),
        "fixed_through_residues": [sorted(block) for block in FIXED],
        "remaining_through_column_sums": list(through_degrees),
        "away_column_sums": [4] * N,
        "triple_constraints_not_fixed": uncovered_fixed,
        "symmetry": "strict binary-signature order within through and away rows",
        "qfree_case": case,
        "qpair_pattern": qpattern,
        "qthrough_type": list(qthrough) if qthrough is not None else None,
        "qaway_triple_intersection": qaway,
        "designated_qfree_residue": list(representative) if representative else None,
    }
    return f, meta


def render(f: Cnf) -> bytes:
    head = f"p cnf {f.nvars} {len(f.clauses)}\n"
    body = "".join(" ".join(map(str, clause)) + " 0\n" for clause in f.clauses)
    return (head + body).encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("metadata", type=Path)
    parser.add_argument("--case", choices=sorted(QFREE_TYPES))
    parser.add_argument("--qpattern", choices=sorted(QPAIR_PATTERNS))
    parser.add_argument("--qthrough", help="four digits a,b,c,t for a 221/222 through-Q orbit")
    parser.add_argument("--qaway", type=int, help="triple intersection of the three away-Q columns")
    args = parser.parse_args()
    qthrough = tuple(map(int, args.qthrough)) if args.qthrough else None
    if qthrough is not None and len(qthrough) != 4:
        parser.error("--qthrough requires four digits")
    f, meta = build(args.case, args.qpattern, qthrough, args.qaway)
    data = render(f)
    meta["cnf_sha256"] = hashlib.sha256(data).hexdigest()
    args.cnf.write_bytes(data)
    args.metadata.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n")
    print(json.dumps(meta, sort_keys=True))


if __name__ == "__main__":
    main()
