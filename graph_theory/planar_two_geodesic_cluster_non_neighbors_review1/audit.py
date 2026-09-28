#!/usr/bin/env python3
"""Independent finite-core and width-five audit (Python standard library)."""

from __future__ import annotations

from collections import Counter, deque
import hashlib
import itertools
import json
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1] / "planar_two_geodesic_cluster_non_neighbors"


def edge(a: int, b: int) -> tuple[int, int]:
    return min(a, b), max(a, b)


def cyclic_partitions(length: int) -> set[tuple[int, ...]]:
    """Independently enumerate partitions by choosing gaps between slots."""
    patterns = set()
    for gaps in range(1 << length):
        parent = list(range(length))

        def root(v: int) -> int:
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v

        for i in range(length):
            if not (gaps >> i) & 1:
                parent[root(i)] = root((i + 1) % length)
        names = {}
        word = []
        for i in range(length):
            r = root(i)
            if r not in names:
                names[r] = len(names)
            word.append(names[r])
        patterns.add(tuple(word))
    return patterns


def graph(k: int, word: tuple[int, ...], keep: int):
    classes = max(word) + 1
    n = 1 + k + classes
    boundary = sorted({edge(k + 1 + word[i], k + 1 + word[(i + 1) % len(word)])
                       for i in range(len(word)) if word[i] != word[(i + 1) % len(word)]})
    actual = {edge(a, b) for a, b in itertools.combinations(range(1, k + 1), 2)}
    actual.update(edge(0, v) for v in range(k + 1, n))
    for source in range(k):
        actual.update(edge(1 + source, k + 1 + word[i])
                      for i in (2 * source, 2 * source + 1))
    actual.update(e for i, e in enumerate(boundary) if (keep >> i) & 1)
    filled = actual | set(boundary) | {edge(0, x) for x in range(1, k + 1)}
    return n, actual, filled, boundary


def adjacency(n: int, edges: set[tuple[int, int]]) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def distance_from(adj: list[set[int]], start: int) -> list[int]:
    dist = [-1] * len(adj)
    dist[start] = 0
    queue = deque([start])
    while queue:
        v = queue.popleft()
        for w in adj[v]:
            if dist[w] < 0:
                dist[w] = dist[v] + 1
                queue.append(w)
    return dist


def bags_and_tree(n: int, filled: set[tuple[int, int]], order: list[int]):
    assert sorted(order) == list(range(n))
    position = {v: i for i, v in enumerate(order)}
    adj = adjacency(n, filled)
    alive = set(range(n))
    bags = []
    tree = [set() for _ in range(n)]
    for step, v in enumerate(order):
        later = adj[v] & alive
        bags.append(later | {v})
        if later:
            parent = min(position[w] for w in later)
            assert parent > step
            tree[step].add(parent)
            tree[parent].add(step)
        for a, b in itertools.combinations(later, 2):
            adj[a].add(b)
            adj[b].add(a)
        alive.remove(v)
    assert sum(map(len, tree)) == 2 * (n - 1)
    return bags, tree


def check_decomposition(n: int, filled: set[tuple[int, int]],
                        bags: list[set[int]], tree: list[set[int]]) -> None:
    assert all(any({a, b} <= bag for bag in bags) for a, b in filled)
    for v in range(n):
        nodes = {i for i, bag in enumerate(bags) if v in bag}
        assert nodes
        reached = {next(iter(nodes))}
        todo = list(reached)
        while todo:
            for neighbor in tree[todo.pop()] & nodes:
                if neighbor not in reached:
                    reached.add(neighbor)
                    todo.append(neighbor)
        assert reached == nodes


def audit_record(record: dict) -> Counter[int]:
    k = record["k"]
    word = tuple(record["labels"])
    n, actual, filled, boundary = graph(k, word, record["keep"])
    bags, tree = bags_and_tree(n, filled, record["order"])
    check_decomposition(n, filled, bags, tree)
    assert len(record["covers"]) == n
    assert all(len(bag) <= 6 for bag in bags)
    assert all(any({0, a, b} <= bag for bag in bags) for a, b in boundary)
    assert all(any({0, y} <= bag for bag in bags) for y in range(k + 1, n))
    adj = adjacency(n, actual)
    distances = [distance_from(adj, source) for source in range(n)]
    for bag, paths in zip(bags, record["covers"]):
        assert 1 <= len(paths) <= 2
        covered = set()
        for path in paths:
            assert 1 <= len(path) <= 3 and len(path) == len(set(path))
            assert all(type(v) is int and 0 <= v < n for v in path)
            assert all(edge(a, b) in actual for a, b in zip(path, path[1:]))
            assert distances[path[0]][path[-1]] == len(path) - 1
            covered.update(path)
        assert bag <= covered
    return Counter(map(len, bags))


def width_four_prefixes() -> int:
    n = 13
    edges = {edge(0, v) for v in range(1, 10)}
    edges.update(edge(v, v % 9 + 1) for v in range(1, 10))
    edges.update({(10, 11), (10, 12), (11, 12)})
    for x, ring in ((10, (9, 1, 2, 3)), (11, (3, 4, 5, 6)),
                    (12, (6, 7, 8, 9))):
        edges.update(edge(x, v) for v in ring)
    assert len(edges) == 33
    graph6 = b"L|eKKE@oJ_bp?~"
    assert graph6[0] == n + 63
    bits = [((byte - 63) >> shift) & 1
            for byte in graph6[1:] for shift in range(5, -1, -1)]
    assert len(bits) == n * (n - 1) // 2
    decoded = set()
    pos = 0
    for v in range(1, n):
        for u in range(v):
            if bits[pos]:
                decoded.add((u, v))
            pos += 1
    assert decoded == edges
    original = adjacency(n, edges)
    seen = {0}
    pending = [0]
    while pending:
        mask = pending.pop()
        adj = [set(row) for row in original]
        alive = set(range(n))
        for v in range(n):
            if not (mask >> v) & 1:
                continue
            later = adj[v] & alive
            for a, b in itertools.combinations(later, 2):
                adj[a].add(b)
                adj[b].add(a)
            alive.remove(v)
        for v in alive:
            if len(adj[v] & alive) <= 4:
                child = mask | (1 << v)
                if child not in seen:
                    seen.add(child)
                    pending.append(child)
    fan = sum(1 << v for v in (1, 2, 4, 5, 7, 8))
    assert seen == {mask for mask in range(1 << n) if mask & ~fan == 0}
    return len(seen)


def main() -> None:
    raw = (SOURCE / "certificate.jsonl").read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == "c04c7fc4a8a185b00afe06601b263757a48ac6b879592ce7a9aa3c7f6eb1410b"
    records = [json.loads(line) for line in raw.splitlines()]
    expected = set()
    by_k = {}
    for k in (1, 2, 3):
        words = cyclic_partitions(2 * k)
        assert len(words) == {1: 2, 2: 12, 3: 58}[k]
        cases = {(k, word, keep) for word in words
                 for keep in range(1 << len(graph(k, word, 0)[3]))}
        by_k[k] = len(cases)
        expected |= cases
    observed = [(r["k"], tuple(r["labels"]), r["keep"]) for r in records]
    assert len(observed) == len(set(observed)) == len(expected) == 751
    assert set(observed) == expected
    histogram = Counter()
    for record in records:
        histogram.update(audit_record(record))
    assert sum(histogram.values()) == 5972
    assert histogram[6] == 432
    assert width_four_prefixes() == 64
    print(json.dumps({"certificate_sha256": digest, "cases_by_clique_order": by_k,
                      "bag_size_histogram": dict(sorted(histogram.items())),
                      "width_four_prefix_sets": 64}, sort_keys=True))


if __name__ == "__main__":
    main()
