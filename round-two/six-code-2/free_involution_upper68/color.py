"""Exact coloring-bound maximum-clique enumeration, copied from own unit-hub work."""
import time
from common import Incomplete, require


def maximum_cliques(adjacency):
    best = []
    maxima = []
    nodes = 0
    started = time.monotonic()

    def colors(pool):
        ordered, bounds = [], []
        color = 0
        while pool:
            color += 1
            available = pool
            while available:
                bit = available & -available
                v = bit.bit_length() - 1
                ordered.append(v)
                bounds.append(color)
                pool ^= bit
                available &= ~bit & ~adjacency[v]
        return ordered, bounds

    def search(pool, chosen):
        nonlocal nodes
        nodes += 1
        if nodes > 3000000 or time.monotonic() - started > 30:
            raise Incomplete('INCOMPLETE clique guard')
        if not pool:
            if len(chosen) > len(best):
                best[:] = chosen
                maxima[:] = [tuple(sorted(chosen))]
            elif len(chosen) == len(best):
                maxima.append(tuple(sorted(chosen)))
            return
        ordered, bounds = colors(pool)
        for j in range(len(ordered) - 1, -1, -1):
            if len(chosen) + bounds[j] < len(best):
                return
            v = ordered[j]
            search(pool & adjacency[v], chosen + [v])
            pool &= ~(1 << v)

    search((1 << len(adjacency)) - 1, [])
    require(len(set(maxima)) == len(maxima), 'duplicate maximum cliques')
    return len(best), tuple(sorted(maxima)), nodes
