#!/usr/bin/env python3
"""Exact finite algebra for quantitative boundary-profile stability.

Python3.11 standard library only. Arithmetic kernels adapt six-sendov-3's
quartic-boundary checker (source f8df996dba7bfec1d05eb6731b3b8e667ca8f860).
They are included here; no prior source is imported. Analytic uniformity,
even root-pair averaging and global coercivity remain written proof.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

class AlgebraError(RuntimeError):
    pass


def require(ok, label):
    if not ok:
        raise AlgebraError(label)


class K:
    """Q[c]/(c^3-3c/4-1/8), normal form (1,c,c^2)."""

    def __init__(self, value=0):
        if isinstance(value, K):
            self.a = value.a
        elif isinstance(value, (tuple, list)):
            require(len(value) == 3, 'cubic normal form length')
            self.a = tuple(map(F, value))
        else:
            self.a = (F(value), F(0), F(0))

    def __add__(self, other):
        other = K(other)
        return K(tuple(a+b for a, b in zip(self.a, other.a)))

    __radd__ = __add__

    def __neg__(self):
        return K(tuple(-a for a in self.a))

    def __sub__(self, other):
        return self + -K(other)

    def __rsub__(self, other):
        return K(other) + -self

    def __mul__(self, other):
        other = K(other)
        a = [F(0)]*5
        for i, x in enumerate(self.a):
            for j, y in enumerate(other.a):
                a[i+j] += x*y
        for i in (4, 3):
            a[i-2] += F(3, 4)*a[i]
            a[i-3] += F(1, 8)*a[i]
        return K(tuple(a[:3]))

    __rmul__ = __mul__

    def __pow__(self, n):
        require(isinstance(n, int) and n >= 0, 'nonnegative field power')
        ans = K(1)
        for _ in range(n):
            ans *= self
        return ans

    def inv(self):
        columns = [(self*K(tuple(int(i == j) for i in range(3)))).a
                   for j in range(3)]
        rows = [[columns[j][i] for j in range(3)] + [F(i == 0)]
                for i in range(3)]
        for j in range(3):
            pivot = next((i for i in range(j, 3) if rows[i][j]), None)
            require(pivot is not None, 'invertible cubic field element')
            rows[j], rows[pivot] = rows[pivot], rows[j]
            q = rows[j][j]
            rows[j] = [v/q for v in rows[j]]
            for i in range(3):
                if i != j:
                    q = rows[i][j]
                    rows[i] = [v-q*w for v, w in zip(rows[i], rows[j])]
        return K(tuple(rows[i][3] for i in range(3)))

    def __truediv__(self, other):
        return self*K(other).inv()

    def __rtruediv__(self, other):
        return K(other)*self.inv()

    def __eq__(self, other):
        return self.a == K(other).a

    def record(self):
        return [str(a) for a in self.a]

    def interval(self, lo, hi):
        # Here 0 < lo < hi, so powers preserve the ordered endpoints.
        lower = upper = self.a[0]
        for i in (1, 2):
            ends = self.a[i]*lo**i, self.a[i]*hi**i
            lower += min(ends)
            upper += max(ends)
        return lower, upper


# Gaussian-rational sparse jets: epsilon, z, seven free h,
# eight u and the rescaled imaginary sum V.
NV = 18
ORDER = 6
ZERO_EXP = (0,)*NV


def gadd(a, b):
    return a[0]+b[0], a[1]+b[1]


def gmul(a, b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def pc(v=0, imag=0):
    v = F(v), F(imag)
    return {ZERO_EXP: v} if v != (0, 0) else {}


def pv(i):
    a = [0]*NV
    a[i] = 1
    return {tuple(a): (F(1), F(0))}


def padd(*ps):
    ans = {}
    for p in ps:
        for e, v in p.items():
            ans[e] = gadd(ans.get(e, (F(0), F(0))), v)
            if ans[e] == (0, 0):
                del ans[e]
    return ans


def pscale(p, real=1, imag=0):
    return {e: w for e, v in p.items()
            if (w := gmul(v, (F(real), F(imag)))) != (0, 0)}


def pmul(*ps):
    ans = pc(1)
    for p in ps:
        new = {}
        for e, v in ans.items():
            for f, w in p.items():
                if e[0]+f[0] > ORDER:
                    continue
                key = tuple(a+b for a, b in zip(e, f))
                new[key] = gadd(new.get(key, (F(0), F(0))), gmul(v, w))
                if new[key] == (0, 0):
                    del new[key]
        ans = new
    return ans


def ppow(p, n):
    return pmul(*([p]*n))


def pdiff(p, i):
    ans = {}
    for e, v in p.items():
        if e[i]:
            f = list(e)
            f[i] -= 1
            ans[tuple(f)] = gmul(v, (F(e[i]), F(0)))
    return ans


def pint(p, i):
    ans = {}
    for e, v in p.items():
        f = list(e)
        f[i] += 1
        ans[tuple(f)] = gmul(v, (F(1, f[i]), F(0)))
    return ans


def psubst(p, i, replacement):
    ans = {}
    for e, v in p.items():
        f = list(e)
        power = f[i]
        f[i] = 0
        # Accumulate directly. Rebuilding the entire partial sum per
        # monomial is quadratic in the sparse output size.
        for key, w in pmul({tuple(f): v}, ppow(replacement, power)).items():
            ans[key] = gadd(ans.get(key, (F(0), F(0))), w)
            if ans[key] == (0, 0):
                del ans[key]
    return ans


def precord(p):
    return [[list(e), str(v[0]), str(v[1])] for e, v in sorted(p.items())]


def phash(p):
    raw = json.dumps(precord(p), separators=(',', ':')).encode()
    return sha256(raw).hexdigest()


class Z:
    """K[s,i]/(s^2-q,i^2+1), with conjugation fixing the real s."""

    def __init__(self, value=0, *, q=None):
        if isinstance(value, Z):
            self.q, self.a = value.q, value.a
        else:
            require(q is not None, 'quadratic extension specified')
            self.q = K(q)
            vals = value if isinstance(value, (list, tuple)) else (value, 0, 0, 0)
            require(len(vals) == 4, 'quadratic Gaussian length')
            self.a = tuple(K(v) for v in vals)

    def coerce(self, other):
        ans = other if isinstance(other, Z) else Z(other, q=self.q)
        require(ans.q == self.q, 'same quadratic extension')
        return ans

    def __add__(self, other):
        other = self.coerce(other)
        return Z(tuple(a+b for a, b in zip(self.a, other.a)), q=self.q)

    __radd__ = __add__

    def __neg__(self):
        return Z(tuple(-a for a in self.a), q=self.q)

    def __sub__(self, other):
        return self+-self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other)+-self

    def __mul__(self, other):
        other = self.coerce(other)
        a, b, c, d = self.a
        e, f, g, h = other.a
        q = self.q
        return Z((a*e+b*f*q-c*g-d*h*q,
                  a*f+b*e-c*h-d*g,
                  a*g+b*h*q+c*e+d*f*q,
                  a*h+b*g+c*f+d*e), q=q)

    __rmul__ = __mul__

    def __truediv__(self, other):
        # Only real-field scalar divisions occur in this checker.
        return self*K(other).inv()

    def __pow__(self, n):
        require(isinstance(n, int) and n >= 0, 'nonnegative extension power')
        ans = Z(1, q=self.q)
        for _ in range(n):
            ans *= self
        return ans

    def conj(self):
        a, b, c, d = self.a
        return Z((a, b, -c, -d), q=self.q)

    def real_field(self):
        require(self.a[1] == 0, 'real part descends to cubic field')
        return self.a[0]

    def __eq__(self, other):
        return self.a == self.coerce(other).a

    def record(self):
        return [a.record() for a in self.a]


# Independent K[eta,z,sigma] construction. Only eta is truncated.
EORDER = 3


def kc(v=0):
    return {(0, 0, 0): K(v)} if K(v) != 0 else {}


def ka(*ps):
    ans = {}
    for p in ps:
        for e, v in p.items():
            ans[e] = ans.get(e, K(0))+v
            if ans[e] == 0:
                del ans[e]
    return ans


def ks(p, a):
    return {e: v for e, w in p.items() if (v := w*a) != 0}


def km(*ps):
    ans = kc(1)
    for p in ps:
        new = {}
        for e, a in ans.items():
            for f, b in p.items():
                if e[0]+f[0] > EORDER:
                    continue
                key = tuple(x+y for x, y in zip(e, f))
                new[key] = new.get(key, K(0))+a*b
                if new[key] == 0:
                    del new[key]
        ans = new
    return ans


def kp(p, n):
    return km(*([p]*n))


def ki(p):
    return {(a, b+1, c): v/(b+1) for (a, b, c), v in p.items()}


def ksubz(p, replacement):
    ans = {}
    for (a, b, c), v in p.items():
        ans = ka(ans, km({(a, 0, c): v}, kp(replacement, b)))
    return ans


def keval(p, order, omega, sigma=0, derivative=0):
    ans = Z(0, q=omega.q)
    for (a, b, c), v in p.items():
        if a == order and b >= derivative:
            coeff = v*K(sigma)**c
            for j in range(derivative):
                coeff *= b-j
            ans += omega**(b-derivative)*coeff
    return ans


def kcoeff(p, n):
    return {(0, b, c): v for (a, b, c), v in p.items() if a == n}


def krecord(p):
    return [[list(e), v.record()] for e, v in sorted(p.items())]


def khash(p):
    return sha256(json.dumps(krecord(p), separators=(',', ':')).encode()).hexdigest()


def build_record():
    records = {}
    checks = 0

    def equal(a, b, label):
        nonlocal checks
        require(a == b, label)
        checks += 1

    def reject(fn, label):
        nonlocal checks
        try:
            fn()
        except AlgebraError:
            checks += 1
            return label
        raise AlgebraError('mutation was not rejected: '+label)

    c = K((0, 1, 0))
    d = 2*c*c-1
    v = 2*d*d-1
    y = 1/(3*(1+c))
    x = K(F(2, 3))-y
    H = 14*y
    C = K(F(8, 3))+y
    U0 = -8*x
    w4 = 1/(c+d)
    w3 = K(F(2, 3))*(7-(1-d)*w4)
    rho = K(F(-3, 2))+w4/4
    sigmacost = K(F(3, 8))-(K(F(3, 2))*w3+(1-v)*w4)/20
    alpha = sigmacost-rho*rho/2
    L = -7*(2*c+1)/18
    beta = (L+rho)**2/2
    mu = beta+alpha/2
    uz = (U0+rho*H)/8
    up = uz-rho*H/2
    Bstar = K((F(2311, 108), F(4934, 27), F(-1976, 9)))
    A = [K(F(3, 2)), 1+c]
    B = [K(F(3, 2)), 1-d]
    C6 = [K(0), K(F(3, 2))]
    C5 = [K(F(3, 2)), 1-v]
    ratios = [K(-1), -2*c]
    sine2 = [K(F(3, 4)), 1-c*c]
    curvature = [-(K(F(7, 2))*x*x+6*x*y*r+K(F(5, 2))*y*y*r*r)*s
                 for r, s in zip(ratios, sine2)]
    T0 = [4+U0-H/2+b*U0*U0/14-c6*U0*H/12+c5*H*H/40+curv
          for b, c6, c5, curv in zip(B, C6, C5, curvature)]
    equal(8*c**3-6*c-1, 0, 'cubic relation')
    equal(rho, (c-5)/3, 'mixed correction coefficient')
    equal(alpha, K((F(-527, 360), F(41, 90), F(13, 90))),
          'profile fourth moment coefficient')
    equal(beta, K((F(1369, 648), F(74, 81), F(8, 81))),
          'profile cubic square coefficient')
    lo, hi = F(3, 4), F(1)
    f = lambda t: 8*t**3-6*t-1
    require(f(lo) < 0 < f(hi) and 24*lo*lo-6 > 0, 'monotone isolation')
    checks += 1
    for _ in range(80):
        mid = (lo+hi)/2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    require(f(lo) < 0 < f(hi), 'final isolation')
    checks += 1
    for name, val in [('negative alpha', -alpha), ('mu', mu),
                      ('pair sum Hessian coefficient', 9*beta+4*alpha),
                      ('H', H)]:
        require(val.interval(lo, hi)[0] > 0, 'strict sign '+name)
        checks += 1
    records['embedding_interval'] = [str(lo), str(hi)]
    records['constants'] = {name: value.record() for name, value in
        [('H', H), ('C', C), ('U0', U0), ('rho', rho), ('alpha', alpha),
         ('beta', beta), ('mu', mu), ('9beta+4alpha', 9*beta+4*alpha),
         ('L', L), ('u_zero', uz), ('u_pair', up), ('Bstar', Bstar)]}

    # Definition-level parity under the exact small imaginary-sum condition.
    ep, z = pv(0), pv(1)
    hs = [pv(i) for i in range(2, 9)]
    VV = pv(17)
    hs.append(padd(pscale(padd(*hs), -1), pmul(ppow(ep, 2), VV)))
    us = [pv(i) for i in range(9, 17)]
    Um = padd(*us)
    Hm = padd(*(ppow(h, 2) for h in hs))
    U2m = padd(*(ppow(u, 2) for u in us))
    J3m = padd(*(ppow(h, 3) for h in hs))
    J4m = padd(*(ppow(h, 4) for h in hs))
    J21m = padd(*(pmul(h, h, u) for h, u in zip(hs, us)))
    Bm = pscale(padd(*(pmul(h, u) for h, u in zip(hs, us))), 2)
    criticals = [padd(pscale(pmul(ep, h), 0, 1), pmul(ppow(ep, 2), u))
                 for h, u in zip(hs, us)]
    derivative = pscale(pmul(*(padd(z, pscale(cr, -1)) for cr in criticals)), 9)
    primitive = pint(derivative, 1)
    marked = padd(pc(1), pscale(ppow(ep, 2), -1))
    polynomial = padd(primitive, pscale(psubst(primitive, 1, marked), -1))
    conjugate = {e: (a, -b) for e, (a, b) in polynomial.items()}
    equal(psubst(polynomial, 0, pscale(ep, -1)), conjugate,
          'full polynomial conjugation parity through order six')
    realpart = {e: (a, F(0)) for e, (a, b) in polynomial.items() if a}
    imagpart = {e: (F(0), b) for e, (a, b) in polynomial.items() if b}
    require(all(e[0] % 2 == 0 for e in realpart), 'real orders are even')
    require(all(e[0] % 2 == 1 and e[0] >= 3 for e in imagpart),
            'imaginary orders are odd and begin at three')
    checks += 2
    diff = lambda n: padd(ppow(z, n), pc(-1))
    g2 = padd(pc(9), pscale(pmul(Um, diff(8)), F(-9, 8)),
              pscale(pmul(Hm, diff(7)), F(9, 14)))
    g4 = padd(pc(-36), pscale(Um, -9), pscale(Hm, F(9, 2)),
        pscale(pmul(padd(ppow(Um, 2), pscale(U2m, -1)), diff(7)), F(9, 14)),
        pmul(padd(pscale(pmul(Um, Hm), F(-3, 4)), pscale(J21m, F(3, 2))), diff(6)),
        pmul(padd(pscale(ppow(Hm, 2), F(9, 40)), pscale(J4m, F(-9, 20))), diff(5)))
    predicted_real = padd(diff(9), pmul(ppow(ep, 2), g2), pmul(ppow(ep, 4), g4))
    remainder = padd(realpart, pscale(predicted_real, -1))
    require(all(e[0] >= 6 for e in remainder), 'real coefficient remainder begins at six')
    checks += 1
    g3 = padd(pscale(pmul(VV, diff(8)), 0, F(-9, 8)),
               pscale(pmul(Bm, diff(7)), 0, F(-9, 14)),
               pscale(pmul(J3m, diff(6)), 0, F(1, 2)))
    imagrem = padd(imagpart, pscale(pmul(ppow(ep, 3), g3), -1))
    require(all(e[0] >= 5 for e in imagrem), 'imaginary coefficient remainder begins at five')
    checks += 1
    equal(psubst(polynomial, 1, marked), {}, 'generic marked root')
    records['generic_parity'] = {'variables': NV, 'epsilon_order': ORDER,
        'derivative_terms': len(derivative), 'derivative_hash': phash(derivative),
        'anchored_terms': len(polynomial), 'anchored_hash': phash(polynomial),
        'real_remainder_terms': len(remainder), 'imag_remainder_terms': len(imagrem)}

    # Constrained local chart at b=1, H=2, with six free small coordinates.
    ts = [pv(i) for i in range(2, 8)]
    tsum = padd(*ts)
    tnorm = padd(*(ppow(t, 2) for t in ts))
    pairmean = pscale(pmul(ep, tsum), F(-1, 2))
    pairdiff = padd(pc(1), pscale(pmul(ppow(ep, 2), tnorm), F(-1, 4)),
                    pscale(pmul(ppow(ep, 2), ppow(tsum, 2)), F(-1, 8)))
    chart = [padd(pairmean, pairdiff), padd(pairmean, pscale(pairdiff, -1))]
    chart += [pmul(ep, t) for t in ts]
    trunc2 = lambda p: {e: v for e, v in p.items() if e[0] <= 2}
    equal(padd(*chart), {}, 'local chart balance')
    equal(trunc2(padd(*(ppow(h, 2) for h in chart))), pc(2),
          'local chart norm through second order')
    j3 = padd(*(ppow(h, 3) for h in chart))
    j4 = padd(*(ppow(h, 4) for h in chart))
    equal(trunc2(j3), pscale(pmul(ep, tsum), -3), 'local cubic linearization')
    equal(trunc2(j4), padd(pc(2), pscale(pmul(ppow(ep, 2),
          padd(ppow(tsum, 2), pscale(tnorm, -1))), 2)), 'local fourth Hessian')
    aa, bb = pv(8), pv(9)
    cost = padd(pmul(aa, padd(j4, pc(-2))),
                pscale(pmul(bb, ppow(j3, 2)), F(1, 2)))
    expected_cost = pscale(pmul(ppow(ep, 2), padd(
        pmul(pscale(aa, -1), tnorm),
        pmul(padd(aa, pscale(bb, F(9, 4))), ppow(tsum, 2)))), 2)
    equal(trunc2(cost), expected_cost, 'full six-variable constrained Hessian')
    records['hessian'] = {'variables': 6, 'chart_hash': phash(padd(*(
        pscale(p, j+1) for j, p in enumerate(chart)))), 'cost_hash': phash(expected_cost)}

    # Two imaginary pairs and four real critical points. sigma is free;
    # the intended parameter range is a neighborhood of zero.
    eta, zz, sigma = ({(1, 0, 0): K(1)}, {(0, 1, 0): K(1)},
                      {(0, 0, 1): K(1)})
    hA2 = ks(ka(kc(1), ks(sigma, -1)), H/2)
    hB2 = ks(sigma, H/2)
    uA = ka(kc(uz), ks(hA2, -rho))
    uB = ka(kc(uz), ks(hB2, -rho))
    U2 = ka(kc(4*uz*uz), ks(kp(uA, 2), 2), ks(kp(uB, 2), 2))
    J21 = ks(ka(km(uA, hA2), km(uB, hB2)), 2)
    J4 = ks(ka(kp(hA2, 2), kp(hB2, 2)), 2)
    equal(ka(kc(4*uz), ks(uA, 2), ks(uB, 2)), kc(U0), 'two-pair real mean')
    equal(ks(ka(hA2, hB2), 2), kc(H), 'two-pair imaginary energy')
    target = [ka(kc(t), ks(J21, c6/6), ks(J4, -c5/20))
              for t, c6, c5 in zip(T0, C6, C5)]
    det = (A[0]*B[1]-A[1]*B[0])/112
    W = ks(ka(ks(target[0], B[1]/14), ks(target[1], -B[0]/14)), 1/det)
    D = ks(ka(ks(target[1], A[0]/8), ks(target[0], -A[1]/8)), 1/det)
    gamma = ks(ka(U2, ks(D, -1)), 1/(2*H))
    for j in range(2):
        equal(ka(ks(W, A[j]/8), ks(D, B[j]/14)), target[j],
              'two-pair generic quartic tangency '+str(j))
    shift = ka(ks(km(W, kp(eta, 2)), F(1, 8)), ks(kp(eta, 3), 100))
    z0 = ka(ks(eta, uz), shift)
    zA = ka(km(eta, uA), shift)
    zB = ka(km(eta, uB), shift)
    imfactor = kp(ka(kc(1), km(gamma, eta)), 2)
    der = ks(km(kp(ka(zz, ks(z0, -1)), 4),
        ka(kp(ka(zz, ks(zA, -1)), 2), km(hA2, eta, imfactor)),
        ka(kp(ka(zz, ks(zB, -1)), 2), km(hB2, eta, imfactor))), 9)
    prim = ki(der)
    markedeta = ka(kc(1), ks(eta, -1))
    pol = ka(prim, ks(ksubz(prim, markedeta), -1))
    equal(ksubz(pol, markedeta), {}, 'two-pair marked root')
    equal(kcoeff(pol, 0), {(0, 9, 0): K(1), (0, 0, 0): K(-1)},
          'two-pair limiting polynomial')
    require(all(e[2] == 0 for e in kcoeff(pol, 1)),
            'first motion independent of sigma')
    require(all(e[2] <= 2 for e in kcoeff(pol, 2)),
            'second radial polynomial has degree at most two')
    checks += 2
    roots = [Z((F(-1, 2), 0, 0, 1), q=sine2[0]),
             Z((-c, 0, 0, 1), q=sine2[1])]
    inward = []
    for j, omega in enumerate(roots):
        equal(omega*omega.conj(), 1, 'active unit root '+str(j))
        equal(omega**9, 1, 'active ninth root '+str(j))
        # Three exact values plus the proven degree-two bound establish
        # the complete identity; these are not numerical sample evidence.
        for value in (F(0), F(1, 7), F(1, 3)):
            r1 = -keval(pol, 1, omega, value)*omega/9
            r2 = -(keval(pol, 2, omega, value)
                    +keval(pol, 1, omega, value, 1)*r1
                    +omega**7*r1**2*36)*omega/9
            equal((r1*omega.conj()).real_field(), 0,
                  'two-pair first radial identity '+str(j)+' '+str(value))
            equal((r2*omega.conj()+r1*r1.conj()/2).real_field(), 0,
                  'two-pair full second radial identity '+str(j)+' '+str(value))
        r1 = -keval(pol, 1, omega)*omega/9
        r2 = -(keval(pol, 2, omega)+keval(pol, 1, omega, derivative=1)*r1
                +omega**7*r1**2*36)*omega/9
        r3 = -(keval(pol, 3, omega)+keval(pol, 2, omega, derivative=1)*r1
                +keval(pol, 1, omega, derivative=1)*r2
                +keval(pol, 1, omega, derivative=2)*r1**2/2
                +omega**7*r1*r2*72+omega**6*r1**3*84)*omega/9
        R3 = (r3*omega.conj()+r1*r2.conj()).real_field()
        require((-R3).interval(lo, hi)[0] > 0, 'third-order inward motion '+str(j))
        checks += 1
        inward.append(R3.record())

    def inverse_real(distance):
        delta = ka(distance, kc(-1))
        return ka(kc(1), ks(delta, -1), kp(delta, 2), ks(kp(delta, 3), -1))

    def inverse_square(distance2):
        delta = ka(distance2, kc(-1))
        return ka(kc(1), ks(delta, F(-1, 2)), ks(kp(delta, 2), F(3, 8)),
                  ks(kp(delta, 3), F(-5, 16)))

    dist0 = ka(markedeta, ks(z0, -1))
    distA2 = ka(kp(ka(markedeta, ks(zA, -1)), 2), km(hA2, eta, imfactor))
    distB2 = ka(kp(ka(markedeta, ks(zB, -1)), 2), km(hB2, eta, imfactor))
    objective = ka(ks(inverse_real(dist0), 4), ks(inverse_square(distA2), 2),
                   ks(inverse_square(distB2), 2))
    expected_second = ka(kc(Bstar), ks(km(sigma, ka(kc(1), ks(sigma, -1))),
                                      -alpha*H*H))
    equal(kcoeff(objective, 0), kc(8), 'two-pair objective constant')
    equal(kcoeff(objective, 1), kc(C), 'two-pair objective first coefficient')
    equal(kcoeff(objective, 2), expected_second, 'full profile cost identity')
    records['two_pair_family'] = {'eta_order': EORDER, 'derivative_terms': len(der),
        'derivative_hash': khash(der), 'polynomial_terms': len(pol),
        'polynomial_hash': khash(pol), 'second_coefficient': krecord(expected_second),
        'inward_third_at_sigma0': inward, 'objective_hash': khash(objective),
        'objective_eta3_at_sigma0': next(v.record() for (a,b,c),v in objective.items()
                                        if (a,b,c)==(3,0,0)),
        'interpolation_nodes': ['0','1/7','1/3'], 'second_radial_degree_bound': 2}
    records['mutations_rejected'] = [
        reject(lambda: equal(trunc2(cost), pscale(expected_cost, -1),
                             'altered Hessian sign'), 'Hessian sign'),
        reject(lambda: equal(ks(J4, -alpha), expected_second,
                             'missing profile constant'), 'profile cost'),
        reject(lambda: equal(psubst(polynomial, 0, pscale(ep, -1)), polynomial,
                             'confused conjugation'), 'conjugation parity'),
        reject(lambda: equal(ka(ks(W, A[1]/8), ks(D, B[1]/14+1)), target[1],
                             'altered active row'), 'radial correction')]
    records['exact_checks'] = checks
    records['trust_boundary'] = ('finite algebra only; analytic pair averaging, '
        'uniformity, compactness, quantitative coercivity and all-root disk '
        'containment are ordinary written arguments')
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit-fixture', action='store_true')
    parser.add_argument('--fixture', type=Path,
                        default=Path(__file__).with_name('expected.json'))
    args = parser.parse_args()
    records = build_record()
    encoded = json.dumps(records, sort_keys=True, indent=2)+'\n'
    if args.emit_fixture:
        print(encoded, end='')
        return
    require(args.fixture.is_file(), 'required fixture is missing')
    try:
        fixture = json.loads(args.fixture.read_text())
    except (ValueError, OSError) as e:
        raise AlgebraError('required fixture is malformed') from e
    require(fixture == records, 'complete fixture differs')
    print('PASS: '+str(records['exact_checks'])+' exact checks; '
          +str(len(records['mutations_rejected']))+' mutations rejected.')
    print('Complete record SHA256: '+sha256(encoded.encode()).hexdigest())


if __name__ == '__main__':
    main()
