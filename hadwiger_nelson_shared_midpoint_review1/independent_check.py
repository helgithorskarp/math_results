#!/usr/bin/env python3
"""Independent exact audit of the shared-midpoint circle-support theorem.

No producer or verifier module is imported.  Exact coordinates are represented
as Fraction coefficients in Q(sqrt(3),sqrt(19)), rather than the author's
scaled dense-integer representation.  The script also checks the universal
two-circle and antipodal-transversal parity logic independently of the fixed
certificate.
"""

import copy
import hashlib
import json
import sys
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE.parent / "hadwiger_nelson_shared_midpoint" / "certificate.json"
EXPECTED_CERTIFICATE_SHA256 = "523ad8d9922a5e3ac6d2ff1a648cff37b4705a69b3d870f4579f9d722c6486b0"
RADICANDS = (1, 3, 19, 57)
RADICAL_INDEX = {value: index for index, value in enumerate(RADICANDS)}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def qadd(left, right):
    return tuple(a + b for a, b in zip(left, right))


def qneg(value):
    return tuple(-x for x in value)


def qsub(left, right):
    return qadd(left, qneg(right))


def qmul(left, right):
    """Multiply in the squarefree basis indexed by masks of {3,19}."""
    out = [F(0)] * 4
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            if a and b:
                out[i ^ j] += a * b * RADICANDS[i & j]
    return tuple(out)


def qscale(value, scalar):
    return tuple(scalar * x for x in value)


def rational(value=0):
    return (F(value), F(0), F(0), F(0))


QZERO = rational()
QONE = rational(1)
UNIT = QONE


def zadd(left, right):
    return qadd(left[0], right[0]), qadd(left[1], right[1])


def zsub(left, right):
    return qsub(left[0], right[0]), qsub(left[1], right[1])


def zmul(left, right):
    return (
        qsub(qmul(left[0], right[0]), qmul(left[1], right[1])),
        qadd(qmul(left[0], right[1]), qmul(left[1], right[0])),
    )


def norm(value):
    return qadd(qmul(value[0], value[0]), qmul(value[1], value[1]))


def distance_squared(left, right):
    return norm(zsub(left, right))


def complex_rational(real=0, imaginary=0):
    return rational(real), rational(imaginary)


def coordinate_key(value):
    return tuple((x.numerator, x.denominator) for axis in value for x in axis)


def certificate_sort_key(value):
    """The producer's documented sparse radical ordering for point labels."""
    return tuple(tuple((radicand, axis[index])
                       for index, radicand in enumerate(RADICANDS) if axis[index])
                 for axis in value)


def decode_point(encoded):
    require(isinstance(encoded, list) and len(encoded) == 2, "point must have two coordinates")
    coordinates = []
    for encoded_axis in encoded:
        require(isinstance(encoded_axis, list), "coordinate must be a list")
        axis = [F(0)] * 4
        previous = 0
        for term in encoded_axis:
            require(isinstance(term, list) and len(term) == 3, "radical term must be a triple")
            radicand, numerator, denominator = term
            require(all(type(x) is int for x in term), "radical term entries must be integers")
            require(radicand in RADICAL_INDEX and radicand > previous, "radicands must be known and ordered")
            require(denominator > 0 and numerator and abs(F(numerator, denominator).numerator) == abs(numerator),
                    "coefficient must be nonzero with a positive denominator")
            coefficient = F(numerator, denominator)
            require(coefficient.numerator == numerator and coefficient.denominator == denominator,
                    "coefficient must be reduced")
            axis[RADICAL_INDEX[radicand]] = coefficient
            previous = radicand
        coordinates.append(tuple(axis))
    return tuple(coordinates)


def encode_point(point):
    result = []
    for axis in point:
        result.append([
            [radicand, axis[index].numerator, axis[index].denominator]
            for index, radicand in enumerate(RADICANDS)
            if axis[index]
        ])
    return result


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


OMEGA = (qscale(QONE, F(1, 2)), (F(0), F(1, 2), F(0), F(0)))
ROOTS = [complex_rational(1)]
for _ in range(5):
    ROOTS.append(zmul(ROOTS[-1], OMEGA))
require(zmul(ROOTS[-1], OMEGA) == ROOTS[0], "sixth-root construction did not close")


def rotate(value, exponent):
    return zmul(value, ROOTS[exponent % 6])


def orbit(value):
    return frozenset(rotate(value, exponent) for exponent in range(6))


def phase_from_rep(value, representative):
    return next(exponent for exponent in range(6) if rotate(representative, exponent) == value)


def check_universal_phase_logic():
    well_defined = chord_edges = cross_edges = 0
    for phase, exponent, owner in product((0, 1), range(6), (0, 1)):
        colour = (phase + owner + exponent) % 2
        for direction in (-1, 1):
            # At an equilateral two-owner point the owner and exponent parity
            # both toggle; the two representations must have the same colour.
            other = (phase + (1 - owner) + exponent + direction) % 2
            require(colour == other, "two-owner representation changes the phase colour")
            well_defined += 1

            same_circle = (phase + owner + exponent + direction) % 2
            require(colour != same_circle, "a unit chord on one circle is monochromatic")
            chord_edges += 1

        other_circle = (phase + (1 - owner) + exponent) % 2
        require(colour != other_circle, "a direction-preserving cross-circle edge is monochromatic")
        cross_edges += 1

    # The four forbidden sixth-root chord-square values and every strict
    # interval used in the written separation proof.
    forbidden = {F(0), F(1), F(3), F(4)}
    separation_intervals = ((F(3), F(4)), (F(0), F(1)), (F(1), F(3)))
    require(all(not (left < value < right)
                for left, right in separation_intervals for value in forbidden),
            "a separation interval contains a sixth-root chord value")

    points = [(i, j, root) for i, j, root in product((0, 1), repeat=3)]
    antipode = lambda point: (1 - point[0], 1 - point[1], 1 - point[2])
    pairs = sorted({tuple(sorted((point, antipode(point)))) for point in points})
    require(len(pairs) == 4 and set().union(*map(set, pairs)) == set(points),
            "the abstract mixed points do not form four antipodal pairs")

    prescriptions = centre_avoidance = orbit_singletons = 0
    transversal_signatures = []
    for mask in range(16):
        selected = {pair[(mask >> index) & 1] for index, pair in enumerate(pairs)}
        require(all(len(selected & set(pair)) == 1 for pair in pairs), "not an antipodal transversal")
        transversal_signatures.append(tuple(sorted(selected)))
        a_constraints = {index: [] for index in range(4)}
        b_constraints = {index: [] for index in range(4)}
        for index, pair in enumerate(pairs):
            for point in pair:
                i, j, _ = point
                if point in selected:
                    colour = 1 - j
                    require(colour != j, "A-palette mixed colour meets its B-centre colour")
                    a_constraints[index].append((point, colour))
                else:
                    colour = 3 - i
                    require(colour != 2 + i, "B-palette mixed colour meets its A-centre colour")
                    b_constraints[index].append((point, colour))
                prescriptions += 1
                centre_avoidance += 1
        require(all(len(row) == 1 for row in a_constraints.values()),
                "an A direction orbit receives other than one phase prescription")
        require(all(len(row) == 1 for row in b_constraints.values()),
                "a B direction orbit receives other than one phase prescription")
        orbit_singletons += 8
    require(len(set(transversal_signatures)) == 16, "transversal enumeration has duplicates")
    return {
        "two_owner_well_defined_checks": well_defined,
        "same_circle_unit_chord_checks": chord_edges,
        "cross_circle_unit_edge_checks": cross_edges,
        "separation_intervals": [[str(a), str(b)] for a, b in separation_intervals],
        "antipodal_pairs": len(pairs),
        "transversals": len(transversal_signatures),
        "mixed_prescription_checks": prescriptions,
        "centre_avoidance_checks": centre_avoidance,
        "single_constraint_orbit_checks": orbit_singletons,
    }


def audit_certificate(data):
    require(data.get("schema") == 1, "unexpected certificate schema")
    require(data.get("orientation") == [[3, 5], [4, 5]], "unexpected orientation")
    require(data.get("translation") == [[1, 5], [-2, 5]], "unexpected translation")
    require(data.get("target_found") is False, "certificate overstates the target")
    require(data.get("sharp_kernel_bound") == 108, "wrong asserted kernel bound")

    r = complex_rational(F(3, 5), F(4, 5))
    t = complex_rational(F(1, 5), F(-2, 5))
    centres = [complex_rational(), complex_rational(1), t, zadd(t, r)]
    require(len(set(centres)) == 4, "centres are not distinct")
    require(zadd(centres[0], centres[1]) == zadd(centres[2], centres[3]),
            "segments do not share a midpoint")
    require(distance_squared(centres[0], centres[1]) == UNIT and
            distance_squared(centres[2], centres[3]) == UNIT,
            "diagonals are not unit segments")

    cross_pairs = ((0, 2), (0, 3), (1, 2), (1, 3))
    rows = data.get("cross_intersections")
    require(isinstance(rows, list) and len(rows) == 4, "four cross-pair rows required")
    intersections = []
    cross_separations = []
    intersection_norm_checks = 0
    for (left, right), row in zip(cross_pairs, rows):
        require(isinstance(row, list) and len(row) == 2, "each strict circle pair needs two intersections")
        decoded = [decode_point(point) for point in row]
        require(decoded[0] != decoded[1], "two listed intersections coincide")
        separation = distance_squared(centres[left], centres[right])
        require(separation[1:] == (F(0), F(0), F(0)) and F(0) < separation[0] < F(4),
                "cross centres do not have two circle intersections")
        for point in decoded:
            require(distance_squared(point, centres[left]) == UNIT and
                    distance_squared(point, centres[right]) == UNIT,
                    "listed point is not on both unit circles")
            intersection_norm_checks += 2
        require(zadd(decoded[0], decoded[1]) == zadd(centres[left], centres[right]),
                "intersection pair has the wrong midpoint")
        intersections.extend(decoded)
        cross_separations.append(separation[0])
    require(len(set(intersections)) == 8, "mixed intersection set does not have eight points")
    require(cross_separations == [F(1, 5), F(4, 5), F(4, 5), F(1, 5)],
            "cross-centre squared distances differ")

    cross_directions = [set(), set()]
    for (left, right), row in zip(cross_pairs, rows):
        for point in map(decode_point, row):
            cross_directions[0].update(orbit(zsub(point, centres[left])))
            cross_directions[1].update(orbit(zsub(point, centres[right])))
    require(len(cross_directions[0]) == len(cross_directions[1]) == 24,
            "four sixfold cross-direction orbits required per group")

    direction_sets = [set(ROOTS), set(orbit(zsub(centres[3], centres[2])))]
    for group in range(2):
        direction_sets[group].update(cross_directions[group])
    require([len(row) for row in direction_sets] == data.get("directions") == [30, 30],
            "example does not have five distinct direction orbits per group")

    patch_a = {zadd(centres[owner], direction) for owner in (0, 1) for direction in direction_sets[0]}
    patch_b = {zadd(centres[owner], direction) for owner in (2, 3) for direction in direction_sets[1]}
    require(len(patch_a) == len(patch_b) == 58, "paired translate size differs")
    require(patch_a & patch_b == set(intersections), "cross-patch overlap is not exactly the mixed set")
    vertices = sorted(patch_a | patch_b, key=certificate_sort_key)
    require(len(vertices) == data.get("vertices") == 108, "kernel does not attain 108 vertices")
    require(digest([encode_point(point) for point in vertices]) == data.get("point_sha256"),
            "canonical point hash differs")
    labels = {point: index for index, point in enumerate(vertices)}
    centre_labels = [labels[point] for point in centres]
    require(centre_labels == data.get("centres"), "centre labels differ")

    edges = [(left, right) for left, right in combinations(range(len(vertices)), 2)
             if distance_squared(vertices[left], vertices[right]) == UNIT]
    require(len(edges) == data.get("edges") == 294, "exact unit-edge count differs")
    require(digest(edges) == data.get("edge_sha256"), "canonical edge hash differs")

    owners = [{index for index, centre in enumerate(centres)
               if distance_squared(point, centre) == UNIT} for point in vertices]
    require(all(1 <= len(row) <= 2 for row in owners), "a kernel point has an invalid owner count")
    mixed = sorted(labels[point] for point in intersections)
    midpoint_sum = zadd(centres[0], centres[1])
    antipodal_pairs = sorted({tuple(sorted((label, labels[zsub(midpoint_sum, vertices[label])])))
                              for label in mixed})
    require(len(antipodal_pairs) == 4 and [list(row) for row in antipodal_pairs] == data.get("cross_pairs"),
            "certificate's antipodal pairs differ")

    group_orbit_checks = 0
    for group in range(2):
        classes = {}
        for label in mixed:
            owner = next(owner for owner in owners[label] if owner // 2 == group)
            classes.setdefault(orbit(zsub(vertices[label], centres[owner])), set()).add(label)
        require(len(classes) == 4 and set(map(frozenset, classes.values())) == set(map(frozenset, antipodal_pairs)),
                "mixed group directions do not form precisely the antipodal pairs")
        group_orbit_checks += len(classes)

    expected_masks = []
    for label, owner_set in enumerate(owners):
        if label in centre_labels:
            mask = 1 << (2, 3, 0, 1)[centre_labels.index(label)]
        elif owner_set <= {0, 1}:
            mask = 3
        elif owner_set <= {2, 3}:
            mask = 12
        else:
            mask = 15
        expected_masks.append(mask)
    require("".join(format(mask, "x") for mask in expected_masks) == data.get("lists"),
            "owner-derived colour lists differ")

    colouring_rows = data.get("colourings")
    require(isinstance(colouring_rows, list) and
            [row.get("transversal_mask") for row in colouring_rows] == list(range(16)),
            "certificate does not contain all 16 ordered transversals")
    edge_inequalities = phase_checks = mixed_checks = 0
    for mask, row in enumerate(colouring_rows):
        text = row.get("colouring")
        require(isinstance(text, str) and len(text) == 108 and set(text) <= set("0123"),
                "malformed colouring string")
        colours = list(map(int, text))
        require(all(bitmask & (1 << colour) for bitmask, colour in zip(expected_masks, colours)),
                "colouring violates an owner list or centre pin")
        require(all(colours[left] != colours[right] for left, right in edges),
                "colouring contains a monochromatic unit edge")
        edge_inequalities += len(edges)
        selected = {pair[(mask >> index) & 1] for index, pair in enumerate(antipodal_pairs)}
        for label in mixed:
            i = next(owner for owner in owners[label] if owner < 2)
            j = next(owner for owner in owners[label] if owner >= 2) - 2
            wanted = 1 - j if label in selected else 3 - i
            require(colours[label] == wanted, "mixed point misses its transversal prescription")
            mixed_checks += 1

        phases = [{}, {}]
        for label, point in enumerate(vertices):
            if label in centre_labels:
                continue
            group = colours[label] // 2
            palette_owners = [owner for owner in owners[label] if owner // 2 == group]
            require(palette_owners, "colour palette has no corresponding owner group")
            for owner in palette_owners:
                direction = zsub(point, centres[owner])
                direction_orbit = orbit(direction)
                representative = min(direction_orbit, key=coordinate_key)
                exponent = phase_from_rep(direction, representative)
                phase = (colours[label] - 2 * group + owner % 2 + exponent) % 2
                require(representative not in phases[group] or phases[group][representative] == phase,
                        "listed colouring is not induced by one phase per direction orbit")
                phases[group][representative] = phase
                phase_checks += 1

    return {
        "field_basis": list(RADICANDS),
        "cross_squared_centre_distances": [str(value) for value in cross_separations],
        "intersection_unit_norm_checks": intersection_norm_checks,
        "cross_intersection_points": len(intersections),
        "group_cross_orbit_class_checks": group_orbit_checks,
        "directions": [len(row) for row in direction_sets],
        "paired_patch_sizes": [len(patch_a), len(patch_b)],
        "patch_overlap": len(patch_a & patch_b),
        "vertices": len(vertices),
        "all_point_pair_norms": len(vertices) * (len(vertices) - 1) // 2,
        "edges": len(edges),
        "transversal_colourings": len(colouring_rows),
        "positive_unit_edge_checks": edge_inequalities,
        "mixed_colour_checks": mixed_checks,
        "phase_consistency_checks": phase_checks,
        "point_sha256": data["point_sha256"],
        "edge_sha256": data["edge_sha256"],
        "sharp_kernel_bound": data["sharp_kernel_bound"],
        "bound_attained": len(vertices) == data["sharp_kernel_bound"],
    }


def reject_mutants(data):
    mutants = []
    bad = copy.deepcopy(data)
    bad["cross_intersections"][0].pop()
    mutants.append(bad)
    bad = copy.deepcopy(data)
    bad["cross_intersections"][0][0][0][0][1] += 1
    mutants.append(bad)
    bad = copy.deepcopy(data)
    bad["point_sha256"] = "0" * 64
    mutants.append(bad)
    bad = copy.deepcopy(data)
    bad["colourings"][0]["colouring"] = "0" * 108
    mutants.append(bad)
    bad = copy.deepcopy(data)
    bad["sharp_kernel_bound"] = 107
    mutants.append(bad)
    for index, mutant in enumerate(mutants):
        try:
            audit_certificate(mutant)
        except AssertionError:
            continue
        raise AssertionError(f"malformed certificate accepted: {index}")
    return len(mutants)


def main():
    certificate_bytes = CERTIFICATE.read_bytes()
    certificate_sha256 = hashlib.sha256(certificate_bytes).hexdigest()
    require(certificate_sha256 == EXPECTED_CERTIFICATE_SHA256, "unpinned source certificate")
    data = json.loads(certificate_bytes)
    result = {
        "status": "INDEPENDENTLY_VERIFIED_SCOPED_THEOREM",
        "universal_logic": check_universal_phase_logic(),
        "fixed_example": audit_certificate(data),
        "malformed_certificate_rejections": reject_mutants(data),
        "certificate_sha256": certificate_sha256,
        "native_solver_calls": 0,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
