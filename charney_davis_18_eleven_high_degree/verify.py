#!/usr/bin/env python3
"""Exact supplementary audits for the suspension-compatibility proof.

No sphere enumeration, attachment search, external package, or solver.
The written proof supplies the universal topology and component reduction.
"""
from collections import Counter
from itertools import combinations, product
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def graph(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        require(0 <= u < v < n and v not in adj[u], "invalid edge list")
        adj[u].add(v)
        adj[v].add(u)
    return adj


def triangle_count_at(adj, v):
    return sum(y in adj[x] for x, y in combinations(sorted(adj[v]), 2))


def local_suspension_audit():
    """A={x,y,r,s} is independent; q is joined to all four.

    The isolated edge u--v of the link complement has all its remaining
    neighbors in A. Colors, not partial degrees in this seven-vertex
    graph, specify global degrees three/four. Missing outside edges can
    only increase the local c+t and common-neighbor obstructions checked.
    """
    counts = Counter()
    survivors = []
    for du, dv in product((3, 4), repeat=2):
        cubic = {0, 1}
        if du == 3:
            cubic.add(5)
        if dv == 3:
            cubic.add(6)
        quartic = set(range(7))-cubic
        for S in combinations(range(4), du-1):
            for R in combinations(range(4), dv-1):
                counts["patterns"] += 1
                edges = {(i, 4) for i in range(4)} | {(5, 6)}
                edges |= {(i, 5) for i in S} | {(i, 6) for i in R}
                adj = graph(7, sorted(edges))
                if any(len(adj[w] & cubic)+triangle_count_at(adj, w) > 2
                       for w in quartic):
                    counts["rejected_quartic_local_bound"] += 1
                    continue
                if any(all(v in adj[u] for u, v in combinations(tri, 2))
                       for tri in combinations(sorted(cubic), 3)):
                    counts["rejected_cubic_triangle"] += 1
                    continue
                if any(len(adj[u] & adj[v]) >= 2
                       for u, v in combinations(sorted(cubic), 2)
                       if v not in adj[u]):
                    counts["rejected_cubic_common_neighbors"] += 1
                    continue
                require(du == dv == 3, "suspension pair must be CC")
                require(set(S).isdisjoint(R) and set(S) | set(R) == set(range(4)),
                        "two disjoint halves cover A")
                require(len(set(S) & {0, 1}) == len(set(R) & {0, 1}) == 1,
                        "each half has one cubic and one quartic")
                survivors.append({"u_neighbors_in_A": list(S),
                                  "v_neighbors_in_A": list(R)})
    require(counts["patterns"] == 100 and len(survivors) == 4,
            "complete local pattern audit")
    return {"counts": dict(sorted(counts.items())), "survivors": survivors}


def eligible_pairs(adj):
    """Endpoints allowed by the new compatibility lemma.

    The two middle vertices have J-degree two. Endpoints must have a free
    quartic degree slot, be nonadjacent, and have no common J-neighbor.
    """
    result = set()
    for u, v in combinations(range(len(adj)), 2):
        if v not in adj[u] or len(adj[u]) != 2 or len(adj[v]) != 2:
            continue
        x, = adj[u]-{v}
        y, = adj[v]-{u}
        if x == y or max(len(adj[x]), len(adj[y])) >= 3:
            continue
        if y in adj[x] or adj[x] & adj[y]:
            continue
        result.add(tuple(sorted((x, y))))
    return result


def branch_matchings(vertices, parent):
    """Every matching with edges between distinct branches, exactly once."""
    if not vertices:
        yield ()
        return
    x, *rest = vertices
    yield from branch_matchings(rest, parent)
    for j, y in enumerate(rest):
        if parent[x] == parent[y]:
            continue
        for matching in branch_matchings(rest[:j]+rest[j+1:], parent):
            yield ((x, y),)+matching


def rooted_component_audit():
    counts = Counter()
    for ks in product(range(3), repeat=3):
        base = {(0, 1), (0, 2), (0, 3)}
        parent = {}
        n = 4
        for a, k in enumerate(ks, 1):
            for _ in range(k):
                base.add((a, n))
                parent[n] = a
                n += 1
        for matching in branch_matchings(list(range(4, n)), parent):
            for outside_edges in range((10-n)//2+1):
                edges = base | set(matching)
                edges |= {(n+2*i, n+2*i+1) for i in range(outside_edges)}
                adj = graph(10, sorted(edges))
                counts["models"] += 1
                counts["middle_edges_with_degree_two_ends"] += sum(
                    len(adj[u]) == len(adj[v]) == 2 for u, v in edges)
                require(not eligible_pairs(adj), "no compatible quartic pair in rooted model")
    return dict(sorted(counts.items()))


def forced_labels(adj):
    """Union degree-two vertices forced to have the same quartic neighbor.

    This implements the empty-common-J-neighborhood version of the
    disjoint edge-link obstruction, independently of eligible_pairs().
    """
    parent = list(range(len(adj)))
    pairs = []

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for u, v in combinations(range(len(adj)), 2):
        if len(adj[u]) != 2 or len(adj[v]) != 2 or v in adj[u] or adj[u] & adj[v]:
            continue
        if any(y in adj[x] for x in adj[u] for y in adj[v]):
            pairs.append((u, v))
            parent[find(v)] = find(u)
    classes = {}
    for v in range(len(adj)):
        if len(adj[v]) == 2:
            classes.setdefault(find(v), []).append(v)
    return pairs, sorted(classes.values())


def maximum_matching(vertices, edges):
    """Independent recursive matching count for the small auxiliary paths."""
    if not vertices:
        return 0
    x = min(vertices)
    rest = vertices-{x}
    value = maximum_matching(rest, edges)
    for y in rest:
        if tuple(sorted((x, y))) in edges:
            value = max(value, 1+maximum_matching(rest-{y}, edges))
    return value


def path_audit():
    rows = []
    for n in range(1, 11):
        adj = graph(n, [(i, i+1) for i in range(n-1)])
        allowed = eligible_pairs(adj)
        require(allowed == {(i, i+3) for i in range(n-3)},
                "path partners are precisely distance-three pairs")
        # Endpoints have only one possible partner. Internal vertices have
        # only one actual quartic slot, independently of auxiliary degree.
        for endpoint in {0, n-1}:
            require(sum(endpoint in pair for pair in allowed) <= 1,
                    "path endpoint has at most one partner")
        matching = maximum_matching(set(range(n)), allowed)
        require(matching <= n//2, "path pair bound")
        forced, classes = forced_labels(adj)
        if n == 10:
            require((1, 4) in forced and (4, 7) in forced,
                    "P10's two forced equalities")
            require(any({1, 4, 7} <= set(block) for block in classes),
                    "P10 forces three cubic neighbors of one quartic")
        rows.append({"vertices": n, "allowed_pairs": len(allowed),
                     "maximum_matching": matching,
                     "largest_forced_label_class": max(map(len, classes), default=0)})
    return rows


def cycle_audit():
    rows = []
    for n in range(5, 11):
        edges = {tuple(sorted((i, (i+1) % n))) for i in range(n)}
        adj = graph(n, sorted(edges))
        allowed = eligible_pairs(adj)
        _, classes = forced_labels(adj)
        record = {"vertices": n, "allowed_pairs": len(allowed),
                  "forced_label_classes": classes}
        if n == 5:
            require(not allowed, "C5 cannot meet a quartic with c=2")
            record["obstruction"] = "no compatible pair"
        elif n >= 7:
            require(any(len(block) >= 3 for block in classes),
                    "long cycle forces a class larger than two")
            record["obstruction"] = "at least three cubic neighbors of one quartic"
        else:
            require(classes == [[0, 3], [1, 4], [2, 5]], "C6 opposite pairs")
            labels = {v: label for label, block in enumerate(classes) for v in block}
            required_neighbors = {}
            for label, block in enumerate(classes):
                x, y = block
                alternatives = []
                for u in adj[x]:
                    for v in adj[y]:
                        if v in adj[u]:
                            alternatives.append(frozenset((labels[u], labels[v])))
                require(alternatives and len(set(alternatives)) == 1,
                        "both C6 paths force the same quartic neighbors")
                required_neighbors[label] = set(alternatives[0])
            require(all(required_neighbors[i] == {0, 1, 2}-{i} for i in range(3)),
                    "C6 forces the forbidden quartic triangle")
            record["obstruction"] = "quartic triangle at a c=2 vertex"
        rows.append(record)
    return rows


def incidence_audit():
    rows = []
    for e in range(7, 11):
        lower = 22-2*e
        # Directly enumerate the eight quartic c-values by their counts.
        feasible = []
        for n0 in range(9):
            for n1 in range(9-n0):
                n2 = 8-n0-n1
                if n1+2*n2 == 30-2*e:
                    require(n2 == lower+n0, "quartic incidence identity")
                    feasible.append(n2)
        require(min(feasible) == lower, "sharp numerical lower count")
        rows.append({"cubic_edges": e, "quartic_incidences": 30-2*e,
                     "minimum_quartics_with_two_cubic_neighbors": lower})
    return rows


def main():
    result = {"status": "PASS", "local_suspension_patterns": local_suspension_audit(),
              "rooted_component_models": rooted_component_audit(),
              "paths": path_audit(), "cycles": cycle_audit(),
              "incidences": incidence_audit(),
              "scope": "Supplementary finite audits of the written structural proof; no sphere census, attachment search, solver, or independent review."}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
