#!/usr/bin/env python3
"""Literal graph, direct-signature and complete formula-tail checking."""
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import argparse
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def inspect(path):
    lines = path.read_text().splitlines()
    n, size = map(int, lines[0].split())
    require(n == 19, 'fixture order')
    edges = [tuple(map(int, line.split())) for line in lines[1:]]
    require(len(edges) == size and len(set(edges)) == size, 'edge count or duplicate')
    require(all(0 <= a < b < n for a, b in edges), 'edge endpoint')
    edges = set(edges)
    bad = [five for five in combinations(range(n), 5)
           if len({pair in edges for pair in combinations(five, 2)}) == 1]
    require(not bad, 'fixture monochromatic five-set')
    signatures = []
    for v in range(9, 19):
        sig = 0
        for i in range(3):
            colors = {(3*i+t, v) in edges for t in range(3)}
            require(len(colors) == 1, 'nonuniform fixture attachment')
            if True in colors:
                sig |= 1 << i
        signatures.append(sig)
    require(signatures == [0, 1, 1, 2, 2, 3, 4, 4, 5, 6], 'fixture signature multiset')
    require(all(((a, b) in edges) == (signatures[a-9] & signatures[b-9] == 0)
                for a, b in combinations(range(9, 19), 2)), 'fixed fixture graph')
    return dict(vertices=n, red_edges=size, five_sets_checked=11628, ramsey=True,
                signatures=signatures, nonempty=9, red_fixed_degrees=[4, 4, 4],
                core_words=''.join(str(int((3*i, 3*j+d) in edges))
                                   for i, j in ((0, 1), (0, 2), (1, 2)) for d in range(3)))


def direct_arithmetic():
    histogram = [0]*11
    basic, stronger, total, maximizing = 0, 0, 0, []
    for signatures in combinations_with_replacement(range(8), 10):
        total += 1
        # Count actual membership, without occupancy-vector generation.
        degree = [sum(bool(s & (1 << i)) for s in signatures) for i in range(3)]
        if max(degree) > 4 or any(signatures.count(s) > 2 for s in (1, 2, 4)):
            continue
        basic += 1
        nonempty = sum(s != 0 for s in signatures)
        histogram[nonempty] += 1
        if nonempty == 9:
            maximizing.append([signatures.count(s) for s in range(8)])
        if all(sum(bool(s & (1 << i)) and not bool(s & (1 << k)) for s in signatures) <= 3
               for i in range(3) for k in range(3) if i != k):
            stronger += 1
    require(total == 19448 and basic == 928 and stronger == 778, 'direct arithmetic census')
    require(maximizing == [[1, 2, 2, 1, 2, 1, 1, 0]] and histogram[10] == 0, 'direct extremizers')
    return dict(compositions=total, basic_profiles=basic, stronger_profiles=stronger,
                nonempty_histogram={i: n for i, n in enumerate(histogram)},
                maximum_nonempty=9, maximizing_profiles=maximizing)


def variable_map():
    def rotate(v):
        return 3*(v//3)+(v % 3+1) % 3 if v < 33 else v
    def key(pair):
        a, b = pair
        if b < 33:
            return 0, a, b
        if a >= 33:
            return 1, a, b
        return 2, b, a
    representatives, pair_rep = set(), {}
    for pair in combinations(range(43), 2):
        a, b = pair
        if b < 33 and a//3 == b//3:
            continue
        orbit, q = set(), pair
        while q not in orbit:
            orbit.add(q)
            q = tuple(sorted((rotate(q[0]), rotate(q[1]))))
        rep = min(orbit)
        representatives.add(rep)
        pair_rep[pair] = rep
    ids = {rep: i+1 for i, rep in enumerate(sorted(representatives, key=key))}
    require(len(ids) == 320, 'primary orbit count')
    return {pair: ids[rep] for pair, rep in pair_rep.items()}


def expected_tail():
    ids = variable_map()
    def var(v, i):
        return ids[3*i, v]
    rows = [tuple(-var(33, i) for i in [j]) for j in range(3)]
    # Each forbidden signature condition is translated through literal incidences.
    for vertices in combinations(range(33, 43), 3):
        for singleton in (1, 2, 4):
            rows.append(tuple(sorted(-var(v, i) if singleton & (1 << i) else var(v, i)
                                     for v in vertices for i in range(3))))
    for vertices in combinations(range(33, 43), 4):
        for i in range(3):
            for k in range(3):
                if i != k:
                    rows.append(tuple(sorted(x for v in vertices for x in (-var(v, i), var(v, k)))))
    require(len(rows) == len(set(rows)) == 1623, 'tail census')
    return sorted(rows, key=lambda row: (len(row), row))


def audit_formula(parent, path, bits):
    ids = variable_map()
    primary = [ids[3*i, 3*j+d] for i, j in ((0, 1), (0, 2), (1, 2)) for d in range(3)]
    units = [(v if b == '1' else -v,) for v, b in zip(primary, bits)]
    with parent.open('rb') as base, path.open('rb') as full:
        h = base.readline().split()
        require(h[:2] == [b'p', b'cnf'], 'parent header')
        nv, nc = map(int, h[2:])
        require(full.readline() == f'p cnf {nv} {nc+1632}\n'.encode(), 'full header')
        for _ in range(nc):
            line = base.readline()
            require(bool(line) and line == full.readline(), 'full parent prefix')
        require(base.read() == b'', 'parent EOF')
        for row in units+expected_tail():
            require(full.readline() == (' '.join(map(str, row))+' 0\n').encode(), 'core or signature clause')
        require(full.read() == b'', 'full EOF')
    return dict(variables=nv, clauses=nc+1632, core_units=9, signature_clauses=1623, complete_prefix=True)


def semantic_controls():
    # Truth-table semantics of all cut shapes on ordered signatures.
    triples = quads = 0
    for sigs in product(range(8), repeat=3):
        for i in range(3):
            value = any((not bool(s & (1 << j))) if j == i else bool(s & (1 << j))
                        for s in sigs for j in range(3))
            require(value == (sum(s == (1 << i) for s in sigs) <= 2), 'singleton cut semantics')
            triples += 1
    for sigs in product(range(8), repeat=4):
        for i in range(3):
            for k in range(3):
                if i != k:
                    value = any(not bool(s & (1 << i)) or bool(s & (1 << k)) for s in sigs)
                    require(value == (sum(bool(s & (1 << i)) and not bool(s & (1 << k)) for s in sigs) <= 3),
                            'four-vertex cut semantics')
                    quads += 1
    return dict(triple_cut_assignments=triples, quadruple_cut_assignments=quads)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--fixture', type=Path)
    a = p.parse_args()
    print(json.dumps(inspect(a.fixture) if a.fixture else direct_arithmetic(), sort_keys=True))
