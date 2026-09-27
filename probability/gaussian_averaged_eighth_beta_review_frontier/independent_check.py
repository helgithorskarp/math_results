#!/usr/bin/env python3
"""Independent exact audit of the averaged eighth-beta scalar premise.

This checker does not import the author's checker or Bernstein certificate.
It encloses the nine radicals on a different dyadic grid and proves the
resulting degree-eight rational polynomial positive by Sturm's theorem.
It also audits the variance identities and every final normalization factor.
"""

from fractions import Fraction as Q
from hashlib import sha256
from math import comb
from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parent
TARGET = ROOT.parent / "gaussian_averaged_eighth_beta"
TARGET_COMMIT = "18fd5b8a6cf732357196f3cb6e413ddf9b2c7a35"
TARGET_CONTRIBUTION = "bafkreibv2gicfcp4n4pghj6y3jb5gnmubc42zjwi7w35zpndlrqbxs4svq"
ROOT_DENOMINATOR = 1 << 20
DEGREE = 8

PINS = {
    "PROOF.md": "487084d0467d720069f34cdc73b5f5cc5355b5e56571a3b54807e85c33f2b3ff",
    "verify.py": "b47cf5fcb791dc3f820c76b38f5e9dccc20dfeb794cf983ad1aeb68a29419399",
    "EXPECTED.json": "2f632e23c22f9e9275ff289ed32c5aef56507f095b10c74ce306addff65544d0",
}


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def verify_pins():
    observed = {name: digest(TARGET / name) for name in PINS}
    require(observed == PINS, "reviewed source does not match pinned packet")
    return observed


def floor_sqrt(value):
    """Integer square root by binary search, independent of math.isqrt."""
    require(value >= 0, "square root requires a nonnegative integer")
    low, high = 0, value + 1
    while high - low > 1:
        middle = (low + high) // 2
        if middle * middle <= value:
            low = middle
        else:
            high = middle
    require(low * low <= value < (low + 1) * (low + 1), "bad integer root")
    return low


def radical_enclosures():
    roots = []
    for n in range(2, 11):
        k = floor_sqrt(n * ROOT_DENOMINATOR**2)
        lower = Q(k, ROOT_DENOMINATOR)
        upper = lower if k * k == n * ROOT_DENOMINATOR**2 else Q(k + 1, ROOT_DENOMINATOR)
        require(lower * lower <= n <= upper * upper, "bad rational enclosure")
        roots.append((lower, upper))
    return roots


def lower_polynomial(roots, constant=Q(19, 100)):
    """Lower P8(u)-[constant-4u/5+u^2/2] coefficientwise."""
    polynomial = []
    for degree, (lower, upper) in enumerate(roots):
        signed_root = lower if degree % 2 == 0 else -upper
        polynomial.append(Q(comb(DEGREE, degree)) * signed_root)
    polynomial[0] -= constant
    polynomial[1] += Q(4, 5)
    polynomial[2] -= Q(1, 2)
    return trim(polynomial)


def upper_polynomial(roots, constant):
    """Upper P8(u)-[constant-4u/5+u^2/2] coefficientwise."""
    polynomial = []
    for degree, (lower, upper) in enumerate(roots):
        signed_root = upper if degree % 2 == 0 else -lower
        polynomial.append(Q(comb(DEGREE, degree)) * signed_root)
    polynomial[0] -= constant
    polynomial[1] += Q(4, 5)
    polynomial[2] -= Q(1, 2)
    return trim(polynomial)


def trim(polynomial):
    answer = list(polynomial)
    while len(answer) > 1 and answer[-1] == 0:
        answer.pop()
    return answer


def derivative(polynomial):
    return trim([Q(i) * polynomial[i] for i in range(1, len(polynomial))] or [Q(0)])


def divide_with_remainder(dividend, divisor):
    require(divisor != [Q(0)], "division by zero polynomial")
    remainder = trim(dividend)
    quotient = [Q(0)] * max(1, len(remainder) - len(divisor) + 1)
    while remainder != [Q(0)] and len(remainder) >= len(divisor):
        shift = len(remainder) - len(divisor)
        coefficient = remainder[-1] / divisor[-1]
        quotient[shift] += coefficient
        for index, value in enumerate(divisor):
            remainder[index + shift] -= coefficient * value
        remainder = trim(remainder)
    return trim(quotient), remainder


def positive_rescale(polynomial):
    polynomial = trim(polynomial)
    if polynomial == [Q(0)]:
        return polynomial
    scale = abs(polynomial[-1])
    return [coefficient / scale for coefficient in polynomial]


def sturm_sequence(polynomial):
    sequence = [positive_rescale(polynomial), positive_rescale(derivative(polynomial))]
    while sequence[-1] != [Q(0)]:
        _, remainder = divide_with_remainder(sequence[-2], sequence[-1])
        if remainder == [Q(0)]:
            break
        sequence.append(positive_rescale([-coefficient for coefficient in remainder]))
    return sequence


def polynomial_value(polynomial, value):
    answer = Q(0)
    for coefficient in reversed(polynomial):
        answer = answer * value + coefficient
    return answer


def sign(value):
    return (value > 0) - (value < 0)


def variations(sequence, value):
    signs = [sign(polynomial_value(polynomial, value)) for polynomial in sequence]
    signs = [entry for entry in signs if entry]
    return sum(left != right for left, right in zip(signs, signs[1:]))


def sturm_audit(polynomial):
    sequence = sturm_sequence(polynomial)
    endpoint_zero = polynomial_value(polynomial, Q(0)) == 0 or polynomial_value(polynomial, Q(1)) == 0
    require(not endpoint_zero, "Sturm endpoint is a polynomial root")
    at_zero, at_one = variations(sequence, Q(0)), variations(sequence, Q(1))
    return sequence, at_zero, at_one, at_zero - at_one


def outer(vector):
    return [[left * right for right in vector] for left in vector]


def variance_matrix(count, ambient):
    return [[Q(int(i == j)) - Q(1, count) if max(i, j) < count else Q(0)
             for j in range(ambient)] for i in range(ambient)]


def check_variance_identities():
    """Check the Q3 equality and Q4 equality as quadratic forms."""
    base3, total3 = variance_matrix(2, 3), variance_matrix(3, 3)
    u3 = outer([Q(-1, 2), Q(-1, 2), Q(1)])
    for i in range(3):
        for j in range(3):
            require(total3[i][j] == base3[i][j] + Q(2, 3) * u3[i][j],
                    "Q3 identity failed")

    base4, total4 = variance_matrix(2, 4), variance_matrix(4, 4)
    u = [Q(-1, 2), Q(-1, 2), Q(1), Q(0)]
    v = [Q(-1, 2), Q(-1, 2), Q(0), Q(1)]
    uu, vv = outer(u), outer(v)
    uv = outer([left + right for left, right in zip(u, v)])
    for i in range(4):
        for j in range(4):
            require(total4[i][j] == base4[i][j] + uu[i][j] + vv[i][j] - uv[i][j] / 4,
                    "Q4 identity failed")
    return 3 * 3 + 4 * 4


def check_normalizations():
    """Audit replica, lift, moment, cubic, and d2 conversion constants."""
    for m in range(2, 11):
        pair_derivative = Q(comb(m, 2), 2 * m)
        require(pair_derivative == Q(m - 1, 4), "replica pair factor failed")
        require(pair_derivative / Q(m * (m - 1)) == Q(1, 4 * m),
                "a_j normalization failed")
        eta_coefficient = Q(1, m**3)
        squared_a_coefficient = Q(1, m**5)
        require(squared_a_coefficient == Q(m) * eta_coefficient**2,
                "lift square-root factor failed")

    eta_coefficients = [Q(19, 100), -Q(4, 5), Q(1, 2)]
    b_coefficients = [coefficient / Q((index + 2)**3)
                      for index, coefficient in enumerate(eta_coefficients)]
    require(b_coefficients == [Q(19, 800), -Q(4, 135), Q(1, 128)],
            "eta-to-B conversion failed")

    h_at_one = sum(b_coefficients, Q(0))
    derivative_upper = -Q(4, 135) + Q(3, 128)
    require(h_at_one == Q(167, 86400), "h(1) failed")
    require(derivative_upper == -Q(107, 17280) < 0, "monotonicity failed")
    b80_over_b2_s = Q(9, 4) * h_at_one
    require(b80_over_b2_s == Q(167, 38400), "b80 normalization failed")
    require(8 * b80_over_b2_s == Q(167, 4800), "d2 normalization failed")
    return b_coefficients, h_at_one, derivative_upper, b80_over_b2_s


def certificate():
    pins = verify_pins()
    roots = radical_enclosures()
    polynomial = lower_polynomial(roots)
    sequence, at_zero, at_one, root_count = sturm_audit(polynomial)
    require(root_count == 0, "lower polynomial has a root in (0,1)")
    require(polynomial_value(polynomial, Q(0)) > 0, "lower polynomial not positive")

    # Damage control: raising 19/100 to 39/200 is rigorously false because an
    # upper enclosure is negative at 3/10.  The corresponding lower
    # polynomial also has two Sturm-detected crossings.
    damaged_lower = lower_polynomial(roots, Q(39, 200))
    damaged_upper = upper_polynomial(roots, Q(39, 200))
    damaged_sequence, damaged_zero, damaged_one, damaged_roots = sturm_audit(damaged_lower)
    damaged_upper_value = polynomial_value(damaged_upper, Q(3, 10))
    require(damaged_upper_value < 0 and damaged_roots == 2,
            "false strengthened claim accepted")

    b_coefficients, h_at_one, derivative_upper, b80_over_b2_s = check_normalizations()
    canonical = json.dumps([str(value) for value in polynomial], separators=(",", ":")).encode()
    return {
        "status": "AVERAGED_EIGHTH_BETA_INDEPENDENT_ACCEPT",
        "target_commit": TARGET_COMMIT,
        "target_contribution": TARGET_CONTRIBUTION,
        "pinned_sha256": pins,
        "arithmetic": "Python integers and Fraction only; no floating point",
        "method": "dyadic radical enclosures plus exact Sturm root count",
        "root_denominator": ROOT_DENOMINATOR,
        "root_enclosures": [
            {"n": n, "lower": str(lower), "upper": str(upper)}
            for n, (lower, upper) in enumerate(roots, start=2)
        ],
        "lower_polynomial_sha256": sha256(canonical).hexdigest(),
        "lower_power_coefficients": [str(value) for value in polynomial],
        "sturm_degrees": [len(entry) - 1 for entry in sequence],
        "variations_at_0": at_zero,
        "variations_at_1": at_one,
        "roots_in_open_unit_interval": root_count,
        "lower_value_at_0": str(polynomial_value(polynomial, Q(0))),
        "lower_value_at_1": str(polynomial_value(polynomial, Q(1))),
        "damaged_constant": "39/200",
        "damaged_upper_value_at_3_over_10": str(damaged_upper_value),
        "damaged_sturm_degrees": [len(entry) - 1 for entry in damaged_sequence],
        "damaged_variations_at_0": damaged_zero,
        "damaged_variations_at_1": damaged_one,
        "damaged_roots_in_open_unit_interval": damaged_roots,
        "variance_matrix_entries_checked": check_variance_identities(),
        "B2_B3_B4_coefficients": [str(value) for value in b_coefficients],
        "h_at_one": str(h_at_one),
        "h_derivative_upper": str(derivative_upper),
        "b80_coefficient_of_B2_over_s": str(b80_over_b2_s),
        "b80_coefficient_of_sqrt2_d2": "167/4800",
        "full_majorisation_proved": False,
    }


def main():
    require(sys.argv[1:] in ([], ["--emit"]),
            "usage: python3 independent_check.py [--emit]")
    result = certificate()
    if sys.argv[1:] == ["--emit"]:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    expected = json.loads((ROOT / "REVIEW_EXPECTED.json").read_text())
    require(result == expected, "review evidence differs from REVIEW_EXPECTED.json")
    print(json.dumps({
        "status": result["status"],
        "sturm_degrees": result["sturm_degrees"],
        "roots_in_open_unit_interval": result["roots_in_open_unit_interval"],
        "damaged_roots_detected": result["damaged_roots_in_open_unit_interval"],
        "accepted_bound": "b_(8,0) >= 167*sqrt(2)*d_2/4800",
        "full_majorisation_proved": False,
    }, indent=2))


if __name__ == "__main__":
    main()
