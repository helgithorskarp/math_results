"""Independent unweighted maximum-clique search on adjacent true twins.

Every call must finish. Guards raise; they never report a smaller maximum.
"""
import time
from core import require

def validate(adjacency):
    n = len(adjacency)
    require(all(type(a) is int and 0 <= a < 1 << n and not a >> i & 1
                for i, a in enumerate(adjacency)), 'simple graph domain')
    require(all(bool(adjacency[i] >> j & 1) == bool(adjacency[j] >> i & 1)
                for i in range(n) for j in range(i)), 'asymmetric graph')

def maximum(adjacency, node_cap=3000000, seconds=30):
    validate(adjacency)
    require(0 <= node_cap <= 3000000 and 0 < seconds <= 30, 'guard domain')
    n = len(adjacency)
    order = sorted(range(n), key=lambda v: (-adjacency[v].bit_count(), v))
    inverse = {v: i for i, v in enumerate(order)}
    rows = []
    for v in order:
        row, old = 0, adjacency[v]
        while old:
            bit = old & -old
            row |= 1 << inverse[bit.bit_length() - 1]
            old ^= bit
        rows.append(row)
    best, nodes, started = (), 0, time.monotonic()
    def visit(candidates, chosen):
        nonlocal best, nodes
        nodes += 1
        if nodes > node_cap or time.monotonic() - started > seconds:
            raise RuntimeError('INCOMPLETE maximum-clique guard')
        if len(chosen) > len(best):
            best = chosen
        if not candidates:
            return
        vertices, bounds, left, color = [], [], candidates, 0
        while left:
            color += 1
            independent = left
            while independent:
                bit = independent & -independent
                v = bit.bit_length() - 1
                vertices.append(v)
                bounds.append(color)
                left ^= bit
                independent &= ~bit & ~rows[v]
        for k in range(len(vertices) - 1, -1, -1):
            if len(chosen) + bounds[k] <= len(best):
                return
            v = vertices[k]
            visit(candidates & rows[v], chosen + (v,))
            candidates &= ~(1 << v)
    visit((1 << n) - 1, ())
    result = tuple(sorted(order[v] for v in best))
    require(all(adjacency[a] >> b & 1 for i, a in enumerate(result) for b in result[i + 1:]),
            'returned nonclique')
    return result, nodes

def twins(adjacency, weights):
    validate(adjacency)
    require(len(adjacency) == len(weights) and all(type(w) is int and w in (1, 2) for w in weights),
            'twin weights')
    carriers = tuple(v for v, w in enumerate(weights) for _ in range(w))
    output = tuple(sum(1 << j for j, b in enumerate(carriers) if i != j and
                       (a == b or adjacency[a] >> b & 1)) for i, a in enumerate(carriers))
    validate(output)
    return output, carriers
