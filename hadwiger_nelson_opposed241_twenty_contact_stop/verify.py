#!/usr/bin/env python3
"""Exact checker for one outside-field two-core physical assembly.

Python 3.11+, standard library only.  No solver verdict is used.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / "hadwiger_nelson_opposed241_conditional_core"
B_PATH = ROOT / "hadwiger_nelson_nonmono159_214_lowden2" / "points214.tsv"
SOURCE_CERT_HASH = "37e1397276f931ee1b9b63f4ca5c343a2ac129fa3b1c6d526e4c151031a750e4"
B_HASH = "97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f"
G = [
    (0, 0, 0, 0), (36, 0, 0, 0), (18, 0, 18, 0),
    (-18, 0, 18, 0), (-36, 0, 0, 0), (-18, 0, -18, 0),
    (18, 0, -18, 0), (6, 0, 0, 6), (-3, -3, 3, -3),
    (-3, 3, -3, -3),
]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(rows):
    return hashlib.sha256(("\n".join(rows) + "\n").encode()).hexdigest()


# K = Q(r), r^2 = 33.  A K element is (a,b) = a+b*r.
KZERO = (F(0), F(0))


def ka(a, b=0):
    return (F(a), F(b))


def kadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def kneg(x):
    return (-x[0], -x[1])


def ksub(x, y):
    return kadd(x, kneg(y))


def kmul(x, y):
    return (x[0] * y[0] + 33 * x[1] * y[1],
            x[0] * y[1] + x[1] * y[0])


def kscale(x, c):
    return (x[0] * c, x[1] * c)


def kinv(x):
    d = x[0] * x[0] - 33 * x[1] * x[1]
    need(d != 0, "K division by zero")
    return (x[0] / d, -x[1] / d)


def kdiv(x, y):
    return kmul(x, kinv(y))


# L = K(t), t^2 = T = (2+2*r)/3.  Negative norm proves T is not
# a square in K, so coefficientwise equality in this basis is faithful.
T = (F(2, 3), F(2, 3))
LZERO = (KZERO, KZERO)


def lift(x):
    return (x, KZERO)


def ladd(x, y):
    return (kadd(x[0], y[0]), kadd(x[1], y[1]))


def lneg(x):
    return (kneg(x[0]), kneg(x[1]))


def lsub(x, y):
    return ladd(x, lneg(y))


def lscale(x, c):
    return (kscale(x[0], c), kscale(x[1], c))


def lmul(x, y):
    return (kadd(kmul(x[0], y[0]), kmul(T, kmul(x[1], y[1]))),
            kadd(kmul(x[0], y[1]), kmul(x[1], y[0])))


def lzero(x):
    return x == LZERO


def source_core():
    need(hashlib.sha256(B_PATH.read_bytes()).hexdigest() == B_HASH,
         "B214 fixture hash")
    source_cert_path = SOURCE / "certificate.json"
    need(hashlib.sha256(source_cert_path.read_bytes()).hexdigest() == SOURCE_CERT_HASH,
         "conditional-core certificate hash")
    source_cert = json.loads(source_cert_path.read_text())
    b = []
    for line in B_PATH.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        z = list(map(int, line.split()))
        need(len(z) == 16 and all(z[i] == 0 for i in
             (1, 2, 3, 4, 6, 7, 8, 10, 11, 13, 14, 15)),
             "B214 coordinate basis")
        b.append((3 * z[0], 3 * z[5], 3 * z[9], 3 * z[12]))
    need(len(b) == 214, "B214 order")
    left = [(a - 18, b0, c, d) for a, b0, c, d in b]
    right = [(-a + 18, -b0, c, d) for a, b0, c, d in b]
    points = []
    index = {}
    for block in (G, left, right):
        for p in block:
            if p not in index:
                index[p] = len(points)
                points.append(p)
    need(len(points) == 343, "opposed source order")
    ids = source_cert["source_ids"]
    need(ids == sorted(set(ids)) and len(ids) == 241 and ids[:10] == list(range(10)),
         "conditional-core labels")
    core = [points[i] for i in ids]
    return core


def base_coordinates(rows):
    # Physical coordinate is (X, sqrt(3)*Y), with X,Y in K.
    return [(ka(F(a, 36), F(b, 36)), ka(F(c, 36), F(d, 108)))
            for a, b, c, d in rows]


def knorm(p):
    return kadd(kmul(p[0], p[0]), kscale(kmul(p[1], p[1]), 3))


def kdot(p, q):
    return kadd(kmul(p[0], q[0]), kscale(kmul(p[1], q[1]), 3))


def kcross_y(p, q):
    # Physical cross product divided by sqrt(3).
    return ksub(kmul(p[1], q[0]), kmul(p[0], q[1]))


def rotation(base):
    # Freeze the positive-square-root branch for which core[45] and the
    # rotated core[65] are one unit apart.
    p, q = base[45], base[65]
    d = kdot(p, q)
    k = kcross_y(p, q)
    c = kscale(ksub(kadd(knorm(p), knorm(q)), ka(1)), F(1, 2))
    r2 = kadd(kmul(d, d), kscale(kmul(k, k), 3))
    delta = ksub(r2, kmul(c, c))
    need(kscale(delta, 3) == T, "rotation quadratic parameter")
    co = (kdiv(kmul(c, d), r2), kdiv(k, r2))
    sy = (kdiv(kmul(c, k), r2), kscale(kdiv(d, r2), F(-1, 3)))
    expected_co = ((F(1, 4), F(1, 12)), (F(-5, 16), F(1, 16)))
    expected_sy = ((F(-5, 12), F(1, 12)), (F(-1, 16), F(-1, 48)))
    need(co == expected_co and sy == expected_sy, "rotation coefficients")
    need(ladd(lmul(co, co), lscale(lmul(sy, sy), 3)) == lift(ka(1)),
         "rotation has unit norm")
    return co, sy


def rotate(q, co, sy):
    x, y = q
    return (lsub(lmul(co, lift(x)), lscale(lmul(sy, lift(y)), 3)),
            ladd(lmul(sy, lift(x)), lmul(co, lift(y))))


def unit(p, q):
    dx = lsub(p[0], q[0])
    dy = lsub(p[1], q[1])
    return lzero(lsub(ladd(lmul(dx, dx), lscale(lmul(dy, dy), 3)),
                      lift(ka(1))))


def point_hash(points):
    def fs(x):
        return f"{x.numerator}/{x.denominator}"
    rows = []
    for x, y in points:
        flat = (x[0][0], x[0][1], x[1][0], x[1][1],
                y[0][0], y[0][1], y[1][0], y[1][1])
        rows.append(" ".join(fs(v) for v in flat))
    return digest(rows)


def all_edges(points):
    return [(i, j) for i, j in combinations(range(len(points)), 2)
            if unit(points[i], points[j])]


def build():
    rows = source_core()
    base = base_coordinates(rows)
    co, sy = rotation(base)
    first = [(lift(x), lift(y)) for x, y in base]
    second = [rotate(q, co, sy) for q in base]
    points = []
    index = {}
    maps = []
    for block in (first, second):
        image = []
        for p in block:
            if p not in index:
                index[p] = len(points)
                points.append(p)
            image.append(index[p])
        maps.append(image)
    edges = all_edges(points)
    return points, edges, maps


def graph_audit(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    tin = [-1] * n
    low = [0] * n
    timer = 0
    arts = set()
    bridges = []

    def dfs(v, parent=-1):
        nonlocal timer
        tin[v] = low[v] = timer
        timer += 1
        children = 0
        for u in sorted(adj[v]):
            if u == parent:
                continue
            if tin[u] >= 0:
                low[v] = min(low[v], tin[u])
            else:
                dfs(u, v)
                low[v] = min(low[v], low[u])
                if low[u] > tin[v]:
                    bridges.append((min(u, v), max(u, v)))
                if parent != -1 and low[u] >= tin[v]:
                    arts.add(v)
                children += 1
        if parent == -1 and children > 1:
            arts.add(v)

    dfs(0)
    need(all(t >= 0 for t in tin), "graph connected")
    live = set(range(n))
    queue = [v for v in live if len(adj[v]) < 4]
    while queue:
        v = queue.pop()
        if v not in live:
            continue
        live.remove(v)
        for u in adj[v] & live:
            if len(adj[u] & live) < 4:
                queue.append(u)
    return adj, sorted(arts), sorted(bridges), len(live)


def proper(word, n, edges):
    need(isinstance(word, str) and len(word) == n, "four-word length")
    need(set(word) <= set("0123"), "four-word alphabet")
    need(all(word[a] != word[b] for a, b in edges), "improper four-word")


def golomb_not_three(rows):
    base = base_coordinates(rows[:10])
    pts = [(lift(x), lift(y)) for x, y in base]
    edges = all_edges(pts)
    need(len(edges) == 18 and all(unit(pts[a], pts[b]) for a, b in edges),
         "Golomb graph")
    for tail in product(range(3), repeat=7):
        word = (0, 1, 2) + tail
        if all(word[a] != word[b] for a, b in edges):
            raise ValueError("Golomb three-colouring")
    return len(edges)


def run(cert):
    need(cert["schema"] == "opposed241-twenty-contact-stop-v1", "schema")
    # A square in K has square field norm; T has norm -128/9.
    tnorm = T[0] * T[0] - 33 * T[1] * T[1]
    need(tnorm == F(-128, 9), "T norm")
    rows = source_core()
    points, edges, maps = build()
    n = len(points)
    need(n == 481 and set(maps[0]) & set(maps[1]) == {0}, "collision quotient")
    aset, bset = set(maps[0]), set(maps[1])
    inherited = [e for e in edges if set(e) <= aset or set(e) <= bset]
    cross = [e for e in edges if e not in set(inherited)]
    need(len(edges) == 2002 and len(inherited) == 1982 and len(cross) == 20,
         "complete edge classes")
    need(cross == [tuple(e) for e in cert["cross_edges"]], "cross-edge list")
    ph = point_hash(points)
    eh = digest(f"{a} {b}" for a, b in edges)
    need(ph == cert["point_sha256"] and eh == cert["edge_sha256"], "graph hashes")
    proper(cert["proper4"], n, edges)
    need(golomb_not_three(rows) == 18, "lower chromatic bound")
    adj, arts, bridges, core4 = graph_audit(n, edges)
    need(not arts and not bridges and core4 == n, "nonseparable four-core")
    result = {
        "status": "VERIFIED_FOUR_COLOUR_STOP",
        "points": n,
        "complete_unit_edges": len(edges),
        "all_pairs": n * (n - 1) // 2,
        "source_copies": 2,
        "points_per_source": 241,
        "shared_points": 1,
        "inherited_edges": len(inherited),
        "private_cross_edges": len(cross),
        "minimum_degree": min(map(len, adj)),
        "maximum_degree": max(map(len, adj)),
        "articulations": arts,
        "bridges": bridges,
        "four_core_points": core4,
        "chromatic_number": 4,
        "rotation_parameter_t_squared": ["2/3", "2/3"],
        "rotation_parameter_norm": "-128/9",
        "point_sha256": ph,
        "edge_sha256": eh,
        "four_word_sha256": hashlib.sha256((cert["proper4"] + "\n").encode()).hexdigest(),
        "record_candidate": False,
    }
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    ap.add_argument("--check-expected", action="store_true")
    args = ap.parse_args()
    result = run(json.loads(args.certificate.read_text()))
    if args.check_expected:
        need(result == json.loads((HERE / "EXPECTED.json").read_text()), "expected result")
    print(json.dumps(result, indent=2, sort_keys=True))
