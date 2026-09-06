#!/usr/bin/env python3
"""Exact mutual graph of the fixed 122 archived H510 completion centres.

Standard-library Python 3.11. All coefficient arithmetic is rational;
coordinates use (1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165).
The large norm transcript is local output, never a public prerequisite.
"""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import lcm
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
RAD = (1, 3, 5, 15, 11, 33, 55, 165)
FRESH = 'hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json'
OLD = 'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json'


def require(test, message):
    if not test:
        raise ValueError(message)


def parse(row):
    require(len(row) == 2 and all(len(a) == 8 for a in row), 'coordinate shape')
    return tuple(tuple(Fraction(c) for c in a) for a in row)


def square(a):
    out = [Fraction(0)] * 8
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(a):
                if y:
                    out[i ^ j] += x * y * RAD[i & j]
    return out


def norm(p, q):
    axes = [square(tuple(x-y for x, y in zip(a, b))) for a, b in zip(p, q)]
    return tuple(x+y for x, y in zip(*axes))


def histogram(values):
    return {str(k): v for k, v in sorted(Counter(values).items())}


def run(out):
    start = time.monotonic()
    plan = json.loads((HERE/'plan.json').read_text())
    for name, digest in plan['inputs'].items():
        require(sha256((REPO/name).read_bytes()).hexdigest() == digest, name)
    old = json.loads((REPO/OLD).read_text())
    labels = [v for v in range(553) if '510' in old['provenance'][v]]
    H = [parse(old['coordinates'][str(v)]) for v in labels]
    rows = json.loads((REPO/FRESH).read_text())
    ids = [r['centre_index'] for r in rows]
    Q = [parse(r['coordinates']) for r in rows]
    require(ids == sorted(set(ids)) and len(ids) == 122, 'fresh labels')
    require(len(H) == len(set(H)) == 510, 'H510 points')
    require(len(set(Q)) == 122 and not set(Q) & set(H), 'fresh distinctness')
    D = lcm(*(c.denominator for p in H+Q for a in p for c in a))
    L = {i for i, p in enumerate(H) if all(p[a][j] == 0 for a in (0, 1) for j in (2, 3, 6, 7))}
    require(len(L) == 375, 'large block size')
    out.mkdir(parents=True, exist_ok=True)
    edges = []
    stream_digest = sha256()
    pair_count = 0
    with (out/'norms.txt').open('w') as stream:
        def record(kind, a, b, n):
            nonlocal pair_count
            ns = [v * D * D for v in n]
            require(all(v.denominator == 1 for v in ns), 'norm scaling')
            line = f'{kind} {a} {b} ' + ' '.join(str(v.numerator) for v in ns) + '\n'
            stream.write(line)
            stream_digest.update(line.encode('ascii'))
            pair_count += 1
        for i, j in combinations(range(122), 2):
            n = norm(Q[i], Q[j])
            record('F', ids[i], ids[j], n)
            if n == (1, 0, 0, 0, 0, 0, 0, 0):
                edges.append([ids[i], ids[j]])
        for i, row in enumerate(rows):
            neighbors = []
            for v, p in enumerate(H):
                n = norm(Q[i], p)
                record('H', ids[i], v, n)
                if n == (1, 0, 0, 0, 0, 0, 0, 0):
                    neighbors.append(v)
            require(neighbors == row['neighbors'], ('old attachment', ids[i]))
            require(len(neighbors) == row['degree'] >= 4, 'degree')
            require(len(row['witness']) == 3 and row['witness'] == sorted(set(row['witness'])) and set(row['witness']) <= set(neighbors), 'old witness')
    require(pair_count == 7381 + 62220, 'pair domain')
    adj = {v: set() for v in ids}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    attach = {r['centre_index']: r['neighbors'] for r in rows}
    types = {v: ('M' if any(n in L for n in ns) and any(n not in L for n in ns) else 'L' if all(n in L for n in ns) else 'S') for v, ns in attach.items()}
    components = []
    unseen = set(ids)
    while unseen:
        todo = [min(unseen)]
        part = set(todo)
        while todo:
            v = todo.pop()
            for w in sorted(adj[v]-part):
                part.add(w)
                todo.append(w)
        unseen -= part
        ne = sum(len(adj[v]) for v in part)//2
        old_neighbors = set().union(*(set(attach[v]) for v in part))
        components.append({'centres': sorted(part), 'edges': ne,
                           'cycle_rank': ne-len(part)+1,
                           'types': histogram(types[v] for v in part),
                           'old_L_neighbors': sorted(old_neighbors & L),
                           'old_S_neighbors': sorted(old_neighbors-L)})
    certificate = {'centre_ids': ids, 'fresh_edges': edges, 'components': components,
                   'attachment_types': {str(v): types[v] for v in ids}}
    # Repeated simultaneous leaf stripping isolates all cycle vertices.
    alive = set(ids)
    while True:
        leaves = {v for v in alive if len(adj[v] & alive) < 2}
        if not leaves:
            break
        alive -= leaves
    cycle = []
    if alive:
        require(all(len(adj[v] & alive) == 2 for v in alive), 'cycle core degree')
        cycle = [min(alive)]
        previous = None
        while True:
            options = sorted((adj[cycle[-1]] & alive) - {previous})
            w = options[0]
            if w == cycle[0]:
                break
            previous = cycle[-1]
            cycle.append(w)
            require(len(cycle) <= len(alive), 'cycle walk')
        require(set(cycle) == alive, 'single cycle')
    certificate['unique_cycle'] = cycle
    result = {'status': 'COMPLETE EXACT FIXED122 MUTUAL INCIDENCE',
              'common_denominator': D, 'old_vertices': len(H), 'fresh_vertices': len(Q),
              'fresh_pair_checks': 7381, 'attachment_pair_checks': 62220,
              'fresh_edges': len(edges), 'old_attachments': sum(len(ns) for ns in attach.values()),
              'fresh_degree_histogram': histogram(len(adj[v]) for v in ids),
              'attachment_type_histogram': histogram(types.values()),
              'edge_type_histogram': histogram(''.join(sorted((types[u], types[v]))) for u, v in edges),
              'component_order_histogram': histogram(len(c['centres']) for c in components),
              'components': len(components), 'norm_stream_sha256': stream_digest.hexdigest(),
              'native_colouring_queries': 0, 'record_improvement': False}
    for name, value in [('certificate.json', certificate), ('result.json', result)]:
        (out/name).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')
    (out/'runtime.json').write_text(json.dumps({'seconds': time.monotonic()-start}, indent=2)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    run(ap.parse_args().out)
