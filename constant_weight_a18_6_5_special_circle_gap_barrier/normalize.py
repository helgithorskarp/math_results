"""Pointed construction and separate literal cover of the special cohort.

All C(63,2) pairs around the chosen H-circle generate the orbit domain.
Literal images are separately checked against every eligible labeled triple.
No automorphism of an unknown packing or unclassified design is assumed.
"""
from collections import Counter
from itertools import combinations
from math import comb
import time
from common import close_group, digest, mask, move, points, require

FIXED = 15


def normalize(circles):
    group, actions = close_group(circles)
    start = time.monotonic()
    design = tuple(frozenset(points(c)) for c in circles)
    q = frozenset(points(FIXED))
    contained = {frozenset(r) for c in design for r in combinations(sorted(c), 4)}
    noncontained = set(map(frozenset, combinations(range(17), 4))) - contained
    require({frozenset(p[i] for i in q) for p in group} == noncontained
            and len(noncontained) == 2040, 'noncontained-word orbit incomplete')
    stab = sorted((p, a) for p, a in zip(group, actions)
                  if frozenset(p[i] for i in q) == q)
    require(len(stab) == 8, 'wrong actual pointed stabilizer order')
    indices = {c: i for i, c in enumerate(circles)}
    forced = {c for c, pts in zip(circles, design) if len(pts & q) >= 3}
    require(sorted(forced) == [6155, 9223, 16910, 33037], 'wrong forced gaps')
    owners = [frozenset(points(c)) for c in sorted(forced)]
    require(all(len(a & b) == 2 and a & b <= q for a, b in combinations(owners, 2)),
            'forced circles have incorrect intersections')
    require(all(len(a - q) == 2 for a in owners)
            and all(not (a - q) & (b - q) for a, b in combinations(owners, 2)),
            'outside parts of forced circles are not disjoint pairs')
    n = frozenset(range(17)) - frozenset().union(*owners)
    require(n == frozenset([4, 5, 6, 7, 16]), 'wrong five-point complement')
    special = {c for c, pts in zip(circles, design)
               if len(pts & q) == len(pts & n) == 2}
    require(sorted(special) == [362, 661, 1178, 2149, 4262, 8281, 16553, 32854],
            'wrong incidence-defined special family')
    require({move(362, p) for p, a in stab} == special and len(special) == 8,
            'chosen special circle does not cover the full family')
    for p, a in stab:
        require({move(c, p) for c in circles} == set(circles), 'point map moves the design')
        require({move(c, p) for c in forced} == forced, 'point map moves forced gaps')
        require(frozenset(p[i] for i in n) == n
                and {move(c, p) for c in special} == special, 'point map moves N or H')
        require(all(move(c, p) == circles[a[indices[c]]] for c in circles),
                'point and circle actions disagree entrywise')
    extras = set(circles) - forced
    require(len(extras) == 64 and special <= extras, 'bad extra-circle domain')
    representatives = set()
    pointed_pairs = 0
    for pair in combinations(sorted(extras - {362}), 2):
        require(time.monotonic() - start < 45, 'INCOMPLETE: pointed normalization guard')
        triple = (362, *pair)
        images = {tuple(sorted(circles[a[indices[c]]] for c in triple)) for p, a in stab}
        representatives.add(min(images))
        pointed_pairs += 1
    require(pointed_pairs == comb(63, 2) == 1953 and len(representatives) == 1763,
            'pointed normalization count differs')
    # This domain is enumerated with literal point sets, rather than by
    # canonicalizing the pointed input stream.
    literal_extras = [pts for c, pts in zip(circles, design) if c in extras]
    literal_special = {frozenset(points(c)) for c in special}
    universe = {tuple(sorted(mask(c) for c in triple))
                for triple in combinations(literal_extras, 3)
                if any(c in literal_special for c in triple)}
    require(len(universe) == comb(64, 3) - comb(56, 3) == 13944,
            'literal labeled-triple count differs')
    covered, cases = set(), []
    for triple in sorted(representatives):
        require(time.monotonic() - start < 45, 'INCOMPLETE: literal cover guard')
        orbit = {tuple(sorted(move(c, p) for c in triple)) for p, a in stab}
        literal = {tuple(sorted(mask(p[i] for i in points(c)) for c in triple))
                   for p, a in stab}
        require(orbit == literal and min(orbit) == triple
                and orbit <= universe and not orbit & covered,
                'literal orbits differ, overlap, or leave the cohort')
        require(8 % len(orbit) == 0, 'wrong pointed orbit size')
        for p, a in stab:
            require({tuple(sorted(move(c, p) for c in other)) for other in orbit} == orbit,
                    'literal orbit is not closed')
        cases.append({'case': len(cases), 'extra_gaps': list(triple),
                      'gaps': sorted(forced | set(triple)), 'orbit_size': len(orbit)})
        covered.update(orbit)
    require(covered == universe and sum(c['orbit_size'] for c in cases) == 13944,
            'special cohort is not completely covered')
    summary = {'fixed_word': FIXED, 'group_order': len(group),
               'noncontained_words': len(noncontained), 'stabilizer_order': len(stab),
               'forced_gaps': sorted(forced), 'complement_points': sorted(n),
               'special_circles': sorted(special), 'pointed_pairs': pointed_pairs,
               'orbits': len(cases), 'labeled_triples': len(covered),
               'orbit_size_histogram': {str(k): v for k, v in
                                        sorted(Counter(c['orbit_size'] for c in cases).items())},
               'cases_sha256': digest(cases)}
    return cases, summary, tuple(p for p, a in stab)
