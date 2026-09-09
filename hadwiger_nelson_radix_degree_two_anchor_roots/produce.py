#!/usr/bin/env python3
"""Produce exact physical-root data for the A5 degree-two-anchor pairs."""

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import json
from math import gcd, lcm
from pathlib import Path
import sys
import tempfile

import sympy as S


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ORBIT = ROOT / "hadwiger_nelson_radix_five_active_orbits"
T = S.symbols("t")
DENOMINATOR = 1 + 3 * T * T
QX = 1 - 3 * T * T
QY = 2 * T


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ORBIT_PRODUCER = load("degree_two_orbit_producer", ORBIT / "produce.py")
D3 = ORBIT_PRODUCER.PENCIL.D3


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def e_conjugate(value):
    return value[0] + value[1], -value[1]


def e_norm(value):
    return value[0] * value[0] + value[0] * value[1] + value[1] * value[1]


def e_multiply(left, right):
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c + b * d


def coordinate(value):
    return S.Rational(2 * value[0] + value[1], 2), S.Rational(value[1], 2)


def canonical_coefficients(polynomial):
    polynomial = S.Poly(polynomial, T, domain=S.QQ)
    coefficients = list(reversed(polynomial.all_coeffs()))
    denominator = lcm(*(int(value.q) for value in coefficients))
    integers = [int(value * denominator) for value in coefficients]
    divisor = 0
    for value in integers:
        divisor = gcd(divisor, abs(value))
    need(divisor > 0, "zero polynomial")
    integers = [value // divisor for value in integers]
    if integers[-1] < 0:
        integers = [-value for value in integers]
    return integers


def as_poly(coefficients):
    return S.Poly.from_list(list(reversed(coefficients)), gens=T, domain=S.QQ)


def sparse(polynomial):
    return tuple((i, j, value) for (i, j), value in sorted(polynomial.items()))


def pullback(polynomial, degree, x_numerator, y_numerator):
    expression = sum(
        coefficient
        * x_numerator**i
        * y_numerator**j
        * DENOMINATOR ** (degree - i - j)
        for i, j, coefficient in polynomial
    )
    return as_poly(canonical_coefficients(S.expand(expression)))


def collision_parts(row):
    real, imaginary = {}, {}
    for (a, b), (left, right) in zip(row, D3.G.POWERS):
        real = D3.G.add(
            real,
            D3.G.add(D3.G.scale(left, 2 * a + b), D3.G.scale(right, -3 * b)),
        )
        imaginary = D3.G.add(
            imaginary,
            D3.G.add(D3.G.scale(left, b), D3.G.scale(right, 2 * a + b)),
        )
    return real, imaginary


def marker_for_center(center, collision_polynomials):
    center_x, center_y = coordinate(center)
    x_numerator = S.expand(center_x * DENOMINATOR + QX)
    y_numerator = S.expand(center_y * DENOMINATOR + QY)
    collision_factors = set()
    for degree, real, imaginary in collision_polynomials:
        left = pullback(real, degree, x_numerator, y_numerator)
        right = pullback(imaginary, degree, x_numerator, y_numerator)
        common = S.gcd(left, right).sqf_part()
        if common.degree() <= 0:
            continue
        for factor, _ in S.factor_list(common)[1]:
            collision_factors.add(tuple(canonical_coefficients(factor)))
    collision_marker = S.Poly(1, T, domain=S.QQ)
    for coefficients in sorted(collision_factors):
        collision_marker *= as_poly(coefficients)
    collision_marker = collision_marker.sqf_part()

    axis_marker = S.Poly(
        S.expand(
            y_numerator
            * (y_numerator - x_numerator)
            * (y_numerator + x_numerator)
        ),
        T,
        domain=S.QQ,
    )
    radial_marker = S.Poly(
        S.expand(
            x_numerator**2
            + 3 * y_numerator**2
            - DENOMINATOR**2
        ),
        T,
        domain=S.QQ,
    )
    closed_marker = S.lcm(collision_marker, axis_marker)
    closed_marker = S.lcm(closed_marker, radial_marker).sqf_part()

    base = center_x - 1, center_y
    base_axis = base[1] * (base[1] - base[0]) * (base[1] + base[0]) == 0
    base_radial = base[0] ** 2 + 3 * base[1] ** 2 == 1
    base_collision = False
    for _, real, imaginary in collision_polynomials:
        rv = sum(value * base[0] ** i * base[1] ** j for i, j, value in real)
        iv = sum(value * base[0] ** i * base[1] ** j for i, j, value in imaginary)
        if rv == 0 and iv == 0:
            base_collision = True
            break
    return {
        "center_eisenstein": list(center),
        "collision_marker": canonical_coefficients(collision_marker),
        "collision_marker_degree": collision_marker.degree(),
        "closed_marker": canonical_coefficients(closed_marker),
        "closed_marker_degree": closed_marker.degree(),
        "base_point_closed": base_axis or base_radial or base_collision,
        "base_point_on_axis": base_axis,
        "base_point_on_radial_circle": base_radial,
        "base_point_collision": base_collision,
    }, (x_numerator, y_numerator), closed_marker


def select_pairs(interface, factors, rows_by_id):
    supports = {
        curve: {index for index, digit in enumerate(row) if index and digit != (0, 0)}
        for curve, row in rows_by_id.items()
    }
    degrees = [max(i + j for i, j, _ in factor) for factor in factors]
    selected = []
    for record in interface["pair_modes"]["exact_five_compatible"]:
        # h4181 moved exactly the pairs whose two row supports have union size two.
        if len(supports[record[0]] | supports[record[1]]) <= 2:
            continue
        anchors = [
            curve
            for curve in record[:2]
            if len(supports[curve]) == 1 and degrees[curve] == 2
        ]
        if anchors:
            need(len(anchors) == 1, "unique degree-two anchor")
            anchor = anchors[0]
            other = record[1] if record[0] == anchor else record[0]
            selected.append((record, anchor, other))
    need(len(selected) == 400, "degree-two-anchor pair census")
    return selected, degrees


def make_certificate():
    with tempfile.TemporaryDirectory(prefix="hn-degree-two-anchor-") as directory:
        path = Path(directory) / "orbit-interface.json"
        orbit_certificate = ORBIT_PRODUCER.compute(path)
        interface = json.loads(path.read_text())

    factors, _ = ORBIT_PRODUCER.FREE.curve_group()
    _, _, _, _, row_ids = ORBIT_PRODUCER.FREE.V.reconstruct_inventory()
    rows_by_id = {curve: row for row, curve in row_ids.items()}
    selected, degrees = select_pairs(interface, factors, rows_by_id)
    _, _, _, _, _, collisions, _, _ = D3.HN2.build()
    collision_polynomials = []
    for row in collisions:
        degree = max(index for index, digit in enumerate(row) if digit != (0, 0))
        real, imaginary = collision_parts(row)
        collision_polynomials.append((degree, sparse(real), sparse(imaginary)))

    centers = {}
    for _, anchor, _ in selected:
        row = rows_by_id[anchor]
        need({index for index, digit in enumerate(row) if index and digit != (0, 0)} == {1}, "linear anchor")
        need(e_norm(row[1]) == 1, "unit leading coefficient")
        ratio = e_multiply(row[0], e_conjugate(row[1]))
        centers[anchor] = (-ratio[0], -ratio[1])
    need(len(set(centers.values())) == 6, "six unit circle centers")

    marker_records = {}
    parameterizations = {}
    markers = {}
    for center in sorted(set(centers.values())):
        record, parameterization, marker = marker_for_center(center, collision_polynomials)
        marker_records[center] = record
        parameterizations[center] = parameterization
        markers[center] = marker

    entries = []
    profile = Counter()
    total_roots = total_closed = total_eligible = total_orbits = 0
    zero_pairs = []
    for pair_record, anchor, other in selected:
        center = centers[anchor]
        x_numerator, y_numerator = parameterizations[center]
        pull = pullback(factors[other], degrees[other], x_numerator, y_numerator)
        squarefree = pull.sqf_part()
        closed = S.gcd(squarefree, markers[center]).sqf_part()
        eligible = S.quo(squarefree, closed)
        finite_roots = int(squarefree.count_roots(-S.oo, S.oo))
        finite_closed = int(closed.count_roots(-S.oo, S.oo)) if closed.degree() else 0
        finite_eligible = int(eligible.count_roots(-S.oo, S.oo)) if eligible.degree() else 0
        need(finite_closed + finite_eligible == finite_roots, "real root partition")

        center_x, center_y = coordinate(center)
        base_x, base_y = center_x - 1, center_y
        infinity_root = (
            sum(
                coefficient * base_x**i * base_y**j
                for i, j, coefficient in factors[other]
            )
            == 0
        )
        infinity_closed = infinity_root and marker_records[center]["base_point_closed"]
        root_count = finite_roots + int(infinity_root)
        closed_count = finite_closed + int(infinity_closed)
        eligible_count = finite_eligible + int(infinity_root and not infinity_closed)
        need(root_count == closed_count + eligible_count, "projective real root partition")
        stabilizer = pair_record[2].bit_count()
        need(stabilizer in (1, 2) and eligible_count % stabilizer == 0, "free stabilizer action")
        orbit_count = eligible_count // stabilizer
        entry = {
            "pair": pair_record[:2],
            "anchor_curve": anchor,
            "other_curve": other,
            "center_eisenstein": list(center),
            "stabilizer_mask": pair_record[2],
            "stabilizer_order": stabilizer,
            "product_surface_intersection_bound": pair_record[3],
            "previous_orbit_allowance": pair_record[4],
            "pullback": canonical_coefficients(pull),
            "squarefree_pullback": canonical_coefficients(squarefree),
            "closed_gcd": canonical_coefficients(closed),
            "eligible_factor": canonical_coefficients(eligible),
            "finite_physical_points": finite_roots,
            "infinity_physical_point": bool(infinity_root),
            "closed_points": closed_count,
            "eligible_points": eligible_count,
            "eligible_stabilizer_orbits": orbit_count,
        }
        entries.append(entry)
        profile[root_count, closed_count, eligible_count, stabilizer] += 1
        total_roots += root_count
        total_closed += closed_count
        total_eligible += eligible_count
        total_orbits += orbit_count
        if eligible_count == 0:
            zero_pairs.append(pair_record[:2])

    previous = json.loads(
        (ROOT / "hadwiger_nelson_radix_two_coordinate_pencils" / "FRONTIER_EFFECT.json").read_text()
    )
    prior_allowance = sum(record[0][4] for record in selected)
    reduction = prior_allowance - total_orbits
    need(
        previous["remaining_exact_five_pairs"] == 128424
        and previous["remaining_exact_five_orbit_allowance"] == 3763324,
        "h4181 frontier",
    )
    result = {
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
            "distinct_physical_pair_intersections": total_roots,
            "points_on_accepted_closed_loci": total_closed,
            "remaining_eligible_points": total_eligible,
            "remaining_eligible_stabilizer_orbits": total_orbits,
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
    need(result["frontier_effect"]["remaining_global_nonfour_orbit_allowance"] == 3844374, "global bound")
    need(result["summary"]["remaining_eligible_stabilizer_orbits"] == 574, "root orbit count")
    return result


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
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--export-interface", type=Path)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(args.out)
    result = make_certificate()
    interface = explicit_interface(result)
    interface_raw = json.dumps(interface, sort_keys=True, separators=(",", ":")) + "\n"
    if args.export_interface is not None:
        if args.export_interface.exists():
            raise FileExistsError(args.export_interface)
        args.export_interface.write_text(interface_raw)
    certificate = compact_certificate(result)
    raw = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    args.out.write_text(raw)
    print(
        json.dumps(
            {
                "path": str(args.out),
                "bytes": len(raw.encode()),
                "sha256": hashlib.sha256(raw.encode()).hexdigest(),
                "explicit_interface_bytes": len(interface_raw.encode()),
                "explicit_interface_file_sha256": hashlib.sha256(interface_raw.encode()).hexdigest(),
                **result["summary"],
                **result["frontier_effect"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
