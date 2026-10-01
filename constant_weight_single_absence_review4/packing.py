"""Pivoted maximal-clique search, exact sets and an independent color bound."""
import time
from covers import need


def find_clique(adj, target, state_limit=200000, seconds=10):
    need(target >= 0 and all(i not in adj[i] for i in range(len(adj)))
         and all(i in adj[j] for i, ns in enumerate(adj) for j in ns), 'simple undirected clique input')
    start = time.monotonic()
    states = color_prunes = 0

    def upper_bound(P, wanted):
        # Complete proper coloring is an upper bound. An unfinished coloring
        # reaching wanted supplies no prune and returns wanted.
        groups = []
        for v in sorted(P, key=lambda v: (-len(adj[v] & P), v)):
            for group in groups:
                if group.isdisjoint(adj[v]):
                    group.add(v)
                    break
            else:
                groups.append({v})
                if len(groups) >= wanted:
                    return wanted
        return len(groups)

    def visit(R, P, X):
        nonlocal states, color_prunes
        states += 1
        if states > state_limit or time.monotonic()-start > seconds:
            raise RuntimeError('INCOMPLETE: pivoted clique guard')
        if len(R) >= target:
            return R
        wanted = target-len(R)
        if len(P) < wanted:
            return None
        if upper_bound(P, wanted) < wanted:
            color_prunes += 1
            return None
        pivot = min(P | X, key=lambda v: (-len(P & adj[v]), v))
        # Bron--Kerbosch pivot: every still-unreported maximal clique contains
        # a vertex outside the pivot's neighborhood, including the pivot itself.
        for v in sorted(P-adj[pivot]):
            answer = visit(R+(v,), P & adj[v], X & adj[v])
            if answer is not None:
                return answer
            P.remove(v)
            X.add(v)
        return None

    answer = visit((), set(range(len(adj))), set())
    if answer is not None:
        need(len(answer) == target and all(v in adj[u] for u in answer for v in answer if v != u), 'literal clique witness')
    return answer, {'states': states, 'color_prunes': color_prunes}
