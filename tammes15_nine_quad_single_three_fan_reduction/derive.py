"""Optional untrusted certificate generator; six-tammes-1, researcher.

SymPy 1.14.0 over Q(c,t), variable order (c,t). Output is canonical JSON
on stdout. check.py verifies its identities without trusting this CAS.
No numerical approximation, modular reconstruction or external data.
"""
import json
import sympy as s

if s.__version__ != '1.14.0':
    raise RuntimeError('Regeneration is pinned to SymPy 1.14.0')
c, t = s.symbols('c t')
H = 1+2*c


def add(a, b):
    return tuple(s.cancel(x+y) for x, y in zip(a, b))


def sub(a, b):
    return tuple(s.cancel(x-y) for x, y in zip(a, b))


def scale(k, a):
    return tuple(s.cancel(k*x) for x in a)


def dot(a, b):
    return s.cancel((1-c)*sum(x*y for x, y in zip(a, b))+c*sum(a)*sum(b))


def cross(a, b):
    return tuple(s.cancel(x) for x in (a[1]*b[2]-a[2]*b[1],
                                     a[2]*b[0]-a[0]*b[2],
                                     a[0]*b[1]-a[1]*b[0]))


def opposite(f, a, b):
    return sub(scale(s.cancel(2*c/(1+dot(a, b))), add(a, b)), f)


def triangle(a, b, sign):
    n = cross(a, b)
    normal = sub(scale(H, n), scale(c*sum(n), (1, 1, 1)))
    return scale(1/(1+c), add(scale(c, add(a, b)), scale(sign, normal)))


def encoded(x):
    p = s.Poly(s.expand(x), c, t, domain=s.QQ)
    if any(a.q != 1 for _, a in p.terms()):
        raise RuntimeError('Expected integer polynomial coefficients')
    return [[i, j, int(a)] for (i, j), a in sorted(p.terms()) if a]


def main():
    F, X, R = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    r = 2*c/(1+c)
    S = sub(scale(r, add(F, R)), X)
    Z = sub(scale(r, add(F, S)), R)
    D = 1+H*t*t
    U = tuple(s.cancel(x) for x in (
        2*c*t*(H*t+1)/D, (1-H*t*t+2*c*t)/D, -2*(1+c)*t/D))
    B = opposite(F, U, X)
    C = opposite(F, U, Z)
    Y = opposite(U, B, C)
    J = triangle(X, B, +1)
    M = triangle(Z, C, -1)
    N = opposite(B, J, Y)
    O = opposite(C, Y, M)
    result = {'format': 'tammes15-five-three-collar-v1',
              'coefficient_domain': 'Z[c,t]', 'variable_order': ['c', 't'],
              'rectangle': ['1/2', '3/5', '5/11', '15/23'], 'points': {}}
    for name, vector in (('F', F), ('X', X), ('R', R), ('S', S), ('Z', Z),
                         ('U', U), ('B', B), ('C', C), ('Y', Y), ('J', J),
                         ('M', M), ('N', N), ('O', O)):
        fractions = [s.fraction(s.cancel(x)) for x in vector]
        denominator = s.lcm([q for p, q in fractions])
        numerators = [s.cancel(p*denominator/q) for p, q in fractions]
        result['points'][name] = {'numerators': [encoded(p) for p in numerators],
                                 'denominator': encoded(denominator)}
    num, den = s.fraction(dot(N, O))
    result['NO_inner_product'] = {'numerator': encoded(num), 'denominator': encoded(den)}
    print(json.dumps(result, separators=(',', ':'), sort_keys=True))


if __name__ == '__main__':
    main()
