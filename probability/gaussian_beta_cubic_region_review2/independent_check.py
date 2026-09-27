"""Independent exact controls for the universal cubic Gaussian beta region.

No target module is imported.  This checker derives the Appell polynomials
both from their coefficients and from the real-order differentiation
operator, checks Gamma comparisons and the one-crossing minorant, proves the
Gaussian product identity as a formal multivariate polynomial identity, and
checks the Mellin-to-beta index bridge on exact test functions.
"""

from fractions import Fraction as Q
from math import comb, factorial
import hashlib
import itertools
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TARGET_COMMIT = "45dc3e6b3d582426e3238e9529f5008450a7054d"


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


def pins():
    records = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    for record in records:
        raw = git_bytes(record["commit"], record["path"])
        require(hashlib.sha256(raw).hexdigest() == record["sha256"],
                "reviewed source drift")
    return len(records)


def trim(poly):
    poly = list(poly)
    while len(poly) > 1 and not poly[-1]:
        poly.pop()
    return poly


def add(left, right):
    out = [Q(0)] * max(len(left), len(right))
    for poly in (left, right):
        for degree, coefficient in enumerate(poly):
            out[degree] += coefficient
    return trim(out)


def scale(poly, scalar):
    return trim([scalar * coefficient for coefficient in poly])


def shift_x(poly):
    return [Q(0)] + list(poly)


def derivative(poly):
    return trim([degree * coefficient for degree, coefficient in enumerate(poly)][1:] or [Q(0)])


def value(poly, x):
    answer = Q(0)
    for coefficient in reversed(poly):
        answer = answer * x + coefficient
    return answer


def rising(a, n):
    answer = Q(1)
    for index in range(n):
        answer *= a + index
    return answer


def h_direct(k):
    coefficients = [Q(0)] * (k + 1)
    falling = Q(1)
    for ell in range(k + 1):
        if ell:
            falling *= Q(1, 2) - (ell - 1)
        coefficients[k - ell] = comb(k, ell) * (-1) ** ell * falling
    return trim(coefficients)


def h_from_real_order(previous, previous_order):
    # If (-D)^n[r^(1/2)q^r]=r^(1/2-n)q^r h_n(-r log q),
    # differentiating once more gives
    # h_(n+1)=(x+n-1/2)h_n-x h'_n.
    return add(shift_x(previous),
               add(scale(previous, Q(previous_order) - Q(1, 2)),
                   scale(shift_x(derivative(previous)), Q(-1))))


def shifted_gamma_expectation(poly, shape):
    # Coefficients in c of E[p(c+Gamma(shape,1))].
    answer = [Q(0)] * len(poly)
    for power, coefficient in enumerate(poly):
        for c_power in range(power + 1):
            answer[c_power] += (coefficient * comb(power, c_power)
                                * rising(shape, power - c_power))
    return trim(answer)


def coefficientwise_nonnegative(poly, message):
    require(all(coefficient >= 0 for coefficient in poly), message)


# Sparse multivariate polynomials in (rho,x,A,B), used for a universal
# coefficient comparison of the Gaussian product completion.
def mp_add(left, right):
    out = dict(left)
    for exponent, coefficient in right.items():
        out[exponent] = out.get(exponent, Q(0)) + coefficient
        if not out[exponent]:
            del out[exponent]
    return out


def mp_scale(poly, scalar):
    return {exponent: scalar * coefficient for exponent, coefficient in poly.items()
            if scalar * coefficient}


def mp_mul(left, right):
    out = {}
    for exponent_left, coefficient_left in left.items():
        for exponent_right, coefficient_right in right.items():
            exponent = tuple(a + b for a, b in zip(exponent_left, exponent_right))
            out[exponent] = out.get(exponent, Q(0)) + coefficient_left * coefficient_right
    return {exponent: coefficient for exponent, coefficient in out.items() if coefficient}


def gaussian_product_identity():
    rho = {(1, 0, 0, 0): Q(1)}
    x = {(0, 1, 0, 0): Q(1)}
    a = {(0, 0, 1, 0): Q(1)}
    b = {(0, 0, 0, 1): Q(1)}
    rho_x = mp_mul(rho, x)
    first = mp_add(rho_x, mp_scale(a, -1))
    second = mp_add(rho_x, mp_scale(b, -1))
    x2 = mp_mul(x, x)
    rho2_x2 = mp_mul(mp_mul(rho, rho), x2)
    # -(1-2/rho^-2)x^2/2 = -x^2/2+rho^2 x^2.
    left = mp_scale(mp_add(mp_mul(first, first), mp_mul(second, second)), Q(-1, 2))
    left = mp_add(left, mp_add(mp_scale(x2, Q(-1, 2)), rho2_x2))
    right = mp_add(mp_scale(mp_add(mp_mul(a, a), mp_mul(b, b)), Q(-1, 2)),
                   mp_scale(x2, Q(-1, 2)))
    right = mp_add(right, mp_mul(rho_x, mp_add(a, b)))
    require(left == right, "formal Gaussian product completion")
    return len(left)


def beta_bridge_controls():
    checked = 0
    for k, j, m in itertools.product(range(1, 11), range(0, 11), range(0, 4)):
        alternating = sum((Q((-1) ** ell * comb(k, ell), j + m + ell + 1)
                           for ell in range(k + 1)), Q(0))
        beta_integral = Q(factorial(j + m) * factorial(k),
                          factorial(j + m + k + 1))
        require(alternating == beta_integral > 0, "Mellin/beta index bridge")
        checked += 1
    return checked


def audit():
    pin_count = pins()
    prior = [Q(1)]
    records = []
    polynomial_orders = constant_cases = gamma_cases = 0
    for k in range(1, 33):
        direct = h_direct(k)
        differentiated = h_from_real_order(prior, k - 1)
        require(direct == differentiated, "real-order derivative polynomial")
        require(direct[-1] == 1 and all(coefficient < 0 for coefficient in direct[:-1]),
                "Appell coefficient signs")
        require(value(direct, 2 * k) >= Q((2 * k) ** k, 2),
                "positive half-leading bound")
        p_poly = [abs(coefficient) for coefficient in direct]
        g_poly = shifted_gamma_expectation(direct, Q(3))
        expected_g = [Q(comb(k, c_power)) * rising(Q(5, 2), k - c_power)
                      for c_power in range(k + 1)]
        require(g_poly == expected_g, "Gamma(3) calibration")
        raw_moment = [Q(comb(k, c_power)) * rising(Q(3), k - c_power)
                      for c_power in range(k + 1)]
        coefficientwise_nonnegative(add(scale(g_poly, k + 1), scale(raw_moment, -1)),
                                     "raw/G comparison")
        old_g = shifted_gamma_expectation(prior, Q(3))
        coefficientwise_nonnegative(add(g_poly, scale(old_g, -k)),
                                     "successive G comparison")
        expected_p = shifted_gamma_expectation(p_poly, Q(3))
        expected_p_prime = shifted_gamma_expectation(derivative(p_poly), Q(3))
        coefficientwise_nonnegative(add(scale(g_poly, 2 * k + 1), scale(expected_p, -1)),
                                     "P expectation")
        coefficientwise_nonnegative(add(scale(g_poly, 2 * k - 1),
                                         scale(expected_p_prime, -1)),
                                     "P prime expectation")
        gamma_cases += 5

        for multiplier in (1, 3):
            r = multiplier * 30720 * k ** 3
            epsilon = Q(24 * k, r)
            tau = epsilon * 32 * k
            require(tau <= Q(1, 40 * k) <= 1, "minorant size")
            require(tau * (10 * k - 1) <= Q(1, 4), "integrated minorant loss")
            require(Q(64 * k, r) <= 1 and Q(2 * k, r) <= 1,
                    "mode Taylor scale")
            require(Q(4 * k, r) <= Q(1, 2), "negative-region logarithm scale")
            correction = add(scale(derivative(p_poly), 3), scale(p_poly, 2))
            minorant = add(direct, scale(correction, -tau))
            require(minorant[-1] > 0 and all(coefficient < 0 for coefficient in minorant[:-1]),
                    "one-crossing minorant")
            expected_minorant = shifted_gamma_expectation(minorant, Q(3))
            coefficientwise_nonnegative(add(expected_minorant, scale(g_poly, Q(-3, 4))),
                                         "Gamma minorant margin")
            tail_majorant = Q(2 ** (3 - 12 * k))
            require(tail_majorant <= Q(1, 512) < Q(1, 4), "radial tail")
            constant_cases += 7
        records.append({"k": k, "h": [str(value_) for value_ in direct],
                        "G0": str(g_poly[0])})
        polynomial_orders += 1
        prior = direct

    product_terms = gaussian_product_identity()
    beta_cases = beta_bridge_controls()
    require(30720 * 8 ** 3 == 15728640, "eighth-order threshold")
    h8 = h_direct(8)
    state = {
        "h8": [str(value_) for value_ in h8],
        "G8_zero": str(shifted_gamma_expectation(h8, Q(3))[0]),
        "record_digest": hashlib.sha256(
            json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "threshold8": 30720 * 8 ** 3,
    }
    state_hash = hashlib.sha256(
        json.dumps(state, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "status": "INDEPENDENT_CUBIC_BETA_REGION_REVIEW_PASS",
        "target_commit": TARGET_COMMIT,
        "source_pins": pin_count,
        "polynomial_orders": polynomial_orders,
        "gamma_coefficient_cases": gamma_cases,
        "constant_and_minorant_cases": constant_cases,
        "formal_gaussian_product_terms": product_terms,
        "beta_bridge_cases": beta_cases,
        "eighth_order_minimum_base": 30720 * 8 ** 3,
        "eighth_order_minimum_j": 30720 * 8 ** 3 - 2,
        "h8_coefficients_ascending": [str(value_) for value_ in h8],
        "exact_state_sha256": state_hash,
        "trust_boundary": "Exact independent controls plus human universal analytic audit; not formalized",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
