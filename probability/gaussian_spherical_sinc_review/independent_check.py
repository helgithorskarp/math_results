#!/usr/bin/env python3
"""Independent exact checks for the spherical sinc comparison.

No target module or target expected record is imported.  The principal
identity is checked on genuinely multivariate polynomials by applying exact
constant-coefficient differential operators.  The Duhamel kernel is
integrated by expanding (t-r)^m and integrating monomials, independently of
the author's scalar affine-form moment implementation.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import comb, factorial
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_inputs():
    manifest = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    for relative, expected in manifest["files"].items():
        actual = sha256((HERE / relative).read_bytes()).hexdigest()
        require(actual == expected, f"input drift: {relative}")
    return len(manifest["files"])


def clean(poly):
    return {exponent: coefficient for exponent, coefficient in poly.items()
            if coefficient}


def add(left, right):
    answer = dict(left)
    for exponent, coefficient in right.items():
        answer[exponent] = answer.get(exponent, F(0)) + coefficient
    return clean(answer)


def scale(coefficient, poly):
    return clean({exponent: coefficient * value
                  for exponent, value in poly.items()})


def subtract(left, right):
    return add(left, scale(F(-1), right))


def directional_derivative(poly, direction):
    answer = {}
    for exponent, coefficient in poly.items():
        for index, power in enumerate(exponent):
            if power and direction[index]:
                lowered = list(exponent)
                lowered[index] -= 1
                lowered = tuple(lowered)
                answer[lowered] = (answer.get(lowered, F(0))
                                   + coefficient * power * direction[index])
    return clean(answer)


def delta_operator(poly, sites):
    """Apply sum over the three column-direction second derivatives."""
    if not sites:
        return {}
    dimensions = len(sites[0])
    answer = {}
    for coordinate in range(dimensions):
        direction = tuple(row[coordinate] for row in sites)
        term = directional_derivative(
            directional_derivative(poly, direction), direction)
        answer = add(answer, term)
    return answer


def operator_power(poly, sites, power):
    answer = poly
    for _ in range(power):
        answer = delta_operator(answer, sites)
        if not answer:
            break
    return answer


def spherical_mean(poly, sites, time, wrong_dimension=False):
    """Finite operator series for an S2 mean (or a corrupt S1 control)."""
    answer = {}
    current = poly
    order = 0
    while current:
        if wrong_dimension:
            coefficient = time ** (2 * order) / (4 ** order * factorial(order) ** 2)
        else:
            coefficient = time ** (2 * order) / factorial(2 * order + 1)
        answer = add(answer, scale(coefficient, current))
        current = delta_operator(current, sites)
        order += 1
    return answer


def integrate_power_product(left_power, right_power, time):
    """Directly integrate (t-r)^left_power r^right_power on [0,t]."""
    answer = F(0)
    for index in range(left_power + 1):
        answer += ((-1) ** index * comb(left_power, index)
                   * time ** (left_power - index)
                   * time ** (right_power + index + 1)
                   / F(right_power + index + 1))
    return answer


def duhamel_rhs(poly, source, target, time, kernel=True):
    base = subtract(delta_operator(poly, source),
                    delta_operator(poly, target))
    answer = {}
    degree = max((sum(exponent) for exponent in poly), default=0)
    maximum = max(0, (degree - 2) // 2)
    for source_power in range(maximum + 1):
        for target_power in range(maximum + 1 - source_power):
            term = operator_power(
                operator_power(base, target, target_power),
                source, source_power)
            if not term:
                continue
            extra = 1 if kernel else 0
            integral = integrate_power_product(
                2 * source_power + extra,
                2 * target_power + extra,
                time) / time
            coefficient = integral / (
                factorial(2 * source_power + 1)
                * factorial(2 * target_power + 1))
            answer = add(answer, scale(coefficient, term))
    return answer


def polynomial(variable_count, terms):
    answer = {}
    for coefficient, exponent in terms:
        require(len(exponent) == variable_count, "bad polynomial arity")
        answer[tuple(exponent)] = answer.get(tuple(exponent), F(0)) + F(coefficient)
    return clean(answer)


def operator_identity_controls():
    cases = []
    source3 = [(F(1), F(0), F(2)), (F(-1), F(2), F(1)),
               (F(2), F(1), F(-1))]
    target3 = [(F(1, 2), F(0), F(1)), (F(-1, 2), F(1), F(1, 2)),
               (F(1), F(1, 2), F(-1, 2))]
    phi3 = polynomial(3, [
        (F(2, 3), (7, 0, 0)), (F(-5, 7), (2, 3, 1)),
        (F(11, 9), (0, 4, 2)), (F(3, 5), (1, 1, 1)),
        (F(-4, 11), (0, 0, 5)), (F(7, 13), (2, 0, 0)),
        (F(9, 17), (0, 0, 0))])
    cases.extend([(phi3, source3, target3, F(2, 3)),
                  (phi3, target3, source3, F(5, 4)),
                  (phi3, source3, source3, F(7, 5)),
                  (phi3, source3, [(F(0),) * 3] * 3, F(3, 2))])

    source4 = [(F(0), F(1), F(-1)), (F(2), F(0), F(1)),
               (F(-1), F(3), F(0)), (F(1), F(-2), F(2))]
    target4 = [(F(0), F(1, 2), F(-1, 3)), (F(1), F(0), F(1, 3)),
               (F(-1, 2), F(3, 2), F(0)), (F(1, 2), F(-1), F(2, 3))]
    phi4 = polynomial(4, [
        (F(1), (2, 2, 2, 2)), (F(-3, 4), (5, 1, 0, 0)),
        (F(5, 6), (0, 3, 1, 2)), (F(7, 8), (1, 0, 4, 1)),
        (F(-2, 9), (0, 0, 0, 6)), (F(11, 10), (1, 1, 1, 0))])
    cases.extend([(phi4, source4, target4, F(4, 5)),
                  (phi4, target4, source4, F(6, 7)),
                  (phi4, [(F(0),) * 3] * 4, target4, F(9, 8)),
                  (phi4, source4, source4, F(11, 9))])

    coefficient_checks = 0
    for poly, source, target, time in cases:
        left = subtract(spherical_mean(poly, source, time),
                        spherical_mean(poly, target, time))
        right = duhamel_rhs(poly, source, target, time)
        require(left == right, "multivariate Duhamel identity")
        coefficient_checks += len(set(left) | set(right))

    selected = cases[0]
    poly, source, target, time = selected
    left = subtract(spherical_mean(poly, source, time),
                    spherical_mean(poly, target, time))
    right = duhamel_rhs(poly, source, target, time)
    require(left != scale(F(-1), right), "reversed sign accepted")
    require(left != duhamel_rhs(poly, source, target, time, kernel=False),
            "missing kernel accepted")
    wrong_left = subtract(spherical_mean(poly, source, time, True),
                          spherical_mean(poly, target, time, True))
    require(wrong_left != right, "wrong sphere dimension accepted")
    require(left != duhamel_rhs(poly, target, source, time),
            "swapped operator order accepted")
    return len(cases), coefficient_checks


def dot(left, right):
    return sum((a * b for a, b in zip(left, right)), F(0))


def subtract_vector(left, right):
    return tuple(a - b for a, b in zip(left, right))


def squared_norm(vector):
    return dot(vector, vector)


def pair_losses(source, target):
    answer = {}
    for i in range(len(source)):
        for j in range(i + 1, len(source)):
            loss = (squared_norm(subtract_vector(source[i], source[j]))
                    - squared_norm(subtract_vector(target[i], target[j])))
            require(loss >= 0, "fixture is not a contraction")
            answer[i, j] = loss
    return answer


def posterior_identity(source, target, posterior):
    count = len(source)
    require(sum(posterior) == 1 and all(value > 0 for value in posterior),
            "invalid posterior")
    hessian = [[((posterior[i] if i == j else F(0))
                 - posterior[i] * posterior[j])
                for j in range(count)] for i in range(count)]
    require(all(sum(row) == 0 for row in hessian), "Hessian row sum")
    require(all(hessian[i][j] < 0 for i in range(count)
                for j in range(count) if i != j), "off-diagonal sign")
    gram = F(0)
    for i in range(count):
        for j in range(count):
            gram += (dot(source[i], source[j]) - dot(target[i], target[j])) \
                    * hessian[i][j]
    losses = pair_losses(source, target)
    pair = sum((loss * posterior[i] * posterior[j]
                for (i, j), loss in losses.items()), F(0))
    require(gram == pair, "Gram-to-pair-loss identity")
    return pair


def transform(points, diagonal, permutation=(0, 1, 2)):
    return [tuple(diagonal[index] * point[permutation[index]]
                  for index in range(3)) for point in points]


def hessian_and_gibbs_controls():
    source = [(F(0), F(0), F(0)), (F(1), F(0), F(0)),
              (F(0), F(2), F(0)), (F(1), F(1), F(3)),
              (F(-2), F(1), F(1))]
    targets = [
        transform(source, (F(1, 2), F(2, 3), F(3, 4))),
        transform(source, (F(3, 5), F(1, 3), F(0)), (1, 0, 2)),
        [(F(0), F(0), F(0)) for _ in source],
    ]
    numerators = [[1, 1, 1, 1, 1], [1, 2, 3, 4, 5],
                  [2, 7, 1, 8, 2], [9, 1, 4, 1, 6]]
    posterior_controls = 0
    translation_controls = 0
    for target, nums in product(targets, numerators):
        posterior = [F(value, sum(nums)) for value in nums]
        value = posterior_identity(source, target, posterior)
        require(value > 0, "strict fixture lost")
        translated_source = [tuple(x + shift for x, shift in zip(point, (2, -3, 1)))
                             for point in source]
        translated_target = [tuple(x + shift for x, shift in zip(point, (-1, 4, 2)))
                             for point in target]
        require(posterior_identity(translated_source, translated_target,
                                   posterior) == value,
                "independent translation changed the sign identity")
        posterior_controls += 1
        translation_controls += 1

    likelihoods = [
        [F(1), F(2), F(1, 2), F(3), F(2, 3)],
        [F(1, 3), F(3, 2), F(4, 3), F(2), F(5, 2)],
        [F(3), F(1, 3), F(1), F(3, 4), F(7, 3)],
    ]
    lower, upper = F(1, 3), F(3)
    gibbs_controls = 0
    for target, factors in product(targets, likelihoods):
        weights = [F(value, 15) for value in [1, 2, 3, 4, 5]]
        normalizer = sum((weight * factor
                          for weight, factor in zip(weights, factors)), F(0))
        posterior = [weight * factor / normalizer
                     for weight, factor in zip(weights, factors)]
        posterior_pair = posterior_identity(source, target, posterior)
        base_pair = posterior_identity(source, target, weights)
        require(posterior_pair >= (lower / upper) ** 2 * base_pair,
                "Gibbs lower bound")
        mean_loss = 2 * base_pair
        require(F(1, 6) * (lower / upper) ** 2 * base_pair
                == (lower / upper) ** 2 * mean_loss / 12,
                "D/12 normalization")
        gibbs_controls += 1
    return posterior_controls, translation_controls, gibbs_controls


def endpoint_constant_controls():
    require(F(1, 2) * F(1, 6) == F(1, 12), "ordered-pair factor")
    require(F(1, 4) * F(1, 12) == F(1, 48), "compact-ray factor")
    require(44 * 96 == 4224, "strict-Lipschitz endpoint constant")
    require(F(9, 64) - F(1, 8) == F(1, 64), "threshold overlap")
    monotonicity = 0
    for radius in [F(1, 2), F(1), F(5, 3)]:
        lambda_zero = F(1, 2) / radius
        for multiplier in [F(1), F(3, 2), F(2), F(7, 2)]:
            parameter = multiplier * lambda_zero
            require(F(2) / parameter - 4 * radius <= 0,
                    "compact-ray exponential bound is not decreasing")
            monotonicity += 1
    return monotonicity


def run():
    pinned = pin_inputs()
    identity_cases, coefficient_checks = operator_identity_controls()
    posterior, translations, gibbs = hessian_and_gibbs_controls()
    monotonicity = endpoint_constant_controls()
    result = {
        "status": "INDEPENDENT_SPHERICAL_SINC_ACCEPT",
        "target_commit": "9c50ebb1b3543cd5c1886ba45f6f782ce2481853",
        "pinned_inputs": pinned,
        "operator_identity_cases": identity_cases,
        "polynomial_coefficients_checked": coefficient_checks,
        "posterior_hessian_controls": posterior,
        "independent_translation_controls": translations,
        "gibbs_lower_bound_controls": gibbs,
        "endpoint_monotonicity_controls": monotonicity,
        "rejected_corruptions": 4,
        "all_variance_majorisation_proved": False,
        "historical_priority_established": False,
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["record_sha256"] = sha256(canonical.encode()).hexdigest()
    return result


def main():
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
