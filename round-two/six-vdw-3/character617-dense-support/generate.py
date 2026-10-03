#!/usr/bin/env python3
"""Finite common-neighbor closure and dense-extension certificates for F617."""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path

P = 617


def need(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def graph():
    need(all(P % i for i in range(2, 25)), 'prime 617')
    squares = sorted(x for x in range(1, P) if pow(x, 308, P) == 1)
    nonsquares = sorted(set(range(1, P)) - set(squares))
    ns = set(nonsquares)
    edges = []
    for d in range(1, P):
        points = [(1 + j*d) % P for j in range(1, 7)]
        if set(points) <= ns:
            edges.append({'step': d, 'support': sorted(points)})
    v = set().union(*(set(e['support']) for e in edges))
    ratios = v | {pow(t, -1, P) for t in v}
    need(len(v) == 33 and len(ratios) == 66 and ratios <= ns, 'endpoint graph')
    neighbors = {q: {q*d % P for d in ratios} for q in squares}
    return squares, nonsquares, edges, ratios, neighbors


def lattice():
    squares, nonsquares, edges, ratios, neighbors = graph()
    index = {t: i for i, t in enumerate(nonsquares)}
    masks = [sum(1 << index[t] for t in neighbors[q]) for q in squares]
    seed = masks[0]
    seen, todo, retained = {seed}, [seed], 0
    while todo:
        b = todo.pop()
        for mask in masks:
            other = b & mask
            if other.bit_count() >= 6:
                retained += 1
                if other not in seen:
                    seen.add(other)
                    todo.append(other)
    rows = []
    hist = collections.Counter()
    for b in seen:
        a = [q for q, mask in zip(squares, masks) if b & mask == b]
        values = [t for i, t in enumerate(nonsquares) if b >> i & 1]
        hist[(len(a), len(values))] += 1
        rows.append({'A': a, 'B': values})
    rows.sort(key=lambda r: r['B'])
    return {'schema': 'character617-dense-lattice-v1', 'prime': P, 'threshold': 6,
            'normalized_vertex': 1, 'endpoint_supports': edges,
            'undirected_ratios': sorted(ratios), 'states': len(rows),
            'tested_transitions': len(rows)*len(squares), 'retained_transitions': retained,
            'maximum_A': max(len(r['A']) for r in rows),
            'A_B_histogram': [[a, b, n] for (a, b), n in sorted(hist.items())],
            'state_records_sha256': digest(rows), 'records': rows}


def cores(lattice_data):
    squares, nonsquares, edges, ratios, neighbors = graph()
    five = {}
    for row in lattice_data['records']:
        if len(row['A']) >= 5:
            for a0 in itertools.combinations(row['A'], 5):
                if 1 in a0:
                    five[a0] = set.intersection(*(neighbors[q] for q in a0))
    five_rows = [{'A0': list(a), 'C': sorted(c)} for a, c in sorted(five.items())]
    cases = []
    surviving = []
    for na, nb in ((10, 12), (11, 11)):
        hist = collections.Counter()
        count = 0
        for a0, c in sorted(five.items()):
            for size in range(nb - 5, len(c) + 1):
                for b0 in itertools.combinations(sorted(c), size):
                    bset = set(b0)
                    gaps = sorted(len(bset-neighbors[q]) for q in squares if q not in a0)
                    lower = nb-size + sum(gaps[:na-5])
                    hist[lower] += 1
                    count += 1
                    if lower <= na*nb-5*(na+nb):
                        need((na, nb, size) == (11, 11, 6), 'only balanced six-point cores survive')
                        surviving.append({'A0': list(a0), 'B0': list(b0), 'C': sorted(c),
                                          'lower_missing': lower})
        cases.append({'part_sizes': [na, nb], 'core_cases': count,
                      'missing_budget': na*nb-5*(na+nb),
                      'minimum_lower_missing': min(hist),
                      'lower_missing_histogram': [[k, n] for k, n in sorted(hist.items())]})
    return {'schema': 'character617-dense-cores-v1', 'prime': P,
            'lattice_record_sha256': lattice_data['state_records_sha256'],
            'normalized_five_sets': len(five_rows), 'five_records_sha256': digest(five_rows),
            'five_records': five_rows, 'part_cases': cases,
            'surviving_balanced_cores': len(surviving), 'balanced_records_sha256': digest(surviving),
            'balanced_records': surviving}


def extend(data, start, stop):
    squares, nonsquares, edges, ratios, neighbors = graph()
    source = data['balanced_records']
    need(0 <= start < stop <= len(source), 'contiguous extension range')
    index = {q: i for i, q in enumerate(squares)}
    reverse_masks = {t: sum(1 << index[q] for q in squares if t in neighbors[q]) for t in nonsquares}
    rows = []
    all_hist = collections.Counter()
    total = 0
    for number in range(start, stop):
        row = source[number]
        a0, b0, c = set(row['A0']), set(row['B0']), set(row['C'])
        groups = {k: [] for k in range(3)}
        for q in squares:
            if q not in a0:
                gap = len(b0-neighbors[q])
                if gap in groups:
                    groups[gap].append(q)
        need(len(groups[0]) <= 1, 'closure bound on zero-cost rows')
        candidates = set(itertools.combinations(groups[1], 6))
        for z in groups[0]:
            candidates.update(tuple(sorted((z, *x))) for x in itertools.combinations(groups[1], 5))
            candidates.update(tuple(sorted((z, *x, y))) for x in itertools.combinations(groups[1], 4)
                              for y in groups[2])
        transcript = hashlib.sha256()
        hist = collections.Counter()
        for rest in sorted(candidates):
            selected = a0 | set(rest)
            need(len(selected) == 11, 'eleven distinct square rows')
            core_missing = sum(len(b0-neighbors[q]) for q in rest)
            mask = sum(1 << index[q] for q in selected)
            losses = sorted((11-(mask & reverse_masks[t]).bit_count(), t)
                            for t in nonsquares if t not in c)
            best = losses[:5]
            missing = core_missing + sum(g for g, t in best)
            transcript.update(canonical([list(rest), core_missing, best, missing])+b'\n')
            hist[missing] += 1
        rows.append({'case': number, 'A0': row['A0'], 'B0': row['B0'],
                     'groups': {str(k): v for k, v in groups.items()},
                     'extensions': len(candidates), 'minimum_missing': min(hist),
                     'missing_histogram': [[k, n] for k, n in sorted(hist.items())],
                     'extension_transcript_sha256': transcript.hexdigest()})
        total += len(candidates)
        all_hist.update(hist)
    return {'schema': 'character617-dense-extension-v1', 'prime': P,
            'balanced_record_sha256': data['balanced_records_sha256'], 'start': start, 'stop': stop,
            'cores': stop-start, 'extensions': total, 'minimum_missing': min(all_hist),
            'missing_histogram': [[k, n] for k, n in sorted(all_hist.items())],
            'records_sha256': digest(rows), 'records': rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('stage', choices=('lattice', 'cores', 'extend'))
    ap.add_argument('--input', type=Path)
    ap.add_argument('--start', type=int)
    ap.add_argument('--stop', type=int)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.stage == 'lattice':
        result = lattice()
    elif args.stage == 'cores':
        result = cores(json.loads(args.input.read_text()))
    else:
        result = extend(json.loads(args.input.read_text()), args.start, args.stop)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('records', 'five_records', 'balanced_records')}))


if __name__ == '__main__':
    main()
