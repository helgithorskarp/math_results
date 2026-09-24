"""Optional discovery producer; stdout is a candidate for check.py.

Requires NumPy and SciPy. Floating-point output is rationalized, then
independently checked by check.py; solver status is not a certificate.
"""
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement
import json

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp


def model(d, loops, edges):
    kinds = sorted(edges + [(i, i) for i in loops])
    triangles = [t for t in combinations_with_replacement(range(d), 3)
                 if all(e in kinds for e in combinations(t, 2))]
    matrix = np.array([[sum(e == kind for e in combinations(t, 2))
                        for t in triangles] for kind in kinds], dtype=float)
    capacities = np.array([0.5 if i == j else 1.0 for i, j in kinds])
    return kinds, triangles, matrix, capacities


def profile(name, d, loops, edges):
    kinds, triangles, matrix, capacities = model(d, loops, edges)
    result = linprog(-np.ones(len(triangles)), A_ub=matrix, b_ub=capacities,
                     bounds=(0, None), method='highs')
    if not result.success:
        raise RuntimeError(result.message)
    primal = [Q(float(v)).limit_denominator(100000) for v in result.x]
    dual = [Q(float(-v)).limit_denominator(100000) for v in result.ineqlin.marginals]
    return {'name': name, 'd': d, 'loops': loops, 'edges': [list(e) for e in edges],
            'primal': [{'types': list(t), 'weight': str(v)} for t, v in zip(triangles, primal) if v],
            'dual': [{'types': list(e), 'weight': str(v)} for e, v in zip(kinds, dual) if v],
            'optimum': str(sum(primal))}


def produce():
    neighborhoods = [(0, 1, 2), (0, 1, 3), (0, 3), (1, 2, 3), (2, 3)]
    seed_edges = list(combinations(range(4), 2)) + [(i, 4 + j) for j, s in enumerate(neighborhoods) for i in s]
    seed = profile('reviewed_nine_vertex_seed', 9, [], seed_edges)
    seed['primal'] = [{'types': [a, b, 4 + j], 'weight': '1/2'}
                      for j, s in enumerate(neighborhoods) for a, b in combinations(s, 2)]
    cube_edges = list(combinations(range(8), 2)) + [(i, 8 + j) for j in range(3) for i in range(8) if (i >> j) & 1]
    cube = profile('three_type_boolean_template', 11, list(range(8)), cube_edges)
    kinds, triangles, matrix, capacities = model(11, list(range(8)), cube_edges)
    integer = milp(np.zeros(len(triangles)), integrality=np.ones(len(triangles)),
                   bounds=Bounds(0, np.inf), constraints=LinearConstraint(matrix, 6 * capacities, 6 * capacities),
                   options={'time_limit': 30})
    if integer.x is None:
        raise RuntimeError('No cube witness within limit: ' + integer.message)
    cube['primal'] = [{'types': list(t), 'weight': str(Q(int(round(v)), 6))}
                      for t, v in zip(triangles, integer.x) if round(v) > 0]
    cube['dual'] = [{'types': list(e), 'weight': '1/3'} for e in kinds]
    clique = profile('one_clique_type', 1, [0], [])
    scale = 2
    literal_edges = sorted({tuple(sorted((a * scale + i, b * scale + j)))
                            for a, b in seed_edges for i in range(scale) for j in range(scale)})
    index = {e: i for i, e in enumerate(literal_edges)}
    literal_triangles = [t for t in combinations(range(18), 3) if all(e in index for e in combinations(t, 2))]
    matrix = np.zeros((len(literal_edges), len(literal_triangles)))
    for j, t in enumerate(literal_triangles):
        for e in combinations(t, 2):
            matrix[index[e], j] = 1
    integer = milp(-np.ones(len(literal_triangles)), integrality=np.ones(len(literal_triangles)),
                   bounds=Bounds(0, 1), constraints=LinearConstraint(matrix, 0, 1), options={'time_limit': 30})
    if integer.x is None:
        raise RuntimeError('No packing witness within limit: ' + integer.message)
    packing = [list(t) for t, v in zip(literal_triangles, integer.x) if v > 0.5]
    supported = set(cube_edges) | {(i, i) for i in range(8)}
    diagonal_edges = [e for e in combinations(range(33), 2)
                      if (e[0] // 3, e[1] // 3) in supported and e[0] % 3 != e[1] % 3]
    diagonal_index = {e: i for i, e in enumerate(diagonal_edges)}
    diagonal_triangles = [t for t in combinations(range(33), 3)
                          if all(e in diagonal_index for e in combinations(t, 2))]
    matrix = np.zeros((len(diagonal_edges), len(diagonal_triangles)))
    for j, t in enumerate(diagonal_triangles):
        for e in combinations(t, 2):
            matrix[diagonal_index[e], j] = 1
    integer = milp(np.zeros(len(diagonal_triangles)), integrality=np.ones(len(diagonal_triangles)),
                   bounds=Bounds(0, 1), constraints=LinearConstraint(matrix, 1, 1), options={'time_limit': 30})
    if integer.x is None:
        raise RuntimeError('No diagonal witness within limit: ' + integer.message)
    diagonal_packing = [list(t) for t, v in zip(diagonal_triangles, integer.x) if v > 0.5]
    return {'format': 1, 'profiles': [seed, cube, clique],
            'independent_lift': {'profile': seed['name'], 'scale': scale, 'packing': packing},
            'diagonal_decomposition': {'profile': cube['name'], 'scale': 3, 'packing': diagonal_packing}}


if __name__ == '__main__':
    print(json.dumps(produce(), indent=2, sort_keys=True))
