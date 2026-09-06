#!/usr/bin/env python3
"""Exact separator and projected-colouring CNF; no selector search."""
import importlib.util
from itertools import permutations
from pathlib import Path

HERE = Path(__file__).resolve().parent


def geometry():
    path = HERE.parent / 'hadwiger_nelson_heule517_family_pilot/engine.py'
    spec = importlib.util.spec_from_file_location('prior_exact_graph', path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    data = mod.geometry()
    large = [v for v, p in enumerate(data['points'])
             if all(p[a][k] == 0 for a in (0, 1) for k in (2, 3, 6, 7))]
    L = set(large); small = sorted(set(range(517)) - L)
    cross = [e for e in data['edges'] if (e[0] in L) != (e[1] in L)]
    boundary = sorted({v for e in cross for v in e if v in L})
    terminals = sorted({v for e in cross for v in e if v not in L})
    edges = [e for e in data['edges'] if set(e) <= L]
    assert len(large) == 375 and len(small) == 142 and len(cross) == 30
    assert len(boundary) == 19 and len(terminals) == 30 and len(edges) == 1920
    assert not any(v >= 510 for e in cross for v in e)
    return data, dict(large=large, small=small, boundary=boundary,
                      terminals=terminals, cross_edges=cross, large_edges=edges)


def cnf(vertices, edges):
    pos = {v: i for i, v in enumerate(vertices)}
    clauses = [[4*i+c+1 for c in range(4)] for i in range(len(vertices))]
    clauses += [[-(4*pos[u]+c+1), -(4*pos[v]+c+1)] for u, v in edges for c in range(4)]
    clauses.append([4*pos[0]+1])
    return 4*len(vertices), clauses


def orbit(pattern):
    return sorted({''.join(str(([0]+list(p))[int(c)]) for c in pattern)
                   for p in permutations([1, 2, 3])})


def blocking(pattern, vertices, boundary):
    pos = {v: i for i, v in enumerate(vertices)}
    return [[-(4*pos[v]+int(c)+1) for v, c in zip(boundary, s)] for s in orbit(pattern)]


def normalized(colour, vertices, boundary):
    pos = {v: i for i, v in enumerate(vertices)}
    rename = {0: 0}
    for v in boundary:
        c = int(colour[pos[v]])
        if c not in rename: rename[c] = len(rename)
    for c in range(4):
        if c not in rename: rename[c] = len(rename)
    full = ''.join(str(rename[int(c)]) for c in colour)
    return ''.join(full[pos[v]] for v in boundary), full


def dimacs(n, clauses):
    return (f'p cnf {n} {len(clauses)}\n' + ''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode()


def small_case(vertices, small_edges, cross_edges, boundary, pattern):
    """Existential colouring of selected small vertices against one fixed row."""
    assert len(pattern) == len(boundary) and set(pattern) <= set('0123')
    pos = {v:i for i,v in enumerate(vertices)}
    assert len(pos) == len(vertices) and not set(vertices).intersection(boundary)
    fixed = dict(zip(boundary, map(int, pattern)))
    clauses = [[4*i+c+1 for c in range(4)] for i in range(len(vertices))]
    clauses += [[-4*pos[u]-c-1,-4*pos[v]-c-1]
                for u,v in small_edges if u in pos and v in pos for c in range(4)]
    for u,v in cross_edges:
        if u in fixed and v in pos: clauses.append([-4*pos[v]-fixed[u]-1])
        if v in fixed and u in pos: clauses.append([-4*pos[u]-fixed[v]-1])
    return 4*len(vertices), clauses
