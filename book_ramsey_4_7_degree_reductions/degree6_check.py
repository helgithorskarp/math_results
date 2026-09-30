#!/usr/bin/env python3
"""Complete normalized classification of ERG(15,8,3).

The analytic coverage argument and attachment obstruction are in degree6.md.
Two different generators are compared entry by entry. Every candidate's
edge-regularity decision is checked with bitsets and literal neighbor lists.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json


def add(adj, a, b):
    adj[a] |= 1 << b
    adj[b] |= 1 << a


def normalize_edges(edges):
    return tuple(sorted(tuple(sorted(edge)) for edge in edges))


def local_patterns():
    fixed = [(0, 1), (0, 6), (0, 7), (1, 4), (1, 5)]
    possible = [(2, 3)] + [(s, d) for s in (2, 3) for d in (4, 5, 6, 7)] + [
        (b, c) for b in (4, 5) for c in (6, 7)
    ]
    found = set()
    for subset in combinations(possible, 7):
        adj = [0] * 8
        for a, b in fixed + list(subset):
            add(adj, a, b)
        if all(x.bit_count() == 3 for x in adj) and all(
            not adj[a] & adj[b] for a, b in fixed + list(subset)
        ):
            found.add(normalize_edges(subset))
    return found


def local_patterns_constructive():
    # The two S vertices are either adjacent or nonadjacent.
    found = set()
    # Adjacent: D_b--D_c is a matching; split D into two pairs, with
    # no matching edge's endpoints assigned to the same S vertex.
    for order in permutations((6, 7)):
        matching = [(4, order[0]), (5, order[1])]
        for first in combinations((4, 5, 6, 7), 2):
            if any(a in first and b in first for a, b in matching):
                continue
            second = set((4, 5, 6, 7)) - set(first)
            edges = [(2, 3)] + matching + [(2, d) for d in first] + [(3, d) for d in second]
            found.add(normalize_edges(edges))
    # Nonadjacent: D_b--D_c has one edge. Each S misses a different
    # endpoint; both S vertices meet the other two D vertices.
    for b, c in product((4, 5), (6, 7)):
        for missed in [(b, c), (c, b)]:
            edges = [(b, c)] + [(s, d) for s, omit in zip((2, 3), missed) for d in (4, 5, 6, 7) if d != omit]
            found.add(normalize_edges(edges))
    return found


def cross_cycles():
    pairs = [(a, b) for a, b in combinations(range(3, 9), 2) if (a - 3) // 2 != (b - 3) // 2]
    found = set()
    for subset in combinations(pairs, 6):
        degree = Counter(a for edge in subset for a in edge)
        if all(degree[a] == 2 for a in range(3, 9)):
            found.add(normalize_edges(subset))
    return found


def cross_cycles_constructive():
    # A simple 2-regular graph on six vertices is a six-cycle or two
    # triangles. No edge may be within a prescribed two-vertex part.
    found = set()
    def allowed(edges):
        return all((a - 3) // 2 != (b - 3) // 2 for a, b in edges)
    for rest in permutations(range(4, 9)):
        cycle = (3,) + rest
        edges = list(zip(cycle, cycle[1:] + cycle[:1]))
        if allowed(edges):
            found.add(normalize_edges(edges))
    for first in combinations(range(3, 9), 3):
        second = sorted(set(range(3, 9)) - set(first))
        edges = list(combinations(first, 2)) + list(combinations(second, 2))
        if allowed(edges):
            found.add(normalize_edges(edges))
    return found


def grid_certificate(adj):
    # Three disjoint independent five-sets supply the rows. Their
    # blue neighbors in other rows supply five independent columns.
    rows = []
    for subset in combinations(range(15), 5):
        mask = sum(1 << v for v in subset)
        if all(not adj[v] & mask for v in subset):
            rows.append(subset)
    assert len(rows) == 3
    assert len(set().union(*map(set, rows))) == 15
    row_of = {v: i for i, row in enumerate(rows) for v in row}
    columns = []
    remaining = set(range(15))
    while remaining:
        v = min(remaining)
        column = {v} | {u for u in range(15) if row_of[u] != row_of[v] and not adj[v] >> u & 1}
        assert len(column) == 3 and len({row_of[u] for u in column}) == 3
        assert column <= remaining
        columns.append(tuple(sorted(column)))
        remaining -= column
    assert len(columns) == 5
    column_of = {v: i for i, column in enumerate(columns) for v in column}
    for a, b in combinations(range(15), 2):
        assert bool(adj[a] >> b & 1) == (row_of[a] != row_of[b] and column_of[a] != column_of[b])
    return rows, columns


def main():
    local = sorted(local_patterns())
    cycles = sorted(cross_cycles())
    assert set(local) == local_patterns_constructive()
    assert set(cycles) == cross_cycles_constructive()
    assert len(local) == 16 and len(cycles) == 20
    fixed = [(0, 1), (0, 2), (1, 2)]
    for i in range(3):
        single = [3 + 2 * i, 4 + 2 * i]
        double = [9 + 2 * i, 10 + 2 * i]
        fixed += [(i, s) for s in single]
        fixed += [(t, d) for t in range(3) if t != i for d in double]
        fixed += [(s, d) for s in single for d in double]
    mappings = []
    for i in range(3):
        j, k = [t for t in range(3) if t != i]
        mapping = [j, k, 3 + 2 * i, 4 + 2 * i, 9 + 2 * j, 10 + 2 * j, 9 + 2 * k, 10 + 2 * k]
        mappings.append([[(mapping[a], mapping[b]) for a, b in pattern] for pattern in local])
    stream = sha256()
    witness_stream = sha256()
    checked = accepted = 0
    for p, q, r in product(range(16), repeat=3):
        edges = fixed + mappings[0][p] + mappings[1][q] + mappings[2][r]
        for cycle in cycles:
            all_edges = edges + list(cycle)
            assert len(normalize_edges(all_edges)) == len(set(normalize_edges(all_edges))) == 60
            adj = [0] * 15
            neighbors = [[] for _ in range(15)]
            for a, b in all_edges:
                add(adj, a, b)
                neighbors[a].append(b)
                neighbors[b].append(a)
            assert all(row.bit_count() == 8 for row in adj)
            assert all(len(row) == 8 for row in neighbors)
            encoding = b''.join(row.to_bytes(2, 'little') for row in adj)
            stream.update(encoding)
            checked += 1
            bitset_decision = all((adj[a] & adj[b]).bit_count() == 3 for a, b in all_edges)
            literal_decision = all(sum(u in neighbors[b] for u in neighbors[a]) == 3 for a, b in all_edges)
            assert bitset_decision == literal_decision
            if bitset_decision:
                accepted += 1
                rows, columns = grid_certificate(adj)
                witness_stream.update(encoding)
    assert checked == 81920 and accepted == 32
    print(json.dumps({
        'agent': 'six-books-1',
        'local_patterns': len(local),
        'cross_cycles': len(cycles),
        'candidates_checked': checked,
        'edge_regular_candidates': accepted,
        'grid_certificates_checked': accepted,
        'isomorphism_types': 1,
        'unique_type': 'K3 tensor K5; complement of the 3 by 5 rook graph',
        'candidate_stream_sha256': stream.hexdigest(),
        'witness_stream_sha256': witness_stream.hexdigest(),
        'degree6_attachment_row_pair_demand': 120,
        'degree6_attachment_row_pair_capacity': 72,
        'degree_range22_with_classification': [7, 12],
        'trust_boundary': 'Python exact integer/list operations; unformalized analytic normalization and attachment proof',
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
