#!/usr/bin/env python3
"""Independent all-four-absence proof of the sharp marked hub bound."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import time

from covers import census, need, pairs
from packing import find_clique


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def family_check(words, x, y, a, Q, expected_x=None):
    words = [tuple(sorted(w)) for w in words]
    need(len(words) == len(set(words)) and all(len(w) == 5 and len(set(w)) == 5
         and set(w) <= set(range(18)) for w in words), 'distinct literal five-words')
    need(all(len(set(first) & set(second)) <= 2 for first, second in combinations(words, 2)), 'all word intersections')
    need(sorted(tuple(v for v in w if v != y) for w in words if y in w) == sorted(map(tuple, Q)), 'exact fixed y star')
    rep = [sum(v in w for w in words) for v in range(18)]
    need(rep[y] == rep[a] == 20 and not any(x in w and a in w for w in words), 'saturated absent neighbor')
    if expected_x is not None:
        need(rep[x] == expected_x, 'literal hub replication')
    return rep


def hub_graph(Q, x, y, a, cover):
    seed = sorted(set(tuple(sorted(set(q) | {y})) for q in Q)
                  | set(tuple(sorted(set(q) | {a})) for q in cover))
    need(len(seed) == 35, 'complete two-star union')
    family_check(seed, x, y, a, Q, 4)
    T = set(range(18))-{x, y, a}
    candidate = []
    for quad in combinations(sorted(T), 4):
        word = set(quad) | {x}
        if all(len(word & set(w)) <= 2 for w in seed):
            candidate.append(quad)
    # Separate full-domain mask decoder, with no tail-group construction.
    masks = [sum(1 << v for v in w) for w in seed]
    literal = []
    for word in combinations(range(18), 5):
        mask = sum(1 << v for v in word)
        if mask >> x & 1 and not (mask >> y & 1) and not (mask >> a & 1):
            if all((mask & other).bit_count() <= 2 for other in masks):
                literal.append(tuple(v for v in word if v != x))
    need(sorted(literal) == candidate, 'every literal extra hub word')
    vertices = list(map(set, candidate))
    adj = [set() for _ in candidate]
    pairsets = [pairs(q) for q in candidate]
    for i, j in combinations(range(len(candidate)), 2):
        overlap = len(vertices[i] & vertices[j]) <= 1
        need(overlap == pairsets[i].isdisjoint(pairsets[j]), 'all compatibility edges agree')
        if overlap:
            adj[i].add(j)
            adj[j].add(i)
    return seed, candidate, adj


def template():
    data = json.loads(Path(__file__).with_name('input.json').read_text())
    need(set(data) == {'point_count', 'x', 'y', 'blocks'} and data['point_count'] == 18
         and data['x'] == 14 and data['y'] == 17, 'literal canonical input schema')
    Q = [tuple(q) for q in data['blocks']]
    need(len(Q) == 20 and len(set(Q)) == 20 and Q == sorted(Q), 'twenty sorted template quadruples')
    need(all(len(q) == 4 and tuple(sorted(set(q))) == q and set(q) <= set(range(17)) for q in Q), 'template quadruples')
    used = [p for q in Q for p in pairs(q)]
    need(len(used) == len(set(used)) == 120, 'template pair packing')
    rep = [sum(v in q for q in Q) for v in range(17)]
    need(sorted(rep) == [4]*5+[5]*12, 'marked profile')
    high = [v for v, r in enumerate(rep) if r == 4]
    leave = set(combinations(range(17), 2))-set(used)
    need(sum(p in leave for p in combinations(high, 2)) == 4
         and all(tuple(sorted((v, data['x']))) not in leave for v in high if v != data['x']), 'marked isolated high leave')
    absent = [v for v in range(17) if v != data['x'] and tuple(sorted((v, data['x']))) in leave]
    need(absent == [2, 9, 15, 16] and rep[data['x']] == 4, 'entire absent-point carrier')
    return Q, data['x'], data['y'], absent


def run(export=None, case_limit=None):
    Q, x, y, absent = template()
    records = []
    full = []
    for a in absent:
        covers, cover_summary = census(Q, x, y, a)
        need(len(covers) == 6, 'complete six covers at each absent point')
        for index, cover in enumerate(covers):
            start = time.monotonic()
            seed, columns, adj = hub_graph(Q, x, y, a, cover)
            negative, upper = find_clique(adj, 13)
            need(negative is None, 'thirteen extra hub words exist; no upper16 proof')
            witness, lower = find_clique(adj, 12)
            need(witness is not None, 'per-cover maximum12 not established')
            words = sorted(seed+[tuple(sorted(set(columns[i]) | {x})) for i in witness])
            family_check(words, x, y, a, Q, 16)
            records.append({'a': a, 'cover_index': index, 'cover_sha256': digest(cover),
                            'columns': len(columns), 'columns_sha256': digest(columns),
                            'edges': sum(map(len, adj))//2,
                            'adjacency_sha256': digest([sorted(row) for row in adj]),
                            'maximum_extra_hub_words': 12, 'upper_search': upper,
                            'lower_search': lower, 'positive_word_count': len(words),
                            'positive_words_sha256': digest(words)})
            full.append({'a': a, 'cover_index': index, 'cover': cover, 'columns': columns,
                         'adjacency': [sorted(row) for row in adj], 'positive_words': words})
            if case_limit is not None and len(records) >= case_limit:
                return records
        cover_summary.pop('legal_columns')
        records[-1]['complete_absent_point_cover_census'] = cover_summary
    need(len(records) == 24, 'all four absences and all six covers')
    if export:
        export.write_text(json.dumps(full, separators=(',', ':'))+'\n')
    return {'agent': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
            'template_sha256': digest(Q), 'absent_points': absent, 'cases': records,
            'complete_cases': 24, 'automorphism_normalization_used': False,
            'maximum_hub_replication_in_every_completion': 16,
            'total_size_hypothesis_used': False, 'complete': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path)
    parser.add_argument('--export', type=Path, help='Private optional regenerated records')
    parser.add_argument('--pilot', type=int, help='Pilot only; does not establish the whole theorem')
    args = parser.parse_args()
    result = run(args.export, args.pilot)
    if args.expected:
        need(result == json.loads(args.expected.read_text()), 'compact expected output')
    print(json.dumps(result, indent=2, sort_keys=True))
