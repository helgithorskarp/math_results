#!/usr/bin/env python3
"""Exact checker for the five-terminal S1-on-S1 host activation gate."""
from argparse import ArgumentParser
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_moser_all_terminal_contacts" / "certificate.json"
ONE = (144, 0, 0, 0)
TARGET = (0, 10, 11, 17, 18)
EXCLUDED = "00112"
COMMON = "00001"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(a, b):
    out = [0] * 4
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            common = i & j
            factor = (3 if common & 1 else 1) * (11 if common & 2 else 1)
            out[i ^ j] += factor * x * y
    return tuple(out)


def norm2(p, q):
    dx, dy = sub(p[0], q[0]), sub(p[1], q[1])
    return add(mul(dx, dx), mul(dy, dy))


def edges(points):
    return [(a, b) for a, b in combinations(range(len(points)), 2)
            if norm2(points[a], points[b]) == ONE]


def close_once(points):
    old_edges = edges(points)
    adj = [[] for _ in points]
    for a, b in old_edges:
        adj[a].append(b)
        adj[b].append(a)
    out = list(points)
    seen = {p: i for i, p in enumerate(out)}
    for centre, ns in enumerate(adj):
        for a, b in combinations(ns, 2):
            q = (sub(add(points[a][0], points[b][0]), points[centre][0]),
                 sub(add(points[a][1], points[b][1]), points[centre][1]))
            need(norm2(q, points[a]) == ONE and norm2(q, points[b]) == ONE,
                 "reflection contact")
            if q not in seen:
                seen[q] = len(out)
                out.append(q)
    return out, old_edges


def row_hash(rows):
    blob = "".join(",".join(map(str, row)) + "\n" for row in rows).encode()
    return sha256(blob).hexdigest()


def build():
    raw = SOURCE.read_bytes()
    source = json.loads(raw)
    need(source["scale"] == 12, "source scale")
    need(source["basis"] == ["1", "sqrt3", "sqrt11", "sqrt33"], "source basis")
    s0 = [(tuple(x), tuple(y)) for x, y in source["C"]]
    need(len(s0) == len(set(s0)) == 25, "source support")
    s1, e0 = close_once(s0)
    _, e1 = close_once(s1)
    need(len(s1) == 115 and len(e1) == 447, "S1 census")
    return raw, s0, s1, e0, e1


def cross(a, b, c):
    abx, aby = sub(b[0], a[0]), sub(b[1], a[1])
    acx, acy = sub(c[0], a[0]), sub(c[1], a[1])
    return sub(mul(abx, acy), mul(aby, acx))


def embeddings(target_points, target_ids, host):
    matrix = [[norm2(target_points[a], target_points[b]) for b in target_ids]
              for a in target_ids]
    out = []

    def extend(prefix):
        k = len(prefix)
        if k == len(target_ids):
            out.append(tuple(prefix))
            return
        for v in range(len(host)):
            if v in prefix:
                continue
            if all(norm2(host[v], host[prefix[j]]) == matrix[k][j]
                   for j in range(k)):
                extend(prefix + [v])

    extend([])
    return out


def word(text, n):
    need(isinstance(text, str) and len(text) == n and set(text) <= set("0123"),
         "colour word")
    return tuple(map(int, text))


def proper(colours, graph_edges):
    return all(colours[a] != colours[b] for a, b in graph_edges)


def audit(cert):
    source_raw, s0, s1, e0, e1 = build()
    need(cert["schema"] == "hn-moser-reflection-s1-host-gate-v1", "schema")
    need(cert["source_sha256"] == sha256(source_raw).hexdigest(), "source hash")
    need(cert["target_terminals"] == list(TARGET), "target terminals")
    need(cert["excluded_pattern"] == EXCLUDED and cert["common_pattern"] == COMMON,
         "terminal patterns")
    need(cross(s0[TARGET[0]], s0[TARGET[1]], s0[TARGET[2]]) != (0, 0, 0, 0),
         "target anchors are collinear")

    found = embeddings(s0, TARGET, s1)
    need(len(found) == 70, "embedding count")
    entries = cert["host_witnesses"]
    need(len(entries) == len(found), "host witness count")
    blocker = word(cert["blocker_word"], len(s1))
    need(proper(blocker, e1), "blocker common-pattern word")
    need("".join(map(str, (blocker[v] for v in TARGET))) == COMMON,
         "blocker terminal pattern")

    for entry, expected in zip(entries, found):
        need(entry["embedding"] == list(expected), "embedding order")
        colours = word(entry["word"], len(s1))
        need(proper(colours, e1), "host common-pattern word")
        need("".join(map(str, (colours[v] for v in expected))) == COMMON,
             "host terminal pattern")

    edge_set = set(e1)
    need(all(tuple(sorted((29, v))) in edge_set for v in (0, 11, 18)),
         "first blocker contacts")
    need(all(tuple(sorted((93, v))) in edge_set for v in (10, 17, 18, 29)),
         "second blocker contacts")
    excluded_at = {v: EXCLUDED[i] for i, v in enumerate(TARGET)}
    need(all(excluded_at[a] != excluded_at[b] for a, b in e0
             if a in excluded_at and b in excluded_at),
         "excluded pattern not admissible on target")
    first = {int(EXCLUDED[TARGET.index(v)]) for v in (0, 11, 18)}
    second = {int(EXCLUDED[TARGET.index(v)]) for v in (10, 17, 18)}
    need(first == second == {0, 1, 2}, "excluded pattern forcing colours")

    result = {
        "source_points": len(s0),
        "host_points": len(s1),
        "host_edges": len(e1),
        "target_terminals": list(TARGET),
        "target_anchors_noncollinear": True,
        "excluded_pattern": EXCLUDED,
        "blocker_forced_vertex": 29,
        "blocker_empty_vertex": 93,
        "labeled_metric_embeddings": len(found),
        "maximum_two_copy_points_after_five_identifications": 225,
        "common_surviving_pattern": COMMON,
        "host_witnesses_checked": len(entries),
        "s1_point_sha256": row_hash([p[0] + p[1] for p in s1]),
        "s1_edge_sha256": row_hash(e1),
        "record_candidate": False,
        "status": "EXACT_S1_HOST_GATE_SURVIVING_RELATION",
    }
    need(result == json.loads((HERE / "EXPECTED.json").read_text()), "EXPECTED mismatch")
    return result


def controls(cert):
    tests = []
    for kind in ("embedding", "host_colour", "blocker_colour"):
        bad = deepcopy(cert)
        if kind == "embedding":
            bad["host_witnesses"][0]["embedding"][0] = 114
        elif kind == "host_colour":
            a, b = (0, 2)
            w = list(bad["host_witnesses"][0]["word"])
            w[b] = w[a]
            bad["host_witnesses"][0]["word"] = "".join(w)
        else:
            a, b = (0, 2)
            w = list(bad["blocker_word"])
            w[b] = w[a]
            bad["blocker_word"] = "".join(w)
        try:
            audit(bad)
        except ValueError:
            tests.append(kind)
        else:
            raise ValueError("corruption accepted: " + kind)
    return tests


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--controls", action="store_true")
    args = parser.parse_args()
    certificate = json.loads((HERE / "certificate.json").read_text())
    output = audit(certificate)
    if args.controls:
        output["corruptions_rejected"] = controls(certificate)
    print(json.dumps(output, indent=2, sort_keys=True))
