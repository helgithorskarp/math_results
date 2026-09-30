#!/usr/bin/env python3
"""Literal triple/set traversal and book-certificate checking."""
from collections import Counter
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json

from check_one_red_edge import compute

HERE = Path(__file__).resolve().parent


def literal_enumeration():
    blocks = [frozenset((x+z)%13 for z in base)
              for base in [(0, 1, 4), (0, 2, 7)] for x in range(13)]
    assert [sorted(b) for b in blocks] == json.loads((HERE/'steiner_blocks.json').read_text())
    indices = [1, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 20, 23, 24]
    triples = [blocks[i] for i in indices]
    graph = [{j for j, b in enumerate(triples) if i != j and not (a & b)}
             for i, a in enumerate(triples)]
    vertices = set(range(16))
    blue = [vertices-{i}-ns for i, ns in enumerate(graph)]
    red_edges = [(i, j) for i in range(16) for j in range(i) if j in graph[i]]
    blue_edges = [(i, j) for i in range(16) for j in range(i) if j in blue[i]]

    @lru_cache(None)
    def load(caps):
        reachable = {(0, 0)}
        for cap in caps:
            reachable = {(spent+b*(b-1)//2, total+b)
                         for spent, total in reachable for b in range(cap+1)
                         if spent+b*(b-1)//2 <= 12}
        return max(total for spent, total in reachable)

    rows, ten = [], []
    for t in range(17):
        for chosen in combinations(range(16), t):
            n = set(chosen)
            degrees = {y: len(graph[y] & n) for y in n}
            if any(d > 3 for d in degrees.values()):
                continue
            assert t <= 10
            if t == 10:
                assert all(d == 3 for d in degrees.values())
                ten.append(n)
                continue
            if any(len(graph[i] & graph[j])+int(i in n and j in n) > 3
                   for i, j in red_edges):
                continue
            b = vertices-n
            caps = tuple(min(4, 7-len(b)+len(graph[y] & b)) if y in b else 4
                         for y in range(16))
            if min(caps) < 0 or load(tuple(sorted(caps))) < 24:
                continue
            mask = sum(2**i for i in n)
            rows.append((mask, n, b, sum(degrees.values())//2,
                         {y for y, d in degrees.items() if d <= 2}, caps))
    rows.sort(key=lambda r: r[0])
    stage, accepted = Counter(), []
    for ia, a in enumerate(rows):
        for b in rows[ia+1:]:
            stage['all_distinct_unordered_unary_pairs'] += 1
            common = a[1] & b[1]
            if not 1 <= len(common) <= 3:
                continue
            stage['intersection_1_to_3'] += 1
            if not common <= a[4] & b[4]:
                continue
            stage['red_endpoint_cross_spines'] += 1
            if any(len(graph[i] & graph[j])+int(i in a[1] and j in a[1])
                   +int(i in b[1] and j in b[1]) > 3 for i, j in red_edges):
                continue
            if any(len(blue[i] & blue[j])+int(i in a[2] and j in a[2])
                   +int(i in b[2] and j in b[2]) > 6 for i, j in blue_edges):
                continue
            stage['core_spine_capacities'] += 1
            caps = tuple(min(x, y) for x, y in zip(a[5], b[5]))
            maximum = load(tuple(sorted(caps)))
            if maximum < 24:
                continue
            stage['joint_column_capacity'] += 1
            accepted.append({'a_mask': a[0], 'b_mask': b[0], 'a_size': len(a[1]), 'b_size': len(b[1]),
                             'edge_cost': a[3]+b[3], 'intersection_size': len(common),
                             'column_caps': list(caps), 'max_ordinary_blue_load': maximum})
    return graph, [r[0] for r in rows], ten, dict(stage), accepted


def decode(mask):
    if not 0 <= mask < 65536:
        raise ValueError('malformed sixteen-vertex row')
    return {i for i in range(16) if (mask//(2**i)) % 2}


def check_witness(core, masks, internal_red_edge, witness):
    graph = [set(ns) for ns in core]+[decode(m) for m in masks]
    for k, ns in enumerate(graph[16:], 16):
        for y in ns:
            graph[y].add(k)
    if internal_red_edge:
        graph[16].add(17)
        graph[17].add(16)
    if witness['color'] == 'red':
        color, pages_required = graph, 4
    elif witness['color'] == 'blue':
        color = [set(range(len(graph)))-{i}-ns for i, ns in enumerate(graph)]
        pages_required = 7
    else:
        raise ValueError('unknown color')
    s, t = witness['spine']
    pages = witness['pages']
    assert t in color[s] and len(set(pages)) == len(pages) >= pages_required
    assert s not in pages and t not in pages
    assert all(p in color[s] and p in color[t] for p in pages)


def main():
    core, literal_rows, ten, stages, literal_pairs = literal_enumeration()
    first, bit_rows, bit_pairs = compute(return_details=True)
    assert first == json.loads((HERE/'one_edge_expected.json').read_text())
    assert literal_rows == bit_rows, 'unary row sets disagree entry by entry'
    assert literal_pairs == bit_pairs, 'endpoint pairs disagree entry by entry'
    assert stages == first['pair_stage_counts']
    assert sorted(sum(2**i for i in n) for n in ten) == first['ten_row_masks']
    check_witness(core, first['ten_row_masks'], False, first['four_ten_row_book'])
    for case in first['partial_book_witnesses']:
        check_witness(core, [case['a_mask'], case['b_mask'], *case['ten_rows']], True, case['witness'])
    print(json.dumps({'agent': 'six-books-2', 'role': 'researcher',
                      'unary_row_entry_level_agreement': len(literal_rows),
                      'endpoint_pair_entry_level_agreement': len(literal_pairs),
                      'pair_stage_counts': stages, 'book_certificates_checked': 13}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
