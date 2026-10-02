"""Exact rational-function checks for the twelve-point frame, without point13.

Same author as the enclosure code; not an independent researcher review.
The elementary polynomial representation uses Fractions, with no CAS package.
"""
from fractions import Fraction as F
from itertools import combinations
import json
import signal


def require(ok, message):
    if not ok:
        raise ValueError(message)


def trim(p):
    p = list(map(F, p))
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)


def add(p, q):
    r = [F(0)] * max(len(p), len(q))
    for i, x in enumerate(p):
        r[i] += x
    for i, x in enumerate(q):
        r[i] += x
    return trim(r)


def mul(p, q):
    r = [F(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            r[i+j] += x*y
    return trim(r)


def derivative(p):
    return trim([i*p[i] for i in range(1, len(p))] or [0])


def evaluate(p, a):
    r = F(0)
    for x in reversed(p):
        r = r*a + x
    return r


class R:
    def __init__(self, numerator=(0,), denominator=(1,)):
        if isinstance(numerator, (int, F)):
            numerator = (numerator,)
        self.n, self.d = trim(numerator), trim(denominator)
        require(self.d != (F(0),), 'nonzero rational-function denominator')

    @staticmethod
    def cv(x):
        return x if isinstance(x, R) else R(x)

    def __add__(self, x):
        x = R.cv(x)
        return R(add(mul(self.n, x.d), mul(x.n, self.d)), mul(self.d, x.d))

    __radd__ = __add__

    def __neg__(self):
        return R([-x for x in self.n], self.d)

    def __sub__(self, x):
        return self + -R.cv(x)

    def __rsub__(self, x):
        return R.cv(x) + -self

    def __mul__(self, x):
        x = R.cv(x)
        return R(mul(self.n, x.n), mul(self.d, x.d))

    __rmul__ = __mul__

    def __truediv__(self, x):
        x = R.cv(x)
        return R(mul(self.n, x.d), mul(self.d, x.n))

    def __rtruediv__(self, x):
        return R.cv(x) / self

    def __pow__(self, n):
        require(type(n) is int and n >= 0, 'nonnegative integer exponent')
        r = R(1)
        for _ in range(n):
            r = r*self
        return r

    def same(self, x):
        x = R.cv(x)
        return mul(self.n, x.d) == mul(x.n, self.d)

    def diff(self):
        return R(add(mul(derivative(self.n), self.d),
                     tuple(-x for x in mul(self.n, derivative(self.d)))),
                 mul(self.d, self.d))

    def at(self, a):
        return evaluate(self.n, F(a)) / evaluate(self.d, F(a))


def dot(x, y, q):
    return (1-q)*sum(a*b for a, b in zip(x, y)) + q*sum(x)*sum(y)


def cross(x, y):
    return [x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2],
            x[0]*y[1]-x[1]*y[0]]


def main():
    t = R((0, 1))
    r = 2*t/(1+t)
    k = t*(9*t*t-2*t-3)/(1+t)**2
    h = 4*t*t/(1+t)-1
    ell = r*(h+k)-t
    D = (1-t)**2*(1+2*t)
    den = (2*r-1)*(r+1)
    mu = (t-1)*(t+1)*(2*t+1)*(3*t-1)/(9*t**3-t*t-t+1)
    count = 0

    def identity(a, b, why):
        nonlocal count
        require(R.cv(a).same(b), why)
        count += 1

    identity(k.diff(), (9*t*t-1)*(t+3)/(1+t)**3, 'k derivative')
    identity(mu*mu, D*(1+2*k)/(1+k)**2, 'U normal coefficient')
    identity(1+2*k, (3*t-1)**2*(2*t+1)/(1+t)**2, 'positive k Gram')
    identity(k-t, 4*t*(2*t+1)*(t-1)/(1+t)**2, 'k packing gap')
    identity(h-t, (3*t+1)*(t-1)/(1+t), 'h packing gap')
    identity(9*t**3-t*t-t+1, (1+t)**2*(1+k), 'mu denominator')

    contacts = {(0,5), (0,6), (0,7), (0,11), (1,2), (1,4), (1,10),
                (1,12), (2,4), (2,8), (2,10), (4,8), (5,7), (5,9),
                (5,11), (6,11), (7,12), (9,10), (9,11), (10,12)}
    B = {i: [R(int(j == s)) for j in range(3)]
         for s, i in enumerate((1, 2, 4))}
    for n, i, j, old in ((8,2,4,1), (10,1,2,4), (12,1,10,2)):
        B[n] = [r*(a+b)-c for a, b, c in zip(B[i], B[j], B[old])]
    A = {6: [R(1), R(0), R(0)], 7: [R(0), R(1), R(0)],
         9: [R(0), R(0), R(1)]}
    for label, coefficients in ((0,(r,r,1-r)), (5,(1-r,r,r)),
                                (11,(r,1-r,r))):
        A[label] = [v/den for v in coefficients]
    internal_contacts = internal_noncontacts = 0
    kinds = {'h': 0, 'k': 0, 'ell': 0}
    for points, metric in ((A, k), (B, t)):
        for v in points.values():
            identity(dot(v, v, metric), 1, 'every cluster unit identity')
        for i, j in combinations(sorted(points), 2):
            product = dot(points[i], points[j], metric)
            if (i, j) in contacts:
                identity(product, t, 'every internal prescribed contact')
                internal_contacts += 1
            else:
                found = [name for name, value in (('h',h), ('k',k), ('ell',ell))
                         if product.same(value)]
                require(len(found) == 1, 'literal noncontact identity')
                count += 1
                internal_noncontacts += 1
                kinds[found[0]] += 1
    require(internal_contacts == 18 and internal_noncontacts == 12,
            'complete two-cluster comparison domain')
    for new, i, j, old in ((6,0,11,5), (7,0,5,11), (9,5,11,0)):
        for component in range(3):
            identity(A[new][component],
                     r*(A[i][component]+A[j][component])-A[old][component],
                     'every inverse A reflection component')

    normal = cross(B[12], B[1])
    d = [x/(1-t)-t*sum(normal)/((1-t)*(1+2*t)) for x in normal]
    identity(dot(d, B[12], t), 0, 'circle normal first orthogonality')
    identity(dot(d, B[1], t), 0, 'circle normal second orthogonality')
    identity(dot(d, d, t), (1-t*t)/D, 'circle normal norm')
    identity(dot(d, B[10], t), -1, 'explicit s linear coefficient')
    identity(2*t*t-t-1, -(1-t)*(1+2*t), 'chart gap constant coefficient')
    identity(D*(1-t), (1-t)**3*(1+2*t), 'chart gap quadratic coefficient')
    lo, hi = F(14,25), F(593,1000)
    require(k.at(lo) > F(-3,10) and k.at(hi) < F(-1,5),
            'closed k bracket endpoints')
    g = lambda s, q, u: 1-s*s-q*q-u*u+2*s*q*u
    require(g(F(-24,25),F(-3,10),lo) == F(-33,12500),
            'lower s forbidden-region maximum')
    require(g(F(7,10),F(-1,5),lo) == F(-1,2500),
            'upper s forbidden-region maximum')
    print(json.dumps({'actual_agent': 'six-tammes-2', 'role': 'researcher',
                      'exact_rational_identities': count,
                      'cluster_unit_identities': 12,
                      'internal_contact_identities': internal_contacts,
                      'internal_noncontact_identities': internal_noncontacts,
                      'noncontact_products': kinds,
                      'k_closed_endpoint_values': [str(k.at(lo)), str(k.at(hi))],
                      'forbidden_s_maxima': ['-33/12500','-1/2500'],
                      'arithmetic': 'exact univariate rational functions over Q',
                      'point13_used': False,
                      'independent_researcher_review': 'pending'}, indent=2))


if __name__ == '__main__':
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(
        TimeoutError('55-second identity guard')))
    signal.alarm(55)
    main()
