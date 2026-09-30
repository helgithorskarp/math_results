#!/usr/bin/env python3
"""Exact author controls for unrestricted local displacement stability.

Actual author six-sendov-2, researcher. Standard library only. The analytic
support, continuum estimates and coverage are proved in PROOF.md; finite
matrix controls do not stand in for them. Polynomial/rational matrix
methods openly adapt the author's previous public checkers.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import argparse
import hashlib
import json

CHECKS = 0


def require(ok, message):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(message)


def p(values):
    a = list(map(F, values)) or [F(0)]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return tuple(a)


def add(a, b):
    return p([(a[i] if i < len(a) else 0) +
              (b[i] if i < len(b) else 0)
              for i in range(max(len(a), len(b)))])


def scale(a, c):
    return p([F(c)*v for v in a])


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    out = [F(0)]*(len(a)+len(b)-1)
    for i, v in enumerate(a):
        for j, w in enumerate(b):
            out[i+j] += v*w
    return p(out)


def power(a, n):
    if n < 0:
        raise ValueError('negative polynomial exponent')
    out = p([1])
    for _ in range(n):
        out = mul(out, a)
    return out


def diff(a):
    return p([i*a[i] for i in range(1, len(a))])


def value(a, x):
    out = F(0)
    for v in reversed(a):
        out = out*x+v
    return out


def bernstein(a, lo, hi):
    """Complete rational forward and inverse basis transformations."""
    require(lo < hi, 'nonempty scalar certificate interval')
    n = len(a)-1
    q = p([sum((a[i]*comb(i, k)*lo**(i-k)*(hi-lo)**k
                for i in range(k, n+1)), F(0)) for k in range(n+1)])
    bs = [sum((q[k]*F(comb(i, k), comb(n, k))
               for k in range(min(i, len(q)-1)+1)), F(0))
          for i in range(n+1)]
    inverse = p([comb(n, k)*sum((comb(k, i)*(-1)**(k-i)*bs[i]
                               for i in range(k+1)), F(0))
                 for k in range(n+1)])
    require(inverse == q, 'inverse Bernstein reconstruction')
    for b in bs:
        require(b > 0, 'strict continuous-domain Bernstein coefficient')
    return {'interval': [str(lo), str(hi)], 'degree': n,
            'power_coefficients': list(map(str, a)),
            'Bernstein_coefficients': list(map(str, bs)),
            'minimum': str(min(bs))}


Z, ONE = p([0]), p([1])
U = p([0, 1])
JN = p([2058, 21912, -15876, 19224, 3402])
JD = mul(p([3, 1]), power(p([1, 3]), 2))
T = sub(mul(diff(JN), JD), mul(JN, diff(JD)))


def j_at(u):
    return value(JN, u)/value(JD, u)


def jp_at(u):
    return value(T, u)/value(JD, u)**2


def tmul(a, b):
    """Polynomials in t with coefficients in Q[u], no CAS input."""
    out = [Z]*(len(a)+len(b)-1)
    for i, v in enumerate(a):
        for j, w in enumerate(b):
            out[i+j] = add(out[i+j], mul(v, w))
    while len(out) > 1 and out[-1] == Z:
        out.pop()
    return out


def td(a):
    return [scale(a[i], i) for i in range(1, len(a))]


def ident(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def mm(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def ma(a, b):
    return [[x+y for x, y in zip(r, s)] for r, s in zip(a, b)]


def ms(a, c):
    return [[v*c for v in row] for row in a]


def diag(v):
    return [[x if i == j else F(0) for j in range(len(v))]
            for i, x in enumerate(v)]


def quad(v, a, w):
    return sum((v[i]*a[i][j]*w[j] for i in range(len(v))
                for j in range(len(w))), F(0))


def matrix_controls(b, lam):
    """Independent Riesz-gradient check on all seven balanced tangent axes.

    Lagrange spectral projectors use the full rational 8 by 8 compression,
    rather than quotient symmetry to derive its derivative. The ambient
    zero projector includes e; its e component has zero w-weight and is
    fixed under every balanced perturbation.
    """
    n = 8
    i8 = ident(n)
    proj = [[F(i == j)-F(1, 8) for j in range(n)] for i in range(n)]
    theta = [F(1)]*3 + [F(-1)]*3 + [b, -b]
    a = mm(mm(proj, diag(theta)), proj)
    vals = [F(-1), -lam, F(0), lam, F(1)]
    ps = {}
    for z in vals:
        q = i8
        for v in vals:
            if v != z:
                q = ms(mm(q, ma(a, ms(i8, -v))), 1/(z-v))
        ps[z] = q
        require(mm(q, q) == q, 'Lagrange projector idempotence')
        require(mm(a, q) == ms(q, z), 'compression spectral equation')
        require(q == list(map(list, zip(*q))), 'orthogonal projector')
    total = [[F(0)]*n for _ in range(n)]
    for q in ps.values():
        total = ma(total, q)
    require(total == i8, 'complete spectral projector partition')
    require(quad(theta, ps[F(-1)], theta) == 0 and
            quad(theta, ps[F(1)], theta) == 0,
            'both inactive cluster weights vanish')
    active = [-lam, F(0), lam]
    weights = {z: quad(theta, ps[z], theta)/8 for z in vals}
    u = b*b
    require(weights[0] == 4*u/(1+3*u), 'active zero secular weight')
    require(weights[lam] == weights[-lam] ==
            3*(1-u)**2/(8*(1+3*u)), 'active pair secular weights')
    m2 = sum(v*v for v in theta)
    m4 = sum(v**4 for v in theta)
    psi = sum(weights[z]**2 for z in active)
    j = 122*m2+(224*m4-5760*psi)/m2
    require(j == j_at(u), 'definition-level scalar curve')
    require(sum(weights.values()) == m2/8, 'full weight partition')
    slope = (j_at(u)-u*jp_at(u))/3
    small = b*jp_at(u)
    gradient = [slope]*3+[-slope]*3+[small, -small]
    reduced = {}
    for z in active:
        reduced[z] = [[F(0)]*n for _ in range(n)]
        for v in vals:
            if v != z:
                reduced[z] = ma(reduced[z], ms(ps[v], 1/(z-v)))
    derivatives = []
    for axis in range(7):
        h = [F(int(k == axis)-int(k == 7)) for k in range(n)]
        ah = mm(mm(proj, diag(h)), proj)
        ds = {}
        for z in active:
            dpi = ma(mm(mm(reduced[z], ah), ps[z]),
                     mm(mm(ps[z], ah), reduced[z]))
            ds[z] = (2*quad(h, ps[z], theta)+quad(theta, dpi, theta))/8
        dpsi = 2*sum(weights[z]*ds[z] for z in active)
        dm2 = 2*sum(v*w for v, w in zip(theta, h))
        dm4 = 4*sum(v**3*w for v, w in zip(theta, h))
        # Keep the signed expression explicit; no numerical differences.
        du = (122*dm2+224*(dm4*m2-m4*dm2)/m2**2-
              5760*(dpsi*m2-psi*dm2)/m2**2)
        target = gradient[axis]-gradient[7]
        require(du == target, 'full balanced Riesz-gradient component')
        derivatives.append(str(du))
    return {'b': str(b), 'lambda': str(lam), 'j': str(j),
            'gradient_large': str(slope), 'gradient_small': str(small),
            'tangent_derivatives': derivatives,
            'weights': {str(z): str(weights[z]) for z in vals}}


def build():
    m2 = p([6, 2])
    m4 = p([6, 0, 2])
    pn = add(scale(power(p([1, -1]), 4), 9), scale(power(U, 2), 512))
    pd = scale(power(p([1, 3]), 2), 32)
    calculated_n = sub(mul(add(scale(mul(m2, m2), 122), scale(m4, 224)), pd),
                       scale(pn, 5760))
    calculated_d = mul(m2, pd)
    require(mul(calculated_n, JD) == mul(JN, calculated_d),
            'scalar objective from secular weights in Q[u]')
    h = tmul(tmul(tmul([scale(ONE, -1), Z, ONE],
                       [scale(ONE, -1), Z, ONE]),
                 [scale(ONE, -1), Z, ONE]), [scale(U, -1), Z, ONE])
    rhs = tmul(tmul([scale(ONE, -1), Z, ONE], [scale(ONE, -1), Z, ONE]),
               [Z, scale(p([1, 3]), -1), Z, p([4])])
    require(td(h) == [scale(v, 2) for v in rhs],
            'full characteristic factorization over Q[u]')
    require(T == p([26634, -231084, -907290, 376920, 971190, 224532, 30618]),
            'credited scalar critical polynomial')
    a_num = sub(sub(mul(JN, JD), mul(U, T)), scale(mul(JD, JD), 750))
    normal = bernstein(a_num, F(2, 25), F(9, 100))
    curvature = bernstein(scale(add(diff(T), p([90000])), -1), F(0), F(1, 4))
    require(all(v > 0 for v in JD), 'positive scalar denominator coefficients')
    require(value(JD, F(1, 4)) == F(637, 64) < 10,
            'credited scalar denominator bound')
    require(value(T, F(2, 25)) > 0 and value(T, F(9, 100)) < 0,
            'optimizer interval with sign change')
    require(j_at(F(1, 9)) == F(5472, 7) > 780,
            'credited optimizer lower comparison')
    require(F(2, 25) > F(1, 16) and F(9, 100) < F(1, 9),
            'local interval lies inside the spectral leaf interval')
    require(F(19, 64) > F(43, 80)**2 and F(1, 3) < F(47, 80)**2,
            'active roots within 1/40 of 9/16')
    require(F(1, 8)-F(1, 40) == F(1, 10), 'base active contour gap')
    require(F(1, 10)-F(1, 40) == F(3, 40), 'perturbed active gap')
    require(1-F(47, 80)-F(1, 8) > F(1, 8), 'inactive base gap')
    pi1 = F(1, 8)*F(40, 3)**2
    pi2 = F(1, 4)*F(40, 3)**3
    require(pi1 == F(200, 9) and pi2 == F(16000, 27),
            'resolvent first and second projection bounds')
    require(2+pi1 < 25 and 2+4*pi1+pi2 < 684,
            'active weight derivative bounds')
    require(2*(3*25**2+684) < 5200, 'active squared-weight Hessian')
    require(2*16**2/F(5**3)+16/F(5**2) < 5,
            'reciprocal moment second derivative')
    require(F(96, 5)+2*32+8*5 < 124, 'fourth-moment quotient Hessian')
    require(F(5200, 5)+2*50+5 == 1145, 'active quotient Hessian')
    hessian = 122*16+224*124+5760*1145
    require(hessian == 6624928 < 6700000, 'support Hessian')
    require(F(6700000, 2) == 3350000, 'support Taylor constant')
    require(250-F(3350000, 100000) >= 200, 'explicit inward strip')
    require(F(1, 100000) < F(1, 40), 'strip inside resolvent domain')
    require(F(100, 8)+1 < 14, 'inactive projection-vector derivative')
    contact = F(5760, 5)*2*14**4
    require(contact == 88510464 < 90000000, 'fourth-order support contact')
    require(F(3, 2)/200 <= F(1, 72) and F(25, 4)/450 == F(1, 72),
            'max-normalized distance bound')
    require(F(4, 5)*F(1, 72) == F(1, 90), 'unit-normalized orbit bound')
    controls = []
    for q in [F(1, 8), F(2, 15), F(3, 22), F(1, 7)]:
        b = 2*q/(1-3*q*q)
        lam = (1+3*q*q)/(2*(1-3*q*q))
        require(4*lam*lam == 1+3*b*b, 'rational active eigenvalue conic')
        require(F(1, 4) < b < F(1, 3), 'matrix control in spectral interval')
        controls.append(matrix_controls(b, lam))
    return {'agent': 'six-sendov-2', 'role': 'researcher',
            'normal_gradient_certificate': normal,
            'credited_curvature_reproduction': curvature,
            'characteristic_coefficients': [list(map(str, v)) for v in td(h)],
            'full_tangent_matrix_controls': controls,
            'support_constants': {'hessian': str(hessian), 'taylor': '3350000',
                                 'strip': '1/100000', 'linear_loss': '200',
                                 'contact_bound': str(contact),
                                 'max_distance_factor': '1/72',
                                 'unit_distance_factor': '1/90'},
            'exact_checks': CHECKS}


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True,
                                   separators=(',', ':')).encode()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--expected', type=Path,
                    default=Path(__file__).with_name('expected.json'))
    ap.add_argument('--write-expected', action='store_true')
    args = ap.parse_args()
    actual = build()
    if args.write_expected:
        args.expected.write_text(json.dumps(actual, indent=2)+'\n')
    else:
        expected = json.loads(args.expected.read_text())
        if expected != actual:
            raise ValueError('complete expected manifest mismatch')
    print(json.dumps({'status': 'PASS', 'agent': 'six-sendov-2',
                      'role': 'researcher', 'checks': CHECKS,
                      'normal_gradient_coefficients':
                        len(actual['normal_gradient_certificate']['Bernstein_coefficients']),
                      'full_tangent_controls': 28,
                      'record_sha256': digest(actual),
                      'manifest_match': not args.write_expected}, indent=2))


if __name__ == '__main__':
    main()
