#!/usr/bin/env python3
"""Complete row lemma for the explicit core; two exact labeled traversals."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
DELETED = [0, 18, 21, 22]
X = [2, 5, 6, 17, 19, 25]
Y = [1, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 20, 23, 24]


def fixture():
    lines = (HERE / "core16.edges").read_text().splitlines()
    n = int(lines[0])
    if n != 16:
        raise ValueError("the core must have sixteen vertices")
    graph = [set() for _ in range(n)]
    for line in lines[1:]:
        i, j = map(int, line.split())
        if not 0 <= j < i < n or j in graph[i]:
            raise ValueError("invalid or duplicate simple edge")
        graph[i].add(j)
        graph[j].add(i)
    return graph


def reconstruct():
    blocks = [frozenset((x + y) % 13 for y in base)
              for base in [(0, 1, 4), (0, 2, 7)] for x in range(13)]
    assert [sorted(b) for b in blocks] == json.loads(
        (HERE / "steiner_blocks.json").read_text())
    assert len(set(blocks)) == 26 and all(len(b) == 3 for b in blocks)
    assert all(sum(set(pair) <= b for b in blocks) == 1
               for pair in combinations(range(13), 2))
    assert set.union(*(set(blocks[i]) for i in DELETED)) == set(range(13)) - {6}
    assert all(not blocks[i] & blocks[j] for i, j in combinations(DELETED, 2))
    remaining = set(range(26)) - set(DELETED)
    assert sorted(i for i in remaining if 6 in blocks[i]) == X
    assert sorted(remaining - set(X)) == Y
    assert all(blocks[i] & blocks[j] for i, j in combinations(X, 2))
    return [blocks[i] for i in Y]


def bitmask_rows(graph):
    masks = [sum(1 << j for j in ns) for ns in graph]
    stream = bytearray([255]) * (1 << 16)
    profiles = {t: Counter() for t in range(17)}
    unrestricted_min = {t: 49 for t in range(17)}
    for subset in range(1 << 16):
        work, degrees = subset, []
        while work:
            bit = work & -work
            i = bit.bit_length() - 1
            degrees.append((masks[i] & subset).bit_count())
            work ^= bit
        t = len(degrees)
        assert sum(degrees) % 2 == 0
        edges = sum(degrees) // 2
        unrestricted_min[t] = min(unrestricted_min[t], edges)
        if max(degrees, default=0) <= 3:
            assert t <= 10 and edges >= 5*t - 35
            stream[subset] = edges
            profiles[t][edges] += 1
    return stream, profiles, unrestricted_min


def combination_rows(blocks):
    """Use the triple definition, not the fixture or the first adjacency masks."""
    stream = bytearray([255]) * (1 << len(blocks))
    visited = 0
    for t in range(len(blocks) + 1):
        for subset in combinations(range(len(blocks)), t):
            edges = sum(not (blocks[i] & blocks[j])
                        for i, j in combinations(subset, 2))
            degrees = [sum(not (blocks[i] & blocks[j])
                           for j in subset if j != i) for i in subset]
            assert sum(degrees) == 2*edges
            if max(degrees, default=0) <= 3:
                mask = sum(2**i for i in subset)
                stream[mask] = edges
            visited += 1
    assert visited == 65536
    return stream


def compute():
    graph, blocks = fixture(), reconstruct()
    assert graph == [{j for j, b in enumerate(blocks)
                      if j != i and not (a & b)} for i, a in enumerate(blocks)]
    edges = [(i, j) for i, ns in enumerate(graph) for j in sorted(ns) if j < i]
    codegrees = Counter(len(graph[i] & graph[j]) for i, j in edges)
    assert len(edges) == 48 and all(len(ns) == 6 for ns in graph)
    assert codegrees == {1: 27, 2: 18, 3: 3}
    codegree_sum = sum(k*v for k, v in codegrees.items())
    assert codegree_sum == 72
    first, profiles, unrestricted = bitmask_rows(graph)
    second = combination_rows(blocks)
    assert first == second, "labeled row streams disagree"
    counts = {t: sum(hist.values()) for t, hist in profiles.items() if hist}
    minima = {t: min(hist) for t, hist in profiles.items() if hist}
    assert counts[8] == 1752 and counts[9] == 214 and counts[10] == 4
    assert [minima[t] for t in [8, 9, 10]] == [7, 10, 15]
    assert unrestricted[10] == 14  # The induced-degree restriction is necessary.
    assert all(b*(b-1)//2 >= 2*b-3 for b in range(7))
    blue_incidence_cap = (2*15 + 3*16)//2
    red_incidence_demand = 6*16 - blue_incidence_cap
    red_edge_demand = 5*red_incidence_demand - 6*35
    red_edge_capacity = 3*len(edges) - codegree_sum
    assert (red_incidence_demand, red_edge_demand, red_edge_capacity) == (57, 75, 72)
    assert red_edge_demand > red_edge_capacity
    return {
        "agent": "six-books-2", "role": "researcher",
        "core": {"vertices": 16, "edges": 48, "degree": 6,
                 "red_codegrees": dict(sorted(codegrees.items())),
                 "red_codegree_sum": codegree_sum,
                 "deleted_block_indices": DELETED,
                 "blue_clique_block_indices": X, "core_block_indices": Y},
        "row_lemma": {"subsets_in_each_traversal": 65536,
                      "streams_agree_entry_by_entry": True,
                      "eligible_counts_by_size": counts,
                      "eligible_min_edges_by_size": minima,
                      "unrestricted_min_edges_at_size_10": unrestricted[10],
                      "profiles_at_sizes_8_9_10": {t: dict(sorted(profiles[t].items()))
                                                    for t in [8, 9, 10]},
                      "minimum_affine_slack": min(e - 5*t + 35
                                                   for t, hist in profiles.items()
                                                   for e in hist),
                      "row_stream_sha256": sha256(first).hexdigest()},
        "analytic_reduction": {"cross_edges": 96,
                               "cross_assignments_covered": "2^96",
                               "blue_incidence_capacity": blue_incidence_cap,
                               "red_incidence_demand": red_incidence_demand,
                               "red_edge_demand": red_edge_demand,
                               "red_edge_capacity": red_edge_capacity,
                               "cross_assignments_enumerated": False}}


def main():
    output = json.loads(json.dumps(compute()))
    expected = json.loads((HERE / "cross_expected.json").read_text())
    if output != expected:
        raise AssertionError("compact expected output mismatch")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
