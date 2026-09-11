#!/usr/bin/env python3
"""Definition-level exhaustive tests and a canonical model of the lower bound."""
import itertools
import json
from pysat.solvers import Solver
from encode import generate
from audit import symbols, clause_kind


def avoiding(coloring, k):
    """Independent integer-set subset sums; updates descend in cardinality."""
    n = len(coloring)
    for color in (0, 1):
        sums = [set() for _ in range(k + 1)]
        sums[0].add(0)
        for x, value in enumerate(coloring, 1):
            if value != color:
                continue
            for count in range(k, 0, -1):
                sums[count].update(s + x for s in sums[count - 1] if s + x <= n)
        if any(coloring[total - 1] == color for total in sums[k]):
            return False
    return True


def main():
    exhaustive = []
    for k, n, r in [(2, 8, 3), (3, 12, 5), (4, 12, 5)]:
        nv, clauses = generate(n, k, r)
        meaning = symbols(n, k, r)
        for clause in clauses:
            clause_kind(clause, meaning, n, k, r)
        edges = [xs + (sum(xs),) for xs in itertools.combinations(range(1, n + 1), k)
                 if sum(xs) <= n and xs[-2] <= r]
        with Solver(name='glucose3', bootstrap_with=clauses) as solver:
            for mask in range(1 << n):
                colors = [(mask >> x) & 1 for x in range(n)]
                expected = not any(len({colors[x - 1] for x in edge}) == 1
                                   for edge in edges)
                actual = solver.solve(assumptions=[x if colors[x - 1] else -x
                                                   for x in range(1, n + 1)])
                if actual != expected:
                    raise RuntimeError((k, n, r, mask, actual, expected))
        exhaustive.append({'k': k, 'n': n, 'r': r, 'colorings': 1 << n})

    # Published full [364] coloring, not an assumed shape for the upper bound.
    n, k, r = 364, 8, 171
    colors = [int(x == 1 or 44 <= x <= 329) for x in range(1, n + 1)]
    if not avoiding(colors, k):
        raise RuntimeError('published lower-bound coloring rejected')
    nv, clauses = generate(n, k, r)
    meaning = symbols(n, k, r)
    assignment = [False] + list(map(bool, colors))
    snapshots = {}
    for color in (0, 1):
        sums = [set() for _ in range(k + 1)]
        sums[0].add(0)
        for prefix in range(1, r + 1):
            if colors[prefix - 1] == color:
                for count in range(k, 0, -1):
                    sums[count].update(s + prefix for s in sums[count - 1]
                                       if s + prefix <= n)
            snapshots[color, prefix] = [frozenset(s) for s in sums]
    for color, prefix, count, total in meaning[n + 1:]:
        assignment.append(total in snapshots[color, prefix][count])
    if len(assignment) != nv + 1:
        raise RuntimeError('canonical-model length mismatch')
    for clause in clauses:
        if not any(assignment[abs(lit)] == (lit > 0) for lit in clause):
            raise RuntimeError(('canonical model violates clause', clause))
    print(json.dumps({'status': 'PASS', 'exhaustive_comparisons': exhaustive,
                      'total_colorings': sum(row['colorings'] for row in exhaustive),
                      'published_lower_bound': {'n': n, 'avoiding': True,
                                               'canonical_model_clauses': len(clauses)}}, indent=2))


if __name__ == '__main__':
    main()
