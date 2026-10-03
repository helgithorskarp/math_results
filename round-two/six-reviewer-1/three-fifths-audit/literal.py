"""Fresh Gaussian-rational identity controls; these are NOT disk-root witnesses."""
import json
from itertools import combinations
from arithmetic import F, require, encode


def C(a=0, b=0):
    return F(a), F(b)


def plus(a, b):
    return a[0]+b[0], a[1]+b[1]


def neg(a):
    return -a[0], -a[1]


def times(a, b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def inv(a):
    s = a[0]*a[0]+a[1]*a[1]
    require(s > 0, 'Gaussian nonzero denominator')
    return a[0]/s, -a[1]/s


def pmul(a, b):
    out = [C()]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] = plus(out[i+j], times(x, y))
    return out


def ppow(a, n):
    out = [C(1)]
    for _ in range(n):
        out = pmul(out, a)
    return out


def evaluate(p, x):
    out = C()
    for c in reversed(p):
        out = plus(c, times(x, out))
    return out


def pintegral(p):
    out = C()
    for i, c in enumerate(p):
        out = plus(out, times(C(F(1, i+1)), c))
    return out


def case(q, a):
    require(len(q) == 8 and all(z != C() for z in q), 'eight finite reciprocals')
    critical = [plus(C(a), neg(inv(z))) for z in q]
    derivative = ppow([C(1)], 0)
    for z in critical:
        derivative = pmul(derivative, [neg(z), C(1)])
    derivative = [times(C(9), z) for z in derivative]
    p = [C()] + [times(C(F(1, i+1)), z) for i, z in enumerate(derivative)]
    p[0] = neg(evaluate(p, C(a)))
    # Full synthetic quotient R=p/(x-a).
    R = [C()]*9; R[8] = p[9]
    for i in range(8, 0, -1):
        R[i-1] = plus(p[i], times(C(a), R[i]))
    require(pmul([C(-a), C(1)], R) == p and evaluate(p, C(a)) == C(),
            'whole original polynomial and root quotient')
    require([times(C(i), p[i]) for i in range(1, 10)] == derivative,
            'whole degree-nine derivative')
    ra = evaluate(R, C(a)); ri = inv(ra)
    origin_product, polar_product = [C(1)], [C(1)]
    for z in q:
        origin_product = pmul(origin_product, [C(1), times(C(-a), z)])
        polar_product = pmul(polar_product, [C(a), times(C(1-a*a), z)])
    O = times(C(9), pintegral(origin_product)); J = pintegral(polar_product)
    require(O == times(C(9), times(R[0], ri)), 'entire origin communication')
    require(J == times(C(a**8), times(evaluate(R, C(1/a)), ri)),
            'entire polar communication')
    mu = C()
    for z in q:
        mu = plus(mu, times(C(F(1, 8)), z))
    centered = [plus(z, neg(mu)) for z in q]
    require(tuple(map(sum, zip(*centered))) == C(), 'centered first moment')
    sym = [C(1)]
    for z in centered:
        sym = pmul(sym, [C(1), z])
    # Independent full subset sums, including EVERY eighth-order contribution.
    subsets = []
    for l in range(9):
        total = C()
        for indices in combinations(range(8), l):
            prod = C(1)
            for i in indices:
                prod = times(prod, centered[i])
            total = plus(total, prod)
        subsets.append(total)
    require(sym == subsets, 'all centered elementary functions')
    expansion = [C()]*9
    terms = []
    for l, e in enumerate(sym):
        term = [C()]*l + [times(times(C((-a)**l), e), x)
                               for x in ppow([C(1), times(C(-a), mu)], 8-l)]
        for i, x in enumerate(term):
            expansion[i] = plus(expansion[i], x)
        terms.append(term)
    require(expansion == origin_product, 'whole centered product, orders0 through8')
    E = sum(((z[0]-1)**2+z[1]**2 for z in q), F(0))
    S = sum((z[0]**2+z[1]**2 for z in centered), F(0))
    require(S == E-8*((mu[0]-1)**2+mu[1]**2), 'entire coupled variance identity')
    return encode(dict(a=a, q=q, critical=critical, original_polynomial=p,
                       derivative=derivative, R=R, origin_product=origin_product,
                       polar_product=polar_product, O=O, J=J, mu=mu, E=E, S=S,
                       all_centered_symmetric=sym, all_centered_terms=terms,
                       original_disk_feasibility_NOT_asserted=True))


def run():
    controls = [[C(1)]*8,
                [C(1, F(1, 8)), C(1, -F(1, 8))]*2 +
                [C(F(7, 8), F(1, 16)), C(F(9, 8), -F(1, 16))]*2,
                [C(F(3, 4), F(1, 7)), C(F(5, 4), -F(1, 7))]*2 +
                [C(1, F(1, 9)), C(1, -F(1, 9))]*2]
    return {'agent': 'six-reviewer-1', 'role': 'independent mathematical reviewer',
            'not_original_disk_witnesses': True,
            'cases': [case(q, a) for a in [F(11, 20), F(23, 40), F(3, 5)] for q in controls]}


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, separators=(',', ':')))
