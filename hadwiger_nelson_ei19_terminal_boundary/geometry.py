"""Exact rational contraction certificate for one isolated real realization.

The 34 variables are x2,y2,...,x18,y18. Vertices 0 and 1 are fixed at
(0,0),(1,0). F contains the 34 non-anchor squared-unit-edge equations.
The proof and norm bounds are stated in README.md.
"""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


def verify(path):
    cert = json.loads(path.read_text())
    need(cert['schema'] == 'EI19-isolated-unit-equations-v1', 'schema')
    h = cert['point_denominator']
    a = cert['inverse_denominator']
    rd = cert['radius_denominator']
    need(all(type(x) is int and x > 0 for x in (h, a, rd)), 'denominators')
    radius = Q(1, rd)
    mid = cert['centre_numerators']
    inv = cert['inverse_numerators']
    edges = list(map(tuple, cert['edge_equations']))
    need(len(mid) == 19 and all(len(p) == 2 and all(type(x) is int for x in p)
                               for p in mid), 'point dimensions')
    need(mid[0] == [0, 0] and mid[1] == [h, 0], 'fixed anchors')
    need(len(inv) == 34 and all(len(row) == 34 and all(type(x) is int for x in row)
                               for row in inv), 'inverse dimensions')
    need(edges == sorted(set(edges)) and len(edges) == 35 and (0, 1) in edges
         and all(type(u) is int and type(v) is int and 0 <= u < v < 19
                 for u, v in edges), 'unit equation list')
    equations = [e for e in edges if e != (0, 1)]
    jac = [[0]*34 for _ in range(34)]  # h times J(mid/h)
    residual = []  # h^2 times F(mid/h)
    for k, (u, v) in enumerate(equations):
        difference = [mid[u][d] - mid[v][d] for d in range(2)]
        residual.append(sum(z*z for z in difference) - h*h)
        for d in range(2):
            if u >= 2:
                jac[k][2*(u-2)+d] = 2*difference[d]
            if v >= 2:
                jac[k][2*(v-2)+d] = -2*difference[d]

    # A = inv/a. These are exact induced infinity-norm bounds.
    defect = [[int(i == j)*a*h - sum(inv[i][k]*jac[k][j] for k in range(34))
               for j in range(34)] for i in range(34)]
    beta = Q(max(sum(abs(x) for x in row) for row in defect), a*h)
    anorm = Q(max(sum(abs(x) for x in row) for row in inv), a)
    afnorm = Q(max(abs(sum(inv[i][k]*residual[k] for k in range(34)))
                  for i in range(34)), a*h*h)
    eta = beta + 16*radius*anorm
    displacement = afnorm + eta*radius
    need(beta < 1, 'A is nonsingular because A J(mid) is nonsingular')
    need(eta < 1, 'uniform contraction bound')
    need(displacement < radius, 'strict self-map of the rational box')

    separation = None
    unit_gap = None
    nonedges = 0
    for u, v in combinations(range(19), 2):
        difference = [Q(mid[u][d] - mid[v][d], h) for d in range(2)]
        d2 = sum(z*z for z in difference)
        error = 4*radius*sum(abs(z) for z in difference) + 8*radius*radius
        lower = d2 - error
        need(lower > 0, 'distinct physical points')
        separation = lower if separation is None else min(separation, lower)
        if (u, v) not in edges:
            gap = abs(d2 - 1) - error
            need(gap > 0, 'exclude every unlisted unit contact')
            unit_gap = gap if unit_gap is None else min(unit_gap, gap)
            nonedges += 1
    need(eta < Q(1, 10**21) and displacement < Q(1, 10**46),
         'advertised compact contraction bounds')
    need(separation > Q(1, 100) and unit_gap > Q(1, 100),
         'advertised compact pair bounds')
    return {'status': 'EXACT ISOLATED EI19 SUPPORT VERIFIED',
            'points': 19, 'unit_edges': 35, 'all_pairs': 171,
            'nonedges_excluded': nonedges, 'root_variables': 34,
            'radius': str(radius), 'inverse_norm_upper': str(anorm),
            'midpoint_defect_norm_upper': str(beta),
            'contraction_norm_upper': str(eta),
            'fixed_point_displacement_bound': str(displacement),
            'squared_separation_lower': str(separation),
            'nonedge_squared_unit_gap_lower': str(unit_gap),
            'certificate_sha256': sha256(path.read_bytes()).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.certificate), indent=2))
