#!/usr/bin/env python3
"""Independent checker for the h4181 two-coordinate A5 pencil closure.

This file imports no producer or verifier module.  It reconstructs the A5
curve inventory directly, enumerates the relevant F4 covers by point masks,
normalizes all lifts, and checks the submitted identities after changing from
the basis {1, omega} to {1, sqrt(-3)}.
"""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
import hashlib
import json
from math import gcd
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_radix_two_coordinate_pencils"

ZERO_E = (0, 0)
UNITS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
DISPLACEMENTS = (ZERO_E,) + UNITS

EXPECTED_CERTIFICATE_SHA256 = (
    "2cee23437feab03d5cfbbeaa87b909fb1a4215194bf649daa523ab31bf84ed21"
)
EXPECTED_INVENTORY_SHA256 = (
    "85c286422c01bcb6ebb244186032bc607984471bc2b705ef7247084dd7c33db9"
)
EXPECTED_PATTERNS_SHA256 = (
    "aba200487055af434b9556fd6abdc85252a31140e61d99abc683fc6bd28d8cb0"
)
EXPECTED_QUINTETS_SHA256 = (
    "6e98cc7cc4a83774b9826b8989518ebdde3982298e7fb08801cb9b3777226e55"
)
EXPECTED_FORMS_SHA256 = (
    "d9b918c2484f1abf2227907552aabef31b3abb4c040cedd1eca3a7120250b082"
)
EXPECTED_TRACE_SHA256 = (
    "99fbf510c6ae7e4d590261d14f6919251f0a7e134c6caed62164edfff31854a1"
)
EXPECTED_ORBIT_INTERFACE_FILE_SHA256 = (
    "be36cc09da60c4bba4c260f42c12b21b88c9dea4553a1ae0214870c0284b047e"
)
EXPECTED_ORBIT_INTERFACE_CANONICAL_SHA256 = (
    "1db1ecc86c993bbe22a83127b85c6d9467d385bdb7dba085193ad47308e1676a"
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


# Eisenstein integers are represented by a+b*omega, omega^2=omega-1.
def e_mul(left, right):
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c + b * d


def e_conj(value):
    a, b = value
    return a + b, -b


def canonical_row(row):
    return min(tuple(e_mul(unit, value) for value in row) for unit in UNITS)


# Exact certificate arithmetic uses p+q*s with s^2=-3.  This deliberately
# differs from the target checker's {1,omega} representation.
QZERO = (Fraction(0), Fraction(0))
QONE = (Fraction(1), Fraction(0))


def q_add(left, right):
    return left[0] + right[0], left[1] + right[1]


def q_mul(left, right):
    return (
        left[0] * right[0] - 3 * left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def q_scale(value, scalar):
    scalar = Fraction(scalar)
    return value[0] * scalar, value[1] * scalar


def q_conj(value):
    return value[0], -value[1]


def q_from_e(value):
    a, b = value
    return Fraction(2 * a + b, 2), Fraction(b, 2)


def p_add(left, right, scale=1):
    result = dict(left)
    for monomial, coefficient in right.items():
        value = q_add(result.get(monomial, QZERO), q_scale(coefficient, scale))
        if value == QZERO:
            result.pop(monomial, None)
        else:
            result[monomial] = value
    return result


def p_mul(left, right):
    result = {}
    for (i, j), a in left.items():
        for (k, l), b in right.items():
            monomial = i + k, j + l
            result[monomial] = q_add(
                result.get(monomial, QZERO), q_mul(a, b)
            )
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient != QZERO}


def p_scalar(poly, coefficient):
    return {
        monomial: value
        for monomial, old in poly.items()
        if (value := q_mul(coefficient, old)) != QZERO
    }


def p_power(poly, exponent):
    result = {(0, 0): QONE}
    for _ in range(exponent):
        result = p_mul(result, poly)
    return result


def p_conj(poly):
    return {monomial: q_conj(value) for monomial, value in poly.items()}


PONE = {(0, 0): QONE}
PU = {(1, 0): QONE}
PV = {(0, 1): QONE}
ONE_PLUS_U = p_add(PONE, PU)
ONE_PLUS_V = p_add(PONE, PV)
DENOMINATOR = p_mul(ONE_PLUS_U, ONE_PLUS_V)
DENOMINATOR_SQUARED = p_mul(DENOMINATOR, DENOMINATOR)


def primitive_integer_polynomial(poly):
    integer = {}
    for monomial, (real, imag) in poly.items():
        require(imag == 0 and real.denominator == 1, "norm polynomial is integral and real")
        if real:
            integer[monomial] = real.numerator
    require(integer, "nonzero event polynomial")
    divisor = 0
    for coefficient in integer.values():
        divisor = gcd(divisor, abs(coefficient))
    if integer[max(integer)] < 0:
        divisor = -divisor
    return tuple(
        (i, j, coefficient // divisor)
        for (i, j), coefficient in sorted(integer.items())
    )


def event_polynomial(row):
    # Form 2*sum row_j*z^j directly in Q(s)[x,y], where z=x+s*y.
    z = {(1, 0): QONE, (0, 1): (Fraction(0), Fraction(1))}
    total = {}
    for exponent, coefficient in enumerate(row):
        total = p_add(
            total,
            p_scalar(p_power(z, exponent), q_scale(q_from_e(coefficient), 2)),
        )
    norm_minus_four = p_add(p_mul(total, p_conj(total)), {(0, 0): QONE}, -4)
    return primitive_integer_polynomial(norm_minus_four)


def curve_inventory():
    rows = sorted(
        {
            canonical_row(row)
            for row in product(DISPLACEMENTS, repeat=5)
            if any(value != ZERO_E for value in row)
        }
    )
    require(len(rows) == 2801, "2,801 unit-normalized displacement rows")
    circle = ((0, 0, -1), (0, 2, 3), (2, 0, 1))
    event_to_row = {}
    monomial_by_position = Counter()
    for row in rows:
        support = [index for index, value in enumerate(row) if value != ZERO_E]
        if len(support) == 1:
            monomial_by_position[support[0]] += 1
            continue
        event = event_polynomial(row)
        require(event != circle, "nonmonomial event is not the radial circle")
        require(event not in event_to_row, "noncircle row-to-event injectivity")
        event_to_row[event] = row
    require(monomial_by_position == Counter({i: 1 for i in range(5)}), "five monomial classes")
    require(len(event_to_row) == 2796, "2,796 noncircle events")
    factors = sorted(tuple(event_to_row) + (circle,))
    require(len(factors) == 2797 and factors.index(circle) == 342, "stable curve IDs")
    require(digest(factors) == EXPECTED_INVENTORY_SHA256, "curve inventory digest")
    factor_id = {factor: index for index, factor in enumerate(factors)}
    row_by_curve = {factor_id[event]: row for event, row in event_to_row.items()}
    return factors, row_by_curve


def gf4_mul(left, right):
    # Bit-polynomial multiplication modulo t^2+t+1.
    product_value = 0
    for bit in range(2):
        if right & (1 << bit):
            product_value ^= left << bit
    if product_value & 4:
        product_value ^= 7
    return product_value


def gf4_dot(left, right):
    result = 0
    for a, b in zip(left, right):
        result ^= gf4_mul(a, b)
    return result


def gf4_projective(vector):
    pivot = next(value for value in vector if value)
    inverse = next(value for value in (1, 2, 3) if gf4_mul(pivot, value) == 1)
    return tuple(gf4_mul(inverse, value) for value in vector)


def signature(row):
    residues = tuple((a & 1) | ((b & 1) << 1) for a, b in row)
    normal = residues[1:]
    normalized = gf4_projective(normal)
    pivot = next(value for value in normal if value)
    inverse = next(value for value in (1, 2, 3) if gf4_mul(pivot, value) == 1)
    return normalized, gf4_mul(inverse, residues[0])


def plane_covers():
    normals = sorted(
        {
            gf4_projective(pair)
            for pair in product(range(4), repeat=2)
            if any(pair)
        }
    )
    require(len(normals) == 5, "five directions in the affine F4 plane")
    points = tuple(product(range(4), repeat=2))
    domains = [tuple(range(1, 4)) if sum(value != 0 for value in normal) == 1 else tuple(range(4)) for normal in normals]
    covers = []
    for constants in product(*domains):
        sections = tuple(zip(normals, constants))
        covered = {
            point
            for point in points
            if any(gf4_dot(normal, point) == constant for normal, constant in sections)
        }
        if len(covered) == 16:
            covers.append(tuple(sorted(sections)))
    require(len(covers) == len(set(covers)) == 9, "nine realized five-section covers")
    return tuple(sorted(covers))


def normalized_census(row_by_curve):
    buckets = defaultdict(list)
    for curve, row in row_by_curve.items():
        buckets[signature(row)].append(curve)
    for values in buckets.values():
        values.sort()
    require(len(buckets) == 336, "336 realized affine hyperplanes")

    patterns = []
    quintets = []
    counts = Counter()
    transcript = []
    for i, j in combinations(range(1, 5), 2):
        e_i = tuple(int(index == i - 1) for index in range(4))
        e_j = tuple(int(index == j - 1) for index in range(4))
        for small_cover in plane_covers():
            pattern = []
            for (a, b), constant in small_cover:
                normal = tuple(a if index == i - 1 else b if index == j - 1 else 0 for index in range(4))
                pattern.append((normal, constant))
            pattern = tuple(sorted(pattern))
            require(sorted(len(buckets[item]) for item in pattern) == [2, 2, 2, 4, 4], "lift bucket sizes")
            patterns.append(pattern)
            anchor_i = next(index for index, item in enumerate(pattern) if item[0] == e_i)
            anchor_j = next(index for index, item in enumerate(pattern) if item[0] == e_j)
            for lift in product(*(buckets[item] for item in pattern)):
                first = row_by_curve[lift[anchor_i]]
                second = row_by_curve[lift[anchor_j]]
                alpha = e_mul(first[i], e_conj(first[0]))
                beta = e_mul(second[j], e_conj(second[0]))
                require(alpha in UNITS and beta in UNITS, "unit anchor phases")
                normalized = []
                for curve in lift:
                    row = row_by_curve[curve]
                    require(
                        all(value == ZERO_E for index, value in enumerate(row) if index not in (0, i, j)),
                        "two-coordinate support",
                    )
                    normalized.append(
                        canonical_row(
                            (
                                row[0],
                                e_mul(row[i], e_conj(alpha)),
                                e_mul(row[j], e_conj(beta)),
                            )
                        )
                    )
                key = tuple(sorted(normalized))
                quintet = tuple(sorted(lift))
                counts[key] += 1
                quintets.append(quintet)
                transcript.append((quintet, key))

    patterns.sort()
    quintets.sort()
    transcript.sort()
    require(len(patterns) == len(set(patterns)) == 54, "54 embedded pencils")
    require(len(quintets) == len(set(quintets)) == 6912, "6,912 distinct lifts")
    require(len(counts) == 32 and set(counts.values()) == {216}, "32 equipopulous normal forms")
    keys = sorted(counts)
    anchors = {((-1, 0), (-1, 0), (0, 0)), ((-1, 0), (0, 0), (-1, 0))}
    require(all(anchors <= set(key) for key in keys), "two normalized anchors")
    require(digest(patterns) == EXPECTED_PATTERNS_SHA256, "pencil-pattern digest")
    require(digest(quintets) == EXPECTED_QUINTETS_SHA256, "quintet digest")
    require(digest(keys) == EXPECTED_FORMS_SHA256, "normal-form digest")
    require(digest(transcript) == EXPECTED_TRACE_SHA256, "entrywise normalization digest")
    return patterns, quintets, keys


def row_equations(rows):
    equations = []
    for raw_a, raw_b, raw_c in rows:
        a, b, c = map(q_from_e, (raw_a, raw_b, raw_c))
        linear = p_add(p_add({(0, 0): a}, p_scalar(PU, b)), p_scalar(PV, c))
        opposite = p_add(
            p_add(
                p_scalar(DENOMINATOR, q_conj(a)),
                p_scalar(p_mul(PU, ONE_PLUS_V), q_conj(b)),
                -1,
            ),
            p_scalar(p_mul(PV, ONE_PLUS_U), q_conj(c)),
            -1,
        )
        equation = p_add(p_mul(linear, opposite), DENOMINATOR, -1)
        if equation:
            equations.append(equation)
    require(len(equations) == 3, "two anchors eliminated and three cubics remain")
    return equations


def decode_multiplier(terms):
    require(terms == sorted(terms), "canonical multiplier ordering")
    result = {}
    for i, j, a, b, denominator in terms:
        require(
            all(type(value) is int for value in (i, j, a, b, denominator))
            and i >= 0
            and j >= 0
            and denominator > 0
            and (a or b),
            "exact multiplier term",
        )
        require((i, j) not in result, "distinct multiplier monomials")
        result[i, j] = (
            Fraction(2 * a + b, 2 * denominator),
            Fraction(b, 2 * denominator),
        )
    return result


def diagonal_remainder(poly):
    values = {}
    for (i, j), coefficient in poly.items():
        values[i + j] = q_add(values.get(i + j, QZERO), coefficient)
    values = {degree: value for degree, value in values.items() if value != QZERO}
    # Reduce by 4*t^2+t+1.
    while values and max(values) >= 2:
        degree = max(values)
        leading = values.pop(degree)
        correction = q_scale(leading, Fraction(-1, 4))
        for lower in (degree - 1, degree - 2):
            value = q_add(values.get(lower, QZERO), correction)
            if value == QZERO:
                values.pop(lower, None)
            else:
                values[lower] = value
    return values


def check_certificate(certificate_path, keys):
    raw = Path(certificate_path).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_CERTIFICATE_SHA256, "certificate byte digest")
    certificate = json.loads(raw)
    require(certificate.get("schema") == "hn-radix-two-coordinate-identities-v1", "certificate schema")
    forms = certificate.get("normal_forms")
    require(isinstance(forms, list) and len(forms) == len(keys) == 32, "complete normal forms")
    claims = Counter()
    degree_histogram = Counter()
    checked = 0
    exceptional_equations = None
    for index, (entry, key) in enumerate(zip(forms, keys)):
        declared_rows = tuple(
            tuple(tuple(coefficient) for coefficient in row)
            for row in entry.get("normalized_rows", [])
        )
        require(declared_rows == key, "certificate bound to independently reconstructed form")
        equations = row_equations(key)
        expected = (
            (
                ("difference", p_mul(DENOMINATOR_SQUARED, p_add(PU, PV, -1))),
                ("norm", p_mul(DENOMINATOR_SQUARED, p_add(p_add(PONE, PV), p_scalar(p_mul(PV, PV), (Fraction(4), Fraction(0)))))),
            )
            if index == 0
            else (("contradiction", DENOMINATOR_SQUARED),)
        )
        identities = entry.get("identities")
        require(isinstance(identities, list) and len(identities) == len(expected), "identity list")
        for identity, (expected_claim, target) in zip(identities, expected):
            claim = identity.get("claim")
            require(claim == expected_claim, "identity target label")
            multipliers = identity.get("multipliers")
            require(isinstance(multipliers, list) and len(multipliers) == 3, "three multipliers")
            degree_bound = identity.get("multiplier_degree_bound")
            total = {}
            for encoded, equation in zip(multipliers, equations):
                multiplier = decode_multiplier(encoded)
                require(all(i + j <= degree_bound for i, j in multiplier), "declared degree bound")
                total = p_add(total, p_mul(multiplier, equation))
            require(total == target, "exact identity in Q(sqrt(-3))[U,V]")
            claims[claim] += 1
            degree_histogram[degree_bound] += 1
            checked += 1
        if index == 0:
            exceptional_equations = equations

    expected_exceptional = (
        ((-1, 0), (-1, 0), (0, 0)),
        ((-1, 0), (-1, 1), (0, -1)),
        ((-1, 0), (0, -1), (-1, 1)),
        ((-1, 0), (0, 0), (-1, 0)),
        ((0, 0), (-1, 0), (-1, 0)),
    )
    require(keys[0] == expected_exceptional, "identified exceptional form")
    require(all(not diagonal_remainder(equation) for equation in exceptional_equations), "exceptional free-vector solutions retained")
    require(diagonal_remainder(DENOMINATOR_SQUARED), "exceptional denominator remains nonzero")
    for i, j in combinations(range(1, 5), 2):
        d = j - i
        require(Fraction(1, 4) ** d != 1, "common-radix power contradiction")
    require(claims == {"contradiction": 31, "difference": 1, "norm": 1}, "33 certificate identities")
    return checked, dict(sorted(degree_histogram.items()))


def conditional_frontier(interface_path, factors, row_by_curve):
    raw = Path(interface_path).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_ORBIT_INTERFACE_FILE_SHA256, "h4177 interface file digest")
    data = json.loads(raw)
    require(digest(data) == EXPECTED_ORBIT_INTERFACE_CANONICAL_SHA256, "h4177 interface canonical digest")
    require(data.get("schema") == "hn-radix-five-active-orbit-interface-v1", "h4177 interface schema")
    require(data.get("curve_inventory_sha256") == EXPECTED_INVENTORY_SHA256, "h4177 curve inventory")
    modes = data.get("pair_modes")
    require(set(modes) == {
        "exact_five_compatible",
        "parallel_signatures_require_at_least_six",
        "unrealized_pencil_type_requires_at_least_six",
    }, "h4177 mode names")
    exact = modes["exact_five_compatible"]
    others = modes["parallel_signatures_require_at_least_six"] + modes["unrealized_pencil_type_requires_at_least_six"]
    all_rows = exact + others
    require(len(all_rows) == 131356 and len({tuple(row[:2]) for row in all_rows}) == 131356, "conditional global pair partition")
    supports = {
        curve: {index for index, value in enumerate(row) if index and value != ZERO_E}
        for curve, row in row_by_curve.items()
    }
    moved = [row for row in exact if len(supports[row[0]] | supports[row[1]]) == 2]
    retained = [row for row in exact if len(supports[row[0]] | supports[row[1]]) != 2]
    # The support-union criterion identifies affected rows only after restricting
    # to h4177's exact-five mode.  Other modes can also have two-coordinate
    # support when their signatures are parallel or their full pencil is absent.
    degrees = [max(i + j for i, j, _ in factor) for factor in factors]
    for a, b, mask, bound, allowance in all_rows:
        stabilizer = int(mask).bit_count()
        require(stabilizer > 0, "nonempty stabilizer mask")
        require(bound == degrees[a] * degrees[b] // 2, "imported bidegree-bound arithmetic")
        require(allowance == bound // stabilizer, "imported free-action allowance arithmetic")
    require(len(moved) == 192, "192 conditionally moved pair systems")
    require(Counter(int(row[2]).bit_count() for row in moved) == {1: 164, 2: 28}, "moved stabilizer histogram")
    require(digest(moved) == "8eb2ca8fbd0342f6939d57cf60d3f32bedda21ac2e6cf8dc6079d89a3afbb73a", "moved-row digest")
    require(digest(retained) == "93ee55009b5a19eb2ee25f928cb26ad31b6fc4a0bfbbd475fe9461fb5d660112", "retained-row digest")
    return {
        "status": "conditional_on_h4177_and_its_h4117/h4175_dependencies",
        "moved_pairs": len(moved),
        "moved_stabilizer_histogram": {str(k): v for k, v in sorted(Counter(int(row[2]).bit_count() for row in moved).items())},
        "moved_product_surface_allowance": sum(row[3] for row in moved),
        "moved_nonfour_orbit_allowance": sum(row[4] for row in moved),
        "remaining_exact_five_pairs": len(retained),
        "remaining_exact_five_orbit_allowance": sum(row[4] for row in retained),
        "now_at_least_six_pairs": len(others) + len(moved),
        "now_at_least_six_orbit_allowance": sum(row[4] for row in others) + sum(row[4] for row in moved),
        "global_pairs_removed": 0,
    }


def run(certificate_path, interface_path=None):
    factors, row_by_curve = curve_inventory()
    patterns, quintets, keys = normalized_census(row_by_curve)
    identities, degree_histogram = check_certificate(certificate_path, keys)
    result = {
        "verdict_scope": "standalone_two_coordinate_nonconcurrence",
        "curve_inventory": len(factors),
        "coordinate_pairs": 6,
        "realized_pencils": len(patterns),
        "lifted_quintets": len(quintets),
        "normal_forms": len(keys),
        "lifts_per_normal_form": 216,
        "identities_checked_in_sqrt_minus_three_basis": identities,
        "multiplier_degree_histogram": {str(k): v for k, v in degree_histogram.items()},
        "direct_denominator_forms": 31,
        "common_radix_power_forms": 1,
        "complex_affine_concurrences": 0,
        "monotone_under_additional_active_curves": True,
        "complete_A5_architecture_closed": False,
        "record_improvement": False,
    }
    if interface_path is not None:
        result["conditional_frontier"] = conditional_frontier(interface_path, factors, row_by_curve)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=TARGET / "certificate.json")
    parser.add_argument("--orbit-interface", type=Path)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = run(args.certificate, args.orbit_interface)
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        require(result == expected, "independent expected result")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
