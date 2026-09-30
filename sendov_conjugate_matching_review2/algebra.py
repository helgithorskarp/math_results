"""Exact polynomial normal forms with two unit-circle relations.

Variables: a,r1,r2,X,Y,Z,T,s; quotient Y^2=1-X^2,T^2=1-Z^2.
This module is independent of the target's polynomial implementation.
"""
from fractions import Fraction as Q
from math import comb

DIM = 8
ZERO = (0,)*DIM


class P:
    def __init__(self, value=0):
        if isinstance(value, P):
            self.terms = value.terms.copy()
        elif isinstance(value, dict):
            self.terms = {e: Q(c) for e, c in value.items() if c}
        else:
            self.terms = {ZERO: Q(value)} if value else {}

    def __add__(self, other):
        result = self.terms.copy()
        for e, c in P(other).terms.items():
            result[e] = result.get(e, Q(0))+c
        return P(result)

    __radd__ = __add__

    def __neg__(self):
        return P({e: -c for e, c in self.terms.items()})

    def __sub__(self, other):
        return self+-P(other)

    def __rsub__(self, other):
        return P(other)+-self

    def __mul__(self, other):
        out = {}
        for e, c in self.terms.items():
            for f, d in P(other).terms.items():
                key = tuple(x+y for x, y in zip(e, f))
                out[key] = out.get(key, Q(0))+c*d
        return P(out)

    __rmul__ = __mul__

    def __pow__(self, n):
        out = P(1)
        for _ in range(n):
            out = out*self
        return out

    def normal(self):
        out = dict(self.terms)
        for imag, real in ((4, 3), (6, 5)):
            new = {}
            for e, c in out.items():
                quotient, parity = divmod(e[imag], 2)
                for j in range(quotient+1):
                    f = list(e)
                    f[imag] = parity
                    f[real] += 2*j
                    f = tuple(f)
                    new[f] = new.get(f, Q(0))+c*comb(quotient, j)*(-1)**j
            out = {e: c for e, c in new.items() if c}
        return P(out)


def variable(i):
    e = [0]*DIM
    e[i] = 1
    return P({tuple(e): 1})


def identities():
    a, r1, r2, X, Y, Z, T, s = [variable(i) for i in range(DIM)]
    r, delta = Q(1, 2)*(r1+r2), r1-r2
    d2 = (X-Z)**2+(Y-T)**2
    g2 = (r1*X-r2*Z)**2+(r1*Y-r2*T)**2
    f1 = (1-a*a)*r1*r1+2*a*r1*X-1
    f2 = (1-a*a)*r2*r2+2*a*r2*Z-1
    fw = (1-a*a)*r*r+a*r*(X+Z)-1
    real_product = r1*r2*(X*Z+Y*T)
    imag_product = r1*r2*(Y*Z-X*T)
    error_norm2 = (real_product-r*r)**2+imag_product**2
    checks = {
        'unit_direction_distance': g2-delta**2-r1*r2*d2,
        'disk_lift': 4*r1*r2*fw-2*r*(r2*f1+r1*f2)-delta**2,
        'real_sum_error': r1*X+r2*Z-r*(X+Z)-Q(1, 2)*delta*(X-Z),
        'real_product_error': real_product-r*r+Q(1, 2)*g2-Q(1, 4)*delta**2,
        'product_error_norm': error_norm2-Q(1, 16)*delta**4-r*r*r1*r2*d2,
        'product_error_bound_gap': r*r*g2-error_norm2-Q(1, 16)*delta**2*(3*r1*r1+10*r1*r2+3*r2*r2),
        'proxy_factor': (1+s*r)**2-(1+s*r1)*(1+s*r2)-Q(1, 4)*s*s*delta**2,
        'direction_displacement': g2-r*r*d2-delta**2*(1-Q(1, 4)*d2),
    }
    # Two formal example identities. Here X,Y,Z,T are indeterminates.
    w, A, t, q = X, Y, Z, T
    h = w*w+t*t
    checks['example_derivative'] = h**4+8*w*(w-A)*h**3-h**3*(9*w*w-8*A*w+t*t)
    checks['example_reciprocal'] = 9*(A*q-1)**2-8*A*q*(A*q-1)+t*t*q*q-((A*A+t*t)*q*q-10*A*q+9)
    for name, poly in checks.items():
        # Example identities vanish before any unit-circle reduction.
        result = poly if name.startswith('example_') else poly.normal()
        if result.terms:
            raise ValueError('Algebraic identity failed: '+name)
    return checks
