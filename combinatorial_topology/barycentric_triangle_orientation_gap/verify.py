#!/usr/bin/env python3
"""Exact corroboration, CPython 3.11+, standard library; no solver or data files.

The universal theorem is proved in PROOF.md. This program independently
optimizes literal triangle-conflict graphs and replays packing witnesses.
It uses explicit checks (also active under python -O).
"""
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys


def require(test, message):
    if not test:
        raise ValueError(message)


def normalize(facets, incidence_limit=True):
    facets = [tuple(sorted(t)) for t in facets]
    require(bool(facets), "empty facet family")
    require(all(len(t) == 3 and len(set(t)) == 3 for t in facets),
            "facets must be three distinct vertices")
    require(len(set(facets)) == len(facets), "duplicate facet")
    facets = tuple(sorted(facets))
    counts = Counter(e for t in facets for e in combinations(t, 2))
    require(not incidence_limit or max(counts.values()) <= 2,
            "edge in more than two facets")
    return facets


def model(facets, incidence_limit=True):
    """Construct the graph from literal face inclusions, then ALL 3-cliques."""
    ts = normalize(facets, incidence_limit)
    faces = sorted({frozenset(s) for t in ts for k in (1, 2, 3)
                    for s in combinations(t, k)},
                   key=lambda s: (len(s), tuple(sorted(s))))
    edges = {frozenset((a, b)) for a, b in combinations(faces, 2)
             if a < b or b < a}
    cliques = {frozenset(c) for c in combinations(faces, 3)
               if all(frozenset(e) in edges for e in combinations(c, 2))}
    flags = [(v, e, i) for i, t in enumerate(ts)
             for e in combinations(t, 2) for v in e]
    triangles = [frozenset((frozenset((v,)), frozenset(e), frozenset(ts[i])))
                 for v, e, i in flags]
    require(set(triangles) == cliques and len(cliques) == 6 * len(ts),
            "flags differ from literal graph triangles")
    triangle_edges = [frozenset(frozenset(e) for e in combinations(c, 2))
                      for c in triangles]
    adj = [0] * len(flags)
    for i, j in combinations(range(len(flags)), 2):
        if triangle_edges[i] & triangle_edges[j]:
            adj[i] |= 1 << j
            adj[j] |= 1 << i
    return ts, flags, edges, triangle_edges, adj


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def maximum_independent_set(adj):
    """Exact maximum clique in complement, with greedy-color upper bounds.

    For each recursion, color the complement subgraph properly. Vertices are
    listed by increasing color; the prefix ending at v uses <= bound[v]
    colors, so no clique in that prefix exceeds bound[v]. Reverse branching
    exhausts the last vertex of every clique unless this bound prunes it.
    No orientation or proposed packing formula is used for any bound.
    """
    n = len(adj)
    full = (1 << n) - 1
    comp = [full ^ a ^ (1 << i) for i, a in enumerate(adj)]
    best = []

    def expand(chosen, candidates):
        nonlocal best
        rest, color, order, bounds = candidates, 0, [], []
        while rest:
            color += 1
            available = rest
            while available:
                bit = available & -available
                v = bit.bit_length() - 1
                order.append(v)
                bounds.append(color)
                rest ^= bit
                available = (available ^ bit) & ~comp[v]
        for i in range(len(order) - 1, -1, -1):
            if len(chosen) + bounds[i] <= len(best):
                return
            v = order[i]
            nxt = candidates & comp[v]
            if nxt:
                expand(chosen + [v], nxt)
            elif len(chosen) + 1 > len(best):
                best = chosen + [v]
            candidates &= ~(1 << v)

    if n:
        expand([], full)
    return sorted(best)


def brute_mis_size(adj):
    """Separate include/exclude recurrence for small-control verification."""
    @lru_cache(None)
    def solve(mask):
        if not mask:
            return 0
        v = next(bits(mask))
        rest = mask & ~(1 << v)
        return max(solve(rest), 1 + solve(rest & ~adj[v]))
    return solve((1 << len(adj)) - 1)


def orientation_data(ts):
    starts = []
    incidence = {}
    for i, (a, b, c) in enumerate(ts):
        d = {tuple(sorted(e)): v for e, v in
             (((a, b), a), ((b, c), b), ((c, a), c))}
        starts.append(d)
        for e, v in d.items():
            incidence.setdefault(e, []).append((i, v))
    constraints = []
    for e, inc in sorted(incidence.items()):
        if len(inc) == 2:
            (a, u), (b, v) = inc
            constraints.append((a, b, int(u == v)))
    return starts, constraints


def coherent_assignment(f, constraints, deleted):
    deleted = set(deleted)
    adj = [[] for _ in range(f)]
    for a, b, parity in constraints:
        adj[a].append((b, parity))
        adj[b].append((a, parity))
    labels = {}
    for start in range(f):
        if start in deleted or start in labels:
            continue
        labels[start] = 0
        queue = [start]
        for u in queue:
            for v, parity in adj[u]:
                if v in deleted:
                    continue
                want = labels[u] ^ parity
                if v in labels:
                    if labels[v] != want:
                        return None
                else:
                    labels[v] = want
                    queue.append(v)
    return labels


def orientation_defect(f, constraints):
    """Enumerate deleted facet subsets, using only orientation propagation."""
    for k in range(f + 1):
        for deleted in combinations(range(f), k):
            labels = coherent_assignment(f, constraints, deleted)
            if labels is not None:
                return deleted, labels
    raise RuntimeError("unreachable")


def greedy_packing(flags, adj, starts, deleted, labels):
    chosen = []
    deleted = set(deleted)
    for j, (v, e, i) in enumerate(flags):
        if i not in deleted and ((v == starts[i][e]) != bool(labels[i])):
            chosen.append(j)
    occupied = sum(1 << j for j in chosen)
    require(all(not (adj[j] & occupied) for j in chosen),
            "coherent triples conflict")
    for i in sorted(deleted):
        available = [j for j in range(6 * i, 6 * i + 6)
                     if not (adj[j] & occupied)]
        require(len(available) >= 3, "too many flags forbidden")
        pair = next(((a, b) for a, b in combinations(available, 2)
                     if not (adj[a] & (1 << b))), None)
        require(pair is not None, "no independent pair")
        chosen.extend(pair)
        occupied |= sum(1 << j for j in pair)
    return sorted(chosen)


def check_packing(chosen, triangle_edges):
    require(len(chosen) == len(set(chosen)), "repeated triangle")
    used = set()
    for i in chosen:
        require(isinstance(i, int) and 0 <= i < len(triangle_edges),
                "triangle index out of range")
        require(not (used & triangle_edges[i]), "packing shares an edge")
        used.update(triangle_edges[i])


def check_cover(cover, graph_edges, triangle_edges):
    require(cover <= graph_edges, "cover contains a nongraph edge")
    require(all(cover & t for t in triangle_edges), "uncovered triangle")


def check_instance(facets):
    ts, flags, edges, triangle_edges, adj = model(facets)
    f = len(ts)
    cover = {frozenset((frozenset((v,)), frozenset(t)))
             for t in ts for v in t}
    check_cover(cover, edges, triangle_edges)
    counts = Counter(e for triangle in triangle_edges for e in triangle)
    require(max(counts.values()) <= 2 and len(cover) == 3 * f,
            "fractional packing / integral cover certificate failed")
    starts, constraints = orientation_data(ts)
    deleted, labels = orientation_defect(f, constraints)
    kappa = len(deleted)
    # Exhaust all sign assignments independently of facet deletions.
    lam = min(sum((((mask >> a) ^ (mask >> b)) & 1) != p
                  for a, b, p in constraints) for mask in range(1 << f))
    require(lam == kappa, "signed frustration equality failed")
    constructed = greedy_packing(flags, adj, starts, deleted, labels)
    check_packing(constructed, triangle_edges)
    exact = maximum_independent_set(adj)
    check_packing(exact, triangle_edges)
    require(len(exact) == len(constructed) == 3 * f - kappa,
            "independent optimization disagrees with formula")
    full = {i for i in range(f) if sum(j // 6 == i for j in exact) == 3}
    require(coherent_assignment(f, constraints, set(range(f)) - full)
            is not None, "full hexagons do not admit orientations")
    require(len(full) == f - kappa, "optimal packing has excess deficient blocks")
    if f <= 4:
        require(brute_mis_size(adj) == len(exact), "MIS control disagreement")
    require(kappa <= f // 2 and 5 * len(cover) <= 6 * len(exact),
            "elementary ratio bound failed")
    return {"facets": f, "graph_vertices": len(set().union(*edges)),
            "graph_triangles": len(flags), "cover": len(cover),
            "packing": len(exact), "orientation_defect": kappa,
            "deleted_facets": list(deleted), "packing_witness": constructed}


def local_checks():
    # A C6 whose three side pairs are (0,1), (2,3), (4,5).
    adj = [(1 << ((i - 1) % 6)) | (1 << ((i + 1) % 6)) for i in range(6)]
    independent = [s for s in range(64) if all(not (adj[i] & s) for i in bits(s))]
    triples = [s for s in independent if s.bit_count() == 3]
    require(triples == [0b010101, 0b101010], "hexagon maximum classes")
    require(max(s.bit_count() for s in independent) == 3, "hexagon alpha")
    # Per side: no forbidden endpoint, first endpoint, or second endpoint.
    for state in product((-1, 0, 1), repeat=3):
        forbidden = sum(1 << (2 * i + b) for i, b in enumerate(state) if b >= 0)
        available = 63 ^ forbidden
        require(any(s.bit_count() == 2 and s & available == s for s in independent),
                "local greedy completion failed")
    return {"independent_subsets": len(independent), "maximum_classes": 2,
            "side_forbiddance_patterns": 27}


def mis_controls():
    # ALL labelled simple graphs on five vertices, unrelated to flag gadgets.
    pairs = list(combinations(range(5), 2))
    for mask in range(1 << len(pairs)):
        adj = [0] * 5
        for j, (a, b) in enumerate(pairs):
            if mask & (1 << j):
                adj[a] |= 1 << b
                adj[b] |= 1 << a
        require(len(maximum_independent_set(adj)) == brute_mis_size(adj),
                "generic exact optimizer failed")
    return 1 << len(pairs)


def closed_surface_signature(facets):
    ts = normalize(facets)
    vertices = set().union(*map(set, ts))
    edges = Counter(e for t in ts for e in combinations(t, 2))
    require(set(edges.values()) == {2}, "surface has boundary or branch edge")
    for v in vertices:
        link_edges = [tuple(u for u in t if u != v) for t in ts if v in t]
        link_vertices = set().union(*map(set, link_edges))
        degrees = Counter(u for e in link_edges for u in e)
        require(set(degrees.values()) == {2}, "noncircular vertex link")
        seen = {min(link_vertices)}
        while True:
            more = {w for a, b in link_edges for u, w in ((a, b), (b, a)) if u in seen}
            if more <= seen:
                break
            seen |= more
        require(seen == link_vertices, "disconnected vertex link")
    return {"vertices": len(vertices), "edges": len(edges), "facets": len(ts),
            "euler_characteristic": len(vertices) - len(edges) + len(ts)}


def rejection_checks():
    bad = [[], [(0, 1)], [(0, 1, 1)], [(0, 1, 2), (2, 0, 1)],
           [(0, 1, 2), (0, 1, 3), (0, 1, 4)]]
    for ts in bad:
        try:
            normalize(ts)
        except ValueError:
            continue
        raise RuntimeError("malformed input accepted")
    _, _, edges, triangles, _ = model([(0, 1, 2)])
    for selected in ([0, 0], [0, 1], [-1], [6]):
        try:
            check_packing(selected, triangles)
        except ValueError:
            continue
        raise RuntimeError("corrupt packing accepted")
    try:
        check_cover(set(), edges, triangles)
    except ValueError:
        pass
    else:
        raise RuntimeError("empty cover accepted")
    return {"input_rejections": len(bad), "packing_rejections": 4,
            "cover_rejections": 1}


def book_control():
    ts, _, edges, triangles, _ = model([(0, 1, i) for i in (2, 3, 4)], False)
    cover = {frozenset((frozenset((v,)), frozenset((0, 1)))) for v in (0, 1)}
    for t in ts:
        for v in (0, 1):
            cover.add(frozenset((frozenset((v, t[2])), frozenset(t))))
    check_cover(cover, edges, triangles)
    require(len(cover) == 8 < 3 * len(ts), "invalid book counterexample")
    return {"facets": 3, "edge_incidence": 3, "explicit_cover": len(cover),
            "false_formula_cover": 9}


def main():
    result = {"local_completion": local_checks(), "generic_MIS_controls": mis_controls()}
    counts = Counter()
    defect_counts = Counter()
    universe = list(combinations(range(5), 3))
    digest = sha256()
    for mask in range(1, 1 << len(universe)):
        ts = [t for i, t in enumerate(universe) if mask & (1 << i)]
        if max(Counter(e for t in ts for e in combinations(t, 2)).values()) > 2:
            continue
        row = check_instance(ts)
        counts[len(ts)] += 1
        defect_counts[row["orientation_defect"]] += 1
        digest.update(json.dumps([mask, row], sort_keys=True, separators=(",", ":")).encode())
        digest.update(b"\n")
    result["all_facet_families_on_five_labels"] = {
        "counts_by_facets": dict(sorted(counts.items())), "total": sum(counts.values()),
        "counts_by_defect": dict(sorted(defect_counts.items())), "witness_sha256": digest.hexdigest()}
    rp2 = [(0, 1, 2), (0, 1, 3), (0, 2, 4), (0, 3, 5), (0, 4, 5),
           (1, 2, 5), (1, 3, 4), (1, 4, 5), (2, 3, 4), (2, 3, 5)]
    fixtures = {
        "projective_plane": rp2,
        "punctured_projective_plane": rp2[1:],
        "two_disjoint_triangles": [(0, 1, 2), (3, 4, 5)],
        "two_triangles_touching_at_vertex": [(0, 1, 2), (0, 3, 4)],
        "tetrahedron_boundary": list(combinations(range(4), 3)),
        "octahedron_boundary": list(product((0, 1), (2, 3), (4, 5))),
    }
    result["fixtures"] = {name: check_instance(ts) for name, ts in fixtures.items()}
    result["projective_plane_surface_check"] = closed_surface_signature(rp2)
    require(result["projective_plane_surface_check"]["euler_characteristic"] == 1,
            "wrong projective plane Euler characteristic")
    require(result["fixtures"]["projective_plane"]["orientation_defect"] == 3,
            "unexpected projective plane defect")
    # Relabel vertices and reverse facet listings; all numerical invariants agree.
    relabelled = [tuple(11 - 2 * v for v in t[::-1]) for t in reversed(rp2)]
    relabel_row = check_instance(relabelled)
    for key in ("facets", "graph_vertices", "graph_triangles", "cover", "packing", "orientation_defect"):
        require(relabel_row[key] == result["fixtures"]["projective_plane"][key],
                "vertex relabelling changed an invariant")
    result["relabelling_checks"] = 1
    result["negative_controls"] = {**rejection_checks(), "three_face_book": book_control()}
    canonical = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if sys.argv[1:] == ["--emit"]:
        print(canonical, end="")
        return
    require(not sys.argv[1:], "usage: verify.py [--emit]")
    expected = Path(__file__).with_name("expected.json").read_text()
    require(canonical == expected, "evidence differs from expected.json")
    print("VERIFIED: " + str(sum(counts.values())) + " facet families, "
          + str(len(fixtures)) + " fixtures, 27 local patterns, 1024 MIS controls")
    print("RP2: f=10, tau=tau*=nu*=30, nu=27, kappa=3")
    print("evidence SHA-256: " + sha256(canonical.encode()).hexdigest())


if __name__ == "__main__":
    main()
