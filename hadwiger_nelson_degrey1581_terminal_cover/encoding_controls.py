#!/usr/bin/env python3
"""Compare optional search CNFs with direct colouring on every small graph."""
import json
from itertools import combinations
from pysat.solvers import Glucose4
from discover import formula

def main():
    graphs = cases = negatives = 0
    for n in range(2, 6):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            edges = [p for i, p in enumerate(pairs) if mask >> i & 1]
            adj = [set() for _ in range(n)]
            for u, v in edges:
                adj[u].add(v); adj[v].add(u)
            with Glucose4(bootstrap_with=formula(n, edges)) as solver:
                for choice in range(1 << (n-2)):
                    selected = {0, 1} | {v for v in range(2, n) if choice >> (v-2) & 1}
                    colours = {0: 0, 1: 1}
                    todo = sorted(selected-{0, 1}, key=lambda v: (-len(adj[v] & selected), v))
                    def rec(i):
                        if i == len(todo):
                            return True
                        v = todo[i]
                        used = {colours[u] for u in adj[v] if u in colours}
                        for c in range(4):
                            if c not in used:
                                colours[v] = c
                                if rec(i+1):
                                    return True
                                del colours[v]
                        return False
                    direct = rec(0)
                    assumptions = [(4*n+v+1)*(1 if v in selected else -1) for v in range(n)]+[1, 6]
                    result = solver.solve(assumptions=assumptions)
                    if result != direct:
                        raise ValueError('gated encoding mismatch')
                    if result:
                        model = set(x for x in solver.get_model() if x > 0)
                        word = {v: next(c for c in range(4) if 4*v+c+1 in model) for v in selected}
                        if word[0] == word[1] or any(word[u] == word[v] for u, v in edges if u in selected and v in selected):
                            raise ValueError('invalid model')
                    negatives += not result; cases += 1
            graphs += 1
    print(json.dumps(dict(verified=True, graphs=graphs, terminal_pinned_subsets=cases,
                          unsatisfiable_cases=negatives, independent_solver='Glucose4'), sort_keys=True, indent=2))

if __name__ == '__main__':
    main()
