#!/usr/bin/env python3
"""Exact contact-event producer; all generated tables belong outside the repo."""
import argparse
from collections import defaultdict
from fractions import Fraction as F
from math import gcd, isqrt
import hashlib
import json
from pathlib import Path


def norm(z):
    a, b = z
    return a*a + a*b + b*b


def mul(z, w):
    a, b = z
    c, d = w
    return a*c-b*d, a*d+b*c+b*d


def conjugate(z):
    return z[0]+z[1], -z[1]


def primitive(u, v, k):
    g = gcd(gcd(u, v), k)
    if not g:
        raise ValueError('zero contact equation')
    t = u//g, v//g, k//g
    return max(t, tuple(-x for x in t))


def pair(q):
    return [q.numerator, q.denominator]


def build(limit=67):
    bound = isqrt(4*limit//3)
    points = sorted((a, b) for a in range(-bound, bound+1)
                    for b in range(-bound, bound+1) if norm((a, b)) <= limit)
    origin = points.index((0, 0))
    seed_edges = [[i, j] for i, z in enumerate(points)
                  for j, w in enumerate(points[:i])
                  if norm((z[0]-w[0], z[1]-w[1])) == 1]
    lines = defaultdict(list)
    universal = []
    for i, z in enumerate(points):
        for j, w in enumerate(points):
            k = norm(z)+norm(w)-1
            if i == origin or j == origin:
                if k == 0:
                    universal.append([i, j])
                continue
            a, b = mul(w, conjugate(z))
            u, v = 2*a+b, -3*b
            if 3*k*k <= 3*u*u+v*v:
                lines[primitive(u, v, k)].append([i, j])
    rational = defaultdict(set)
    irrational = []
    residues = [(a-b) % 3 for a, b in points]
    for (u, v, k), edges in sorted(lines.items()):
        s = 3*u*u+v*v
        d = s-3*k*k
        root = isqrt(d)
        if root*root == d:
            for sign in (-1, 1):
                xy = (F(3*u*k+sign*v*root, s), F(v*k-sign*u*root, s))
                rational[xy].update(map(tuple, edges))
        else:
            products = {residues[i]*residues[j] % 3 for i, j in edges
                        if residues[i] and residues[j]}
            if len(products) > 1:
                raise ValueError('residue product is not constant')
            zero_edge = next(([i, j] for i, j in edges
                              if not residues[i] and not residues[j]), None)
            irrational.append({'line': [u, v, k], 'radicand': d,
                               'cross_edges': edges,
                               'epsilon': next(iter(products), 1),
                               'zero_edge': zero_edge,
                               'chromatic_number': 4 if zero_edge else 3})
    # Enumerate coincidences independently of contact events. An omitted
    # coincidence-only rotation would otherwise invalidate the generic case.
    coincidences = defaultdict(list)
    for i, z in enumerate(points):
        if i == origin:
            continue
        for j, w in enumerate(points):
            n = norm(w)
            if n and norm(z) == n:
                a, b = mul(z, conjugate(w))
                xy = F(2*a+b, 2*n), F(b, 2*n)
                coincidences[xy].append([i, j])
    rational_rows = []
    for xy in sorted(set(rational) | set(coincidences)):
        rational_rows.append({'rotation': [pair(q) for q in xy],
                              'cross_edges': [list(e) for e in sorted(rational[xy])],
                              'coincidences': coincidences[xy]})
    result = {'format': 1, 'norm_limit': limit, 'points': points,
              'seed_edges': seed_edges, 'universal_cross_edges': universal,
              'irrational': irrational, 'rational': rational_rows,
              'contact_lines': [list(t) for t in sorted(lines)]}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    table = build()
    data = (json.dumps(table, separators=(',', ':'))+'\n').encode()
    (args.work/'catalog.json').write_bytes(data)
    print(json.dumps({'catalog_sha256': hashlib.sha256(data).hexdigest(),
                      'bytes': len(data), 'points': len(table['points']),
                      'irrational_lines': len(table['irrational']),
                      'rational_rotations': len(table['rational'])}, sort_keys=True))


if __name__ == '__main__':
    main()
