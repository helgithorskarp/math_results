#!/usr/bin/env python3
"""Independent exact audit of the circuit-zonotope illumination argument.

This checker deliberately does not import the target verifier.  It combines a
Dilworth/matching computation on the proper Boolean lattice, direct quotient
inequality checks with rational arithmetic, exact planar Minkowski-sum tests,
and an exhaustive census of labelled cactus graphs through six vertices.
"""

from __future__ import annotations

from collections import deque
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations, product
from json import dumps
from math import comb


def proper_masks(k: int) -> list[int]:
    return list(range(1, (1 << k) - 1))


def strict_subset(a: int, b: int) -> bool:
    return a != b and (a & ~b) == 0


def illuminated_masks(c: tuple[int, ...]) -> list[int]:
    k = len(c)
    out = []
    for mask in proper_masks(k):
        inside = [c[i] for i in range(k) if mask >> i & 1]
        outside = [c[i] for i in range(k) if not (mask >> i & 1)]
        if max(inside) < min(outside):
            out.append(mask)
    return out


def hopcroft_karp(nodes: list[int], edges: dict[int, list[int]]):
    """Maximum matching in the bipartite comparability graph."""
    left_match: dict[int, int] = {}
    right_match: dict[int, int] = {}
    inf = len(nodes) + 1

    while True:
        distance: dict[int, int] = {}
        queue: deque[int] = deque()
        for u in nodes:
            if u not in left_match:
                distance[u] = 0
                queue.append(u)
            else:
                distance[u] = inf
        augmenting_distance = inf
        while queue:
            u = queue.popleft()
            if distance[u] >= augmenting_distance:
                continue
            for v in edges[u]:
                predecessor = right_match.get(v)
                if predecessor is None:
                    augmenting_distance = distance[u] + 1
                elif distance[predecessor] == inf:
                    distance[predecessor] = distance[u] + 1
                    queue.append(predecessor)

        if augmenting_distance == inf:
            return left_match, right_match

        def dfs(u: int) -> bool:
            for v in edges[u]:
                predecessor = right_match.get(v)
                if predecessor is None or (
                    distance.get(predecessor, inf) == distance[u] + 1
                    and dfs(predecessor)
                ):
                    left_match[u] = v
                    right_match[v] = u
                    return True
            distance[u] = inf
            return False

        for u in nodes:
            if u not in left_match:
                dfs(u)


def matching_chain_cover(k: int) -> list[list[int]]:
    nodes = proper_masks(k)
    edges = {a: [b for b in nodes if strict_subset(a, b)] for a in nodes}
    left_match, right_match = hopcroft_karp(nodes, edges)
    starts = [a for a in nodes if a not in right_match]
    chains = []
    seen = set()
    for start in starts:
        chain = []
        current = start
        while True:
            assert current not in seen
            seen.add(current)
            chain.append(current)
            if current not in left_match:
                break
            current = left_match[current]
        chains.append(chain)
    assert seen == set(nodes)
    for chain in chains:
        assert all(strict_subset(a, b) for a, b in zip(chain, chain[1:]))
    assert len(chains) == len(nodes) - len(left_match)
    return chains


def direction_for_chain(chain: list[int], k: int) -> tuple[int, ...]:
    ordering = []
    previous = 0
    for mask in chain:
        block = mask & ~previous
        ordering.extend(i for i in range(k) if block >> i & 1)
        previous = mask
    ordering.extend(i for i in range(k) if not (previous >> i & 1))
    assert sorted(ordering) == list(range(k))
    c = [0] * k
    for rank, i in enumerate(ordering):
        c[i] = rank
    return tuple(c)


def audit_boolean_lattices():
    chain_rows = []
    for k in range(2, 10):
        chains = matching_chain_cover(k)
        expected = comb(k, k // 2)
        assert len(chains) == expected
        covered = set()
        for chain in chains:
            c = direction_for_chain(chain, k)
            lit = set(illuminated_masks(c))
            assert set(chain) <= lit
            covered.update(lit)
        assert covered == set(proper_masks(k))
        middle = [m for m in proper_masks(k) if m.bit_count() == k // 2]
        assert len(middle) == expected
        assert all(
            not strict_subset(a, b) and not strict_subset(b, a)
            for a, b in combinations(middle, 2)
        )
        chain_rows.append(
            {
                "chains": len(chains),
                "labels": len(proper_masks(k)),
                "middle_antichain": len(middle),
                "n": k,
            }
        )

    weak_rows = []
    for k in range(2, 6):
        tested = tied = max_lit = 0
        for c in product(range(-2, 3), repeat=k):
            if len(set(c)) == 1:
                assert not illuminated_masks(c)
                continue
            tested += 1
            if len(set(c)) < k:
                tied += 1
            lit = illuminated_masks(c)
            max_lit = max(max_lit, len(lit))
            assert all(
                strict_subset(a, b) or strict_subset(b, a)
                for a, b in combinations(lit, 2)
            )
        weak_rows.append(
            {
                "coefficient_vectors": tested,
                "max_labels_illuminated": max_lit,
                "n": k,
                "with_ties": tied,
            }
        )
    return chain_rows, weak_rows


def mat_vec(matrix: list[list[F]], vector: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix)


def vec_sum(vectors: list[tuple[F, ...]]) -> tuple[F, ...]:
    if not vectors:
        return ()
    return tuple(sum(v[j] for v in vectors) for j in range(len(vectors[0])))


def vec_scale(a: F, v: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(a * x for x in v)


def quotient_strict_step(
    ell: list[F], mask: int, c: tuple[int, ...], should_illuminate: bool
) -> None:
    k = len(ell)
    a = [ell[i] if mask >> i & 1 else F(0) for i in range(k)]
    active = [(i, j) for i in range(k) for j in range(k) if i != j and a[i] - a[j] == ell[i]]
    predicted_active = [
        (i, j)
        for i in range(k)
        for j in range(k)
        if (mask >> i & 1) and not (mask >> j & 1)
    ]
    assert active == predicted_active
    actual = all(c[i] - c[j] < 0 for i, j in active)
    assert actual == should_illuminate
    if not actual:
        assert any(c[i] - c[j] >= 0 for i, j in active)
        return
    bounds = []
    for i in range(k):
        for j in range(k):
            if i == j:
                continue
            slack = ell[i] - (a[i] - a[j])
            derivative = c[i] - c[j]
            if derivative > 0:
                bounds.append(slack / derivative)
    epsilon = min(bounds, default=F(1)) / 2
    assert epsilon > 0
    assert all(
        a[i] - a[j] + epsilon * (c[i] - c[j]) < ell[i]
        for i in range(k)
        for j in range(k)
        if i != j
    )


def matrix_rank(columns: list[tuple[F, ...]]) -> int:
    if not columns:
        return 0
    rows = [[columns[j][i] for j in range(len(columns))] for i in range(len(columns[0]))]
    rank = 0
    for col in range(len(columns)):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][col]
        rows[rank] = [x / scale for x in rows[rank]]
        for r in range(len(rows)):
            if r != rank and rows[r][col]:
                factor = rows[r][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return rank


def audit_normalization():
    rows = []
    literal_failures = 0
    for k in range(2, 7):
        d = k - 1
        canonical = []
        for i in range(d):
            canonical.append(tuple(F(int(i == j)) for j in range(d)))
        canonical.append(tuple(F(-1) for _ in range(d)))
        transform = [
            [F(1 if i == j else ((i + 2) * (j + 1)) % 3 - 1 if j < i else 0) for j in range(d)]
            for i in range(d)
        ]
        v = [mat_vec(transform, x) for x in canonical]
        alpha = [F((i + 2) * (1 if i % 2 == 0 else -1), (i % 3) + 1) for i in range(k)]
        g = [vec_scale(F(1, 1) / alpha[i], v[i]) for i in range(k)]
        assert all(x == 0 for x in vec_sum([vec_scale(alpha[i], g[i]) for i in range(k)]))
        h = [vec_scale(F(1 if alpha[i] > 0 else -1), g[i]) for i in range(k)]
        beta = [abs(x) for x in alpha]
        corrected_v = [vec_scale(beta[i], h[i]) for i in range(k)]
        assert corrected_v == v
        assert all(x == 0 for x in vec_sum(corrected_v))
        literal_v = [vec_scale(alpha[i], h[i]) for i in range(k)]
        if any(x != 0 for x in vec_sum(literal_v)):
            literal_failures += 1
        ell = [F(1, 1) / x for x in beta]
        assert all(vec_scale(ell[i], corrected_v[i]) == h[i] for i in range(k))
        assert matrix_rank(corrected_v) == d
        assert all(matrix_rank([corrected_v[i] for i in inds]) == len(inds) for size in range(1, k) for inds in combinations(range(k), size))

        endpoint_images = {}
        for mask in range(1 << k):
            coords = [ell[i] if mask >> i & 1 else F(0) for i in range(k)]
            point = tuple(sum(coords[i] * corrected_v[i][j] for i in range(k)) for j in range(d))
            endpoint_images.setdefault(point, []).append(mask)
            strict = all(
                coords[i] - coords[j] < ell[i]
                for i in range(k)
                for j in range(k)
                if i != j
            )
            assert strict == (mask in (0, (1 << k) - 1))
        proper_points = []
        for mask in proper_masks(k):
            coords = [ell[i] if mask >> i & 1 else F(0) for i in range(k)]
            point = tuple(sum(coords[i] * corrected_v[i][j] for i in range(k)) for j in range(d))
            proper_points.append(point)
        assert len(set(proper_points)) == (1 << k) - 2

        coefficient_tests = 0
        coefficient_source = product(range(-2, 3), repeat=k) if k <= 4 else permutations(range(k))
        for c_raw in coefficient_source:
            c = tuple(c_raw)
            if len(set(c)) == 1:
                continue
            for mask in proper_masks(k):
                predicted = mask in illuminated_masks(c)
                quotient_strict_step(ell, mask, c, predicted)
                coefficient_tests += 1
        rows.append(
            {
                "coefficient_vertex_tests": coefficient_tests,
                "corner_images": len(endpoint_images),
                "dimension": d,
                "n": k,
                "proper_vertices": len(set(proper_points)),
            }
        )
    assert literal_failures == 5
    return rows, literal_failures


def cross(a: tuple[F, F], b: tuple[F, F], c: tuple[F, F]) -> F:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def convex_hull(points: list[tuple[F, F]]) -> list[tuple[F, F]]:
    points = sorted(set(points))
    if len(points) <= 1:
        return points
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def zonotope_hull(generators: list[tuple[F, F]]) -> list[tuple[F, F]]:
    points = []
    for bits in product((0, 1), repeat=len(generators)):
        points.append(
            tuple(sum(bits[i] * generators[i][j] for i in range(len(generators))) for j in range(2))
        )
    return convex_hull(points)


def polygon_vertex_illuminated(hull: list[tuple[F, F]], index: int, w: tuple[F, F]) -> bool:
    previous = hull[index - 1]
    current = hull[index]
    following = hull[(index + 1) % len(hull)]
    incoming = (current[0] - previous[0], current[1] - previous[1])
    outgoing = (following[0] - current[0], following[1] - current[1])
    return incoming[0] * w[1] - incoming[1] * w[0] > 0 and outgoing[0] * w[1] - outgoing[1] * w[0] > 0


def audit_summand_monotonicity():
    q_generators = [(F(1), F(0)), (F(0), F(1)), (F(-1), F(-1))]
    coefficient_directions = [(1, 2, 3), (3, 1, 2), (2, 3, 1)]
    directions = [
        tuple(sum(c[i] * q_generators[i][j] for i in range(3)) for j in range(2))
        for c in coefficient_directions
    ]
    summands = [
        [],
        [(F(2), F(1))],
        [(F(2), F(1)), (F(-1), F(3))],
        [(F(2), F(0)), (F(0), F(3)), (F(1), F(1))],
    ]
    rows = []
    for extra in summands:
        hull = zonotope_hull(q_generators + extra)
        assert all(any(polygon_vertex_illuminated(hull, i, w) for w in directions) for i in range(len(hull)))
        rows.append(
            {
                "directions": len(directions),
                "extra_segments": len(extra),
                "generators": len(q_generators) + len(extra),
                "vertices": len(hull),
            }
        )
    return rows


def connected(n: int, edges: set[tuple[int, int]]) -> bool:
    seen = {0}
    stack = [0]
    adjacency = [[] for _ in range(n)]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    while stack:
        u = stack.pop()
        for v in adjacency[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == n


def alternate_paths(
    n: int, edges: set[tuple[int, int]], forbidden: tuple[int, int]
) -> list[list[tuple[int, int]]]:
    source, target = forbidden
    adjacency = [[] for _ in range(n)]
    for edge in edges:
        if edge == forbidden:
            continue
        u, v = edge
        adjacency[u].append(v)
        adjacency[v].append(u)
    found: list[list[tuple[int, int]]] = []

    def dfs(u: int, seen: set[int], path: list[tuple[int, int]]) -> None:
        if len(found) >= 2:
            return
        if u == target:
            found.append(path[:])
            return
        for v in adjacency[u]:
            if v not in seen:
                edge = (u, v) if u < v else (v, u)
                dfs(v, seen | {v}, path + [edge])

    dfs(source, {source}, [])
    return found


def cactus_data(n: int, edges: set[tuple[int, int]]):
    bridges = []
    cycles = set()
    for edge in edges:
        paths = alternate_paths(n, edges, edge)
        if len(paths) >= 2:
            return None
        if not paths:
            bridges.append(edge)
        else:
            cycles.add(frozenset(paths[0] + [edge]))
    cycle_sets = list(cycles)
    assert all(sum(edge in cycle for cycle in cycle_sets) <= 1 for edge in edges)
    return bridges, cycle_sets


def forest_rank(n: int, edges: set[tuple[int, int]]) -> int:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    rank = 0
    for u, v in edges:
        a, b = find(u), find(v)
        if a != b:
            parent[a] = b
            rank += 1
    return rank


def incidence_columns(n: int, edges: list[tuple[int, int]]) -> list[tuple[F, ...]]:
    columns = []
    for u, v in edges:
        column = [F(0) for _ in range(n - 1)]
        if u < n - 1:
            column[u] += 1
        if v < n - 1:
            column[v] -= 1
        columns.append(tuple(column))
    return columns


def audit_cacti():
    rows = []
    for n in range(2, 7):
        possible = list(combinations(range(n), 2))
        connected_count = cactus_count = tree_count = cyclic_count = max_cycles = 0
        for mask in range(1 << len(possible)):
            if mask.bit_count() < n - 1:
                continue
            edges = {possible[i] for i in range(len(possible)) if mask >> i & 1}
            if not connected(n, edges):
                continue
            connected_count += 1
            data = cactus_data(n, edges)
            if data is None:
                continue
            cactus_count += 1
            bridges, cycles = data
            if cycles:
                cyclic_count += 1
            else:
                tree_count += 1
            max_cycles = max(max_cycles, len(cycles))
            assert len(edges) == len(bridges) + sum(len(cycle) for cycle in cycles)
            assert n - 1 == len(bridges) + sum(len(cycle) - 1 for cycle in cycles)
            selected = set(bridges)
            for cycle in cycles:
                chosen_basis = set(cycle) - {min(cycle)}
                assert forest_rank(n, chosen_basis) == len(cycle) - 1
                selected.update(chosen_basis)
            assert len(selected) == n - 1
            assert connected(n, selected)
            assert forest_rank(n, selected) == n - 1
            assert matrix_rank(incidence_columns(n, list(selected))) == n - 1
        rows.append(
            {
                "cacti": cactus_count,
                "connected_graphs": connected_count,
                "cyclic_cacti": cyclic_count,
                "max_cycles": max_cycles,
                "n": n,
                "trees": tree_count,
            }
        )

    k24_a = {(0, 2), (1, 2), (1, 3), (0, 3)}
    k24_b = {(0, 4), (1, 4), (1, 5), (0, 5)}
    negative_ranks = [
        matrix_rank(incidence_columns(6, sorted(k24_a))),
        matrix_rank(incidence_columns(6, sorted(k24_b))),
        matrix_rank(incidence_columns(6, sorted(k24_a | k24_b))),
    ]
    assert negative_ranks == [3, 3, 5]
    return rows, negative_ranks


def embedded_circuit(k: int, offset: int, dimension: int) -> list[tuple[F, ...]]:
    out = []
    for i in range(k - 1):
        v = [F(0)] * dimension
        v[offset + i] = 1
        out.append(tuple(v))
    v = [F(0)] * dimension
    for i in range(k - 1):
        v[offset + i] = -1
    out.append(tuple(v))
    return out


def extend_basis(columns: list[tuple[F, ...]], initial: list[int], dimension: int) -> list[int]:
    chosen = initial[:]
    rank = matrix_rank([columns[i] for i in chosen])
    for i in range(len(columns)):
        if i in chosen:
            continue
        trial = matrix_rank([columns[j] for j in chosen + [i]])
        if trial > rank:
            chosen.append(i)
            rank = trial
        if rank == dimension:
            break
    assert rank == dimension
    return chosen


def audit_basis_extension():
    rows = []

    dimension = 7
    first = embedded_circuit(3, 0, dimension)
    second = embedded_circuit(4, 2, dimension)
    e5 = tuple(F(int(i == 5)) for i in range(dimension))
    e6 = tuple(F(int(i == 6)) for i in range(dimension))
    mixed = tuple(F(i + 1) for i in range(dimension))
    columns = first + second + [mixed, e6, e5]
    initial = [0, 1, 3, 4, 5]
    chosen = extend_basis(columns, initial, dimension)
    assert len(chosen) - len(initial) == 2
    rows.append({"circuits": [3, 4], "dimension": dimension, "extension_generators": 2})

    dimension = 4
    unit = [tuple(F(int(i == j)) for i in range(dimension)) for j in range(dimension)]
    columns = [tuple(F(1) for _ in range(dimension))] + unit
    chosen = extend_basis(columns, [], dimension)
    assert len(chosen) == 4
    rows.append({"circuits": [], "dimension": dimension, "extension_generators": 4})

    dimension = 4
    columns = embedded_circuit(5, 0, dimension)
    chosen = extend_basis(columns, [0, 1, 2, 3], dimension)
    assert len(chosen) == 4
    rows.append({"circuits": [5], "dimension": dimension, "extension_generators": 0})
    return rows


def audit_product_conflicts():
    cases = [([], 3), ([2], 0), ([3, 4], 1), ([2, 5], 2)]
    rows = []
    for circuit_sizes, segment_count in cases:
        factor_values = [
            [m for m in proper_masks(k) if m.bit_count() == k // 2]
            for k in circuit_sizes
        ] + [[0, 1] for _ in range(segment_count)]
        witnesses = list(product(*factor_values))
        expected = (2**segment_count)
        for k in circuit_sizes:
            expected *= comb(k, k // 2)
        assert len(witnesses) == expected
        for a, b in combinations(witnesses, 2):
            conflicting = False
            for index, (x, y) in enumerate(zip(a, b)):
                if x == y:
                    continue
                if index < len(circuit_sizes):
                    conflicting = not strict_subset(x, y) and not strict_subset(y, x)
                else:
                    conflicting = True
                if conflicting:
                    break
            assert conflicting
        rows.append(
            {
                "circuits": circuit_sizes,
                "segments": segment_count,
                "pairwise_conflicting_witnesses": len(witnesses),
            }
        )
    return rows


def main() -> None:
    chain_rows, weak_rows = audit_boolean_lattices()
    normalization_rows, literal_failures = audit_normalization()
    evidence = {
        "basis_extensions": audit_basis_extension(),
        "boolean_chain_covers": chain_rows,
        "cactus_census": None,
        "normalization": normalization_rows,
        "normalization_literal_old_coefficient_failures": literal_failures,
        "product_lower_certificates": audit_product_conflicts(),
        "summand_polygons": audit_summand_monotonicity(),
        "weak_order_directions": weak_rows,
    }
    cactus_rows, negative_ranks = audit_cacti()
    evidence["cactus_census"] = cactus_rows
    evidence["edge_disjoint_nondirect_ranks"] = negative_ranks
    payload = dumps(evidence, sort_keys=True, separators=(",", ":")).encode()
    result = {
        "evidence": evidence,
        "payload_sha256": sha256(payload).hexdigest(),
        "status": "VERIFIED",
    }
    print(dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
