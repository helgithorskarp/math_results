#!/usr/bin/env python3
"""Full Ramsey formulas for 1^10 3^11, with local bounds and centralizer order."""
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parent
T = 100000


def require(ok, why):
    if not ok:
        raise ValueError(why)


def info(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        while b := stream.read(1 << 20):
            h.update(b)
    return dict(bytes=path.stat().st_size, sha256=h.hexdigest())


class Formula:
    def __init__(self, primary):
        self.nv = primary
        self.clauses = set()

    def add(self, literals):
        c = set(literals)
        if any(-v in c for v in c):
            return
        require(all(1 <= abs(v) < T for v in c), 'literal range')
        self.clauses.add(tuple(sorted(c)))

    def atmost(self, literals, bound):
        previous = {}
        for i, literal in enumerate(literals, 1):
            row = {}
            for j in range(1, min(i, bound+1)+1):
                self.nv += 1
                row[j] = self.nv
                if j == 1:
                    self.add((-literal, row[j]))
                if j in previous:
                    self.add((-previous[j], row[j]))
                if j > 1 and j-1 in previous:
                    self.add((-literal, -previous[j-1], row[j]))
            previous = row
        if bound+1 in previous:
            self.add((-previous[bound+1],))


def model(r, k=11, n=43):
    require(0 <= r <= k and 3*k <= n, 'model dimensions')
    colors = [1]*r+[0]*(k-r)
    pairs = list(combinations(range(k), 2))
    ids = {p: tuple(range(1+3*i, 4+3*i)) for i, p in enumerate(pairs)}
    nv = 3*len(pairs)
    fixed, links = {}, {}
    for i, j in combinations(range(3*k, n), 2):
        nv += 1
        fixed[i, j] = nv
    for j in range(3*k, n):
        for i in range(k):
            nv += 1
            links[i, j] = nv

    def edge(a, b):
        a, b = sorted((a, b))
        if a >= 3*k:
            return fixed[a, b]
        i, u = divmod(a, 3)
        if b >= 3*k:
            return links[i, b]
        j, v = divmod(b, 3)
        if i == j:
            return T if colors[i] else -T
        return ids[i, j][(v-u) % 3]
    return nv, colors, ids, fixed, links, edge


def ramsey(formula, edge, n):
    for five in combinations(range(n), 5):
        edges = [edge(a, b) for a, b in combinations(five, 2)]
        for sign in (-1, 1):
            signed = [sign*e for e in edges]
            if T not in signed:
                formula.add(x for x in signed if x != -T)


def generate(r, path):
    require(r in range(6), 'red count outside complement cover')
    primary, colors, ids, fixed, links, edge = model(r)
    f = Formula(primary)
    ramsey(f, edge, 43)
    base_count = len(f.clauses)
    tokens, full = [[] for _ in range(11)], [[] for _ in range(11)]
    for (i, j), bits in ids.items():
        gates = {}
        for color in sorted({colors[i], colors[j]}):
            u, v, z = f.nv+1, f.nv+2, f.nv+3
            f.nv += 3
            gates[color] = (u, v, z)
            for values in product((0, 1), repeat=3):
                weight = sum(x == color for x in values)
                cost = 2-weight+3*(weight == 3)
                antecedent = [-b if x else b for b, x in zip(bits, values)]
                for gate, truth in ((u, cost >= 1), (v, cost >= 2), (z, weight == 3)):
                    f.add(antecedent+[gate if truth else -gate])
        for endpoint in (i, j):
            tokens[endpoint].extend(gates[colors[endpoint]][:2])
            full[endpoint].append(gates[colors[endpoint]][2])
        if i == 0:
            f.add((-bits[1], bits[0]))
            f.add((-bits[2], bits[1]))
    for row in tokens:
        require(len(row) == 20, 'deficit tokens')
        f.atmost(row, 8)
    for i in range(11):
        sign = 1 if colors[i] else -1
        fixed_own = [sign*links[i, j] for j in range(33, 43)]
        f.atmost(fixed_own+[z for z in full[i] for _ in range(3)], 4)
        cross = [sign*v for pair, bits in ids.items() if i in pair for v in bits]
        own = fixed_own+cross
        require(len(own) == 40, 'outside triangle degree occurrences')
        f.atmost(own, 22)  # total own degree <=24, including two internal edges
        f.atmost([-x for x in own], 24)  # outside own degree >=16
    for j in range(33, 43):
        incident = [fixed[tuple(sorted((j, t)))] for t in range(33, 43) if t != j]
        incident += [links[i, j] for i in range(11) for _ in range(3)]
        require(len(incident) == 42, 'fixed incident-edge multiplicity')
        f.atmost(incident, 24)
        f.atmost([-x for x in incident], 24)
    for j in range(1, 10):
        if colors[j] == colors[j+1]:
            for a, b in zip(ids[0, j], ids[0, j+1]):
                f.add((-a, b))
    for j in range(33, 42):
        a = [links[i, j] for i in range(11)]
        b = [links[i, j+1] for i in range(11)]
        for q in range(11):
            for prefix in product((0, 1), repeat=q):
                clause = []
                for t, bit in enumerate(prefix):
                    clause.extend((-a[t], -b[t]) if bit else (a[t], b[t]))
                f.add(clause+[-a[q], b[q]])
    require(f.nv == 34196+3*r*(11-r) < T, 'auxiliary variable count')
    ordered = sorted(f.clauses, key=lambda c: (len(c), c))
    with path.open('w') as stream:
        stream.write(f'p cnf {f.nv} {len(ordered)}\n')
        for clause in ordered:
            stream.write(' '.join(map(str, clause))+' 0\n')
    return dict(info(path), red_cycles=r, variables=f.nv, clauses=len(ordered),
                primary_variables=primary, edge_orbits=primary+11, ramsey_clauses=base_count)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--red-cycles', type=int, choices=range(6), required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    require(not args.output.resolve().is_relative_to(ROOT.parent), 'large formula outside Git')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    print(json.dumps(generate(args.red_cycles, args.output), sort_keys=True))
