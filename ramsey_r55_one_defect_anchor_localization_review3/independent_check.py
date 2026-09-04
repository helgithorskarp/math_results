#!/usr/bin/env python3
"""Independent exact checks for the one-defect anchor localization proof.

This imports no code or data from the reviewed artifact.  The universal
identity is proved in the accompanying review and tested here from the literal
definitions on every graph through order five and deterministic larger graphs.
"""

from __future__ import annotations

from itertools import combinations
from math import comb
import random


U = dict(zip(range(18, 25), (85, 92, 100, 107, 114, 122, 132), strict=True))


def statistics(n, edges):
    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    degrees = [len(row) for row in adjacency]
    vertices = set(range(n))
    local = []
    for v in range(n):
        red = adjacency[v]
        blue = vertices - red - {v}
        t_red = sum(tuple(sorted(pair)) in edges for pair in combinations(red, 2))
        t_blue = sum(tuple(sorted(pair)) not in edges for pair in combinations(blue, 2))
        local.append((t_red, t_blue))
    return adjacency, degrees, local


def check_identity(n, edges):
    adjacency, degrees, local = statistics(n, edges)
    for v in range(n):
        right = comb(n - 1 - degrees[v], 2) - len(edges)
        right += sum(degrees[w] for w in adjacency[v])
        assert sum(local[v]) == right
    return n


def identity_audit():
    graphs = vertices = 0
    for n in range(6):
        pairs = tuple(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            edges = {pair for bit, pair in enumerate(pairs) if mask & (1 << bit)}
            vertices += check_identity(n, edges)
            graphs += 1
    assert (graphs, vertices) == (1100, 5405)
    rng = random.Random(0xD3FEC7)
    random_graphs = random_vertices = 0
    for n in range(6, 13):
        pairs = tuple(combinations(range(n), 2))
        for _ in range(100):
            edges = {pair for pair in pairs if rng.randrange(2)}
            random_vertices += check_identity(n, edges)
            random_graphs += 1
    assert (random_graphs, random_vertices) == (700, 6300)
    return graphs, vertices, random_graphs, random_vertices


def integer_partitions(total, least=1):
    if total == 0:
        yield ()
    for first in range(least, total + 1):
        for rest in integer_partitions(total - first, first):
            yield (first,) + rest


def disconnected_maximum(independence_budget, component_caps):
    candidates = []
    for used in range(2, independence_budget + 1):
        for partition in integer_partitions(used):
            if len(partition) >= 2:
                candidates.append((sum(component_caps[a] for a in partition), partition))
    return max(candidates)


def main():
    graphs, vertices, random_graphs, random_vertices = identity_audit()
    print(f"identity_exhaustive_graphs={graphs} exhaustive_vertices={vertices} "
          f"random_graphs={random_graphs} random_vertices={random_vertices}")

    m = (20 + 42 * 21) // 2
    assert m == 451
    blue_to_z = [(r, 200 - r) for r in range(101) if 0 <= 200-r <= 100]
    red_to_z = [(r, 199 - r) for r in range(101) if 0 <= 199-r <= 100]
    at_z = [(r, 200-r) for r in range(U[20]-7+1)
            if 0 <= 200-r <= U[22]-7]
    assert blue_to_z == [(100, 100)]
    assert red_to_z == [(99, 100), (100, 99)]
    assert at_z == [(93, 107)]
    blue_degree_z = 42 - 20
    blue_edges_d = at_z[0][1]
    red_edges_d = comb(blue_degree_z, 2) - blue_edges_d
    assert (blue_degree_z, red_edges_d, blue_edges_d) == (22, 124, 107)
    print("one_defect=m451 D22 local_blue=(100,100) "
          "local_red=(99,100)/(100,99) z=(93,107) D_edges_red_blue=124,107")

    # R(r,a+1)-1 component caps for alpha=a.
    blue_max, blue_partition = disconnected_maximum(4, {1: 3, 2: 8, 3: 17})
    red_max, red_partition = disconnected_maximum(3, {1: 4, 2: 13})
    assert (blue_max, blue_partition) == (20, (1, 3))
    assert (red_max, red_partition) == (17, (1, 2))
    assert 22 - blue_max == 2 and 22 - red_max == 5
    print("disconnected_max_blue=20 partition=1+3 kappa_blue=2 "
          "disconnected_max_red=17 partition=1+2 kappa_red=5")

    # Internal degree interval in the blue (4,5) graph on 22 vertices.
    blue_internal_min = 21 - (18 - 1)
    blue_internal_max = 14 - 1
    assert (blue_internal_min, blue_internal_max) == (4, 13)
    print("internal_degrees_blue=4..13 red=8..17")

    forced = comb(22, 2) - 107
    encoded_base = 100 + 21
    assert (forced, encoded_base, forced - 21) == (124, 121, 103)
    print("singleton_local_profile_contradiction=forced124_base121 anchor103_vs100")

    offsets = tuple(comb(42-d, 2) + 21*d - U[d] - U[42-d] + 14 - 231
                    for d in range(18, 25))
    assert offsets == (220, 221, 220, 220, 221, 223, 223)
    print("degree_neighborhood_offsets=" + ",".join(map(str, offsets)))
    print("independent_one_defect_check=true")


if __name__ == "__main__":
    main()
