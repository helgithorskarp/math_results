"""Exact small original-face checks, six-tammes-1, researcher.
Necessary local incidences, not a full contact-map or packing enumeration.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json

ORIGINALS = ('U', 'V', 'F', 'G', 'A', 'D', 'B') + tuple('o'+str(i) for i in range(8))
ORD = ORIGINALS[7:]
DEGREE = dict(zip(ORIGINALS, (3, 3, 5, 5, 4, 4, 4)+(4,)*8))
TCAP = dict(zip(ORIGINALS, (0, 0, 3, 3, 1, 1, 0)+(2,)*8))


def need(b, m):
    if not b:
        raise ValueError(m)


def edge(a, b):
    return tuple(sorted((a, b)))


def cycle_edges(c):
    return {edge(c[i], c[(i+1) % len(c)]) for i in range(len(c))}


def stars(names, t, rt=(), rq=(), qq=()):
    out = []
    rt, rq = set(rt), set(rq)
    for p in permutations(names[1:]):
        cycle = names[:1]+p
        pairs = [edge(cycle[i], cycle[(i+1) % len(cycle)]) for i in range(len(cycle))]
        for ids in combinations(range(len(cycle)), t):
            ts = {pairs[i] for i in ids}
            qs = set(pairs)-ts
            if not rt <= ts or not rq <= qs:
                continue
            if any(any(v in e for e in ts) for v in qq):
                continue
            out.append({'cycle': list(cycle), 'T_pairs': sorted(map(list, ts)), 'Q_pairs': sorted(map(list, qs))})
    return sorted(out, key=lambda x: (x['cycle'], x['T_pairs']))


def neighbor_cover():
    triples = list(combinations(('A', 'B', 'D', 'F', 'G'), 3))
    pairs = [(u, v) for u, v in product(triples, repeat=2) if u != v
             and all(sum(f in t for t in (u, v)) <= 1 for f in ('F', 'G'))]
    def canonical(pair):
        candidates = []
        for ad, fg in product((False, True), repeat=2):
            rename = {'A': 'D', 'D': 'A'} if ad else {}
            if fg:
                rename.update({'F': 'G', 'G': 'F'})
            candidates.append(tuple(sorted(tuple(sorted(rename.get(x, x) for x in t)) for t in pair)))
        return min(candidates)
    orbits = sorted({canonical(p) for p in pairs})
    beta = [p for p in pairs if all(not {'F', 'G'} <= set(t) for t in p)]
    need(len(pairs) == 36 and len(orbits) == 8 and len(beta) == 30, 'complete full/beta neighbor covers')
    need(len({canonical(p) for p in beta}) == 6, 'six beta role orbits')
    entries = []
    for p in pairs:
        shared = set(p[0]) & set(p[1])
        bad = sorted(a for a in ('A', 'D') if a in shared and not shared-{a})
        entries.append({'ordered_triples': list(map(list, p)), 'role_orbit': list(map(list, canonical(p))),
                        'shared_one_T_without_other_common_contact': bad})
    return {'all_36_entries': entries, 'eight_full_interval_orbits': list(map(lambda p: list(map(list, p)), orbits)),
            'beta_ordered_count': len(beta), 'beta_orbit_count': 6}


def fan_placements(case):
    out = []
    for d, g in product(range(5), repeat=2):
        if d == g and d != 4:
            continue
        if d in (1, 2):
            reason = 'one_T_D_cannot_be_internal'
        elif case in ('C1', 'C7') and d == 0:
            reason = 'D_B_contact_forbidden_by_three_star'
        elif case == 'C1' and d == 3:
            reason = 'D_A_contact_forbidden_by_three_star'
        elif case == 'C5' and d == 3:
            reason = 'A_side_endpoint_has_two_Ts'
        elif g in (0, 3):
            reason = 'adjacent_fives_in_Q'
        elif case == 'C5' and g == 4:
            reason = 'single_D_cannot_cover_both_distinct_zero_B_endpoints'
        elif case == 'C5' and g == 2:
            reason = 'G_third_T_overloads_full_R_or_Z'
        elif g != 1:
            reason = 'ordinary_zero_B_endpoint_pair'
        elif case == 'C5' and d == 0:
            reason = 'G_third_T_overloads_one_T_X_equals_D'
        else:
            reason = 'RETAINED_G_R_D_'+('Z' if d == 3 else 'outside')
        out.append({'D_position': d, 'G_position': g, 'reason': reason})
    need(len(out) == 21, 'all distinct-role fan placements')
    return out


def quad_cycle(q):
    return min(q[i:]+q[:i] for q in (q, q[::-1]) for i in range(4))


def possible(triangles, quadrilaterals, extra=()):
    """Only necessary simple-face, quota, contact and incidence conditions."""
    if any(len(set(f)) != len(f) for f in triangles+quadrilaterals):
        return False
    ts = {tuple(sorted(t)) for t in triangles}
    qs = {quad_cycle(q) for q in quadrilaterals}
    adj = {v: set() for v in ORIGINALS}
    faces_per_edge = Counter()
    for f in ts | qs:
        for a, b in cycle_edges(f):
            adj[a].add(b)
            adj[b].add(a)
            faces_per_edge[edge(a, b)] += 1
    for a, b in extra:
        if a == b:
            return False
        adj[a].add(b)
        adj[b].add(a)
    if any(len(adj[v]) > DEGREE[v] for v in ORIGINALS):
        return False
    counts = Counter(v for t in ts for v in t)
    if any(counts[v] > TCAP[v] for v in ORIGINALS):
        return False
    if any(n > 2 for n in faces_per_edge.values()):
        return False
    if any(q[2] in adj[q[0]] or q[3] in adj[q[1]] for q in qs):
        return False
    if any(len(adj[a] & adj[b]) > 2 for a, b in combinations(ORIGINALS, 2)):
        return False
    return True


def instantiate(fs, mapping):
    return [tuple(mapping.get(x, x) for x in f) for f in fs]


def encoded(values):
    n = 0
    for v in values:
        n = 16*n+ORIGINALS.index(v)
    return n


def c1_alias_frames(y_domain):
    triangles = [('F', 'X', 'G'), ('F', 'G', 'S'), ('F', 'S', 'Z'),
                 ('A', 'Z', 'J'), ('J', 'D', 'K'), ('G', 'X', 'N')]
    quads = [('V', 'F', 'X', 'B'), ('V', 'A', 'Z', 'F'), ('U', 'A', 'V', 'B'),
             ('U', 'A', 'J', 'D'), ('U', 'D', 'L', 'B')]
    accepted = []
    terminal_same_opposite = []
    raw = 0
    for j, k, l, n in product(ORD, ORD+('G',), ORD+('G',), ORD):
        m = dict(X=ORD[0], S=ORD[1], Z=ORD[2], J=j, K=k, L=l, N=n)
        ts, qs = instantiate(triangles, m), instantiate(quads, m)
        for y in y_domain:
            raw += 1
            if y in ('F', ORD[0], ORD[1], n):
                continue
            if possible(ts, qs, extra=[('U', a) for a in ('A', 'B', 'D')]
                        +[('V', a) for a in ('A', 'B', 'F')]+[('G', y)]):
                code = encoded((j, k, l, n, y))
                if l == k:
                    # T(D,K,J),Q(U,D,K,B): J is full and ordinary K
                    # therefore forces its second T at zero-T B.
                    count = Counter(v for t in {tuple(sorted(t)) for t in ts} for v in t)
                    need(k in ORD and k != ORD[2] and count[j] == 2, 'repeated opposite: ordinary K differs from A/Z, J has full quota')
                    terminal_same_opposite.append(code)
                else:
                    accepted.append(code)
    return {'raw_assignments': raw, 'slot_order': ['J', 'K', 'L', 'N', 'Y'],
            'K_equals_L_prefixes_excluded_by_terminal_endpoint_rule': sorted(terminal_same_opposite),
            'accepted_encoded_original_assignments': sorted(accepted)}


def c7_alias_frames():
    triangles = [('F', 'X', 'G'), ('F', 'G', 'S'), ('F', 'S', 'Z'),
                 ('G', 'X', 'W'), ('A', 'Z', 'J'), ('J', 'D', 'M')]
    quads = [('U', 'F', 'X', 'B'), ('U', 'A', 'Z', 'F'), ('V', 'G', 'W', 'B'),
             ('V', 'D', 'S', 'G'), ('U', 'A', 'L', 'B'), ('S', 'D', 'J', 'Z'),
             ('V', 'D', 'M', 'E')]
    accepted = []
    for j, l, m, e in product(ORD, ORD, ORD, ('G', 'B')):
        alias = dict(X=ORD[0], S=ORD[1], Z=ORD[2], W=ORD[3], J=j, L=l, M=m, E=e)
        if possible(instantiate(triangles, alias), instantiate(quads, alias),
                    extra=[('U', a) for a in ('A', 'B', 'F')]+[('V', a) for a in ('B', 'D', 'G')]):
            accepted.append(encoded((j, l, m, e)))
    return {'raw_assignments': 1024, 'slot_order': ['J', 'L', 'M', 'E'],
            'accepted_encoded_original_assignments': sorted(accepted)}


def c5_last_quad():
    ts = [('F', 'X', 'G'), ('F', 'G', 'S'), ('F', 'S', 'Z'), ('G', 'X', 'W'), ('A', 'Z', 'W')]
    qs = [('U', 'F', 'X', 'B'), ('U', 'A', 'Z', 'F'), ('V', 'G', 'S', 'B'),
          ('V', 'A', 'W', 'G'), ('U', 'A', 'V', 'B'), ('B', 'X', 'K', 'S')]
    accepted = []
    for w, k in product(ORD, ('F', 'G')):
        alias = dict(X=ORD[0], S=ORD[1], Z=ORD[2], W=w, K=k)
        if possible(instantiate(ts, alias), instantiate(qs, alias)):
            accepted.append(encoded((w, k)))
    return {'raw_assignments': 16, 'slot_order': ['W', 'last_Q_opposite'],
            'accepted_encoded_original_assignments': accepted}


def c2_three_T_stars():
    out = []
    for s in stars(('F', 'X', 'S', 'Z', 'H'), 3,
                   rt=[edge('F', 'X'), edge('F', 'S'), edge('Z', 'H')]):
        if ['S', 'Z'] in s['Q_pairs']:
            reason, domain = 'S_Z_contact_Q_diagonal', None
        else:
            need(['H', 'S'] in s['Q_pairs'], 'other three-T G corner')
            domain = ['Z']  # H's exact U,V,Z,G contacts; ordinary S cannot contact U,V.
            reason = 'forced_Z_creates_G_Z_contact_Q_diagonal'
        out.append(dict(s, reason=reason, opposite_domain=domain))
    need(len(out) == 4, 'both orientations of both three-T G star cycles')
    return out


def c8_budget_and_last_quad():
    names = ('X', 'R', 'S', 'Z', 'Xp', 'Rp', 'Sp', 'Zp')
    mapping = dict(zip(names, ORD))
    ts = instantiate([('F', 'X', 'R'), ('F', 'R', 'S'), ('F', 'S', 'Z'),
                      ('G', 'Xp', 'Rp'), ('G', 'Rp', 'Sp'), ('G', 'Sp', 'Zp'),
                      ('A', 'X', 'Xp'), ('D', 'Z', 'Zp')], mapping)
    qs = instantiate([('U', 'F', 'X', 'A'), ('U', 'D', 'Z', 'F'),
                      ('V', 'G', 'Xp', 'A'), ('V', 'D', 'Zp', 'G'), ('U', 'A', 'V', 'D')], mapping)
    counts = Counter(v for t in ts for v in t)
    need(all(counts[v] == TCAP[v] for v in ORIGINALS), 'all triangle quotas exactly saturated')
    adj = {v: set() for v in ORIGINALS}
    for f in ts+qs:
        for a, b in cycle_edges(f):
            adj[a].add(b)
            adj[b].add(a)
    remaining = sorted(v for v in ORIGINALS if v != 'B' and len(adj[v]) < DEGREE[v])
    need(remaining == sorted(mapping[n] for n in ('R', 'S', 'Rp', 'Sp')), 'only four internal contact slots available to B')
    entries = []
    rlinks = stars(('F', 'X', 'S', 'B'), 2, rt=[edge('F', 'X'), edge('F', 'S')])
    slinks = stars(('F', 'R', 'Z', 'B'), 2, rt=[edge('F', 'R'), edge('F', 'Z')])
    for r, t in product(rlinks, slinks):
        def next_away(cycle, neighbor):
            i = cycle.index(neighbor)
            return next(cycle[j % 4] for j in (i-1, i+1) if cycle[j % 4] != 'F')
        b1 = next_away(r['cycle'], 'S')
        b2 = next_away(t['cycle'], 'R')
        need(b1 == b2 == 'B', 'both fourth-neighbor Q positions are the same B')
        entries.append({'R_cycle': r['cycle'], 'S_cycle': t['cycle'], 'forced_Q': ['R', 'S', b2, b1], 'simple': False})
    need(len(entries) == 4, 'both orientations of both saturated internal links')
    relaxed_s = stars(('F', 'R', 'Z', 'Bp'), 2, rt=[edge('F', 'R'), edge('F', 'Z')])
    relaxed_qs = [['R', 'S', next_away(t['cycle'], 'R'), next_away(r['cycle'], 'S')]
                  for r, t in product(rlinks, relaxed_s)]
    need(len(relaxed_qs) == 4 and all(len(set(q)) == 4 for q in relaxed_qs), 'nonempty distinct fourth-neighbor control')
    return {'all_15_original_triangle_counts': {v: counts[v] for v in ORIGINALS},
            'only_B_contact_candidates': remaining, 'last_Q_all_four_entries': entries,
            'relaxing_one_fourth_neighbor_to_Bp_gives_four_simple_local_Qs': 4}


def catalogue():
    root = Path(__file__).resolve().parent
    deps = json.loads((root/'DEPENDENCIES.json').read_text())['files']
    for path, meta in deps.items():
        need(hashlib.sha256((root.parent/path).read_bytes()).hexdigest() == meta['sha256'], 'public dependency '+path)
    old = json.loads((root.parent/'tammes15_one_triangle_four_exclusion/EXPECTED.json').read_text())['catalogue_corollary']
    rows = old['remaining_beta_profiles']
    need(len(rows) == 21 and old['counts_r1_r2_r3'] == [0, 10, 11], 'preceding published21-row cover')
    removed = [r for r in rows if (r['r'], r['a'], r['b'], tuple(r['five_counts_f0_f1_f2'])) == (2, 2, 1, (0, 2, 0))]
    need(len(removed) == 1, 'new excluded row occurs exactly once')
    remaining = [r for r in rows if r not in removed]
    return {'newly_excluded_row': removed[0], 'remaining_beta_profiles': remaining, 'counts_r1_r2_r3': [0, 9, 11],
            'remaining_profile_sha256': hashlib.sha256(json.dumps(remaining, separators=(',', ':')).encode()).hexdigest(),
            'prior_catalogue_imported_not_regenerated': True,
            'guarded_dependency_sha256': {p: m['sha256'] for p, m in deps.items()}}


def main():
    one = stars(('U', 'V', 'P', 'Q'), 1, qq=('U', 'V'))
    need(len(one) == 4 and all(['U', 'V'] in s['Q_pairs'] for s in one), 'two threes at one-T four share a Q')
    relax_one = [s for s in stars(('U', 'V', 'P', 'Q'), 0) if ['U', 'V'] not in s['Q_pairs']]
    need(len(relax_one) == 2, 'zero-T four allows nonadjacent three contacts')
    endpoint = stars(('H', 'R', 'C', 'J'), 2, rt=[edge('H', 'R')], rq=[edge('H', 'C')])
    saturated = [s for s in endpoint if not any('R' in p for p in s['T_pairs'] if p != ['H', 'R'])]
    need(len(endpoint) == 4 and len(saturated) == 2, 'ordinary endpoint saturation and its nonempty quota control')
    extension = stars(('F', 'P', 'Q', 'N', 'V'), 3, rt=[edge('F', 'P'), edge('F', 'Q')], qq=('V',))
    need(len(extension) == 4, 'all third-T extensions at a five with a three contact')
    for s in extension:
        added = [p for p in s['T_pairs'] if p not in (['F', 'P'], ['F', 'Q'])]
        need(len(added) == 1 and added[0] in (['N', 'P'], ['N', 'Q']), 'third T extends one common original')
    contiguous = stars(('F', 'X', 'S', 'N', 'Y'), 3,
                       rt=[edge('F', 'X'), edge('F', 'S'), edge('X', 'N')])
    need(len(contiguous) == 2 and all(all('Y' not in p for p in s['T_pairs']) for s in contiguous), 'C1 fifth contact is Q-Q')
    sealed = [s for s in stars(('F', 'G', 'D', 'K'), 2) if {edge('F','G'),edge('F','D'),edge('G','D')} <= cycle_edges(tuple(s['cycle']))]
    need(not sealed, 'a sealed C3 cannot fit a degree-four link')
    c1 = c1_alias_frames(('A', 'D', 'B'))
    c1_control = c1_alias_frames(ORD)
    c7, c5 = c7_alias_frames(), c5_last_quad()
    need(not c1['accepted_encoded_original_assignments'] and not c7['accepted_encoded_original_assignments']
         and not c5['accepted_encoded_original_assignments'], 'all finite forced-face alias frames excluded')
    need(c1_control['accepted_encoded_original_assignments'], 'dropping large-corner ordinary QQ exclusion opens C1 necessary frames')
    return {'agent': 'six-tammes-1', 'role': 'researcher',
            'status': 'conditional hand proof with exact local checks; independent mathematical review pending',
            'scope': 'actual N15 complete connected degree3..5, simple convex hemispherical cellular T/Q, nine Qs',
            'new_row_interval': 'FULL OPEN1/2<c<3/5; no beta/H premise',
            'original_encoding': list(ORIGINALS), 'encoded_assignments': 'base16 original indices in stated slot order',
            'neighbor_cover': neighbor_cover(), 'one_T_four_two_three_contact_stars': one,
            'ordinary_endpoint_all_links': endpoint,
            'qualified_endpoint_assumption': 'the full internal point other known triangles exclude the ordinary endpoint', 'ordinary_endpoint_saturated_links': saturated,
            'three_T_five_all_third_extensions': extension, 'C1_contiguous_known_G_stars': contiguous,
            'fan_placement_entries': {k: fan_placements(k) for k in ('C1', 'C5', 'C7')},
            'C2_and_C1_G_alias_three_T_star_obstructions': c2_three_T_stars(),
            'C1_all_original_alias_frames': c1, 'C7_all_original_alias_frames': c7, 'C5_last_Q_frames': c5,
            'C8_original_budget_and_nonsimple_Q': c8_budget_and_last_quad(),
            'credited_Bernstein_margin': ['1/2', '7/20', '4/25'],
            'controls': {'zero_T_four_nonadjacent_threes': relax_one,
                         'ordinary_QQ_neighbor_C1_relaxed_frames': c1_control,
                         'relaxed_assignments_are_not_sphere_packings': True},
            'catalogue_corollary': catalogue(), 'written_geometric_bridges_unformalized': True,
            'global_numerical_Tammes15_bounds_unchanged': True}


if __name__ == '__main__':
    print(json.dumps(main(), sort_keys=True, indent=2))
