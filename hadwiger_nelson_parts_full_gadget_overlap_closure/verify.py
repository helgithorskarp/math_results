#!/usr/bin/env python3
"""Exact alignment of the full Parts gadgets with the reviewed four-colour field.

The universal conclusion uses the imported theorem, not the sample placements.
No SAT solver, numerical distance filter, or finite all-isometry search is used.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import gcd, lcm
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAD = (1, 3, 5, 15, 11, 33, 55, 165)
POINTS = 'hadwiger_nelson_parts509_completion_census_degree9/points.tsv'
SEEDS = 'hadwiger_nelson_parts509_two_overlap_library_census/residual_seeds.tsv'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(',', ':')).encode()).hexdigest()


def inputs():
    pins = json.loads((HERE / 'inputs.json').read_text())
    for name, pin in pins.items():
        raw = (ROOT / name).read_bytes()
        need(len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256'],
             'input mismatch: ' + name)
    path = ROOT / 'hadwiger_nelson_nonmono_field_obstruction/coloring.py'
    spec = importlib.util.spec_from_file_location('reviewed_field_colouring', path)
    field = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(field)
    rows = [tuple(map(int, line.split())) for line in (ROOT / POINTS).read_text().splitlines()
            if line and not line.startswith('#')]
    need(len(rows) == len(set(rows)) == 509 and all(len(r) == 16 for r in rows),
         'point table shape or collision')
    need(rows[0] == (0,) * 16, 'S+ origin label changed')
    seeds = [tuple(map(int, line.split())) for line in (ROOT / SEEDS).read_text().splitlines()
             if line and not line.startswith('#')]
    need(len(seeds) == len(set(seeds)) == 2772, 'residual seed count')
    return rows, seeds, field


def sqrt15_times(v):
    # sqrt(15)*sqrt(d) = gcd(15,d)*sqrt(15*d/gcd(15,d)^2).
    out = [0] * 8
    for d, a in zip(RAD, v, strict=True):
        h = gcd(15, d)
        out[RAD.index(15 * d // (h * h))] += h * a
    return tuple(out)


def rotate_numerators(row, sign=-1):
    """Multiply by (7 + sign*i*sqrt(15))/8; output denominator is eightfold."""
    x, y = row[:8], row[8:]
    hy, hx = sqrt15_times(y), sqrt15_times(x)
    return tuple(7*a-sign*b for a, b in zip(x, hy)) + tuple(7*a+sign*b for a, b in zip(y, hx))


def in_E(row):
    return not any(a for i, a in enumerate(row) if i not in (0, 5, 9, 12))


def project(row, denominator):
    need(in_E(row), 'point lies outside E')
    return tuple(Q(row[i], denominator) for i in (0, 5, 9, 12))


def squared_distance8(p, q):
    # Sparse radical multiplication by gcd, independent of XOR table indexing.
    out = [0] * 8
    for offset in (0, 8):
        diff = [(d, p[offset+i]-q[offset+i]) for i, d in enumerate(RAD)]
        for i, (d, a) in enumerate(diff):
            if not a:
                continue
            for j in range(i, 8):
                e, b = diff[j]
                if not b:
                    continue
                h = gcd(d, e)
                out[RAD.index(d*e//(h*h))] += (1 if i == j else 2)*h*a*b
    return tuple(out)


def complete_graph_E(vertices):
    """All pairs, using the two norm coefficients instead of field multiplication."""
    need(len(vertices) == len(set(vertices)), 'unmerged collision')
    D = lcm(*(a.denominator for p in vertices for a in p))
    rows = [tuple(int(a*D) for a in p) for p in vertices]
    edges = []
    for i, p in enumerate(rows):
        for j in range(i+1, len(rows)):
            a, b, c, d = (x-y for x, y in zip(p, rows[j]))
            if a*a+33*b*b+3*c*c+11*d*d == D*D and a*b+c*d == 0:
                edges.append((i, j))
    return edges


def checked_word(field, vertices, edges):
    word = ''.join(str(field.color(p)) for p in vertices)
    check_word(word, len(vertices), edges)
    return word


def check_word(word, n, edges):
    need(len(word) == n and set(word) <= set('0123'), 'malformed four-colouring')
    need(all(word[i] != word[j] for i, j in edges), 'monochromatic unit edge')


def sample(seed_index, seed, L, B, field):
    orientation, e0, e1 = seed
    p0, q0 = divmod(e0, 136)
    p1, q1 = divmod(e1, 136)
    source = [field.conjugate(p) for p in B] if orientation >= 1420 else B
    subtract = lambda a, b: field.add(a, field.negate(b))
    u = field.multiply(subtract(L[p1], L[p0]), field.inverse(subtract(source[q1], source[q0])))
    need(field.is_unit(u), 'overlap map is not an isometry')
    t = subtract(L[p0], field.multiply(u, source[q0]))
    placed = [field.add(field.multiply(u, z), t) for z in source]
    overlaps = [(p, q) for q, z in enumerate(placed) for p in range(len(L)) if z == L[p]]
    need(sorted(overlaps) == sorted(((p0, q0), (p1, q1))), 'sample not exactly two overlaps')
    merged = list(dict.fromkeys(L + placed))
    need(len(merged) == 508, 'sample point budget')
    edges = complete_graph_E(merged)
    word = checked_word(field, merged, edges)
    return {'seed_index': seed_index, 'seed': list(seed), 'overlaps': [list(p) for p in sorted(overlaps)],
            'points': len(merged), 'all_pairs': len(merged)*(len(merged)-1)//2,
            'unit_edges': len(edges), 'four_colouring': word,
            'edge_sha256': digest(edges)}


def run():
    rows, seeds, field = inputs()
    large, small = rows[:374], [rows[0]] + rows[374:]
    need(all(in_E(r) for r in large), 'large gadget not in E')
    normalized = [rotate_numerators(r) for r in small]
    need(all(in_E(r) for r in normalized), 'normalized small gadget not in E')
    need(all(rotate_numerators(z, 1) == tuple(64*a for a in r)
             for r, z in zip(small, normalized)), 'rotation inverse check')
    need(Q(7, 8)**2 + Q(15, 64) == 1, 'rho norm')
    L = [project(r, 96) for r in large]
    B = [project(r, 768) for r in normalized]
    need(len(set(L)) == 374 and len(set(B)) == 136, 'normalized gadget collisions')
    E_L, E_B = complete_graph_E(L), complete_graph_E(B)
    need((len(E_L), len(E_B)) == (1860, 564), 'internal complete edge sets')
    Lword, Bword = checked_word(field, L, E_L), checked_word(field, B, E_B)
    for orientation, e0, e1 in seeds:
        p0, q0 = divmod(e0, 136)
        p1, q1 = divmod(e1, 136)
        need(0 <= orientation < 2840 and 0 <= p0 < p1 < 374 and 0 <= q0 < 136
             and 0 <= q1 < 136 and q0 != q1, 'bad residual seed')
        need(squared_distance8(large[p0], large[p1]) == squared_distance8(small[q0], small[q1]),
             'residual seed has unequal segment lengths')
    chosen = []
    for reflected in (False, True):
        ids = [i for i, s in enumerate(seeds) if (s[0] >= 1420) == reflected]
        chosen.extend((ids[0], ids[-1]))
    samples = [sample(i, seeds[i], L, B, field) for i in chosen]
    for s in samples:
        need(s['four_colouring'][:374] == Lword, 'large colouring changed')
    return {'status': 'FULL_GADGET_CAPPED_ISOMETRY_CLASS_CLOSED_BY_IMPORTED_FIELD_THEOREM',
            'large_points': 374, 'small_with_origin_points': 136,
            'large_in_E': True, 'rho_inverse_small_in_E': True,
            'original_small_points_outside_E': sum(not in_E(r) for r in small),
            'unit_rho': True, 'inverse_rotation_roundtrips': 136,
            'large_unit_edges': len(E_L), 'small_unit_edges': len(E_B),
            'large_four_colouring': Lword, 'normalized_small_four_colouring': Bword,
            'normalized_small_integer_rows_sha256': digest(normalized),
            'residual_seeds': len(seeds), 'residual_segment_checks': len(seeds),
            'residual_graphs_enumerated': False, 'direct_samples': samples,
            'direct_sample_all_pairs': sum(s['all_pairs'] for s in samples),
            'direct_sample_unit_edges': sum(s['unit_edges'] for s in samples),
            'native_solver_used': False, 'record_candidate': False, 'record_improved': False}


if __name__ == '__main__':
    result = run()
    expected = HERE / 'EXPECTED.json'
    if expected.exists():
        need(result == json.loads(expected.read_text()), 'expected result mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))
