#!/usr/bin/env python3
"""Exact finite audit of PROOF.md; no simulation or asymptotic oracle.

Python 3.10+, standard library only. All checks survive python -O.
Graphs use vertices range(n), with lexicographically ordered unordered
edges. Exhaustion is over every edge bit mask, not an isomorphism sample.
"""

from collections import deque
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from math import comb
from pathlib import Path
import argparse
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def graph(n, edges):
    require(isinstance(n, int) and n >= 2, "order must be an integer >=2")
    adj = [set() for _ in range(n)]
    seen = set()
    for u, v in edges:
        require(isinstance(u, int) and isinstance(v, int), "integer labels required")
        require(0 <= u < n and 0 <= v < n and u != v, "invalid edge")
        e = tuple(sorted((u, v)))
        require(e not in seen, "duplicate edge")
        seen.add(e)
        adj[u].add(v)
        adj[v].add(u)
    return adj


def complement(adj):
    vertices = set(range(len(adj)))
    return [vertices - {v} - neighbors for v, neighbors in enumerate(adj)]


def response_bad_vertices(adj):
    """Definition-level all-pairs BFS, independent of common-neighbor tests."""
    n = len(adj)
    distances = []
    for start in range(n):
        dist = [-1] * n
        dist[start] = 0
        queue = deque([start])
        while queue:
            v = queue.popleft()
            for w in adj[v]:
                if dist[w] < 0:
                    dist[w] = dist[v] + 1
                    queue.append(w)
        if -1 in dist:
            return False, set(range(n)), None
        distances.append(dist)
    bad = set()
    for v in range(n):
        seen = set()
        for x in range(n):
            if v == x:
                response = frozenset([v])
            else:
                response = frozenset(w for w in adj[v]
                                     if distances[w][x] == distances[v][x] - 1)
            if response in seen:
                bad.add(v)
            seen.add(response)
    return True, bad, max(map(max, distances))


def defects(adj):
    """Direct finite-set definitions of Z, X, T, Y, including witnesses."""
    n = len(adj)
    non = complement(adj)
    zero, single = set(), set()
    for u, v in combinations(range(n), 2):
        if v not in adj[u]:
            common = adj[u] & adj[v]
            if len(common) == 0:
                zero.add((u, v))
            if len(common) == 1:
                single.add((u, v))
    traces, cherries = set(), set()
    for v in range(n):
        for x, y in combinations(sorted(non[v]), 2):
            if adj[v] & adj[x] == adj[v] & adj[y]:
                traces.add((v, x, y))
            if non[x] == {v} and non[y] == {v}:
                cherries.add((v, x, y))
    return zero, single, traces, cherries


def check_reduction(adj):
    connected, bad, diameter = response_bad_vertices(adj)
    z, x, t, y = defects(adj)
    u = connected and not bad
    require(y <= t, "complement cherry is not a trace collision")
    require(not x or not u, "singleton pair failed to obstruct U")
    require(not y or not u, "complement cherry failed to obstruct U")
    if not z:
        require(connected and diameter <= 2, "zero-free graph must have diameter <=2")
        predicted = {v for pair in x for v in pair} | {s[0] for s in t}
        require(bad == predicted, "response-level bad vertices disagree with defects")
    if not (z or x or t):
        require(u, "sufficient certificate failed")
    return connected, bad, diameter, (z, x, t, y)


def falling(n, r):
    result = 1
    for i in range(r):
        result *= n - i
    return result if n >= r else 0


def exact_means(n, p):
    require(n >= 3 and F(0) <= p <= F(1), "invalid moment parameters")
    q = 1 - p
    b, a = 1 - p*p, 1 - 2*p*p*q
    return {
        "Z": comb(n, 2)*q*b**(n-2),
        "X": comb(n, 2)*q*(n-2)*p*p*b**(n-3),
        "T": n*comb(n-1, 2)*q*q*a**(n-3),
        "Y": n*comb(n-1, 2)*q*q*p**(2*n-5),
    }


def exact_pair_probabilities(n, p):
    require(n >= 5 and 0 < p < 1, "interior probability and order >=5 required")
    q = 1 - p
    h = 1 - 2*p*p + p**3
    overlap = q*q*((n-3)*p**3*h**(n-4)
                     + (n-3)*(n-4)*p**4*q*q*h**(n-5))
    b0 = (1-p*p)**(n-4)
    b1 = (n-4)*p*p*(1-p*p)**(n-5)
    disjoint = q*q*((q**4+4*p*q**3+2*p*p*q*q)*b1*b1
                       + 4*p*p*q*q*b0*b1 + 4*p**3*q*b0*b0)
    x2 = falling(n, 3)*overlap + F(falling(n, 4), 4)*disjoint
    y2 = (F(falling(n, 6)+falling(n, 5), 4)*q**4*p**(4*n-14)
          + falling(n, 4)*q**3*p**(3*n-9))
    return {"adjacent_X": overlap, "disjoint_X": disjoint, "X2": x2, "Y2": y2}


def expectation(hist, n, p):
    m = comb(n, 2)
    return sum((count*p**e*(1-p)**(m-e)
                for e, count in enumerate(hist)), F(0))


def finite_exhaustion():
    records = []
    counts = {"graphs": 0, "connected_graphs": 0, "diameter_two_graphs": 0,
              "probe_checks": 0, "weighted_first_moments": 0,
              "weighted_second_and_joint_moments": 0}
    histograms = {}
    names = ("U", "Z", "X", "T", "Y", "X2", "Y2", "adjacent_X", "disjoint_X")
    for n in range(2, 7):
        edges = list(combinations(range(n), 2))
        hist = {name: [0]*(len(edges)+1) for name in names}
        for mask in range(1 << len(edges)):
            adj = graph(n, (e for i, e in enumerate(edges) if mask >> i & 1))
            connected, bad, diameter, (z, x, t, y) = check_reduction(adj)
            counts["graphs"] += 1
            counts["connected_graphs"] += int(connected)
            counts["diameter_two_graphs"] += int(connected and diameter <= 2)
            counts["probe_checks"] += n if connected else 0
            e = mask.bit_count()
            values = {"U": int(connected and not bad), "Z": len(z), "X": len(x),
                      "T": len(t), "Y": len(y), "X2": len(x)*(len(x)-1),
                      "Y2": len(y)*(len(y)-1),
                      "adjacent_X": int((0, 1) in x and (0, 2) in x),
                      "disjoint_X": int((0, 1) in x and (2, 3) in x)}
            for name, value in values.items():
                hist[name][e] += value
        histograms[n] = hist
        records.append({"n": n, "histograms": hist})
        for p in (F(1, 5), F(1, 3), F(1, 2), F(2, 3), F(9, 10)):
            if n >= 3:
                for name, claimed in exact_means(n, p).items():
                    actual = expectation(hist[name], n, p)
                    require(actual == claimed, f"first moment mismatch: {n,p,name}")
                    counts["weighted_first_moments"] += 1
            if n >= 5:
                for name, claimed in exact_pair_probabilities(n, p).items():
                    actual = expectation(hist[name], n, p)
                    require(actual == claimed, f"joint moment mismatch: {n,p,name}")
                    counts["weighted_second_and_joint_moments"] += 1
    return records, counts, histograms


def cross_edge_audit():
    """All four cross-edge patterns underlying equation (9)."""
    tally = {}
    cross = [(0, 2), (0, 3), (1, 2), (1, 3)]
    for mask in range(16):
        adj = graph(4, (e for i, e in enumerate(cross) if mask >> i & 1))
        key = (mask.bit_count(), len(adj[0] & adj[1]), len(adj[2] & adj[3]))
        tally[key] = tally.get(key, 0) + 1
    expected = {(0, 0, 0): 1, (1, 0, 0): 4, (2, 0, 0): 2,
                (2, 1, 0): 2, (2, 0, 1): 2, (3, 1, 1): 4, (4, 2, 2): 1}
    require(tally == expected, "cross-edge pattern error")
    return [[*k, v] for k, v in sorted(tally.items())]


def leaf_constraint_audit():
    """Count explicit forbidden edges, independently of formula (19)."""
    records = []
    for n in range(3, 15):
        for ell in range(2, n):
            for centers in range(1, min(ell//2, n-ell)+1):
                leaves = set(range(ell))
                # Each center gets >=2 leaves; remaining leaves go to the last.
                parent = {v: ell + min(v//2, centers-1) for v in leaves}
                required = {tuple(sorted((v, parent[v]))) for v in leaves}
                forbidden = {e for e in combinations(range(n), 2)
                             if set(e) & leaves and e not in required}
                require(len(required) == ell, "required leaf-edge count")
                require(len(forbidden) == ell*n-ell*(ell+3)//2,
                        "forbidden leaf-edge exponent")
                records.append([n, centers, ell, len(required), len(forbidden)])
    return records


def fixtures():
    cases = []
    cube = graph(8, ((u, v) for u, v in combinations(range(8), 2)
                     if (u ^ v).bit_count() == 1))
    cases.append(("cube3", cube, True, 0, 3))
    for name, missing, universal, bad_count in (
        ("complete", [], True, 0),
        ("complement_matching", [(0, 1), (2, 3), (4, 5), (6, 7)], True, 0),
        ("complement_cherry", [(0, 1), (0, 2)], False, 1),
        ("complement_three_leaf_star", [(0, 1), (0, 2), (0, 3)], False, 1),
        ("complement_two_cherries", [(0, 1), (0, 2), (3, 4), (3, 5)], False, 2),
        ("complement_triangle", [(0, 1), (0, 2), (1, 2)], False, 3),
    ):
        h = graph(8, missing)
        cases.append((name, complement(h), universal, bad_count, 1 if not missing else 2))
    records = []
    for name, adj, expected_u, expected_bad, expected_diameter in cases:
        connected, bad, diameter, (z, x, t, y) = check_reduction(adj)
        require((connected and not bad) == expected_u, name + " U")
        require(len(bad) == expected_bad and diameter == expected_diameter,
                name + " bad-count or diameter")
        records.append({"name": name, "bad_vertices": sorted(bad), "diameter": diameter,
                        "Z": len(z), "X": len(x), "T": len(t), "Y": len(y)})
    require(records[0]["Z"] > 0, "cube must expose the diameter-two boundary")
    require(records[-1]["Y"] == 0 and records[-1]["T"] > 0,
            "triangle must expose non-cherry trace collisions")
    return records


def rejection_checks(histograms):
    count = 0
    for call in (
        lambda: graph(3, [(0, 0)]),
        lambda: graph(3, [(0, 3)]),
        lambda: graph(3, [(0, 1), (1, 0)]),
        lambda: graph(1, []),
        lambda: exact_means(5, F(4, 3)),
        lambda: exact_pair_probabilities(4, F(1, 2)),
    ):
        try:
            call()
        except ValueError:
            count += 1
        else:
            raise ValueError("invalid input was accepted")
    # Corrupt an entry, not just an aggregate checksum: the exact weighted
    # moment must reject this change independently of the expected JSON.
    corrupt = list(histograms[6]["Y2"])
    corrupt[2] += 1
    try:
        require(expectation(corrupt, 6, F(1, 3)) ==
                exact_pair_probabilities(6, F(1, 3))["Y2"], "corrupted moment")
    except ValueError:
        count += 1
    else:
        raise ValueError("corrupted histogram was accepted")
    return count


def run():
    records, counts, histograms = finite_exhaustion()
    cross = cross_edge_audit()
    leaves = leaf_constraint_audit()
    examples = fixtures()
    rejected = rejection_checks(histograms)
    payload = {"exhaustion": records, "cross_edges": cross,
               "leaf_constraints": leaves, "fixtures": examples}
    digest = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"status": "VERIFIED", **counts, "cross_edge_patterns": 16,
            "leaf_constraint_checks": len(leaves), "fixtures": examples,
            "rejection_checks": rejected,
            "universal_graphs_by_order": {str(n): sum(h["U"]) for n, h in histograms.items()},
            "record_sha256": digest}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare all output fields with EXPECTED.json")
    args = parser.parse_args()
    result = run()
    if args.check:
        expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
        require(result == expected, "audit differs from EXPECTED.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
