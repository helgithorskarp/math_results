#!/usr/bin/env python3
"""Exact finite checks for the interior surplus stability proof.

six-sendov-2, researcher. Standard library only, one process and thread.
Sparse algebra follows the author's preceding boundary checker, but all
interior identities and bounds are checked here without importing it.
The universal complex-analytic proof is in PROOF.md.
"""

from fractions import Fraction as F
from itertools import combinations
from math import comb


DIM = 18
ZERO = (0,) * DIM
ONE = {ZERO: F(1)}


class Checks:
    def __init__(self):
        self.count = 0
        self.mutations = 0

    def require(self, condition, name):
        if not condition:
            raise AssertionError(name)
        self.count += 1

    def identity(self, left, right, name):
        self.require(left == right, name)

    def reject(self, condition, name):
        if condition:
            raise AssertionError("mutation accepted: " + name)
        self.count += 1
        self.mutations += 1


def constant(value):
    return {ZERO: F(value)} if value else {}


def variable(index):
    return {tuple(int(j == index) for j in range(DIM)): F(1)}


def add(p, q):
    result = p.copy()
    for m, c in q.items():
        result[m] = result.get(m, F(0)) + c
        if not result[m]:
            del result[m]
    return result


def scale(p, c):
    return {m: c*v for m, v in p.items() if c*v}


def mul(p, q):
    result = {}
    for m, c in p.items():
        for n, d in q.items():
            exponent = tuple(a+b for a, b in zip(m, n))
            result[exponent] = result.get(exponent, F(0)) + c*d
    return {m: c for m, c in result.items() if c}


def total(polynomials):
    result = {}
    for p in polynomials:
        result = add(result, p)
    return result


def product(polynomials):
    result = ONE
    for p in polynomials:
        result = mul(result, p)
    return result


def power(p, k):
    return product(p for _ in range(k))


def symmetric(xs, k):
    return total(product(xs[i] for i in indices)
                 for indices in combinations(range(len(xs)), k))


def derivative(p, index):
    result = {}
    for m, c in p.items():
        if m[index]:
            n = tuple(v-int(j == index) for j, v in enumerate(m))
            result[n] = c*m[index]
    return result


def complex_mul(p, q):
    return (add(mul(p[0], q[0]), scale(mul(p[1], q[1]), -1)),
            add(mul(p[0], q[1]), mul(p[1], q[0])))


def complex_symmetric(xs, k):
    real, imag = {}, {}
    for indices in combinations(range(len(xs)), k):
        term = (ONE, {})
        for i in indices:
            term = complex_mul(term, xs[i])
        real, imag = add(real, term[0]), add(imag, term[1])
    return real, imag


def algebra(c):
    xs = [variable(i) for i in range(8)]
    e, L, M = (symmetric(xs, k) for k in (1, 2, 3))
    lhs = add(scale(power(L, 2), 12), scale(mul(e, M), -21))
    rhs = {}
    for i, j in combinations(range(8), 2):
        diff = add(xs[i], scale(xs[j], -1))
        other = [xs[k] for k in range(8) if k not in (i, j)]
        bracket = add(total(power(x, 2) for x in other), symmetric(other, 2))
        rhs = add(rhs, mul(power(diff, 2), bracket))
    c.identity(lhs, rhs, "Newton sum-of-squares identity")
    c.require(len(lhs) == 266, "Newton support size")
    expected = {(2, 2): 12, (2, 1, 1): 3, (1, 1, 1, 1): -12}
    for m, v in lhs.items():
        pattern = tuple(sorted((x for x in m if x), reverse=True))
        c.require(v == expected.get(pattern), "Newton monomial coefficient")
    c.reject(add(scale(power(L, 2), 12), scale(mul(e, M), -20)) == rhs,
             "altered Newton coefficient")

    rs = [add(x, constant(F(1, 2))) for x in xs]
    r1, r2, r3 = (symmetric(rs, k) for k in (1, 2, 3))
    shift = total([r3, scale(r2, -4), scale(r1, F(35, 4)), constant(-14)])
    c.identity(add(M, scale(L, -1)), shift, "shifted saturation")
    c.identity(r2, total([L, scale(e, F(7, 2)), constant(7)]),
               "shifted second symmetric polynomial")
    variance64 = add(scale(total(power(x, 2) for x in xs), 8),
                     scale(power(e, 2), -1))
    c.identity(variance64, add(scale(power(e, 2), 7), scale(L, -16)),
               "variance identity")
    mu = scale(r1, F(1, 8))
    variance = add(scale(total(power(r, 2) for r in rs), F(1, 8)),
                   scale(power(mu, 2), -1))
    real_sum_q = variable(16)
    energy = total([total(power(r, 2) for r in rs),
                    scale(real_sum_q, -2), constant(8)])
    c.identity(energy, total([scale(variance, 8), scale(power(mu, 2), 8),
                             scale(real_sum_q, -2), constant(8)]),
               "interior reciprocal critical energy")

    vertical = [(constant(F(1, 2)), x) for x in xs]
    re2, re3 = (complex_symmetric(vertical, k)[0] for k in (2, 3))
    c.identity(re2, add(constant(7), scale(L, -1)), "vertical e2")
    c.identity(re3, add(constant(7), scale(L, -3)), "vertical e3")
    c.identity(re3, add(scale(re2, 3), constant(-14)), "vertical relation")

    alphas, ts = xs, [variable(i+8) for i in range(8)]
    us = [(add(constant(F(1, 2)), a), t) for a, t in zip(alphas, ts)]
    A, B = total(alphas), total(ts)
    alpha2 = total(power(a, 2) for a in alphas)
    t2 = total(power(t, 2) for t in ts)
    E = add(alpha2, t2)
    re_u2 = complex_symmetric(us, 2)[0]
    signed_rhs = total([scale(alpha2, 2), power(B, 2), constant(-14),
                        scale(A, -7), scale(power(A, 2), -1), scale(re_u2, 2)])
    c.identity(E, signed_rhs, "signed other-root reciprocal energy")
    c.reject(E == add(signed_rhs, scale(A, 14)),
             "discarded sign of the A term")

    eta = variable(16)
    a = add(ONE, scale(eta, -1))
    b = add(ONE, scale(power(a, 2), -1))
    sum_u2 = total(add(power(u[0], 2), power(u[1], 2)) for u in us)
    c.identity(sum_u2, total([constant(2), A, E]),
               "collapsed reciprocal squared norm")
    direct_D = total([mul(b, sum_u2), scale(mul(a, add(constant(4), A)), 2),
                      constant(-8)])
    collapsed_D = total([scale(eta, -4), scale(power(eta, 2), -2),
                         mul(add(constant(2), scale(power(eta, 2), -1)), A),
                         mul(b, E)])
    c.identity(direct_D, collapsed_D, "collapsed radial feasibility identity")
    re_u, im_u = variable(0), variable(1)
    norm_u = add(power(re_u, 2), power(im_u, 2))
    norm_au_minus1 = add(power(add(mul(a, re_u), constant(-1)), 2),
                        power(mul(a, im_u), 2))
    c.identity(add(norm_u, scale(norm_au_minus1, -1)),
               total([mul(b, norm_u), scale(mul(a, re_u), 2), constant(-1)]),
               "single-root disk constraint after clearing denominator")

    w = variable(17)
    g = product(add(ONE, mul(w, x)) for x in xs)
    dg = derivative(mul(w, g), 17)
    coeffs = total(scale(mul(power(w, k), symmetric(xs, k)), k+1)
                   for k in range(9))
    c.identity(dg, coeffs, "reciprocal generating derivative")

    T = variable(17)
    paired = total(scale(power(T, 7-k), 2*F(9, k)*F(comb(8, 9-k), 8))
                   for k in range(1, 5))
    c.identity(paired, scale(total([scale(power(T, 3), 126),
                                   scale(power(T, 4), 84),
                                   scale(power(T, 5), 36),
                                   scale(power(T, 6), 9)]), F(1, 4)),
               "paired high-index coefficient sum")
    for k in range(2, 9):
        c.require(F(comb(6, k-2), comb(k, 2))*F(7, 2) == F(comb(8, k), 8),
                  "pair averaging binomial constant")

    # A genuine interior example with zero OTHER-root radial defect.
    z = variable(0)
    collapsed_p = mul(add(z, scale(a, -1)), power(add(z, ONE), 8))
    projected_p = mul(add(z, constant(-1)), power(add(z, ONE), 8))
    c.identity(add(collapsed_p, scale(projected_p, -1)),
               mul(eta, power(add(z, ONE), 8)), "marked-root projection term")
    c.require(sum(comb(8, k) for k in range(9)) == 256,
              "marked-root coefficient norm")
    c.reject(256*F(1, 10**14) <= 1024*F(0),
             "omitted marked-root projection cost when D_a=0")
    c.identity(derivative(collapsed_p, 0),
               mul(power(add(z, ONE), 7),
                   total([scale(z, 9), ONE, scale(a, -8)])),
               "sharp collapsed slope derivative factorization")
    sigma_numerator = scale(eta, 8)
    denominator = add(constant(2), scale(eta, -1))
    c.identity(total([constant(16), scale(denominator, -8)]),
               sigma_numerator, "sharp-family exact surplus numerator")
    small_x_num = eta
    dominant_x_num = add(constant(16), eta)
    L_numerator = total([scale(power(small_x_num, 2), 21),
                         scale(mul(small_x_num, dominant_x_num), 7)])
    c.identity(L_numerator, scale(mul(eta, add(constant(4), eta)), 28),
               "sharp-family collapsed L numerator")


def bounds(c):
    h0 = F(1, 10**13)
    sqrt_h_upper = F(1, 3000000)
    radius_u, radius_q = 9, 5
    c.require(h0 <= sqrt_h_upper**2, "rational square-root enclosure")
    c.require(1-h0 >= F(99, 100), "marked-root normalization range")
    c.require(7*(1+h0/8) < 8, "reciprocal other-root bound")
    c.require(F(9, 2)+h0 < radius_q, "reciprocal critical bound")
    c.require(F(127, 2)/F(99, 100) < 65, "negative alpha bound")
    c.require(8+65*h0 < radius_u, "vertical projection radius")
    cauchy = sum((F(comb(8, k), (k+1)*7**k) for k in range(1, 9)), F(0))
    c.require(cauchy == F(41980912, 51883209) < 1, "Cauchy sum")
    c.require(2*8*65 == 1040, "signed total real defect")
    c.require(1040 <= 1100, "total phase error")
    p2 = 7*radius_u*1040
    p3 = 21*radius_u**2*1040
    c.require(p2 == 65520 and p3 == 1769040, "projection constants")
    c.require(4*(p3+3*p2) == 7862400 < 8316000, "complex saturation constant")
    phase2 = 2*7*radius_q*1100
    phase3 = 3*21*radius_q**2*1100
    c.require(phase2 == 77000 and phase3 == 1732500, "phase product constants")
    c.require(8316000+phase3+4*phase2+F(35, 4)*1040 == 10365600 < 11000000,
              "shifted saturation error")
    c.require(F(7, 16)*(4+h0)**2 < 8, "upper L bound")
    c.require(F(7, 4)*(4+h0) < 8, "Newton positive multiplier")
    c.require(F(7, 4)*1040*8+8*11000000 < 90000000, "Newton branch separation")
    c.require(F(90000000, 4)+F(7, 64)*(8+h0) < 23000000,
              "regular variance")
    c.require(8*23000000+2080+2+h0/8 < 190000000, "regular reciprocal energy")
    c.require(8*190000000+16*h0 < 1600000000, "regular critical energy")
    c.require(1600000000 == 40000**2, "energy coefficient square root")
    c.require(40000*sqrt_h_upper == F(1, 75) < F(1, 32), "critical radius")
    c.require(2*8*64-8 == 1016, "weighted radial defect")
    c.require(2**8 == 256 and 2**8*4 == 1024, "nine-root radial projection")
    c.require(126+84*F(1, 32)+36*F(1, 32)**2+9*F(1, 32)**3 < 129,
              "paired coefficient envelope")
    c.require(F(129, 4)*1600000000**2*40000 ==
              3302400000000000000000000 < 4*10**24,
              "high-index h-power constant")
    c.require(F(33, 32)**8 < 2, "integration error at z=1")
    high_radius_per_h = 2*10**24*h0*sqrt_h_upper
    c.require(high_radius_per_h == F(200000, 3), "Rouche high-index radius")
    c.require(81+300*1016+high_radius_per_h < 400000, "anchored root matching")
    c.require(400000*h0 < F(1, 100), "small Rouche disks")
    c.require(sum((F(comb(9, k))*F(1, 100)**(k-1) for k in range(2, 10)), F(0)) < 1,
              "Rouche binomial tail")
    c.require(F(101, 100)**8+1 < F(21, 10), "Rouche norm factor")
    c.require(18+F(21, 10)*256 < 8*80, "marked-root Rouche comparison")
    c.require(F(21, 10)*1024 < 8*300, "other-root radial comparison")
    c.require(F(21, 10)*4*10**24 < 8*2*10**24, "high-index comparison")
    c.require(F(1, 50) < F(4, 9), "disjoint Rouche disks")
    c.require(F(90000000, 6) == 15000000, "collapsed L bound")
    c.require(7*520 == 3640, "retained signed A contribution")
    c.require(4*5*1100 == 22000, "imaginary sum energy")
    c.require(2*1040**2*h0+22000+3640+F(2, 3)*15000000+F(7, 3) < 11000000,
              "collapsed reciprocal original-root energy")
    c.require(11000000 < 3317**2, "collapsed square-root enclosure")
    c.require(2*sqrt_h_upper < 1 and 4*3317+1 < 15000, "collapsed root distance")
    c.require((4-1040*h0)/8 > F(1, 3), "largest shifted coordinate")
    c.require(3*15000000 == 45000000, "other shifted-coordinate sum")
    c.require((45000000**2+45001040**2)*h0 < 410, "critical scalar matching")
    c.require(2*5*1100 == 11000, "critical phase energy")
    c.require(2*410+2*11000 == 22820, "combined critical matching")
    c.require(22820 < 152**2 and 4*152+1 < 1000, "critical inversion bound")
    c.require(2*11000000 == 22000000, "collapsed radial obstruction")
    c.require(4-22000000*h0 > 3, "low-surplus collapse exclusion")
    c.require(0 < 1-h0**2/2 <= 1, "radial obstruction positive denominator")
    c.require(4*1600000000 == 6400000000 and 4*400000 == 1600000,
              "analytic-lane necessary energy and root bounds")
    tiny_eta = h0/6
    c.require(8/(2-tiny_eta) < 5, "sharp family lies in h range")
    c.require(7*tiny_eta*(4+tiny_eta)/(2-tiny_eta)**2 < 1,
              "sharp family lies in collapsed branch")


def main():
    c = Checks()
    algebra(c)
    bounds(c)
    print(f"PASS: {c.count} exact checks; {c.mutations} certificate mutations rejected.")


if __name__ == "__main__":
    main()
