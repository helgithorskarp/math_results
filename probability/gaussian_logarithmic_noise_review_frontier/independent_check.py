#!/usr/bin/env python3
"""Clean-room exact checks for the logarithmic-noise polynomial review.

This checker imports no code or expected record from the target packet.  It
checks the theorem's scalar reductions, reconstructs Legendre polynomials by
Rodrigues' formula, tests the abstract hinge envelope on explicit globally
nonnegative polynomials, and evaluates the full Taylor order on a different
four-site contraction by definition-level replica enumeration.
"""

from fractions import Fraction as F
from itertools import product
from math import comb, factorial, isqrt
from pathlib import Path
import hashlib
import json
import random


ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "probability" / "gaussian_logarithmic_noise_certificate"
HERE = Path(__file__).resolve().parent
PINS = {
    "PROOF.md": "c997d0e58746e17f4f002a1299fa5079704bf2a59de850a89f07d10998b9fa5f",
    "SOURCES.md": "4a7877f8baa4f8298f8416cad4408993290197343eca44337ba9e3ffc8a8ba56",
    "INPUTS.json": "22132a31b6a176ea205ac5bd41dc1664d87f8cdd4e37364c633bdd80cdbcbd11",
    "EXPECTED.json": "c388c0bfa5f553ba9d0967d7304b5f8fe4177b47ca55655700615541c5203a19",
    "certificate.py": "beec07357ca79cb162b36e41fab72217fd0cf66a02b0ec8e9e87c179fd7b6958",
    "moments.py": "a6f6d1ea464e7e3b828ee66c665a3eec430ebb50f2140eccfe8525593e1ebf7b",
    "verify.py": "1e2553f8ee3b986572f57eb0c13ed8fadf77000d8dad779916024e7fd7c2662d",
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(obj):
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def pin_target():
    for name, wanted in PINS.items():
        actual = hashlib.sha256((TARGET / name).read_bytes()).hexdigest()
        need(actual == wanted, "target pin mismatch: " + name)
    return len(PINS)


def constant_chain():
    # log(2)=2 sum 1/((2j+1)3^(2j+1)).  The first term is 2/3; bounding
    # 1/(2j+1) by 1/3 in the remaining geometric tail gives 25/36.
    log_lower = F(2, 3)
    log_upper = F(2, 3) + F(1, 36)
    need(log_lower < log_upper < F(3, 4), "logarithm bounds")

    # Elementary exponential-series controls used in the proof.
    exp_three_quarters_upper = 1 + F(3, 4) + F(9, 32) / (1 - F(1, 4))
    exp_four_partial = sum(F(4) ** j / factorial(j) for j in range(5))
    need(exp_three_quarters_upper == F(17, 8) < 4, "exp(3/4) upper")
    need(exp_four_partial > 32, "exp(4) lower")
    need(1 / (1 - F(1, 4)) == F(4, 3), "exp(1/4) geometric upper")
    need(1 / (1 - F(1, 2)) == 2, "exp(1/2) geometric upper")
    # For e, n!>=2^(n-1) from n=2 onward, so its strict upper bound is
    # 1+1+sum_(n>=2)2^(-(n-1))=3.
    need(1 + 1 + F(1, 1) == 3, "e geometric upper")

    # Worst-case interior constants: k>=12, epsilon<=1/(8k),
    # ell<=2k log(2), and kappa>=95/96.
    q_squared_upper = 32 * F(1, 8) * F(3, 2) * F(96, 95)
    beta_lower = 5 - F(96, 95)
    need(q_squared_upper < F(25, 4), "q<5/2")
    need(beta_lower - F(5, 2) > 1, "beta-q gap")
    need(F(5, 96) + F(5, 2) < 3, "interior exponential")
    need(2 * log_lower - F(1, 192) > 1, "interior log length")
    need(F(1, 648) > F(1, 1024), "interior weakening")

    # The loss-modulus constant after sqrt(pi)<2, sqrt(pi)>5/3,
    # sqrt(2pi)<8/3, and exp(1/4)<4/3.
    modulus = F(1, 4) * F(9, 8) * F(4, 3) * F(169, 25) * F(139, 25)
    need(modulus == F(70473, 5000) < 16, "tail modulus")

    # It suffices to compare the lower bound 4k-3/4 with
    # (5k-2)log(2), using log(2)<3/4.
    for k in (12, 13, 32, 128, 1024):
        need(4 * k - F(3, 4) > (5 * k - 2) * log_upper,
             "outer cutoff")
    return {
        "log_interval": [str(log_lower), str(log_upper)],
        "q_squared_upper": str(q_squared_upper),
        "modulus_upper": str(modulus),
        "outer_k_controls": 5,
    }


def add(p, q):
    out = [F(0)] * max(len(p), len(q))
    for i, value in enumerate(p):
        out[i] += value
    for i, value in enumerate(q):
        out[i] += value
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def scale(p, value):
    return [value * coefficient for coefficient in p]


def mul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, left in enumerate(p):
        for j, right in enumerate(q):
            out[i + j] += left * right
    return out


def derivative(p):
    return [F(i) * p[i] for i in range(1, len(p))] or [F(0)]


def power(p, exponent):
    out = [F(1)]
    for _ in range(exponent):
        out = mul(out, p)
    return out


def value(p, x):
    out = F(0)
    for coefficient in reversed(p):
        out = out * x + coefficient
    return out


def integral(p, left, right):
    return sum(coefficient * (right ** (i + 1) - left ** (i + 1)) / (i + 1)
               for i, coefficient in enumerate(p))


def rodrigues_legendre(n):
    row = power([-1, 0, 1], n)
    for _ in range(n):
        row = derivative(row)
    return scale(row, F(1, (2 ** n) * factorial(n)))


def legendre_controls():
    rows = [rodrigues_legendre(n) for n in range(15)]
    orthogonality = 0
    for i, left in enumerate(rows):
        for j, right in enumerate(rows):
            actual = integral(mul(left, right), F(-1), F(1))
            wanted = F(2, 2 * i + 1) if i == j else F(0)
            need(actual == wanted, "Rodrigues orthogonality")
            orthogonality += 1

    reproductions = 0
    test_points = (F(-7, 4), F(-1), F(1, 5), F(4, 3))
    for n in range(8):
        for degree in range(n + 1):
            monomial = [F(0)] * degree + [F(1)]
            for x in test_points:
                got = sum(F(2 * j + 1, 2) * value(rows[j], x)
                          * integral(mul(rows[j], monomial), F(-1), F(1))
                          for j in range(n + 1))
                need(got == x ** degree, "reproducing kernel")
                reproductions += 1

    # The Abel coefficient is evaluated independently by x=W(1-t^2).
    beta = F(2)
    abel = []
    for m in range(13):
        if m:
            beta *= F(2 * m, 2 * m + 1)
        abel.append(beta)
    need(abel[1] == F(4, 3), "interior Abel factor")
    return {
        "Rodrigues_rows": len(rows),
        "orthogonality_pairs": orthogonality,
        "reproductions_including_outside": reproductions,
        "Abel_coefficients_digest": digest([str(x) for x in abel]),
    }


def schedule(k, n):
    need(k >= 12 and 0 <= n <= 2 ** (k - 4) - 1, "eligible schedule")
    r = F(1, 2 ** (2 * k))
    a = F(1, 2 ** (5 * k - 2))
    length = F(1, 4) - r
    root_a_upper = F(1, 2 ** (2 * k - 1))
    need(0 < a < r < F(1, 4) and length >= F(1, 8), "interval order")
    need((n + 1) ** 2 * r <= F(1, 256), "degree-radius bound")
    need((n + 1) ** 2 * r / length <= F(1, 32), "kernel prefactor")
    need(4 * n * n * r / length < F(1, 4), "kernel exponent")
    need(a <= root_a_upper ** 2, "tail square-root upper")
    adverse = F(2, 3 * r) * a * root_a_upper
    need(adverse < r / 2048, "tail payment")
    need(length / (n + 1) ** 2 >= 32 * r, "mass from maximum")
    need((r / 1024 - adverse) * length / (n + 1) ** 2
         >= r * r / 64, "final polynomial margin")


def schedule_controls():
    checked = 0
    for n in range(1025):
        k = max(12, 4 + n.bit_length())
        schedule(k, n)
        q = 8 * n + 4 * k + 24
        epsilon = F(1, 8 * k)
        need(q >= 3 * (n + 2) * epsilon, "factorial schedule")
        need(7 * n - q - 3 <= -4 * k - 8, "Taylor exponent")
        checked += 1
    endpoints = []
    for k in (12, 13, 16, 32, 64, 128, 1024):
        n = 2 ** (k - 4) - 1
        schedule(k, n)
        endpoints.append([k, n, 8 * n + 4 * k + 24])
    return {
        "small_degrees": checked,
        "endpoint_digest": digest(endpoints),
        "large_k": [row[0] for row in endpoints],
    }


def chebyshev_and_taylor_controls():
    # Worst allowed affine substitution t=16u-3.  Coefficient l1 norms for
    # smaller |alpha|,|beta| obey the same recurrence bound.
    rows = [[F(1)], [F(-3), F(16)]]
    for degree in range(1, 32):
        rows.append(add(scale(mul([F(-3), F(16)], rows[degree]), 2),
                        scale(rows[degree - 1], -1)))
    norms = [sum(abs(coefficient) for coefficient in row) for row in rows]
    for degree, norm in enumerate(norms):
        need(norm <= 64 ** degree, "Chebyshev coefficient norm")
        need(1 + 2 * sum(F(64) ** j for j in range(1, degree + 1))
             <= 2 * (degree + 1) * F(64) ** degree,
             "curvature coefficient sum")

    exact_budgets = 0
    for n in range(65):
        k = max(12, 4 + n.bit_length())
        epsilon = F(1, 8 * k)
        order = 8 * n + 4 * k + 24
        prefactor = F((n + 1) * 64 ** n, 8)
        exact = prefactor * (F(n + 2) * epsilon / 2) ** order \
                / factorial(order)
        need(exact <= F(1, 2 ** (4 * k + 8)), "exact Taylor budget")
        exact_budgets += 1
    return {
        "Chebyshev_rows": len(rows),
        "norm_digest": digest([str(value) for value in norms]),
        "exact_factorial_budgets": exact_budgets,
    }


def sqrt_enclosure(integer, bits=240):
    denominator = 1 << bits
    lower_numerator = isqrt(integer << (2 * bits))
    return F(lower_numerator, denominator), F(lower_numerator + 1, denominator)


def dist2(left, right):
    return sum((a - b) ** 2 for a, b in zip(left, right))


def taylor_polynomial(z, order):
    total = F(1)
    term = F(1)
    for j in range(1, order + 1):
        term *= -z / j
        total += term
    return total


def direct_taylor_numerator(points, weights, m, order):
    total = F(0)
    tuples = 0
    for labels in product(range(len(points)), repeat=m):
        weight = F(1)
        for label in labels:
            weight *= weights[label]
        scatter = sum(dist2(points[labels[i]], points[labels[j]])
                      for i in range(m) for j in range(i + 1, m)) / (2 * m)
        total += weight * (1 - taylor_polynomial(scatter, order))
        tuples += 1
    return total, tuples


def dyadic_interval(lower, upper, bits=80):
    denominator = 1 << bits
    lo = (lower * denominator).numerator // (lower * denominator).denominator
    hi_scaled = upper * denominator
    hi = -((-hi_scaled.numerator) // hi_scaled.denominator)
    return [str(F(lo, denominator)), str(F(hi, denominator))]


def finite_functional_control():
    # A four-site collapse, unrelated to the target packet's deep-flap data.
    points = [
        (F(1, 20), F(0), F(0)),
        (F(-1, 25), F(1, 30), F(0)),
        (F(0), F(-1, 28), F(1, 32)),
        (F(1, 40), F(1, 35), F(-1, 30)),
    ]
    weights = [F(1, 10), F(2, 10), F(3, 10), F(4, 10)]
    epsilon = F(1, 96)
    need(max(sum(coordinate * coordinate for coordinate in point)
             for point in points) <= epsilon, "support radius")
    loss = sum(weights[i] * weights[j] * dist2(points[i], points[j])
               for i in range(4) for j in range(4))
    need(loss > 0, "positive collapse loss")

    # Curvature p(u)=(1-u)^2 has a negative monomial coefficient.  The
    # theorem's full order at n=2,k=12 is Q=88.
    order = 88
    numerators = {}
    tuple_count = 0
    for m in (2, 3, 4):
        numerators[m], count = direct_taylor_numerator(points, weights, m, order)
        need(numerators[m] > 0, "positive Taylor numerator")
        tuple_count += count

    sqrt2_lo, sqrt2_hi = sqrt_enclosure(2)
    sqrt3_lo, sqrt3_hi = sqrt_enclosure(3)
    l2_lo = numerators[2] / (4 * sqrt2_hi)
    l2_hi = numerators[2] / (4 * sqrt2_lo)
    l3_lo = numerators[3] / (18 * sqrt3_hi)
    l3_hi = numerators[3] / (18 * sqrt3_lo)
    l4 = numerators[4] / 96
    functional_lo = l2_lo - 2 * l3_hi + l4
    functional_hi = l2_hi - 2 * l3_lo + l4
    need(0 < functional_lo <= functional_hi, "direct functional enclosure")

    r = F(1, 2 ** 24)
    maximum = (1 - r) ** 2
    claimed = 3 * loss * maximum / 2 ** 56
    need(functional_lo > claimed, "finite-functional theorem margin")
    need(functional_hi < loss / 10, "overclaim mutation was not rejected")

    error = F(0)
    for exponent, coefficient in enumerate((1, -2, 1)):
        m = exponent + 2
        error += abs(coefficient) * (F(m) * epsilon / 2) ** order \
                 / (4 * m * m * factorial(order))
    need(error < maximum / 2 ** 56, "Taylor error budget")
    exact_data = [[m, str(numerators[m])] for m in (2, 3, 4)]
    return {
        "geometry": "four-site collapse",
        "loss": str(loss),
        "order": order,
        "replica_tuples": tuple_count,
        "functional_over_loss": dyadic_interval(functional_lo / loss,
                                                   functional_hi / loss),
        "exact_numerators_digest": digest(exact_data),
    }


def integrate_sqrt(poly, upper):
    # In this check upper=a=2^-58, so sqrt(upper)=2^-29 exactly.
    root = F(1, 2 ** 29)
    need(root * root == upper, "exact tail root")
    return sum(coefficient * 2 * upper ** i * upper * root / (2 * i + 3)
               for i, coefficient in enumerate(poly))


def envelope_value(poly, a, r, b):
    adverse = 16 * integrate_sqrt(poly, a)
    positive = integral([F(0)] + poly, r, b) / 1024
    return positive - adverse


def abstract_envelope_controls():
    k = 12
    a = F(1, 2 ** (5 * k - 2))
    r = F(1, 2 ** (2 * k))
    b = F(1, 4)
    families = []

    for degree in range(13):
        monomial = [F(0)] * degree + [F(1)]
        families.append((monomial, b ** degree))
        reflected = power([F(1), F(-1)], degree)
        families.append((reflected, (1 - r) ** degree))
    for center in (F(0), F(1, 8), F(1, 3), F(1, 2), F(3, 4), F(1)):
        for half_degree in range(1, 7):
            polynomial = power([-center, F(1)], 2 * half_degree)
            maximum = max(abs(r - center), abs(b - center)) ** (2 * half_degree)
            families.append((polynomial, maximum))

    margins = []
    for polynomial, maximum in families:
        need(all(value(polynomial, x) >= 0
                 for x in (F(0), a, r, b, F(1))), "family nonnegativity")
        lower = envelope_value(polynomial, a, r, b)
        need(lower >= maximum * r * r / 64, "abstract envelope margin")
        margins.append(str(lower - maximum * r * r / 64))

    # Positive sums remain globally nonnegative.  The sum of component
    # maxima is an upper bound for the true maximum, so this is a stronger
    # check than using a sampled maximum.
    rng = random.Random(27182818)
    sums = 0
    for _ in range(40):
        selected = [families[rng.randrange(len(families))] for _ in range(5)]
        coefficients = [F(rng.randrange(1, 10), rng.randrange(2, 13))
                        for _ in selected]
        polynomial = [F(0)]
        maximum_upper = F(0)
        for coefficient, (row, maximum) in zip(coefficients, selected):
            polynomial = add(polynomial, scale(row, coefficient))
            maximum_upper += coefficient * maximum
        lower = envelope_value(polynomial, a, r, b)
        need(lower >= maximum_upper * r * r / 64,
             "positive-sum envelope margin")
        margins.append(str(lower - maximum_upper * r * r / 64))
        sums += 1
    return {
        "individual_polynomials": len(families),
        "positive_sums": sums,
        "margin_digest": digest(margins),
    }


def layer_cake_controls():
    rng = random.Random(314159)
    checks = 0
    curvatures = [
        [F(1)],
        power([F(1), F(-1)], 2),
        power([F(-1, 3), F(1)], 4),
    ]
    for _ in range(40):
        f = [F(rng.randrange(1, 90), 100) for _ in range(4)]
        transfer = min(f[1], 1 - f[0]) / F(rng.randrange(3, 10))
        g = [f[0] + transfer, f[1] - transfer, f[2], f[3]]
        need(sum(f) == sum(g) and all(0 <= x <= 1 for x in f + g),
             "mass-preserving values")
        for curvature in curvatures:
            # Double antiderivative with zero affine part.
            energy = [F(0), F(0)] + [coefficient / ((i + 1) * (i + 2))
                                      for i, coefficient in enumerate(curvature)]
            direct = sum(value(energy, x) for x in g) \
                     - sum(value(energy, x) for x in f)
            hinges = sum(sum(coefficient * x ** (i + 2) / ((i + 1) * (i + 2))
                              for i, coefficient in enumerate(curvature))
                          for x in g) \
                     - sum(sum(coefficient * x ** (i + 2) / ((i + 1) * (i + 2))
                               for i, coefficient in enumerate(curvature))
                           for x in f)
            need(direct == hinges, "layer-cake normalization")
            checks += 1
    return checks


def build_record():
    return {
        "status": "LOGARITHMIC_NOISE_INDEPENDENT_ACCEPT",
        "target_pins": pin_target(),
        "constants": constant_chain(),
        "Legendre_and_Abel": legendre_controls(),
        "schedules": schedule_controls(),
        "Chebyshev_and_Taylor": chebyshev_and_taylor_controls(),
        "abstract_envelope": abstract_envelope_controls(),
        "finite_functional": finite_functional_control(),
        "layer_cake_identities": layer_cake_controls(),
    }


def main():
    actual = build_record()
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    need(actual == expected, "independent expected record mismatch")
    print(actual["status"])
    print("record_sha256=" + digest(actual))


if __name__ == "__main__":
    main()
