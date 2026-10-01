#!/usr/bin/env python3
"""Exact finite algebra for the second-order boundary proof.

Python 3.11 standard library only. The K and sparse Gaussian-polynomial
kernels extend six-sendov-3/sharp-boundary-slope/verify.py (commit
7a7764e3516426353b08b7132c7481239fac79e4). Finite identities only;
analytic concentration, bootstrap and uniform root containment are in PROOF.md.
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


# Gaussian-rational sparse jets: epsilon, z, seven free balanced h,
# and eight free coordinates in each of u, v, w.
NV = 33
ORDER = 4
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
        ans = padd(ans, pmul({tuple(f): v}, ppow(replacement, power)))
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


# A separate bivariate implementation over K, without Gaussian fractions,
# computes the explicit six-plus-two derivative from its definition.
EORDER = 3


def kc(v=0):
    return {(0, 0): K(v)} if K(v) != 0 else {}


def ka(*ps):
    ans = {}
    for p in ps:
        for e, v in p.items():
            ans[e] = ans.get(e, K(0))+v
            if ans[e] == 0:
                del ans[e]
    return ans


def ks(p, v):
    return {e: w for e, a in p.items() if (w := a*v) != 0}


def km(*ps):
    ans = kc(1)
    for p in ps:
        new = {}
        for (a, b), v in ans.items():
            for (c, d), w in p.items():
                if a+c > EORDER:
                    continue
                e = (a+c, b+d)
                new[e] = new.get(e, K(0))+v*w
                if new[e] == 0:
                    del new[e]
        ans = new
    return ans


def kp(p, n):
    return km(*([p]*n))


def ki(p):
    return {(a, b+1): v/(b+1) for (a, b), v in p.items()}


def ksubz(p, z):
    ans = {}
    for (a, b), v in p.items():
        ans = ka(ans, km({(a, 0): v}, kp(z, b)))
    return ans


def keval(p, order, z, derivative=0):
    ans = Z(0, q=z.q)
    for (a, b), v in p.items():
        if a == order and b >= derivative:
            coeff = v
            for j in range(derivative):
                coeff *= b-j
            ans += z**(b-derivative)*coeff
    return ans


def krecord(p):
    return [[list(e), v.record()] for e, v in sorted(p.items())]


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
    U0 = -8*x
    C = K(F(8, 3))+y
    w4 = 1/(c+d)
    w3 = K(F(2, 3))*(7-(1-d)*w4)
    A = [K(F(3, 2)), 1+c]
    B = [K(F(3, 2)), 1-d]
    C6 = [K(0), K(F(3, 2))]
    C5 = [K(F(3, 2)), 1-v]
    ratio = [K(-1), -2*c]
    sine2 = [K(F(3, 4)), 1-c*c]
    curvature = [
        -(K(F(7, 2))*x*x+6*x*y*r+K(F(5, 2))*y*y*r*r)*s
        for r, s in zip(ratio, sine2)]
    T0 = [
        4+U0-H/2+b*U0*U0/14+c6*(-U0*H/12)+c5*H*H/40+curv
        for b, c6, c5, curv in zip(B, C6, C5, curvature)]
    const = 8+2*U0-K(F(3, 2))*H+w3*T0[0]+w4*T0[1]
    aa = K(F(-3, 2))+w4/4
    qq = K(F(3, 8))-(w3*C5[0]+w4*C5[1])/20
    L = -7*(2*c+1)/18
    alpha = qq-aa*aa/2
    beta = (L+aa)**2/2
    base = const+(U0+aa*H)**2/16
    Bstar = base+alpha*H*H/2
    uz = (U0+aa*H)/8
    up = uz-aa*H/2
    U2 = 6*uz*uz+2*up*up
    J21 = H*up
    J4 = H*H/2
    targets = [t+c6*J21/6-c5*J4/20
               for t, c6, c5 in zip(T0, C6, C5)]
    det = (A[0]*B[1]-A[1]*B[0])/112
    W = (targets[0]*B[1]/14-targets[1]*B[0]/14)/det
    D = (A[0]*targets[1]/8-A[1]*targets[0]/8)/det
    gamma = (U2-D)/(2*H)
    equal(8*c**3-6*c-1, 0, 'defining cubic')
    equal(A[0]*w3/8+A[1]*w4/8, 1, 'dual first moment')
    equal(B[0]*w3/14+B[1]*w4/14, F(1, 2), 'dual second moment')
    equal(8-w3-w4, C, 'dual first-order constant')
    equal(det, -3*(c+d)/224, 'active constraint determinant')
    equal(aa, K((F(-5, 3), F(1, 3), 0)), 'mixed quartic constant')
    equal(qq, K((F(-3, 40), F(-1, 10), F(1, 5))),
          'fourth moment constant')
    equal(Bstar, K((F(2311, 108), F(4934, 27), F(-1976, 9))),
          'second-order coefficient normal form')
    equal(6*uz+2*up, U0, 'optimizer real mean')
    equal(H*up, J21, 'optimizer mixed moment')
    equal(A[0]*W/8+B[0]*D/14, targets[0], 'first quartic tangency')
    equal(A[1]*W/8+B[1]*D/14, targets[1], 'second quartic tangency')
    equal(U2-2*H*gamma, D, 'optimizer imaginary energy correction')
    equal(W+D/2+U2/2+8+2*U0-K(F(3, 2))*H
          -K(F(3, 2))*J21+K(F(3, 8))*J4,
          Bstar, 'explicit family second-order objective')

    lo, hi = F(3, 4), F(1)
    f = lambda t: 8*t**3-6*t-1
    require(f(lo) < 0 < f(hi) and 24*lo*lo-6 > 0,
            'monotone cubic isolation')
    checks += 1
    for _ in range(80):
        mid = (lo+hi)/2
        require(f(mid) != 0, 'cubic bisection avoided rational root')
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    require(f(lo) < 0 < f(hi), 'final cubic isolation')
    checks += 1

    def positive(a, label):
        nonlocal checks
        require(a.interval(lo, hi)[0] > 0, 'strict positive sign: '+label)
        checks += 1

    for label, value in [('H', H), ('w3', w3), ('w4', w4),
                         ('negative alpha', -alpha),
                         ('beta plus alpha/2', beta+alpha/2),
                         ('negative second coefficient', -Bstar),
                         ('nonactive first-root slack', 1-x*(1-d)-y*(1-v)),
                         ('nonactive second-root slack', 1-x*(1-v)-y*(1+c))]:
        positive(value, label)
    lb, ub = Bstar.interval(lo, hi)
    dec_lo, dec_hi = F(-754160683222, 10**12), F(-754160683221, 10**12)
    require(dec_lo < lb <= ub < dec_hi, 'second coefficient decimal enclosure')
    checks += 1
    records['second_coefficient_enclosure'] = [str(dec_lo), str(dec_hi)]
    records['embedding_interval'] = [str(lo), str(hi)]
    records['constants'] = {label: value.record() for label, value in
        [('c', c), ('d', d), ('v', v), ('x', x), ('y', y), ('H', H),
         ('U0', U0), ('C', C), ('w3', w3), ('w4', w4), ('L', L),
         ('mixed', aa), ('fourth', qq), ('alpha', alpha), ('beta', beta),
         ('const', const), ('base', base), ('Bstar', Bstar),
         ('u_zero', uz), ('u_pair', up), ('U2', U2), ('J21', J21),
         ('J4', J4), ('W', W), ('D', D), ('gamma', gamma)]}

    # Full definition-level eight-critical expansion with no assumed real
    # correction pattern. Only sum h=0 is eliminated in this calculation.
    ep, z = pv(0), pv(1)
    hs = [pv(i) for i in range(2, 9)]
    hs.append(pscale(padd(*hs), -1))
    us = [pv(i) for i in range(9, 17)]
    vs = [pv(i) for i in range(17, 25)]
    ws = [pv(i) for i in range(25, 33)]
    Um, Vm, Wm = padd(*us), padd(*vs), padd(*ws)
    Hm = padd(*(ppow(h, 2) for h in hs))
    J3m = padd(*(ppow(h, 3) for h in hs))
    J4m = padd(*(ppow(h, 4) for h in hs))
    J21m = padd(*(pmul(h, h, u) for h, u in zip(hs, us)))
    U2m = padd(*(ppow(u, 2) for u in us))
    Bm = pscale(padd(*(pmul(h, u) for h, u in zip(hs, us))), 2)
    Dm = padd(U2m, pscale(padd(*(pmul(h, vv) for h, vv in zip(hs, vs))), -2))
    criticals = [padd(pscale(pmul(ep, h), 0, 1),
                      pmul(ppow(ep, 2), u),
                      pscale(pmul(ppow(ep, 3), vv), 0, 1),
                      pmul(ppow(ep, 4), w))
                 for h, u, vv, w in zip(hs, us, vs, ws)]
    derivative = pscale(pmul(*(padd(z, pscale(cr, -1)) for cr in criticals)), 9)
    primitive = pint(derivative, 1)
    marked = padd(pc(1), pscale(ppow(ep, 2), -1))
    polynomial = padd(primitive, pscale(psubst(primitive, 1, marked), -1))
    diff = lambda n: padd(ppow(z, n), pc(-1))
    g2 = padd(pc(9), pscale(pmul(Um, diff(8)), F(-9, 8)),
              pscale(pmul(Hm, diff(7)), F(9, 14)))
    g3 = padd(pscale(pmul(Vm, diff(8)), 0, F(-9, 8)),
              pscale(pmul(Bm, diff(7)), 0, F(-9, 14)),
              pscale(pmul(J3m, diff(6)), 0, F(1, 2)))
    g4 = padd(pc(-36), pscale(Um, -9), pscale(Hm, F(9, 2)),
              pscale(pmul(Wm, diff(8)), F(-9, 8)),
              pscale(pmul(padd(ppow(Um, 2), pscale(Dm, -1)), diff(7)), F(9, 14)),
              pmul(padd(pscale(pmul(Um, Hm), F(-3, 4)),
                         pscale(J21m, F(3, 2))), diff(6)),
              pmul(padd(pscale(ppow(Hm, 2), F(9, 40)),
                         pscale(J4m, F(-9, 20))), diff(5)))
    expected_poly = padd(diff(9), pmul(ppow(ep, 2), g2),
                          pmul(ppow(ep, 3), g3), pmul(ppow(ep, 4), g4))
    equal(polynomial, expected_poly, 'full generic fourth-order anchored jet')
    equal(pdiff(expected_poly, 1), derivative, 'full generic derivative jet')
    equal(psubst(polynomial, 1, marked), {}, 'marked-root jet')
    realdist = padd(pc(1), pscale(pmul(ppow(ep, 2), padd(pc(1), us[0])), -1),
                     pscale(pmul(ppow(ep, 4), ws[0]), -1))
    imagdist = padd(pmul(ep, hs[0]), pmul(ppow(ep, 3), vs[0]))
    dist2 = padd(ppow(realdist, 2), ppow(imagdist, 2))
    delta = padd(dist2, pc(-1))
    reciprocal = padd(pc(1), pscale(delta, F(-1, 2)),
                       pscale(ppow(delta, 2), F(3, 8)))
    expected_rec = padd(pc(1), pmul(ppow(ep, 2),
        padd(pc(1), us[0], pscale(ppow(hs[0], 2), F(-1, 2)))),
        pmul(ppow(ep, 4), padd(ws[0], pscale(pmul(hs[0], vs[0]), -1),
          ppow(padd(pc(1), us[0]), 2),
          pscale(pmul(ppow(hs[0], 2), padd(pc(1), us[0])), F(-3, 2)),
          pscale(ppow(hs[0], 4), F(3, 8)))))
    equal(reciprocal, expected_rec, 'unconstrained scalar reciprocal jet')
    equal(pmul(ppow(reciprocal, 2), dist2), pc(1),
          'scalar reciprocal defining equation')
    records['generic_jets'] = {
        'epsilon_order': ORDER, 'variables': NV,
        'derivative_terms': len(derivative), 'derivative_hash': phash(derivative),
        'anchored_terms': len(polynomial), 'anchored_hash': phash(polynomial),
        'reciprocal_terms': len(reciprocal), 'reciprocal_hash': phash(reciprocal)}

    # Independently evaluate the active-root perturbation formula in the
    # exact quadratic Gaussian extension. Moment coefficients are free.
    roots = [Z((F(-1, 2), 0, 0, 1), q=sine2[0]),
             Z((-c, 0, 0, 1), q=sine2[1])]
    root_checks = []
    for j, omega in enumerate(roots):
        equal(omega*omega.conj(), 1, 'unit active root '+str(j))
        equal(omega**9, 1, 'ninth root identity '+str(j))
        equal(1-(omega**6).real_field(), C6[j], 'sixth harmonic '+str(j))
        equal(1-(omega**5).real_field(), C5[j], 'fifth harmonic '+str(j))
        g2w = 9+(omega**8-1)*(9*x)+(omega**7-1)*(9*y)
        motion = -g2w/9  # normalized delta_1 / omega
        equal(motion.real_field(), 0, 'active first radial motion '+str(j))
        curv = (motion*motion.conj()/2-4*motion**2
                -(omega**8*(8*x)+omega**7*(7*y))*motion).real_field()
        equal(curv, curvature[j], 'independent root curvature '+str(j))
        # With J3=1, B=2L, V=4B/7, the complete cubic radial term is zero.
        Bc = 2*L
        Vc = 4*Bc/7
        g3w = ((omega**8-1)*(-9*Vc/8)
                +(omega**7-1)*(-9*Bc/14)+(omega**6-1)/2)
        g3w *= Z((0, 0, 1, 0), q=omega.q)
        cubic = -g3w/9
        equal(cubic.real_field(), 0, 'independent cubic cancellation '+str(j))
        for label, term, expected in [
            ('W', (omega**8-1)*K(F(-9, 8)), -A[j]/8),
            ('D', (omega**7-1)*K(F(-9, 14)), -B[j]/14),
            ('J21', (omega**6-1)*K(F(3, 2)), C6[j]/6),
            ('J4', (omega**5-1)*K(F(-9, 20)), -C5[j]/20)]:
            equal((-term/9).real_field(), expected,
                  'generic radial coefficient '+label+' '+str(j))
        root_checks.append({'curvature': curv.record(),
                            'normalized_motion': motion.record(),
                            'cubic_cancellation': cubic.record()})
    records['active_root_checks'] = root_checks

    # Explicit symmetric disk-root candidate, including the fixed M=100
    # third-order inward repair. Its derivative and primitive are computed
    # from scratch in K[eta,z], not imported from the generic moment jet.
    eta = {(1, 0): K(1)}
    zz = {(0, 1): K(1)}
    M = 100
    shift = ka(ks(kp(eta, 2), W/8), ks(kp(eta, 3), M))
    rz = ka(ks(eta, uz), shift)
    rp = ka(ks(eta, up), shift)
    der = ks(km(kp(ka(zz, ks(rz, -1)), 6),
                ka(kp(ka(zz, ks(rp, -1)), 2),
                   ks(km(eta, kp(ka(kc(1), ks(eta, gamma)), 2)), H/2))), 9)
    prim = ki(der)
    a = ka(kc(1), ks(eta, -1))
    pol = ka(prim, ks(ksubz(prim, a), -1))
    equal(ksubz(pol, a), {}, 'explicit primitive marked root')
    equal({e: val for e, val in pol.items() if e[0] == 0},
          {(0, 9): K(1), (0, 0): K(-1)}, 'explicit limiting polynomial')
    construction = []
    for j, omega in enumerate(roots):
        p1, p2, p3 = (keval(pol, n, omega) for n in (1, 2, 3))
        r1 = -p1*omega/9
        r2 = -(p2+keval(pol, 1, omega, 1)*r1
                +omega**7*r1**2*36)*omega/9
        r3 = -(p3+keval(pol, 2, omega, 1)*r1
                +keval(pol, 1, omega, 1)*r2
                +keval(pol, 1, omega, 2)*r1**2/2
                +omega**7*r1*r2*72+omega**6*r1**3*84)*omega/9
        first = (r1*omega.conj()).real_field()
        second = (r2*omega.conj()+r1*r1.conj()/2).real_field()
        third = (r3*omega.conj()+r1*r2.conj()).real_field()
        equal(first, 0, 'explicit first tangency '+str(j))
        equal(second, 0, 'explicit second tangency '+str(j))
        positive(-third, 'explicit third-order inward root motion '+str(j))
        construction.append({'half_squared_modulus_eta3': third.record()})
    records['explicit_family'] = {
        'M': M, 'derivative_terms_through_eta3': len(der),
        'primitive_terms_through_eta3': len(pol),
        'primitive': krecord(pol), 'active_pairs': construction}

    # Definition-level objective from the six real and two conjugate
    # distances. Inverting the linear-distance polynomial gives the real
    # contribution; binomial expansion gives the nonreal contribution.
    realdist = ka(kc(1), ks(eta, -1), ks(rz, -1))
    pairdist = ka(kc(1), ks(eta, -1), ks(rp, -1))
    pairdist2 = ka(kp(pairdist, 2),
                   ks(km(eta, kp(ka(kc(1), ks(eta, gamma)), 2)), H/2))
    td = ka(realdist, kc(-1))
    invreal = ka(kc(1), ks(td, -1), kp(td, 2), ks(kp(td, 3), -1))
    td2 = ka(pairdist2, kc(-1))
    invpair = ka(kc(1), ks(td2, F(-1, 2)),
                 ks(kp(td2, 2), F(3, 8)), ks(kp(td2, 3), F(-5, 16)))
    total = ka(ks(invreal, 6), ks(invpair, 2))
    equal(total.get((0, 0)), 8, 'definition-level objective constant')
    equal(total.get((1, 0)), C, 'definition-level objective linear term')
    equal(total.get((2, 0)), Bstar, 'definition-level objective quadratic term')
    records['explicit_objective_jet'] = krecord(total)

    mutations = [
        reject(lambda: equal(Bstar+F(1, 100), base+alpha*H*H/2,
                             'altered second coefficient'), 'second coefficient'),
        reject(lambda: equal(A[1]*(W+1)/8+B[1]*D/14, targets[1],
                             'altered quartic tangency'), 'quartic correction'),
        reject(lambda: equal(aa+1, K((F(-5, 3), F(1, 3), 0)),
                             'altered mixed term'), 'mixed moment'),
        reject(lambda: equal(pscale(derivative, F(8, 9)),
                             pdiff(expected_poly, 1), 'altered degree'),
               'degree-nine factor'),
        reject(lambda: equal(padd(expected_rec, ppow(ep, 4)),
                             reciprocal, 'altered reciprocal'),
               'reciprocal coefficient'),
        reject(lambda: equal(2*L+1, -7*(2*c+1)/9,
                             'altered cubic moment relation'), 'cubic cancellation')]
    records['mutations_rejected'] = mutations
    records['exact_checks'] = checks
    records['trust_boundary'] = ('exact finite algebra only; concentration, '
        'rate bootstrap, moment inequality, uniform remainders and all-root '
        'disk containment are ordinary arguments in PROOF.md')
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
    digest = sha256(encoded.encode()).hexdigest()
    print('PASS: '+str(records['exact_checks'])+' exact checks; '
          +str(len(records['mutations_rejected']))+' mutations rejected.')
    print('Complete record SHA256: '+digest)
    print('Exact second-coefficient enclosure: '+
          str(records['second_coefficient_enclosure']))


if __name__ == '__main__':
    main()
