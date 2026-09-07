#!/usr/bin/env python3
"""Untrusted exact geometry and SAT proposal; write generated state outside Git."""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path
from flint import fmpz_poly
from pysat.solvers import Cadical195


def dump(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':')) + '\n'


def cyclotomics(limit):
    ans = {}
    for n in range(1, limit + 1):
        f = fmpz_poly([-1] + [0] * (n - 1) + [1])
        for d in range(1, n):
            if n % d == 0:
                f, rem = divmod(f, ans[d])
                if rem:
                    raise ValueError('nonexact cyclotomic division')
        ans[n] = f
    return ans


def geometry(n, phi):
    deg = phi.degree()
    powers = [fmpz_poly([0] * j + [1]) % phi for j in range(n)]
    key = lambda p: tuple(int(p[j]) for j in range(deg))
    point_keys, addresses, seen = [], [], set()
    for i in range(n):
        for j in range(n):
            p = key(powers[i] - powers[j])
            if p not in seen:
                seen.add(p)
                point_keys.append(p)
                addresses.append([i, j])
    pts = [fmpz_poly(list(p)) for p in point_keys]
    bars = [sum((powers[-j % n] * int(p[j]) for j in range(deg)),
                fmpz_poly([])) for p in pts]
    shells = {}
    for a in range(len(pts)):
        for b in range(a + 1, len(pts)):
            delta = key(((pts[a] - pts[b]) * (bars[a] - bars[b])) % phi)
            if not any(delta):
                raise ValueError('distinct points with zero norm')
            shells.setdefault(delta, []).append([a, b])
    return addresses, point_keys, list(shells.items())


def classify(m, edges):
    adj = [[] for _ in range(m)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    colours = [-1] * m
    bip = True
    for root in range(m):
        if colours[root] != -1:
            continue
        colours[root] = 0
        queue = deque([root])
        while queue:
            a = queue.popleft()
            for b in adj[a]:
                if colours[b] == -1:
                    colours[b] = 1 - colours[a]
                    queue.append(b)
                elif colours[a] == colours[b]:
                    bip = False
    if bip:
        return 2, ''.join(map(str, colours)), None, 0
    degree = list(map(len, adj))
    removed = [x <= 2 for x in degree]
    peel = [i for i in range(m) if removed[i]]
    for a in peel:
        for b in adj[a]:
            if not removed[b]:
                degree[b] -= 1
                if degree[b] <= 2:
                    removed[b] = True
                    peel.append(b)
    core = [a for a in range(m) if not removed[a]]
    colours = [-1] * m
    word, conflicts = None, 0
    if core:
        index = {v: i for i, v in enumerate(core)}
        with Cadical195() as solver:
            for a in range(len(core)):
                solver.add_clause([3 * a + c + 1 for c in range(3)])
            for a, b in edges:
                if a in index and b in index:
                    for c in range(3):
                        solver.add_clause([-3 * index[a] - c - 1,
                                           -3 * index[b] - c - 1])
            solver.add_clause([1])
            solver.conf_budget(200000)
            answer = solver.solve_limited()
            conflicts = solver.accum_stats()['conflicts']
            if answer is not True:
                raise RuntimeError('gate incomplete: ' + repr(answer))
            model = set(solver.get_model())
            for a in core:
                colours[a] = next(c for c in range(3)
                                  if 3 * index[a] + c + 1 in model)
        word = ''.join(str(colours[a]) for a in core)
    for a in reversed(peel):
        used = {colours[b] for b in adj[a]}
        colours[a] = next(c for c in range(3) if c not in used)
    if not all(colours[a] != colours[b] for a, b in edges):
        raise ValueError('bad positive proposal')
    return 3, ''.join(map(str, colours)), word, conflicts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', type=Path, required=True)
    args = ap.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    polys = cyclotomics(31)
    orders = [n for n in range(2, 32)
              if (n * (n - 1) if n % 2 else n * n // 2) + 1 <= 508]
    certificate = {'version': 1, 'family': 'polygon_difference_all_scales_508',
                   'cores': []}
    stats = []
    for n in orders:
        addresses, points, shells = geometry(n, polys[n])
        cases = []
        calls = conflicts = 0
        for delta, edges in shells:
            chi, colour, word, cost = classify(len(points), edges)
            if word is not None:
                certificate['cores'].append({'n': n, 'pair': edges[0], 'word': word})
                calls += 1
                conflicts = max(conflicts, cost)
            cases.append({'delta': list(delta), 'edges': edges,
                          'chi': chi, 'colour': colour})
        obj = {'n': n, 'addresses': addresses,
               'coordinates': [list(p) for p in points], 'cases': cases}
        (args.work / f'{n}.json').write_text(dump(obj))
        row = {'n': n, 'vertices': len(points), 'shells': len(shells),
               'chi2': sum(c['chi'] == 2 for c in cases),
               'chi3': sum(c['chi'] == 3 for c in cases),
               'SAT_calls': calls, 'maximum_conflicts': conflicts}
        stats.append(row)
        print(dump(row), end='', flush=True)
    (args.work / 'certificate.json').write_text(dump(certificate))
    (args.work / 'proposal_summary.json').write_text(dump(stats))
    print('certificate_sha256', hashlib.sha256(dump(certificate).encode()).hexdigest())


if __name__ == '__main__':
    main()
