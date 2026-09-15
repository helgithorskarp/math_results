#!/usr/bin/env python3
"""Independent nested-field geometry and positive-colour audit.

This file imports no submitted arithmetic or graph code.  A scalar is
A+B*sqrt(11), with A,B in Q(sqrt(3)).
"""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEP = HERE.parent / "hadwiger_nelson_parts509_g14_g15_embedding" / "embedding_certificate.json"


def radd(x, y): return x[0] + y[0], x[1] + y[1]
def rneg(x): return -x[0], -x[1]
def rsub(x, y): return radd(x, rneg(y))
def rmul(x, y): return x[0] * y[0] + 3 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]
def rscale(x, q): return q * x[0], q * x[1]
R0 = (Q(0), Q(0))
R1 = (Q(1), Q(0))


def add(x, y): return radd(x[0], y[0]), radd(x[1], y[1])
def neg(x): return rneg(x[0]), rneg(x[1])
def sub(x, y): return add(x, neg(y))
def mul(x, y):
    return radd(rmul(x[0], y[0]), rscale(rmul(x[1], y[1]), Q(11))), radd(rmul(x[0], y[1]), rmul(x[1], y[0]))
def scale(x, q): return rscale(x[0], q), rscale(x[1], q)
K0 = (R0, R0)
K1 = (R1, R0)
SQ11 = (R0, R1)


def padd(p, q): return add(p[0], q[0]), add(p[1], q[1])
def psub(p, q): return sub(p[0], q[0]), sub(p[1], q[1])
def pscale(p, q): return scale(p[0], q), scale(p[1], q)
def d2(p, q):
    x, y = psub(p, q)
    return add(mul(x, x), mul(y, y))


def flat(x): return x[0][0], x[0][1], x[1][0], x[1][1]
def ftxt(x): return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def main():
    if hashlib.sha256(DEP.read_bytes()).hexdigest() != "993121f93b552350a5c5270af3dc052c82c505a86fe7083bc3eb87163271bd8f":
        raise ValueError("dependency hash mismatch")
    source_obj = json.loads(DEP.read_text())
    source = []
    for row in source_obj["g15"]["coordinates"]:
        a, b, c, d = map(Q, row)
        source.append((((a, b), R0), ((c, d), R0)))

    unit, third, four = [], [], []
    for i in range(15):
        for j in range(i + 1, 15):
            value = d2(source[i], source[j])
            if value == K1: unit.append((i, j))
            elif value == (((Q(1, 3), Q(0)), R0)): third.append((i, j))
            elif value == (((Q(4), Q(0)), R0)): four.append((i, j))

    formal = list(source)
    for i, j in third:
        delta = psub(source[j], source[i])
        midpoint = pscale(padd(source[i], source[j]), Q(1, 2))
        offset = (scale(mul(delta[1], SQ11), Q(-1, 2)), scale(mul(delta[0], SQ11), Q(1, 2)))
        formal.extend((padd(midpoint, offset), psub(midpoint, offset)))
    for i, j in four:
        formal.append(pscale(padd(source[i], source[j]), Q(1, 2)))
    points = list(dict.fromkeys(formal))
    edges = [(i, j) for i in range(len(points)) for j in range(i + 1, len(points)) if d2(points[i], points[j]) == K1]

    cert = json.loads((HERE / "certificate.json").read_text())
    if [len(formal), len(points), len(edges)] != [cert["formal_addresses"], cert["physical_vertices"], cert["strict_unit_edges"]]:
        raise ValueError("count mismatch")
    rows = [[[ftxt(v) for v in flat(coordinate)] for coordinate in point] for point in points]
    point_hash = hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    edge_hash = hashlib.sha256(json.dumps([list(e) for e in edges], separators=(",", ":")).encode()).hexdigest()
    if point_hash != cert["point_stream_sha256"] or edge_hash != cert["edge_stream_sha256"]:
        raise ValueError("stream hash mismatch")
    word = cert["four_colouring"]
    if len(word) != len(points) or any(word[u] == word[v] for u, v in edges):
        raise ValueError("four-colour word failure")
    print(json.dumps({"audit": "PASS", "arithmetic": "Q(sqrt(3))(sqrt(11))", "physical_vertices": len(points), "strict_unit_edges": len(edges), "checked_word_edges": len(edges)}, sort_keys=True))


if __name__ == "__main__":
    main()
