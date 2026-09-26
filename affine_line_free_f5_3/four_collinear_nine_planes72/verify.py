#!/usr/bin/env python3
"""Replay an exact global reduction at 72; no optimizer or SAT solver."""
import argparse
from collections import Counter
import hashlib
import itertools as it
import json
from pathlib import Path
import subprocess

from model import choose2, system


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dot(a, b):
    return sum(x*y for x, y in zip(a, b)) % 5


def direct_geometry(parent):
    points = list(it.product(range(5), repeat=3))
    normals = [p for p in points if any(p) and next(x for x in p if x) == 1]
    planes = [frozenset(i for i, p in enumerate(points) if dot(n, p) == b)
              for n in normals for b in range(5)]
    index = {p: i for i, p in enumerate(points)}
    lines = {frozenset(index[tuple((x+t*y) % 5 for x, y in zip(p, n))]
                       for t in range(5)) for p in points for n in normals}
    require(len(planes) == 155 and len(lines) == 775, 'affine cardinalities')
    require({len(h) for h in planes} == {25}, 'affine plane size')
    blocks = [list(range(5*i, 5*i+5)) for i in range(31)]
    for line in lines:
        pencil = [i for i, h in enumerate(planes) if line <= h]
        require(len(pencil) == 6, 'affine pencil size')
        blocks.append(pencil)
    occurrences = Counter(pair for block in blocks for pair in it.combinations(block, 2))
    all_pairs = set(it.combinations(range(155), 2))
    require(set(occurrences) == all_pairs and set(occurrences.values()) == {1},
            'every pair of planes must occur in exactly one block')
    require(set(Counter(i for block in blocks for i in block).values()) == {31},
            'each plane has 30 line pencils and one parallel class')
    known = set(json.loads((parent/'known70.json').read_text())['points'])
    require(len(known) == 70 and all(not line <= known for line in lines),
            'known70 positive control')
    sizes = [len(h & known) for h in planes]
    left = Counter(tuple(sorted((sizes[i], sizes[j]))) for i, j in all_pairs)
    right = Counter(tuple(sorted((sizes[i], sizes[j]))) for block in blocks
                    for i, j in it.combinations(block, 2))
    require(left == right, 'plane-pair identity on known70')
    projective_lines = [frozenset(i for i, n in enumerate(normals) if dot(n, a) == 0)
                        for a in normals]
    require(len(normals) == 31 and {len(h) for h in projective_lines} == {6},
            'dual projective plane orders')
    pcounts = Counter(pair for line in projective_lines
                      for pair in it.combinations(sorted(line), 2))
    require(len(pcounts) == choose2(31) and set(pcounts.values()) == {1},
            'unique projective joining line')
    # Arithmetic behind the written twelve-point argument:
    # each selected point has one 2-secant; outside a 12-set,
    # r_2 is 0,3,6. Each such value obeys C(r_2,2) >= r_2.
    outside = [(r0, r2, r3) for r0, r2, r3 in it.product(range(7), repeat=3)
               if r0+r2+r3 == 6 and 2*r2+3*r3 == 12]
    require(outside == [(0, 6, 0), (1, 3, 2), (2, 0, 4)], 'outside-point types')
    require(all(choose2(r2) >= r2 for _, r2, _ in outside), 'secant inequality')
    require(choose2(6) < 6*4, 'twelve-point contradiction')
    return {'affine_planes': 155, 'affine_lines': 775, 'plane_pairs': len(all_pairs),
            'parallel_and_pencil_blocks': len(blocks), 'projective_points': 31,
            'projective_lines': 31, 'known70_verified': True}


def normalize_affine_line(points):
    for a in range(5):
        offsets = {(y-a*x) % 5 for x, y in points}
        if len(offsets) == 1:
            return a, offsets.pop()
    return None


def arrangements(here):
    representatives = [(0, 0, 0, 1), (0, 0, 1, 1)]
    matrices = [(a, b, c, d) for a, b, c, d in it.product(range(5), repeat=4)
                if (a*d-b*c) % 5]
    require(len(matrices) == 480, 'GL(2,5) order')
    directions = [frozenset((x, slope*x % 5) for x in range(5)) for slope in range(5)]
    vertical = frozenset((0, y) for y in range(5))
    six = directions + [vertical]
    image_sets = set()
    for a, b, c, d in matrices:
        transformed = []
        for line in six[:4]:
            image = frozenset(((a*x+b*y) % 5, (c*x+d*y) % 5) for x, y in line)
            transformed.append(six.index(image))
        image_sets.add(frozenset(transformed))
    require(len(image_sets) == 15, 'transitivity on four normal directions')
    covers = []
    for offsets in representatives:
        base = [frozenset((x, (slope*x+offsets[slope]) % 5) for x in range(5))
                for slope in range(4)]
        orbit = set()
        for a, b, c, d in matrices:
            transformed = [frozenset(((a*x+b*y) % 5, (c*x+d*y) % 5)
                                     for x, y in line) for line in base]
            labels = [normalize_affine_line(line) for line in transformed]
            if any(label is None for label in labels):
                continue
            if {label[0] for label in labels} != set(range(4)):
                continue
            for tx, ty in it.product(range(5), repeat=2):
                result = [0]*4
                for slope, offset in labels:
                    result[slope] = (offset+ty-slope*tx) % 5
                orbit.add(tuple(result))
        covers.append(orbit)
    all_offsets = set(it.product(range(5), repeat=4))
    concurrent = {tuple((y-a*x) % 5 for a in range(4))
                  for x, y in it.product(range(5), repeat=2)}
    require(len(concurrent) == 25, 'fourfold-concurrent arrangements')
    require(len(covers[0]) == 400 and len(covers[1]) == 200, 'orbit cardinalities')
    require(not (covers[0] & covers[1]), 'overlapping arrangement orbits')
    require(covers[0] | covers[1] | concurrent == all_offsets,
            'incomplete affine arrangement cover')
    for orbit, triple in zip(covers, [True, False]):
        for offsets in orbit:
            multiplicities = [sum((y-a*x) % 5 == offsets[a] for a in range(4))
                              for x, y in it.product(range(5), repeat=2)]
            require(max(multiplicities) == (3 if triple else 2),
                    'wrong concurrency label')
    maps = json.loads((here/'normalization_maps.json').read_text())
    expected_sources = {(0, 0, 0, 1)} | {(0, 0, 1, t) for t in range(5)}
    require({tuple(row['normalized_offsets']) for row in maps} == expected_sources
            and len(maps) == 6, 'six-map normalization domain')
    for row in maps:
        offsets, target = row['normalized_offsets'], row['target_offsets']
        a, b, c, d, tx, ty = row['affine_map']
        require((a*d-b*c) % 5 != 0, 'singular normalization map')
        source = [frozenset((x, (s*x+offsets[s]) % 5) for x in range(5))
                  for s in range(4)]
        transformed = {frozenset(((a*x+b*y+tx) % 5, (c*x+d*y+ty) % 5)
                                 for x, y in line) for line in source}
        destination = {frozenset((x, (s*x+target[s]) % 5) for x in range(5))
                       for s in range(4)}
        require(tuple(target) in representatives and transformed == destination,
                'explicit affine normalization table')
    return {'four_direction_subsets': 15, 'all_offset_tuples': 625,
            'fourfold_concurrent': 25, 'triple_orbit': 400, 'quadrilateral_orbit': 200,
            'explicit_normalization_maps': len(maps)}


def quotient_controls(controls):
    points = list(it.product(range(5), repeat=2))
    lines = [[i for i, (x, y) in enumerate(points) if x == b] for b in range(5)]
    lines += [[i for i, (x, y) in enumerate(points) if (y-a*x) % 5 == b]
              for a in range(5) for b in range(5)]
    output = []
    for control in controls:
        w, offsets = control['weights'], control['offsets']
        require(len(w) == 25 and all(type(x) is int and 0 <= x <= 4 for x in w),
                'quotient weight domain')
        require(sum(w) == 72, 'quotient total')
        sums = [sum(w[i] for i in line) for line in lines]
        selected = {5+5*a+offsets[a] for a in range(4)}
        require(all(sums[i] == 9 if i in selected else 10 <= sums[i] <= 16
                    for i in range(30)), 'quotient line weights')
        require(all(sorted(sums[5+5*a:10+5*a]) == [9, 15, 16, 16, 16]
                    for a in range(4)), 'four B profiles')
        output.append({'offsets': offsets, 'total': sum(w), 'line_sums': sums})
    require({tuple(c['offsets']) for c in controls} == {(0, 0, 0, 1), (0, 0, 1, 1)},
            'quotient controls do not cover both cases')
    return output


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
            'parent planar spectra changed')
    spectra = [tuple(map(int, line.split())) for line in raw.decode().splitlines()]
    (columns, names, rows, rhs, sizes, pairs, pair_rows,
     labels, augmented, target) = system(spectra)
    require(len(spectra) == 70 and len(columns) == 463 and len(rows) == 61,
            'original incidence dimensions')
    require(len(augmented) == 72 and len(pair_rows) == 45, 'new equation counts')
    cert_raw = (here/'certificate.json').read_bytes()
    cert = json.loads(cert_raw)
    z = cert['multipliers']
    require(len(z) == 72 and all(type(x) is int for x in z), 'certificate integers')
    require(cert['row_names'] == labels, 'certificate row order')
    slacks = [sum(z[i]*augmented[i][j] for i in range(72)) for j in range(463)]
    value = sum(x*y for x, y in zip(z, target))
    require(min(slacks) == cert['minimum_slack'] == 0, 'Farkas column inequality')
    require(value == cert['rhs_dot'] == -181596, 'Farkas contradiction')
    damaged = z[:]
    damaged[0] -= 100000000
    require(any(sum(damaged[i]*augmented[i][j] for i in range(72)) < 0
                for j in range(463)), 'damaged certificate accepted')
    control = json.loads((here/'incidence_control.json').read_text())
    vector = [0]*len(columns)
    seen = set()
    for index, count in control['nonzero']:
        require(type(index) is int and type(count) is int and 0 <= index < len(columns)
                and count > 0 and index not in seen, 'control encoding')
        seen.add(index)
        vector[index] = count
    require([sum(x*y for x, y in zip(row, vector)) for row in rows] == rhs,
            'original integer incidence control')
    a = [sum(x*y for x, y in zip(row, vector)) for row in sizes]
    require(a == control['a'] == [0, 16, 0, 0, 14, 8, 12, 32, 73],
            'control plane counts')
    for (m, n), row in zip(pairs, pair_rows):
        value = sum(x*y for x, y in zip(row, vector))
        expected = choose2(a[m-8]) if m == n else a[m-8]*a[n-8]
        require(value == expected, f'full pair control {m},{n}')
    # A sparse positive entry altered by one must fail the original system.
    damaged_vector = vector[:]
    damaged_vector[control['nonzero'][0][0]] += 1
    require(any(sum(x*y for x, y in zip(row, damaged_vector)) != t
                for row, t in zip(rows, rhs)), 'damaged incidence control accepted')
    result = {
        'status': 'FOUR_COLLINEAR_NINE_PLANES72_VERIFIED',
        'planar_subsets_enumerated': 2**25, 'planar_spectra': len(spectra),
        'farkas_equations': len(augmented), 'farkas_columns': len(columns),
        'farkas_rhs_dot': cert['rhs_dot'], 'minimum_nine_planes': 12,
        'new_plane_pair_equations': 45, 'incidence_control_sizes': a,
        'certificate_sha256': sha(cert_raw),
        'augmented_matrix_sha256': sha(json.dumps([columns, labels, augmented, target],
                                                separators=(',', ':')).encode()),
        'geometry': direct_geometry(parent), 'arrangement_cover': arrangements(here),
        'quotient_controls': quotient_controls(json.loads((here/'quotient_controls.json').read_text())),
        'damaged_controls_rejected': True, 'bounds': [70, 72], 'exact_value': 'OPEN',
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
