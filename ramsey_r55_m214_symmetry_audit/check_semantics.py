#!/usr/bin/env python3
"""Audit all OPB rows by graph supports, without importing the upstream code.

Five-set coverage uses combinatorial colex ranks. Triangle geometry is inferred
from conjunction rows, then used to check the local triangle equalities. The
checker accepts permutations of terms and of whole five-set/gate blocks; the
separate byte hash pins the canonical upstream file.
"""
from itertools import combinations
from math import comb
from pathlib import Path
import argparse
import hashlib
import json

N = 43
PAIRS = [None] + list(combinations(range(N), 2))
EDGE_ID = {pair: index for index, pair in enumerate(PAIRS) if index}
FIVES = comb(N, 5)
TRIPLES = comb(N, 3)
VARIABLES = comb(N, 2) + TRIPLES
ROWS = 2 * FIVES + 4 * TRIPLES + 3 * N + N - 1
HEADER = f"* #variable= {VARIABLES} #constraint= {ROWS} #equal= 128 intsize= 64"
RANK_TERMS = [[comb(v, i) for v in range(N)] for i in range(6)]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def parse(line):
    words = line.split()
    require(len(words) >= 5 and len(words) % 2 == 1, "malformed row length")
    require(words[-1] == ";" and words[-3] in ("=", ">="), "bad row ending")
    terms = {}
    for k in range(0, len(words) - 3, 2):
        require(words[k + 1].startswith("x"), "bad variable name")
        variable = int(words[k + 1][1:])
        coefficient = int(words[k])
        require(1 <= variable <= VARIABLES and variable not in terms, "bad/duplicate variable")
        require(coefficient != 0, "zero coefficient")
        terms[variable] = coefficient
    return terms, words[-3], int(words[-2])


def expected(row, terms, relation, rhs):
    require(row == (terms, relation, rhs), "constraint semantics mismatch")


def clique_support(edge_ids, size):
    require(len(edge_ids) == comb(size, 2), "wrong clique support size")
    require(all(1 <= x < len(PAIRS) for x in edge_ids), "nonedge in clique support")
    vertices = sorted({v for x in edge_ids for v in PAIRS[x]})
    require(len(vertices) == size, "wrong clique vertex count")
    require({PAIRS[x] for x in edge_ids} == set(combinations(vertices, 2)), "incomplete clique support")
    return vertices


def five_block(positive, negative):
    terms, relation, rhs = positive
    require(relation == ">=" and rhs == 1 and set(terms.values()) == {1}, "wrong blue K5 row")
    vertices = clique_support(terms, 5)
    expected(negative, {x: -1 for x in terms}, ">=", -9)
    return sum(RANK_TERMS[i][v] for i, v in enumerate(vertices, 1))


def gate_block(rows):
    edges = []
    z = None
    for terms, relation, rhs in rows[:3]:
        require(relation == ">=" and rhs == 0 and len(terms) == 2, "wrong triangle upper row")
        positive = [x for x, c in terms.items() if c == 1]
        negative = [x for x, c in terms.items() if c == -1]
        require(len(positive) == len(negative) == 1, "wrong gate signs")
        edge, gate = positive[0], negative[0]
        require(len(PAIRS) <= gate <= VARIABLES, "nontriangle gate variable")
        require(z is None or z == gate, "gate variable changed")
        z = gate
        edges.append(edge)
    require(len(set(edges)) == 3, "repeated gate edge")
    vertices = clique_support(edges, 3)
    expected(rows[3], {z: 1, **{x: -1 for x in edges}}, ">=", -2)
    return z, vertices


def audit(path):
    digest = hashlib.sha256()
    bytes_read = 0
    rows_read = 0
    equalities = 0
    seen_fives = bytearray(FIVES)
    seen_triples = bytearray(TRIPLES)
    seen_z = set()
    incident_z = [set() for _ in range(N)]
    with path.open("rb") as stream:
        raw = stream.readline()
        digest.update(raw)
        bytes_read += len(raw)
        require(raw.decode("ascii").rstrip("\n") == HEADER, "wrong header")

        def read():
            nonlocal bytes_read, rows_read, equalities
            raw = stream.readline()
            require(bool(raw), "premature EOF")
            digest.update(raw)
            bytes_read += len(raw)
            rows_read += 1
            row = parse(raw.decode("ascii"))
            equalities += row[1] == "="
            return row

        for _ in range(FIVES):
            rank = five_block(read(), read())
            require(not seen_fives[rank], "duplicate five-set")
            seen_fives[rank] = 1
        require(all(seen_fives), "missing five-set")
        for _ in range(TRIPLES):
            z, vertices = gate_block([read() for _ in range(4)])
            rank = sum(RANK_TERMS[i][v] for i, v in enumerate(vertices, 1))
            require(z not in seen_z and not seen_triples[rank], "duplicate triangle or gate")
            seen_z.add(z)
            seen_triples[rank] = 1
            for v in vertices:
                incident_z[v].add(z)
        require(all(seen_triples) and len(seen_z) == TRIPLES, "incomplete triangle coverage")
        for v in range(N):
            edges = {EDGE_ID[tuple(sorted((v, w)))]: 1 for w in range(N) if v != w}
            expected(read(), edges, "=", 20 if v < 13 else 21)
        for v in range(N):
            require(len(incident_z[v]) == comb(N - 1, 2), "wrong triangle incidence count")
            expected(read(), {z: 1 for z in incident_z[v]}, "=", 93 if v < 13 else 100)
        for v in range(N):
            edges = {EDGE_ID[tuple(sorted((v, w)))]: 1 for w in range(13) if v != w}
            expected(read(), edges, ">=", 6)
        anchor_red = set(range(6)) | set(range(14, 29))
        for w in range(N):
            if w != 13:
                expected(read(), {EDGE_ID[tuple(sorted((13, w)))]: 1}, "=", int(w in anchor_red))
        require(stream.read(1) == b"", "trailing data")
    require(rows_read == ROWS and equalities == 128, "wrong row totals")
    return {"bytes": bytes_read, "constraints": rows_read, "equalities": equalities,
            "five_sets": FIVES, "triangle_gates": TRIPLES, "variables": VARIABLES,
            "sha256": digest.hexdigest(), "semantic_check": "PASS"}


def mutation_checks():
    """Small semantic controls target different constraint families."""
    terms = {EDGE_ID[p]: 1 for p in combinations(range(5), 2)}
    positive, negative = (terms, ">=", 1), ({x: -1 for x in terms}, ">=", -9)
    require(five_block(positive, negative) == 0, "valid first five-set rejected")
    e = [EDGE_ID[p] for p in combinations(range(3), 2)]
    z = 904
    gate = [({z: -1, x: 1}, ">=", 0) for x in e] + [({z: 1, **{x: -1 for x in e}}, ">=", -2)]
    require(gate_block(gate) == (z, [0, 1, 2]), "valid gate rejected")
    malformed = dict(terms)
    malformed.pop(EDGE_ID[(0, 1)])
    malformed[EDGE_ID[(0, 5)]] = 1
    bad_gate = gate[:3] + [(gate[3][0], ">=", -3)]
    checks = [
        lambda: five_block((malformed, ">=", 1), negative),
        lambda: five_block(positive, (negative[0], ">=", -10)),
        lambda: gate_block(bad_gate),
        lambda: gate_block([gate[0], gate[0], gate[2], gate[3]]),
        lambda: expected(({904: 1}, "=", 93), {904: 1, 905: 1}, "=", 93),
        lambda: expected(({13: 1}, "=", 0), {13: 1}, "=", 1),
        lambda: parse("+1 x1 +1 x1 >= 1 ;"),
        lambda: parse("+1 x13245 >= 1 ;"),
    ]
    for check in checks:
        try:
            check()
        except ValueError:
            continue
        raise ValueError("semantic mutation was accepted")
    return len(checks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("formula", type=Path)
    args = parser.parse_args()
    result = audit(args.formula)
    result["rejected_mutations"] = mutation_checks()
    print(json.dumps(result, sort_keys=True))
