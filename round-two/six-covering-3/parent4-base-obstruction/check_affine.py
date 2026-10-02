"""Literal independent audit of all288 prefix affine maps and270 phase pairs.

Uses general CRT by finite candidate testing rather than producer v formula.
All original phase permutations are checked, with the congruence transport
bridge justified algebraically in proof.md. No native solver.
"""
from hashlib import sha256
from itertools import product
from math import gcd
import json

from affine import group, normalize, normalizer, REPS15, REPS18


def require(ok, message):
    if not ok:
        raise ValueError(message)


def run():
    P = [(8, 0), (9, 0), (10, 1), (14, 1), (12, 10)]
    B = [n for n in range(8, 2521) if 2520 % n == 0 and n not in (8, 9, 10, 12, 14)]
    # All576 units, all35 translations allowed by8:0 and9:0. Test EVERY
    # original prefix phase equation, including the mandatory12:10.
    found = []
    for u in range(2520):
        if gcd(u, 2520) != 1:
            continue
        for v in range(0, 2520, 72):
            if all((u * a + v) % n == a for n, a in P):
                found.append((u, v))
    require(found == group() and len(found) == 288, 'Complete affine prefix stabilizer differs')
    elements = set(found)
    require((1, 0) in elements and all(((u * w) % 2520, (u * z + v) % 2520) in elements
            for u, v in found for w, z in found), 'Affine group not closed')
    physical_transports = phase_permutations = 0
    digest = sha256()
    initial = {x for x in range(2520) if all(x % n != a for n, a in P)}
    for u, v in found:
        require(v % 72 == 0 and u % 3 == 1 and (u + v) % 35 == 1,
                'Independent CRT stabilizer structure')
        for n in B:
            image = [(u * a + v) % n for a in range(n)]
            require(sorted(image) == list(range(n)) and gcd(u, n) == 1,
                    'Original phase action not a bijection')
            digest.update(json.dumps([u, v, n, image], separators=(',', ':')).encode() + b'\n')
            phase_permutations += len(image)
        mapped = set()
        for x in range(2520):
            t = (u * x + v) % 2520
            require((x in initial) == (t in initial) and (x % 8 == 4) == (t % 8 == 4)
                    and x % 3 == t % 3, 'Physical P/parent4/color transport differs')
            require(all(t % d == (u * (x % d) + v) % d for d in (5, 7, 9)),
                    'Literal CRT coordinate transport')
            mapped.add(t)
            physical_transports += 1
        require(len(mapped) == 2520, 'Physical affine transport is not bijective')
    orbits = {}
    witnesses = []
    for a in range(15):
        for b in range(18):
            images = {(u * a + v) % 15 * 18 + (u * b + v) % 18 for u, v in found}
            representative = min(images)
            ra, rb = divmod(representative, 18)
            orbits.setdefault(representative, images)
            require(ra in REPS15 and rb in REPS18
                    and all(divmod(i, 18)[0] % 3 == a % 3 for i in images),
                    'Simultaneous original15/18 representatives differ')
            u, v = normalizer(a, b)
            require(((u * a + v) % 15, (u * b + v) % 18) == (ra, rb),
                    'Producer normalizer lost lex orbit representative')
            witnesses.append([a, b, ra, rb, u, v, len(images)])
    reps = [divmod(i, 18) for i in sorted(orbits)]
    require(reps == list(product(REPS15, REPS18)) and len(reps) == 60
            and sum(len(o) for o in orbits.values()) == 270
            and set().union(*orbits.values()) == set(range(270)),
            'Original phase-pair orbit cover incomplete')
    # Every18 phase of color0 is fixed separately modulo9:0/3/6 cannot
    # be pooled. A false six-class18 normalization would discard a route.
    require({(u * 3 + v) % 18 for u, v in found} == {3}
            and {(u * 12 + v) % 18 for u, v in found} == {12},
            'Original18 fixed-color0 singleton control')
    u, v = 11, 2160
    require(gcd(u, 2520) == 1 and all((u * a + v) % n == a for n, a in P if n != 12)
            and (u * 10 + v) % 12 != 10 and (u, v) not in elements,
            'Missing12:10 prefix-control map incorrectly admitted')
    phases = [[n, (7 * n + 11) % n] for n in B]
    normalized, transform = normalize(phases)
    uu, vv = transform
    require([n for n, a in normalized] == B and dict(normalized)[15] in REPS15
            and dict(normalized)[18] in REPS18, 'Whole original inventory normalization')
    holes = {x for x in initial if all(x % n != a for n, a in phases)}
    transformed_holes = {(uu * x + vv) % 2520 for x in holes}
    literal_new_holes = {x for x in initial if all(x % n != a for n, a in normalized)}
    require(literal_new_holes == transformed_holes, 'Literal actual BASE hole transport')
    return {'agent': 'six-covering-3', 'role': 'researcher', 'all_units_tested': 576,
            'all72_multiple_translations_per_unit': 35, 'complete_prefix_group': 288,
            'all_group_products_checked': 82944, 'all_physical_point_transports': physical_transports,
            'all_original_phase_permutations': phase_permutations,
            'all_phase_permutations_sha256': digest.hexdigest(),
            'complete_original15_18_phase_pairs': 270, 'pair_orbits': 60,
            'canonical15': list(REPS15), 'canonical18': list(REPS18),
            'all_pair_normalizers_sha256': sha256(json.dumps(witnesses, separators=(',', ':')).encode()).hexdigest(),
            'missing_prefix12_control': [11, 2160], 'original18_fixed_phase_controls': [3, 12],
            'literal_whole_BASE_phase_inventory_transport': True,
            'normalization_projection_equivalence_ordinary_unformalized': True,
            'historical_priority_or_external_review_claimed': False,
            'native_solver_run': False, 'fullcover_found': False}


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True))
