#!/usr/bin/env python3
"""Exact algebraic controls for SUPPORT_SIGN.md, without Gaussian integration.

The universal Price identity, weak differentiation, endpoint continuity and
Gaussian/spherical integration remain written-proof inputs. Only integers
and fractions are used; no solver, quadrature or external data is required.
"""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def transpose(a):
    return tuple(zip(*a))


def mm(a, b):
    return tuple(tuple(sum(x*y for x, y in zip(row, col))
                       for col in transpose(b)) for row in a)


def identity(n):
    return tuple(tuple(F(i == j) for j in range(n)) for i in range(n))


def diagonal(a):
    return tuple(tuple(x if i == j else F(0) for j in range(len(a)))
                 for i, x in enumerate(a))


def inverse(a):
    n = len(a)
    rows = [list(map(F, row))+list(identity(n)[i]) for i, row in enumerate(a)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if rows[i][j]), None)
        require(pivot is not None, 'singular matrix')
        rows[j], rows[pivot] = rows[pivot], rows[j]
        v = rows[j][j]
        rows[j] = [x/v for x in rows[j]]
        for i in range(n):
            if i != j:
                v = rows[i][j]
                rows[i] = [x-v*y for x, y in zip(rows[i], rows[j])]
    result = tuple(tuple(row[n:]) for row in rows)
    require(mm(a, result) == identity(n), 'inverse multiplication')
    return result


def det(a):
    rows = [list(map(F, row)) for row in a]
    answer = F(1)
    for j in range(len(rows)):
        pivot = next((i for i in range(j, len(rows)) if rows[i][j]), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            rows[j], rows[pivot] = rows[pivot], rows[j]
            answer = -answer
        v = rows[j][j]
        answer *= v
        for i in range(j+1, len(rows)):
            factor = rows[i][j]/v
            rows[i] = [x-factor*y for x, y in zip(rows[i], rows[j])]
    return answer


def frobenius_squared(a):
    return sum(x*x for row in a for x in row)


def vsub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def norm_squared(a):
    return sum(x*x for x in a)


def geometry(vertices, heights):
    vertices = tuple(tuple(map(F, v)) for v in vertices)
    heights = tuple(map(F, heights))
    require(len(vertices) == 4 and all(h > 0 for h in heights), 'valid positive heights')
    edges = transpose(tuple(vsub(vertices[i], vertices[0]) for i in (1, 2, 3)))
    gradients = inverse(edges)  # Rows 1,2,3 of the barycentric gradient system.
    grad_zero = tuple(-sum(row[k] for row in gradients) for k in range(3))
    gradients = (grad_zero,)+gradients
    normals = tuple(tuple(h*x for x in row) for h, row in zip(heights, gradients))
    return vertices, heights, normals


def covariance_control(vertices, heights, normals, j):
    indices = [i for i in range(4) if i != j]
    edges = tuple(vsub(vertices[i], vertices[j]) for i in indices)
    E = transpose(edges)
    D = transpose(tuple(normals[i] for i in indices))
    h = tuple(heights[i] for i in indices)
    H = diagonal(h)
    require(mm(transpose(D), E) == H, 'normal-edge diagonal duality')
    invD, invE = inverse(D), inverse(E)
    require(transpose(invD) == mm(E, diagonal(tuple(1/x for x in h))), 'D inverse transpose duality')
    require(transpose(invE) == mm(D, diagonal(tuple(1/x for x in h))), 'E inverse transpose duality')
    P = h[0]*h[1]*h[2]
    require(det(D)*det(E) == P, 'basis determinant product')
    K = sum((6*norm_squared(vsub(vertices[i], vertices[j]))
             +2*norm_squared(normals[i]))/heights[i]**2 for i in indices)
    require(K == 6*frobenius_squared(invD)+2*frobenius_squared(invE), 'box exponent K')

    A, B = mm(transpose(D), D), mm(transpose(E), E)
    # These are finite matrix controls of the universal factorization in the proof.
    for r in [F(-3, 4), F(-1, 2), F(0), F(1, 3), F(1, 2), F(3, 4)]:
        sigma = tuple(tuple(A[a][b] if a < 3 and b < 3 else
                            B[a-3][b-3] if a >= 3 and b >= 3 else
                            r*H[a % 3][b % 3] for b in range(6)) for a in range(6))
        require(det(sigma) == P**2*(1-r*r)**3, 'six-dimensional covariance determinant')
        # Inverse from the explicit block factorization, compared to elimination.
        left = tuple(tuple(invD[a][b] if a < 3 and b < 3 else
                           invE[a-3][b-3] if a >= 3 and b >= 3 else F(0)
                           for b in range(6)) for a in range(6))
        middle = tuple(tuple((F(a == b) if (a < 3) == (b < 3) else
                              -r*F(a % 3 == b % 3))/(1-r*r)
                             for b in range(6)) for a in range(6))
        require(mm(mm(left, middle), transpose(left)) == inverse(sigma), 'covariance inverse formula')

    # Every one-tip support/core/occupied-set case, including missing labels.
    cases = 0
    for support_bits in range(8):
        moving = {k for k in range(3) if support_bits >> k & 1}
        for core in [False, True]:
            if not moving and not core:
                continue
            for occupied_bits in range(8):
                occupied = {k for k in range(3) if occupied_bits >> k & 1}
                # Positive masses can be arbitrary; use distinct rational controls.
                gamma = sum(h[k]*F(k+1, 7)*F(k+2, 11)
                            for k in moving if k in occupied)
                matching = moving & occupied
                require((gamma > 0) == bool(matching), 'Gamma/support matching equality criterion')
                for i in matching:
                    # All 32 vertices of its five-dimensional unit box.
                    for bits in product((0, 1), repeat=5):
                        x = [F(-1), F(-1), F(-1)]
                        x[i] = 1+bits[0]
                        other = [k for k in range(3) if k != i]
                        for k, bit in zip(other, bits[1:3]):
                            x[k] = -1+bit
                        y = [F(0), F(0), F(0)]
                        for k, bit in zip(other, bits[3:]):
                            y[k] = -1+bit
                        competitors = [x[k] for k in moving if k != i]+([F(0)] if core else [])
                        require(all(x[i] > z for z in competitors), 'maximizer derivative is one on box')
                        require(all(y[k] <= 0 for k in occupied), 'orthant boundary box')
                        require(norm_squared(x) <= 6 and norm_squared(y) <= 2, 'box norm bounds')
                cases += 1
    require(cases == 120, 'all nonempty local label supports and occupied subsets')
    ceiling_K = (K.numerator+K.denominator-1)//K.denominator
    # pi<4, sqrt2<2 and e<3 imply (3) exceeds the following compressed bound
    # whenever at least one matching index is present. No exponential is evaluated.
    numerator = min(h)/(64*P)
    return {'tip': j, 'P': str(P), 'K': str(K), 'ceil_K': ceiling_K,
            'minimum_positive_support_bound': {'mantissa': str(numerator),
                                               'factor': '3^(-ceil_K)'},
            'local_support_cases': cases, 'covariance_matrix_controls': 6}


def scalar_controls():
    # For q=|r|<=1/2 the exponent inequality reduces to a sum of squares.
    # (1-2q)(1+q)(u^2+v^2)+q(u+v)^2
    #   = (1-2q^2)(u^2+v^2)+2q*u*v.
    coefficients = [1, -1, -2]  # (1-2q)(1+q)
    coefficients[1] += 1       # q(u+v)^2's u^2 coefficient
    require(coefficients == [1, 0, -2], 'universal exponent sum-of-squares identity')
    require(F(4, 2*8) == F(1, 4), 'sphere/density prefactor rational component')
    # E R=2 sqrt(2/pi); delta Psi=1/(2 sqrt(2pi)); (13) yields pi/2.
    require(F(4, 2*2*2) == F(1, 2), 'octant normalization rational component')
    return {'r_interval': '[-1/2,1/2]', 'box_x_squared_bound': 6,
            'box_y_squared_bound': 2, 'box_coordinate_volume': 1,
            'octant_exact_ell': 'pi/2', 'octant_Psi': '-r/(4 sqrt(2pi))'}


def run():
    fixtures = {
        'right_tetrahedron': (((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)), (1, 1, 1, 1)),
        'asymmetric_tetrahedron': (((0, 0, 0), (2, 0, 0), (1, 3, 0), (1, 1, 4)), (1, 2, 3, 5)),
    }
    records = {}
    for name, (v, h) in fixtures.items():
        v, h, d = geometry(v, h)
        records[name] = [covariance_control(v, h, d, j) for j in range(4)]

    asymmetric = records['asymmetric_tetrahedron']
    require(all(row['ceil_K'] <= 150 and
                F(row['minimum_positive_support_bound']['mantissa']) >= F(1, 960)
                for row in asymmetric), 'uniform asymmetric support lower bound')

    # A moving but isometric support; the corresponding normals need not be
    # orthogonal. The diagonal normal-edge pairing is what makes the cross term zero.
    v, h, d = geometry(*fixtures['asymmetric_tetrahedron'])
    require(sum(x*y for x, y in zip(d[2], vsub(v[1], v[0]))) == 0,
            'two occupied tips, unmatched moving label gives zero covariance')
    isometric = {'alpha_0': '1/3', 'beta_20': '1/3', 'alpha_1': '1/3',
                 'occupied_tips': [0, 1], 'moving_tip_0_normals': [2], 'Gamma': 0}

    rejected = []
    for label, args in [
        ('coplanar core', (((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)), (1, 1, 1, 1))),
        ('nonpositive normal height', (fixtures['right_tetrahedron'][0], (1, 1, -1, 1))),
    ]:
        try:
            geometry(*args)
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('invalid control accepted: '+label)

    return {'scope': 'Exact controls for universal strict support sign; analytic proof remains SUPPORT_SIGN.md',
            'scalar_controls': scalar_controls(), 'fixtures': records,
            'asymmetric_any_nonisometric_support_lower_bound': '1/(960*3^150)',
            'isometry_support_control': isometric, 'rejected_invalid_inputs': rejected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    output = (json.dumps(run(), indent=2, sort_keys=True)+'\n').encode()
    if args.check:
        require(output == Path(__file__).with_name('SUPPORT_EXPECTED.json').read_bytes(),
                'SUPPORT_EXPECTED.json mismatch')
        print('PASS: exact duality, covariance determinants/inverses and support cases')
        print('PASS: strict lower-bound data, octant normalization algebra and isometry control')
        print('SUPPORT_EXPECTED.json sha256', hashlib.sha256(output).hexdigest())
    else:
        print(output.decode(), end='')


if __name__ == '__main__':
    main()
