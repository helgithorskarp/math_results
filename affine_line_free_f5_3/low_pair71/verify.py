"""Optimizer-free replay of the 71-point low-plane pair theorem.

The C++ census is rerun in full. Everything after that uses exact Python
integers. No assertions are used as verification conditions, so -O is safe.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path
import random
import subprocess

from model import (FORMS, LOW_PROFILES, case_rhs, character, incidence_system,
                   parallel_profiles, projective_points)

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def weak_compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for tail in weak_compositions(total-first, length-1):
                yield (first,) + tail


def audit_profiles():
    # Independent generation by ordered deficit compositions, with no sorting
    # or permutation of a five-tuple of section sizes.
    direct = set()
    all_centered = set()
    low_at_zero = set()
    for d in weak_compositions(9, 5):
        p = tuple(16-x for x in d)
        if p[0] <= 9:
            low_at_zero.add(p)
        if sum(t*p[t] for t in range(5)) % 5:
            continue
        q = sum(t*t*p[t] for t in range(5)) % 5
        all_centered.add((p, q))
        if q in (0, 1, 2):
            direct.add((p, q))
    require(direct == set(parallel_profiles()), 'parallel profile coverage')
    for p, q in all_centered:
        # At least one legitimate scaling of the normal has canonical q.
        images = []
        for scale in (1, 2, 3, 4):
            image = tuple(p[(pow(scale, -1, 5)*t) % 5] for t in range(5))
            newq = sum(t*t*image[t] for t in range(5)) % 5
            require(newq == scale*scale*q % 5, 'quadratic scaling identity')
            images.append((image, newq))
        require(any(image in direct for image in images), 'normal scaling cover')
    # The five pair-cover profiles use only multiplication of field labels.
    covered = set()
    for p in LOW_PROFILES:
        for scale in (1, 2, 3, 4):
            covered.add(tuple(p[(pow(scale, -1, 5)*t) % 5] for t in range(5)))
    require(covered == low_at_zero, 'five low-plane profile orbit cover')
    means = tuple(sum(t*p[t] for t in range(5)) % 5 for p in LOW_PROFILES)
    variances = tuple((sum(t*t*p[t] for t in range(5))-mean*mean) % 5
                      for p, mean in zip(LOW_PROFILES, means))
    require(means == (0, 4, 3, 2, 0), 'low profile barycenters')
    require(variances == (0, 3, 4, 1, 3), 'low profile quadratic moments')
    for p, q in direct:
        if q == 0 and min(p) <= 9:
            require(p == LOW_PROFILES[0], 'zero quadratic low profile')
    ranges = []
    for i, j in combinations_with_replacement(range(5), 2):
        m, n = LOW_PROFILES[i][0], LOW_PROFILES[j][0]
        cap = (m+n-7)//5
        minimum, maximum = m+n-7-cap, m+n-7
        require(0 <= cap <= 2 and maximum <= 11, 'interior bounds')
        for total in range(minimum, maximum+1):
            d00 = 11-m-n+total
            require(4-cap <= d00 <= 4, 'boundary reconstruction')
        ranges.append([i, j, cap, minimum, maximum])
    # Five weight-four points in the interior contain an affine frame:
    # each quotient line has at most four interior points.
    interior = set(product(range(1, 5), repeat=2))
    for a, b in projective_points(2):
        for c in range(5):
            require(sum((a*x+b*y) % 5 == c for x, y in interior) <= 4,
                    'interior line bound')
    return dict(ordered_profiles=len(direct), low_profiles=len(LOW_PROFILES),
                normalized_pair_types=len(ranges), pair_ranges=ranges)


def audit_quadratic_forms():
    normals = projective_points(3)
    require(len(normals) == 31, 'number of normal directions')
    expected = {counts for _, counts in FORMS.values()}
    require(len(expected) == 7, 'seven distinct character distributions')
    for diagonal, counts in FORMS.values():
        values = [sum(d*x*x for d, x in zip(diagonal, v)) % 5 for v in normals]
        actual = tuple(sum(character(q) == c for q in values) for c in (0, 1, -1))
        require(actual == counts, 'canonical form character counts')
    # Inspect every symmetric matrix independently of diagonalization.
    evaluation = [(x*x, y*y, z*z, 2*x*y, 2*x*z, 2*y*z) for x, y, z in normals]
    frequencies = Counter()
    for coefficients in product(range(5), repeat=6):
        count = Counter(character(sum(a*b for a, b in zip(coefficients, row)))
                        for row in evaluation)
        vector = tuple(count[c] for c in (0, 1, -1))
        require(vector in expected, 'uncovered symmetric moment matrix')
        frequencies[vector] += 1
    require(sum(frequencies.values()) == 15625, 'symmetric matrix total')
    return {name: frequencies[counts] for name, (_, counts) in FORMS.items()}


def audit_geometry():
    points = tuple(product(range(5), repeat=3))
    normals = projective_points(3)
    planes = [tuple(i for i, p in enumerate(points)
                    if sum(a*x for a, x in zip(v, p)) % 5 == t)
              for v in normals for t in range(5)]
    # Generate affine lines from unordered pairs, not projective directions.
    line_set = set()
    for p, q in combinations(points, 2):
        line_set.add(tuple(sorted(tuple((p[i]+t*(q[i]-p[i])) % 5 for i in range(3))
                                  for t in range(5))))
    point_index = {p: i for i, p in enumerate(points)}
    lines = [tuple(point_index[p] for p in line) for line in sorted(line_set)]
    require(len(lines) == 775 and all(len(line) == 5 for line in lines), 'affine lines')
    require(len(planes) == 155 and all(len(plane) == 25 for plane in planes), 'affine planes')
    plane_sets = [set(plane) for plane in planes]
    containers = [[h for h, plane in enumerate(plane_sets) if set(line) <= plane]
                  for line in lines]
    require(all(len(hs) == 6 for hs in containers), 'six-plane pencils')
    stars = [[h for h, plane in enumerate(plane_sets) if p in plane] for p in range(125)]
    require(all(len(star) == 31 for star in stars), 'point stars')
    # These arbitrary 71-subsets need not be line-free. They check moment and
    # incidence identities, separately from necessary section restrictions.
    rng = random.Random(710319)
    for trial in range(20):
        selected = set(rng.sample(range(125), 71))
        mu = tuple(sum(points[i][j] for i in selected) % 5 for j in range(3))
        moment = [[sum((points[p][i]-mu[i])*(points[p][j]-mu[j]) for p in selected) % 5
                   for j in range(3)] for i in range(3)]
        counts = [len(selected.intersection(plane)) for plane in planes]
        require(sum(counts) == 31*71, 'plane point count control')
        require(sum(m*(m-1)//2 for m in counts) == 6*71*70//2, 'plane pair control')
        require(sum(counts[h] for h in stars[point_index[mu]])
                == 6*71+25*int(point_index[mu] in selected), 'barycenter star control')
        for line, hs in zip(lines, containers):
            require(sum(counts[h] for h in hs) == 71+5*len(selected.intersection(line)),
                    'line pencil control')
        for v in normals:
            values = [sum(a*(x-b) for a, x, b in zip(v, points[i], mu)) % 5
                      for i in selected]
            profile = tuple(values.count(t) for t in range(5))
            require(sum(t*profile[t] for t in range(5)) % 5 == 0, 'centered first moment')
            quadratic = sum(v[i]*moment[i][j]*v[j] for i in range(3) for j in range(3)) % 5
            require(sum(t*t*profile[t] for t in range(5)) % 5 == quadratic,
                    'centered second moment')
    return dict(planes=len(planes), lines=len(lines), identity_controls=20)


def verify_certificates(spectra, path):
    columns, names, matrix, base, objective = incidence_system(spectra)
    data = json.loads(path.read_text())
    require(data['schema'] == 1 and data['row_names'] == list(names), 'certificate schema/rows')
    expected_cases = {(form, bit) for form in FORMS for bit in (0, 1)}
    observed = set()
    bounds = {}
    required = {'zero': (2, 4), 'rank1_square': (3, 3), 'rank1_nonsquare': (2, 2),
                'rank2_split': (2, 2), 'rank2_anisotropic': (3, 3),
                'rank3_square': (2, 2), 'rank3_nonsquare': (2, 2)}
    for case in data['cases']:
        require(type(case['form']) is str and type(case['mu_in_set']) is int,
                'case identifier types')
        key = (case['form'], case['mu_in_set'])
        require(key in expected_cases and key not in observed, 'case cover')
        observed.add(key)
        z, den = case['multipliers'], case['denominator']
        require(type(den) is int and den > 0 and len(z) == len(names), 'multiplier shape')
        require(all(type(v) is int for v in z), 'integral multipliers')
        for j in range(len(columns)):
            require(sum(z[i]*matrix[i][j] for i in range(len(names))) <= den*objective[j],
                    f'failed certificate column {key} {j}')
        rhs = case_rhs(base, *key)
        numerator = sum(v*w for v, w in zip(z, rhs))
        require(type(case['numerator']) is int and numerator == case['numerator'],
                'certificate objective value')
        bound = -(-numerator // den)
        require(bound == case['lower_bound'] == required[key[0]][key[1]], 'claimed bound')
        bounds[f'{key[0]}/{key[1]}'] = str(Fraction(numerator, den))
    require(observed == expected_cases, 'incomplete fourteen-case certificate family')
    require(len(names) == 71, 'equation count')
    return dict(rows=len(names), columns=len(columns), certificates=len(observed),
                exact_lower_bounds=bounds, certificate_sha256=digest(path.read_bytes()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True, type=Path,
                        help='directory for rebuilt census executable and summary')
    parser.add_argument('--cxx', default='g++')
    parser.add_argument('--sanitize', action='store_true')
    parser.add_argument('--certificates', type=Path, default=HERE/'certificates.json')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    executable = args.out.resolve() / 'enumerate_spectra'
    flags = ['-std=c++20', '-Wall', '-Wextra', '-Wpedantic']
    flags += (['-O1', '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer']
              if args.sanitize else ['-O3'])
    subprocess.run([args.cxx, *flags, str(HERE/'enumerate_spectra.cpp'), '-o', str(executable)],
                   check=True)
    census = subprocess.check_output([str(executable)])
    require(census == (HERE/'spectra_expected.txt').read_bytes(), 'complete planar census mismatch')
    lines = [tuple(map(int, line.split())) for line in census.decode().splitlines()]
    require(len(lines) == 91 and all(len(row) == 7 and row[-1] > 0 for row in lines),
            'planar spectrum count')
    spectra = [row[:6] for row in lines]
    for m, *f in spectra:
        require(sum(f) == 30 and sum(k*f[k] for k in range(5)) == 6*m
                and sum(k*(k-1)//2*f[k] for k in range(5)) == m*(m-1)//2,
                'planar spectrum identities')
        require(m > 10 or f[4] == 0, 'small-section line bound')
    summary = dict(status='LOW_PAIR71_VERIFIED', spectra=91,
                   spectrum_sha256=digest(census),
                   profile_audit=audit_profiles(),
                   symmetric_matrix_counts=audit_quadratic_forms(),
                   geometry_audit=audit_geometry(),
                   certificate_audit=verify_certificates(spectra, args.certificates))
    encoded = json.dumps(summary, sort_keys=True, indent=2) + '\n'
    (args.out/'summary.json').write_text(encoded)
    print(encoded, end='')


if __name__ == '__main__':
    main()
