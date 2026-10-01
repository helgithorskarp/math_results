#!/usr/bin/env python3
"""Exact author checks for the angular square and its equality polynomials.

All arithmetic is in Q[b,z,X,eta,d]. No numerical roots or external packages.
The written spectral and analytic arguments are outside this checker.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import sys

NAMES = ("b", "z", "X", "eta", "d")
ZERO = (0,) * len(NAMES)


class Poly:
    def __init__(self, terms=0):
        if isinstance(terms, Poly):
            self.t = terms.t.copy()
        elif isinstance(terms, dict):
            self.t = {k: Q(v) for k, v in terms.items() if v}
        else:
            self.t = {ZERO: Q(terms)} if terms else {}

    def __add__(self, other):
        out = self.t.copy()
        for key, value in Poly(other).t.items():
            out[key] = out.get(key, Q(0)) + value
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.t.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) + -self

    def __mul__(self, other):
        out = {}
        for k, v in self.t.items():
            for l, w in Poly(other).t.items():
                key = tuple(x + y for x, y in zip(k, l))
                out[key] = out.get(key, Q(0)) + v * w
        return Poly(out)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * (Q(1) / Q(scalar))

    def __pow__(self, exponent):
        if not isinstance(exponent, int) or exponent < 0:
            raise ValueError("only nonnegative integer polynomial powers")
        out = Poly(1)
        for _ in range(exponent):
            out = out * self
        return out

    def derivative(self, name):
        idx = NAMES.index(name)
        out = {}
        for key, value in self.t.items():
            if key[idx]:
                reduced = list(key)
                reduced[idx] -= 1
                out[tuple(reduced)] = value * key[idx]
        return Poly(out)

    def substitute(self, name, value):
        idx = NAMES.index(name)
        value = Poly(value)
        out = Poly()
        for key, coeff in self.t.items():
            reduced = list(key)
            reduced[idx] = 0
            out += Poly({tuple(reduced): coeff}) * value ** key[idx]
        return out

    def coefficient(self, name, degree):
        idx = NAMES.index(name)
        out = {}
        for key, coeff in self.t.items():
            if key[idx] == degree:
                reduced = list(key)
                reduced[idx] = 0
                out[tuple(reduced)] = coeff
        return Poly(out)

    def scalar(self):
        if any(k != ZERO for k in self.t):
            raise ValueError("polynomial is not a scalar")
        return self.t.get(ZERO, Q(0))

    def record(self):
        return [[list(k), str(v)] for k, v in sorted(self.t.items())]


def variable(name):
    key = list(ZERO)
    key[NAMES.index(name)] = 1
    return Poly({tuple(key): Q(1)})


def require(condition, message):
    if not condition:
        raise ValueError(message)


def equal(left, right, message):
    require(not (Poly(left) - right).t, message)


def trim(p):
    p = list(p)
    while len(p) > 1 and not p[-1]:
        p.pop()
    return p


def uadd(p, q):
    out = [Q(0)] * max(len(p), len(q))
    for i, c in enumerate(p):
        out[i] += c
    for i, c in enumerate(q):
        out[i] += c
    return trim(out)


def umul(p, q):
    out = [Q(0)] * (len(p) + len(q) - 1)
    for i, c in enumerate(p):
        for j, e in enumerate(q):
            out[i + j] += c * e
    return trim(out)


def uscale(p, c):
    return trim([x * c for x in p])


def udivrem(p, q):
    p, q = trim(p), trim(q)
    require(q != [0], "division by zero polynomial")
    out = [Q(0)] * max(1, len(p) - len(q) + 1)
    while len(p) >= len(q) and p != [0]:
        k, c = len(p) - len(q), p[-1] / q[-1]
        out[k] += c
        p = uadd(p, uscale([Q(0)] * k + q, -c))
    return trim(out), p


def uinverse(p, modulus):
    a, b = modulus, p
    u, v = [Q(0)], [Q(1)]
    while b != [0]:
        quotient, remainder = udivrem(a, b)
        a, b = b, remainder
        u, v = v, uadd(u, uscale(umul(quotient, v), -1))
    require(len(a) == 1 and bool(a[0]), "polynomial inverse does not exist")
    return udivrem(uscale(u, 1 / a[0]), modulus)[1]


def newton_sums(p, order):
    n = len(p) - 1
    require(p[-1] == 1, "Newton polynomial is not monic")
    out = [Q(n)]
    for k in range(1, order + 1):
        total = Q(0)
        for j in range(1, min(k, n) + 1):
            total += p[n - j] * (out[k - j] if j < k else Q(k))
        out.append(-total)
    return out


def normalized_trace_word(order):
    """Expand tr((P D)^order), P=I-ee^T, using cyclic gap lengths.

    mu_1=0 and mu_2=1; for the used orders mu_4 is variable X.
    The empty projection word is tr(D^order). Every other word has
    one factor mu_gap/8 for each cyclic gap between rank-one factors.
    """
    X = variable("X")
    moments = {1: Poly(0), 2: Poly(1), 3: variable("z"), 4: X}
    result = Poly()
    for mask in itertools.product((0, 1), repeat=order):
        positions = [i for i, bit in enumerate(mask) if bit]
        if not positions:
            result += moments[order]
            continue
        term = Poly(Q((-1) ** len(positions), 8 ** len(positions)))
        for i, position in enumerate(positions):
            nxt = positions[(i + 1) % len(positions)]
            gap = (nxt - position) % order or order
            term *= moments[gap]
        result += term
    return result


def verify():
    b, z, X, eta, d = map(variable, NAMES)
    records = {}
    count = 0

    def identity(name, left, right=0):
        nonlocal count
        equal(left, right, name)
        count += 1
        records[name] = Poly(left).record()

    identity("trace_H2_all_four_words", normalized_trace_word(2), Q(3, 4))
    identity("trace_H4_all_sixteen_words", normalized_trace_word(4), X / 2 + Q(1, 32))
    identity("weight_second_moment", 8 * (X / 8 - Q(1, 64)), X - Q(1, 8))
    identity("centered_weight_pairing", X - Q(1, 8) - Q(3, 28), X - Q(13, 56))
    identity("centered_trace_square", X / 2 + Q(1, 32)
             - 2 * Q(3, 28) * Q(3, 4) + 7 * Q(3, 28) ** 2,
             X / 2 - Q(11, 224))

    R = 2 * b - b * b / 2
    expanded = eta - Q(1, 7) - 2 * b * (X - Q(13, 56)) + b * b * (X / 2 - Q(11, 224))
    target = eta - R * X - Q(1, 7) + Q(13, 56) * R + Q(15, 224) * b * b
    identity("complete_spectral_square", expanded, target)

    s = 4 - 3 * b
    D = 11239424 * (2 - b) * (4 - b)
    F = D * z ** 8 - D * z ** 6 / 2 + 376320 * s * (4 - b) * z ** 4 \
        - 13440 * s ** 2 * z ** 2 + 15 * s ** 3
    records["cleared_polynomial"] = F.record()
    sigma, beta = s / 224 + b * z ** 2 / 8, 1 + Q(7, 8) * b
    identity("full_ODE", sigma * F.derivative("z").derivative("z")
             - beta * z * F.derivative("z") + 8 * F)
    identity("fixed_c2", F.coefficient("z", 6), -D / 2)
    for k in range(3, 9):
        ck = F.coefficient("z", 8 - k)
        prev = F.coefficient("z", 10 - k)
        identity("recurrence_k" + str(k),
                 k * (1 - b * Q(8 - k, 8)) * ck + s * Q((10 - k) * (9 - k), 224) * prev)
    positivity = {}
    for k in range(3, 9):
        for endpoint in (Q(-8, 5), Q(4, 3)):
            value = k * (1 - endpoint * Q(8 - k, 8))
            require(value > 0, "recurrence factor is not positive")
            positivity[str(k) + "@" + str(endpoint)] = str(value)
    records["affine_recurrence_endpoint_signs"] = positivity

    evaluation = Poly()
    for k in range(5):
        evaluation += F.coefficient("z", 2 * k) * (-s) ** k * (28 * b) ** (4 - k)
    factored = 87808 * s ** 3 * (7 * b + 8) * (5 * b + 8) * (3 * b + 8) * (b + 8)
    identity("complete_sigma_zero_evaluation", evaluation, factored)
    records["collision_parameter_factors"] = ["-8/7", "-8/5", "-8/3", "-8"]
    # The only such factor inside (-8/5,4/3) is -8/7.
    for value in (Q(-8, 3), Q(-8)):
        require(value < Q(-8, 5), "unaccounted collision parameter")

    def at(parameter):
        denom = D.substitute("b", parameter).scalar()
        require(bool(denom), "singular polynomial parameter")
        return F.substitute("b", parameter) / denom

    endpoint = at(Q(-8, 7))
    derivative_y = sum(k * endpoint.coefficient("z", 2 * k).scalar() * Q(13, 56) ** (k - 1)
                       for k in range(1, 5))
    require(derivative_y == Q(169, 90552), "exceptional derivative-root collision")
    records["exceptional_hprime"] = str(derivative_y)
    identity("lower_endpoint_factorization", at(Q(-8, 5)),
             (z ** 2 - Q(11, 56)) ** 2 * (z ** 4 - Q(3, 28) * z ** 2 + Q(11, 9408)))
    identity("upper_endpoint_factorization", at(Q(4, 3)), z ** 6 * (z ** 2 - Q(1, 2)))

    h0, h1 = Poly(1), z
    for n in range(1, 8):
        h0, h1 = h1, z * h1 - Q(n, 56) * h0
    identity("Hermite_Jacobi_determinant_recurrence", at(0), h1)
    records["Hermite_polynomial"] = at(0).record()
    records["endpoint_polynomials"] = {str(k): at(k).record() for k in (Q(-8, 5), Q(-8, 7), Q(4, 3))}

    identity("complete_Xb_formula",
             112 * (2 - b) * (D / 2 - 4 * F.coefficient("z", 4)), (52 - 11 * b) * D)
    identity("Qnorm_at_optimizer", (52 - 11 * b) / 2 - Q(11, 2) * (2 - b), 15)
    for parameter, ex, ee in ((Q(-8, 5), Q(29, 168), Q(5, 21)), (Q(0), Q(13, 56), Q(1, 7)),
                              (Q(4, 3), Q(1, 2), Q(1, 2))):
        px = [at(parameter).coefficient("z", i).scalar() for i in range(9)]
        sums = newton_sums(px, 4)
        require(sums[1] == 0 and sums[2] == 1 and sums[4] == ex, "endpoint normalization/moment")
        actual_eta = Q(1, 7) + 15 * parameter ** 2 / (112 * (2 - parameter))
        require(actual_eta == ee, "endpoint weight invariant")
    records["endpoint_X_eta"] = {"-8/5": ["29/168", "5/21"], "0": ["13/56", "1/7"], "4/3": ["1/2", "1/2"]}

    numerator = 16 * (48 * d ** 2 - 40 * d - 53)
    denominator = (4 * d + 1) ** 2
    identity("radius_ratio_derivative_numerator", numerator.derivative("d") * denominator
             - numerator * denominator.derivative("d"), 2048 * (2 * d + 3) * (4 * d + 1))
    identity("lower_radius_equation", numerator + Q(112, 25) * denominator,
             Q(32, 25) * (656 * d ** 2 - 472 * d - 659))
    identity("upper_radius_equation", numerator - Q(16, 9) * denominator,
             Q(32, 9) * (208 * d ** 2 - 184 * d - 239))
    identity("Hermite_radius_equation", (48 * d ** 2 - 40 * d - 53).substitute("d", d + 1),
             48 * d ** 2 + 56 * d - 45)
    radius_discriminants = {
        "a_L": 840 ** 2 + 4 * 656 * 475,
        "a_minus": 232 ** 2 + 4 * 208 * 215,
        "a_H": 56 ** 2 + 4 * 48 * 45,
    }
    require(radius_discriminants == {"a_L": 80 ** 2 * 305, "a_minus": 48 ** 2 * 101, "a_H": 16 ** 2 * 46},
            "radius radical normalization")
    records["radius_discriminants"] = radius_discriminants

    D0, Db0 = D.substitute("b", 0).scalar(), D.derivative("b").substitute("b", 0).scalar()
    tangent = (F.derivative("b").substitute("b", 0) * D0 - F.substitute("b", 0) * Db0) / (2 * D0 ** 2)
    identity("whole_Hermite_R_tangent", tangent,
             -Q(15, 1792) * z ** 4 + Q(45, 50176) * z ** 2 - Q(45, 5619712))
    f = [at(0).coefficient("z", i).scalar() for i in range(9)]
    fp = [i * f[i] for i in range(1, 9)]
    ht = [tangent.coefficient("z", i).scalar() for i in range(5)]
    root_tangent = udivrem(uscale(umul(ht, uinverse(fp, f)), -1), f)[1]
    require(root_tangent == [0, -Q(13, 64), 0, Q(7, 8)], "root-response quotient identity")
    speed_poly = umul(root_tangent, root_tangent)
    moments = newton_sums(f, 6)
    speed2 = sum(c * moments[i] for i, c in enumerate(speed_poly))
    require(speed2 == Q(15, 2048), "root-response Euclidean norm")
    records["Hermite_root_response"] = {"polynomial": [str(x) for x in root_tangent], "norm_squared": str(speed2)}

    # Derive first response of X from the whole coefficient tangent.
    xprime = -4 * tangent.coefficient("z", 4).scalar()
    require(xprime == Q(15, 448), "fourth-moment response")
    records["Hermite_response_coefficients"] = {"X_R": str(xprime), "eta_R2": "15/896", "maximum_R2": "15/896"}

    return {"identity_count": count, "records": records}


def damage_controls():
    b, z, X, eta, d = map(variable, NAMES)
    for name, left, right in (
        ("wrong_weight_moment", X - Q(1, 8), X - Q(1, 7)),
        ("wrong_square_constant", eta - Q(1, 7), eta - Q(1, 8)),
        ("wrong_Hermite_tangent", Q(7, 8) * z ** 3 - Q(13, 64) * z,
         Q(7, 8) * z ** 3 - Q(13, 63) * z),
        ("dropped_collision_factor", (7 * b + 8) * (5 * b + 8), 7 * b + 8),
    ):
        rejected = False
        try:
            equal(left, right, name)
        except ValueError:
            rejected = True
        require(rejected, "damaged expression was accepted: " + name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected", type=Path, default=Path(__file__).with_name("expected.json"))
    parser.add_argument("--write-expected", action="store_true", help="maintainer operation; explicitly replace the fixture")
    args = parser.parse_args()
    result = verify()
    damage_controls()
    serialized = json.dumps(result, sort_keys=True, separators=(",", ":"))
    if args.write_expected:
        args.expected.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    expected = json.loads(args.expected.read_text())
    require(result == expected, "complete expected-record mismatch")
    # A damaged fixture must also fail equality under optimized Python.
    damaged = json.loads(serialized)
    damaged["identity_count"] += 1
    require(result != damaged, "damaged fixture was accepted")
    print(json.dumps({"status": "all exact checks passed", "identities": result["identity_count"],
                      "records": len(result["records"]), "damage_controls": 5,
                      "record_sha256": hashlib.sha256(serialized.encode()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print("verification failed: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
