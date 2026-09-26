#!/usr/bin/env python3
"""Independent exact audit of the square-root Gaussian degree budget.

No submitted module or expected output is imported.  The checker reconstructs
the genuine Bernstein--Durrmeyer kernel in a polynomial basis different from
the submitted implementation, verifies its endpoint atoms and beta-row
indexing, and audits the degree/error schedules with arbitrary-precision
integers and Fractions.  The universal modulus remains an analytic argument,
documented in REVIEW.md rather than inferred from these finite checks.
"""

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from math import comb, factorial
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def poly_add(left, right):
    out = [Q(0)] * max(len(left), len(right))
    for i, value in enumerate(left):
        out[i] += value
    for i, value in enumerate(right):
        out[i] += value
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_scale(poly, scalar):
    return [scalar * value for value in poly]


def binomial_weight_polynomial(n, j):
    """Power-basis coefficients of binom(n,j) u^j (1-u)^(n-j)."""
    out = [Q(0)] * (n + 1)
    for ell in range(n - j + 1):
        out[j + ell] = Q(comb(n, j) * comb(n - j, ell) * (-1) ** ell)
    return out


def beta_moment(a, b, power):
    """Moment of Beta(a,b), with (0,b) and (a,0) used as endpoint atoms."""
    require(a >= 0 and b >= 0 and a + b >= 2 and power >= 0, "beta moment inputs")
    if power == 0:
        return Q(1)
    if a == 0:
        return Q(0)
    if b == 0:
        return Q(1)
    value = Q(1)
    for q in range(power):
        value *= Q(a + q, a + b + q)
    return value


def beta_root_product(a, b):
    require(a >= 0 and b >= 0 and a + b >= 2, "beta root inputs")
    if a == 0:
        return Q(0)
    if b == 0:
        return Q(1)
    value = Q(1)
    for q in range(b):
        value *= Q(2 * (a + q), 2 * (a + q) + 1)
    return value


def beta_root_expanded_density(a, b):
    require(a >= 1 and b >= 1, "interior beta density")
    normalizer = Q(factorial(a + b - 1), factorial(a - 1) * factorial(b - 1))
    return normalizer * sum(
        (-1) ** q * comb(b - 1, q) * Q(2, 2 * a + 2 * q + 1)
        for q in range(b)
    )


def kernel_values(n, u, omit_endpoints=False):
    """Mass, first two moments, and E sqrt(V) for the genuine kernel."""
    mass = mean = second = root = Q(0)
    for j in range(n + 1):
        if omit_endpoints and j in (0, n):
            continue
        weight = Q(comb(n, j)) * u ** j * (1 - u) ** (n - j)
        mass += weight
        mean += weight * beta_moment(j, n - j, 1)
        second += weight * beta_moment(j, n - j, 2)
        root += weight * beta_root_product(j, n - j)
    return mass, mean, second, root


def polynomial_kernel_audit(max_degree):
    """Prove the kernel moment identities coefficient by coefficient."""
    coefficient_checks = 0
    stream = sha256()
    for degree in range(max_degree + 1):
        n = degree + 2
        mass = [Q(0)]
        mean = [Q(0)]
        second = [Q(0)]
        for j in range(n + 1):
            weight = binomial_weight_polynomial(n, j)
            mass = poly_add(mass, weight)
            mean = poly_add(mean, poly_scale(weight, Q(j, n)))
            second = poly_add(second, poly_scale(weight, Q(j * (j + 1), n * (n + 1))))
        target_second = [Q(0), Q(2, n + 1), Q(n - 1, n + 1)]
        require(mass == [Q(1)], "symbolic kernel mass")
        require(mean == [Q(0), Q(1)], "symbolic kernel mean")
        require(second == target_second, "symbolic kernel second moment")
        coefficient_checks += len(mass) + len(mean) + len(second)
        stream.update((f"{degree}:" + ":".join(
            ",".join(map(str, poly)) for poly in (mass, mean, second)
        ) + "\n").encode())
    return coefficient_checks, stream.hexdigest()


def test_hinge(value):
    """An endpoint-zero polynomial used only to check beta-row indexing."""
    return value * (1 - value) * (3 * value - 1)


def beta_test_hinge(a, b):
    # H(v)=-v+4v^2-3v^3.
    return (-beta_moment(a, b, 1)
            + 4 * beta_moment(a, b, 2)
            - 3 * beta_moment(a, b, 3))


def audit():
    # Exact rational forms of the elementary analytic constant checks.
    require(Q(2, 3) < Q(25, 36), "sqrt(2/pi)/3 coefficient from pi>3")
    require(sum(Q(1, factorial(j)) for j in range(5)) > Q(8, 3), "e>8/3")
    require(Q(100, 81) * 6 ** 3 / Q(8, 3) ** 3 == Q(225, 16),
            "calculus maximum envelope")
    require(80 < 81, "radius constant")
    require(Q(11, 4) + Q(27, 64) == Q(203, 64), "compact composition")
    require(Q(11, 4) + Q(27, 64) + Q(161, 256) == Q(973, 256),
            "rational composition")
    require(Q(1, 2) + Q(973, 2048) == Q(1997, 2048) < 1,
            "epsilon handoff")

    symbolic_checks, symbolic_hash = polynomial_kernel_audit(128)

    root_identity_checks = 0
    risk_checks = 0
    endpoint_omission_checks = 0
    beta_row_checks = 0
    sample_t = tuple(Q(j, 32) for j in range(33))
    for degree in range(65):
        n = degree + 2
        for j in range(1, n):
            require(beta_root_product(j, n - j)
                    == beta_root_expanded_density(j, n - j),
                    "beta root representations")
            root_identity_checks += 1
        for t in sample_t:
            u = t * t
            mass, mean, second, root = kernel_values(n, u)
            require(mass == 1 and mean == u, "numeric kernel mass or mean")
            require(second - u * u == Q(2, n + 1) * u * (1 - u),
                    "numeric kernel variance")
            risk = mean + u - 2 * t * root
            require(0 <= risk <= Q(2, n + 1), "square-root risk")
            risk_checks += 1
        omitted_mass = kernel_values(n, Q(1, 4), omit_endpoints=True)[0]
        require(omitted_mass < 1, "endpoint deletion did not lose mass")
        endpoint_omission_checks += 1

    # Reconstruct the exact beta-row mixture for an unrelated endpoint-zero H.
    for degree in range(33):
        n = degree + 2
        row = [beta_test_hinge(j + 1, degree - j + 1)
               for j in range(degree + 1)]
        for u in (Q(0), Q(1, 11), Q(2, 7), Q(1, 2), Q(5, 6), Q(1)):
            mixture = sum(Q(comb(n, j)) * u ** j * (1 - u) ** (n - j)
                          * row[j - 1] for j in range(1, n))
            direct = sum(Q(comb(n, j)) * u ** j * (1 - u) ** (n - j)
                         * beta_test_hinge(j, n - j) for j in range(n + 1))
            require(mixture == direct, "beta-row shift or endpoint handling")
            if u in (Q(0), Q(1)):
                require(direct == test_hinge(u) == 0, "kernel endpoint")
            beta_row_checks += 1

    # The universal k schedule is integer arithmetic after the analytic bound.
    budget_stream = sha256()
    improved = 0
    maximum_k = 10000
    for k in range(1, maximum_k + 1):
        degree = 2048 * k ** 5 - 3
        largest_power = degree + 2
        old_largest_power = 65536 * k ** 8
        require(degree >= 0 and degree + 3 == 2048 * k ** 5, "degree schedule")
        require(largest_power * 32 * k ** 3 < old_largest_power,
                "strict degree improvement")
        require(Q(27, 64 * k) + Q(11, 4 * k) == Q(203, 64 * k),
                "per-k compact error")
        require(Q(203, 64 * k) + Q(161, 256 * k) == Q(973, 256 * k),
                "per-k rational error")
        improved += 1
        budget_stream.update(
            f"{k}:{degree}:{largest_power}:{old_largest_power}:{Q(973,256*k)}\n".encode()
        )

    result = {
        "status": "INDEPENDENT_SQUARE_ROOT_BUDGET_REVIEW_PASS",
        "imports_submitted_code_or_expected_output": False,
        "symbolic_kernel_degrees": [0, 128],
        "symbolic_kernel_coefficient_checks": symbolic_checks,
        "symbolic_kernel_stream_sha256": symbolic_hash,
        "beta_root_identity_checks": root_identity_checks,
        "square_root_risk_checks": risk_checks,
        "endpoint_omission_failures_detected": endpoint_omission_checks,
        "beta_row_mixture_checks": beta_row_checks,
        "budget_k_range": [1, maximum_k],
        "strict_degree_improvements": improved,
        "budget_stream_sha256": budget_stream.hexdigest(),
    }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    encoded = json.dumps(audit(), indent=2, sort_keys=True) + "\n"
    if args.check:
        expected = Path(__file__).with_name("EXPECTED.json").read_text()
        require(encoded == expected, "review expected-output mismatch")
    print(encoded, end="")


if __name__ == "__main__":
    main()
