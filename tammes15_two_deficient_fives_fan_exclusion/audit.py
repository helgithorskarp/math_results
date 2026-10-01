"""Separate definition-level finite checks, with no production-code import.

Binary incidences, raw cyclic links and binary role assignments replace
the production combinations enumerations. Same author, not peer review.
"""
from itertools import permutations, product
from pathlib import Path
import hashlib
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    root = Path(__file__).resolve().parent
    checked = json.loads((root/'EXPECTED.json').read_text())
    # All 2^4 U-F incidence matrices, ordered row-major (two Us, two Fs).
    matrices = [list(v) for v in product((0, 1), repeat=4)
                if v[0]+v[1] >= 1 and v[2]+v[3] >= 1
                and v[0]+v[2] <= 1 and v[1]+v[3] <= 1]
    families = []
    for v in matrices:
        families.append([['B', 'C']+['F'+str(j+1) for j in range(2) if v[2*i+j]] for i in range(2)])
    need(sorted(families) == checked['ordered_neighbor_families'], 'every ordered neighbor family')
    stars = []
    for bits in range(32):
        if bits.bit_count() != 3:
            continue
        word = ''.join('T' if bits >> i & 1 else 'Q' for i in range(5))
        qq = [i for i in range(5) if not (bits >> i & 1) and not (bits >> ((i+1) % 5) & 1)]
        need(len(qq) <= 1, 'one QQ edge at most')
        if qq:
            need(any(word[i:] + word[:i] == 'TTTQQ' for i in range(5)), 'three consecutive Ts')
        stars.append({'word': word, 'QQ_edges': qq})
    need(sorted(stars, key=lambda x: x['word']) == checked['five_three_T_cyclic_stars'], 'all ten star entries')
    # Raw neighbor permutations, canonicalized only after the full link check.
    links = set()
    relaxed = set()
    for cycle in permutations(('F', 'R', 'D', 'J')):
        edges = [tuple(sorted((cycle[i], cycle[(i+1) % 4]))) for i in range(4)]
        for faceword in product('QT', repeat=4):
            if faceword.count('T') != 2:
                continue
            faces = dict(zip(edges, faceword))
            if faces.get(('F', 'R')) != 'T' or faces.get(('D', 'F')) != 'Q':
                continue
            other = [e for e, kind in faces.items() if kind == 'T' and e != ('F', 'R')][0]
            i = cycle.index('F')
            canonical = cycle[i:] + cycle[:i]
            entry = (canonical, tuple(sorted(e for e, kind in faces.items() if kind == 'T')))
            relaxed.add(entry)
            if 'R' in other:
                continue
            need('D' in other and other == ('D', 'J'), 'definition-level endpoint obstruction')
            links.add(entry)
    records = [{'cycle': list(c), 'triangle_edges': [list(e) for e in es]} for c, es in sorted(links)]
    need(records == checked['ordinary_endpoint_links'], 'every allowed endpoint link')
    need(len(relaxed) == 4 and len(links) == 2, 'nonempty internal-degree control')
    roles = []
    one = []
    for bits in range(16):
        # Positions X,R,S,Z: endpoint/internal pairs are bits (0,1),(3,2).
        hit_left, hit_right = bool(bits & 3), bool(bits & 12)
        e = sorted(p for i, p in enumerate(('X', 'R', 'S', 'Z')) if bits >> i & 1)
        if hit_left and hit_right:
            need(bits.bit_count() >= 2, 'two distinct original exceptions required')
            roles.append(e)
        if bits.bit_count() <= 1:
            ordinary = []
            if not hit_left:
                ordinary.append(['R', 'X'])
            if not hit_right:
                ordinary.append(['S', 'Z'])
            need(ordinary, 'all five F2 positions obstructed')
            one.append({'F2_position': e, 'ordinary_pairs': sorted(ordinary)})
    cover = checked['fan_role_cover']
    need(sorted(roles) == cover['exceptional_subsets_hitting_both_pairs'], 'all binary fan-role assignments')
    need(sorted(one, key=lambda x: x['F2_position']) == sorted(cover['one_other_five_cases'], key=lambda x: x['F2_position']), 'all original F2 placements')
    dep = json.loads((root/'DEPENDENCIES.json').read_text())
    for name, row in dep['files'].items():
        need(hashlib.sha256((root.parent/name).read_bytes()).hexdigest() == row['sha256'], 'dependency bytes: '+name)
    old = json.loads((root.parent/'tammes15_nine_quad_odd_degree_reduction/EXPECTED.json').read_text())['cover']['profiles']
    removed = []
    rows = []
    for row in old:
        if row['r'] == 1:
            continue
        key = (row['r'], row['a'], row['b'], *row['five_counts_f0_f1_f2'])
        if key == (2, 0, 2, 0, 2, 0):
            removed.append(row)
        else:
            rows.append({k: row[k] for k in ('r', 'a', 'b', 'five_counts_f0_f1_f2', 'ordinary_fours')})
    need(len(removed) == 1 and rows == checked['catalogue_corollary']['remaining_beta_profiles'], 'entire surviving 22-row imported catalogue')
    # Controls expose exactly why the two pair / role hypotheses matter.
    need(set(('X', 'R')).isdisjoint(('Z', 'S')), 'actual disjoint pairs')
    for i in (0, 1):
        need(sum('F'+str(i+1) in t for t in (('B', 'C', 'D'), ('B', 'C', 'F1'))) <= 1, 'extra-four control feasible for capacity')
    need(sum('F'+str(i+1) in t for i in (0, 1) for t in (('B', 'C', 'D'), ('B', 'C', 'F1'))) == 1, 'extra-four control loses matching')
    return {'agent': 'six-tammes-1', 'role': 'researcher',
            'status': 'separate same-author exact finite audit; written proof not formalized',
            'raw_U_F_binary_matrices': 16, 'accepted_U_F_matrices': matrices,
            'raw_five_binary_words': 32, 'three_T_words_compared_entrywise': 10,
            'raw_endpoint_permutations': 24, 'raw_endpoint_facewords_per_permutation': 16,
            'ordinary_endpoint_links_compared_entrywise': len(links),
            'relaxed_internal_degree_links': len(relaxed),
            'raw_fan_binary_roles': 16, 'one_other_five_cases_compared_entrywise': 5,
            'minimum_two_exception_subsets': sorted(e for e in roles if len(e) == 2),
            'remaining_beta_profiles_compared_entrywise': len(rows),
            'controls_passed': True,
            'controls_are_not_spherical_packings': True}


if __name__ == '__main__':
    print(json.dumps(main(), sort_keys=True, indent=2))
