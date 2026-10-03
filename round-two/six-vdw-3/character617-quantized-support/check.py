#!/usr/bin/env python3
"""Separate literal-ratio checker, adjacent-column bound and full row search.

No producer imports and no prior contribution's code or generated files.
"""
import argparse
from collections import Counter, deque
import hashlib
import heapq
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
        quotient = a//b
        a, b, u, v = b, a-quotient*b, v, u-quotient*v
    need(a == 1, 'invertible nonzero residue')
    return u % p


def graph():
    p = 617
    need(all(p % d for d in range(2, 25)), 'field primality')
    squares = sorted({j*j % p for j in range(1, p)})
    nonsquares = sorted(set(range(1, p))-set(squares))
    ns = set(nonsquares)
    supports = []
    for step in range(1, p):
        points, current = [], 1
        for _ in range(6):
            current = (current+step) % p
            points.append(current)
        if all(t in ns for t in points):
            supports.append({'step': step, 'support': sorted(points)})
    union = set().union(*(set(r['support']) for r in supports))
    opposite = {inverse(t, p) for t in union}
    ratios = union | opposite
    need(len(supports) == 6 and len(union) == 33 and not (union & opposite), 'full six-support domain')
    need(len(ratios) == 66 and ratios <= ns, 'undirected ratio domain')
    neighbors = {}
    for q in squares:
        qi = inverse(q, p)
        neighbors[q] = {t for t in nonsquares if t*qi % p in ratios}
        need(len(neighbors[q]) == 66, 'full literal degree')
    return squares, nonsquares, supports, ratios, neighbors


def subsets(values, count, index=0, chosen=()):
    if count == 0:
        yield chosen
    else:
        for i in range(index, len(values)-count+1):
            yield from subsets(values, count-1, i+1, chosen+(values[i],))


def check_lattice(data):
    squares, nonsquares, supports, ratios, neighbors = graph()
    masks = {q: sum(1 << t for t in neighbors[q]) for q in squares}
    need(data['prime'] == 617 and data['threshold'] == 6 and data['normalized_vertex'] == 1, 'closure definition')
    records = data['records']
    need(records == sorted(records, key=lambda r: r['B']), 'canonical state order')
    states, hist = {}, Counter()
    for row in records:
        b = row['B']
        need(b == sorted(set(b)) and len(b) >= 6 and set(b) <= ratios, 'whole retained state domain')
        mask = sum(1 << t for t in b)
        need(mask not in states, 'unique states')
        a = [q for q in squares if mask & masks[q] == mask]
        need(row == {'A': a, 'B': b}, 'full literal square closure')
        states[mask] = row
        hist[(len(a), len(b))] += 1
    seed = sum(1 << t for t in ratios)
    need(seed in states, 'normalization seed')
    retained, adjacency = 0, {}
    for mask in states:
        children = set()
        for q in squares:
            other = mask & masks[q]
            if other.bit_count() >= 6:
                need(other in states, 'complete retained transition coverage')
                retained += 1
                children.add(other)
        adjacency[mask] = children
    reached, queue = {seed}, deque([seed])
    while queue:
        for other in adjacency[queue.popleft()]:
            if other not in reached:
                reached.add(other)
                queue.append(other)
    need(reached == set(states), 'every retained state reachable')
    expected = {'schema': 'character617-quantized-lattice-v1', 'prime': 617,
                'threshold': 6, 'normalized_vertex': 1, 'endpoint_supports': supports,
                'undirected_ratios': sorted(ratios), 'states': len(records),
                'tested_transitions': len(records)*len(squares), 'retained_transitions': retained,
                'maximum_A': max(len(r['A']) for r in records),
                'A_B_histogram': [[a, b, n] for (a, b), n in sorted(hist.items())],
                'records_sha256': digest(records), 'records': records}
    need(data == expected, 'entire closed-family record')
    need(all(not (len(r['A']) >= a and len(r['B']) >= b)
             for a, b in ((5, 9), (6, 7), (7, 6)) for r in records), 'all required biclique absences')


def scores_literal(a0, b0, common, na, nb, squares, nonsquares, neighbors):
    slots, k = na-5, nb-len(b0)
    d0 = {t: sum(t not in neighbors[q] for q in a0)
          for t in nonsquares if t not in common}
    need(slots >= 5 and all(1 <= d <= 5 for d in d0.values()), 'uniform deficit domain')
    result = []
    for q in squares:
        if q not in a0:
            g = sum(t not in neighbors[q] for t in b0)
            # Every adjacent cost is <=5; every nonadjacent cost is >=slots+1.
            # At least66-|C| adjacent outside columns exist, more than k.
            choices = [d0[t] for t in neighbors[q] if t not in common]
            need(len(choices) >= k, 'complete adjacent outside minimization')
            best = sum(heapq.nsmallest(k, choices))
            result.append((slots*g+best, q, g))
    return sorted(result)


def item_counts(scores, slots, budget):
    # One independent 0/1 factor per row; no grouped binomial convolution.
    dp = {(0, 0): 1}
    for cost, q, g in scores:
        other = dict(dp)
        for (size, used), number in dp.items():
            if size < slots and used+cost <= budget:
                key = size+1, used+cost
                other[key] = other.get(key, 0)+number
        dp = other
    return [[weight, number] for (size, weight), number in sorted(dp.items()) if size == slots]


def check_cores(data, lattice_data):
    check_lattice(lattice_data)
    squares, nonsquares, supports, ratios, neighbors = graph()
    fives = {}
    for row in lattice_data['records']:
        if len(row['A']) >= 5:
            need(1 in row['A'], 'normalized vertex present')
            for other in subsets([q for q in row['A'] if q != 1], 4):
                a0 = (1, *other)
                common = {t for t in nonsquares if all(t in neighbors[q] for q in a0)}
                need(6 <= len(common) <= 8, 'full five-row common-neighbor bound')
                fives[a0] = common
    five_records = [{'A0': list(a), 'C': sorted(c)} for a, c in sorted(fives.items())]
    cases, surviving = [], []
    for na, nb in ((10, 13), (11, 12)):
        allowance, slots = na*nb-115, na-5
        need(6+2*(na-5) > allowance, 'integral least-five reduction valid')
        rows, elementary_hist, weighted_hist = [], Counter(), Counter()
        for a0, common in sorted(fives.items()):
            for size in range(nb-5, len(common)+1):
                for b0 in subsets(sorted(common), size):
                    scores = scores_literal(a0, b0, common, na, nb, squares, nonsquares, neighbors)
                    gaps = sorted(sum(t not in neighbors[q] for t in b0) for q in squares if q not in a0)
                    elementary = nb-size+sum(gaps[:slots])
                    lower = sum(h for h, q, g in scores[:slots])
                    elementary_hist[elementary] += 1
                    weighted_hist[lower] += 1
                    row = {'A0': list(a0), 'B0': list(b0), 'C': sorted(common),
                           'elementary_lower': elementary, 'weighted_lower': lower,
                           'best_rows': [[h, q] for h, q, g in scores[:slots]],
                           'score_histogram': [[h, n] for h, n in sorted(Counter(h for h, q, g in scores).items())]}
                    if lower <= slots*allowance:
                        counts = item_counts(scores, slots, slots*allowance)
                        row['choice_weight_histogram'] = counts
                        row['row_choices'] = sum(n for h, n in counts)
                        surviving.append({'part_sizes': [na, nb], **row})
                    rows.append(row)
        cases.append({'part_sizes': [na, nb], 'missing_budget': allowance, 'guaranteed_common': nb-5,
                      'core_cases': len(rows), 'elementary_histogram': [[h, n] for h, n in sorted(elementary_hist.items())],
                      'weighted_histogram': [[h, n] for h, n in sorted(weighted_hist.items())],
                      'weighted_surviving_cores': sum(r['weighted_lower'] <= slots*allowance for r in rows),
                      'records_sha256': digest(rows), 'records': rows})
    expected = {'schema': 'character617-quantized-cores-v1', 'prime': 617,
                'lattice_records_sha256': lattice_data['records_sha256'],
                'five_sets': len(five_records), 'five_records_sha256': digest(five_records), 'five_records': five_records,
                'cases': cases, 'surviving_cores': len(surviving), 'row_choices': sum(r['row_choices'] for r in surviving),
                'survivor_records_sha256': digest(surviving), 'survivors': surviving}
    need(data == expected, 'whole core domain, coefficients and allocated bounds')


def budget_subsets(values, costs, slots, budget):
    n = len(values)
    suffix = [[0]+[10**9]*slots for _ in range(n+1)]
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
    squares, nonsquares, supports, ratios, neighbors = graph()
    reverse = {t: {q for q in squares if t in neighbors[q]} for t in nonsquares}
    records, all_hist = [], Counter()
    for core in core_data['survivors']:
        na, nb = core['part_sizes']
        a0, b0, common = core['A0'], core['B0'], set(core['C'])
        scores = scores_literal(a0, b0, common, na, nb, squares, nonsquares, neighbors)
        weighted = {q: h for h, q, g in scores}
        values = [q for q in squares if q not in a0]
        rows, hist = [], Counter()
        for extra in budget_subsets(values, [weighted[q] for q in values], na-5, (na-5)*(na*nb-115)):
            a = set(a0) | set(extra)
            need(len(a) == na, 'all distinct selected rows')
            core_cost = sum(t not in neighbors[q] for q in extra for t in b0)
            losses = sorted((na-len(a & reverse[t]), t) for t in nonsquares if t not in common)
            best = losses[:nb-len(b0)]
            missing = core_cost+sum(d for d, t in best)
            rows.append({'Aextra': list(extra), 'core_cost': core_cost,
                         'best_outside': [[d, t] for d, t in best], 'minimum_missing': missing})
            hist[missing] += 1
        need(len(rows) == core['row_choices'], 'complete independent all-row search')
        all_hist.update(hist)
        records.append({'part_sizes': [na, nb], 'A0': a0, 'B0': b0, 'C': sorted(common),
                        'extensions': len(rows), 'minimum_missing': min(hist), 'records': rows})
    expected = {'schema': 'character617-quantized-extension-v1', 'prime': 617,
                'survivor_records_sha256': core_data['survivor_records_sha256'],
                'cores': len(records), 'row_choices': sum(r['extensions'] for r in records),
                'minimum_missing': min(all_hist), 'missing_histogram': [[h, n] for h, n in sorted(all_hist.items())],
                'records_sha256': digest(records), 'records': records}
    need(data == expected, 'whole exact row and outside-column minimization')
    need(all(r['minimum_missing'] > r['part_sizes'][0]*r['part_sizes'][1]-115 for r in records), 'all surviving domains excluded')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=Path)
    ap.add_argument('--controls', action='store_true')
    ap.add_argument('--lattice', type=Path)
    ap.add_argument('--cores', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    if args.controls:
        values, costs = list(range(6)), [0, 1, 1, 2, 3, 4]
        rows = []
        for slots in range(7):
            for budget in range(11):
                literal = []
                for mask in range(1 << 6):
                    selected = tuple(q for q in values if mask & (1 << q))
                    if len(selected) == slots and sum(costs[q] for q in selected) <= budget:
                        literal.append(selected)
                actual = list(budget_subsets(values, costs, slots, budget))
                need(actual == sorted(literal), 'all small positive/negative budget controls')
                rows.append([slots, budget, len(actual)])
        result = {'schema': 'character617-quantized-controls-v1', 'cases': len(rows),
                  'records': rows, 'status': 'COMPLETE_LITERAL_CONTROLS_PASSED'}
        if args.output:
            args.output.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
        print(json.dumps({'cases': len(rows), 'status': result['status']}))
        return
    need(args.input is not None, 'certificate input required')
    raw = args.input.read_bytes()
    data = json.loads(raw)
    if data['schema'] == 'character617-quantized-lattice-v1':
        check_lattice(data)
    elif data['schema'] == 'character617-quantized-cores-v1':
        check_cores(data, json.loads(args.lattice.read_text()))
    elif data['schema'] == 'character617-quantized-extension-v1':
        check_extension(data, json.loads(args.cores.read_text()), json.loads(args.lattice.read_text()))
    else:
        raise ValueError('unknown certificate schema')
    result = {'schema': 'character617-quantized-checked-v1', 'certificate_schema': data['schema'],
              'certificate_bytes': len(raw), 'certificate_sha256': hashlib.sha256(raw).hexdigest(),
              'status': 'COMPLETE_LITERAL_CHECK_PASSED'}
    if args.output:
        args.output.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
