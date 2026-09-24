"""Classical Vizing implementation, copied unchanged from the accepted
independent-extension package at commit 2c70b54190876234fe1d22fa2c94bd648875ff01.
No new coloring result is claimed.
"""
from collections import Counter


def require(ok, message):
    if not ok:
        raise ValueError(message)


def edge(a, b):
    return (min(a, b), max(a, b))


def edge_color(n, edges):
    """Classical Vizing fan/Kempe construction using Delta+1 colors.

    Returns every edge with a color and counts of the recoloring branches.
    This is not an optimal edge-coloring algorithm or a new coloring result.
    """
    edges = list(edges)
    require(type(n) is int and n >= 0, 'invalid vertex count')
    require(len(edges) == len(set(edges)), 'repeated coloring edge')
    degree = [0] * n
    for a, b in edges:
        require(type(a) is int and type(b) is int and 0 <= a < b < n,
                'invalid coloring edge')
        degree[a] += 1
        degree[b] += 1
    delta = max(degree, default=0)
    palette = range(delta + 1)
    at = [dict() for _ in range(n)]
    colors = {}
    stats = Counter()

    def missing(v):
        return next(c for c in palette if c not in at[v])

    def add(a, b, c):
        e = edge(a, b)
        require(e not in colors and c not in at[a] and c not in at[b],
                'improper coloring update')
        colors[e] = c
        at[a][c] = b
        at[b][c] = a

    def remove(a, b):
        c = colors.pop(edge(a, b))
        del at[a][c]
        del at[b][c]
        return c

    def rotate(u, fan, c):
        old = [remove(u, v) for v in fan[1:]]
        for v, color in zip(fan[:-1], old):
            add(u, v, color)
        add(u, fan[-1], c)
        stats['fan_rotations'] += 1
        stats['rotated_positions'] += len(fan)

    for u, v in sorted(edges):
        alpha = missing(u)
        fan = [v]
        while True:
            beta = missing(fan[-1])
            if beta not in at[u]:
                rotate(u, fan, beta)
                stats['direct_fan_completion'] += 1
                break
            w = at[u][beta]
            if w not in fan:
                fan.append(w)
                continue
            j = fan.index(w)
            require(j >= 1, 'uncolored fan head has a color')
            pivot = fan[j - 1]
            seen, stack, component_edges = {u}, [u], set()
            while stack:
                a = stack.pop()
                for c in (alpha, beta):
                    b = at[a].get(c)
                    if b is not None:
                        component_edges.add(edge(a, b))
                        if b not in seen:
                            seen.add(b)
                            stack.append(b)
            changed = [(a, b, colors[a, b]) for a, b in sorted(component_edges)]
            for a, b, c in changed:
                remove(a, b)
            for a, b, c in changed:
                add(a, b, beta if c == alpha else alpha)
            stats['kempe_components'] += 1
            stats['kempe_recolored_edges'] += len(changed)
            if pivot in seen:
                rotate(u, fan, beta)
                stats['kempe_full_fan'] += 1
            else:
                rotate(u, fan[:j], beta)
                stats['kempe_prefix_fan'] += 1
            break
    return [(a, b, colors[a, b]) for a, b in sorted(edges)], dict(stats)
