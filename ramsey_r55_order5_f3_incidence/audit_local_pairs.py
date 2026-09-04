#!/usr/bin/env python3
"""Directly test every five-set of every local 13-vertex candidate.

No constraints, edge generators, or clique routines are imported from the
incidence enumerators. The output is a scope check: both residual patterns
pass the two-moving-cycle extension test for every internal orientation.
"""
from itertools import combinations, product
from hashlib import sha256
import json

PAIRS = tuple(combinations(range(13), 2))
EDGE = {pair: 1 << i for i, pair in enumerate(PAIRS)}
FIVES = tuple(sum(EDGE[pair] for pair in combinations(vertices, 2))
              for vertices in combinations(range(13), 5))


def edge(u, v):
    return EDGE[tuple(sorted((u, v)))]


def graph(a, b, s, t, word):
    red = edge(0, 1)  # unique red fixed edge; 0--2 and 1--2 are blue
    for start, column, step in ((3, a, s), (8, b, t)):
        for u, v in combinations(range(5), 2):
            if (v-u) % 5 in (step, 5-step):
                red |= edge(start+u, start+v)
        for fixed in range(3):
            if column & (1 << fixed):
                for vertex in range(start, start+5):
                    red |= edge(fixed, vertex)
    for u, v in product(range(5), repeat=2):
        if word & (1 << ((v-u) % 5)):
            red |= edge(3+u, 8+v)
    return red


def allowed(red):
    return all((red & five) not in (0, five) for five in FIVES)


def main():
    assert not allowed(0)
    assert not allowed((1 << 78)-1)
    permutation = [0, 1, 2, 4, 5, 6, 7, 3, 9, 10, 11, 12, 8]
    rotated_edges = [(edge(u, v), edge(permutation[u], permutation[v]))
                     for u, v in PAIRS]
    records, sizes = [], []
    tested = 0
    for h in (0, 1):
        counts = (1, 1, 1, 1, h, 2-h, 2-h, h)
        columns = [i for i, n in enumerate(counts) for _ in range(n)]
        for i, j in combinations(range(8), 2):
            for s, t in product((1, 2), repeat=2):
                words = []
                for word in range(32):
                    tested += 1
                    red = graph(columns[i], columns[j], s, t, word)
                    assert all(bool(red & a) == bool(red & b)
                               for a, b in rotated_edges)
                    if allowed(red):
                        words.append(word)
                assert words, (h, i, j, s, t)
                sizes.append(len(words))
                records.append([h, i, j, s, t, words])
    encoded = json.dumps(records, separators=(",", ":")).encode("ascii")
    print(f"LOCAL_AUDIT templates={len(records)} colorings={tested} "
          f"five_sets_per_coloring={len(FIVES)} rotation_checks={tested}")
    print(f"LOCAL_DOMAINS min={min(sizes)} max={max(sizes)} "
          f"sha256={sha256(encoded).hexdigest()}")
    print("PASS: both patterns admit every local pair orientation; "
          "global extension remains open")


if __name__ == "__main__":
    main()
