"""Separate exact incidence/scalar checker; imports no author checker."""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
CLUSTERS = [[(0, 5, 11), (0, 6, 11), (0, 5, 7), (5, 9, 11)],
            [(1, 2, 4), (2, 4, 8), (1, 2, 10), (1, 10, 12)]]
PENTAGON = (5, 7, 12, 10, 9)


def demand(test, label):
    if not test:
        raise ValueError(label)


def undirected(a, b):
    return (min(a, b), max(a, b))


def arrows(vertices):
    return list(zip(vertices, vertices[1:] + vertices[:1]))


def analyze_patch(triangles):
    oriented = [triangles[0]]
    graph_edges = set()
    for t in triangles[1:]:
        boundary_arrows = set(sum([arrows(q) for q in oriented], []))
        direct = set(arrows(t)) & boundary_arrows
        reverse = set(arrows(tuple(reversed(t)))) & boundary_arrows
        demand(bool(direct) != bool(reverse), 'shared side has one orientation')
        oriented.append(tuple(reversed(t)) if direct else t)
    for t in triangles:
        graph_edges.update(undirected(u, v) for u, v in arrows(t))
    all_arrows = Counter(sum([arrows(t) for t in oriented], []))
    remaining = {e for e in all_arrows if tuple(reversed(e)) not in all_arrows}
    demand(len(remaining) == 6, 'six oriented exterior sides')
    nxt = dict(remaining)
    start = min(nxt)
    walk = [start]
    for _ in range(len(remaining) - 1):
        walk.append(nxt[walk[-1]])
    demand(nxt[walk[-1]] == start and len(set(walk)) == 6, 'closed single boundary')
    walk = min(walk, [walk[0]] + list(reversed(walk[1:])))
    shared = []
    for i, t in enumerate(triangles):
        for j in range(i + 1, len(triangles)):
            if len(set(t) & set(triangles[j])) == 2:
                shared.append([i, j])
    earlier, fresh = set(triangles[0]), []
    for t in triangles[1:]:
        new = set(t) - earlier
        demand(len(new) == 1, 'fresh attachment')
        fresh.append(next(iter(new)))
        earlier |= set(t)
    return {'faces': [list(t) for t in triangles], 'support': sorted(earlier),
            'edges': [list(e) for e in sorted(graph_edges)], 'tree_edges': shared,
            'fresh_attachment_corners': fresh, 'boundary': walk}


def routes(cycle, first, last):
    graph = {}
    for u, v in arrows(tuple(cycle)):
        graph.setdefault(u, []).append(v)
        graph.setdefault(v, []).append(u)
    walks = []
    for successor in graph[first]:
        walk = [first, successor]
        while walk[-1] != last:
            walk.append(next(v for v in graph[walk[-1]] if v != walk[-2]))
        walks.append(walk)
    return sorted(walks, key=lambda w: (len(w), w))


def alternating(e, f):
    if set(e) & set(f):
        return False
    word = [0 if vertex in e else 1 for vertex in PENTAGON if vertex in e or vertex in f]
    return all(word[i] != word[(i + 1) % 4] for i in range(4))


def subdivide(chords):
    polygons = [list(PENTAGON)]
    for u, v in chords:
        indices = [i for i, q in enumerate(polygons) if u in q and v in q
                   and undirected(u, v) not in {undirected(a, b) for a, b in arrows(tuple(q))}]
        demand(len(indices) == 1, 'unique chord disk')
        q = polygons.pop(indices[0])
        i, j = sorted((q.index(u), q.index(v)))
        polygons.extend([q[i:j + 1], q[j:] + q[:i + 1]])
    return polygons


def reconstruct():
    a, b = [analyze_patch(q) for q in CLUSTERS]
    base_edges = sorted(set(tuple(e) for e in a['edges'] + b['edges']) | {(7, 12), (9, 10)})
    ar, br = routes(a['boundary'], 7, 9), routes(b['boundary'], 10, 12)
    pairing = []
    for swap in (False, True):
        polygons = [ar[i] + br[1 - i if swap else i] for i in (0, 1)]
        pairing.append({'lengths': sorted(len(q) for q in polygons), 'cycles': polygons})
    diagonals = sorted({undirected(PENTAGON[i], PENTAGON[j])
                        for i in range(5) for j in range(i + 1, 5)
                        if (j - i) not in (1, 4)})
    rows = []
    masks = sorted([tuple(diagonals[i] for i in range(5) if mask & (1 << i))
                    for mask in range(32)], key=lambda q: (len(q), q))
    for selected in masks:
        pairs = [[list(e), list(f)] for e, f in combinations(selected, 2) if alternating(e, f)]
        if (7, 9) in selected:
            why = 'strict-internal-noncontact-7-9'
        elif pairs:
            why = 'alternating-endpoints'
        else:
            pieces = subdivide(selected)
            neighbors_at5 = {v if u == 5 else u for u, v in set(base_edges) | set(selected)
                             if 5 in (u, v)}
            triangles_at5 = sum(len(q) == 3 and 5 in q for q in pieces)
            if len(neighbors_at5) >= 6:
                why = 'six-neighbors-at5'
            elif triangles_at5 + 3 == 5:
                why = 'five-triangles-at5'
            elif not selected:
                why = 'possible-empty'
            elif selected == ((5, 12),):
                why = 'possible-V'
            elif selected == ((5, 10),):
                why = 'U-quad-angle-star-at10'
            elif selected == ((7, 10),):
                why = 'W-quad-partner-below-alpha'
            elif selected == ((9, 12),):
                why = 'Z-quad-partner-below-alpha'
            else:
                raise ValueError('uncovered diagonal subset')
        rows.append({'diagonals': [list(e) for e in selected], 'crossing_pairs': pairs,
                     'reason': why, 'retained': why.startswith('possible-')})
    low, high = Fraction(1, 2), Fraction(3, 5)
    scalars = {
        'lo': low, 'hi': high, 'lo_minus_half': low - Fraction(1, 2),
        'lo_squared_minus_one_fifth': low ** 2 - Fraction(1, 5),
        'three_eighths_minus_upper_angle_cosine': Fraction(3, 8) - high / (high + 1),
        'sqrt2_upper_squared_gap': Fraction(529 - 512, 256),
        'sqrt5_upper_squared_gap': Fraction(49 - 45, 9),
        'sqrt5_lower_squared_gap': Fraction(125 - 121, 25),
        'nine_c_squared_minus_two_c_minus_one_at_lo': (3 * low) ** 2 - (2 * low + 1),
        'derivative_lower': 2 * (9 * low - 1), 'one_minus_hi': 1 - high,
    }
    demand(scalars['lo_minus_half'] >= 0 and scalars['three_eighths_minus_upper_angle_cosine'] >= 0,
           'closed endpoint inequalities')
    demand(all(v > 0 for k, v in scalars.items()
               if k not in ('lo_minus_half', 'three_eighths_minus_upper_angle_cosine')),
           'exact positive scalar comparisons')
    all_profiles = sorted(q for length in range(1, 9)
                          for q in combinations_with_replacement(range(1, 12), length)
                          if sum(q) == 11)
    profiles = [q for q in all_profiles if sum(v >= 4 for v in q) >= 2]
    assignments = []
    for q in profiles:
        available = Counter(q)
        for av in sorted(available):
            for bv in sorted(available):
                if min(av, bv) < 4 or (av == bv and available[av] < 2):
                    continue
                rest_counts = available.copy()
                rest_counts[av] -= 1
                rest_counts[bv] -= 1
                rest = sorted(rest_counts.elements())
                assignments.append({'profile': list(q), 'e': 8 - len(q), 'A': av, 'B': bv,
                                    'other': rest, 'P_branch_retained': True,
                                    'V_branch_retained': av >= 5,
                                    'V_degree10_five_retained': av == 5 and bv == 6 and not rest})
    allocations = []
    for branch, used in [('P', [8, 0, 1]), ('V', [9, 1, 0])]:
        counts = [n - k for n, k in zip([11, 3, 3], used)]
        incidence = sum(n * sides for n, sides in zip(counts, [3, 4, 5]))
        demand((incidence - 11) % 2 == 0, 'whole interior edge incidences')
        inner_edges = (incidence - 11) // 2
        demand(14 - 11 - inner_edges + sum(counts) == 1, 'disk Euler identity')
        allocations.append({'branch': branch, 'TQP': counts, 'boundary_vertices': 11,
                            'interior_vertices': 3, 'interior_edges': inner_edges,
                            'inner_faces': sum(counts)})
    augmented = set(base_edges) | {(5, 12)}
    degrees = []
    for vertex, cap in [(5, 5), (9, 4), (10, 5), (12, 4)]:
        neighbors = sorted(v if u == vertex else u for u, v in augmented if vertex in (u, v))
        degrees.append({'vertex': vertex, 'required_neighbors': neighbors,
                        'minimum_degree': len(neighbors), 'maximum_degree': cap})
    outside_check = []
    for candidate in sorted(set(a['support'] + b['support']) - {1, 2, 9, 10, 12}):
        contacts = augmented | {undirected(candidate, n) for n in (2, 9, 10)}
        neighbors = sorted(v if u == candidate else u for u, v in contacts if candidate in (u, v))
        if candidate in (0, 11):
            demand(len(neighbors) > 5, 'core degree obstruction')
            reason = 'degree-seven' if len(neighbors) == 7 else 'degree-six'
        elif candidate in (5, 7):
            reason = 'excluded-U' if candidate == 5 else 'excluded-W'
        else:
            center, sectors = {4: (1, 'two'), 6: (11, 'three'), 8: (2, 'three')}[candidate]
            other = 9 if candidate == 6 else 10
            reason = f'strict-{candidate}-{other}-at{center}-{sectors}-alpha'
        outside_check.append({'candidate': candidate, 'required_neighbors': neighbors, 'reason': reason})
    eleven = CLUSTERS[0] + [(5, 7, 12)] + CLUSTERS[1] + [(2, 10, 3), (9, 10, 3)]
    dual, adjacency = [], {i: set() for i in range(11)}
    face_sides = [{undirected(u, v) for u, v in arrows(t)} for t in eleven]
    for i in range(11):
        for j in range(i + 1, 11):
            if face_sides[i] & face_sides[j]:
                dual.append([i, j]); adjacency[i].add(j); adjacency[j].add(i)
    parts = []
    for start in range(11):
        if any(start in part for part in parts):
            continue
        part = {start}
        while True:
            larger = part | set().union(*(adjacency[v] for v in part))
            if larger == part:
                break
            part = larger
        parts.append(sorted(part))
    required_edges = set().union(*face_sides) | augmented
    demand(sorted(map(len, parts)) == [5, 6] and len(required_edges) == 24,
           'literal whole fresh G24 incidence')
    return {'schema': 'g20-five-cycle-routing-v1',
            'local_band': ['1/2', '3/5'], 'separated_profile_band': ['7/13', '3/5'],
            'parameter_checks': {k: str(v) for k, v in scalars.items()},
            'patch_A': a, 'patch_B': b, 'G20_edges': [list(e) for e in base_edges],
            'G20_VEF': [12, 20, 10], 'P': list(PENTAGON),
            'R': [7, 0, 6, 11, 9, 10, 2, 8, 4, 1, 12],
            'boundary_pairings': pairing, 'all_diagonal_subsets': rows,
            'V_degree_restrictions': degrees,
            'V_degree10_five_forced_faces': [[2, 10, 'x'], [9, 10, 'x']],
            'V_degree10_five_noncore_check': outside_check,
            'V_degree10_five_required_G24': {'fresh_symbol': 3, 'edges': [list(e) for e in sorted(required_edges)],
                                           'faces': [list(t) for t in eleven],
                                           'full_TT_edges': dual, 'components': parts},
            'disk_allocations': allocations, 'all_partitions_checked': len(all_profiles),
            'separated_profiles': [list(q) for q in profiles],
            'oriented_component_assignments': assignments}


def verify_data(data):
    expected = reconstruct()
    demand(json.dumps(data, sort_keys=True) == json.dumps(expected, sort_keys=True),
           'complete independently reconstructed certificate differs')
    return {'schema': expected['schema'], 'exact_arithmetic': True, 'patch_faces': 8,
            'G20_vertices': 12, 'G20_edges': 20, 'boundary_pairings': 2,
            'diagonal_subsets': 32,
            'retained_subsets': [q['diagonals'] for q in expected['all_diagonal_subsets'] if q['retained']],
            'strict_scalar_comparisons': len(expected['parameter_checks']) - 4,
            'nonstrict_scalar_comparisons': 2, 'noncore_neighbor_cases': 7,
            'forced_G24_edges': 24, 'forced_TT_component_sizes': [5, 6],
            'partitions': len([1 for length in range(1, 9)
                               for q in combinations_with_replacement(range(1, 12), length) if sum(q) == 11]),
            'separated_profiles': len(expected['separated_profiles']),
            'oriented_assignments': len(expected['oriented_component_assignments']),
            'V_assignments': sum(q['V_branch_retained'] for q in expected['oriented_component_assignments']),
            'V_degree10_five_assignments': sum(q['V_degree10_five_retained']
                                            for q in expected['oriented_component_assignments']),
            'disk_allocations': expected['disk_allocations']}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--emit', action='store_true')
    p.add_argument('--certificate', type=Path, default=HERE / 'CERTIFICATE.json')
    args = p.parse_args()
    if args.emit:
        print(json.dumps(reconstruct(), indent=2, sort_keys=True))
    else:
        result = verify_data(json.loads(args.certificate.read_text()))
        result['certificate_sha256'] = sha256(args.certificate.read_bytes()).hexdigest()
        print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
