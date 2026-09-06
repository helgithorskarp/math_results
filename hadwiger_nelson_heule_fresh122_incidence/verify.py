#!/usr/bin/env python3
"""Definition-level check; no producer or solver import.

Points are sparse dictionaries keyed by squarefree radicands. Squared
distances use diagonal terms and twice each unordered off-diagonal term,
reducing sqrt(a*b) by gcd(a,b). All operations use unbounded integers after
an independently derived common denominator. Components use union-find;
their sole cycle is recovered from a spanning tree and its non-tree edge.
"""
import argparse
from collections import Counter, deque
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd, lcm
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
RADICALS = (1, 3, 5, 15, 11, 33, 55, 165)


def check(test, message):
    if not test:
        raise ValueError(message)


def rational(row):
    check(len(row) == 2 and all(len(axis) == 8 for axis in row), 'point shape')
    return tuple({r: Fraction(c) for r, c in zip(RADICALS, axis) if Fraction(c)} for axis in row)


def scaled(point, denominator):
    out = []
    for axis in point:
        row = {}
        for r, c in axis.items():
            v = c * denominator
            check(v.denominator == 1, 'exact scaling')
            row[r] = v.numerator
        out.append(row)
    return out


def squared_distance(p, q):
    result = Counter()
    for a, b in zip(p, q):
        delta = {r: a.get(r, 0)-b.get(r, 0) for r in a.keys() | b.keys()}
        terms = sorted((r, c) for r, c in delta.items() if c)
        for r, c in terms:
            result[1] += c*c*r
        for (r, c), (s, d) in combinations(terms, 2):
            common = gcd(r, s)
            result[r*s//(common*common)] += 2*c*d*common
    check(set(result) <= set(RADICALS), 'closed radical basis')
    return tuple(result[r] for r in RADICALS)


def hist(values):
    c = Counter(values)
    return {str(v): c[v] for v in sorted(c)}


def compare_certificate(actual, expected):
    check(actual == expected, 'entrywise certificate equality')


def audit(out, transcript=None):
    start = time.monotonic()
    plan = json.loads((HERE/'plan.json').read_text())
    for path, digest in plan['inputs'].items():
        check(sha256((REPO/path).read_bytes()).hexdigest() == digest, ('input identity', path))
    old = json.loads((REPO/'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json').read_text())
    old_keys = sorted(map(int, old['coordinates']))
    check(old_keys == list(range(553)), 'union coordinate labels')
    old_labels = [v for v in old_keys if '510' in old['provenance'][v]]
    Hrat = [rational(old['coordinates'][str(v)]) for v in old_labels]
    rows = json.loads((REPO/'hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json').read_text())
    ids = [r['centre_index'] for r in rows]
    Qrat = [rational(r['coordinates']) for r in rows]
    check(len(ids) == 122 and ids == sorted(set(ids)), 'fixed fresh domain')
    check(len(Hrat) == 510, 'fixed old domain')
    D = lcm(*(v.denominator for p in Hrat+Qrat for a in p for v in a.values()))
    H = [scaled(p, D) for p in Hrat]
    Q = [scaled(p, D) for p in Qrat]
    keys = [tuple(tuple(sorted(a.items())) for a in p) for p in H+Q]
    check(len(set(keys)) == 632, 'all points distinct')
    large = {v for v, p in enumerate(H) if all(all(r % 5 for r in a) for a in p)}
    check(len(large) == 375, 'independent large-block classification')
    unit = (D*D, 0, 0, 0, 0, 0, 0, 0)
    # Direct hand-computable controls include a radical cross term.
    controls = [([{}, {}], [{1: D}, {}], unit),
                ([{}, {}], [{3: D//2}, {1: D//2}], unit),
                ([{}, {}], [{3: D, 5: D}, {}], (8*D*D, 0, 0, 2*D*D, 0, 0, 0, 0)),
                ([{11: D}, {5: D}], [{11: D}, {5: D}], (0,)*8)]
    for p, q, expected in controls:
        check(squared_distance(p, q) == expected, 'exact norm control')
    norm_hash = sha256()
    source = transcript.open() if transcript is not None else None
    checks = 0
    def record(kind, a, b, n):
        nonlocal checks
        line = f'{kind} {a} {b} ' + ' '.join(map(str, n)) + '\n'
        norm_hash.update(line.encode('ascii'))
        if source is not None:
            check(source.readline() == line, ('entrywise exact norm', kind, a, b))
        checks += 1
    edges = []
    for i in range(122):
        for j in range(i+1, 122):
            n = squared_distance(Q[i], Q[j])
            record('F', ids[i], ids[j], n)
            if n == unit:
                edges.append([ids[i], ids[j]])
    attach = {}
    types = {}
    for i in range(122):
        neighbors = []
        for v in range(510):
            n = squared_distance(Q[i], H[v])
            record('H', ids[i], v, n)
            if n == unit:
                neighbors.append(v)
        row = rows[i]
        check(neighbors == row['neighbors'] and len(neighbors) == row['degree'] >= 4, ('complete old neighbors', ids[i]))
        check(len(row['witness']) == 3 and row['witness'] == sorted(set(row['witness'])) and set(row['witness']) <= set(neighbors), 'old witness')
        attach[ids[i]] = set(neighbors)
        Lcount = len(set(neighbors) & large)
        types[ids[i]] = 'L' if Lcount == len(neighbors) else 'S' if Lcount == 0 else 'M'
    if source is not None:
        check(source.read() == '', 'complete transcript consumed')
        source.close()
    check(checks == 69601, 'full comparison domain')
    parent = {v: v for v in ids}
    forest = {v: [] for v in ids}
    adjacency = {v: [] for v in ids}
    def root(v):
        while parent[v] != v:
            v = parent[v]
        return v
    back = []
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
        ru, rv = root(u), root(v)
        if ru == rv:
            back.append((u, v))
        else:
            parent[rv] = ru
            forest[u].append(v)
            forest[v].append(u)
    groups = {}
    for v in ids:
        groups.setdefault(root(v), []).append(v)
    components = []
    for group in sorted(groups.values(), key=lambda p: p[0]):
        ns = set.union(*(attach[v] for v in group))
        ne = sum(len(adjacency[v]) for v in group)//2
        components.append({'centres': group, 'edges': ne, 'cycle_rank': ne-len(group)+1,
                           'types': hist(types[v] for v in group),
                           'old_L_neighbors': sorted(ns & large),
                           'old_S_neighbors': sorted(ns-large)})
    check(len(back) == 1, 'exactly one cycle in full graph')
    u, v = back[0]
    todo = deque([u])
    prev = {u: None}
    while v not in prev:
        z = todo.popleft()
        for w in forest[z]:
            if w not in prev:
                prev[w] = z
                todo.append(w)
    cycle = [v]
    while cycle[-1] != u:
        cycle.append(prev[cycle[-1]])
    alternatives = []
    for direction in (cycle, list(reversed(cycle))):
        k = direction.index(min(cycle))
        alternatives.append(direction[k:]+direction[:k])
    cycle = min(alternatives)
    expected = {'centre_ids': ids, 'fresh_edges': edges, 'components': components,
                'attachment_types': {str(v): types[v] for v in ids}, 'unique_cycle': cycle}
    actual = json.loads((HERE/'certificate.json').read_text())
    compare_certificate(actual, expected)
    check(cycle == [1239, 1370, 1522, 1371], 'precise unique even cycle')
    mixed = sorted(v for v in ids if types[v] == 'M')
    check(mixed == [170, 436, 1239, 1527], 'all mixed points')
    check(all(attach[v] & large == {0} for v in mixed), 'only old origin across mixed interface')
    check(all('L' not in (types[u], types[v]) or types[u] == types[v] == 'L' for u, v in edges), 'fresh large-block separation')
    summary = {'status': 'COMPLETE EXACT FIXED122 MUTUAL INCIDENCE', 'common_denominator': D,
               'old_vertices': 510, 'fresh_vertices': 122, 'fresh_pair_checks': 7381,
               'attachment_pair_checks': 62220, 'fresh_edges': len(edges),
               'old_attachments': sum(map(len, attach.values())),
               'fresh_degree_histogram': hist(map(len, adjacency.values())),
               'attachment_type_histogram': hist(types.values()),
               'edge_type_histogram': hist(''.join(sorted((types[u], types[v]))) for u, v in edges),
               'component_order_histogram': hist(map(len, groups.values())), 'components': len(groups),
               'norm_stream_sha256': norm_hash.hexdigest(), 'native_colouring_queries': 0,
               'record_improvement': False}
    check(summary == json.loads((HERE/'result.json').read_text()), 'full summary equality')
    # Four-colour instances of the even-cycle lemma: all 6^4 choices of
    # two-element lists on the unique cycle, checked by direct 4^4 assignments.
    pair_lists = list(combinations(range(4), 2))
    good_cycle_colours = [c for c in product(range(4), repeat=4) if all(c[i] != c[(i+1)%4] for i in range(4))]
    list_checks = 0
    for lists in product(pair_lists, repeat=4):
        check(any(all(c[i] in lists[i] for i in range(4)) for c in good_cycle_colours), 'two-list cycle control')
        list_checks += 1
    malformed = []
    bad = deepcopy(actual); bad['fresh_edges'].pop(); malformed.append(bad)
    bad = deepcopy(actual); bad['fresh_edges'].append([35, 90]); malformed.append(bad)
    bad = deepcopy(actual); bad['attachment_types']['170'] = 'S'; malformed.append(bad)
    bad = deepcopy(actual); bad['components'][0]['centres'] = []; malformed.append(bad)
    bad = deepcopy(actual); bad['unique_cycle'][1], bad['unique_cycle'][2] = bad['unique_cycle'][2], bad['unique_cycle'][1]; malformed.append(bad)
    for bad in malformed:
        try:
            compare_certificate(bad, expected)
        except ValueError:
            continue
        raise ValueError('malformed certificate accepted')
    result = {'status': 'VERIFIED EXACT INCIDENCE AND EVEN UNICYCLIC DECOMPOSITION',
              'exact_norm_vectors_checked': checks, 'entrywise_local_transcript': source is not None,
              'norm_stream_sha256': norm_hash.hexdigest(), 'unique_cycle': cycle,
              'sparse_norm_controls': len(controls), 'four_colour_two_list_cycle_cases': list_checks,
              'malformed_certificates_rejected': len(malformed),
              'independent_author_review_claimed': False, 'native_colouring_queries': 0,
              'record_improvement': False, 'seconds': time.monotonic()-start}
    out.mkdir(parents=True, exist_ok=True)
    (out/'verification.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--transcript', type=Path)
    args = ap.parse_args()
    audit(args.out, args.transcript)
