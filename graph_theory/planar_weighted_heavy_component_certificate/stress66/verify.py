#!/usr/bin/env python3
"""Check the 66-vertex stress certificate; Python standard library only."""
from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("common_checker", HERE.parent / "verify.py")
common = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(common)


def graph():
    """Two caps and an alternatingly triangulated 8-by-8 cylinder."""
    edges = set()

    def add(a, b):
        edges.add(tuple(sorted((a, b))))

    def at(i, j):
        return 2 + 8 * (i % 8) + j

    for i in range(8):
        meridian = [0] + [at(i, j) for j in range(8)] + [1]
        for a, b in zip(meridian, meridian[1:]):
            add(a, b)
        for j in range(8):
            add(at(i, j), at(i + 1, j))
        for j in range(7):
            if (i + j) % 2 == 0:
                add(at(i, j), at(i + 1, j + 1))
            else:
                add(at(i + 1, j), at(i, j + 1))
    adj = [set() for _ in range(66)]
    lengths = {}
    for a, b in sorted(edges):
        digest = sha256(f"0:{a}:{b}".encode("ascii")).digest()
        length = 1 + int.from_bytes(digest[:4], "big") % 19
        adj[a].add(b)
        adj[b].add(a)
        lengths[a, b] = lengths[b, a] = length
    return adj, lengths


def audit(certificate, adj, lengths, dist):
    return common.check_certificate(certificate, adj, lengths, dist,
                                    graph_name="capped-cylinder-8-by-8", metric_seed=0)


def compatible_choices(cuts, adj):
    """Enumerate compatible component choices, without a forcing rule."""
    states = [()]
    counts = []
    for cut in cuts:
        removed = set().union(*(set(p) for p in cut["paths"]))
        parts = common.components(adj, removed)
        states = [state + (c,) for state in states for c in parts
                  if all(c & previous for previous in state)]
        counts.append(len(states))
    return counts


def main():
    raw = (HERE / "certificate.json").read_bytes()
    certificate = json.loads(raw)
    adj, lengths = graph()
    dist = common.distances(adj, lengths)
    trace, path_count = audit(certificate, adj, lengths, dist)
    longest = common.longest_geodesic(adj, lengths, dist)
    assert 4 * len(longest) < len(adj)
    counts = compatible_choices(certificate["cuts"], adj)
    assert counts[-1] == 0
    rejected = 0

    def reject(fn):
        nonlocal rejected
        try:
            fn()
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("invalid control accepted")

    missing = deepcopy(certificate)
    missing["cuts"].pop()
    reject(lambda: audit(missing, adj, lengths, dist))
    wrong_metric = deepcopy(certificate)
    wrong_metric["metric_seed"] = 1
    reject(lambda: audit(wrong_metric, adj, lengths, dist))
    reject(lambda: common.check_path([0, 25], adj, lengths, dist))
    reject(lambda: common.check_path([0, 2, 0], adj, lengths, dist))
    nonshortest = next([a, b, c] for a in range(len(adj)) for b in sorted(adj[a])
                       for c in sorted(adj[b]) if a != c and
                       lengths[a, b] + lengths[b, c] > dist[a][c])
    reject(lambda: common.check_path(nonshortest, adj, lengths, dist))
    summary = {"status": "PASS", "vertices": len(adj), "edges": len(lengths) // 2,
               "edge_length_min": min(lengths.values()), "edge_length_max": max(lengths.values()),
               "certificate_cuts": len(certificate["cuts"]), "distinct_certificate_paths": path_count,
               "forcing_steps": len(trace) - 1, "longest_geodesic_vertices": len(longest),
               "longest_geodesic_witness": list(longest), "four_path_cover_capacity_bound": 4 * len(longest),
               "trace": trace, "compatible_prefix_counts": counts, "rejected_controls": rejected,
               "certificate_sha256": sha256(raw).hexdigest(),
               "distance_matrix_sha256": sha256(json.dumps(dist, separators=(",", ":")).encode()).hexdigest()}
    if sys.argv[1:] == ["--check"]:
        if summary != json.loads((HERE / "expected.json").read_text()):
            raise AssertionError("result differs from expected.json")
    elif sys.argv[1:]:
        raise SystemExit("usage: verify.py [--check]")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
