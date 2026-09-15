"""Producer-side exact model for two Moser reflection-closure rounds."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_moser_all_terminal_contacts/certificate.json"
SCALE2 = 144
ONE = (SCALE2, 0, 0, 0)

# Canonical named colourings found during the bounded selector.  They are
# witnesses, not solver premises: the verifier checks them from scratch.
S0_NONEXTENDING = "0010200212030312121120001"
S1_NONEXTENDING = (
    "012330011111230303003232021133030212321312330303022113120022313301220120"
    "3230311022220202000022020010220032211111111"
)
S2_FOUR_WORD = (
    "012000032223112112232000232211330223122133330331301022131231031131302213"
    "331303331211313330331000031111000333000000012223130222212011201223000322"
    "222110302223212030002012200130030023020002231222011001200211123121001210"
    "010022033331332311020210122202020110201101113002220113313322313333232222"
    "123132111031212220133222020333331031311330212223111331122301133012022333"
    "21112323301311322222000020123201012021"
)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(a, b):
    out = [0, 0, 0, 0]
    for i in range(4):
        for j in range(4):
            common = i & j
            factor = (3 if common & 1 else 1) * (11 if common & 2 else 1)
            out[i ^ j] += a[i] * b[j] * factor
    return tuple(out)


def norm2(p, q):
    dx = sub(p[0], q[0])
    dy = sub(p[1], q[1])
    return add(mul(dx, dx), mul(dy, dy))


def strict_edges(points):
    return [(i, j) for i, j in combinations(range(len(points)), 2) if norm2(points[i], points[j]) == ONE]


def closure(points):
    edges = strict_edges(points)
    adj = [[] for _ in points]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    out = list(points)
    index = {p: i for i, p in enumerate(out)}
    routes = []
    for r, ns in enumerate(adj):
        for p, q in combinations(ns, 2):
            z = (sub(add(points[p][0], points[q][0]), points[r][0]),
                 sub(add(points[p][1], points[q][1]), points[r][1]))
            if z not in index:
                index[z] = len(out)
                out.append(z)
            routes.append((r, p, q, index[z]))
    return out, edges, routes


def stream_hash(rows):
    blob = "".join(",".join(map(str, row)) + "\n" for row in rows).encode()
    return hashlib.sha256(blob).hexdigest()


def point_hash(points):
    return stream_hash([p[0] + p[1] for p in points])


def graph_stats(points, edges, routes, next_count):
    deg = [0] * len(points)
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    return {
        "points": len(points),
        "unit_edges": len(edges),
        "unit_two_paths": len(routes),
        "next_points": next_count,
        "minimum_degree": min(deg),
        "maximum_degree": max(deg),
        "degree_histogram": {str(k): v for k, v in sorted(Counter(deg).items())},
        "point_sha256": point_hash(points),
        "edge_sha256": stream_hash(edges),
        "route_sha256": stream_hash(routes),
    }


def proper(word, n, edges):
    return len(word) == n and set(word) <= set("0123") and all(word[a] != word[b] for a, b in edges)


def propagation(points, edges, base_word):
    n = len(points)
    b = len(base_word)
    adj = [[] for _ in points]
    for a, c in edges:
        adj[a].append(c)
        adj[c].append(a)
    domains = [15] * n
    for i, c in enumerate(base_word):
        domains[i] = 1 << int(c)
    trace = []
    rounds = 0
    forced = 0
    while True:
        rounds += 1
        changed = False
        for x in range(b, n):
            old = domains[x]
            singleton_neighbour = {}
            for y in adj[x]:
                d = domains[y]
                if d and not d & (d - 1):
                    singleton_neighbour[d] = y
            new = old & ~sum(singleton_neighbour)
            if new == old:
                continue
            changed = True
            for colour in range(4):
                bit = 1 << colour
                if old & bit and not new & bit:
                    trace.append((x, colour, singleton_neighbour[bit]))
            domains[x] = new
            if new and not new & (new - 1) and old & (old - 1):
                forced += 1
            if not new:
                return {
                    "contradiction": True,
                    "rounds": rounds,
                    "colour_removals": len(trace),
                    "forced_vertices": forced,
                    "empty_vertex": x,
                    "trace_sha256": stream_hash(trace),
                }
        if not changed:
            return {
                "contradiction": False,
                "rounds": rounds,
                "colour_removals": len(trace),
                "forced_vertices": forced,
                "trace_sha256": stream_hash(trace),
            }


def build_certificate():
    source_bytes = SOURCE.read_bytes()
    source = json.loads(source_bytes)
    if source["scale"] != 12 or source["basis"] != ["1", "sqrt3", "sqrt11", "sqrt33"]:
        raise ValueError("unexpected source coordinate model")
    s0 = [(tuple(x), tuple(y)) for x, y in source["C"]]
    s1, e0, r0 = closure(s0)
    s2, e1, r1 = closure(s1)
    s3, e2, r2 = closure(s2)
    if not proper(S0_NONEXTENDING, len(s0), e0):
        raise ValueError("bad S0 relation witness")
    if not proper(S1_NONEXTENDING, len(s1), e1):
        raise ValueError("bad S1 relation witness")
    if not proper(S2_FOUR_WORD, len(s2), e2):
        raise ValueError("bad S2 colouring")
    p01 = propagation(s1, e1, S0_NONEXTENDING)
    p12 = propagation(s2, e2, S1_NONEXTENDING)
    if not p01["contradiction"] or not p12["contradiction"]:
        raise ValueError("relation witness does not propagate to contradiction")
    return {
        "schema": "hn-moser-reflection-closure-gain-v1",
        "source_certificate_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "scale": 12,
        "basis": source["basis"],
        "rounds": [
            graph_stats(s0, e0, r0, len(s1)),
            graph_stats(s1, e1, r1, len(s2)),
            graph_stats(s2, e2, r2, len(s3)),
        ],
        "s0_nonextending_word": S0_NONEXTENDING,
        "s0_to_s1_propagation": p01,
        "s1_nonextending_word": S1_NONEXTENDING,
        "s1_to_s2_propagation": p12,
        "s2_four_word": S2_FOUR_WORD,
        "s1_extending_word": S2_FOUR_WORD[:len(s1)],
        "s0_extending_word": S2_FOUR_WORD[:len(s0)],
        "natural_next_round_points": len(s3),
        "record_candidate": False,
        "status": "EXACT_TWO_STRICT_RELATION_GAINS_CAP_STOPS_AT_CHI4",
    }
