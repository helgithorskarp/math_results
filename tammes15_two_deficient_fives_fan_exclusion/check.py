"""Tiny exact checks accompanying the hand proof; six-tammes-1, researcher.

This enumerates local necessary conditions, not spherical configurations.
CPython >=3.11, standard library only. Written bridges are in PROOF.md.
"""
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(',', ':')).encode()).hexdigest()


def neighbors(eligible=('B', 'C', 'F1', 'F2')):
    triples = list(combinations(eligible, 3))
    return [list(map(list, family)) for family in product(triples, repeat=2)
            if all(sum(f in t for t in family) <= 1 for f in ('F1', 'F2'))]


def stars():
    rows = []
    for t in combinations(range(5), 3):
        word = ''.join('T' if i in t else 'Q' for i in range(5))
        qq = [i for i in range(5) if word[i] == word[(i+1) % 5] == 'Q']
        need(len(qq) <= 1, 'deficit-one five permits at most one three contact')
        if qq:
            start = (qq[0]+2) % 5
            rotated = ''.join(word[(start+i) % 5] for i in range(5))
            need(rotated == 'TTTQQ', 'a three contact forces a consecutive three-T fan')
        rows.append({'word': word, 'QQ_edges': qq})
    return sorted(rows, key=lambda x: x['word'])


def endpoint_stars():
    """All oriented X-links with distinct neighbors F,R,D,J, fixing F first.

    T(F,X,R) and Q(F,X,D,U) fix FR=T and FD=Q in the link.
    R already has both its T faces. Exactly two T faces are required at X.
    """
    out = []
    for rest in permutations(('R', 'D', 'J')):
        cycle = ('F',) + rest
        pairs = [frozenset((cycle[i], cycle[(i+1) % 4])) for i in range(4)]
        if frozenset(('F', 'R')) not in pairs or frozenset(('F', 'D')) not in pairs:
            continue
        for t in combinations(range(4), 2):
            triangles = [pairs[i] for i in t]
            if frozenset(('F', 'R')) not in triangles:
                continue
            if frozenset(('F', 'D')) in triangles:
                continue
            second = next(p for p in triangles if p != frozenset(('F', 'R')))
            if 'R' in second:
                continue
            need(second == frozenset(('D', 'J')), 'endpoint forces a triangle at D')
            out.append({'cycle': list(cycle), 'triangle_edges': sorted(sorted(p) for p in triangles)})
    need(len(out) == 2, 'both link orientations retained')
    return sorted(out, key=lambda x: x['cycle'])


def fan_cases():
    positions = ('X', 'R', 'S', 'Z')
    pairs = (frozenset(('X', 'R')), frozenset(('Z', 'S')))
    one_five = []
    for exceptional in (frozenset(),) + tuple(frozenset((p,)) for p in positions):
        ordinary_pairs = [sorted(p) for p in pairs if not p & exceptional]
        need(ordinary_pairs, 'one other original five cannot cover both disjoint pairs')
        one_five.append({'F2_position': sorted(exceptional), 'ordinary_pairs': sorted(ordinary_pairs)})
    avoiding = []
    for k in range(5):
        for t in combinations(positions, k):
            e = frozenset(t)
            if all(p & e for p in pairs):
                need(len(e) >= 2, 'two distinct exceptional original fan vertices required')
                avoiding.append(sorted(e))
    need(len(avoiding) == 9, 'all 16 binary exceptional-role subsets inspected')
    return {'one_other_five_cases': one_five,
            'exceptional_subsets_hitting_both_pairs': sorted(avoiding),
            'minimum_exceptional_count': min(map(len, avoiding))}


def dependencies_and_rows():
    root = Path(__file__).resolve().parent
    dep = json.loads((root/'DEPENDENCIES.json').read_text())
    for name, record in dep['files'].items():
        need(hashlib.sha256((root.parent/name).read_bytes()).hexdigest() == record['sha256'],
             'published dependency bytes: '+name)
    old = json.loads((root.parent/'tammes15_nine_quad_odd_degree_reduction/EXPECTED.json').read_text())['cover']
    need(old['total_necessary_count_profiles'] == 32, 'prior beta count catalogue')
    target = [x for x in old['profiles'] if x['r'] == 2 and x['a'] == 0 and x['b'] == 2
              and x['five_counts_f0_f1_f2'] == [0, 2, 0]]
    need(len(target) == 1, 'exactly one newly excluded catalogue row')
    need(target[0]['first_U_family'] == [[0, 1, 2], [0, 1, 3]], 'prior representative matches direct argument')
    keys = ('r', 'a', 'b', 'five_counts_f0_f1_f2', 'ordinary_fours')
    rows = [{k: x[k] for k in keys} for x in old['profiles'] if x['r'] != 1 and x not in target]
    need(len(rows) == 22 and [sum(x['r'] == r for x in rows) for r in (1, 2, 3)] == [0, 11, 11],
         'prior r1 exclusion and new row give 22 necessary profiles')
    return {'hash_guarded_public_dependencies': {p: v['sha256'] for p, v in dep['files'].items()},
            'newly_excluded_row': {k: target[0][k] for k in keys},
            'remaining_beta_profiles': rows,
            'counts_r1_r2_r3': [0, 11, 11],
            'remaining_beta_profiles_sha256': digest(rows),
            'prior_catalogue_is_imported_not_regenerated': True}


def controls():
    extra = neighbors(('B', 'C', 'D', 'F1', 'F2'))
    witness = [['B', 'C', 'D'], ['B', 'C', 'F1']]
    need(witness in extra, 'a third eligible deficient four breaks forced matching')
    p = (frozenset(('X', 'R')), frozenset(('Z', 'S')))
    need(all(q & {'X', 'Z'} for q in p), 'two exceptional fan vertices can cover both pairs')
    need(any(not q & {'X', 'R'} for q in p), 'two exceptions in the same pair do not suffice')
    need(all(q & {'V'} for q in ({'X', 'V'}, {'Z', 'V'})), 'merged internal vertices would invalidate disjointness')
    # Relaxing R's exact two-T count admits the second triangle X,R,J.
    need(frozenset(('R', 'J')) != frozenset(('D', 'J')), 'third T at R can avoid D')
    return {'extra_eligible_four_counterfamily': witness,
            'two_five_control': ['X', 'Z'],
            'same_pair_control_still_forces_opposite_pair': ['X', 'R'],
            'aliased_internal_control': 'R=S=V',
            'relaxed_internal_triangle_capacity_control': ['R', 'J'],
            'controls_are_necessary_role_assignments_not_packings': True}


def result():
    matched = neighbors()
    expected = [[['B', 'C', 'F1'], ['B', 'C', 'F2']],
                [['B', 'C', 'F2'], ['B', 'C', 'F1']]]
    need(matched == expected, 'all 16 ordered contact-triple choices yield exactly two matchings')
    return {'agent': 'six-tammes-1', 'role': 'researcher',
            'status': 'hand proof with exact finite local checks; independent review pending',
            'full_interval': '1/2<c<3/5',
            'scope': 'complete connected degree3..5 cellular simple strictly convex hemispherical T/Q contact graph; nine Qs',
            'ordered_neighbor_families': matched,
            'five_three_T_cyclic_stars': stars(),
            'ordinary_endpoint_links': endpoint_stars(),
            'fan_role_cover': fan_cases(),
            'controls': controls(),
            'catalogue_corollary': dependencies_and_rows(),
            'trust_boundary': 'written spherical corner reduction and face/point correspondence are unformalized; no global bound or optimizer coverage'}


if __name__ == '__main__':
    print(json.dumps(result(), sort_keys=True, indent=2))
