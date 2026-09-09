#!/usr/bin/env python3
"""Independent checker for the h4167 radix incidence exclusions.

The curve inventory comes from reviewer-1's independently published h4151
checker, not from either target implementation.  This checker enumerates all
13^5 raw disjoint-support states and quotients them directly, constructs the
constant-offset bundles from normalized tails, compares the complete 3 MB
interface entry by entry, and independently applies its pair constraints to a
supplied h4117 quotient export.
"""

import argparse
from collections import Counter
import hashlib
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
INVENTORY_SOURCE = (
    HERE.parent
    / "hadwiger_nelson_radix_four_active_closure_review1"
    / "independent_check.py"
)
SPEC = importlib.util.spec_from_file_location("reviewer_inventory", INVENTORY_SOURCE)
R = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(R)

ZERO = (0, 0)
UNITS = R.UNITS
D = (ZERO,) + UNITS
POSITION_STATES = ((ZERO, ZERO),) + tuple((unit, ZERO) for unit in UNITS) + tuple(
    (ZERO, unit) for unit in UNITS
)

EXPECTED_INTERFACE_BYTES_SHA256 = (
    "37321cbfb596695ed42e8f0336004f1e09c8b77dc42fd8205785b5160d9b10ec"
)
EXPECTED_INTERFACE_SHA256 = (
    "c9cb33688915d282b9d410898eeeb22d4bd33e242b3d28b7703ca4fe2111c477"
)
EXPECTED_QUOTIENT_BYTES_SHA256 = (
    "90e6235fcd71a8998fe6c4229882f383fe9d18c7c3dd6c66cca9098fa5057998"
)
EXPECTED_PAIR_REPRESENTATIVES_SHA256 = (
    "ab9d291e1b59a234712eb9ef95aaeb70654921351542b825afeee887b118ccd6"
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def e_add(left, right):
    return left[0] + right[0], left[1] + right[1]


def e_neg(value):
    return -value[0], -value[1]


def e_sub(left, right):
    return e_add(left, e_neg(right))


def e_norm(value):
    return value[0] ** 2 + value[0] * value[1] + value[1] ** 2


def row_scale(unit, row):
    return tuple(R.e_mul(unit, value) for value in row)


def row_add(left, right):
    return tuple(e_add(a, b) for a, b in zip(left, right))


def reconstruct_curve_owner():
    rows, factors, circle, monomial_rows, row_to_curve = R.reconstruct_inventory()
    require(len(rows) == 2801 and len(row_to_curve) == 2796, "independent curve inventory")

    def owner(row):
        normalized = R.canonical_row(row)
        if normalized in monomial_rows:
            return None if monomial_rows[normalized] == 0 else circle
        return row_to_curve[normalized]

    return rows, factors, circle, monomial_rows, row_to_curve, owner


def raw_disjoint_pair_representatives():
    representatives = set()
    raw_nonzero_pairs = 0
    for state_word in product(POSITION_STATES, repeat=5):
        left = tuple(state[0] for state in state_word)
        right = tuple(state[1] for state in state_word)
        if all(value == ZERO for value in left) or all(value == ZERO for value in right):
            continue
        raw_nonzero_pairs += 1
        normalized = tuple(sorted((R.canonical_row(left), R.canonical_row(right))))
        representatives.add(normalized)
    formula = 13**5 - 2 * 7**5 + 1
    require(raw_nonzero_pairs == formula == 337680, "raw disjoint ordered-pair formula")
    require(len(representatives) == formula // (2 * 6**2) == 4690, "free-action quotient")
    return sorted(representatives), raw_nonzero_pairs


def exact_unit_controls():
    digit_differences = {
        e_sub(left, right) for left in (ZERO, (1, 0), (0, 1)) for right in (ZERO, (1, 0), (0, 1))
    }
    require(digit_differences == set(D), "D is exactly the digit-difference alphabet")

    determinants = []
    for a, b, c in combinations(UNITS, 3):
        determinant = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (
            c[0] - a[0]
        )
        require(determinant != 0, "three phase centres became collinear")
        determinants.append(determinant)

    separation_histogram = Counter(e_norm(e_sub(a, b)) for a, b in combinations(UNITS, 2))
    require(separation_histogram == {1: 6, 3: 6, 4: 3}, "hexagon separation census")

    triangle_ratio_counts = Counter()
    nonadjacent_cases = 0
    for phase in UNITS:
        ratios = [ratio for ratio in UNITS if e_norm(e_add(ratio, phase)) == 1]
        require(len(ratios) == 2, "unit-endpoint triangle ratios")
        triangle_ratio_counts[len(ratios)] += 1
    for u, v in combinations(UNITS, 2):
        separation = e_norm(e_sub(u, v))
        if separation == 1:
            continue
        nonadjacent_cases += 1
        if separation == 3:
            forced = e_neg(e_add(u, v))
            require(e_norm(forced) == 1, "separation-sqrt(3) forced unit ratio")
            require(
                e_norm(e_add(forced, u)) == e_norm(e_add(forced, v)) == 1,
                "forced ratio does not satisfy phase equations",
            )
            q_endpoint_roots = [ZERO, e_neg(e_add(u, v))]
            require(
                all(e_norm(e_add(root, u)) == e_norm(e_add(root, v)) == 1 for root in q_endpoint_roots),
                "Q-endpoint circle intersections",
            )
        else:
            require(v == e_neg(u), "distance-two phases are antipodal")
    require(nonadjacent_cases == 9, "nonadjacent phase-pair count")

    # Adjacent phases cannot be excluded by this rule: this exact local
    # configuration satisfies the endpoint and two phase equations while the
    # other endpoint is neither zero nor unit.
    endpoint = (1, 0)
    other = (-2, 1)
    adjacent_phase = (0, 1)
    require(
        e_norm(endpoint)
        == e_norm(e_add(endpoint, other))
        == e_norm(e_add(endpoint, R.e_mul(adjacent_phase, other)))
        == 1,
        "adjacent-phase boundary fixture",
    )
    require(e_norm(other) == 3 and e_norm(e_sub((1, 0), adjacent_phase)) == 1, "adjacent fixture domain")
    return {
        "phase_triple_determinants_checked": len(determinants),
        "phase_separation_histogram": {str(key): value for key, value in sorted(separation_histogram.items())},
        "unit_triangle_phase_cases_checked": sum(triangle_ratio_counts.values()),
        "nonadjacent_phase_pairs_checked": nonadjacent_cases,
        "allowed_adjacent_phase_control": True,
    }


def enumerate_phase_exclusions(owner, circle):
    pair_representatives, raw_count = raw_disjoint_pair_representatives()
    pencils = set()
    forbidden = set()
    arity_sources = Counter()

    def exclude(curves, source):
        if circle in curves:
            return
        key = tuple(sorted({curve for curve in curves if curve is not None}))
        require(len(key) >= 2, "degenerate off-circle exclusion")
        forbidden.add(key)
        arity_sources[source, len(key)] += 1

    for left, right in pair_representatives:
        require(
            all(a == ZERO or b == ZERO for a, b in zip(left, right)),
            "representative supports overlap",
        )
        members = []
        for unit in UNITS:
            member_row = row_add(left, row_scale(unit, right))
            require(all(value in D for value in member_row), "phase row leaves D^5")
            members.append(owner(member_row))
        require(
            len(set(members)) == 6 and None not in members and circle not in members,
            "six distinct noncircle member events",
        )
        pencil = tuple(sorted(members))
        require(pencil not in pencils, "two raw orbits produce one phase pencil")
        pencils.add(pencil)
        endpoints = [owner(left), owner(right)]

        for triple in combinations(members, 3):
            exclude(triple, "three_phases")
        for member in members:
            exclude(endpoints + [member], "both_endpoints")
        for i, j in combinations(range(6), 2):
            if e_norm(e_sub(UNITS[i], UNITS[j])) == 1:
                continue
            for endpoint in endpoints:
                exclude([endpoint, members[i], members[j]], "endpoint_nonadjacent")

    require(len(pencils) == 4690, "phase-pencil census")
    forbidden = sorted(forbidden)
    require(Counter(map(len, forbidden)) == {2: 5976, 3: 176420}, "phase-exclusion census")
    return sorted(pencils), forbidden, raw_count, arity_sources


def offset_intersection_controls():
    cases = 0
    for a, b in combinations(D, 2):
        if a == ZERO or b == ZERO:
            unit = b if a == ZERO else a
            values = [R.e_mul(unit, UNITS[2]), R.e_mul(unit, UNITS[4])]
        else:
            values = [ZERO, e_neg(e_add(a, b))]
        require(
            all(e_norm(e_add(value, a)) == e_norm(e_add(value, b)) == 1 for value in values),
            "constant-offset intersection leaves E",
        )
        cases += 1
    require(cases == 21, "constant-offset pair types")
    return cases


def enumerate_offset_pairs(owner, circle):
    tails = sorted(
        {
            R.canonical_row(tail)
            for tail in product(D, repeat=4)
            if any(value != ZERO for value in tail)
        }
    )
    require(len(tails) == (7**4 - 1) // 6 == 400, "tail-orbit census")
    bundles = []
    offset_pairs = set()
    for tail in tails:
        group = {}
        for offset in D:
            curve = owner((offset,) + tail)
            if curve == circle:
                continue
            require(curve is not None and curve not in group.values(), "offset curve ownership")
            group[offset] = curve
        require(len(group) in (6, 7), "offset-bundle size")
        bundles.append(group)
        offset_pairs.update(tuple(sorted(pair)) for pair in combinations(group.values(), 2))
    histogram = Counter(map(len, bundles))
    require(histogram == {6: 4, 7: 396}, "offset-bundle histogram")
    require(len(offset_pairs) == 8376, "constant-offset pair census")
    return bundles, sorted(offset_pairs)


def build_interface(factors, circle, pencils, forbidden, offset_pairs):
    interface = {
        "schema": "hn-radix-incidence-geometry-v1",
        "curve_inventory_sha256": digest(factors),
        "circle_id": circle,
        "injectivity_excluded_sets": forbidden,
        "monic_degree_four_excluded_pairs": offset_pairs,
        "six_event_phase_pencils": pencils,
        "scope": "All fields use original h4105 curve IDs. The first list forces label collision; the second forces a monic Eisenstein relation of degree at most four. Either excludes a non-four-colourable physical A5 member. Higher active incidence does not evade these exclusions.",
    }
    combined = sorted(set(forbidden) | set(offset_pairs))
    return interface, combined


def verify_submitted_interface(path, reconstructed):
    raw = Path(path).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_INTERFACE_BYTES_SHA256, "submitted interface byte hash")
    submitted = json.loads(raw)
    require(digest(submitted) == EXPECTED_INTERFACE_SHA256, "submitted canonical interface hash")
    reconstructed_raw = (
        json.dumps(reconstructed, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode()
    require(raw == reconstructed_raw, "entrywise submitted/reviewer interface mismatch")


def apply_frontier(quotient_path, factors, circle, forbidden, offset_pairs):
    raw = Path(quotient_path).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_QUOTIENT_BYTES_SHA256, "h4117 quotient bytes")
    quotient = json.loads(raw)
    pairs = quotient["pair_system_representatives"]
    require(len(pairs) == 132130, "h4117 pair count")
    require(digest(pairs) == EXPECTED_PAIR_REPRESENTATIVES_SHA256, "h4117 pair digest")
    require(
        pairs == sorted(pairs)
        and len({tuple(pair) for pair in pairs}) == len(pairs)
        and all(
            isinstance(pair, list)
            and len(pair) == 2
            and pair[0] < pair[1]
            and 0 <= pair[0] < len(factors)
            and 0 <= pair[1] < len(factors)
            for pair in pairs
        ),
        "h4117 pair shape, ordering, uniqueness, and domain",
    )

    degrees = [max(i + j for i, j, _ in polynomial) for polynomial in factors]
    allowance = lambda items: sum(degrees[left] * degrees[right] for left, right in items)
    collision_pairs = {item for item in forbidden if len(item) == 2}
    all_excluded_pairs = collision_pairs | set(offset_pairs)
    off_circle = [pair for pair in pairs if circle not in pair]
    removed = [pair for pair in off_circle if tuple(pair) in all_excluded_pairs]
    retained = [pair for pair in off_circle if tuple(pair) not in all_excluded_pairs]
    require(all(tuple(pair) in collision_pairs for pair in removed), "removed pair lacks collision proof")

    result = {
        "source_global_systems": len(pairs),
        "source_global_parameter_allowance": allowance(pairs),
        "after_circle_systems": len(off_circle),
        "after_circle_allowance": allowance(off_circle),
        "removed_whole_systems": len(removed),
        "removed_parameter_allowance": allowance(removed),
        "removed_pairs_sha256": digest(removed),
        "remaining_global_systems": len(retained),
        "remaining_parameter_allowance": allowance(retained),
        "remaining_pairs_sha256": digest(retained),
        "all_removed_pairs_force_collision": True,
    }
    expected = {
        "source_global_systems": 132130,
        "source_global_parameter_allowance": 7785424,
        "after_circle_systems": 131788,
        "after_circle_allowance": 7780224,
        "removed_whole_systems": 432,
        "removed_parameter_allowance": 25696,
        "removed_pairs_sha256": "44f2c41114a911c9113b433ae08a83335ba6acbbf23872b938c526d98ef37576",
        "remaining_global_systems": 131356,
        "remaining_parameter_allowance": 7754528,
        "remaining_pairs_sha256": "9aa6caf04379f9e8c9736ad8d287ea51902c63e4d317f9c9c7deb112700f8149",
        "all_removed_pairs_force_collision": True,
    }
    require(result == expected, "independent frontier accounting")
    return result


def main(interface_path, quotient_path):
    controls = exact_unit_controls()
    offset_control_count = offset_intersection_controls()
    rows, factors, circle, _, _, owner = reconstruct_curve_owner()
    pencils, forbidden, raw_disjoint_count, source_counts = enumerate_phase_exclusions(owner, circle)
    bundles, offset_pairs = enumerate_offset_pairs(owner, circle)
    interface, combined = build_interface(factors, circle, pencils, forbidden, offset_pairs)
    verify_submitted_interface(interface_path, interface)
    frontier = apply_frontier(quotient_path, factors, circle, forbidden, offset_pairs)

    collision_pairs = {item for item in forbidden if len(item) == 2}
    offset_pair_set = set(offset_pairs)
    require(collision_pairs <= offset_pair_set, "phase collision pairs are not offset pairs")
    result = {
        "schema": "hn-radix-incidence-geometry-independent-review-v1",
        "difference_classes": len(rows),
        "active_curves": len(factors),
        "circle_id": circle,
        "raw_nonzero_ordered_disjoint_pairs": raw_disjoint_count,
        "phase_pencils": len(pencils),
        "injectivity_excluded_sets": len(forbidden),
        "injectivity_excluded_arity_histogram": {
            str(key): value for key, value in sorted(Counter(map(len, forbidden)).items())
        },
        "constant_offset_bundles": len(bundles),
        "constant_offset_bundle_size_histogram": {
            str(key): value for key, value in sorted(Counter(map(len, bundles)).items())
        },
        "monic_degree_four_excluded_pairs": len(offset_pairs),
        "phase_pairs_contained_in_offset_pairs": len(collision_pairs),
        "additional_offset_only_pairs": len(offset_pair_set - collision_pairs),
        "combined_nonfour_excluded_sets": len(combined),
        "interface_entrywise_identical": True,
        "interface_sha256": digest(interface),
        "phase_pencils_sha256": digest(pencils),
        "injectivity_excluded_sets_sha256": digest(forbidden),
        "monic_degree_four_excluded_pairs_sha256": digest(offset_pairs),
        "combined_nonfour_excluded_sets_sha256": digest(combined),
        "offset_intersection_types_checked": offset_control_count,
        "generated_rule_application_histogram": {
            f"{name}:arity_{arity}": count
            for (name, arity), count in sorted(source_counts.items())
        },
        "algebraic_controls": controls,
        "frontier": frontier,
        "eight_active_gate_closed": False,
        "record_improvement": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--interface", type=Path, required=True)
    parser.add_argument("--quotient", type=Path, required=True)
    args = parser.parse_args()
    main(args.interface, args.quotient)
