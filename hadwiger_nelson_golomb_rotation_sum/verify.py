#!/usr/bin/env python3
"""Independent standard-library verifier for every Golomb rotational sum."""
from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations, product
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
Z = (F(0), F(0))
O = (F(1), F(0))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add(a, b): return a[0] + b[0], a[1] + b[1]
def neg(a): return -a[0], -a[1]
def sub(a, b): return add(a, neg(b))
def mul(a, b): return a[0] * b[0] + 33 * a[1] * b[1], a[0] * b[1] + a[1] * b[0]
def scale(a, q): return a[0] * q, a[1] * q


def inv(a):
    d = a[0] * a[0] - 33 * a[1] * a[1]
    require(d != 0, "division by zero")
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
    d = x * x - 33 * y * y
    return ((x > 0) - (x < 0)) * ((d > 0) - (d < 0))


def rational_sqrt(x):
    if x < 0:
        return None
    a, b = isqrt(x.numerator), isqrt(x.denominator)
    return F(a, b) if a * a == x.numerator and b * b == x.denominator else None


def field_sqrt(z):
    """Return one square root in Q(sqrt(33)), if one exists."""
    a, b = z
    if not b:
        p = rational_sqrt(a)
        if p is not None:
            return p, F(0)
        q = rational_sqrt(a / 33)
        return (F(0), q) if q is not None else None
    root_norm = rational_sqrt(a * a - 33 * b * b)
    if root_norm is None:
        return None
    for signed in (root_norm, -root_norm):
        p = rational_sqrt((a + signed) / 2)
        if p not in (None, 0):
            q = b / (2 * p)
            if mul((p, q), (p, q)) == z:
                return p, q
    return None


def trim(poly):
    poly = list(poly)
    while poly and poly[-1] == Z:
        poly.pop()
    return poly


def canonical(poly):
    poly = trim(poly)
    return tuple(div(c, poly[-1]) for c in poly) if poly else ()


def poly_mul(a, b):
    out = [Z] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = add(out[i + j], mul(x, y))
    return canonical(out)


def irreducible_real_factors(poly):
    """Distinct real-root factors of a degree-at-most-two polynomial."""
    if len(poly) == 2:
        return [poly]
    require(len(poly) == 3, "bad event degree")
    c, b, a = poly
    discriminant = sub(mul(b, b), scale(mul(a, c), 4))
    root = field_sqrt(discriminant)
    if root is None:
        return [poly] if sign(discriminant) > 0 else []
    roots = {div(add(neg(b), signed), scale(a, 2)) for signed in (root, neg(root))}
    factors = [canonical((neg(r), O)) for r in sorted(roots)]
    reconstructed = (poly_mul(factors[0], factors[0]) if len(factors) == 1 else poly_mul(factors[0], factors[1]))
    require(reconstructed == poly, "incorrect quadratic splitting")
    return factors


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


def conjugate_product(a, b):
    return (
        add(mul(a[0], b[0]), scale(mul(a[1], b[1]), 3)),
        sub(mul(a[0], b[1]), mul(a[1], b[0])),
    )


def event_polynomial(a, b, target):
    """D*(|a+u*b|^2-target), u=(1+i*sqrt(3)t)/(1-i*sqrt(3)t)."""
    p, q = conjugate_product(a, b)
    k = sub(add(norm(a), norm(b)), (F(target), F(0)))
    return canonical((add(k, scale(p, 2)), scale(q, -12), sub(scale(k, 3), scale(p, 6))))


def encode_k(a):
    return [[a[0].numerator, a[0].denominator], [a[1].numerator, a[1].denominator]]


def encode_factor(factor):
    return [encode_k(c) for c in factor]


def case_key(case):
    return tuple(sorted(case[0])), tuple(sorted(case[1]))


def case_rows(cases):
    return [
        [[list(e) for e in sorted(unit)], [[[v, w], "="] for v, w in sorted(collision)]]
        for unit, collision in cases
    ]


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def construct_cases():
    addresses = list(product(range(10), repeat=2))
    delta = {(i, j): csub(G[i], G[j]) for i in range(10) for j in range(10)}
    generic = set()
    events = defaultdict(lambda: {"unit": set(), "collision": set()})
    impossible = Counter()
    real_event_polynomials = set()
    event_pair_incidences = Counter()
    for v, w in combinations(range(100), 2):
        a, b = (delta[i, j] for i, j in zip(addresses[v], addresses[w]))
        minus_norm = norm(csub(a, b))
        for kind, target in (("unit", 1), ("collision", 0)):
            poly = event_polynomial(a, b, target)
            minus_hit = minus_norm == (F(target), F(0))
            if not poly:
                require(kind == "unit", "generic collision")
                generic.add((v, w))
                continue
            factors = irreducible_real_factors(poly) if len(poly) > 1 else []
            if not factors and not minus_hit:
                impossible[kind] += 1
            elif poly:
                # A constant polynomial with only the omitted root represents
                # the unique tangent line at u=-1.
                real_event_polynomials.add(poly if factors else ("minus_tangent",))
                event_pair_incidences[kind] += 1
            for factor in factors:
                events[factor][kind].add((v, w))

    minus_unit, minus_collision = set(), set()
    for v, w in combinations(range(100), 2):
        i, j = addresses[v]
        k, ell = addresses[w]
        difference = csub(csub(G[i], G[k]), csub(G[j], G[ell]))
        squared = norm(difference)
        if squared == O:
            minus_unit.add((v, w))
        if squared == Z:
            minus_collision.add((v, w))

    event_cases = {
        (frozenset(generic | row["unit"]), frozenset(row["collision"]))
        for row in events.values()
    }
    event_cases.add((frozenset(minus_unit), frozenset(minus_collision)))
    cases = {(frozenset(generic), frozenset())} | event_cases
    ordered = sorted(cases, key=case_key)
    factor_rows = [
        {
            "factor": encode_factor(factor),
            "unit": [list(e) for e in sorted(events[factor]["unit"])],
            "collision": [list(e) for e in sorted(events[factor]["collision"])],
        }
        for factor in sorted(events)
    ]
    return ordered, generic, events, factor_rows, impossible, real_event_polynomials, event_pair_incidences


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
        require(u != v, "unit pair collapses")
        edges.add(tuple(sorted((u, v))))
    return len({find(v) for v in range(100)}), len(edges)


def covers(word, case):
    unit, collision = case
    return all(word[u] != word[v] for u, v in unit) and all(word[u] == word[v] for u, v in collision)


def validate_certificate(cert, cases, metadata, hashes, base_edges):
    require(cert.get("schema") == "golomb-rotation-sum-cover-v1", "wrong schema")
    require(cert.get("target_found") is False, "wrong target flag")
    require(cert.get("construction") == metadata, "construction metadata mismatch")
    claimed_hashes = cert.get("hashes")
    require(type(claimed_hashes) is dict and claimed_hashes == hashes, "hash mismatch")

    base_word = cert.get("base_four_colouring")
    require(type(base_word) is str and len(base_word) == 10 and set(base_word) <= set("0123"), "bad base word")
    require(all(base_word[u] != base_word[v] for u, v in base_edges), "improper base four-colouring")

    library = cert.get("library")
    require(type(library) is list and len(library) == 32, "wrong library size")
    seen = set()
    coverage_sets = []
    for row in library:
        require(type(row) is dict and set(row) == {"word", "coverage_count", "new_coverage_count", "trigger_case"}, "bad library row")
        word = row["word"]
        require(type(word) is str and len(word) == 100 and set(word) <= set("0123"), "bad colour word")
        require([word[v] for v in (0, 10, 20)] == ["0", "1", "2"], "triangle pin mismatch")
        covered = {i for i, case in enumerate(cases) if covers(word, case)}
        trigger = row["trigger_case"]
        require(type(trigger) is int and 0 <= trigger < len(cases) and trigger in covered, "bad trigger")
        require(row["coverage_count"] == len(covered), "wrong coverage count")
        require(row["new_coverage_count"] == len(covered - seen), "wrong new coverage count")
        require(covered - seen, "redundant library row")
        seen |= covered
        coverage_sets.append(covered)
    require(seen == set(range(len(cases))), "incomplete case cover")
    first_cover = [next(i for i, covered in enumerate(coverage_sets) if j in covered) for j in range(len(cases))]
    require(hashlib.sha256(bytes(first_cover)).hexdigest() == hashes["first_cover_rows_sha256"], "first-cover hash mismatch")


def reject_controls(cert, cases, metadata, hashes, base_edges):
    bad_cases = []
    bad = copy.deepcopy(cert); bad["schema"] = "wrong"; bad_cases.append(bad)
    bad = copy.deepcopy(cert); bad["target_found"] = True; bad_cases.append(bad)
    bad = copy.deepcopy(cert); bad["construction"]["cases_with_generic"] += 1; bad_cases.append(bad)
    bad = copy.deepcopy(cert); bad["hashes"]["cases_sha256"] = "0" * 64; bad_cases.append(bad)
    bad = copy.deepcopy(cert); bad["base_four_colouring"] = "0" * 10; bad_cases.append(bad)
    bad = copy.deepcopy(cert); bad["library"] = bad["library"][:-1]; bad_cases.append(bad)
    bad = copy.deepcopy(cert); bad["library"][0]["word"] = "x" + bad["library"][0]["word"][1:]; bad_cases.append(bad)
    bad = copy.deepcopy(cert); bad["library"][0]["coverage_count"] += 1; bad_cases.append(bad)
    rejected = 0
    for bad in bad_cases:
        try:
            validate_certificate(bad, cases, metadata, hashes, base_edges)
        except (ValueError, KeyError, TypeError):
            rejected += 1
    require(rejected == len(bad_cases), "malformed control accepted")
    return rejected


def main():
    cert = json.loads((HERE / "certificate.json").read_text())
    require(len(set(ROWS)) == 10, "duplicate Golomb rows")
    require(all(sign(norm(csub(G[u], G[v]))) > 0 for u, v in combinations(range(10), 2)), "coincident Golomb points")
    base_edges = [list(e) for e in combinations(range(10), 2) if norm(csub(G[e[0]], G[e[1]])) == O]
    require(len(base_edges) == 18, "wrong strict Golomb graph")
    # The triangle 0,1,2 fixes every three-colour palette permutation.
    require(all(list(e) in base_edges for e in ((0, 1), (0, 2), (1, 2))), "missing base triangle")
    three_colourings = 0
    for tail in product(range(3), repeat=7):
        word = (0, 1, 2) + tail
        three_colourings += all(word[u] != word[v] for u, v in base_edges)
    require(three_colourings == 0, "Golomb graph unexpectedly three-colourable")

    cases, generic, events, factor_rows, impossible, real_event_polynomials, event_pair_incidences = construct_cases()
    factor_degrees = Counter(len(factor) - 1 for factor in events)
    qhist = Counter(quotient_counts(case) for case in cases)
    metadata = {
        "base_vertices": 10,
        "base_edges": 18,
        "formal_addresses": 100,
        "formal_pairs": 4950,
        "generic_edges": 360,
        "real_event_lines": len(real_event_polynomials),
        "field_valued_exceptional_parameters": factor_degrees[1] + 1,
        "nonfield_secant_lines": factor_degrees[2],
        "exceptional_parameters": 1 + sum(degree * count for degree, count in factor_degrees.items()),
        "event_cases": len(cases) - 1,
        "cases_with_generic": len(cases),
        "physical_order_range": [min(v for v, _ in qhist), max(v for v, _ in qhist)],
        "physical_edge_range": [min(e for _, e in qhist), max(e for _, e in qhist)],
        "quotient_histogram": [
            {"vertices": v, "edges": e, "cases": n}
            for (v, e), n in sorted(qhist.items())
        ],
        "event_pair_incidences": dict(sorted(event_pair_incidences.items())),
        "discarded_constant_or_nonreal_pair_conditions": dict(sorted(impossible.items())),
    }
    require(len(events) == 203 and factor_degrees == {1: 77, 2: 126}, "wrong factor census")
    require(len(cases) == 205 and len(generic) == 360, "wrong case census")
    hashes = {
        "base_rows_sha256": digest(ROWS),
        "base_edges_sha256": digest(base_edges),
        "generic_edges_sha256": digest([list(e) for e in sorted(generic)]),
        "cases_sha256": digest(case_rows(cases)),
        "first_cover_rows_sha256": cert.get("hashes", {}).get("first_cover_rows_sha256"),
    }
    validate_certificate(cert, cases, metadata, hashes, base_edges)
    rejected = reject_controls(cert, cases, metadata, hashes, base_edges)
    output = {
        "verified": True,
        "all_members_four_colourable": True,
        "all_members_exactly_four_chromatic": True,
        "base_vertices": 10,
        "base_edges": 18,
        "formal_addresses": 100,
        "finite_event_factors": len(events),
        "linear_factors": factor_degrees[1],
        "irreducible_quadratic_real_factors": factor_degrees[2],
        "exceptional_parameters": 330,
        "event_cases": 204,
        "cases_with_generic": len(cases),
        "physical_order_range": [46, 100],
        "physical_edge_range": [141, 372],
        "colouring_library_rows": len(cert["library"]),
        "three_colourings_with_triangle_pin": three_colourings,
        "malformed_controls_rejected": rejected,
        "factor_events_sha256": digest(factor_rows),
        "hashes": hashes,
        "target_found": False,
    }
    print(json.dumps(output, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
