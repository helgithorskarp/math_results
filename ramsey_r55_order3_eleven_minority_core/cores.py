#!/usr/bin/env python3
"""Exact normalizer cover of three internally red moving triangles."""
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json

PAIRS = tuple(combinations(range(3), 2))
NORMAL = ((0, 0, 0), (1, 0, 0), (1, 1, 0))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def transform(bits, perm, shift, sign):
    """New vertex (i,s) is old vertex (perm[i], sign*s+shift[i])."""
    def word(i, j, d):
        if i > j:
            i, j, d = j, i, -d
        return bits[3*PAIRS.index((i, j)) + d % 3]
    return tuple(word(perm[i], perm[j], sign*d+shift[j]-shift[i])
                 for i, j in PAIRS for d in range(3))


def normalized(bits):
    return bits[:3] in NORMAL and bits[3:6] in NORMAL and sum(bits[:3]) <= sum(bits[3:6])


def invariant(bits):
    words = [bits[q:q+3] for q in (0, 3, 6)]
    weights = tuple(sorted(map(sum, words)))
    if 0 in weights:
        return weights, None
    # Distinguished phase: unique 1 for weight one, unique 0 for weight two.
    phase = [w.index(1 if sum(w) == 1 else 0) for w in words]
    return weights, int((phase[0]+phase[2]-phase[1]) % 3 != 0)


def cover():
    words = [w for w in product((0, 1), repeat=3) if sum(w) < 3]
    domain = set(a+b+c for a, b, c in product(words, repeat=3))
    maps = list(product(permutations(range(3)), product(range(3), repeat=3), (1, -1)))
    left = set(domain)
    rows = []
    while left:
        seed = min(left)
        orbit = {transform(seed, *m) for m in maps}
        require(orbit <= left, 'overlap or domain failure')
        choices = sorted(x for x in orbit if normalized(x))
        require(bool(choices), 'missing normalized representative')
        rep = choices[0]
        require({invariant(x) for x in orbit} == {invariant(rep)}, 'invariant failure')
        rows.append(dict(bits=''.join(map(str, rep)), labeled=len(orbit),
                         normalized=len(choices), invariant=invariant(rep),
                         members=sorted(''.join(map(str, x)) for x in orbit)))
        left -= orbit
    rows.sort(key=lambda row: row['bits'])
    for index, row in enumerate(rows):
        row['index'] = index
    require(len(rows) == 14 and len(domain) == 343, 'unexpected cover')
    require(len({str(row['invariant']) for row in rows}) == 14, 'invariant not complete')
    return dict(format='r55-k11-r3-core-cover-v1', labeled_cores=343,
                normalizer_maps=len(maps), normalized_cores=sum(r['normalized'] for r in rows), cases=rows)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    data = cover()
    a.output.write_text(json.dumps(data, indent=2, sort_keys=True)+'\n')
    print('PASS 343 labeled cores, 14 classes, 42 normalized cores')
