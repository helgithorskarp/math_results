#!/usr/bin/env python3
"""Independent, standard-library proof check via Ramanujan trace coordinates."""
import argparse
from collections import Counter, deque
import hashlib
import heapq
import json
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def dump(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')) + '\n'


def digest(obj):
    return hashlib.sha256(dump(obj).encode()).hexdigest()


def mobius(n):
    parity, p = 0, 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            parity += 1
            if n % p == 0:
                return 0
        p += 1
    return (-1) ** (parity + (n > 1))


def ramanujan(n):
    return [sum(d * mobius(n // d) for d in range(1, n + 1)
                if n % d == 0 and k % d == 0) for k in range(n)]


def trace(coefficients, n, r):
    return tuple(sum(c * r[(j - k) % n] for j, c in enumerate(coefficients) if c)
                 for k in range(n))


def geometry(n):
    r = ramanujan(n)
    require(r[0] == sum(gcd(j, n) == 1 for j in range(n)), 'trace degree')
    points, addresses = {}, []
    for i in range(n):
        for j in range(n):
            t = tuple(r[(i - k) % n] - r[(j - k) % n] for k in range(n))
            if t not in points:
                points[t] = len(addresses)
                addresses.append([i, j])
    size = (n * (n - 1) if n % 2 else n * n // 2) + 1
    require(len(addresses) == size, 'complete chord collision count')
    shells, cache = {}, {}
    for a, (i, j) in enumerate(addresses):
        for b in range(a + 1, len(addresses)):
            k, l = addresses[b]
            difference = Counter()
            for exponent, sign in ((i, 1), (j, -1), (k, -1), (l, 1)):
                difference[exponent] += sign
            terms = [(e, c) for e, c in difference.items() if c]
            norm = [0] * n
            for e, c in terms:
                for f, d in terms:
                    norm[(e - f) % n] += c * d
            key = tuple(norm)
            if key not in cache:
                cache[key] = trace(key, n, r)
            t = cache[key]
            require(any(t), 'positive nonzero squared distance')
            shells.setdefault(t, []).append([a, b])
    return addresses, list(shells.items())


def adjacency(m, edges):
    adj = [set() for _ in range(m)]
    for a, b in edges:
        require(type(a) is int and type(b) is int and 0 <= a < b < m,
                'edge domain')
        require(b not in adj[a], 'duplicate edge')
        adj[a].add(b)
        adj[b].add(a)
    return adj


def bipartite_or_cycle(adj):
    colours, parent = [-1] * len(adj), [-1] * len(adj)
    for root in range(len(adj)):
        if colours[root] >= 0:
            continue
        colours[root] = 0
        queue = deque([root])
        while queue:
            a = queue.popleft()
            for b in sorted(adj[a]):
                if colours[b] < 0:
                    colours[b], parent[b] = 1 - colours[a], a
                    queue.append(b)
                elif colours[b] == colours[a]:
                    pa, pb = [a], [b]
                    while parent[pa[-1]] >= 0:
                        pa.append(parent[pa[-1]])
                    while pb[-1] not in pa:
                        pb.append(parent[pb[-1]])
                    cycle = pa[:pa.index(pb[-1]) + 1] + pb[-2::-1]
                    return None, cycle
    return colours, None


def core_and_peel(adj):
    degree = list(map(len, adj))
    heap = [i for i, d in enumerate(degree) if d <= 2]
    heapq.heapify(heap)
    removed, peel = set(), []
    while heap:
        a = heapq.heappop(heap)
        if a in removed:
            continue
        require(degree[a] <= 2, 'three-colour restoration degree')
        removed.add(a)
        peel.append(a)
        for b in adj[a]:
            if b not in removed:
                degree[b] -= 1
                if degree[b] == 2:
                    heapq.heappush(heap, b)
    return [i for i in range(len(adj)) if i not in removed], peel


def check_cycle(adj, cycle):
    require(isinstance(cycle, list) and len(cycle) >= 3 and len(cycle) % 2 == 1,
            'odd cycle length')
    require(all(type(v) is int and 0 <= v < len(adj) for v in cycle),
            'odd cycle vertex domain')
    require(len(set(cycle)) == len(cycle), 'simple odd cycle')
    require(all(cycle[(i + 1) % len(cycle)] in adj[a]
                for i, a in enumerate(cycle)), 'odd cycle edges')


def check_word(word, length):
    require(type(word) is str and len(word) == length and set(word) <= set('012'),
            'ternary word shape')


def certificate_rows(cert):
    require(type(cert) is dict and set(cert) == {'version', 'family', 'cores'},
            'certificate fields')
    require(type(cert['version']) is int and cert['version'] == 1,
            'certificate version')
    require(cert['family'] == 'polygon_difference_all_scales_508', 'family tag')
    require(type(cert['cores']) is list, 'core rows')
    rows = {}
    for row in cert['cores']:
        require(type(row) is dict and set(row) == {'n', 'pair', 'word'}, 'core fields')
        n, pair = row['n'], row['pair']
        require(type(n) is int and type(pair) is list and len(pair) == 2
                and all(type(v) is int for v in pair) and 0 <= pair[0] < pair[1],
                'core key domain')
        key = (n, *pair)
        require(key not in rows, 'duplicate core key')
        check_word(row['word'], len(row['word']) if type(row['word']) is str else -1)
        rows[key] = row['word']
    return rows


def verify(cert, compare_data=None, only_orders=None):
    rows = certificate_rows(cert)
    orders = [n for n in range(2, 32)
              if (n * (n - 1) if n % 2 else n * n // 2) + 1 <= 508]
    require(orders == list(range(2, 25)) + [26, 28, 30], 'admissible orders')
    if only_orders is not None:
        orders = only_orders
    reports, used, lower_witnesses = [], set(), []
    for n in orders:
        addresses, shells = geometry(n)
        m = len(addresses)
        proposal = None
        if compare_data is not None:
            proposal = json.loads((compare_data / f'{n}.json').read_text())
            require(proposal['n'] == n and proposal['addresses'] == addresses,
                    'proposal addresses')
            require(len(proposal['cases']) == len(shells), 'proposal shell count')
            require(len(proposal['coordinates']) == m, 'proposal coordinate count')
            r = ramanujan(n)
            for (i, j), p in zip(addresses, proposal['coordinates']):
                require(trace(p, n, r) == tuple(r[(i-k) % n] - r[(j-k) % n]
                                              for k in range(n)), 'proposal coordinates')
        hist = Counter()
        core_cases = core_vertices = max_odd = 0
        incidence, classification = [], []
        for index, (delta, edges) in enumerate(shells):
            adj = adjacency(m, edges)
            colour, cycle = bipartite_or_cycle(adj)
            key = (n, *edges[0])
            if cycle is None:
                chi = 2
                require(key not in rows, 'unneeded bipartite core row')
            else:
                chi = 3
                check_cycle(adj, cycle)
                max_odd = max(max_odd, len(cycle))
                lower_witnesses.append([n, edges[0], cycle])
                core, peel = core_and_peel(adj)
                colour = [-1] * m
                if core:
                    require(key in rows, 'missing core colouring')
                    word = rows[key]
                    check_word(word, len(core))
                    for a, c in zip(core, word):
                        colour[a] = int(c)
                    used.add(key)
                    core_cases += 1
                    core_vertices += len(core)
                else:
                    require(key not in rows, 'unneeded empty core row')
                for a in reversed(peel):
                    forbidden = {colour[b] for b in adj[a]}
                    available = [c for c in range(3) if c not in forbidden]
                    require(bool(available), 'colour restoration')
                    colour[a] = available[0]
            require(all(type(c) is int and 0 <= c < chi for c in colour),
                    'full colour domain')
            require(all(colour[a] != colour[b] for a, b in edges),
                    'full positive edge colouring')
            hist[chi] += 1
            incidence.append([edges[0], edges])
            classification.append([edges[0], len(edges), chi])
            if proposal is not None:
                p = proposal['cases'][index]
                require(p['edges'] == edges, 'complete proposal shell incidence')
                require(trace(p['delta'], n, r) == delta, 'proposal norm value')
                require(p['chi'] == chi, 'proposal chromatic number')
                check_word(p['colour'], m)
                require(all(p['colour'][a] != p['colour'][b] for a, b in edges),
                        'proposal positive colouring')
        reports.append({'n': n, 'vertices': m, 'pair_checks': m * (m - 1) // 2,
                        'shells': len(shells), 'chi2': hist[2], 'chi3': hist[3],
                        'edge_range': [min(len(e) for _, e in shells),
                                       max(len(e) for _, e in shells)],
                        'core_cases': core_cases, 'core_vertices': core_vertices,
                        'maximum_odd_cycle': max_odd,
                        'incidence_sha256': digest([n, addresses, incidence]),
                        'classification_sha256': digest(classification)})
    if only_orders is None:
        require(used == set(rows), 'exact core certificate coverage')
    return {'verified': True, 'record_improvement': False, 'orders': reports,
            'polygon_orders': len(reports), 'distance_shells': sum(r['shells'] for r in reports),
            'bipartite_shells': sum(r['chi2'] for r in reports),
            'three_chromatic_shells': sum(r['chi3'] for r in reports),
            'pair_checks': sum(r['pair_checks'] for r in reports),
            'core_words': sum(r['core_cases'] for r in reports),
            'core_colour_symbols': sum(r['core_vertices'] for r in reports),
            'maximum_vertices': max(r['vertices'] for r in reports),
            'odd_cycles_sha256': digest(lower_witnesses),
            'certificate_sha256': digest(cert)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    ap.add_argument('--compare-data', type=Path)
    ap.add_argument('--check-expected', action='store_true')
    ap.add_argument('--out', type=Path)
    args = ap.parse_args()
    report = verify(json.loads(args.certificate.read_text()), args.compare_data)
    if args.check_expected:
        require(report == json.loads((HERE / 'expected.json').read_text()),
                'expected report')
    if args.out:
        args.out.write_text(dump(report))
    print(dump(report), end='')


if __name__ == '__main__':
    main()
