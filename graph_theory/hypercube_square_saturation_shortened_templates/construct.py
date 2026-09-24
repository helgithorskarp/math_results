#!/usr/bin/env python3
"""Expand the certificate construction. Python 3.11+, standard library only."""
from __future__ import annotations
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATES = {t['name']:t for t in json.loads((ROOT / 'templates.json').read_text())}


class Block:
    def __init__(self, name: str, m: int):
        if name not in TEMPLATES or m < 1 or m & (m - 1):
            raise ValueError('name must be H, S or F; scale must be a positive power of two')
        t = TEMPLATES[name]
        self.name, self.m, self.q = name, m, 1 << t['k']
        self.C, self.D = set(t['C']), set(t['D'])
        self.A = self.C | self.D
        self.core = {tuple(e) for e in t['core_edges']}
        self.rows = list(map(set, t['outside_neighbors']))
        self.length = len(t['T']) * m - 1
        self.order = self.q * m
        self.r0, self.r1 = len(self.core), sum(map(len, self.rows))
        self.delta = Fraction(len(self.A), self.order)
        self.h = Fraction(self.r0 + (m - 1) * self.r1, self.order)
        self.residues = t['T']

    def selected(self, s: int, t: int) -> bool:
        if s < self.q and t < self.q:
            return tuple(sorted((s, t))) in self.core
        if s in self.A and t >= self.q:
            return s in self.rows[t % self.q]
        if t in self.A and s >= self.q:
            return t in self.rows[s % self.q]
        return False

    def expand(self) -> tuple[list[int], list[int]]:
        labels = [z * self.q + a for z in range(self.m) for a in self.residues
                  if z or a]
        if len(labels) != self.length:
            raise RuntimeError('coordinate count mismatch')
        sigma = [0] * (1 << self.length)
        for v in range(1, len(sigma)):
            bit = v & -v
            sigma[v] = sigma[v ^ bit] ^ labels[bit.bit_length() - 1]
        return labels, sigma


def choose(n: int) -> tuple[Block, Block, int]:
    if n < 14:
        raise ValueError('uniform parameter selection requires n >= 14')
    x = n + 2
    m = 1 << ((x // 16).bit_length() - 1)
    if x < 18 * m:
        specs = [('H', 2*m), ('H', 2*m)]
    elif x < 20 * m:
        specs = [('H', 2*m), ('F', m)]
    elif x < 22 * m:
        specs = [('H', 2*m), ('S', 4*m)]
    elif x < 24 * m:
        specs = [('F', m), ('S', 4*m)]
    elif x < 28 * m:
        specs = [('S', 4*m), ('S', 4*m)]
    else:
        specs = [('S', 4*m), ('H', 4*m)]
    a, b = [Block(*s) for s in specs]
    return a, b, n - a.length - b.length


def bound(n: int, a: Block, b: Block) -> Fraction:
    if n < a.length + b.length:
        raise ValueError('blocks exceed the dimension')
    return (a.h + b.h + ((n - a.length)*a.delta + (n - b.length)*b.delta)/4
            + n*a.delta*b.delta)


def construct(a: Block, b: Block, r: int) -> tuple[dict, list[int]]:
    n = a.length + b.length + r
    if r < 0 or not 4 <= n <= 18:
        raise ValueError('expanded instances require 4 <= n <= 18 and padding >= 0')
    al, sa = a.expand(); bl, sb = b.expand()
    ma, mb = (1 << a.length) - 1, ((1 << b.length) - 1) << a.length
    vertices = 1 << n
    exceptional = bytearray(vertices)
    adj = [0] * vertices
    for u in range(vertices):
        s, t = sa[u & ma], sb[(u & mb) >> a.length]
        exceptional[u] = s in a.A and t in b.A
    initial = 0
    for u in range(vertices):
        s, t = sa[u & ma], sb[(u & mb) >> a.length]
        for i in range(n):
            bit = 1 << i
            if u & bit:
                continue
            v = u ^ bit
            if exceptional[u] or exceptional[v]:
                continue
            use = False
            if i < a.length:
                use = a.selected(s, s ^ al[i])
            elif i < a.length + b.length:
                use = b.selected(t, t ^ bl[i-a.length])
            if i >= a.length and s in a.A:
                use |= ((u & ~ma).bit_count() % 2 == (0 if s in a.C else 1))
            if not a.length <= i < a.length + b.length and t in b.A:
                use |= ((u & ~mb).bit_count() % 2 == (0 if t in b.C else 1))
            if use:
                adj[u] |= bit; adj[v] |= bit; initial += 1
    def witnessed(u: int, i: int) -> bool:
        bit = 1 << i
        v = u ^ bit
        candidates = adj[u] & adj[v] & ~bit
        while candidates:
            other = candidates & -candidates
            if adj[u ^ other] & bit:
                return True
            candidates ^= other
        return False
    uncovered = []
    for u in range(vertices):
        for i in range(n):
            bit = 1 << i
            if u & bit:
                continue
            witness = witnessed(u, i)
            if adj[u] & bit:
                if witness:
                    raise RuntimeError('initial square')
            elif not witness:
                if not (exceptional[u] or exceptional[u ^ bit]):
                    raise RuntimeError('unwitnessed edge outside exceptional set')
                uncovered.append((u, i))
    added = 0
    for u, i in uncovered:
        if not witnessed(u, i):
            bit = 1 << i
            adj[u] |= bit; adj[u ^ bit] |= bit; added += 1
    coefficient = bound(n, a, b)
    if initial + added > coefficient * vertices:
        raise RuntimeError('edge bound failed')
    if sum(exceptional) != a.delta*b.delta*vertices:
        raise RuntimeError('exceptional cardinality failed')
    digest = hashlib.sha256()
    for u in range(vertices):
        for i in range(n):
            bit = 1 << i
            if adj[u] & bit and not u & bit:
                digest.update(f'{u} {u ^ bit}\n'.encode('ascii'))
    record = {'dimension':n, 'blocks':[[a.name,a.m],[b.name,b.m]], 'padding':r,
              'initial_edges':initial, 'initial_uncovered_edges':len(uncovered),
              'uncovered_away_from_exceptional_set':0,
              'exceptional_vertices':sum(exceptional), 'completion_edges':added,
              'edge_count':initial+added, 'edge_sha256':digest.hexdigest(),
              'bound_coefficient':str(coefficient)}
    return record, adj


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--dimension',type=int)
    g.add_argument('--blocks',nargs=5,metavar=('TYPE1','SCALE1','TYPE2','SCALE2','PADDING'))
    p.add_argument('--bound',action='store_true')
    p.add_argument('--output',type=Path,help='private expanded witness JSON; do not commit')
    args = p.parse_args()
    if args.dimension is not None:
        a,b,r = choose(args.dimension)
    else:
        ta,ma,tb,mb,r = args.blocks
        a,b,r = Block(ta,int(ma)),Block(tb,int(mb)),int(r)
    n = a.length + b.length + r
    if r < 0:
        raise ValueError('negative padding')
    if args.bound:
        print(json.dumps({'dimension':n,'blocks':[[a.name,a.m],[b.name,b.m]],
                          'padding':r,'bound_coefficient':str(bound(n,a,b))},sort_keys=True))
        return
    record,adj = construct(a,b,r)
    if args.output:
        args.output.write_text(json.dumps({'dimension':n,'adjacency_masks':adj},separators=(',',':'))+'\n')
    print(json.dumps(record,sort_keys=True))


if __name__ == '__main__':
    main()
