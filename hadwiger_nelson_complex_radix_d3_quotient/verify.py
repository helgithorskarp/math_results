#!/usr/bin/env python3
"""Independent exact verifier for the complex-radix D3 quotient."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
from math import gcd, lcm
import argparse
import hashlib
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_complex_radix_architecture"
sys.path.insert(0, str(SOURCE))
SOURCE_SPEC = importlib.util.spec_from_file_location("hn2_complex_radix_verify", SOURCE / "verify.py")
HN2 = importlib.util.module_from_spec(SOURCE_SPEC)
SOURCE_SPEC.loader.exec_module(HN2)

SOURCE_COMMIT = "95687bd35321aa6fb767fc508eac6ab186ba6d2e"
UNITS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
TRIANGLE = ((0, 0), (1, 0), (0, 1))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def emul(left, right):
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c + b * d


def eadd(left, right):
    return left[0] + right[0], left[1] + right[1]


def eneg(value):
    return -value[0], -value[1]


def canonical_row(row):
    return min(tuple(emul(unit, digit) for digit in row) for unit in UNITS)


def rotate_row(row):
    omega2 = (-1, 1)
    power = (1, 0)
    image = []
    for digit in row:
        image.append(emul(digit, power))
        power = emul(power, omega2)
    return canonical_row(tuple(image))


def conjugate_row(row):
    return canonical_row(tuple((a + b, -b) for a, b in row))


def padd(left, right):
    result = dict(left)
    for key, value in right.items():
        result[key] = result.get(key, Fraction(0)) + value
        if not result[key]:
            del result[key]
    return result


def pmul(left, right):
    result = {}
    for (i, j), value in left.items():
        for (k, m), other in right.items():
            key = (i + k, j + m)
            result[key] = result.get(key, Fraction(0)) + value * other
    return {key: value for key, value in result.items() if value}


def pscale(poly, scalar):
    return {key: scalar * value for key, value in poly.items() if scalar * value}


def powers(poly, maximum):
    result = [{(0, 0): Fraction(1)}]
    for _ in range(maximum):
        result.append(pmul(result[-1], poly))
    return result


def substitution_basis(x_image, y_image, maximum=8):
    xp = powers(x_image, maximum)
    yp = powers(y_image, maximum)
    return {(i, j): pmul(xp[i], yp[j]) for i in range(maximum + 1) for j in range(maximum + 1 - i)}


def primitive_rational(poly):
    need(poly, "zero pullback polynomial")
    denominator = 1
    for value in poly.values():
        denominator = lcm(denominator, value.denominator)
    integral = {key: int(value * denominator) for key, value in poly.items()}
    divisor = 0
    for value in integral.values():
        divisor = gcd(divisor, value)
    if integral[max(integral)] < 0:
        divisor = -divisor
    return tuple((i, j, value // divisor) for (i, j), value in sorted(integral.items()))


def pullback(factor, basis):
    result = {}
    for i, j, coefficient in factor:
        result = padd(result, pscale(basis[i, j], Fraction(coefficient)))
    return primitive_rational(result)


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def generated_group(generators):
    identity = tuple(range(len(generators[0])))
    result = {identity}
    frontier = {identity}
    while frontier:
        next_frontier = set()
        for old in frontier:
            for generator in generators:
                candidate = compose(old, generator)
                if candidate not in result:
                    result.add(candidate)
                    next_frontier.add(candidate)
        frontier = next_frontier
    return tuple(sorted(result))


def pair_image(pair, action):
    a, b = action[pair[0]], action[pair[1]]
    return (a, b) if a < b else (b, a)


def histogram(values):
    return {str(key): value for key, value in sorted(Counter(values).items())}


def check_digit_isometries():
    # R scales the j-th digit triangle by omega^(2j); each scaled triangle
    # must be a translate of T. C uses conjugate(T)=1-T.
    omega2 = (-1, 1)
    power = (1, 0)
    translations = []
    triangle_set = set(TRIANGLE)
    for _ in range(5):
        scaled = {emul(power, digit) for digit in TRIANGLE}
        possible = []
        for a in scaled:
            for b in TRIANGLE:
                shift = eadd(a, eneg(b))
                if {eadd(digit, eneg(shift)) for digit in scaled} == triangle_set:
                    possible.append(shift)
        need(possible, "rotation digit triangle is not a translate")
        translations.append(min(possible))
        power = emul(power, omega2)
    conjugated = {(a + b, -b) for a, b in TRIANGLE}
    reflected = {eadd((1, 0), eneg(digit)) for digit in TRIANGLE}
    need(conjugated == reflected, "conjugation digit identity")
    return translations


def actual_certificate():
    rows, events, factors, factor_edges, base, collisions, _, _ = HN2.build()
    source_certificate = json.loads((SOURCE / "certificate.json").read_text())
    _, _, _, pairs = HN2.finite_cover(
        source_certificate["colour_specs"], factors, factor_edges, base
    )
    need(len(rows) == 2801 and len(events) == 2801, "source displacement inventory")
    check_digit_isometries()

    # Unlike the producer's coefficient-word action, derive the active-curve
    # action by substituting the two rational parameter transformations into
    # each integer curve polynomial.
    rotation_basis = substitution_basis(
        {(1, 0): Fraction(-1, 2), (0, 1): Fraction(-3, 2)},
        {(1, 0): Fraction(1, 2), (0, 1): Fraction(-1, 2)},
    )
    conjugation_basis = substitution_basis(
        {(1, 0): Fraction(1)}, {(0, 1): Fraction(-1)}
    )
    factor_ids = {factor: i for i, factor in enumerate(factors)}
    rotation = tuple(factor_ids[pullback(factor, rotation_basis)] for factor in factors)
    conjugation = tuple(factor_ids[pullback(factor, conjugation_basis)] for factor in factors)
    curve_group = generated_group((rotation, conjugation))
    identity = tuple(range(len(factors)))
    need(len(curve_group) == 6, "curve action is not D3")
    need(compose(rotation, compose(rotation, rotation)) == identity, "R^3 relation")
    need(compose(conjugation, conjugation) == identity, "C^2 relation")
    need(
        compose(conjugation, compose(rotation, conjugation)) == compose(rotation, rotation),
        "CRC=R^-1 relation",
    )

    unvisited = set(range(len(factors)))
    curve_reps = []
    curve_sizes = []
    while unvisited:
        seed = min(unvisited)
        orbit = {action[seed] for action in curve_group}
        curve_reps.append(min(orbit))
        curve_sizes.append(len(orbit))
        unvisited.difference_update(orbit)
    curve_degrees = [HN2.degree(factor) for factor in factors]

    pair_set = set(pairs)
    pair_orbits = {}
    for seed in pairs:
        orbit = {pair_image(seed, action) for action in curve_group}
        pair_orbits.setdefault(min(orbit), orbit)
    need(all(pair_orbits[rep] == {pair_image(rep, action) for action in curve_group} for rep in pair_orbits), "pair orbit consistency")
    pair_reps = sorted(pair_orbits)
    pair_sizes = [len(pair_orbits[rep]) for rep in pair_reps]
    source_members = [len(pair_orbits[rep] & pair_set) for rep in pair_reps]
    pair_products = [curve_degrees[a] * curve_degrees[b] for a, b in pair_reps]

    collision_ids = {row: i for i, row in enumerate(collisions)}
    collision_rotation = tuple(collision_ids[rotate_row(row)] for row in collisions)
    collision_conjugation = tuple(collision_ids[conjugate_row(row)] for row in collisions)
    collision_group = generated_group((collision_rotation, collision_conjugation))
    collision_identity = tuple(range(len(collisions)))
    need(len(collision_group) == 6, "collision action is not D3")
    need(
        compose(collision_rotation, compose(collision_rotation, collision_rotation))
        == collision_identity,
        "collision R^3 relation",
    )
    need(compose(collision_conjugation, collision_conjugation) == collision_identity, "collision C^2 relation")
    need(
        compose(
            collision_conjugation,
            compose(collision_rotation, collision_conjugation),
        )
        == compose(collision_rotation, collision_rotation),
        "collision CRC=R^-1 relation",
    )
    collision_unvisited = set(range(len(collisions)))
    collision_reps = []
    collision_sizes = []
    while collision_unvisited:
        seed = min(collision_unvisited)
        orbit = {action[seed] for action in collision_group}
        collision_reps.append(min(orbit))
        collision_sizes.append(len(orbit))
        collision_unvisited.difference_update(orbit)
    collision_degrees = [len(row) - 1 for row in collisions]
    collision_rep_degrees = [collision_degrees[item] for item in collision_reps]

    result = {
        "schema": "hn-complex-radix-d3-quotient-v1",
        "source_commit": SOURCE_COMMIT,
        "source_certificate_sha256": hashlib.sha256((SOURCE / "certificate.json").read_bytes()).hexdigest(),
        "source_factor_inventory_sha256": HN2.digest(factors),
        "source_pair_inventory_sha256": HN2.digest(pairs),
        "source_collision_inventory_sha256": HN2.digest(collisions),
        "parameter_action": {
            "R": "(x,y)->((-x-3y)/2,(x-y)/2)",
            "C": "(x,y)->(x,-y)",
            "group": "D3=<R,C | R^3=C^2=1, CRC=R^-1>",
            "fundamental_chamber": "x>=0 and 0<=y<=x",
            "nonfour_radial_chamber": "1/4 < x^2+3*y^2 <= 4",
        },
        "curves": {
            "objects": len(factors),
            "orbits": len(curve_reps),
            "orbit_size_histogram": histogram(curve_sizes),
            "representative_degree_histogram": histogram(curve_degrees[i] for i in curve_reps),
            "fixed_counts_sorted": sorted(
                sum(action[i] == i for i in range(len(factors))) for action in curve_group
            ),
            "rotation_permutation_sha256": digest(rotation),
            "conjugation_permutation_sha256": digest(conjugation),
            "representatives_sha256": digest(curve_reps),
        },
        "pairs": {
            "source_systems": len(pairs),
            "full_D3_closure_systems": sum(pair_sizes),
            "orbits": len(pair_reps),
            "orbit_size_histogram": histogram(pair_sizes),
            "source_members_per_orbit_histogram": histogram(source_members),
            "representatives_sha256": digest(pair_reps),
            "representative_degree_product_histogram": histogram(pair_products),
            "parameter_orbit_bezout_bound": sum(pair_products),
        },
        "collisions": {
            "objects": len(collisions),
            "orbits": len(collision_reps),
            "orbit_size_histogram": histogram(collision_sizes),
            "representative_degree_histogram": histogram(collision_rep_degrees),
            "fixed_counts_sorted": sorted(
                sum(action[i] == i for i in range(len(collisions)))
                for action in collision_group
            ),
            "representatives_sha256": digest(collision_reps),
            "parameter_orbit_degree_bound": sum(collision_rep_degrees),
        },
    }
    result["all_exceptional_parameter_orbits_upper_bound"] = (
        result["pairs"]["parameter_orbit_bezout_bound"]
        + result["collisions"]["parameter_orbit_degree_bound"]
    )
    return result


def check_certificate(certificate, actual):
    need(certificate == actual, "certificate differs from exact reconstruction")


def run(certificate_path):
    certificate = json.loads(certificate_path.read_text())
    actual = actual_certificate()
    check_certificate(certificate, actual)
    return {
        "status": "EXACT_D3_QUOTIENT_VERIFIED",
        "maximum_physical_order": 243,
        "active_curve_orbits": actual["curves"]["orbits"],
        "source_pair_systems": actual["pairs"]["source_systems"],
        "D3_closed_pair_systems": actual["pairs"]["full_D3_closure_systems"],
        "pair_system_orbits": actual["pairs"]["orbits"],
        "injective_exceptional_parameter_orbits_upper_bound": actual["pairs"]["parameter_orbit_bezout_bound"],
        "collision_polynomial_orbits": actual["collisions"]["orbits"],
        "collision_parameter_orbits_upper_bound": actual["collisions"]["parameter_orbit_degree_bound"],
        "all_exceptional_parameter_orbits_upper_bound": actual["all_exceptional_parameter_orbits_upper_bound"],
        "fundamental_chamber": actual["parameter_action"]["fundamental_chamber"],
        "nonfour_radial_chamber": actual["parameter_action"]["nonfour_radial_chamber"],
        "certificate_sha256": hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
        "source_commit": SOURCE_COMMIT,
        "source_certificate_sha256": actual["source_certificate_sha256"],
        "independent_curve_action_method": "exact rational substitution in all 2797 integer event polynomials",
        "proof_CAS_calls": 0,
        "proof_solver_calls": 0,
        "record_improvement": False,
        "candidate_claimed": False,
        "external_reviewer_acceptance_claimed": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--check-expected", action="store_true")
    parser.add_argument("--write-expected", type=Path)
    args = parser.parse_args()
    result = run(args.certificate)
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        need(result == expected, "expected output differs")
    if args.write_expected:
        need(not args.write_expected.exists(), "expected output path already exists")
        args.write_expected.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
