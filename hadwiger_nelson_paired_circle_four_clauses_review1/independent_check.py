#!/usr/bin/env python3
"""Independent finite audits for the paired-circle four-clause theorem.

This script imports no producer code or certificate.  It checks the abstract
phase identities, the complete small 2-CNF census (with an extra five-variable
stratum), and the exact rational/square-root data used in the examples.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def normalize_clause(literals):
    """Return a canonical equality-literal clause; None denotes a tautology."""
    values = {}
    for variable, value in literals:
        values.setdefault(variable, set()).add(value)
    if any(len(seen) == 2 for seen in values.values()):
        return None
    return tuple(sorted((variable, next(iter(seen))) for variable, seen in values.items()))


def clause_mask(n, clause):
    result = 0
    for assignment in range(1 << n):
        if any(((assignment >> variable) & 1) == value for variable, value in clause):
            result |= 1 << assignment
    return result


def classify_minimal_unsatisfiable(clauses):
    """Classify four pairwise-disjoint falsifying codimension-two cubes."""
    require(len(clauses) == 4, "an unsatisfiable formula must have four clauses")
    supports = [frozenset(variable for variable, _ in clause) for clause in clauses]
    require(all(len(support) == 2 for support in supports), "non-binary clause in census")
    for left, right in combinations(clauses, 2):
        require(any((variable, 1 - value) in right for variable, value in left),
                "falsifying subcubes are not disjoint")

    used = frozenset().union(*supports)
    if len(used) == 2:
        return "four_signs"
    common = frozenset.intersection(*supports)
    if len(used) == 3 and len(common) == 1:
        hub = next(iter(common))
        require(sorted(sum((hub, sign) in clause for clause in clauses) for sign in (0, 1)) == [2, 2],
                "bad hub-sign split")
        return "two_opposite_forcing_pairs"
    raise AssertionError("unclassified unsatisfiable support pattern")


def census(n, maximum_clauses=4):
    options = [((u, a), (v, b))
               for u, v in combinations(range(n), 2)
               for a, b in product((0, 1), repeat=2)]
    masks = [clause_mask(n, clause) for clause in options]
    universe = (1 << (1 << n)) - 1
    formulas = unsatisfiable = deletion_checks = 0
    kinds = Counter()
    for size in range(maximum_clauses + 1):
        for indices in combinations(range(len(options)), size):
            formulas += 1
            surviving = universe
            for index in indices:
                surviving &= masks[index]
            if surviving:
                continue
            unsatisfiable += 1
            clauses = [options[index] for index in indices]
            kinds[classify_minimal_unsatisfiable(clauses)] += 1
            for removed in range(4):
                reduced = universe
                for position, index in enumerate(indices):
                    if position != removed:
                        reduced &= masks[index]
                require(reduced, "four-clause obstruction is not deletion-minimal")
                deletion_checks += 1
    return {
        "named_variables": n,
        "proper_binary_clause_options": len(options),
        "formulas": formulas,
        "unsatisfiable": unsatisfiable,
        "obstruction_types": dict(sorted(kinds.items())),
        "minimal_deletion_checks": deletion_checks,
    }


def check_phase_clauses():
    two_root_checks = truth_table_checks = distance_table_checks = 0
    chord_squared = (0, 1, 3, 4, 3, 1)
    for i, j, k, ell in product(range(2), range(2), range(6), range(6)):
        parity = (1 + i + j) % 2
        for same_variable in (False, True):
            v, w = (0, 0) if same_variable else (0, 1)
            first = normalize_clause(((v, (parity + k) % 2),
                                      (w, (1 + parity + ell) % 2)))
            reflected = normalize_clause(((w, (parity + ell + 3) % 2),
                                          (v, (1 + parity + k + 3) % 2)))
            require(first == reflected, "the two circle intersections give different clauses")
            two_root_checks += 1

            for bits in product((0, 1), repeat=1 if same_variable else 2):
                eligibility = (bits[v] == (parity + k) % 2 or
                               bits[w] == (1 + parity + ell) % 2)
                formula_value = True if first is None else any(bits[x] == value for x, value in first)
                require(eligibility == formula_value, "clause does not equal owner eligibility")
                truth_table_checks += 1

            if same_variable:
                distance = chord_squared[(ell - k) % 6]
                if distance in (0, 3):
                    require(first is None, "zero/sqrt(3) orbit separation should be tautological")
                elif distance in (1, 4):
                    require(first is not None and len(first) == 1,
                            "unit/tangent orbit separation should give a unit clause")
                distance_table_checks += 1

    multi_owner_checks = 0
    nonempty_subsets = ((0,), (1,), (0, 1))
    for owners_a, owners_b in product(nonempty_subsets, repeat=2):
        for values in product((False, True), repeat=4):
            p = values[:2]
            q = values[2:]
            pairwise = all(p[j] or q[i] for i in owners_a for j in owners_b)
            one_palette = all(p[j] for j in owners_b) or all(q[i] for i in owners_a)
            require(pairwise == one_palette, "multi-owner clauses permit inconsistent palettes")
            multi_owner_checks += 1

    return {
        "two_root_clause_identities": two_root_checks,
        "clause_truth_table_checks": truth_table_checks,
        "same_orbit_distance_table_checks": distance_table_checks,
        "multi_owner_distributive_checks": multi_owner_checks,
    }


def check_two_circle_phase():
    checks = 0
    # The two equilateral intersections for centres at exponents 0 and 0.
    for exponent_from_0, exponent_from_1 in ((1, 2), (5, 4)):
        require(exponent_from_0 % 2 == (1 + exponent_from_1) % 2,
                "owner change does not preserve the phase colour")
        checks += 1
    # A unit chord on one circle changes the sixth-root exponent by +/- 1.
    for phase, owner, exponent, direction in product((0, 1), (0, 1), range(6), (-1, 1)):
        left = (phase + owner + exponent) % 2
        right = (phase + owner + exponent + direction) % 2
        require(left != right, "unit chord is monochromatic")
        checks += 1
    # A noncentre edge crossing the two owner circles preserves direction and flips owner.
    for phase, exponent in product((0, 1), range(6)):
        require((phase + exponent) % 2 != (phase + 1 + exponent) % 2,
                "cross-owner unit edge is monochromatic")
        checks += 1
    return checks


def squared_distance(left, right):
    """Coordinates are (rational x, rational coefficient of sqrt(3) in y)."""
    dx = left[0] - right[0]
    dy = left[1] - right[1]
    return dx * dx + 3 * dy * dy


def check_examples():
    zero = (Fraction(0), Fraction(0))
    one = (Fraction(1), Fraction(0))
    b0 = (Fraction(12, 7), Fraction(1, 7))
    b1 = (Fraction(17, 14), Fraction(9, 14))
    positive = (zero, one, b0, b1)
    require(squared_distance(zero, one) == squared_distance(b0, b1) == 1,
            "positive centres do not form unit segments")
    cross = ((0, 2), (0, 3), (1, 2), (1, 3))
    positive_cross = [squared_distance(positive[u], positive[v]) for u, v in cross]
    require(positive_cross == [3, Fraction(19, 7), Fraction(4, 7), Fraction(9, 7)],
            "positive example cross-distance list differs")

    top_left = (Fraction(0), Fraction(1))
    top_right = (Fraction(1), Fraction(1))
    boundary = (zero, one, top_left, top_right)
    boundary_cross = [squared_distance(boundary[u], boundary[v]) for u, v in cross]
    require(boundary_cross == [3, 4, 4, 3], "boundary distances differ")
    common = (Fraction(1, 2), Fraction(1, 2))
    require(all(squared_distance(common, centre) == 1 for centre in boundary),
            "displayed boundary point is not adjacent to every centre")
    points = boundary + (common,)
    edges = [(u, v) for u, v in combinations(range(5), 2)
             if squared_distance(points[u], points[v]) == 1]
    require(edges == [(0, 1), (0, 4), (1, 4), (2, 3), (2, 4), (3, 4)],
            "boundary graph is not two triangles sharing one point")
    colours = (0, 1, 0, 1, 2)
    require(all(colours[u] != colours[v] for u, v in edges), "boundary graph control is not 3-coloured")
    return {
        "positive_cross_squared_distances": [str(value) for value in positive_cross],
        "boundary_cross_squared_distances": [str(value) for value in boundary_cross],
        "boundary_common_neighbour_unit_checks": 4,
        "boundary_five_point_edges": len(edges),
        "boundary_three_colour_control": list(colours),
    }


def main():
    rows = [census(n) for n in (2, 3, 4, 5)]
    require([(row["formulas"], row["unsatisfiable"]) for row in rows] ==
            [(16, 1), (794, 9), (12951, 30), (102091, 70)],
            "independent Boolean census differs from the theorem")
    require([row["obstruction_types"] for row in rows] == [
        {"four_signs": 1},
        {"four_signs": 3, "two_opposite_forcing_pairs": 6},
        {"four_signs": 6, "two_opposite_forcing_pairs": 24},
        {"four_signs": 10, "two_opposite_forcing_pairs": 60},
    ], "an unsatisfiable formula lies outside the two claimed types")

    three_clause_row = census(6, maximum_clauses=3)
    require(three_clause_row["unsatisfiable"] == 0, "three proper binary clauses are unsatisfiable")
    result = {
        "status": "INDEPENDENTLY_VERIFIED_SCOPED_INTERMEDIATE_RESULT",
        "phase_logic": check_phase_clauses(),
        "two_circle_phase_checks": check_two_circle_phase(),
        "boolean_census": rows,
        "six_variable_three_clause_control": three_clause_row,
        "examples": check_examples(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
