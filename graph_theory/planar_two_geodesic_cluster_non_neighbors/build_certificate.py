"""Rebuild the small, exact finite-core certificate; Python standard library.

The verifier is separate and does not call this search. No planar graph
enumerator or solver is used. Unit metric adjacency and fill adjacency are
deliberately separate.
"""
import itertools
import json
from functools import lru_cache
from pathlib import Path


def bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask -= low


def patterns(k):
    size = 2 * k
    yield (0,) * size
    for count in range(2, size + 1):
        for cuts in itertools.combinations(range(size), count):
            labels = [None] * size
            start = (cuts[0] + 1) % size
            label = 0
            for step in range(size):
                i = (start + step) % size
                labels[i] = label
                if i in cuts:
                    label += 1
            rename = {}
            yield tuple(rename.setdefault(x, len(rename)) for x in labels)


def graph(k, labels, keep):
    m = max(labels) + 1
    n = 1 + k + m
    edges = {tuple(sorted((i, j))) for i in range(1, k + 1)
             for j in range(i + 1, k + 1)}
    edges.update((0, k + 1 + b) for b in range(m))
    edges.update((1 + i // 2, k + 1 + b) for i, b in enumerate(labels))
    cycle = sorted({tuple(sorted((k + 1 + labels[i],
                                k + 1 + labels[(i + 1) % len(labels)])))
                    for i in range(len(labels))
                    if labels[i] != labels[(i + 1) % len(labels)]})
    edges.update(e for i, e in enumerate(cycle) if keep & (1 << i))
    filled = edges | set(cycle) | {(0, x) for x in range(1, k + 1)}

    def masks(es):
        a = [0] * n
        for u, v in es:
            a[u] |= 1 << v
            a[v] |= 1 << u
        return a

    return masks(edges), masks(filled), cycle


def search(adj, fill):
    n = len(adj)
    full = (1 << n) - 1
    paths = {1 << u: (u,) for u in range(n)}
    for u in range(n):
        for v in bits(adj[u]):
            paths[(1 << u) | (1 << v)] = (u, v)
            for w in bits(adj[v] & ~adj[u] & ~(1 << u)):
                paths[(1 << u) | (1 << v) | (1 << w)] = (u, v, w)
    allowed = [False] * (1 << n)
    for p in paths:
        for q in paths:
            allowed[p | q] = True
    for u in range(n):
        for mask in range(1 << n):
            if mask & (1 << u) and allowed[mask]:
                allowed[mask ^ (1 << u)] = True

    def bag(mask, v):
        reached = todo = 1 << v
        boundary = 0
        while todo:
            bit = todo & -todo
            todo -= bit
            w = bit.bit_length() - 1
            boundary |= fill[w]
            new = fill[w] & mask & ~reached
            reached |= new
            todo |= new
        return (boundary & ~mask) | (1 << v)

    @lru_cache(None)
    def dfs(mask):
        if mask == full:
            return ()
        candidates = sorted((bag(mask, v).bit_count(), v, bag(mask, v))
                            for v in bits(full ^ mask))
        for _, v, b in candidates:
            if allowed[b]:
                suffix = dfs(mask | (1 << v))
                if suffix is not None:
                    return ((v, b),) + suffix
        return None

    order_bags = dfs(0)
    assert order_bags is not None, 'finite-core lemma failed'
    order, covers = [], []
    for v, b in order_bags:
        pair = next((p, q) for p in paths for q in paths if b & ~(p | q) == 0)
        order.append(v)
        covers.append([list(paths[p]) for p in pair])
    return order, covers


def main():
    lines = []
    counts = {}
    for k in range(1, 4):
        cases = []
        for labels in sorted(set(patterns(k))):
            _, _, cycle = graph(k, labels, 0)
            for keep in range(1 << len(cycle)):
                adj, fill, _ = graph(k, labels, keep)
                order, covers = search(adj, fill)
                cases.append({'k': k, 'labels': list(labels), 'keep': keep,
                              'order': order, 'covers': covers})
        counts[k] = len(cases)
        lines.extend(json.dumps(c, separators=(',', ':')) for c in cases)
    path = Path(__file__).with_name('certificate.jsonl')
    path.write_text('\n'.join(lines) + '\n')
    print(json.dumps({'cases_by_clique_order': counts,
                      'total_cases': len(lines), 'certificate_bytes': path.stat().st_size},
                     indent=2))


if __name__ == '__main__':
    main()
