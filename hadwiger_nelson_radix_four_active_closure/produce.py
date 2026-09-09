#!/usr/bin/env python3
"""Generate the finite four-active closure; exploratory solvers are not used."""
import argparse
from collections import Counter, defaultdict
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'hadwiger_nelson_complex_radix_architecture'))
import geometry as G


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def fm(a, b):
    return ((a & 1) * (b & 1) ^ (a >> 1) * (b >> 1)) | (((a & 1) * (b >> 1) ^ (a >> 1) * (b & 1) ^ (a >> 1) * (b >> 1)) << 1)


def signature(row):
    values = [(a % 2) ^ ((b % 2) << 1) for a, b in row]
    pivot = next(v for v in values[1:] if v)
    inverse = next(v for v in (1, 2, 3) if fm(v, pivot) == 1)
    return tuple(fm(inverse, v) for v in values[1:]), fm(inverse, values[0])


def first_clique(adj):
    for a in range(len(adj)):
        for b in sorted(v for v in adj[a] if v > a):
            common = adj[a] & adj[b]
            for c in sorted(v for v in common if v > b):
                last = [v for v in common & adj[c] if v > c]
                if last:
                    return a, b, c, min(last)
    raise ValueError('uncovered quartet: neither linear three-colouring nor K4')


def compute(export=None):
    rows, row_edges = G.inventory()
    circle_poly = G.primitive({(2, 0): 1, (0, 2): 3, (0, 0): -1})
    events = []
    for row in rows:
        support = [i for i, d in enumerate(row) if d != (0, 0)]
        events.append((circle_poly if support[0] else ()) if len(support) == 1 else G.distance_event(row))
    factors = sorted(set(events) - {()})
    ids = {f: i for i, f in enumerate(factors)}
    circle = ids[circle_poly]
    edge_groups, reps, base = {}, {}, []
    for row, event, edges in zip(rows, events, row_edges):
        if not event:
            base += edges
        elif event != circle_poly:
            cid = ids[event]
            if cid in reps:
                raise ValueError('nonmonomial event is not unique')
            reps[cid], edge_groups[cid] = row, edges

    words = [(1,) + w for w in product(range(3), repeat=4)]
    masks, buckets = {}, defaultdict(list)
    for cid in sorted(reps):
        row = reps[cid]
        residues = [(a - b) % 3 for a, b in row]
        masks[cid] = sum(1 << i for i, w in enumerate(words) if sum(a * b for a, b in zip(residues, w)) % 3 == 0)
        buckets[signature(row)].append(cid)
    patterns = [tuple((n, c) for c in range(4)) for n in sorted({n for n, c in buckets}) if all((n, c) in buckets for c in range(4))]
    full = (1 << len(words)) - 1
    counts, support_counts, word_counts = Counter(), defaultdict(Counter), Counter()
    transcript = hashlib.sha256()
    obstruction_map = {}
    obstruction_assignments = Counter()
    edge_owner = {tuple(e): cid for cid, edges in edge_groups.items() for e in edges}
    for pattern in patterns:
        support = sum(bool(v) for v in pattern[0][0])
        for quartet in product(*(buckets[s] for s in pattern)):
            available = full ^ (masks[quartet[0]] | masks[quartet[1]] | masks[quartet[2]] | masks[quartet[3]])
            if available:
                word = (available & -available).bit_length() - 1
                record = [list(quartet), 'F3', word]
                counts['linear_three_colourings'] += 1
                support_counts[support]['linear_three_colourings'] += 1
                word_counts[word] += 1
            else:
                adj = [set() for _ in G.LABELS]
                for u, v in base + [e for cid in quartet for e in edge_groups[cid]]:
                    adj[u].add(v)
                    adj[v].add(u)
                clique = first_clique(adj)
                if not all(v in adj[u] for u, v in combinations(clique, 2)):
                    raise ValueError('invalid K4 witness')
                obstruction = tuple(sorted({edge_owner[e] for e in combinations(clique, 2) if e in edge_owner}))
                obstruction_map.setdefault(obstruction, clique)
                obstruction_assignments[len(obstruction)] += 1
                record = [list(quartet), 'K4', list(clique)]
                counts['impossible_planar_K4'] += 1
                support_counts[support]['impossible_planar_K4'] += 1
            transcript.update(json.dumps(record, separators=(',', ':')).encode() + b'\n')
    obstructions = [[list(q), list(w)] for q, w in sorted(obstruction_map.items())]
    interface = {
        'schema': 'hn-radix-four-active-forbidden-incidences-v1',
        'circle_id': circle,
        'curve_inventory_sha256': digest(factors),
        'label_order': 'lexicographic product(range(3),repeat=5); digits=(0,1,omega)',
        'forbidden_curve_sets_with_K4_labels': obstructions,
        'scope': 'Each listed active-curve set is impossible at every complex z, even with further active curves or label coincidences. This is a sufficient list, not an exhaustive census of forbidden incidences.',
    }
    if export is not None:
        with Path(export).open('x') as f:
            json.dump(interface, f, sort_keys=True, separators=(',', ':'))
            f.write('\n')
    return {
        'schema': 'hn-radix-four-active-closure-v1',
        'label_vertices': len(G.LABELS), 'label_pairs': sum(map(len, row_edges)),
        'difference_classes': len(rows), 'universal_edges_off_circle': len(base),
        'active_curves': len(factors), 'circle_id': circle,
        'curve_inventory_sha256': digest(factors),
        'F3_word_count': len(words), 'F4_affine_word_count': 256,
        'realized_hyperplanes': len(buckets), 'eligible_patterns': len(patterns),
        'eligible_patterns_sha256': digest(patterns),
        'eligible_quartets': sum(counts.values()), **dict(counts),
        'quartet_classification_by_tail_support': {str(k): dict(v) for k, v in sorted(support_counts.items())},
        'F3_word_assignment_histogram': {str(k): v for k, v in sorted(word_counts.items())},
        'entrywise_witness_transcript_sha256': transcript.hexdigest(),
        'forbidden_incidence_count': len(obstructions),
        'forbidden_incidence_arity_histogram': {str(k): v for k, v in sorted(Counter(map(len, obstruction_map)).items())},
        'K4_assignment_arity_histogram': {str(k): v for k, v in sorted(obstruction_assignments.items())},
        'forbidden_incidence_list_sha256': digest(obstructions),
        'forbidden_incidence_interface_sha256': digest(interface),
        'unresolved_eligible_quartets': 0,
        'minimum_active_curves_for_nonfour': 5,
        'proof_solver_calls': 0, 'proof_CAS_calls': 0,
        'record_improvement': False,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--export-interface', type=Path)
    args = parser.parse_args()
    result = compute(args.export_interface)
    with args.out.open('x') as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write('\n')
    print(json.dumps(result, indent=2, sort_keys=True))
