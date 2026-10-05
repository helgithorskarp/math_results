#!/usr/bin/env python3
"""Finite algebra for the exact-minimum Sendov skew germ; not an analytic proof.

The cubic-field arithmetic follows six-sendov-3 analytic-boundary/algebra.py,
commit ac6099018ea9e0e8e3092122db6ff24d549ebf32, with attribution.  The
literal directional reconstruction, full cubic moment and bordered matrix are
fresh here.  Only Python standard-library exact rational arithmetic is used.
No predecessor program, fixture or experimental data is imported.
"""
from fractions import Fraction as F
import argparse
import json
from pathlib import Path


class CertificateError(RuntimeError):
    pass


def need(ok, label):
    if not ok:
        raise CertificateError(label)


class K:
    """Characteristic-zero Q[c]/(c^3-3c/4-1/8), basis (1,c,c^2)."""
    def __init__(self, x=0):
        if isinstance(x, K):
            self.a = x.a
        elif isinstance(x, (tuple, list)):
            need(len(x) == 3, 'field normal-form length')
            self.a = tuple(F(y) for y in x)
        else:
            self.a = (F(x), F(0), F(0))

    def __add__(self, x):
        return K(tuple(a+b for a, b in zip(self.a, K(x).a)))
    __radd__ = __add__
    def __neg__(self):
        return K(tuple(-a for a in self.a))
    def __sub__(self, x):
        return self + -K(x)
    def __rsub__(self, x):
        return K(x) + -self
    def __mul__(self, x):
        q = [F(0)]*5
        for i, a in enumerate(self.a):
            for j, b in enumerate(K(x).a):
                q[i+j] += a*b
        for i in (4, 3):
            q[i-2] += F(3, 4)*q[i]
            q[i-3] += F(1, 8)*q[i]
        return K(tuple(q[:3]))
    __rmul__ = __mul__
    def __pow__(self, n):
        need(isinstance(n, int) and n >= 0, 'field nonnegative exponent')
        out = K(1)
        for _ in range(n):
            out *= self
        return out
    def inv(self):
        cols = [(self*K(tuple(int(i == j) for i in range(3)))).a
                for j in range(3)]
        a = [[cols[j][i] for j in range(3)] + [F(i == 0)] for i in range(3)]
        for j in range(3):
            p = next((i for i in range(j, 3) if a[i][j]), None)
            need(p is not None, 'nonzero field divisor')
            a[j], a[p] = a[p], a[j]
            t = a[j][j]
            a[j] = [v/t for v in a[j]]
            for i in range(3):
                if i != j:
                    t = a[i][j]
                    a[i] = [v-t*w for v, w in zip(a[i], a[j])]
        out = K(tuple(a[i][3] for i in range(3)))
        need(self*out == 1, 'whole field inverse product')
        return out
    def __truediv__(self, x):
        return self*K(x).inv()
    def __rtruediv__(self, x):
        return K(x)*self.inv()
    def __eq__(self, x):
        return self.a == K(x).a
    def __bool__(self):
        return any(self.a)
    def record(self):
        return [str(v) for v in self.a]
    def interval(self, lo, hi):
        lower = upper = self.a[0]
        for i in (1, 2):
            ends = (self.a[i]*lo**i, self.a[i]*hi**i)
            lower += min(ends)
            upper += max(ends)
        return lower, upper


def jconst(x, n=2):
    return [K(x)] + [K(0)]*n


def jadd(*items):
    return [sum((x[i] for x in items), K(0)) for i in range(len(items[0]))]


def jscale(x, k):
    return [v*k for v in x]


def jmul(*items):
    n = len(items[0])-1
    out = jconst(1, n)
    for x in items:
        nxt = jconst(0, n)
        for i in range(n+1):
            for j in range(n+1-i):
                nxt[i+j] += out[i]*x[j]
        out = nxt
    return out


def jpow(x, n):
    return jmul(*([x]*n)) if n else jconst(1, len(x)-1)


def jinv(x):
    out = jconst(0, len(x)-1)
    out[0] = 1/x[0]
    for i in range(1, len(x)):
        out[i] = -sum((x[j]*out[i-j] for j in range(1, i+1)), K(0))/x[0]
    need(jmul(x, out) == jconst(1, len(x)-1), 'whole truncated inverse')
    return out


def constants():
    c = K((0, 1, 0))
    H = 14/(3*(1+c))
    b2 = H/2
    U = -8*(F(2, 3)-1/(3*(1+c)))
    rho = (c-5)/3
    L = -7*(2*c+1)/18
    uz = (U+rho*H)/8
    up = uz-rho*H/2
    aT = K((F(-11564, 405), F(-20482, 81), F(123284, 405)))
    bT = K((F(49, 180), F(-105889, 486), F(305123, 1215)))
    alpha = K((F(-527, 360), F(41, 90), F(13, 90)))
    kappa = (L+rho)**2/2+10*alpha/27
    gamma = 4*(aT+6*bT)/(27*H**3)
    w4 = 1/(c+2*c*c-1)
    w3 = 2*(7-(2-2*c*c)*w4)/3
    sigma = K((F(-3, 40), F(-1, 10), F(1, 5)))
    K0 = K((F(-2609, 405), F(-2000, 81), F(12964, 405)))
    Bstar = K((F(2311, 108), F(4934, 27), F(-1976, 9)))
    return locals()


def literal_direction(v, k):
    """Entire degree-two literal eta=0 chart cost for t_i=v_i q,r_i=v_{6+i}q.

    h_small=b*t, h_head=b*(m+-s); the positive square root has the
    complete degree-two jet s=1-T/4-S^2/8. All square roots cancel in
    the mixed equation and the cost. All six small multiplicities remain.
    """
    t = [[K(0), K(v[i]), K(0)] for i in range(6)]
    rr = [[K(0), K(v[6+i]), K(0)] for i in range(6)]
    S, T = jadd(*t), jadd(*(jpow(x, 2) for x in t))
    m = jscale(S, F(-1, 2))
    s = jadd(jconst(1), jscale(T, F(-1, 4)), jscale(jpow(S, 2), F(-1, 8)))
    need(jpow(s, 2) == jadd(jconst(1), jscale(T, F(-1, 2)),
                           jscale(jpow(S, 2), F(-1, 4))), 'whole positive square-root jet')
    hs = [jadd(m, s), jadd(m, jscale(s, -1))] + t
    us = [jadd(jconst(k['uz']), x) for x in rr]
    mu = jscale(jadd(jconst(k['U']), jscale(jadd(*us), -1)), F(1, 2))
    Jt = jadd(*(jpow(x, 3) for x in hs))
    N = jadd(jscale(Jt, k['L']*k['b2']), jscale(jmul(m, mu), -2),
             jscale(jadd(*(jmul(t[i], us[i]) for i in range(6))), -1))
    du = jscale(jmul(N, jinv(s)), F(1, 2))
    uu = [jadd(mu, du), jadd(mu, jscale(du, -1))] + us
    need(jadd(*hs) == jconst(0), 'all-eight literal imaginary mean')
    need(jadd(*(jpow(x, 2) for x in hs)) == jconst(2), 'all-eight literal imaginary norm')
    need(jadd(*uu) == jconst(k['U']), 'all-eight literal real mean')
    need(jadd(*(jmul(hs[i], uu[i]) for i in range(8))) == jscale(Jt, k['L']*k['b2']),
         'all-eight literal mixed constraint')
    cost = jadd(jconst(k['K0']), jscale(jadd(*(jpow(x, 2) for x in uu)), F(1, 2)),
                jscale(jadd(*(jmul(jpow(hs[i], 2), uu[i]) for i in range(8))), k['rho']*k['b2']),
                jscale(jadd(*(jpow(x, 4) for x in hs)), k['sigma']*k['b2']**2))
    need(cost[0] == k['Bstar'] and cost[1] == 0, 'literal constant and gradient')
    return cost[2]


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), K(0))


def mv(a, x):
    return [dot(row, x) for row in a]


def determinant(a):
    n = len(a)
    need(all(len(row) == n for row in a), 'square determinant matrix')
    m = [row[:] for row in a]
    out = K(1)
    for j in range(n):
        p = next((i for i in range(j, n) if m[i][j]), None)
        if p is None:
            return K(0)
        if p != j:
            m[j], m[p] = m[p], m[j]
            out = -out
        q = m[j][j]
        out *= q
        for i in range(j+1, n):
            t = m[i][j]/q
            for l in range(j, n):
                m[i][l] -= t*m[j][l]
    return out


def padd(*ps):
    out = {}
    for p in ps:
        for e, c in p.items():
            out[e] = out.get(e, K(0))+c
            if not out[e]:
                del out[e]
    return out


def pscale(p, a):
    return {e:c*a for e, c in p.items() if c*a}


def pmul(*ps):
    out = {(0,)*6:K(1)}
    for p in ps:
        nxt = {}
        for e, a in out.items():
            for f, b in p.items():
                t = tuple(x+y for x, y in zip(e, f))
                nxt[t] = nxt.get(t, K(0))+a*b
        out = {e:c for e, c in nxt.items() if c}
    return out


def build(damage=None):
    k = constants()
    H, b2, aT, bT, gamma = (k[x] for x in ('H', 'b2', 'aT', 'bT', 'gamma'))
    c = k['c']
    need(8*c**3-6*c-1 == 0, 'minimal polynomial')
    need(gamma == k['kappa']/H, 'gamma equals credited kappa over H')
    Mscaled = [[K(0) for _ in range(12)] for _ in range(12)]
    axes = []
    for i in range(12):
        v = [0]*12
        v[i] = 1
        axes.append(literal_direction(v, k))
        Mscaled[i][i] = axes[-1]
    for i in range(12):
        for j in range(i+1, 12):
            v = [0]*12
            v[i] = v[j] = 1
            Mscaled[i][j] = Mscaled[j][i] = (literal_direction(v, k)-axes[i]-axes[j])/2
    theoretical = [[(aT*int(i == j)+bT if i < 6 and j < 6 else
                     K(F(1, 2)*int(i == j)+F(1, 4)) if i >= 6 and j >= 6 else K(0))
                    for j in range(12)] for i in range(12)]
    need(Mscaled == theoretical, 'all-144 literal tangent entries')
    M = [[Mscaled[i][j]/b2 if i < 6 and j < 6 else Mscaled[i][j]
          for j in range(12)] for i in range(12)]
    L = [-3*H/2]*6+[K(0)]*6
    e = [-1/(9*H)]*6+[K(0)]*6
    need(dot(L, e) == 1 and dot(e, mv(M, e)) == gamma, 'normalized maximizing axis')
    need(mv(M, e) == [gamma*v for v in L], 'all-12 constrained first-order equations')
    R = [[(aT/b2*(K(int(i == j))-F(1, 6)) if i < 6 and j < 6 else
           K(F(1, 2)*int(i == j)+F(1, 4)) if i >= 6 and j >= 6 else K(0))
          for j in range(12)] for i in range(12)]
    if damage == 'drop-one-mean-column':
        M[0][1] = K(0)
    need([[M[i][j]-gamma*L[i]*L[j] for j in range(12)] for i in range(12)] == R,
         'whole sharp rank-one remainder')
    detM = determinant(M)
    need(detM == (aT/b2)**5*((aT+6*bT)/b2)*K(F(1, 2))**5*2,
         'full-12 determinant against four eigenspaces')
    Me = mv(M, e)
    border = [[-M[i][j]/gamma for j in range(12)]+[-2*Me[i]] for i in range(12)]
    border.append([2*x for x in Me]+[K(0)])
    if damage == 'reverse-multiplier-column':
        for row in border[:12]:
            row[12] = -row[12]
    if damage == 'erase-level-row':
        border[12] = [K(0)]*13
    detBorder = determinant(border)
    need(detBorder == -4*detM/gamma**10 and bool(detBorder), 'full-13 bordered Jacobian')
    xs = []
    for i in range(6):
        v = [0]*6
        v[i] = 1
        xs.append({tuple(v):K(1)})
    S = padd(*xs)
    T = padd(*(pmul(x, x) for x in xs))
    mh = pscale(S, F(-1, 2))
    sh2 = padd({(0,)*6:b2}, pscale(T, F(-1, 2)), pscale(pmul(S, S), F(-1, 4)))
    small = padd(*(pmul(x, x, x) for x in xs))
    if damage == 'omit-sixth-critical-cube':
        small = padd(*(pmul(x, x, x) for x in xs[:5]))
    cubic = padd(pscale(pmul(mh, mh, mh), 2), pscale(pmul(mh, sh2), 6), small)
    expected_cubic = padd(pscale(S, -3*H/2), pscale(pmul(S, T), F(3, 2)),
                          pscale(pmul(S, S, S), F(1, 2)),
                          padd(*(pmul(x, x, x) for x in xs)))
    need(cubic == expected_cubic, 'whole all-eight cubic moment')
    for i, x in enumerate(xs):
        need(cubic[tuple(next(iter(x)))] == L[i], 'literal cubic gradient coordinate')
    # Reflection acts as (h,u)->(h,-u) in blow-up coordinates when r changes sign.
    signature = [1]*6+[-1]*6
    if damage == 'wrong-real-reflection':
        signature[6] = 1
    physical_conjugation = [-1]*6+[1]*6
    need([-x for x in signature] == physical_conjugation, 'all-12 signed-radius conjugation')
    need([[signature[i]*M[i][j]*signature[j] for j in range(12)] for i in range(12)] == M,
         'entire tangent reflection symmetry')
    need([signature[i]*L[i] for i in range(12)] == L, 'entire peak reflection symmetry')
    lo, hi = F(15, 16), F(47, 50)
    f = lambda x:8*x**3-6*x-1
    need(f(lo) < 0 < f(hi) and 24*lo*lo-6 > 0, 'physical c embedding and uniqueness')
    for _ in range(48):
        mid = (lo+hi)/2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    signs = {}
    for name, value in [('H', H), ('b2', b2), ('aT', aT), ('aT_plus_6bT', aT+6*bT),
                        ('gamma', gamma), ('kappa', k['kappa']), ('w3', k['w3']),
                        ('w4', k['w4'])]:
        a, b = value.interval(lo, hi)
        need(a > 0, 'physical positive sign: '+name)
        signs[name] = {'normal_form':value.record(), 'interval':[str(a), str(b)],
                       'method':'exact rational enclosure of the cubic normal form'}
    # Expanded inverse powers can have severe cancellation in the basis
    # (1,c,c^2).  Certify their signs from the already checked exact
    # factorization and positive interval factors; do not infer a sign from
    # a failed coarse enclosure of a different expression.
    a_lo, a_hi = aT.interval(lo, hi)
    s_lo, s_hi = (aT+6*bT).interval(lo, hi)
    b_lo, b_hi = b2.interval(lo, hi)
    g_lo, g_hi = gamma.interval(lo, hi)
    det_lo = (a_lo/b_hi)**5*(s_lo/b_hi)*F(1, 16)
    det_hi = (a_hi/b_lo)**5*(s_hi/b_lo)*F(1, 16)
    border_lo = 4*det_lo/g_hi**10
    border_hi = 4*det_hi/g_lo**10
    need(0 < det_lo <= det_hi and 0 < border_lo <= border_hi, 'factored positive determinant signs')
    signs['detM'] = {'normal_form':detM.record(), 'interval':[str(det_lo), str(det_hi)],
                    'method':'checked exact product (aT/b2)^5*((aT+6bT)/b2)/16'}
    signs['minus_detBorder'] = {'normal_form':(-detBorder).record(),
                              'interval':[str(border_lo), str(border_hi)],
                              'method':'checked exact quotient 4*detM/gamma^10'}
    return {'schema':'exact-minimum-skew-germ-finite-v1', 'agent':'six-sendov-3', 'role':'researcher',
            'coefficient_domain':'Q[c]/(8c^3-6c-1), normal form (1,c,c^2), characteristic zero',
            'literal_directions':78, 'tangent_entries':144, 'bordered_entries':169,
            'scaled_tangent_matrix':[[x.record() for x in row] for row in Mscaled],
            'raw_tangent_matrix':[[x.record() for x in row] for row in M],
            'cubic_gradient':[x.record() for x in L], 'maximizing_axis':[x.record() for x in e],
            'sharp_remainder_matrix':[[x.record() for x in row] for row in R],
            'bordered_jacobian':[[x.record() for x in row] for row in border],
            'detM':detM.record(), 'detBorder':detBorder.record(), 'gamma':gamma.record(),
            'whole_all8_cubic':[[list(e), a.record()] for e, a in sorted(cubic.items())],
            'physical_c_interval':[str(lo), str(hi)], 'signs':signs,
            'reflection_signature':signature,
            'trust_boundary':'Finite exact algebra only. Global entry, root inverse, radial exhaustion, compactness, analytic IFT and uniqueness are ordinary written mathematics; no formalization or independent review.'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path)
    p.add_argument('--expected', type=Path)
    p.add_argument('--damage', choices=['drop-one-mean-column', 'reverse-multiplier-column',
                                      'erase-level-row', 'omit-sixth-critical-cube', 'wrong-real-reflection'])
    args = p.parse_args()
    record = build(args.damage)
    if args.expected is not None:
        need(json.loads(args.expected.read_text()) == record, 'entire frozen record mismatch')
    raw = (json.dumps(record, indent=2, sort_keys=True)+'\n').encode()
    if args.output:
        args.output.write_bytes(raw)
    print('PASS: 78 literal directions, all144 tangent entries, all169 bordered entries, whole all-eight cubic and ten strict embedding signs.')
    print('Finite certificate only; analytic global theorem is a separate ordinary proof.')


if __name__ == '__main__':
    main()
