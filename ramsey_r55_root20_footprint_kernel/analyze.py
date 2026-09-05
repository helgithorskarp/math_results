#!/usr/bin/env python3
"""Exact subset recurrence; no solver is used for any published conclusion."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
GRAPH_SHA = "8d404855787227dc182d7bdc0e98751474ce6c9f1cf872abc52888477c096ccf"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def decode(doc):
    require(set(doc) == {"n", "red_edges"}, "graph fields")
    n = doc["n"]
    require(type(n) is int and 1 <= n <= 20, "graph order")
    require(type(doc["red_edges"]) is list, "edge list")
    red, seen = [0] * n, set()
    for e in doc["red_edges"]:
        require(type(e) is list and len(e) == 2 and all(type(v) is int for v in e), "edge schema")
        u, v = e
        require(0 <= u < v < n and (u, v) not in seen, "edge bounds or duplicate")
        seen.add((u, v))
        red[u] |= 1 << v
        red[v] |= 1 << u
    return red


def cliques(red, color, k):
    return [sum(1 << v for v in q) for q in combinations(range(len(red)), k)
            if all(bool(red[u] >> v & 1) == color for u, v in combinations(q, 2))]


def pair_colors(red, first, second):
    """Allowed outside pair colors, assuming each one-vertex footprint is valid."""
    full = (1 << len(red)) - 1
    require(type(first) is int and type(second) is int and 0 <= first <= full and 0 <= second <= full,
            "footprint bounds")
    common = {True: first & second, False: full ^ (first | second)}
    return [c for c in (False, True) if not any(common[c] & t == t for t in cliques(red, c, 3))]


def calculate(red):
    n, full = len(red), (1 << len(red)) - 1
    require(n == 20, "this census is for H20")
    require(not cliques(red, True, 4) and not cliques(red, False, 5), "input is not Ramsey(4,5)")
    blue = [full ^ row ^ (1 << v) for v, row in enumerate(red)]
    edges, rt, bt, b4 = (bytearray(1 << n) for _ in range(4))
    for mask in range(1, 1 << n):
        bit = mask & -mask
        v, rest = bit.bit_length() - 1, mask ^ bit
        r, b = rest & red[v], rest & blue[v]
        edges[mask] = edges[rest] + r.bit_count()
        rt[mask] = bool(rt[rest] or edges[r])
        size = b.bit_count()
        bt[mask] = bool(bt[rest] or edges[b] < size * (size - 1) // 2)
        b4[mask] = bool(b4[rest] or bt[b])
    extension = [s for s in range(1 << n) if not rt[s] and not b4[full ^ s]]
    domains = {t: [s for s in range(t, 1 << n, 4) if not b4[full ^ s]] for t in (1, 2, 3)}
    minimal = {t: [s for s in ds if all(b4[full ^ (s ^ (1 << i))]
                    for i in range(2, n) if s >> i & 1)] for t, ds in domains.items()}
    report = {"graph_sha256": GRAPH_SHA, "n": n, "red_edges": sum(x.bit_count() for x in red)//2,
              "red_triangles": len(cliques(red, True, 3)), "blue_triangles": len(cliques(red, False, 3)),
              "blue_four_cliques": len(cliques(red, False, 4)), "subsets_checked": 1 << n,
              "ramsey45_extension_masks": extension, "domain_sizes": {str(t):len(ds) for t,ds in domains.items()},
              "minimal_domain_sizes": {str(t):len(ds) for t,ds in minimal.items()},
              "domain_size_histograms": {str(t):dict(sorted(Counter(s.bit_count() for s in ds).items())) for t,ds in domains.items()},
              "identical_footprint_blue_allowed": {str(t):sum(not bt[full ^ s] for s in ds) for t,ds in domains.items()},
              "identical_footprint_red_allowed": {str(t):sum(not rt[s] for s in ds) for t,ds in domains.items()},
              "claim": "H20 has no Ramsey(4,5;21) vertex extension; exact one/two-outside-vertex interface only",
              "full_43_extension_decided": False}
    return report, domains, minimal


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=False)
    data = (HERE / "GRAPH.json").read_bytes()
    require(hashlib.sha256(data).hexdigest() == GRAPH_SHA, "graph identity")
    report, domains, minimum = calculate(decode(json.loads(data)))
    for name, family in (("domains.txt", domains), ("minimal.txt", minimum)):
        text = "".join(f"{t} {s:05x}\n" for t, masks in family.items() for s in masks)
        (args.work / name).write_text(text)
        report[name + "_sha256"] = hashlib.sha256(text.encode()).hexdigest()
    (args.work / "analysis.json").write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
