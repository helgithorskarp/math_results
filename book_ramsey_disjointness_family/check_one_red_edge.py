#!/usr/bin/env python3
"""Exact endpoint reduction and compact book witnesses; Python stdlib only."""
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json

from verify_cross_repair import fixture, bitmask_rows

HERE = Path(__file__).resolve().parent


def build_graph(core, row_masks, internal_red_edges=()):
    graph = [set(ns) for ns in core]+[set() for _ in row_masks]
    for k, mask in enumerate(row_masks, len(core)):
        for y in range(len(core)):
            if mask >> y & 1:
                graph[k].add(y)
                graph[y].add(k)
    for i, j in internal_red_edges:
        i, j = i+len(core), j+len(core)
        graph[i].add(j)
        graph[j].add(i)
    return graph


def first_book(graph):
    vertices = set(range(len(graph)))
    blue = [vertices-{i}-ns for i, ns in enumerate(graph)]
    for color, adjacency, cap in [('red', graph, 3), ('blue', blue, 6)]:
        for i in range(len(graph)):
            for j in range(i):
                if j in adjacency[i]:
                    pages = sorted(adjacency[i] & adjacency[j])
                    if len(pages) > cap:
                        return {'color': color, 'spine': [j, i], 'pages': pages[:cap+1]}
    return None


def compute(return_details=False):
    graph = fixture()
    assert all(len(ns) == 6 for ns in graph)
    adj = [sum(1 << j for j in ns) for ns in graph]
    full = (1 << 16)-1
    blue = [full ^ adj[i] ^ (1 << i) for i in range(16)]
    red_edges = [(i, j) for i in range(16) for j in range(i) if j in graph[i]]
    blue_edges = [(i, j) for i in range(16) for j in range(i) if j not in graph[i]]
    assert len(red_edges) == 48 and len(blue_edges) == 72
    red_caps = [3-len(graph[i] & graph[j]) for i, j in red_edges]
    blue_caps = [6-(blue[i] & blue[j]).bit_count() for i, j in blue_edges]
    assert Counter(red_caps) == {0: 3, 1: 18, 2: 27}
    assert Counter(blue_caps) == {1: 27, 2: 42, 3: 3}
    red_zero = sum(1 << k for k, c in enumerate(red_caps) if c == 0)
    red_one = sum(1 << k for k, c in enumerate(red_caps) if c == 1)
    blue_one = sum(1 << k for k, c in enumerate(blue_caps) if c == 1)
    stream, profiles, unused = bitmask_rows(graph)

    @lru_cache(None)
    def max_load(histogram):
        caps = [c for c, count in enumerate(histogram) for _ in range(count)]
        result = sum(c >= 1 for c in caps)
        budget = 12
        for level in [2, 3, 4]:
            take = min(sum(c >= level for c in caps), budget//(level-1))
            result += take
            budget -= take*(level-1)
        # Exact integer dynamic program checks the marginal-cost calculation.
        dp = [-1]*13
        dp[0] = 0
        for cap in caps:
            next_dp = [-1]*13
            for spent, load in enumerate(dp):
                if load < 0:
                    continue
                for b in range(cap+1):
                    cost = b*(b-1)//2
                    if spent+cost <= 12:
                        next_dp[spent+cost] = max(next_dp[spent+cost], load+b)
            dp = next_dp
        assert result == max(dp)
        return result

    def cap_hist(caps):
        return tuple(caps.count(c) for c in range(5))

    ten = [m for m, e in enumerate(stream) if e != 255 and m.bit_count() == 10]
    assert len(ten) == 4
    assert all((adj[i] & m).bit_count() == 3 for m in ten for i in range(16) if m >> i & 1)
    four_ten = build_graph(graph, ten)
    four_ten_pages = sorted(four_ten[2] & four_ten[6])
    assert four_ten_pages == [8, 9, 16, 18]
    four_ten_witness = {'color': 'red', 'spine': [2, 6], 'pages': four_ten_pages}

    rows, unary_counts = [], Counter()
    for n, e in enumerate(stream):
        if e == 255 or n.bit_count() == 10:
            continue
        # Ten endpoint rows are ruled out by the written empty-T argument.
        rfeat = sum(1 << k for k, (i, j) in enumerate(red_edges) if n >> i & n >> j & 1)
        if rfeat & red_zero:
            continue
        b = full ^ n
        caps = [min(4, 7-b.bit_count()+(adj[y] & b).bit_count())
                if b >> y & 1 else 4 for y in range(16)]
        if min(caps) < 0 or max_load(cap_hist(caps)) < 24:
            continue
        bfeat = sum(1 << k for k, (i, j) in enumerate(blue_edges) if b >> i & b >> j & 1)
        low = sum(1 << y for y in range(16) if n >> y & 1 and (adj[y] & n).bit_count() <= 2)
        rows.append((n, b, e, rfeat, bfeat, low, caps))
        unary_counts[n.bit_count()] += 1
    assert unary_counts == {6: 23, 7: 871, 8: 801, 9: 91}

    stage, accepted, by_sizes = Counter(), [], Counter()
    for ia, a in enumerate(rows):
        for b in rows[ia+1:]:
            stage['all_distinct_unordered_unary_pairs'] += 1
            common = a[0] & b[0]
            if not 1 <= common.bit_count() <= 3:
                continue
            stage['intersection_1_to_3'] += 1
            if common & ~(a[5] & b[5]):
                continue
            stage['red_endpoint_cross_spines'] += 1
            if a[3] & b[3] & red_one or a[4] & b[4] & blue_one:
                continue
            stage['core_spine_capacities'] += 1
            caps = [min(x, y) for x, y in zip(a[6], b[6])]
            load = max_load(cap_hist(caps))
            if load < 24:
                continue
            stage['joint_column_capacity'] += 1
            accepted.append({'a_mask': a[0], 'b_mask': b[0], 'a_size': a[0].bit_count(),
                             'b_size': b[0].bit_count(), 'edge_cost': a[2]+b[2],
                             'intersection_size': common.bit_count(),
                             'column_caps': caps, 'max_ordinary_blue_load': load})
            by_sizes[tuple(sorted((a[0].bit_count(), b[0].bit_count())))] += 1
    load_hist = Counter(p['max_ordinary_blue_load'] for p in accepted)
    assert load_hist == {24: 99, 25: 3}
    partial_witnesses = []
    for pair in accepted:
        if pair['max_ordinary_blue_load'] != 25:
            continue
        for triple in combinations(ten, 3):
            masks = [pair['a_mask'], pair['b_mask'], *triple]
            partial = build_graph(graph, masks, [(0, 1)])
            witness = first_book(partial)
            assert witness is not None
            partial_witnesses.append({'a_mask': pair['a_mask'], 'b_mask': pair['b_mask'],
                                      'ten_rows': list(triple), 'witness': witness})
    assert len(partial_witnesses) == 12
    unary_masks = [r[0] for r in rows]
    unary_bytes = b''.join(m.to_bytes(2, 'little') for m in unary_masks)
    pair_bytes = json.dumps(accepted, sort_keys=True, separators=(',', ':')).encode()
    output = {
        'agent': 'six-books-2', 'role': 'researcher',
        'scope': 'Fixed core F and exactly one red edge inside X; all 2^96 cross assignments excluded by the analytic reduction.',
        'ten_row_masks': ten, 'four_ten_row_book': four_ten_witness,
        'unary_endpoint_rows': len(rows), 'unary_by_size': dict(sorted(unary_counts.items())),
        'unary_rows_sha256': sha256(unary_bytes).hexdigest(),
        'pair_stage_counts': dict(stage),
        'surviving_sizes': {str(k): v for k, v in sorted(by_sizes.items())},
        'surviving_endpoint_pairs': len(accepted),
        'joint_max_load_histogram': dict(sorted(load_hist.items())),
        'surviving_pairs_sha256': sha256(pair_bytes).hexdigest(),
        'distinct_column_capacity_histograms_checked': max_load.cache_info().currsize,
        'partial_book_witnesses': partial_witnesses,
        'fixed_internal_edge_cross_assignments_covered': '2^96',
        'internal_edge_positions_covered_by_relabeling_X': 15,
        'cross_assignments_enumerated': False}
    output = json.loads(json.dumps(output))
    return (output, unary_masks, accepted) if return_details else output


def main():
    output = compute()
    expected = json.loads((HERE/'one_edge_expected.json').read_text())
    if output != expected:
        raise AssertionError('compact expected output mismatch')
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
