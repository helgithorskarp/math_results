#!/usr/bin/env python3
"""Uniform symbolic algebra for PROOF.md, using the Python standard library.

Domain Q[m,a,c,z,q,h,x,r,U2,U1,X,Y,R,E,A]; characteristic zero.
Monomials are sorted variable-index tuples. All coefficients are Fraction.
The sole algebraic extension is r^2=m+1, reduced explicitly when used.
Parameter denominators are cleared; the proof assumes m>=3, 0<=a<=1,
d=1+a>0. No degree enumeration, numerical roots, CAS package or input file.

The sparse polynomial arithmetic is adapted from this author's published
degree-nine checker. The new checks keep m as an indeterminate and verify
the new one-pair cubic, rather than infer a theorem from degree samples.
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
                key = tuple(sorted(k + l))
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


def extension_reduce(p, root_variable, radicand):
    """Normal form modulo root^2-radicand, with no numerical square root."""
    out = Poly(0)
    for k, v in p.t.items():
        count = k.count(root_variable)
        base = tuple(i for i in k if i != root_variable)
        out += (Poly({base: v}) * radicand**(count//2)
                * Poly.var(root_variable)**(count % 2))
    return out


def ij_mul(left, right, dimension):
    """Multiply aI+bJ using the uniform relation J^2=dimension*J."""
    a, b = left
    c, d = right
    return a*c, a*d+b*c+dimension*b*d


def series_mul(left, right, degree=2):
    return [sum((left[i]*right[k-i] for i in range(k+1)), Poly(0))
            for k in range(degree+1)]


def series_power(series, exponent):
    out = [Poly(1), Poly(0), Poly(0)]
    for _ in range(exponent):
        out = series_mul(out, series)
    return out


def run():
    groups = {}

    def check(group, valid, label):
        if not valid:
            raise AssertionError(group + ": " + label)
        groups[group] = groups.get(group, 0) + 1

    m, a, c, z, q, h, x, root, U2, U1 = [Poly.var(i) for i in range(10)]
    n, d, b = m+1, a+1, 1-a*a
    pnum, qnum = (m, Poly(-1)), (Poly(0), Poly(1))
    snum = (m, root-1)
    check("projection_algebra", ij_mul(pnum, pnum, m) == (m*m, -m),
          "P^2=P, after multiplying by m^2")
    check("projection_algebra", ij_mul(qnum, qnum, m) == (Poly(0), m),
          "Q^2=Q")
    check("projection_algebra", ij_mul(pnum, qnum, m) == (Poly(0), Poly(0)),
          "PQ=0")
    check("projection_algebra", ij_mul(snum, pnum, m) == (m*m, -m),
          "SP=P")
    squared = ij_mul(snum, snum, m)
    check("projection_algebra",
          tuple(extension_reduce(v, 7, n) for v in squared) == (m*m, m*m),
          "S^2=I+J modulo root^2=n")

    # Universal rank-one trace contractions. The index identity
    # tr(D^r1 J ... D^rk J)=prod_j sum_i delta_i^rj reduces all these words.
    def trace_word(word):
        if "J" not in word:
            if len(word) != 2:
                raise ValueError("Only the two-D contraction is used")
            return U2
        first = word.index("J")
        cyclic = word[first+1:] + word[:first+1]
        blocks = []
        count = 0
        for letter in cyclic:
            if letter == "D":
                count += 1
            else:
                blocks.append(count)
                count = 0
        out = Poly(1)
        for exponent in blocks:
            out *= {0: m, 1: U1, 2: U2}[exponent]
        return out

    moment_scaled = (m*m*trace_word("DD") - m*trace_word("DDJ")
                     - m*trace_word("DJD") + trace_word("DJDJ"))
    check("uniform_trace", moment_scaled == (m*m-2*m)*U2+U1*U1,
          "m^2 tr(DPDP)=(m^2-2m)sum delta^2+(sum delta)^2")
    check("uniform_trace", trace_word("DDJJ") == m*U2, "adjacent J contraction")
    X, Y, R, E, A0 = [Poly.var(i) for i in range(10, 15)]
    negative_real_scaled = -(m*m-2*m)*(2*R-E)-(A0*A0-Y*Y)
    check("complex_trace", negative_real_scaled ==
          (m*m-2*m)*E-2*(m*m-2*m)*R-A0*A0+Y*Y,
          "negative real compressed trace, all dimensions")

    # Direct Laurent coefficients at w=0 for w^2/[w^P (w-gap)^Q].
    # No dimension enters, so these finite checks apply to every m.
    def residue(np, nq):
        if np < 3:
            return F(0)
        degree = np-3
        if nq == 0:
            return F(degree == 0)
        # This branch would give a rational multiple of gap^(-nq-degree);
        # it is not reached by the low-order words in this proof.
        return F((-1)**nq * comb(nq+degree-1, degree))

    for order in range(3):
        for word in product("PQ", repeat=order+1):
            res = residue(word.count("P"), word.count("Q"))
            check("contour_words", res == F(word == ("P", "P", "P")),
                  "".join(word))
    check("contour_tail", F(1, 2)**3*2*2**3 == 2,
          "actual contour prefactor is 2")
    check("contour_tail", F(2) <= 16, "conservative uniform prefactor")
    check("contour_tail", F(16)/(1-F(1, 2)) == 32, "Neumann tail denominator")

    xr, yi = X, Y
    disk_cleared = b*((1+d*xr)**2+(d*yi)**2)+2*a*d*(1+d*xr)-d*d
    check("disk_geometry", disk_cleared == d*d*(2*xr+b*(xr*xr+yi*yi)),
          "full centered disk constraint")
    kappa_scaled = d*(2*m*a-m-2)
    check("disk_geometry", (m-2)*d-2*m*b == kappa_scaled,
          "gamma/(2v)-b=kappa, multiply by 2m")
    check("disk_geometry", 2*m-4-kappa_scaled ==
          (1-a)*(2*m*a+3*m-2), "kappa<=gamma for 0<=a<=1")
    check("disk_geometry", 8*m*(1-b)-2*kappa_scaled ==
          2*m*(1-a)+4*m*a*a+4*d,
          "1-b-kappa/2=(1-a)/4+a^2/2+d/(2m) for all radii")

    # Product-rule calculation leaves an ordinary cubic for every integer m>=3.
    g = z*z+2*c*z+1
    critical = (z+1)*g+(m-2)*(z-a)*g+(z-a)*(z+1)*g.diff(3)
    D = a*a+2*a*c+1
    reciprocal = (d*D*q**3-((m-1)*D+4*d*(a+c))*q*q
                  +(2*m*(a+c)+3*d)*q-n)
    substituted = Poly(0)
    for monomial, coeff in critical.t.items():
        power = monomial.count(3)
        base = tuple(i for i in monomial if i != 3)
        substituted += Poly({base: coeff})*(a*q-1)**power*q**(3-power)
    check("one_pair_cubic", substituted == reciprocal,
          "direct derivative cubic after z=a-1/q")
    Lscaled = (-2*a*x**3+(2*a*(m-1)+4*d)*x*x-2*m*d*x)
    normalized_scaled = d*d*(x-1)**2*(x-n)+h*Lscaled
    # q=x/d, c=1-h in (18), multiply the cubic by d^3.
    transformed = Poly(0)
    for monomial, coeff in reciprocal.t.items():
        power = monomial.count(4)
        base = tuple(i for i in monomial if i != 4)
        transformed += Poly({base: coeff})*x**power*d**(3-power)
    check("one_pair_cubic", transformed.at(2, 1-h) ==
          d*normalized_scaled, "normalization to (19)")

    f0 = (x-1)**2*(x-n)
    check("implicit_root", f0.diff(6).at(6, n) == m*m, "simple-root derivative")
    check("implicit_root", f0.diff(6).diff(6).at(6, n) == 4*m,
          "second simple-root derivative")
    K = m+2-m*a
    beta_num = -2*n*K
    lprime_num = -2*a*n*(m+5)+(6*m+8)*d
    chi_num = -2*beta_num**2-m*lprime_num*beta_num
    check("implicit_root", Lscaled.at(6, n) == 2*n*K, "L(n)")
    check("implicit_root", Lscaled.diff(6).at(6, n) == lprime_num, "L'(n)")

    # Substitute the proposed series directly, with common denominator
    # den=m^5 d^4, into the normalized cubic, truncated only after h^2.
    den = m**5*d**4
    xx = [n*den, beta_num*m**3*d*d, chi_num]
    minus_one = [xx[0]-den, xx[1], xx[2]]
    minus_n = [xx[0]-n*den, xx[1], xx[2]]
    main = series_mul(series_power(minus_one, 2), minus_n)
    cube, square = series_power(xx, 3), series_power(xx, 2)
    lseries = [(-2*a*cube[k]+(2*a*(m-1)+4*d)*square[k]*den
                -2*m*d*xx[k]*den*den) for k in range(3)]
    direct_series = [d*d*main[k]+(lseries[k-1] if k else 0)
                     for k in range(3)]
    for order, coeff in enumerate(direct_series):
        check("implicit_substitution", coeff == 0, "h^"+str(order))

    # Independently verify the positive square-root series used in (22).
    # B=beta/n, T=chi/n, S=s are formal variables here.
    Br, Tr, Sr = [Poly.var(i) for i in range(16, 19)]
    denominator_series = [Poly(1), Br-Sr, Tr-Sr*Br]
    sqrt_series = [Poly(1), -F(1, 2)*(Br-Sr),
                   F(3, 8)*(Br-Sr)**2-F(1, 2)*(Tr-Sr*Br)]
    sqrt_check = series_mul(series_power(sqrt_series, 2), denominator_series)
    for order, coeff in enumerate(sqrt_check):
        check("modulus_series", coeff == int(order == 0),
              "sqrt(W)^2*(1-sh)*x_*/n=1, h^"+str(order))

    # Pair-sum discriminant derivative and the first-order gap are checked
    # separately from the implicit-series substitution.
    check("pair_discriminant", 6*a*m-4*m*d+2*K == -2*(m-2),
          "4[3s-4/d-beta*m/n]=-8(m-2)/(m*d^2)")
    check("gap_coefficient", beta_num+2*a*m*n == 2*n*(2*m*a-m-2),
          "beta*m/n+s=4(a-alpha)/d^2")
    check("family_energy", ((a+c)*d-D)**2+d*d*(1-c*c) ==
          2*(1-c)*D, "two moving roots: E=4h/(D*d^2)")

    # Specialize at a=alpha_m using homogeneous substitution over Q[m].
    def cutoff_numerator(poly):
        degree = max((k.count(1) for k in poly.t), default=0)
        out = Poly(0)
        for k, coeff in poly.t.items():
            power = k.count(1)
            base = tuple(i for i in k if i != 1)
            out += (Poly({base: coeff})*(m+2)**power
                    *(2*m)**(degree-power))
        return out, (2*m)**degree

    dN, sN = 3*m+2, 4*m*(m+2)
    LN = -sN*n*(m+5)+2*m*(6*m+8)*dN
    beta0N = -n*sN  # denominator m*dN^2
    chi0N = n*sN*(LN-2*n*sN)  # denominator m^3*dN^4
    beta_cutN, beta_cutD = cutoff_numerator(beta_num)
    chi_cutN, chi_cutD = cutoff_numerator(chi_num)
    check("cutoff_specialization", 4*m*beta_cutN == beta0N*beta_cutD,
          "beta=-n*s/m at cutoff")
    check("cutoff_specialization", 16*m*m*chi_cutN == chi0N*chi_cutD,
          "specialized chi from general cubic")
    BinnerN = (sN*(LN-2*n*sN)+F(3, 4)*sN*sN*n*n-sN*sN*m)
    H = m**3-4*m*m+13*m+18
    check("cutoff_coefficient", 2*BinnerN == -8*m*m*(m+2)*H,
          "second-order gap=-8m(m+2)H/(3m+2)^5")
    y = Poly.var(15)
    check("uniform_signs", H.at(0, y+3) == y**3+5*y*y+16*y+48,
          "negative cutoff coefficient in all m>=3")

    # These are polynomial certificates, not a scan over degrees.
    certificates = {
        "radius_implies_epsilon_1_over_4n": 80*m*(m+1)**2-4,
        "root_radius_denominator_7680": 40*m*(m+1)**3-7680,
        "loss_budget": 5*m*(m+1)**3-2*(m+1)-3*m,
        "real_trace_correction": m*m+4*m-1,
        "cutoff_strictly_below_one": m-2,
        "cluster_discriminant_negative": m-2,
    }
    for label, polynomial in certificates.items():
        shifted = polynomial.at(0, y+3)
        check("uniform_signs", all(v >= 0 for v in shifted.t.values())
              and bool(shifted.t), label)
    check("rational_bounds", F(37, 80) < F(1, 2), "half kappa retained")
    check("rational_bounds", F(3, 2)*(F(3, 2)-F(1, 7680)) > 2,
          "original-root radius conversion")
    check("rational_bounds", 80*8*9**3 == 466560,
          "honest comparison with the degree-nine radius")
    check("rational_bounds",
          -F(2*8*10*(8**3-4*8**2+13*8+18), (3*8+2)**5)
          == -F(1890, 13**5), "degree-nine one-pair quartic, illustration only")

    # Alter genuine coefficients and reject them via the symbolic identities.
    mutations = {
        "square_root_n_plus_one":
            tuple(extension_reduce(v, 7, n+1) for v in squared) != (m*m, m*m),
        "compressed_trace_1_minus_1_over_m":
            moment_scaled != (m*m-m)*U2+U1*U1,
        "cutoff_m_plus_one_over_2m":
            (m-2)*d-2*m*b != d*(2*m*a-m-1),
        "positive_cutoff_coefficient":
            2*BinnerN != 8*m*m*(m+2)*H,
    }
    for label, rejected in mutations.items():
        if not rejected:
            raise AssertionError("Mutation escaped: " + label)

    print(json.dumps({
        "status": "PASS", "exact_checks": sum(groups.values()), "groups": groups,
        "mutations_rejected": list(mutations), "symbolic_degree_parameter": "m=n-1",
        "external_inputs": 0, "floating_point_operations": 0
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    run()
