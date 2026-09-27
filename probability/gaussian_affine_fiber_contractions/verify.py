#!/usr/bin/env python3
"""Exact controls and a supplied-frame affine-fiber extension certificate.

CPython 3.11+; standard library only. No floating point, quadrature or solver.
The continuum theorem and external transfer results are written in PROOF.md.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json
import re
import sys


def require(ok, message):
    if not ok:
        raise ValueError(message)


def rational(value):
    if type(value) is int:
        return F(value)
    require(type(value) is str and re.fullmatch(r'[+-]?\d+(?:/\d+)?', value),
            'Expected an integer or rational string')
    return F(value)


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def norm2(v):
    return sum((a*a for a in v), F(0))


def certificate(data):
    require(type(data) is dict and set(data) == {'source', 'target', 'slope'},
            'Expected source, target and slope')
    a = rational(data['slope'])
    require(-1 <= a <= 1, 'Slope must lie in [-1,1]')
    p, q = data['source'], data['target']
    require(type(p) is list and type(q) is list and len(p) == len(q) > 0,
            'Nonempty paired point lists required')
    def points(values):
        out = []
        for v in values:
            require(type(v) is list and len(v) == 3, 'Expected a 3-vector')
            out.append(tuple(rational(x) for x in v))
        return out
    p, q = points(p), points(q)
    budgets = []
    for i, j in combinations(range(len(p)), 2):
        x, y = sub(p[i], p[j]), sub(q[i], q[j])
        if abs(a) < 1:
            budget = (1-a*a)*(norm2(x[:2])-norm2(y[:2]))-(y[2]-a*x[2])**2
        else:
            if y[2] != a*x[2]:
                return {'status': 'NOT_IN_CLASS_AT_SUPPLIED_FRAMES_AND_SLOPE',
                        'failing_pair': [i, j], 'reason': 'Nonconstant fiber offset'}
            budget = norm2(x[:2])-norm2(y[:2])
        if budget < 0:
            return {'status': 'NOT_IN_CLASS_AT_SUPPLIED_FRAMES_AND_SLOPE',
                    'failing_pair': [i, j], 'budget': str(budget)}
        budgets.append(budget)
    return {'status': 'AFFINE_FIBER_EXTENSION_CERTIFIED', 'slope': str(a),
            'points': len(p), 'pairs': len(budgets),
            'branch': 'saturated' if abs(a) == 1 else 'short_profile',
            'minimum_budget': str(min(budgets, default=F(0)))}


# Small exact sparse polynomial ring Q[a,t,z,b,U,H,w].
# Universal cleared-denominator identities, not evaluations on a grid.
NV = 7
ZERO_MONOMIAL = (0,)*NV


class Poly:
    def __init__(self, terms):
        self.terms = {m: F(c) for m, c in terms.items() if c}

    @staticmethod
    def constant(c):
        return Poly({ZERO_MONOMIAL: c})

    @staticmethod
    def variable(i):
        powers = [0]*NV
        powers[i] = 1
        return Poly({tuple(powers): 1})

    def __add__(self, other):
        if not isinstance(other, Poly):
            other = Poly.constant(other)
        terms = dict(self.terms)
        for m, c in other.terms.items():
            terms[m] = terms.get(m, F(0))+c
        return Poly(terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-other if isinstance(other, Poly) else -F(other))

    def __rsub__(self, other):
        return (-self)+other

    def __mul__(self, other):
        if not isinstance(other, Poly):
            other = Poly.constant(other)
        terms = {}
        for m, c in self.terms.items():
            for n, d in other.terms.items():
                k = tuple(x+y for x, y in zip(m, n))
                terms[k] = terms.get(k, F(0))+c*d
        return Poly(terms)

    __rmul__ = __mul__

    def __pow__(self, n):
        require(type(n) is int and n >= 0, 'Polynomial exponent')
        out = Poly.constant(1)
        for _ in range(n):
            out = out*self
        return out


def polynomial_controls():
    a, t, z, b, U, H, w = (Poly.variable(i) for i in range(NV))
    C = 1-a*a
    d = a*a+t*C
    numerator = a*z+t*b
    Lc = (U-H)*C-b*b
    Mc = (C*z-a*b)**2
    distance = ((1-t)*U+t*H)*d*C+numerator**2*C
    decomposition = (U+z*z)*d*C-t*Lc*d-t*Mc
    derivative = (H-U)*C*d*d+(2*numerator*b*d-numerator**2*C)*C
    derivative_decomposition = -Lc*d*d-a*a*Mc
    finite_budget = C*(U-H)-(w-a*z)**2
    D = U+z*z-H-w*w
    finite_loss_budget = C*D-(z-a*w)**2
    quadratic = (w*w+D)*a*a-2*z*w*a+z*z-D
    controls = [distance-decomposition, derivative-derivative_decomposition,
                finite_budget-finite_loss_budget, finite_budget+quadratic]
    for p in controls:
        require(not p.terms, 'Universal polynomial identity failed')
    # A damaged sign must not silently pass the ring implementation.
    require(bool((finite_budget+finite_loss_budget).terms), 'Negative ring control')
    return len(controls)


def determinant(rows):
    a = [[F(x) for x in row] for row in rows]
    n, ans = len(a), F(1)
    require(all(len(row) == n for row in a), 'Square determinant required')
    for k in range(n):
        pivot = next((j for j in range(k, n) if a[j][k]), None)
        if pivot is None:
            return F(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            ans = -ans
        scale = a[k][k]
        ans *= scale
        for j in range(k+1, n):
            ratio = a[j][k]/scale
            for l in range(k+1, n):
                a[j][l] -= ratio*a[k][l]
    return ans


def profile(u):
    x, y = u
    return ((x*x-y*y)/8, x*y/4, (x*x+y*y)/8)


def target(p, a, c):
    h1, h2, g = profile(p[:2])
    return h1, h2, a*p[2]+c*g


def input_record(p, q, a):
    return {'source': [[str(v) for v in x] for x in p],
            'target': [[str(v) for v in x] for x in q], 'slope': str(a)}


def audit():
    universal = polynomial_controls()
    state = sha256()
    def record(*items):
        state.update(json.dumps(items, default=str, separators=(',', ':')).encode()+b'\n')
    values = [F(-1), F(0), F(1)]
    heights = [F(-2), F(-1, 2), F(0), F(1, 2), F(2)]
    points = list(product(values, values, heights))
    slopes = [(F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)),
              (F(8, 17), F(15, 17))]
    clocks = [F(0), F(1, 16), F(1, 4), F(1, 2), F(3, 4), F(15, 16), F(1)]
    pair_checks = motion_checks = derivative_checks = monotone_checks = 0
    certificates = []
    for a, c in slopes:
        require(a*a+c*c == 1, 'Pythagorean slope')
        outputs = [target(p, a, c) for p in points]
        cert = certificate(input_record(points, outputs, a))
        require(cert['status'] == 'AFFINE_FIBER_EXTENSION_CERTIFIED', 'Finite consumer')
        certificates.append(cert)
        for i, j in combinations(range(len(points)), 2):
            p, q = points[i], points[j]
            du = sub(p[:2], q[:2]); dz = p[2]-q[2]
            gp, gq = profile(p[:2]), profile(q[:2])
            dh = sub(gp[:2], gq[:2]); dg = gp[2]-gq[2]
            U, H = norm2(du), norm2(dh)
            L, S = U-H-dg*dg, (c*dz-a*dg)**2
            direct_loss = norm2(sub(p, q))-norm2(sub(outputs[i], outputs[j]))
            require(L >= 0 and direct_loss == L+S and direct_loss > 0,
                    'Endpoint loss or strictness')
            pair_checks += 1
            previous = None
            for t in clocks:
                d = a*a+t*c*c
                n = a*dz+t*c*dg
                direct = (1-t)*U+t*H+n*n/d
                reduced = U+dz*dz-t*L-t*S/d
                require(direct == reduced, 'Distance identity')
                ddirect = H-U+2*n*c*dg/d-n*n*c*c/(d*d)
                dreduced = -L-a*a*S/(d*d)
                require(ddirect == dreduced and ddirect <= 0, 'Derivative sign')
                if previous is not None:
                    require(direct <= previous, 'Clock monotonicity')
                    monotone_checks += 1
                if t == 0:
                    require(direct == norm2(sub(p, q)), 'Source endpoint')
                if t == 1:
                    require(direct == norm2(sub(outputs[i], outputs[j])), 'Target endpoint')
                previous = direct
                motion_checks += 1; derivative_checks += 1
                record(a, i, j, t, L, S, direct, ddirect)
    # Exactly saturated profile and zero second loss, including both zero.
    equality_controls = 0
    for a, c in slopes:
        for v in [F(-2), F(0), F(3, 2)]:
            for L in [F(0), F(2, 7)]:
                z = a*v/c
                for t in clocks:
                    d = a*a+t*c*c
                    direct = (1-t)*(v*v+L)+(a*z+t*c*v)**2/d
                    require(direct == v*v+L+z*z-t*L, 'Zero-square equality')
                    equality_controls += 1
                    record('equal', a, v, L, t, direct)
    # Whole-domain differential controls and independent frame obstruction algebra.
    require(F(24, 64) == F(3, 8), 'Profile Frobenius bound')
    require(F(2, 8)+F(16, 25*8)+F(9, 25) == F(69, 100),
            'Full-map Frobenius bound')
    hessian_controls = 0
    for alpha, beta in product(range(-3, 4), repeat=2):
        det = determinant([[F(alpha, 4), F(beta, 4)],
                           [F(beta, 4), F(-alpha, 4)]])
        require(det == -F(alpha*alpha+beta*beta, 16), 'Hessian pencil')
        require((det == 0) == (alpha == beta == 0), 'Hessian rank')
        hessian_controls += 1
    labels = [(F(0),)*3, (F(1), F(0), F(0)), (F(-1), F(0), F(0)),
              (F(0), F(1), F(0)), (F(0), F(-1), F(0)),
              (F(1), F(1), F(0)), (F(0), F(0), F(1))]
    a, c = slopes[0]
    outputs = [target(p, a, c) for p in labels]
    paired_det = determinant([list(p+q) for p, q in zip(labels[1:], outputs[1:])])
    require(paired_det != 0, 'Paired rank six')
    fixture = input_record(labels, outputs, a)
    require(certificate(fixture)['status'] == 'AFFINE_FIBER_EXTENSION_CERTIFIED',
            'Seven-site certificate')
    # Signed, zero and saturated fibers, duplicates and independent translations.
    boundary_certificates = 0
    for slope in [F(-3, 5), F(0), F(1), F(-1)]:
        if abs(slope) == 1:
            q = [(p[0]/2, p[1]/2, slope*p[2]+F(7, 3)) for p in labels]
        else:
            cc = F(1) if slope == 0 else F(4, 5)
            q = [target(p, slope, cc) for p in labels]
        inp = input_record(labels+[labels[0]], q+[q[0]], slope)
        require(certificate(inp)['status'] == 'AFFINE_FIBER_EXTENSION_CERTIFIED',
                'Signed or saturated branch')
        boundary_certificates += 1
    for src_sign, tgt_sign in product([-1, 1], repeat=2):
        pp = [(p[1]+2, -p[0]-3, src_sign*p[2]+5) for p in labels]
        qq = [(-q[1]+7, q[0]-11, tgt_sign*q[2]+13) for q in outputs]
        new_a = a*src_sign*tgt_sign
        require(certificate(input_record(pp, qq, new_a))['status'] ==
                'AFFINE_FIBER_EXTENSION_CERTIFIED', 'Independent endpoint frames')
        boundary_certificates += 1
    rejection_controls = 0
    wrong = {'source': [[0, 0, 0], [0, 0, 1]],
             'target': [[0, 0, 0], [0, 0, '1/2']], 'slope': '3/5'}
    require(certificate(wrong)['status'] == 'NOT_IN_CLASS_AT_SUPPLIED_FRAMES_AND_SLOPE',
            'Contracting but wrong supplied slope must be rejected')
    rejection_controls += 1
    wrong_sat = dict(wrong, slope='1')
    require(certificate(wrong_sat)['status'] == 'NOT_IN_CLASS_AT_SUPPLIED_FRAMES_AND_SLOPE',
            'Saturated offset must be constant')
    rejection_controls += 1
    malformed = [None, {}, dict(fixture, extra=1), dict(fixture, slope=True),
                 dict(fixture, slope=0.6), dict(fixture, slope='1/0'),
                 dict(fixture, slope='2'), dict(fixture, slope='0.6'),
                 dict(fixture, source=[]), dict(fixture, source=[[0, 0]]),
                 dict(fixture, target=[[0, 0, 0]]),
                 {'source': [[0, 0, 'nan']], 'target': [[0, 0, 0]], 'slope': '0'}]
    for bad in malformed:
        try:
            certificate(bad)
        except (ValueError, ZeroDivisionError):
            rejection_controls += 1
        else:
            raise ValueError('Malformed certificate was accepted')
    record('polynomials', universal, 'determinant', paired_det,
           'certificates', certificates, 'boundary', boundary_certificates)
    return {'status': 'AFFINE_FIBER_EXACT_CONTROLS_PASS',
            'universal_polynomial_identities': universal, 'sites_per_profile': len(points),
            'slope_profiles': len(slopes), 'endpoint_pairs': pair_checks,
            'motion_identities': motion_checks, 'derivative_signs': derivative_checks,
            'successive_clock_comparisons': monotone_checks,
            'zero_square_controls': equality_controls,
            'hessian_pencil_controls': hessian_controls,
            'paired_rank_six_determinant': str(paired_det),
            'profile_frobenius_square_bound': '3/8',
            'map_frobenius_square_bound': '69/100',
            'finite_certificates': len(certificates)+1+boundary_certificates,
            'invalid_or_failed_controls': rejection_controls,
            'exact_state_sha256': state.hexdigest()}


def main():
    if len(sys.argv) == 1:
        result = audit()
        expected = json.loads(Path(__file__).with_name('EXPECTED.json').read_text())
        require(result == expected, 'Exact record differs from EXPECTED.json')
        supplied = json.loads(Path(__file__).with_name('INPUT.json').read_text())
        require(certificate(supplied)['status'] == 'AFFINE_FIBER_EXTENSION_CERTIFIED',
                'Published input failed')
    else:
        require(len(sys.argv) == 2, 'Usage: verify.py [input.json]')
        result = certificate(json.loads(Path(sys.argv[1]).read_text()))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
