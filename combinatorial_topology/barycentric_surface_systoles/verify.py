#!/usr/bin/env python3
"""Exact witness checks; Python 3.11+, standard library, no external downloads.

The universal proof is in PROOF.md. Four graph6 records are primary-source
fixtures; completeness of their classification is an imported theorem.
All checks remain active with python -O. No floating point or solver is used.
"""
from collections import Counter, defaultdict, deque
from itertools import combinations
from pathlib import Path
from hashlib import sha256
import json
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def solve_f2(rows, variables):
    """Solve dot(a,x)=b. Integer bitsets, exact row elimination."""
    basis = {}
    for a, b in rows:
        require(0 <= a < 1 << variables and b in (0, 1), "bad F2 row")
        while a:
            pivot = a.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (a, b)
                break
            c, d = basis[pivot]
            a ^= c
            b ^= d
        else:
            if b:
                return None
    answer = 0
    for pivot, (a, b) in sorted(basis.items()):
        if (a & answer).bit_count() % 2 != b:
            answer |= 1 << pivot
    return answer


def connected(adjacency):
    seen = {min(adjacency)}
    queue = list(seen)
    for u in queue:
        for v in adjacency[u] - seen:
            seen.add(v)
            queue.append(v)
    return len(seen) == len(adjacency)


def surface(facets):
    """Validate a connected closed abstract simplicial 2-manifold."""
    ts = tuple(sorted(tuple(sorted(t)) for t in facets))
    require(ts and all(len(t) == 3 and len(set(t)) == 3 for t in ts),
            "malformed triangle")
    require(len(set(ts)) == len(ts), "repeated triangle")
    vertices = sorted({v for t in ts for v in t})
    edges = sorted({e for t in ts for e in combinations(t, 2)})
    index = {e: i for i, e in enumerate(edges)}
    adjacency = defaultdict(set)
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    require(connected(adjacency), "disconnected surface")
    incidence, starts, columns = defaultdict(list), [], []
    for i, (a, b, c) in enumerate(ts):
        start = {tuple(sorted((u, v))): u for u, v in ((a, b), (b, c), (c, a))}
        starts.append(start)
        columns.append(sum(1 << index[e] for e in start))
        for e, u in start.items():
            incidence[e].append((i, u))
    require(all(len(ls) == 2 for ls in incidence.values()), "nonmanifold edge")
    for v in vertices:
        link = defaultdict(set)
        for t in ts:
            if v in t:
                a, b = (u for u in t if u != v)
                link[a].add(b)
                link[b].add(a)
        require(all(len(ls) == 2 for ls in link.values()), "noncircular link")
        require(connected(link), "disconnected vertex link")
    x0 = sum(1 << index[e] for e, ls in incidence.items() if ls[0][1] == ls[1][1])
    require(all(sum((x0 >> index[e]) & 1 for e in edges if v in e) % 2 == 0
                for v in vertices), "characteristic chain is not a cycle")
    return ts, vertices, edges, incidence, starts, columns, x0


def boundary_solution(columns, chain, edge_count):
    rows = [(sum(1 << j for j, c in enumerate(columns) if (c >> i) & 1),
             (chain >> i) & 1) for i in range(edge_count)]
    return solve_f2(rows, len(columns))


def characteristic_minimum_exhaustive(data):
    """Independent Gray-code enumeration of ALL orientation supports.

    Complementing all facets changes no edge, so fix the last facet.
    Used only on fixtures with at most eighteen facets.
    """
    ts, _, _, _, _, columns, x0 = data
    current, flips, best, best_flips = x0, 0, x0, 0
    for i in range(1, 1 << (len(ts) - 1)):
        pivot = (i & -i).bit_length() - 1
        current ^= columns[pivot]
        flips ^= 1 << pivot
        if current.bit_count() < best.bit_count():
            best, best_flips = current, flips
    return best, best_flips


def shortest_projective_cycle(data):
    """Two-sheet homology cover; return minimum cycle and facet flips."""
    ts, vertices, edges, _, _, columns, x0 = data
    require(len(vertices) - len(edges) + len(ts) == 1, "not a projective plane")
    lam = solve_f2([(c, 0) for c in columns] + [(x0, 1)], len(edges))
    require(lam is not None, "zero characteristic class")
    vi = {v: i for i, v in enumerate(vertices)}
    adjacency = [[] for _ in range(2 * len(vertices))]
    for j, (u, v) in enumerate(edges):
        sign = (lam >> j) & 1
        for sheet in (0, 1):
            a, b = 2 * vi[u] + sheet, 2 * vi[v] + (sheet ^ sign)
            adjacency[a].append((b, j))
            adjacency[b].append((a, j))
    best, chain, walk = None, None, None
    targets = []
    for root in range(len(vertices)):
        source, target = 2 * root, 2 * root + 1
        distance, predecessor = [-1] * len(adjacency), [None] * len(adjacency)
        distance[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v, e in adjacency[u]:
                if distance[v] < 0:
                    distance[v] = distance[u] + 1
                    predecessor[v] = (u, e)
                    queue.append(v)
        require(min(distance) >= 0, "disconnected homology cover")
        # Distance labels certify a lower bound along every possible path.
        require(all(abs(distance[u] - distance[v]) <= 1
                    for u, ls in enumerate(adjacency) for v, _ in ls),
                "invalid shortest-path labels")
        targets.append(distance[target])
        if best is None or distance[target] < best:
            best, current, chain = distance[target], target, 0
            walk = [vertices[current // 2]]
            while current != source:
                current, e = predecessor[current]
                chain ^= 1 << e
                walk.append(vertices[current // 2])
            walk.reverse()
    require(chain.bit_count() == best and len(set(walk[:-1])) == best
            and walk[0] == walk[-1], "minimum walk is not simple")
    require((chain & lam).bit_count() % 2 == 1, "homologically trivial cycle")
    require(boundary_solution(columns, chain, len(edges)) is None,
            "essential cycle is a boundary")
    flips = boundary_solution(columns, chain ^ x0, len(edges))
    require(flips is not None, "cycle not in characteristic class")
    return chain, flips, lam, targets, walk


def packing(data, chain, flips):
    """Reconstruct and literally verify an edge-disjoint flag packing."""
    ts, _, edges, incidence, starts, columns, x0 = data
    actual = x0
    for i in bits(flips):
        actual ^= columns[i]
    require(actual == chain, "wrong orientation reconstruction")
    counts = Counter(i for j in bits(chain) for i, _ in incidence[edges[j]])
    require(max(counts.values(), default=0) <= 1, "bad dual edges not a matching")
    deleted = {min(i for i, _ in incidence[edges[j]]) for j in bits(chain)}
    require(len(deleted) == chain.bit_count(), "repeated deleted facet")
    flags = [(i, v, e) for i, t in enumerate(ts) for e in combinations(t, 2) for v in e]
    triangle_edges = [frozenset(combinations(((v,), e, ts[i]), 2)) for i, v, e in flags]
    chosen, occupied = [], set()

    def insert(j):
        require(not occupied & triangle_edges[j], "packing conflict")
        chosen.append(j)
        occupied.update(triangle_edges[j])

    for j, (i, v, e) in enumerate(flags):
        if i not in deleted and ((v == starts[i][e]) != bool((flips >> i) & 1)):
            insert(j)
    for i in sorted(deleted):
        free = [j for j in range(6 * i, 6 * i + 6) if not occupied & triangle_edges[j]]
        pair = next(((a, b) for a, b in combinations(free, 2)
                     if not triangle_edges[a] & triangle_edges[b]), None)
        require(pair is not None, "no completion pair")
        for j in pair:
            insert(j)
    require(len(chosen) == 3 * len(ts) - chain.bit_count(), "packing size")
    cover = {((v,), t) for t in ts for v in t}
    require(len(cover) == 3 * len(ts), "cover size")
    require(all(c & cover for c in triangle_edges), "uncovered triangle")
    require(max(Counter(e for c in triangle_edges for e in c).values()) == 2,
            "invalid half-weight fractional packing")
    return sorted(chosen), sorted(deleted)


def refine(facets, k):
    """Uniform triangular k-grid, with exact integer barycentric labels."""
    labels, refined = {}, []

    def label(t, weights):
        key = tuple((v, w) for v, w in zip(t, weights) if w)
        if key not in labels:
            labels[key] = len(labels)
        return labels[key]

    for t in sorted(tuple(sorted(t)) for t in facets):
        points = {(i, j): label(t, (k - i - j, i, j))
                  for i in range(k + 1) for j in range(k + 1 - i)}
        for i in range(k):
            for j in range(k - i):
                refined.append((points[i, j], points[i + 1, j], points[i, j + 1]))
                if i + j <= k - 2:
                    refined.append((points[i + 1, j], points[i + 1, j + 1], points[i, j + 1]))
    return refined, labels


def graph6_facets(record):
    n = ord(record[0]) - 63
    require(0 < n < 63, "unsupported graph6 header")
    binary = [(ord(c) - 63 >> j) & 1 for c in record[1:] for j in range(5, -1, -1)]
    pairs = [(i, j) for j in range(n) for i in range(j)]
    require(len(binary) >= len(pairs), "truncated graph6")
    edges = {e for e, b in zip(pairs, binary) if b}
    facets = [t for t in combinations(range(n), 3) if all(e in edges for e in combinations(t, 2))]
    return n, edges, facets


def first_nonboundary_triangle(data):
    _, vertices, edges, _, _, columns, _ = data
    for t in combinations(vertices, 3):
        es = list(combinations(t, 2))
        if all(e in edges for e in es):
            chain = sum(1 << edges.index(e) for e in es)
            if boundary_solution(columns, chain, len(edges)) is None:
                return list(t)
    return None


def icosahedron_check(rp2, permutation):
    facets, antipode = [], {10: 11, 11: 10}
    for i in range(5):
        j = (i + 1) % 5
        facets += [(10, i, j), (11, 5 + i, 5 + j), (i, j, 5 + i),
                   (i, 5 + (i - 1) % 5, 5 + i)]
        antipode[i] = 5 + (i + 2) % 5
        antipode[5 + (i + 2) % 5] = i
    require({tuple(sorted(antipode[v] for v in t)) for t in facets}
            == {tuple(sorted(t)) for t in facets}, "antipode not simplicial")
    representatives = sorted({min(v, antipode[v]) for v in antipode})
    quotient = {tuple(sorted(permutation[representatives.index(min(v, antipode[v]))]
                             for v in t)) for t in facets}
    require(quotient == {tuple(t) for t in rp2}, "wrong icosahedron quotient")


def rejection_checks(rp2):
    malformed = [[], [(0, 1, 1)], [(0, 1, 2)], rp2 + [rp2[0]],
                 rp2 + [tuple(v + 10 for v in t) for t in rp2]]
    for facets in malformed:
        try:
            surface(facets)
        except ValueError:
            continue
        raise ValueError("malformed input accepted")
    data = surface(rp2)
    chain, flips, _, _, _ = shortest_projective_cycle(data)
    try:
        packing(data, chain, flips ^ 1)
    except ValueError:
        pass
    else:
        raise ValueError("corrupt orientation accepted")
    require(solve_f2([(1, 0), (1, 1)], 1) is None, "inconsistent system accepted")
    # Exhaust ALL 2-variable equation subsets against literal truth tables.
    equations = [(a, b) for a in range(4) for b in (0, 1)]
    for mask in range(1 << len(equations)):
        rows = [r for i, r in enumerate(equations) if (mask >> i) & 1]
        literal = [x for x in range(4) if all((a & x).bit_count() % 2 == b for a, b in rows)]
        answer = solve_f2(rows, 2)
        require((answer is None and not literal) or answer in literal, "F2 control failed")
    return {"malformed_surfaces": len(malformed), "corrupt_orientation": 1,
            "exhaustive_two_variable_systems": 256}


def main():
    fixture = json.loads(Path(__file__).with_name("fixtures.json").read_text())
    rp2 = fixture["rp2_facets"]
    icosahedron_check(rp2, fixture["icosahedron_quotient_isomorphism"])
    report = {"controls": rejection_checks(rp2), "projective_fixtures": {}, "four_graphs": []}
    stellar = [tuple(t) for t in rp2[1:]] + [(0, 1, 6), (0, 2, 6), (1, 2, 6)]
    cases = {"six_vertex": rp2, "stellar": stellar, "grid_two": refine(rp2, 2)[0]}
    for name, facets in cases.items():
        data = surface(facets)
        chain, flips, lam, targets, walk = shortest_projective_cycle(data)
        chosen, deleted = packing(data, chain, flips)
        if len(facets) <= 18:
            brute, _ = characteristic_minimum_exhaustive(data)
            require(brute.bit_count() == chain.bit_count(), "cover/enumeration disagreement")
        require(10 * chain.bit_count() <= 3 * len(facets), "sharp ratio failed")
        report["projective_fixtures"][name] = {
            "vertices": len(data[1]), "facets": len(facets), "edgewidth": chain.bit_count(),
            "packing": len(chosen), "cover": 3 * len(facets), "cycle": walk,
            "cocycle_edges": [data[2][i] for i in bits(lam)], "cover_target_distances": targets,
            "deleted_facets": deleted, "packing_witness": chosen}
    for record in fixture["adamaszek_four_graph6"]:
        n, edges, facets = graph6_facets(record)
        row = {"graph6": record, "vertices": n, "edges": len(edges), "triangles": len(facets)}
        try:
            data = surface(facets)
        except ValueError:
            # Record an explicit non-surface obstruction, not just rejection.
            edge_counts = Counter(e for t in facets for e in combinations(t, 2))
            bad = next((e for e, count in sorted(edge_counts.items()) if count != 2), None)
            require(bad is not None, "missing nonmanifold witness")
            row.update({"surface": False, "bad_edge": bad, "incident_triangles": edge_counts[bad]})
        else:
            require(not any(all(e in edges for e in combinations(q, 2))
                            for q in combinations(range(n), 4)), "higher clique in surface")
            chain, _, lam, _, walk = shortest_projective_cycle(data)
            require(chain.bit_count() == 4, "unexpected eleven-vertex edgewidth")
            row.update({"surface": True, "edgewidth": 4, "cycle": walk,
                        "cocycle_edges": [data[2][i] for i in bits(lam)]})
        report["four_graphs"].append(row)
    require(sum(row["surface"] for row in report["four_graphs"]) == 2,
            "wrong number of surface fixtures")
    # Connected sum of two projective planes; same three boundary labels.
    relabel = {0: 0, 1: 1, 2: 2, 3: 6, 4: 7, 5: 8}
    klein = [tuple(t) for t in rp2[1:]] + [tuple(relabel[v] for v in t) for t in rp2[1:]]
    torus = [tuple((v + i) % 7 for v in t) for i in range(7) for t in ((0, 1, 3), (0, 2, 3))]
    sphere = list(combinations(range(4), 3))
    report["other_surfaces"] = {}
    for name, facets, expected_gap in (("sphere", sphere, 0), ("torus", torus, 0), ("klein", klein, 4)):
        data = surface(facets)
        chain, flips = characteristic_minimum_exhaustive(data)
        require(chain.bit_count() == expected_gap, "unexpected characteristic minimum")
        chosen, _ = packing(data, chain, flips)
        triangle = first_nonboundary_triangle(data)
        require((triangle is None) == (name == "sphere"), "topological control failed")
        report["other_surfaces"][name] = {"vertices": len(data[1]), "facets": len(facets),
            "characteristic_minimum": chain.bit_count(), "packing": len(chosen),
            "nonboundary_triangle": triangle, "orientation_classes_checked": 1 << (len(facets) - 1)}
    # Literal five-edge essential cycle in the midpoint refinement.
    facets, labels = refine(rp2, 2)
    walk = [labels[tuple((v, 1) for v in e)] for e in fixture["midpoint_countercycle_edges"]]
    data = surface(facets)
    chain = sum(1 << data[2].index(tuple(sorted((walk[i], walk[(i + 1) % 5])))) for i in range(5))
    require(boundary_solution(data[5], chain, len(data[2])) is None, "midpoint cycle is a boundary")
    report["midpoint_countercheck"] = {"icosahedron_quotient_checked": True,
        "cycle_in_original_edge_midpoints": fixture["midpoint_countercycle_edges"],
        "length": 5, "nonboundary": True, "claimed_3k_at_k2": 6}
    output = json.dumps(report, sort_keys=True, indent=2) + "\n"
    if "--check" in sys.argv:
        require(output == Path(__file__).with_name("expected.json").read_text(), "expected output differs")
        print("PASS: characteristic cycles, exact covers, packing witnesses, four classified graphs, surface controls")
        print("expected.json SHA256 " + sha256(output.encode()).hexdigest())
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
