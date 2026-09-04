#!/usr/bin/env python3
"""Generate the exact exceptional-degree count relaxation certificate.

Standard library only. Output is deterministic TSV on stdout; no file writes.
The search classifies integer count matrices, not Ramsey graphs.
"""

from itertools import combinations_with_replacement, product
from math import comb


DEGREES = (18, 19, 20, 22, 23, 24)
WEIGHTS = (21, 12, 3, 3, 12, 21)
U = dict(zip(range(18, 25), (85, 92, 100, 107, 114, 122, 132)))
OFFSETS = tuple(comb(42-d, 2) + 21*d - U[d] - U[42-d] + 14 - 231
                for d in DEGREES)
HEADER = "counts_18_to_24\tM\tW\tsplit_count\tstatus\tedge_counts\thalf_counts\tmultipliers"


def profiles():
    for ns in product(*(range(39 // w + 1) for w in WEIGHTS)):
        weight = sum(n*w for n, w in zip(ns, WEIGHTS))
        deviation = sum(n*(d-21) for n, d in zip(ns, DEGREES))
        if weight <= 39 and weight % 6 == 3 and deviation < 0 and deviation % 2:
            yield ns, (441 + deviation) // 2, weight


def system(ns, cross_total):
    active = tuple(i for i, n in enumerate(ns) if n)
    edges, capacities = [], []
    for i, j in combinations_with_replacement(active, 2):
        cap = comb(ns[i], 2) if i == j else ns[i]*ns[j]
        if cap:
            edges.append((i, j))
            capacities.append(cap)
    targets = [ns[i]*(cross_total-OFFSETS[i]) for i in active]
    coefficients = [[int(i == a)*(DEGREES[j]-21) + int(j == a)*(DEGREES[i]-21)
                     for i, j in edges] for a in active]
    weighted_degree = sum(n*d*(d-21) for n, d in zip(ns, DEGREES))
    lower_total = weighted_degree - (43-sum(ns))*(cross_total-220)
    return active, edges, capacities, targets, coefficients, lower_total


def first_solution(ns, cross_total, denominator=1):
    """Exact DFS with interval pruning; scale 2 tests half-integer solutions."""
    _, edges, caps, targets, coeff, lower = system(ns, cross_total)
    caps = [denominator*c for c in caps]
    targets = [denominator*t for t in targets]
    lower *= denominator
    nrows, ncols = len(targets), len(edges)
    row_min = [[0]*nrows for _ in range(ncols+1)]
    total_max = [0]*(ncols+1)
    for k in range(ncols-1, -1, -1):
        for a in range(nrows):
            row_min[k][a] = row_min[k+1][a] + min(0, coeff[a][k]*caps[k])
        total_max[k] = total_max[k+1] + max(0, sum(row[k] for row in coeff)*caps[k])

    def visit(k, sums, values):
        if any(sums[a]+row_min[k][a] > targets[a] for a in range(nrows)):
            return None
        if sum(sums)+total_max[k] < lower:
            return None
        if k == ncols:
            return values
        for value in range(caps[k]+1):
            result = visit(k+1, tuple(sums[a]+value*coeff[a][k] for a in range(nrows)),
                           values+(value,))
            if result is not None:
                return result
        return None

    return visit(0, (0,)*nrows, ())


def linear_obstruction(ns, cross_total):
    """Try small nonnegative combinations of exceptional-class inequalities."""
    _, edges, caps, targets, coeff, _ = system(ns, cross_total)
    for multipliers in product(range(5), repeat=len(targets)):
        rhs = sum(a*b for a, b in zip(multipliers, targets))
        weighted = [sum(a*row[k] for a, row in zip(multipliers, coeff))
                    for k in range(len(edges))]
        minimum = sum(cap*min(0, weight) for cap, weight in zip(caps, weighted))
        if minimum > rhs:
            return multipliers
    return None


def csv(values):
    return ",".join(map(str, values)) if values else "-"


def main():
    print(HEADER)
    for ns, cross_total, weight in profiles():
        full = ns[:3]+(43-sum(ns),)+ns[3:]
        splits = sum(sum(a*(d-21) for a, d in zip(first, DEGREES)) == cross_total-220
                     for first in product(*(range(n+1) for n in ns)))
        solution = first_solution(ns, cross_total)
        fractional = multipliers = None
        if solution is None:
            multipliers = linear_obstruction(ns, cross_total)
            if multipliers is None:
                fractional = first_solution(ns, cross_total, 2)
                if fractional is None:
                    raise AssertionError(("unclassified obstruction", ns))
        print("\t".join((csv(full), str(cross_total), str(weight), str(splits),
                         "feasible" if solution is not None else "excluded",
                         csv(solution), csv(fractional), csv(multipliers))))


if __name__ == "__main__":
    main()
