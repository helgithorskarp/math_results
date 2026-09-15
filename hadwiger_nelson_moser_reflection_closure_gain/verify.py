#!/usr/bin/env python3
"""Independent exact checker; imports no producer/model code."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_moser_all_terminal_contacts/certificate.json"
ONE = (144, 0, 0, 0)


def need(q, message):
    if not q:
        raise ValueError(message)


def kadd(a, b):
    return tuple(a[i] + b[i] for i in range(4))


def ksub(a, b):
    return tuple(a[i] - b[i] for i in range(4))


def kmul(a, b):
    # Independent multiplication table in 1,sqrt(3),sqrt(11),sqrt(33).
    return (
        a[0]*b[0] + 3*a[1]*b[1] + 11*a[2]*b[2] + 33*a[3]*b[3],
        a[0]*b[1] + a[1]*b[0] + 11*(a[2]*b[3] + a[3]*b[2]),
        a[0]*b[2] + a[2]*b[0] + 3*(a[1]*b[3] + a[3]*b[1]),
        a[0]*b[3] + a[3]*b[0] + a[1]*b[2] + a[2]*b[1],
    )


def squared_distance(a, b):
    x = ksub(a[0], b[0])
    y = ksub(a[1], b[1])
    return kadd(kmul(x, x), kmul(y, y))


def reconstruct_edges(points):
    return [(a, b) for a, b in combinations(range(len(points)), 2)
            if squared_distance(points[a], points[b]) == ONE]


def sha_rows(rows):
    h = hashlib.sha256()
    for row in rows:
        h.update((",".join(str(x) for x in row) + "\n").encode())
    return h.hexdigest()


def close_once(points):
    edges = reconstruct_edges(points)
    neighbours = [[] for _ in points]
    for a, b in edges:
        neighbours[a].append(b)
        neighbours[b].append(a)
    new_points = list(points)
    lookup = {p: i for i, p in enumerate(new_points)}
    routes = []
    for centre, ns in enumerate(neighbours):
        for a, b in combinations(ns, 2):
            q = (ksub(kadd(points[a][0], points[b][0]), points[centre][0]),
                 ksub(kadd(points[a][1], points[b][1]), points[centre][1]))
            if q not in lookup:
                lookup[q] = len(new_points)
                new_points.append(q)
            routes.append((centre, a, b, lookup[q]))
            # The defining two contacts are checked rather than assumed.
            need(squared_distance(q, points[a]) == ONE, "first reflection contact failed")
            need(squared_distance(q, points[b]) == ONE, "second reflection contact failed")
    return new_points, edges, routes


def proper(word, points, edges):
    need(type(word) is str and len(word) == len(points) and set(word) <= set("0123"), "bad colour word")
    need(all(word[a] != word[b] for a, b in edges), "monochromatic unit edge")


def propagate(edges, target_n, base_word):
    adj = [[] for _ in range(target_n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    domains = [15] * target_n
    for i, c in enumerate(base_word):
        domains[i] = 1 << int(c)
    trace = []
    forced = 0
    rounds = 0
    while True:
        rounds += 1
        changed = False
        for x in range(len(base_word), target_n):
            old = domains[x]
            singleton_sources = {}
            for y in adj[x]:
                d = domains[y]
                if d and d & (d - 1) == 0:
                    singleton_sources[d] = y
            forbidden = 0
            for d in singleton_sources:
                forbidden |= d
            new = old & ~forbidden
            if new == old:
                continue
            changed = True
            for c in range(4):
                bit = 1 << c
                if old & bit and not new & bit:
                    y = singleton_sources[bit]
                    need(y in adj[x] and domains[y] == bit, "unsound propagation reason")
                    trace.append((x, c, y))
            domains[x] = new
            if new and new & (new - 1) == 0 and old & (old - 1):
                forced += 1
            if new == 0:
                return {
                    "contradiction": True,
                    "rounds": rounds,
                    "colour_removals": len(trace),
                    "forced_vertices": forced,
                    "empty_vertex": x,
                    "trace_sha256": sha_rows(trace),
                }
        if not changed:
            return {
                "contradiction": False,
                "rounds": rounds,
                "colour_removals": len(trace),
                "forced_vertices": forced,
                "trace_sha256": sha_rows(trace),
            }


def graph_summary(points, edges, routes, next_n):
    degrees = [0] * len(points)
    for a, b in edges:
        degrees[a] += 1
        degrees[b] += 1
    return {
        "points": len(points),
        "unit_edges": len(edges),
        "unit_two_paths": len(routes),
        "next_points": next_n,
        "minimum_degree": min(degrees),
        "maximum_degree": max(degrees),
        "degree_histogram": {str(k): v for k, v in sorted(Counter(degrees).items())},
        "point_sha256": sha_rows([p[0] + p[1] for p in points]),
        "edge_sha256": sha_rows(edges),
        "route_sha256": sha_rows(routes),
    }


def moser_three_colour_count(source, s0, e0):
    m = [(tuple(x), tuple(y)) for x, y in source["M"]]
    indices = [s0.index(q) for q in m]
    edge_set = set(e0)
    medges = [(i, j) for i, j in combinations(range(7), 2)
              if tuple(sorted((indices[i], indices[j]))) in edge_set]
    need(len(medges) == 11, "source does not contain the strict Moser graph")
    return sum(all(w[a] != w[b] for a, b in medges) for w in product(range(3), repeat=7))


def audit(cert):
    need(cert["schema"] == "hn-moser-reflection-closure-gain-v1", "wrong schema")
    source_bytes = SOURCE.read_bytes()
    need(hashlib.sha256(source_bytes).hexdigest() == cert["source_certificate_sha256"], "source hash mismatch")
    source = json.loads(source_bytes)
    need(source["scale"] == cert["scale"] == 12, "wrong scale")
    need(source["basis"] == cert["basis"] == ["1", "sqrt3", "sqrt11", "sqrt33"], "wrong basis")
    s0 = [(tuple(x), tuple(y)) for x, y in source["C"]]
    need(len(s0) == len(set(s0)) == 25, "bad source support")
    s1, e0, r0 = close_once(s0)
    s2, e1, r1 = close_once(s1)
    s3, e2, r2 = close_once(s2)
    summaries = [
        graph_summary(s0, e0, r0, len(s1)),
        graph_summary(s1, e1, r1, len(s2)),
        graph_summary(s2, e2, r2, len(s3)),
    ]
    need(summaries == cert["rounds"], "round census/hash mismatch")
    need([len(s0), len(s1), len(s2), len(s3)] == [25, 115, 398, 1020], "unexpected closure sizes")
    need([len(e0), len(e1), len(e2)] == [53, 447, 2084], "unexpected edge counts")
    proper(cert["s0_nonextending_word"], s0, e0)
    proper(cert["s1_nonextending_word"], s1, e1)
    proper(cert["s2_four_word"], s2, e2)
    need(cert["s1_extending_word"] == cert["s2_four_word"][:len(s1)], "bad S1 positive restriction")
    need(cert["s0_extending_word"] == cert["s2_four_word"][:len(s0)], "bad S0 positive restriction")
    p01 = propagate(e1, len(s1), cert["s0_nonextending_word"])
    p12 = propagate(e2, len(s2), cert["s1_nonextending_word"])
    need(p01 == cert["s0_to_s1_propagation"] and p01["contradiction"], "S0 relation exclusion failed")
    need(p12 == cert["s1_to_s2_propagation"] and p12["contradiction"], "S1 relation exclusion failed")
    three = moser_three_colour_count(source, s0, e0)
    need(three == 0, "Moser subgraph unexpectedly three-colourable")
    need(cert["natural_next_round_points"] == len(s3) == 1020, "wrong cap stop")
    need(cert["record_candidate"] is False, "incorrect candidate status")
    need(cert["status"] == "EXACT_TWO_STRICT_RELATION_GAINS_CAP_STOPS_AT_CHI4", "wrong status")
    return {
        "round_points": [25, 115, 398],
        "round_edges": [53, 447, 2084],
        "next_round_points": 1020,
        "exact_pair_decisions": sum(len(s)*(len(s)-1)//2 for s in (s0, s1, s2)),
        "defining_contact_checks": 2 * (len(r0) + len(r1) + len(r2)),
        "moser_three_colourings": three,
        "s2_four_word_checked": True,
        "s0_to_s1_relation_strict": True,
        "s1_to_s2_relation_strict": True,
        "propagation_removals": [p01["colour_removals"], p12["colour_removals"]],
        "record_candidate": False,
        "status": "PASS",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    p.add_argument("--check-expected", action="store_true")
    p.add_argument("--controls", action="store_true")
    a = p.parse_args()
    cert = json.loads(a.certificate.read_text())
    result = audit(cert)
    if a.check_expected:
        need(result == json.loads((HERE / "EXPECTED.json").read_text()), "expected result mismatch")
    if a.controls:
        raw = a.certificate.read_text()
        for label in ("colour", "relation", "count"):
            bad = json.loads(raw)
            if label == "colour":
                w = list(bad["s2_four_word"]); w[0] = w[1]; bad["s2_four_word"] = "".join(w)
            elif label == "relation":
                bad["s0_nonextending_word"] = bad["s0_extending_word"]
            else:
                bad["rounds"][1]["unit_edges"] += 1
            try:
                audit(bad)
            except ValueError:
                pass
            else:
                raise ValueError("corrupted certificate accepted: " + label)
        result["corruptions_rejected"] = 3
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
