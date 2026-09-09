#!/usr/bin/env python3
"""Independent exact checker for the h4185 first-step anchor theorem.

No h4185 module is imported.  The curve inventory comes from the reviewer-1
h4181 checker, whose direct Q(sqrt(-3))[x,y] construction differs from the
target's h4163 bivariate source.  Restrictions are rebuilt directly from
displacement rows as rational functions on the anchor circles.
"""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
import hashlib
import importlib.util
import json
from math import gcd, isqrt, lcm
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_radix_first_step_anchor"
PREVIOUS_CHECKER = (
    ROOT
    / "hadwiger_nelson_radix_two_coordinate_pencils_review1"
    / "independent_check.py"
)

spec = importlib.util.spec_from_file_location("reviewer_curve_inventory", PREVIOUS_CHECKER)
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)

CERTIFICATE_SHA256 = "15235c8e304f762422162f3cb7422e74b683b2f8e997e11037cc43f567cf9976"
PHYSICAL_SHA256 = "845d08282f55e27461b413fa6d0a21b8610ccba8b1806e985b1005af7fdbf8d7"
RESTRICTION_SHA256 = "1fed3b8b15e84549d4a549bc665cbdafd6f9566041c7e4094ef058630370134f"
ORBIT_INTERFACE_FILE_SHA256 = "be36cc09da60c4bba4c260f42c12b21b88c9dea4553a1ae0214870c0284b047e"
ORBIT_INTERFACE_CANONICAL_SHA256 = "1db1ecc86c993bbe22a83127b85c6d9467d385bdb7dba085193ad47308e1676a"
INCIDENCE_INTERFACE_CANONICAL_SHA256 = "c9cb33688915d282b9d410898eeeb22d4bd33e242b3d28b7703ca4fe2111c477"
PRIME = 1_000_003

ZERO_E = (0, 0)
DIGITS = (ZERO_E, (1, 0), (0, 1))
LABELS = tuple(product(range(3), repeat=5))
WEIGHTS = tuple((1,) + tail for tail in product(range(3), repeat=4))
H = (1, 0, 3)
CIRCLE = ((0, 0, -1), (0, 2, 3), (2, 0, 1))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def trim(poly):
    result = list(poly)
    while result and result[-1] == 0:
        result.pop()
    return result


def poly_add(left, right, scale=1):
    result = list(left) + [0] * max(0, len(right) - len(left))
    for index, value in enumerate(right):
        result[index] += scale * value
    return trim(result)


def poly_mul(left, right):
    if not left or not right:
        return []
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return trim(result)


def poly_power(poly, exponent):
    result = [1]
    base = list(poly)
    while exponent:
        if exponent & 1:
            result = poly_mul(result, base)
        exponent //= 2
        if exponent:
            base = poly_mul(base, base)
    return result


def poly_derivative(poly):
    return [index * poly[index] for index in range(1, len(poly))]


def poly_divmod(left, right):
    numerator = trim(map(Fraction, left))
    denominator = trim(map(Fraction, right))
    require(denominator, "polynomial division by zero")
    quotient = [Fraction(0)] * max(0, len(numerator) - len(denominator) + 1)
    while numerator and len(numerator) >= len(denominator):
        offset = len(numerator) - len(denominator)
        scale = numerator[-1] / denominator[-1]
        quotient[offset] += scale
        for index, value in enumerate(denominator):
            numerator[offset + index] -= scale * value
        numerator = trim(numerator)
    return trim(quotient), numerator


def exact_quotient(left, right):
    quotient, remainder = poly_divmod(left, right)
    require(not remainder, "exact polynomial quotient")
    return quotient


def primitive(poly):
    values = trim(map(Fraction, poly))
    require(values, "primitive zero polynomial")
    denominator = lcm(*(value.denominator for value in values))
    integers = [int(value * denominator) for value in values]
    content = 0
    for value in integers:
        content = gcd(content, abs(value))
    require(content > 0, "nonzero polynomial content")
    if integers[-1] < 0:
        content = -content
    return tuple(value // content for value in integers)


def sturm_root_count(poly):
    first = trim(map(Fraction, poly))
    require(len(first) >= 2, "positive-degree Sturm input")
    chain = [first, trim(map(Fraction, poly_derivative(first)))]
    require(chain[-1], "nonconstant derivative")
    while chain[-1]:
        _, remainder = poly_divmod(chain[-2], chain[-1])
        if not remainder:
            break
        # Positive rescaling is harmless and keeps fractions smaller.
        scale = abs(remainder[-1])
        chain.append([-value / scale for value in remainder])

    def variations(positive_infinity):
        signs = []
        for item in chain:
            sign = 1 if item[-1] > 0 else -1
            if not positive_infinity and (len(item) - 1) % 2:
                sign = -sign
            signs.append(sign)
        return sum(a != b for a, b in zip(signs, signs[1:]))

    return variations(False) - variations(True)


def is_prime(value):
    return value >= 2 and all(value % divisor for divisor in range(2, isqrt(value) + 1))


def mod_trim(poly, prime=PRIME):
    return trim(value % prime for value in poly)


def mod_remainder(left, right, prime=PRIME):
    numerator = mod_trim(left, prime)
    denominator = mod_trim(right, prime)
    require(denominator, "modular polynomial division by zero")
    inverse = pow(denominator[-1], -1, prime)
    while numerator and len(numerator) >= len(denominator):
        offset = len(numerator) - len(denominator)
        scale = numerator[-1] * inverse % prime
        for index, value in enumerate(denominator):
            numerator[offset + index] = (
                numerator[offset + index] - scale * value
            ) % prime
        numerator = trim(numerator)
    return numerator


def modular_coprime(left, right, prime=PRIME):
    a, b = mod_trim(left, prime), mod_trim(right, prime)
    while b:
        a, b = b, mod_remainder(a, b, prime)
    return len(a) == 1


# A Q(sqrt(-3))-valued polynomial is a pair (real polynomial, s coefficient).
def qp_add(left, right, scale=1):
    return poly_add(left[0], right[0], scale), poly_add(left[1], right[1], scale)


def qp_mul(left, right):
    return (
        poly_add(poly_mul(left[0], right[0]), poly_mul(left[1], right[1]), -3),
        poly_add(poly_mul(left[0], right[1]), poly_mul(left[1], right[0])),
    )


def qp_scalar(value, scalar):
    return [scalar * coefficient for coefficient in value[0]], [scalar * coefficient for coefficient in value[1]]


def qp_power(value, exponent):
    result = ([1], [])
    for _ in range(exponent):
        result = qp_mul(result, value)
    return result


def row_numerator(row, sign):
    """Return H^k sum row_j z(t)^j in the {1,s} basis."""
    order = max(index for index, value in enumerate(row) if value != ZERO_E)
    z_numerator = ([0, 0, -6 * sign], [0, 2 * sign])
    z_powers = [qp_power(z_numerator, index) for index in range(order + 1)]
    h_powers = [poly_power(H, index) for index in range(order + 1)]
    total = ([], [])
    for index, coefficient in enumerate(row[: order + 1]):
        a, b = coefficient
        # a+b*omega = (a+b/2)+(b/2)*s.
        scalar = (Fraction(2 * a + b, 2), Fraction(b, 2))
        term = qp_mul(([scalar[0]], [scalar[1]]), z_powers[index])
        term = (
            poly_mul(term[0], h_powers[order - index]),
            poly_mul(term[1], h_powers[order - index]),
        )
        total = qp_add(total, term)
    return total, order


def restricted_event(row, sign):
    numerator, order = row_numerator(row, sign)
    norm = poly_add(
        poly_add(poly_mul(numerator[0], numerator[0]), poly_mul(numerator[1], numerator[1]), 3),
        poly_power(H, 2 * order),
        -1,
    )
    reduced = exact_quotient(norm, poly_power(H, order))
    if not reduced:
        return ()
    return primitive(reduced)


def inventories():
    factors, row_by_curve = R.curve_inventory()
    require(tuple(factors[342]) == CIRCLE, "radial circle ID")
    restrictions = []
    for sign in (1, -1):
        values = []
        for curve in range(len(factors)):
            if curve == 342:
                values.append((-1, 0, 9))
            else:
                values.append(restricted_event(row_by_curve[curve], sign))
        restrictions.append(values)
    require([values.count(()) for values in restrictions] == [1, 1], "one identically active anchor per sign")
    require([values.index(()) for values in restrictions] == [2209, 2208], "representative anchor IDs")
    require(set(restrictions[0]) == set(restrictions[1]), "common restriction inventory")
    unique = sorted(set(restrictions[0]) - {()})
    require(len(unique) == 2760, "2,760 distinct nonzero restrictions")
    require(digest(unique) == RESTRICTION_SHA256, "restriction inventory digest")
    return factors, row_by_curve, restrictions, unique


def label_edge_inventory(row_by_curve):
    curve_by_row = {row: curve for curve, row in row_by_curve.items()}
    groups = [[] for _ in range(2797)]
    base = []
    for left, right in combinations(range(243), 2):
        difference = tuple(
            (
                DIGITS[LABELS[left][index]][0] - DIGITS[LABELS[right][index]][0],
                DIGITS[LABELS[left][index]][1] - DIGITS[LABELS[right][index]][1],
            )
            for index in range(5)
        )
        row = R.canonical_row(difference)
        support = [index for index, value in enumerate(row) if value != ZERO_E]
        if len(support) == 1:
            owner = "base" if support[0] == 0 else 342
        else:
            owner = curve_by_row[row]
        if owner == "base":
            base.append((left, right))
        else:
            groups[owner].append((left, right))
    require(len(base) == 243 and sum(map(len, groups)) == 29160, "all 29,403 label pairs assigned")
    require(len(groups[342]) == 972, "radial-circle label pairs")
    return base, groups, curve_by_row


def check_factor_certificate(certificate, unique):
    blocks = [tuple(block) for block in certificate.get("blocks", [])]
    require(blocks == sorted(blocks) and len(set(blocks)) == 2536, "2,536 canonical blocks")
    for block in blocks:
        require(2 <= len(block) <= 9 and primitive(block) == block, "primitive positive-leading block")
    factorizations = certificate.get("factorizations")
    require(isinstance(factorizations, list) and len(factorizations) == len(unique), "complete restriction factorizations")
    by_polynomial = {}
    all_used = set()
    for polynomial, entry in zip(unique, factorizations):
        require(isinstance(entry, list) and len(entry) == 2, "factorization record")
        scalar, terms = entry
        require(type(scalar) is int and scalar > 0, "positive factor content")
        require(terms == sorted(terms) and len({index for index, _ in terms}) == len(terms), "canonical factor terms")
        product_value = [scalar]
        used = set()
        for index, exponent in terms:
            require(type(index) is int and 0 <= index < len(blocks), "block index")
            require(type(exponent) is int and 1 <= exponent <= 8, "factor multiplicity")
            for _ in range(exponent):
                product_value = poly_mul(product_value, blocks[index])
            used.add(index)
        require(tuple(product_value) == polynomial, "exact factor product")
        by_polynomial[polynomial] = used
        all_used.update(used)
    require(all_used == set(range(2536)), "every block used")
    return blocks, by_polynomial


def check_roots_and_coprimality(blocks, declared_roots):
    require(is_prime(PRIME), "independently trial-divided proof modulus")
    require(len(declared_roots) == len(blocks), "one root count per block")
    roots = []
    for block, declared in zip(blocks, declared_roots):
        actual = sturm_root_count(block)
        require(type(declared) is int and actual == declared, "exact Sturm real-root count")
        roots.append(actual)

    squarefree_indices = []
    for index, block in enumerate(blocks):
        require(block[-1] % PRIME != 0, "block degree preserved modulo p")
        require(len(block) - 1 < PRIME, "derivative degree preserved modulo p")
        require(modular_coprime(block, poly_derivative(block)), "squarefree block modulo p")
        squarefree_indices.append(PRIME)

    real_indices = [index for index, count in enumerate(roots) if count]
    trace = hashlib.sha256()
    pairs = 0
    for left, right in combinations(real_indices, 2):
        require(blocks[left][-1] % PRIME and blocks[right][-1] % PRIME, "pair degrees preserved modulo p")
        require(modular_coprime(blocks[left], blocks[right]), "real-root blocks pairwise coprime modulo p")
        trace.update(f"{left},{right},{PRIME}\n".encode())
        pairs += 1
    require(pairs == 1_817_371, "complete real-block pair census")
    require(trace.hexdigest() == "7fdea25f5ea1030f4b1f35a8df2807e4abee3ef717e567967e9d59202a03e47b", "coprimality transcript")
    require(digest(squarefree_indices) == "e922d15c47f1c31df6b7c86636cb79ae74a9e64614fde85a9393ea2db6ccf5cf", "squarefree-prime transcript")
    return roots, {
        "prime": PRIME,
        "squarefree_blocks": len(squarefree_indices),
        "real_block_pair_checks": pairs,
        "pair_trace_sha256": trace.hexdigest(),
        "squarefree_primes_sha256": digest(squarefree_indices),
    }


def colours_for_weight(weight):
    return [sum(a * b for a, b in zip(weight, label)) % 3 for label in LABELS]


def check_word(weight, active_curves, base, groups):
    colours = colours_for_weight(weight)
    require(all(colours[a] != colours[b] for a, b in base), "proper universal edges")
    for curve in active_curves:
        require(all(colours[a] != colours[b] for a, b in groups[curve]), "proper active-curve edges")


def collision_numerator_vanishes(row, block, sign):
    row = tuple(tuple(value) for value in row)
    require(len(row) == 5 and any(value != ZERO_E for value in row), "nonzero collision row")
    require(all(value == ZERO_E or value in R.UNITS for value in row), "digit-difference collision row")
    numerator, _ = row_numerator(row, sign)
    require(not poly_divmod(numerator[0], block)[1], "collision real numerator divisible")
    require(not poly_divmod(numerator[1], block)[1], "collision imaginary numerator divisible")


def check_colouring_certificate(certificate, restrictions, blocks, roots, by_polynomial, base, groups):
    collision_entries = certificate.get("collision_witnesses")
    require(isinstance(collision_entries, list) and len(collision_entries) == 5, "five collision blocks")
    collision_blocks = set()
    for entry in collision_entries:
        index = entry.get("block_id")
        require(type(index) is int and 0 <= index < len(blocks) and roots[index] == 1, "real collision block")
        require(index not in collision_blocks, "distinct collision blocks")
        rows = entry.get("rows")
        require(isinstance(rows, list) and len(rows) == 2, "collision row for both signs")
        for row, sign in zip(rows, (1, -1)):
            collision_numerator_vanishes(row, blocks[index], sign)
        collision_blocks.add(index)

    assignments = certificate.get("colour_assignments")
    require(isinstance(assignments, list) and [len(values) for values in assignments] == [2536, 2536], "complete colour assignments")
    used_words = []
    for sign_index, (special, assigned) in enumerate(zip(restrictions, assignments)):
        anchor = special.index(())
        events = [{anchor} for _ in blocks]
        for curve, polynomial in enumerate(special):
            if polynomial:
                for block in by_polynomial[polynomial]:
                    events[block].add(curve)
        check_word(WEIGHTS[0], {anchor}, base, groups)
        used = set()
        for index, assignment in enumerate(assigned):
            if roots[index] == 0 or index in collision_blocks:
                require(assignment is None, "no word on nonreal or collision block")
                continue
            require(type(assignment) is int and 0 <= assignment < len(WEIGHTS), "valid colour-word index")
            check_word(WEIGHTS[assignment], events[index], base, groups)
            used.add(WEIGHTS[assignment])
        require(sum(value is not None for value in assigned) == 1902, "1,902 coloured real blocks")
        used_words.append([list(word) for word in sorted(used)])
    return collision_blocks, used_words


def check_symmetry_and_endpoints():
    rho = (-1, 1)  # omega^2
    power = (1, 0)
    shifts = []
    for _ in range(5):
        rotated = {R.e_mul(power, digit) for digit in DIGITS}
        candidates = [
            shift
            for shift in rotated
            if {
                (value[0] - shift[0], value[1] - shift[1])
                for value in rotated
            }
            == set(DIGITS)
        ]
        require(len(candidates) == 1, "unique digit-triangle translation")
        shifts.append(candidates[0])
        power = R.e_mul(power, rho)
    require(shifts == [(0, 0), (-1, 0), (0, -1), (0, 0), (-1, 0)], "A5 rotation translation identity")

    positive_orbit = set()
    value = (1, 0)
    for _ in range(3):
        positive_orbit.add(value)
        value = R.e_mul(value, rho)
    negative_orbit = {(-a, -b) for a, b in positive_orbit}
    require(positive_orbit.isdisjoint(negative_orbit) and positive_orbit | negative_orbit == set(R.UNITS), "six anchor circles reduce to two sign representatives")

    endpoint_results = []
    for z in (2, -2):
        points = set()
        for label in LABELS:
            point = (0, 0)
            for exponent, digit_index in enumerate(label):
                digit = DIGITS[digit_index]
                point = (
                    point[0] + digit[0] * z**exponent,
                    point[1] + digit[1] * z**exponent,
                )
            points.add(point)
        edges = 0
        for left, right in combinations(sorted(points), 2):
            a, b = left[0] - right[0], left[1] - right[1]
            if a * a + a * b + b * b == 1:
                require((a - b) % 3 != 0, "proper endpoint quotient colour")
                edges += 1
        require({(0, 0), (1, 0), (0, 1)} <= points, "endpoint unit triangle")
        endpoint_results.append({"z": z, "physical_vertices": len(points), "unit_edges": edges})
    return shifts, endpoint_results


# Arithmetic in Q[t]/(21*t^2-1), represented as c0+c1*t.
def k_add(left, right, scale=1):
    return left[0] + scale * right[0], left[1] + scale * right[1]


def k_mul(left, right):
    return (
        left[0] * right[0] + left[1] * right[1] / 21,
        left[0] * right[1] + left[1] * right[0],
    )


KZERO = (Fraction(0), Fraction(0))
KONE = (Fraction(1), Fraction(0))


def ek_add(left, right, scale=1):
    return k_add(left[0], right[0], scale), k_add(left[1], right[1], scale)


def ek_mul(left, right):
    return (
        k_add(k_mul(left[0], right[0]), k_mul(left[1], right[1]), -1),
        k_add(k_add(k_mul(left[0], right[1]), k_mul(left[1], right[0])), k_mul(left[1], right[1])),
    )


def decode_coordinate(row):
    require(isinstance(row, list) and len(row) == 5 and all(type(value) is int for value in row) and row[4] > 0, "physical coordinate encoding")
    denominator = row[4]
    return (
        (Fraction(row[0], denominator), Fraction(row[1], denominator)),
        (Fraction(row[2], denominator), Fraction(row[3], denominator)),
    )


def reduced_at_fixture(polynomial):
    _, remainder = poly_divmod(polynomial, (-1, 0, 21))
    return trim(remainder)


def edge_owner(left_index, right_index, curve_by_row):
    difference = tuple(
        (
            DIGITS[LABELS[left_index][index]][0] - DIGITS[LABELS[right_index][index]][0],
            DIGITS[LABELS[left_index][index]][1] - DIGITS[LABELS[right_index][index]][1],
        )
        for index in range(5)
    )
    row = R.canonical_row(difference)
    support = [index for index, value in enumerate(row) if value != ZERO_E]
    if len(support) == 1:
        return "base" if support[0] == 0 else 342
    return curve_by_row[row]


def check_physical_fixture(path, restrictions, curve_by_row):
    raw = Path(path).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PHYSICAL_SHA256, "physical fixture digest")
    fixture = json.loads(raw)
    require(fixture.get("schema") == "hn-radix-first-anchor-physical-v1", "physical schema")
    require(fixture.get("real_parameter_polynomial") == [-1, 0, 21], "fixture field")
    require(fixture.get("isolating_interval") == ["1/5", "1/4"], "positive-root interval")
    require(Fraction(21, 25) - 1 < 0 and Fraction(21, 16) - 1 > 0, "root bracket signs")
    require(all((21 * value * value - 1) % 11 for value in range(11)), "quadratic irreducible modulo 11")

    results = []
    examples = fixture.get("examples")
    require(isinstance(examples, list) and [entry.get("sign") for entry in examples] == [1, -1], "two signed fixtures")
    for example, special in zip(examples, restrictions):
        sign = example["sign"]
        encoded = example.get("vertices")
        word = example.get("colour_word")
        require(isinstance(encoded, list) and len(encoded) == 243, "243 encoded vertices")
        require(isinstance(word, list) and len(word) == 5 and all(type(value) is int and 0 <= value < 3 for value in word), "fixture colour word")
        declared = list(map(decode_coordinate, encoded))

        z = (
            (Fraction(-sign, 4), Fraction(-7 * sign, 4)),
            (Fraction(0), Fraction(7 * sign, 2)),
        )
        powers = [((KONE), KZERO)]
        for _ in range(4):
            powers.append(ek_mul(powers[-1], z))
        reconstructed = []
        for label in LABELS:
            point = (KZERO, KZERO)
            for exponent, digit_index in enumerate(label):
                digit = ((Fraction(DIGITS[digit_index][0]), Fraction(0)), (Fraction(DIGITS[digit_index][1]), Fraction(0)))
                point = ek_add(point, ek_mul(powers[exponent], digit))
            reconstructed.append(point)
        require(reconstructed == declared, "all fixture coordinates independently reconstructed")

        colours = colours_for_weight(tuple(word))
        edges = []
        active = set()
        for left, right in combinations(range(243), 2):
            difference = ek_add(declared[left], declared[right], -1)
            require(difference != (KZERO, KZERO), "all fixture vertices distinct")
            norm = k_add(
                k_add(k_mul(difference[0], difference[0]), k_mul(difference[0], difference[1])),
                k_mul(difference[1], difference[1]),
            )
            if norm == KONE:
                require(colours[left] != colours[right], "proper physical fixture edge")
                edges.append((left, right))
                owner = edge_owner(left, right, curve_by_row)
                if owner != "base":
                    active.add(owner)
        require(all(edge in edges for edge in ((0, 81), (0, 162), (81, 162))), "physical unit triangle")
        expected_active = {
            curve
            for curve, polynomial in enumerate(special)
            if not polynomial or not reduced_at_fixture(polynomial)
        }
        require(active == expected_active and len(active) == 8, "eight exact active curves")
        results.append(
            {
                "sign": sign,
                "vertices": 243,
                "unit_edges": len(edges),
                "edge_sha256": digest(edges),
                "coordinates_sha256": digest(encoded),
                "active_curves": sorted(active),
                "colour_word": word,
                "chromatic_number": 3,
            }
        )
    return {"physical_pair_checks": 58_806, "examples": results}


def gf4_affine_span(left, right):
    result = set()
    for a, b in product(range(4), repeat=2):
        normal = tuple(
            R.gf4_mul(a, x) ^ R.gf4_mul(b, y)
            for x, y in zip(left[0], right[0])
        )
        if not any(normal):
            continue
        constant = R.gf4_mul(a, left[1]) ^ R.gf4_mul(b, right[1])
        normalized = R.gf4_projective(normal)
        pivot = next(value for value in normal if value)
        inverse = next(value for value in (1, 2, 3) if R.gf4_mul(pivot, value) == 1)
        result.add((normalized, R.gf4_mul(inverse, constant)))
    require(len(result) == 5, "five affine sections in nonparallel span")
    return tuple(sorted(result))


def count_incidence_survivors(pencil, buckets, forbidden_pairs, forbidden_triples):
    domains = sorted((buckets[signature] for signature in pencil), key=lambda values: (len(values), values))

    def visit(selected, index):
        if index == 5:
            return 1
        total = 0
        for curve in domains[index]:
            if any(tuple(sorted((old, curve))) in forbidden_pairs for old in selected):
                continue
            if any(tuple(sorted((a, b, curve))) in forbidden_triples for a, b in combinations(selected, 2)):
                continue
            total += visit(selected + (curve,), index + 1)
        return total

    return visit((), 0)


def conditional_frontier(orbit_path, incidence_path, factors, row_by_curve):
    orbit_raw = Path(orbit_path).read_bytes()
    require(hashlib.sha256(orbit_raw).hexdigest() == ORBIT_INTERFACE_FILE_SHA256, "h4177 interface file digest")
    orbit = json.loads(orbit_raw)
    incidence = json.loads(Path(incidence_path).read_text())
    require(digest(orbit) == ORBIT_INTERFACE_CANONICAL_SHA256, "h4177 canonical interface")
    require(digest(incidence) == INCIDENCE_INTERFACE_CANONICAL_SHA256, "accepted h4167 incidence interface")

    signatures = {curve: R.signature(row) for curve, row in row_by_curve.items()}
    supports = {
        curve: {index for index, value in enumerate(row) if index and value != ZERO_E}
        for curve, row in row_by_curve.items()
    }
    anchors = sorted(
        curve
        for curve, row in row_by_curve.items()
        if row[0] != ZERO_E and row[1] != ZERO_E and all(value == ZERO_E for value in row[2:])
    )
    require(anchors == [591, 592, 1277, 1278, 2208, 2209], "six first-step anchors")
    anchor_set = set(anchors)
    e1 = (1, 0, 0, 0)
    buckets = defaultdict(list)
    for curve, signature in signatures.items():
        buckets[signature].append(curve)
    for values in buckets.values():
        values.sort()
    require({curve for signature, curves in buckets.items() if signature[0] == e1 for curve in curves} == anchor_set, "anchors are all realized e1 sections")

    modes = orbit["pair_modes"]
    old_exact = modes["exact_five_compatible"]
    prior_moves = [row for row in old_exact if len(supports[row[0]] | supports[row[1]]) == 2]
    require(len(prior_moves) == 192 and digest(prior_moves) == "8eb2ca8fbd0342f6939d57cf60d3f32bedda21ac2e6cf8dc6079d89a3afbb73a", "reviewed h4181 mode moves")
    prior_set = {tuple(row[:2]) for row in prior_moves}
    exact = [row for row in old_exact if tuple(row[:2]) not in prior_set]
    six = [row for name, rows in modes.items() if name != "exact_five_compatible" for row in rows] + prior_moves
    all_rows = exact + six
    require(len(all_rows) == len({tuple(row[:2]) for row in all_rows}) == 131356, "conditional source pair partition")

    degrees = [max(i + j for i, j, _ in factor) for factor in factors]
    for a, b, mask, bound, allowance in all_rows:
        require(0 <= a < b < len(factors) and 0 < mask < 64, "valid imported pair row")
        require(bound == degrees[a] * degrees[b] // 2, "imported bidegree arithmetic")
        require(allowance == bound // int(mask).bit_count(), "imported stabilizer allowance")

    removed = sorted(row for row in all_rows if anchor_set.intersection(row[:2]))
    removed_set = {tuple(row[:2]) for row in removed}
    moved = sorted(
        row
        for row in exact
        if tuple(row[:2]) not in removed_set
        and any(signature[0] == e1 for signature in gf4_affine_span(signatures[row[0]], signatures[row[1]]))
    )
    moved_set = {tuple(row[:2]) for row in moved}
    kept_exact = sorted(row for row in exact if tuple(row[:2]) not in removed_set | moved_set)
    kept_six = sorted([row for row in six if tuple(row[:2]) not in removed_set] + moved)

    all_anchor_pencils = set()
    for constant in range(1, 4):
        anchor_signature = (e1, constant)
        for other in buckets:
            if other[0] == e1:
                continue
            pencil = gf4_affine_span(anchor_signature, other)
            if all(signature in buckets for signature in pencil):
                all_anchor_pencils.add(pencil)
    old_pencils = {
        pencil
        for pencil in all_anchor_pencils
        if tuple(sorted(sum(value != 0 for value in signature[0]) for signature in pencil)) == (1, 1, 2, 2, 2)
    }
    new_pencils = sorted(all_anchor_pencils - old_pencils)
    require(len(all_anchor_pencils) == 243 and len(old_pencils) == 27 and len(new_pencils) == 216, "complete new anchor-pencil classification")

    forbidden_pairs = {
        tuple(sorted(values))
        for values in incidence["monic_degree_four_excluded_pairs"]
    }
    forbidden_pairs.update(
        tuple(sorted(values))
        for values in incidence["injectivity_excluded_sets"]
        if len(values) == 2
    )
    forbidden_triples = {
        tuple(sorted(values))
        for values in incidence["injectivity_excluded_sets"]
        if len(values) == 3
    }
    transcript = []
    for pencil in new_pencils:
        raw_count = 1
        for signature in pencil:
            raw_count *= len(buckets[signature])
        survivor_count = count_incidence_survivors(pencil, buckets, forbidden_pairs, forbidden_triples)
        transcript.append([pencil, raw_count, survivor_count])

    exported = {
        "anchor_curves": anchors,
        "removed": removed,
        "moved": moved,
        "remaining_exact": kept_exact,
        "remaining_six": kept_six,
        "pencils": new_pencils,
        "lift_transcript": transcript,
    }
    expected_hashes = {
        "removed": "6ac211914f15a0556f5dc36d8975caf4e7db813a45ff7f817025f051353d2ed7",
        "moved": "7fe3c2ee21d54961d2399e122e4047e25a1822075a88aa49357d99a6c8cc36f1",
        "remaining_exact": "10397f8fbbec7e37c43045ed2de60306d6481c4ecdad78e9eb035ce44d35fd86",
        "remaining_six": "e6f501838836b886e24613fab1543ce31cc51dcec562f46a5ddae7a0411e97ad",
        "pencils": "a5d3819ad099b9c3837d9f4c4558a1ade3eb147ef091e5262344acb982903304",
        "lift_transcript": "b6334286de9b12531703784c0d3a625e7c35a7ebc8ae8c774fcc5a77fbd4cd89",
    }
    require({key: digest(value) for key, value in exported.items() if key != "anchor_curves"} == expected_hashes, "entrywise frontier hashes")

    return {
        "status": "pair_orbit_figures_conditional_on_h4177_h4175_h4117",
        "anchor_curves": anchors,
        "removed_whole_pairs": len(removed),
        "removed_exact_five_pairs": sum(tuple(row[:2]) in removed_set for row in exact),
        "removed_at_least_six_pairs": sum(tuple(row[:2]) in removed_set for row in six),
        "removed_orbit_allowance": sum(row[4] for row in removed),
        "moved_to_at_least_six": len(moved),
        "moved_allowance": sum(row[4] for row in moved),
        "remaining_global_pairs": len(kept_exact) + len(kept_six),
        "remaining_global_allowance": sum(row[4] for row in kept_exact + kept_six),
        "remaining_exact_five_pairs": len(kept_exact),
        "remaining_exact_five_allowance": sum(row[4] for row in kept_exact),
        "remaining_at_least_six_pairs": len(kept_six),
        "remaining_at_least_six_allowance": sum(row[4] for row in kept_six),
        "new_closed_pencils": len(new_pencils),
        "previously_closed_two_coordinate_pencils": len(old_pencils),
        "new_closed_raw_lifts": sum(row[1] for row in transcript),
        "new_closed_h4171_survivors": sum(row[2] for row in transcript),
        "remaining_pencils": 5328 - len(new_pencils),
        "remaining_quintets": 132225984 - sum(row[2] for row in transcript),
    }


def run(certificate_path, physical_path, orbit_path=None, incidence_path=None):
    certificate_raw = Path(certificate_path).read_bytes()
    require(hashlib.sha256(certificate_raw).hexdigest() == CERTIFICATE_SHA256, "target certificate digest")
    certificate = json.loads(certificate_raw)
    require(certificate.get("schema") == "hn-radix-first-anchor-v1", "certificate schema")

    factors, row_by_curve, restrictions, unique = inventories()
    require(certificate.get("curve_inventory_sha256") == R.EXPECTED_INVENTORY_SHA256, "certificate curve inventory")
    require(certificate.get("restriction_inventory_sha256") == RESTRICTION_SHA256, "certificate restriction inventory")
    base, groups, curve_by_row = label_edge_inventory(row_by_curve)
    blocks, by_polynomial = check_factor_certificate(certificate, unique)
    roots, coprimality = check_roots_and_coprimality(
        blocks, certificate.get("real_root_counts")
    )
    collision_blocks, used_words = check_colouring_certificate(
        certificate,
        restrictions,
        blocks,
        roots,
        by_polynomial,
        base,
        groups,
    )
    shifts, endpoints = check_symmetry_and_endpoints()
    physical = check_physical_fixture(physical_path, restrictions, curve_by_row)

    result = {
        "verdict_scope": "all_six_first_step_anchor_circles",
        "event_curves": len(factors),
        "representative_anchor_curves": [values.index(()) for values in restrictions],
        "unique_nonzero_restricted_polynomials": len(unique),
        "primitive_blocks": len(blocks),
        "degree_histogram": {
            str(degree): count
            for degree, count in sorted(Counter(len(block) - 1 for block in blocks).items())
        },
        "blocks_with_real_roots": sum(count > 0 for count in roots),
        "nonreal_blocks": sum(count == 0 for count in roots),
        "distinct_finite_real_event_parameters_per_representative": sum(roots),
        "coprimality": coprimality,
        "colour_word_blocks_per_representative": [1902, 1902],
        "blocks_closed_by_accepted_collision_theorem": len(collision_blocks),
        "real_parameters_closed_by_accepted_collision_theorem": sum(roots[index] for index in collision_blocks),
        "used_colour_words": used_words,
        "rotation_translation_shifts": [list(value) for value in shifts],
        "endpoints": endpoints,
        "physical_fixture": physical,
        "all_six_anchor_loci_chromatic_number": 3,
        "maximum_physical_order": 243,
        "complete_architecture_closed": False,
        "record_improvement": False,
    }
    if (orbit_path is None) != (incidence_path is None):
        raise AssertionError("frontier audit needs both interfaces")
    if orbit_path is not None:
        result["conditional_frontier"] = conditional_frontier(
            orbit_path, incidence_path, factors, row_by_curve
        )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=TARGET / "certificate.json")
    parser.add_argument("--physical", type=Path, default=TARGET / "physical.json")
    parser.add_argument("--orbit-interface", type=Path)
    parser.add_argument("--incidence-interface", type=Path)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = run(args.certificate, args.physical, args.orbit_interface, args.incidence_interface)
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        require(result == expected, "independent expected output")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
