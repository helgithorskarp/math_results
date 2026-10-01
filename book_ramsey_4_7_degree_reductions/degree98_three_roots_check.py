"""Exact local reduction for 98-edge histogram(3,18,1).
Actual author six-books-1, researcher, 2026-10-01. Standalone standard library.
"""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import json
import argparse
from hashlib import sha256
from random import Random

PAIRS = list(combinations(range(8), 2))
PERMS = [p + q + r for p in ((0, 1), (1, 0)) for q in ((2,),)
         for r in permutations(range(3, 8))]

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def matrix(mask):
    return [[0 if i == j else (mask >> PAIRS.index(tuple(sorted((i, j))))) & 1
             for j in range(8)] for i in range(8)]

def canonical(j):
    return min(sum(j[p[i]][p[k]] << bit for bit, (i, k) in enumerate(PAIRS))
               for p in PERMS)

def cubic_graphs():
    # Decide each remaining star completely. Fixed b-c edge; b-z,c-z blue.
    j = [[0] * 8 for _ in range(8)]
    j[0][1] = j[1][0] = 1
    demand = [2, 2, 3, 3, 3, 3, 3, 3]
    def rec(i):
        if i == 8:
            need(not any(demand), 'cubic terminal demand')
            yield [row[:] for row in j]
            return
        allowed = [k for k in range(i + 1, 8) if demand[k] and not j[i][k]
                   and not (i < 2 and k == 2)]
        for neighbors in combinations(allowed, demand[i]):
            value = demand[i]
            demand[i] = 0
            for k in neighbors:
                j[i][k] = j[k][i] = 1
                demand[k] -= 1
            if all(demand[k] <= sum(demand[l] > 0 for l in range(i + 1, 8) if l != k)
                   for k in range(i + 1, 8)):
                yield from rec(i + 1)
            for k in neighbors:
                j[i][k] = j[k][i] = 0
                demand[k] += 1
            demand[i] = value
    yield from rec(0)

def weighted_graphs(cap, initial):
    demand = initial[:]
    e = [[0] * 8 for _ in range(8)]
    def rec():
        i = next((v for v in range(8) if demand[v]), None)
        if i is None:
            yield [row[:] for row in e]
            return
        allowed = [k for k in range(i + 1, 8) if demand[k] and cap[i][k]]
        limits = [min(cap[i][k], demand[k]) for k in allowed]
        def stars(index, left):
            if index == len(allowed):
                if left == 0:
                    yield []
                return
            for value in range(max(0, left - sum(limits[index + 1:])), min(left, limits[index]) + 1):
                for suffix in stars(index + 1, left - value):
                    yield [value] + suffix
        total = demand[i]
        for weights in stars(0, total):
            demand[i] = 0
            for k, w in zip(allowed, weights):
                e[i][k] = e[k][i] = w
                demand[k] -= w
            if all(demand[k] <= sum(min(cap[k][l], demand[l]) for l in range(i + 1, 8) if l != k)
                   for k in range(i + 1, 8)):
                yield from rec()
            for k, w in zip(allowed, weights):
                e[i][k] = e[k][i] = 0
                demand[k] += w
            demand[i] = total
    yield from rec()


TRIPLES = [t for t in combinations(range(8), 3) if 0 <= (0 in t) + (1 in t) - (2 in t) <= 1]
ROW_EDGES = [tuple(PAIRS.index(p) for p in combinations(t, 2)) for t in TRIPLES]
ROW_MASKS = [sum(1 << i for i in t) for t in TRIPLES]

def incidence_sets(target):
    remaining = list(target)
    used = [0] * len(TRIPLES)
    def rec(available):
        if not any(remaining):
            need(sum(used) == 13, 'thirteen rows at terminal')
            yield tuple(mask for mask, value in zip(ROW_MASKS, used) for _ in range(value))
            return
        live = [t for t in available if all(remaining[p] for p in ROW_EDGES[t])]
        supports = [[] for _ in PAIRS]
        for t in live:
            for p in ROW_EDGES[t]:
                supports[p].append(t)
        if any(remaining[p] and not supports[p] for p in range(len(PAIRS))):
            return
        p = min((p for p in range(len(PAIRS)) if remaining[p]),
                key=lambda p: (len(supports[p]), -remaining[p], p))
        selected = supports[p]
        others = [t for t in live if t not in selected]
        def assign(index, left):
            if index == len(selected):
                if not left:
                    yield from rec(others)
                return
            t = selected[index]
            cap = min(left, *(remaining[q] for q in ROW_EDGES[t]))
            future_capacity = sum(min(remaining[q] for q in ROW_EDGES[r]) for r in selected[index + 1:])
            for value in range(max(0, left - future_capacity), cap + 1):
                used[t] = value
                for q in ROW_EDGES[t]:
                    remaining[q] -= value
                yield from assign(index + 1, left - value)
                for q in ROW_EDGES[t]:
                    remaining[q] += value
                used[t] = 0
        yield from assign(0, remaining[p])
    yield from rec(list(range(len(TRIPLES))))

def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()

def positive_rows():
    rows = [(0, 3, 4), (1, 5, 6), (0, 2, 3), (0, 2, 4), (0, 2, 7),
            (1, 2, 5), (1, 2, 6), (1, 2, 7)]
    rows += [tuple(sorted((3 + i, 3 + (i + 1) % 5, 3 + (i + 2) % 5))) for i in range(5)]
    return rows

def root_census():
    pairs = list(combinations(range(4), 2))
    classes = {}
    masks = []
    for mask in range(64):
        adj = [[0] * 4 for _ in range(4)]
        for bit, (i, j) in enumerate(pairs):
            adj[i][j] = adj[j][i] = (mask >> bit) & 1
        f = [-2 + 2 * (sum(adj[i][:3]) - adj[i][3]) for i in range(3)]
        if min(f) < 0:
            continue
        k = sum(adj[3][:3])
        shape = 'P3' if sum(sum(adj[i][:3]) for i in range(3)) == 4 else 'K3'
        key = min(sum(adj[p[i]][p[j]] << bit for bit, (i, j) in enumerate(pairs))
                  for perm in permutations(range(3)) for p in [perm + (3,)])
        masks.append([mask, key])
        if key not in classes:
            classes[key] = {'mask': key, 'shape': shape, 'k': k,
                            'sum_qA': sum(f), 'qz': 2 + 2 * k,
                            'qB': 24 - sum(f) - 2 - 2 * k, 'multiplicity': 0}
        classes[key]['multiplicity'] += 1
    need(len(masks) == 14 and len(classes) == 6, 'complete four-root census')
    p3 = [[e, g, r, g - e, 2 + e + r] for e in range(2) for g in range(e, 2) for r in range(2)]
    k2 = [[g, r, 2 + g, 4 + r] for g in range(2) for r in range(2)]
    need(all(p[-1] > p[-2] for p in p3 + k2) and 3 < 7, 'incidence gap tables')
    return {'tested_masks': 64, 'eligible_masks': masks,
            'classes': [classes[k] for k in sorted(classes)],
            'P3_parameters': p3, 'K3_k2_parameters': k2, 'K3_k3_incidence': [3, 7]}

def baseline():
    rows = Path(__file__).with_name('baseline21.rows').read_text().split()
    need(len(rows) == 21 and all(len(r) == 21 and set(r) <= {'0', '1'} for r in rows), 'baseline format')
    red = [{j for j, bit in enumerate(r) if bit == '1'} for r in rows]
    need(all(i not in red[i] and all((j in red[i]) == (i in red[j]) for j in range(21))
             for i in range(21)), 'baseline symmetry')
    blue = [set(range(21)) - r - {i} for i, r in enumerate(red)]
    maxima = [max(len(n[i] & n[j]) for i, j in combinations(range(21), 2) if j in n[i]) for n in (red, blue)]
    need(Counter(map(len, red)) == {8: 4, 9: 16, 10: 1} and maxima == [3, 6], 'baseline pages')
    return {'vertices': 21, 'red_edges': sum(map(len, red)) // 2,
            'red_page_maximum': maxima[0], 'blue_page_maximum': maxima[1]}

def signed_controls(masks):
    """Literal host identities on 22 signed, generally invalid page instances."""
    row_patterns = positive_rows()
    gram_entries = outside_rows = incident_rows = 0
    hashes = []
    for number, mask in enumerate(masks):
        j = matrix(mask)
        red = [set() for _ in range(22)]
        def edge(i, k):
            red[i].add(k)
            red[k].add(i)
        for i in range(1, 9):
            edge(0, i)
        for i, k in PAIRS:
            if j[i][k]:
                edge(i + 1, k + 1)
        for v, row in enumerate(row_patterns, 9):
            for i in row:
                edge(v, i + 1)
        w = [set() for _ in range(13)]
        for i in range(13):
            w[i] = {(i + d) % 13 for d in (1, 2, 3, -1, -2, -3)}
        rng = Random(1598 + number)
        for _ in range(50):
            edges = [(i, k) for i in range(13) for k in w[i] if i < k]
            (a, b), (c, d) = rng.sample(edges, 2)
            if len({a, b, c, d}) < 4 or c in w[a] or d in w[b]:
                continue
            for i, k in ((a, b), (c, d)):
                w[i].remove(k)
                w[k].remove(i)
            for i, k in ((a, c), (b, d)):
                w[i].add(k)
                w[k].add(i)
        for i in range(13):
            for k in w[i]:
                if i < k:
                    edge(i + 9, k + 9)
        degrees = list(map(len, red))
        need(degrees == [8, 8, 8, 10] + [9] * 18, 'signed histogram')
        blue = [set(range(22)) - n - {i} for i, n in enumerate(red)]
        f = [[0] * 22 for _ in range(22)]
        for i, k in combinations(range(22), 2):
            f[i][k] = f[k][i] = 3 - len(red[i] & red[k]) if k in red[i] else 6 - len(blue[i] & blue[k])
        need(not any(f[0]), 'signed saturated root')
        need(any(value < 0 for row in f for value in row), 'signed control is not a valid host')
        for i in range(22):
            sa = len(red[i] & {0, 1, 2})
            eps = int(3 in red[i])
            need(sum(f[i]) == 2 - (degrees[i] - 10) ** 2 + 2 * (sa - eps), 'literal incident identity')
            incident_rows += 1
        for i in range(8):
            for k in range(8):
                actual = sum(i in row and k in row for row in row_patterns)
                predicted = degrees[i + 1] - 4 if i == k else (
                    2 if j[i][k] else degrees[i + 1] + degrees[k + 1] - 15
                ) - sum(j[i][l] * j[k][l] for l in range(8)) - f[i + 1][k + 1]
                need(actual == predicted, 'literal local Gram identity')
                gram_entries += 1
        for i in range(9, 22):
            delta = int(1 in red[i]) + int(2 in red[i]) - int(3 in red[i])
            need(sum(f[i][k] for k in range(1, 9)) == 1 + delta, 'literal cross defect row')
            need(sum(f[i][k] for k in range(9, 22)) == delta, 'literal outside defect row')
            outside_rows += 1
        hashes.append(sha256(encode([sorted(n) for n in red])).hexdigest())
    return {'graphs': len(masks), 'incident_rows': incident_rows, 'Gram_entries': gram_entries,
            'outside_defect_rows': outside_rows, 'signed_graph_hashes': hashes}

def build(include_matrices=False):
    need(len(TRIPLES) == 41, 'all allowed binary row types')
    control = positive_rows()
    target = [sum(i in row and k in row for row in control) for i, k in PAIRS]
    controls = list(incidence_sets(target))
    wanted = tuple(sorted(sum(1 << i for i in row) for row in control))
    need(any(tuple(sorted(rows)) == wanted for rows in controls), 'positive row decomposition control')
    groups = Counter()
    for j in cubic_graphs():
        need(all(sum(row) == 3 for row in j), 'cubic generation')
        groups[canonical(j)] += 1
    need(sum(groups.values()) == 3370 and len(groups) == 22, 'marked cubic census')
    degrees = [8, 8, 10, 9, 9, 9, 9, 9]
    records = []
    full = []
    for mask, multiplicity in sorted(groups.items()):
        j = matrix(mask)
        orbit = {sum(j[p[i]][p[k]] << bit for bit, (i, k) in enumerate(PAIRS)) for p in PERMS}
        need(len(orbit) == multiplicity, 'explicit normalization orbit')
        common = [[sum(j[i][l] * j[k][l] for l in range(8)) for k in range(8)] for i in range(8)]
        s0 = [[degrees[i] - 4 if i == k else
               (2 if j[i][k] else degrees[i] + degrees[k] - 15) - common[i][k]
               for k in range(8)] for i in range(8)]
        d = [1, 1, 2] + [1 + j[i][0] + j[i][1] - j[i][2] for i in range(3, 8)]
        need(sum(d) == 10 and min(d) >= 0, 'five-edge defect budget')
        need([sum(s0[i]) - 3 * s0[i][i] for i in range(8)] == d, 'Gram row budget')
        row = {'J_mask': mask, 'multiplicity': multiplicity,
               'capacities': [s0[i][k] for i, k in PAIRS], 'defect_degrees': d,
               'negative_capacity': any(value < 0 for line in s0 for value in line),
               'weighted_forms': 0, 'binary_incidence_survivors': 0}
        fingerprints = []
        if not row['negative_capacity']:
            cap = [[s0[i][k] if i != k else 0 for k in range(8)] for i in range(8)]
            for e in weighted_graphs(cap, d):
                s = [[s0[i][k] - e[i][k] for k in range(8)] for i in range(8)]
                need([sum(line) for line in e] == d, 'literal weighted degrees')
                upper = [e[i][k] for i, k in PAIRS]
                fingerprints.append(upper)
                row['weighted_forms'] += 1
                pair_targets = [s[i][k] for i, k in PAIRS]
                need(sum(pair_targets) == 39, 'thirteen weight-three rows')
                for incidence in incidence_sets(pair_targets):
                    need([sum((r >> i) & (r >> k) & 1 for r in incidence) for i, k in PAIRS] == pair_targets,
                         'literal binary Gram replay')
                    row['binary_incidence_survivors'] += 1
                if include_matrices:
                    full.append({'J_mask': mask, 'E': e, 'S': s})
        need(not row['binary_incidence_survivors'], 'one-edge triangle branch survives')
        need(len({tuple(v) for v in fingerprints}) == len(fingerprints), 'duplicate weighted form')
        row['weighted_forms_sha256'] = sha256(encode(sorted(fingerprints))).hexdigest()
        records.append(row)
    out = {'agent': 'six-books-1', 'role': 'researcher', 'schema': 1,
           'claim': 'histogram(3,18,1) forces A=K3 and e(z,A)=0; histogram remains open',
           'root_census': root_census(), 'allowed_row_types': [list(t) for t in TRIPLES],
           'marked_cubic_labeled': sum(groups.values()), 'marked_cubic_classes': len(groups),
           'negative_capacity_classes': sum(r['negative_capacity'] for r in records),
           'weighted_forms': sum(r['weighted_forms'] for r in records),
           'binary_incidence_survivors': sum(r['binary_incidence_survivors'] for r in records),
           'cores': records, 'known21_validation_only': baseline(),
           'signed_identity_controls': signed_controls(sorted(groups))}
    need(out['weighted_forms'] == 1014 and not out['binary_incidence_survivors'], 'complete finite boundary')
    return out, full

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--matrices', type=Path, help='write regenerated full local E/S matrices outside source')
    parser.add_argument('--output', type=Path, help='write regenerated compact certificate')
    args = parser.parse_args()
    out, full = build(args.matrices is not None)
    expected = json.loads(Path(__file__).with_name('degree98_three_roots_expected.json').read_text())
    need(out == expected, 'compact expected certificate differs')
    if args.output:
        args.output.write_text(json.dumps(out, indent=2) + '\n')
    if args.matrices:
        args.matrices.write_text(json.dumps(full, separators=(',', ':')) + '\n')
    print(json.dumps({'complete': True, 'root_masks': 14, 'root_classes': 6,
                      'marked_cubic_labeled': out['marked_cubic_labeled'],
                      'marked_cubic_classes': out['marked_cubic_classes'],
                      'weighted_forms': out['weighted_forms'], 'binary_incidence_survivors': 0,
                      'remaining_shape': 'K3,k=0', 'full_matrices_written': bool(args.matrices)}))

if __name__ == '__main__':
    main()
