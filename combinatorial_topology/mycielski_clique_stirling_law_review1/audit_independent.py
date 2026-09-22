#!/usr/bin/env python3
"""Independent exact audit of the Mycielski clique-complex wedge law.

CPython 3.11+, standard library only.  This file imports no target module,
fixture, output, or certificate.  It uses bitset graphs, row reduction of the
triangle boundary matrix, recurrence iteration, and exhaustive triangle-
subcomplex peeling for Cl(M^2(K3)).  The universal claim still rests on the
human proof audited in REVIEW.md.
"""

from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def graph_from_edges(n, edges):
    adj = [0] * n
    for a, b in edges:
        require(0 <= a < b < n, "noncanonical edge")
        require(not (adj[a] >> b) & 1, "duplicate edge")
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    return tuple(adj)


def edges_of(adj):
    return [(a, b) for a in range(len(adj)) for b in range(a + 1, len(adj))
            if (adj[a] >> b) & 1]


def connected_components(vertex_mask, adj):
    count = 0
    unseen = vertex_mask
    while unseen:
        count += 1
        seed = unseen & -unseen
        unseen ^= seed
        frontier = seed
        while frontier:
            neighbours = 0
            scan = frontier
            while scan:
                bit = scan & -scan
                scan ^= bit
                neighbours |= adj[bit.bit_length() - 1]
            frontier = neighbours & unseen
            unseen ^= frontier
    return count


def triangles_of(adj):
    answer = []
    n = len(adj)
    for a in range(n):
        for b in range(a + 1, n):
            if not ((adj[a] >> b) & 1):
                continue
            common = adj[a] & adj[b] & ~((1 << (b + 1)) - 1)
            while common:
                bit = common & -common
                common ^= bit
                answer.append((a, b, bit.bit_length() - 1))
    return answer


def contains_k4(adj):
    for a, b, c in triangles_of(adj):
        if adj[a] & adj[b] & adj[c] & ~((1 << (c + 1)) - 1):
            return True
    return False


def statistics(adj):
    n = len(adj)
    es = edges_of(adj)
    ts = triangles_of(adj)
    multiplicity = {e: 0 for e in es}
    for tri in ts:
        for e in combinations(tri, 2):
            multiplicity[e] += 1
    link_components = []
    link_cycle_ranks = []
    for v in range(n):
        vertices = adj[v]
        link_edges = sum(1 for a, b in es
                         if (vertices >> a) & 1 and (vertices >> b) & 1)
        components = connected_components(vertices, adj)
        link_components.append(components)
        link_cycle_ranks.append(link_edges - vertices.bit_count() + components)
    e0 = sum(value == 0 for value in multiplicity.values())
    y = sum(max(value - 1, 0) for value in multiplicity.values())
    return {
        "n": n,
        "m": len(es),
        "t": len(ts),
        "e0": e0,
        "C": sum(link_components),
        "D": sum(link_cycle_ranks),
        "Y": y,
        "link_components": link_components,
    }


def mycielski(adj):
    """Definition-level bitset lift: old, clone, then apex."""
    n = len(adj)
    out = [0] * (2 * n + 1)
    apex = 2 * n
    for v in range(n):
        out[v] |= adj[v]
        scan = adj[v]
        while scan:
            bit = scan & -scan
            scan ^= bit
            w = bit.bit_length() - 1
            out[v] |= 1 << (n + w)
            out[n + w] |= 1 << v
        out[n + v] |= 1 << apex
        out[apex] |= 1 << (n + v)
    return tuple(out)


def matrix_rank_mod(rows, prime):
    rows = [[x % prime for x in row] for row in rows]
    if not rows:
        return 0
    height, width = len(rows), len(rows[0])
    pivot_row = 0
    for col in range(width):
        pivot = next((r for r in range(pivot_row, height) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][col], -1, prime)
        rows[pivot_row] = [(inverse * x) % prime for x in rows[pivot_row]]
        for r in range(height):
            if r == pivot_row or rows[r][col] == 0:
                continue
            factor = rows[r][col]
            rows[r] = [(x - factor * y) % prime
                       for x, y in zip(rows[r], rows[pivot_row])]
        pivot_row += 1
        if pivot_row == height:
            break
    return pivot_row


def betti_012(adj, prime):
    """Homology of a K4-free clique complex over F_prime."""
    require(not contains_k4(adj), "two-dimensional input required")
    n = len(adj)
    es = edges_of(adj)
    ts = triangles_of(adj)
    edge_index = {edge: i for i, edge in enumerate(es)}
    boundary = [[0] * len(ts) for _ in es]
    for j, (a, b, c) in enumerate(ts):
        boundary[edge_index[(b, c)]][j] = 1
        boundary[edge_index[(a, c)]][j] = -1
        boundary[edge_index[(a, b)]][j] = 1
    r2 = matrix_rank_mod(boundary, prime)
    components = connected_components((1 << n) - 1, adj)
    r1 = n - components
    return [components, len(es) - r1 - r2, len(ts) - r2]


def stirling(n, r):
    row = [1] + [0] * r
    for _ in range(n):
        row = [0] + [j * row[j] + row[j - 1] for j in range(1, r + 1)]
    return row[r]


def closed_counts(base, k):
    s2, s3, s4 = (stirling(k + 1, r) for r in (2, 3, 4))
    return (
        (base["C"] - 1) * s2 + (2 * base["e0"] + 2 * base["n"] + 1) * s3,
        base["D"] * s2 + 2 * base["Y"] * s3 + 6 * base["t"] * s4,
    )


def next_statistics(s):
    n = 2 * s["n"] + 1
    m = 3 * s["m"] + s["n"]
    t = 4 * s["t"]
    e0 = 3 * s["e0"] + s["n"]
    c = 2 * s["C"] + 2 * s["e0"] + 2 * s["n"]
    return {
        "n": n, "m": m, "t": t, "e0": e0, "C": c,
        "D": 3 * t - 2 * m + c,
        "Y": 3 * t - m + e0,
    }


def iterated_counts(base, k):
    current = dict(base)
    circles = spheres = 0
    for _ in range(k):
        circles += current["C"] - 1
        spheres += current["D"]
        current = next_statistics(current)
    return circles, spheres


def first_failure(s):
    return 1 if s["D"] else 2 if s["Y"] else 3 if s["t"] else 0


def graph_from_mask(n, mask):
    all_edges = list(combinations(range(n), 2))
    return graph_from_edges(n, [e for i, e in enumerate(all_edges) if (mask >> i) & 1])


def recurrence_tuple(s):
    return tuple(s[key] for key in ("n", "m", "t", "e0", "C", "D", "Y"))


def check_exhaustive_bases():
    counts = {"labelled": 0, "connected_k4_free": 0, "one_step_field_checks": 0}
    failures = {"1": 0, "2": 0, "3": 0, "never": 0}
    digest = sha256()
    for n in range(2, 7):
        edge_count = n * (n - 1) // 2
        for mask in range(1 << edge_count):
            counts["labelled"] += 1
            base_graph = graph_from_mask(n, mask)
            if connected_components((1 << n) - 1, base_graph) != 1 or contains_k4(base_graph):
                continue
            counts["connected_k4_free"] += 1
            base = statistics(base_graph)
            lift_graph = mycielski(base_graph)
            lift = statistics(lift_graph)
            predicted = next_statistics(base)
            require(recurrence_tuple(lift) == recurrence_tuple(predicted),
                    f"statistic recurrence n={n} mask={mask}")
            r1, q1 = closed_counts(base, 1)
            for prime in (2, 3):
                before = betti_012(base_graph, prime)
                after = betti_012(lift_graph, prime)
                require(after == [1, before[1] + r1, before[2] + q1],
                        f"homology increment n={n} mask={mask} p={prime}")
                counts["one_step_field_checks"] += 1
            for k in range(9):
                require(closed_counts(base, k) == iterated_counts(base, k),
                        f"closed recurrence n={n} mask={mask} k={k}")
            failure = first_failure(base)
            failures[str(failure) if failure else "never"] += 1
            record = [n, mask, recurrence_tuple(base), recurrence_tuple(lift), failure]
            digest.update(json.dumps(record, separators=(",", ":")).encode() + b"\n")
    return counts, failures, digest.hexdigest()


def peelable_triangle_family(adj, selected_mask):
    triangles = triangles_of(adj)
    edge_incidence = {}
    for i, tri in enumerate(triangles):
        for edge in combinations(tri, 2):
            edge_incidence[edge] = edge_incidence.get(edge, 0) | (1 << i)
    current = selected_mask
    removed = 0
    while current:
        removable = 0
        for incidence in edge_incidence.values():
            present = current & incidence
            if present and not (present & (present - 1)):
                removable = present
                break
        if not removable:
            return False, removed
        current ^= removable
        removed += 1
    return True, removed


def check_all_triangle_subcomplexes():
    k3 = graph_from_edges(3, [(0, 1), (0, 2), (1, 2)])
    second = mycielski(mycielski(k3))
    triangle_count = len(triangles_of(second))
    require(triangle_count == 16, "unexpected triangle count for M^2(K3)")
    family_count = 1 << triangle_count
    total_removed = 0
    for selected in range(family_count):
        ok, removed = peelable_triangle_family(second, selected)
        require(ok and removed == selected.bit_count(),
                f"noncollapsible triangle family {selected}")
        total_removed += removed
    require(total_removed == triangle_count * (1 << (triangle_count - 1)),
            "triangle-family incidence total")
    return {
        "fixture": "Cl(M^2(K3))",
        "triangles": triangle_count,
        "triangle_subfamilies": family_count,
        "collapse_pairs_replayed": total_removed,
    }


def check_named_adversaries():
    fixtures = {
        "edge": (2, [(0, 1)]),
        "path3": (3, [(0, 1), (1, 2)]),
        "triangle": (3, [(0, 1), (0, 2), (1, 2)]),
        "diamond": (4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)]),
        "book3": (5, [(0, 1), (0, 2), (1, 2), (0, 3), (1, 3),
                       (0, 4), (1, 4)]),
        "bowtie": (5, [(0, 1), (0, 2), (1, 2), (0, 3), (0, 4), (3, 4)]),
        "wheel4": (5, [(0, 1), (1, 2), (2, 3), (0, 3),
                        (0, 4), (1, 4), (2, 4), (3, 4)]),
        "octahedron": (6, [e for e in combinations(range(6), 2)
                            if e[0] // 2 != e[1] // 2]),
    }
    answer = {}
    for name, (n, edges) in fixtures.items():
        graph = graph_from_edges(n, edges)
        s = statistics(graph)
        rows = []
        for k in range(4):
            rows.append({"k": k, "R": closed_counts(s, k)[0],
                         "Q": closed_counts(s, k)[1]})
        answer[name] = {"statistics": {key: s[key] for key in
                                        ("n", "m", "t", "e0", "C", "D", "Y")},
                        "first_failure": first_failure(s), "counts": rows}
    require([answer[x]["first_failure"] for x in
             ("wheel4", "diamond", "triangle", "edge")] == [1, 2, 3, 0],
            "one/two/three/never boundary")
    require(answer["book3"]["statistics"]["Y"] == 2,
            "three-page repeated-edge defect")
    require(answer["bowtie"]["statistics"]["Y"] == 0 and
            answer["bowtie"]["statistics"]["t"] == 2,
            "edge-disjoint triangle boundary")
    return answer


def check_domain_boundary():
    k4 = graph_from_edges(4, combinations(range(4), 2))
    lift = mycielski(k4)
    # This is a 3-dimensional flag complex.  Euler characteristic suffices to
    # refute the K4-free two-dimensional formula's predicted four S^2 terms:
    # target theorem is deliberately not applied here.
    vertices = len(lift)
    edges = len(edges_of(lift))
    triangles = len(triangles_of(lift))
    four_cliques = 0
    for a, b, c, d in combinations(range(vertices), 4):
        if all((lift[x] >> y) & 1 for x, y in combinations((a, b, c, d), 2)):
            four_cliques += 1
    chi = vertices - edges + triangles - four_cliques
    require((vertices, edges, triangles, four_cliques, chi) == (9, 22, 16, 5, -2),
            "K4 boundary control")
    return {"base": "K4 (excluded)", "f_vector": [vertices, edges, triangles, four_cliques],
            "euler_characteristic": chi}


def run():
    base_counts, failures, digest = check_exhaustive_bases()
    return {
        "status": "pass",
        "exhaustive_bases": base_counts,
        "first_failure_categories": failures,
        "base_audit_sha256": digest,
        "all_triangle_subcomplexes": check_all_triangle_subcomplexes(),
        "named_adversaries": check_named_adversaries(),
        "domain_boundary": check_domain_boundary(),
    }


if __name__ == "__main__":
    result = run()
    if "--emit" not in sys.argv[1:]:
        expected_path = Path(__file__).with_name("EXPECTED_OUTPUT.json")
        require(result == json.loads(expected_path.read_text()), "expected output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))
