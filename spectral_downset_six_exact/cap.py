#!/usr/bin/env python3
"""Exact capped certificate for the exceptional six-element downset.

Only standard integer/Fraction arithmetic is used.  The product-family
consequence is proved in CAP_THEOREM.md without building product matrices.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import argparse
import hashlib
import json

from verify import (EXCEPTION, FACETS, check_downset, decode,
                    exact_ldl_psd, characteristic_polynomial,
                    disjoint_collections, exceptional_matrix)

REPRESENTATIVES = ((1, 2), (1, 6), (1, 12), (1, 26),
                   (3, 12), (3, 20), (3, 28))
PARAMETERS = (F(0), F(3, 2), F(9, 2))
EXPECTED_RREF = ((1, 0, 0, 0, -4, -8, -12, -66),
                 (0, 1, 0, 0, 1, 2, 2, 11),
                 (0, 0, 1, 0, 1, 2, 1, 11),
                 (0, 0, 0, 1, 0, 0, 2, 11))
C_FACTORS = ((6, (1, 0)), (1, (1, -16, 52)),
             (4, (1, -41, 337)), (5, (1, -88, 2228, -14048)))
U_FACTORS = ((1, (1, -114, 3308, -4008)), (4, (1, -87, 1809)),
             (5, (1, -64)), (5, (1, -104, 3252, -30240)))
L_FACTORS = ((6, (1, 0)), (1, (1, -64)), (1, (1, -36, 212)),
             (4, (1, -41, 337)), (5, (1, -88, 2228, -14048)))


def orbit_data(sets):
    included = set(sets)
    automorphisms = []
    for p in permutations(range(6)):
        image = {a: sum(1 << p[i] for i in range(6) if a >> i & 1)
                 for a in sets}
        if set(image.values()) == included:
            automorphisms.append(image)
    if len(automorphisms) != 60:
        raise AssertionError("automorphism order differs")
    orbit_index = {}
    sizes = []
    for k, (a, b) in enumerate(REPRESENTATIVES):
        orbit = {tuple(sorted((p[a], p[b]))) for p in automorphisms}
        if set(orbit_index).intersection(orbit):
            raise AssertionError("pair orbits overlap")
        orbit_index.update({pair: k for pair in orbit})
        sizes.append(len(orbit))
    allowed = {(a, b) for a, b in combinations(sets, 2) if not a & b}
    if set(orbit_index) != allowed:
        raise AssertionError("pair orbits do not exhaust allowed entries")
    return orbit_index, sizes


def affine_face(sets, orbit_index):
    """Reduce all maximum-star kernel equations, including dependent rows."""
    rows = []
    for a in sets:
        for k in range(6):
            if a >> k & 1:
                continue
            counts = Counter(orbit_index[tuple(sorted((a, b)))]
                             for b in sets if b >> k & 1 and not a & b)
            rows.append([F(counts[j]) for j in range(7)] + [F(11)])
    rank = 0
    for col in range(7):
        pivot = next((j for j in range(rank, len(rows)) if rows[j][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        divisor = rows[rank][col]
        rows[rank] = [x / divisor for x in rows[rank]]
        for j in range(len(rows)):
            if j != rank and rows[j][col]:
                multiplier = rows[j][col]
                rows[j] = [x - multiplier * y
                           for x, y in zip(rows[j], rows[rank])]
        rank += 1
    if rank != 4 or any(any(x for x in row) for row in rows[rank:]):
        raise AssertionError("affine constraint rank or consistency differs")
    if rows[:rank] != [[F(x) for x in row] for row in EXPECTED_RREF]:
        raise AssertionError("maximum-star affine face differs")
    return [[int(x) for x in row] for row in rows[:rank]]


def core(sets, orbit_index, parameters):
    u, v, w = parameters
    values = (4*u + 8*v + 12*w - 66, 11-u-2*v-2*w,
              11-u-2*v-w, 11-2*w, u, v, w)
    c = []
    for a in sets:
        row = []
        for b in sets:
            if a == b:
                row.append(F(10))
            elif a & b:
                row.append(F(-1))
            else:
                row.append(values[orbit_index[tuple(sorted((a, b)))]] - 1)
        c.append(row)
    return c, values


def twice_integer(matrix):
    result = []
    for row in matrix:
        if any((2*x).denominator != 1 for x in row):
            raise AssertionError("certificate has unexpected denominator")
        result.append([int(2*x) for x in row])
    return result


def lift(c2):
    """Return 2 L = 2 J + E (2 C) E^T, E=[-1^T;I]."""
    sums = [sum(row) for row in c2]
    return [[2 + sum(sums)] + [2 - x for x in sums]] + [
        [2 - sums[i]] + [2 + x for x in row] for i, row in enumerate(c2)]


def psd_two_routes(matrix, expected_rank):
    n = len(matrix)
    if any(matrix[i][j] != matrix[j][i] for i in range(n) for j in range(n)):
        raise AssertionError("PSD input is not symmetric")
    rank = exact_ldl_psd(matrix)
    coefficients = characteristic_polynomial(matrix)
    if any((-1)**k * x < 0 for k, x in enumerate(coefficients)):
        raise AssertionError("characteristic polynomial permits a negative root")
    nullity = 0
    for x in reversed(coefficients):
        if x:
            break
        nullity += 1
    if rank != expected_rank or rank != n - nullity:
        raise AssertionError("two independent rank checks disagree")
    return coefficients


def check_factorization(coefficients, factors):
    """Multiply the displayed small factors and compare to the matrix polynomial."""
    expanded = [1]
    for multiplicity, polynomial in factors:
        for _ in range(multiplicity):
            result = [0]*(len(expanded) + len(polynomial) - 1)
            for i, x in enumerate(expanded):
                for j, y in enumerate(polynomial):
                    result[i+j] += x*y
            expanded = result
    if expanded != coefficients:
        raise AssertionError("displayed characteristic factorization differs")


def verify_cap():
    all_sets = decode(EXCEPTION, 6)
    check_downset(all_sets)
    if len(all_sets) != 32 or all_sets[0] != 0:
        raise AssertionError("wrong exceptional family")
    if tuple(a for a in all_sets if a.bit_count() == 3) != FACETS:
        raise AssertionError("wrong triple design")
    if [sum(a >> i & 1 for a in all_sets) for i in range(6)] != [11]*6:
        raise AssertionError("largest-star size differs")
    sets = all_sets[1:]
    orbit_index, sizes = orbit_data(sets)
    rref = affine_face(sets, orbit_index)
    c, values = core(sets, orbit_index, PARAMETERS)
    if any(sum(c[i][j] for j, b in enumerate(sets) if b >> k & 1)
           for i in range(31) for k in range(6)):
        raise AssertionError("maximum-star kernel condition failed")
    c2 = twice_integer(c)
    u2 = [[64*int(i == j) - 2 - c2[i][j] for j in range(31)]
          for i in range(31)]
    c_coeff = psd_two_routes(c2, 25)
    u_coeff = psd_two_routes(u2, 31)
    check_factorization(c_coeff, C_FACTORS)
    check_factorization(u_coeff, U_FACTORS)
    l2 = lift(c2)
    upper2 = [[64*int(i == j) - l2[i][j] for j in range(32)]
              for i in range(32)]
    # Direct integer checks connect the core inequalities to the full matrix.
    u_sums = [sum(row) for row in u2]
    euet = [[sum(u_sums)] + [-x for x in u_sums]] + [
        [-u_sums[i]] + row for i, row in enumerate(u2)]
    if upper2 != euet:
        raise AssertionError("upper-bound congruence identity failed")
    if exact_ldl_psd(l2) != 26 or exact_ldl_psd(upper2) != 31:
        raise AssertionError("full-matrix PSD checks failed")
    check_factorization(characteristic_polynomial(l2), L_FACTORS)
    numerator = [[l2[i][j] - 22*int(i == j) for j in range(32)]
                 for i in range(32)]
    if any(numerator[i][j] != numerator[j][i]
           for i in range(32) for j in range(32)):
        raise AssertionError("H matrix is not symmetric")
    if any(numerator[i][j] for i, a in enumerate(all_sets)
           for j, b in enumerate(all_sets) if a & b):
        raise AssertionError("H matrix has an intersecting entry")
    if any(sum(row) != 42 for row in numerator):
        raise AssertionError("H row sum differs")
    if any(numerator[i][i] for i in range(32)):
        raise AssertionError("new certificate does not have zero diagonal")
    empty_by_rank = []
    for rank in (1, 2, 3):
        entries = {numerator[0][i] for i, a in enumerate(all_sets)
                   if a.bit_count() == rank}
        if len(entries) != 1:
            raise AssertionError("empty-row orbit is not constant")
        empty_by_rank.append(entries.pop())
    # The original uncapped matrix is a useful negative control for the cap.
    _, old_c, _ = exceptional_matrix()
    exact_ldl_psd(old_c)
    old_u = [[32*int(i == j) - 1 - old_c[i][j] for j in range(31)]
             for i in range(31)]
    try:
        exact_ldl_psd(old_u)
    except AssertionError:
        pass
    else:
        raise AssertionError("old certificate unexpectedly passes the upper cap")
    # This base dual is lifted analytically, rather than enumerating products.
    if max(disjoint_collections(sets)) != 3:
        raise AssertionError("fractional-dual clique constraints failed")
    if sum(F(a.bit_count()-1, 3) for a in sets) != F(35, 3):
        raise AssertionError("fractional-dual objective differs")
    return {"agent": "six-downset-3", "role": "researcher",
            "family_mask": EXCEPTION, "N": 32, "s": 11,
            "parameters_u_v_w": [str(x) for x in PARAMETERS],
            "Q_orbit_entries": [str(x) for x in values],
            "disjoint_pair_orbit_sizes": sizes,
            "maximum_star_affine_rref": rref,
            "C_rank": 25, "upper_core_rank": 31,
            "L_rank": 26, "I_minus_M_rank": 31,
            "twice_C_characteristic_coefficients": c_coeff,
            "twice_upper_core_characteristic_coefficients": u_coeff,
            "characteristic_factorizations": {
                key: [[multiplicity, list(polynomial)]
                      for multiplicity, polynomial in factors]
                for key, factors in (("twice_C", C_FACTORS),
                    ("twice_upper_core", U_FACTORS), ("twice_L", L_FACTORS))},
            "M_denominator": 42,
            "M_empty_row_numerators_by_rank": empty_by_rank,
            "M_numerator_sha256": hashlib.sha256(json.dumps(
                numerator, separators=(",", ":")).encode()).hexdigest(),
            "minimum_eigenvalue": "-11/21", "minimum_eigenvalue_multiplicity": 6,
            "maximum_eigenvalue": "1", "maximum_eigenvalue_multiplicity": 1,
            "old_uncapped_certificate_rejected": True,
            "product_formulas": {"k": "every integer k>=1",
                "N": "32^k", "s": "11*32^(k-1)",
                "ground_set_size": "6*k", "rank_of_downset": "3*k",
                "H_PSD_rank": "32^k-6*k",
                "H_PSD_rank_is_maximal": True,
                "fractional_dual_lower_bound": "(35/3)*32^(k-1)",
                "fractional_bound_to_star_ratio": "35/33"}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = verify_cap()
    if args.check and result != json.loads(args.check.read_text()):
        raise AssertionError("capped-certificate output differs from saved result")
    print(json.dumps(result, indent=2, sort_keys=True))
