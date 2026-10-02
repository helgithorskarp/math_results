#!/usr/bin/env python3
"""Independent exact nonagon, complex-phase and whole-window audit.

No producer source, fixture or helper is imported. Classical analytic bridges
are stated in REVIEW.md; these finite maps do not formalize them.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trim(p):
    while p and not p[-1]:
        p.pop()
    return p


def division(a, b):
    a = trim(list(a))
    b = trim(list(b))
    require(bool(b), 'zero polynomial divisor')
    q = [F(0)] * max(0, len(a) - len(b) + 1)
    while len(a) >= len(b):
        n = len(a) - len(b)
        c = a[-1] / b[-1]
        q[n] += c
        for j, value in enumerate(b):
            a[n + j] -= c * value
        trim(a)
    return trim(q), a


def polyadd(a, b):
    return trim([(a[j] if j < len(a) else F(0)) +
                 (b[j] if j < len(b) else F(0))
                 for j in range(max(len(a), len(b)))])


def polymul(a, b):
    p = [F(0)] * max(0, len(a) + len(b) - 1)
    for j, x in enumerate(a):
        for k, y in enumerate(b):
            p[j + k] += x * y
    return trim(p)


MODULUS = [F(1), F(0), F(0), F(1), F(0), F(0), F(1)]


class K:
    """Q[omega]/(omega^6+omega^3+1), exact primitive nonagon field."""
    __slots__ = ('v',)

    def __init__(self, value=0):
        if isinstance(value, K):
            self.v = value.v
        elif isinstance(value, (int, F)):
            self.v = (F(value),) + (F(0),) * 5
        else:
            p = [F(x) for x in value]
            for j in range(len(p) - 1, 5, -1):
                p[j - 3] -= p[j]
                p[j - 6] -= p[j]
            self.v = tuple((p[:6] + [F(0)] * 6)[:6])

    def __bool__(self):
        return any(self.v)

    def __eq__(self, other):
        return self.v == K(other).v

    def __add__(self, other):
        if not isinstance(other, (K, int, F, list, tuple)):
            return NotImplemented
        other = K(other)
        return K([x + y for x, y in zip(self.v, other.v)])

    __radd__ = __add__

    def __neg__(self):
        return K([-x for x in self.v])

    def __sub__(self, other):
        if not isinstance(other, (K, int, F, list, tuple)):
            return NotImplemented
        return self + -K(other)

    def __rsub__(self, other):
        return K(other) + -self

    def __mul__(self, other):
        if not isinstance(other, (K, int, F, list, tuple)):
            return NotImplemented
        other = K(other)
        return K(polymul(list(self.v), list(other.v)))

    __rmul__ = __mul__

    def inverse(self):
        require(bool(self), 'zero field inverse')
        a, b = list(MODULUS), trim(list(self.v))
        s, t = [], [F(1)]
        while b:
            q, r = division(a, b)
            a, b = b, r
            s, t = t, polyadd(s, [-x for x in polymul(q, t)])
        require(len(a) == 1, 'nonunit cyclotomic element')
        return K([x / a[0] for x in s])

    def __truediv__(self, other):
        return self * K(other).inverse()

    def __rtruediv__(self, other):
        return K(other) * self.inverse()

    def __pow__(self, power):
        if power < 0:
            return self.inverse() ** (-power)
        result, base = K(1), self
        while power:
            if power & 1:
                result = result * base
            base = base * base
            power //= 2
        return result

    def conjugate(self):
        return sum((x * OMEGA_POWERS[(-j) % 9]
                    for j, x in enumerate(self.v)), K())

    def pack(self):
        return [str(x) for x in self.v]


OMEGA = K([0, 1])
OMEGA_POWERS = [OMEGA ** j for j in range(9)]


def monomial_product(a, b):
    d = dict(a)
    for key, value in b:
        d[key] = d.get(key, 0) + value
    return tuple(sorted((key, value) for key, value in d.items() if value))


def conjugate_variable(name):
    if name in ['u', 'ub']:
        return {'u': 'ub', 'ub': 'u'}[name]
    if name in ['T', 'Tb', 'U3', 'U3b']:
        return {'T': 'Tb', 'Tb': 'T', 'U3': 'U3b', 'U3b': 'U3'}[name]
    if name.startswith('db'):
        return 'd' + name[2:]
    if name.startswith('d') and name[1:].isdigit():
        return 'db' + name[1:]
    return name


class P:
    """Laurent polynomials in independent formal variables over K."""
    __slots__ = ('terms',)

    def __init__(self, value=0):
        if isinstance(value, P):
            self.terms = dict(value.terms)
        elif isinstance(value, dict):
            self.terms = {m: K(c) for m, c in value.items() if K(c)}
        else:
            c = K(value)
            self.terms = {(): c} if c else {}

    def __eq__(self, other):
        return self.terms == P(other).terms

    def __add__(self, other):
        d = dict(self.terms)
        for m, c in P(other).terms.items():
            d[m] = d.get(m, K()) + c
            if not d[m]:
                del d[m]
        return P(d)

    __radd__ = __add__

    def __neg__(self):
        return P({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + -P(other)

    def __rsub__(self, other):
        return P(other) + -self

    def __mul__(self, other):
        d = {}
        for m, c in self.terms.items():
            for n, b in P(other).terms.items():
                key = monomial_product(m, n)
                d[key] = d.get(key, K()) + c * b
        return P(d)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * K(scalar).inverse()

    def __pow__(self, power):
        require(isinstance(power, int) and power >= 0, 'polynomial power')
        result, base = P(1), self
        while power:
            if power & 1:
                result = result * base
            base = base * base
            power //= 2
        return result

    def conjugate(self):
        return P({tuple(sorted((conjugate_variable(name), power)
                               for name, power in m)): c.conjugate()
                  for m, c in self.terms.items()})

    def pack(self):
        return [[[[name, power] for name, power in m], c.pack()]
                for m, c in sorted(self.terms.items())]


def variable(name, power=1):
    return P({((name, power),): 1}) if power else P(1)


def real(p):
    p = P(p)
    return (p + p.conjugate()) / 2


def cosine(k):
    return (OMEGA_POWERS[k % 9] + OMEGA_POWERS[-k % 9]) / 2


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


class G:
    """Q(omega)[i], for a separate literal Gaussian-critical computation."""
    __slots__ = ('r', 'i')

    def __init__(self, value=0, imag=0):
        if isinstance(value, G):
            self.r, self.i = value.r, value.i
        else:
            self.r, self.i = K(value), K(imag)

    def __eq__(self, other):
        other = G(other)
        return self.r == other.r and self.i == other.i

    def __add__(self, other):
        other = G(other)
        return G(self.r + other.r, self.i + other.i)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.r, -self.i)

    def __sub__(self, other):
        return self + -G(other)

    def __rsub__(self, other):
        return G(other) + -self

    def __mul__(self, other):
        other = G(other)
        return G(self.r * other.r - self.i * other.i,
                 self.r * other.i + self.i * other.r)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = G(other)
        norm = other.r**2 + other.i**2
        return G((self.r * other.r + self.i * other.i) / norm,
                 (self.i * other.r - self.r * other.i) / norm)

    def __pow__(self, power):
        if power < 0:
            return (G(1) / self) ** (-power)
        result = G(1)
        for _ in range(power):
            result = result * self
        return result

    def conjugate(self):
        return G(self.r.conjugate(), -self.i.conjugate())

    def pack(self):
        return [self.r.pack(), self.i.pack()]


def evaluate(poly, values):
    result = G()
    for m, c in P(poly).terms.items():
        term = G(c)
        for name, power in m:
            term = term * values[name] ** power
        result = result + term
    return result


def greal(value):
    return (value + value.conjugate()) / 2


def literal_controls():
    e = F(1, 65536)
    datasets = [
        ('actual centered total collision; high-F arm', G(), [G()] * 8),
        ('repeated centered imaginary criticals', G(-e / 2, e / 5),
         [G(0, F(1, 2048)), G(0, F(-1, 2048))] * 4),
        ('asymmetric nonconjugate criticals', G(-3 * e / 4, e / 4),
         [G(F(x, 8192), F(y, 8192)) for x, y in
          [(1, 1), (2, -1), (-2, 1), (1, -2), (-1, 3), (2, 1), (-3, -1), (0, -2)]]),
        ('repeated asymmetric Gaussian criticals', G(-e / 3, -e / 7),
         [G(F(x, 16384), F(y, 16384)) for x, y in
          [(1, 2), (1, 2), (1, 2), (-2, 1), (-2, 1), (1, -1), (1, -1), (-1, -6)]]),
    ]
    result = []
    for name, mean, nus in datasets:
        require(sum(nus, G()) == 0, 'literal zero mean: ' + name)
        a, u = G(1 - e), G(1 - e) - mean
        # Ascending coefficients of the complete eight-factor critical product.
        product = [G(1)]
        for nu in nus:
            next_product = [G()] * (len(product) + 1)
            for j, coef in enumerate(product):
                next_product[j] = next_product[j] - coef * nu
                next_product[j + 1] = next_product[j + 1] + coef
            product = next_product
        integrated = [G()] + [9 * coef / (j + 1)
                              for j, coef in enumerate(product)]
        T = sum((nu**2 for nu in nus), G())
        U3 = sum((nu**3 for nu in nus), G())
        V = sum((nu * nu.conjugate() for nu in nus), G())
        rotated = T * u.conjugate() / u
        require(integrated[7] == -9 * T / 14 and integrated[6] == -U3 / 2,
                'literal Newton: ' + name)
        values = {'a': a, 'u': u, 'ub': u.conjugate(),
                  'T': T, 'Tb': T.conjugate(), 'U3': U3, 'U3b': U3.conjugate()}
        values.update({'d' + str(j): integrated[j] for j in range(1, 8)})
        values.update({'db' + str(j): integrated[j].conjugate() for j in range(1, 8)})
        phase = []
        for k in range(9):
            w = G(OMEGA_POWERS[k])
            basepoint = mean + u * w
            value = sum((integrated[j] * ((u * w)**j - u**j)
                         for j in range(1, 10)), G())
            direct = -value / (9 * (u * w)**8)
            formal = sum((variable('d' + str(j)) * variable('u', j - 8) *
                          (OMEGA_POWERS[k] - OMEGA_POWERS[k]**(j - 8)) / 9
                          for j in range(1, 8)), P())
            require(direct == evaluate(formal, values), 'literal full displacement: ' + name)
            phase.append({'k': k, 'basepoint': basepoint.pack(),
                          'linear_displacement': direct.pack(),
                          'whole_linear_half_normal': greal(basepoint.conjugate() * direct).pack()})
        entry = {'name': name, 'mean': mean.pack(), 'centered_criticals': [nu.pack() for nu in nus],
                 'full_critical_product': [coef.pack() for coef in product],
                 'full_integrated_coefficients': [coef.pack() for coef in integrated],
                 'T': T.pack(), 'U3': U3.pack(), 'V': V.pack(),
                 'rotated_T': rotated.pack(), 'whole_phase_values': phase,
                 'scope': 'literal algebra controls; only first case has independently evident original-disk feasibility, on the HIGH-F arm'}
        result.append({**entry, 'full_control_sha256': digest(entry)})
    return result


def compute():
    identities = []
    margins = []

    def identity(name, lhs, rhs):
        lhs, rhs = P(lhs), P(rhs)
        require(lhs == rhs, 'identity: ' + name)
        common = lhs.pack()
        identities.append({'name': name, 'full_map': common,
                           'terms': len(common), 'sha256': digest(common)})

    def margin(name, value):
        value = F(value)
        require(value > 0, 'strict margin: ' + name)
        margins.append({'name': name, 'exact': str(value)})

    c = -cosine(4)
    d = cosine(1)
    y = 1 / K(3 * (1 + c))
    x = K(F(2, 3)) - y
    C = K(F(8, 3)) + y
    w4 = (c + d).inverse()
    w3 = (7 - (1 - d) * w4) * F(2, 3)
    A3, A4 = 1 - cosine(3), 1 - cosine(4)
    B3, B4 = 1 - cosine(6), 1 - cosine(8)
    for name, lhs, rhs in [
        ('cosine cubic', 8 * c**3 - 6 * c, 1),
        ('double angle', d, 2 * c**2 - 1),
        ('cube optimum', A3 * x + B3 * y, 1),
        ('fourth optimum', A4 * x + B4 * y, 1),
        ('dual mean', w3 * A3 + w4 * A4, 8),
        ('dual second moment', w3 * B3 + w4 * B4, 7),
        ('sharp coefficient', 8 - w3 - w4, C),
        ('Cramer determinant', A4 * B3 - A3 * B4, F(3, 2) * (c + d)),
        ('weight simplification', w3 * (2 * c - 1), (16 * c - 9) * F(2, 3)),
        ('cube primitive identity', cosine(3), F(-1, 2)),
    ]:
        identity(name, lhs, rhs)

    a, u, ub = variable('a'), variable('u'), variable('ub')
    m, mb = a - u, a - ub
    M = (m + mb) / 2
    T, U3 = variable('T'), variable('U3')
    rotated_T = T * ub * variable('u', -1)
    Q = real(rotated_T)
    H3 = real(U3 * ub * variable('u', -2))
    phase_rows = []
    for k in range(9):
        w = OMEGA_POWERS[k]
        z = m + u * w
        zminus = m + u * OMEGA_POWERS[-k % 9]
        base = (z * z.conjugate() + zminus * zminus.conjugate() - 2) / 4
        Ak = 1 - cosine(k)
        expected = (a**2 - 1) / 2 - Ak * (a * M - m * mb)
        identity('entire base half-normal pair ' + str(k), base, expected)
        residual = sum((variable('d' + str(j)) * u**j * (w**j - 1)
                        for j in range(1, 8)), P())
        delta = residual * variable('u', -8) * (-w**-8 / 9)
        whole = sum((variable('d' + str(j)) * variable('u', j - 8) *
                     (w - w**(j - 8)) / 9 for j in range(1, 8)), P())
        identity('entire integrated linear displacement ' + str(k), delta, whole)
        delta7 = -F(9, 14) * T * variable('u', -1) * (w - w**-1) / 9
        delta6 = -F(1, 2) * U3 * variable('u', -2) * (w - w**-2) / 9
        minus_w = OMEGA_POWERS[-k % 9]
        minus7 = -F(9, 14) * T * variable('u', -1) * (minus_w - minus_w**-1) / 9
        minus6 = -F(1, 2) * U3 * variable('u', -2) * (minus_w - minus_w**-2) / 9
        principal = (real(ub * w.conjugate() * (delta7 + delta6)) +
                     real(ub * minus_w.conjugate() * (minus7 + minus6))) / 2
        expected_principal = -(1 - cosine(2 * k)) * Q / 14 + (cosine(3 * k) - 1) * H3 / 18
        identity('full second-third moment pair ' + str(k), principal, expected_principal)
        phase_rows.append({'k': k, 'A': Ak.pack(),
                           'B': (1 - cosine(2 * k)).pack(),
                           'third_factor': ((cosine(3 * k) - 1) / 18).pack()})
    identity('cube third moment vanishes', (cosine(9) - 1) / 18, 0)
    identity('fourth third moment survives', (cosine(12) - 1) / 18, F(-1, 12))

    # Complete zero-mean Newton identities, with the eighth root eliminated.
    roots = [variable('n' + str(j)) for j in range(7)]
    roots.append(-sum(roots, P()))
    elementary = [P(1)]
    for root in roots:
        elementary = [elementary[j] - root * elementary[j - 1]
                      if 0 < j < len(elementary) else
                      (elementary[0] if j == 0 else -root * elementary[-1])
                      for j in range(len(elementary) + 1)]
    T2 = sum((z**2 for z in roots), P())
    T3 = sum((z**3 for z in roots), P())
    identity('full centered integrated d7', elementary[2] * F(9, 7), -T2 * F(9, 14))
    identity('full centered integrated d6', elementary[3] * F(3, 2), -T3 / 2)

    eta, Mv, Qv, Vv = [variable(t) for t in ['eta', 'M', 'Q', 'V']]
    s3, s4, R3v, R4v = [variable(t) for t in ['s3', 's4', 'R3', 'R4']]
    L3, L4 = -A3 * Mv - B3 * Qv / 14, -A4 * Mv - B4 * Qv / 14
    Phi = w3 * s3 + w4 * s4 + (Vv + Qv) / 4
    constraint = w3 * (L3 - eta + s3 + R3v) + w4 * (L4 - eta + s4 + R4v)
    identity('complete physical coercivity reduction',
             8 * eta + 8 * Mv + (Vv + 3 * Qv) / 4 + constraint,
             C * eta + Phi + w3 * R3v + w4 * R4v)
    determinant = A4 * B3 - A3 * B4
    t3, t4 = L3 - eta, L4 - eta
    identity('complete complex mean Cramer map', Mv + x * eta,
             (B4 * t3 - B3 * t4) / determinant)
    identity('complete second moment Cramer map', -Qv / 14 - y * eta,
             (A4 * t3 - A3 * t4) / determinant)
    mm, kk = variable('merror'), variable('Kerror')
    for k, w in enumerate(OMEGA_POWERS):
        motion = (-x * eta + mm) + (1 - eta + x * eta - mm) * w + (-y * eta + kk) * (w**-1 - w)
        target = w + eta * (-w / 3 - x - y * w**-1)
        identity('entire original motion ' + str(k), motion - target,
                 mm * (1 - w) + kk * (w**-1 - w))

    xs = [variable('X' + str(j)) for j in range(8)]
    ys = [variable('Y' + str(j)) for j in range(8)]
    vx, vy = sum((v**2 for v in xs), P()), sum((v**2 for v in ys), P())
    cross = sum((xj * yj for xj, yj in zip(xs, ys)), P())
    wedges = sum(((xs[j] * ys[k] - xs[k] * ys[j])**2
                  for j in range(8) for k in range(j + 1, 8)), P())
    identity('whole eight-coordinate complex covariance Gram',
             (vx + vy)**2 - (vx - vy)**2 - 4 * cross**2, 4 * wedges)

    # Endpoint arithmetic majorizes entire windows, never an eta sample grid.
    from math import comb
    e, rho, vmax = F(1, 65536), F(1, 64), F(1, 512)
    astar = 1 - e
    rlo, rhi = astar - rho, 1 + rho
    radius = rhi + vmax / 2
    Aj = {j: F(9, 8 * j) * comb(8, 9 - j) * rho**(7 - j)
          for j in range(1, 7)}
    Aj[7] = F(9, 14)
    Cd = sum(j * Aj[j] * radius**(j - 1) for j in Aj)
    N = 2 * sum(Aj[j] * rhi**j for j in Aj)
    Bd = 9 * rlo**8 - 18 * radius**7 * vmax - Cd * vmax
    B = radius**7 / (4 * rlo**8) + Cd / (36 * rlo**8)
    Bj = {5: F(63, 32), 4: F(63, 32) * rho,
          3: F(21, 128) * vmax, 2: F(9, 128) * rho * vmax,
          1: F(9, 4096) * vmax**2}
    low_tail = sum(Bj[j] * rlo**(j - 7) for j in Bj)
    Lambda = 1 / ((astar - F(1, 96)) * astar**3)
    cl, ch = F(15, 16), F(47, 50)
    f = lambda c0: 8 * c0**3 - 6 * c0 - 1
    wl3 = F(2, 3) * (16 * cl - 9) / (2 * cl - 1)
    wh3 = F(2, 3) * (16 * ch - 9) / (2 * ch - 1)
    wl4, wh4 = 1 / (ch + 2 * ch**2 - 1), 1 / (cl + 2 * cl**2 - 1)
    origin37 = F(13, 15) * 6 / 6 + 36
    original_R3 = F(1, 2) + F(3, 2) * F(4, 5) + F(3, 2) * F(13, 15)**2 + origin37
    original_R4 = F(1, 2) + 2 * F(4, 5) + 2 * F(13, 15)**2 + F(13, 15) * 6 / 4 + F(9, 8) * 36
    original_drop = 8 * F(4, 5) * (2 - e) / astar**2 + 4 * F(169, 225) / astar**3 + 24
    scalar = {
        'positive astar': astar,
        'centered rho margin': rho**2 - 6 * e,
        'centered tail radius': F(1, 96)**2 - 6 * e,
        'quarter root displacement': Bd / 4 - N,
        'quarter linear displacement': 9 * rlo**8 / 4 - N,
        'all-phase half-normal budget': F(9, 8) - ((1 + 2 * rho) * B + F(1, 32) + F(2, 9) * low_tail),
        'all-phase displacement tail': 1 - (B + F(2, 9) * low_tail / astar),
        'entire Legendre denominator': astar - F(1, 96),
        'cubic lower sign': -f(cl), 'cubic upper sign': f(ch),
        'cubic branch monotonicity': 24 * cl**2 - 6,
        'dual w3 lower4': wl3 - 4, 'dual w3 upper23over5': F(23, 5) - wh3,
        'dual w4 lowerhalf': wl4 - F(1, 2), 'dual w4 upper3over5': F(3, 5) - wh4,
        'original mu square': F(55, 12)**2 - 21,
        'individual cube error37': 37 - origin37,
        'original cube remainder40': 40 - original_R3,
        'original fourth remainder46': 46 - original_R4,
        'original reciprocal quadratic40': 40 - original_drop,
        'inverse radius cubic4': 4 - (3 - 3 * e + e**2) / astar**3,
        'original coercivity16': 16 - F(252, 256) - F(55, 4) * (Lambda + F(1, 20) / astar),
        'original rational111over40': F(826, 291) - F(1, 16) - F(111, 40),
        'original cube Delta margin': F(1, 100) - F(40, 16 * 256),
        'original fourth Delta margin': F(1, 12) - (F(46, 256) + F(55, 48) / astar) / 16,
        'Cramer determinant increasing': F(3, 2) * (1 + 4 * cl),
        'fourth B strictly decreasing': 4 * cl,
        'fourth A strictly increasing': F(1),
        'original mean4over3': F(4, 3) - (F(62, 651) * F(13, 50) + F(128, 217) * F(25, 12)),
        'original Q3over2': F(3, 2) - (F(24832, 32550) * F(13, 50) + F(128, 217) * F(25, 12)),
        'original H26': 1 - 8 * F(169, 225) / (16 * 256),
        'original D sqrt1': 1 - F(12, 49) / astar**2,
        'original D Delta1': 1 - F(7, 24) / astar,
        'original D quadratic44': 44 - F(259, 6) / astar,
        'original real energy7': 1 - (F(384, 25) + 4 * e / astar**2) / (16 * 256),
        'all-root quadratic125': 125 - (88 + 36 + F(56, 15) * F(16, 93) / astar),
        'original motion sqrt3': 1 - F(48, 49) / astar**2,
        'original motion Delta8': 8 - F(14, 3) - 3 / astar - (F(125, 256) + F(55, 36) / astar**2) / 16,
        'original collar entry': F(1, 512) - 25 * e,
    }

    mu = F(62, 5)
    new_R3 = F(1, 2) + F(3, 2) * F(3, 4) + F(3, 2) * F(4, 5)**2 + F(4, 5) * F(28, 5) / 6 + F(28, 5)**2
    new_R4 = F(1, 2) + 2 * F(3, 4) + 2 * F(4, 5)**2 + F(4, 5) * F(28, 5) / 4 + F(9, 8) * F(28, 5)**2
    new_drop = 8 * F(3, 4) * (2 - e) / astar**2 + 4 * F(4, 5)**2 / astar**3 + F(112, 5)
    new_cost = (37 + F(139, 4) * wh3 + F(397, 10) * wh4) / 256 + mu * (Lambda + wh4 / (12 * astar))
    scalar.update({
        'new mu62over5 square': mu**2 - F(7, 8) * F(28, 5)**3,
        'new cube139over4': F(139, 4) - new_R3,
        'new fourth397over10': F(397, 10) - new_R4,
        'new reciprocal37': 37 - new_drop,
        'new coercivity14': 14 - new_cost,
        'new rational89over32': F(826, 291) - F(7, 128) - F(89, 32),
        'new cube Delta margin': F(1, 100) - F(139, 4 * 14 * 256),
        'new fourth9over100 Delta margin': F(9, 100) - (F(397, 10 * 256) + mu / (12 * astar)) / 14,
        'new mean4over3': F(4, 3) - (F(62, 651) * F(13, 50) + F(128, 217) * F(209, 100)),
        'new Q3over2': F(3, 2) - (F(24832, 32550) * F(13, 50) + F(128, 217) * F(209, 100)),
        'new H26': 1 - 8 * F(169, 225) / (14 * 256),
        'new D sqrt half': F(1, 4) - F(12, 49) / astar**2,
        'new D Delta third': F(1, 3) - F(7, 24) / astar,
        'new real energy7': 1 - (F(384, 25) + 4 * e / astar**2) / (14 * 256),
        'new motion sqrt2': 1 - F(48, 49) / astar**2,
        'new motion Delta13over2': F(13, 2) - F(10, 3) - 3 / astar - (F(125, 256) + F(55, 36) / astar**2) / 14,
        'same eta lower-radius margin': astar - F(1, 25),
    })
    for name, value in scalar.items():
        margin(name, value)
    endpoint_equalities = {
        'Cramer endpoint651over256': [str(F(3, 2) * (cl + 2 * cl**2 - 1)), '651/256'],
        'fourth B endpoint31over128': [str(2 - 2 * cl**2), '31/128'],
        'fourth A endpoint97over50': [str(1 + ch), '97/50'],
        'new dual w3 endpoint151over33': [str(wh3), '151/33'],
        'new dual w4 endpoint128over217': [str(wh4), '128/217'],
    }
    for name, (lhs, rhs) in endpoint_equalities.items():
        require(F(lhs) == F(rhs), 'endpoint equality: ' + name)
    return {'schema': 'independent-effective-stability-audit-v1',
            'field_modulus': [str(x) for x in MODULUS],
            'identities': identities, 'strict_margins': margins,
            'whole_phase_table': phase_rows,
            'rational_endpoint_equalities': endpoint_equalities,
            'whole_literal_controls': literal_controls(),
            'original_eta_endpoint': str(e),
            'original_remainder': '16', 'proved_remainder': '14',
            'new_coercivity_cost': str(new_cost),
            'new_motion_Delta_coefficient': '13/2',
            'new_motion_sqrt_coefficient': '2',
            'new_imaginary_mean_sqrt_coefficient': '1/2',
            'new_imaginary_mean_Delta_coefficient': '1/3',
            'extra_input': 'CREDITED independently confirmed REVIEW9669 same-domain upper bounds'}


def load_fixture(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate fixture key')
            result[key] = value
        return result

    def bad_constant(value):
        raise ValueError('nonfinite fixture token')

    return json.loads(path.read_text(), object_pairs_hook=pairs,
                      parse_constant=bad_constant)


def exact_types_equal(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(exact_types_equal(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(exact_types_equal(x, y) for x, y in zip(a, b))
    return a == b


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expect', type=Path)
    parser.add_argument('--record', type=Path)
    args = parser.parse_args()
    record = compute()
    if args.expect:
        require(exact_types_equal(record, load_fixture(args.expect)), 'complete typed record mismatch')
    if args.record:
        args.record.write_text(json.dumps(record, sort_keys=True, separators=(',', ':')) + '\n')
    print(json.dumps({'status': 'PASS', 'whole_record_sha256': digest(record),
                      'whole_identities': len(record['identities']),
                      'strict_margins': len(record['strict_margins']),
                      'whole_phase_rows': len(record['whole_phase_table']),
                      'whole_literal_controls': len(record['whole_literal_controls']),
                      'new_remainder': record['proved_remainder'],
                      'exact_new_coercivity_gap': str(F(14) - F(record['new_coercivity_cost']))},
                     sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
