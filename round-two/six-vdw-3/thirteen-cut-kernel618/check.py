#!/usr/bin/env python3
"""Independently audit every core using unordered field endpoints and affine maps.

Imports no census generator or previous local-profile implementation. Tests use
explicit exceptions, so all checks remain active under optimized Python.
"""
import argparse
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def audit(data):
    q = 103
    inv2, inv4, inv6 = (pow(d, -1, q) for d in (2, 4, 6))
    points = range(q)
    pattern = frozenset((2+j) % q for j in range(-4, 5)) | frozenset((2+j*inv2) % q for j in (-3, -1, 1, 3))
    endpoints = list(itertools.combinations(points, 2))
    seven = {}
    for first, last in endpoints:
        slope = (last-first)*inv6 % q
        support = tuple(sorted((first+j*slope) % q for j in range(7)))
        require(len(support) == 7, 'Collapsed field seven')
        seven[first, last] = support, frozenset(support)
    template = sorted({s for s, support in seven.values() if support <= pattern})
    require(len(template) == 6, 'Incorrect endpoint-derived pattern supports')

    # Derive the complete affine quotient by direct images, independently of
    # the six lambda transformations used by the proposal.
    reps = data.get('representatives')
    require(isinstance(reps, list) and reps == sorted(set(reps)), 'Bad representatives')
    require(all(isinstance(x, int) and 2 <= x < q for x in reps), 'Bad representative domain')
    owner = {}
    orbit_counts = {}
    for lam in reps:
        orbit = {tuple(sorted((offset, (offset+scale) % q, (offset+scale*lam) % q)))
                 for scale in range(1, q) for offset in points}
        orbit_counts[str(lam)] = len(orbit)
        for holes in orbit:
            require(holes not in owner, 'Affine quotient overlaps')
            owner[holes] = lam
        normalized = [h[2] for h in orbit if h[:2] == (0, 1)]
        require(min(normalized) == lam, 'Nonminimal normalized representative')
    require(len(owner) == math.comb(q, 3), 'Affine quotient fails total count')
    raw_triples = 0
    for holes in itertools.combinations(points, 3):
        require(holes in owner, 'Raw hole triple missing')
        raw_triples += 1

    classes = []
    endpoint_core_tests = 0
    essential_keys = set()
    for lam in reps:
        holes = {0, 1, lam}
        rows = {}
        eligible = 0
        for first, last in endpoints:
            slope = (last-first)*inv4 % q
            center = (first+last)*inv2 % q
            seed = tuple(sorted((center+j*slope) % q for j in range(-2, 3)))
            if holes.intersection(seed):
                continue
            eligible += 1
            full_core = {(center+j*slope) % q for j in range(-4, 5)}
            full_core.update((center+j*slope*inv2) % q for j in (-3, -1, 1, 3))
            core = tuple(sorted(full_core - holes))
            regular = frozenset(core)
            available = []
            for pair in itertools.combinations(core, 2):
                endpoint_core_tests += 1
                candidate, support = seven[pair]
                if support <= regular:
                    available.append(candidate)
            witness = min(available) if available else None
            row = {'seed': list(seed), 'core': list(core),
                   'field_seven_witness': list(witness) if witness is not None else None}
            require(core not in rows, 'Distinct seed endpoint pairs have the same core')
            rows[core] = row
        ordered = [rows[core] for core in sorted(rows)]
        digest = hashlib.sha256()
        for row in ordered:
            digest.update((json.dumps(row, sort_keys=True, separators=(',', ':')) + '\n').encode())
        exceptional = [r for r in ordered if r['field_seven_witness'] is None]
        for row in exceptional:
            essential_keys.add((lam, tuple(row['seed']), tuple(row['core'])))
        histogram = Counter(len(r['core']) for r in ordered)
        classes.append({
            'lambda': lam, 'holes': sorted(holes), 'eligible_seed_supports': eligible,
            'distinct_regular_cores': len(ordered), 'locally_covered_cores': len(ordered) - len(exceptional),
            'cores_without_field_seven': len(exceptional),
            'core_size_histogram': {str(k): histogram[k] for k in sorted(histogram)},
            'all_core_rows_sha256': digest.hexdigest(), 'exceptional_cores': exceptional,
        })

    # A second coverage mechanism: exhaust seed-disjoint normalized triples,
    # then move the surviving transversals by every affine field map.
    normalized_seed = set(range(5))
    normalized_transversals = []
    seed_disjoint_holes = 0
    for holes in itertools.combinations((x for x in points if x not in normalized_seed), 3):
        seed_disjoint_holes += 1
        hole_set = set(holes)
        if all(hole_set.intersection(support) for support in template):
            normalized_transversals.append(holes)
    target = {tuple(sorted((0, 1, lam))): lam for lam in reps}
    transported_keys = set()
    affine_matching_maps = Counter()
    affine_maps_checked = 0
    for holes in normalized_transversals:
        for scale in range(1, q):
            for offset in points:
                affine_maps_checked += 1
                image_holes = tuple(sorted((scale*x+offset) % q for x in holes))
                if image_holes not in target:
                    continue
                lam = target[image_holes]
                affine_matching_maps[lam] += 1
                image_seed = tuple(sorted((scale*x+offset) % q for x in normalized_seed))
                image_core = tuple(sorted({(scale*x+offset) % q for x in pattern} - set(image_holes)))
                transported_keys.add((lam, image_seed, image_core))
    require(transported_keys == essential_keys, 'Affine transversal census disagrees with endpoint core census')

    expected = {'agent': 'six-vdw-3', 'role': 'researcher', 'q': q,
                'pattern': sorted(pattern), 'field_sevens_in_pattern': [list(s) for s in template],
                'representatives': reps, 'classes': classes,
                'full_cyclic_exclusion_claimed': False, 'W_bound_improved': False}
    for key in ('eligible_seed_supports', 'distinct_regular_cores', 'locally_covered_cores', 'cores_without_field_seven'):
        expected['total_' + key] = sum(c[key] for c in classes)
    require(data == expected, 'Census bytes decode to a different complete record')
    return {'status': 'COMPLETE_ENDPOINT_AND_AFFINE_CENSUSES_AGREE',
            'all_seed_endpoint_pairs_per_class': len(endpoints),
            'raw_three_hole_triples': raw_triples, 'raw_orbit_sizes': orbit_counts,
            'all_core_endpoint_tests': endpoint_core_tests,
            'seed_disjoint_normalized_hole_triples': seed_disjoint_holes,
            'normalized_seven_transversals': [list(h) for h in normalized_transversals],
            'exceptional_affine_maps_checked': affine_maps_checked,
            'exceptional_matching_affine_maps': {str(k): affine_matching_maps[k] for k in sorted(affine_matching_maps)},
            'total_core_supports': expected['total_distinct_regular_cores'],
            'locally_covered_core_supports': expected['total_locally_covered_cores'],
            'exceptional_core_supports': expected['total_cores_without_field_seven'],
            'nonlocal_cut_classes': sorted({k[0] for k in essential_keys}),
            'full_cyclic_exclusion_claimed': False, 'W_bound_improved': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--census', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = audit(json.loads(args.census.read_text()))
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))
