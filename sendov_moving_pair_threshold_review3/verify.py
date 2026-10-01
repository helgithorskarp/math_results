#!/usr/bin/env python3
"""Independent exact audit of claim8160 and a proved moving-pair angular interval.

Reviewer six-reviewer-3. Standard-library unified sparse rational ring
Q[v,v^-1,w,i][[t]]/(t^(N+1),i^2+1): direct degree-nine differentiation,
geometric/binomial series and simultaneous Newton doubling. No author import.
Uniform analytic and real-rooted arguments are in REVIEW.md.
"""
import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
import hashlib
import json
from math import comb, factorial
from pathlib import Path


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


class S:
    limit = 6

    def __init__(self, value=0):
        if isinstance(value, S):
            self.c = dict(value.c)
        elif isinstance(value, dict):
            self.c = {tuple(k): Q(x) for k, x in value.items() if x}
        else:
            self.c = {(0, 0, 0, 0): Q(value)} if value else {}

    @classmethod
    def var(cls, axis):
        exponent = [0, 0, 0, 0]
        exponent[axis] = 1
        return cls({tuple(exponent): 1})

    def __add__(self, other):
        out = dict(self.c)
        for key, value in S(other).c.items():
            out[key] = out.get(key, Q()) + value
        return S(out)

    __radd__ = __add__

    def __neg__(self):
        return S({key: -x for key, x in self.c.items()})

    def __sub__(self, other):
        return self + -S(other)

    def __rsub__(self, other):
        return S(other) + -self

    def __mul__(self, other):
        out = {}
        for (t, v, w, i), x in self.c.items():
            for (tt, vv, ww, ii), y in S(other).c.items():
                if t + tt > self.limit:
                    continue
                key = (t + tt, v + vv, w + ww, (i + ii) % 2)
                out[key] = out.get(key, Q()) + x * y * (-1 if i + ii == 2 else 1)
        return S(out)

    __rmul__ = __mul__

    def __pow__(self, n):
        if n < 0:
            return self.inverse() ** (-n)
        out, factor = S(1), self
        while n:
            if n % 2:
                out *= factor
            factor *= factor
            n //= 2
        return out

    def coefficient(self, axis, degree):
        return S({tuple(0 if j == axis else x for j, x in enumerate(k)): c
                  for k, c in self.c.items() if k[axis] == degree})

    def inverse(self):
        constant = self.coefficient(0, 0)
        need(len(constant.c) == 1, "series unit must have a monomial constant")
        (t, v, w, i), c = next(iter(constant.c.items()))
        need(not t and not w, "unsupported constant divisor")
        base = S({(0, -v, 0, i): (1 if not i else -1) / c})
        residual = 1 - self * base
        need(not residual.coefficient(0, 0), "nonzero geometric constant")
        term, out = S(1), S(1)
        for _ in range(self.limit):
            term *= residual
            out += term
        return base * out

    def __truediv__(self, other):
        return self * S(other).inverse()

    def __rtruediv__(self, other):
        return S(other) * self.inverse()

    def conjugate(self):
        return S({k: (-c if k[3] else c) for k, c in self.c.items()})

    def sqrt(self, constant):
        constant = S(constant)
        need(constant * constant == self.coefficient(0, 0), "wrong square-root branch")
        residual = self / (constant * constant) - 1
        need(not residual.coefficient(0, 0), "nonzero binomial constant")
        term, out, factor = S(1), S(1), Q(1)
        for k in range(1, self.limit + 1):
            term *= residual
            factor *= (Q(1, 2) - (k - 1)) / k
            out += factor * term
        result = constant * out
        need(result * result == self, "complete binomial inverse")
        return result

    def substitute_w(self, value):
        out = S()
        for (t, v, w, i), c in self.c.items():
            out += S({(t, v, 0, i): c}) * S(value) ** w
        return out

    def __bool__(self):
        return bool(self.c)

    def __eq__(self, other):
        return self.c == S(other).c

    def encode(self):
        return [[*k, x.numerator, x.denominator] for k, x in sorted(self.c.items())]


IDENTITIES = []
RECORDS = {}
LEGACY = {}


def equal(name, actual, expected):
    need(actual == expected, "exact identity: " + name)
    IDENTITIES.append(name)


def record(name, value):
    need(name not in RECORDS, "duplicate record")
    RECORDS[name] = value.encode() if hasattr(value, "encode") else value


def scalar_wire(value):
    value = S(value)
    need(all(not t and not w and not i for t, v, w, i in value.c), "nonreal scalar wire")
    return [[v, c.numerator, c.denominator] for (t, v, w, i), c in sorted(value.c.items())]


def jet_wire(value, degree):
    value = S(value)
    need(all(not w for t, v, w, i in value.c), "unbound mean in original comparison")
    return [{"re": [[v, c.numerator, c.denominator]
                    for (t, v, w, i), c in sorted(value.c.items()) if t == k and not i],
             "im": [[v, c.numerator, c.denominator]
                    for (t, v, w, i), c in sorted(value.c.items()) if t == k and i]}
            for k in range(degree + 1)]


def exp_i(phi):
    out, term, imaginary = S(1), S(1), S.var(3)
    for k in range(1, S.limit + 1):
        term = term * imaginary * phi / k
        out += term
    return out


def pmul(left, right):
    out = [S() for _ in range(len(left) + len(right) - 1)]
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] += x * y
    return out


def ppow(coeffs, degree):
    out = [S(1)]
    for _ in range(degree):
        out = pmul(out, coeffs)
    return out


def derivative(coeffs):
    return [k * coeffs[k] for k in range(1, len(coeffs))]


def peval(coeffs, point):
    # Direct power sum, independent of the author's Horner evaluation.
    return sum((c * point ** k for k, c in enumerate(coeffs)), S())


def divide_polynomial(coeffs, divisor):
    remainder = list(coeffs)
    quotient = [S() for _ in range(len(coeffs) - len(divisor) + 1)]
    for k in range(len(quotient) - 1, -1, -1):
        quotient[k] = remainder[k + len(divisor) - 1] / divisor[-1]
        for j, c in enumerate(divisor):
            remainder[k + j] -= quotient[k] * c
    need(not any(remainder), "physical repeated-root division remainder")
    equal("entire physical derivative factorization", pmul(quotient, divisor), coeffs)
    return quotient


def reciprocal(coeffs, a):
    n = len(coeffs) - 1
    out = [S() for _ in range(n + 1)]
    for k, c in enumerate(coeffs):
        for j in range(k + 1):
            out[n - j] += c * comb(k, j) * a ** (k - j) * (-1) ** j
    return [x / peval(coeffs, a) for x in out]


def implicit_newton(coeffs, initial):
    root = S(initial)
    iterations = 0
    while peval(coeffs, root):
        need(iterations < 5, "Newton doubling did not complete")
        root -= peval(coeffs, root) / peval(derivative(coeffs), root)
        iterations += 1
    equal("complete simultaneous Newton residual", peval(coeffs, root), S())
    return root


def constants():
    v = S.var(1)
    d = v ** -1
    a = d - 1
    kappa = d * (a - Q(5, 8))
    A = d ** 3 * (48 * d ** 2 - 40 * d - 53) / 512
    B = d ** 3 * (16 * d ** 2 - 104 * d + 203) / 8192
    C = d ** 3 * (4 * d + 1) ** 2 / 8192
    K1 = d ** 3 * (516 * d ** 2 - 528 * d - 393) / 7168
    KQ = d ** 3 * (784 * d ** 2 - 856 * d - 443) / 16384
    PG = 2768 * a ** 2 + 3080 * a - 2875
    return v, d, a, kappa, A, B, C, K1, KQ, PG


def moving_pair():
    S.limit = 3
    v, d, a, kappa, A, B, C, K1, KQ, PG = constants()
    e = S.var(0)
    denominator = 4 + 2 * a * d ** 2 * e
    numerator = d ** 4 * e
    x = numerator / denominator
    equal("full rational energy-inverse numerator", x * denominator, numerator)
    equal("physical reciprocal denominator cancellation",
          d ** 2 * denominator - 2 * a * numerator, 4 * d ** 2)
    h = denominator / (4 * d ** 2)
    j = 2 * (d * denominator - numerator) / (4 * d ** 2)
    equal("derived light reciprocal product", h, v ** 2 + a * e / 2)
    equal("derived light reciprocal sum", j, 2 * v + (a ** 2 - 1) * e / 2)
    equal("exact physical energy", 2 * h - 2 * v * j + 2 * v ** 2, e)
    # Differentiate the literal degree-nine Q, then divide its fivefold factor.
    physical = pmul(pmul([-a, S(1)], ppow([S(1), S(1)], 6)),
                    [S(1), 2 * (1 - x), S(1)])
    residual = divide_polynomial(derivative(physical), ppow([S(1), S(1)], 5))
    cubic = reciprocal(residual, a)
    equal("full physical reciprocal cubic", cubic,
          [-9 * v * h, 3 * h + 8 * v * j, -2 * j - 7 * v, S(1)])
    qfar = implicit_newton(cubic, 9 * v)
    equal("positive far derivative at collapse",
          peval(derivative(cubic), 9 * v).coefficient(0, 0), 64 * v ** 2)
    equal("literal far secular numerator",
          (j * qfar - 2 * h) * (qfar - v)
          + 6 * v * (qfar ** 2 - j * qfar + h)
          - (qfar ** 2 - j * qfar + h) * (qfar - v), S())
    product = 9 * v * h / qfar
    norm = product.sqrt(v)
    discriminant = (2 * j + 7 * v - qfar) ** 2 - 4 * product
    equal("conjugate-pair discriminant constant", discriminant.coefficient(0, 0), S())
    equal("conjugate-pair discriminant first coefficient",
          discriminant.coefficient(0, 1), S(Q(-3, 2)))
    objective = 5 * v + qfar + 2 * norm
    equal("moving-pair collapsed objective", objective.coefficient(0, 0), 16 * v)
    equal("moving-pair linear objective", objective.coefficient(0, 1), kappa)
    equal("moving-pair quartic objective", objective.coefficient(0, 2), -KQ)
    CQ = objective.coefficient(0, 3)
    wanted = Q(1127, 65536) * d ** 8 - Q(6855, 131072) * d ** 7 \
        + Q(52737, 1048576) * d ** 6 - Q(28853, 2097152) * d ** 5
    equal("full moving-pair cubic energy coefficient", CQ, wanted)
    data = {"energy inverse": x, "reciprocal product": h, "reciprocal sum": j,
            "far jet": qfar, "secular far jet": qfar, "near product": product,
            "near modulus": norm, "near discriminant": discriminant,
            "energy": e, "objective": objective}
    for name, value in data.items():
        record("moving pair " + name, value)
        LEGACY["moving pair " + name] = jet_wire(value, 3)
    LEGACY["moving pair physical residual polynomial"] = [jet_wire(x, 3) for x in residual]
    LEGACY["moving pair reciprocal residual cubic"] = [jet_wire(x, 3) for x in cubic]
    LEGACY["credited earlier moving-pair full reciprocal cubic"] = [jet_wire(x, 3) for x in cubic]
    LEGACY["moving pair cubic coefficient"] = scalar_wire(CQ)
    record("moving pair cubic coefficient", CQ)
    return CQ


def stationary():
    S.limit = 6
    v, d, a, kappa, A, B, C, K1, KQ, PG = constants()
    t, w = S.var(0), S.var(2)
    rootL, rootH = -exp_i(7 * t + w * t ** 3), -exp_i(-t + w * t ** 3)
    uL, uH = 1 / (a - rootL), 1 / (a - rootH)
    # All nine original factors are formed before differentiation.
    physical = pmul(pmul([-a, S(1)], [-rootL, S(1)]), ppow([-rootH, S(1)], 7))
    residual = divide_polynomial(derivative(physical), ppow([-rootH, S(1)], 6))
    quadratic = reciprocal(residual, a)
    equal("entire original stationary reciprocal quadratic", quadratic,
          [9 * uL * uH, -2 * uL - 8 * uH, S(1)])
    qfar = implicit_newton(quadratic, 9 * v)
    qnear = 2 * uL + 8 * uH - qfar
    equal("entire near quadratic residual", peval(quadratic, qnear), S())
    equal("quadratic root product", qnear * qfar, 9 * uL * uH)
    objective = 6 * (uH * uH.conjugate()).sqrt(v) \
        + (qnear * qnear.conjugate()).sqrt(v) \
        + (qfar * qfar.conjugate()).sqrt(9 * v)
    energy = (uL - v) * (uL - v).conjugate() \
        + 7 * (uH - v) * (uH - v).conjugate()
    equal("complete imaginary objective cancellation", objective, objective.conjugate())
    equal("complete imaginary energy cancellation", energy, energy.conjugate())
    equal("complete stationary energy leading coefficient", energy.coefficient(0, 2), 56 * v ** 4)
    reduced = objective - kappa * energy + K1 * energy ** 2
    for k in range(6):
        equal("entire symbolic-mean residual degree " + str(k),
              reduced.coefficient(0, k), 16 * v if k == 0 else S())
    sextic = reduced.coefficient(0, 6)
    p0, p1, p2 = [sextic.coefficient(2, k) for k in range(3)]
    equal("full arbitrary-mean quadratic", sextic, p0 + p1 * w + p2 * w ** 2)
    beta = -p1 / (2 * p2)
    equal("positive mean stiffness", p2, 5 * v ** 3)
    equal("stationary leading mean", beta, (392 - 1197 * v + 945 * v ** 2) / 20)
    CP = (p0 - p1 ** 2 / (4 * p2)) / (56 * v ** 4) ** 3
    wanted = -Q(297, 35840) * d ** 9 + Q(78387, 1003520) * d ** 8 \
        - Q(741429, 4014080) * d ** 7 + Q(15471, 100352) * d ** 6 \
        - Q(15303, 458752) * d ** 5
    equal("complete stationary energy-cubic coefficient", CP, wanted)
    equal("known mean constant", p0, Q(931, 2) * v ** 3 + Q(15897, 8) * v ** 4
          - Q(168525, 32) * v ** 5 - Q(9639, 8) * v ** 6 + Q(678993, 128) * v ** 7)
    profile = {"far": qfar, "near": qnear, "objective": objective,
               "energy": energy, "reduced residual": reduced}
    for name, value in profile.items():
        specialized = value.substitute_w(beta)
        LEGACY["stationary " + name] = jet_wire(specialized, 6)
        record("stationary symbolic mean " + name, value)
    LEGACY["stationary physical quadratic"] = [jet_wire(x.substitute_w(beta), 6) for x in residual]
    LEGACY["stationary reciprocal quadratic"] = [jet_wire(x.substitute_w(beta), 6) for x in quadratic]
    for mean in [0, -1, 1, 2]:
        LEGACY["mean-control " + str(mean) + " full residual"] = jet_wire(reduced.substitute_w(mean), 6)
    for name, value in {"beta": beta, "mean constant": p0, "mean linear": p1,
                        "mean quadratic": p2, "cubic coefficient": CP}.items():
        LEGACY["stationary " + name] = scalar_wire(value)
        record("stationary " + name, value)
    return CP


@dataclass(frozen=True)
class Field:
    r: int
    a: Q = Q()
    b: Q = Q()

    def cast(self, value):
        if isinstance(value, Field):
            need(self.r == value.r, "mixed quadratic fields")
            return value
        return Field(self.r, Q(value))

    def __add__(self, x):
        x = self.cast(x)
        return Field(self.r, self.a + x.a, self.b + x.b)

    __radd__ = __add__

    def __neg__(self):
        return Field(self.r, -self.a, -self.b)

    def __sub__(self, x):
        return self + -self.cast(x)

    def __rsub__(self, x):
        return self.cast(x) + -self

    def __mul__(self, x):
        x = self.cast(x)
        return Field(self.r, self.a * x.a + self.r * self.b * x.b,
                     self.a * x.b + self.b * x.a)

    __rmul__ = __mul__

    def inverse(self):
        norm = self.a * self.a - self.r * self.b * self.b
        need(norm != 0, "zero quadratic-field divisor")
        return Field(self.r, self.a / norm, -self.b / norm)

    def __truediv__(self, x):
        return self * self.cast(x).inverse()

    def __pow__(self, n):
        if n < 0:
            return self.inverse() ** (-n)
        out = Field(self.r, Q(1))
        for _ in range(n):
            out *= self
        return out

    def sign(self):
        sa, sb = (self.a > 0) - (self.a < 0), (self.b > 0) - (self.b < 0)
        if not sb:
            return sa
        if not sa or sa == sb:
            return sb
        difference = self.a ** 2 - self.r * self.b ** 2
        need(difference != 0, "unexpected rational radical")
        return sa if difference > 0 else sb

    def encode(self):
        return {"radicand": self.r, "rational": [self.a.numerator, self.a.denominator],
                "radical": [self.b.numerator, self.b.denominator]}

    def legacy(self):
        return [[self.a.numerator, self.a.denominator], [self.b.numerator, self.b.denominator]]


def field_evaluate(polynomial, value):
    need(all(not t and not w and not i for t, v, w, i in polynomial.c), "non-scalar field evaluation")
    return sum((c * value ** v for (t, v, w, i), c in polynomial.c.items()), Field(value.r))


def matrix_multiply(left, right):
    return [[sum((x * right[k][j] for k, x in enumerate(row)), Q())
             for j in range(len(right[0]))] for row in left]


def profile_controls():
    # Literal P diag(theta) P, without any external eigensolver.
    theta = [Q(1), Q(-1)] + [Q()] * 6
    projection = [[Q(int(i == j)) - Q(1, 8) for j in range(8)] for i in range(8)]
    compression = [[sum((projection[i][k] * theta[k] * projection[k][j]
                         for k in range(8)), Q()) for j in range(8)] for i in range(8)]
    square = matrix_multiply(compression, compression)
    active = [[Q(4, 3) * x for x in row] for row in square]
    equal("entire pair compression minimal polynomial",
          matrix_multiply(square, compression),
          [[Q(3, 4) * x for x in row] for row in compression])
    equal("entire pair active projector", matrix_multiply(active, active), active)
    equal("active projector full rank", sum(active[j][j] for j in range(8)), Q(2))
    coupling = [sum((row[k] * theta[k] for k in range(8)), Q()) for row in square]
    equal("pair coupling in active space", coupling, [Q(3, 4) * x for x in theta])
    moment = sum((theta[i] * compression[i][j] * theta[j]
                  for i in range(8) for j in range(8)), Q())
    equal("opposite sites have equal spectral weights", moment, Q())
    for name, value in [("compression", compression), ("active projector", active)]:
        LEGACY["credited moving-pair " + name] = [
            [[x.numerator, x.denominator] for x in row] for row in value]
    for name, value in [("X", Q(1, 2)), ("eta", Q(1, 2)),
                        ("Delta", Q(15, 56)), ("Gamma", Q())]:
        LEGACY["credited moving-pair " + name] = [value.numerator, value.denominator]
    return {"compression_sha256": hashlib.sha256(json.dumps(LEGACY["credited moving-pair compression"]).encode()).hexdigest(),
            "active_rank": 2, "X": "1/2", "eta": "1/2"}


SIGNS = []


def positive(name, value):
    need(value.sign() == 1, "strict exact field sign " + name)
    SIGNS.append({"name": name, "value": value.encode()})


def angular_and_fields(CP, CQ):
    v, d, a, kappa, A, B, C, K1, KQ, PG = constants()
    slope = d ** 3 * PG / 30720
    equal("singleton angular coefficient", A * Q(43, 56) + B - C, K1)
    equal("moving-pair angular coefficient", (A - C) / 2 + B, KQ)
    equal("full angular deficit constant", K1 - B, slope * Q(43, 56) + C * Q(13, 30))
    equal("full angular deficit X coefficient", -A, -slope - C * Q(56, 30))
    equal("two-family quartic coefficient", KQ - K1, -d ** 3 * PG / 114688)
    equal("all-radius angular mu4 coefficient", -A * v ** 8,
          -Q(3, 32) * v ** 3 + Q(5, 64) * v ** 4 + Q(53, 512) * v ** 5)
    equal("all-radius angular mu2-square coefficient", -B * v ** 8,
          -v ** 3 / 512 + Q(13, 1024) * v ** 4 - Q(203, 8192) * v ** 5)
    equal("all-radius angular Psi coefficient", 64 * C * v ** 8,
          v ** 3 / 8 + v ** 4 / 16 + v ** 5 / 128)
    # Bind v-exponent to Delta and w-exponent to h solely in this identity.
    delta, h = S.var(1), S.var(2)
    X = Q(43, 56) - delta
    z = Q(12, 5) * (X - Q(1, 2)) + h
    gramD = Q(3, 4) * delta - Q(25, 48) * h
    gramN = delta - Q(5, 6) * h
    equal("entire Gram identity", (Q(1, 7) + Q(4, 3) * z - (56 * X - 13) / 30)
          * gramD + gramN ** 2, delta * h / 36)
    equal("strict Gram remainder", delta * h - Q(4, 3) * h * gramD, Q(25, 36) * h ** 2)
    equal("quantitative Gram remainder",
          36 * delta * h - 48 * h * gramD, 25 * h ** 2)
    LEGACY["equality Gram certificate"] = jet_wire(
        S({(ww, vv, 0, ii): cc for (tt, vv, ww, ii), cc
           in (delta * h / 36).c.items()}), 2)
    equal("new pair-threshold factorization", 3 * PG + (4 * d + 1) ** 2,
          40 * (208 * a ** 2 + 232 * a - 215))
    equal("new one-sided angular gap coefficient", slope + Q(4, 45) * C,
          d ** 3 * (208 * a ** 2 + 232 * a - 215) / 2304)
    equal("new Gram denominator bound",
          Q(3, 4) * (Q(15, 56) + delta) - Q(25, 48) * Q(12, 5) * delta,
          Q(45, 224) - delta / 2)
    equal("new quadratic one-sided gap constant",
          Q(25) * Q(12, 5) ** 2 / (1296 * Q(45, 224)), Q(224, 405))
    # Bind v-exponent to s and t-exponent to y for the reversed quartic.
    S.limit = 4
    s, y = S.var(1), S.var(0)
    reverse = 1680 - 180 * y ** 2 - 40 * s * y ** 3 - Q(5, 2) * s ** 2 * y ** 4
    deriv = S({(t - 1, v, w, i): t * c for (t, v, w, i), c in reverse.c.items() if t})
    equal("reversed real-rooted quartic derivative", deriv, -10 * y * (s * y + 6) ** 2)
    fourth = 1680 * y ** 4 - 180 * y ** 2 - 40 * s * y - Q(5, 2) * s ** 2
    LEGACY["equality fourth derivative"] = jet_wire(fourth, 4)
    LEGACY["equality reversed derivative"] = jet_wire(deriv, 4)
    LEGACY["equality zero-third-moment quartic"] = jet_wire(
        S({k: c for k, c in fourth.c.items() if k[1] == 0}), 4)
    record("Gram strict remainder", {"h_over_27": True, "h_square_over_D": "25/1296",
                                    "for_X_below_half": ["4/45", "224/405"]})
    ag = Field(1614, Q(-385, 692), Q(5, 173))
    ap = Field(101, Q(-29, 52), Q(3, 26))
    oneg, onep = Field(1614, Q(1)), Field(101, Q(1))
    equal("angular threshold minimal polynomial", 2768 * ag ** 2 + 3080 * ag - 2875, Field(1614))
    equal("moving-pair interval endpoint minimal polynomial", 208 * ap ** 2 + 232 * ap - 215, Field(101))
    for name, value in [
        ("aG lower isolation", ag - Q(604757, 1000000)),
        ("aG upper isolation", Q(604758, 1000000) - ag),
        ("aP lower isolation", ap - Q(601908, 1000000)),
        ("aP upper isolation", Q(601909, 1000000) - ap),
        ("positive aP", ap),
        ("aP below one", onep - ap),
        ("aG below five eighths", Q(5, 8) - ag),
    ]:
        positive(name, value)
    cg = field_evaluate(CP - CQ, (oneg + ag).inverse())
    da = -(oneg + ag) ** 3 * (5536 * ag + 3080) / 114688
    ceq = -cg / da
    distance_coefficient = (2768 * ag + 3080) / 114688
    for name, value in [
        ("positive cubic tie", cg), ("cubic tie lower", cg - Q(30800, 1000000)),
        ("cubic tie upper", Q(30802, 1000000) - cg), ("negative a derivative", -da),
        ("positive equal-value slope", ceq), ("slope lower", ceq - Q(132978, 1000000)),
        ("slope upper", Q(132979, 1000000) - ceq),
        ("uniform quartic-distance margin", (2768 * ag + 3080) / (4 * 114688) - Q(77, 10000)),
        ("uniform cubic margin", cg / 4 - Q(77, 10000)),
        ("new uniform three-percent coefficient", cg - Q(3, 100)),
        ("uniform distance coefficient exceeds cubic tie", distance_coefficient - cg),
    ]:
        positive(name, value)
    equal("implicit curve slope equation", da * ceq + cg, Field(1614))
    local = lambda x: 1616 * x * x + 1800 * x - 1675
    need(local(Q(151, 250)) > 0 and 2768 * Q(151, 250) ** 2 + 3080 * Q(151, 250) - 2875 < 0,
         "local versus angular threshold ordering")
    record("aG", ag)
    record("aP", ap)
    record("cubic tie", cg)
    record("equal-value derivative", da)
    record("equal-value slope", ceq)
    for name, value in [("A", A), ("B", B), ("C", C), ("K1", K1),
                        ("Kpair", KQ), ("S", slope), ("radius sign polynomial", PG),
                        ("quartic objective gap", KQ - K1)]:
        LEGACY["angular " + name] = scalar_wire(value)
    cutoff = sum((c * Q(8, 13) ** vv for (tt, vv, ww, ii), c in KQ.c.items()), Q())
    equal("credited moving-pair cutoff coefficient", cutoff, Q(2076165, 33554432))
    LEGACY["credited earlier moving-pair cutoff coefficient"] = [cutoff.numerator, cutoff.denominator]
    LEGACY["cubic objective gap"] = scalar_wire(CP - CQ)
    for name, value in [("radius", ag), ("v", (oneg + ag).inverse()),
                        ("stationary cubic", field_evaluate(CP, (oneg + ag).inverse())),
                        ("moving-pair cubic", field_evaluate(CQ, (oneg + ag).inverse())),
                        ("cubic difference", cg), ("comparison a derivative", da),
                        ("equal-value curve slope", ceq)]:
        LEGACY["threshold " + name] = value.legacy()
    return {"aP": ap.encode(), "aG": ag.encode(), "cubic_tie": cg.encode(),
            "equal_value_slope": ceq.encode(),
            "new_pair_optimizer_interval": "[aP,aG)",
            "at_aG": "pair and singleton/seven, exactly",
            "optimal_lower_endpoint_claimed": False,
            "improved_uniform_actual_comparison": "3/100",
            "uniform_actual_comparison_supremum": "C_G",
            "supremum_attainment_claimed": False}


def controls():
    S.limit = 6
    t, v = S.var(0), S.var(1)
    q = v + (2 + S.var(3)) * t + Q(3, 5) * t ** 3
    equal("geometric full inverse control", q * q.inverse(), S(1))
    equal("binomial full square control", (q * q.conjugate()).sqrt(v) ** 2, q * q.conjugate())
    rejected = []
    for name, callback in [
        ("zero series divisor", lambda: S().inverse()),
        ("nonunit leading polynomial", lambda: (1 + v).inverse()),
        ("wrong square-root branch", lambda: (q * q.conjugate()).sqrt(2 * v)),
        ("zero field divisor", lambda: Field(1614).inverse()),
        ("mixed radicals", lambda: Field(1614) + Field(101)),
    ]:
        try:
            callback()
        except RuntimeError:
            rejected.append(name)
        else:
            raise RuntimeError("negative control accepted: " + name)
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", type=Path)
    parser.add_argument("--check", type=Path)
    parser.add_argument("--original", type=Path)
    args = parser.parse_args()
    CQ = moving_pair()
    CP = stationary()
    refinement = angular_and_fields(CP, CQ)
    profile = profile_controls()
    rejected = controls()
    original_comparison = None
    if args.original:
        old = json.loads(args.original.read_text())
        for name, value in LEGACY.items():
            need(old["records"][name] == value, "literal original record " + name)
        original_comparison = len(LEGACY)
        print("Literal complete original records compared: " + str(original_comparison))
    result = {
        "agent": "six-reviewer-3", "role": "independent mathematical reviewer",
        "target_height": 8160, "method": "Unified sparse four-index ring; direct full-degree-nine differentiation; geometric/binomial series and simultaneous Newton doubling; arbitrary symbolic mean.",
        "identity_count": len(IDENTITIES), "identities": IDENTITIES,
        "strict_sign_count": len(SIGNS), "strict_signs": SIGNS,
        "negative_controls": rejected, "refinement": refinement,
        "full_matrix_profile": profile,
        "record_count": len(RECORDS),
        "record_sha256": hashlib.sha256(json.dumps(RECORDS, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "records": RECORDS,
        "original_records_eligible_for_literal_comparison": len(LEGACY),
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        args.write.write_text(encoded)
    if args.check:
        need(json.loads(args.check.read_text()) == result, "complete expected independent summary")
    print(json.dumps({"agent": "six-reviewer-3", "verified": True,
                      "identities": len(IDENTITIES), "strict_signs": len(SIGNS),
                      "result_sha256": hashlib.sha256(encoded.encode()).hexdigest(),
                      "new_pair_interval": "[aP,aG)"}))


if __name__ == "__main__":
    main()
