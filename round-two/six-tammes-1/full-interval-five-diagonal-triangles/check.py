"""Full-interval five-diagonal lemma and necessary q9 count cover.

six-tammes-1, researcher. Ordinary written geometry is in PROOF.md.
The exact cover concerns counts and necessary graphs, not sphere packings.
CPython >=3.11, standard library only, no external runtime input.
--entries exposes all small finite entries for bytewise separate replay.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations
import hashlib
import json
import sys


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(entries):
    return hashlib.sha256(json.dumps(entries, separators=(',', ':')).encode()).hexdigest()


def arithmetic():
    lo, hi = Q(1, 2), Q(3, 5)
    lower = lambda c: 4*c*c/(1+c)-1
    upper = lambda c: (3*c*c-1)/(1+c*c)
    need(lower(lo) == Q(-1, 3), 'lower diagonal endpoint')
    need(upper(hi) == Q(1, 17), 'upper diagonal endpoint')
    need(Q(1, 17) < Q(1, 16), 'strict common side window')
    need(Q(-1, 3)*Q(1, 16) == Q(-1, 48), 'product lower bound')
    need((Q(-1, 3)-Q(1, 9))/Q(8, 9) == Q(-1, 2), 'triangle cosine lower')
    need((Q(1, 16)+Q(1, 48))/Q(8, 9) == Q(3, 32), 'triangle cosine upper')
    need(Q(3, 32) < Q(1, 8), 'strict sine-concavity comparator')
    need(1-Q(3, 2)*Q(3, 8) == Q(7, 16), 'consecutive five sector bound')
    need(2*Q(3, 8) == Q(3, 4) > Q(2, 3), 'nonconsecutive sector bound')
    need(512 < 529, 'alpha lower squared comparison')
    need(45 < 49, 'alpha upper squared comparison')
    need(Q(3, 8) > Q(4, 11), 'one-T-four small-corner bound')
    c = Q(599, 1000)
    p = 1+4*c+2*c*c-4*c**3-11*c**4-24*c**5
    need(lo < c < hi and p < 0, 'interval has parameters outside old beta range')
    return {
        'side_lower_at_half': str(lower(lo)),
        'side_upper_at_three_fifths': str(upper(hi)),
        'credited_side_window': ['-1/3', '1/16'],
        'triangle_cosine_window': ['-1/2', '3/32'],
        'sine_concavity_lower_comparator': '1/8',
        'five_consecutive_upper_pi_multiple': '7/16',
        'nonconsecutive_lower_pi_multiple': '3/4',
        'outside_old_beta_control': {'c': str(c), 'P(c)': str(p)},
        'transcendental_trust_boundary': 'written Q identities, angle monotonicity and strict sine concavity',
    }


def link_cases():
    out = []
    for i, j in combinations(range(5), 2):
        gaps = (j-i-1, 4-(j-i))
        consecutive = 0 in gaps
        need(sorted(gaps) == ([0, 3] if consecutive else [1, 2]), 'complete five-gap cases')
        out.append({'Q_positions': [i, j], 'other_gaps_in_two_sectors': list(gaps),
                    'case': 'consecutive' if consecutive else 'separated'})
    need(Counter(x['case'] for x in out) == {'consecutive': 5, 'separated': 5}, 'all ten five-link pairs')
    return out


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for x in range(total+1):
            for tail in compositions(total-x, length-1):
                yield (x,)+tail


def raw_profiles(r):
    n4 = 15-2*r
    out = []
    for five in compositions(r, 5):
        deficit = sum(j*five[j] for j in range(5))
        if deficit > 6:
            continue
        for b in range((6-deficit)//2+1):
            a = 6-deficit-2*b
            if a+b <= n4:
                need(a+2*(n4-a-b)+sum((4-j)*five[j] for j in range(5)) == 24,
                     'all eight triangle corners counted')
                out.append((a, b)+five)
    return tuple(sorted(out))


def roles(row):
    a, b, f0, f1, f2, f3, f4 = row
    need(not f3 and not f4, 'deficit-three/four five already geometrically excluded')
    hc = (2,)*a+(3,)*b+(2,)*f1+(3,)*f2
    uc = (2,)*a+(4,)*b+(1,)*f1+(2,)*f2
    need(len(hc) <= 6, 'deficit-six gives at most six deficient originals')
    return hc, uc, a+b


def h_valid(row, mask, pruned=True):
    hc, _, first_five = roles(row)
    n = len(hc)
    pairs = tuple(combinations(range(n), 2))
    if type(mask) is not int or not 0 <= mask < 1 << len(pairs):
        return False
    adj, deg = [0]*n, [0]*n
    for k, (i, j) in enumerate(pairs):
        if mask >> k & 1:
            if pruned and j < first_five:
                return False
            adj[i] |= 1 << j
            adj[j] |= 1 << i
            deg[i] += 1
            deg[j] += 1
    if any(deg[i] > hc[i] or (i >= first_five and deg[i] != hc[i]) for i in range(n)):
        return False
    # With pruned=False only triangles containing an actual five are excluded.
    return not any(adj[i] >> j & 1 and adj[i] >> k & 1 and adj[j] >> k & 1
                   for i, j, k in combinations(range(n), 3) if k >= first_five)


def h_masks(row):
    hc, _, first_five = roles(row)
    n = len(hc)
    all_pairs = tuple(combinations(range(n), 2))
    eligible = tuple((k, i, j) for k, (i, j) in enumerate(all_pairs) if j >= first_five)
    adj, deg, out = [0]*n, [0]*n, []

    def visit(p, mask):
        if p == len(eligible):
            if all(i < first_five or deg[i] == hc[i] for i in range(n)):
                need(h_valid(row, mask), 'every complete H* entry checked')
                out.append(mask)
            return
        k, i, j = eligible[p]
        visit(p+1, mask)
        if deg[i] < hc[i] and deg[j] < hc[j] and not adj[i] & adj[j]:
            deg[i] += 1
            deg[j] += 1
            adj[i] |= 1 << j
            adj[j] |= 1 << i
            visit(p+1, mask | 1 << k)
            deg[i] -= 1
            deg[j] -= 1
            adj[i] ^= 1 << j
            adj[j] ^= 1 << i

    visit(0, 0)
    return tuple(sorted(out))


def u_valid(row, r, family):
    _, cap, first_five = roles(row)
    n = len(cap)
    if len(family) != r or len(set(family)) != r:
        return False
    if any(len(t) != 3 or tuple(sorted(set(t))) != t or any(v not in range(n) for v in t) for t in family):
        return False
    if any(sum(v >= first_five for v in t) > 1 for t in family):
        return False
    occurrence = Counter(v for t in family for v in t)
    if any(occurrence[v] > cap[v] for v in range(n)):
        return False
    return all(x <= 2 for x in Counter(p for t in family for p in combinations(t, 2)).values())


def u_families(row, r):
    _, cap, _ = roles(row)
    return tuple(f for f in combinations(tuple(combinations(range(len(cap)), 3)), r) if u_valid(row, r, f))


def encode_edges(n, edges):
    pairs = tuple(combinations(range(n), 2))
    return sum(1 << pairs.index(tuple(sorted(e))) for e in edges)


def controls():
    row = (5, 0, 0, 1, 0, 0, 0)
    full = encode_edges(6, [(0, 1), (0, 2), (1, 2), (3, 5), (4, 5)])
    pruned = encode_edges(6, [(3, 5), (4, 5)])
    need(h_valid(row, full, pruned=False), 'four-only triangle allowed by weaker necessary predicate')
    need(not h_valid(row, full), 'full H not misidentified as H*')
    need(h_valid(row, pruned), 'four-four edge deletion preserves required five degrees')
    bad_triangle = encode_edges(6, [(0, 1), (0, 5), (1, 5)])
    need(not h_valid(row, bad_triangle, pruned=False), 'triangle containing a five excluded')
    need(not h_valid(row, encode_edges(6, [(3, 5)])), 'required five degree not an upper bound')
    need(not h_valid(row, -1) and not h_valid(row, True), 'malformed masks')
    ordinary = (0, 3, 1, 0, 0, 0, 0)
    need(h_masks(ordinary) == (0,), 'H* is empty when all fives are ordinary')
    need(not u_valid(ordinary, 2, ((0, 1, 2), (0, 1, 2))), 'equal neighbor triples rejected')
    high = (6, 0, 3, 0, 0, 0, 0)
    need(not u_valid(high, 3, ((0, 1, 2), (0, 1, 3), (0, 1, 4))), 'third common contact rejected')
    limited = (1, 2, 0, 1, 0, 0, 0)
    need(not u_valid(limited, 2, ((0, 1, 3), (0, 2, 3))), 'five Q-Q capacity retained')
    double = (4, 0, 0, 2, 0, 0, 0)
    need(not u_valid(double, 2, ((0, 4, 5), (1, 2, 3))), 'two five contacts at one three rejected')
    need(u_valid(ordinary, 1, ((0, 1, 2),)), 'nonempty necessary neighbor positive control')
    return {'four_only_triangle_preserved_before_pruning': True,
            'required_five_degrees_preserved_after_pruning': True,
            'necessary_controls_passed': 12,
            'controls_are_not_claimed_spherical_realizations': True}


def finite_entries():
    raw = {r: raw_profiles(r) for r in range(1, 8)}
    entries, rejection = [], {}
    for r, rows in raw.items():
        why = Counter()
        for row in rows:
            if r >= 4:
                why['imported_written_degree_bound'] += 1
            elif row[-1] or row[-2]:
                why['five_deficit_at_least_three'] += 1
            elif 3*r+row[3]+2*row[4] > 12:
                why['degree_three_contact_capacity'] += 1
            else:
                entries.append({'r': r, 'row': row, 'H_star_masks': h_masks(row),
                                'U_families': u_families(row, r)})
        rejection[r] = dict(sorted(why.items()))
    need(len(entries) == 44, 'complete necessary domains including empty ones')
    return {'raw_profiles': raw, 'domains': entries, 'pre_domain_rejections': rejection}


def summary(data):
    domains, profiles = [], []
    for e in data['domains']:
        h, u = e['H_star_masks'], e['U_families']
        d = {'r': e['r'], 'row': list(e['row']), 'H_star_count': len(h), 'H_star_sha256': digest(h),
             'U_family_count': len(u), 'U_families_sha256': digest(u)}
        domains.append(d)
        if h and u:
            a, b, f0, f1, f2, _, _ = e['row']
            profiles.append({'tuple_r_a_b_f0_f1_f2_O': [e['r'], a, b, f0, f1, f2, 15-2*e['r']-a-b],
                             'first_H_star_mask': h[0], 'first_U_family': u[0]})
    counts = dict(sorted(Counter(p['tuple_r_a_b_f0_f1_f2_O'][0] for p in profiles).items()))
    need(counts == {1: 9, 2: 12, 3: 11}, 'complete full-interval count cover')
    return {'raw_counts_by_r': {r: len(rows) for r, rows in data['raw_profiles'].items()},
            'pre_domain_rejections': data['pre_domain_rejections'], 'domains': domains,
            'all_domain_entries_sha256': digest(data['domains']),
            'profiles_by_r': counts, 'total_profiles': len(profiles), 'profiles': profiles}


def main():
    need(sys.argv[1:] in ([], ['--entries']), 'only supported flag is --entries')
    a, links, control = arithmetic(), link_cases(), controls()
    data = finite_entries()
    if sys.argv[1:]:
        out = data
    else:
        out = {'actual_agent': 'six-tammes-1', 'role': 'researcher',
               'interval': ['1/2', '3/5'], 'arithmetic': a, 'five_link_cases': links,
               'controls': control, 'cover': summary(data),
               'scope': 'Handwritten five-vertex H-triangle exclusion; full-interval necessary count cover with H*. No complete packing enumeration or global bound.'}
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
