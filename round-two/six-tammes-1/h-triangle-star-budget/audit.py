"""Separate same-author audit; imports no check.py.

Rebuild symbolic products from latitude/phase Gram data, turns from a
gnomonic factorization, Bernstein coefficients by polarization, aliases
by raw labeled products and bit incidences, and links by Hamiltonian sets.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
import hashlib
import json


def require(test, why):
    if not test:
        raise RuntimeError(why)


def p(sequence):
    return {i: F(x) for i, x in enumerate(sequence) if x}


def plus(*terms):
    result = {}
    for term in terms:
        for i, value in term.items():
            result[i] = result.get(i, F(0)) + value
    return {i: x for i, x in result.items() if x}


def times(x, y):
    result = {}
    for i, a in x.items():
        for j, b in y.items():
            result[i + j] = result.get(i + j, F(0)) + a * b
    return {i: value for i, value in result.items() if value}


def multiple(x, a):
    return {i: a * value for i, value in x.items() if a * value}


def coeffs(x):
    return [str(x.get(i, F(0))) for i in range(max(x, default=-1) + 1)]


def eval_at(x, t):
    return sum(a * t ** i for i, a in x.items())


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def polar_coefficients(x):
    degree = max(x)
    left, right = F(1, 2), F(3, 5)
    return [sum(a / comb(degree, k) *
                sum(choose(i, j) * choose(degree - i, k - j) *
                    right ** j * left ** (k - j) for j in range(k + 1))
                for k, a in x.items()) for i in range(degree + 1)]


NAMES = ['U', 'F0', 'F1', 'F2', 'W01', 'W12', 'W20', 'J0', 'J1', 'J2']
W_ENDPOINTS = {'W01': {0, 1}, 'W12': {1, 2}, 'W20': {2, 0}}
ONE, C = p([1]), p([0, 1])
S = times(C, C)
D = plus(ONE, multiple(S, 3))
D2, D3 = times(D, D), times(times(D, D), D)
RADIAL_SQUARED = plus(ONE, multiple(S, -1))


def gram():
    # Each point has z=z_num/D, planar radius=radial_num*sqrt(1-c^2)/D,
    # and angle phase*pi/3. No Cartesian radical vectors are used.
    data = {'U': (D, {}, 0)}
    for i in range(3):
        data['F' + str(i)] = (times(C, D), D, 2 * i)
        data['J' + str(i)] = (times(plus(multiple(S, 2), multiple(ONE, -1)), D),
                              multiple(times(C, D), 2), 2 * i)
    for label, phase in zip(['W01', 'W12', 'W20'], [1, 3, 5]):
        data[label] = (plus(multiple(S, 5), multiple(ONE, -1)), multiple(C, 4), phase)
    cosines = [F(1), F(1, 2), F(-1, 2), F(-1), F(-1, 2), F(1, 2)]
    matrix = {}
    for i, a in enumerate(NAMES):
        for b in NAMES[i:]:
            za, ra, pa = data[a]; zb, rb, pb = data[b]
            matrix[a, b] = plus(times(za, zb), multiple(times(times(ra, rb), RADIAL_SQUARED),
                                                        cosines[(pa - pb) % 6]))
    return matrix


def category(a, b):
    roles = {a[0], b[0]}
    if roles == {'F'}:
        return 'FF'
    if roles == {'W'}:
        return 'WW'
    if roles == {'J'}:
        return 'JJ'
    if 'U' in roles:
        other = b if a == 'U' else a
        return {'F': 'UF_contact', 'W': 'UW', 'J': 'UJ'}[other[0]]
    if roles == {'F', 'W'}:
        f = a if a[0] == 'F' else b; w = b if a[0] == 'F' else a
        return 'FW_contact' if int(f[1]) in W_ENDPOINTS[w] else 'FW_nonadjacent'
    if roles == {'F', 'J'}:
        f = a if a[0] == 'F' else b; j = b if a[0] == 'F' else a
        return 'FJ_contact' if f[1] == j[1] else 'FJ_nonmatching'
    w = a if a[0] == 'W' else b; j = b if a[0] == 'W' else a
    return 'WJ_adjacent' if int(j[1]) in W_ENDPOINTS[w] else 'WJ_opposite'


def bit_graph(k, assignment, cap=True):
    labels = NAMES[:7] + ['X' + str(i) for i in range(k)]
    index = {name: i for i, name in enumerate(labels)}
    adjacency = [0] * len(labels)

    def edge(a, b):
        i, j = index[a], index[b]
        if i == j:
            return False
        adjacency[i] |= 1 << j; adjacency[j] |= 1 << i
        return True

    for i in range(3):
        edge('U', 'F' + str(i))
    for w, endpoints in W_ENDPOINTS.items():
        for i in endpoints:
            edge(w, 'F' + str(i))
    for i, target in enumerate(assignment):
        if not edge('F' + str(i), target):
            return None
    for i in range(3):
        fi = index['F' + str(i)]
        if adjacency[fi].bit_count() != 3 + (i < k):
            return None
        if any(adjacency[fi] >> index['F' + str(j)] & 1 for j in range(3) if i != j):
            return None
    if cap and any((adjacency[i] & adjacency[j]).bit_count() > 2
                   for i, j in combinations(range(len(labels)), 2)):
        return None
    return adjacency


def raw_aliases(k, cap=True):
    labels = NAMES[:7] + ['X' + str(i) for i in range(k)]
    return sorted(a for a in product(labels, repeat=k) if bit_graph(k, a, cap) is not None)


def center_cycles(degree):
    names = ['F0', 'F1', 'F2'] + ['X' + str(i) for i in range(degree - 3)]
    complete = list(combinations(range(degree), 2))
    required = {frozenset(e) for e in [(0, 1), (1, 2), (2, 0)]}
    cycles = []
    for indices in combinations(range(len(complete)), degree):
        selected = [complete[i] for i in indices]
        if not required <= {frozenset(e) for e in selected}:
            continue
        adjacency = [set() for _ in names]
        for a, b in selected:
            adjacency[a].add(b); adjacency[b].add(a)
        if not all(len(s) == 2 for s in adjacency):
            continue
        for start in sorted(adjacency[0]):
            path = [0, start]
            while len(path) < degree:
                options = adjacency[path[-1]] - {path[-2]}
                nxt = next(iter(options))
                if nxt in path:
                    break
                path.append(nxt)
            if len(path) == degree and 0 in adjacency[path[-1]]:
                cycles.append([names[i] for i in path])
    return sorted(cycles)


def certificate():
    matrix = gram()
    norm = {name: coeffs(matrix[name, name]) for name in NAMES}
    require(all(matrix[name, name] == D2 for name in NAMES), 'phase/latitude norm')
    rows = []; categories = {}
    for a, b in combinations(NAMES, 2):
        number = matrix[a, b]; tag = category(a, b)
        require(tag not in categories or categories[tag] == number, 'Gram dot classes')
        categories[tag] = number
        rows.append({'points': [a, b], 'kind': tag, 'numerator': coeffs(number)})
    contacts = {'UF_contact', 'FW_contact', 'FJ_contact'}
    require(all(categories[tag] == times(C, D2) for tag in contacts), 'Gram contacts')
    gaps = {}
    for tag, number in sorted(categories.items()):
        if tag in contacts:
            continue
        gap = plus(times(C, D2), multiple(number, -1)); bs = polar_coefficients(gap)
        require(min(bs) > 0, 'polarized packing gap')
        gaps[tag] = {'numerator': coeffs(gap), 'bernstein': list(map(str, bs))}
    # The four gnomonic determinants have factors B,hB,B,hB, with
    # B=sqrt(3)*(1-c^2)/2 and h=4c/D. Clear denominator D^3.
    even = multiple(times(RADIAL_SQUARED, D3), F(1, 2))
    odd = multiple(times(times(C, RADIAL_SQUARED), D2), 2)
    require(min(polar_coefficients(even)) > 0 and min(polar_coefficients(odd)) > 0, 'gnomonic turn factors')
    turns = []
    for w, (i, j) in zip(['W01', 'W12', 'W20'], [(0, 1), (1, 2), (2, 0)]):
        face = ['U', 'F' + str(i), w, 'F' + str(j)]
        turns.extend({'face': face, 'at': label, 'sqrt3_numerator': coeffs(even if n % 2 == 0 else odd)}
                     for n, label in enumerate(face))
    threshold = p([1, 4, 2, -4, -11, -24])
    d = p([1, 2, -1]); fourth = times(S, S)
    require(plus(times(d, d), multiple(times(fourth, p([1, 2])), -12)) == threshold, 'threshold expansion')
    lower, upper, sample = F(119, 200), F(3, 5), F(599, 1000)
    require(eval_at(threshold, lower) > 0 > eval_at(threshold, upper), 'bracket')
    require(eval_at(threshold, sample) < 0, 'sample')
    require(F(32, 5) - 3 - F(11, 2) - F(15, 2) == F(-48, 5), 'derivative bound')
    require(eval_at(threshold, F(1, 2)) == F(25, 16) and eval_at(threshold, upper) == F(-112, 3125), 'threshold endpoint signs')
    family = []
    for mask in range(8):
        chosen = [i for i in range(3) if mask >> i & 1]
        names = NAMES[:7] + ['J' + str(i) for i in chosen]
        edges = [row['points'] for row in rows if all(x in names for x in row['points']) and row['kind'] in contacts]
        degrees = {name: sum(name in e for e in edges) for name in names}
        require(degrees['U'] == 3 and all(degrees['F' + str(i)] == 3 + (i in chosen) for i in range(3)), 'family degrees')
        family.append({'J_mask': mask, 'point_count': len(names), 'vertices': names, 'edges': edges,
                       'degrees': degrees, 'H_triangle': ['F0', 'F1', 'F2'], 'selected_Q_count': 3})
    alias_records = []
    for k in range(4):
        accepted, relaxed = raw_aliases(k), raw_aliases(k, False)
        minimum = min(7 + len(set(x) - set(NAMES[:7])) for x in accepted)
        require(len(accepted) == [1, 1, 2, 6][k] and minimum == 7 + k, 'raw original alias cover')
        alias_records.append({'four_contact_corners': k, 'raw_candidate_count': (7 + k) ** k,
                              'accepted': [list(x) for x in accepted], 'minimum_distinct_points': minimum,
                              'relaxed_common_contact_cap_minimum': min(7 + len(set(x) - set(NAMES[:7])) for x in relaxed)})
    links = []
    for degree in (3, 4, 5):
        for mask in range(1 << degree):
            if mask.bit_count() != 2:
                continue
            positions = [i for i in range(degree) if mask >> i & 1]
            counts = []
            for start, stop in [positions, positions[::-1]]:
                cursor, count = (start + 1) % degree, 0
                while cursor != stop:
                    count += 1; cursor = (cursor + 1) % degree
                counts.append(count)
            counts.sort()
            status = 'excluded_separated_budget' if counts[0] else 'excluded_five_budget' if degree == 5 else 'consecutive_possible'
            links.append({'degree': degree, 'Q_positions': positions, 'other_gap_counts': counts, 'status': status})
    links.sort(key=lambda z: (z['degree'], z['Q_positions']))
    center = {str(n): center_cycles(n) for n in (3, 4, 5)}
    require(len(center['3']) == 2 and not center['4'] and not center['5'], 'Hamiltonian center seal')
    changed_reflector_norm = plus(multiple(D2, 2), multiple(categories['UW'], 2))
    require(changed_reflector_norm != D2, 'changed reflection rejected')
    require(bit_graph(3, ('X0', 'X0', 'X0')) is None, 'shared extra alias')
    require(bit_graph(1, ('F1',)) is None, 'H diagonal control')
    require(all(row['relaxed_common_contact_cap_minimum'] == 7 for row in alias_records), 'cap relaxation admits core seven')
    controls = {'correct_unit_and_contacts': True, 'norm_changed_reflector_rejected': True,
                'three_common_contacts_reject_center_alias': True, 'repeated_fourth_contact_rejected': True,
                'diagonal_as_fourth_contact_rejected': True, 'common_cap_relaxation_admits_seven_points': True,
                'upper_strip_c599_over1000': str(eval_at(threshold, sample)),
                'lower_bracket_c119over200_not_H_triangle': str(eval_at(threshold, lower))}
    result = {'actual_author': 'six-tammes-1', 'claim_status': 'author geometric proof; exact auxiliary checks; independent review pending',
              'polynomial_order': 'ascending', 'radical_basis': ['1', 'a', 'b', 'a*b'],
              'radical_relations': {'a_squared': coeffs(RADIAL_SQUARED), 'b_squared': '3'},
              'coordinate_common_denominator': coeffs(D), 'dot_common_denominator': coeffs(D2),
              'norm_numerators': norm, 'all_45_pair_products': rows,
              'strict_packing_gap_certificates': gaps, 'closed_certificate_interval': ['1/2', '3/5'],
              'local_geometric_lemma_range': 'CLOSED 1/2<=c<=3/5; endpoint geometry is a written proof obligation',
              'all_12_Q_turns': turns, 'turn_common_denominator': coeffs(D3),
              'threshold_polynomial': coeffs(threshold), 'threshold_derivative_upper_bound': '-48/5',
              'threshold_endpoint_signs': ['25/16', '-112/3125'],
              'root_bracket': [str(lower), str(upper)], 'root_bracket_signs': [str(eval_at(threshold, lower)), str(eval_at(threshold, upper))],
              'family_sample_c': str(sample), 'all_eight_family_subsets': family,
              'all_four_alias_domains': alias_records, 'all_19_corner_link_choices': links,
              'sealed_center_cycles': center, 'controls': controls,
              'geometric_face_and_correspondence_bridges_proved_only_in_written_PROOF': True,
              'N15_nine_Q_global_occurrence_claimed': False}
    digest = hashlib.sha256(json.dumps(result, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    result['canonical_certificate_sha256_without_this_field'] = digest
    return result


if __name__ == '__main__':
    print(json.dumps(certificate(), sort_keys=True, indent=2))
