#!/usr/bin/env python3
"""Exact finite corroboration; the universal homotopy proof is in PROOF.md.

CPython 3.11+, standard library. No floating point, randomness or datasets.
Vertices are integers 0,...,n-1; graph edges are sorted endpoint pairs.
A simplex is an integer bit mask of its vertices. Labelled graphs are
enumerated in lexicographic edge order; no isomorphism filtering is used.
"""

import argparse
from collections import Counter
from itertools import combinations
import json
from math import comb
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def graph(n, edges):
    edges = tuple(sorted(tuple(sorted(e)) for e in edges))
    require(n >= 0 and len(set(edges)) == len(edges), "bad graph or duplicate edge")
    require(all(len(e) == 2 and 0 <= e[0] < e[1] < n for e in edges),
            "not a simple graph on the specified vertices")
    return n, edges


def degrees(g):
    d = [0] * g[0]
    for u, v in g[1]:
        d[u] += 1
        d[v] += 1
    return d


def connected(g):
    if not g[0]:
        return False
    seen = {0}
    while True:
        expanded = seen | {v for e in g[1] if seen.intersection(e) for v in e}
        if expanded == seen:
            return len(seen) == g[0]
        seen = expanded


def line(g):
    edges = g[1]
    return graph(len(edges), [(i, j) for i, j in combinations(range(len(edges)), 2)
                             if set(edges[i]).intersection(edges[j])])


def sigma(g):
    return sum(comb(d - 1, 3) for d in degrees(g) if d >= 4)


def cliques(g, max_size=None):
    """Enumerate faces directly from pairwise adjacency, not star structure."""
    adj = [0] * g[0]
    for u, v in g[1]:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    result = set()

    def visit(face, candidates):
        while candidates:
            bit = candidates & -candidates
            candidates ^= bit
            new = face | bit
            result.add(new)
            if max_size is None or new.bit_count() < max_size:
                visit(new, candidates & adj[bit.bit_length() - 1])

    visit(0, (1 << g[0]) - 1)
    return result


def facets(face):
    bits = face
    while bits:
        bit = bits & -bits
        bits ^= bit
        yield face ^ bit


def gf2_rank(columns):
    pivots = {}
    for col in columns:
        while col:
            pivot = col.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = col
                break
            col ^= pivots[pivot]
    return len(pivots)


def betti012(faces):
    # Four-vertex faces are essential: they contribute to im(d_3).
    levels = {k: sorted(f for f in faces if f.bit_count() == k) for k in range(1, 5)}
    ranks = {0: 0}
    for dim in range(1, 4):
        index = {f: j for j, f in enumerate(levels[dim])}
        columns = []
        for f in levels[dim + 1]:
            columns.append(sum(1 << index[b] for b in facets(f)))
        ranks[dim] = gf2_rank(columns)
    return [len(levels[d + 1]) - ranks[d] - ranks[d + 1] for d in range(3)]


def remove_free_pair(faces, lower, upper):
    require(lower in faces and upper in faces, "missing collapse face")
    require(upper.bit_count() == lower.bit_count() + 1 and lower & upper == lower,
            "not a codimension-one pair")
    cofaces = {f for f in faces if f != lower and f & lower == lower}
    require(cofaces == {upper}, "collapse face is not free in the full complex")
    faces.remove(lower)
    faces.remove(upper)


def collapse_certificate(g):
    require(connected(g) and len(g[1]) >= 2, "recurrence domain requires two edges")
    original = cliques(line(g))
    current = original.copy()
    pairs = []
    omitted = {}
    for v in range(g[0]):
        star = [i for i, e in enumerate(g[1]) if v in e]
        apex, rest = star[0], star[1:]
        for size in range(len(rest), 2, -1):
            for vertices in combinations(rest, size):
                lower = sum(1 << i for i in vertices)
                upper = lower | (1 << apex)
                remove_free_pair(current, lower, upper)
                pairs.append((lower, upper))
        for triple in combinations(rest, 3):
            mask = sum(1 << i for i in triple)
            require(mask not in omitted, "duplicate omitted triangle")
            omitted[mask] = apex
    require(all(f.bit_count() <= 3 for f in current), "collapse not two dimensional")
    require({f for f in original if f.bit_count() <= 2} <= current,
            "collapse changed the one-skeleton")
    skeleton = {f for f in original if f.bit_count() <= 3}
    require(skeleton - current == set(omitted), "wrong omitted faces")
    require(len(omitted) == sigma(g), "wrong sphere count")
    for triangle, apex in omitted.items():
        require(not triangle & (1 << apex), "cone apex lies on boundary")
        disk = {e | (1 << apex) for e in facets(triangle)}
        require(len(disk) == 3 and disk <= current, "missing cone disk")
        boundary = Counter(e for face in disk for e in facets(face))
        require({e for e, count in boundary.items() if count % 2} == set(facets(triangle)),
                "cone disk has wrong boundary")
    require(betti012(current) == betti012(original), "collapse changed homology")
    return len(pairs), len(omitted)


def exceptional(g):
    d = degrees(g)
    return max(d, default=0) <= 2 or sorted(d) == [1, 1, 1, 3]


def degree_hitting_time(g):
    require(not exceptional(g), "degree growth requested for an exception")
    for j in range(4):
        if max(degrees(g), default=0) >= 4:
            return j
        g = line(g)
    raise ValueError("degree-four vertex not found by third iteration")


def expect_rejection(action):
    try:
        action()
    except ValueError:
        return
    raise ValueError("negative control was incorrectly accepted")


def run():
    counts, hitting = Counter(), Counter()
    pairs = disks = comparisons = 0
    for n in range(1, 6):
        potential = list(combinations(range(n), 2))
        for bits in range(1 << len(potential)):
            g = graph(n, [e for j, e in enumerate(potential) if bits & (1 << j)])
            if not connected(g):
                continue
            counts[n] += 1
            if not exceptional(g):
                hitting[degree_hitting_time(g)] += 1
            if len(g[1]) < 2:
                continue
            a, b = collapse_certificate(g)
            pairs += a
            disks += b
            first = line(g)
            beta = betti012(cliques(first, 4))
            second_beta = betti012(cliques(line(first), 4))
            require(second_beta == [beta[0], beta[1], beta[2] + sigma(g)],
                    "second-iterate homology disagrees with splitting")
            base_beta = betti012(cliques(g, 3))
            require(beta == base_beta, "known one-step theorem control failed")
            comparisons += 1

    high_degree = {}
    fixtures = {
        "six_leaf_star": graph(7, [(0, v) for v in range(1, 7)]),
        "K6": graph(6, combinations(range(6), 2)),
        "K2_5": graph(7, [(u, v) for u in range(2) for v in range(2, 7)]),
        "six_rim_wheel": graph(7, [(0, v) for v in range(1, 7)]
                              + [(v, v + 1) for v in range(1, 6)] + [(1, 6)]),
    }
    for name, g in fixtures.items():
        a, b = collapse_certificate(g)
        beta = betti012(cliques(line(g), 4))
        second_beta = betti012(cliques(line(line(g)), 4))
        require(second_beta == [beta[0], beta[1], beta[2] + sigma(g)],
                "high-degree homology control failed")
        high_degree[name] = {"collapse_pairs": a, "cone_disks": b,
                             "first_betti012": beta, "second_betti012": second_beta}

    # Explicit sharpness fixture, with no dependence on a graph-isomorphism package.
    sharp = graph(5, [(0, 1), (0, 2), (0, 3), (3, 4)])
    initial = sharp
    degree_profiles, sharp_betti = [], []
    for r in range(6):
        if r <= 3:
            degree_profiles.append(sorted(degrees(sharp), reverse=True))
        if r:
            beta = betti012(cliques(sharp, 4))
            require(beta == [1, 0, int(r == 5)], "sharpness fixture failed")
            sharp_betti.append(beta)
        if r < 5:
            sharp = line(sharp)
    require(degree_hitting_time(initial) == 3, "sharp degree time failed")

    # Scope controls and a non-simply-connected example.
    k4 = graph(4, combinations(range(4), 2))
    require(betti012(cliques(line(k4))) == [1, 0, 1], "K4 control failed")
    four_cycle = graph(4, [(0, 1), (1, 2), (2, 3), (0, 3)])
    require(betti012(cliques(line(four_cycle))) == [1, 1, 0], "cycle control failed")
    cycle_leaf = graph(5, list(four_cycle[1]) + [(0, 4)])
    require(betti012(cliques(line(cycle_leaf))) == [1, 1, 0], "pi1 control failed")
    k2 = graph(2, [(0, 1)])
    require(line(k2)[0] == 1 and line(line(k2))[0] == 0, "K2 domain control failed")
    expect_rejection(lambda: collapse_certificate(k2))
    expect_rejection(lambda: collapse_certificate(graph(4, [(0, 1), (2, 3)])))
    expect_rejection(lambda: graph(2, [(0, 0)]))
    expect_rejection(lambda: graph(2, [(0, 1), (1, 0)]))
    # Corrupt a valid tetrahedral collapse by adding an outside coface.
    tet = set(range(1, 16))
    remove_free_pair(tet.copy(), 14, 15)
    corrupted = tet | {f for f in range(1, 31) if f & 30 == f}
    expect_rejection(lambda: remove_free_pair(corrupted, 14, 15))
    expect_rejection(lambda: remove_free_pair(tet - {15}, 14, 15))

    require(dict(counts) == {1: 1, 2: 1, 3: 4, 4: 38, 5: 728},
            "labelled connected graph enumeration incomplete")
    return {
        "status": "VERIFIED",
        "connected_labelled_graphs_by_order": dict(sorted(counts.items())),
        "recurrence_graphs_checked": comparisons,
        "elementary_collapse_pairs_replayed": pairs,
        "null_attachment_cone_disks_checked": disks,
        "nonexceptional_graphs_by_degree_hitting_time": dict(sorted(hitting.items())),
        "high_degree_fixtures": high_degree,
        "sharp_fixture_degree_profiles_r0_to_r3": degree_profiles,
        "sharp_fixture_betti012_r1_to_r5": sharp_betti,
        "scope_controls": ["K4 sphere", "C4 circle", "C4 with leaf circle",
                           "K2 becomes empty", "disconnected rejected", "loops rejected",
                           "parallel edges rejected", "two corrupt collapses rejected"],
        "trust_boundary": "finite corroboration only; universal homotopy proof is in PROOF.md",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="print results without expected-file comparison")
    args = parser.parse_args()
    result = run()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if not args.emit:
        expected = Path(__file__).with_name("expected.json").read_text()
        require(json.loads(encoded) == json.loads(expected), "expected result mismatch")
    print(encoded, end="")


if __name__ == "__main__":
    main()
