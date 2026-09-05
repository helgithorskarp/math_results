#!/usr/bin/env python3
"""Complete four-vertex motif enumerators and two forest checks."""
from itertools import combinations


def adjacency(vertices, edges):
    out = {v: set() for v in vertices}
    for a, b in edges:
        if a in out and b in out:
            out[a].add(b); out[b].add(a)
    return out


def kind(block, adj):
    B = set(block)
    degrees = sorted(len(adj[v] & B) for v in block)
    if degrees == [2, 2, 2, 2]:
        return 'C4'
    if degrees == [2, 2, 3, 3]:
        return 'diamond'
    return None


def opposite_pairs(vertices, edges):
    adj = adjacency(vertices, edges)
    blocks = set()
    for a, b in combinations(sorted(vertices), 2):
        for c, d in combinations(sorted(adj[a] & adj[b]), 2):
            block = tuple(sorted((a, b, c, d)))
            k = kind(block, adj)
            if k is not None:
                blocks.add((k, block))
    return sorted(blocks)


def closed_walks(vertices, edges):
    """Independent census via canonical simple closed walks of length four."""
    adj = adjacency(vertices, edges)
    blocks = set()
    for a in sorted(vertices):
        for b in sorted(adj[a]):
            if b <= a:
                continue
            for c in sorted(adj[b]):
                if c <= a or c == b:
                    continue
                for d in sorted(adj[c]):
                    if d <= a or d in (b, c) or b >= d or a not in adj[d]:
                        continue
                    block = tuple(sorted((a, b, c, d)))
                    # The walk already certifies a spanning four-cycle.
                    # Four induced edges give C4, five give K4 minus an edge.
                    ecount = sum(y in adj[x] for x, y in combinations(block, 2))
                    k = 'C4' if ecount == 4 else 'diamond' if ecount == 5 else None
                    if k is not None:
                        blocks.add((k, block))
    return sorted(blocks)


def components(vertices, edges):
    adj = adjacency(vertices, edges)
    unseen = set(vertices)
    out = []
    while unseen:
        first = min(unseen); unseen.remove(first)
        reached = {first}; todo = [first]
        while todo:
            v = todo.pop()
            nxt = adj[v] & unseen
            unseen.difference_update(nxt); reached.update(nxt); todo.extend(sorted(nxt))
        selected_edges = sorted([a, b] for a, b in edges if a in reached and b in reached)
        out.append(dict(vertices=sorted(reached), edges=selected_edges,
                        tree=len(selected_edges) == len(reached)-1))
    return out


def forest_union(vertices, edges):
    """Separate cycle test: each edge must join distinct union-find sets."""
    parent = {v: v for v in vertices}
    def root(v):
        while parent[v] != v:
            v = parent[v]
        return v
    for a, b in edges:
        if a not in parent or b not in parent:
            continue
        x, y = root(a), root(b)
        if x == y:
            return False
        parent[x] = y
    return True
