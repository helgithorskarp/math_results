#!/usr/bin/env python3
"""Passive full-array comparison; neither search reads author verdicts."""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path

from audit import family_check, template
from covers import census, need


def run(own_path, author_path, witness_path):
    own = json.loads(own_path.read_text())
    author = json.loads(author_path.read_text())
    Q, x, y, absent = template()
    own2 = {tuple(map(tuple, r['cover'])): r for r in own if r['a'] == 2}
    need(len(own) == 24 and len(own2) == 6, 'complete own records')
    covers, detail = census(Q, x, y, 2)
    need(author['a_columns'] == list(map(list, detail['legal_columns'])), 'all 150 author a columns')
    tails = [set(q)-{2} for q in Q if 2 in q]
    T = set(range(18))-{x, y, 2}
    pairs = sorted(p for p in combinations(sorted(T), 2) if not any(set(p) <= tail for tail in tails))
    need(author['a_pairs'] == list(map(list, pairs)), 'all 90 author residual pairs')
    reconstructed = sorted(tuple(sorted(tuple(author['a_columns'][i]) for i in C)) for C in author['a_covers'])
    need(reconstructed == covers, 'all six actual author cover keys')
    vertices = edges = graph_pairs = 0
    for fiber in author['fibers']:
        key = tuple(sorted(tuple(author['a_columns'][i]) for i in fiber['a_cover']))
        r = own2[key]
        need(fiber['seed'] == sorted([list(w) for w in Q_to_words(Q, y)]
                                   + [sorted([2]+list(q)) for q in key]), 'all 35 author seed words')
        need(fiber['x_columns'] == r['columns'], 'all literal author extra hub columns')
        adj = [set(row) for row in r['adjacency']]
        for i, j in combinations(range(len(fiber['x_columns'])), 2):
            compatible = len(set(fiber['x_columns'][i]) & set(fiber['x_columns'][j])) <= 1
            need(compatible == (j in adj[i]), 'each graph pair agrees with author literal blocks')
            graph_pairs += 1
            edges += compatible
        vertices += len(fiber['x_columns'])
    witness = json.loads(witness_path.read_text())
    need((witness['point_count'], witness['x'], witness['y'], witness['a']) == (18, x, y, 2), 'author witness parameters')
    need(len(witness['words']) == 47, 'author literal witness size')
    family_check(witness['words'], x, y, 2, Q, 16)
    encoded = (json.dumps(sorted(witness['words']), sort_keys=True, separators=(',', ':'))+'\n').encode()
    canonical = hashlib.sha256(encoded).hexdigest()
    need(canonical == 'afe0c1910e0033a96f886db63ab79e0da71b9cd7ccc1cc9d0ee6ff0ef74169fa', 'author canonical witness hash')
    return {'author_absent_point': 2, 'a_columns_compared': 150, 'a_pairs_compared': 90,
            'complete_cover_keys_compared': 6, 'seed_words_compared': 210,
            'hub_columns_compared': vertices, 'all_graph_pairs_compared': graph_pairs,
            'compatible_edges_compared': edges, 'author_witness_words_checked': 47,
            'author_witness_pair_checks': 1081, 'author_canonical_words_sha256': canonical,
            'author_file_sha256': hashlib.sha256(witness_path.read_bytes()).hexdigest(),
            'search_consumed_author_decisions': False, 'complete': True}


def Q_to_words(Q, y):
    return [tuple(sorted((*q, y))) for q in Q]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--own-records', type=Path, required=True)
    parser.add_argument('--author-census', type=Path, required=True)
    parser.add_argument('--author-witness', type=Path, required=True)
    parser.add_argument('--expected', type=Path)
    args = parser.parse_args()
    result = run(args.own_records, args.author_census, args.author_witness)
    if args.expected:
        need(result == json.loads(args.expected.read_text()), 'comparison expected output')
    print(json.dumps(result, indent=2, sort_keys=True))
