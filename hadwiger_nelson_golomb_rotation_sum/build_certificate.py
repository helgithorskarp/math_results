#!/usr/bin/env python3
"""Produce a compact colouring cover using an exact line-circle census."""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations, product
from math import isqrt
from pathlib import Path

from pysat.solvers import Cadical195

HERE = Path(__file__).resolve().parent
Z = (F(0), F(0))
O = (F(1), F(0))


def add(a, b): return a[0] + b[0], a[1] + b[1]
def neg(a): return -a[0], -a[1]
def sub(a, b): return add(a, neg(b))
def mul(a, b): return a[0] * b[0] + 33 * a[1] * b[1], a[0] * b[1] + a[1] * b[0]
def scale(a, q): return a[0] * q, a[1] * q


def inv(a):
    d = a[0] * a[0] - 33 * a[1] * a[1]
    if not d:
        raise ZeroDivisionError
    return a[0] / d, -a[1] / d


def div(a, b): return mul(a, inv(b))


def sign(a):
    x, y = a
    if not x:
        return (y > 0) - (y < 0)
    if not y:
        return (x > 0) - (x < 0)
    if (x > 0) == (y > 0):
        return (x > 0) - (x < 0)
    return ((x > 0) - (x < 0)) * ((x * x - 33 * y * y > 0) - (x * x - 33 * y * y < 0))


def qsqrt(x):
    if x < 0:
        return None
    a, b = isqrt(x.numerator), isqrt(x.denominator)
    return F(a, b) if a * a == x.numerator and b * b == x.denominator else None


def ksqrt(z):
    """Return one square root in Q(sqrt(33)), or None."""
    a, b = z
    if not b:
        p = qsqrt(a)
        if p is not None:
            return p, F(0)
        q = qsqrt(a / 33)
        return (F(0), q) if q is not None else None
    rn = qsqrt(a * a - 33 * b * b)
    if rn is None:
        return None
    for signed in (rn, -rn):
        p = qsqrt((a + signed) / 2)
        if p not in (None, 0):
            q = b / (2 * p)
            if mul((p, q), (p, q)) == z:
                return p, q
    return None


# A row (a,b,c,d) denotes (a+b*sqrt(33))/36 + i*sqrt(3)*(c+d*sqrt(33))/36.
ROWS = [
    (0, 0, 0, 0),
    (36, 0, 0, 0), (18, 0, 18, 0), (-18, 0, 18, 0),
    (-36, 0, 0, 0), (-18, 0, -18, 0), (18, 0, -18, 0),
    (6, 0, 0, 2), (-3, -3, 3, -1), (-3, 3, -3, -1),
]
G = [((F(a, 36), F(b, 36)), (F(c, 36), F(d, 36))) for a, b, c, d in ROWS]


def csub(a, b): return sub(a[0], b[0]), sub(a[1], b[1])
def norm(a): return add(mul(a[0], a[0]), scale(mul(a[1], a[1]), 3))


def conjprod(a, b):
    return (
        add(mul(a[0], b[0]), scale(mul(a[1], b[1]), 3)),
        sub(mul(a[0], b[1]), mul(a[1], b[0])),
    )


def event_line(a, b, target):
    """Normalized A*x+B*y=C for u=x+i*sqrt(3)*y."""
    p, q = conjprod(a, b)
    aa, bb = scale(p, 2), scale(q, -6)
    cc = sub((F(target), F(0)), add(norm(a), norm(b)))
    if aa != Z:
        return O, div(bb, aa), div(cc, aa)
    if bb != Z:
        return Z, O, div(cc, bb)
    return None


def line_roots(line):
    """Return [], exact K roots, or None for two non-K real roots."""
    a, b, c = line
    d = add(mul(a, a), scale(mul(b, b), F(1, 3)))
    delta = scale(sub(d, mul(c, c)), F(1, 3))
    if sign(delta) < 0:
        return []
    r = ksqrt(delta)
    if r is None:
        return None
    out = []
    for t in ({Z} if r == Z else {r, neg(r)}):
        x = div(add(mul(a, c), mul(b, t)), d)
        y = div(sub(scale(mul(b, c), F(1, 3)), mul(a, t)), d)
        if add(mul(x, x), scale(mul(y, y), 3)) != O:
            raise RuntimeError("bad line-circle root")
        out.append((x, y))
    return out


def case_key(case):
    return tuple(sorted(case[0])), tuple(sorted(case[1]))


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def construct_cases():
    addresses = list(product(range(10), repeat=2))
    delta = {(i, j): csub(G[i], G[j]) for i in range(10) for j in range(10)}
    generic = set()
    events = defaultdict(lambda: {"unit": set(), "collision": set()})
    impossible = Counter()
    for v, w in combinations(range(100), 2):
        a, b = (delta[i, j] for i, j in zip(addresses[v], addresses[w]))
        for kind, target in (("unit", 1), ("collision", 0)):
            line = event_line(a, b, target)
            if line is None:
                hit = add(norm(a), norm(b)) == (F(target), F(0))
                if kind == "unit" and hit:
                    generic.add((v, w))
                elif hit:
                    raise RuntimeError("identical distinct formal addresses")
                else:
                    impossible[kind] += 1
            else:
                roots = line_roots(line)
                if roots == []:
                    impossible[kind] += 1
                else:
                    events[line][kind].add((v, w))

    root_lines = defaultdict(set)
    nonfield_lines = set()
    for line in events:
        roots = line_roots(line)
        if roots is None:
            nonfield_lines.add(line)
        else:
            for root in roots:
                root_lines[root].add(line)
    signatures = {frozenset((line,)) for line in nonfield_lines}
    signatures.update(frozenset(lines) for lines in root_lines.values())
    cases = {(frozenset(generic), frozenset())}
    for signature in signatures:
        unit = set(generic)
        collision = set()
        for line in signature:
            unit.update(events[line]["unit"])
            collision.update(events[line]["collision"])
        cases.add((frozenset(unit), frozenset(collision)))
    ordered = sorted(cases, key=case_key)
    return ordered, generic, events, root_lines, nonfield_lines, impossible


def var(v, colour): return 4 * v + colour + 1


def solve_case(case):
    unit, collision = case
    clauses = []
    for v in range(100):
        clauses.append([var(v, c) for c in range(4)])
        for c, d in combinations(range(4), 2):
            clauses.append([-var(v, c), -var(v, d)])
    for u, v in unit:
        for c in range(4):
            clauses.append([-var(u, c), -var(v, c)])
    for u, v in collision:
        for c in range(4):
            clauses.append([-var(u, c), var(v, c)])
            clauses.append([var(u, c), -var(v, c)])
    clauses.extend(([var(0, 0)], [var(10, 1)], [var(20, 2)]))
    with Cadical195(bootstrap_with=clauses) as solver:
        if not solver.solve():
            raise RuntimeError("non-four-colourable rotational sum found")
        positive = {literal for literal in solver.get_model() if literal > 0}
    word = "".join(str(next(c for c in range(4) if var(v, c) in positive)) for v in range(100))
    if not covers(word, case):
        raise RuntimeError("decoded model failed direct check")
    return word


def covers(word, case):
    unit, collision = case
    return all(word[u] != word[v] for u, v in unit) and all(word[u] == word[v] for u, v in collision)


def quotient_counts(case):
    unit, collision = case
    parent = list(range(100))
    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    for u, v in collision:
        u, v = find(u), find(v)
        if u != v:
            parent[v] = u
    edges = set()
    for u, v in unit:
        u, v = find(u), find(v)
        if u == v:
            raise RuntimeError("unit edge collapsed")
        edges.add(tuple(sorted((u, v))))
    return len({find(v) for v in range(100)}), len(edges)


def main():
    base_edges = [list(e) for e in combinations(range(10), 2) if norm(csub(G[e[0]], G[e[1]])) == O]
    if len(base_edges) != 18:
        raise RuntimeError("wrong Golomb graph")
    cases, generic, events, root_lines, nonfield_lines, impossible = construct_cases()
    if (len(generic), len(events), len(root_lines), len(nonfield_lines), len(cases)) != (360, 432, 78, 126, 205):
        raise RuntimeError("event census mismatch")

    candidates = []
    for case in cases:
        word = solve_case(case)
        if word not in candidates:
            candidates.append(word)
    masks = [{i for i, case in enumerate(cases) if covers(word, case)} for word in candidates]
    unseen = set(range(len(cases)))
    library = []
    selected_words = []
    while unseen:
        k = max(range(len(candidates)), key=lambda j: (len(masks[j] & unseen), -j))
        gain = masks[k] & unseen
        if not gain:
            raise RuntimeError("failed colouring cover")
        selected_words.append(candidates[k])
        library.append({
            "word": candidates[k],
            "coverage_count": len(masks[k]),
            "new_coverage_count": len(gain),
            "trigger_case": min(gain),
        })
        unseen -= gain
    first_cover = [next(i for i, word in enumerate(selected_words) if covers(word, case)) for case in cases]
    qhist = Counter(quotient_counts(case) for case in cases)
    case_rows = [
        [[list(e) for e in sorted(unit)], [[[v, w], "="] for v, w in sorted(collision)]]
        for unit, collision in cases
    ]
    certificate = {
        "schema": "golomb-rotation-sum-cover-v1",
        "construction": {
            "base_vertices": 10,
            "base_edges": 18,
            "formal_addresses": 100,
            "formal_pairs": 4950,
            "generic_edges": 360,
            "real_event_lines": 432,
            "field_valued_exceptional_parameters": 78,
            "nonfield_secant_lines": 126,
            "exceptional_parameters": 330,
            "event_cases": 204,
            "cases_with_generic": 205,
            "physical_order_range": [46, 100],
            "physical_edge_range": [141, 372],
            "quotient_histogram": [
                {"vertices": v, "edges": e, "cases": n}
                for (v, e), n in sorted(qhist.items())
            ],
            "event_pair_incidences": {
                "unit": sum(len(row["unit"]) for row in events.values()),
                "collision": sum(len(row["collision"]) for row in events.values()),
            },
            "discarded_constant_or_nonreal_pair_conditions": dict(sorted(impossible.items())),
        },
        "hashes": {
            "base_rows_sha256": digest(ROWS),
            "base_edges_sha256": digest(base_edges),
            "generic_edges_sha256": digest([list(e) for e in sorted(generic)]),
            "cases_sha256": digest(case_rows),
            "first_cover_rows_sha256": hashlib.sha256(bytes(first_cover)).hexdigest(),
        },
        "base_four_colouring": "".join(selected_words[0][10 * i] for i in range(10)),
        "library": library,
        "target_found": False,
    }
    (HERE / "certificate.json").write_text(json.dumps(certificate, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps({
        "cases": len(cases),
        "colouring_library_rows": len(library),
        "distinct_sat_words": len(candidates),
        "exceptional_parameters": 330,
        "target_found": False,
        **certificate["hashes"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
