#!/usr/bin/env python3
"""Exact example checks and a deletion-first enumeration; Python stdlib only."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def graph_from_sets(objects):
    """Adjacency means disjointness, directly from the construction definition."""
    if len(set(objects)) != len(objects) or any(not x for x in objects):
        raise ValueError("objects must be nonempty and distinct")
    return [{j for j, y in enumerate(objects) if i != j and not x & y}
            for i, x in enumerate(objects)]


def complement(graph):
    universe = set(range(len(graph)))
    return [universe - {i} - ns for i, ns in enumerate(graph)]


def codegrees(graph):
    return Counter(len(graph[i] & graph[j]) for i in range(len(graph))
                   for j in graph[i] if i < j)


def summary(graph):
    red, blue = codegrees(graph), codegrees(complement(graph))
    return {"vertices": len(graph), "edges": sum(map(len, graph)) // 2,
            "degrees": dict(sorted(Counter(map(len, graph)).items())),
            "red_codegrees": dict(sorted(red.items())),
            "blue_codegrees": dict(sorted(blue.items())),
            "avoids_B4_B7": max(red, default=0) <= 3
                            and max(blue, default=0) <= 6}


def simple_edges(edges):
    objects = [frozenset(e) for e in edges]
    if any(len(e) != 2 for e in objects) or len(set(objects)) != len(objects):
        raise ValueError("simple root graph required")
    return objects


def restricted_growth_strings(n):
    """One representative for each partition of n labeled positions."""
    def rec(prefix):
        if len(prefix) == n:
            yield tuple(prefix)
        else:
            for x in range(max(prefix) + 2):
                yield from rec(prefix + [x])
    if n <= 0:
        raise ValueError("positive n required")
    yield from rec([0])


def baseline():
    lines = (HERE / "baseline21.edges").read_text().splitlines()
    n = int(lines[0])
    graph = [set() for _ in range(n)]
    for line in lines[1:]:
        i, j = map(int, line.split())
        if not 0 <= j < i < n or j in graph[i]:
            raise ValueError("malformed edge fixture")
        graph[i].add(j)
        graph[j].add(i)
    result = summary(graph)
    assert result == {"vertices": 21, "edges": 93,
                      "degrees": {8: 4, 9: 16, 10: 1},
                      "red_codegrees": {1: 3, 2: 33, 3: 57},
                      "blue_codegrees": {4: 5, 5: 44, 6: 68},
                      "avoids_B4_B7": True}
    blue = complement(graph)
    center, leaves = 0, [3, 11, 12]
    assert all(x in blue[center] for x in leaves)
    assert all(y not in blue[x] for x, y in combinations(leaves, 2))
    result["blue_induced_claw"] = [center, *leaves]
    return result


def equality_checks():
    k7 = graph_from_sets(simple_edges(combinations(range(7), 2)))
    assert summary(k7) == {"vertices": 21, "edges": 105,
                           "degrees": {10: 21}, "red_codegrees": {3: 105},
                           "blue_codegrees": {5: 105}, "avoids_B4_B7": True}
    valid, total = [], 0
    for pattern in restricted_growth_strings(6):
        root = list(combinations(range(6), 2))
        root += [(i, 6 + pattern[i]) for i in range(6)]
        if summary(graph_from_sets(simple_edges(root)))["avoids_B4_B7"]:
            valid.append(list(pattern))
        total += 1
    assert total == 203 and valid == [[0] * 6]
    # Check the root-degree implication of blue B7-freeness at its boundary.
    assert summary(graph_from_sets(simple_edges((0, i) for i in range(1, 9))))[
        "avoids_B4_B7"]
    assert not summary(graph_from_sets(simple_edges((0, i) for i in range(1, 10))))[
        "avoids_B4_B7"]
    for malformed in [[(0, 1), (1, 0)], [(0, 0)]]:
        try:
            simple_edges(malformed)
        except ValueError:
            pass
        else:
            raise AssertionError("malformed simple graph accepted")
    return {"KG_7_2": summary(k7), "attachment_partitions_checked": total,
            "valid_attachment_patterns": valid}


def steiner_blocks():
    objects = [frozenset((x + y) % 13 for y in base)
               for base in [(0, 1, 4), (0, 2, 7)] for x in range(13)]
    assert len(set(objects)) == 26
    assert all(sum(set(pair) <= block for block in objects) == 1
               for pair in combinations(range(13), 2))
    return objects


def deletion_counts(return_vector=False):
    blocks = steiner_blocks()
    red = graph_from_sets(blocks)
    blue = complement(red)
    assert summary(red) == {"vertices": 26, "edges": 130,
                            "degrees": {10: 26}, "red_codegrees": {3: 130},
                            "blue_codegrees": {8: 195}, "avoids_B4_B7": False}
    masks = [sum(1 << j for j in ns) for ns in blue]
    edges = [(i, j, masks[i] & masks[j]) for i, ns in enumerate(blue)
             for j in sorted(ns) if i < j]
    counts, hist = [], Counter()
    best, best_pattern = 196, None
    for deleted in combinations(range(26), 4):
        dm = sum(1 << x for x in deleted)
        keep = ((1 << 26) - 1) ^ dm
        values = [(common & keep).bit_count() for i, j, common in edges
                  if not ((dm >> i) & 1 or (dm >> j) & 1)]
        bad = sum(x >= 7 for x in values)
        assert bad >= 15 and sum(x - 6 for x in values) >= 30
        counts.append(bad)
        hist[bad] += 1
        if bad < best:
            best, best_pattern = bad, deleted
    assert len(counts) == 14950 and best == 39 and hist[39] == 13
    assert best_pattern == (0, 18, 21, 22)
    # Check the attaining example afresh using set intersection, no masks.
    remaining = [b for i, b in enumerate(blocks) if i not in best_pattern]
    check = summary(graph_from_sets(remaining))
    assert check["blue_codegrees"] == {5: 12, 6: 84, 7: 36, 8: 3}
    digest = sha256(bytes(counts)).hexdigest()  # counts lie in [0,195]
    result = {"deletion_sets_checked": len(counts), "minimum_bad_blue_spines": best,
            "minimizers": hist[best], "first_minimizer": list(best_pattern),
            "minimizer": check, "bad_spine_histogram": dict(sorted(hist.items())),
            "ordered_counts_sha256": digest}
    return (result, counts) if return_vector else result


def main():
    output = {"agent": "six-books-2", "role": "researcher",
              "baseline": baseline(), "simple_edge_equality": equality_checks(),
              "cyclic_STS13": deletion_counts()}
    expected = json.loads((HERE / "expected.json").read_text())
    # JSON normalization makes integer histogram keys explicit strings.
    output = json.loads(json.dumps(output))
    if output != expected:
        raise AssertionError("compact expected output mismatch")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
