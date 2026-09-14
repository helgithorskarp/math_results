#!/usr/bin/env python3
"""Cross-check image edges by a modular sieve and generic radical products.

Coordinate loading, certified side selection and collision merging are shared
with verify.py. Distance multiplication and edge construction are separate.
This is same-author validation, not independent review.
"""
from hashlib import sha256
from itertools import combinations
import json
from math import gcd
import verify

P = 1321
ROOTS = (1, 321, 416, 321*416, 501, 321*501, 416*501, 321*416*501)
RAD = (1, 3, 5, 15, 11, 33, 55, 165)


def exact_unit(a, b):
    out = {r: 0 for r in RAD}
    for axis in range(2):
        delta = [x-y for x, y in zip(a[axis], b[axis], strict=True)]
        for i, r in enumerate(RAD):
            for j, s in enumerate(RAD):
                common = gcd(r, s)
                out[r*s//(common*common)] += delta[i]*delta[j]*common
    return out[1] == 288**2 and all(out[r] == 0 for r in RAD[1:])


def main():
    verify.require(all((r*r-d) % P == 0 for r, d in zip(ROOTS, RAD, strict=True)),
                   'modular roots')
    _, parent = verify.load_parent()
    points, _, _ = verify.fold(parent)
    mapped = [tuple(sum(a*b for a, b in zip(axis, ROOTS, strict=True)) % P
                    for axis in p) for p in points]
    edges, rejected, decided = [], 0, 0
    for a, b in combinations(range(len(points)), 2):
        if (sum((x-y)**2 for x, y in zip(mapped[a], mapped[b], strict=True))-288**2) % P:
            rejected += 1
            continue
        decided += 1
        if exact_unit(points[a], points[b]):
            edges.append((a, b))
    verify.require(edges == verify.unit_edges(points), 'complete edge disagreement')
    word = json.loads((verify.HERE/'certificate.json').read_text())['four_colouring']
    verify.check_word(word, len(points), edges)
    result = dict(all_checks=True, modular_nonunit_exclusions=rejected,
                  exact_polynomial_decisions=decided, unit_edges=len(edges),
                  every_edge_matches=True, shared_coordinate_and_fold_code=True,
                  edge_sha256=sha256(''.join(f'{a} {b}\n' for a, b in edges).encode()).hexdigest())
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
