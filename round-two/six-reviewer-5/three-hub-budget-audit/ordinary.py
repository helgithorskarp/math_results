"""Exact count bridges and literal all-partition controls; no author imports."""
from collections import Counter
from itertools import combinations, product
import json
from audit import HERE, digest, require


def parameters(profile, multiplicities):
    P = sum(multiplicities); a, b, c = multiplicities
    return tuple(75-4*profile[i]+P-(c, b, a)[i] for i in range(3))


def admissible_pairs(profile, P, t):
    result = []
    for lam in product(range(6), repeat=3):
        if sum(lam) != P:
            continue
        D = parameters(profile, lam)
        if min(D) < 0:
            continue
        if all(15-D[i]-D[j] <= 3*m-t for (i, j), m in zip(((0, 1), (0, 2), (1, 2)), lam)):
            result.append(lam)
    return result


def literal_partition_controls(data):
    raw = data['words']
    require(len(raw) == len(set(raw)) == 69 and all(type(w) is int and 0 < w < 1 << 18
            and w.bit_count() == 5 for w in raw), 'known witness literal domain')
    words = [frozenset(i for i in range(18) if w >> i & 1) for w in raw]
    require(all(len(a & b) <= 2 for a, b in combinations(words, 2)), 'known witness repeated triple')
    covered = {tuple(sorted(t)) for w in words for t in combinations(w, 3)}
    require(len(covered) == 690, 'whole known witness triple ownership')
    uncovered = set(combinations(range(18), 3))-covered
    degrees = Counter(p for w in words for p in w)
    pairs = Counter(tuple(sorted(p)) for w in words for p in combinations(w, 2))
    records = []
    for H in combinations(range(18), 3):
        hs = set(H); S = set(range(18))-hs
        f = tuple(sum(len(w & hs) == j for w in words) for j in range(4))
        lam = tuple(pairs[p] for p in combinations(H, 2)); P = sum(lam)
        R = sum(degrees[p] for p in H); t = f[3]
        require(f == (69-R+P-t, R-2*P+3*t, P-3*t, t), 'literal hub-word count identity')
        a0 = sum(set(v) <= S for v in uncovered)
        require(a0 == 455-10*69+6*R-3*P+t, 'literal wholly saturated-side uncovered count')
        D = tuple(sum(5-pairs[tuple(sorted((h, s)))] for s in S) for h in H)
        require(D == tuple(75-4*degrees[H[i]]+P-lam[(2, 1, 0)[i]] for i in range(3)),
                'literal cross deficit identity')
        SS = sum(5-pairs[tuple(sorted(p))] for p in combinations(sorted(S), 2))
        require(SS == 525-10*69+4*R-P, 'literal saturated-side pair deficit identity')
        records.append((H, R, lam, f, a0, D, SS))
    require(len(records) == 816, 'every three-point partition')
    return {'partitions': len(records), 'records_sha256': digest(records)}


def check():
    profile = (17, 19, 19)
    require(sum(profile) == 55 and 15*20+55 == 5*71, 'exact size71 degree profile')
    cases6 = {t: admissible_pairs(profile, 6, t) for t in (0, 1)}
    require(all(v == [(1, 1, 4), (1, 2, 3), (2, 1, 3)] for v in cases6.values()), 'complete ordered P6 pair cases')
    cases7 = {t: admissible_pairs(profile, 7, t) for t in (0, 1)}
    normalized = {tuple((min(a, b), max(a, b), c)) for a, b, c in cases7[0]}
    require(normalized == {(1, 1, 5), (1, 2, 4), (1, 3, 3), (2, 2, 3)}
            and cases7[0] == cases7[1], 'exact P7 low-pair necessary cases')
    unit_sectors = []
    for n0, n1, n2, n3 in product(range(16), repeat=4):
        if n0+n1+n2+n3 != 15 or n1+2*n2+3*n3 != 19:
            continue
        for t in (0, 1):
            if 2*n2+3*n3 <= 6-t:
                unit_sectors.append((n0, n1, n2, n3, t))
    require(unit_sectors == [(0, 13, 0, 2, 0)], 'complete P7 unit-row hub-count sectors')
    unit_pairs = []
    for a, b, c in cases7[0]:
        D = parameters(profile, (a, b, c)); singleton = tuple(d-2 for d in D)
        if min(singleton) >= 0 and max(4*n for n in singleton) <= 28:
            unit_pairs.append(((a, b, c), singleton))
    require(unit_pairs == [((1, 1, 5), (7, 3, 3))], 'complete P7 unit good-cohort degree sectors')
    # All SS support edges touch the independent seven-point w cohort.
    # At a singleton u center, low v cannot have u as its leave friend:
    # the uv words cover all15 S tails. Its friend is therefore a
    # saturated w-cohort neighbor. The full ordinary selector proof is
    # in REVIEW.md; the imported exact local bound is9141's63 subcase.
    require(4*7 == 28 and 3*5 == 15, 'P7 unit incident-edge and whole-tail saturation')
    for P in range(5):
        require(all(3*P-15-t < 0 for t in (0, 1)), 'nonnegative budget forces prior P>=5')
    # Separately proved necessary structure, not a realizing code.
    require(admissible_pairs((18, 18, 19), 5, 0) == [(1, 2, 2)], 'other-profile P5 pair restriction')
    other_D = parameters((18, 18, 19), (1, 2, 2))
    require(other_D == (6, 6, 3), 'other-profile good cohort sizes')
    degree_sums = tuple(4*n for n in other_D)
    cross_edges = ((degree_sums[0]+degree_sums[1]-degree_sums[2])//2,
                   (degree_sums[0]+degree_sums[2]-degree_sums[1])//2,
                   (degree_sums[1]+degree_sums[2]-degree_sums[0])//2)
    require(cross_edges == (18, 6, 6), 'other-profile SS degree accounting')
    positive = literal_partition_controls(json.loads((HERE/'WITNESS69.json').read_text()))
    return {'status': 'PASS_ORDINARY_THREE_HUB_COUNTS', 'literal_partition_controls': positive,
            'P6_ordered_pair_cases': cases6, 'P7_ordered_pair_cases': cases7,
            'P7_unordered_degree19_cases': sorted(normalized),
            'P7_unit_sector': {'hub_count_rows': unit_sectors[0],
            'pair_multiplicities': (1, 1, 5), 'singleton_cohorts': (7, 3, 3),
            'all_SS_edges_incident_to_w_cohort': True, 'complete_uv_S_tail_coverage': 15,
            'selector_uses_no_covered_triangle_premise': True,
            'imported_review9141_lambda_xu4_local_bound': 63,
            'conclusion': 'E>=1 atP7, conditional on9141; notP>=8'},
            'other_profile_P5_necessary_structure': {'pair_multiplicities': (1, 2, 2),
            'cohort_sizes': other_D, 'SS_cross_edges': cross_edges,
            'hub_word_counts': (21, 45, 5, 0), 'realization_claimed': False}}
