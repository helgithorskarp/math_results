"""Separate extension algorithm: arc consistency and direct cycle enumeration.

Imports no producing oracle. It handles retained subgraphs of the certified
fixed graph, or the supplied forest/unicyclic control graphs. Cycle labels
are interpreted in cyclic order, not just as an unordered vertex set.
"""
from collections import deque
from itertools import product


def check(ok, message):
    if not ok:
        raise ValueError(message)


def solve(vertices, edges, masks, cycle=()):
    check(set(masks) <= set(vertices), 'selected domain')
    check(all(type(m) is int and 0 <= m <= 15 for m in masks.values()), 'list domain')
    domains = {v: {c for c in range(4) if m & (1 << c)} for v, m in masks.items()}
    arcs = [(u, v) for a, b in edges if a in domains and b in domains for u, v in ((a, b), (b, a))]
    while True:
        changed = False
        for u, v in arcs:
            keep = {c for c in domains[u] if domains[v] - {c}}
            if keep != domains[u]:
                domains[u] = keep
                changed = True
        if any(not d for d in domains.values()):
            return None
        if not changed:
            break
    answer = {}
    if cycle and all(v in domains for v in cycle):
        for values in product(*(sorted(domains[v]) for v in cycle)):
            if all(values[i] != values[(i+1) % len(values)] for i in range(len(values))):
                answer.update(zip(cycle, values))
                break
        else:
            return None
    neighbors = {v: [] for v in domains}
    for u, v in arcs:
        neighbors[u].append(v)
    queue = deque(sorted(answer))
    # Outside a surviving cycle each component is a tree. Arc consistency
    # guarantees an available child colour for every chosen parent colour.
    # Drain the precoloured cycle first. Otherwise the first smaller-labelled
    # disconnected root could be skipped while that initial queue is nonempty.
    for root in [None] + sorted(domains):
        if root is not None and root not in answer:
            answer[root] = min(domains[root])
            queue.append(root)
        while queue:
            v = queue.popleft()
            for w in neighbors[v]:
                if w not in answer:
                    legal = domains[w] - {answer[v]}
                    check(bool(legal), 'arc support during reconstruction')
                    answer[w] = min(legal)
                    queue.append(w)
    check(set(answer) == set(domains), 'complete independent reconstruction')
    check(all(answer[u] != answer[v] for u, v in arcs), 'independent edge check')
    return answer


def brute(vertices, edges, masks):
    """Definition-level finite controls; no propagation or graph structure."""
    vs = [v for v in vertices if v in masks]
    for values in product(*([c for c in range(4) if masks[v] & (1 << c)] for v in vs)):
        answer = dict(zip(vs, values))
        if all(u not in answer or v not in answer or answer[u] != answer[v] for u, v in edges):
            return answer
    return None
