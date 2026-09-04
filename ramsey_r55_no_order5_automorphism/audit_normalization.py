#!/usr/bin/env python3
"""Audit the h=1 relabeling on explicit graphs, without importing the encoder.

These sampled arbitrary invariant colorings are not Ramsey witnesses. The
audit verifies the normalization bridge independently of solving a formula.
The proof that the bridge covers every coloring is in PROOF.md.
"""
from itertools import combinations, product
from random import Random


def matrix(internals, words):
    graph = [[False] * 43 for _ in range(43)]

    def set_edge(a, b, value):
        graph[a][b] = graph[b][a] = bool(value)

    set_edge(0, 1, 1)
    for c in range(8):
        for f in range(3):
            for r in range(5):
                set_edge(f, 3+5*c+r, c & (1 << f))
        for r, s in combinations(range(5), 2):
            step = 1 if internals[c] else 2
            set_edge(3+5*c+r, 3+5*c+s, (s-r) in (step, 5-step))
    for (a, b), word in words.items():
        for r, s in product(range(5), repeat=2):
            set_edge(3+5*a+r, 3+5*b+s, word[(s-r) % 5])
    return graph


def relabel(graph, permutation):
    assert sorted(permutation) == list(range(43))
    return [[graph[permutation[a]][permutation[b]] for b in range(43)]
            for a in range(43)]


def main():
    rng = Random(430508)
    cases = 256
    for mask in range(cases):
        internal = tuple((mask >> i) & 1 for i in range(8))
        words = {pair: tuple(rng.randrange(2) for _ in range(5))
                 for pair in combinations(range(8), 2)}
        original = matrix(internal, words)
        perm1 = list(range(43))
        if not internal[0]:
            for c, r in product(range(8), range(5)):
                perm1[3+5*c+r] = 3+5*c+(2*r) % 5
        first = relabel(original, perm1)
        assert first[3][4]
        perm2 = list(range(43))
        for c in range(1, 8):
            word = tuple(first[3][3+5*c+r] for r in range(5))
            shift = min(range(5), key=lambda s: word[s:]+word[:s])
            for r in range(5):
                perm2[3+5*c+r] = 3+5*c+(r+shift) % 5
        normalized = relabel(first, perm2)
        composed = [perm1[perm2[v]] for v in range(43)]
        assert normalized == relabel(original, composed)
        assert normalized[3][4]
        for c in range(1, 8):
            word = tuple(normalized[3][3+5*c+r] for r in range(5))
            assert word == min(word[s:]+word[:s] for s in range(5))
        for c, f, r in product(range(8), range(3), range(5)):
            assert normalized[f][3+5*c+r] == bool(c & (1 << f))
        rotation = list(range(3)) + [3+5*c+(r+1) % 5
                                    for c, r in product(range(8), range(5))]
        assert normalized == relabel(normalized, rotation)
        assert sum(map(sum, normalized)) == sum(map(sum, original))
    print(f"NORMALIZATION_AUDIT colorings={cases} "
          "all_internal_profiles=256 checked_edges_per_coloring=903 PASS")


if __name__ == "__main__":
    main()
