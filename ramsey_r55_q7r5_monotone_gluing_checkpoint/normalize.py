"""One-pass red-deletion normalization, on physical edge colors only.

The caller must choose mutable edges that preserve its fixed frame and other
downward-closed conditions. This routine alone does not implement a carrier.
"""

if not __debug__:
    raise RuntimeError('Run this research program without -O or -OO; its exact checks require assertions.')
from itertools import combinations


def witness(adjacency, u, v):
    """A blue triangle in the common blue neighborhood of a red pair."""
    n = len(adjacency)
    common = [w for w in range(n) if w not in (u, v) and not adjacency[u][w] and not adjacency[v][w]]
    for a, b, c in combinations(common, 3):
        if not adjacency[a][b] and not adjacency[a][c] and not adjacency[b][c]:
            return (a, b, c)
    return None


def normalize(adjacency, selected_edges):
    a = [list(row) for row in adjacency]
    n = len(a)
    assert all(len(row) == n for row in a)
    assert all(a[i][i] == 0 for i in range(n))
    assert all(a[i][j] in (0, 1) and a[i][j] == a[j][i] for i, j in combinations(range(n), 2))
    selected_edges = tuple(selected_edges)
    assert len(set(selected_edges)) == len(selected_edges)
    assert all(0 <= u < v < n for u, v in selected_edges)
    deleted, kept = [], []
    for u, v in selected_edges:
        if not a[u][v]:
            continue
        found = witness(a, u, v)
        if found is None:
            a[u][v] = a[v][u] = 0
            deleted.append((u, v))
        else:
            kept.append({'edge': (u, v), 'witness': found})
    return a, {'deleted': deleted, 'kept': kept}
