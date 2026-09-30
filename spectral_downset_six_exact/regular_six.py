#!/usr/bin/env python3
"""Complete regular rank-three six-point cohort and exact capped certificates.

No floating point or third-party package enters this verifier.  The two
labelled hypergraph enumerations are compared entry by entry.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations
from math import gcd, lcm
from pathlib import Path
import argparse
import hashlib
import json

from verify import check_downset, decode, exact_ldl_psd, characteristic_polynomial

TRIPLES = tuple(a for a in range(64) if a.bit_count() == 3)
POINTS = tuple(tuple(i for i in range(6) if a >> i & 1) for a in TRIPLES)
BASE = sum(1 << a for a in range(64) if a.bit_count() <= 2)


def image(a, p):
    return sum(1 << p[i] for i in range(6) if a >> i & 1)


def permutation_data():
    position = {a: i for i, a in enumerate(TRIPLES)}
    return [(p, tuple(1 << position[image(a, p)] for a in TRIPLES))
            for p in permutations(range(6))]


def relabel(mask, powers):
    return sum(powers[i] for i in range(20) if mask >> i & 1)


def regular_gray():
    """Every nonzero 20-bit mask once, maintaining its six triple degrees."""
    degree = [0]*6
    mask = 0
    for ordinal in range(1, 1 << 20):
        bit = (ordinal & -ordinal).bit_length()-1
        mask ^= 1 << bit
        change = 1 if mask >> bit & 1 else -1
        for i in POINTS[bit]:
            degree[i] += change
        if degree[0] > 0 and degree.count(degree[0]) == 6:
            yield mask, degree[0]


def regular_backtrack():
    """Independent degree-constrained include/exclude enumeration."""
    tail = [[0]*6 for _ in range(21)]
    for k in range(19, -1, -1):
        tail[k] = tail[k+1][:]
        for i in POINTS[k]:
            tail[k][i] += 1

    def visit(k, mask, remaining):
        if any(x < 0 or x > tail[k][i] for i, x in enumerate(remaining)):
            return
        if not any(remaining):
            yield mask
            return
        if k == 20:
            return
        yield from visit(k+1, mask, remaining)
        next_remaining = list(remaining)
        for i in POINTS[k]:
            next_remaining[i] -= 1
        yield from visit(k+1, mask | (1 << k), tuple(next_remaining))

    for degree in range(1, 11):
        yield from visit(0, 0, (degree,)*6)


def census():
    pdata = permutation_data()
    labelled = set()
    seen_orbits = set()
    degrees = Counter()
    cases = []
    for mask, degree in regular_gray():
        if mask in labelled:
            raise AssertionError("Gray enumeration repeated a labelled family")
        labelled.add(mask)
        degrees[degree] += 1
        if mask in seen_orbits:
            continue
        orbit = {relabel(mask, powers) for _, powers in pdata}
        canonical = min(orbit)
        seen_orbits.update(orbit)
        triples = [a for i, a in enumerate(TRIPLES) if canonical >> i & 1]
        autos = [p for p, powers in pdata if relabel(canonical, powers) == canonical]
        if len(orbit)*len(autos) != 720 or len(triples) != 2*degree:
            raise AssertionError("orbit or regular-degree identity differs")
        family = BASE + sum(1 << a for a in triples)
        cases.append({"family": family, "triples": triples, "triple_degree": degree,
                      "N": 22+len(triples), "s": 6+degree,
                      "labelled_orbit_size": len(orbit), "automorphism_order": len(autos),
                      "vertex_transitive": len({p[0] for p in autos}) == 6})
    independent = list(regular_backtrack())
    if len(independent) != len(set(independent)) or set(independent) != labelled:
        raise AssertionError("independent labelled enumerations disagree")
    if seen_orbits != labelled or sum(x['labelled_orbit_size'] for x in cases) != len(labelled):
        raise AssertionError("canonical orbits do not reconstruct the labelled domain")
    return sorted(cases, key=lambda x: x['family']), len(labelled), dict(sorted(degrees.items()))


def matrix_from_orbits(case, certificate):
    sets = decode(case['family'], 6)[1:]
    check_downset([0]+sets)
    if any(sum(a >> k & 1 for a in sets) != case['s'] for k in range(6)):
        raise AssertionError("actual largest stars differ from cohort formula")
    included = set(sets)
    autos = []
    for p in permutations(range(6)):
        mapping = {a: image(a, p) for a in sets}
        if set(mapping.values()) == included:
            autos.append(mapping)
    if len(autos) != case['automorphism_order']:
        raise AssertionError("independent automorphism count differs")
    entries = {}
    representatives = certificate['orbit_representatives']
    values = certificate['orbit_values']
    if len(representatives) != len(values):
        raise AssertionError("certificate orbit/value lengths differ")
    for (a, b), value in zip(representatives, values):
        if a == b or a & b or a not in included or b not in included:
            raise AssertionError("invalid disjoint orbit representative")
        orbit = {tuple(sorted((p[a], p[b]))) for p in autos}
        if set(entries).intersection(orbit):
            raise AssertionError("certificate orbits overlap")
        entries.update({pair: F(value) for pair in orbit})
    if set(entries) != {(a, b) for a, b in combinations(sets, 2) if not a & b}:
        raise AssertionError("certificate orbits miss allowed entries")
    core = [[F(case['s']-1) if a == b else F(-1) if a & b else
             entries[tuple(sorted((a, b)))]-1 for b in sets] for a in sets]
    scale = lcm(*(x.denominator for row in core for x in row))
    return sets, scale, [[int(x*scale) for x in row] for row in core]


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def two_psd_checks(matrix, expected_rank):
    if any(matrix[i][j] != matrix[j][i] for i in range(len(matrix))
           for j in range(len(matrix))):
        raise AssertionError("PSD input is not symmetric")
    rank = exact_ldl_psd(matrix)
    coefficients = characteristic_polynomial(matrix)
    if any((-1)**k*x < 0 for k, x in enumerate(coefficients)):
        raise AssertionError("characteristic polynomial has a possible negative root")
    zeroes = 0
    for x in reversed(coefficients):
        if x:
            break
        zeroes += 1
    if rank != expected_rank or rank != len(matrix)-zeroes:
        raise AssertionError("two exact rank checks disagree")
    return digest(coefficients)


def check_case(case, certificate):
    sets, scale, core = matrix_from_orbits(case, certificate)
    n, s = case['N'], case['s']
    if len(sets)+1 != n:
        raise AssertionError("cohort dimension differs")
    for i in range(n-1):
        for k in range(6):
            if sum(core[i][j] for j, b in enumerate(sets) if b >> k & 1):
                raise AssertionError("maximum-star kernel equation failed")
    upper = [[scale*(n*int(i == j)-1)-core[i][j] for j in range(n-1)]
             for i in range(n-1)]
    core_hash = two_psd_checks(core, n-7)
    upper_hash = two_psd_checks(upper, n-1)
    sums = [sum(row) for row in core]
    bound = [[scale+sum(sums)] + [scale-x for x in sums]] + [
        [scale-sums[i]] + [scale+x for x in row] for i, row in enumerate(core)]
    upper_sums = [sum(row) for row in upper]
    upper_lift = [[sum(upper_sums)] + [-x for x in upper_sums]] + [
        [-upper_sums[i]] + row for i, row in enumerate(upper)]
    if upper_lift != [[scale*n*int(i == j)-bound[i][j] for j in range(n)]
                      for i in range(n)]:
        raise AssertionError("full upper-bound congruence identity failed")
    all_sets = [0]+sets
    numerator = [[bound[i][j]-scale*s*int(i == j) for j in range(n)] for i in range(n)]
    if any(numerator[i][j] != numerator[j][i] for i in range(n) for j in range(n)):
        raise AssertionError("H symmetry failed")
    if any(numerator[i][j] for i, a in enumerate(all_sets)
           for j, b in enumerate(all_sets) if a & b):
        raise AssertionError("H support failed")
    denominator = scale*(n-s)
    if any(sum(row) != denominator for row in numerator):
        raise AssertionError("H row sum failed")
    common = denominator
    for row in numerator:
        for x in row:
            common = gcd(common, x)
    denominator //= common
    numerator = [[x//common for x in row] for row in numerator]
    return dict(case, core_denominator=scale, core_rank=n-7, upper_core_rank=n-1,
                H_PSD_rank=n-6, I_minus_M_rank=n-1, M_denominator=denominator,
                M_numerator_sha256=digest(numerator),
                core_characteristic_sha256=core_hash, upper_characteristic_sha256=upper_hash,
                M_empty_diagonal=str(F(numerator[0][0], denominator)))


def verify_all(certificate_path):
    fixture = json.loads(certificate_path.read_text())
    cases, labelled_count, degree_counts = census()
    certificates = {x['family']: x for x in fixture['certificates']}
    if len(certificates) != len(fixture['certificates']) or set(certificates) != {
            x['family'] for x in cases}:
        raise AssertionError("certificate list does not cover the exact cohort once")
    results = [check_case(case, certificates[case['family']]) for case in cases]
    return {"agent": "six-downset-3", "role": "researcher",
            "claim_status": "exact capped maximal-rank certificates for the complete regular rank-three full-two-skeleton six-point cohort",
            "classes": len(cases), "labelled_triple_families": labelled_count,
            "vertex_transitive_classes": sum(x['vertex_transitive'] for x in cases),
            "labelled_counts_by_triple_degree": {str(k): v for k, v in degree_counts.items()},
            "independent_labelled_enumerations_agree_entrywise": True,
            "certificate_fixture_sha256": hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
            "cases": results}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificates', type=Path,
                        default=Path(__file__).with_name('REGULAR_SIX_CERTIFICATES.json'))
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = verify_all(args.certificates)
    if args.check and result != json.loads(args.check.read_text()):
        raise AssertionError("complete cohort verification differs from saved results")
    print(json.dumps(result, indent=2, sort_keys=True))
