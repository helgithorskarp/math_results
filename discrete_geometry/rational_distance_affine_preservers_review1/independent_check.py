#!/usr/bin/env python3
"""Independent exact audit of the rational-distance affine preserver theorem.

The target checker works in Q(cos(pi/8)) and transforms physical vertices.
This checker instead uses a different unit-triangle rotation whose doubled
angle has (cos(2t), sin(2t))=(1/3, 2*sqrt(2)/3), works only in Q(sqrt(2)),
and independently audits the local norm obstruction and coordinate recovery.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction as F
from itertools import product
from math import isqrt
from pathlib import Path


ROOT = Path(__file__).resolve().parent
K = tuple[F, F]  # a+b*sqrt(2)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def k(a: int | F = 0, b: int | F = 0) -> K:
    return (F(a), F(b))


def kadd(x: K, y: K) -> K:
    return (x[0] + y[0], x[1] + y[1])


def kneg(x: K) -> K:
    return (-x[0], -x[1])


def kmul(x: K, y: K) -> K:
    return (x[0] * y[0] + 2 * x[1] * y[1],
            x[0] * y[1] + x[1] * y[0])


def kscale(q: F, x: K) -> K:
    return (q * x[0], q * x[1])


def krational(x: K) -> bool:
    return x[1] == 0


def serialize_k(x: K) -> list[str]:
    return [str(x[0]), str(x[1])]


def rotated_gram(
    a: F, b: F, c: F, cos_twice: K, sin_twice: K
) -> tuple[K, K, K]:
    """Entries 11,12,22 of R^T [[a,b],[b,c]] R."""
    average = k((a + c) / 2)
    diagonal_half_difference = F(a - c, 2)
    first_delta = kadd(
        kscale(diagonal_half_difference, cos_twice),
        kscale(b, sin_twice),
    )
    off_diagonal = kadd(
        kscale(b, cos_twice),
        kscale(F(c - a, 2), sin_twice),
    )
    return (
        kadd(average, first_delta),
        off_diagonal,
        kadd(average, kneg(first_delta)),
    )


def rational_values(bound: int = 3, denominator_bound: int = 3) -> list[F]:
    return sorted({F(n, d)
                   for n in range(-bound, bound + 1)
                   for d in range(1, denominator_bound + 1)})


def audit_two_triangle_rigidity() -> dict[str, object]:
    # A different rotation from the target: cos(2t)=1/3, sin(2t)=2sqrt(2)/3.
    cos_alt = k(F(1, 3))
    sin_alt = k(0, F(2, 3))
    require(kadd(kmul(cos_alt, cos_alt), kmul(sin_alt, sin_alt)) == k(1),
            "invalid doubled-angle data")

    # Also reconstruct the target's pi/8 counterexample in the smaller field.
    root_half = k(0, F(1, 2))
    target_bad = rotated_gram(F(4), F(0), F(1), root_half, root_half)
    require(target_bad == (
        k(F(5, 2), F(3, 4)),
        k(0, F(-3, 4)),
        k(F(5, 2), F(-3, 4)),
    ), "displayed diagonal counterexample")

    values = rational_values()
    positive = [x for x in values if x > 0]
    checked = scalar = anisotropic = 0
    digest = hashlib.sha256()
    for a, b, c in product(positive, values, positive):
        if a * c - b * b <= 0:
            continue
        image = rotated_gram(a, b, c, cos_alt, sin_alt)
        image_rational = all(krational(entry) for entry in image)
        is_scalar = a == c and b == 0
        require(image_rational == is_scalar, "alternative rotation missed anisotropy")
        scalar += int(is_scalar)
        anisotropic += int(not is_scalar)
        checked += 1
        digest.update(json.dumps(
            [[str(a), str(b), str(c)], [serialize_k(x) for x in image]],
            separators=(",", ":"),
        ).encode())

    # Smallest pressure cases for the two separate tests.
    first_test_only = (F(4), F(0), F(1))
    require(all(isinstance(x, F) for x in first_test_only), "first test rationality")
    require(not all(krational(x) for x in rotated_gram(
        *first_test_only, cos_alt, sin_alt
    )), "anisotropic rational matrix passed the second test")
    require(rotated_gram(F(2), F(0), F(2), cos_alt, sin_alt)
            == (k(2), k(0), k(2)), "scalar positive control")
    return {
        "alternative_rotation": {
            "cos_twice": serialize_k(cos_alt),
            "sin_twice": serialize_k(sin_alt),
        },
        "positive_definite_rational_grams": checked,
        "scalar_grams": scalar,
        "anisotropic_grams": anisotropic,
        "record_sha256": digest.hexdigest(),
        "published_gl2q_counterexample_gram": [serialize_k(x) for x in target_bad],
    }


def factor_integer(n: int) -> dict[int, int]:
    require(n >= 1, "factorization needs a positive integer")
    factors: dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            n //= divisor
        divisor += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def prime(p: int) -> bool:
    return p >= 2 and all(p % d for d in range(2, isqrt(p) + 1))


def valuation_integer(n: int, p: int) -> int:
    require(n != 0 and prime(p), "valuation input")
    n = abs(n)
    exponent = 0
    while n % p == 0:
        n //= p
        exponent += 1
    return exponent


def valuation(q: F, p: int) -> int:
    require(q != 0, "zero valuation")
    return valuation_integer(q.numerator, p) - valuation_integer(q.denominator, p)


def positive_rational_square(q: F) -> bool:
    return (q > 0
            and isqrt(q.numerator) ** 2 == q.numerator
            and isqrt(q.denominator) ** 2 == q.denominator)


def odd_valuation_prime(alpha: F) -> int:
    require(alpha > 0 and not positive_rational_square(alpha),
            "positive nonsquare required")
    primes = sorted(set(factor_integer(alpha.numerator))
                    | set(factor_integer(alpha.denominator)))
    return next(p for p in primes if valuation(alpha, p) % 2)


def anisotropic_d(p: int) -> int:
    if p == 2:
        return 3
    return next(d for d in range(1, p)
                if pow((-d) % p, (p - 1) // 2, p) == p - 1)


def audit_local_form(p: int, d: int) -> dict[str, int]:
    if p == 2:
        primitive = [(x, y) for x, y in product(range(8), repeat=2)
                     if x % 2 or y % 2]
        valuations = []
        for x, y in primitive:
            value = x * x + d * y * y
            valuations.append(valuation_integer(value, 2))
        require(set(valuations) == {0, 2}, "dyadic norm parity")
        return {"residue_pairs": len(primitive), "zero_pairs": 0}

    zeros = [(x, y) for x, y in product(range(p), repeat=2)
             if (x * x + d * y * y) % p == 0]
    require(zeros == [(0, 0)], "odd-prime norm is isotropic")
    return {"residue_pairs": p * p, "zero_pairs": len(zeros)}


def form(alpha: F, d: int, x: F, y: F) -> F:
    return alpha * (x * x + d * y * y)


def audit_norm_obstruction() -> dict[str, object]:
    alphas = sorted({F(n, d) for n, d in product(range(1, 41), repeat=2)})
    coordinates = rational_values(bound=4, denominator_bound=4)
    local_forms: dict[tuple[int, int], dict[str, int]] = {}
    certificates = []
    sample_parity_checks = 0
    bounded_nonrepresentation_checks = 0
    square_controls = 0

    for alpha in alphas:
        if positive_rational_square(alpha):
            root = F(isqrt(alpha.numerator), isqrt(alpha.denominator))
            require(form(alpha, 1, 1 / root, F(0)) == 1,
                    "rational square scale lost representation")
            square_controls += 1
            continue

        p = odd_valuation_prime(alpha)
        d = anisotropic_d(p)
        if (p, d) not in local_forms:
            local_forms[p, d] = audit_local_form(p, d)
            for x, y in product(coordinates, repeat=2):
                if x == 0 and y == 0:
                    continue
                norm = x * x + d * y * y
                require(valuation(norm, p) % 2 == 0,
                        "sampled norm has odd valuation")
                sample_parity_checks += 1

        for x, y in product(coordinates, repeat=2):
            require(form(alpha, d, x, y) != 1,
                    "bounded rational counterexample to local obstruction")
            bounded_nonrepresentation_checks += 1
        certificates.append([str(alpha), p, d, valuation(alpha, p)])

    require(any(row[3] < 0 for row in certificates),
            "denominator valuations were not tested")
    require(any(row[3] > 0 for row in certificates),
            "numerator valuations were not tested")

    adversarial = {}
    for alpha in (F(2), F(1, 2), F(3), F(1, 3), F(5, 2)):
        p = odd_valuation_prime(alpha)
        d = anisotropic_d(p)
        adversarial[str(alpha)] = {
            "p": p, "d": d, "valuation": valuation(alpha, p)
        }
    require(adversarial["2"] == {"p": 2, "d": 3, "valuation": 1},
            "sqrt(2) boundary certificate")
    require(adversarial["1/2"]["valuation"] == -1,
            "negative valuation boundary")

    certificate_digest = hashlib.sha256(json.dumps(
        certificates, separators=(",", ":")
    ).encode()).hexdigest()
    return {
        "positive_rational_scales": len(alphas),
        "square_scale_controls": square_controls,
        "nonsquare_certificates": len(certificates),
        "negative_valuation_certificates": sum(row[3] < 0 for row in certificates),
        "local_forms": [
            {"p": p, "d": d, **record}
            for (p, d), record in sorted(local_forms.items())
        ],
        "rational_norm_parity_checks": sample_parity_checks,
        "bounded_nonrepresentation_checks": bounded_nonrepresentation_checks,
        "certificate_sha256": certificate_digest,
        "adversarial_certificates": adversarial,
    }


def square(q: F) -> bool:
    return q == 0 or positive_rational_square(q)


def evaluate_binary_form(H: tuple[F, F, F], z: tuple[F, F]) -> F:
    a, b, c = H
    x, y = z
    return a * x * x + 2 * b * x * y + c * y * y


def solve_symmetric(H: tuple[F, F, F], rhs: tuple[F, F]) -> tuple[F, F]:
    a, b, c = H
    determinant = a * c - b * b
    require(determinant != 0, "singular Gram")
    return ((c * rhs[0] - b * rhs[1]) / determinant,
            (a * rhs[1] - b * rhs[0]) / determinant)


def audit_coordinate_recovery_and_empty_locus() -> dict[str, int]:
    coordinates = rational_values(bound=3, denominator_bound=3)
    matrices = [
        (F(1), F(0), F(1)),
        (F(2), F(1, 2), F(3)),
        (F(5, 3), F(-1, 3), F(7, 4)),
    ]
    recovery_checks = 0
    for H in matrices:
        a, b, c = H
        require(a > 0 and a * c - b * b > 0, "non-positive Gram fixture")
        for z in product(coordinates, repeat=2):
            q0 = evaluate_binary_form(H, z)
            q1 = evaluate_binary_form(H, (z[0] - 1, z[1]))
            q2 = evaluate_binary_form(H, (z[0], z[1] - 1))
            rhs = ((a + q0 - q1) / 2, (c + q0 - q2) / 2)
            require(solve_symmetric(H, rhs) == z, "distance subtraction recovery")
            recovery_checks += 1

    empty_locus_checks = 0
    for alpha in (F(2), F(1, 2), F(3), F(1, 3)):
        p = odd_valuation_prime(alpha)
        d = anisotropic_d(p)
        H = (alpha, F(0), alpha * d)
        for z in product(coordinates, repeat=2):
            distance_squares = (
                evaluate_binary_form(H, z),
                evaluate_binary_form(H, (z[0] - 1, z[1])),
                evaluate_binary_form(H, (z[0], z[1] - 1)),
            )
            require(not all(square(q) for q in distance_squares),
                    "sampled rational-distance extension point")
            empty_locus_checks += 1
    return {
        "coordinate_recovery_checks": recovery_checks,
        "empty_locus_sample_checks": empty_locus_checks,
    }


def main() -> None:
    result = {
        "schema": 1,
        "two_triangle_rigidity": audit_two_triangle_rigidity(),
        "norm_obstruction": audit_norm_obstruction(),
        "coordinate_and_empty_locus": audit_coordinate_recovery_and_empty_locus(),
        "trust_boundary": (
            "The finite exact checks corroborate rigidity, local norms, and "
            "coordinate recovery. The universal theorem uses the audited written "
            "argument and the external Corvaja-Turchet-Zannier density criteria."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["result_sha256"] = hashlib.sha256(encoded).hexdigest()
    expected = json.loads((ROOT / "EXPECTED.json").read_text())
    require(result["result_sha256"] == expected["result_sha256"],
            "result digest differs from EXPECTED.json")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
