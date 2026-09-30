#!/usr/bin/env python3
"""six-reviewer-5: exact identities and positive-coefficient certificates.

Coefficient domain Z inside Q(R,T), characteristic zero. No CAS/imported
researcher module. Regime substitutions are R=3+x,T=2+x+y and
R=4+x+y,T=2+y, with x,y>=0. Every polynomial operation is explicit.
"""
from math import gcd
import hashlib
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


def plus(a, b):
    out = dict(a)
    for key, value in b.items():
        out[key] = out.get(key, 0)+value
        if not out[key]:
            del out[key]
    return out


def times(a, b):
    out = {}
    for (i, j), x in a.items():
        for (k, l), y in b.items():
            key = (i+k, j+l)
            out[key] = out.get(key, 0)+x*y
    return {key: value for key, value in out.items() if value}


class Q:
    def __init__(self, numerator=0, denominator=1):
        self.n = dict(numerator) if isinstance(numerator, dict) else ({(0, 0): numerator} if numerator else {})
        self.d = dict(denominator) if isinstance(denominator, dict) else {(0, 0): denominator}
        need(bool(self.d), 'zero rational-function denominator')
        if not self.n:
            self.d = {(0, 0): 1}
        factor = 0
        for value in list(self.n.values())+list(self.d.values()):
            factor = gcd(factor, value)
        if factor > 1:
            self.n = {key: value//factor for key, value in self.n.items()}
            self.d = {key: value//factor for key, value in self.d.items()}

    def __add__(self, other):
        other = other if isinstance(other, Q) else Q(other)
        return Q(plus(times(self.n, other.d), times(other.n, self.d)), times(self.d, other.d))

    __radd__ = __add__

    def __neg__(self):
        return Q({key: -value for key, value in self.n.items()}, self.d)

    def __sub__(self, other):
        return self+-asq(other)

    def __rsub__(self, other):
        return asq(other)+-self

    def __mul__(self, other):
        other = asq(other)
        return Q(times(self.n, other.n), times(self.d, other.d))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = asq(other)
        return Q(times(self.n, other.d), times(self.d, other.n))

    def __rtruediv__(self, other):
        return asq(other)/self

    def __pow__(self, count):
        need(isinstance(count, int) and count >= 0, 'invalid polynomial power')
        result = Q(1)
        for _ in range(count):
            result = result*self
        return result


def asq(value):
    return value if isinstance(value, Q) else Q(value)


R, T = Q({(1, 0): 1}), Q({(0, 1): 1})


def coefficients(regime):
    if regime == 1:
        return dict(alpha=Q(0), q=Q(0), eta=Q(0), p=-(R-1)/T,
                    beta=-1+R*(R-3)*(T-R+1)/(2*T*(T-1)),
                    u=(T-R+3)/T, v=1/T, w=2/T,
                    h=(R-2)*(R-1-T)/(T*(T-1)), z=(2*T-2*R+3)/(T*(T-1)))
    delta = T*(T-1)/(R-1+T*(T-1))
    return dict(alpha=-1+delta, q=2*(R-1-T)/((R-1)*(R-2)),
                eta=2*(R-1-T)/((R-1)*(R-2)), p=Q(-1), beta=Q(-1),
                u=2/(R-1), v=2/(R-1)-delta/T, w=2/(R-1),
                h=Q(0), z=delta/(T*(T-1)))


def substitute(poly, rr, tt):
    need(rr.d == tt.d == {(0, 0): 1}, 'substitution must be polynomial')
    result = Q(0)
    for (i, j), value in poly.items():
        result += value*rr**i*tt**j
    need(result.d == {(0, 0): 1}, 'nonpolynomial result')
    return result.n


def positive(name, expression, rr, tt, strict):
    expression = asq(expression)
    n, d = substitute(expression.n, rr, tt), substitute(expression.d, rr, tt)
    # Sign-normalize denominator before checking the coefficient certificate.
    if d.get((0, 0), 0) < 0:
        n, d = ({key: -v for key, v in p.items()} for p in (n, d))
    need(d.get((0, 0), 0) > 0 and all(v >= 0 for v in d.values()), name+': denominator sign')
    need(all(v >= 0 for v in n.values()), name+': numerator sign')
    need(not strict or n.get((0, 0), 0) > 0, name+': strict constant')
    witness = [[i, j, v] for (i, j), v in sorted(n.items())]
    return {'name': name, 'strict': strict, 'numerator_terms': len(n),
            'constant': n.get((0, 0), 0), 'degree': max((i+j for i, j in n), default=0),
            'numerator_sha256': hashlib.sha256(json.dumps(witness, separators=(',', ':')).encode()).hexdigest()}


def audit():
    reports = []
    for regime, rr, tt in [(1, 3+R, 2+R+T), (2, 4+R+T, 2+T)]:
        p = coefficients(regime)
        a, q, e, pp, b, u, v, w, h, z = [p[k] for k in ('alpha', 'q', 'eta', 'p', 'beta', 'u', 'v', 'w', 'h', 'z')]
        d, ell = R+T-1, R*(R-1)/2
        identities = [a-1+(R-2)*q+T*v, q-2+(R-3)*e+T*w,
                      pp-1+(R-1)*u+(T-1)*h, v-2+(R-2)*w+(T-1)*z,
                      T*pp+(R-1)-(R-1)*(R-2)*q/2,
                      T*u-d+2*(R-2)-(R-2)*(R-3)*e/2,
                      d+(T-1)*b-ell*u,
                      -1+(T-1)*h+(R-1)-(R-1)*(R-2)*w/2,
                      d-a-(R-2)*(1+q)-T*(1+v),
                      T+3-(R-3)*e-(1+q)-T*(1+w),
                      R+1-(T-1)*z-(1+v)-(R-2)*(1+w),
                      1+R+T+ell+R*T-3*(R+T)-(ell-3+(R-2)*(T-2))]
        need(all(not identity.n for identity in identities), 'row/kernel/Laplacian identity failure')
        h11, h22 = d-b, T+1-(R-1)*z
        hdet = h11*h22-R*(1+h)**2
        k11, k22, k12sq = R*(d+(R-1)*a), ell*T*u, (R*T*pp)**2
        certs = [positive('off_'+name, value+1, rr, tt, False) for name, value in p.items()]
        for name, value in [('edge_kernel', d+2+e), ('mixed_spoke', d+2+z),
                            ('leaf_diagonal', h11), ('leaf_determinant', hdet),
                            ('constant_diagonal', k11), ('constant_determinant', k11*k22-k12sq),
                            ('standard_edge_conductance', (R-2)*(1+q)),
                            ('standard_single_spoke_conductance', T*(1+v)),
                            ('standard_edge_spoke_conductance', (R-2)*T*(1+w)),
                            ('rho_less_one', 1+R+T+ell+R*T-2*(R+T))]:
            certs.append(positive(name, value, rr, tt, True))
        certs.append(positive('fractional_density_gap', 1+R+T+ell+R*T-3*(R+T), rr, tt, False))
        reports.append({'regime': regime, 'zero_identities': len(identities), 'positive_coefficients': certs})
    # Original two-center cap margins and friendship Schur bridge.
    companion = []
    for name, expr in [('two_center_constant_determinant', R*(R+1)-2),
                       ('two_center_standard_cap_minus_I', 2*R-2/R),
                       ('two_center_leaf_cap_minus_I', R+1/R),
                       ('two_center_constant_cap_minus_I', R-2+1/R),
                       ('friendship_Schur', 2*R+1-7*R/(3*(R-1)**2))]:
        companion.append(positive(name, expr, 2+R, T, True))
    return {'reviewer': 'six-reviewer-5', 'role': 'independent mathematical reviewer',
            'domain': 'Q(R,T), characteristic zero; positive coefficients after domain shifts',
            'regimes': reports, 'companion_certificates': companion}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True))
