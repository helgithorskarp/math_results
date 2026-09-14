#!/usr/bin/env python3
"""Solver-independent exact verifier for three fixed-weight HN gates."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def ftext(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def flatten(value):
    if isinstance(value, F):
        return [ftext(value)]
    out = []
    for item in value:
        out.extend(flatten(item))
    return out


def graph_hashes(points, edges):
    point_stream = "".join(f"{i}:" + ",".join(flatten(point)) + "\n" for i, point in enumerate(points)).encode()
    edge_stream = "".join(f"{a},{b}\n" for a, b in edges).encode()
    return hashlib.sha256(point_stream).hexdigest(), hashlib.sha256(edge_stream).hexdigest()


def physical_graph(address_points, is_unit):
    by_point = {}
    for address, point in address_points:
        by_point.setdefault(point, []).append(address)
    points = sorted(by_point)
    edges = []
    adjacency = [set() for _ in points]
    for i, a in enumerate(points):
        for j in range(i + 1, len(points)):
            if is_unit(a, points[j]):
                edges.append((i, j))
                adjacency[i].add(j)
                adjacency[j].add(i)
    return points, [by_point[p] for p in points], edges, adjacency


def check_word(case, word, colours, points, edges, adjacency):
    require(len(word) == len(points), case + ": word length")
    require(all(c in "0123456789" and int(c) < colours for c in word), case + ": word alphabet")
    require(all(word[a] != word[b] for a, b in edges), case + ": monochromatic unit edge")
    triangle = next((a, b, min(adjacency[a] & adjacency[b])) for a, b in edges if adjacency[a] & adjacency[b])
    require(all(b in adjacency[a] for a, b in combinations(triangle, 2)), case + ": triangle")
    return triangle


# Q(sqrt(3)) real arithmetic for the 12-gon case.
QZERO = (F(0), F(0))
QONE = (F(1), F(0))


def qadd(a, b):
    return a[0] + b[0], a[1] + b[1]


def qsub(a, b):
    return a[0] - b[0], a[1] - b[1]


def qmul(a, b):
    return a[0] * b[0] + 3 * a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def p12_add(a, b):
    return qadd(a[0], b[0]), qadd(a[1], b[1])


def p12_sub(a, b):
    return qsub(a[0], b[0]), qsub(a[1], b[1])


def p12_norm(a):
    return qadd(qmul(a[0], a[0]), qmul(a[1], a[1]))


def regular12():
    h = F(1, 2)
    r = (F(0), h)
    z = QZERO
    q = lambda x: (F(x), F(0))
    directions = [
        (q(1), z), (r, q(h)), (q(h), r), (z, q(1)), (q(-h), r),
        ((F(0), -h), q(h)), (q(-1), z), ((F(0), -h), q(-h)),
        (q(-h), (F(0), -h)), (z, q(-1)), (q(h), (F(0), -h)),
    ]
    require(all(p12_norm(d) == QONE for d in directions), "regular12 unit directions")
    address_points = []
    for address in combinations(range(11), 5):
        point = (QZERO, QZERO)
        for i in address:
            point = p12_add(point, directions[i])
        address_points.append((address, point))
    return physical_graph(address_points, lambda a, b: p12_norm(p12_sub(a, b)) == QONE)


# Q(zeta_18), Phi_18(X)=X^6-X^3+1.
CZERO = (F(0),) * 6
CONE = (F(1),) + (F(0),) * 5


def cadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def cneg(a):
    return tuple(-x for x in a)


def creduce(values):
    values = list(map(F, values))
    values += [F(0)] * max(0, 6-len(values))
    for degree in range(len(values)-1, 5, -1):
        coefficient = values[degree]
        values[degree-3] += coefficient
        values[degree-6] -= coefficient
    return tuple(values[:6])


def cmul(a, b):
    raw = [F(0)] * 11
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            raw[i+j] += x*y
    return creduce(raw)


def cpow(exponent):
    exponent %= 18
    raw = [F(0)] * (exponent+1)
    raw[exponent] = 1
    return creduce(raw)


CCONJ = tuple(cpow((-j) % 18) for j in range(6))


def cconj(a):
    out = CZERO
    for coefficient, image in zip(a, CCONJ):
        out = cadd(out, tuple(coefficient*x for x in image))
    return out


def cnorm(a):
    return cmul(a, cconj(a))


def regular18():
    directions = [cpow(j) for j in range(12)]
    require(all(cnorm(d) == CONE for d in directions), "regular18 unit directions")
    require(cadd(cadd(cpow(6), cneg(cpow(3))), CONE) == CZERO, "Phi18 identity")
    require(cpow(9) == cneg(CONE) and cpow(18) == CONE, "zeta18 order")
    address_points = []
    for address in combinations(range(12), 4):
        point = CZERO
        for i in address:
            point = cadd(point, directions[i])
        address_points.append((address, point))
    return physical_graph(address_points, lambda a, b: cnorm(cadd(a, cneg(b))) == CONE)


# E=Q(sqrt(33),i sqrt(3)) in basis 1,sqrt33,i sqrt3,i sqrt11.
EZERO = (F(0),) * 4
EONE = (F(1), F(0), F(0), F(0))
IALPHA = (F(0), F(0), F(1), F(0))
IBETA = (F(0), F(0), F(0), F(1))


def eadd(a, b):
    return tuple(x+y for x, y in zip(a, b))


def escale(a, q):
    return tuple(q*x for x in a)


def esub(a, b):
    return eadd(a, escale(b, -1))


def emul(x, y):
    a, b, c, d = x
    A, B, C, D = y
    return (a*A+33*b*B-3*c*C-11*d*D,
            a*B+b*A-c*D-d*C,
            a*C+c*A+11*(b*D+d*B),
            a*D+d*A+3*(b*C+c*B))


def econj(x):
    return x[0], x[1], -x[2], -x[3]


def enorm(x):
    return emul(x, econj(x))


# F=E(sqrt5,sqrt13), indexed by square-class bits.
FZERO = (EZERO,) * 4
FONE = (EONE, EZERO, EZERO, EZERO)


def xadd(a, b):
    return tuple(eadd(x, y) for x, y in zip(a, b))


def xscale(a, q):
    return tuple(escale(x, q) for x in a)


def xmul(a, b):
    out = [EZERO] * 4
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            common = i & j
            factor = (5 if common & 1 else 1) * (13 if common & 2 else 1)
            out[i ^ j] = eadd(out[i ^ j], escale(emul(x, y), factor))
    return tuple(out)


def xconj(a):
    return tuple(econj(x) for x in a)


def xnorm(a):
    return xmul(a, xconj(a))


def xembed(a):
    return a, EZERO, EZERO, EZERO


def xcanonical(a):
    return min(a, xscale(a, -1))


def spindle():
    rho = escale(eadd(EONE, IALPHA), F(1, 2))
    eta = escale(eadd(escale(EONE, 5), IBETA), F(1, 6))
    return [EZERO, EONE, rho, eadd(EONE, rho), eta, emul(eta, rho), emul(eta, eadd(EONE, rho))]


def golomb():
    rows = [(0,0,0,0),(36,0,0,0),(18,0,18,0),(-18,0,18,0),(-36,0,0,0),
            (-18,0,-18,0),(18,0,-18,0),(6,0,0,2),(-3,-3,3,-1),(-3,3,-3,-1)]
    return [(F(a,36), F(b,36), F(c,36), F(d,12)) for a,b,c,d in rows]


def unit_directions(points):
    out = set()
    for a, b in combinations(points, 2):
        delta = esub(a, b)
        if enorm(delta) == EONE:
            out.add(min(delta, escale(delta, -1)))
    return sorted(out)


def mixed_weight5():
    base = sorted(set(unit_directions(spindle()) + unit_directions(golomb())))
    require(len(base) == 13, "mixed base direction count")
    u = (escale(EONE, F(7,8)), escale(IALPHA, F(1,8)), EZERO, EZERO)
    v = (escale(EONE, F(5,8)), EZERO, escale(IALPHA, F(1,8)), EZERO)
    require(xnorm(u) == xnorm(v) == FONE, "mixed phase norms")
    blocks = [[xcanonical(xmul(phase, xembed(z))) for z in base] for phase in (FONE, u, v)]
    indices = ((0, (1,5,6,7)), (1, (1,6,7,10)), (2, (10,12)))
    directions = [blocks[block][i] for block, chosen in indices for i in chosen]
    require(len(directions) == 10 and all(xnorm(d) == FONE for d in directions), "mixed unit directions")
    address_points = []
    for address in combinations(range(10), 5):
        point = FZERO
        for i in address:
            point = xadd(point, directions[i])
        address_points.append((address, point))
    return physical_graph(address_points, lambda a, b: xnorm(xadd(a, xscale(b, -1))) == FONE)


def summarize(name, formal, built, certificate):
    points, addresses, edges, adjacency = built
    colours = certificate[name]["colours"]
    word = certificate[name]["word"]
    triangle = check_word(name, word, colours, points, edges, adjacency)
    point_hash, edge_hash = graph_hashes(points, edges)
    return {
        "formal_addresses": formal,
        "vertices": len(points),
        "edges": len(edges),
        "address_collisions": formal-len(points),
        "multi_address_vertices": sum(len(a) > 1 for a in addresses),
        "maximum_address_multiplicity": max(map(len, addresses)),
        "maximum_degree": max(map(len, adjacency)),
        "colours_in_checked_word": len(set(word)),
        "triangle": list(triangle),
        "point_sha256": point_hash,
        "edge_sha256": edge_hash,
    }


def run(certificate_path):
    certificate = json.loads(certificate_path.read_text())
    require(set(certificate) == {"regular12_weight5", "regular18_weight4", "mixed_weight5"}, "certificate cases")
    return {
        "regular12_weight5": summarize("regular12_weight5", 462, regular12(), certificate),
        "regular18_weight4": summarize("regular18_weight4", 495, regular18(), certificate),
        "mixed_weight5": summarize("mixed_weight5", 252, mixed_weight5(), certificate),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=ROOT / "certificate.json")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = run(args.certificate)
    if args.check_expected:
        require(result == json.loads((ROOT / "EXPECTED.json").read_text()), "expected result mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
