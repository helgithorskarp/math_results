#!/usr/bin/env python3
"""Exact positive-witness decoder, six-heesch-3, researcher.

No foreign executable imports. Drafter triangles and cell residues are
generated from two fundamental triangles by the six Euclidean rotations.
The literal producer tables are read as AST data only and compared whole.
Foreign vertex coordinates (u,v) use metric u^2+uv+v^2. The similarity
G(u,v)=((u+2v)/42,-u/42) places them in owned (x,sqrt(3)y)/4 coordinates.
The computation keeps42*G integral until a source isometry is established.
Headers are parsed for format only: no solver-trusted upper is adopted.
"""
import argparse
import ast
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import re
import resource
import time
import geometry as b


def matrix(M, p):
    a, c, d, e = M
    return a*p[0]+c*p[1], d*p[0]+e*p[1]


def rotation(p):
    return -p[1], p[0]+p[1]


def repeated(p, n):
    for _ in range(n):
        p = rotation(p)
    return p


# One twelve-cell hexagonal star is generated, not transcribed wholesale.
centres = []
triangles = []
for k in range(6):
    for p, triangle in [((2, 1), ((0, 0), (6, 0), (4, 4))),
                        ((1, 2), ((0, 0), (4, 4), (0, 6)))]:
        centres.append(repeated(p, k))
        triangles.append(tuple(repeated(v, k) for v in triangle))
types = {(p[0] % 7, p[1] % 7): i for i, p in enumerate(centres)}
b.require(len(types) == 12, 'drafter residues are not distinct')


def foreign_vertices(p):
    b.require((p[0] % 7, p[1] % 7) in types, 'invalid drafter label')
    i = types[(p[0] % 7, p[1] % 7)]
    c = p[0]-centres[i][0], p[1]-centres[i][1]
    b.require(c[0] % 7 == c[1] % 7 == 0, 'incorrect fundamental centre')
    return tuple((12*c[0]+7*v[0], 12*c[1]+7*v[1]) for v in triangles[i])


def G42(p):
    return p[0]+2*p[1], -p[0]


def inverse_G42(p):
    return -p[1], Fraction(p[0]+p[1], 2)


def raw_owned_linear(M, p):
    return G42(matrix(M, inverse_G42(p)))


def undo(pose, p):
    a, f = pose
    x, y = b.rotate((-a) % 12, p)
    return x, -y if f else y


def compact(cycle):
    result = list(cycle)
    while True:
        shortened = [p for i, p in enumerate(result)
            if b.turn(result[i-1], p, result[(i+1) % len(result)]) != 0]
        if len(shortened) == len(result):
            break
        result = shortened
    b.require(len(result) >= 3, 'empty simplified polygon')
    if b.twice_area(result) < 0:
        result.reverse()
    i = min(range(len(result)), key=lambda i: result[i])
    return tuple(result[i:] + result[:i])


def tables_match(path):
    literals = {}
    for node in ast.parse(Path(path).read_text()).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in (
                        'DRAFTER_TYPE_TABLE', 'DRAFTER_LOS', 'DRAFTER_VERTICES'):
                    literals[target.id] = ast.literal_eval(node.value)
    classifier = [types.get((x, y), -1) for y in range(7) for x in range(7)]
    b.require(classifier == literals['DRAFTER_TYPE_TABLE'], 'full type table differs')
    b.require([(-x, -y) for x, y in centres] == literals['DRAFTER_LOS'], 'centres differ')
    b.require(len(literals['DRAFTER_VERTICES']) == len(triangles) == 12,
              'incomplete fundamental triangle table')
    b.require(all(set(a) == set(c) for a, c in zip(triangles,
                  literals['DRAFTER_VERTICES'])), 'fundamental triangles differ')
    return {'generated_type_entries': 49, 'generated_cell_centres': 12,
            'generated_fundamental_triangles': 12,
            'foreign_code_executed': False, 'foreign_tables_AST_literal_only': True}


def parse(path):
    lines = Path(path).read_text().splitlines()
    b.require(lines and lines[0].startswith('D '), 'only D source supported')
    values = [int(x) for x in lines[0][2:].split()]
    b.require(values and len(values) % 2 == 0, 'bad source coordinate list')
    cells = tuple(zip(values[::2], values[1::2]))
    b.require(len(cells) == len(set(cells)), 'duplicate source cell')
    b.require(re.fullmatch(r'(?:~ \d+ \d+ 1|! 1)', lines[1]), 'unsupported header')
    count = int(lines[2])
    b.require(len(lines) == count+3 and count > 0, 'placement count differs')
    rows = []
    for line in lines[3:]:
        match = re.fullmatch(r'(\d+) <(-?\d+),(-?\d+),(-?\d+),(-?\d+),(-?\d+),(-?\d+)>', line)
        b.require(match is not None, 'bad affine row')
        r = list(map(int, match.groups()))
        rows.append((r[0], tuple(r[1:])))
    b.require(sum(l == 0 for l, _ in rows) == 1 and
              next(T for l, T in rows if l == 0) == (1, 0, 0, 0, 1, 0),
              'foreign root is not identity')
    return cells, rows, lines[1]


def identify(source_atoms, m, cap):
    for a, c in combinations(source_atoms, 2):
        if b.boxes_meet(b.box(a), b.box(c), False):
            b.require(not b.convex_intersection(a, c, False), 'source triangle overlap')
    source_cycle = compact(b.boundary(source_atoms)[0])
    prototype = b.atoms(m)
    if cap:
        prototype += (b.ccw(((-2, 2), (0, 0), (2, 2))),)
    own_cycle = compact(b.boundary(prototype)[0])
    own42 = tuple((42*x, 42*y) for x, y in own_cycle)
    for a in range(0, 12, 2):
        for f in (0, 1):
            image = compact(tuple(b.point((a, f, 0, 0), p) for p in own42))
            shift = b.sub(source_cycle[0], image[0])
            moved = tuple((x+shift[0], y+shift[1]) for x, y in image)
            if moved == source_cycle:
                return (a, f), shift, source_cycle, prototype
    raise ValueError('exact source boundary does not match the proposed prototype')


def decode(path, m, cap, table_path):
    start = time.monotonic()
    audit = tables_match(table_path)
    cells, rows, header = parse(path)
    source_atoms = tuple(b.ccw(tuple(G42(v) for v in foreign_vertices(p))) for p in cells)
    H, delta, cycle, prototype = identify(source_atoms, m, cap)
    normalized = []
    vertex_checks = 0
    affine_records = []
    for level, T in rows:
        a, c, tx, d, e, ty = T
        M = a, c, d, e
        # Exact metric identity in the foreign oblique coordinates.
        u, v = matrix(M, (1, 0)), matrix(M, (0, 1))
        norm = lambda p: p[0]*p[0]+p[0]*p[1]+p[1]*p[1]
        b.require(norm(u) == norm(v) == 1 and norm((u[0]+v[0], u[1]+v[1])) == 3,
                  'foreign linear part is not an isometry')
        def L(p):
            return undo(H, raw_owned_linear(M, b.point((*H, 0, 0), p)))
        matches = [(angle, reflect) for angle in range(0, 12, 2) for reflect in (0, 1)
                   if all(b.point((angle, reflect, 0, 0), p) == L(p)
                          for p in [(2, 0), (0, 2)])]
        b.require(len(matches) == 1, 'normalized physical orientation is not unique')
        angle, reflect = matches[0]
        raw_delta = raw_owned_linear(M, delta)
        translation42 = undo(H, (raw_delta[0]+12*(tx+2*ty)-delta[0],
                                 raw_delta[1]-12*tx-delta[1]))
        translation = tuple(Fraction(x, 42) for x in translation42)
        b.require(all(x.denominator == 1 for x in translation), 'normalized translation not integral')
        pose = angle, reflect, int(translation[0]), int(translation[1])
        for p in cells:
            q = (a*p[0]+c*p[1]+tx, d*p[0]+e*p[1]+ty)
            actual = {G42(v) for v in foreign_vertices(q)}
            transformed = {G42((a*u+c*v+12*tx, d*u+e*v+12*ty))
                           for u, v in foreign_vertices(p)}
            b.require(actual == transformed, 'physical affine cell footprint differs')
            vertex_checks += 1
        normalized.append({'pose': list(pose), 'level': level})
        affine_records.append({'foreign': list(T), 'normalized': list(pose), 'level': level})
    witness = {'tile_hexagons': m, 'left_cap_triangle': cap, 'copies': normalized}
    counts = [sum(row['level'] == l for row in normalized) for l in range(7)]
    b.require(max(row['level'] for row in normalized) == 6 and min(counts) > 0,
              'not a six-corona placement list')
    output = {'agent': 'six-heesch-3', 'role': 'researcher', 'foreign_input': str(path),
        'foreign_input_sha256': sha256(Path(path).read_bytes()).hexdigest(),
        'foreign_record_header_not_an_upper_proof': header,
        'tables': audit, 'source_cells': len(cells), 'proposed_strip_hexagons': m,
        'left_cap_triangle': cap, 'source_similarity_G': ['(u+2v)/42', '-u/42'],
        'prototype_to_G_source_orientation': list(H),
        'prototype_to_G_source_translation_scaled42': list(delta),
        'source_cycle_scaled42': [list(p) for p in cycle],
        'prototype_atoms': [[list(p) for p in atom] for atom in prototype],
        'source_scaled42_twice_area': b.twice_area(cycle),
        'source_simple_and_atom_packing_checked': True, 'source_boundary_exact_match': True,
        'whole_placement_cell_vertex_equalities': vertex_checks,
        'affine_rows': affine_records, 'copies': len(rows), 'level_counts': counts,
        'complete_coronas_not_checked_in_this_decoder': True,
        'global_finite_upper_claimed': False,
        'elapsed_seconds': time.monotonic()-start,
        'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    return witness, output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--hexagons', type=int, required=True)
    parser.add_argument('--cap', action='store_true')
    parser.add_argument('--tables', default=str(Path(__file__).resolve().with_name('drafter_tables.py')))
    parser.add_argument('--witness', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    b.require(not Path(args.out).exists() and not Path(args.witness).exists(), 'refuse overwrite')
    witness, result = decode(args.input, args.hexagons, args.cap, args.tables)
    Path(args.witness).write_text(json.dumps(witness, indent=2)+'\n')
    result['witness'] = args.witness
    result['witness_sha256'] = sha256(Path(args.witness).read_bytes()).hexdigest()
    Path(args.out).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in
                     ('source_cycle_scaled42', 'prototype_atoms', 'affine_rows')}, indent=2))
