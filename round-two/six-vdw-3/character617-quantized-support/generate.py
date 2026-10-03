#!/usr/bin/env python3
"""Exact size23 graph exclusion: integral degrees and uniform deficit allocation."""
import argparse
from collections import Counter, defaultdict, deque
import hashlib
import itertools
import json
import math
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def graph():
    p = 617
    squares = [q for q in range(1, p) if pow(q, 308, p) == 1]
    nonsquares = [t for t in range(1, p) if pow(t, 308, p) == p-1]
    supports = []
    for d in range(1, p):
        points = [(1+j*d) % p for j in range(1, 7)]
        if all(pow(t, 308, p) == p-1 for t in points):
            supports.append({'step': d, 'support': sorted(points)})
    v = set().union(*(set(r['support']) for r in supports))
    ratios = v | {pow(t, -1, p) for t in v}
    neighbors = {q: {q*d % p for d in ratios} for q in squares}
    masks = {q: sum(1 << t for t in neighbors[q]) for q in squares}
    need(len(v) == 33 and len(ratios) == 66, 'endpoint graph size')
    return squares, nonsquares, supports, ratios, neighbors, masks


def lattice():
    squares, nonsquares, supports, ratios, neighbors, masks = graph()
    seed = masks[1]
    states, queue, retained = {seed}, deque([seed]), 0
    while queue:
        b = queue.popleft()
        for q in squares:
            c = b & masks[q]
            if c.bit_count() >= 6:
                retained += 1
                if c not in states:
                    states.add(c)
                    queue.append(c)
    records = []
    for b in states:
        records.append({'A': [q for q in squares if b & masks[q] == b],
                        'B': [t for t in nonsquares if b & (1 << t)]})
    records.sort(key=lambda r: r['B'])
    hist = Counter((len(r['A']), len(r['B'])) for r in records)
    return {'schema': 'character617-quantized-lattice-v1', 'prime': 617,
            'threshold': 6, 'normalized_vertex': 1, 'endpoint_supports': supports,
            'undirected_ratios': sorted(ratios), 'states': len(records),
            'tested_transitions': len(records)*len(squares), 'retained_transitions': retained,
            'maximum_A': max(len(r['A']) for r in records),
            'A_B_histogram': [[a, b, n] for (a, b), n in sorted(hist.items())],
            'records_sha256': digest(records), 'records': records}


def weighted_scores(a0, b0, common, na, nb, squares, nonsquares, neighbors, masks):
    slots, k = na-5, nb-len(b0)
    bm = sum(1 << t for t in b0)
    buckets = defaultdict(list)
    for t in nonsquares:
        if t not in common:
            buckets[sum(t not in neighbors[q] for q in a0)].append(t)
    buckets = {i: (len(vals), sum(1 << t for t in vals)) for i, vals in buckets.items()}
    scores = []
    for q in squares:
        if q not in a0:
            cost = len(b0)-(masks[q] & bm).bit_count()
            distribution = Counter()
            for i, (number, mask) in buckets.items():
                hit = (mask & masks[q]).bit_count()
                distribution[i] += hit
                distribution[i+slots] += number-hit
            left, best = k, 0
            for weight, number in sorted(distribution.items()):
                take = min(left, number)
                best += take*weight
                left -= take
                if not left:
                    break
            need(left == 0, 'entire outside-column minimization')
            scores.append((slots*cost+best, q, cost))
    return sorted(scores)


def choice_counts(scores, slots, budget):
    dp = {(0, 0): 1}
    for cost, number in sorted(Counter(h for h, q, g in scores).items()):
        other = defaultdict(int)
        for (size, used), count in dp.items():
            for take in range(min(number, slots-size)+1):
                if used+cost*take <= budget:
                    other[size+take, used+cost*take] += count*math.comb(number, take)
        dp = other
    return [[weight, count] for (size, weight), count in sorted(dp.items()) if size == slots]


def cores(lattice_data):
    squares, nonsquares, supports, ratios, neighbors, masks = graph()
    fives = {}
    for row in lattice_data['records']:
        if len(row['A']) >= 5:
            for other in itertools.combinations([q for q in row['A'] if q != 1], 4):
                a0 = (1, *other)
                c = masks[1]
                for q in other:
                    c &= masks[q]
                fives[a0] = {t for t in nonsquares if c & (1 << t)}
    five_records = [{'A0': list(a), 'C': sorted(c)} for a, c in sorted(fives.items())]
    cases, surviving = [], []
    for na, nb in ((10, 13), (11, 12)):
        allowance, slots = na*nb-115, na-5
        need(6+2*(na-5) > allowance, 'integral least-five bound')
        rows, elementary_hist, weighted_hist = [], Counter(), Counter()
        for a0, common in sorted(fives.items()):
            for size in range(nb-5, len(common)+1):
                for b0 in itertools.combinations(sorted(common), size):
                    scores = weighted_scores(a0, b0, common, na, nb, squares, nonsquares, neighbors, masks)
                    elementary = nb-size+sum(sorted(g for h, q, g in scores)[:slots])
                    lower = sum(h for h, q, g in scores[:slots])
                    elementary_hist[elementary] += 1
                    weighted_hist[lower] += 1
                    row = {'A0': list(a0), 'B0': list(b0), 'C': sorted(common),
                           'elementary_lower': elementary, 'weighted_lower': lower,
                           'best_rows': [[h, q] for h, q, g in scores[:slots]],
                           'score_histogram': [[h, n] for h, n in sorted(Counter(h for h, q, g in scores).items())]}
                    if lower <= slots*allowance:
                        counts = choice_counts(scores, slots, slots*allowance)
                        row['choice_weight_histogram'] = counts
                        row['row_choices'] = sum(n for h, n in counts)
                        surviving.append({'part_sizes': [na, nb], **row})
                    rows.append(row)
        cases.append({'part_sizes': [na, nb], 'missing_budget': allowance, 'guaranteed_common': nb-5,
                      'core_cases': len(rows), 'elementary_histogram': [[h, n] for h, n in sorted(elementary_hist.items())],
                      'weighted_histogram': [[h, n] for h, n in sorted(weighted_hist.items())],
                      'weighted_surviving_cores': sum(r['weighted_lower'] <= slots*allowance for r in rows),
                      'records_sha256': digest(rows), 'records': rows})
    return {'schema': 'character617-quantized-cores-v1', 'prime': 617,
            'lattice_records_sha256': lattice_data['records_sha256'],
            'five_sets': len(five_records), 'five_records_sha256': digest(five_records), 'five_records': five_records,
            'cases': cases, 'surviving_cores': len(surviving), 'row_choices': sum(r['row_choices'] for r in surviving),
            'survivor_records_sha256': digest(surviving), 'survivors': surviving}


def grouped_subsets(scores, slots, budget):
    groups = defaultdict(list)
    smallest = scores[0][0]
    # Other slots cost at least the global minimum; this discards no valid tuple.
    for h, q, g in scores:
        if h+(slots-1)*smallest <= budget:
            groups[h].append(q)
    groups = sorted(groups.items())
    def recurse(index, left, allowance, chosen):
        if left == 0:
            yield tuple(sorted(chosen))
        elif index < len(groups) and left*groups[index][0] <= allowance:
            cost, values = groups[index]
            for take in range(min(left, len(values), allowance//cost)+1):
                for part in itertools.combinations(values, take):
                    yield from recurse(index+1, left-take, allowance-cost*take, chosen+part)
    yield from recurse(0, slots, budget, ())


def extend(core_data):
    squares, nonsquares, supports, ratios, neighbors, masks = graph()
    records, all_hist = [], Counter()
    for core in core_data['survivors']:
        na, nb = core['part_sizes']
        a0, b0, common = core['A0'], core['B0'], set(core['C'])
        scores = weighted_scores(a0, b0, common, na, nb, squares, nonsquares, neighbors, masks)
        by_q = {q: g for h, q, g in scores}
        rows, hist = [], Counter()
        for extra in grouped_subsets(scores, na-5, (na-5)*(na*nb-115)):
            a = [*a0, *extra]
            cost = sum(by_q[q] for q in extra)
            losses = sorted((sum(t not in neighbors[q] for q in a), t)
                            for t in nonsquares if t not in common)
            best = losses[:nb-len(b0)]
            missing = cost+sum(d for d, t in best)
            rows.append({'Aextra': list(extra), 'core_cost': cost,
                         'best_outside': [[d, t] for d, t in best], 'minimum_missing': missing})
            hist[missing] += 1
        rows.sort(key=lambda r: r['Aextra'])
        need(len(rows) == core['row_choices'], 'coefficient count and grouped enumeration')
        need(len({tuple(r['Aextra']) for r in rows}) == len(rows), 'distinct row combinations')
        all_hist.update(hist)
        records.append({'part_sizes': [na, nb], 'A0': a0, 'B0': b0, 'C': sorted(common),
                        'extensions': len(rows), 'minimum_missing': min(hist), 'records': rows})
    return {'schema': 'character617-quantized-extension-v1', 'prime': 617,
            'survivor_records_sha256': core_data['survivor_records_sha256'],
            'cores': len(records), 'row_choices': sum(r['extensions'] for r in records),
            'minimum_missing': min(all_hist), 'missing_histogram': [[h, n] for h, n in sorted(all_hist.items())],
            'records_sha256': digest(records), 'records': records}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=('lattice', 'cores', 'extend'))
    parser.add_argument('--input', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = lattice() if args.stage == 'lattice' else (cores if args.stage == 'cores' else extend)(json.loads(args.input.read_text()))
    args.output.write_text(json.dumps(data, sort_keys=True, indent=2)+'\n')
    print(json.dumps({'schema': data['schema'], 'output_sha256': hashlib.sha256(args.output.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
