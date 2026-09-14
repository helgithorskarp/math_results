#!/usr/bin/env python3
"""Separate distance/group/connectivity audit; source coordinate loading is shared."""
from collections import defaultdict
from hashlib import sha256
from itertools import combinations
import json
from math import gcd
import verify as v

RAD = (1, 3, 5, 15, 11, 33, 55, 165)
ROOTS = (1, 321, 416, 321*416, 501, 321*501, 416*501, 321*416*501)
PRIME = 1321


def exact_unit(p, q):
    out = {r: 0 for r in RAD}
    for a, b in zip(p, q, strict=True):
        d = [x-y for x, y in zip(a, b, strict=True)]
        for i, r in enumerate(RAD):
            for j, s in enumerate(RAD):
                g = gcd(r, s)
                out[r*s//g**2] += d[i]*d[j]*g
    return out[1] == 288**2 and all(out[r] == 0 for r in RAD[1:])


def connected(n, edges):
    parent = list(range(n))
    def root(x):
        while x != parent[x]:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in edges:
        parent[root(a)] = root(b)
    return len({root(x) for x in range(n)}) == 1


def main():
    v.require(all((x*x-r) % PRIME == 0 for x, r in zip(ROOTS, RAD, strict=True)), 'roots')
    points = v.load_points()
    residues = [tuple(sum(x*y for x, y in zip(axis, ROOTS, strict=True)) % PRIME
                      for axis in point) for point in points]
    edges, groups = [], defaultdict(list)
    rejected = tested = 0
    for a, b in combinations(range(len(points)), 2):
        if (sum((x-y)**2 for x, y in zip(residues[a], residues[b], strict=True))-288**2) % PRIME:
            rejected += 1
            continue
        tested += 1
        if not exact_unit(points[a], points[b]):
            continue
        edges.append((a, b))
        # Opposite canonical sign to the primary implementation.
        d = tuple(y-x for pa, pb in zip(points[a], points[b], strict=True)
                  for x, y in zip(pa, pb, strict=True))
        groups[min(d, tuple(-x for x in d))].append((a, b))
    primary_edges, primary_groups = v.geometry(points)
    v.require(edges == primary_edges, 'complete physical edge mismatch')
    blocks = [groups[d] for d in sorted(groups)]
    v.require({tuple(g) for g in blocks} == {tuple(g) for g in primary_groups}, 'direction partition')
    count = 0
    for i, j in combinations(range(len(blocks)), 2):
        retained = [e for k, g in enumerate(blocks) if k not in (i, j) for e in g]
        v.require(connected(len(points), retained), ('DSU disconnected', i, j))
        count += 1
    print(json.dumps(dict(all_checks=True, complete_edge_and_partition_agreement=True,
                          independent_dsu_pair_tests=count, modular_nonunit_exclusions=rejected,
                          exact_polynomial_decisions=tested, shared_coordinate_loader=True,
                          source_edge_sha256=sha256(''.join(f'{a} {b}\n' for a, b in edges).encode()).hexdigest()),
                     sort_keys=True))


if __name__ == '__main__':
    main()
