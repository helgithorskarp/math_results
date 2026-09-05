#!/usr/bin/env python3
"""Independent literal-action reconstruction of the complete added layer.

Imports no formula-generator module. Base checking uses the separately
compiled parent C++ DSU/literal-five-set verifier; this file also checks
byte preservation of the exact base. Word enumeration uses integer bit
patterns and actual vertex permutations, rather than the generator's
tuple-word implementation.
"""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import random
import subprocess

BASES = {
    9: (105, 211323, '7846688b50408ebb6f9d6a9fc0a537d06186e9d732f5be9856edae6b7e88ca75'),
    10: (103, 210907, '6455b56f83001e09fd53f7fa8bdbd26270df013a32b3895569ddab3e5d18d929'),
}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def generators(index):
    need(index in BASES, 'unsupported case')
    g, h = list(range(43)), list(range(43))
    for s, cy in ((1, 2 if index == 9 else 1), (4, 2)):
        for t in range(3):
            g[s+t], h[s+t] = s+(t+1) % 3, s+(t+cy) % 3
    for s in (7, 16, 25, 34):
        for j in range(9):
            u, v = divmod(j, 3)
            g[s+j], h[s+j] = s+3*((u+1) % 3)+v, s+3*u+(v+1) % 3
    return g, h


def orbits(index):
    g, h = generators(index)
    remaining = set(combinations(range(43), 2))
    groups = []
    while remaining:
        start = min(remaining)
        seen, todo = {start}, [start]
        while todo:
            u, v = todo.pop()
            for p in (g, h):
                image = tuple(sorted((p[u], p[v])))
                if image not in seen:
                    seen.add(image)
                    todo.append(image)
        need(seen <= remaining, 'overlapping pair orbits')
        remaining -= seen
        groups.append(seen)
    need(len(groups) == BASES[index][0], 'pair-orbit count')
    return {e: i+1 for i, group in enumerate(groups) for e in group}


def translation(start, shift):
    p = list(range(43))
    if start in (1, 4):
        for j in range(3):
            p[start+j] = start+(j+shift) % 3
    else:
        x, y = divmod(shift, 3)
        for j in range(9):
            u, v = divmod(j, 3)
            p[start+j] = start+3*((u+x) % 3)+(v+y) % 3
    return p


def tail(index):
    mapping = orbits(index)
    e = lambda u, v: mapping[tuple(sorted((u, v)))]
    clauses = set()
    # Literal fixed edge followed by the four direction edges in each copy.
    for s, t in ((7, 16), (16, 25), (25, 34)):
        variables = ([e(0, s)] + [e(s, s+d) for d in (1, 3, 4, 5)]
                     + [e(0, t)] + [e(t, t+d) for d in (1, 3, 4, 5)])
        need(len(set(variables)) == 10, 'profile variables')
        for bits in range(1024):
            a, b = bits >> 5, bits & 31
            if a > b:
                clauses.add(tuple(sorted(-v if bits & (1 << (9-j)) else v
                                         for j, v in enumerate(variables))))
    for start, size in ((16, 9), (25, 9), (34, 9), (1, 3), (4, 3)):
        variables = [e(7, start+j) for j in range(size)]
        need(len(set(variables)) == size, 'cross word variables')
        for bits in range(1 << size):
            values = {v: (bits >> (size-1-j)) & 1 for j, v in enumerate(variables)}
            images = []
            for shift in range(size):
                p = translation(start, shift)
                image = 0
                for j in range(size):
                    image = 2*image+values[e(p[7], p[start+j])]
                images.append(image)
            if min(images) < bits:
                clauses.add(tuple(sorted(-v if values[v] else v for v in variables)))
    need(len(clauses) == 2840, 'tail cardinality')
    return sorted(clauses, key=lambda q: (len(q), q))


def audit(index, parent, full, checker):
    nv, nc, digest = BASES[index]
    need(hashlib.sha256(parent.read_bytes()).hexdigest() == digest, 'parent digest')
    bs = [0, 0, 0, 2] if index == 9 else [0, 0, 1, 1]
    result = subprocess.run([str(checker), '1', *map(str, bs), '4', str(parent)],
                            capture_output=True, text=True, check=True)
    need(' PASS' in result.stdout, 'missing full base audit')
    expected = tail(index)
    with parent.open() as src, full.open() as dst:
        need(src.readline() == f'p cnf {nv} {nc}\n', 'base header')
        need(dst.readline() == f'p cnf {nv} {nc+len(expected)}\n', 'extended header')
        count = 0
        for line in src:
            need(dst.readline() == line, 'parent clause not byte preserved')
            count += 1
        need(count == nc, 'parent clause count')
        for clause in expected:
            need(dst.readline() == ' '.join(map(str, clause))+' 0\n', 'normalization tail mismatch')
        need(dst.read() == '', 'unexpected extra content')
    return dict(index=index, variables=nv, parent_clauses=nc, tail_clauses=len(expected),
                full_sha256=hashlib.sha256(full.read_bytes()).hexdigest(), status='verified')


def controls(index):
    mapping = orbits(index)
    g, h = generators(index)
    e = lambda u, v: mapping[tuple(sorted((u, v)))]
    constraints = tail(index)
    randomizer = random.Random(33543+index)
    n = BASES[index][0]
    inputs = [[0]*(n+1), [1]*(n+1)]
    inputs += [[0]+[randomizer.randrange(2) for _ in range(n)] for _ in range(256)]
    for values in inputs:
        # Complement first, before centralizer normalization; x1 is edge(0,1).
        need(e(0, 1) == 1, 'complement convention')
        values = [v ^ (1-values[1]) for v in values]
        edge = lambda u, v: values[e(u, v)]
        profile = lambda s: tuple([edge(0, s)]+[edge(s, s+d) for d in (1, 3, 4, 5)])
        p = list(range(43))  # new labels -> old labels
        for new, old in zip((7, 16, 25, 34), sorted((7, 16, 25, 34), key=profile)):
            p[new:new+9] = range(old, old+9)
        for start, size in ((16, 9), (25, 9), (34, 9), (1, 3), (4, 3)):
            choices = [translation(start, shift) for shift in range(size)]
            q = min(choices, key=lambda q: tuple(edge(p[7], p[q[start+j]]) for j in range(size)))
            p = [p[q[v]] for v in range(43)]
        need(sorted(p) == list(range(43)), 'not a relabeling')
        need(all(p[q[v]] == q[p[v]] for q in (g, h) for v in range(43)), 'not in centralizer')
        new_values = {}
        for (u, v), variable in mapping.items():
            value = edge(p[u], p[v])
            need(variable not in new_values or new_values[variable] == value, 'broken orbit invariance')
            new_values[variable] = value
        need(new_values[1] == 1, 'complement unit broken')
        need(all(any(new_values[abs(lit)] == (lit > 0) for lit in clause)
                 for clause in constraints), 'failed normalization')
        need(all(new_values[e(u, v)] == edge(p[u], p[v])
                 for u, v in combinations(range(43), 2)), 'literal edge mismatch')
    # Burnside independently predicts 64 regular binary translation classes.
    counts = {}
    for start, size, expected in ((16, 9, (512+8*8)//9), (1, 3, (8+2*2)//3)):
        minima = set()
        for bits in range(1 << size):
            words = []
            for shift in range(size):
                p = translation(start, shift)
                value = 0
                for j in range(size):
                    value = 2*value+((bits >> (size-1-(p[start+j]-start))) & 1)
                words.append(value)
            minima.add(min(words))
        need(len(minima) == expected, 'Burnside mismatch')
        counts[str(size)] = len(minima)
    return dict(index=index, arbitrary_colorings=len(inputs), all_edges_per_coloring=903,
                complement_unit_preserved=True, centralizer_verified=True,
                binary_translation_classes=counts)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path)
    p.add_argument('--checker', type=Path)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    report = {'controls': [controls(i) for i in (9, 10)]}
    if a.work:
        need(a.checker is not None, 'checker required')
        report['formulas'] = [audit(i, a.work / f'parent_{i:02}.cnf', a.work / f'case_{i:02}.cnf',
                                    a.checker) for i in (9, 10)]
    a.report.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report, sort_keys=True))
