#!/usr/bin/env python3
"""Exact all-degree algebra for PROOF.md, Python standard library.

Coefficient domain Q(m,r)[i][t]/(t^5), i^2=-1, characteristic zero.
Polynomial order is (m,r); rational denominators are products of m,
3m+2 and m+2. All are nonzero for m>=3. Every truncated reciprocal
and positive square root is verified by substitution. No interpolation,
floating point, solver, imported certificate or external input is used.
The analytic interpretation and asymptotic remainders are written proofs,
not formalized here. Agent six-sendov-2, role researcher. This is author
validation; arithmetic adapts the author's earlier exact checkers.
"""
from fractions import Fraction as F
from math import factorial
import json


def require(condition, label):
    if not condition:
        raise AssertionError(label)


class Poly:
    def __init__(self, terms=0):
        if isinstance(terms, (int, F)):
            terms = {(0, 0): F(terms)}
        self.t = {k: F(v) for k, v in terms.items() if v}

    def __add__(self, other):
        other = poly(other)
        out = dict(self.t)
        for k, v in other.t.items():
            out[k] = out.get(k, F(0)) + v
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.t.items()})

    def __sub__(self, other):
        return self + -poly(other)

    def __rsub__(self, other):
        return poly(other) + -self

    def __mul__(self, other):
        if not isinstance(other, (Poly, int, F)):
            return NotImplemented
        other = poly(other)
        out = {}
        for (a, b), v in self.t.items():
            for (c, d), w in other.t.items():
                k = (a+c, b+d)
                out[k] = out.get(k, F(0)) + v*w
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0, "nonnegative integer exponent")
        out = Poly(1)
        for _ in range(exponent):
            out *= self
        return out

    def at(self, variable, value):
        out = Poly(0)
        for k, c in self.t.items():
            base = list(k)
            base[variable] = 0
            out += Poly({tuple(base): c}) * poly(value)**k[variable]
        return out

    def coefficient(self, variable, degree):
        out = {}
        for k, c in self.t.items():
            if k[variable] == degree:
                base = list(k)
                base[variable] = 0
                out[tuple(base)] = c
        return Poly(out)

    def __eq__(self, other):
        return self.t == poly(other).t

    def divide_linear_m(self, root, leading):
        """Division by leading*(m-root), independently for each r degree."""
        quotient = {}
        remainder = {}
        for r in sorted({b for a, b in self.t}):
            coeff = {a: v for (a, b), v in self.t.items() if b == r}
            top = max(coeff)
            carry = coeff.get(top, F(0))
            if top:
                quotient[(top-1, r)] = carry/leading
            for a in range(top-1, 0, -1):
                carry = coeff.get(a, F(0)) + root*carry
                quotient[(a-1, r)] = carry/leading
            rem = coeff.get(0, F(0)) + (root*carry if top else F(0))
            if rem:
                remainder[(0, r)] = rem
        return Poly(quotient), Poly(remainder)

    def terms(self):
        return [[a, b, str(c)] for (a, b), c in sorted(self.t.items())]


def poly(x):
    return x if isinstance(x, Poly) else Poly(x)


m = Poly({(1, 0): 1})
r = Poly({(0, 1): 1})
D = 3*m+2
M = m+2
FACTORS = (m, D, M)
ROOTS = ((F(0), F(1)), (F(-2, 3), F(3)), (F(-2), F(1)))


class RF:
    def __init__(self, numerator=0, denominator=(0, 0, 0)):
        self.p = poly(numerator)
        self.d = list(denominator)
        if self.p == 0:
            self.d = [0, 0, 0]
        for i, (root, leading) in enumerate(ROOTS):
            while self.d[i] and self.p != 0:
                quotient, remainder = self.p.divide_linear_m(root, leading)
                if remainder != 0:
                    break
                self.p = quotient
                self.d[i] -= 1
        self.d = tuple(self.d)

    def __add__(self, other):
        other = rf(other)
        exps = tuple(max(x, y) for x, y in zip(self.d, other.d))
        n1, n2 = self.p, other.p
        for i in range(3):
            n1 *= FACTORS[i]**(exps[i]-self.d[i])
            n2 *= FACTORS[i]**(exps[i]-other.d[i])
        return RF(n1+n2, exps)

    __radd__ = __add__

    def __neg__(self):
        return RF(-self.p, self.d)

    def __sub__(self, other):
        return self + -rf(other)

    def __rsub__(self, other):
        return rf(other) + -self

    def __mul__(self, other):
        other = rf(other)
        return RF(self.p*other.p, tuple(x+y for x, y in zip(self.d, other.d)))

    __rmul__ = __mul__

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0, "nonnegative integer exponent")
        return RF(self.p**exponent, tuple(exponent*x for x in self.d))

    def __eq__(self, other):
        return (self-rf(other)).p == 0

    def coefficient(self, degree):
        return RF(self.p.coefficient(1, degree), self.d)

    def data(self):
        return {'numerator_terms_m_r': self.p.terms(),
                'denominator_exponents_m_3mplus2_mplus2': list(self.d)}


def rf(x):
    return x if isinstance(x, RF) else RF(x)


N = 4
ZERO = (RF(0), RF(0))
ONE = (RF(1), RF(0))


def cadd(x, y):
    return x[0]+y[0], x[1]+y[1]


def cneg(x):
    return -x[0], -x[1]


def cmul(x, y):
    return x[0]*y[0]-x[1]*y[1], x[0]*y[1]+x[1]*y[0]


def csum(items):
    out = ZERO
    for item in items:
        out = cadd(out, item)
    return out


def constant(x):
    return [(rf(x), RF(0))] + [ZERO]*N


def add(*ss):
    return [csum(s[k] for s in ss) for k in range(N+1)]


def neg(s):
    return [cneg(c) for c in s]


def mul(*ss):
    out = constant(1)
    for s in ss:
        out = [csum(cmul(out[i], s[k-i]) for i in range(k+1)) for k in range(N+1)]
    return out


def scale(s, x):
    return [cmul(c, (rf(x), RF(0))) for c in s]


def conj(s):
    return [(c[0], -c[1]) for c in s]


def inv(s, inverse_base):
    inverse_base = rf(inverse_base)
    require(cmul(s[0], (inverse_base, RF(0))) == ONE, "reciprocal base")
    out = [(inverse_base, RF(0))]+[ZERO]*N
    for k in range(1, N+1):
        out[k] = cmul(cneg(csum(cmul(s[i], out[k-i]) for i in range(1, k+1))),
                      (inverse_base, RF(0)))
    require(mul(s, out) == constant(1), "reciprocal residual")
    return out


def sqrt_series(s, base, half_inverse_base):
    base, half_inverse_base = rf(base), rf(half_inverse_base)
    require(all(c[1] == 0 for c in s), "real square-root argument")
    require(s[0][0] == base*base, "square-root base")
    require(2*base*half_inverse_base == 1, "square-root inverse base")
    out = [(base, RF(0))]+[ZERO]*N
    for k in range(1, N+1):
        rest = csum(cmul(out[i], out[k-i]) for i in range(1, k))
        out[k] = cmul(cadd(s[k], cneg(rest)), (half_inverse_base, RF(0)))
    require(mul(out, out) == s, "square-root residual")
    return out


def exponential(theta):
    phases = ((1, 0), (0, 1), (-1, 0), (0, -1))
    return [(RF(theta**k * F(phases[k % 4][0], factorial(k))),
             RF(theta**k * F(phases[k % 4][1], factorial(k)))) for k in range(N+1)]


class MP:
    """A separate free polynomial ring Q[a,x,y,m,r,q,bR,bI,wR,wI]."""
    def __init__(self, terms=0):
        if isinstance(terms, (int, F)):
            terms = {(): F(terms)}
        self.t = {k: F(v) for k, v in terms.items() if v}

    @staticmethod
    def var(i):
        return MP({(i,): F(1)})

    def __add__(self, other):
        other = other if isinstance(other, MP) else MP(other)
        out = dict(self.t)
        for k, c in other.t.items():
            out[k] = out.get(k, F(0))+c
        return MP(out)

    __radd__ = __add__

    def __neg__(self):
        return MP({k: -v for k, v in self.t.items()})

    def __sub__(self, other):
        return self + -(other if isinstance(other, MP) else MP(other))

    def __rsub__(self, other):
        return (other if isinstance(other, MP) else MP(other)) + -self

    def __mul__(self, other):
        other = other if isinstance(other, MP) else MP(other)
        out = {}
        for k, c in self.t.items():
            for l, d in other.t.items():
                key = tuple(sorted(k+l))
                out[key] = out.get(key, F(0))+c*d
        return MP(out)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0, "MP exponent")
        out = MP(1)
        for _ in range(exponent):
            out *= self
        return out

    def __eq__(self, other):
        return self.t == (other if isinstance(other, MP) else MP(other)).t


def value(p, m0, r0):
    p = rf(p)
    numerator = sum(c*F(m0)**i*F(r0)**j for (i, j), c in p.p.t.items())
    denominator = F(m0)**p.d[0]*F(3*m0+2)**p.d[1]*F(m0+2)**p.d[2]
    return numerator/denominator


def run():
    groups = {}

    def check(group, condition, label):
        require(condition, group+": "+label)
        groups[group] = groups.get(group, 0)+1

    # The product rule leaves R(z); its reciprocal transform is a quadratic.
    a0, x0, y0, m0, r0, q0, br, bi, wr, wi = [MP.var(i) for i in range(10)]
    s0 = m0-r0
    A0 = (a0+x0)*(a0+y0)
    B0 = (m0+2)*a0+(s0+1)*x0+(r0+1)*y0
    zcoefficient = (s0+1)*x0+(r0+1)*y0-m0*a0
    constantcoefficient = x0*y0-a0*(r0*y0+s0*x0)
    transformed = ((m0+1)*(a0*a0*q0*q0-2*a0*q0+1)
                   +zcoefficient*(a0*q0*q0-q0)+constantcoefficient*q0*q0)
    check("factorization", transformed == A0*q0*q0-B0*q0+m0+1,
          "q^2 R(a-1/q)=A q^2-B q+n")
    check("factorization",
          zcoefficient == x0+y0+r0*y0+s0*x0-m0*a0,
          "product-rule coefficient")
    check("modulus_identity",
          (br+wr)**2+(bi+wi)**2+(br-wr)**2+(bi-wi)**2 ==
          2*(br*br+bi*bi+wr*wr+wi*wi), "parallelogram identity")

    s, n, k = m-r, m+1, r*(m-r)
    x, y = exponential(s), exponential(-r)
    AN = mul(add(constant(M), scale(x, 2*m)),
             add(constant(M), scale(y, 2*m)))
    BN = add(constant(M*M), scale(x, 2*m*(s+1)), scale(y, 2*m*(r+1)))
    deltaN = add(mul(BN, BN), neg(scale(AN, 4*n)))
    check("bases", AN[0] == (RF(D**2), RF(0)), "AN(0)=D^2")
    check("bases", BN[0] == (RF(M*D), RF(0)), "BN(0)=MD")
    check("bases", deltaN[0] == (RF(m*m*D**2), RF(0)), "DeltaN(0)=m^2 D^2")
    normA = sqrt_series(mul(AN, conj(AN)), D**2, RF(F(1, 2), (0, 2, 0)))
    normDelta = sqrt_series(mul(deltaN, conj(deltaN)), m*m*D**2,
                            RF(F(1, 2), (2, 2, 0)))
    zsquare = scale(add(mul(BN, conj(BN)), normDelta, scale(normA, 4*n)), F(1, 2))
    z = sqrt_series(zsquare, M*D, RF(F(1, 2), (0, 1, 1)))
    qsum = scale(mul(z, inv(normA, RF(1, (0, 2, 0)))), 2*m)
    check("residuals", mul(normA, normA) == mul(AN, conj(AN)), "normA")
    check("residuals", mul(normDelta, normDelta) == mul(deltaN, conj(deltaN)), "normDelta")
    check("residuals", mul(z, z) == zsquare, "positive outer square root")
    check("residuals", scale(mul(qsum, qsum, normA, normA), F(1, 4)) ==
          scale(zsquare, m*m), "quadratic modulus-sum identity")

    v = RF(2*m, (0, 1, 0))
    K2 = RF(2*m*m*M, (0, 3, 0))
    L = 9*m*m+24*m-4
    K4 = RF(m*m*M*L*F(1, 6), (0, 5, 0))
    check("single_modulus", K4 ==
          RF(-m*m*M*F(1, 6), (0, 3, 0))+RF(3*m**3*M**2, (0, 5, 0)),
          "scalar square-root expansion")
    a = RF(M*F(1, 2), (1, 0, 0))
    ux, uy = inv(add(constant(a), x), v), inv(add(constant(a), y), v)
    for u, theta in [(ux, s), (uy, -r)]:
        normu = sqrt_series(mul(u, conj(u)), v, RF(D*F(1, 4), (1, 0, 0)))
        check("single_modulus", normu[0] == (v, RF(0)), "base reciprocal")
        check("single_modulus", normu[1] == ZERO and normu[3] == ZERO, "even orders")
        check("single_modulus", normu[2] == (K2*theta**2, RF(0)), "quadratic order")
        check("single_modulus", normu[4] == (K4*theta**4, RF(0)), "quartic order")
    dx, dy = add(ux, constant(-v)), add(uy, constant(-v))
    energy = add(scale(mul(dx, conj(dx)), r), scale(mul(dy, conj(dy)), s))
    e2 = RF(16*m**5*k, (0, 4, 0))
    check("energy", energy[0] == ZERO, "zero base")
    check("energy", energy[1] == ZERO and energy[3] == ZERO, "even energy")
    check("energy", energy[2] == (e2, RF(0)), "m r s/d^4")
    check("energy", all(c[1] == 0 for c in energy), "real energy coefficients")

    R2 = (r-1)*s**2+(s-1)*r**2
    R4 = (r-1)*s**4+(s-1)*r**4
    check("multiplicities", R2 == M*k-m*m, "second angular moment")
    check("multiplicities", R4 == -m**4+(m**3+4*m*m)*k-D*k*k,
          "fourth angular moment")
    Q4 = RF(m*m*M*F(1, 6), (0, 5, 0)) * (
        m**4*L-m*m*(15*m**3+36*m*m+68*m-16)*k
        +D*(15*m*m-12*m-4)*k*k)
    expected_qsum = constant(v*M)
    expected_qsum[2] = (K2*(m*m-M*k), RF(0))
    expected_qsum[4] = (Q4, RF(0))
    for j in range(5):
        check("quadratic_sum_coefficients", qsum[j] == expected_qsum[j], str(j))
    repeated = constant(v*(m-2))
    repeated[2] = (K2*R2, RF(0))
    repeated[4] = (K4*R4, RF(0))
    gap = add(qsum, repeated, constant(-2*m*v))
    check("gap", gap[:4] == [ZERO]*4, "all orders below four vanish")
    check("gap", all(c[1] == 0 for c in gap), "real gap")
    T = m*m-4*m-4
    f4 = RF(m**3*M*k, (0, 5, 0)) * (-m*m*T+(m-6)*D*k)
    check("gap", gap[4] == (f4, RF(0)), "uniform fourth-order formula")
    A = RF(M*T*D**3*F(1, 256), (5, 0, 0))
    B = RF(M*(m-6)*D**4*F(1, 256), (7, 0, 0))
    # Clear the sole rs denominator in K=A/(rs)-B.
    check("energy_conversion", -f4*k == (A-B*k)*e2**2, "K=-f4/e2^2")

    # Uniform sign and multiplicity optimization; only small exceptions
    # are specialized. These finite controls do not prove an all-degree claim.
    check("signs", T.at(0, m+5) == m*m+6*m+1, "T>0 for m>=5")
    check("signs", 4*T-(m-6)*D == m*m-4, "C positive using rs<=m^2/4")
    check("optimization", k-(m-1) == (r-1)*(m-r-1), "rs>=m-1")
    check("optimization", m*m-4*k == (m-2*r)**2, "rs<=m^2/4")
    exceptional = []
    for mv in [3, 4]:
        coefficients = [value(A, mv, rv)/F(rv*(mv-rv))-value(B, mv, rv)
                        for rv in range(1, mv)]
        check("small_exceptions", min(coefficients)>0, "positive m="+str(mv))
        largest = max(coefficients)
        argmax = [rv for rv, c in enumerate(coefficients, 1) if c == largest]
        check("small_exceptions", argmax == ([1, 2] if mv == 3 else [2]),
              "maximizing m="+str(mv))
        exceptional.append({'m': mv, 'maximum': str(largest), 'argmax_r': argmax})

    # Comparison uses the previously proved moving-pair coefficient,
    # explicitly a dependency of the comparison, not of this expansion.
    H = m**3-4*m*m+13*m+18
    P = m**4-9*m**3+13*m*m-13*m-6
    difference = RF(M*D**3*F(1, 512), (7, 0, 0))*P
    check("comparison", (2*A-2*B*(m-1)
          -RF(M*H*D**3*F(1, 256), (7, 0, 0))*(m-1)) == 2*difference,
          "singleton minus moving pair, denominator cleared")
    check("comparison", P.at(0, m+8) == m**4+23*m**3+181*m*m+515*m+210,
          "strictly positive for m>=8")
    for mv in [5, 6, 7]:
        check("comparison", P.at(0, mv).t[(0, 0)] < 0, "negative m="+str(mv))
    for row in exceptional:
        mv = row['m']
        pair = F((mv+2)*(mv**3-4*mv*mv+13*mv+18)*(3*mv+2)**3, 512*mv**7)
        check("comparison", F(row['maximum'])<pair, "small-degree maximum below pair")
    C9 = value(A, 8, 1)/7-value(B, 8, 1)
    pair9 = F(2076165, 33554432)
    check("degree_nine", C9 == F(560235, 8388608), "maximum two-block coefficient")
    check("degree_nine", C9-pair9 == F(164775, 33554432), "strict excess")
    check("degree_nine", value(f4, 8, 1) == F(-1599360, 371293), "gap t^4")
    check("degree_nine", value(e2, 8, 1) == F(229376, 28561), "energy t^2")
    for rv in range(1, 8):
        check("degree_nine", value(A, 8, rv)/F(rv*(8-rv))-value(B, 8, rv) ==
              F(10985, 8388608)*(F(448, rv*(8-rv))-13), "profile "+str(rv))

    mutations = [
        ("wrong gap sign", f4 == -gap[4][0]),
        ("drop rs factor", -f4 == (A-B*k)*e2**2),
        ("wrong energy factor", energy[2][0] == 2*e2),
        ("wrong quadratic sum coefficient", qsum[4][0] == Q4+1),
        ("wrong comparison constant", P.at(0, m+8) ==
         m**4+23*m**3+181*m*m+515*m+209),
    ]
    for label, condition in mutations:
        require(not condition, "mutation not rejected: "+label)
    print(json.dumps({
        'status': 'PASS', 'agent': 'six-sendov-2', 'role': 'researcher',
        'exact_checks': sum(groups.values()), 'checks_by_group': groups,
        'rejected_coefficient_mutations': len(mutations),
        'symbolic_parameters': ['m=n-1>=3', 'r', 's=m-r'],
        'formula': 'K_m(r)=(m+2)(3m+2)^3/(256*m^7) * '
                   '(m^2*(m^2-4m-4)/(r*(m-r))-(m-6)*(3m+2))',
        'maximum_degree_nine': str(C9), 'excess_over_moving_pair': str(C9-pair9),
        'small_degree_exceptions': exceptional,
        'all_degree_quantifier_from': 'symbolic identities and written sign arguments',
        'external_inputs': 0, 'floating_point_operations': 0,
        'analytic_bridge_formalized': False, 'global_extremality_proved': False,
    }, indent=2))


if __name__ == '__main__':
    run()
