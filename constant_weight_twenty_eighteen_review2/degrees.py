"""Own residual-edge recursion reused with attribution from source d408e72d803d58e8d07b3f42e6b138fd68f0afbe.
"""
from collections import Counter
import time
from exact import insist

def edge_degree_graphs(vertices, degrees, allowed, cap=200000, seconds=10):
    """Binary decisions on edges; exhaust a given degree coefficient exactly."""
    insist(set(vertices) == set(degrees) and all(type(d) is int and d >= 0 for d in degrees.values()), 'degree domain')
    allowed = tuple(sorted(allowed, key=lambda p: (-sum(degrees[x] for x in p), -max(degrees[x] for x in p), p)))
    insist(len(allowed) == len(set(allowed)) and all(len(p) == 2 and p[0] < p[1] and set(p) <= set(vertices) for p in allowed), 'edge domain')
    indices = {x: i for i, x in enumerate(vertices)}
    edges = tuple((indices[x], indices[y]) for x, y in allowed)
    answers, states = [], 0
    started = time.monotonic()

    def visit(k, remaining, selected):
        nonlocal states
        states += 1
        if states > cap or time.monotonic() - started > seconds:
            raise RuntimeError('INCOMPLETE: degree graph guard')
        if not any(remaining):
            answers.append(tuple(sorted(allowed[i] for i in selected)))
            return
        if k == len(edges) or sum(remaining) % 2:
            return
        available = [0] * len(vertices)
        for i, j in edges[k:]:
            if remaining[i] and remaining[j]:
                available[i] += 1
                available[j] += 1
        if any(d > available[i] for i, d in enumerate(remaining)):
            return
        i, j = edges[k]
        if remaining[i] and remaining[j]:
            child = list(remaining)
            child[i] -= 1
            child[j] -= 1
            visit(k + 1, tuple(child), selected + (k,))
        visit(k + 1, remaining, selected)

    visit(0, tuple(degrees[x] for x in vertices), ())
    insist(len(answers) == len(set(answers)), 'duplicate degree graph')
    for edges_out in answers:
        got = Counter(x for edge in edges_out for x in edge)
        insist(all(got[x] == degrees[x] for x in vertices), 'false degree graph')
    return sorted(answers), states
