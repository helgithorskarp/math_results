#!/usr/bin/env python3
"""Physical audit of block witnesses; does not certify unsampled table minima."""
import argparse
from collections import Counter
import csv
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from physical import (decode, edge_bytes, family, literal_defects, need, orbits,
                      read_graph, recursive_defects)


def free_block(q, k):
    vertices = {42} | {v for t in q for v in range(3*t, 3*t+3)}
    free, _ = orbits()
    selected = [i for i, orbit in enumerate(free)
                if all(u in vertices and v in vertices for u, v in orbit)]
    need(len(selected) == 22, 'physical block orbit coverage')
    return selected[:k]


def change(word, ids, mask):
    need(0 <= mask < (1 << len(ids)), 'assignment range')
    bits = list(word)
    for j, index in enumerate(ids):
        bits[index] = str(int(bits[index]) ^ ((mask >> j) & 1))
    return ''.join(bits)


def run(parent, work, count, k, table=None):
    original = read_graph(parent)
    word = family(original)
    need(list(map(len, recursive_defects(original))) == [72, 51], 'baseline physical score')
    blocks = list(combinations(range(14), 4))
    records = list(csv.DictReader((work/'blocks.tsv').open(), delimiter='\t'))
    status = json.loads((work/'status.json').read_text())
    need(status['complete_requested_range'] is True, 'unfinished range')
    need(status['done'] == count == len(records), 'range coverage')
    need(status['bits'] == k, 'block dimension')
    cache = {word: [72, 51]}
    best = 123
    best_word = word
    best_block = -1
    best_mask = 0
    minimum_histogram = Counter()
    for offset, record in enumerate(records):
        index = status['start']+offset
        q = tuple(int(record[v]) for v in 'abcd')
        need(int(record['block']) == index and q == blocks[index], 'canonical block coverage')
        need(int(record['bits']) == k, 'record dimension')
        ids = free_block(q, k)
        mask = int(record['first_mask'])
        candidate = change(word, ids, mask)
        if candidate not in cache:
            cache[candidate] = list(map(len, recursive_defects(decode(candidate))))
        minimum = sum(cache[candidate])
        need(minimum == int(record['minimum']), 'minimum witness physical score')
        need(1 <= int(record['multiplicity']) <= (1 << k), 'minimum multiplicity range')
        need(minimum <= 123 <= int(record['maximum']) <= 962598, 'record bounds')
        need(0 <= int(record['sum']) <= (1 << k)*962598, 'sum range')
        minimum_histogram[minimum] += 1
        if minimum < best:
            best, best_word, best_block, best_mask = minimum, candidate, index, mask
    need(status['best_score'] == best and status['best_block'] == best_block
         and status['best_mask'] == best_mask, 'best status')
    winner = read_graph(work/'best.edges')
    need(family(winner) == best_word, 'winner physical identity')
    bad = literal_defects(winner)
    need(bad == recursive_defects(winner), 'complete winner defect lists')
    table_checks = 0
    if table:
        need(count == 1 and k <= 10, 'literal table control scope')
        values = [tuple(map(int, line.split())) for line in table.read_text().splitlines()]
        need([i for i, _ in values] == list(range(1 << k)), 'table coverage')
        ids = free_block(blocks[status['start']], k)
        for mask, expected in values:
            candidate = decode(change(word, ids, mask))
            actual = sum(map(len, recursive_defects(candidate)))
            need(actual == expected, 'table vs physical graph')
            table_checks += 1
        scores = [score for _, score in values]
        record = records[0]
        need(min(scores) == int(record['minimum']) and max(scores) == int(record['maximum'])
             and sum(scores) == int(record['sum']) and scores.index(min(scores)) == int(record['first_mask'])
             and scores.count(min(scores)) == int(record['multiplicity']), 'table summary')
    full = count == 1001 and status['start'] == 0 and k == 22
    need(status['full_family'] == full, 'full family label')
    return {'status': 'VERIFIED_BLOCK_WITNESSES_AND_WINNER', 'range_start': status['start'],
            'blocks': count, 'bits_per_block': k, 'complete_1001_block_range': full,
            'minimum_histogram': dict(sorted(minimum_histogram.items())),
            'unique_argmin_graphs': len(cache), 'best_score': best,
            'best_block': best_block, 'best_mask': best_mask,
            'winner_blue_red': list(map(len, bad)), 'red_edges': sum(map(int.bit_count, winner))//2,
            'degree_histogram': dict(sorted(Counter(map(int.bit_count, winner)).items())),
            'graph_sha256': sha256(edge_bytes(winner)).hexdigest(), 'complete_defects': bad,
            'ramsey_target': best == 0, 'improved_below_123': best < 123,
            'literal_table_assignments_checked': table_checks,
            'minimum_trust': 'All production minima use the native subset transform; this audit independently checks physical argmin witnesses, not every production table entry.'}


def polynomial_controls():
    checked = 0
    for k in range(7):
        for states in product(range(3), repeat=k):
            p = sum(1 << i for i, state in enumerate(states) if state == 1)
            q = sum(1 << i for i, state in enumerate(states) if state == 2)
            a = [0]*(1 << k)
            sub = q
            while True:
                a[p | sub] += (-1)**sub.bit_count()
                if not sub:
                    break
                sub = (sub-1) & q
            for j in range(k):
                for mask in range(1 << k):
                    if mask & (1 << j):
                        a[mask] += a[mask ^ (1 << j)]
            expected = [int((mask & p) == p and not mask & q) for mask in range(1 << k)]
            need(a == expected, 'all ternary event polynomials')
            checked += 1
    return checked


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('parent', type=Path)
    p.add_argument('work', type=Path)
    p.add_argument('--count', type=int, required=True)
    p.add_argument('--bits', type=int, required=True)
    p.add_argument('--table', type=Path)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--controls', action='store_true')
    a = p.parse_args()
    result = run(a.parent, a.work, a.count, a.bits, a.table)
    if a.controls:
        result['all_ternary_event_polynomials_checked'] = polynomial_controls()
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(result['status'], result['best_score'], result['minimum_histogram'],
          result['literal_table_assignments_checked'], result.get('all_ternary_event_polynomials_checked', 0))
