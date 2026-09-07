"""Producer-side physical frame and compatible-five-clique enumeration."""
from itertools import combinations


def pins(n=43, cycles=5, joined=True):
    start = 2 if joined else 0
    if cycles < int(joined) or cycles < 0 or n < start + 5 * cycles:
        raise ValueError("invalid frame dimensions")
    fixed = {}
    for b in range(cycles):
        base = start + 5 * b
        red = {tuple(sorted((base + i, base + (i + 1) % 5))) for i in range(5)}
        for pair in combinations(range(base, base + 5), 2):
            fixed[pair] = int(pair in red)
    if joined:
        fixed[0, 1] = 1
        for u in (0, 1):
            for v in range(2, 7):
                fixed[u, v] = 1
    return fixed


def variables(n=43, cycles=5, joined=True):
    fixed = pins(n, cycles, joined)
    return [e for e in combinations(range(n), 2) if e not in fixed]


def cliques(adj, candidates, prefix=()):
    if len(prefix) == 5:
        yield prefix
        return
    while candidates.bit_count() >= 5 - len(prefix):
        bit = candidates & -candidates
        candidates ^= bit
        v = bit.bit_length() - 1
        yield from cliques(adj, candidates & adj[v], prefix + (v,))


def clauses(n=43, cycles=5, joined=True):
    fixed = pins(n, cycles, joined)
    number = {e: k + 1 for k, e in enumerate(variables(n, cycles, joined))}
    for color in (1, 0):
        adj = [0] * n
        for i, j in combinations(range(n), 2):
            if fixed.get((i, j), color) == color:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
        sign = -1 if color else 1
        for vertices in cliques(adj, (1 << n) - 1):
            yield color, [sign * number[e] for e in combinations(vertices, 2)
                          if e in number]
