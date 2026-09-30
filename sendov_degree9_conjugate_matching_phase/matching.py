"""Finite matching of exact nonnegative singleton and unordered-pair costs.

This module accepts costs, not numerical polynomial roots.  Certification
of the costs and the analytic criterion belongs to the caller.
"""
from functools import lru_cache


def partitions(n):
    """Yield every partition into singletons and pairs exactly once."""
    if not 0 <= n <= 8:
        raise ValueError('This compact implementation supports 0 <= n <= 8')

    def visit(indices):
        if not indices:
            yield ()
            return
        i, *rest = indices
        for tail in visit(tuple(rest)):
            yield ((i,),) + tail
        for offset, j in enumerate(rest):
            others = tuple(rest[:offset] + rest[offset + 1:])
            for tail in visit(others):
                yield ((i, j),) + tail

    yield from visit(tuple(range(n)))


def minimum_cost(singletons, pairs):
    """Return (minimum cost, attaining partition); exact ordered costs work.

    `pairs` must contain exactly the keys (i,j), 0 <= i < j < n.  Equal
    minima are resolved by lexicographic comparison of the partitions.
    """
    n = len(singletons)
    if not 0 <= n <= 8:
        raise ValueError('This compact implementation supports 0 <= n <= 8')
    keys = {(i, j) for i in range(n) for j in range(i + 1, n)}
    if set(pairs) != keys:
        raise ValueError('Pair table is incomplete or has noncanonical keys')
    if any(c < 0 for c in singletons) or any(c < 0 for c in pairs.values()):
        raise ValueError('Costs must be nonnegative')

    @lru_cache(None)
    def solve(mask):
        if mask == 0:
            return 0, ()
        bit = mask & -mask
        i = bit.bit_length() - 1
        rest = mask ^ bit
        cost, tail = solve(rest)
        candidates = [(singletons[i] + cost, ((i,),) + tail)]
        for j in range(i + 1, n):
            if rest & (1 << j):
                cost, tail = solve(rest ^ (1 << j))
                candidates.append((pairs[i, j] + cost, ((i, j),) + tail))
        return min(candidates)

    return solve((1 << n) - 1)


def partition_cost(partition, singletons, pairs):
    return sum(singletons[g[0]] if len(g) == 1 else pairs[g] for g in partition)
