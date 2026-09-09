#!/usr/bin/env python3
"""Independent arithmetic and malformed-certificate controls."""
from copy import deepcopy
from pathlib import Path
import importlib.util
import json
import random
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common  # noqa: E402

spec = importlib.util.spec_from_file_location("concurrence_verifier_controls", HERE / "verify.py")
VERIFY = importlib.util.module_from_spec(spec)
spec.loader.exec_module(VERIFY)


def determinant(matrix, prime):
    matrix = [row[:] for row in matrix]
    result = 1
    for column in range(len(matrix)):
        pivot = next((row for row in range(column, len(matrix)) if matrix[row][column] % prime), None)
        if pivot is None:
            return 0
        if pivot != column:
            matrix[pivot], matrix[column] = matrix[column], matrix[pivot]
            result = -result
        value = matrix[column][column] % prime
        result = result * value % prime
        inverse = pow(value, -1, prime)
        for row in range(column + 1, len(matrix)):
            scale = matrix[row][column] * inverse % prime
            for j in range(column, len(matrix)):
                matrix[row][j] = (matrix[row][j] - scale * matrix[column][j]) % prime
    return result % prime


def sylvester_determinant(left, right, prime):
    left = common.trim(left[:])
    right = common.trim(right[:])
    m, n = len(left) - 1, len(right) - 1
    if m < 0 or n < 0:
        return 0
    if not m:
        return pow(left[0], n, prime)
    if not n:
        return pow(right[0], m, prime)
    first = left[::-1]
    second = right[::-1]
    matrix = []
    for shift in range(n):
        matrix.append([0] * shift + first + [0] * (n - 1 - shift))
    for shift in range(m):
        matrix.append([0] * shift + second + [0] * (m - 1 - shift))
    return determinant(matrix, prime)


def reject(certificate, mutation):
    malformed = deepcopy(certificate)
    mutation(malformed)
    try:
        VERIFY.precheck_certificate(malformed)
    except (KeyError, TypeError, ValueError):
        return
    raise ValueError("malformed certificate accepted")


def main():
    prime = 1_000_003
    rng = random.Random(20260909)
    resultant_checks = 0
    for _ in range(256):
        left = [rng.randrange(prime) for _ in range(rng.randrange(1, 9))]
        right = [rng.randrange(prime) for _ in range(rng.randrange(1, 9))]
        left[-1] = left[-1] or 1
        right[-1] = right[-1] or 1
        recursive = common.resultant_value(left, right, prime)
        direct = sylvester_determinant(left, right, prime)
        if recursive not in (direct, (-direct) % prime):
            raise ValueError("resultant recurrence versus Sylvester determinant")
        resultant_checks += 1

    interpolation_checks = 0
    for degree in range(33):
        coefficients = [rng.randrange(prime) for _ in range(degree + 1)]
        values = [
            sum(coefficient * pow(value, exponent, prime) for exponent, coefficient in enumerate(coefficients)) % prime
            for value in range(degree + 1)
        ]
        if common.interpolate_consecutive(values, prime) != coefficients:
            raise ValueError("Newton interpolation control")
        interpolation_checks += 1

    curve = ((0, 0, 7), (2, 1, -5), (0, 4, 11), (3, 0, 2))
    substitution_checks = 0
    for slope in (2, 3, 4):
        for value in range(7):
            coefficients = common.evaluate_curve(curve, value, slope, prime)
            for y_value in range(7):
                via_coefficients = sum(
                    coefficient * pow(y_value, exponent, prime)
                    for exponent, coefficient in enumerate(coefficients)
                ) % prime
                x_value = value - slope * y_value
                direct = sum(
                    coefficient * pow(x_value, i, prime) * pow(y_value, j, prime)
                    for i, j, coefficient in curve
                ) % prime
                if via_coefficients != direct:
                    raise ValueError("linear projection substitution control")
                substitution_checks += 1

    certificate = json.loads((HERE / "certificate.json").read_text())
    VERIFY.precheck_certificate(certificate)
    mutations = [
        lambda item: item.__setitem__("schema", "corrupt"),
        lambda item: item["result"].__setitem__("prime", 1_000_005),
        lambda item: item["result"].__setitem__("projection_slopes", [2, 4, 3]),
        lambda item: item["result"]["primary"]["survivors"].pop(),
        lambda item: item["result"]["primary"]["gcd_degree_histogram"].__setitem__("0", 1),
        lambda item: item["result"]["secondary"][0]["survivors"].clear(),
        lambda item: item["result"].__setitem__("all_eligible_quartets_excluded", False),
    ]
    for mutation in mutations:
        reject(certificate, mutation)
    print(json.dumps({
        "status": "CONTROLS_PASSED",
        "resultant_recurrence_checks": resultant_checks,
        "interpolation_checks": interpolation_checks,
        "projection_substitution_checks": substitution_checks,
        "malformed_certificates_rejected": len(mutations),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
