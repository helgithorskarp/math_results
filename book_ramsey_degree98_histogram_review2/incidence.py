"""Reviewer2 incidence refinement; adapted from own independently published audit.

Branch on every vertex of an intrinsic nonsingleton point cell. No external
canonization library or author automorphism enumerator is used.
"""
from collections import Counter
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


def image(words, mapping):
    return tuple(sorted(sum(1 << mapping[z] for z in range(len(mapping))
                            if w >> z & 1) for w in words))


def inverse(mapping):
    result = [0] * len(mapping)
    for z, target in enumerate(mapping):
        result[target] = z
    return tuple(result)


def canonical(words, n, point_cells, cap=200000, seconds=10):
    need(type(cap) is int and 0 <= cap <= 200000 and 0 < seconds <= 10, 'invalid incidence guard')
    words = tuple(sorted(words))
    need(len(words) == len(set(words)) and all(type(w) is int and 0 <= w < 1 << n for w in words), 'invalid incidence words')
    point_cells = tuple(tuple(c) for c in point_cells)
    need(sorted(z for c in point_cells for z in c) == list(range(n)), 'invalid point colors')
    neighbors = [set() for _ in range(n + len(words))]
    for i, w in enumerate(words, n):
        for z in range(n):
            if w >> z & 1:
                neighbors[z].add(i)
                neighbors[i].add(z)
    initial = point_cells + (tuple(range(n, n + len(words))),)
    best, leaves, states, leaf_maps = None, 0, 0, []
    started = time.monotonic()

    def refine(cells):
        while True:
            color = {v: i for i, c in enumerate(cells) for v in c}
            result = []
            for c in cells:
                buckets = {}
                for v in c:
                    count = Counter(color[u] for u in neighbors[v])
                    key = tuple(count[i] for i in range(len(cells)))
                    buckets.setdefault(key, []).append(v)
                result.extend(tuple(buckets[k]) for k in sorted(buckets))
            result = tuple(result)
            if len(result) == len(cells):
                return result
            cells = result

    def visit(cells):
        nonlocal best, states, leaves, leaf_maps
        states += 1
        need(states <= cap and time.monotonic() - started <= seconds, 'INCOMPLETE incidence guard')
        cells = refine(cells)
        choices = [(len(c), i, c) for i, c in enumerate(cells) if len(c) > 1 and c[0] < n]
        if not choices:
            order = tuple(c[0] for c in cells if c[0] < n)
            need(sorted(order) == list(range(n)), 'incomplete incidence labeling')
            key = image(words, inverse(order))
            leaves += 1
            if best is None or key < best:
                best, leaf_maps = key, [order]
            elif key == best:
                leaf_maps.append(order)
            return
        _, index, c = min(choices)
        for v in c:
            visit(cells[:index] + ((v,), tuple(u for u in c if u != v)) + cells[index+1:])

    visit(initial)
    need(best is not None and leaf_maps and len(leaf_maps) == len(set(leaf_maps)), 'missing/duplicate canonical leaves')
    base = inverse(leaf_maps[0])
    automorphisms = tuple(sorted(tuple(p[base[z]] for z in range(n)) for p in leaf_maps))
    group = set(automorphisms)
    need(len(group) == len(leaf_maps) and tuple(range(n)) in group, 'bad automorphism collection')
    colors = {z: i for i, c in enumerate(point_cells) for z in c}
    for p in automorphisms:
        need(sorted(p) == list(range(n)) and all(colors[p[z]] == colors[z] for z in range(n)) and image(words, p) == words, 'false automorphism')
    for p in group:
        for q in group:
            need(tuple(p[q[z]] for z in range(n)) in group, 'automorphism group not closed')
    return dict(canonical=best, automorphisms=automorphisms, states=states, leaves=leaves, order=len(group), to_canonical=inverse(leaf_maps[0]))
