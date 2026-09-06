#!/usr/bin/env python3
"""A concrete non-subsumption check against the teammate's fixed 41-core family."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from physical import catalog, decode, require, CATALOG_SHA

CORE186_SHA = "996d8040696d0aaf4e9faf92eb24cd17ff54248eecebb699fa87d8c764b8f68a"


def invariant(graph, vertices):
    counts = {edge: 0 for edge in combinations(vertices, 2)}
    for u, v, w in combinations(vertices, 3):
        if graph[u][v] ^ graph[u][w] ^ graph[v][w]:
            counts[u, v] += 1
            counts[u, w] += 1
            counts[v, w] += 1
    return dict(sorted(Counter(counts.values()).items()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core186", type=Path, default=Path(__file__).resolve().parent.parent/
                        "ramsey_r55_core186_switch_family/core.edges")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    raw = args.core186.read_bytes()
    require(sha256(raw).hexdigest() == CORE186_SHA, "Wrong teammate physical core")
    lines = raw.decode().splitlines()
    require(lines[0] == "41", "Wrong core order")
    core = [[0]*41 for _ in range(41)]
    for line in lines[1:]:
        u, v = map(int, line.split())
        require(0 <= u < v < 41 and not core[u][v], "Bad edge input")
        core[u][v] = core[v][u] = 1
    target = invariant(core, range(41))
    opposite = dict(sorted((39-key, value) for key, value in target.items()))
    complemented = [[int(u != v) ^ core[u][v] for v in range(41)] for u in range(41)]
    require(invariant(complemented, range(41)) == opposite, "Complement invariant mismatch")
    # Explicit member of our whole 43-family: unswitched parent0 plus isolated42.
    record = catalog(Path(__file__).with_name("r55_42some.g6"))[0]
    graph = [row+[0] for row in decode(record)] + [[0]*43]
    full = {}
    for u, v in combinations(range(43), 2):
        full[u, v] = sum(graph[u][v] ^ graph[u][w] ^ graph[v][w]
                         for w in range(43) if w not in (u, v))
    mismatches, direct_controls = 0, 0
    for a, b in combinations(range(43), 2):
        vertices = [v for v in range(43) if v not in (a, b)]
        counts = Counter(full[u, v] - (graph[u][v] ^ graph[u][a] ^ graph[v][a])
                         - (graph[u][v] ^ graph[u][b] ^ graph[v][b])
                         for u, v in combinations(vertices, 2))
        histogram = dict(sorted(counts.items()))
        require(sum(histogram.values()) == 820 and all(0 <= x <= 39 for x in histogram), "Invariant range")
        require(histogram == invariant(graph, vertices), "Independent triple reconstruction mismatch")
        direct_controls += 1
        require(histogram not in (target, opposite), "Invariant inconclusive; do not claim non-subsumption")
        mismatches += 1
    require(mismatches == 903, "Incomplete induced-core coverage")
    # This witness is deliberately not a target: exhibit a literal blue K5.
    obstruction = next(q for q in combinations(range(43), 5)
                       if all(graph[u][v] == 0 for u, v in combinations(q, 2)))
    report = {"status": "CATALOG_FAMILY_NOT_SUBSUMED_BY_FIXED_CORE186_FAMILY",
              "catalog_sha256": CATALOG_SHA, "teammate_core_sha256": CORE186_SHA,
              "witness": {"parent": 0, "all_switch_bits": 0, "all_new_edge_bits": 0, "vertices": 43,
                          "blue_K5": list(obstruction)},
              "induced_41_subsets": mismatches, "matching_parity_histograms": 0,
              "teammate_complement_also_tested": True,
              "direct_triangle_controls": direct_controls,
              "teammate_parity_histogram": target,
              "claim_of_disjoint_full_families": False,
              "uses_teammate_exclusion_as_premise": False}
    text = json.dumps(report, indent=2)+"\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
