#!/usr/bin/env python3
"""Exact finite controls for the structural proof, not a universal census.

Author: Atlas / studio-researcher-1, researcher. Standard library only.
No inherited evaluator or classification code is imported. Run with
Python 3.11+; all mathematical comparisons are exact.
"""

import argparse
from collections import Counter, deque
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def make_tree(n, edges):
    if not isinstance(n, int) or n < 2:
        raise ValueError("order must be an integer at least two")
    neighbors = [set() for _ in range(n)]
    seen = set()
    for u, v in edges:
        if not (isinstance(u, int) and isinstance(v, int)
                and 0 <= u < n and 0 <= v < n and u != v):
            raise ValueError("invalid vertex or loop")
        edge = tuple(sorted((u, v)))
        if edge in seen:
            raise ValueError("duplicate edge")
        seen.add(edge)
        neighbors[u].add(v)
        neighbors[v].add(u)
    if len(seen) != n - 1:
        raise ValueError("a tree must have n-1 distinct edges")
    reached, pending = {0}, [0]
    while pending:
        u = pending.pop()
        for v in neighbors[u] - reached:
            reached.add(v)
            pending.append(v)
    if len(reached) != n:
        raise ValueError("disconnected input")
    return tuple(tuple(sorted(row)) for row in neighbors)


def bfs(adj, root):
    n = len(adj)
    distance = [-1] * n
    parent = [-1] * n
    distance[root] = 0
    queue = deque([root])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if distance[v] < 0:
                distance[v] = distance[u] + 1
                parent[v] = u
                queue.append(v)
    require(all(d >= 0 for d in distance), "BFS missed a vertex")
    return distance, parent


def direct_data(adj):
    n = len(adj)
    degree = [len(row) for row in adj]
    leaves = [v for v in range(n) if degree[v] == 1]
    internal = [v for v in range(n) if degree[v] > 1]
    distances = [bfs(adj, v)[0] for v in range(n)]
    potential = [sum(degree[u] * (1 << distances[v][u])
                     for u in internal) for v in range(n)]
    parents = sorted({adj[z][0] for z in leaves})
    maximum = max(potential[p] for p in parents)
    maximizers = [p for p in parents if potential[p] == maximum]
    return degree, leaves, internal, distances, potential, parents, maximizers


def deficit(adj, u, excluded):
    children = [x for x in adj[u] if x != excluded]
    return (1 if not children
            else 3 + 2 * sum(deficit(adj, x, u) for x in children))


def check_deficit_identity(adj, degree, internal, distances, counts):
    for u, neighbors in enumerate(adj):
        for v in neighbors:
            component = {u}
            pending = [u]
            while pending:
                x = pending.pop()
                for y in adj[x]:
                    if y == v or y in component:
                        continue
                    component.add(y)
                    pending.append(y)
            reference = 1 + 2 * sum(degree[x] * (1 << distances[u][x])
                                    for x in internal if x in component)
            require(deficit(adj, u, v) == reference,
                    "directed deficit/full-degree identity failed")
            counts["oriented_deficit_identities"] += 1


def edge_certificate(adj, p, data, counts):
    degree, leaves, internal, distances, potential, _, maximizers = data
    n = len(adj)
    depth, parent = bfs(adj, p)
    H = max(depth)
    h = max(depth[u] for u in internal)
    d = sum(degree[z] == 1 for z in adj[p])
    require(H == h + 1, "leaf/core eccentricity translation failed")
    require(potential[p] <= 2 * (n - 1) * (1 << h),
            "potential degree-sum bound failed")
    counts["parent_height_and_potential_controls"] += 1

    for z in adj[p]:
        if degree[z] == 1:
            require(potential[z] == 2 * potential[p],
                    "leaf/parent potential identity failed")
            require(deficit(adj, p, z) == 1 + 2 * potential[p],
                    "leaf deficit/excess normalization failed")
            counts["leaf_normalization_controls"] += 1

    weak_rhs = (h + 1 + Fraction(9, 5) * d
                - Fraction(4, 5) * d / (1 << h))
    if H == 1:
        require(d == n - 1 and potential[p] == d,
                "H=1 did not have the star normalization")
        require(weak_rhs == n, "star weaker-budget equality failed")
        counts["star_parent_controls"] += 1
        return None

    # This decomposition and its upper bound hold even without maximality.
    w = min(z for z in leaves if depth[z] == H)
    path = set()
    x = w
    while x != p:
        path.add((parent[x], x))
        x = parent[x]
    root_leaf_edges = {(p, z) for z in adj[p] if degree[z] == 1}
    require(path.isdisjoint(root_leaf_edges), "path/root-leaf overlap")
    weights = {(parent[v], v): (3 if degree[v] > 1 else 1)
               * (1 << depth[parent[v]]) for v in range(n) if v != p}
    require(sum(weights.values()) == potential[p],
            "edge-end split disagreed with BFS potential")
    t = 1 << (H - 1)
    require(sum(weights[e] for e in path) == 4 * t - 3,
            "chosen path weight failed")
    require(sum(weights[e] for e in root_leaf_edges) == d,
            "root-leaf weight failed")
    remaining = set(weights) - path - root_leaf_edges
    m = len(remaining)
    require(m == n - 1 - d - H and m >= 0,
            "remaining-edge count failed")
    E = Fraction(sum(weights[e] for e in remaining), t)
    require(potential[p] == d + 4 * t - 3 + t * E,
            "potential/path/complement identity failed")

    heavy = sorted(e for e in remaining
                   if degree[e[1]] > 1 and depth[e[0]] == H - 2)
    paired_edges = set()
    for edge in heavy:
        _, v = edge
        children = [z for z in adj[v] if parent[z] == v]
        require(children and all(degree[z] == 1 for z in children),
                "a bottom nonleaf lacked leaf children")
        mate = (v, min(children))
        require(mate in remaining, "pair left the remaining set")
        require(edge not in paired_edges and mate not in paired_edges,
                "bottom-edge pairing was not injective")
        require(Fraction(weights[edge], t) == Fraction(3, 2)
                and Fraction(weights[mate], t) == 1,
                "pair weights failed")
        paired_edges.update((edge, mate))
    require(all(Fraction(weights[e], t) <= 1
                for e in remaining - paired_edges),
            "an unpaired edge was overweight")
    require(E <= m + Fraction(len(heavy), 2) <= Fraction(5, 4) * m,
            "edge-charge upper bound failed")
    require(Fraction(potential[w], 2) >= (d + 3) * t - 2,
            "deepest-leaf comparator failed")
    counts["nonstar_edge_certificates"] += 1
    counts["explicit_bottom_edge_pairs"] += len(heavy)

    lower = Fraction(d - 1) * (1 - Fraction(1, t))
    if p in maximizers:
        require(potential[p] >= Fraction(potential[w], 2),
                "maximality did not apply to the chosen leaf")
        require(lower <= E <= Fraction(5, 4) * m,
                "strong nonstar budget failed")
        strong_rhs = (h + Fraction(6, 5) + Fraction(9, 5) * d
                      - Fraction(4, 5) * (d - 1) / (1 << h))
        require(n >= strong_rhs > weak_rhs,
                "strong-to-weak budget implication failed")
        require(strong_rhs - weak_rhs == Fraction(1, 5)
                + Fraction(4, 5) / (1 << h), "budget slack mismatch")
        counts["maximizing_nonstar_budget_controls"] += 1
        if d == 1:
            counts["maximizing_d1_controls"] += 1
    return {"n": n, "p": p, "d": d, "H": H, "h": h,
            "Xp": potential[p], "deepest_leaf": w,
            "deepest_leaf_score": potential[w] // 2,
            "remaining_edges": m, "bottom_pairs": len(heavy),
            "E": str(E), "strong_left": str(lower),
            "charge_upper": str(Fraction(5, 4) * m)}


def check_case(adj, counts):
    counts["input_cases"] += 1
    if len(adj) == 2:
        require(adj == ((1,), (0,)), "K2 fixture failed")
        # Mass-two and mass-three behavior is proved directly in PROOF.md.
        counts["K2_fixtures"] += 1
        return
    data = direct_data(adj)
    check_deficit_identity(adj, data[0], data[2], data[3], counts)
    for p in data[5]:
        edge_certificate(adj, p, data, counts)
    counts["maximizing_parent_occurrences"] += len(data[6])
    if len(data[6]) > 1:
        counts["tied_input_cases"] += 1


def decode_prufer(n, sequence):
    degree = [1] * n
    for v in sequence:
        degree[v] += 1
    edges = []
    for v in sequence:
        leaf = next(u for u in range(n) if degree[u] == 1)
        edges.append((leaf, v))
        degree[leaf] -= 1
        degree[v] -= 1
    final = [u for u in range(n) if degree[u] == 1]
    require(len(final) == 2, "Pruefer decoding failed")
    edges.append(tuple(final))
    return make_tree(n, edges)


def path_tree(n):
    return make_tree(n, [(u, u + 1) for u in range(n - 1)])


def star(d):
    return make_tree(d + 1, [(0, v) for v in range(1, d + 1)])


def branched_broom(d, e, t):
    require(min(d, e, t) >= 1, "positive R parameters required")
    edges = [(u, u + 1) for u in range(t)]
    next_vertex = t + 1
    for _ in range(d):
        edges.append((0, next_vertex))
        next_vertex += 1
    for _ in range(e):
        edges.extend(((t, next_vertex), (next_vertex, next_vertex + 1)))
        next_vertex += 2
    return make_tree(next_vertex, edges)


def double_broom(d, e, t):
    edges = [(u, u + 1) for u in range(t)]
    next_vertex = t + 1
    for root, count in ((0, d), (t, e)):
        for _ in range(count):
            edges.append((root, next_vertex))
            next_vertex += 1
    return make_tree(next_vertex, edges)


def negative_controls():
    n22 = branched_broom(8, 4, 5)
    data = direct_data(n22)
    require(0 in data[6] and data[4][0] == 741,
            "order-22 maximizing root changed")
    h = max(data[3][0][u] for u in data[2])
    require(h == 6 and h > len(n22) - 2 * 8 - 1,
            "false old height bound was not refuted")
    opposite = sorted({n22[z][0] for z in data[1] if n22[z][0] != 0})
    require(all(data[4][q] == 732 for q in opposite),
            "order-22 opposite potential changed")

    nonmax = branched_broom(8, 1, 3)
    data = direct_data(nonmax)
    H = max(data[3][0])
    m = len(nonmax) - 1 - 8 - H
    lhs = 7 * (1 - Fraction(1, 1 << (H - 1)))
    require(0 not in data[6] and lhs > Fraction(5, 4) * m,
            "missing-maximality control did not fail")

    d = 4
    n = len(star(d))
    strong_star_rhs = Fraction(6, 5) + Fraction(9, 5) * d - Fraction(4, 5) * (d - 1)
    require(strong_star_rhs > n,
            "nonstar-only stronger budget wrongly accepted a star")

    return {
        "false_old_height_bound": {"R": [8, 4, 5], "n": 22, "h": h,
                                   "n_minus_2d_minus_1": 5,
                                   "Xp": 741, "opposite_X": 732},
        "maximality_is_necessary": {"R": [8, 1, 3], "n": len(nonmax),
                                   "p": 0, "Xp": data[4][0],
                                   "maximum_parent_X": max(data[4][q] for q in data[5]),
                                   "H": H, "remaining_edges": m,
                                   "strong_left": str(lhs), "charge_upper": str(Fraction(5, 4) * m)},
        "strong_nonstar_budget_excludes_star": {"d": d, "n": n,
                                                "strong_rhs": str(strong_star_rhs)},
    }


def run():
    counts = Counter()
    order_counts = {}
    for n in range(3, 6):
        cases = 0
        for sequence in product(range(n), repeat=n - 2):
            check_case(decode_prufer(n, sequence), counts)
            cases += 1
        require(cases == n ** (n - 2), "labeled control range incomplete")
        order_counts[str(n)] = cases

    fixtures = [path_tree(2)]
    fixtures += [star(d) for d in range(2, 7)]
    fixtures += [path_tree(n) for n in range(3, 10)]
    fixtures += [double_broom(3, 3, 2), branched_broom(8, 4, 5),
                 branched_broom(8, 4, 6), branched_broom(13, 6, 11)]
    fixtures += [make_tree(14, [(0, 1), (1, 2), (0, 3), (0, 4),
                               (0, 5), (0, 6), (2, 7), (7, 8),
                               (2, 9), (9, 10), (9, 11),
                               (0, 12), (12, 13)])]
    for adj in fixtures:
        check_case(adj, counts)

    grid_cases = 0
    for d, e, t in product(range(1, 13), range(1, 7), range(1, 7)):
        check_case(branched_broom(d, e, t), counts)
        grid_cases += 1
    require(grid_cases == 432, "R-grid control range incomplete")

    invalid = [(1, []), (3, [(0, 1), (1, 2), (2, 0)]),
               (4, [(0, 1), (1, 2), (2, 0)]),
               (3, [(0, 1), (1, 0)]), (2, [(0, 0)]),
               (2, [(0, 2)])]
    for n, edges in invalid:
        try:
            make_tree(n, edges)
        except ValueError:
            counts["invalid_inputs_rejected"] += 1
        else:
            raise AssertionError("invalid graph accepted")
    require(counts["invalid_inputs_rejected"] == len(invalid),
            "not all invalid controls were rejected")

    return {
        "schema": "atlas-structural-controls-v1",
        "scope": "finite implementation controls; universal proof is PROOF.md",
        "arithmetic": "Python integers and fractions.Fraction",
        "labeled_trees_by_order": order_counts,
        "boundary_fixture_cases": len(fixtures),
        "R_grid": {"d": [1, 12], "e": [1, 6], "t": [1, 6], "cases": grid_cases},
        "counts": dict(sorted(counts.items())),
        "negative_controls": negative_controls(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        help="write compact deterministic JSON to this path")
    args = parser.parse_args()
    encoded = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
