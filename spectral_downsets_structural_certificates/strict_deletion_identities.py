#!/usr/bin/env python3
"""Independent rational identities and positive coefficients, without sampling."""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
import json


def add(a, b):
    out = defaultdict(F, a)
    for p, c in b.items(): out[p] += c
    return {p: c for p, c in out.items() if c}


def mul(a, b):
    out = defaultdict(F)
    for p, c in a.items():
        for q, d in b.items():
            out[tuple(x+y for x, y in zip(p, q))] += c*d
    return {p: c for p, c in out.items() if c}


class R:
    def __init__(self, a=0, b=None):
        self.a = a if isinstance(a, dict) else ({(0, 0, 0): F(a)} if a else {})
        self.b = {(0, 0, 0): F(1)} if b is None else b
        if not self.b: raise ValueError('Zero polynomial denominator')
    @staticmethod
    def coerce(x): return x if isinstance(x, R) else R(x)
    def __add__(self, other):
        other = self.coerce(other)
        return R(add(mul(self.a, other.b), mul(other.a, self.b)), mul(self.b, other.b))
    __radd__ = __add__
    def __neg__(self): return R({p: -c for p, c in self.a.items()}, self.b)
    def __sub__(self, other): return self + -self.coerce(other)
    def __rsub__(self, other): return self.coerce(other) + -self
    def __mul__(self, other):
        other = self.coerce(other)
        return R(mul(self.a, other.a), mul(self.b, other.b))
    __rmul__ = __mul__
    def __truediv__(self, other):
        other = self.coerce(other)
        if not other.a: raise ValueError('Division by zero polynomial')
        return R(mul(self.a, other.b), mul(self.b, other.a))
    def __rtruediv__(self, other): return self.coerce(other) / self
    def __pow__(self, exponent):
        out = R(1)
        for _ in range(exponent): out = out * self
        return out


def variable(i):
    return R({tuple(int(j == i) for j in range(3)): F(1)})


def certificates():
    n, t, k = [variable(i) for i in range(3)]
    ell = n*(n-1)/2; d = (n-2)*(n-3)
    b = -1+d*t; p = 2/(n-2)-(n-3)*t; z = 2/(n-2)+t
    kappa = n*(n-1)/(n-2); gamma = d*(2*n-1)/2
    A = n*(n-1)*d*t; a = n-d*t
    checks = []
    def identity(name, lhs, rhs):
        if (lhs-rhs).a: raise ValueError('Rational identity failed: '+name)
        checks.append(name)
    identity('singleton_star', b-1+(n-2)*p, R(0))
    identity('pair_star', p-2+(n-3)*z, R(0))
    identity('constant_11_count', n*(n-1)*(1+b), A)
    identity('constant_12_count', n*(-(n-1)+(n-1)*(n-2)*p/2), -A/2)
    identity('constant_22_count', ell*(n-1-2*(n-2)+d*z/2), A/4)
    identity('standard_11', n-1-b, a)
    identity('standard_12', (n-2)*(-1-p), -a)
    identity('standard_22', (n-2)*(n-1-z+(-1-z)*(n-4)), a)
    identity('standard_trace', a+a/(n-2), kappa-(n-1)*(n-3)*t)
    identity('constant_trace', A/n+(A/4)/ell, gamma*t)
    identity('incidence_kernel', n+1+z, kappa+t)
    identity('uniform_gap', 1+n+ell-kappa, (n*(n-1)*(n-2)-4)/(2*(n-2)))
    q = kappa+(k-1)*(n-1+2*(k-1)/(n-2))
    h = n*(n+3)/2-kappa-n*k-2*(k-1)**2/(n-2)
    identity('matching_gap', 1+n+ell-k-q, h)
    endpoint = (n-1)/2
    endgap = n*(n+3)/2-kappa-n*endpoint-2*(endpoint-1)**2/(n-2)
    identity('matching_endpoint_gap', endgap, (n*n-9)/(2*(n-2)))
    qstar = kappa+(k-1)*(n-k)
    identity('partial_star_gap', 1+n+ell-k-qstar,
             (k-(n+2)/2)**2+n*n*(n-4)/(4*(n-2)))
    clique_k = (n-1)*(n-2)/2
    clique_g = n-1-2*(n-3)+2*(clique_k-1-2*(n-3))/(n-2)
    identity('star_retained_boundary', kappa+(clique_k-1)*clique_g, 2*n)
    mu, beta = t, k
    epsilon = mu/(2*(mu+2*beta))
    identity('convex_upper_buffer', (1-epsilon)*mu/2-epsilon*beta, mu/4)
    identity('perturbation_upper_loss', gamma*(mu/(2*gamma)), mu/2)
    identity('standard_positivity_margin', kappa-(n-1)*(n-3)*mu/(2*gamma),
             (n-1)/(n-2)*(n-mu/(2*n-1)))

    # Shifted signs are expanded directly, not inferred from finite evaluations.
    U = variable(0); nn = U+4
    raw = {
        'uniform_gap_numerator': nn*(nn-1)*(nn-2)-4,
        'matching_gap_numerator': nn*nn-9,
        'gamma_minus_one_twice': (nn-2)*(nn-3)*(2*nn-1)-2,
        'gamma_minus_standard_twice': (nn-2)*(nn-3)*(2*nn-1)-2*(nn-1)*(nn-3),
        'partial_star_n_ge_5_numerator': (U+5)**2*(U+1)}
    positive = {}
    for name, P in raw.items():
        if P.b != {(0, 0, 0): F(1)}:
            raise ValueError('Unexpected non-polynomial sign certificate')
        if not P.a or any(c <= 0 or c.denominator != 1 for c in P.a.values()) or not P.a.get((0, 0, 0)):
            raise ValueError('Positive-coefficient certificate failed: '+name)
        positive[name] = [[*e, int(c)] for e, c in sorted(P.a.items())]
    payload = dict(identities=checks, positive_coefficients=positive)
    payload['canonical_sha256'] = sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return payload


if __name__ == '__main__': print(json.dumps(certificates(), sort_keys=True, indent=2))
