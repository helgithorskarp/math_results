#!/usr/bin/env python3
"""Independent checks of the wider-cylinder finite certificates and quotient."""
from collections import deque
from heapq import heappush, heappop
from itertools import combinations
import json
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent / 'planar_annular_stretch_family/wider/certificate.json'


def model(m, h):
    north, south = ('N',), ('S',)
    vertices = [north, south] + [(i, j) for j in range(h) for i in range(m)]
    adj = {v: set() for v in vertices}
    vertical = set()

    def add(a, b, is_vertical=False):
        assert a != b
        adj[a].add(b)
        adj[b].add(a)
        if is_vertical:
            vertical.add(frozenset((a, b)))

    for j in range(h):
        for i in range(m):
            x = (i, j)
            add(x, ((i + 1) % m, j))
            if j == 0:
                add(north, x)
            if j == h - 1:
                add(south, x)
            if j < h - 1:
                add(x, (i, j + 1), True)
                if (i + j) % 2 == 0:
                    add(x, ((i + 1) % m, j + 1))
                else:
                    add(((i + 1) % m, j), (i, j + 1))
    return adj, vertical


def decode(v, m, h):
    if v == 0:
        return ('N',)
    if v == 1:
        return ('S',)
    i, j = divmod(v - 2, h)
    assert 0 <= i < m
    return i, j


def distance(adj, a, b):
    todo = deque([(a, 0)])
    seen = {a}
    while todo:
        v, d = todo.popleft()
        if v == b:
            return d
        for u in adj[v]:
            if u not in seen:
                seen.add(u)
                todo.append((u, d + 1))
    raise AssertionError('disconnected')


def components(adj, removed):
    unseen = set(adj) - removed
    out = []
    while unseen:
        root = unseen.pop()
        stack = [root]
        part = {root}
        while stack:
            v = stack.pop()
            for u in adj[v] & unseen:
                unseen.remove(u)
                part.add(u)
                stack.append(u)
        out.append(frozenset(part))
    return out


def possible_heavies(options, selected):
    for index in selected:
        if not options[index]:
            return False
    order = sorted(selected, key=lambda i: len(options[i]))

    def search(depth, chosen):
        if depth == len(order):
            return True
        for part in options[order[depth]]:
            if all(part & old for old in chosen) and search(depth + 1, chosen + [part]):
                return True
        return False

    return search(0, [])


def kernel(item):
    m, h = item['m'], item['height']
    adj, vertical = model(m, h)
    anchor = {('N',)} | {(i, j) for i in range(m) for j in range(item['anchor_rows'])} if item['anchor_rows'] else set()
    options = []
    path_count = 0
    for cut in item['cuts']:
        assert 1 <= len(cut) <= 2
        removed = set()
        for numeric_path in cut:
            path = [decode(v, m, h) for v in numeric_path]
            assert len(set(path)) == len(path)
            assert item['proxy'] is None or ('S',) not in path
            for a, b in zip(path, path[1:]):
                assert b in adj[a]
                assert frozenset((a, b)) not in vertical
            assert distance(adj, path[0], path[-1]) == len(path) - 1
            removed.update(path)
            path_count += 1
        parts = components(adj, removed)
        options.append([p for p in parts if not anchor or p & anchor])
    assert not possible_heavies(options, range(len(options)))
    minimum = None
    examples = []
    for size in range(1, len(options) + 1):
        for chosen in combinations(range(len(options)), size):
            if not possible_heavies(options, chosen):
                examples.append(chosen)
        if examples:
            minimum = size
            break
    return {'m': m, 'h': h, 'vertices': len(adj), 'cuts': len(options),
            'paths': path_count, 'minimum_cuts_by_intersection': minimum,
            'minimum_subset_count': len(examples),
            'first_minimum_subset': examples[0]}


def quotient(m, h, k, bottom, vertex):
    if vertex == ('N',):
        return ('S',) if bottom else ('N',)
    if vertex == ('S',):
        return ('N',) if bottom else ('S',)
    i, j = vertex
    if bottom:
        i = (i + (h % 2 == 0)) % m
        j = h - 1 - j
    return (i, j) if j < k else ('S',)


def quotient_checks():
    checked = 0
    for m, k in ((10, 3), (12, 4)):
        kernel_graph, _ = model(m, k)
        for h in range(k, 34):
            graph, _ = model(m, h)
            for bottom in (False, True):
                for a, neighbors in graph.items():
                    for b in neighbors:
                        x, y = quotient(m, h, k, bottom, a), quotient(m, h, k, bottom, b)
                        assert x == y or y in kernel_graph[x]
                        checked += 1
    return checked


def balanced(adj, mass, paths):
    removed = set().union(*(set(path) for path in paths))
    total = sum(mass.values())
    return all(2 * sum(mass[v] for v in part) <= total
               for part in components(adj, removed))


def lifted_paths(m, h, mass, kernels):
    total = sum(mass.values())
    if total == 0:
        return [], 'zero'
    for cap in (('N',), ('S',)):
        if 2 * mass[cap] >= total:
            return [[cap]], 'cap'
    if m == 10 and h == 2:
        item = kernels[(m, h)]
        adj, _ = model(m, h)
        for cut in item['cuts']:
            paths = [[decode(v, m, h) for v in p] for p in cut]
            if balanced(adj, mass, paths):
                return paths, 'short'
        raise AssertionError('short kernel has no cut')
    q, k = (1, 3) if m == 10 else (2, 4)
    cumulative = mass[('N',)]
    for j in range(h):
        cumulative += sum(mass[i, j] for i in range(m))
        if 2 * cumulative >= total:
            break
    if q <= j < h - q:
        return [[(i, j) for i in range(m // 2)],
                [(i, j) for i in range(m // 2, m)]], 'row'
    bottom = j >= h - q
    item = kernels[(m, k)]
    kernel_adj, _ = model(m, k)
    aggregate = {v: 0 for v in kernel_adj}
    for v, value in mass.items():
        aggregate[quotient(m, h, k, bottom, v)] += value
    anchor = {('N',)} | {(i, level) for level in range(q) for i in range(m)}
    assert 2 * sum(aggregate[v] for v in anchor) >= total
    for cut in item['cuts']:
        kernel_paths = [[decode(v, m, k) for v in p] for p in cut]
        if balanced(kernel_adj, aggregate, kernel_paths):
            def lift(v):
                if v == ('N',):
                    return ('S',) if bottom else ('N',)
                assert v != ('S',)
                i, level = v
                return ((i - (h % 2 == 0)) % m, h - 1 - level) if bottom else v
            return [[lift(v) for v in p] for p in kernel_paths], 'bottom' if bottom else 'top'
    raise AssertionError('boundary kernel has no cut')


def weighted_distance(adj, vertical, a, b, mode):
    def code(v):
        return -2 if v == ('N',) else -1 if v == ('S',) else 100 * v[1] + v[0]

    todo = [(0, code(a), a)]
    dist = {a: 0}
    while todo:
        d, _, v = heappop(todo)
        if d != dist[v]:
            continue
        if v == b:
            return d
        for u in adj[v]:
            e = frozenset((u, v))
            if e in vertical and mode == 3:
                continue
            if e in vertical and mode == 2 and (sum(map(code, e)) % 3 == 0):
                continue
            x, y = sorted(map(code, e))
            length = (1 + (abs(37 * x + 53 * y) % 101)) if e in vertical and mode else 1
            nd = d + length
            if nd < dist.get(u, nd + 1):
                dist[u] = nd
                heappush(todo, (nd, code(u), u))
    raise AssertionError('disconnected')


def witness_checks(kernels):
    counts = {'witnesses': 0, 'cases': {}}
    def code(v):
        return -2 if v == ('N',) else -1 if v == ('S',) else 100 * v[1] + v[0]
    for m, heights in ((10, (2, 3, 4, 5, 8, 15)), (12, (4, 5, 6, 8, 15))):
        for h in heights:
            adj, vertical = model(m, h)
            fixtures = [{v: 0 for v in adj}, {v: 1 for v in adj}]
            for index in range(6):
                fixtures.append({v: (17 * (index + 1) + 29 * abs(code(v)) + 3) % 97 for v in adj})
            for cap in (('N',), ('S',)):
                fixtures.append({v: 10**6 if v == cap else 1 for v in adj})
            for row in range(h):
                fixtures.append({v: (1 + v[0]) if len(v) == 2 and v[1] == row else 0 for v in adj})
            for mass in fixtures:
                paths, case = lifted_paths(m, h, mass, kernels)
                for mode in range(4):
                    allowed = {v: set(neighbors) for v, neighbors in adj.items()}
                    if mode >= 2:
                        for edge in vertical:
                            if mode == 3 or sum(map(code, edge)) % 3 == 0:
                                a, b = tuple(edge)
                                allowed[a].remove(b)
                                allowed[b].remove(a)
                    assert balanced(allowed, mass, paths)
                    for path in paths:
                        assert len(path) == len(set(path))
                        for a, b in zip(path, path[1:]):
                            assert b in allowed[a] and frozenset((a, b)) not in vertical
                        assert weighted_distance(adj, vertical, path[0], path[-1], mode) == len(path) - 1
                    counts['witnesses'] += 1
                    counts['cases'][case] = counts['cases'].get(case, 0) + 1
    return counts


def main():
    kernels = json.loads(SOURCE.read_text())['kernels']
    kernel_map = {(x['m'], x['height']): x for x in kernels}
    result = {'kernels': [kernel(x) for x in kernels],
              'directed_quotient_edge_checks': quotient_checks(),
              'weighted_witness_checks': witness_checks(kernel_map)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
