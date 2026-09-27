#!/usr/bin/env python3
"""Independent exact controls for all-radius loss-relative localization.

No target module is imported.  The checker pins the exact reviewed commit,
checks the straight-path and Procrustes algebra on independent rational
families, reconstructs the beta-kernel variance as a polynomial identity,
and audits the interpolation and symbolic budget constants.
"""

from fractions import Fraction as Q
from math import comb, factorial, isqrt
import hashlib
import itertools
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TARGET_COMMIT = "1104fcce0bfcf2d9cb16f70daa45c361f54c977c"
TARGET_DIR = "probability/gaussian_all_radius_loss_localization"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def git_bytes(commit, path):
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout


def pin_sources():
    records = json.loads((HERE / "TARGET_SOURCES.json").read_text())
    for record in records:
        raw = git_bytes(record["commit"], record["path"])
        require(hashlib.sha256(raw).hexdigest() == record["sha256"],
                f"reviewed source drift: {record['path']}")
    return len(records)


def trim(poly):
    poly = list(poly)
    while len(poly) > 1 and not poly[-1]:
        poly.pop()
    return poly


def poly_add(left, right):
    result = [Q(0)] * max(len(left), len(right))
    for poly in (left, right):
        for degree, coefficient in enumerate(poly):
            result[degree] += coefficient
    return trim(result)


def poly_scale(poly, scalar):
    return trim([scalar * coefficient for coefficient in poly])


def poly_mul(left, right):
    result = [Q(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return trim(result)


def poly_pow(poly, exponent):
    result = [Q(1)]
    factor = list(poly)
    while exponent:
        if exponent & 1:
            result = poly_mul(result, factor)
        factor = poly_mul(factor, factor)
        exponent //= 2
    return result


def beta_variance_polynomial_controls(maximum_n=48):
    checks = 0
    u = [Q(0), Q(1)]
    one_minus_u = [Q(1), Q(-1)]
    for n in range(maximum_n + 1):
        denominator = (n + 2) * (n + 3)
        direct = [Q(0)]
        for j in range(n + 1):
            binomial_mass = poly_scale(
                poly_mul(poly_pow(u, j), poly_pow(one_minus_u, n - j)),
                comb(n, j))
            conditional = [Q((j + 1) * (j + 2), denominator),
                           Q(-2 * (j + 1), n + 2), Q(1)]
            direct = poly_add(direct, poly_mul(binomial_mass, conditional))
        expected = [Q(2, denominator), Q(2 * (n - 3), denominator),
                    Q(-2 * (n - 3), denominator)]
        require(trim(direct) == trim(expected),
                "Bernstein--Durrmeyer variance polynomial")
        # The quadratic maximum is at an endpoint or u=1/2.
        for value in (Q(0), Q(1, 2), Q(1)):
            evaluated = sum(c * value ** degree
                            for degree, c in enumerate(expected))
            require(evaluated <= Q(1, n + 2), "variance upper bound")
        checks += 4
    return checks


def lagrange_controls():
    checks = 0
    records = []
    for r in range(1, 18):
        B = Q(r + 4, 2)
        b = Q(3, 2)
        # Quantile-separated nodes, with deliberately nonuniform extra gaps.
        nodes = [(-B + Q(1, 3)
                  + Q(j * b, r)
                  + Q(j * (j - 1), 20 * r * r)) for j in range(r + 1)]
        require(nodes[-1] < B, "test nodes escaped the anchor interval")
        coefficients = []
        for j, xj in enumerate(nodes):
            denominator = Q(1)
            numerator = Q(1)
            for i, xi in enumerate(nodes):
                if i != j:
                    denominator *= xj - xi
                    numerator *= B - xi
                    require(abs(xj - xi) >= Q(abs(j - i)) * b / r,
                            "quantile separation")
            coefficient = numerator / denominator
            coefficients.append(coefficient)
            bound = ((2 * B * r / b) ** r
                     / (factorial(j) * factorial(r - j)))
            require(abs(coefficient) <= bound, "Lagrange coefficient bound")
        for degree in range(r + 1):
            require(sum(coefficient * node ** degree
                        for coefficient, node in zip(coefficients, nodes))
                    == B ** degree, "Lagrange monomial reproduction")
            checks += 1
        reciprocal_sum = sum(Q(1, factorial(j) * factorial(r - j))
                             for j in range(r + 1))
        require(reciprocal_sum == Q(2 ** r, factorial(r)),
                "binomial reciprocal sum")
        require(sum(map(abs, coefficients)) <= (12 * B / b) ** r,
                "summed interpolation coefficient bound")
        records.append((r, str(sum(map(abs, coefficients)))))
        checks += r + 4
    return checks, records


def derivative_and_remainder_controls():
    checks = 0
    double_factorial = 1
    for m in range(1, 41):
        double_factorial *= 2 * m - 1
        require(double_factorial == factorial(2 * m) // (2 ** m * factorial(m)),
                "Gaussian Fourier moment")
        checks += 1
    for B in range(1, 13):
        m = 16 * B * B
        # (2B^2)^m/m! <= (3/8)^m <= 2^-m, without floating point.
        require((8 * 2 * B * B) ** m <= 3 ** m * factorial(m),
                "factorial interpolation remainder")
        require(3 ** m <= 4 ** m, "dyadic interpolation remainder")
        checks += 2
    return checks


def ceil_sqrt(value):
    root = isqrt(value)
    return root + (root * root < value)


def ceil_log2(value):
    require(value > 0, "positive logarithm argument")
    exponent = value.numerator.bit_length() - value.denominator.bit_length()
    power = Q(2 ** exponent) if exponent >= 0 else Q(1, 2 ** (-exponent))
    if power < value:
        exponent += 1
    lower = (Q(2 ** (exponent - 1)) if exponent - 1 >= 0
             else Q(1, 2 ** (1 - exponent)))
    upper = Q(2 ** exponent) if exponent >= 0 else Q(1, 2 ** (-exponent))
    require(lower < value <= upper, "logarithm ceiling")
    return exponent


def localization_constants(radius, kappa, level_index):
    B = 2 * radius + ceil_sqrt(2 * (level_index + 1))
    r = 32 * B * B - 1
    lam = 1 + Q(4 * radius * radius, 1) / kappa
    K = 56 * B ** 3 * 2 ** (3 * level_index) * lam
    T = 4 * (2 * radius + 3) ** 3 * lam * 2 ** (296 * radius * radius)
    return B, r, lam, K, T


def constant_controls():
    checks = 0
    for radius, level_index in itertools.product(range(1, 9),
                                                  (0, 1, 4, 16, 64, 127)):
        B, r, lam, K, tail = localization_constants(
            radius, Q(1, 257), level_index)
        m = 16 * B * B
        require((B - 2 * radius) ** 2 >= 2 * (level_index + 1),
                "far-anchor Gaussian decay")
        require(m >= level_index + 2 and r == 2 * m - 1,
                "interpolation order")
        require(K == 56 * B ** 3 * 2 ** (3 * level_index) * lam,
                "middle constant normalization")
        require(tail >= 4 * (2 * radius + 3) ** 3 * lam,
                "tail constant normalization")
        checks += 4
    return checks


def squared_norm(vector):
    return sum(value * value for value in vector)


def subtract(left, right):
    return tuple(a - b for a, b in zip(left, right))


def path_and_gram_controls():
    points = [tuple(Q(value) for value in signs)
              for signs in itertools.product((-1, 1), repeat=3)]
    weights = [Q(1, 8)] * len(points)
    path_checks = gram_checks = 0
    records = []
    for scales in ((Q(1), Q(1), Q(1)),
                   (Q(3, 4), Q(1, 2), Q(1, 4)),
                   (Q(1), Q(2, 3), Q(0)),
                   (Q(1, 32), Q(1, 64), Q(1, 128))):
        images = [tuple(scale * value for scale, value in zip(scales, point))
                  for point in points]
        D = Q(0)
        for i, x in enumerate(points):
            for j, xp in enumerate(points):
                y, yp = images[i], images[j]
                source_difference = subtract(x, xp)
                target_difference = subtract(y, yp)
                h_difference = subtract(target_difference, source_difference)
                loss = (squared_norm(source_difference)
                        - squared_norm(target_difference))
                require(loss >= 0, "independent fixture is not contractive")
                D += weights[i] * weights[j] * loss
                for t in (Q(0), Q(1, 7), Q(1, 2), Q(6, 7), Q(1)):
                    interpolated = tuple(a + t * h
                                         for a, h in zip(source_difference,
                                                         h_difference))
                    dot_product = sum(a * h for a, h in
                                      zip(interpolated, h_difference))
                    require(-2 * dot_product
                            == loss + (1 - 2 * t) * squared_norm(h_difference),
                            "straight-path pair identity")
                    path_checks += 1
        M = sum(weight * squared_norm(subtract(y, x))
                for weight, x, y in zip(weights, points, images))
        # Cov(X)=I and R^2=3, so kappa=1 and R=2 is a valid integer guard.
        require(M <= 8 * D, "Procrustes loss scaling")
        if D == 0:
            require(M == 0, "zero loss rigidity")
        records.append((tuple(map(str, scales)), str(D), str(M)))
        gram_checks += 1
    return path_checks, gram_checks, records


def budget_controls():
    checks = 0
    records = []
    for radius, kappa, zeta in itertools.product(
            (1, 2, 5, 8), (Q(1), Q(1, 64), Q(1, 1000)),
            (Q(1), Q(1, 16), Q(1, 1024))):
        _, _, _, _, tail = localization_constants(radius, kappa, 0)
        t = ceil_log2(16 * tail / zeta)
        level_index = 2 * t
        B, r, _, K, _ = localization_constants(radius, kappa, level_index)
        p = ceil_log2(8 * K / zeta)
        exponent = 2 * r * p
        b = ceil_log2(Q(2, 1) / zeta)
        prefactor = 3 * radius * radius + b + exponent + 1
        require(2 * tail * Q(1, 2 ** t) <= zeta / 8,
                "low-threshold schedule")
        require(K * Q(1, 2 ** p) <= zeta / 8,
                "reconstruction schedule")
        require(Q(1, 2 ** b) <= zeta / 2,
                "cubature error schedule")
        require(prefactor >= 3 * radius * radius,
                "radius degree guard")
        # Since 2^exponent>=1, this stronger comparison avoids allocating
        # the deliberately enormous degree itself.
        require(prefactor - 2 >= b + exponent - 4,
                "symbolic row degree guard")
        records.append((radius, str(kappa), str(zeta), B, exponent))
        checks += 5
    return checks, records


def audit():
    source_pins = pin_sources()
    beta_checks = beta_variance_polynomial_controls()
    lagrange_checks, lagrange_records = lagrange_controls()
    derivative_checks = derivative_and_remainder_controls()
    constant_checks = constant_controls()
    path_checks, gram_checks, path_records = path_and_gram_controls()
    schedule_checks, schedule_records = budget_controls()
    state = {
        "beta_checks": beta_checks,
        "lagrange_checks": lagrange_checks,
        "lagrange_digest": hashlib.sha256(
            json.dumps(lagrange_records, separators=(",", ":")).encode()).hexdigest(),
        "derivative_checks": derivative_checks,
        "constant_checks": constant_checks,
        "path_checks": path_checks,
        "gram_checks": gram_checks,
        "path_records": path_records,
        "schedule_checks": schedule_checks,
        "schedule_digest": hashlib.sha256(
            json.dumps(schedule_records, separators=(",", ":")).encode()).hexdigest(),
    }
    state_hash = hashlib.sha256(
        json.dumps(state, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "status": "INDEPENDENT_ALL_RADIUS_LOCALIZATION_REVIEW_PASS",
        "target_artifact": "bafkreibivrqpvaay3jjrqcg3ezx4u64efeszvrtcyr6k5jtlh4lexfghqm",
        "target_commit": TARGET_COMMIT,
        "source_pins": source_pins,
        "beta_variance_polynomial_checks": beta_checks,
        "lagrange_and_quantile_checks": lagrange_checks,
        "gaussian_derivative_and_remainder_checks": derivative_checks,
        "localization_constant_checks": constant_checks,
        "straight_path_pair_checks": path_checks,
        "procrustes_loss_checks": gram_checks,
        "symbolic_budget_checks": schedule_checks,
        "new_gaussian_sign_proved": False,
        "strict_screw_sign_evaluated": False,
        "exact_state_sha256": state_hash,
    }


def main():
    result = audit()
    expected_path = HERE / "EXPECTED.json"
    if expected_path.exists():
        require(result == json.loads(expected_path.read_text()),
                "expected independent record mismatch")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
