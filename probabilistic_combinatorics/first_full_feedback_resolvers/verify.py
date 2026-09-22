#!/usr/bin/env python3
"""Exact corroboration for PROOF.md; Python 3.11+, standard library only.

No test below proves an asymptotic limit. BFS defines the feedback independently
of the code proxy. Exhaustive rational sums check the finite probability algebra.
"""
import argparse
from collections import Counter, deque
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from math import comb, prod
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def graph(n, edges):
    require(isinstance(n, int) and n >= 1, "positive order required")
    adj = [0] * n
    for a, b in edges:
        require(0 <= a < n and 0 <= b < n and a != b, "invalid edge")
        require(not (adj[a] >> b & 1), "duplicate edge")
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    return tuple(adj)


def vertices(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask -= bit


def distances(adj):
    rows = []
    for source in range(len(adj)):
        ds = [-1] * len(adj)
        ds[source] = 0
        queue = deque([source])
        while queue:
            v = queue.popleft()
            for w in vertices(adj[v]):
                if ds[w] == -1:
                    ds[w] = ds[v] + 1
                    queue.append(w)
        rows.append(ds)
    return rows


def feedback(adj, ds, v):
    require(0 <= v < len(adj), "invalid probe")
    if -1 in ds[v]:
        return None
    out = []
    for x in range(len(adj)):
        if x == v:
            out.append(1 << v)
        else:
            out.append(sum(1 << u for u in vertices(adj[v])
                           if ds[u][x] == ds[v][x] - 1))
    return tuple(out)


def data(adj, v):
    d = adj[v]
    ts = [x for x in range(len(adj)) if x != v and not (d >> x & 1)]
    codes = [d & adj[x] for x in ts]
    zeros = [x for x, c in zip(ts, codes) if c == 0]
    singles = sum(c.bit_count() == 1 for c in codes)
    large = [c for c in codes if c.bit_count() >= 2]
    saturation = all(adj[z] & adj[u] for z in zeros for u in vertices(d))
    h = (d.bit_count() >= 2 and len(large) == len(set(large))
         and d not in large and saturation and (bool(large) or bool(zeros)))
    return singles, len(zeros), h, codes


def weight(k, total, p):
    return p ** k * (1 - p) ** (total - k)


def row_probabilities(neighborhoods, p):
    """Direct enumeration, no independence of overlapping neighborhoods."""
    require(0 < p < 1, "probability must be strictly between zero and one")
    require(neighborhoods and all(isinstance(d, int) and d >= 0
                                 for d in neighborhoods), "invalid neighborhoods")
    universe = 0
    for d in neighborhoods:
        universe |= d
    bits = list(vertices(universe))
    out = Counter()
    for chosen in range(1 << len(bits)):
        mask = sum(1 << bits[j] for j in range(len(bits)) if chosen >> j & 1)
        counts = tuple((mask & d).bit_count() for d in neighborhoods)
        out[counts] += weight(chosen.bit_count(), len(bits), p)
    require(sum(out.values()) == 1, "row mass")
    return out


def mark_coefficients(rows):
    out = Counter()
    for counts, probability in rows.items():
        if 1 not in counts:
            mask = sum(1 << i for i, count in enumerate(counts) if count == 0)
            out[mask] += probability
    return out


def partitions(items):
    if not items:
        yield []
        return
    first, *rest = items
    for tail in partitions(rest):
        yield [1 << first] + tail
        for j in range(len(tail)):
            yield tail[:j] + [tail[j] | (1 << first)] + tail[j + 1:]


def falling(m, k):
    return prod(range(m - k + 1, m + 1)) if 0 <= k <= m else 0


def partition_coefficient(coefficients, m, wanted):
    """Exact coefficient for marks in {0,1}; PROOF.md Section 4."""
    answer = F(0)
    for blocks in partitions(list(vertices(wanted))):
        h = len(blocks)
        if h <= m:
            answer += (falling(m, h) * coefficients[0] ** (m - h)
                       * prod(coefficients[b] for b in blocks))
    return answer


def direct_coefficient(coefficients, m, wanted):
    """Independent labelled-target sum; no partition formula."""
    answer = F(0)
    for events in product(sorted(coefficients), repeat=m):
        used = 0
        legal = True
        for mark in events:
            if used & mark or mark & ~wanted:
                legal = False
                break
            used |= mark
        if legal and used == wanted:
            answer += prod(coefficients[e] for e in events)
    return answer


def conditional_proxy(d, m, p, k):
    require(d >= 0 and m >= 0 and k in (0, 1), "invalid proxy parameters")
    b0 = (1 - p) ** d
    b1 = d * p * (1 - p) ** (d - 1) if d else F(0)
    b = 1 - b0 - b1
    return b ** m if k == 0 else (m * b0 * b ** (m - 1) if m else F(0))


def exact_one_probe(n, p, k):
    return sum(comb(n - 1, d) * weight(d, n - 1, p)
               * conditional_proxy(d, n - 1 - d, p, k) for d in range(n))


def graph_audit():
    counts = Counter()
    by_edge = {}
    examples = {}
    digest = sha256()
    for n in range(2, 7):
        pairs = list(combinations(range(n), 2))
        totals = [[0, 0] for _ in range(len(pairs) + 1)]
        for mask in range(1 << len(pairs)):
            edges = [e for j, e in enumerate(pairs) if mask >> j & 1]
            adj = graph(n, edges)
            ds = distances(adj)
            counts['labelled_graphs'] += 1
            connected = -1 not in ds[0]
            counts['connected_graphs'] += connected
            record = []
            for v in range(n):
                x, z, h, codes = data(adj, v)
                f0, f1 = (x == 0 and z == 0), (x == 0 and z == 1)
                response = feedback(adj, ds, v)
                resolves = response is not None and len(set(response)) == n
                ecc = max(ds[v]) if connected else -1
                counts['probe_checks'] += 1
                counts['resolving_probes'] += resolves
                require(not resolves or x == 0, 'singleton defect missed')
                if x == 0 and h:
                    require(resolves == (z <= 1), 'deterministic comparison')
                    if resolves:
                        require(ecc == z + 2, 'eccentricity mark')
                    counts['auxiliary_comparisons'] += 1
                if resolves != (f0 or f1):
                    tag = 'false_positive' if not resolves else 'false_negative'
                    counts['proxy_' + tag] += 1
                    examples.setdefault(tag, dict(n=n, edges=edges, probe=v,
                                                  singletons=x, zeros=z, eccentricity=ecc))
                if resolves and ecc == 3:
                    examples.setdefault('distance_three', dict(n=n, edges=edges, probe=v))
                    counts['eccentricity_three_resolvers'] += 1
                if v == 0:
                    totals[len(edges)][0] += f0
                    totals[len(edges)][1] += f1
                record.append([v, x, z, int(h), int(resolves), ecc])
            digest.update(json.dumps([n, mask, record], separators=(',', ':')).encode())
        by_edge[n] = totals
    for n, totals in by_edge.items():
        for p in (F(1, 3), F(1, 2), F(2, 3)):
            for k in (0, 1):
                direct = sum(t[k] * weight(j, comb(n, 2), p)
                             for j, t in enumerate(totals))
                require(direct == exact_one_probe(n, p, k), 'degree mixture')
                counts['rational_graph_probabilities'] += 1
    require('false_positive' in examples, 'proxy needs a finite warning example')
    return dict(counts), examples, digest.hexdigest()


def algebra_audit():
    counts = Counter()
    records = []
    probabilities = (F(1, 4), F(1, 2), F(2, 3))
    for d in range(0, 7):
        for p in probabilities:
            subsets = {s: weight(s.bit_count(), d, p) for s in range(1 << d)}
            b0 = subsets[0]
            b1 = sum(w for s, w in subsets.items() if s.bit_count() == 1)
            require(b0 == (1-p)**d, 'empty-code formula')
            require(b1 == (d*p*(1-p)**(d-1) if d else 0), 'singleton formula')
            collision = sum(w*w for s, w in subsets.items() if s.bit_count() >= 2)
            formula = (1-p)**(2*d) * ((1+(p/(1-p))**2)**d-1-d*(p/(1-p))**2)
            require(collision == formula, 'large-code collision identity')
            counts['collision_identities'] += 1
            if d >= 2:
                direct_beta = sum(w for s, w in subsets.items()
                                  if s & 1 and s.bit_count() != 1) / (1-b1)
                beta = p*(1-(1-p)**(d-1))/(1-b1)
                require(direct_beta == beta, 'conditional edge marginal')
                counts['conditional_edge_marginals'] += 1
            if d <= 4:
                for m in range(0, 4):
                    for k in (0, 1):
                        direct = sum(prod(subsets[s] for s in choices)
                                     for choices in product(subsets, repeat=m)
                                     if all(s.bit_count() != 1 for s in choices)
                                     and sum(s == 0 for s in choices) == k)
                        require(direct == conditional_proxy(d, m, p, k), 'one-probe count')
                        counts['conditional_proxy_sums'] += 1
    for di in range(0, 5):
        for dj in range(0, 5):
            for overlap in range(min(di, dj) + 1):
                left = (1 << di) - 1
                right = ((1 << overlap) - 1) | (((1 << (dj-overlap)) - 1) << di)
                for p in probabilities:
                    rows = row_probabilities((left, right), p)
                    direct = sum(w for ks, w in rows.items() if max(ks) <= 1)
                    q = 1-p
                    formula = q**(di+dj-overlap)*((1+(di-overlap)*p/q)
                               *(1+(dj-overlap)*p/q)+overlap*p/q)
                    require(direct == formula, 'overlap formula')
                    counts['overlap_identities'] += 1
    systems = ((0,), (3,), (3, 12), (7, 14), (7, 7), (3, 5, 6),
               (7, 14, 28), (1, 3, 15), (0, 3, 12))
    for system in systems:
        for p in probabilities:
            co = mark_coefficients(row_probabilities(system, p))
            for m in range(0, 5):
                for wanted in range(1 << len(system)):
                    a = partition_coefficient(co, m, wanted)
                    b = direct_coefficient(co, m, wanted)
                    require(a == b, 'partition coefficient')
                    records.append([list(system), str(p), m, wanted, str(a)])
                    counts['joint_partition_checks'] += 1
    for d in (2, 3):
        allowed = [s for s in range(1 << d) if s.bit_count() != 1]
        for m in range(1, 4):
            target_edges = list(combinations(range(m), 2))
            for tail in product(allowed, repeat=m-1):
                codes = (0,) + tail  # designated zero-code target is 0
                for b in range(d):
                    support = {j for j, code in enumerate(codes) if code >> b & 1}
                    for p in (F(1, 3), F(1, 2)):
                        direct = F(0)
                        for mask in range(1 << len(target_edges)):
                            selected = {edge for j, edge in enumerate(target_edges)
                                        if mask >> j & 1}
                            if all((0,j) not in selected for j in support):
                                direct += weight(mask.bit_count(), len(target_edges), p)
                        require(direct == (1-p)**len(support), 'untouched path edges')
                        counts['zero_target_path_identities'] += 1
    return dict(counts), sha256(json.dumps(records, separators=(',', ':')).encode()).hexdigest()


def fixtures_and_rejections():
    fixtures = []
    for n, edges, name in [
        (8, [(a, b) for a, b in combinations(range(8), 2)
             if (a ^ b).bit_count() == 1], 'three_cube'),
        (4, [(0, 1), (0, 2)], 'disconnected_proxy'),
        (6, list(combinations(range(6), 2)), 'complete'),
        (6, [(0, x) for x in range(1, 6)], 'star'),
        (6, [(x, (x+1) % 6) for x in range(6)], 'six_cycle'),
        (6, [(0,1),(0,2),(0,3),(1,4),(2,4),(1,5),(2,5)], 'repeated_large_code'),
    ]:
        adj = graph(n, edges)
        ds = distances(adj)
        statuses = []
        for v in range(n):
            out = feedback(adj, ds, v)
            statuses.append(int(out is not None and len(set(out)) == n))
        if name == 'three_cube':
            require(sum(statuses) == 8 and all(data(adj,v)[:3] == (0, 1, True)
                                             and max(ds[v]) == 3 for v in range(n)),
                    'cube distance-three fixture')
        if name == 'disconnected_proxy':
            require(data(adj,0)[:2] == (0,1) and not statuses[0], 'finite proxy error')
        if name == 'repeated_large_code':
            require(data(adj,0)[:2] == (0,0) and not statuses[0]
                    and -1 not in ds[0], 'connected proxy error')
        fixtures.append(dict(name=name, resolving=statuses))
    tests = [lambda: graph(0, []), lambda: graph(2, [(0,0)]),
             lambda: graph(2, [(0,2)]), lambda: graph(2, [(0,1),(1,0)]),
             lambda: row_probabilities((3,), F(1)),
             lambda: row_probabilities((-1,), F(1,2)),
             lambda: conditional_proxy(2, -1, F(1,2), 0),
             lambda: conditional_proxy(2, 3, F(1,2), 2)]
    for test in tests:
        try:
            test()
        except ValueError:
            continue
        raise ValueError('malformed input accepted')
    return fixtures, len(tests)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='compare with EXPECTED.json')
    args = parser.parse_args()
    gc, examples, gh = graph_audit()
    ac, ah = algebra_audit()
    fixtures, rejects = fixtures_and_rejections()
    result = dict(graph=gc, graph_digest=gh, finite_examples=examples,
                  algebra=ac, algebra_digest=ah, fixtures=fixtures,
                  rejected_inputs=rejects)
    encoded = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        require(json.loads(Path(__file__).with_name('EXPECTED.json').read_text()) == result,
                'expected-output mismatch')
        print('PASS: exact BFS, rare-event proxy, overlap, and marked coefficients')
        print('record_sha256=' + sha256(encoded.encode()).hexdigest())
    else:
        print(encoded, end='')


if __name__ == '__main__':
    main()
