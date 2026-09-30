#!/usr/bin/env python3
"""Exact algebra controls for the written full-motion quartic reduction.

No author imports, floating arithmetic, eigenvalue solver or external input.
Finite profiles check algebra; the universal analytic bridges are in PROOF.md.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
from math import factorial, isqrt
from pathlib import Path
import json
import sys

ORDER = 4


@dataclass(frozen=True)
class G:
    re: Q = Q(0)
    im: Q = Q(0)

    def __add__(self, b):
        b = gaussian(b)
        return G(self.re + b.re, self.im + b.im)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.re, -self.im)

    def __sub__(self, b):
        return self + -gaussian(b)

    def __rsub__(self, b):
        return gaussian(b) + -self

    def __mul__(self, b):
        b = gaussian(b)
        return G(self.re * b.re - self.im * b.im,
                 self.re * b.im + self.im * b.re)

    __rmul__ = __mul__

    def __truediv__(self, b):
        b = gaussian(b)
        d = b.re * b.re + b.im * b.im
        if not d:
            raise ZeroDivisionError("Gaussian division by zero")
        return self * G(b.re / d, -b.im / d)

    def conjugate(self):
        return G(self.re, -self.im)


def gaussian(x):
    return x if isinstance(x, G) else G(Q(x))


def constant(x):
    return [gaussian(x)] + [G()] * ORDER


def series(*coefficients):
    if len(coefficients) > ORDER + 1:
        raise ValueError("Too many coefficients")
    return [gaussian(x) for x in coefficients] + [G()] * (ORDER + 1 - len(coefficients))


def add(a, b):
    return [x + y for x, y in zip(a, b)]


def scale(a, x):
    return [y * x for y in a]


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    return [sum((a[k] * b[n-k] for k in range(n+1)), G())
            for n in range(ORDER+1)]


def inverse(a):
    b = [G(1) / a[0]]
    for n in range(1, ORDER+1):
        b.append(-sum((a[k] * b[n-k] for k in range(1, n+1)), G()) / a[0])
    return b


def square_root(a):
    if a[0].im or a[0].re <= 0:
        raise ValueError("Positive rational constant required")
    p, q = a[0].re.numerator, a[0].re.denominator
    ip, iq = isqrt(p), isqrt(q)
    if ip * ip != p or iq * iq != q:
        raise ValueError("Constant square root is not rational")
    b = [G(Q(ip, iq))]
    for n in range(1, ORDER+1):
        b.append((a[n] - sum((b[k]*b[n-k] for k in range(1, n)), G())) / (2*b[0]))
    return b


def modulus(a):
    return square_root(mul(a, [x.conjugate() for x in a]))


def exponential_i(phi):
    iphi, power, total = scale(phi, G(0, 1)), constant(1), constant(0)
    for k in range(ORDER+1):
        total = add(total, scale(power, Q(1, factorial(k))))
        power = mul(power, iphi)
    return total


def root_and_reciprocal(phi, tau):
    radial_exp = mul(sub(constant(1), tau), exponential_i(phi))
    return scale(radial_exp, -1), inverse(add(constant(A), radial_exp))


A, V, F0 = Q(5, 8), Q(8, 13), Q(128, 13)
RADIAL, MEAN = Q(128, 169), Q(40, 2197)
P8, CMAX, CMIN = Q(10985, 33554432), Q(560235, 8388608), Q(164775, 8388608)
checks = []
records = []


def check(label, actual, expected):
    if actual != expected:
        raise RuntimeError(f"{label}: {actual!r} != {expected!r}")
    checks.append(label)


def reject(label, actual, wrong):
    if actual == wrong:
        raise RuntimeError(f"Corruption survived: {label}")


def encode(x):
    if isinstance(x, G):
        return [encode(x.re), encode(x.im)]
    if isinstance(x, Q):
        return [x.numerator, x.denominator]
    if isinstance(x, list):
        return [encode(y) for y in x]
    return x


def two_block(r, phi_a, phi_b, tau_a, tau_b, label):
    s = 8-r
    za, ua = root_and_reciprocal(phi_a, tau_a)
    zb, ub = root_and_reciprocal(phi_b, tau_b)
    trace = add(scale(ua, r+1), scale(ub, s+1))
    determinant = scale(mul(ua, ub), 9)
    discriminant = sub(mul(trace, trace), scale(determinant, 4))
    root_disc = square_root(discriminant)
    near = scale(sub(trace, root_disc), Q(1, 2))
    far = scale(add(trace, root_disc), Q(1, 2))
    for which, q in [('near', near), ('far', far)]:
        check(label+':quadratic:'+which,
              add(sub(mul(q, q), mul(trace, q)), determinant), constant(0))
    # Different derivation: differentiate (z-a)(z-za)^r(z-zb)^s,
    # then substitute z=a-1/q in its residual quadratic.
    z_linear = scale(add(add(scale(za, s+1), scale(zb, r+1)), constant(8*A)), -1)
    z_constant = add(mul(za, zb), scale(add(scale(zb, r), scale(za, s)), A))
    q2 = add(add(constant(9*A*A), scale(z_linear, A)), z_constant)
    q1 = sub(scale(z_linear, -1), constant(18*A))
    direct_trace = scale(mul(q1, inverse(q2)), -1)
    direct_determinant = scale(inverse(q2), 9)
    check(label+':direct-derivative-trace', direct_trace, trace)
    check(label+':direct-derivative-determinant', direct_determinant, determinant)
    total = add(add(scale(modulus(ua), r-1), scale(modulus(ub), s-1)),
                add(modulus(near), modulus(far)))
    gap = sub(total, constant(F0))
    ea, eb = sub(ua, constant(V)), sub(ub, constant(V))
    energy = add(scale(mul(ea, [x.conjugate() for x in ea]), r),
                 scale(mul(eb, [x.conjugate() for x in eb]), s))
    records.append([label, encode(gap), encode(energy)])
    return gap, energy


def matrix_mul(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(8)), Q(0))
             for j in range(8)] for i in range(8)]


def run():
    c2 = V*V/2 - V**3
    gamma = Q(3, 4)
    check('balanced-quadratic-cancellation', 2*c2 + gamma*V**3/2, Q(0))
    check('inward-constant', 2*V*V, RADIAL)
    check('mean-constant', Q(10, 128)*V**3, MEAN)
    check('far-mean-part', 9*V**3/128, Q(36, 2197))
    check('near-mean-part', V**3/128, Q(4, 2197))
    check('angular-max', 204*P8, CMAX)
    check('angular-min', 60*P8, CMIN)

    projection = [[Q(int(i == j))-Q(1, 8) for j in range(8)] for i in range(8)]
    for k in range(12):
        slopes = [Q(((i+1)*(k+3)) % 13 - 6, k+1) for i in range(8)]
        dproj = [[slopes[i]*projection[i][j] for j in range(8)] for i in range(8)]
        product = matrix_mul(dproj, dproj)
        mu2, mu1 = sum(x*x for x in slopes), sum(slopes)
        check(f'projection:{k}', sum(product[i][i] for i in range(8)),
              gamma*mu2 + mu1*mu1/64)

    quartic_profiles = 0
    second_profiles = 0
    controls = []
    for r in range(1, 8):
        s = 8-r
        mu2 = Q(8*r*s)
        x_moment = Q(64-3*r*s, 8*r*s)
        coefficient = P8*(224*x_moment+32)
        for k in range(6):
            beta_a, beta_b = Q(k-2, 3), Q(3-k, 5)
            alpha_a, alpha_b = Q(2-k, 7), Q(k+1, 11)
            radial_a, radial_b = Q(k, 4), Q(5-k, 6)
            label = f'quartic:r{r}:k{k}'
            gap, energy = two_block(r, series(0, s, beta_a, alpha_a),
                                   series(0, -r, beta_b, alpha_b),
                                   series(0, 0, 0, 0, radial_a),
                                   series(0, 0, 0, 0, radial_b), label)
            inward = Q(r)*radial_a + Q(s)*radial_b
            mean = Q(r)*beta_a + Q(s)*beta_b
            expected = RADIAL*inward + MEAN*mean*mean - coefficient*V**8*mu2*mu2
            for order in range(4):
                check(label+f':gap-order{order}', gap[order], G())
            check(label+':gap-order4', gap[4], G(expected))
            check(label+':energy-order2', energy[2], G(V**4*mu2))
            check(label+':energy-squared-order4', mul(energy, energy)[4], G(V**8*mu2*mu2))
            controls.append((r, coefficient, inward, mean, expected))
            quartic_profiles += 1
        for k in range(8):
            sa, sb = Q(k-3, 2), Q(4-k, 3)
            ra, rb = Q(k, 9), Q(7-k, 10)
            label = f'second:r{r}:k{k}'
            gap, energy = two_block(r, series(0, sa), series(0, sb),
                                   series(0, 0, ra), series(0, 0, rb), label)
            expected = RADIAL*(r*ra+s*rb)+MEAN*(r*sa+s*sb)**2
            check(label+':gap-order2', gap[2], G(expected))
            check(label+':gap-order1', gap[1], G())
            second_profiles += 1
    # Inward first-order and pure nonlinear mean controls, with angles zero.
    gap, _ = two_block(1, series(), series(), series(0, Q(1, 3)),
                       series(0, Q(2, 5)), 'linear-inward')
    check('linear-inward-cost', gap[1], G(RADIAL*(Q(1, 3)+7*Q(2, 5))))
    # Nontrivial defects: these mutations exercise distinct cost/coefficient terms.
    r, coeff, inward, mean, observed = controls[0]
    scale_energy = V**8*Q(8*r*(8-r))**2
    reject('omit-inward-cost', observed, MEAN*mean*mean-coeff*scale_energy)
    reject('omit-mean-cost', observed, RADIAL*inward-coeff*scale_energy)
    reject('omit-far-mean', observed, RADIAL*inward+Q(4, 2197)*mean*mean-coeff*scale_energy)
    reject('double-inward-cost', observed, 2*RADIAL*inward+MEAN*mean*mean-coeff*scale_energy)
    reject('alter-angular-max', coeff, CMAX+Q(1, 8388608))
    reject('misidentify-angular-min', controls[18][1], CMAX)
    manifest = {
        'agent': 'six-sendov-3', 'role': 'researcher',
        'status': 'EXACT ALGEBRA CONTROLS; UNIVERSAL BRIDGES ARE WRITTEN PROOFS',
        'python_arithmetic': 'standard-library Fraction, Gaussian rationals, t^5 truncation',
        'exact_checks': len(checks), 'quartic_mixed_profiles': quartic_profiles,
        'second_order_profiles': second_profiles, 'projection_profiles': 12,
        'rejected_mutations': 6, 'sharp_energy_deficit_constant': encode(CMAX),
        'inward_cost': encode(RADIAL), 'mean_square_cost': encode(MEAN),
        'profile_coefficient_sha256': sha256(json.dumps(records, separators=(',', ':')).encode()).hexdigest(),
        'check_labels_sha256': sha256('\n'.join(checks).encode()).hexdigest(),
        'analytic_bridge_formalized': False, 'external_inputs': []}
    expected_path = Path(__file__).with_name('expected.json')
    if '--write-expected' in sys.argv:
        expected_path.write_text(json.dumps(manifest, indent=2, sort_keys=True)+'\n')
    else:
        expected = json.loads(expected_path.read_text())
        if manifest != expected:
            raise RuntimeError('Manifest differs from expected.json')
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == '__main__':
    run()
