#!/usr/bin/env python3
"""Exact finite algebra for PROOF.md; the variational proof is written mathematics.

CPython 3.10+, standard library only. No proof input uses floating point.
The required expected.json is read only and compared in full.
"""
import copy
from fractions import Fraction as F
import hashlib
import json
from math import comb
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return tuple(p) or (F(0),)


def add(p, q):
    out = [F(0)] * max(len(p), len(q))
    for i, v in enumerate(p):
        out[i] += v
    for i, v in enumerate(q):
        out[i] += v
    return trim(out)


def scale(p, c):
    return trim(c * v for v in p)


def mul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, c in enumerate(p):
        for j, d in enumerate(q):
            out[i + j] += c * d
    return trim(out)


def power(p, n):
    require(n >= 0, "negative polynomial power")
    out = (F(1),)
    for _ in range(n):
        out = mul(out, p)
    return out


def shift(p, n):
    return trim((F(0),) * n + tuple(p))


def evaluate(p, x):
    out = F(0)
    for c in reversed(p):
        out = out * x + c
    return out


def derivative(p):
    return trim(i * p[i] for i in range(1, len(p)))


def divide_delta(p):
    # Increasing-power division by 1-a, with a mandatory remainder check.
    out, total = [], F(0)
    for c in p[:-1]:
        total += c
        out.append(total)
    require(total == -p[-1], "nonzero remainder in delta division")
    result = trim(out)
    require(mul(result, (F(1), F(-1))) == p, "division inverse mismatch")
    return result


def bernstein(p, n):
    require(len(p) <= n + 1, "incorrect Bernstein degree")
    return tuple(sum(p[k] * F(comb(i, k), comb(n, k))
                     for k in range(min(i + 1, len(p)))) for i in range(n + 1))


def invert_bernstein(beta):
    n = len(beta) - 1
    return trim(comb(n, k) * sum((-1) ** (k - i) * comb(k, i) * beta[i]
                                 for i in range(k + 1)) for k in range(n + 1))


def integral_binomial(n, weight):
    b = (F(1), F(0), F(-1))
    out = (F(0),)
    for k in range(n + 1):
        out = add(out, scale(shift(power(b, k), n - k), F(comb(n, k), k + weight + 1)))
    return out


def integral_convolution(n, weight):
    # A different full expansion: polynomials in t with coefficients in Q[a].
    a, b = (F(0), F(1)), (F(1), F(0), F(-1))
    terms = [(F(1),)]
    for _ in range(n):
        nxt = [(F(0),)] * (len(terms) + 1)
        for k, p in enumerate(terms):
            nxt[k] = add(nxt[k], mul(a, p))
            nxt[k + 1] = add(nxt[k + 1], mul(b, p))
        terms = nxt
    out = (F(0),)
    for k, p in enumerate(terms):
        out = add(out, scale(p, F(1, k + weight + 1)))
    return out


def gaussian_add(z, w):
    return z[0] + w[0], z[1] + w[1]


def gaussian_scale(z, c):
    return z[0] * c, z[1] * c


def gaussian_mul(z, w):
    return z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0]


def norm2(z):
    return z[0] ** 2 + z[1] ** 2


def lagrange_integral_weights():
    nodes = tuple(F(k, 8) for k in range(9))
    out = []
    for i, x in enumerate(nodes):
        p, denominator = (F(1),), F(1)
        for j, y in enumerate(nodes):
            if i != j:
                p = mul(p, (-y, F(1)))
                denominator *= x - y
        out.append(sum(c / (k + 1) for k, c in enumerate(p)) / denominator)
    for k in range(9):
        require(sum(w * x ** k for w, x in zip(out, nodes)) == F(1, k + 1),
                "Lagrange integration is not exact through degree eight")
    return nodes, tuple(out)


def polar_convolution(a, q):
    b = 1 - a * a
    coefficients = [(F(1), F(0))]
    for z in q:
        nxt = [(F(0), F(0))] * (len(coefficients) + 1)
        for k, c in enumerate(coefficients):
            nxt[k] = gaussian_add(nxt[k], gaussian_scale(c, a))
            nxt[k + 1] = gaussian_add(nxt[k + 1], gaussian_mul(c, gaussian_scale(z, b)))
        coefficients = nxt
    out = (F(0), F(0))
    for k, c in enumerate(coefficients):
        out = gaussian_add(out, gaussian_scale(c, F(1, k + 1)))
    return out


def polar_interpolation(a, q, nodes, weights):
    b = 1 - a * a
    out = (F(0), F(0))
    for t, w in zip(nodes, weights):
        product = (F(1), F(0))
        for z in q:
            factor = gaussian_add((a, F(0)), gaussian_scale(z, b * t))
            product = gaussian_mul(product, factor)
        out = gaussian_add(out, gaussian_scale(product, w))
    return out


def product(values):
    out = F(1)
    for x in values:
        out *= x
    return out


def vector_digest(p):
    return hashlib.sha256(json.dumps([str(x) for x in p], separators=(",", ":")).encode()).hexdigest()


def derive_manifest():
    H, T = integral_binomial(8, 0), integral_binomial(6, 1)
    require(H == integral_convolution(8, 0), "full H expansions disagree")
    require(T == integral_convolution(6, 1), "full T expansions disagree")
    a = (F(0), F(1))
    b, delta, D = (F(1), F(0), F(-1)), (F(1), F(-1)), (F(4), F(-3))
    J = mul(b, T)
    numerator = add(mul(D, add((F(1),), scale(H, -1))), scale(mul(mul(a, delta), J), 8))
    P = divide_delta(divide_delta(numerator))
    require(mul(power(delta, 2), P) == numerator, "full defect identity failed")
    require(len(P) == 16, "unexpected P degree")
    R = add(P, scale(D, -F(8, 9)))
    W = add(P, scale(T, -F(16, 5)))
    beta_R, beta_W = bernstein(R, 15), bernstein(W, 15)
    require(invert_bernstein(beta_R) == R, "R Bernstein inverse failed")
    require(invert_bernstein(beta_W) == W, "W Bernstein inverse failed")
    require(all(v >= 0 for v in beta_R), "negative R coefficient")
    require([i for i, v in enumerate(beta_R) if v == 0] == [0], "wrong R zero support")
    require(all(v > 0 for v in beta_W), "nonpositive W coefficient")
    require(min(beta_W) == F(7346, 20475), "wrong W minimum")

    # Complete identities supporting the written one-loss extremum calculus.
    y = (F(0), F(1))
    u = scale(mul(y, add(y, (F(-1),))), F(8, 7))
    ell = (F(8, 7), F(-1, 7))
    Q = add(power(y, 2), scale(u, -1))
    require(Q == mul(y, ell), "extremal norm identity failed")
    require(add(Q, scale(add(y, scale(u, -F(1, 8))), -1)) == (F(0),), "stationary identity failed")
    denominator_bound = add(add((F(1),), scale(u, F(3, 4))), scale(Q, -1))
    require(denominator_bound == power((F(-1), F(1)), 2), "derivative bound identity failed")
    differential_identity = add(mul((F(8), F(-16)), Q), mul(derivative(u), mul(y, (F(8), F(-1)))))
    require(differential_identity == (F(0),), "logarithmic derivative identity failed")
    require(mul(power(ell, 14), Q) == mul(y, power(ell, 15)), "extremal product square failed")

    extremal_controls = 0
    for M in (F(1, 2), F(1), F(3, 2)):
        for Y in (F(1), F(5, 4), F(3, 2), F(2), F(12, 5)):
            U, L = evaluate(u, Y), evaluate(ell, Y)
            z = [M * Y] + [M * L] * 7
            Qs = [M * M * (Y * Y - U)] + [(M * L) ** 2] * 7
            require(sum(z) == 8 * M and sum(Z * Z - q for Z, q in zip(z, Qs)) == U * M * M,
                    "extremal control violates constraints")
            require(0 <= U <= 4 and all(0 < q <= Z * Z for Z, q in zip(z, Qs)), "bad extremal control")
            require(product(Qs) == M ** 16 * Y * L ** 15, "extremal product mismatch")
            require(product(Qs) <= M ** 16 * ((4 + U) / (4 + 3 * U)) ** 2, "extremal rational control failed")
            extremal_controls += 1

    # Include an equal-radius positive-loss perturbation: its improvement is second order.
    perturbation_controls = 0
    for zi, zj, qi, qj in ((F(1), F(1), F(1, 2), F(1, 2)), (F(2), F(1), F(3), F(3, 4))):
        eps = F(1, 100)
        gain = 2 * eps * (zi - zj) + 2 * eps * eps
        ni, nj = qi + gain / 2, qj + gain / 2
        require(0 < ni < (zi + eps) ** 2 and 0 < nj < (zj - eps) ** 2, "perturbation lost strict slack")
        require((zi + eps) ** 2 - ni + (zj - eps) ** 2 - nj == zi ** 2 - qi + zj ** 2 - qj,
                "perturbation changed total loss")
        require(ni * nj > qi * qj, "perturbation did not increase product")
        perturbation_controls += 1

    nodes, weights = lagrange_integral_weights()
    saturation_controls = polar_controls = low_mean_controls = forced_gap_controls = 0
    for index in range(32):
        radii = [F(1 + (index * (j + 3) + j * j) % 13, 8) for j in range(8)]
        budget = (F(1), F(4, 5), F(1, 2))[index % 3]
        radii = [r * 8 * budget / sum(radii) for r in radii]
        phases = []
        for j in range(8):
            k = F((index + 2 * j) % 9 - 4, 3)
            phases.append(((1 - k * k) / (1 + k * k), 2 * k / (1 + k * k)))
        if index in (0, 1):
            phases = [(F(1), F(0))] * 8
        require(all(norm2(z) == 1 for z in phases), "nonunit Gaussian phase")
        q = [gaussian_scale(z, r) for z, r in zip(phases, radii)]
        real = [z[0] for z in q]
        mu, x = sum(radii) / 8, sum(real) / 8
        require(mu == budget and x <= mu <= 1, "bad first-moment control")
        for A in (F(1, 10), F(1, 2), F(3, 4), F(9, 10)):
            B = 1 - A * A
            enlarged = [r + 1 - mu for r in radii]
            S = max(A, x)
            if x <= A:
                lam = (A - x) / (1 - x)
                projections = [p + lam * (r - p) for p, r in zip(real, enlarged)]
            else:
                projections = real
            require(sum(enlarged) == 8 and sum(projections) == 8 * S, "saturation mean failed")
            for tau in (F(0), F(1, 7), F(1, 2), F(1)):
                h, M = B * tau, A + B * tau
                z = [A + h * r for r in enlarged]
                Qs = [A * A + 2 * A * h * p + h * h * r * r for p, r in zip(projections, enlarged)]
                original = [norm2(gaussian_add((A, F(0)), gaussian_scale(v, h))) for v in q]
                c = 16 * A * h * (1 - S)
                U = c / (M * M)
                require(sum(z) == 8 * M and sum(Z * Z - v for Z, v in zip(z, Qs)) == c,
                        "saturation loss identity failed")
                require(all(0 <= old <= new <= Z * Z for old, new, Z in zip(original, Qs, z)),
                        "saturation monotonicity failed")
                require(0 <= U <= 4 * (1 - S) <= 4, "relaxed deficit range failed")
                require(product(Qs) <= M ** 16 * ((4 + U) / (4 + 3 * U)) ** 2,
                        "pointwise rational control failed")
                bound = M ** 8 - 8 * A * h * (1 - S) * M ** 6 / (4 - 3 * S)
                require(bound >= 0 and product(original) <= bound * bound, "pointwise simplified control failed")
                saturation_controls += 1
            C = polar_convolution(A, q)
            require(C == polar_interpolation(A, q, nodes, weights), "full Gaussian polar integrals disagree")
            Ha, Ta = evaluate(H, A), evaluate(T, A)
            upper = Ha - 8 * A * (1 - S) * B * Ta / (4 - 3 * S)
            require(upper >= 0 and norm2(C) <= upper * upper, "integrated envelope control failed")
            if x <= A:
                margin = 1 - F(8, 9) * (1 - A) ** 2
                require(norm2(C) <= margin * margin, "low-mean control failed")
                low_mean_controls += 1
            if norm2(C) >= 1:
                require(x > A + F(2, 5) * (1 - A) / (A * (1 + A)), "necessary mean-gap control failed")
                forced_gap_controls += 1
            polar_controls += 1

    return {
        "agent": "six-sendov-1", "role": "researcher", "claim": "arbitrary-eight-term-polar-mean",
        "status": "ordinary-written-proof-with-exact-algebra", "formalized": False,
        "first_power_endpoint_proved": False, "critical_multiplicity_restriction": None,
        "radius_floor_required": False, "low_mean_defect": "8/9", "uniform_mean_gap": "2/5",
        "P_degree": len(P) - 1, "T_degree": len(T) - 1,
        "complete_sign_coefficients": len(beta_R) + len(beta_W),
        "R_zero_indices": [i for i, v in enumerate(beta_R) if v == 0],
        "W_minimum": str(min(beta_W)),
        "R_bernstein": [str(v) for v in beta_R], "W_bernstein": [str(v) for v in beta_W],
        "power_sha256": {name: vector_digest(p) for name, p in (("H", H), ("T", T), ("P", P), ("R", R), ("W", W))},
        "independent_full_integral_expansions": 2, "full_Bernstein_inverse_identities": 2,
        "extremum_polynomial_identities": 5, "extremal_controls": extremal_controls,
        "two_loss_perturbation_controls": perturbation_controls, "saturation_controls": saturation_controls,
        "polar_convolution_interpolation_controls": polar_controls,
        "low_mean_controls": low_mean_controls, "forced_gap_controls": forced_gap_controls,
    }


def validate_fixture(expected, derived):
    require(expected == derived, "complete expected fixture mismatch")


def main():
    derived = derive_manifest()
    expected = json.loads(Path(__file__).with_name("expected.json").read_text())
    validate_fixture(expected, derived)
    corruptions = []
    for key, value in (("uniform_mean_gap", "1"), ("first_power_endpoint_proved", True),
                       ("radius_floor_required", True), ("complete_sign_coefficients", 31)):
        bad = copy.deepcopy(expected)
        bad[key] = value
        corruptions.append(bad)
    bad = copy.deepcopy(expected)
    bad["R_bernstein"][1] = "0"
    corruptions.append(bad)
    bad = copy.deepcopy(expected)
    bad["W_bernstein"][10] = "-1"
    corruptions.append(bad)
    bad = copy.deepcopy(expected)
    bad["power_sha256"]["P"] = "0" * 64
    corruptions.append(bad)
    for bad in corruptions:
        try:
            validate_fixture(bad, derived)
        except ValueError:
            continue
        raise ValueError("corrupted fixture was accepted")
    output = {"result": "PASS", **derived, "rejected_corruptions": len(corruptions)}
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
