"""Independent geometry/normalization audit of the 71-point decision cover.

Production APIs are called only as objects under test; all expected
geometry, profiles, coordinate maps and clauses are constructed here.
This does not check any UNSAT proof.
"""
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import time


def need(condition, message):
    if not condition:
        raise ValueError(message)


P2 = tuple(product(range(5), repeat=2))
P3 = tuple(product(range(5), repeat=3))
I2 = {p: i for i, p in enumerate(P2)}
I3 = {p: i for i, p in enumerate(P3)}


def dot(a, b):
    return sum(x*y for x, y in zip(a, b)) % 5


def line_sets(points):
    index = {p: i for i, p in enumerate(points)}
    return {frozenset(index[tuple((x+t*(y-x)) % 5 for x, y in zip(p, q))]
                      for t in range(5)) for p, q in combinations(points, 2)}


def plane_sets():
    # Generate linear planes as spans, then their translates. No supplied normals.
    zero_lines = {L for L in line_sets(P3) if 0 in L}
    linear = set()
    for L in zero_lines:
        u = P3[min(L-{0})]
        for i, v in enumerate(P3):
            if i in L:
                continue
            linear.add(frozenset(I3[tuple((a*x+b*y) % 5 for x, y in zip(u, v))]
                                 for a, b in product(range(5), repeat=2)))
    need(len(linear) == 31 and all(len(H) == 25 for H in linear), 'linear-plane spans')
    planes = {frozenset(I3[tuple((x+y) % 5 for x, y in zip(P3[i], t))] for i in H)
              for H in linear for t in P3}
    return planes


def inverse(matrix):
    n = len(matrix)
    work = [[x % 5 for x in row]+[int(i == j) for j in range(n)]
            for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if work[r][col]), None)
        if pivot is None:
            raise ValueError('singular matrix')
        work[col], work[pivot] = work[pivot], work[col]
        multiplier = pow(work[col][col], -1, 5)
        work[col] = [x*multiplier % 5 for x in work[col]]
        for r in range(n):
            if r != col:
                factor = work[r][col]
                work[r] = [(x-factor*y) % 5 for x, y in zip(work[r], work[col])]
    return [row[n:] for row in work]


def profile_table():
    result = []; raw = []
    for m in range(7, 11):
        words = set()
        for deficits in combinations_with_replacement(range(1, 5), m-7):
            c = Counter(deficits)
            words.add((m,)+tuple(16-c[t] for t in range(1, 5)))
        canonical = set()
        for w in words:
            images = []
            for a in range(1, 5):
                image = [0]*5
                for t, value in enumerate(w):
                    image[a*t % 5] = value
                images.append(tuple(image))
            canonical.add(min(images))
        result.extend(sorted(canonical)); raw.append(len(words))
    pairs = sorted(list(combinations_with_replacement(range(5), 2))+
                   [(0, j) for j in range(5, 10)])
    return result, pairs, raw


def audit_geometry():
    lines2 = line_sets(P2); lines3 = line_sets(P3); planes = plane_sets()
    need(len(lines2) == 30 and len(lines3) == 775 and len(planes) == 155, 'geometry counts')
    plane_pairs = Counter(len(H & K) for H, K in combinations(planes, 2))
    need(plane_pairs == {0: 310, 5: 11625}, 'plane intersections')
    for L in lines3:
        pencil = [H for H in planes if L <= H]
        need(len(pencil) == 6, 'pencil size')
        need(all(sum(p in H for H in pencil) == 1+5*(p in L) for p in range(125)),
             'pencil coefficient identity')
    for p in range(25):
        star = [L for L in lines2 if p in L]
        need(len(star) == 6 and all(sum(q in L for L in star) == 1+5*(q == p)
                                   for q in range(25)), 'quotient-star identity')
    normals = sorted({min(tuple(a*x % 5 for x in p) for a in range(1, 5))
                      for p in P3 if p != (0, 0, 0)})
    maps = 0
    for u, v in product(normals, repeat=2):
        if u == v:
            continue
        for e in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            try:
                inv = inverse([u, v, e])
                break
            except ValueError:
                continue
        else:
            raise ValueError('no complement to independent plane forms')
        image = [I3[(dot(u, p), dot(v, p), dot(e, p))] for p in P3]
        need(len(set(image)) == 125, 'coordinate map not bijective')
        need(all(tuple(dot(row, P3[image[i]]) for row in inv) == p
                 for i, p in enumerate(P3)), 'coordinate inverse failed')
        need(all(frozenset(image[i] for i in L) in lines3 for L in lines3),
             'coordinate map loses a line')
        for a, b in product(range(5), repeat=2):
            intersection = {i for i, p in enumerate(P3) if dot(u, p) == a and dot(v, p) == b}
            need(len(intersection) == 5 and intersection in lines3, 'plane-frame intersection')
        maps += 1
    need(maps == 930, 'normal pair count')
    # Every translation and every height shear preserve the independently generated lines.
    for shift in P3:
        image = [I3[tuple((a+b) % 5 for a, b in zip(p, shift))] for p in P3]
        need(all(frozenset(image[i] for i in L) in lines3 for L in lines3), 'translation loses a line')
    for c, a, b in P3:
        image = [I3[(x, y, (z-c-a*x-b*y) % 5)] for x, y, z in P3]
        need(len(set(image)) == 125 and all(frozenset(image[i] for i in L) in lines3 for L in lines3),
             'height shear is not an affine line bijection')
    triples = 0; interpolations = 0
    for abc in combinations(range(25), 3):
        try:
            inv = inverse([(1,)+P2[i] for i in abc])
        except ValueError:
            continue
        triples += 1
        for heights in P3:
            coefficients = tuple(dot(row, heights) for row in inv)
            need(all(dot((1,)+P2[i], coefficients) == h for i, h in zip(abc, heights)),
                 'three-hole interpolation failed')
            interpolations += 1
    need((triples, interpolations) == (2000, 250000), 'gauge completeness')
    return lines2, lines3, planes, {'planar_lines': 30, 'spatial_lines': 775, 'planes': 155,
            'parallel_plane_pairs': 310, 'intersecting_plane_pairs': 11625,
            'coefficientwise_pencils': 775, 'quotient_stars': 25,
            'ordered_affine_plane_frames': maps*25, 'linear_frame_maps': maps,
            'translations': 125, 'height_shears': 125,
            'noncollinear_gauge_triples': triples, 'height_interpolations': interpolations}


def audit_catalogue(path, profiles, pairs, lines):
    counts = Counter(); seen = {}; min_full = 25; max_interior = 0
    for s in path.read_text().splitlines():
        kind, word = s.split(); kind = int(kind)
        need(kind in range(20) and len(word) == 25 and set(word) <= set('01234'), 'typed word')
        need(word not in seen, 'duplicate quotient word'); seen[word] = kind
        w = tuple(map(int, word)); need(sum(w) == 71, 'total weight')
        need(all(sum(w[p] for p in L) <= 16 for L in lines), 'quotient line bound')
        i, j = pairs[kind]
        need(tuple(sum(w[5*x+y] for y in range(5)) for x in range(5)) == profiles[i], 'row profile')
        need(tuple(sum(w[5*x+y] for x in range(5)) for y in range(5)) == profiles[j], 'column profile')
        axis = [w[p] for p in range(25) if 0 in P2[p]]
        need(max(axis) <= 3 and 5*w[0] <= profiles[i][0]+profiles[j][0]-7, 'pencil-derived axis bound')
        interior = [p for p in range(25) if 0 not in P2[p]]
        T = sum(4-w[p] for p in interior)
        need(T+w[0] == profiles[i][0]+profiles[j][0]-7, 'interior identity')
        need(T <= 11, 'interior budget')
        full = [p for p in interior if w[p] == 4]
        need(len(full) >= 16-T and len(full) >= 5, 'full interior fibers')
        need(not any(set(full) <= L for L in lines), 'no noncollinear gauge')
        min_full = min(min_full, len(full)); max_interior = max(max_interior, T)
        counts[kind] += 1
    need(len(seen) == 309611, 'incomplete catalogue')
    return {'typed_quotients_checked': len(seen), 'counts_by_type': [counts[i] for i in range(20)],
            'minimum_full_interior_fibers': min_full, 'maximum_interior_deficit': max_interior}, seen


def expected_formula(word, lines3):
    clauses = [[-(i+1) for i in sorted(L)] for L in lines3]
    for p, char in enumerate(word):
        n = int(char); fiber = list(range(5*p+1, 5*p+6))
        for bits in product((0, 1), repeat=5):
            # Only inclusion-minimal forbidden one-sets or zero-sets are needed.
            selected = [fiber[j] for j, b in enumerate(bits) if b]
            if len(selected) == n+1:
                clauses.append([-v for v in selected])
            if len(selected) == 6-n:
                clauses.append(selected)
    full = [i for i, c in enumerate(word) if c == '4']
    for abc in combinations(full, 3):
        try:
            inverse([(1,)+P2[i] for i in abc])
        except ValueError:
            continue
        gauge = abc; break
    else:
        raise ValueError('missing gauge')
    clauses += [[-(5*i+1)] for i in gauge]
    return Counter(tuple(sorted(c)) for c in clauses), gauge


def audit_production_api(source, representatives, lines3, planes):
    spec = importlib.util.spec_from_file_location('reviewed_point_model', source/'point_model.py')
    reviewed = importlib.util.module_from_spec(spec); spec.loader.exec_module(reviewed)
    got_lines, got_planes = reviewed.geometry()
    need({frozenset(v-1 for v in L) for L in got_lines} == lines3, 'production lines differ')
    need({frozenset(v-1 for v in H) for H in got_planes} == planes, 'production planes differ')
    # All exact-five truth tables are evaluated from Boolean semantics.
    for n in range(5):
        clauses = reviewed.fiber_clauses([1, 2, 3, 4, 5], n)
        for bits in product((False, True), repeat=5):
            value = all(any(bits[abs(lit)-1] == (lit > 0) for lit in C) for C in clauses)
            need(value == (sum(bits) == n), 'cardinality truth table')
    chosen = {}
    for r in representatives:
        chosen.setdefault(r['type'], r['weights'])
    need(set(chosen) == set(range(20)), 'missing proof-family type')
    for word in chosen.values():
        actual, gauge = reviewed.generate(word)
        expected, independent_gauge = expected_formula(word, lines3)
        need(Counter(tuple(sorted(C)) for C in actual.clauses) == expected and gauge == independent_gauge,
             'direct point formula differs')
    return reviewed, {'fiber_truth_assignments': 160, 'full_formula_types_compared': len(chosen)}


def audit_controls(source, reviewed, lines3):
    witnesses = ('known70.json', 'odd_symmetry/witness70.json',
                 'affine_asymmetry71/witness70.json')
    inputs = {}
    for name in witnesses:
        path = source.parent/name
        points = json.loads(path.read_text())['points']
        selected = set(points)
        need(len(points) == len(selected) == 70 and selected <= set(range(125)), '70-point control size')
        need(not any(L <= selected for L in lines3), '70-point control contains a line')
        word = ''.join(str(sum(5*p+z in selected for z in range(5))) for p in range(25))
        expected, gauge = expected_formula(word, lines3)
        heights = [next(z for z in range(5) if 5*p+z not in selected) for p in gauge]
        coefficients = tuple(dot(row, heights) for row in inverse([(1,)+P2[p] for p in gauge]))
        normalized = {I3[(x, y, (z-dot((1, x, y), coefficients)) % 5)]
                      for x, y, z in (P3[p] for p in selected)}
        need(not any(L <= normalized for L in lines3), 'positive control shear loses line-freeness')
        actual, actual_gauge = reviewed.generate(word)
        need(actual_gauge == gauge and Counter(tuple(sorted(C)) for C in actual.clauses) == expected,
             'positive control formula differs')

        def satisfies(point_set):
            return all(any(((abs(v)-1) in point_set) == (v > 0) for v in C)
                       for C in actual.clauses)

        need(satisfies(normalized), 'positive control fails its point formula')
        need(not satisfies(normalized-{min(normalized)}), 'deleted-point control accepted')
        missing_line = next(L for L in lines3 if not L <= normalized)
        corrupted = normalized | missing_line
        need(any(L <= corrupted for L in lines3) and not satisfies(corrupted),
             'completed-line control accepted')
        inputs[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    try:
        inverse([(1,)+P2[p] for p in (0, 1, 2)])
    except ValueError:
        pass
    else:
        raise ValueError('collinear gauge accepted')
    return {'positive70_controls': len(witnesses), 'deleted_point_controls_rejected': len(witnesses),
            'completed_line_controls_rejected': len(witnesses), 'collinear_gauge_rejected': True}, inputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--reduction', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--check-expected', action='store_true')
    args = parser.parse_args(); start = time.monotonic()
    lines2, lines3, planes, geometry = audit_geometry()
    profiles, pairs, raw = profile_table()
    supplied = json.loads((args.source/'profiles.json').read_text())
    need(profiles == list(map(tuple, supplied['profiles'])) and pairs == list(map(tuple, supplied['pairs'])),
         'independent profile cover differs')
    need(raw == [1, 4, 10, 20] and len(pairs) == 20, 'profile counts')
    catalogue, words = audit_catalogue(args.reduction/'deficit_quotients.txt', profiles, pairs, lines2)
    representatives = json.loads((args.reduction/'orbits.json').read_text())
    need(len(representatives) == 109676 and sum(r['orbit_size'] for r in representatives) == 309611,
         'representative coverage counts')
    need(len({r['weights'] for r in representatives}) == len(representatives)
         and all(words.get(r['weights']) == r['type'] for r in representatives),
         'representative outside catalogue or repeated')
    reviewed, api = audit_production_api(args.source, representatives, lines3, planes)
    controls, inputs = audit_controls(args.source, reviewed, lines3)
    result = {'status': 'GEOMETRIC_DECISION_BRIDGE_AUDITED', 'geometry': geometry,
              'profiles': {'raw_counts': raw, 'normalized': len(profiles), 'pairs': len(pairs)},
              'catalogue': catalogue, 'point_formula': api, 'controls': controls,
              'proofs_rechecked': False,
              'input_hashes': {'deficit_quotients.txt': hashlib.sha256(
                                   (args.reduction/'deficit_quotients.txt').read_bytes()).hexdigest(),
                               'orbits.json': hashlib.sha256(
                                   (args.reduction/'orbits.json').read_bytes()).hexdigest()},
              'control_hashes': inputs,
              'reviewed_files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in sorted(args.source.iterdir()) if p.is_file()}}
    if args.check_expected:
        expected = json.loads(Path(__file__).with_name('EXPECTED.json').read_text())
        need(result == expected, 'audit differs from pinned expected results or reviewed source')
    result['seconds'] = time.monotonic()-start
    args.out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'reviewed_files'}, indent=2))


if __name__ == '__main__':
    main()
