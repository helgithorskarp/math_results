#!/usr/bin/env python3
"""Independent exact verifier for the 800-system viability certificate.

The checker uses only the CPython standard library.  It recomputes reduced
lexicographic Groebner bases with Buchberger's algorithm, squarefree
projections, Sturm root counts, factor predicates, and collision predicates.
"""
from collections import Counter
from fractions import Fraction as Q
from functools import reduce
from itertools import combinations, product
from math import comb, gcd
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SYMMETRY = ROOT / "hadwiger_nelson_three_wheel_symmetry_frontier"
SYMMETRY_CERTIFICATE_SHA256 = "14e2a5e3fc00af36d4ef57b6a8fdd964450633b0ab76f0f2783094172ec69132"
CLOSURE = ROOT / "hadwiger_nelson_three_wheel_closure"
CLOSURE_CERTIFICATE_SHA256 = "301ca9a0ee089dfa10ba1b7d29f4e0a23d2e446a2592101dcd60e6cf2a1e6385"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def load_symmetry_verifier():
    sys.path.insert(0, str(SYMMETRY))
    spec = importlib.util.spec_from_file_location("hn_three_wheel_symmetry_verify", SYMMETRY / "verify.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Univariate polynomials are dense coefficient lists, constant first.
def utrim(poly):
    poly = list(poly)
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def uadd(left, right, scale=Q(1)):
    out = [Q(0)] * max(len(left), len(right))
    for i, value in enumerate(left):
        out[i] += value
    for i, value in enumerate(right):
        out[i] += scale * value
    return utrim(out)


def umul(left, right):
    if not left or not right:
        return []
    out = [Q(0)] * (len(left) + len(right) - 1)
    for i, value in enumerate(left):
        for j, other in enumerate(right):
            out[i + j] += value * other
    return utrim(out)


def uscale(poly, scale):
    return utrim([scale * value for value in poly])


def udivmod(dividend, divisor):
    need(divisor, "zero polynomial divisor")
    remainder = list(dividend)
    quotient = [Q(0)] * max(0, len(dividend) - len(divisor) + 1)
    while len(remainder) >= len(divisor):
        offset = len(remainder) - len(divisor)
        coefficient = remainder[-1] / divisor[-1]
        quotient[offset] += coefficient
        for i, value in enumerate(divisor):
            remainder[i + offset] -= coefficient * value
        remainder = utrim(remainder)
    return utrim(quotient), remainder


def umonic(poly):
    need(poly, "zero polynomial is not monic")
    return uscale(poly, Q(1) / poly[-1])


def ugcd(left, right):
    left, right = utrim(left), utrim(right)
    while right:
        _, remainder = udivmod(left, right)
        left, right = right, remainder
    return umonic(left) if left else []


def uxgcd(left, right):
    old_r, r = list(left), list(right)
    old_s, s = [Q(1)], []
    old_t, tt = [], [Q(1)]
    while r:
        quotient, remainder = udivmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, uadd(old_s, umul(quotient, s), Q(-1))
        old_t, tt = tt, uadd(old_t, umul(quotient, tt), Q(-1))
    scale = Q(1) / old_r[-1]
    return uscale(old_r, scale), uscale(old_s, scale), uscale(old_t, scale)


def uderivative(poly):
    return utrim([i * poly[i] for i in range(1, len(poly))])


def usqf(poly):
    common = ugcd(poly, uderivative(poly))
    quotient, remainder = udivmod(poly, common)
    need(not remainder, "squarefree division")
    return umonic(quotient)


def ueval(poly, value):
    result = Q(0)
    for coefficient in reversed(poly):
        result = result * value + coefficient
    return result


def primitive_integers(poly):
    poly = utrim(poly)
    need(poly, "empty primitive polynomial")
    denominator = 1
    for value in poly:
        denominator = denominator * value.denominator // gcd(denominator, value.denominator)
    integers = [int(value * denominator) for value in poly]
    common = reduce(gcd, (abs(value) for value in integers))
    integers = [value // common for value in integers]
    if integers[-1] < 0:
        integers = [-value for value in integers]
    return integers


def sturm(poly):
    rows = [utrim(poly), uderivative(poly)]
    while rows[-1]:
        _, remainder = udivmod(rows[-2], rows[-1])
        if not remainder:
            break
        rows.append(uscale(remainder, Q(-1)))
    return rows


def variations(signs):
    signs = [sign for sign in signs if sign]
    return sum(left != right for left, right in zip(signs, signs[1:]))


def sign(value):
    return 1 if value > 0 else -1 if value < 0 else 0


def sturm_at(rows, value):
    return variations([sign(ueval(row, value)) for row in rows])


def sturm_infinity(rows, positive):
    signs = []
    for row in rows:
        value = sign(row[-1])
        if not positive and (len(row) - 1) % 2:
            value = -value
        signs.append(value)
    return variations(signs)


def real_root_count(poly):
    rows = sturm(poly)
    return sturm_infinity(rows, False) - sturm_infinity(rows, True)


def check_intervals(poly, encoded):
    rows = sturm(poly)
    intervals = []
    for item in encoded:
        need(type(item) is list and len(item) == 2, "interval schema")
        left, right = map(Q, item)
        need(left <= right, "ordered interval")
        if left == right:
            need(ueval(poly, left) == 0, "singleton rational root")
        else:
            need(ueval(poly, left) and ueval(poly, right), "nonroot interval endpoints")
            need(sturm_at(rows, left) - sturm_at(rows, right) == 1, "isolating interval")
        intervals.append((left, right))
    ordered = sorted(intervals)
    need(intervals == ordered, "ordered isolating intervals")
    # Equal singleton intervals pass the endpoint-order test below but
    # count the same rational root twice. Root counts require distinct roots.
    need(len(set(intervals)) == len(intervals), "distinct isolating intervals")
    need(all(left[1] <= right[0] for left, right in zip(intervals, intervals[1:])),
         "disjoint isolating intervals")
    need(len(intervals) == real_root_count(poly), "complete real-root coverage")
    return intervals


# Bivariate polynomials use sparse (y exponent, t exponent) dictionaries.
def bclean(poly):
    return {monomial: coefficient for monomial, coefficient in poly.items() if coefficient}


def badd(left, right, scale=Q(1)):
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, Q(0)) + scale * coefficient
    return bclean(out)


def bmonomial_multiply(poly, monomial, coefficient):
    return bclean({(i + monomial[0], j + monomial[1]): value * coefficient
                   for (i, j), value in poly.items()})


def bmonic(poly):
    leading = poly[max(poly)]
    return {monomial: coefficient / leading for monomial, coefficient in poly.items()}


def breduce(poly, basis):
    poly = dict(poly)
    remainder = {}
    while poly:
        monomial = max(poly)
        coefficient = poly[monomial]
        for divisor in basis:
            leading = max(divisor)
            if monomial[0] >= leading[0] and monomial[1] >= leading[1]:
                multiple = (monomial[0] - leading[0], monomial[1] - leading[1])
                scaled = bmonomial_multiply(divisor, multiple, coefficient / divisor[leading])
                poly = badd(poly, scaled, Q(-1))
                break
        else:
            remainder[monomial] = coefficient
            del poly[monomial]
    return bclean(remainder)


def spolynomial(left, right):
    lm_left, lm_right = max(left), max(right)
    common = (max(lm_left[0], lm_right[0]), max(lm_left[1], lm_right[1]))
    first = bmonomial_multiply(left, (common[0] - lm_left[0], common[1] - lm_left[1]),
                               Q(1) / left[lm_left])
    second = bmonomial_multiply(right, (common[0] - lm_right[0], common[1] - lm_right[1]),
                                Q(-1) / right[lm_right])
    return badd(first, second)


def groebner(generators):
    basis = []
    for generator in generators:
        remainder = breduce(generator, basis)
        if remainder:
            basis.append(bmonic(remainder))
    pairs = [(i, j) for i in range(len(basis)) for j in range(i)]
    while pairs:
        i, j = pairs.pop(0)
        remainder = breduce(spolynomial(basis[i], basis[j]), basis)
        if remainder:
            remainder = bmonic(remainder)
            index = len(basis)
            basis.append(remainder)
            pairs.extend((index, other) for other in range(index))

    minimal = []
    for i, row in enumerate(basis):
        leading = max(row)
        if any(i != j and leading != max(other)
               and leading[0] >= max(other)[0] and leading[1] >= max(other)[1]
               for j, other in enumerate(basis)):
            continue
        if any(max(other) == leading for other in minimal):
            continue
        minimal.append(row)
    reduced = [bmonic(breduce(row, minimal[:i] + minimal[i + 1:]))
               for i, row in enumerate(minimal)]
    reduced.sort(key=max, reverse=True)
    return reduced


def shear_factor(factor, shear):
    result = {}
    for (xdegree, ydegree), coefficient in factor.items():
        for k in range(xdegree + 1):
            monomial = ydegree + k, xdegree - k
            value = Q(coefficient * comb(xdegree, k) * (-shear) ** k)
            result[monomial] = result.get(monomial, Q(0)) + value
    return bclean(result)


def coefficient_in_y(poly, ydegree):
    degree = max((j for (i, j) in poly if i == ydegree), default=-1)
    if degree < 0:
        return []
    return utrim([poly.get((ydegree, j), Q(0)) for j in range(degree + 1)])


def qreduce(poly, modulus):
    return udivmod(poly, modulus)[1]


def qadd(left, right, modulus, scale=Q(1)):
    return qreduce(uadd(left, right, scale), modulus)


def qmul(left, right, modulus):
    return qreduce(umul(left, right), modulus)


def qinv(poly, modulus):
    common, inverse, _ = uxgcd(poly, modulus)
    need(common == [Q(1)], "noninvertible shape coefficient")
    return qreduce(inverse, modulus)


def quotient_value(factor, xvalue, yvalue, modulus):
    xpowers = [[Q(1)], xvalue, qmul(xvalue, xvalue, modulus)]
    ypowers = [[Q(1)], yvalue, qmul(yvalue, yvalue, modulus)]
    value = []
    for (i, j), coefficient in factor.items():
        term = qmul(xpowers[i], ypowers[j], modulus)
        value = qadd(value, term, modulus, Q(coefficient))
    return value


def cmul(left, right, modulus):
    real = qadd(qmul(left[0], right[0], modulus),
                qmul(left[1], right[1], modulus), modulus, Q(-3))
    imag = qadd(qmul(left[0], right[1], modulus),
                qmul(left[1], right[0], modulus), modulus)
    return real, imag


def cadd(left, right, modulus):
    return qadd(left[0], right[0], modulus), qadd(left[1], right[1], modulus)


def phi(value, modulus):
    square = qmul(value, value, modulus)
    denominator = qadd([Q(1)], square, modulus, Q(3))
    inverse = qinv(denominator, modulus)
    real = qmul(qadd([Q(1)], square, modulus, Q(-3)), inverse, modulus)
    imag = qmul(uscale(value, Q(2)), inverse, modulus)
    return real, imag


def eisenstein(pair):
    a, b = pair
    return [Q(2 * a + b, 2)], [Q(b, 2)]


def collision_value(displacements, xvalue, yvalue, modulus):
    U, V = phi(xvalue, modulus), phi(yvalue, modulus)
    d, e, f = map(eisenstein, displacements)
    return cadd(d, cadd(cmul(U, e, modulus), cmul(V, f, modulus), modulus), modulus)


def no_common_root(modulus, *values):
    common = modulus
    for value in values:
        common = ugcd(common, value)
    return len(common) == 1


def run(certificate_path):
    symmetry_bytes = (SYMMETRY / "certificate.json").read_bytes()
    need(hashlib.sha256(symmetry_bytes).hexdigest() == SYMMETRY_CERTIFICATE_SHA256,
         "symmetry certificate hash")
    need(hashlib.sha256((CLOSURE / "certificate.json").read_bytes()).hexdigest()
         == CLOSURE_CERTIFICATE_SHA256, "h4085 closure certificate hash")
    symmetry_certificate = json.loads(symmetry_bytes)
    symmetry = load_symmetry_verifier()
    source, factors, active, words, cover = symmetry.source_state()
    alignment = symmetry.alignment_ids(factors)
    pairs = symmetry_certificate["pair_orbit_representatives"]
    need(len(pairs) == 800, "representative pair count")
    nonzero = [difference for difference in source.D if difference != (0, 0)]
    collision_rows = sorted({source.canonical(row) for row in product(nonzero, repeat=3)})
    need(len(collision_rows) == 972, "collision row count")

    certificate_bytes = certificate_path.read_bytes()
    certificate = json.loads(certificate_bytes)
    need(certificate.get("schema") == "hn-three-wheel-exact-viability-v1", "certificate schema")
    need(certificate.get("source_symmetry_certificate_sha256") == SYMMETRY_CERTIFICATE_SHA256,
         "declared source hash")
    need(certificate.get("coordinate_convention") == "t=x+shear*y; A(t)*y+B(t)=0",
         "coordinate convention")
    pair_rows = certificate.get("pair_rows")
    need(type(pair_rows) is list and len(pair_rows) == len(pairs), "pair row count")

    outcome_counts = Counter()
    shear_counts = Counter()
    real_embedding_counts = Counter()
    survivor_pairs = []
    survivor_fields = []
    total_projection_degree = 0
    total_components = 0
    empty_systems = 0

    for pair_index, (pair, row) in enumerate(zip(pairs, pair_rows)):
        need(row.get("pair") == pair, "pair order")
        shear = row.get("shear")
        need(type(shear) is int and 0 <= shear <= 2, "shear range")
        shear_counts[shear] += 1
        basis = groebner([shear_factor(factors[factor_id], shear) for factor_id in pair])
        components = row.get("components")
        need(type(components) is list, "component list")
        if len(basis) == 1 and max(basis[0]) == (0, 0):
            need(basis[0] == {(0, 0): Q(1)}, "unit Groebner basis")
            need(set(row) == {"pair", "shear", "components"} and not components,
                 "empty system row")
            empty_systems += 1
            continue

        need(len(basis) == 2, "two-row shape basis")
        relation, projection_with_multiplicity = basis
        need(max(i for i, _ in relation) == 1 and all(i == 0 for i, _ in projection_with_multiplicity),
             "shape basis degrees")
        A = coefficient_in_y(relation, 1)
        B = coefficient_in_y(relation, 0)
        projection = coefficient_in_y(projection_with_multiplicity, 0)
        squarefree = usqf(projection)
        need(ugcd(A, squarefree) == [Q(1)], "shape denominator coprimality")
        need(row.get("relation_a") == [str(value) for value in A], "relation A")
        need(row.get("relation_b") == [str(value) for value in B], "relation B")
        need(row.get("squarefree_projection") == primitive_integers(squarefree),
             "squarefree projection")
        total_projection_degree += len(squarefree) - 1

        component_polynomials = []
        for component in components:
            encoded = component.get("polynomial")
            need(type(encoded) is list and len(encoded) >= 2
                 and all(type(value) is int for value in encoded), "component polynomial")
            modulus = umonic(list(map(Q, encoded)))
            need(encoded == primitive_integers(modulus), "primitive component encoding")
            component_polynomials.append(modulus)
        product_polynomial = [Q(1)]
        for modulus in component_polynomials:
            product_polynomial = umul(product_polynomial, modulus)
        need(umonic(product_polynomial) == squarefree, "complete component factorization")
        need(all(ugcd(left, right) == [Q(1)]
                 for left, right in combinations(component_polynomials, 2)),
             "coprime projection components")

        inverse_A = qinv(A, squarefree)
        # This pair-level inverse is not used below, but proves one rational
        # shape relation covers every distinct complex solution.
        need(qmul(A, inverse_A, squarefree) == [Q(1)], "global shape inverse")

        pair_survives = False
        for component, modulus in zip(components, component_polynomials):
            total_components += 1
            intervals = check_intervals(modulus, component.get("intervals"))
            outcome = component.get("outcome")
            need(outcome in {"no_real_roots", "alignment", "proper_word", "collision", "survivor"},
                 "component outcome")
            outcome_counts[outcome] += 1
            real_embedding_counts[outcome] += len(intervals)
            if not intervals:
                need(outcome == "no_real_roots" and set(component) == {"polynomial", "intervals", "outcome"},
                     "nonreal component outcome")
                continue
            need(outcome != "no_real_roots", "real component marked nonreal")

            inverse = qinv(A, modulus)
            yvalue = qmul(uscale(B, Q(-1)), inverse, modulus)
            xvalue = qadd([Q(0), Q(1)], yvalue, modulus, Q(-shear))

            if outcome == "alignment":
                factor_id = component.get("alignment_factor_id")
                need(type(factor_id) is int and factor_id in alignment, "alignment witness id")
                need(not quotient_value(factors[factor_id], xvalue, yvalue, modulus),
                     "alignment witness identity")
            elif outcome == "proper_word":
                word_index = component.get("proper_word_index")
                need(type(word_index) is int and 0 <= word_index < len(words), "proper word index")
                for factor_id in words[word_index]["bad"]:
                    value = quotient_value(factors[factor_id], xvalue, yvalue, modulus)
                    need(no_common_root(modulus, value), "proper word bad-factor exclusion")
            elif outcome == "collision":
                displacements = component.get("collision_displacements")
                need(type(displacements) is list and len(displacements) == 3, "collision witness")
                displacements = tuple(tuple(value) for value in displacements)
                need(displacements in collision_rows, "canonical collision row")
                value = collision_value(displacements, xvalue, yvalue, modulus)
                need(not value[0] and not value[1], "collision identity")
            else:
                pair_survives = True
                zero_ids = component.get("zero_factor_ids")
                need(type(zero_ids) is list and zero_ids == sorted(set(zero_ids)), "zero factor ids")
                actual_zero = [factor_id for factor_id, factor in enumerate(factors)
                               if not quotient_value(factor, xvalue, yvalue, modulus)]
                need(zero_ids == actual_zero, "complete identically-zero factor set")
                witnesses = component.get("failure_factor_ids")
                need(type(witnesses) is list and len(witnesses) == len(words), "failure witnesses")
                for word, factor_id in zip(words, witnesses):
                    need(type(factor_id) is int and factor_id in word["bad"], "bad-factor witness id")
                    need(not quotient_value(factors[factor_id], xvalue, yvalue, modulus),
                         "bad-factor witness identity")
                for factor_id in alignment:
                    value = quotient_value(factors[factor_id], xvalue, yvalue, modulus)
                    need(no_common_root(modulus, value), "survivor nonalignment")
                for displacements in collision_rows:
                    real, imag = collision_value(displacements, xvalue, yvalue, modulus)
                    need(no_common_root(modulus, real, imag), "survivor injectivity")
                survivor_fields.append({
                    "pair_index": pair_index,
                    "factor_pair": pair,
                    "shear": shear,
                    "defining_polynomial": component["polynomial"],
                    "real_intervals": component["intervals"],
                    "relation_a": row["relation_a"],
                    "relation_b": row["relation_b"],
                    "zero_factor_ids": zero_ids,
                })
        if pair_survives:
            survivor_pairs.append(pair_index)

    survivor_embeddings = real_embedding_counts["survivor"]
    survivor_fields_encoded = json.dumps(
        survivor_fields, separators=(",", ":"), sort_keys=True).encode()
    return {
        "status": "THREE_WHEEL_800_SYSTEM_FRONTIER_FILTERED_EXACTLY",
        "record_improvement": False,
        "source_symmetry_certificate_sha256": SYMMETRY_CERTIFICATE_SHA256,
        "certificate_sha256": hashlib.sha256(certificate_bytes).hexdigest(),
        "representative_pair_systems": len(pairs),
        "empty_complex_systems": empty_systems,
        "shape_shear_histogram": {str(key): value for key, value in sorted(shear_counts.items())},
        "squarefree_projection_degree_sum": total_projection_degree,
        "projection_components": total_components,
        "component_outcome_histogram": dict(sorted(outcome_counts.items())),
        "real_embedding_outcome_histogram": dict(sorted(real_embedding_counts.items())),
        "real_embeddings_total": sum(real_embedding_counts.values()),
        "injective_all_thirteen_failure_pair_systems": len(survivor_pairs),
        "injective_all_thirteen_failure_pair_indices": survivor_pairs,
        "injective_all_thirteen_failure_field_components": len(survivor_fields),
        "injective_all_thirteen_failure_real_embeddings": survivor_embeddings,
        "original_thirteen_word_residual_physical_class_upper_bound": survivor_embeddings,
        "architecture_closed_by_h4085": True,
        "current_unresolved_physical_classes": 0,
        "h4085_closure_certificate_sha256": CLOSURE_CERTIFICATE_SHA256,
        "survivor_field_interface_sha256": hashlib.sha256(survivor_fields_encoded).hexdigest(),
        "survivor_field_summary": [
            {"pair_index": field["pair_index"],
             "degree": len(field["defining_polynomial"]) - 1,
             "real_embeddings": len(field["real_intervals"])}
            for field in survivor_fields
        ],
        "physical_order_of_every_survivor": 343,
        "chromatic_solver_calls": 0,
        "new_chromatic_decisions": False,
        "external_peer_review_claimed": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    output = run(args.certificate)
    if args.check_expected:
        need(output == json.loads((HERE / "EXPECTED.json").read_text()), "expected output")
    print(json.dumps(output, indent=2, sort_keys=True))
