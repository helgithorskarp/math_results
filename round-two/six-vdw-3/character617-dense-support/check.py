#!/usr/bin/env python3
"""Independent literal-ratio closure checker and budget-pruned row search.

No imports from the producer or an earlier mathematical contribution.
"""
import argparse
from collections import Counter, deque
import hashlib
import json
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def inverse(x, p):
    a, b, u, v = p, x, 0, 1
    while b:
        quotient = a // b
        a, b, u, v = b, a-quotient*b, v, u-quotient*v
    need(a == 1, 'invertible field element')
    return u % p


def graph():
    p = 617
    need(all(p % d for d in range(2, 25)), 'field primality')
    squares = sorted({j*j % p for j in range(1, p)})
    nonsquares = sorted(set(range(1, p))-set(squares))
    ns = set(nonsquares)
    edges = []
    for step in range(1, p):
        points, current = [], 1
        for _ in range(6):
            current = (current+step) % p
            points.append(current)
        if all(t in ns for t in points):
            edges.append({'step': step, 'support': sorted(points)})
    union = set().union(*(set(row['support']) for row in edges))
    ratios = union | {inverse(t, p) for t in union}
    need(len(union) == 33 and len(ratios) == 66 and ratios <= ns, 'literal support graph')
    neighbors = {}
    for q in squares:
        qi = inverse(q, p)
        neighbors[q] = {t for t in nonsquares if t*qi % p in ratios}
    return squares, nonsquares, edges, ratios, neighbors


def subsets(values, count, index=0, chosen=()):
    """Lexicographic inclusion recursion, independent of product enumeration."""
    if count == 0:
        yield chosen
    else:
        for i in range(index, len(values)-count+1):
            yield from subsets(values, count-1, i+1, chosen+(values[i],))


def check_lattice(data):
    squares, nonsquares, edges, ratios, neighbors = graph()
    masks = {q: sum(1 << t for t in neighbors[q]) for q in squares}
    rows = data['records']
    need(rows == sorted(rows, key=lambda r: r['B']), 'canonical closure order')
    states, hist = {}, Counter()
    for row in rows:
        b = row['B']
        need(b == sorted(set(b)) and len(b) >= 6 and set(b) <= ratios, 'retained state domain')
        mask = sum(1 << t for t in b)
        need(mask not in states, 'distinct retained states')
        a = [q for q in squares if masks[q] & mask == mask]
        need(row == {'A': a, 'B': b}, 'entire literal square-side closure')
        hist[(len(a), len(b))] += 1
        states[mask] = row
    seed = sum(1 << t for t in ratios)
    need(seed in states, 'seed neighborhood present')
    adjacency, retained = {}, 0
    for mask in states:
        children = set()
        for q in squares:
            other = mask & masks[q]
            if other.bit_count() >= 6:
                need(other in states, 'missing closed-family successor')
                retained += 1
                children.add(other)
        adjacency[mask] = children
    visited, queue = {seed}, deque([seed])
    while queue:
        for child in adjacency[queue.popleft()]:
            if child not in visited:
                visited.add(child)
                queue.append(child)
    need(visited == set(states), 'all retained states reachable')
    expected = {'schema': 'character617-dense-lattice-v1', 'prime': 617, 'threshold': 6,
                'normalized_vertex': 1, 'endpoint_supports': edges,
                'undirected_ratios': sorted(ratios), 'states': len(rows),
                'tested_transitions': len(rows)*len(squares), 'retained_transitions': retained,
                'maximum_A': max(len(r['A']) for r in rows),
                'A_B_histogram': [[a, b, n] for (a, b), n in sorted(hist.items())],
                'state_records_sha256': digest(rows), 'records': rows}
    need(data == expected, 'entire closed-family record')


def check_cores(data, lattice_data):
    check_lattice(lattice_data)
    squares, nonsquares, edges, ratios, neighbors = graph()
    fives = {}
    for row in lattice_data['records']:
        if len(row['A']) >= 5:
            need(1 in row['A'], 'normalized vertex in full closure')
            for others in subsets([q for q in row['A'] if q != 1], 4):
                a = (1, *others)
                common = {t for t in nonsquares if all(t in neighbors[q] for q in a)}
                need(6 <= len(common) <= 8, 'all relevant five-row common neighborhoods')
                fives[a] = common
    five_rows = [{'A0': list(a), 'C': sorted(c)} for a, c in sorted(fives.items())]
    cases, balanced = [], []
    for na, nb in ((10, 12), (11, 11)):
        histogram, count = Counter(), 0
        for a, common in sorted(fives.items()):
            for size in range(nb-5, len(common)+1):
                for core in subsets(sorted(common), size):
                    # Counts use literal adjacency membership, not set difference.
                    gaps = sorted(sum(t not in neighbors[q] for t in core)
                                  for q in squares if q not in a)
                    lower = nb-size + sum(gaps[:na-5])
                    histogram[lower] += 1
                    count += 1
                    if lower <= na*nb-5*(na+nb):
                        need((na, nb, size) == (11, 11, 6), 'all surviving domains')
                        balanced.append({'A0': list(a), 'B0': list(core), 'C': sorted(common),
                                         'lower_missing': lower})
        cases.append({'part_sizes': [na, nb], 'core_cases': count,
                      'missing_budget': na*nb-5*(na+nb), 'minimum_lower_missing': min(histogram),
                      'lower_missing_histogram': [[k, n] for k, n in sorted(histogram.items())]})
    expected = {'schema': 'character617-dense-cores-v1', 'prime': 617,
                'lattice_record_sha256': lattice_data['state_records_sha256'],
                'normalized_five_sets': len(five_rows), 'five_records_sha256': digest(five_rows),
                'five_records': five_rows, 'part_cases': cases,
                'surviving_balanced_cores': len(balanced), 'balanced_records_sha256': digest(balanced),
                'balanced_records': balanced}
    need(data == expected, 'entire normalized core domain and all missing-pair bounds')


def budget_subsets(values, costs, slots, budget):
    """All fixed-size subsets whose sum of costs is at most budget.

    Independent general dynamic suffix lower bounds and inclusion search; the
    producer's three specialized combinations are not used here.
    """
    n = len(values)
    impossible = 10**6
    suffix = [[0]+[impossible]*slots for _ in range(n+1)]
    for i in range(n-1, -1, -1):
        for k in range(1, slots+1):
            suffix[i][k] = min(suffix[i+1][k], costs[i]+suffix[i+1][k-1])
    def recurse(index, left, allowance, chosen):
        if left == 0:
            yield chosen
        elif suffix[index][left] <= allowance:
            for i in range(index, n-left+1):
                after = allowance-costs[i]
                if suffix[i+1][left-1] <= after:
                    yield from recurse(i+1, left-1, after, chosen+(values[i],))
    yield from recurse(0, slots, budget, ())


def check_extension(data, core_data, lattice_data):
    check_cores(core_data, lattice_data)
    squares, nonsquares, edges, ratios, neighbors = graph()
    reverse = {t: sum(1 << q for q in squares if t in neighbors[q]) for t in nonsquares}
    start, stop = data['start'], data['stop']
    need(type(start) is int and type(stop) is int and 0 <= start < stop <= len(core_data['balanced_records']), 'extension range')
    rows, all_hist, total = [], Counter(), 0
    for number in range(start, stop):
        core = core_data['balanced_records'][number]
        a0, b0, common = core['A0'], core['B0'], core['C']
        values = [q for q in squares if q not in a0]
        costs = [sum(t not in neighbors[q] for t in b0) for q in values]
        groups = {str(k): [q for q, cost in zip(values, costs) if cost == k] for k in range(3)}
        need(len(groups['0']) <= 1, 'full closure has at most one extra zero-cost row')
        transcript, hist, count = hashlib.sha256(), Counter(), 0
        # All 303 remaining square vertices are searched, including cost >=3.
        for rest in budget_subsets(values, costs, 6, 6):
            a = sorted((*a0, *rest))
            need(len(a) == 11 and len(set(a)) == 11, 'eleven distinct literal rows')
            cost = sum(t not in neighbors[q] for q in rest for t in b0)
            mask = sum(1 << q for q in a)
            losses = []
            for t in nonsquares:
                if t not in common:
                    losses.append((11-(mask & reverse[t]).bit_count(), t))
            best = sorted(losses)[:5]
            missing = cost + sum(g for g, t in best)
            transcript.update(canonical([list(rest), cost, best, missing])+b'\n')
            hist[missing] += 1
            count += 1
        rows.append({'case': number, 'A0': a0, 'B0': b0, 'groups': groups,
                     'extensions': count, 'minimum_missing': min(hist),
                     'missing_histogram': [[k, n] for k, n in sorted(hist.items())],
                     'extension_transcript_sha256': transcript.hexdigest()})
        all_hist.update(hist)
        total += count
    expected = {'schema': 'character617-dense-extension-v1', 'prime': 617,
                'balanced_record_sha256': core_data['balanced_records_sha256'],
                'start': start, 'stop': stop, 'cores': stop-start, 'extensions': total,
                'minimum_missing': min(all_hist),
                'missing_histogram': [[k, n] for k, n in sorted(all_hist.items())],
                'records_sha256': digest(rows), 'records': rows}
    need(data == expected, 'entire exact dense-extension enumeration')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=Path, required=True)
    ap.add_argument('--lattice', type=Path)
    ap.add_argument('--cores', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    raw = args.input.read_bytes()
    data = json.loads(raw)
    if data['schema'] == 'character617-dense-lattice-v1':
        check_lattice(data)
    elif data['schema'] == 'character617-dense-cores-v1':
        check_cores(data, json.loads(args.lattice.read_text()))
    elif data['schema'] == 'character617-dense-extension-v1':
        check_extension(data, json.loads(args.cores.read_text()), json.loads(args.lattice.read_text()))
    else:
        raise ValueError('unknown certificate schema')
    result = {'schema': 'character617-dense-checked-v1', 'certificate_schema': data['schema'],
              'certificate_bytes': len(raw), 'certificate_sha256': hashlib.sha256(raw).hexdigest(),
              'status': 'COMPLETE_LITERAL_CHECK_PASSED'}
    if args.output:
        args.output.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
