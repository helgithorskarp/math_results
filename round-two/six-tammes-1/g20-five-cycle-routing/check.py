"""Exact small supporting certificate; the continuum proof is PROOF.md."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from hashlib import sha256
import argparse
import json

HERE = Path(__file__).resolve().parent
A = [(0, 5, 11), (0, 6, 11), (0, 5, 7), (5, 9, 11)]
B = [(1, 2, 4), (2, 4, 8), (1, 2, 10), (1, 10, 12)]
P = [5, 7, 12, 10, 9]
R = [7, 0, 6, 11, 9, 10, 2, 8, 4, 1, 12]
DIAGONALS = [(5, 10), (5, 12), (7, 9), (7, 10), (9, 12)]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def edge(a, b):
    return tuple(sorted((a, b)))


def cycle_edges(cycle):
    return [edge(cycle[i], cycle[(i + 1) % len(cycle)])
            for i in range(len(cycle))]


def boundary(faces):
    counts = {}
    for face in faces:
        for e in cycle_edges(face):
            counts[e] = counts.get(e, 0) + 1
    graph = {}
    for (u, v), count in counts.items():
        require(count in (1, 2), 'manifold patch incidence')
        if count == 1:
            graph.setdefault(u, []).append(v)
            graph.setdefault(v, []).append(u)
    require(all(len(n) == 2 for n in graph.values()), 'simple disk boundary')
    start = min(graph)
    walk = [start, min(graph[start])]
    while walk[-1] != start:
        nxt = next(x for x in graph[walk[-1]] if x != walk[-2])
        walk.append(nxt)
        require(len(walk) <= len(graph) + 1, 'boundary termination')
    require(len(walk) == len(graph) + 1, 'single boundary component')
    return walk[:-1]


def patch(faces):
    edges = sorted(set(sum([cycle_edges(t) for t in faces], [])))
    support = sorted(set(sum([list(t) for t in faces], [])))
    adj = []
    for i, j in combinations(range(len(faces)), 2):
        if len(set(faces[i]) & set(faces[j])) == 2:
            adj.append([i, j])
    growing = set(faces[0])
    fresh = []
    for t in faces[1:]:
        new = sorted(set(t) - growing)
        require(len(new) == 1 and len(set(t) & growing) == 2,
                'fresh disk attachment')
        fresh.append(new[0])
        growing.update(t)
    require(len(adj) == len(faces) - 1, 'patch tree edges')
    return {'faces': [list(t) for t in faces], 'support': support,
            'edges': [list(e) for e in edges], 'tree_edges': adj,
            'fresh_attachment_corners': fresh, 'boundary': boundary(faces)}


def paths(cycle, start, end):
    answers = []
    for direction in (1, -1):
        i = cycle.index(start)
        path = [start]
        while path[-1] != end:
            i = (i + direction) % len(cycle)
            path.append(cycle[i])
        answers.append(path)
    return sorted(answers, key=lambda p: (len(p), p))


def crosses(first, second):
    if set(first) & set(second):
        return False
    i, j = sorted(P.index(x) for x in first)
    k, l = sorted(P.index(x) for x in second)
    return (i < k < j) != (i < l < j)


def partitions(total, minimum=1):
    if total == 0:
        yield ()
    for part in range(minimum, total + 1):
        for rest in partitions(total - part, part):
            yield (part,) + rest


def generate():
    lo, hi = F(1, 2), F(3, 5)
    pa, pb = patch(A), patch(B)
    edges = sorted(set(map(tuple, pa['edges'] + pb['edges']))
                   | {(7, 12), (9, 10)})
    ap, bp = paths(pa['boundary'], 7, 9), paths(pb['boundary'], 10, 12)
    pairings = []
    for match in (((0, 0), (1, 1)), ((0, 1), (1, 0))):
        cycles = [ap[i] + [10] + bp[j][1:] for i, j in match]
        outside_edges = sum([cycle_edges(c) for c in cycles], [])
        expected_edges = cycle_edges(pa['boundary']) + cycle_edges(pb['boundary'])
        expected_edges += [(7, 12)] * 2 + [(9, 10)] * 2
        require(sorted(outside_edges) == sorted(expected_edges), 'whole boundary pairing')
        pairings.append({'lengths': sorted(map(len, cycles)), 'cycles': cycles})
    require(set(cycle_edges(pairings[0]['cycles'][0])) == set(cycle_edges(P)), 'P pairing')
    require(pairings[0]['cycles'][1] == R, 'R pairing')
    reasons = {
        (): 'possible-empty', ((5, 12),): 'possible-V',
        ((5, 10),): 'U-quad-angle-star-at10',
        ((7, 10),): 'W-quad-partner-below-alpha',
        ((9, 12),): 'Z-quad-partner-below-alpha',
        ((5, 10), (5, 12)): 'six-neighbors-at5',
        ((5, 10), (7, 10)): 'five-triangles-at5',
        ((5, 12), (9, 12)): 'five-triangles-at5',
    }
    subsets = []
    for size in range(6):
        for selected in combinations(DIAGONALS, size):
            bad_pairs = [[list(e), list(f)] for e, f in combinations(selected, 2)
                         if crosses(e, f)]
            if (7, 9) in selected:
                reason = 'strict-internal-noncontact-7-9'
            elif bad_pairs:
                reason = 'alternating-endpoints'
            else:
                require(selected in reasons, 'complete noncrossing classification')
                reason = reasons[selected]
            subsets.append({'diagonals': [list(e) for e in selected],
                            'crossing_pairs': bad_pairs, 'reason': reason,
                            'retained': reason.startswith('possible-')})
    scalar = {
        'lo': str(lo), 'hi': str(hi),
        'lo_minus_half': str(lo - F(1, 2)),
        'lo_squared_minus_one_fifth': str(lo * lo - F(1, 5)),
        'three_eighths_minus_upper_angle_cosine': str(F(3, 8) - hi / (1 + hi)),
        'sqrt2_upper_squared_gap': str(F(23, 16) ** 2 - 2),
        'sqrt5_upper_squared_gap': str(F(7, 3) ** 2 - 5),
        'sqrt5_lower_squared_gap': str(5 - F(11, 5) ** 2),
        'nine_c_squared_minus_two_c_minus_one_at_lo': str(9 * lo * lo - 2 * lo - 1),
        'derivative_lower': str(18 * lo - 2),
        'one_minus_hi': str(1 - hi),
    }
    nonstrict = {'lo_minus_half', 'three_eighths_minus_upper_angle_cosine'}
    require(all(F(v) >= 0 if k in nonstrict else F(v) > 0
                for k, v in scalar.items()), 'exact scalar signs')
    all_profiles = [p for p in partitions(11) if len(p) <= 8]
    profiles = [p for p in all_profiles if sum(v >= 4 for v in p) >= 2]
    assignments = []
    for p in profiles:
        distinct = set()
        for i in range(len(p)):
            for j in range(len(p)):
                if i != j and p[i] >= 4 and p[j] >= 4:
                    distinct.add((p[i], p[j], tuple(p[k] for k in range(len(p))
                                                   if k not in (i, j))))
        for a, b, rest in sorted(distinct):
            assignments.append({'profile': list(p), 'e': 8 - len(p),
                                'A': a, 'B': b, 'other': list(rest),
                                'P_branch_retained': True,
                                'V_branch_retained': a >= 5,
                                'V_degree10_five_retained': a == 5 and b == 6 and not rest})
    allocations = []
    for branch, used, counts in [('P', 0, [3, 3, 2]), ('V', 1, [2, 2, 3])]:
        inner_edges = 30 - 20 - used
        require(sum(counts) == 11 + inner_edges - 14 + 1, 'disk Euler count')
        require(sum(n * s for n, s in zip(counts, [3, 4, 5])) == 11 + 2 * inner_edges,
                'whole inner incidence count')
        allocations.append({'branch': branch, 'TQP': counts, 'boundary_vertices': 11,
                            'interior_vertices': 3, 'interior_edges': inner_edges,
                            'inner_faces': sum(counts)})
    ext = set(edges) | {(5, 12)}
    degrees = []
    for v, minimum, maximum in [(5, 5, 5), (9, 3, 4), (10, 4, 5), (12, 4, 4)]:
        neighbors = sorted(b if a == v else a for a, b in ext if v in (a, b))
        require(len(neighbors) == minimum, 'required V neighbor count')
        degrees.append({'vertex': v, 'required_neighbors': neighbors,
                        'minimum_degree': minimum, 'maximum_degree': maximum})
    fresh_cases = []
    for v in sorted(set(pa['support'] + pb['support']) - {1, 2, 9, 10, 12}):
        joined = ext | {edge(v, n) for n in (2, 9, 10)}
        neighbors = sorted(b if a == v else a for a, b in joined if v in (a, b))
        why = {0: 'degree-seven', 11: 'degree-six', 4: 'strict-4-10-at1-two-alpha',
               6: 'strict-6-9-at11-three-alpha', 8: 'strict-8-10-at2-three-alpha',
               5: 'excluded-U', 7: 'excluded-W'}[v]
        fresh_cases.append({'candidate': v, 'required_neighbors': neighbors, 'reason': why})
    forced_faces = A + [(5, 7, 12)] + B + [(2, 10, 3), (9, 10, 3)]
    dual = [[i, j] for i, j in combinations(range(11), 2)
            if len(set(forced_faces[i]) & set(forced_faces[j])) == 2]
    unseen, components = set(range(11)), []
    while unseen:
        stack, component = [min(unseen)], set()
        while stack:
            v = stack.pop()
            if v in component:
                continue
            component.add(v)
            stack.extend(b if a == v else a for a, b in dual if v in (a, b))
        unseen -= component
        components.append(sorted(component))
    forced_edges = sorted(ext | set(sum([cycle_edges(t) for t in forced_faces], [])))
    require([len(q) for q in components] == [5, 6] and len(forced_edges) == 24,
            'whole forced fresh G24 / triangle dual')
    return {'schema': 'g20-five-cycle-routing-v1', 'parameter_checks': scalar,
            'local_band': ['1/2', '3/5'], 'separated_profile_band': ['7/13', '3/5'],
            'patch_A': pa, 'patch_B': pb, 'G20_edges': [list(e) for e in edges],
            'G20_VEF': [12, 20, 10], 'P': P, 'R': R, 'boundary_pairings': pairings,
            'all_diagonal_subsets': subsets, 'V_degree_restrictions': degrees,
            'V_degree10_five_forced_faces': [[2, 10, 'x'], [9, 10, 'x']],
            'V_degree10_five_noncore_check': fresh_cases,
            'V_degree10_five_required_G24': {'fresh_symbol': 3, 'edges': [list(e) for e in forced_edges],
                                           'faces': [list(t) for t in forced_faces],
                                           'full_TT_edges': dual, 'components': components},
            'disk_allocations': allocations, 'all_partitions_checked': len(all_profiles),
            'separated_profiles': [list(p) for p in profiles],
            'oriented_component_assignments': assignments}


def verify_data(data):
    expected = generate()
    require(json.dumps(data, sort_keys=True) == json.dumps(expected, sort_keys=True),
            'entire supporting certificate differs')
    return summary(expected)


def summary(data):
    masks = data['all_diagonal_subsets']
    assignments = data['oriented_component_assignments']
    return {'schema': data['schema'], 'exact_arithmetic': True,
            'patch_faces': 8, 'G20_vertices': 12, 'G20_edges': 20,
            'boundary_pairings': 2, 'diagonal_subsets': len(masks),
            'retained_subsets': [x['diagonals'] for x in masks if x['retained']],
            'strict_scalar_comparisons': len(data['parameter_checks']) - 4,
            'nonstrict_scalar_comparisons': 2, 'noncore_neighbor_cases': 7,
            'forced_G24_edges': 24, 'forced_TT_component_sizes': [5, 6],
            'partitions': data['all_partitions_checked'],
            'separated_profiles': len(data['separated_profiles']),
            'oriented_assignments': len(assignments),
            'V_assignments': sum(x['V_branch_retained'] for x in assignments),
            'V_degree10_five_assignments': sum(x['V_degree10_five_retained'] for x in assignments),
            'disk_allocations': data['disk_allocations']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'CERTIFICATE.json')
    args = parser.parse_args()
    if args.emit:
        print(json.dumps(generate(), indent=2, sort_keys=True))
    else:
        data = json.loads(args.certificate.read_text())
        result = verify_data(data)
        result['certificate_sha256'] = sha256(args.certificate.read_bytes()).hexdigest()
        print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
