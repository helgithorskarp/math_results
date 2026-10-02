"""Exact symbolic coordinates and original-alias checks; no external input.

Polynomials use ascending Fraction coefficients. The radical basis is
(1,a,b,ab), with a^2=1-c^2 and b^2=3. Every vector has denominator D=1+3c^2.
The written geometric bridges are in PROOF.md, not proved by this script.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations
from math import comb
import hashlib
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


def poly(values):
    values = list(map(Q, values))
    while values and not values[-1]:
        values.pop()
    return tuple(values)


def add(p, q):
    return poly((p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0)
                for i in range(max(len(p), len(q))))


def scale(p, s):
    return poly(x * s for x in p)


def mul(p, q):
    if not p or not q:
        return ()
    out = [Q(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return poly(out)


def power(p, n):
    out = (Q(1),)
    for _ in range(n):
        out = mul(out, p)
    return out


ONE, C, A2 = poly([1]), poly([0, 1]), poly([1, 0, -1])
X = mul(C, C)
D = add(ONE, scale(X, 3))
D2, D3 = power(D, 2), power(D, 3)
ZERO = ((), (), (), ())


def scalar(p):
    return (p, (), (), ())


def fadd(p, q):
    return tuple(add(x, y) for x, y in zip(p, q))


def fscale(p, s):
    return tuple(scale(x, s) for x in p)


def fmul(p, q):
    out = [()] * 4
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            term = mul(x, y)
            if i & j & 1:
                term = mul(term, A2)
            if i & j & 2:
                term = scale(term, 3)
            out[i ^ j] = add(out[i ^ j], term)
    return tuple(out)


def vfscale(v, p):
    return tuple(fmul(x, scalar(p)) for x in v)


def vadd(v, w):
    return tuple(fadd(x, y) for x, y in zip(v, w))


def dot(v, w):
    out = ZERO
    for x, y in zip(v, w):
        out = fadd(out, fmul(x, y))
    return out


def det(u, v, w):
    out = ZERO
    for permutation in permutations(range(3)):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(3) for j in range(i + 1, 3))
        term = fmul(fmul(u[permutation[0]], v[permutation[1]]), w[permutation[2]])
        out = fadd(out, fscale(term, (-1) ** inversions))
    return out


def rational(p):
    need(not any(p[1:]), 'unremoved radical in dot product')
    return p[0]


def values(p):
    return [str(x) for x in p]


def evaluate(p, t):
    value = Q(0)
    for coefficient in reversed(p):
        value = value * t + coefficient
    return value


def bernstein(p):
    """Substitute c=1/2+s/10, then change power to Bernstein basis."""
    n = len(p) - 1
    transformed = [Q(0)] * (n + 1)
    for j, coefficient in enumerate(p):
        for i in range(j + 1):
            transformed[i] += coefficient * comb(j, i) * Q(1, 2) ** (j - i) * Q(1, 10) ** i
    return [sum(transformed[j] * Q(comb(i, j), comb(n, j)) for j in range(i + 1))
            for i in range(n + 1)]


LABELS = ['U', 'F0', 'F1', 'F2', 'W01', 'W12', 'W20', 'J0', 'J1', 'J2']
W_PAIRS = {'W01': (0, 1), 'W12': (1, 2), 'W20': (2, 0)}
BASE_EDGES = {frozenset(('U', 'F' + str(i))) for i in range(3)}
for w, pair in W_PAIRS.items():
    BASE_EDGES.update(frozenset((w, 'F' + str(i))) for i in pair)


def vectors():
    a = ((), ONE, (), ())
    ab = ((), (), (), ONE)
    fs = [(a, ZERO, scalar(C)),
          (fscale(a, Q(-1, 2)), fscale(ab, Q(1, 2)), scalar(C)),
          (fscale(a, Q(-1, 2)), fscale(ab, Q(-1, 2)), scalar(C))]
    u = (ZERO, ZERO, scalar(ONE))
    out = {'U': vfscale(u, D)}
    out.update({'F' + str(i): vfscale(f, D) for i, f in enumerate(fs)})
    for label, (i, j) in W_PAIRS.items():
        out[label] = vadd(vfscale(vadd(fs[i], fs[j]), scale(C, 4)), vfscale(u, scale(D, -1)))
    for i, f in enumerate(fs):
        out['J' + str(i)] = vfscale((fmul(f[0], scalar(scale(C, 2))),
                                   fmul(f[1], scalar(scale(C, 2))),
                                   scalar(add(scale(X, 2), scale(ONE, -1)))), D)
    return out


def kind(a, b):
    a, b = sorted((a, b), key=lambda z: 'UFWJ'.index(z[0]))
    if a == 'U':
        return 'UF_contact' if b[0] == 'F' else 'UW' if b[0] == 'W' else 'UJ'
    if a[0] == b[0]:
        return {'F': 'FF', 'W': 'WW', 'J': 'JJ'}[a[0]]
    if a[0] == 'F' and b[0] == 'W':
        return 'FW_contact' if int(a[1]) in W_PAIRS[b] else 'FW_nonadjacent'
    if a[0] == 'F' and b[0] == 'J':
        return 'FJ_contact' if a[1] == b[1] else 'FJ_nonmatching'
    return 'WJ_adjacent' if int(b[1]) in W_PAIRS[a] else 'WJ_opposite'


def alias_ok(k, assignment, cap=True):
    edges = set(BASE_EDGES)
    core = LABELS[:7]
    for i, neighbor in enumerate(assignment):
        f = 'F' + str(i)
        known = {y for e in edges if f in e for y in e if y != f}
        if neighbor == f or neighbor in known or neighbor.startswith('F'):
            return False
        edges.add(frozenset((f, neighbor)))
    if not cap:
        return True
    names = set(core) | set(assignment)
    neighbors = {x: {y for e in edges if x in e for y in e if y != x} for x in names}
    return all(len(neighbors[a] & neighbors[b]) <= 2 for a, b in combinations(names, 2))


def aliases(k, cap=True):
    labels = LABELS[:7] + ['X' + str(i) for i in range(k)]
    out = []

    def walk(prefix):
        if len(prefix) == k:
            if alias_ok(k, prefix, cap):
                out.append(prefix)
            return
        for label in labels:
            if alias_ok(len(prefix) + 1, prefix + (label,), cap):
                walk(prefix + (label,))

    walk(())
    return sorted(out)


def build():
    vs = vectors()
    norm = {label: values(rational(dot(vs[label], vs[label]))) for label in LABELS}
    need(all(tuple(map(Q, x)) == D2 for x in norm.values()), 'unit identities')
    pairs = []
    numerators = {}
    for a, b in combinations(LABELS, 2):
        p = rational(dot(vs[a], vs[b])); tag = kind(a, b)
        need(tag not in numerators or numerators[tag] == p, 'rotation-class dot mismatch')
        numerators[tag] = p
        pairs.append({'points': [a, b], 'kind': tag, 'numerator': values(p)})
    contacts = {'UF_contact', 'FW_contact', 'FJ_contact'}
    need(all(numerators[t] == mul(C, D2) for t in contacts), 'exact contacts')
    gaps = {}
    for tag, p in sorted(numerators.items()):
        if tag in contacts:
            continue
        gap = add(mul(C, D2), scale(p, -1)); bs = bernstein(gap)
        need(all(x > 0 for x in bs), 'strict packing Bernstein gap ' + tag)
        gaps[tag] = {'numerator': values(gap), 'bernstein': list(map(str, bs))}
    turns = []
    for w, (i, j) in W_PAIRS.items():
        face = ['U', 'F' + str(i), w, 'F' + str(j)]
        for t, label in enumerate(face):
            value = det(vs[face[(t - 1) % 4]], vs[label], vs[face[(t + 1) % 4]])
            need(not value[0] and not value[1] and not value[3], 'turn not rational times sqrt3')
            bs = bernstein(value[2]); need(all(x > 0 for x in bs), 'strict hemispherical turn')
            turns.append({'face': face, 'at': label, 'sqrt3_numerator': values(value[2])})
    p = poly([1, 4, 2, -4, -11, -24])
    d = poly([1, 2, -1])
    need(add(power(d, 2), scale(mul(power(C, 4), poly([1, 2])), -12)) == p, 'threshold identity')
    lower, upper, sample = Q(119, 200), Q(3, 5), Q(599, 1000)
    need(evaluate(p, lower) > 0 > evaluate(p, upper), 'root bracket')
    need(evaluate(p, sample) < 0, 'upper-strip sample')
    need(Q(32, 5) - 3 - Q(11, 2) - Q(15, 2) == Q(-48, 5), 'derivative bound arithmetic')
    need(evaluate(p, Q(1, 2)) == Q(25, 16) and evaluate(p, upper) == Q(-112, 3125), 'threshold endpoint signs')
    family = []
    for mask in range(8):
        chosen = [i for i in range(3) if mask >> i & 1]
        names = LABELS[:7] + ['J' + str(i) for i in chosen]
        edges = [x['points'] for x in pairs if x['points'][0] in names and x['points'][1] in names and x['kind'] in contacts]
        degrees = {x: sum(x in e for e in edges) for x in names}
        need(degrees['U'] == 3 and all(degrees['F' + str(i)] == 3 + (i in chosen) for i in range(3)), 'family contacts')
        family.append({'J_mask': mask, 'point_count': len(names), 'vertices': names,
                       'edges': edges, 'degrees': degrees,
                       'H_triangle': ['F0', 'F1', 'F2'], 'selected_Q_count': 3})
    alias_records = []
    for k in range(4):
        accepted = aliases(k); relaxed = aliases(k, False)
        need(len(accepted) == [1, 1, 2, 6][k], 'all original aliases')
        minimum = min(7 + len(set(x) - set(LABELS[:7])) for x in accepted)
        need(minimum == 7 + k, 'sharp point budget')
        alias_records.append({'four_contact_corners': k, 'raw_candidate_count': (7 + k) ** k,
                              'accepted': [list(x) for x in accepted], 'minimum_distinct_points': minimum,
                              'relaxed_common_contact_cap_minimum': min(7 + len(set(x) - set(LABELS[:7])) for x in relaxed)})
    links = []
    for degree in (3, 4, 5):
        for i, j in combinations(range(degree), 2):
            gaps_pair = sorted([j - i - 1, degree - j + i - 1])
            classification = 'consecutive_possible' if gaps_pair[0] == 0 and degree <= 4 else 'excluded_five_budget' if gaps_pair[0] == 0 else 'excluded_separated_budget'
            links.append({'degree': degree, 'Q_positions': [i, j], 'other_gap_counts': gaps_pair, 'status': classification})
    center = {}
    for degree in (3, 4, 5):
        names = ['F0', 'F1', 'F2'] + ['X' + str(i) for i in range(degree - 3)]
        kept = []
        for suffix in permutations(names[1:]):
            cycle = [names[0], *suffix]
            edges = {frozenset((cycle[i], cycle[(i + 1) % degree])) for i in range(degree)}
            if {frozenset(e) for e in [('F0', 'F1'), ('F1', 'F2'), ('F2', 'F0')]} <= edges:
                kept.append(cycle)
        center[str(degree)] = kept
    need(len(center['3']) == 2 and not center['4'] and not center['5'], 'sealed center link')
    controls = {'correct_unit_and_contacts': True, 'norm_changed_reflector_rejected': True,
                'three_common_contacts_reject_center_alias': True, 'repeated_fourth_contact_rejected': True,
                'diagonal_as_fourth_contact_rejected': True, 'common_cap_relaxation_admits_seven_points': True,
                'upper_strip_c599_over1000': str(evaluate(p, sample)),
                'lower_bracket_c119over200_not_H_triangle': str(evaluate(p, lower))}
    bad = vadd(vs['W01'], vs['U'])
    need(rational(dot(bad, bad)) != D2, 'bad reflector control')
    need(not alias_ok(3, ('X0', 'X0', 'X0')), 'repeated fourth contact control')
    need(not alias_ok(1, ('F1',)), 'contact diagonal control')
    need(all(x['relaxed_common_contact_cap_minimum'] == 7 for x in alias_records), 'relaxed original budget')
    result = {'actual_author': 'six-tammes-1', 'claim_status': 'author geometric proof; exact auxiliary checks; independent review pending',
              'polynomial_order': 'ascending', 'radical_basis': ['1', 'a', 'b', 'a*b'],
              'radical_relations': {'a_squared': values(A2), 'b_squared': '3'},
              'coordinate_common_denominator': values(D), 'dot_common_denominator': values(D2),
              'norm_numerators': norm, 'all_45_pair_products': pairs,
              'strict_packing_gap_certificates': gaps, 'closed_certificate_interval': ['1/2', '3/5'],
              'local_geometric_lemma_range': 'CLOSED 1/2<=c<=3/5; endpoint geometry is a written proof obligation',
              'all_12_Q_turns': turns, 'turn_common_denominator': values(D3),
              'threshold_polynomial': values(p), 'threshold_derivative_upper_bound': '-48/5',
              'threshold_endpoint_signs': ['25/16', '-112/3125'],
              'root_bracket': [str(lower), str(upper)], 'root_bracket_signs': [str(evaluate(p, lower)), str(evaluate(p, upper))],
              'family_sample_c': str(sample), 'all_eight_family_subsets': family,
              'all_four_alias_domains': alias_records, 'all_19_corner_link_choices': links,
              'sealed_center_cycles': center, 'controls': controls,
              'geometric_face_and_correspondence_bridges_proved_only_in_written_PROOF': True,
              'N15_nine_Q_global_occurrence_claimed': False}
    digest = hashlib.sha256(json.dumps(result, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    result['canonical_certificate_sha256_without_this_field'] = digest
    return result


if __name__ == '__main__':
    print(json.dumps(build(), sort_keys=True, indent=2))
