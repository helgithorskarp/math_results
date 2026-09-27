"""Exact algebra for PROOF.md, not a Gaussian-integration certificate.

Standard-library Python 3.11+. Universal quantification still uses the
written exchangeability/Jensen proof. All finite comparisons use Fraction;
explicit exceptions, not asserts, preserve checks under python -O.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import product, combinations
import json
from pathlib import Path

SIGNS = list(product((-1, 1), repeat=2))
U = [(F(1), F(0), F(0)), (F(3, 5), F(4, 5), F(0)),
     (F(1, 3), F(2, 3), F(2, 3))]


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def scale(a, x):
    return tuple(a*t for t in x)


def add(x, y):
    return tuple(a+b for a, b in zip(x, y))


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def det(matrix):
    a = [list(map(F, row)) for row in matrix]
    value = F(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            a[pivot], a[j] = a[j], a[pivot]
            value = -value
        value *= a[j][j]
        for i in range(j+1, len(a)):
            factor = a[i][j]/a[j][j]
            a[i] = [x-factor*y for x, y in zip(a[i], a[j])]
    return value


def fold(a):
    return a if abs(a) <= 1 else (2 if a > 0 else -2)-a


def triangle(a):
    s = 1 if a >= 0 else -1
    r = abs(a) % 2
    return s*min(r, 2-r)


def certificate(a, b, ha, hb):
    D, E, d, e = a-b, a+b, ha-hb, ha+hb
    require(abs(d) <= abs(D) and abs(e) <= abs(E), 'coefficient expands')
    rho = d/D if D else F(0)
    tau = e/E if E else F(0)
    C = [[(1+i*k*rho)*(1+j*l*tau)/4 for k, l in SIGNS] for i, j in SIGNS]
    # Coerce the entirely degenerate integer expression as well.
    C = [[F(v) for v in row] for row in C]
    require(all(v >= 0 for row in C for v in row), 'negative probability')
    require(all(sum(row) == 1 for row in C), 'row is not stochastic')
    require(all(sum(row[k] for row in C) == 1 for k in range(4)), 'column is not stochastic')
    return C, (D, E, d, e)


def check_barycenters(C, coeff, u, v):
    D, E, d, e = coeff
    p, q = scale(F(1, 2), add(u, v)), scale(F(1, 2), sub(u, v))
    src = [add(scale(i*D, p), scale(j*E, q)) for i, j in SIGNS]
    dst = [add(scale(i*d, p), scale(j*e, q)) for i, j in SIGNS]
    for row, target in zip(C, dst):
        barycenter = tuple(sum(row[k]*src[k][axis] for k in range(4)) for axis in range(3))
        require(barycenter == target, 'wrong barycenter')
    return 4


def fixture():
    zero = (F(0),)*3
    x = [zero]+U+[scale(F(4), u) for u in U]
    y = [zero]+U+[scale(F(-2), u) for u in U]
    weights = list(map(F, ['1/5', '3/20', '1/10', '1/20', '1/4', '1/6', '1/12']))
    require(sum(weights) == 1 and min(weights) == F(1, 20), 'wrong fixture weights')
    require(all(dot(u, u) == 1 for u in U), 'nonunit fixture direction')
    require(det(U) == F(8, 15), 'wrong directional determinant')
    paired = det([list(a)+list(b) for a, b in zip(x[1:], y[1:])])
    require(paired == F(-1536, 25), 'rank-six determinant failed')
    losses = [dot(sub(x[i], x[j]), sub(x[i], x[j]))-
              dot(sub(y[i], y[j]), sub(y[i], y[j])) for i, j in combinations(range(7), 2)]
    require(min(losses) == 0 and min(v for v in losses if v > 0) == F(16, 5), 'fixture contraction failed')
    require(sum(v > 0 for v in losses) == 12, 'wrong strict-pair count')
    # Check the full norm-loss identity independently of its endpoint form.
    radii = [F(0)]+[F(1)]*3+[F(4)]*3
    directions = [U[0]]+U+U
    for i, j in combinations(range(7), 2):
        a, b = radii[i], radii[j]
        ha, hb, c = fold(a), fold(b), dot(directions[i], directions[j])
        decomposed = (1+c)*((a-b)**2-(ha-hb)**2)/2+(1-c)*((a+b)**2-(ha+hb)**2)/2
        direct = dot(sub(x[i], x[j]), sub(x[i], x[j]))-dot(sub(y[i], y[j]), sub(y[i], y[j]))
        require(decomposed == direct and decomposed >= 0, 'distance identity failed')
    return x, y, weights, losses, paired


def direct_law_checks(x, y, weights):
    # Reconstruct independent-copy differences from the endpoint laws,
    # without the four-point certificate or its barycenter formula.
    directions = U+[(F(1), F(2), F(-3)), (F(-2), F(1), F(4))]
    count = 0
    for t in directions:
        laws = []
        for cloud in (x, y):
            hist = {}
            for i, j in product(range(7), repeat=2):
                val = dot(t, sub(cloud[i], cloud[j]))
                hist[val] = hist.get(val, F(0))+weights[i]*weights[j]
            require(sum(hist.values()) == 1 and sum(v*w for v, w in hist.items()) == 0, 'difference law normalization failed')
            laws.append(hist)
        for level in sorted(set(laws[0]) | set(laws[1])):
            hinges = [sum(w*max(F(0), v-level) for v, w in law.items()) for law in laws]
            require(hinges[0] >= hinges[1], 'direct convex-order control failed')
            count += 1
    return count


def rejected(fn):
    try:
        fn()
    except ArithmeticError:
        return True
    raise ArithmeticError('damaged control was accepted')


def run():
    scalars = list(map(F, ['-4', '-2', '-1', '-1/2', '0', '1/2', '1', '2', '4']))
    profiles = [('zero', lambda a: F(0)), ('identity', lambda a: a),
                ('reflection', lambda a: -a), ('clip', lambda a: min(F(1), max(F(-1), a))),
                ('signed_fold', fold), ('triangle', triangle)]
    digest = sha256(); certificates = identities = 0; degeneracies = [0, 0]
    for name, h in profiles:
        for a, b in product(scalars, repeat=2):
            C, coeff = certificate(a, b, h(a), h(b))
            degeneracies[0] += coeff[0] == 0
            degeneracies[1] += coeff[1] == 0
            for u, v in product(U, repeat=2):
                identities += check_barycenters(C, coeff, u, v)
            digest.update(json.dumps([name, str(a), str(b), [[str(v) for v in row] for row in C]], separators=(',', ':')).encode())
            certificates += 1
    x, y, weights, losses, paired = fixture()
    direct_checks = direct_law_checks(x, y, weights)
    C, coeff = certificate(F(1), F(4), F(1), F(-2))
    damaged = [row[:] for row in C]; damaged[0][0] += F(1, 7)
    controls = {
        'expansive_profile_rejected': rejected(lambda: certificate(F(1), F(2), F(2), F(4))),
        'nonodd_zero_shift_rejected': rejected(lambda: certificate(F(0), F(0), F(1), F(1))),
        'damaged_barycenter_rejected': rejected(lambda: check_barycenters(damaged, coeff, U[0], U[1])),
    }
    # Independence counter-control: source projection is constant, target is not.
    xx = [U[0], (F(1), F(12, 5), F(0))]
    yy = [U[0], (F(-3, 13), F(-36, 65), F(0))]
    loss = dot(sub(xx[0], xx[1]), sub(xx[0], xx[1]))-dot(sub(yy[0], yy[1]), sub(yy[0], yy[1]))
    var_x = (xx[0][0]-xx[1][0])**2/4
    var_y = (yy[0][0]-yy[1][0])**2/4
    require(loss == F(256, 65) and var_x == 0 and var_y == F(64, 169), 'independence control failed')
    # Exact rational coefficient in the analytic all-lambda margin.
    margin = F(1, 2)*F(1, 5)*F(16-4, 2)*F(1, 3)
    require(margin == F(1, 5), 'strict-margin coefficient failed')
    return {'status': 'SIGNED_RADIAL_TAIL_EXCLUSION_EXACT_PASS',
            'four_point_certificates': certificates, 'barycenter_identities': identities,
            'zero_difference_and_sum_cases': degeneracies,
            'certificate_sha256': digest.hexdigest(), 'direct_finite_law_hinge_checks': direct_checks,
            'fixture': {'paired_determinant': str(paired), 'pairs': len(losses),
                        'strict_pairs': sum(v > 0 for v in losses),
                        'minimum_strict_loss': str(min(v for v in losses if v > 0)),
                        'weights': list(map(str, weights)),
                        'source': [list(map(str, v)) for v in x],
                        'target': [list(map(str, v)) for v in y]},
            'strict_spherical_margin': 'lambda^2*exp(-8*lambda)/5',
            'independence_counter_control': {'pair_loss': str(loss), 'source_projection_variance': str(var_x),
                'target_projection_variance': str(var_y), 'is_gaussian_counterexample': False},
            'damaged_controls': controls,
            'trust_boundary': 'Exact finite algebra; universal proof uses written exchangeability/Jensen. No full Gaussian sign.'}


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check', action='store_true')
    group.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    result = run()
    expected = Path(__file__).with_name('EXPECTED.json')
    if args.write_expected:
        expected.write_text(json.dumps(result, indent=2)+'\n')
    else:
        require(result == json.loads(expected.read_text()), 'expected record mismatch')
    print(json.dumps({k: result[k] for k in ['status', 'four_point_certificates', 'barycenter_identities',
          'certificate_sha256', 'direct_finite_law_hinge_checks', 'damaged_controls']}, indent=2))


if __name__ == '__main__':
    main()
