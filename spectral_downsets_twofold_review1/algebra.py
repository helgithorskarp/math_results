"""Independent one-variable rational-function certificates, stdlib only."""
from fractions import Fraction as Q
from math import gcd, lcm, comb


def require(ok, message):
    if not ok:
        raise ValueError(message)


def trim(p):
    p = list(map(Q, p))
    while len(p) > 1 and not p[-1]:
        p.pop()
    return tuple(p)


def add(a, b):
    return trim([(a[i] if i < len(a) else 0) +
                 (b[i] if i < len(b) else 0) for i in range(max(len(a), len(b)))])


def mul(a, b):
    p = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            p[i+j] += x*y
    return trim(p)


def divide(a, b):
    a = list(trim(a)); b = trim(b)
    require(any(b), 'zero polynomial divisor')
    q = [Q(0)] * max(1, len(a)-len(b)+1)
    while any(a) and len(a) >= len(b):
        k = len(a)-len(b); c = a[-1]/b[-1]; q[k] += c
        for j, x in enumerate(b):
            a[k+j] -= c*x
        a = list(trim(a))
    return trim(q), trim(a)


def pgcd(a, b):
    while any(b):
        a, b = b, divide(a, b)[1]
    return trim([x/a[-1] for x in a])


class R:
    def __init__(self, n=0, d=(1,)):
        self.n = trim(n if isinstance(n, (tuple, list)) else (n,))
        self.d = trim(d)
        require(any(self.d), 'zero rational denominator')
        g = pgcd(self.n, self.d)
        self.n, rn = divide(self.n, g); self.d, rd = divide(self.d, g)
        require(not any(rn) and not any(rd), 'polynomial cancellation')
        scale = self.d[-1]
        self.n = trim([x/scale for x in self.n]); self.d = trim([x/scale for x in self.d])

    def __add__(self, o):
        o = o if isinstance(o, R) else R(o)
        return R(add(mul(self.n, o.d), mul(o.n, self.d)), mul(self.d, o.d))
    __radd__ = __add__

    def __neg__(self):
        return R([-x for x in self.n], self.d)

    def __sub__(self, o):
        return self + -(o if isinstance(o, R) else R(o))

    def __rsub__(self, o):
        return R(o) - self

    def __mul__(self, o):
        o = o if isinstance(o, R) else R(o)
        return R(mul(self.n, o.n), mul(self.d, o.d))
    __rmul__ = __mul__

    def __truediv__(self, o):
        o = o if isinstance(o, R) else R(o)
        return self * R(o.d, o.n)

    def __rtruediv__(self, o):
        return R(o) / self

    def __pow__(self, k):
        require(type(k) is int and k >= 0, 'nonnegative power')
        p = R(1)
        for _ in range(k):
            p = p*self
        return p


def shifted(p, a=13):
    return trim([sum(p[j]*comb(j, i)*a**(j-i) for j in range(i, len(p)))
                 for i in range(len(p))])


def coefficients(p):
    scale = lcm(*(x.denominator for x in p))
    ints = [int(x*scale) for x in p]
    g = gcd(*ints)
    return [x//g for x in ints] if g else ints


def certificates():
    v = R((0, 1)); s = 2*v-1; m = v*(v-1)/2; b = v*(v-1)/3
    n = 1+v+m+b; k = (v-2)*(v-3)/2
    a = R(Q(-2, 3)); w = 1+4*v*(2*v-5)/(3*(v-2)*(v-3)*(v-4))
    c = 1+4/(3*(v-2)*(v-3)); d = (v*v-v-4)/((v-3)*(v-4))
    h = (v*v-7)/((v-3)*(v-4)); t = (v-1)/(v-4)
    alpha1 = s-c*(v-3); alpha2 = s+c
    beta = t-d*d/alpha2
    gamma = t-4*d*d/(alpha2*(v-2))+d*d*(v-4)**2/((v-2)*alpha1)
    bracket = t*(v-6)/(v-2)+d*d*(v-4)**2/((v-2)*alpha1)
    mu = v*(3*v**3-13*v*v+32)/((v-3)*(v-2)*(3*v*v-16))
    gap = n-7*v; stronger = n-Q(28,5)*v; eta = stronger/(8*m*k)
    A = (v-3)*d*d*(v-4)**2/(v-2)
    identities = {
        'triple_star': h+(v-4)*d+(v-7)*t-s,
        'triple_row': 1+s+(v-3)*h-3*t+(v-3)*(v-4)*d/2+(v-4)*(v-6)*t/3-n,
        'pair_star': w+(v-3)*c+(v-5)*d-s,
        'pair_row': 1+s+(v-2)*w-2*d+(v-2)*(v-3)*c/2+(v-3)*(v-4)*d/3-n,
        'point_star': a+(v-2)*w-2*d+(v-3)*h-3*t-s,
        'point_row': 1+s+(v-1)*a+(v-1)*(v-2)*w/2-(v-1)*d+(v-1)*(v-3)*h/3-(v-1)*t-n,
        'constant_pair': s+c-2*c*(v-1)+(c-1)*m-Q(8,3),
        'constant_cross': 2*d-2*d*(v-1)+(d-1)*b+Q(4,3),
        'constant_triple': s-t+6*t-3*t*(v-1)+(t-1)*b-1,
        'alpha1': alpha1-(3*v*v-16)/(3*(v-2)),
        'Schur_cancellation': gamma-4*beta/(v-2)-bracket,
        'mu': s-t-(v-3)*bracket-mu,
        'mu_minus_one': mu-1-2*(v-4)*(v*v+3*v-12)/((v-3)*(v-2)*(3*v*v-16)),
        'trace': (v-1)/3+Q(8,3)+1-(v+10)/3,
        'original_eta': gap/(8*m*k)-(5*v*v-41*v+6)/(12*v*(v-1)*(v-2)*(v-3)),
        'new_eta': eta-(25*v*v-163*v+30)/(60*v*(v-1)*(v-2)*(v-3)),
        'eta_increment': eta-gap/(8*m*k)-7/(10*(v-1)*(v-2)*(v-3)),
    }
    for name, r in identities.items():
        require(not any(r.n), 'failed identity '+name)
    margins = {
        'alpha1_gt_v': alpha1-v,
        'alpha2_gt_2v': alpha2-2*v,
        'beta_gt_1_minus_2_over_v': beta-(1-2/v),
        'mu_gt_one': mu-1,
        'A_lt_4v2': 4*v*v-A,
        'original_gap_positive': gap,
        'stronger_gap_positive': stronger,
        'stronger_gap_lt_v2': v*v-stronger,
        'eight_mk_gt_v4': 8*m*k-v**4,
        'w_le_11_over_8': Q(11,8)-w,
        'd_le_17_over_10': Q(17,10)-d,
        'h_le_9_over_5': Q(9,5)-h,
        't_le_4_over_3': Q(4,3)-t,
        'c_le_4_over_3': Q(4,3)-c,
        'sqrt_v_le_5v_over_18': 25*v-324,
        'row1_gap': (Q(28,5)-Q(12035,2160))*v,
        'row2_gap': (583*v-240)/720,
        'row3_gap': (203*v-1530)/270,
        'constant_gap': (79*v-50)/15,
        'repair_mu_margin': 1-8/v,
    }
    result = {}
    for name, r in margins.items():
        num, den = shifted(r.n), shifted(r.d)
        require(all(x>=0 for x in num) and any(num), 'numerator sign '+name)
        require(all(x>=0 for x in den) and den[0]>0, 'denominator sign '+name)
        if name not in ['h_le_9_over_5', 't_le_4_over_3']:
            require(num[0]>0, 'strict margin at13 '+name)
        result[name] = {'numerator':coefficients(num), 'denominator':coefficients(den)}
    return {'identities':list(identities), 'nonnegative_shifted_coefficient_certificates':result}
