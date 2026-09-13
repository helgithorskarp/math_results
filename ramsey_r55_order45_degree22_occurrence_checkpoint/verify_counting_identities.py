#!/usr/bin/env python3
"""Independent exact checks for the order-22 root-cut counting formulas."""

from itertools import combinations
from math import comb
import random


def check(seed: int) -> None:
    rng = random.Random(seed)
    h = tuple(range(22))
    x = tuple(range(22, 44))
    root = 44
    edge = [[False] * 45 for _ in range(45)]
    for u, v in combinations(range(44), 2):
        edge[u][v] = edge[v][u] = bool(rng.getrandbits(1))
    for u in h:
        edge[root][u] = edge[u][root] = True

    eh = sum(edge[u][v] for u, v in combinations(h, 2))
    ey = sum(edge[u][v] for u, v in combinations(x, 2))
    eq = comb(22, 2) - ey
    j = {u: sum(edge[u][v] for v in h) for u in h}
    c = {u: sum(edge[u][v] for v in x) for u in h}
    y = {u: sum(edge[u][v] for v in x) for u in x}
    k = {u: sum(edge[u][v] for v in h) for u in x}
    q = {u: 21-y[u] for u in x}

    c_left = sum(comb(c[u], 2) for u in h)
    c_right_term = sum(q[u] * k[u] for u in x)
    c_triples = sum(
        (edge[u][v] and edge[u][w])
        - (not edge[v][w]) * (edge[u][v] + edge[u][w])
        for u in h for v, w in combinations(x, 2)
    ) + 27 * eq
    assert c_triples == c_left - c_right_term + 27 * eq

    r_left = sum(comb(k[u], 2) for u in x)
    r_tail = sum(c[u] * (21-j[u]) for u in h)
    r_triples = sum(
        (edge[w][u] and edge[w][v])
        - (not edge[u][v]) * (edge[w][u] + edge[w][v])
        for u, v in combinations(h, 2) for w in x
    ) - 17 * eh
    assert r_triples == r_left - r_tail - 17 * eh

    vertices = tuple(range(45))
    hn_direct = hq_direct = xn_direct = xq_direct = 0
    for u in h + x:
        neighbours = [v for v in vertices if v != u and edge[u][v]]
        nonneighbours = [v for v in vertices if v != u and not edge[u][v]]
        neighbour_edges = sum(edge[v][w] for v, w in combinations(neighbours, 2))
        nonneighbour_nonedges = sum(not edge[v][w] for v, w in combinations(nonneighbours, 2))
        if u in h:
            hn_direct += neighbour_edges
            hq_direct += nonneighbour_nonedges
        else:
            xn_direct += neighbour_edges
            xq_direct += nonneighbour_nonedges

    hn_triples = 2 * eh
    hq_triples = 0
    xn_triples = 0
    xq_triples = 2 * eq
    for triple in combinations(range(44), 3):
        a = sum(u in h for u in triple)
        edges = sum(edge[u][v] for u, v in combinations(triple, 2))
        if edges == 3:
            hn_triples += a
            xn_triples += 3-a
        if edges == 0:
            hq_triples += a
            xq_triples += 3-a
    assert (hn_direct, hq_direct, xn_direct, xq_direct) == (
        hn_triples, hq_triples, xn_triples, xq_triples
    )


if __name__ == "__main__":
    for test_seed in range(100):
        check(test_seed)
    print("100 exact randomized counting checks passed")
