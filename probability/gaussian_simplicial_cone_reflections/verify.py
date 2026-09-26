#!/usr/bin/env python3
"""Exact audits for PROOF.md; CPython standard library only.

Universal statements are proved in PROOF.md. This program checks the
polynomial identities and finite algebra used there. It neither samples
Gaussian integrals nor interprets finite sampling as a proof of a motion.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def add(x, y):
    return tuple(a+b for a, b in zip(x, y))


def scale(c, x):
    return tuple(c*a for a in x)


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), Q(0))


def distance2(x, y):
    return dot(add(x, scale(-1, y)), add(x, scale(-1, y)))


def linear_combination(coefficients, vectors):
    return tuple(sum(c*v[j] for c, v in zip(coefficients, vectors))
                 for j in range(len(vectors[0])))


def rank(matrix):
    a = [[Q(x) for x in row] for row in matrix]
    if not a:
        return 0
    pivot = 0
    for col in range(len(a[0])):
        candidates = [i for i in range(pivot, len(a)) if a[i][col]]
        if not candidates:
            continue
        p = candidates[0]
        a[pivot], a[p] = a[p], a[pivot]
        d = a[pivot][col]
        a[pivot] = [x/d for x in a[pivot]]
        for i in range(len(a)):
            if i != pivot and a[i][col]:
                d = a[i][col]
                a[i] = [x-d*y for x, y in zip(a[i], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def det3(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def gram(vectors):
    return [[dot(x, y) for y in vectors] for x in vectors]


def affine_paired_rank(x, y):
    pairs = [a+b for a, b in zip(x, y)]
    return rank([add(row, scale(-1, pairs[0])) for row in pairs[1:]])


# Sparse multivariate polynomials with integer coefficients. All variables
# are formal; zero means coefficientwise identity, not evaluation at points.
def padd(a, b):
    c = dict(a)
    for m, v in b.items():
        c[m] = c.get(m, 0)+v
    return {m: v for m, v in c.items() if v}


def pneg(a):
    return {m: -v for m, v in a.items()}


def pmul(a, b):
    c = {}
    for i, u in a.items():
        for j, v in b.items():
            k = tuple(x+y for x, y in zip(i, j))
            c[k] = c.get(k, 0)+u*v
    return {m: v for m, v in c.items() if v}


def psquare(a):
    return pmul(a, a)


def polynomial_audits():
    one, h, t = {(0, 0): 1}, {(1, 0): 1}, {(0, 1): 1}
    num, den = padd(t, h), padd(one, pmul(h, t))
    q2, k2 = padd(one, pneg(psquare(t))), padd(one, pneg(psquare(h)))
    identities = [
        padd(padd(psquare(num), pmul(k2, q2)), pneg(psquare(den))),
        padd(padd(pmul(t, num), q2), pneg(den)),
        padd(padd(den, pneg(pmul(h, num))), pneg(k2)),
    ]
    # a(v)-a(u): exact cleared-denominator monotonicity identity.
    one = {(0, 0, 0): 1}
    h, u, v = {(1, 0, 0): 1}, {(0, 1, 0): 1}, {(0, 0, 1): 1}
    lhs = padd(pmul(padd(v, h), padd(one, pmul(h, u))),
               pneg(pmul(padd(u, h), padd(one, pmul(h, v)))))
    rhs = pmul(padd(v, pneg(u)), padd(one, pneg(psquare(h))))
    identities.append(padd(lhs, pneg(rhs)))
    for i, identity in enumerate(identities):
        require(not identity, f'Polynomial identity {i} failed')
    require(bool(padd(lhs, pneg(padd(rhs, one)))), 'Corrupt identity accepted')
    return len(identities)


def fixture():
    v = [tuple(map(Q, row)) for row in (
        ('3/13', '4/13', '12/13'), ('1', '0', '0'), ('3/5', '4/5', '0'))]
    a = [tuple(map(Q, row)) for row in (
        ('0', '0', '13/12'), ('1', '-3/4', '0'), ('0', '5/4', '-5/12'))]
    require([[dot(x, y) for y in v] for x in a] ==
            [[Q(i == j) for j in range(3)] for i in range(3)], 'Wrong dual basis')
    return a, v


def time_coordinates(parameter):
    if parameter is None:
        return Q(1), Q(0)
    u = Q(parameter)
    return (u*u-1)/(u*u+1), 2*u/(u*u+1)


def rational_motion(v, parameter):
    t, q = time_coordinates(parameter)
    h = Q(12, 13)
    aa = (t+h)/(1+h*t)
    result = [scale(aa, v[0])+scale(q/(1+h*t), v[0][:2])]
    result.extend(scale(t, w)+scale(q, w[:2]) for w in v[1:])
    return result


def check_cloud_motion(a, v, frames):
    # Nonnegative combinations test interior points, not only extreme rays.
    cs = [tuple(map(Q, row)) for row in (
        (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1),
        (2, 3, 5), ('1/2', '1/3', '1/4'))]
    fixed = [linear_combination(c, a) for c in cs]
    moving = [linear_combination(c, v) for c in cs]
    require(min(dot(x, y) for x in fixed for y in moving) >= 0,
            'Not positive-dual separated')
    previous = None
    pair_checks = 0
    gram_checks = 0
    for frame in frames:
        require(gram(frame) == gram(v), 'Moving frame lost its Gram matrix')
        gram_checks += 9
        points = [(Q(0),)*5]+[p+(Q(0), Q(0)) for p in fixed]
        points += [linear_combination(c, frame) for c in cs]
        if previous is not None:
            for i in range(len(points)):
                for j in range(i):
                    require(distance2(points[i], points[j]) <=
                            distance2(previous[i], previous[j]), 'Distance increased')
                    pair_checks += 1
        previous = points
    require(frames[0] == [scale(-1, w)+(Q(0), Q(0)) for w in v], 'Initial endpoint')
    require(frames[-1] == [w+(Q(0), Q(0)) for w in v], 'Final endpoint')
    return dict(points=13, times=len(frames), pair_checks=pair_checks, gram_entries=gram_checks)


def motion_audits():
    a, v = fixture()
    zero = (Q(0),)*3
    x, y = [zero]+a+[scale(-1, w) for w in v], [zero]+a+v
    require(affine_paired_rank(x, y) == 6, 'Seven-point rank')
    parameters = [Q(0), Q(1, 5), Q(1, 3), Q(1, 2), Q(1), Q(2), Q(3), Q(5), None]
    frames = [rational_motion(v, t) for t in parameters]
    regular = check_cloud_motion(a, v, frames)
    require(det3(v) != 0 and det3(a) != 0, 'Singular fixture')
    require(dot(v[0], v[1]) != 0, 'Orthogonal fixture loses strong-contraction exclusion')
    # Boundary case h=1, implemented separately as in the proof.
    v0 = [tuple(map(Q, row)) for row in ((0, 0, 1), (1, 0, 0), ('3/5', '4/5', 0))]
    a0 = [tuple(map(Q, row)) for row in ((0, 0, 1), (1, '-3/4', 0), (0, '5/4', 0))]
    boundary_frames = []
    for u in parameters:
        t, q = time_coordinates(u)
        boundary_frames.append([scale(t, v0[0])+(q, Q(0))]+
                               [scale(-1, w)+(Q(0), Q(0)) for w in v0[1:]])
    for u in parameters[1:]:
        t, q = time_coordinates(u)
        boundary_frames.append([v0[0]+(Q(0), Q(0))]+
                               [scale(t, w)+scale(q, w[:2]) for w in v0[1:]])
    boundary = check_cloud_motion(a0, v0, boundary_frames)
    # Deliberately violate the dual-cone hypothesis.
    bad_a = scale(-1, a[0])
    loss = distance2(bad_a, scale(-1, v[0]))-distance2(bad_a, v[0])
    require(loss == -4, 'Invalid-dual control failed to detect expansion')
    return dict(regular=regular, h_equals_one=boundary, paired_rank=6,
                determinant_v=str(det3(v)), determinant_a=str(det3(a)),
                invalid_dual_squared_loss=str(loss))


def square_audits():
    a = [tuple(map(Q, row)) for row in ((1, 0, 1), (0, 1, 1), (-1, 0, 1), (0, -1, 1))]
    b = [tuple(map(Q, row)) for row in ((1, 1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1))]
    zero = (Q(0),)*3
    x, y = [zero]+a+[scale(-1, w) for w in b], [zero]+a+b
    cross = [[dot(u, v) for v in b] for u in a]
    require(set(t for row in cross for t in row) == {0, 2}, 'Unexpected incidence values')
    strict = preserved = 0
    for i in range(9):
        for j in range(i):
            loss = distance2(x[i], x[j])-distance2(y[i], y[j])
            expected = 4*dot(a[j-1], b[i-5]) if i >= 5 and 1 <= j <= 4 else Q(0)
            require(loss == expected and loss >= 0, 'Endpoint squared-distance identity')
            strict += loss > 0
            preserved += loss == 0
    require(affine_paired_rank(x, y) == 6, 'Nine-point paired rank')
    require(affine_paired_rank(x[1:], y[1:]) == 5, 'Deleting origin must give rank five')
    require(rank(a) == rank(b) == 3, 'Three-dimensional blocks required')
    circuit = (Q(1), Q(-1), Q(1), Q(-1))
    require(linear_combination(circuit, b) == zero, 'Wrong moving circuit')
    require(all(det3([b[j] for j in range(4) if j != i]) != 0 for i in range(4)),
            'Moving circuit has a missing coefficient')
    normals = []
    for j in range(4):
        inc = [a[i] for i in range(4) if cross[i][j] == 0]
        require(len(inc) == 2 and rank(inc) == 2, 'Facet normals do not pin an extreme ray')
        normals.append(inc)
    # Independent linear encoding of the projection rigidity: a_i^T L b_j=0
    # at each zero incidence. Eight independent rows leave only scalar I.
    constraints = [tuple(u[r]*v[s] for r in range(3) for s in range(3))
                   for u in a for v in b if dot(u, v) == 0]
    identity = tuple(Q(r == s) for r in range(3) for s in range(3))
    require(rank(constraints) == 8, 'Projection constraints not rank eight')
    require(all(dot(row, identity) == 0 for row in constraints), 'Scalar matrix not feasible')
    first_gram = gram(b[:3])
    require(det3(first_gram) == 16, 'Residual rank-three certificate')
    require(any(distance2(y[i], y[j])-distance2(x[i], x[j]) < 0
                for i in range(9) for j in range(i)), 'Reversed-contraction control')
    weights = [Q(2**i, 511) for i in range(9)]
    subsets = {}
    for mask in range(512):
        total = sum((weights[i] for i in range(9) if mask & (1 << i)), Q(0))
        require(total not in subsets, 'Binary subset collision')
        subsets[total] = mask
    require(sum(weights) == 1, 'Weight normalization')
    require(all(subsets[w] == 1 << i for i, w in enumerate(weights)),
            'An alternative deterministic matching was not excluded')
    return dict(points=9, strict_pairs=strict, preserved_pairs=preserved,
                paired_rank=6, paired_rank_without_origin=5,
                anchored_rank=3, moving_rank=3, moving_circuit=list(map(str, circuit)),
                zero_incidence_constraints=len(constraints), projection_constraint_rank=8,
                asymmetric_weights=list(map(str, weights)), distinct_subset_sums=len(subsets),
                residual_gram_minor=str(det3(first_gram)),
                positive_cross_products=[[str(t) for t in row] for row in cross],
                input_points=[[str(t) for t in row] for row in x],
                output_points=[[str(t) for t in row] for row in y])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    report = dict(status='CONE_REFLECTION_EXACT_AUDITS_PASS',
                  universal_polynomial_identities=polynomial_audits(),
                  motion=motion_audits(), square_obstruction=square_audits(),
                  rejected_invalid_controls=3,
                  trust_boundary='Written proof plus Fraction/integer audits; no formalization')
    output = json.dumps(report, indent=2, sort_keys=True)+'\n'
    if args.check:
        expected = (HERE/'EXPECTED.json').read_text()
        require(output == expected, 'Output differs from EXPECTED.json')
        print(json.dumps(dict(status=report['status'],
              expected_sha256=hashlib.sha256(output.encode()).hexdigest()), sort_keys=True))
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
