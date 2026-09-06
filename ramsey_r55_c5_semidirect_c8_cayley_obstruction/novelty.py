"""Compare the new family with 21 saved literal graphs, not entire basins.

Fixture bit k is the red edge at position k in combinations(range(43),2).
Use --edges NAME to emit any fixture as a standalone literal edge list.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json


def need(ok, message):
    if not ok:
        raise ValueError(message)


def decode(record):
    value = int(record['red_edge_bits_hex'], 16)
    need(0 <= value < 1 << 903, '903 edge bits')
    edges = [pair for k, pair in enumerate(combinations(range(43), 2)) if value >> k & 1]
    rows = [0]*43
    for u, v in edges:
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return edges, rows


def edge_text(edges):
    return '43 '+str(len(edges))+'\n'+''.join(f'{u} {v}\n' for u, v in edges)


def count_fives(rows):
    def visit(candidates, remaining):
        if remaining == 1:
            return candidates.bit_count()
        count = 0
        while candidates.bit_count() >= remaining:
            bit = candidates & -candidates
            candidates ^= bit
            count += visit(candidates & rows[bit.bit_length()-1], remaining-1)
        return count
    return visit((1 << 43)-1, 5)


def compare():
    records = json.loads((Path(__file__).parent/'novelty_fixtures.json').read_text())['records']
    full = (1 << 43)-1
    results = []
    for record in records:
        edges, rows = decode(record)
        need(sha256(edge_text(edges).encode()).hexdigest() == record['canonical_edge_list_sha256'], 'fixture hash')
        complement = [full ^ (1 << v) ^ rows[v] for v in range(43)]
        blue_red = [count_fives(complement), count_fives(rows)]
        need(blue_red == record['expected_blue_red_five_sets'], 'physical defect count')
        regular_cores = 0
        triples = 0
        for deleted in combinations(range(43), 3):
            triples += 1
            kept = full ^ sum(1 << v for v in deleted)
            first = (kept & -kept).bit_length()-1
            degree = (rows[first] & kept).bit_count()
            regular_cores += all((rows[v] & kept).bit_count() == degree for v in range(43) if kept >> v & 1)
        need(regular_cores == 0, 'this fixture has a regular forty-vertex core')
        results.append({'name': record['name'], 'blue_red_five_sets': blue_red,
                        'degree_histogram': {str(k): v for k, v in sorted(Counter(map(int.bit_count, rows)).items())},
                        'deletion_triples_tested': triples, 'regular_40_cores': regular_cores})
    return {'status': 'VERIFIED_SEPARATION_FROM_SAVED_REPRESENTATIVES',
            'scope': 'These literal graphs and their relabelings/complements; no assertion about all historical basin vertices.',
            'compared_graphs': len(results), 'records': results}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--edges', metavar='NAME')
    args = ap.parse_args()
    if args.edges is None:
        print(json.dumps(compare(), indent=2, sort_keys=True))
    else:
        records = json.loads((Path(__file__).parent/'novelty_fixtures.json').read_text())['records']
        matches = [r for r in records if r['name'] == args.edges]
        need(len(matches) == 1, 'unique fixture name required')
        print(edge_text(decode(matches[0])[0]), end='')
