#!/usr/bin/env python3
"""Integer replay of the new global inequality and its frame normal form."""
import argparse
from collections import Counter
import hashlib
import itertools as it
import json
from pathlib import Path
import random
import subprocess


def require(test, message):
    if not test:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True,
                                   separators=(',', ':')).encode()).hexdigest()


def matrix(spectra):
    """Rebuild the cited incidence system; do not import its model code."""
    parallel = [p for p in it.combinations_with_replacement(range(8, 17), 5)
                if sum(p) == 72]
    pencils = [(k, p) for k in range(5)
               for p in it.combinations_with_replacement(range(max(8, 5*k-8), 17), 6)
               if sum(p) == 72+5*k]
    columns = [('s', s) for s in spectra]+[('p', p) for p in parallel]
    columns += [('l', p) for p in pencils]
    rows, names, rhs = [], [], []

    def add(name, fn, value):
        names.append(name)
        rows.append([fn(t, x) for t, x in columns])
        rhs.append(value)

    add('planes', lambda t, x: int(t == 's'), 155)
    add('plane_points', lambda t, x: x[0] if t == 's' else 0, 2232)
    add('plane_pairs', lambda t, x: x[0]*(x[0]-1)//2 if t == 's' else 0, 15336)
    add('parallel_classes', lambda t, x: int(t == 'p'), 31)
    for m in range(8, 17):
        add(f'parallel_size_{m}', lambda t, x:
            int(x[0] == m) if t == 's' else -x.count(m) if t == 'p' else 0, 0)
    for k in range(5):
        for m in range(8, 17):
            add(f'pencil_{k}_size_{m}', lambda t, x:
                (x[k+1] if x[0] == m else 0) if t == 's'
                else -x[1].count(m) if t == 'l' and x[0] == k else 0, 0)
    add('lines', lambda t, x: int(t == 'l'), 775)
    add('line_points', lambda t, x: x[0] if t == 'l' else 0, 2232)
    add('line_pairs', lambda t, x: x[0]*(x[0]-1)//2 if t == 'l' else 0, 2556)
    objective = [3*int(t == 's' and x[0] == 8)+int(t == 's' and x[0] == 9)
                 for t, x in columns]
    return columns, names, rows, rhs, objective


def determinant(a, b, c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            -a[1]*(b[0]*c[2]-b[2]*c[0])
            +a[2]*(b[0]*c[1]-b[1]*c[0])) % 5


def dot(a, b):
    return sum(x*y for x, y in zip(a, b)) % 5


def normalized(v):
    scale = pow(next(x for x in v if x), -1, 5)
    return tuple(scale*x % 5 for x in v)


def geometry(parent):
    points = tuple(it.product(range(5), repeat=3))
    normals = tuple(p for p in points if any(p) and next(x for x in p if x) == 1)
    planes = {(n, b): frozenset(p for p in points if dot(n, p) == b)
              for n in normals for b in range(5)}
    lines = {frozenset(tuple((x+t*y) % 5 for x, y in zip(p, n))
                       for t in range(5)) for p in points for n in normals}
    require(len(normals) == 31 and len(planes) == 155 and len(lines) == 775,
            'geometry cardinalities')
    require({len(v) for v in planes.values()} == {25}, 'plane orders')
    require(set(Counter(p for h in planes.values() for p in h).values()) == {31},
            'point-plane incidence')
    require(set(Counter(pair for h in planes.values()
                        for pair in it.combinations(sorted(h), 2)).values()) == {6},
            'pair-plane incidence')
    for line in lines:
        pencil = [h for h in planes.values() if line <= h]
        require(len(pencil) == 6, 'pencil size')
        count = Counter(p for h in pencil for p in h)
        require(all(count[p] == 1+5*int(p in line) for p in points), 'pencil identity')
    projective_lines = [frozenset(n for n in normals if dot(n, a) == 0)
                        for a in normals]
    require({len(line) for line in projective_lines} == {6}, 'projective line order')
    # Audit the elementary no-frame containment proof on every triangle
    # and every fourth point. A fourth point outside its three sides gives
    # a frame; a point P on AB rules out every Q outside AB union {C}.
    triangle_cases = fifth_point_cases = 0
    for a, b, c in it.combinations(normals, 3):
        if determinant(a, b, c) == 0:
            continue
        triangle_cases += 1
        for p in normals:
            if p in (a, b, c) or determinant(a, b, p) != 0:
                continue
            for q in normals:
                if q == c or determinant(a, b, q) == 0:
                    continue
                candidates = ((a, b, c, q), (b, c, p, q), (a, c, p, q))
                require(any(all(determinant(*triple) != 0
                                for triple in it.combinations(four, 3))
                            for four in candidates), 'frame containment lemma')
                fifth_point_cases += 1
    extra = [(n, b) for n, b in planes if all(n)]
    require(len(extra) == 80, 'fourth-plane family')
    rng = random.Random(5272)
    normalizations = 256
    for _ in range(normalizations):
        while True:
            ns = rng.sample(normals, 3)
            if determinant(*ns):
                break
        offsets = [rng.randrange(5) for _ in range(3)]
        steps = [rng.randrange(1, 5) for _ in range(3)]
        coefficients = [rng.randrange(1, 5) for _ in range(3)]
        fourth = tuple(sum(coefficients[i]*ns[i][j] for i in range(3)) % 5
                       for j in range(3))
        fourth_offset = rng.randrange(5)
        image = {p: tuple((dot(ns[i], p)-offsets[i])*pow(steps[i], -1, 5) % 5
                          for i in range(3)) for p in points}
        require(set(image.values()) == set(points), 'affine map not bijective')
        for i in range(3):
            for label in (0, 1):
                original = {p for p in points
                            if dot(ns[i], p) == (offsets[i]+label*steps[i]) % 5}
                require({image[p] for p in original} == {p for p in points if p[i] == label},
                        'low/companion-plane normalization')
        new_normal = tuple(coefficients[i]*steps[i] % 5 for i in range(3))
        new_offset = (fourth_offset-sum(x*y for x, y in zip(coefficients, offsets))) % 5
        require(all(new_normal), 'fourth normal lost a coordinate')
        require({image[p] for p in points if dot(fourth, p) == fourth_offset}
                == {p for p in points if dot(new_normal, p) == new_offset},
                'fourth-plane normalization')
    control = json.loads((parent/'known70.json').read_text())
    selected = {points[i] for i in control['points']}
    require(len(selected) == 70 and all(not line <= selected for line in lines),
            'known70 positive control')
    return {'affine_points': 125, 'affine_lines': 775, 'affine_planes': 155,
            'projective_triangles': triangle_cases, 'frame_extension_checks': fifth_point_cases,
            'affine_normalization_checks': normalizations,
            'possible_fourth_planes': len(extra), 'known70_verified': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    parent = here.parent
    args.out.mkdir(parents=True, exist_ok=True)
    executable = (args.out/'planar_spectra').resolve()
    subprocess.run(['g++', '-O3', '-std=c++20', '-Wall', '-Wextra', '-Wconversion',
                    str(parent/'low_planes72/enumerate_spectra.cpp'), '-o', str(executable)],
                   check=True)
    raw = subprocess.check_output([str(executable)])
    require(raw == (parent/'low_planes72/spectra_expected.txt').read_bytes(),
            'parent planar census changed')
    spectra = [tuple(map(int, line.split())) for line in raw.decode().splitlines()]
    require(len(spectra) == 70, 'planar spectra count')
    columns, names, rows, rhs, objective = matrix(spectra)
    require(len(rows) == 61 and len(columns) == 463, 'incidence dimensions')
    cert = json.loads((here/'certificate.json').read_text())
    d, z = cert['denominator'], cert['multipliers']
    require(type(d) is int and d > 0 and len(z) == 61 and all(type(v) is int for v in z),
            'certificate types')
    require(cert['row_names'] == names and cert['objective'] == '3*a_8+a_9',
            'certificate indexing')
    slacks = [d*objective[j]-sum(z[i]*rows[i][j] for i in range(61))
              for j in range(463)]
    value = sum(x*y for x, y in zip(z, rhs))
    require(min(slacks) == cert['minimum_slack'] >= 0, 'dual inequality')
    require(value == cert['bound_numerator'] > 10*d, 'objective bound')
    require((value+d-1)//d == 11, 'integer consequence')
    damaged = z[:]
    damaged[0] += 10*d
    require(any(sum(damaged[i]*rows[i][j] for i in range(61)) > d*objective[j]
                for j in range(463)), 'corrupted-certificate control')
    result = {'status': 'NINE_PLANE_FRAME72_VERIFIED', 'planar_subsets_enumerated': 2**25,
              'planar_spectra': 70, 'incidence_equations': 61, 'checked_columns': 463,
              'bound_numerator': value, 'bound_denominator': d,
              'weighted_integer_lower_bound': 11, 'nine_planes_if_one_eight': 8,
              'nine_planes_if_no_eight': 11, 'global_case': 'BBB with a four-normal frame',
              'matrix_sha256': digest([columns, names, rows, rhs, objective]),
              'certificate_sha256': hashlib.sha256((here/'certificate.json').read_bytes()).hexdigest(),
              'geometry': geometry(parent), 'corrupted_certificate_rejected': True,
              'numeric_bounds': [70, 72], 'exact_value': 'OPEN'}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
