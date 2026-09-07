"""Construct positive maps or square-chain obstructions; standard library only."""
import argparse
from collections import deque
import json
from pathlib import Path


def canonical_graph(n, edges):
    if type(n) is not int or n < 0:
        raise ValueError('Bad order')
    result = set()
    for e in edges:
        if len(e) != 2 or any(type(v) is not int or not 0 <= v < n for v in e):
            raise ValueError('Bad edge')
        a, b = sorted(e)
        if a == b:
            raise ValueError('Loop')
        result.add((a, b))
    return {'vertices': n, 'edges': [list(e) for e in sorted(result)]}


def lift(base, r):
    if type(r) is not int or r < 1:
        raise ValueError('Bad layer count')
    n = base['vertices']
    edges = list(map(tuple, base['edges']))
    for j in range(r - 1):
        for a, b in base['edges']:
            edges.extend(((j*n+a, (j+1)*n+b), (j*n+b, (j+1)*n+a)))
    edges.extend(((r-1)*n+a, r*n) for a in range(n))
    return canonical_graph(r*n+1, edges)


def bipartition_or_cycle(base):
    n = base['vertices']
    adj = [[] for _ in range(n)]
    for a, b in base['edges']:
        adj[a].append(b)
        adj[b].append(a)
    colour = [-1]*n
    parent = [-1]*n
    for root in range(n):
        if colour[root] != -1:
            continue
        colour[root] = 0
        queue = deque([root])
        while queue:
            a = queue.popleft()
            for b in adj[a]:
                if colour[b] == -1:
                    colour[b] = 1-colour[a]
                    parent[b] = a
                    queue.append(b)
                elif colour[a] == colour[b]:
                    def ancestors(v):
                        p = [v]
                        while parent[p[-1]] != -1:
                            p.append(parent[p[-1]])
                        return p
                    p, q = ancestors(a), ancestors(b)
                    while len(p) > 1 and len(q) > 1 and p[-2] == q[-2]:
                        p.pop()
                        q.pop()
                    return None, p + q[-2::-1]
    return colour, None


def square_witness(base_order, r, cycle):
    n, k = base_order, len(cycle)
    def v(i, j):
        return j*n+cycle[i % k]
    apex = r*n
    faces = []
    if r == 1:
        faces = [[1, apex, v(i, 0), v(i+1, 0), v(i+2, 0)] for i in range(k)]
    else:
        faces.extend([1, v(i, 0), v(i+1, 0), v(i+2, 0), v(i+1, 1)]
                     for i in range(k))
        for j in range(1, r-1):
            faces.extend([1, v(i, j-1), v(i+1, j), v(i, j+1), v(i-1, j)]
                         for i in range(k))
        faces.extend([1, apex, v(i, r-1), v(i+1, r-2), v(i+2, r-1)]
                     for i in range(k))
    return {'walk': list(cycle), 'multiplier': 2, 'faces': faces}


def produce(base, r):
    base = canonical_graph(base['vertices'], base['edges'])
    graph = lift(base, r)
    colour, cycle = bipartition_or_cycle(base)
    out = {'base': base, 'layers': r, 'graph': graph}
    if cycle is not None:
        out.update(kind='obstruction', certificate=square_witness(base['vertices'], r, cycle))
    else:
        # The lift of K2 is one cycle. Traverse it to give polygon indices.
        target = lift(canonical_graph(2, [(0, 1)]), r)
        adj = [[] for _ in range(target['vertices'])]
        for a, b in target['edges']:
            adj[a].append(b)
            adj[b].append(a)
        order = [2*r]
        previous, current = 2*r, min(adj[2*r])
        while current != 2*r:
            order.append(current)
            nxt = next(v for v in adj[current] if v != previous)
            previous, current = current, nxt
        index = {v: i for i, v in enumerate(order)}
        mapping = [index[2*j+c] for j in range(r) for c in colour] + [0]
        out.update(kind='polygon_map', certificate={
            'cycle_order': 2*r+1, 'map': mapping, 'base_bipartition': colour})
    return out


def fixture():
    cases = []
    for k, r in [(3, 1), (5, 2), (7, 3), (3, 4)]:
        cases.append(produce(canonical_graph(k, [(i, (i+1) % k) for i in range(k)]), r))
    cases.append(produce(canonical_graph(6, [(a, b) for a in range(3) for b in range(3, 6)]), 3))
    cases.append(produce(canonical_graph(0, []), 2))
    return {'schema': 'mycielski-plane-transfer-v1', 'cases': cases}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--base', type=Path)
    p.add_argument('--layers', type=int, default=2)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    x = ({'schema': 'mycielski-plane-transfer-v1', 'cases': [produce(
        json.loads(args.base.read_text()), args.layers)]} if args.base else fixture())
    with args.out.open('x') as f:
        json.dump(x, f, separators=(',', ':'))
        f.write('\n')


if __name__ == '__main__':
    main()
