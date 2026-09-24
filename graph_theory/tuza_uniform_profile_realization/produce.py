"""Optional floating-point witness discovery; check.py is the exact authority.

Requires NumPy and SciPy (originally SciPy 1.17.1). Emits one compact JSON
certificate to stdout. No optimality or infeasibility claim uses solver status.
"""
from fractions import Fraction as Q
from itertools import combinations
import json
import sys

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp

import construct as C


def produce():
    es = C.boolean_support()
    ts = C.triangles(11, es)
    A = np.array([[C.incidence(t)[e] for t in ts] for e in es], dtype=float)
    capacity = np.array([.5 if i == j else 1 for i, j in es])
    # Maximize mu subject to A x=c and every triangle-type mass x_T>=mu.
    objective = np.zeros(len(ts) + 1)
    objective[-1] = -1
    result = linprog(objective, A_ub=np.column_stack([-np.eye(len(ts)), np.ones(len(ts))]),
                     b_ub=np.zeros(len(ts)), A_eq=np.column_stack([A, np.zeros(len(es))]),
                     b_eq=capacity, bounds=(0, None), method='highs')
    C.require(result.success, 'profile solver failed: ' + result.message)
    x = [Q(float(v)).limit_denominator(10**6) for v in result.x[:-1]]
    mu = Q(float(result.x[-1])).limit_denominator(10**6)
    C.require(all(sum(C.incidence(t)[e] * z for t, z in zip(ts, x)) ==
                  (Q(1, 2) if e[0] == e[1] else 1) for e in es), 'rational profile failed')
    C.require(min(x) == mu == Q(1, 26), 'unexpected margin; inspect before use')
    positive = {'d': 11, 'core_types': list(range(8)), 'edges': [list(e) for e in es if e[0] != e[1]],
                'margin': str(mu), 'profile': [{'types': list(t), 'weight': str(z)} for t, z in zip(ts, x)]}
    sizes = [5] + [4] * 10
    parent, edges = C.literal_host(sizes, es)
    edges = sorted(edges)
    edge_set = set(edges)
    triangles = [t for t in combinations(range(len(parent)), 3)
                 if all(e in edge_set for e in combinations(t, 2))]
    ids = {e: j for j, e in enumerate(edges)}
    incidence = np.zeros((len(edges), len(triangles)))
    for j, t in enumerate(triangles):
        for e in combinations(t, 2):
            incidence[ids[e], j] = 1
    # One binary variable per actual triangle; every graph edge is covered once.
    result = milp(np.zeros(len(triangles)), integrality=np.ones(len(triangles)), bounds=Bounds(0, 1),
                  constraints=LinearConstraint(incidence, 1, 1), options={'time_limit': 30})
    C.require(result.x is not None, 'no finite witness: ' + result.message)
    packing = [list(t) for t, value in zip(triangles, result.x) if value > .5]
    candidate = {'positive_profile': positive, 'unequal_decomposition': {'sizes': sizes, 'packing': packing}}
    # Independently formulated exact checks certify feasibility, not solver optimality.
    from check import profile_check, packing_check
    checked_support, _ = profile_check(positive)
    packing_check(candidate['unequal_decomposition'], checked_support)
    print('Verified profile and literal packing; MILP variables=' + str(len(triangles)), file=sys.stderr)
    return candidate


if __name__ == '__main__':
    print(json.dumps(produce(), indent=2))
