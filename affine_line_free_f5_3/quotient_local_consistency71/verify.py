"""Verify explicit planar realizations and the local-consistency obstruction."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import subprocess

from model import TEMPLATES, height_images, lift_profile, local_family, quotient_lines

SOURCE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def affine_lines(dimension):
    points = tuple(product(range(5), repeat=dimension))
    return {frozenset(tuple((x+t*(y-x)) % 5 for x, y in zip(p, q))
                      for t in range(5)) for p, q in combinations(points, 2)}


PLANE_LINES = tuple(sum(1 << (5*x+y) for x, y in line)
                    for line in affine_lines(2))


def check_rows(rows, profile, cap):
    require(len(rows) == 5 and all(type(r) is int and 0 <= r < 32 for r in rows),
            'bad row masks')
    require(tuple(r.bit_count() for r in rows) == tuple(profile), 'row profile mismatch')
    mask = sum(r << (5*t) for t, r in enumerate(rows))
    require(max((mask & line).bit_count() for line in PLANE_LINES) <= cap,
            'planar line cap violated')


def canonical(profile):
    return min(tuple(profile[(a*t+b) % 5] for t in range(5))
               for a in range(1, 5) for b in range(5))


def domain(size):
    return tuple(m for m in range(32) if m.bit_count() == size)


def check_distribution(images, profile):
    require(len(images) == 100, 'affine averaging group size')
    for t, size in enumerate(profile):
        law = Counter(row[t] for row in images)
        expected = {mask: 100//comb(5, size) for mask in domain(size)}
        require(law == expected, 'nonuniform full-fiber marginal')
    pair_count = 0
    for i, j in combinations(range(5), 2):
        if profile[i] != 4 and profile[j] != 4:
            continue
        counts = Counter((row[i], row[j]) for row in images)
        denominator = comb(5, profile[i])*comb(5, profile[j])
        expected = {pair: 100//denominator for pair in product(domain(profile[i]), domain(profile[j]))}
        require(counts == expected, 'two-fiber transitivity involving a full fiber')
        pair_count += 1
    return pair_count


def audit_profiles():
    require(len(PLANE_LINES) == 30, 'planar line count')
    counts = {}
    pairs = 0
    for cap, target, orbit_count in ((4, 16, 6), (3, 10, 7)):
        top = {w for w in product(range(cap+1), repeat=5) if sum(w) == target}
        canon = {canonical(w) for w in top}
        require(len(canon) == orbit_count and canon == {p for k, p in TEMPLATES if k == cap},
                'template orbit coverage')
        for p in sorted(canon):
            rows = TEMPLATES[cap, p]
            check_rows(rows, p, cap)
            images = tuple(height_images(rows))
            for image in images:
                check_rows(image, p, cap)
            pairs += check_distribution(images, p)
        accepted = 0
        for w in product(range(cap+1), repeat=5):
            if sum(w) > target:
                try:
                    lift_profile(w, cap)
                except ValueError:
                    continue
                raise ValueError('constructor accepted an out-of-domain profile')
            check_rows(lift_profile(w, cap), w, cap)
            accepted += 1
        counts[str(cap)] = {'top_profiles': len(top), 'affine_profile_orbits': len(canon),
                            'all_profiles_constructed': accepted}
    malformed = [([-1, 0, 0, 0, 0], 4), ([False, 0, 0, 0, 0], 4),
                 ([0, 0, 0, 0], 4), ([5, 0, 0, 0, 0], 4), ([0]*5, 2)]
    for w, cap in malformed:
        try:
            lift_profile(w, cap)
        except ValueError:
            continue
        raise ValueError('malformed profile accepted')
    # Reject a corrupted geometric template even if its profile metadata
    # is updated to agree with the added selected point.
    bad = list(TEMPLATES[4, (0, 4, 4, 4, 4)])
    bad[0] = 1
    try:
        check_rows(bad, [r.bit_count() for r in bad], 4)
    except ValueError:
        pass
    else:
        raise ValueError('a full affine line was not rejected')
    return counts, pairs


def audit_control(record, space_lines):
    weights, total = record['weights'], record['total']
    require(len(weights) == 25 and all(type(w) is int and 0 <= w <= 4 for w in weights),
            'bad control weights')
    require(sum(weights) == total, 'control total')
    lines = quotient_lines()
    planes = [frozenset((x, y, z) for x, y in line for z in range(5)) for line in lines]
    require(len(planes) == 30 and len(set(planes)) == 30, 'projection-plane family')
    incidence = Counter()
    for plane in planes:
        contained = [line for line in space_lines if line <= plane]
        require(len(contained) == 30, 'lines in a projection plane')
        incidence.update(contained)
    require(set(incidence) == space_lines and Counter(incidence.values()) == {1: 750, 6: 25},
            'all 775 affine lines must be covered')
    profile_sizes = []
    full = [(x, y) for x, y in product(range(5), repeat=2) if weights[5*x+y] == 4]
    anchors = next((p, q, r) for p, q, r in combinations(full, 3)
                   if ((q[0]-p[0])*(r[1]-p[1])-(r[0]-p[0])*(q[1]-p[1])) % 5)
    laws = defaultdict(list)
    conditional = defaultdict(list)
    gauge_sizes = []
    pair_count = 0
    for line in lines:
        profile = tuple(weights[5*x+y] for x, y in line)
        m = sum(profile)
        require(total-64 <= m <= 16, 'quotient line weight')
        cap = 3 if m <= 10 else 4
        require(cap <= (m+80-total)//5, 'control violates a pencil-derived line cap')
        images = tuple(height_images(lift_profile(profile, cap)))
        for image in images:
            check_rows(image, profile, cap)
        pair_count += check_distribution(images, profile)
        anchor_positions = [i for i, p in enumerate(line) if p in anchors]
        require(len(anchor_positions) <= 2, 'three anchors must not be collinear')
        conditioned = [row for row in images if all(row[i] == 30 for i in anchor_positions)]
        require(conditioned, 'a single plane failed the three-hole gauge restriction')
        gauge_sizes.append(len(conditioned))
        for i, p in enumerate(line):
            laws[p].append(Counter(row[i] for row in images))
            law = Counter(row[i] for row in conditioned)
            conditional[p].append(tuple(sorted((mask, Fraction(count, len(conditioned)))
                                               for mask, count in law.items())))
        profile_sizes.append(m)
    require(all(len(v) == 6 and all(law == v[0] for law in v) for v in laws.values()),
            'full shared-fiber marginals do not match')
    mismatches = sum(len(set(v)) > 1 for v in conditional.values())
    if total == 71:
        family = local_family(weights)
        require(len(family) == 30, 'public local-family constructor')
    return {'name': record['name'], 'total': total,
            'plane_size_histogram': dict(sorted(Counter(profile_sizes).items())),
            'overlap_fibers_verified': len(laws), 'two_fiber_pair_laws_verified': pair_count,
            'gauge_anchor_positions': anchors,
            'all_individual_planes_survive_gauge': True,
            'conditioned_recipe_fibers_with_mismatches': mismatches,
            'gauge_conditioned_consistency_claimed': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--sanitize', action='store_true')
    parser.add_argument('--check-expected', action='store_true')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    exe = (args.out/'planar_cap').resolve()
    flags = ['-std=c++20', '-Wall', '-Wextra', '-Wconversion', '-Werror']
    flags += (['-O1', '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer']
              if args.sanitize else ['-O3'])
    subprocess.run(['g++', *flags, str(SOURCE/'planar_cap.cpp'), '-o', str(exe)], check=True)
    cap = json.loads(subprocess.check_output([str(exe)]))
    require(cap == {'seventeen_subsets': 1081575, 'line_free_seventeen_subsets': 0},
            'planar cap audit')
    profiles, template_pairs = audit_profiles()
    space_lines = affine_lines(3)
    require(len(space_lines) == 775, 'three-dimensional affine lines')
    controls = [audit_control(r, space_lines)
                for r in json.loads((SOURCE/'quotient_controls.json').read_text())]
    result = {'status': 'UNIVERSAL_QUOTIENT_LOCAL_CONSISTENCY_VERIFIED',
              'profiles': profiles, 'templates': len(TEMPLATES),
              'template_pair_laws_verified': template_pairs, 'planar_cap': cap,
              'controls': controls,
              'template_sha256': hashlib.sha256((SOURCE/'templates.json').read_bytes()).hexdigest(),
              'global_71_lifting_decision': 'OPEN', 'optimizer_required': False}
    # Normalize tuple and integer dictionary keys exactly as serialized.
    result = json.loads(json.dumps(result))
    if args.check_expected:
        require(result == json.loads((SOURCE/'EXPECTED.json').read_text()), 'expected result mismatch')
    (args.out/'verified.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
