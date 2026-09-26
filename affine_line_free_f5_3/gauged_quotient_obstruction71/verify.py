#!/usr/bin/env python3
"""Definition-level exact audit. No solver or numerical package is used."""
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

import model

ROOT = Path(__file__).resolve().parent
require = model.require


def affine_lines(dimension):
    """Generate unordered geometric lines from pairs, independent of the model."""
    points = tuple(product(range(5), repeat=dimension))
    lines = set()
    for p, q in combinations(points, 2):
        line = tuple(sorted(tuple((x+t*(y-x)) % 5 for x, y in zip(p, q)) for t in range(5)))
        lines.add(line)
    return tuple(sorted(lines))


PLANAR_LINES = affine_lines(2)
PLANAR_MASKS = tuple(sum(1 << (5*t+z) for t, z in line) for line in PLANAR_LINES)


@lru_cache(maxsize=None)
def max_line(rows):
    mask = sum(r << (5*t) for t, r in enumerate(rows))
    return max((mask & line).bit_count() for line in PLANAR_MASKS)


def check_law(profile, law, cap):
    require(bool(law) and sum(law.values(), Fraction(0)) == 1, 'mass is not one')
    marginals = [defaultdict(Fraction) for _ in range(5)]
    for rows, mass in law.items():
        require(type(mass) is Fraction and mass > 0, 'bad rational mass')
        require(len(rows) == 5 and all(type(m) is int and 0 <= m < 32 for m in rows), 'bad masks')
        require(tuple(m.bit_count() for m in rows) == tuple(profile), 'wrong profile')
        require(all(not m & 1 for m in rows), 'a selected point has height zero')
        require(max_line(rows) <= cap, 'geometric line cap violated')
        for t, mask in enumerate(rows):
            marginals[t][mask] += mass
    for v, marginal in zip(profile, marginals):
        domain = tuple(x for x in range(32) if not x & 1 and x.bit_count() == v)
        expected = {m: Fraction(1, len(domain)) for m in domain}
        require(dict(marginal) == expected, 'full fiber law is not uniform outside zero')


def reject_controls():
    cases = [(model.ordinary_law, (4, 4, 4, 4, 1)),
             (model.ordinary_law, (5, 0, 0, 0, 0)),
             (model.small_law, (4, 0, 0, 0, 0)),
             (model.small_law, (3, 3, 3, 3, 0)),
             (model.family71, [3]*25)]
    for function, arg in cases:
        try:
            function(arg)
        except ValueError:
            pass
        else:
            raise ValueError('an invalid input was accepted')
    broken = {(0, 2, 14, 22, 29): Fraction(1)}
    try:
        check_law((0, 1, 3, 3, 4), broken, 3)
    except ValueError:
        pass
    else:
        raise ValueError('corrupted template was accepted')
    law = model.ordinary_law((1, 3, 4, 4, 4))
    law[next(iter(law))] += Fraction(1, 10)
    try:
        check_law((1, 3, 4, 4, 4), law, 4)
    except ValueError:
        pass
    else:
        raise ValueError('bad normalization was accepted')
    return len(cases)+2


def audit():
    require(len(PLANAR_LINES) == 30, 'wrong planar geometry')
    templates = model.load_templates()
    top = [p for p in product(range(4), repeat=5) if sum(p) == 10]
    canonical = {min(tuple(p[(a*t+b) % 5] for t in range(5))
                     for a in range(1, 5) for b in range(5)) for p in top}
    require(canonical == set(templates) and len(top) == 101, 'incomplete top-profile cover')
    for p in top:
        check_law(p, model.small_top_law(p, templates), 3)
    counts = {}
    for cap, bound, function in ((4, 16, model.ordinary_law), (3, 10, model.small_law)):
        count = 0
        for profile in product(range(cap+1), repeat=5):
            if sum(profile) <= bound:
                check_law(profile, function(profile), cap)
                count += 1
        counts[str(cap)] = count
    spatial = affine_lines(3)
    require(len(spatial) == 775, 'wrong spatial geometry')
    quotient = model.quotient_lines()
    require({tuple(sorted(L)) for L in quotient} == set(PLANAR_LINES), 'wrong quotient geometry')
    coverage = Counter()
    for L in quotient:
        for ell in spatial:
            if all((x, y) in L for x, y, z in ell):
                coverage[ell] += 1
    require(set(coverage) == set(spatial) and Counter(coverage.values()) == {1: 750, 6: 25},
            'projection planes do not cover all spatial lines correctly')
    weights = (0, 0, 1, 3, 3, 1, 4, 4, 3, 4, 2, 4, 4, 3, 3, 2, 4, 4, 3, 3, 2, 4, 3, 4, 3)
    all_marginals = defaultdict(list)
    sizes = Counter()
    for L, law in model.family71(weights):
        profile = tuple(weights[5*x+y] for x, y in L)
        check_law(profile, law, 3 if sum(profile) <= 10 else 4)
        sizes[sum(profile)] += 1
        for t, p in enumerate(L):
            marginal = defaultdict(Fraction)
            for rows, mass in law.items():
                marginal[rows[t]] += mass
            all_marginals[p].append(dict(marginal))
    require(len(all_marginals) == 25 and all(len(v) == 6 and all(m == v[0] for m in v)
                                           for v in all_marginals.values()), 'overlap disagreement')
    require(all(m == {30: Fraction(1)} for p, values in all_marginals.items()
                if weights[5*p[0]+p[1]] == 4 for m in values), 'full-fiber gauge not fixed')
    layer_expected = [sum(sum(mass for mask, mass in values[0].items() if mask >> z & 1)
                          for values in all_marginals.values()) for z in range(5)]
    require(layer_expected == [0]+[Fraction(71, 4)]*4, 'wrong transverse plane expectations')
    box = {p for p in product(range(1, 5), repeat=3)}
    require(len(box) == 64 and all(not set(L) <= box for L in spatial), '64-point sharpness control failed')
    rejects = reject_controls()
    return {'status': 'UNIVERSAL_GAUGED_MARGINAL_OBSTRUCTION_VERIFIED',
            'ordinary_profiles': counts['4'], 'small_profiles': counts['3'],
            'small_top_profiles': len(top), 'small_affine_profile_types': len(templates),
            'small_templates': sum(len(v) for v in templates.values()),
            'spatial_lines': len(spatial), 'overlap_fibers_checked': len(all_marginals),
            'control_full_fibers_fixed': sum(v == 4 for v in weights),
            'control_plane_sizes': {str(k): v for k, v in sorted(sizes.items())},
            'control_layer_expectations': [str(x) for x in layer_expected],
            'global_empty_plane_bound': 64, 'global_71_decision': 'OPEN',
            'negative_controls': rejects, 'optimizer_required': False,
            'templates_sha256': hashlib.sha256((ROOT/'small_templates.json').read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--sanitize', action='store_true')
    parser.add_argument('--check-expected', action='store_true')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    flags = ['-O1', '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer', '-no-pie'] if args.sanitize else ['-O3']
    binary = args.out/'planar_cap'
    subprocess.run(['g++', '-std=c++20', '-Wall', '-Wextra', '-Wconversion', *flags,
                    str(ROOT/'planar_cap.cpp'), '-o', str(binary)], check=True)
    cap = json.loads(subprocess.check_output([str(binary.resolve())], text=True))
    require(cap == {'seventeen_subsets': 1081575, 'line_free_seventeen_subsets': 0}, 'planar cap failed')
    result = audit()
    result['planar_cap'] = cap
    if args.check_expected:
        require(result == json.loads((ROOT/'EXPECTED.json').read_text()), 'expected summary mismatch')
    (args.out/'verified.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
