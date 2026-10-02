"""Separate same-author set/subset and ordered-triple finite audit.

No primary checker import. Geometry remains the written argument.
Default summary and --entries agree bytewise with the prefix checker.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
import hashlib
import json
import sys


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(entries):
    return hashlib.sha256(json.dumps(entries, separators=(',', ':')).encode()).hexdigest()


def rational_record():
    c0, c1 = Q(1, 2), Q(3, 5)
    low = (4*c0*c0-c0-1)/(c0+1)
    high = 4*c1*c1/(1+c1*c1)-1
    require(low == Q(-1, 3) and high == Q(1, 17), 'rational side endpoints')
    require(high < Q(1, 16), 'full-interval upper side comparator')
    product_low = Q(-1, 3)*Q(1, 16)
    lower_angle = (low-Q(1, 9))/Q(8, 9)
    upper_angle = (Q(1, 16)-product_low)/Q(8, 9)
    require(lower_angle == Q(-1, 2) and upper_angle == Q(3, 32), 'credited angle comparator')
    require(upper_angle < Q(1, 8), 'sine-concavity angle gap')
    require(2-3*Q(3, 8) == Q(7, 8), 'twice consecutive sector bound')
    require(Q(3, 4) > Q(2, 3), 'separated sector bound')
    require(512 < 529 and 45 < 49 and Q(3, 8) > Q(4, 11), 'alpha exact comparisons')
    c = Q(599, 1000)
    p = -24
    for coefficient in (-11, -4, 2, 4, 1):
        p = p*c+coefficient
    require(c0 < c < c1 and p < 0, 'outside beta control')
    return {'side_lower_at_half': str(low), 'side_upper_at_three_fifths': str(high),
            'credited_side_window': ['-1/3', '1/16'],
            'triangle_cosine_window': ['-1/2', '3/32'],
            'sine_concavity_lower_comparator': '1/8',
            'five_consecutive_upper_pi_multiple': '7/16',
            'nonconsecutive_lower_pi_multiple': '3/4',
            'outside_old_beta_control': {'c': str(c), 'P(c)': str(p)},
            'transcendental_trust_boundary': 'written Q identities, angle monotonicity and strict sine concavity'}


def cyclic_pairs():
    out = []
    for bits in product((0, 1), repeat=5):
        if sum(bits) != 2:
            continue
        i, j = [k for k, b in enumerate(bits) if b]
        g0 = sum(bits[k] == 0 for k in range(i+1, j))
        g1 = sum(bits[k % 5] == 0 for k in range(j+1, i+5))
        typ = 'consecutive' if min(g0, g1) == 0 else 'separated'
        require(sorted((g0, g1)) in ([0, 3], [1, 2]), 'all raw cyclic words')
        out.append({'Q_positions': [i, j], 'other_gaps_in_two_sectors': [g0, g1], 'case': typ})
    require(len(out) == 10 and sum(x['case'] == 'consecutive' for x in out) == 5, 'ten link cases')
    return sorted(out, key=lambda x: x['Q_positions'])


def box_rows(r):
    n4 = 15-2*r
    out = set()
    for f in product(range(r+1), repeat=5):
        if sum(f) != r:
            continue
        d = sum(j*f[j] for j in range(5))
        if d > 6:
            continue
        for a in range(n4+1):
            for b in range(n4-a+1):
                if a+2*b+d == 6:
                    require(2*n4+4*r-d-a-2*b == 24, 'direct triangle-corner total')
                    out.add((a, b)+f)
    return tuple(sorted(out))


def specifications(row):
    a, b, _, f1, f2, f3, f4 = row
    require(f3 == f4 == 0, 'admissible deficit roles')
    h = [2]*a+[3]*b+[2]*f1+[3]*f2
    u = [2]*a+[4]*b+[1]*f1+[2]*f2
    require(len(h) <= 6, 'six-original bound')
    return h, u, set(range(a+b, len(h)))


def allowed_h(row, edges, pruned=True):
    bound, _, fives = specifications(row)
    n = len(bound)
    if type(edges) is not set:
        return False
    if any(len(e) != 2 or min(e) < 0 or max(e) >= n for e in edges):
        return False
    if pruned and any(not (set(e) & fives) for e in edges):
        return False
    deg = [sum(v in e for e in edges) for v in range(n)]
    if any(deg[v] > bound[v] or (v in fives and deg[v] != bound[v]) for v in range(n)):
        return False
    for tri in combinations(range(n), 3):
        if set(tri) & fives and set(combinations(tri, 2)) <= edges:
            return False
    return True


def subset_h(row):
    bound, _, fives = specifications(row)
    pairs = tuple(combinations(range(len(bound)), 2))
    eligible = tuple(e for e in pairs if set(e) & fives)
    masks = []
    for bits in range(1 << len(eligible)):
        edges = {e for k, e in enumerate(eligible) if bits >> k & 1}
        if allowed_h(row, edges):
            masks.append(sum(1 << pairs.index(e) for e in edges))
    return tuple(sorted(masks))


def allowed_u(row, r, family):
    _, cap, fives = specifications(row)
    if len(family) != r or len(set(family)) != r:
        return False
    if any(len(t) != 3 or len(set(t)) != 3 or any(v not in range(len(cap)) for v in t) for t in family):
        return False
    if any(len(set(t) & fives) > 1 for t in family):
        return False
    if any(sum(v in t for t in family) > cap[v] for v in range(len(cap))):
        return False
    return not any(sum(i in t and j in t for t in family) > 2 for i, j in combinations(range(len(cap)), 2))


def labeled_u(row, r):
    _, cap, _ = specifications(row)
    triples = tuple(combinations(range(len(cap)), 3))
    families = set()
    for ordered in product(triples, repeat=r):
        if allowed_u(row, r, ordered):
            families.add(tuple(sorted(ordered)))
    return tuple(sorted(families))


def fixed_controls():
    row = (5, 0, 0, 1, 0, 0, 0)
    original = {(0, 1), (0, 2), (1, 2), (3, 5), (4, 5)}
    reduced = {(3, 5), (4, 5)}
    require(allowed_h(row, original, pruned=False), 'four-only triangle retained')
    require(not allowed_h(row, original), 'four-four edges not permitted in H*')
    require(allowed_h(row, reduced), 'pruning positive control')
    require(not allowed_h(row, {(0, 1), (0, 5), (1, 5)}, pruned=False), 'five triangle negative control')
    require(not allowed_h(row, {(3, 5)}), 'exact five degree negative control')
    require(not allowed_h(row, -1) and not allowed_h(row, True), 'scalar masks cannot be decoded as edge sets')
    ordinary = (0, 3, 1, 0, 0, 0, 0)
    require(subset_h(ordinary) == (0,), 'no deficient five gives empty H*')
    require(not allowed_u(ordinary, 2, ((0, 1, 2), (0, 1, 2))), 'repeat triple')
    require(not allowed_u((6, 0, 3, 0, 0, 0, 0), 3, ((0, 1, 2), (0, 1, 3), (0, 1, 4))), 'third common neighbor')
    require(not allowed_u((1, 2, 0, 1, 0, 0, 0), 2, ((0, 1, 3), (0, 2, 3))), 'five capacity')
    require(not allowed_u((4, 0, 0, 2, 0, 0, 0), 2, ((0, 4, 5), (1, 2, 3))), 'two five suppliers')
    require(allowed_u(ordinary, 1, ((0, 1, 2),)), 'neighbor positive control')
    return {'four_only_triangle_preserved_before_pruning': True,
            'required_five_degrees_preserved_after_pruning': True,
            'necessary_controls_passed': 12,
            'controls_are_not_claimed_spherical_realizations': True}


def entries():
    raw = {r: box_rows(r) for r in range(1, 8)}
    domains, rejected = [], {}
    for r, rows in raw.items():
        why = Counter()
        for row in rows:
            if r > 3:
                why['imported_written_degree_bound'] += 1
            elif row[5] != 0 or row[6] != 0:
                why['five_deficit_at_least_three'] += 1
            elif 3*r > 12-row[3]-2*row[4]:
                why['degree_three_contact_capacity'] += 1
            else:
                domains.append({'r': r, 'row': row, 'H_star_masks': subset_h(row), 'U_families': labeled_u(row, r)})
        rejected[r] = dict(sorted(why.items()))
    require(len(domains) == 44, 'all finite domains')
    return {'raw_profiles': raw, 'domains': domains, 'pre_domain_rejections': rejected}


def compact(data):
    domains, profiles = [], []
    for d in data['domains']:
        hs, us = d['H_star_masks'], d['U_families']
        domains.append({'r': d['r'], 'row': list(d['row']), 'H_star_count': len(hs),
                        'H_star_sha256': sha(hs), 'U_family_count': len(us), 'U_families_sha256': sha(us)})
        if hs and us:
            a, b, f0, f1, f2, _, _ = d['row']
            profiles.append({'tuple_r_a_b_f0_f1_f2_O': [d['r'], a, b, f0, f1, f2, 15-2*d['r']-a-b],
                             'first_H_star_mask': hs[0], 'first_U_family': us[0]})
    by_r = dict(sorted(Counter(p['tuple_r_a_b_f0_f1_f2_O'][0] for p in profiles).items()))
    require(by_r == {1: 9, 2: 12, 3: 11}, '32 complete necessary count profiles')
    return {'raw_counts_by_r': {r: len(rows) for r, rows in data['raw_profiles'].items()},
            'pre_domain_rejections': data['pre_domain_rejections'], 'domains': domains,
            'all_domain_entries_sha256': sha(data['domains']), 'profiles_by_r': by_r,
            'total_profiles': len(profiles), 'profiles': profiles}


def main():
    require(sys.argv[1:] in ([], ['--entries']), 'supported flag')
    a, links, controls = rational_record(), cyclic_pairs(), fixed_controls()
    data = entries()
    out = data if sys.argv[1:] else {
        'actual_agent': 'six-tammes-1', 'role': 'researcher', 'interval': ['1/2', '3/5'],
        'arithmetic': a, 'five_link_cases': links, 'controls': controls, 'cover': compact(data),
        'scope': 'Handwritten five-vertex H-triangle exclusion; full-interval necessary count cover with H*. No complete packing enumeration or global bound.'}
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
