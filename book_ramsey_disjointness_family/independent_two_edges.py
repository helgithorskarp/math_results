#!/usr/bin/env python3
"""Reconstruct from triples; classify by indexed constraints and literal pages.

Imports no generator code. All trace domains are compared entry by entry,
not merely by their sizes or hashes. Assertions must remain enabled.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
if not __debug__:
    raise RuntimeError('run this checker with Python assertions enabled')
Y = [1, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 20, 23, 24]


def core_from_triples():
    blocks = [frozenset((x+d) % 13 for d in base)
              for base in [(0, 1, 4), (0, 2, 7)] for x in range(13)]
    assert len(set(blocks)) == 26
    assert all(sum(set(p) <= b for b in blocks) == 1
               for p in combinations(range(13), 2))
    triples = [blocks[i] for i in Y]
    return [frozenset(j for j, b in enumerate(triples)
                      if i != j and not a & b)
            for i, a in enumerate(triples)]


def internal(path):
    edges = [(3, 4), (3, 5)] if path else [(2, 3), (4, 5)]
    red = [set() for _ in range(6)]
    for i, j in edges:
        red[i].add(j)
        red[j].add(i)
    blue = [set(range(6))-{i}-red[i] for i in range(6)]
    return red, blue


def known_adjacency(core, masks, J):
    """Unknown cross edges belong to neither color; all J edges are known."""
    vertices = set(range(16))
    red = [set(s) for s in core]+[set() for _ in range(6)]
    blue = [vertices-{i}-set(s) for i, s in enumerate(core)]+[set() for _ in range(6)]
    for role in range(6):
        red[16+role] = {16+j for j in J[0][role]}
        blue[16+role] = {16+j for j in J[1][role]}
    for role, mask in masks.items():
        for y in range(16):
            adjacency = red if mask >> y & 1 else blue
            adjacency[16+role].add(y)
            adjacency[y].add(16+role)
    return red, blue


def first_book(core, masks, J):
    for color, adjacency in enumerate(known_adjacency(core, masks, J)):
        cap = [3, 6][color]
        for i in range(22):
            for j in range(i):
                if j in adjacency[i]:
                    pages = adjacency[i] & adjacency[j]
                    if len(pages) > cap:
                        return color, j, i, sorted(pages)[:cap+1]
    return None


def read_trace(path):
    rows, ten_cases, ordinary, matching, pairs, triples = [], [], [], {}, {}, {}
    for line in Path(path).read_text().splitlines():
        tag, *values = line.split()
        a = list(map(int, values))
        if tag == 'R':
            assert len(a) == 1
            rows.append(a[0])
        elif tag == 'H':
            assert len(a) == 7+[4, 7][a[4]]
            ten_cases.append(a)
        elif tag == 'O':
            assert len(a) == 2
            ordinary.append(tuple(a))
        elif tag == 'M':
            assert len(a) == 3+a[2] and tuple(a[:2]) not in matching
            matching[tuple(a[:2])] = a[3:]
        elif tag == 'P':
            assert len(a) == 4
            pairs.setdefault(tuple(a[:2]), []).append(tuple(a[2:]))
        elif tag == 'T':
            key = tuple(a[:3])
            assert key not in triples
            count = a[3]
            centers = a[4:4+count]
            leaf_count = a[4+count]
            leaves = a[5+count:]
            assert len(leaves) == leaf_count
            triples[key] = (centers, leaves)
        else:
            raise AssertionError('unrecognized trace record')
    assert len(ordinary) == len(set(ordinary))
    return rows, ten_cases, ordinary, matching, pairs, triples


def compute(trace_path):
    core = core_from_triples()
    fixture = (HERE/'core16.edges').read_text().splitlines()
    assert fixture[0] == '16'
    fixture_edges = [tuple(map(int, line.split())) for line in fixture[1:]]
    assert len(fixture_edges) == len(set(fixture_edges)) == 48
    assert set(fixture_edges) == {(i, j) for i in range(16) for j in core[i] if j < i}
    vertices = frozenset(range(16))
    blue_core = [vertices-{i}-ns for i, ns in enumerate(core)]
    assert all(len(s) == 6 for s in core)
    spines = [(i, j, color) for color, adjacency in enumerate([core, blue_core])
              for i in range(16) for j in range(i) if j in adjacency[i]]
    capacities = [[3, 6][c]-len([core, blue_core][c][i] & [core, blue_core][c][j])
                  for i, j, c in spines]
    assert Counter(capacities) == {0: 3, 1: 45, 2: 69, 3: 3}
    zero = [(i, j, c) for (i, j, c), cap in zip(spines, capacities) if cap == 0]
    # Combination traversal and literal neighborhoods, rather than mask scan.
    row_sets = {}
    for size in range(17):
        for subset in combinations(range(16), size):
            ns = frozenset(subset)
            if any(len(core[y] & ns) > 3 for y in ns):
                continue
            bs = vertices-ns
            if any(i in [ns, bs][c] and j in [ns, bs][c] for i, j, c in zero):
                continue
            if any(len(blue_core[y] & bs) > 6 for y in bs):
                continue
            row_sets[sum(1 << y for y in ns)] = (ns, bs)
    masks = sorted(row_sets)
    ns = [row_sets[m][0] for m in masks]
    bs = [row_sets[m][1] for m in masks]
    m = len(masks)
    all_rows = (1 << m)-1
    row_id = {mask: i for i, mask in enumerate(masks)}
    observed, h_trace, o_trace, m_trace, p_trace, t_trace = read_trace(trace_path)
    assert observed == masks, 'complete row domain disagrees'
    ten = [i for i, n in enumerate(ns) if len(n) == 10]
    assert len(ten) == 4
    assert all(len(core[y] & ns[i]) == 3 for i in ten for y in ns[i])
    not_ten = all_rows ^ sum(1 << i for i in ten)
    matching_J, path_J = internal(False), internal(True)
    expected_ten_metadata = []
    for a in ten:
        for e, f in combinations([i for i in ten if i != a], 2):
            b = 65535 ^ masks[a]
            while True:
                expected_ten_metadata.append([masks[e], masks[f], masks[a], b])
                if b == 0:
                    break
                b = (b-1) & (65535 ^ masks[a])
    assert [h[:4] for h in h_trace] == expected_ten_metadata
    for e, f, a, b, color, i, j, *pages in h_trace:
        adjacency = known_adjacency(core, {0: e, 1: f, 2: a, 3: b}, matching_J)[color]
        assert i != j and j in adjacency[i]
        assert len(pages) == [4, 7][color] and len(set(pages)) == len(pages)
        assert all(p in adjacency[i] & adjacency[j] for p in pages)
    # Bit sets index rows, not core vertex assignments. All tables below are
    # derived from literal page definitions in this independent reconstruction.
    points = [sum(1 << i for i in range(m) if y in ns[i]) for y in range(16)]
    new_red = [[sum(1 << i for i in range(m)
                    if y not in ns[i] or len(core[y] & ns[i])+k <= 3)
                for k in range(6)] for y in range(16)]
    new_blue = [[sum(1 << i for i in range(m)
                     if y not in bs[i] or len(blue_core[y] & bs[i])+k <= 6)
                 for k in range(6)] for y in range(16)]
    features = [frozenset(k for k, (a, b, c) in enumerate(spines)
                          if a in [ns[i], bs[i]][c] and b in [ns[i], bs[i]][c])
                for i in range(m)]
    spine_rows = [sum(1 << i for i in range(m) if k in features[i])
                  for k in range(len(spines))]
    compat = {(0, 3): [0]*m, **{(1, cap): [0]*m for cap in [2, 3, 4]}}
    for i in range(m):
        for j in range(i, m):
            common_red = (masks[i] & masks[j]).bit_count()
            common_blue = ((65535 ^ masks[i]) & (65535 ^ masks[j])).bit_count()
            for key, good in [((0, 3), common_red <= 3),
                              ((1, 2), common_blue <= 2),
                              ((1, 3), common_blue <= 3),
                              ((1, 4), common_blue <= 4)]:
                if good:
                    compat[key][i] |= 1 << j
                    compat[key][j] |= 1 << i

    def members(bits):
        while bits:
            low = bits & -bits
            yield low.bit_length()-1
            bits ^= low

    def domain(context, role, J, base=all_rows):
        allowed = base
        # First intersect whole indexed pair domains. No branch is dropped
        # by a heuristic; every intersection expresses a spine inequality.
        for old_role, old_id in context:
            color = 0 if old_role in J[0][role] else 1
            cap = [3, 6][color]-len(J[color][role] & J[color][old_role])
            allowed &= compat[color, cap][old_id]
            if not allowed:
                return 0
        used = Counter(k for _, old_id in context for k in features[old_id])
        for k, count in used.items():
            assert count <= capacities[k], 'invalid input context'
            if count == capacities[k]:
                allowed &= all_rows ^ spine_rows[k]
                if not allowed:
                    return 0
        for old_role, old_id in context:
            color = 0 if old_role in J[0][role] else 1
            neighbor_set = [ns, bs][color][old_id]
            for y in neighbor_set:
                pages = len([core, blue_core][color][y] & neighbor_set)
                pages += sum(other_role in J[color][old_role] and
                             y in [ns, bs][color][other_id]
                             for other_role, other_id in context)
                assert pages <= [3, 6][color]
                if pages == [3, 6][color]:
                    allowed &= (all_rows ^ points[y]) if color == 0 else points[y]
                    if not allowed:
                        return 0
        for y in range(16):
            r = sum(old_role in J[0][role] and y in ns[old_id]
                    for old_role, old_id in context)
            b = sum(old_role in J[1][role] and y in bs[old_id]
                    for old_role, old_id in context)
            allowed &= new_red[y][r] & new_blue[y][b]
            if not allowed:
                return 0
        return allowed

    ordinary = []
    for e in range(m):
        bits = domain([(0, e)], 1, matching_J) >> (e+1) << (e+1)
        ordinary.extend((e, f) for f in members(bits))
    assert [(masks[e], masks[f]) for e, f in ordinary] == o_trace
    assert set(m_trace) == set(o_trace)
    found_pairs = {}
    matching_contexts = 0
    for e, f in ordinary:
        context = [(0, e), (1, f)]
        bits = domain(context, 2, matching_J, not_ten)
        ids = list(members(bits))
        key = masks[e], masks[f]
        assert [masks[i] for i in ids] == m_trace[key]
        if len(ids) < 4:
            continue
        matching_contexts += 1
        pairs = []
        for a in ids:
            partners = domain(context+[(2, a)], 3, matching_J, bits)
            partners = partners >> (a+1) << (a+1)
            pairs.extend((masks[a], masks[b]) for b in members(partners))
        if pairs:
            found_pairs[key] = pairs
            for a, b in pairs:
                assert first_book(core, {0: masks[e], 1: masks[f], 2: a, 3: b}, matching_J) is None
        assert len(pairs) <= 1, 'matching case needs further classification'
    assert found_pairs == p_trace
    found_triples, rejected_center_leaf = {}, 0
    for e, f in ordinary:
        context = [(0, e), (1, f)]
        thirds = domain(context, 2, path_J) >> (f+1) << (f+1)
        for g in members(thirds):
            three = context+[(2, g)]
            center_ids = list(members(domain(three, 3, path_J, not_ten)))
            leaf_ids = list(members(domain(three, 4, path_J)))
            key = masks[e], masks[f], masks[g]
            found_triples[key] = ([masks[c] for c in center_ids], [masks[a] for a in leaf_ids])
            for c in center_ids:
                assert first_book(core, {0: masks[e], 1: masks[f], 2: masks[g], 3: masks[c]}, path_J) is None
                assert domain(three+[(3, c)], 4, path_J) == 0
                for a in leaf_ids:
                    assert first_book(core, {0: masks[e], 1: masks[f], 2: masks[g], 3: masks[c], 4: masks[a]}, path_J) is not None
                    rejected_center_leaf += 1
            for a in leaf_ids:
                assert first_book(core, {0: masks[e], 1: masks[f], 2: masks[g], 4: masks[a]}, path_J) is None
    assert found_triples == t_trace
    expected = json.loads((HERE/'two_edges_expected.json').read_text())
    assert expected['trace_sha256'] == sha256(Path(trace_path).read_bytes()).hexdigest()
    return {'agent': 'six-books-2', 'role': 'researcher',
            'row_domains_agree_entry_by_entry': len(masks),
            'verified_ten_endpoint_books': len(h_trace),
            'ordinary_pair_domains_agree_entry_by_entry': len(ordinary),
            'matching_row_domains_agree_entry_by_entry': len(m_trace),
            'matching_contexts_with_at_least_four_rows': matching_contexts,
            'matching_red_pair_records_agree_entry_by_entry': sum(map(len, found_pairs.values())),
            'path_triple_and_role_domains_agree_entry_by_entry': len(found_triples),
            'literal_rejected_center_leaf_books': rejected_center_leaf,
            'degree_or_edge_bounds_used': False,
            'complete': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('trace')
    args = parser.parse_args()
    print(json.dumps(compute(args.trace), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
