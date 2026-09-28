"""Independent literal audit of the reflected 545 CNF and both full controls."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path

A = 109
M = 36
N = 5 * A
CNF_SHA256 = "0b2b8adecfdd9f5f6e9144fcad75449ea9355e3afb6454beb873c3a8c6d55886"
AXIS_COLOURS = (0, 1, 3, 4, 5)
FIBRE_COLOURS = (0, 3, 4, 5)
ROOT = Path(__file__).resolve().parents[1]
CONTROLS = ROOT / "additive_combinatorics/schur6_full_middle_third_545/controls.json"


def normal(literals):
    return tuple(sorted(set(literals)))


def variable_maps():
    axis = {}
    fibre = {}
    support = {}
    next_id = 1
    for u in range(1, (A + 1) // 2):
        for colour in AXIS_COLOURS:
            axis[u, colour] = next_id
            next_id += 1
    places = tuple(range(1, M + 1)) + tuple(range(A - M, A))
    for u in places:
        for colour in FIBRE_COLOURS:
            fibre[u, colour] = next_id
            next_id += 1
    for u in range(1, M + 1):
        for colour in (3, 4, 5):
            support[u, colour] = next_id
            next_id += 1
    assert next_id - 1 == 666
    return axis, fibre, support


def read_cnf(path):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == CNF_SHA256
    clauses = set()
    with path.open(encoding="ascii") as stream:
        assert stream.readline().strip() == "p cnf 666 20574"
        for line in stream:
            data = [int(v) for v in line.split()]
            assert data and data[-1] == 0 and 0 not in data[:-1]
            clause = normal(data[:-1])
            assert len(clause) == len(data) - 1
            assert all(1 <= abs(v) <= 666 for v in clause)
            assert clause not in clauses
            clauses.add(clause)
    assert len(clauses) == 20574
    return clauses


def palette_clauses(axis, fibre):
    clauses = set()
    seen = {3: [], 4: []}
    for u in range(1, (A + 1) // 2):
        nodes = []
        if u <= M:
            nodes.extend((fibre, x) for x in (u, A - u))
        nodes.append((axis, u))
        for table, x in nodes:
            clauses.add(normal([-table[x, 4], *seen[3]]))
            clauses.add(normal([-table[x, 5], *seen[4]]))
            seen[3].append(table[x, 3])
            seen[4].append(table[x, 4])
    for u in range(1, (A + 1) // 2):
        clauses.add(normal([-axis[u, 1], *(axis[v, 0] for v in range(1, u))]))
    assert len(clauses) == 306
    return clauses


def projected_clauses(axis, fibre):
    projected = set()
    for u in range(1, (A + 1) // 2):
        values = [axis[u, c] for c in AXIS_COLOURS]
        projected.add(normal(values))
        projected.update(normal((-v, -w)) for v, w in itertools.combinations(values, 2))
    places = (*range(1, M + 1), *range(A - M, A))
    for x in places:
        values = [fibre[x, c] for c in FIBRE_COLOURS]
        projected.add(normal(values))
        projected.update(normal((-v, -w)) for v, w in itertools.combinations(values, 2))

    middle = set(range(37, 73))

    def colour_term(t, colour):
        u, b = t % A, t % 5
        if b == 0:
            return False if colour == 2 else axis[min(u, A - u), colour]
        special = 0 if b in (1, 4) else 1
        q = u if b in (1, 2) else (-u) % A
        if q == 0:
            return colour == special
        if q in middle:
            return colour == 2
        if colour == special:
            return fibre[q, 0]
        if colour in (3, 4, 5):
            return fibre[q, colour]
        return False

    terms = {(t, c): colour_term(t, c) for t in range(1, N) for c in range(6)}
    pairs = doubling = 0
    for x in range(1, N):
        for y in range(x, N):
            z = (x + y) % N
            if not z:
                continue
            pairs += 1
            doubling += (x == y)
            for c in range(6):
                entries = (terms[x, c], terms[y, c], terms[z, c])
                if any(v is False for v in entries):
                    continue
                projected.add(normal(-v for v in entries if v is not True))
    assert pairs == 147968 and doubling == 544
    assert len(projected) == 26640
    return projected


def subsumed_count(left, right):
    count = 0
    for clause in left - right:
        if not any(tuple(part) in right for size in range(len(clause))
                   for part in itertools.combinations(clause, size)):
            raise AssertionError(("unmatched clause", clause))
        count += 1
    return count


def audit_encoding(path):
    axis, fibre, support = variable_maps()
    all_clauses = read_cnf(path)
    palette = palette_clauses(axis, fibre)
    assert palette <= all_clauses
    base = all_clauses - palette
    assert len(base) == 20268

    definitions = set()
    choices = {}
    for (u, c), p in support.items():
        left, right = fibre[u, c], fibre[A - u, c]
        choices[p] = (left, right)
        definitions.update((normal((-left, p)), normal((-right, p)),
                            normal((-p, left, right))))
    assert len(definitions) == 324 and definitions <= base
    expanded = set()
    pids = set(support.values())
    for clause in base - definitions:
        p_lits = [v for v in clause if abs(v) in pids]
        assert all(v < 0 for v in p_lits)
        remaining = [v for v in clause if abs(v) not in pids]
        for selection in itertools.product(*(choices[-v] for v in p_lits)):
            expanded.add(normal([*remaining, *(-v for v in selection)]))
    projected = projected_clauses(axis, fibre)
    assert len(expanded) == 26532
    extra_literal = subsumed_count(projected, expanded)
    extra_reduced = subsumed_count(expanded, projected)
    assert (extra_literal, extra_reduced) == (108, 0)
    print("PASS modulus=545 variables=666 clauses=20574 palette=306 "
          "pairs=147968 projected=26640 expanded=26532 "
          "subsumed_projected=108 subsumed_reduced=0")


def audit_controls():
    data = json.loads(CONTROLS.read_text())
    assert len(data) == 2
    for index, case in enumerate(data):
        a, n, word = case["axis_factor"], case["modulus"], case["word"]
        assert a == 47 and n == 235 and len(word) == n - 1
        assert set(word) == set(range(6))
        labels = {(t % a, t % 5): word[t - 1] for t in range(1, n)}
        assert len(labels) == n - 1
        axis = {c: {u for u in range(1, a) if labels[u, 0] == c} for c in range(6)}
        fibre = {c: {u for u in range(a) if labels[u, 1] == c} for c in (0, 2, 3, 4, 5)}
        assert labels[0, 1] == 0
        assert all({(-u) % a for u in axis[c]} == axis[c] for c in range(6))
        for (u, b), c in labels.items():
            if b == 0:
                assert u in axis[c]
            else:
                q = u if b in (1, 2) else (-u) % a
                state = labels[q, 1]
                assert c == (state if state else (0 if b in (1, 4) else 1))
        for x in range(1, n):
            for y in range(x, n):
                z = (x + y) % n
                if z:
                    assert not word[x - 1] == word[y - 1] == word[z - 1]
        assert not axis[case["absent_axis_colour"]]
        middle = {u for u in range(a) if a < 3 * u < 2 * a}
        if index == 0:
            assert fibre[2] == middle
            assert [word.count(c) for c in range(6)] == [24, 24, 64, 36, 42, 44]
        else:
            assert not any(fibre[5] <= {k * u % a for u in middle}
                           for k in range(1, a))
            assert all(fibre[c] <= {k * u % a for u in middle}
                       for c, k in zip((2, 3, 4), (1, 4, 23)))
            assert [word.count(c) for c in range(6)] == [24, 34, 40, 50, 42, 44]
    print("PASS controls=2 endpoints=234,234 modular_sum_free=yes "
          "full_middle_third=yes noninterval_branch=yes")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    args = parser.parse_args()
    m = M
    middle = set(range(37, 73))
    assert {-u % A for u in middle} == middle
    assert set(range(A)) - middle == {0} | set(range(1, m + 1)) | set(range(A - m, A))
    assert all((x + y) % A not in middle for x in middle for y in middle)
    signed = {tuple(sorted({min(x, A - x), min(y, A - y),
                            min((x + y) % A, A - (x + y) % A)}))
              for x in (*range(1, m + 1), *range(A - m, A))
              for y in (*range(1, m + 1), *range(A - m, A))
              if (x + y) % A in set((*range(1, m + 1), *range(A - m, A)))}
    ordinary = {tuple(sorted({x, y, x + y}))
                for x in range(1, m + 1) for y in range(x, m - x + 1)}
    assert signed == ordinary and len(signed) == 324
    audit_encoding(args.cnf)
    audit_controls()
    print("PASS signed_supports=324 ordinary_supports=324 equal=yes")


if __name__ == "__main__":
    main()
