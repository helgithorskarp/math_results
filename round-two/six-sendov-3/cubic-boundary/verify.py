#!/usr/bin/env python3
"""Exact algebra for the third degree-nine first-power boundary coefficient.

Self-contained arithmetic kernels adapt six-sendov-3 profile-stability,
source3f74956df840a6763e34087e87323ded361cd1d0, with attribution.
Uniform analytic bridges and all-root disk coverage remain ordinary proof.
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


# Gaussian-rational moment jets: eta,z,ten real moments,six imaginary moments.
NV = 18
ORDER = 3
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


# Independent sparse K[eta,z,m,theta], retaining all eta orders <=4.
KNV = 4; KORDER = 4; KZERO = (0,)*KNV
def kpc(a=0):
    return {KZERO: K(a)} if K(a) != 0 else {}
def kpv(j):
    e = [0]*KNV; e[j] = 1
    return {tuple(e): K(1)}
def kadd(*ps):
    out = {}
    for p in ps:
        for e, a in p.items():
            out[e] = out.get(e, K(0))+a
            if out[e] == 0: del out[e]
    return out
def kscale(p, a):
    return {e: b for e, v in p.items() if (b := v*a) != 0}
def kmul(*ps):
    out = kpc(1)
    for p in ps:
        new = {}
        for e, a in out.items():
            for f, b in p.items():
                if e[0]+f[0] > KORDER: continue
                key = tuple(x+y for x, y in zip(e, f))
                new[key] = new.get(key, K(0))+a*b
                if new[key] == 0: del new[key]
        out = new
    return out
def kpower(p, n):
    return kmul(*([p]*n))
def kintegrate(p):
    out = {}
    for e, a in p.items():
        f = list(e); f[1] += 1
        out[tuple(f)] = a/f[1]
    return out
def ksubstitute(p, j, replacement):
    out = {}
    for e, a in p.items():
        f = list(e); n = f[j]; f[j] = 0
        out = kadd(out, kmul({tuple(f): a}, kpower(replacement, n)))
    return out
def kcoefficient(p, order):
    return {tuple([0]+list(e[1:])): a for e, a in p.items() if e[0] == order}
def kevaluate(p, order, omega, mm=0, tt=0, derivative=0):
    out = Z(0, q=omega.q)
    for (a, b, g, h), coeff in p.items():
        if a == order and b >= derivative:
            coeff *= K(mm)**g*K(tt)**h
            for j in range(derivative): coeff *= b-j
            out += omega**(b-derivative)*coeff
    return out
def kphash(p):
    record = [[list(e), a.record()] for e, a in sorted(p.items())]
    return sha256(json.dumps(record, separators=(',', ':')).encode()).hexdigest()


def generic_moments(equal):
    """Full Newton/integration identity; imaginary moments have their proved orders."""
    eta, z = pv(0), pv(1)
    U, H, W, D, J21, U3, J4, J22, J41, J6 = [pv(j) for j in range(2, 12)]
    ims = [pv(j) for j in range(12, 18)]
    e2, e3 = ppow(eta, 2), ppow(eta, 3)
    powers = [None,
        padd(pmul(U, eta), pmul(W, e2), pscale(pmul(ims[0], e2), 0, 1)),
        padd(pscale(pmul(H, eta), -1), pmul(D, e2),
             pscale(pmul(ims[1], e2), 0, 1)),
        padd(pscale(pmul(J21, e2), -3), pmul(U3, e3),
             pscale(pmul(ims[2], e2), 0, 1)),
        padd(pmul(J4, e2), pscale(pmul(J22, e3), -6),
             pscale(pmul(ims[3], e3), 0, 1)),
        padd(pscale(pmul(J41, e3), 5), pscale(pmul(ims[4], e3), 0, 1)),
        padd(pscale(pmul(J6, e3), -1), pscale(pmul(ims[5], e3), 0, 1)),
        pc(), pc()]
    elementary = [pc(1)]
    for n in range(1, 9):
        elementary.append(pscale(padd(*(pscale(pmul(elementary[n-j], powers[j]),
            (-1)**(j-1)) for j in range(1, n+1))), F(1, n)))
    der = pscale(padd(*(pscale(pmul(elementary[j], ppow(z, 8-j)), (-1)**j)
                        for j in range(9))), 9)
    primitive = pint(der, 1)
    marked = padd(pc(1), pscale(eta, -1))
    pol = padd(primitive, pscale(psubst(primitive, 1, marked), -1))
    equal(psubst(pol, 1, marked), {}, 'generic Newton anchor')
    real = {e: (a, F(0)) for e, (a, b) in pol.items() if a}
    diff = lambda n: padd(ppow(z, n), pc(-1))
    g2 = padd(pc(9), pscale(pmul(U, diff(8)), F(-9, 8)),
              pscale(pmul(H, diff(7)), F(9, 14)))
    g4 = padd(pc(-36), pscale(U, -9), pscale(H, F(9, 2)),
        pscale(pmul(W, diff(8)), F(-9, 8)),
        pscale(pmul(padd(ppow(U, 2), pscale(D, -1)), diff(7)), F(9, 14)),
        pmul(padd(pscale(pmul(U, H), F(-3, 4)), pscale(J21, F(3, 2))), diff(6)),
        pmul(padd(pscale(ppow(H, 2), F(9, 40)), pscale(J4, F(-9, 20))), diff(5)))
    K6 = padd(pc(84), pscale(U, F(63, 2)), pscale(H, F(-27, 2)),
        pscale(W, -9), pscale(padd(ppow(U, 2), pscale(D, -1)), F(9, 2)),
        pscale(pmul(U, H), F(-9, 2)), pscale(J21, 9),
        pscale(ppow(H, 2), F(9, 8)), pscale(J4, F(-9, 4)))
    c7 = pscale(pmul(U, W), F(9, 7))
    c6 = padd(pscale(ppow(U, 3), F(-1, 4)),
        pscale(padd(pmul(U, D), pscale(pmul(H, W), -1)), F(3, 4)),
        pscale(U3, F(-1, 2)))
    c5 = pscale(padd(pscale(pmul(U, U, H), F(1, 4)),
        pscale(pmul(H, D), F(-1, 4)), pscale(pmul(U, J21), -1),
        pscale(J22, F(3, 2))), F(9, 5))
    c4 = pscale(padd(pscale(pmul(U, H, H), F(1, 8)),
        pscale(pmul(H, J21), F(-1, 2)), pscale(pmul(U, J4), F(-1, 4)),
        J41), F(-9, 4))
    c3 = pscale(padd(pscale(ppow(H, 3), F(1, 48)),
        pscale(pmul(H, J4), F(-1, 8)), pscale(J6, F(1, 6))), 3)
    g6 = padd(K6, *(pmul(a, diff(n)) for n, a in [(7,c7),(6,c6),(5,c5),(4,c4),(3,c3)]))
    predicted = padd(diff(9), pmul(eta, g2), pmul(e2, g4), pmul(e3, g6))
    equal(real, predicted, 'complete generic real polynomial through eta3')
    equal(all(e[0] >= 2 for e,(a,b) in pol.items() if b),
          True, 'imaginary moment polynomial starts at eta2')

    # One exact inverse-distance series and its complete moment-sum substitution.
    h, u = pv(2), pv(3)
    q = padd(pc(1), u)
    distance = padd(ppow(padd(pc(1), pscale(pmul(eta, q), -1)), 2),
                    pmul(eta, h, h))
    delta = padd(distance, pc(-1))
    inverse = padd(*(pscale(ppow(delta, j), a) for j,a in enumerate(
        [F(1),F(-1,2),F(3,8),F(-5,16)])))
    single2 = padd(ppow(q, 2), pscale(pmul(h,h,q), F(-3,2)),
                   pscale(ppow(h, 4), F(3,8)))
    single3 = padd(ppow(q, 3), pscale(pmul(h,h,q,q), -3),
        pscale(pmul(ppow(h,4),q), F(15,8)), pscale(ppow(h,6), F(-5,16)))
    predicted_single = padd(pc(1), pmul(eta,padd(q,pscale(ppow(h,2),F(-1,2)))),
        pmul(e2,single2),pmul(e3,single3))
    equal(inverse,predicted_single,'generic scalar inverse-distance through eta3')
    U2 = pv(12)
    Um = padd(U,pmul(eta,W)); Hm = padd(H,pmul(eta,padd(U2,pscale(D,-1))))
    total2 = padd(pc(8),pscale(Um,2),U2,pscale(Hm,F(-3,2)),
                 pscale(J21,F(-3,2)),pscale(J4,F(3,8)))
    total3 = padd(pc(8),pscale(Um,3),pscale(U2,3),U3,pscale(Hm,-3),
                 pscale(J21,-6),pscale(J22,-3),pscale(J4,F(15,8)),
                 pscale(J41,F(15,8)),pscale(J6,F(-5,16)))
    total = padd(pc(8),pmul(eta,padd(pc(8),Um,pscale(Hm,F(-1,2)))),
                 pmul(e2,total2),pmul(e3,total3))
    want2 = padd(W,pscale(D,F(1,2)),pscale(U2,F(1,2)),pc(8),pscale(U,2),
                 pscale(H,F(-3,2)),pscale(J21,F(-3,2)),pscale(J4,F(3,8)))
    want3 = padd(pscale(W,2),pscale(padd(U2,pscale(D,-1)),F(-3,2)),
                 pc(8),pscale(U,3),pscale(U2,3),U3,pscale(H,-3),
                 pscale(J21,-6),pscale(J22,-3),pscale(J4,F(15,8)),
                 pscale(J41,F(15,8)),pscale(J6,F(-5,16)))
    want = padd(pc(8),pmul(eta,padd(pc(8),U,pscale(H,F(-1,2)))),
                pmul(e2,want2),pmul(e3,want3))
    equal(total,want,'complete generic summed scalar and exact mean/norm substitution')
    record={'variables':NV,'eta_order':ORDER,'derivative_terms':len(der),
        'derivative_hash':phash(der),'anchored_terms':len(pol),'anchored_hash':phash(pol),
        'g6_terms':len(g6),'g6_hash':phash(g6),'scalar_hash':phash(total)}
    return record,real,predicted,inverse,predicted_single


def residual_roots(poly, omega, mm, tt):
    """Independent implicit solving by complete polynomial residual coefficients."""
    zero=lambda:[Z(0,q=omega.q) for _ in range(KORDER+1)]
    def add(a,b):return [x+y for x,y in zip(a,b)]
    def mul(a,b):
        out=zero()
        for i,x in enumerate(a):
            for j,y in enumerate(b[:KORDER+1-i]):
                out[i+j]+=x*y
        return out
    byz={}
    for (a,b,g,h),v in poly.items():
        byz.setdefault(b,zero())[a]+=v*K(mm)**g*K(tt)**h
    def evaluate(r):
        ans=zero()
        for b in range(9,-1,-1):ans=add(mul(ans,r),byz.get(b,zero()))
        return ans
    r=zero();r[0]=omega
    for n in range(1,KORDER+1):
        # r_n=0 here; p0'(omega)=9/omega determines the new coefficient.
        residual=evaluate(r)[n]
        r[n]=-residual*omega/9
    residual=evaluate(r)
    rad=[]
    for n in range(1,KORDER+1):
        coeff=sum((r[j]*r[n-j].conj() for j in range(n+1)),
                  Z(0,q=omega.q))/2
        rad.append(coeff.real_field())
    return r,residual,rad,evaluate


def build_record():
    checks=0
    def equal(a,b,label):
        nonlocal checks
        require(a==b,label); checks+=1
    def reject(fn,label):
        nonlocal checks
        try:fn()
        except AlgebraError:
            checks+=1;return label
        raise AlgebraError('mutation not rejected: '+label)
    lo,hi=F(3,4),F(1)
    f=lambda t:8*t**3-6*t-1
    equal(f(lo)<0<f(hi) and 24*lo*lo-6>0,True,'cubic embedding isolation')
    for _ in range(80):
        mid=(lo+hi)/2
        if f(mid)<0:lo=mid
        else:hi=mid
    equal(f(lo)<0<f(hi),True,'refined cubic embedding isolation')
    # Credited prior finite coefficients are reconstructed below from factors.
    fixture={'constants': {'Bstar': ['2311/108', '4934/27', '-1976/9']}, 'two_pair_family': {'inward_third_at_sigma0': [['-5378807/10368', '-19292351/10368', '345355/144'], ['-3572867/186624', '4372007/10368', '-1667129/2592']], 'objective_eta3_at_sigma0': ['-2367865/5184', '-32430797/5184', '15660043/1944']}}
    c = K((0, 1, 0)); d = 2*c*c-1; v = 2*d*d-1
    y = 1/(3*(1+c)); x = K(F(2, 3))-y
    H = 14*y; U0 = -8*x; C = K(F(8, 3))+y
    rho = (c-5)/3; uz = (U0+rho*H)/8; up = uz-rho*H/2
    w4 = 1/(c+d); w3 = K(F(2, 3))*(7-(1-d)*w4)
    sigma = K(F(3, 8))-(K(F(3, 2))*w3+(1-v)*w4)/20
    Bstar = K(fixture['constants']['Bstar'])
    A = [K(F(3, 2)), 1+c]; B = [K(F(3, 2)), 1-d]
    sine2 = [K(F(3, 4)), 1-c*c]
    roots = [Z((F(-1, 2), 0, 0, 1), q=sine2[0]),
             Z((-c, 0, 0, 1), q=sine2[1])]
    U2 = 6*uz**2+2*up**2; U3 = 6*uz**3+2*up**3
    J21 = H*up; J22 = H*up**2; J4 = H**2/2
    J41 = H**2*up/2; J6 = H**3/4
    T = []
    for aj, bj, c6, c5, ratio, sn in zip(A, B, [K(0), K(F(3, 2))],
            [K(F(3, 2)), 1-v], [K(-1), -2*c], sine2):
        curv = -(K(F(7, 2))*x*x+6*x*y*ratio+K(F(5, 2))*y*y*ratio**2)*sn
        T.append(4+U0-H/2+bj*U0**2/14+c6*(-U0*H/12+J21/6)
                 +c5*(H**2/40-J4/20)+curv)
    det = (A[0]*B[1]-A[1]*B[0])/112
    W = (T[0]*B[1]/14-T[1]*B[0]/14)/det
    D = (A[0]*T[1]/8-A[1]*T[0]/8)/det
    gamma = (U2-D)/(2*H)
    R100 = [K(a) for a in fixture['two_pair_family']['inward_third_at_sigma0']]
    O100 = K(fixture['two_pair_family']['objective_eta3_at_sigma0'])
    C3 = O100+w3*R100[0]+w4*R100[1]
    aa, bb = -A[0], H*B[0]/7
    cc, dd = -A[1], H*B[1]/7
    det3 = aa*dd-cc*bb
    m = 100+(-R100[0]*dd+R100[1]*bb)/det3
    theta = (-aa*R100[1]+cc*R100[0])/det3

    eta, z, mv, tv = [kpv(i) for i in range(4)]
    marked = kadd(kpc(1), kscale(eta, -1))
    shift = kadd(kscale(kpower(eta, 2), W/8), kmul(mv, kpower(eta, 3)))
    L0 = kadd(kscale(eta, uz), shift); Lp = kadd(kscale(eta, up), shift)
    imfac = kpower(kadd(kpc(1), kscale(eta, gamma), kmul(tv, kpower(eta, 2))), 2)
    der = kscale(kmul(kpower(kadd(z, kscale(L0, -1)), 6),
        kadd(kpower(kadd(z, kscale(Lp, -1)), 2),
            kscale(kmul(eta, imfac), H/2))), 9)
    primitive = kintegrate(der)
    pol = kadd(primitive, kscale(ksubstitute(primitive, 1, marked), -1))
    equal(ksubstitute(pol, 1, marked), {}, 'anchored original root')
    equal(kcoefficient(pol, 0), kadd(kpower(z, 9), kpc(-1)), 'limiting nonagon')
    require(all(e[2] == e[3] == 0 for e in pol if e[0] < 3),
            'corrections start only at order three'); checks += 1
    require(all(e[2]+e[3] <= 1 for e in pol if e[0] == 3),
            'third kcoefficient affine in both independent corrections'); checks += 1
    base3 = ksubstitute(ksubstitute(kcoefficient(pol, 3), 2, {}), 3, {})
    predicted3 = kadd(base3,
        kscale(kmul(mv, kadd(kpower(z, 8), kpc(-1))), -9),
        kscale(kmul(tv, kadd(kpower(z, 7), kpc(-1))), 9*H/7))
    equal(kcoefficient(pol, 3), predicted3, 'complete free third polynomial response')

    def root_jets(poly, omega, mm, tt):
        ev = lambda order, derivative=0: kevaluate(poly, order, omega, mm, tt, derivative)
        r1 = -ev(1)*omega/9
        r2 = -(ev(2)+ev(1, 1)*r1+omega**7*r1**2*36)*omega/9
        r3 = -(ev(3)+ev(2, 1)*r1+ev(1, 1)*r2+ev(1, 2)*r1**2/2
            +omega**7*r1*r2*72+omega**6*r1**3*84)*omega/9
        r4 = -(ev(4)+ev(3, 1)*r1+ev(2, 1)*r2+ev(2, 2)*r1**2/2
            +ev(1, 1)*r3+ev(1, 2)*r1*r2+ev(1, 3)*r1**3/6
            +omega**7*(2*r1*r3+r2**2)*36
            +omega**6*r1**2*r2*252+omega**5*r1**4*126)*omega/9
        radial = [(r1*omega.conj()).real_field(),
            (r2*omega.conj()+r1*r1.conj()/2).real_field(),
            (r3*omega.conj()+r1*r2.conj()).real_field(),
            (r4*omega.conj()+r1*r3.conj()+r2*r2.conj()/2).real_field()]
        return radial

    radials = []
    for j, omega in enumerate(roots):
        equal(omega**9, 1, 'exact active ninth root')
        radial100 = root_jets(pol, omega, 100, 0)
        equal(radial100[2], R100[j], 'previous inward cubic kcoefficient')
        rr = root_jets(pol, omega, m, theta)
        for n in range(3): equal(rr[n], 0, 'active tangency order '+str(n+1))
        radials.append(rr)

    # Generic objective through fourth order, retaining both free corrections.
    def inverse(p):
        delta = kadd(p, kpc(-1))
        return kadd(*(kscale(kpower(delta, j), (-1)**j) for j in range(KORDER+1)))
    def inverse_sqrt(p):
        delta = kadd(p, kpc(-1))
        return kadd(*(kscale(kpower(delta, j), a) for j, a in enumerate(
            [F(1), F(-1, 2), F(3, 8), F(-5, 16), F(35, 128)])))
    dist0 = kadd(marked, kscale(L0, -1))
    distpair = kadd(kpower(kadd(marked, kscale(Lp, -1)), 2), kscale(kmul(eta, imfac), H/2))
    objective = kadd(kscale(inverse(dist0), 6), kscale(inverse_sqrt(distpair), 2))
    equal(kcoefficient(objective, 0), kpc(8), 'objective constant')
    equal(kcoefficient(objective, 1), kpc(C), 'objective linear kcoefficient')
    equal(kcoefficient(objective, 2), kpc(Bstar), 'objective quadratic kcoefficient')
    third = kcoefficient(objective, 3)
    equal(third, kadd(kpc(O100-800), kscale(mv, 8), kscale(tv, -H)),
          'complete objective affine third response')
    equal(ksubstitute(ksubstitute(third, 2, kpc(m)), 3, kpc(theta)), kpc(C3),
          'candidate third kcoefficient from actual critical distances')

    # Independent generic real-kcoefficient expansion at the limiting profile.
    diff = lambda n: kadd(kpower(z, n), kpc(-1))
    g2 = kadd(kpc(9), kscale(diff(8), -9*U0/8), kscale(diff(7), 9*H/14))
    g4 = kadd(kpc(-36-9*U0+9*H/2), kscale(diff(8), -9*W/8),
        kscale(diff(7), 9*(U0**2-D)/14),
        kscale(diff(6), -3*U0*H/4+3*J21/2),
        kscale(diff(5), 9*H**2/40-9*J4/20))
    constant6 = (84+K(F(63, 2))*U0-K(F(27, 2))*H-9*W
        +K(F(9, 2))*(U0**2-D)-K(F(9, 2))*U0*H
        +9*J21+K(F(9, 8))*H**2-K(F(9, 4))*J4)
    g6 = kadd(kpc(constant6), kscale(diff(7), 9*U0*W/7),
        kscale(diff(6), -U0**3/4+3*(U0*D-H*W)/4-U3/2),
        kscale(diff(5), K(F(9, 5))*(U0**2*H/4-H*D/4-U0*J21+3*J22/2)),
        kscale(diff(4), -K(F(9, 4))*(U0*H**2/8-H*J21/2-U0*J4/4+J41)),
        kscale(diff(3), 3*(H**3/48-H*J4/8+J6/6)))
    limitpoly = kadd(diff(9), kmul(eta, g2), kmul(kpower(eta, 2), g4),
                    kmul(kpower(eta, 3), g6))
    limit_radial3 = [root_jets(limitpoly, w, 0, 0)[2] for w in roots]
    Theta = uz*W+(rho*up+sigma*H)*(U2-D)
    pairh2 = H/2
    f3 = (2*W-K(F(3, 2))*(U2-D)+6*(1+uz)**3
        +2*((1+up)**3-3*pairh2*(1+up)**2
            +K(F(15, 8))*pairh2**2*(1+up)-K(F(5, 16))*pairh2**3))
    candidate_global_cost = Theta+f3+w3*limit_radial3[0]+w4*limit_radial3[1]
    equal(candidate_global_cost, C3, 'independent normalization/root/scalar third cost')

    # A common eta^4 real repair makes both previously tangent pairs inward.
    R4 = [rr[3] for rr in radials]
    repair = 1
    while any((repair*A[j]-R4[j]).interval(lo, hi)[0] <= 0 for j in range(2)):
        repair *= 10
    require(repair <= 1000000, 'bounded explicit fourth repair'); checks += 1
    repaired_shift = kadd(shift, kscale(kpower(eta, 4), repair))
    L0r = kadd(kscale(eta, uz), repaired_shift); Lpr = kadd(kscale(eta, up), repaired_shift)
    derr = kscale(kmul(kpower(kadd(z, kscale(L0r, -1)), 6),
        kadd(kpower(kadd(z, kscale(Lpr, -1)), 2), kscale(kmul(eta, imfac), H/2))), 9)
    primr = kintegrate(derr)
    polr = kadd(primr, kscale(ksubstitute(primr, 1, marked), -1))
    inward = []
    for j, omega in enumerate(roots):
        rr = root_jets(polr, omega, m, theta)
        for n in range(3): equal(rr[n], 0, 'repair preserves lower tangency')
        equal(rr[3], R4[j]-repair*A[j], 'repair response at fourth order')
        require((-rr[3]).interval(lo, hi)[0] > 0, 'strict fourth inward sign'); checks += 1
        inward.append(rr[3].record())
    require((-C3).interval(lo, hi)[0] > 0, 'negative candidate kcoefficient'); checks += 1


    moment_record,real,predicted,scalar,scalar_prediction=generic_moments(equal)
    equal(up+rho*H/2,uz,'normalization u gradient')
    equal(2*rho*up+2*sigma*H,2*(rho*up+sigma*H),
          'normalization h gradient')
    equal(repair,10,'fixed fourth inward repair')
    profile_rate_squared=H*gamma*gamma+W*W/8
    equal(profile_rate_squared.interval(lo,hi)[0]>0,True,
          'positive optimal joint profile rate')
    # All nine original branches, including every conjugate and marked root.
    omega1=Z((d,0,0,1),q=1-d*d)
    omega2=Z((v,0,0,1),q=1-v*v)
    allroots=[Z(1,q=0),omega1,omega2,*roots,roots[1].conj(),
              roots[0].conj(),omega2.conj(),omega1.conj()]
    branch_record=[]; mutating_branch=None
    for j,omega in enumerate(allroots):
        equal(omega**9,1,'nine-branch ninth-root identity '+str(j))
        r,residual,rad,evaluate_root=residual_roots(polr,omega,m,theta)
        equal(all(x==0 for x in residual),True,'full root residual '+str(j))
        equal(rad,root_jets(polr,omega,m,theta),'two independent radial routes '+str(j))
        if j==0:
            equal(r,[omega,Z(-1,q=0),Z(0,q=0),Z(0,q=0),Z(0,q=0)],
                  'exact marked original root')
        elif j in (1,2,7,8):
            equal((-rad[0]).interval(lo,hi)[0]>0,True,
                  'inactive first radial sign '+str(j))
        else:
            equal(rad[:3],[K(0)]*3,'active tangencies through cubic '+str(j))
            equal((-rad[3]).interval(lo,hi)[0]>0,True,
                  'active fourth inward sign '+str(j))
        raw=json.dumps([a.record() for a in r],separators=(',',':')).encode()
        branch_record.append({'index':j,'jet_hash':sha256(raw).hexdigest(),
                               'radial':[a.record() for a in rad]})
        if j==4:mutating_branch=(r,evaluate_root)
    wrong=list(mutating_branch[0]);wrong[3]=wrong[3]+1
    mutations=[
        reject(lambda:equal(real,pscale(predicted,-1),'altered generic real sign'),
               'generic Newton real sign'),
        reject(lambda:equal(scalar,pscale(scalar_prediction,-1),'altered scalar jet'),
               'scalar coefficient sign'),
        reject(lambda:equal(candidate_global_cost-Theta,C3,'omitted normalization cost'),
               'normalization cost'),
        reject(lambda:equal(kcoefficient(pol,3),kscale(predicted3,-1),
                            'altered independent radius response'),'radius response'),
        reject(lambda:equal(all(x==0 for x in mutating_branch[1](wrong)),True,
                            'altered cubic root coefficient'),'root residual'),
        reject(lambda:equal(inward[0],[str(-F(x)) for x in inward[0]],
                            'reversed inward sign'),'inward radial sign')]
    return {'constants':{'C':C.record(),'Bstar':Bstar.record(),'C3':C3.record(),
        'H':H.record(),'U0':U0.record(),'rho':rho.record(),'u_zero':uz.record(),
        'u_pair':up.record(),'Wstar':W.record(),'Dstar':D.record(),'gamma':gamma.record(),
        'eta3_shift':m.record(),'radius_eta2_correction':theta.record(),
        'profile_rate_squared':profile_rate_squared.record(),
        'normalization_cost':Theta.record(),'scalar_eta3_cost':f3.record(),
        'radial_eta3_cost':[a.record() for a in limit_radial3]},
        'embedding_interval':[str(lo),str(hi)],'generic_moments':moment_record,
        'construction':{'eta_order':KORDER,'variables':KNV,'family_terms':len(pol),
            'family_hash':kphash(pol),'repaired_family_hash':kphash(polr),
            'objective_hash':kphash(objective),'common_eta4_repair':repair,
            'all_nine_root_branches':branch_record},'exact_checks':checks,
        'mutations_rejected':mutations,
        'trust_boundary':'finite exact algebra; concentration, uniform remainders, '
            'active slack and odd root-map bootstrap, projection/Young absorption '
            'and all-root containment are ordinary written proofs'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit-fixture',action='store_true')
    parser.add_argument('--fixture',type=Path,default=Path(__file__).with_name('expected.json'))
    args=parser.parse_args()
    fixture=None
    if not args.emit_fixture:
        require(args.fixture.is_file(),'required fixture missing')
        try:fixture=json.loads(args.fixture.read_text())
        except (OSError,ValueError) as e:raise AlgebraError('required fixture malformed') from e
        require(isinstance(fixture,dict),'required fixture must be an object')
    record=build_record();encoded=json.dumps(record,sort_keys=True,indent=2)+'\n'
    if args.emit_fixture:
        print(encoded,end='');return
    require(fixture==record,'complete fixture differs')
    print('PASS: '+str(record['exact_checks'])+' exact checks; '+
          str(len(record['mutations_rejected']))+' mutations rejected; all nine root branches.')
    print('Complete record SHA256: '+sha256(encoded.encode()).hexdigest())


if __name__=='__main__':main()
