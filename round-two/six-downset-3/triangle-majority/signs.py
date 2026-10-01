"""Regenerate the infinite coefficient certificates, using only Q[u] arithmetic."""
from fractions import Fraction as F
from itertools import permutations
from poly import R, polynomial, mul, add, neg, exact_divide
from model import formula, model
from exact import require, digest


def determinant(matrix):
    n = len(matrix)
    result = polynomial(0)
    for p in permutations(range(n)):
        term = polynomial(1)
        for i, j in enumerate(p):
            term = mul(term, matrix[i][j])
        parity = sum(p[i] > p[j] for i in range(n) for j in range(i+1, n)) % 2
        result = add(result, neg(term) if parity else term)
    return result


def lower_sign(p):
    require(p and all(isinstance(c, (int, F)) for c in p), 'inexact determinant coefficients')
    require(p[0] > 0 and all(c >= 0 for c in p), 'lower determinant is not coefficient-positive')


def regenerate():
    q = R((4, 1))
    data, result = model(q, formula(q)), []
    common = 2*q*(q-1)*(q-2)*(q-3)*(3*q+5)
    common.coefficients_positive()
    for sector in data:
        degree, levels, g = sector['degree'], sector['levels'], sector['lower']
        anchors = [(1, 0), (2, 0)] if degree == (0, 0) else [(1, 0)] if degree == (1, 0) else []
        keep = [i for i, level in enumerate(levels) if level not in anchors]
        if sector['kernel']:
            anchor_positions = [levels.index(level) for level in anchors]
            minor = [[polynomial(v[i]) for i in anchor_positions] for v in sector['kernel']]
            require(determinant(minor) != (0,), 'kernel anchor minor is singular')
        scaled = [[exact_divide(mul(common.n, g[i][j].n), mul(common.d, g[i][j].d))
                   for j in keep] for i in keep]
        for k in range(1, len(keep)+1):
            p = determinant([row[:k] for row in scaled[:k]])
            lower_sign(p)
            result.append({'kind': 'lower_leading_minor', 'sector': list(degree), 'size': k,
                           'scaled_by': '2q(q-1)(q-2)(q-3)(3q+5)', 'coefficients': [str(c) for c in p]})
        if degree == (0, 0):
            v = [F(4, 3)/q if a == 0 else 2+1/q if a == 3 else R(1) for a, b in levels]
        elif degree == (0, 1):
            v = [R(1) if a == 0 else R(F(9, 10)) for a, b in levels]
        else:
            v = [R(1)]*len(levels)
        for weight in v:
            weight.coefficients_positive()
        for i in range(len(levels)):
            absolute = R(0)
            for j in range(len(levels)):
                entry = g[i][j]/sector['norms'][i]
                try:
                    entry.coefficients_positive(strict=False)
                except ValueError:
                    entry = -entry
                    entry.coefficients_positive(strict=False)
                absolute += entry*v[j]/v[i]
            margin = 2*(3*q+4)-absolute
            margin.coefficients_positive(strict=False)
            result.append({'kind': 'weighted_Gershgorin_margin', 'sector': list(degree), 'row': i,
                           **margin.record()})
    trivial = data[0]
    levels, norms = trivial['levels'], trivial['norms']
    a, d = [a for a, b in levels], [int(a >= 2) for a, b in levels]
    gram = [[sum(norms[k]*x[k]*y[k] for k in range(len(levels))) for y in [a, d]] for x in [a, d]]
    expected = [[15*(q+1)+9, 6*(q+1)+3], [6*(q+1)+3, 3*(q+1)+1]]
    require(gram == expected, 'projection Gram identity differs')
    residual = [R(1) if c == 0 else 1/(3*q+5) if c < 3 else -3*(q+1)/(3*q+5)
                for c, b in levels]
    require(all(sum(norms[i]*residual[i]*v[i] for i in range(len(levels))) == 0 for v in [a, d]),
            'projected constant is not orthogonal to the kernel')
    require(all(sum(trivial['lower'][i]) == norms[i]*residual[i]/2 for i in range(len(levels))),
            'controlled constant-direction identity differs')
    require(len(result) == 33, 'infinite sign coverage differs')
    return {'scope': 'q=4+u,u>=0', 'signs': result, 'sign_count': len(result),
            'lower_determinants': 15, 'Gershgorin_margins': 18,
            'coefficient_count': sum(len(r['coefficients']) if 'coefficients' in r else
                                     len(r['numerator'])+len(r['denominator']) for r in result),
            'signs_sha256': digest(result), 'kernel_projection_C1_identities': True}


def compare(expected, actual):
    require(expected == actual, 'stored infinite certificate differs from exact regeneration')


if __name__ == '__main__':
    import json
    print(json.dumps(regenerate(), indent=2))
