#!/usr/bin/env python3
"""Exact finite checks for PROOF.md; no search, solver, or floating point."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def norm(x):
    return dot(x, x)


def p(u):
    return (u[0] + u[1], u[1] - u[0])


def a(v):
    return (*v, (1 + norm(v)) / 2)


def b(u):
    return (*u, -norm(u))


def target(u):
    return (-u[1], u[0], 1 - norm(u))


def rank(rows):
    rows = [[F(x) for x in row] for row in rows]
    if not rows:
        return 0
    r = 0
    for c in range(len(rows[0])):
        pivot = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        scale = rows[r][c]
        rows[r] = [x / scale for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                scale = rows[i][c]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[r])]
        r += 1
        if r == len(rows):
            break
    return r


def affine_rank(points):
    return rank([sub(x, points[0]) for x in points[1:]])


PARAMETERS = tuple(tuple(map(F, u)) for u in
                   [(0, 0), (1, 0), (-1, 0), (2, 0), (-2, 0),
                    (0, 1), (0, -1), (1, 1)])
EPS = F(1, 4)
FIXED = [p(u) for u in PARAMETERS]
for u in (PARAMETERS[0], PARAMETERS[1]):
    for j in range(2):
        for sign in (-1, 1):
            v = list(p(u))
            v[j] += sign * EPS
            FIXED.append(tuple(v))

LABELS = [('A', v) for v in FIXED] + [('B', u) for u in PARAMETERS]
SOURCE = [a(v) for v in FIXED] + [b(u) for u in PARAMETERS]
TARGET = [a(v) for v in FIXED] + [target(u) for u in PARAMETERS]


def fixture():
    return {'format': 'rational-two-body-screw-v1',
            'epsilon': str(EPS),
            'sites': [
                {'label': f'{kind}{i}', 'group': kind,
                 'parameter': list(map(str, u)),
                 'source': list(map(str, x)), 'target': list(map(str, y))}
                for i, ((kind, u), x, y) in
                enumerate(zip(LABELS, SOURCE, TARGET))]}


def loss_row(v, u):
    """Coefficients of (7): M row-major, t_phys, c, d, constant."""
    av, bu = a(v), b(u)
    return ([2 * av[i] * bu[j] for i in range(3) for j in range(3)]
            + [2 * x for x in av] + [-2 * x for x in bu]
            + [F(-1), -2 * dot(av, bu)])


# Polynomials in alpha, v01, v02, represented by exact monomial dictionaries.
ZERO = {}


def const(x):
    return {(0, 0, 0): F(x)} if x else {}


def var(j):
    exponent = [0, 0, 0]
    exponent[j] = 1
    return {tuple(exponent): F(1)}


def add(*polys):
    out = {}
    for poly in polys:
        for exponent, coefficient in poly.items():
            out[exponent] = out.get(exponent, F(0)) + coefficient
    return {e: c for e, c in out.items() if c}


def scale(poly, q):
    return {e: c * q for e, c in poly.items() if c * q}


def mul(left, right):
    out = {}
    for e, c in left.items():
        for f, d in right.items():
            g = tuple(x + y for x, y in zip(e, f))
            out[g] = out.get(g, F(0)) + c * d
    return {e: c for e, c in out.items() if c}


def checks():
    require(len(set(SOURCE)) == 24, 'distinct source sites')
    require(len(FIXED) == len(set(FIXED)) == 16, 'fixed parameter count')
    require(len(PARAMETERS) == 8, 'moving parameter count')
    require(affine_rank(SOURCE[:16]) == 3, 'fixed affine rank')
    require(affine_rank(SOURCE[16:]) == 3, 'moving affine rank')
    paired_rank = affine_rank([(*x, *y) for x, y in zip(SOURCE, TARGET)])
    require(paired_rank == 6, 'paired affine rank')
    tight, pairs = 0, 0
    for i, j in combinations(range(24), 2):
        loss = norm(sub(SOURCE[i], SOURCE[j])) - norm(sub(TARGET[i], TARGET[j]))
        if LABELS[i][0] == LABELS[j][0]:
            expected = F(0)
        else:
            expected = norm(sub(LABELS[i][1], p(LABELS[j][1])))
        require(loss == expected and loss >= 0, f'endpoint pair {i},{j}')
        pairs += 1
        tight += loss == 0
    require(pairs == 276 and tight == 156, 'pair counts')

    # Exact linear certificate forcing M33=1 from five tight equations.
    combo = [F(0)] * 17
    for x, weight in zip(range(-2, 3), (1, -4, 6, -4, 1)):
        row = loss_row(p((F(x), F(0))), (F(x), F(0)))
        combo = [c + weight * r for c, r in zip(combo, row)]
    expected_combo = [F(0)] * 17
    expected_combo[8], expected_combo[16] = F(-48), F(48)
    require(combo == expected_combo, 'fourth difference identity')
    unisolvent = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1)]
    require(rank([[1, x, y, x*x, x*y, y*y] for x, y in unisolvent]) == 6,
            'quadratic unisolvence')

    alpha, v1, v2 = (var(j) for j in range(3))
    # Substitutions from (9), (11), (12) at tau=1/2.
    assignments = [alpha, scale(alpha, -1), ZERO,
                   alpha, alpha, ZERO, ZERO, ZERO, const(1),
                   v1, v2, const(F(1, 2)),
                   add(v1, scale(v2, -1)), add(v1, v2), const(F(1, 2)),
                   const(F(1, 2)), const(1)]
    identities = 0
    for v in FIXED:
        for u in PARAMETERS:
            actual = add(*(scale(poly, q) for poly, q in
                           zip(assignments, loss_row(v, u))))
            eta = sub(v, p(u))
            ipj_u = (u[0] - u[1], u[0] + u[1])
            expected = add(const(norm(eta) / 2),
                           scale(add(alpha, const(F(-1, 2))),
                                 2 * dot(eta, ipj_u)),
                           scale(v1, 2 * eta[0]), scale(v2, 2 * eta[1]))
            require(actual == expected, 'midpoint loss polynomial')
            identities += 1

    # Norm of [(1-alpha)I+(1+alpha)J]v is 2(1+alpha^2)|v|^2.
    one_minus = add(const(1), scale(alpha, -1))
    one_plus = add(const(1), alpha)
    w1 = add(mul(one_minus, v1), scale(mul(one_plus, v2), -1))
    w2 = add(mul(one_plus, v1), mul(one_minus, v2))
    v_norm = add(mul(v1, v1), mul(v2, v2))
    rhs = mul(scale(add(const(1), mul(alpha, alpha)), 2), v_norm)
    require(add(mul(w1, w1), mul(w2, w2)) == rhs, 'norm polynomial')
    k2 = add(const(1), scale(mul(alpha, alpha), -2))
    require(add(k2, scale(add(const(1), mul(alpha, alpha)), 2)) == const(3),
            'coefficient cancellation')
    upper_v = 2 * (EPS / 4)**2
    upper_alpha = F(1, 2) + EPS / 2
    lower_k = 1 - 2 * upper_alpha**2
    lower_v = lower_k / 12
    require(upper_v == F(1, 128) and lower_v == F(7, 384), 'rational bounds')
    gap = lower_v - upper_v
    require(gap == F(1, 96) and gap > 0, 'midpoint contradiction')

    # Direct squared-distance replay of the R6 positive control (19).
    # Square roots are eliminated only in their squared Euclidean contribution.
    motion_checks = 0
    for s in map(F, ('0', '1/4', '1/2', '3/4', '1')):
        r = 1 - s
        physical, transverse, last = [], [], []
        for kind, u in LABELS:
            if kind == 'A':
                physical.append(a(u)); transverse.append((F(0), F(0))); last.append(F(0))
            else:
                physical.append((r*u[0]-s*u[1], s*u[0]+r*u[1], -norm(u)+s))
                transverse.append(u); last.append(F(1))
        for i, j in combinations(range(24), 2):
            moved = (norm(sub(physical[i], physical[j]))
                     + 2*s*r*norm(sub(transverse[i], transverse[j]))
                     + s*r*(last[i]-last[j])**2)
            desired = r*norm(sub(SOURCE[i], SOURCE[j])) + s*norm(sub(TARGET[i], TARGET[j]))
            require(moved == desired, 'R6 motion control')
            motion_checks += 1

    # Adverse controls: endpoint inequality is not automatic for arbitrary
    # axial translation; the midpoint numerical certificate is not valid
    # for arbitrary probe spacing.
    bad_loss = norm(sub(a((F(0), F(0))), b((F(0), F(0))))) - norm(sub(a((F(0), F(0))), (F(0), F(0), F(2))))
    require(bad_loss == -2, 'wrong-translation rejection')
    bad_eps = F(1, 2)
    bad_gap = (1-2*(F(1, 2)+bad_eps/2)**2)/12 - 2*(bad_eps/4)**2
    require(bad_gap <= 0, 'wide-probe certificate rejection')
    return {'sites': 24, 'fixed_sites': 16, 'moving_sites': 8,
            'pairs': pairs, 'tight_pairs': tight, 'strict_pairs': pairs-tight,
            'paired_affine_rank': paired_rank,
            'fourth_difference_M33_coefficient': '-48',
            'quadratic_evaluation_rank': 6, 'midpoint_polynomial_checks': identities,
            'norm_polynomial_checks': 2, 'midpoint_lower_bound': str(lower_v),
            'midpoint_upper_bound': str(upper_v), 'contradiction_gap': str(gap),
            'R6_pair_time_checks': motion_checks, 'adverse_controls': 2}


def main():
    if sys.argv[1:] == ['--write-fixture']:
        (HERE / 'WITNESS.json').write_text(json.dumps(fixture(), indent=2) + '\n')
        return
    require(not sys.argv[1:], 'unknown arguments')
    witness_bytes = (HERE / 'WITNESS.json').read_bytes()
    require(json.loads(witness_bytes) == fixture(), 'fixture mismatch')
    result = checks()
    result['witness_sha256'] = sha256(witness_bytes).hexdigest()
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
