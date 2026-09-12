#!/usr/bin/env python3
"""Generate finite obstruction witnesses. Python 3.11+, standard library only."""
import itertools as it
import json
import sys

FORBIDDEN = [
    [(0, 1), (1, 2), (2, 3), (4, 0), (4, 1), (4, 2), (4, 3)],
    [(0, 1), (1, 2), (2, 0), (0, 3), (1, 4)],
]
PRISM = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5),
         (0, 3), (1, 4), (2, 5)]
PAIRS = list(it.combinations(range(5), 2))


def rows(n, edges):
    a = [0] * n
    for u, v in edges:
        a[u] |= 1 << v
        a[v] |= 1 << u
    return a


def code(a, vertices):
    return sum(1 << i for i, (u, v) in enumerate(it.combinations(vertices, 2))
               if (a[u] >> v) & 1)


BAD = {}
for kind, edges in enumerate(FORBIDDEN):
    a = rows(5, edges)
    for p in it.permutations(range(5)):
        BAD[code(a, p)] = kind


def witness(a):
    # Entry 2*j+kind names a five-subset in lexicographic order and its type.
    for j, vertices in enumerate(it.combinations(range(len(a)), 5)):
        kind = BAD.get(code(a, vertices))
        if kind is not None:
            return 2 * j + kind
    return None


def generate():
    majority = []
    for edges in FORBIDDEN:
        f = rows(5, edges)
        for apex in range(5):
            outside = [v for v in range(5) if v != apex]
            base = [(i, j) for i, j in it.combinations(range(4), 2)
                    if (f[outside[i]] >> outside[j]) & 1]
            base += [(4, 5), (4, 6), (5, 6)]
            options = [[s for s in range(8)
                        if (s.bit_count() >= 2) == bool((f[apex] >> v) & 1)]
                       for v in outside]
            certificates = []
            for masks in it.product(*options):
                edges7 = base + [(v, 4 + j) for v, s in enumerate(masks)
                                 for j in range(3) if (s >> j) & 1]
                w = witness(rows(7, edges7))
                if w is None:
                    raise RuntimeError(("majority counterexample", apex, masks))
                certificates.append(w)
            majority.append(bytes(certificates).hex())
    attachment = []
    for s in range(64):
        w = witness(rows(7, PRISM + [(6, j) for j in range(6) if (s >> j) & 1]))
        attachment.append(255 if w is None else w)
    isolation = []
    for s in range(1, 64):
        w = witness(rows(8, PRISM + [(6, 7)] +
                         [(7, j) for j in range(6) if (s >> j) & 1]))
        if w is None:
            raise RuntimeError(("isolation counterexample", s))
        isolation.append(w)
    return {"format": "prism-majority-v1", "majority": majority,
            "attachment": bytes(attachment).hex(),
            "isolation": bytes(isolation).hex()}


if __name__ == "__main__":
    json.dump(generate(), sys.stdout, indent=2, sort_keys=True)
    print()
