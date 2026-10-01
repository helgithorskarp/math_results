"""Independent whole-point-star partition search using ordinary pair sets.

Each branch installs every remaining occurrence of one point, in sorted
column order. This differs from the native single-column quota search.
"""
from itertools import combinations
import time
from incidence import need


def solve(columns, quotas, mandatory, high, budget, cap=200000, seconds=10):
    need(type(cap) is int and 0 <= cap <= 200000 and 0 < seconds <= 10, 'invalid literal guard')
    cols = tuple(tuple(sorted(c)) for c in columns)
    need(len(cols) == len(set(cols)) and all(len(c) == 4 and len(set(c)) == 4 and all(type(z) is int and 0 <= z < 15 for z in c) for c in cols), 'invalid literal columns')
    q = tuple(quotas)
    need(len(q) == 15 and all(type(t) is int and 0 <= t <= 5 for t in q) and sum(q) % 4 == 0, 'invalid literal quotas')
    high = frozenset(high)
    need(all(type(z) is int and 0 <= z < 15 for z in high) and type(budget) is int and 0 <= budget <= 10, 'invalid high/budget')
    mandatory = frozenset(tuple(sorted(p)) for p in mandatory)
    need(all(len(p) == 2 and p[0] < p[1] and 0 <= p[0] < p[1] < 15 for p in mandatory), 'invalid mandatory pairs')
    pairs = tuple(frozenset(combinations(c, 2)) for c in cols)
    costs = tuple(len(frozenset(c) & high) * (len(frozenset(c) & high)-1)//2 for c in cols)
    states = 0
    started = time.monotonic()

    def guard():
        nonlocal states
        states += 1
        need(states <= cap and time.monotonic()-started <= seconds, 'INCOMPLETE literal point-partition guard')

    def visit(q, mandatory, budget, available, chosen):
        guard()
        if sum(q) == 0:
            return chosen if not mandatory and budget == 0 else None
        active = tuple(i for i in available if costs[i] <= budget and all(q[z] for z in cols[i]))
        at = tuple(tuple(i for i in active if z in cols[i]) for z in range(15))
        if len(active) < sum(q)//4 or any(len(at[z]) < q[z] for z in range(15)):
            return None
        if any(not any(p in pairs[i] for i in active) for p in mandatory):
            return None
        z = min((z for z in range(15) if q[z]), key=lambda z: (len(at[z]), q[z], -z))
        incident = frozenset(p for p in mandatory if z in p)

        def partition(start, left, q, required, budget, available, selected):
            guard()
            if left == 0:
                if q[z] != 0 or any(z in p for p in required):
                    return None
                return visit(q, required, budget, available, chosen+selected)
            choices = tuple(i for i in at[z] if i >= start and i in available and costs[i] <= budget and all(q[u] for u in cols[i]))
            if len(choices) < left:
                return None
            if any(not any(p in pairs[i] for i in choices) for p in required & incident):
                return None
            for i in choices:
                nq = list(q)
                for u in cols[i]:
                    nq[u] -= 1
                nxt = tuple(j for j in available if not pairs[i] & pairs[j])
                result = partition(i+1, left-1, tuple(nq), required-pairs[i], budget-costs[i], nxt, selected+(i,))
                if result is not None:
                    return result
            return None

        return partition(0, q[z], q, mandatory, budget, active, ())

    answer = visit(q, mandatory, budget, tuple(range(len(cols))), ())
    need(time.monotonic()-started <= seconds, 'INCOMPLETE literal final time guard')
    if answer is not None:
        covered = set()
        found = [0]*15
        cost = 0
        for i in answer:
            need(not covered & pairs[i], 'false literal witness pair repetition')
            covered.update(pairs[i]);cost += costs[i]
            for z in cols[i]:
                found[z] += 1
        need(tuple(found) == q and mandatory <= covered and cost == budget, 'false literal witness')
        return dict(sat=True, states=states, witness=[cols[i] for i in answer])
    return dict(sat=False, states=states, witness=[])
