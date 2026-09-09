#!/usr/bin/env python3
"""Independent certificate checker for the h4139 unit-circle theorem.

The submitted certificate is treated only as a declarative factor witness.
This checker imports no target module, reconstructs physical events directly,
ignores the submitted colour assignments, searches all normalized F3-linear
words, and proves the chosen exclusions at split primes disjoint from those
used by the target checker.
"""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from math import isqrt
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_CERTIFICATE = ROOT.parent / "hadwiger_nelson_radix_unit_circle" / "certificate.json"
ZERO = (0, 0)
ONE = (1, 0)
OMEGA = (0, 1)
DIGITS = (ZERO, ONE, OMEGA)
LABELS = tuple(product(range(3), repeat=5))
TARGET_MODULAR_PRIMES = {7, 13, 19}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def e_add(left, right):
    return left[0] + right[0], left[1] + right[1]


def e_neg(value):
    return -value[0], -value[1]


def e_mul(left, right):
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c + b * d


def e_conjugate(value):
    a, b = value
    return a + b, -b


def e_norm(value):
    product_value = e_mul(value, e_conjugate(value))
    require(product_value[1] == 0, "Eisenstein norm did not land in Z")
    return product_value[0]


def trim_e(poly):
    poly = tuple(poly)
    while poly and poly[-1] == ZERO:
        poly = poly[:-1]
    return poly


def e_poly_mul(left, right):
    if not left or not right:
        return ()
    result = [ZERO] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = e_add(result[i + j], e_mul(a, b))
    return trim_e(result)


def e_poly_remainder(dividend, monic_divisor):
    dividend = list(trim_e(dividend))
    divisor = trim_e(monic_divisor)
    require(divisor and divisor[-1] == ONE, "monic Eisenstein divisor required")
    while len(dividend) >= len(divisor):
        coefficient = dividend[-1]
        shift = len(dividend) - len(divisor)
        for j, value in enumerate(divisor):
            dividend[shift + j] = e_add(
                dividend[shift + j], e_neg(e_mul(coefficient, value))
            )
        dividend = list(trim_e(dividend))
    return tuple(dividend)


def flatten(poly):
    return tuple(coordinate for value in poly for coordinate in value)


def unflatten(row):
    require(isinstance(row, list) and len(row) % 2 == 0, "malformed flat polynomial")
    require(all(type(value) is int for value in row), "nonintegral coefficient")
    return tuple(zip(row[::2], row[1::2]))


def digest(value):
    payload = json.dumps(value, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def physical_event(left_label, right_label):
    """Build z^n(|P(z)|^2-1) as a Laurent dictionary, then normalize."""
    differences = [
        e_add(DIGITS[a], e_neg(DIGITS[b]))
        for a, b in zip(left_label, right_label)
    ]
    support = [j for j, value in enumerate(differences) if value != ZERO]
    require(support, "equal labels")
    low, high = support[0], support[-1]
    if low == high:
        require(e_norm(differences[low]) == 1, "monomial difference is not a unit")
        return ()

    trimmed = differences[low : high + 1]
    half_degree = len(trimmed) - 1
    laurent = defaultdict(lambda: ZERO)
    for i, left in enumerate(trimmed):
        for j, right in enumerate(trimmed):
            exponent = i - j
            laurent[exponent] = e_add(laurent[exponent], e_mul(left, e_conjugate(right)))
    laurent[0] = e_add(laurent[0], (-1, 0))
    polynomial = tuple(laurent[exponent] for exponent in range(-half_degree, half_degree + 1))
    require(polynomial[0] != ZERO and polynomial[-1] != ZERO, "event degree dropped")
    leading = polynomial[-1]
    require(e_norm(leading) == 1, "event leading coefficient is not a unit")
    normalized = tuple(e_mul(value, e_conjugate(leading)) for value in polynomial)
    require(normalized[-1] == ONE, "event normalization failed")
    return normalized


def reconstruct_events():
    by_event = defaultdict(list)
    for left_index, right_index in combinations(range(len(LABELS)), 2):
        event = physical_event(LABELS[left_index], LABELS[right_index])
        by_event[event].append((left_index, right_index))
    require(sum(len(pairs) for pairs in by_event.values()) == 29403, "label-pair coverage")
    require(len(by_event[()]) == 1215, "universal edge count")
    events = sorted(event for event in by_event if event)
    require(len(events) == 1272, "event count")
    require(
        Counter(2 * (len(event) - 1) // 2 for event in events)
        == {2: 6, 4: 27, 6: 168, 8: 1071},
        "event degree histogram",
    )
    return events, by_event


def is_prime(value):
    return value >= 2 and all(value % divisor for divisor in range(2, isqrt(value) + 1))


def independent_split_primes(count=12):
    result = []
    candidate = 211
    while len(result) < count:
        if is_prime(candidate) and candidate % 3 == 1 and candidate not in TARGET_MODULAR_PRIMES:
            roots = [r for r in range(candidate) if (r * r - r + 1) % candidate == 0]
            require(len(roots) == 2, "split-prime root count")
            # The target always chooses the first root. Use the conjugate root.
            result.append((candidate, roots[-1]))
        candidate += 1
    require(not ({prime for prime, _ in result} & TARGET_MODULAR_PRIMES), "prime sets overlap")
    return result


def trim_mod(poly, prime):
    poly = [value % prime for value in poly]
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def modular_remainder(dividend, divisor, prime):
    dividend = trim_mod(dividend, prime)
    divisor = trim_mod(divisor, prime)
    require(divisor, "zero modular divisor")
    inverse_lead = pow(divisor[-1], -1, prime)
    while len(dividend) >= len(divisor):
        scale = dividend[-1] * inverse_lead % prime
        shift = len(dividend) - len(divisor)
        for j, value in enumerate(divisor):
            dividend[shift + j] = (dividend[shift + j] - scale * value) % prime
        dividend = trim_mod(dividend, prime)
    return dividend


def modular_gcd(left, right, prime):
    left = trim_mod(left, prime)
    right = trim_mod(right, prime)
    while right:
        left, right = right, modular_remainder(left, right, prime)
    return left


def modular_multiply(left, right, modulus, prime):
    raw = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            raw[i + j] = (raw[i + j] + a * b) % prime
    return modular_remainder(raw, modulus, prime)


def modular_power(base, exponent, modulus, prime):
    result = [1]
    while exponent:
        if exponent & 1:
            result = modular_multiply(result, base, modulus, prime)
        base = modular_multiply(base, base, modulus, prime)
        exponent //= 2
    return trim_mod(result, prime)


def reduce_e_poly(poly, prime, omega_image):
    return [(a + b * omega_image) % prime for a, b in poly]


def normalized_colour_words():
    return [(1,) + tail for tail in product((1, 2), repeat=4)]


def label_colours(weights):
    return tuple(sum(weight * digit for weight, digit in zip(weights, label)) % 3 for label in LABELS)


def bad_event_sets(events, by_event):
    result = {}
    for weights in normalized_colour_words():
        colours = label_colours(weights)
        require(
            all(colours[left] != colours[right] for left, right in by_event[()]),
            "word fails on a universal edge",
        )
        result[weights] = {
            index
            for index, event in enumerate(events)
            if any(colours[left] == colours[right] for left, right in by_event[event])
        }
    return result


def verify_factor_witness(certificate, events):
    require(certificate.get("schema") == "hn-radix-unit-circle-v1", "certificate schema")
    factors = [unflatten(row) for row in certificate["factors"]]
    require(len(factors) == 820 and len(set(factors)) == 820, "factor census")
    require(factors == sorted(factors), "factor ordering")
    require(all(factor[-1] == ONE and 2 <= len(factor) <= 9 for factor in factors), "factor shape")
    factorizations = certificate["factorizations"]
    require(len(factorizations) == len(events), "factorization coverage")
    active = [set() for _ in factors]
    for event_index, (event, part) in enumerate(zip(events, factorizations)):
        require(part, "empty product witness")
        product_value = (ONE,)
        for factor_index, exponent in part:
            require(0 <= factor_index < len(factors) and 1 <= exponent <= 8, "factor reference")
            active[factor_index].add(event_index)
            for _ in range(exponent):
                product_value = e_poly_mul(product_value, factors[factor_index])
        require(product_value == event, "factor product identity")
    require(all(active), "unused factor")
    return factors, active


def independent_colour_cover(factors, active, events, bad):
    prime_maps = independent_split_primes()
    event_reductions = {
        (prime, omega_image): [
            reduce_e_poly(event, prime, omega_image) for event in events
        ]
        for prime, omega_image in prime_maps
    }
    pair_witness_cache = {}
    witness_histogram = Counter()
    assignments = []
    low_degree = 0

    def witness(factor_index, event_index):
        key = factor_index, event_index
        if key in pair_witness_cache:
            return pair_witness_cache[key]
        factor = factors[factor_index]
        for prime, omega_image in prime_maps:
            reduced_factor = reduce_e_poly(factor, prime, omega_image)
            reduced_event = event_reductions[(prime, omega_image)][event_index]
            if len(modular_gcd(reduced_factor, reduced_event, prime)) == 1:
                pair_witness_cache[key] = prime
                return prime
        pair_witness_cache[key] = None
        return None

    for factor_index, factor in enumerate(factors):
        degree = len(factor) - 1
        if degree <= 4:
            low_degree += 1
            assignments.append(None)
            continue
        chosen = None
        for weights in normalized_colour_words():
            bad_events = bad[weights]
            if active[factor_index] & bad_events:
                continue
            local_witnesses = []
            for event_index in sorted(bad_events):
                prime = witness(factor_index, event_index)
                if prime is None:
                    break
                local_witnesses.append(prime)
            else:
                chosen = weights
                witness_histogram.update(local_witnesses)
                break
        require(chosen is not None, f"no independently certified word for factor {factor_index}")
        assignments.append(chosen)

    distribution = Counter(weights for weights in assignments if weights is not None)
    require(low_degree == 124 and len(assignments) - low_degree == 696, "low/high block split")
    require(
        set(distribution)
        == {(1, 1, 1, 1, 1), (1, 1, 1, 1, 2), (1, 1, 1, 2, 1)},
        "unexpected independent word family",
    )
    require(sum(witness_histogram.values()) == 381888, "coprimality-check census")
    return assignments, distribution, witness_histogram, prime_maps


def rational_polynomial_remainder(dividend, divisor):
    dividend = [Fraction(value) for value in dividend]
    divisor = [Fraction(value) for value in divisor]
    while dividend and dividend[-1] == 0:
        dividend.pop()
    while divisor and divisor[-1] == 0:
        divisor.pop()
    require(divisor, "zero rational divisor")
    while len(dividend) >= len(divisor):
        scale = dividend[-1] / divisor[-1]
        shift = len(dividend) - len(divisor)
        for j, value in enumerate(divisor):
            dividend[shift + j] -= scale * value
        while dividend and dividend[-1] == 0:
            dividend.pop()
    return dividend


def rational_evaluate(poly, value):
    result = Fraction(0)
    for coefficient in reversed(poly):
        result = result * value + coefficient
    return result


def sturm_root_count(poly, left, right):
    require(left < right, "invalid Sturm interval")
    require(rational_evaluate(poly, left) != 0, "left Sturm endpoint is a root")
    require(rational_evaluate(poly, right) != 0, "right Sturm endpoint is a root")
    derivative = [Fraction(j * poly[j]) for j in range(1, len(poly))]
    sequence = [[Fraction(value) for value in poly], derivative]
    while sequence[-1]:
        remainder = rational_polynomial_remainder(sequence[-2], sequence[-1])
        if not remainder:
            break
        sequence.append([-value for value in remainder])

    def variations(value):
        signs = []
        for row in sequence:
            evaluation = rational_evaluate(row, value)
            if evaluation:
                signs.append(1 if evaluation > 0 else -1)
        return sum(left_sign != right_sign for left_sign, right_sign in zip(signs, signs[1:]))

    return variations(left) - variations(right)


def fixture_audit(events, by_event):
    fixture_factor = (
        (-1, 0),
        (-2, 1),
        (-2, 2),
        (-3, 2),
        (1, 2),
        (0, 2),
        (1, 1),
        (1, 0),
    )

    irreducibility_witness = None
    for prime in range(7, 600):
        if prime == 31 or not is_prime(prime) or prime % 3 != 1:
            continue
        roots = [value for value in range(prime) if (value * value - value + 1) % prime == 0]
        for omega_image in reversed(roots):
            modulus = reduce_e_poly(fixture_factor, prime, omega_image)
            x = [0, 1]
            frobenius = modular_power(x, prime, modulus, prime)
            difference = frobenius[:]
            if len(difference) < 2:
                difference += [0] * (2 - len(difference))
            difference[1] = (difference[1] - 1) % prime
            if len(modular_gcd(modulus, difference, prime)) != 1:
                continue
            if modular_power(x, prime**7, modulus, prime) == x:
                irreducibility_witness = prime, omega_image
                break
        if irreducibility_witness:
            break
    require(irreducibility_witness is not None, "no independent fixture irreducibility witness")

    cayley_numerator = (ONE, (-1, 2))
    cayley_denominator = (ONE, (1, -2))
    numerator_powers = [(ONE,)]
    denominator_powers = [(ONE,)]
    for _ in range(7):
        numerator_powers.append(e_poly_mul(numerator_powers[-1], cayley_numerator))
        denominator_powers.append(e_poly_mul(denominator_powers[-1], cayley_denominator))
    transformed = [ZERO] * 8
    for degree, coefficient in enumerate(fixture_factor):
        term = e_poly_mul(numerator_powers[degree], denominator_powers[7 - degree])
        for j, value in enumerate(term):
            transformed[j] = e_add(transformed[j], e_mul(coefficient, value))
    require(all(2 * a + b == 0 and b % 2 == 0 for a, b in transformed), "Cayley identity")
    t_polynomial = [b // 2 for _, b in transformed]
    require(
        t_polynomial == [5, 39, -15, -189, -81, 261, 27, 81],
        "fixture t-polynomial",
    )
    require(
        sturm_root_count(t_polynomial, Fraction(-1, 7), Fraction(-1, 8)) == 1,
        "fixture isolating interval",
    )

    weights = (1, 1, 1, 1, 1)
    colours = label_colours(weights)
    edges = list(by_event[()])
    vanishing_events = 0
    for event in events:
        if not e_poly_remainder(event, fixture_factor):
            vanishing_events += 1
            edges.extend(by_event[event])
    require(len(edges) == 1221, "fixture strict edge count")
    require(all(colours[left] != colours[right] for left, right in edges), "fixture colouring")
    return {
        "irreducibility_prime": irreducibility_witness[0],
        "omega_image": irreducibility_witness[1],
        "target_prime_31_avoided": irreducibility_witness[0] != 31,
        "isolated_real_roots": 1,
        "vanishing_nonuniversal_events": vanishing_events,
        "strict_unit_edges": len(edges),
        "physical_vertices": 243,
        "colours": 3,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    args = parser.parse_args()
    raw_certificate = args.certificate.read_bytes()
    certificate = json.loads(raw_certificate)
    require(
        hashlib.sha256(raw_certificate).hexdigest()
        == "c76efb83fab51605eb7e59c7fa9114b3fbe1bc643500c8eb047f47f1d5bc8bb7",
        "unexpected certificate bytes",
    )

    events, by_event = reconstruct_events()
    event_rows = [flatten(event) for event in events]
    event_sha256 = digest(event_rows)
    require(event_sha256 == certificate["event_sha256"], "event stream mismatch")
    factors, active = verify_factor_witness(certificate, events)
    bad = bad_event_sets(events, by_event)
    assignments, distribution, witness_histogram, prime_maps = independent_colour_cover(
        factors, active, events, bad
    )
    fixture = fixture_audit(events, by_event)

    degree_histogram = Counter(len(factor) - 1 for factor in factors)
    require(
        degree_histogram == {1: 6, 2: 3, 3: 28, 4: 87, 5: 144, 6: 258, 7: 168, 8: 126},
        "factor degree histogram",
    )
    result = {
        "verified": True,
        "imports_target_code": False,
        "uses_certificate_as_factor_witness": True,
        "ignores_submitted_colour_specs_and_factor_cover": True,
        "arithmetic": "exact Python integers, Fractions, Eisenstein pairs, and finite fields",
        "label_vertices": 243,
        "label_pairs": 29403,
        "universal_edges": len(by_event[()]),
        "event_polynomials": len(events),
        "event_degree_histogram": dict(sorted(Counter(len(event) - 1 for event in events).items())),
        "event_sha256": event_sha256,
        "factor_polynomials": len(factors),
        "factor_degree_histogram": dict(sorted(degree_histogram.items())),
        "factor_product_identities": len(events),
        "low_degree_blocks_delegated_to_accepted_h4119": sum(a is None for a in assignments),
        "high_degree_blocks_independently_coloured": sum(a is not None for a in assignments),
        "independent_colour_distribution": {
            "".join(map(str, weights)): count for weights, count in sorted(distribution.items())
        },
        "independent_modular_primes": [prime for prime, _ in prime_maps],
        "independent_modular_witness_histogram": dict(sorted(witness_histogram.items())),
        "modular_coprimality_checks": sum(witness_histogram.values()),
        "fixture": fixture,
        "unit_circle_chromatic_number": 3,
        "record_improvement": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
