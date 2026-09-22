#!/usr/bin/env python3
"""Deterministically generate TORSION.json; verify.py checks its chain identities directly.

Only combinatorial construction is done here. The proof and exact direct
chain checks are in PROOF.md and verify.py. CPython 3.11+, standard library.
"""
from collections import defaultdict
from itertools import combinations, permutations
from pathlib import Path
import json

FACETS = [tuple(map(int, s)) for s in
          '012 013 024 035 045 125 134 145 234 235'.split()]


def add(out, face, value):
    inversions = sum(face[i] > face[j] for i in range(len(face))
                     for j in range(i + 1, len(face)))
    out[tuple(sorted(face))] += value * (-1) ** inversions


def faces_of(face):
    for k in range(1, len(face) + 1):
        yield from combinations(face, k)


def differential(chain):
    out = defaultdict(int)
    for face, a in chain.items():
        for i in range(len(face)):
            out[face[:i] + face[i + 1:]] += a * (-1) ** i
    return {f: a for f, a in out.items() if a}


def main():
    faces = sorted({s for f in FACETS for s in faces_of(f)}, key=lambda f: (len(f), f))
    index = {f: i for i, f in enumerate(faces)}
    base_edges = list(combinations(range(6), 2))
    c = dict.fromkeys(FACETS, 1)
    dc = differential(c)
    if any(a % 2 for a in dc.values()):
        raise ValueError('base chain boundary is not even')
    a = {e: value // 2 for e, value in dc.items()}

    # The lexicographically first bit-mask cocycle detecting the Bockstein.
    for mask in range(1 << len(base_edges)):
        beta = {e: (mask >> i) & 1 for i, e in enumerate(base_edges)}
        if all(sum(value * beta[e] for e, value in differential({f: 1}).items()) % 2 == 0
               for f in FACETS) and sum(value * beta[e] for e, value in a.items()) % 2 == 1:
            break
    else:
        raise ValueError('no detecting cocycle found')

    def subdivide(chain):
        out = defaultdict(int)
        for face, value in chain.items():
            for perm in permutations(face):
                sign = (-1) ** sum(perm[i] > perm[j] for i in range(len(perm))
                                  for j in range(i + 1, len(perm)))
                flag = tuple(index[tuple(sorted(perm[:j + 1]))] for j in range(len(perm)))
                add(out, flag, value * sign)
        return {f: value for f, value in out.items() if value}

    ca, aa = subdivide(c), subdivide(a)
    u, v = len(faces), len(faces) + 1
    z, w = defaultdict(int), defaultdict(int)
    for face, value in aa.items():
        add(z, (u,) + face, value)
        add(z, (v,) + face, -value)
    for face, value in ca.items():
        add(w, (v,) + face, value)
        add(w, (u,) + face, -value)
    eta = {}
    for i, f in enumerate(faces):
        for j, g in enumerate(faces):
            if i < j and set(f) < set(g):
                r, s = min(f), min(g)
                if r != s and beta[tuple(sorted((r, s)))]:
                    eta[(i, j, u)] = 1

    def entries(chain):
        return [[list(f), value] for f, value in sorted(chain.items()) if value]

    result = {'description': 'Integral cycle z, dw=2z, and mod-2 cocycle eta(z)=1 in sd(P)*S0.',
              'labels': 'Nonempty faces of P sorted by size then lexicographically; apices 31 and 32.',
              'cycle_z': entries(z), 'chain_w': entries(w),
              'cocycle_eta_mod2': entries(eta)}
    destination = Path(__file__).resolve().parent / 'TORSION.json'
    destination.write_text(json.dumps(result, separators=(',', ':'), sort_keys=True) + '\n')
    print('Wrote TORSION.json; run verify.py to validate every claim about it.')


if __name__ == '__main__':
    main()
