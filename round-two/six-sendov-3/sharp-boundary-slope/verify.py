#!/usr/bin/env python3
"""Exact finite algebra for PROOF.md. Python 3.11 standard library only.

This does not certify analytic remainders, compactness or disk containment.
The latter are ordinary arguments in the written proof.
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


# Generic Gaussian-rational polynomial ring. Variables are
# epsilon, z, x, h_1,...,h_7; h_8 is eliminated by the balance equation.
NV = 10
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
        ans = padd(ans, pmul({tuple(f): v}, ppow(replacement, power)))
    return ans


def precord(p):
    return [[list(e), str(v[0]), str(v[1])] for e, v in sorted(p.items())]


def phash(p):
    raw = json.dumps(precord(p), separators=(',', ':')).encode()
    return sha256(raw).hexdigest()


def build_record():
    records = {}
    checks = 0

    def equal(a, b, label):
        nonlocal checks
        require(a == b, label)
        checks += 1

    def reject(fn, label):
        nonlocal checks
        try:
            fn()
        except AlgebraError:
            checks += 1
            return label
        raise AlgebraError('mutation was not rejected: '+label)

    c = K((0, 1, 0))
    d = 2*c*c-1
    v = 2*d*d-1
    y = 1/(3*(1+c))
    x = K(F(2, 3))-y
    H = 14*y
    C = K(F(8, 3))+y
    w4 = 1/(c+d)
    w3 = K(F(2, 3))*(7-(1-d)*w4)
    equal(8*c**3-6*c-1, 0, 'defining cubic relation')
    equal(c+d, (2*c-1)*(1+c), 'trigonometric denominator factorization')
    equal(x, (1+2*d)/(3*(c+d)), 'primal x normalization')
    equal(y, (2*c-1)/(3*(c+d)), 'primal y normalization')
    equal(x+y, K(F(2, 3)), 'balanced first-order original motion')
    equal(C, 8-8*x-7*y, 'first-power coefficient')
    equal(C, (10*c+8*d-1)/(3*(c+d)), 'alternate coefficient')
    equal(C, 8-w3-w4, 'dual coefficient')
    equal(F(3, 16)*w3+(1+c)*w4/8, 1, 'dual real first moment')
    equal(F(3, 28)*w3+(1-d)*w4/14, F(1, 2), 'dual real second moment')
    equal(K(F(3, 16))*(1-d)/14
          -K(F(3, 28))*(1+c)/8,
          -3*(c+d)/224, 'moment constraint determinant')
    A = [1-d, 1-v, K(F(3, 2)), 1+c]
    B = [1-v, 1+c, K(F(3, 2)), 1-d]
    slacks = [1-x*a-y*b for a, b in zip(A, B)]
    equal(slacks[2], 0, 'cube-root tangency')
    equal(slacks[3], 0, 'outer nonagon pair tangency')
    equal(slacks[0]+slacks[1], 1, 'two strict radial slacks')
    equal(8*(1-x)-H/2, C, 'critical-profile objective coefficient')

    def f(t):
        return 8*t**3-6*t-1

    lo, hi = F(3, 4), F(1)
    require(f(lo) < 0 < f(hi), 'initial cubic isolation')
    require(24*lo*lo-6 > 0, 'monotonic cubic interval')
    checks += 2
    for _ in range(72):
        mid = (lo+hi)/2
        value = f(mid)
        require(value != 0, 'bisection did not hit rational cubic root')
        if value < 0:
            lo = mid
        else:
            hi = mid
    require(f(lo) < 0 < f(hi), 'final cubic isolation')
    checks += 1
    for label, a in [('x', x), ('y', y), ('H', H), ('w3', w3), ('w4', w4),
                     ('radial slack k1', slacks[0]),
                     ('radial slack k2', slacks[1]),
                     ('C-14/5', C-F(14, 5)), ('3-H', 3-H),
                     ('4-C', 4-C), ('c-1/2', c-F(1, 2))]:
        lower, upper = a.interval(lo, hi)
        require(lower > 0, 'positive real-embedding sign: '+label)
        checks += 1
        records[label] = a.record()
    lower, upper = C.interval(lo, hi)
    decimal_lo = F(2838515200687, 10**12)
    decimal_hi = F(2838515200688, 10**12)
    require(decimal_lo < lower <= upper < decimal_hi, 'slope decimal enclosure')
    checks += 1
    records['slope_enclosure'] = [str(decimal_lo), str(decimal_hi)]
    records['embedding_interval'] = [str(lo), str(hi)]
    records['constants'] = {name: a.record() for name, a in
                            [('c', c), ('d', d), ('v', v), ('x', x),
                             ('y', y), ('H', H), ('C', C),
                             ('w3', w3), ('w4', w4)]}
    records['radial_slacks'] = [a.record() for a in slacks]

    # An independent universal formal calculation at seven free coordinates.
    ep, z, X = (pv(i) for i in range(3))
    hs = [pv(i) for i in range(3, 10)]
    hs.append(pscale(padd(*hs), -1))
    H2 = padd(*(ppow(h, 2) for h in hs))
    H3 = padd(*(ppow(h, 3) for h in hs))
    equal(padd(*hs), {}, 'full profile balance')
    pair_sum = padd(*(pmul(hs[i], hs[j]) for i in range(8)
                      for j in range(i+1, 8)))
    triple_sum = padd(*(pmul(hs[i], hs[j], hs[k]) for i in range(8)
                        for j in range(i+1, 8) for k in range(j+1, 8)))
    equal(pair_sum, pscale(H2, F(-1, 2)), 'full balanced second Newton identity')
    equal(triple_sum, pscale(H3, F(1, 3)), 'full balanced third Newton identity')
    derivative = pscale(pmul(*(padd(z, pmul(X, ppow(ep, 2)),
                                   pscale(ppow(ep, 3), -1),
                                   pscale(pmul(ep, h), 0, -1))
                              for h in hs)), 9)
    expected_derivative = padd(
        pscale(ppow(z, 8), 9),
        pscale(pmul(ppow(ep, 2), X, ppow(z, 7)), 72),
        pscale(pmul(ppow(ep, 2), H2, ppow(z, 6)), F(9, 2)),
        pscale(pmul(ppow(ep, 3), ppow(z, 7)), -72),
        pscale(pmul(ppow(ep, 3), H3, ppow(z, 5)), 0, 3))
    equal(derivative, expected_derivative, 'complete derivative jet')
    primitive = pint(derivative, 1)
    a = padd(pc(1), pscale(ppow(ep, 2), -1))
    polynomial = padd(primitive, pscale(psubst(primitive, 1, a), -1))
    expected_poly = padd(
        ppow(z, 9), pc(-1), pscale(ppow(ep, 2), 9),
        pscale(pmul(ppow(ep, 2), X, padd(ppow(z, 8), pc(-1))), 9),
        pscale(pmul(ppow(ep, 2), H2, padd(ppow(z, 7), pc(-1))), F(9, 14)),
        pscale(pmul(ppow(ep, 3), padd(ppow(z, 8), pc(-1))), -9),
        pscale(pmul(ppow(ep, 3), H3, padd(ppow(z, 6), pc(-1))), 0, F(1, 2)))
    equal(polynomial, expected_poly, 'complete anchored polynomial jet')
    equal(pdiff(polynomial, 1), derivative, 'primitive derivative recovery')
    equal(psubst(polynomial, 1, a), {}, 'marked root in full jet')

    # A scalar inverse-distance jet uses one unconstrained h coordinate.
    h = hs[0]
    real_distance = padd(pc(1), pmul(padd(X, pc(-1)), ppow(ep, 2)),
                         pscale(ppow(ep, 3), -1))
    distance2 = padd(ppow(real_distance, 2), pmul(ppow(ep, 2), ppow(h, 2)))
    u = padd(distance2, pc(-1))
    reciprocal = padd(pc(1), pscale(u, F(-1, 2)),
                       pscale(ppow(u, 2), F(3, 8)),
                       pscale(ppow(u, 3), F(-5, 16)))
    expected_reciprocal = padd(pc(1), pmul(ppow(ep, 2),
                               padd(pc(1), pscale(X, -1),
                                    pscale(ppow(h, 2), F(-1, 2)))),
                               ppow(ep, 3))
    equal(reciprocal, expected_reciprocal, 'generic inverse-distance jet')
    equal(pmul(ppow(reciprocal, 2), distance2), pc(1),
          'inverse-distance defining equation through third order')
    records['generic_jets'] = {
        'variables': ['epsilon', 'z', 'x']+['h'+str(i) for i in range(1, 8)],
        'epsilon_order': ORDER,
        'derivative_terms': len(derivative),
        'derivative_hash': phash(derivative),
        'anchored_polynomial_terms': len(polynomial),
        'anchored_polynomial_hash': phash(polynomial),
        'reciprocal_terms': len(reciprocal),
        'reciprocal_hash': phash(reciprocal),
        'balance_second_terms': len(H2),
        'balance_third_terms': len(H3)}

    mutations = [
        reject(lambda: equal(C+F(1, 100), 8-w3-w4, 'wrong coefficient'),
               'slope corruption'),
        reject(lambda: equal((x+F(1, 100))*A[3]+y*B[3], 1,
                             'wrong active constraint'), 'primal corruption'),
        reject(lambda: equal(pscale(derivative, F(8, 9)), expected_derivative,
                             'wrong degree-nine derivative'), 'degree corruption'),
        reject(lambda: equal(padd(polynomial,
                                  pscale(pmul(ppow(ep, 3),
                                        padd(ppow(z, 8), pc(-1))), 18)),
                             expected_poly, 'outward correction'),
               'inward-sign corruption'),
        reject(lambda: equal(padd(expected_reciprocal, ppow(ep, 3)),
                             reciprocal, 'wrong reciprocal coefficient'),
               'reciprocal corruption'),
        reject(lambda: equal(triple_sum, pscale(H3, F(1, 2)),
                             'wrong balanced third moment'), 'Newton corruption')]
    records['mutations_rejected'] = mutations
    records['exact_checks'] = checks
    records['trust_boundary'] = ('finite algebra only; uniform analytic '
                                 'arguments and credited premises are in PROOF.md')
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit-fixture', action='store_true')
    parser.add_argument('--fixture', type=Path,
                        default=Path(__file__).with_name('expected.json'))
    args = parser.parse_args()
    records = build_record()
    encoded = json.dumps(records, sort_keys=True, indent=2)+'\n'
    if args.emit_fixture:
        print(encoded, end='')
        return
    require(args.fixture.is_file(), 'required fixture is missing')
    try:
        fixture = json.loads(args.fixture.read_text())
    except (ValueError, OSError) as e:
        raise AlgebraError('required fixture is malformed') from e
    require(fixture == records, 'complete fixture differs')
    digest = sha256(encoded.encode()).hexdigest()
    print('PASS: '+str(records['exact_checks'])+' exact checks; '
          +str(len(records['mutations_rejected']))+' mutations rejected.')
    print('Complete record SHA256: '+digest)
    print('Exact slope enclosure: '+str(records['slope_enclosure']))


if __name__ == '__main__':
    main()
