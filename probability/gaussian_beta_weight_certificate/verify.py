"""Reproduce the compact certificate and audit its algebraic normalization."""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
from math import comb, factorial
from collections import Counter
import json

from certificate import (HERE, M, Cell, coefficient_bounds, geometry, require,
                         run_certificate, exp_negative, sqrt_integer, DENOM)


def weighted_subset_coefficient(row, degree, k, kernel):
    total = F(0)
    for m in range(k+2, degree+3):
        average = sum(kernel(tuple(sorted(s))) for s in combinations(row, m))/comb(len(row), m)
        total += ((degree+1)*comb(degree, k)*(-1)**(m-k-2)*comb(degree-k, m-k-2)
                  * average / (m*(m-1)))
    return total


def algebra_controls():
    # Arbitrary rational symmetric kernels make the homogenization check
    # independent of Gaussian values and of their positivity.
    def kernel(row):
        return F((1+sum((i+1)**2 for i in row))**2, len(row)+1)
    weights = (F(1, 6), F(1, 3), F(1, 2))
    checked = 0
    for degree in range(6):
        size = degree+2
        moments = {}
        for m in range(2, size+1):
            total = F(0)
            for row in product(range(3), repeat=m):
                weight = F(1)
                for i in row:
                    weight *= weights[i]
                total += weight*kernel(tuple(sorted(row)))
            moments[m] = total
        for k in range(degree+1):
            direct = (degree+1)*comb(degree, k)*sum(
                (-1)**j*comb(degree-k, j)*moments[k+j+2]/((k+j+1)*(k+j+2))
                for j in range(degree-k+1))
            expanded = F(0)
            for row in combinations_with_replacement(range(3), size):
                multiplicity, weight = factorial(size), F(1)
                for i, count in Counter(row).items():
                    multiplicity //= factorial(count)
                    weight *= weights[i]**count
                expanded += multiplicity*weight*weighted_subset_coefficient(row, degree, k, kernel)
            require(direct == expanded, 'homogenization normalization')
            checked += 1
    # The edge-factor identity used to obtain the positive five-dimensional
    # integral. This is also proved algebraically for arbitrary degree.
    edge_checks = 0
    for degree in range(9):
        size = degree+2
        for k in range(degree+1):
            for r in range(k, degree+1):
                left = F((degree+1)*comb(degree, k)*comb(degree-k, r-k),
                         (r+2)*(r+1)*comb(size, r+2))
                require(left == F(comb(r, k), size), 'rooted coefficient normalization')
                edge_checks += 1
    return {'rational_homogenization_identities': checked, 'edge_factor_identities': edge_checks}


def boundary_controls():
    x, y = geometry()
    zero = Cell(x, x, F(0))
    require(all(z == (0, 0) for z in coefficient_bounds(zero, tuple(range(M)))),
            'isometry did not cancel exactly')
    rejected = 0
    for args in ((y, x, F(0)), (x, y, F(-1))):
        try:
            Cell(*args)
        except RuntimeError:
            rejected += 1
        else:
            raise RuntimeError('malformed cell accepted')
    require(exp_negative(0).lo == exp_negative(0).hi == 1, 'exponential at zero')
    root = sqrt_integer(2, 30)
    require(root.lo**2 <= 2 <= root.hi**2, 'square-root enclosure')
    # A direct Fraction assembly must agree at every endpoint with the
    # common-denominator path on these asymmetric, repeated and distinct rows.
    box = Cell(x, y, F(1, 100))
    endpoint_checks = 0
    for row in ((0, 0, 0, 4, 8, 12, 15), (0, 1, 4, 7, 8, 11, 15), tuple(range(7))):
        fast = coefficient_bounds(box, row)
        for k in range(6):
            exact = [F(0), F(0)]
            for m in range(k+2, M+1):
                scalar = F(6*comb(5, k)*(-1)**(m-k-2)*comb(5-k, m-k-2),
                           m*(m-1)*comb(M, m))
                for sub in combinations(row, m):
                    lo, hi = box.row(sub)
                    exact[0] += scalar*(lo if scalar >= 0 else hi)/box.scale
                    exact[1] += scalar*(hi if scalar >= 0 else lo)/box.scale
            require(exact == [F(v, DENOM*box.scale) for v in fast[k]], 'integer assembly mismatch')
            endpoint_checks += 2
    return {'rejected_malformed_cells': rejected, 'direct_fraction_endpoint_checks': endpoint_checks,
            'exact_isometry_control': True}


def verify():
    controls = {**algebra_controls(), **boundary_controls()}
    actual = run_certificate()
    expected = json.loads((HERE/'EXPECTED.json').read_text())
    require(actual == expected['certificate'], 'certificate differs from EXPECTED.json')
    require(controls == expected['controls'], 'controls differ from EXPECTED.json')
    print(json.dumps({'status': 'PASS', 'enclosed_signs': actual['enclosed_signs'],
                      'coefficient_stream_sha256': actual['coefficient_stream_sha256'],
                      'controls': controls}, indent=2, sort_keys=True))


if __name__ == '__main__':
    verify()
