"""Exact triangle edge cover for split graphs with three neighborhood types.

Input: eight clique-cell counts, then three independent-side multiplicities.
Bit i of cell M says that vertices in that cell belong to neighborhood i.
The enumeration is O(k^7) arithmetic operations, with a substantial constant;
this reference implementation is intended for small examples and auditing.
"""
from pathlib import Path
import argparse
import json


def compositions(total, length, prefix=()):
    if length == 1:
        yield prefix + (total,)
    else:
        for x in range(total + 1):
            yield from compositions(total - x, length - 1, prefix + (x,))


def load_templates():
    records = json.loads(Path(__file__).with_name("templates.json").read_text())
    pairs = [(a, b) for a in range(1, 8) for b in range(a + 1, 8) if not (a & b)]
    return [(tuple(e for j, e in enumerate(pairs) if (h >> j) & 1),
             tuple(j + 1 for j in range(7) if (u >> j) & 1),
             tuple(j + 1 for j in range(7) if (v >> j) & 1), tuple(colors))
            for h, u, v, colors in records]


TEMPLATES = load_templates()
# The 18 nontrivial upper sets of the Boolean lattice on three elements.
UPPER_SETS = tuple(tuple(b for b in range(8) if (bits >> b) & 1)
                   for bits in range(1, 255)
                   if all(not ((bits >> b) & 1) or all((bits >> c) & 1
                          for c in range(8) if (b & c) == b) for b in range(8)))


def core_maximum(a):
    """Max triangle-free edges in K_k minus the three protected cliques."""
    d = a[0]
    best = (-1, -1, -1)
    for index, (edges, left, right, _) in enumerate(TEMPLATES):
        p, r = sum(a[b] for b in left), sum(a[b] for b in right)
        x = min(d, max(0, (d + p - r) // 2))
        value = sum(a[b] * a[c] for b, c in edges)
        value += x * p + (d - x) * r + x * (d - x)
        if value > best[0]:
            best = value, index, x
    return best


def feasible(a, c):
    return sum(a) == sum(c) and all(sum(a[b] for b in u) <= sum(c[b] for b in u)
                                  for u in UPPER_SETS)


def allocation(a, c):
    """Integral downward transport, by augmenting paths on a 18-vertex network."""
    capacity = [[0] * 18 for _ in range(18)]
    k = sum(c)
    for original in range(8):
        capacity[16][original] = c[original]
        for retained in range(8):
            if (original & retained) == retained:
                capacity[original][8 + retained] = k
    for retained in range(8):
        capacity[8 + retained][17] = a[retained]
    residual = [row[:] for row in capacity]
    total = 0
    while total < k:
        parent = [-1] * 18
        parent[16] = 16
        queue = [16]
        for u in queue:
            for v in range(18):
                if parent[v] < 0 and residual[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
            if parent[17] >= 0:
                break
        if parent[17] < 0:
            raise ValueError("infeasible retained-cell vector")
        amount, v = k, 17
        while v != 16:
            u = parent[v]
            amount = min(amount, residual[u][v])
            v = u
        v = 17
        while v != 16:
            u = parent[v]
            residual[u][v] -= amount
            residual[v][u] += amount
            v = u
        total += amount
    return [[capacity[b][8 + a] - residual[b][8 + a] for a in range(8)]
            for b in range(8)]


def solve(c, m):
    if len(c) != 8 or len(m) != 3 or any(type(x) is not int or x < 0 for x in (*c, *m)):
        raise ValueError("eight nonnegative integer counts and three multiplicities required")
    k = sum(c)
    sizes = [sum(c[b] for b in range(8) if (b >> i) & 1) for i in range(3)]
    mu = [sum(m[i] for i in range(3) if (b >> i) & 1) for b in range(8)]
    upper_totals = [sum(c[b] for b in u) for u in UPPER_SETS]
    best_value, best = -1, None
    candidates = 0
    for a in compositions(k, 8):
        if any(sum(a[b] for b in u) > bound for u, bound in zip(UPPER_SETS, upper_totals)):
            continue
        candidates += 1
        value, index, x = core_maximum(a)
        value += sum(a[b] * mu[b] for b in range(8))
        if value > best_value:
            best_value, best = value, (a, index, x)
    a, index, x = best
    edge_count = k * (k - 1) // 2 + sum(m[i] * sizes[i] for i in range(3))
    return {"cells": list(c), "multiplicities": list(m), "clique_order": k,
            "tau": edge_count - best_value, "surviving_edges": best_value,
            "feasible_retained_vectors": candidates, "retained_cells": list(a),
            "template_index": index, "free_left": x, "allocation": allocation(a, c)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("parameters", nargs=11, type=int, metavar="N")
    args = parser.parse_args()
    print(json.dumps(solve(tuple(args.parameters[:8]), tuple(args.parameters[8:])), sort_keys=True))
