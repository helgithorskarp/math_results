#!/usr/bin/env python3
"""Portable independent verifier for the A5 degree-two-anchor root census."""

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import json
from math import gcd, lcm
from pathlib import Path
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ORBIT = ROOT / "hadwiger_nelson_radix_five_active_orbits"
REVIEW_PATH = ROOT / "hadwiger_nelson_radix_four_active_closure_review1" / "independent_check.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ORBIT_CHECKER = load("degree_two_orbit_checker", ORBIT / "verify.py")
REVIEW = load("degree_two_inventory_checker", REVIEW_PATH)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def trim(poly):
    poly = list(poly)
    while poly and poly[-1] == 0:
        poly.pop()
    return tuple(poly)


def p_add(left, right, scale=Fraction(1)):
    result = [Fraction(0)] * max(len(left), len(right))
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += scale * value
    return trim(result)


def p_scale(poly, scale):
    return trim(Fraction(scale) * value for value in poly)


def p_mul(left, right):
    if not left or not right:
        return ()
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return trim(result)


def p_power(poly, exponent):
    result = (Fraction(1),)
    base = poly
    while exponent:
        if exponent & 1:
            result = p_mul(result, base)
        base = p_mul(base, base)
        exponent //= 2
    return result


def p_divrem(left, right):
    left = list(trim(left))
    right = trim(right)
    need(right, "polynomial division by zero")
    quotient = [Fraction(0)] * max(0, len(left) - len(right) + 1)
    while left and len(left) >= len(right):
        value = Fraction(left[-1]) / right[-1]
        shift = len(left) - len(right)
        quotient[shift] = value
        for index, coefficient in enumerate(right):
            left[index + shift] -= value * coefficient
        left = list(trim(left))
    return trim(quotient), trim(left)


def p_quotient(left, right):
    quotient, remainder = p_divrem(left, right)
    need(not remainder, "nonexact polynomial quotient")
    return quotient


def p_monic(poly):
    poly = trim(poly)
    need(poly, "zero monic polynomial")
    return p_scale(poly, Fraction(1) / poly[-1])


def p_gcd(left, right):
    left, right = trim(left), trim(right)
    while right:
        _, remainder = p_divrem(left, right)
        left, right = right, remainder
    return p_monic(left) if left else ()


def p_lcm(left, right):
    if not left or not right:
        return ()
    return p_monic(p_quotient(p_mul(left, right), p_gcd(left, right)))


def derivative(poly):
    return trim(Fraction(index) * value for index, value in enumerate(poly) if index)


def squarefree(poly):
    poly = trim(poly)
    if len(poly) <= 1:
        return (Fraction(1),)
    return p_monic(p_quotient(poly, p_gcd(poly, derivative(poly))))


def positive_normalize(poly):
    poly = trim(poly)
    if not poly:
        return ()
    return p_scale(poly, Fraction(1) / abs(poly[-1]))


def sign_at_infinity(poly, positive):
    sign = 1 if poly[-1] > 0 else -1
    if not positive and (len(poly) - 1) % 2:
        sign = -sign
    return sign


def variations(signs):
    return sum(left != right for left, right in zip(signs, signs[1:]))


def real_root_count(poly):
    poly = squarefree(poly)
    if len(poly) <= 1:
        return 0
    sequence = [positive_normalize(poly), positive_normalize(derivative(poly))]
    while len(sequence[-1]) > 1:
        _, remainder = p_divrem(sequence[-2], sequence[-1])
        need(remainder, "unexpected zero Sturm remainder")
        sequence.append(positive_normalize(p_scale(remainder, -1)))
    negative = variations([sign_at_infinity(poly, False) for poly in sequence])
    positive = variations([sign_at_infinity(poly, True) for poly in sequence])
    need(negative >= positive, "invalid Sturm variation")
    return negative - positive


def canonical_coefficients(poly):
    poly = trim(poly)
    need(poly, "zero canonical polynomial")
    denominator = lcm(*(value.denominator for value in poly))
    integers = [int(value * denominator) for value in poly]
    divisor = 0
    for value in integers:
        divisor = gcd(divisor, abs(value))
    need(divisor > 0, "zero polynomial content")
    integers = [value // divisor for value in integers]
    if integers[-1] < 0:
        integers = [-value for value in integers]
    return integers


def from_coefficients(coefficients):
    return trim(Fraction(value) for value in coefficients)


def d_add(left, right, scale=1):
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + scale * coefficient
        if not result[monomial]:
            del result[monomial]
    return result


def d_shift(poly, dx, dy, scale=1):
    return {(i + dx, j + dy): scale * value for (i, j), value in poly.items()}


def radix_powers():
    powers = [({(0, 0): 1}, {})]
    for _ in range(4):
        real, imaginary = powers[-1]
        powers.append(
            (
                d_add(d_shift(real, 1, 0), d_shift(imaginary, 0, 1), -3),
                d_add(d_shift(imaginary, 1, 0), d_shift(real, 0, 1)),
            )
        )
    return tuple(powers)


POWERS = radix_powers()


def collision_parts(row):
    real, imaginary = {}, {}
    for (a, b), (left, right) in zip(row, POWERS):
        real = d_add(real, left, 2 * a + b)
        real = d_add(real, right, -3 * b)
        imaginary = d_add(imaginary, left, b)
        imaginary = d_add(imaginary, right, 2 * a + b)
    return real, imaginary


def pullback(polynomial, degree, x_numerator, y_numerator):
    x_powers = [p_power(x_numerator, exponent) for exponent in range(degree + 1)]
    y_powers = [p_power(y_numerator, exponent) for exponent in range(degree + 1)]
    denominator_powers = [p_power((1, 0, 3), exponent) for exponent in range(degree + 1)]
    result = ()
    for i, j, coefficient in polynomial:
        term = p_mul(x_powers[i], y_powers[j])
        term = p_mul(term, denominator_powers[degree - i - j])
        result = p_add(result, term, Fraction(coefficient))
    return from_coefficients(canonical_coefficients(result))


def e_multiply(left, right):
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c + b * d


def e_conjugate(value):
    return value[0] + value[1], -value[1]


def e_norm(value):
    return value[0] * value[0] + value[0] * value[1] + value[1] * value[1]


def coordinate(value):
    return Fraction(2 * value[0] + value[1], 2), Fraction(value[1], 2)


def evaluate_sparse(polynomial, x, y):
    return sum(Fraction(value) * x**i * y**j for i, j, value in polynomial)


def collision_inventory(rows):
    result = set()
    for row in rows:
        reduced = list(row)
        while reduced and reduced[0] == (0, 0):
            reduced.pop(0)
        while reduced and reduced[-1] == (0, 0):
            reduced.pop()
        if len(reduced) > 1:
            result.add(REVIEW.canonical_row(tuple(reduced)))
    result = sorted(result)
    need(len(result) == 2400, "complete collision-row inventory")
    return result


def marker_for_center(center, collision_polynomials):
    center_x, center_y = coordinate(center)
    denominator = (Fraction(1), Fraction(0), Fraction(3))
    qx = (Fraction(1), Fraction(0), Fraction(-3))
    qy = (Fraction(0), Fraction(2))
    x_numerator = p_add(p_scale(denominator, center_x), qx)
    y_numerator = p_add(p_scale(denominator, center_y), qy)
    collision_marker = (Fraction(1),)
    for degree, real, imaginary in collision_polynomials:
        left = pullback(real, degree, x_numerator, y_numerator)
        right = pullback(imaginary, degree, x_numerator, y_numerator)
        common = squarefree(p_gcd(left, right))
        collision_marker = p_lcm(collision_marker, common)
    collision_marker = squarefree(collision_marker)

    y_minus_x = p_add(y_numerator, x_numerator, -1)
    y_plus_x = p_add(y_numerator, x_numerator)
    axis_marker = p_mul(y_numerator, p_mul(y_minus_x, y_plus_x))
    radial_marker = p_add(
        p_add(p_mul(x_numerator, x_numerator), p_mul(y_numerator, y_numerator), 3),
        p_mul(denominator, denominator),
        -1,
    )
    marker = squarefree(p_lcm(p_lcm(collision_marker, axis_marker), radial_marker))
    base_x, base_y = center_x - 1, center_y
    base_axis = base_y * (base_y - base_x) * (base_y + base_x) == 0
    base_radial = base_x**2 + 3 * base_y**2 == 1
    base_collision = any(
        evaluate_sparse(real, base_x, base_y) == 0
        and evaluate_sparse(imaginary, base_x, base_y) == 0
        for _, real, imaginary in collision_polynomials
    )
    record = {
        "center_eisenstein": list(center),
        "collision_marker": canonical_coefficients(collision_marker),
        "collision_marker_degree": len(collision_marker) - 1,
        "closed_marker": canonical_coefficients(marker),
        "closed_marker_degree": len(marker) - 1,
        "base_point_closed": base_axis or base_radial or base_collision,
        "base_point_on_axis": base_axis,
        "base_point_on_radial_circle": base_radial,
        "base_point_collision": base_collision,
    }
    return record, (x_numerator, y_numerator), marker


def select_pairs(interface, factors, rows_by_id):
    supports = {
        curve: {index for index, digit in enumerate(row) if index and digit != (0, 0)}
        for curve, row in rows_by_id.items()
    }
    degrees = [max(i + j for i, j, _ in factor) for factor in factors]
    selected = []
    for record in interface["pair_modes"]["exact_five_compatible"]:
        if len(supports[record[0]] | supports[record[1]]) <= 2:
            continue
        anchors = [
            curve
            for curve in record[:2]
            if len(supports[curve]) == 1 and degrees[curve] == 2
        ]
        if anchors:
            need(len(anchors) == 1, "unique linear anchor")
            anchor = anchors[0]
            selected.append((record, anchor, record[1] if record[0] == anchor else record[0]))
    need(len(selected) == 400, "degree-two-anchor pair census")
    return selected, degrees


def precheck(certificate):
    need(certificate.get("schema") == "hn-radix-degree-two-anchor-roots-v1", "schema")
    summary = certificate["summary"]
    effect = certificate["frontier_effect"]
    need(summary["selected_pair_systems"] == 400, "selected systems")
    need(summary["distinct_physical_pair_intersections"] == 890, "physical roots")
    need(summary["points_on_accepted_closed_loci"] == 272, "closed roots")
    need(summary["remaining_eligible_points"] == 618, "eligible roots")
    need(summary["remaining_eligible_stabilizer_orbits"] == 574, "eligible orbits")
    need(summary["pair_systems_with_no_eligible_point"] == 44, "removed systems")
    need(summary["orbit_allowance_reduction"] == 2330, "allowance reduction")
    need(effect["remaining_global_pair_systems"] == 131312, "global systems")
    need(effect["remaining_global_nonfour_orbit_allowance"] == 3844374, "global allowance")
    need(effect["remaining_exact_five_pair_systems"] == 128380, "exact-five systems")
    need(effect["remaining_exact_five_nonfour_orbit_allowance"] == 3760994, "exact-five allowance")
    need(not certificate["record_improvement"] and not certificate["physical_chromatic_search_performed"], "claim scope")


def compute():
    source_certificate = json.loads((ORBIT / "certificate.json").read_text())
    with tempfile.TemporaryDirectory(prefix="hn-degree-two-anchor-check-") as directory:
        interface_path = Path(directory) / "orbit-interface.json"
        orbit_certificate = ORBIT_CHECKER.compute(source_certificate, interface_path)
        interface = json.loads(interface_path.read_text())

    rows, factors, _, _, row_ids = REVIEW.reconstruct_inventory()
    rows_by_id = {curve: row for row, curve in row_ids.items()}
    need(digest(factors) == interface["curve_inventory_sha256"], "curve inventory alignment")
    selected, degrees = select_pairs(interface, factors, rows_by_id)
    collisions = collision_inventory(rows)
    collision_polynomials = []
    for row in collisions:
        degree = len(row) - 1
        real, imaginary = collision_parts(row)
        collision_polynomials.append(
            (
                degree,
                tuple((i, j, value) for (i, j), value in sorted(real.items())),
                tuple((i, j, value) for (i, j), value in sorted(imaginary.items())),
            )
        )

    centers = {}
    for _, anchor, _ in selected:
        row = rows_by_id[anchor]
        need({index for index, digit in enumerate(row) if index and digit != (0, 0)} == {1}, "linear anchor")
        need(e_norm(row[1]) == 1, "unit leading coefficient")
        ratio = e_multiply(row[0], e_conjugate(row[1]))
        centers[anchor] = (-ratio[0], -ratio[1])
    need(len(set(centers.values())) == 6, "six circle centers")
    marker_records, parameterizations, markers = {}, {}, {}
    for center in sorted(set(centers.values())):
        record, parameterization, marker = marker_for_center(center, collision_polynomials)
        marker_records[center] = record
        parameterizations[center] = parameterization
        markers[center] = marker

    entries = []
    profile = Counter()
    roots = closed_total = eligible_total = orbit_total = 0
    zero_pairs = []
    for pair_record, anchor, other in selected:
        center = centers[anchor]
        x_numerator, y_numerator = parameterizations[center]
        pull = pullback(factors[other], degrees[other], x_numerator, y_numerator)
        squarefree_pull = squarefree(pull)
        closed = squarefree(p_gcd(squarefree_pull, markers[center]))
        eligible = p_quotient(squarefree_pull, closed)
        finite_roots = real_root_count(squarefree_pull)
        finite_closed = real_root_count(closed)
        finite_eligible = real_root_count(eligible)
        need(finite_roots == finite_closed + finite_eligible, "finite real-root partition")
        center_x, center_y = coordinate(center)
        base_x, base_y = center_x - 1, center_y
        infinity_root = evaluate_sparse(factors[other], base_x, base_y) == 0
        infinity_closed = infinity_root and marker_records[center]["base_point_closed"]
        root_count = finite_roots + int(infinity_root)
        closed_count = finite_closed + int(infinity_closed)
        eligible_count = finite_eligible + int(infinity_root and not infinity_closed)
        stabilizer = pair_record[2].bit_count()
        need(root_count == closed_count + eligible_count, "projective root partition")
        need(stabilizer in (1, 2) and eligible_count % stabilizer == 0, "free stabilizer action")
        orbit_count = eligible_count // stabilizer
        entries.append(
            {
                "pair": pair_record[:2],
                "anchor_curve": anchor,
                "other_curve": other,
                "center_eisenstein": list(center),
                "stabilizer_mask": pair_record[2],
                "stabilizer_order": stabilizer,
                "product_surface_intersection_bound": pair_record[3],
                "previous_orbit_allowance": pair_record[4],
                "pullback": canonical_coefficients(pull),
                "squarefree_pullback": canonical_coefficients(squarefree_pull),
                "closed_gcd": canonical_coefficients(closed),
                "eligible_factor": canonical_coefficients(eligible),
                "finite_physical_points": finite_roots,
                "infinity_physical_point": bool(infinity_root),
                "closed_points": closed_count,
                "eligible_points": eligible_count,
                "eligible_stabilizer_orbits": orbit_count,
            }
        )
        profile[root_count, closed_count, eligible_count, stabilizer] += 1
        roots += root_count
        closed_total += closed_count
        eligible_total += eligible_count
        orbit_total += orbit_count
        if not eligible_count:
            zero_pairs.append(pair_record[:2])

    previous = json.loads(
        (ROOT / "hadwiger_nelson_radix_two_coordinate_pencils" / "FRONTIER_EFFECT.json").read_text()
    )
    prior_allowance = sum(record[0][4] for record in selected)
    reduction = prior_allowance - orbit_total
    return {
        "schema": "hn-radix-degree-two-anchor-roots-v1",
        "sources": {
            "five_active_orbit_certificate_sha256": file_digest(ORBIT / "certificate.json"),
            "h4181_frontier_effect_sha256": file_digest(
                ROOT / "hadwiger_nelson_radix_two_coordinate_pencils" / "FRONTIER_EFFECT.json"
            ),
            "curve_inventory_sha256": digest(factors),
            "h4177_interface_sha256": orbit_certificate["explicit_interface"]["canonical_json_sha256"],
        },
        "circle_parameterization": {
            "coordinates": "z=x+i*sqrt(3)y",
            "center": "c=-a0/a1",
            "x": "c_x+(1-3*t^2)/(1+3*t^2)",
            "y": "c_y+2*t/(1+3*t^2)",
            "omitted_point": "(c_x-1,c_y), tested separately",
        },
        "closed_loci": {
            "collision_rows": len(collisions),
            "reflection_axes": ["y=0", "y=x", "y=-x"],
            "radial_unit_circle": "x^2+3*y^2=1",
            "center_markers": [marker_records[center] for center in sorted(marker_records)],
        },
        "entries": entries,
        "summary": {
            "selected_pair_systems": len(entries),
            "pair_stabilizer_histogram": {
                str(key): value
                for key, value in sorted(Counter(entry["stabilizer_order"] for entry in entries).items())
            },
            "previous_product_surface_allowance": sum(record[0][3] for record in selected),
            "previous_nonfour_orbit_allowance": prior_allowance,
            "distinct_physical_pair_intersections": roots,
            "points_on_accepted_closed_loci": closed_total,
            "remaining_eligible_points": eligible_total,
            "remaining_eligible_stabilizer_orbits": orbit_total,
            "orbit_allowance_reduction": reduction,
            "pair_systems_with_no_eligible_point": len(zero_pairs),
            "zero_pair_sha256": digest(zero_pairs),
            "root_closed_eligible_stabilizer_histogram": {
                str(key): value for key, value in sorted(profile.items())
            },
        },
        "frontier_effect": {
            "previous_global_pair_systems": previous["global_pair_systems"],
            "remaining_global_pair_systems": previous["global_pair_systems"] - len(zero_pairs),
            "previous_global_nonfour_orbit_allowance": previous["global_nonfour_orbit_allowance"],
            "remaining_global_nonfour_orbit_allowance": previous["global_nonfour_orbit_allowance"] - reduction,
            "previous_exact_five_pair_systems": previous["remaining_exact_five_pairs"],
            "remaining_exact_five_pair_systems": previous["remaining_exact_five_pairs"] - len(zero_pairs),
            "previous_exact_five_nonfour_orbit_allowance": previous["remaining_exact_five_orbit_allowance"],
            "remaining_exact_five_nonfour_orbit_allowance": previous["remaining_exact_five_orbit_allowance"] - reduction,
            "at_least_six_pair_systems": previous["now_at_least_six_pairs"],
            "at_least_six_nonfour_orbit_allowance": previous["now_at_least_six_orbit_allowance"],
            "whole_pair_systems_removed": len(zero_pairs),
        },
        "entry_sha256": digest(entries),
        "record_improvement": False,
        "physical_chromatic_search_performed": False,
    }


def explicit_interface(result):
    return {
        "schema": "hn-radix-degree-two-anchor-root-interface-v1",
        "circle_parameterization": result["circle_parameterization"],
        "closed_loci": result["closed_loci"],
        "entries": result["entries"],
        "scope": (
            "Exact physical roots of the 400 post-h4181 exact-five global pair "
            "representatives containing a degree-two anchor. Closed collision, "
            "reflection-axis and radial-unit-circle points are marked unusable for "
            "a non-four counterexample. No chromatic decision is included."
        ),
    }


def compact_certificate(result):
    interface = explicit_interface(result)
    encoded = json.dumps(interface, sort_keys=True, separators=(",", ":")) + "\n"
    return {
        key: value for key, value in result.items() if key not in ("entries", "entry_sha256")
    } | {
        "explicit_interface": {
            "entries": len(result["entries"]),
            "bytes": len(encoded.encode()),
            "canonical_json_sha256": digest(interface),
            "file_sha256": hashlib.sha256(encoded.encode()).hexdigest(),
            "entry_sha256": result["entry_sha256"],
        }
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--check-expected", action="store_true")
    parser.add_argument("--export-interface", type=Path)
    args = parser.parse_args()
    submitted = json.loads(args.certificate.read_text())
    precheck(submitted)
    full = compute()
    actual = compact_certificate(full)
    precheck(actual)
    need(actual == submitted, "certificate mismatch")
    if args.export_interface is not None:
        if args.export_interface.exists():
            raise FileExistsError(args.export_interface)
        args.export_interface.write_text(
            json.dumps(explicit_interface(full), sort_keys=True, separators=(",", ":")) + "\n"
        )
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        projection = {
            "status": "DEGREE_TWO_ANCHOR_ROOT_FRONTIER_VERIFIED",
            **actual["summary"],
            **actual["frontier_effect"],
            "record_improvement": actual["record_improvement"],
        }
        need(projection == expected, "expected projection")
    print(json.dumps({"verified": True, **actual["summary"], **actual["frontier_effect"]}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
