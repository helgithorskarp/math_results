#!/usr/bin/env python3
"""Exact algebra for PROOF.md; Python standard library, no external input.

Domain Q[m,a,c,z,q,h,x,r,U1,U2,R,E,A,I], characteristic zero.
The dimension m=n-1 remains an indeterminate, with m>=3 in sign checks.
Free matrix words retain their order; trace words are reduced only by
projection identities and cyclicity. Written analytic arguments are not
formalized by this program. Polynomial arithmetic is adapted from the
author's preceding uniform-collapsed checker, not an independent review.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
import json


class Poly:
    def __init__(self, terms=None):
        if isinstance(terms, (int, F)):
            terms = {(): F(terms)}
        self.t = {k: F(v) for k, v in (terms or {}).items() if v}

    @staticmethod
    def var(i):
        return Poly({(i,): F(1)})

    def __add__(self, other):
        out = dict(self.t)
        for k, v in aspoly(other).t.items():
            out[k] = out.get(k, F(0)) + v
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.t.items()})

    def __sub__(self, other):
        return self + (-aspoly(other))

    def __rsub__(self, other):
        return aspoly(other) - self

    def __mul__(self, other):
        out = {}
        for k, v in self.t.items():
            for l, w in aspoly(other).t.items():
                key = tuple(sorted(k+l))
                out[key] = out.get(key, F(0)) + v*w
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        if not isinstance(exponent, int) or exponent < 0:
            raise ValueError("Only nonnegative integer powers")
        out = Poly(1)
        for _ in range(exponent):
            out *= self
        return out

    def diff(self, variable):
        out = {}
        for k, v in self.t.items():
            count = k.count(variable)
            if count:
                key = list(k)
                key.remove(variable)
                key = tuple(key)
                out[key] = out.get(key, F(0)) + count*v
        return Poly(out)

    def at(self, variable, value):
        out = Poly(0)
        for k, v in self.t.items():
            count = k.count(variable)
            base = tuple(i for i in k if i != variable)
            out += Poly({base: v}) * aspoly(value)**count
        return out

    def __eq__(self, other):
        return self.t == aspoly(other).t


def aspoly(value):
    return value if isinstance(value, Poly) else Poly(value)


def trace_cycle(word):
    """Normal form of a trace word: adjacent P,Q annihilate; P^2=P,Q^2=Q."""
    word = list(word)
    while word:
        reduction = None
        for i in range(len(word)):
            j = (i+1) % len(word)
            if i == j:
                break
            if word[i] in "PQ" and word[j] in "PQ":
                if word[i] != word[j]:
                    return None
                reduction = j
                break
        if reduction is None:
            break
        word.pop(reduction)
    if not word:
        return ()
    word = tuple(word)
    return min(word[i:]+word[:i] for i in range(len(word)))


def residue(np, nq):
    """Residue of t^(2-np)*(t-G)^(-nq) as (coefficient, power of G)."""
    degree = np-3
    if degree < 0:
        return F(0), 0
    if nq == 0:
        return F(degree == 0), 0
    return F((-1)**nq*comb(nq+degree-1, degree)), -nq-degree


def nc_mul(*factors):
    """Free associative multiplication, retaining every matrix factor."""
    out = {(): F(1)}
    for factor in factors:
        new = {}
        for word, coefficient in out.items():
            for other, value in factor.items():
                key = word+other
                new[key] = new.get(key, F(0))+coefficient*value
        out = {k: v for k, v in new.items() if v}
    return out


def nc_add(*polynomials):
    out = {}
    for polynomial in polynomials:
        for word, value in polynomial.items():
            out[word] = out.get(word, F(0))+value
    return {k: v for k, v in out.items() if v}


def nc_scale(polynomial, scalar):
    return {k: scalar*v for k, v in polynomial.items() if scalar*v}


def run():
    groups = {}

    def check(group, condition, label):
        if not condition:
            raise AssertionError(group+": "+label)
        groups[group] = groups.get(group, 0)+1

    m, a, c, z, q, h, x, U1, U2, R, E, A, I = [
        Poly.var(i) for i in range(13)]
    n, d, b = m+1, a+1, 1-a*a
    kappaN = d*(2*m*a-m-2)  # kappa=kappaN/(2m)

    check("disk_algebra",
          b*((1+d*A)**2+(d*I)**2)+2*a*d*(1+d*A)-d*d ==
          d*d*(2*A+b*(A*A+I*I)), "centered disk constraint")
    check("disk_algebra", (m-2)*d-2*m*b == kappaN,
          "gamma/(2v)-b=kappa")
    check("disk_algebra",
          8*m*(1-b)-2*kappaN == 2*m*(1-a)+4*m*a*a+4*d,
          "real-part l1 budget, signed kappa")
    check("disk_algebra", 2*m-4-kappaN ==
          (1-a)*(2*m*a+3*m-2), "kappa<=gamma<1")

    # The index contraction tr(D^r1 J ... D^rk J)=product sum(delta^rj)
    # makes the dimension symbolic rather than instantiate any matrix size.
    compressedN = (m*m-2*m)*U2+U1*U1
    check("compressed_trace", m*m*U2-m*U2-m*U2+U1*U1 == compressedN,
          "rank-one compressed moment")
    check("compressed_trace",
          -(m*m-2*m)*(2*R-E)-A*A+I*I ==
          (m*m-2*m)*E-2*(m*m-2*m)*R-A*A+I*I,
          "negative real second moment")

    moments = []
    for order in range(4):
        result = {}
        for word in product("PQ", repeat=order+1):
            interlaced = []
            for i, projection in enumerate(word):
                interlaced.append(projection)
                if i != order:
                    interlaced.append("V")
            cycle = trace_cycle(tuple(interlaced))
            coefficient, power = residue(word.count("P"), word.count("Q"))
            if cycle is None:
                coefficient = F(0)
            expected = F(0)
            expected_power = 0
            if order == 2 and word == ("P", "P", "P"):
                expected = F(1)
            if order == 3 and word in [
                    ("P", "P", "Q", "P"), ("P", "Q", "P", "P")]:
                expected, expected_power = F(-1), -1
            check("contour_words", coefficient == expected and
                  (not coefficient or power == expected_power),
                  str(order)+":"+"".join(word))
            if coefficient:
                key = cycle, power
                result[key] = result.get(key, F(0))+coefficient
        moments.append({k: v for k, v in result.items() if v})
    c2 = trace_cycle(("P", "V", "P", "V"))
    c3 = trace_cycle(("P", "V", "P", "V", "Q", "V"))
    check("contour_moments", moments[:2] == [{}, {}], "M0=M1=0")
    check("contour_moments", moments[2] == {(c2, 0): F(1)}, "M2")
    check("contour_moments", moments[3] == {(c3, -1): F(-2)}, "M3=-2 tr/G")

    # All coefficients are real rational functions of the real gap G.
    # Expand the three slots in M3(X+iY) and retain exact powers of i.
    phases = ((1, 0), (0, 1), (-1, 0), (0, -1))
    cubic_real_words = {}
    pure_y = None
    for letters in product("XY", repeat=3):
        real, imaginary = phases[letters.count("Y") % 4]
        check("cubic_reality", not real or "X" in letters,
              "every real cubic term contains X: "+"".join(letters))
        if real:
            cubic_real_words[letters] = -2*real
        if letters == ("Y", "Y", "Y"):
            pure_y = (-2*real, -2*imaginary)
    check("cubic_reality", pure_y == (0, 2), "pure Y term is 2i times real trace/G")

    rr, xx, ww = ({("R",): F(1)}, {("X",): F(1)}, {("W",): F(1)})
    vv = nc_add(xx, ww)
    left = nc_add(nc_mul(rr, vv, rr, vv, rr, vv, rr),
                  nc_scale(nc_mul(rr, ww, rr, ww, rr, ww, rr), -1))
    right = nc_add(nc_mul(rr, xx, rr, vv, rr, vv, rr),
                   nc_mul(rr, ww, rr, xx, rr, vv, rr),
                   nc_mul(rr, ww, rr, ww, rr, xx, rr))
    check("noncommutative_telescope", left == right,
          "three ordered differences, no commutativity assumption")

    check("norm_constants", F(1, 2)**3*2**4*3 == 6,
          "cubic real-error contour prefactor")
    check("norm_constants", F(1, 2)**3*2*2**4 == 4,
          "order-four contour prefactor")
    check("norm_constants", F(4)/(1-F(1, 2)) == 8,
          "geometric tail denominator")
    check("norm_constants", 2*F(1, 4) == F(1, 2),
          "Neumann bound 2n epsilon<=1/2 from n epsilon<=1/4")
    check("norm_constants", F(3, 2)*(F(3, 2)-F(1, 144)) > 2,
          "original-root radius conversion")

    # Nonnegative coefficients after m=y+3 are universal certificates.
    y = Poly.var(13)
    certificates = {
        "real_trace_error_3": m*m+4*m-1,
        "cubic_and_tail_moment_10": 2*m*n**4-6*m*n**3-3,
        "projected_gap_3_over_m": 4*m*m-12*m+3,
        "real_displacement_5n": 4*m-3*n,
        "energy_implies_positive_real_part": 16*n*n-20*n,
        "modulus_displacement_4n2": 2*n*n-5*n,
        "angular_error_11mn4": m*n**4-8*n*n,
        "positive_energy_cap_implies_basic_cap": 22*m*n*n-16,
        "root_radius_at_most_1_over_144": 3*m*n*n-144,
        "root_radius_energy_cap": (36-22)*m*n**4,
        "cutoff_below_one": m-2,
        "pair_discriminant_negative": m-2,
    }
    for label, polynomial in certificates.items():
        shifted = polynomial.at(0, y+3)
        check("uniform_signs", all(v >= 0 for v in shifted.t.values()),
              label)
    check("uniform_signs", certificates["projected_gap_3_over_m"].at(0, y+3)
          == 4*y*y+12*y+3, "explicit gap polynomial")
    check("uniform_signs", 22*m*n**4-16*n*n ==
          n*n*(22*m*n*n-16), "positive cap denominator clearing")

    # Recheck the needed one-pair identities of the cited input.
    g = z*z+2*c*z+1
    critical = (z+1)*g+(m-2)*(z-a)*g+(z-a)*(z+1)*g.diff(3)
    D = a*a+2*a*c+1
    reciprocal = (d*D*q**3-((m-1)*D+4*d*(a+c))*q*q
                  +(2*m*(a+c)+3*d)*q-n)
    substituted = Poly(0)
    for monomial, coefficient in critical.t.items():
        power = monomial.count(3)
        base = tuple(i for i in monomial if i != 3)
        substituted += (Poly({base: coefficient})*(a*q-1)**power
                        *q**(3-power))
    check("moving_pair", substituted == reciprocal,
          "differentiate and translate the critical cubic")
    Lscaled = -2*a*x**3+(2*a*(m-1)+4*d)*x*x-2*m*d*x
    normalized = d*d*(x-1)**2*(x-n)+h*Lscaled
    transformed = Poly(0)
    for monomial, coefficient in reciprocal.t.items():
        power = monomial.count(4)
        base = tuple(i for i in monomial if i != 4)
        transformed += Poly({base: coefficient})*x**power*d**(3-power)
    check("moving_pair", transformed.at(2, 1-h) == d*normalized,
          "normalized reciprocal cubic")
    f0 = (x-1)**2*(x-n)
    K = m+2-m*a
    betaN = -2*n*K  # denominator m^2 d^2
    LprimeN = -2*a*n*(m+5)+(6*m+8)*d  # denominator d^2
    chiN = -2*betaN**2-m*LprimeN*betaN  # denominator m^5 d^4
    check("implicit_coefficients", f0.diff(6).at(6, n) == m*m,
          "simple-root derivative")
    check("implicit_coefficients", f0.diff(6).diff(6).at(6, n) == 4*m,
          "second simple-root derivative")
    check("implicit_coefficients", Lscaled.at(6, n) == -betaN,
          "order h equation")
    check("implicit_coefficients", Lscaled.diff(6).at(6, n) == LprimeN,
          "L prime")
    check("implicit_coefficients",
          m**2*chiN+2*m**2*betaN**2+m**3*LprimeN*betaN == 0,
          "order h^2 implicit equation, common denominator m^5 d^4")
    check("moving_pair", 6*a*m-4*m*d+2*K == -2*(m-2),
          "negative discriminant derivative")
    check("moving_pair", betaN+2*a*m*n == 2*n*(2*m*a-m-2),
          "linear gap coefficient")
    check("moving_pair", ((a+c)*d-D)**2+d*d*(1-c*c) ==
          2*(1-c)*D, "exact reciprocal energy")
    check("moving_pair", (2-2*c).at(2, 1-h) == 2*h,
          "original-root distance squared is 2h")

    # Verify the modulus expansion with formal B=beta/n, T=chi/n, S=s.
    Br, Tr, Sr = [Poly.var(i) for i in range(14, 17)]
    def mul2(left, right):
        return [sum((left[i]*right[k-i] for i in range(k+1)), Poly(0))
                for k in range(3)]
    denominator = [Poly(1), Br-Sr, Tr-Sr*Br]
    sqrt_series = [Poly(1), -F(1, 2)*(Br-Sr),
                   F(3, 8)*(Br-Sr)**2-F(1, 2)*(Tr-Sr*Br)]
    reciprocal_check = mul2(mul2(sqrt_series, sqrt_series), denominator)
    for order, coefficient in enumerate(reciprocal_check):
        check("modulus_series", coefficient == int(order == 0),
              "positive sqrt(W), order "+str(order))

    # Specialize general beta,chi at a=(m+2)/(2m), clearing denominators.
    def cutoff_numerator(polynomial):
        degree = max((k.count(1) for k in polynomial.t), default=0)
        out = Poly(0)
        for monomial, coefficient in polynomial.t.items():
            power = monomial.count(1)
            base = tuple(i for i in monomial if i != 1)
            out += (Poly({base: coefficient})*(m+2)**power
                    *(2*m)**(degree-power))
        return out, (2*m)**degree
    dN, sN = 3*m+2, 4*m*(m+2)
    LN = -sN*n*(m+5)+2*m*(6*m+8)*dN
    beta0N = -n*sN  # denominator m dN^2
    chi0N = n*sN*(LN-2*n*sN)  # denominator m^3 dN^4
    bcN, bcD = cutoff_numerator(betaN)
    ccN, ccD = cutoff_numerator(chiN)
    check("quartic_coefficient", 4*m*bcN == beta0N*bcD,
          "specialized beta")
    check("quartic_coefficient", 16*m*m*ccN == chi0N*ccD,
          "specialized chi")
    innerN = (sN*(LN-2*n*sN)+F(3, 4)*sN*sN*n*n-sN*sN*m)
    H = m**3-4*m*m+13*m+18
    check("quartic_coefficient", 2*innerN == -8*m*m*(m+2)*H,
          "negative h^2 gap coefficient")
    check("quartic_coefficient", H.at(0, y+3) == y**3+5*y*y+16*y+48,
          "H positive for every m>=3")
    # Multiply the h^2 gap coefficient by d0^8/16 and clear denominators.
    Cnum = (m+2)*H*dN**3  # denominator 512 m^7
    check("quartic_coefficient",
          8*m*(m+2)*H*dN**8*512*m**7 ==
          Cnum*dN**5*16*(2*m)**8,
          "quartic energy conversion: C_m")
    check("quartic_coefficient",
          F(10*(8**3-4*8**2+13*8+18)*(3*8+2)**3, 512*8**7)
          == F(2076165, 33554432), "degree-nine exact coefficient")
    check("degree_nine", 11*8*9**4 == 577368, "quartic error constant")
    check("degree_nine", 22*8*9**4 == 1154736, "positive energy cap")
    check("degree_nine", 3*8*9**2 == 1944, "square-root root cap")
    check("degree_nine", F(8+2, 2*8) == F(5, 8), "cutoff")

    mutations = {
        "wrong_cubic_residue_sign":
            moments[3] != {(c3, -1): F(2)},
        "pure_imaginary_cubic_is_real":
            pure_y != (2, 0),
        "wrong_projected_gap_constant":
            any(v < 0 for v in
                ((2*m-1)**2-8*m*m).at(0, y+3).t.values()),
        "positive_cutoff_gap":
            2*innerN != 8*m*m*(m+2)*H,
        "quartic_conversion_missing_16":
            8*m*(m+2)*H*dN**8*512*m**7 !=
            Cnum*dN**5*(2*m)**8,
    }
    for label, rejected in mutations.items():
        if not rejected:
            raise AssertionError("Mutation escaped: "+label)
    print(json.dumps({
        "status": "PASS", "exact_checks": sum(groups.values()),
        "groups": groups, "mutations_rejected": list(mutations),
        "symbolic_degree_parameter": "m=n-1",
        "external_inputs": 0, "floating_point_operations": 0,
        "scope": "symbolic algebra and uniform sign certificates; not formalization"
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    run()
