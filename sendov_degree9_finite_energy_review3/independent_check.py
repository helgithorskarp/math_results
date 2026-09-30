#!/usr/bin/env python3
"""six-reviewer-3: exact original-derivative local-variation audit.

No author/campaign module imports. Simple critical points are solved from
the differentiated original polynomial by coefficient recursion, without
the reciprocal quadratic discriminant. A paired split is reduced to its
original quartic; its coefficient trace reconstructs the colliding cluster.
Arithmetic is Q[v,v^-1][i] with exact formal t jets. This small arithmetic
design adapts this reviewer's own earlier standalone rational checkers.
"""
from fractions import Fraction as Q
from hashlib import sha256
from math import factorial, comb, isqrt
from pathlib import Path
import json
import sys

N = 10
RECORDS = []


def demand(ok, message):
    if not ok:
        raise ValueError(message)


class P:
    def __init__(self, value=0):
        self.d = ({k: Q(c) for k, c in value.items() if c}
                  if isinstance(value, dict) else ({0: Q(value)} if value else {}))

    @staticmethod
    def cast(x):
        return x if isinstance(x, P) else P(x)

    def __add__(self, x):
        d = dict(self.d)
        for k, c in P.cast(x).d.items():
            d[k] = d.get(k, Q()) + c
        return P(d)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -c for k, c in self.d.items()})

    def __sub__(self, x):
        return self + -P.cast(x)

    def __rsub__(self, x):
        return P.cast(x) + -self

    def __mul__(self, x):
        d = {}
        for k, c in self.d.items():
            for j, b in P.cast(x).d.items():
                d[k+j] = d.get(k+j, Q()) + c*b
        return P(d)

    __rmul__ = __mul__

    def __truediv__(self, x):
        x = P.cast(x)
        demand(len(x.d) == 1, 'nonzero Laurent monomial divisor required')
        j, b = next(iter(x.d.items()))
        return P({k-j: c/b for k, c in self.d.items()})

    def __pow__(self, n):
        if n < 0:
            return P(1)/self**(-n)
        y = P(1)
        for _ in range(n):
            y = y*self
        return y

    def at(self, x):
        return sum((c*x**k for k, c in self.d.items()), Q())

    def record(self):
        return [[k, c.numerator, c.denominator] for k, c in sorted(self.d.items())]


V = P({1: 1})
A0 = V**-1 - 1
BETA = (392-1197*V+945*V**2)/20
LEADING = V**3*(1616-1432*V-1859*V**2)/224
KAPPA = (A0+1)*(A0-Q(5, 8))
K1 = (516*V**-5-528*V**-4-393*V**-3)/7168


class G:
    def __init__(self, re=0, im=0):
        self.r, self.i = P.cast(re), P.cast(im)

    @staticmethod
    def cast(x):
        return x if isinstance(x, G) else G(x)

    def __add__(self, x):
        x = G.cast(x)
        return G(self.r+x.r, self.i+x.i)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.r, -self.i)

    def __sub__(self, x):
        return self + -G.cast(x)

    def __rsub__(self, x):
        return G.cast(x) + -self

    def __mul__(self, x):
        x = G.cast(x)
        return G(self.r*x.r-self.i*x.i, self.r*x.i+self.i*x.r)

    __rmul__ = __mul__

    def conjugate(self):
        return G(self.r, -self.i)

    def __truediv__(self, x):
        x = G.cast(x)
        z = self*x.conjugate()
        d = x.r*x.r+x.i*x.i
        return G(z.r/d, z.i/d)

    def zero(self):
        return not self.r.d and not self.i.d

    def record(self):
        return [self.r.record(), self.i.record()]


class T:
    def __init__(self, x=0):
        self.d = ({k: G.cast(c) for k, c in x.items()
                   if k <= N and not G.cast(c).zero()}
                  if isinstance(x, dict) else ({} if G.cast(x).zero() else {0: G.cast(x)}))

    @staticmethod
    def cast(x):
        return x if isinstance(x, T) else T(x)

    def c(self, k):
        return self.d.get(k, G())

    def __add__(self, x):
        d = dict(self.d)
        for k, c in T.cast(x).d.items():
            d[k] = d.get(k, G()) + c
        return T(d)

    __radd__ = __add__

    def __neg__(self):
        return T({k: -c for k, c in self.d.items()})

    def __sub__(self, x):
        return self + -T.cast(x)

    def __rsub__(self, x):
        return T.cast(x) + -self

    def __mul__(self, x):
        d = {}
        for k, c in self.d.items():
            for j, b in T.cast(x).d.items():
                if k+j <= N:
                    d[k+j] = d.get(k+j, G()) + c*b
        return T(d)

    __rmul__ = __mul__

    def shift(self, s):
        return T({k+s: c for k, c in self.d.items()})

    def inverse(self):
        demand(bool(self.d), 'invert zero series')
        k0 = min(self.d)
        a = self.shift(-k0)
        b = {0: G(1)/a.c(0)}
        for n in range(1, N+1):
            b[n] = -sum((a.c(k)*b[n-k] for k in range(1, n+1)), G())/a.c(0)
        return T(b).shift(-k0)

    def __truediv__(self, x):
        return self*T.cast(x).inverse()

    def __pow__(self, n):
        if n < 0:
            return self.inverse()**(-n)
        y = T(1)
        for _ in range(n):
            y = y*self
        return y

    def conjugate(self):
        return T({k: c.conjugate() for k, c in self.d.items()})

    def real(self):
        return T({k: c.r for k, c in self.d.items()})

    def diff(self):
        return T({k-1: k*c for k, c in self.d.items() if k})

    def norm(self):
        a = self*self.conjugate()
        demand(not a.c(0).i.d and len(a.c(0).r.d) == 1,
               'positive square monomial constant required')
        k, c = next(iter(a.c(0).r.d.items()))
        p, q = isqrt(c.numerator), isqrt(c.denominator)
        demand(c > 0 and k % 2 == 0 and p*p == c.numerator and q*q == c.denominator,
               'exact norm constant square root')
        b = {0: G(P({k//2: Q(p, q)}))}
        for n in range(1, N+1):
            b[n] = (a.c(n)-sum((b[j]*b[n-j] for j in range(1, n)), G()))/(2*b[0])
        return T(b)


def exp_i(phi):
    y, power = T(), T(1)
    for k in range(N+1):
        y = y + power/factorial(k)
        power = power*G(0, 1)*phi
    return y


def check(label, actual, expected=0):
    z = G.cast(actual)-expected
    demand(z.zero(), label)
    RECORDS.append({'label': label, 'value': G.cast(actual).record()})


def pmul(a, b):
    y = [T() for _ in range(len(a)+len(b)-1)]
    for i, c in enumerate(a):
        for j, d in enumerate(b):
            y[i+j] = y[i+j]+c*d
    return y


def padd(a, b):
    return [(a[j] if j < len(a) else T())+(b[j] if j < len(b) else T())
            for j in range(max(len(a), len(b)))]


def pdiff(a):
    return [j*a[j] for j in range(1, len(a))]


def peval(a, x):
    y = T()
    for c in reversed(a):
        y = y*x+c
    return y


def root_recursion(a, r0):
    """Implicit original-coordinate residual root; no quadratic radical."""
    r = T(r0)
    derivative = peval(pdiff(a), r).c(0)
    for n in range(1, N+1):
        r = r + T({n: -peval(a, r).c(n)/derivative})
    for n in range(N+1):
        check('original residual root coefficient '+str(n), peval(a, r).c(n))
    return r


def reciprocal_poly(a):
    """q^degree*a(a0-1/q), by coefficient substitution."""
    d = len(a)-1
    out = [T() for _ in range(d+1)]
    for j, c in enumerate(a):
        for k in range(j+1):
            out[d-k] = out[d-k]+c*((-1)**k*comb(j, k)*A0**(j-k))
    return out


def profile(w):
    t = T({1: 1})
    m = T({3: w})
    A, B = -exp_i(7*t+m), -exp_i(-t+m)
    prod = pmul([-T(A0), T(1)], [-A, T(1)])
    residual = padd(pmul(pdiff(prod), [-B, T(1)]), [7*c for c in prod])
    rn = root_recursion(residual, -1)
    rf = root_recursion(residual, A0-(9*V)**-1)
    qn, qf = (T(A0)-rn).inverse(), (T(A0)-rf).inverse()
    u = (T(A0)-B).inverse()
    ua = (T(A0)-A).inverse()
    F = 6*u.norm()+qn.norm()+qf.norm()
    E = (ua-V)*(ua-V).conjugate()+7*(u-V)*(u-V).conjugate()
    Ggap = F-16*V
    check('energy leading coefficient', E.c(2), 56*V**4)
    return A, B, u, qn, qf, residual, prod, F, E, Ggap


def transverse(p):
    A, B, u, qn, qf, residual, prod, F, E, gap = p
    # p_eps'= (z-B)^4 [D0(z)+eps^2 D2(z)+O(eps^4)].
    # Paired phase directions have squared norm S=2.
    zB = [-B, T(1)]
    f = [T()]+[B*c for c in prod]
    D0 = pmul(pmul(zB, zB), residual)
    D2 = padd(pmul(zB, pdiff(f)), [5*c for c in f])
    d0, d2 = peval(D0, T(A0)), peval(D2, T(A0))
    c0 = [x/d0 for x in reciprocal_poly(D0)]
    raw2 = [T()]+reciprocal_poly(D2)
    c2 = [raw2[j]/d0-c0[j]*d2/d0 for j in range(5)]
    # Complete normalization and base polynomial identity.
    qr = [(qn*qf), -(qn+qf), T(1)]
    factored = pmul(pmul([-u, T(1)], [-u, T(1)]), qr)
    for j in range(5):
        for n in range(7):
            check('quartic normalization coefficient %d/%d'%(j,n), c0[j].c(n), factored[j].c(n))
    shifts = []
    for q in [qn, qf]:
        shifts.append(-peval(c2, q)/peval(pdiff(c0), q))
    # Coefficient trace, rather than the author's colliding-cluster residue.
    total_shift = -c2[3]
    cluster_shift = total_shift-shifts[0]-shifts[1]
    alpha2 = -peval(c2, u)/peval(qr, u)
    c = B*G(0, 1)*u**2
    for n in range(5):
        check('paired eigenvalue first-split square '+str(n), alpha2.c(n), (Q(5, 7)*c**2).c(n))
    cluster_variance = Q(5, 14)*(c*c.conjugate()/u.norm()
                           -(c*u.conjugate()).real()**2/u.norm()**3)
    F2 = (cluster_shift*u.conjugate()).real()/u.norm()/2+cluster_variance
    for shift, q in zip(shifts, [qn, qf]):
        F2 = F2+(shift*q.conjugate()).real()/q.norm()/2
    up = B*G(0, 1)*u**2
    upp = -B*u**2-2*B**2*u**3
    E2 = up*up.conjugate()+((u-V)*upp.conjugate()).real()
    # Differentiate at fixed physical m, independently of m=w*t^3.
    At, Bt = A*G(0,7), B*G(0,-1)
    prod_t = [-At*x for x in [-T(A0),T(1)]]
    residual_t = padd(padd(pmul(pdiff(prod_t),[-B,T(1)]),
                            [-Bt*x for x in pdiff(prod)]),[7*x for x in prod_t])
    ut = Bt*u**2
    ua = (T(A0)-A).inverse()
    uat = At*ua**2
    Ft = 6*(ut*u.conjugate()).real()/u.norm()
    for q in [qn,qf]:
        r = T(A0)-q.inverse()
        rt = -peval(residual_t,r)/peval(pdiff(residual),r)
        qt = q**2*rt
        Ft = Ft+(qt*q.conjugate()).real()/q.norm()
    Et = 2*(uat*(ua-V).conjugate()).real()+14*(ut*(u-V).conjugate()).real()
    multiplier = Ft/Et
    for n in range(5):
        check('physical versus curve multiplier through order4 '+str(n),
              multiplier.c(n),(gap.diff()/E.diff()).c(n))
    H = F2-multiplier*E2
    for n in range(-2, 2):
        check('constrained lower-order cancellation '+str(n), H.c(n))
    check('independent transverse leading coefficient', H.c(2), LEADING)
    check('transverse cubic parity', H.c(3))
    return H


def auxiliary_controls():
    # The whole zero-sum quadratic form, rather than a finite direction sample.
    projection = [[Q(int(j == k))-Q(1, 7) for k in range(7)] for j in range(7)]
    for j in range(7):
        check('projector row sum '+str(j), sum(projection[j]))
        for k in range(7):
            check('projection squared-trace coefficient %d/%d'%(j,k),
                  projection[j][k]**2, Q(5, 7)*int(j == k)+Q(1,49))
    # A directly moved original root, independent of the transverse route.
    A, B = T({0: -1, 1: 1}), T(-1)
    prod = pmul([-T(A0), T(1)], [-A, T(1)])
    residual = padd(pmul(pdiff(prod), [-B, T(1)]), [7*c for c in prod])
    rn = root_recursion(residual, -1)
    rf = root_recursion(residual, A0-(9*V)**-1)
    u = T(V)
    qn, qf = (T(A0)-rn).inverse(), (T(A0)-rf).inverse()
    F = 6*u.norm()+qn.norm()+qf.norm()
    ua = (T(A0)-A).inverse()
    E = (ua-V)*(ua-V).conjugate()
    check('original inward objective derivative', F.c(1), 2*V**2)
    check('original inward energy derivative', E.c(1))
    check('original inward energy quadratic', E.c(2), V**4)


def imul(a,b):
    c = [a[j]*b[k] for j in (0,1) for k in (0,1)]
    return min(c), max(c)


def iadd(a,b):
    return a[0]+b[0], a[1]+b[1]


def ipow(a,n):
    if n < 0:
        demand(a[0] > 0, 'positive interval inverse')
        return ipow((1/a[1],1/a[0]),-n)
    b = (Q(1),Q(1))
    for _ in range(n):
        b = imul(b,a)
    return b


def bound(p,x):
    y = (Q(),Q())
    for k,c in p.d.items():
        y = iadd(y, imul((c,c),ipow(x,k)))
    return y


def slope_certificate(correction):
    # Positive root of 1859 v^2+1432 v-1616, isolated with rational signs.
    lo, hi = Q(1,2), Q(1)
    f = lambda x: 1859*x*x+1432*x-1616
    for _ in range(60):
        mid = (lo+hi)/2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    demand(f(lo)<0<f(hi), 'strict rational root isolation')
    # da_st/de = -4 R(v*)/[v*^9(1432+3718 v*)].
    numerator = bound(-4*correction, (lo,hi))
    denominator = imul(ipow((lo,hi),9), (1432+3718*lo,1432+3718*hi))
    demand(denominator[0] > 0, 'strict slope denominator')
    result = imul(numerator,(1/denominator[1],1/denominator[0]))
    scale = 10**6
    lower = Q((result[0]*scale).__floor__(),scale)
    upper = lower+Q(1,scale)
    demand(lower < result[0] <= result[1] < upper, 'compact exact slope bracket')
    demand(lower > 0, 'strictly positive stability slope')
    return {'v_star_interval': [[x.numerator,x.denominator] for x in (lo,hi)],
            'a_st_energy_slope_interval': [[x.numerator,x.denominator] for x in (lower,upper)]}


def make_result():
    profiles = {w: profile(w) for w in [0, -1, 1, 2]}
    coefficients = []
    for w, p in profiles.items():
        rem = p[-1]-p[-2]*KAPPA+p[-2]**2*K1
        for n in range(6):
            check('mean lower cancellation %d/%d'%(w,n), rem.c(n))
        coefficients.append((w, rem.c(6).r))
    p0 = coefficients[0][1]
    linear = (coefficients[2][1]-coefficients[1][1])/2
    quadratic = (coefficients[2][1]+coefficients[1][1])/2-p0
    check('complete sextic mean constant', p0,
          Q(931,2)*V**3+Q(15897,8)*V**4-Q(168525,32)*V**5
          -Q(9639,8)*V**6+Q(678993,128)*V**7)
    check('complete sextic mean linear', linear,
          -196*V**3+Q(1197,2)*V**4-Q(945,2)*V**5)
    check('complete sextic mean quadratic', quadratic, 5*V**3)
    check('fourth full mean value', coefficients[3][1], p0+2*linear+4*quadratic)
    check('leading stationary mean', -linear/(10*V**3), BETA)
    h0 = transverse(profiles[0])
    stationary = profile(BETA)
    hs = transverse(stationary)
    check('cutoff curvature', LEADING.at(Q(8,13)), Q(83200,2599051))
    # Unreported order-four coefficient; interpreted in PROOF.md.
    correction = hs.c(4)
    demand(not correction.i.d, 'real stability correction')
    auxiliary_controls()
    slope = slope_certificate(correction.r)
    result = {
        'schema': 1, 'agent': 'six-reviewer-3', 'role': 'independent mathematical reviewer',
        'arithmetic': 'Q[v,v^-1][i], exact formal t jets; input through order%d, report through order6/4'%N,
        'identity_count': len(RECORDS),
        'record_sha256': sha256(json.dumps(RECORDS,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        'stationary_beta': BETA.record(), 'transverse_L': LEADING.record(),
        'transverse_t4_zero_mean': h0.c(4).record(),
        'transverse_t4_stationary_mean': correction.record(),
        'mean_constant': p0.record(), 'mean_linear': linear.record(),
        'mean_quadratic': quadratic.record(),
        **slope,
    }
    return result


def main():
    global N
    demand(sys.argv[1:] in ([], ['--write-fixture'], ['--precision-check']), 'invalid command line')
    if sys.argv[1:] == ['--precision-check']:
        N = 12
    result = make_result()
    path = Path(__file__).with_name('expected.json')
    if sys.argv[1:] == ['--write-fixture']:
        path.write_text(json.dumps(result,indent=2)+'\n')
    else:
        try:
            expected = json.loads(path.read_text())
        except (OSError, ValueError) as error:
            raise ValueError('required complete fixture absent or malformed') from error
        if sys.argv[1:] == ['--precision-check']:
            skipped = {'arithmetic','identity_count','record_sha256'}
            demand({k:v for k,v in result.items() if k not in skipped} ==
                   {k:v for k,v in expected.items() if k not in skipped},
                   'higher precision coefficient mismatch')
        else:
            demand(result == expected, 'required complete fixture mismatch')
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
