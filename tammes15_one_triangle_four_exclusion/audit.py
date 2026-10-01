"""Separate exact finite audit: binary incidences and Hamiltonian edge sets.
No production-code import. Same author; independent mathematical review pending.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json


def need(b, m):
    if not b:
        raise ValueError(m)


def all_fan_roles(case, independence=True):
    result = []
    positions = (1, 2, 4, 8, 0)
    for apos, amask in enumerate(positions):
        for gpos, gmask in enumerate(positions):
            if amask & gmask:
                continue
            if amask & 6:
                reason = 'A_one_T_cannot_be_internal'
            elif case == 'BC':
                if independence and amask & 9:
                    reason = 'A_contacts_B_or_C_but_U_neighbor_pair_is_noncontact'
                elif not ((amask | gmask) & 3 and (amask | gmask) & 12):
                    reason = 'ordinary_pair_forces_T_at_zero_opposite'
                else:
                    reason = 'RELAXED_survivor'
            elif amask:
                reason = 'A_Q_opposite_of_F_is_noncontact_of_F'
            elif not gmask & 3:
                reason = 'ordinary_XR_pair_forces_T_at_zero_B'
            elif gmask & 1:
                reason = 'F_and_G_cannot_be_adjacent_in_Q'
            else:
                reason = 'RETAINED_G_at_R'
            result.append({'A_position': apos, 'G_position': gpos, 'reason': reason})
    return sorted(result, key=lambda x: (x['A_position'], x['G_position']))


def ordinary_j_entries():
    labels = ('F', 'G', 'A', 'B', 'C', 'U', 'V', 'X', 'S', 'Z', 'N')
    faces = [('F', 'X', 'G'), ('F', 'G', 'S'), ('F', 'S', 'Z'), ('Z', 'A', 'J')]
    quads = [('V', 'F', 'X', 'B'), ('V', 'A', 'Z', 'F')]
    out = []
    for alias in ('X', 'N'):
        pairs = set()
        for t in faces:
            t = tuple(alias if x == 'J' else x for x in t)
            pairs.update(tuple(sorted(e)) for e in combinations(t, 2))
        for q in quads:
            pairs.update(tuple(sorted((q[i], q[(i+1) % 4]))) for i in range(4))
        pairs.update(tuple(sorted((u, v))) for u, vertices in [('U', 'ABC'), ('V', ('F', 'A', 'B'))] for v in vertices)
        index = {v: i for i, v in enumerate(labels)}
        adj = [0]*len(labels)
        for a, b in pairs:
            adj[index[a]] |= 1 << index[b]
            adj[index[b]] |= 1 << index[a]
        def ns(v):
            return sorted(x for i, x in enumerate(labels) if adj[index[v]] >> i & 1)
        if alias == 'X':
            need(len(ns('X')) == 5, 'original J=X exceeds ordinary-four degree')
            out.append({'J_alias': 'X', 'reason': 'ordinary_X_has_five_distinct_contacts', 'contacts': ns('X')})
            continue
        need(adj[index['A']].bit_count() == 4 and adj[index['Z']].bit_count() == 4 and adj[index['V']].bit_count() == 3, 'complete contact lists saturated')
        candidates = [p for p in ns('A') if p != 'U' and not (p in ('V', 'Z') and not (adj[index[p]] >> index['C'] & 1))]
        need(candidates == ['N'], 'whole opposite domain is the forced J')
        out.append({'J_alias': 'N', 'A_contacts': ns('A'), 'Z_contacts': ns('Z'),
                    'U_A_C_opposite_candidates': candidates,
                    'excluded_candidates': {'V': 'complete_degree_three_V_cannot_contact_C', 'Z': 'complete_degree_four_Z_cannot_contact_C'},
                    'forced_Q': ['U', 'A', 'N', 'C'], 'endpoint_second_T_contains_zero_C': True})
    return out


def endpoint_entries():
    out = set()
    for cycle in permutations(('A', 'Z', 'C', 'K')):
        edges = [tuple(sorted((cycle[i], cycle[(i+1) % 4]))) for i in range(4)]
        for word in product((0, 1), repeat=4):
            if sum(word) != 2:
                continue
            faces = dict(zip(edges, word))
            if faces.get(('A', 'Z')) != 1 or faces.get(('A', 'C')) != 0:
                continue
            second = [e for e in edges if faces[e] and e != ('A', 'Z')][0]
            if 'Z' in second:
                continue
            need(second == ('C', 'K'), 'raw J link forces C triangle')
            i = cycle.index('A')
            out.add((cycle[i:] + cycle[:i], second))
    return [{'J_neighbor_cycle': list(c), 'second_T_neighbors': list(e)} for c, e in sorted(out)]


def hamiltonian_stars(tg=4, caps_override=None):
    """All undirected 5-cycles by edge sets; direct triangle incidences.
    Expand both orientations only after the undirected star is checked.
    """
    names = ('F', 'X', 'S', 'Z', 'A')
    pairs = list(combinations(range(5), 2))
    req = {pairs.index((0, 1)), pairs.index((0, 2)), pairs.index((3, 4))}
    initial = [('G', 'F', 'X'), ('G', 'F', 'S'), ('F', 'S', 'Z'), ('G', 'Z', 'A')]
    used = Counter(p for t in initial for p in t)
    caps = {'F': 3, 'X': 2, 'S': 2, 'Z': 2, 'A': 1, 'G': tg}
    if caps_override:
        caps.update(caps_override)
    out = []
    cycles_count = 0
    for ids in combinations(range(10), 5):
        adjacency = [set() for _ in names]
        for e in ids:
            i, j = pairs[e]
            adjacency[i].add(j)
            adjacency[j].add(i)
        if any(len(a) != 2 for a in adjacency):
            continue
        seen, stack = {0}, [0]
        while stack:
            v = stack.pop()
            for u in adjacency[v]-seen:
                seen.add(u)
                stack.append(u)
        if len(seen) != 5:
            continue
        cycles_count += 1
        for tids in combinations(ids, tg):
            triangles = set(tids)
            if not req <= triangles:
                continue
            extra = triangles-req
            incident = used.copy()
            for e in extra:
                incident['G'] += 1
                for i in pairs[e]:
                    incident[names[i]] += 1
            overloaded = sorted(p for p in names if incident[p] > caps[p])
            need(incident['G'] == tg, 'exact G triangle count in the complete star')
            for first in sorted(adjacency[0]):
                order = [0, first]
                while len(order) < 5:
                    nxt = next(iter(adjacency[order[-1]]-{order[-2]}))
                    need(nxt not in order, 'simple Hamiltonian traversal')
                    order.append(nxt)
                need(0 in adjacency[order[-1]], 'closed cycle')
                out.append({'G_neighbor_cycle': [names[i] for i in order],
                            'Q_sectors': sorted(sorted(names[i] for i in pairs[e]) for e in set(ids)-triangles),
                            'additional_T_sectors': sorted(sorted(names[i] for i in pairs[e]) for e in extra),
                            'overloaded_original_vertices': overloaded})
    need(cycles_count == 12, 'all twelve undirected five-vertex Hamiltonian cycles')
    return sorted(out, key=lambda x: (x['G_neighbor_cycle'], x['Q_sectors']))


def main():
    root = Path(__file__).resolve().parent
    expected = json.loads((root/'EXPECTED.json').read_text())
    families = []
    for a, b in product(range(16), repeat=2):
        if a.bit_count() != 3 or b.bit_count() != 3 or a == b or (bool(a & 8)+bool(b & 8) > 1):
            continue
        families.append([[p for i, p in enumerate(('A', 'B', 'C', 'F')) if mask >> i & 1] for mask in (a, b)])
    need(sorted(families) == expected['ordered_neighbor_families'], 'every ordered contact-neighbor family')
    repeats = sum(a.bit_count() == b.bit_count() == 3 and (bool(a & 8)+bool(b & 8) <= 1)
                  for a, b in product(range(16), repeat=2))
    relaxed_f = sum(a.bit_count() == b.bit_count() == 3 and a != b
                    for a, b in product(range(16), repeat=2))
    need(repeats == expected['controls']['repeated_neighbor_family_count'] == 7, 'repeated ABC control')
    need(relaxed_f == expected['controls']['relaxed_F_capacity_neighbor_family_count'] == 12, 'relaxed F contact-capacity control')
    swap = {'B': 'C', 'C': 'B'}
    roles = {'A': (4, 1), 'B': (4, 0), 'C': (4, 0), 'F': (5, 3), 'G': (5, 4), 'U': (3, 0), 'V': (3, 0)}
    need(all(roles[p] == roles[swap.get(p, p)] for p in roles), 'B/C renaming preserves all exceptional degrees and T counts')
    def rename(face):
        return tuple(swap.get(p, p) for p in face)
    schemas = [('V', 'F', 'X', 'B'), ('V', 'A', 'Z', 'F'), ('U', 'A', 'J', 'C')]
    need(all(rename(rename(face)) == face for face in schemas), 'explicit B/C face-renaming involution')
    for case, key in [('BC', 'FBC'), ('AB', 'FAB')]:
        need(all_fan_roles(case) == expected['fan_cases'][key], 'all twenty-one fixed A/G placements: '+case)
    need(ordinary_j_entries() == expected['ordinary_J_aliases_and_Q_forcing'], 'ordinary-J aliases and full opposite domains')
    need(endpoint_entries() == expected['ordinary_J_endpoint_links'], 'all ordinary-J endpoint links')
    stars = hamiltonian_stars()
    need(stars == expected['G_equals_J_all_eight_star_obstructions'], 'all G=J stars entrywise by a different representation')
    need(all(x['overloaded_original_vertices'] for x in stars), 'every terminal star excluded')
    controls = expected['controls']
    need(hamiltonian_stars(3) == controls['three_T_G_stars'], 'nonempty three-T G control')
    for key, cap in [('unsaturated_A_stars', {'A': 2}), ('unsaturated_Z_stars', {'Z': 3})]:
        relaxed = [x for x in hamiltonian_stars(caps_override=cap) if not x['overloaded_original_vertices']]
        need(relaxed == controls[key] and len(relaxed) == 2, 'saturation control: '+key)
    relaxed = [x for x in all_fan_roles('BC', False) if x['reason'] == 'RELAXED_survivor']
    need(relaxed == controls['without_U_neighbor_independence_fan_survivors'] and relaxed, 'nonempty U-independence control')
    # Direct affine expansion followed by power-to-Bernstein conversion.
    lo, width = Fraction(1, 2), Fraction(1, 10)
    powers = [1+lo-4*lo*lo, width*(1-8*lo), -4*width*width]
    bernstein = [powers[0], powers[0]+powers[1]/2, sum(powers)]
    need(list(map(str, bernstein)) == expected['credited_1_plus_c_minus_4c_squared_Bernstein'], 'all credited exact coefficients')
    deps = json.loads((root/'DEPENDENCIES.json').read_text())['files']
    for name, entry in deps.items():
        need(hashlib.sha256((root.parent/name).read_bytes()).hexdigest() == entry['sha256'], 'public dependency '+name)
    prior = json.loads((root.parent/'tammes15_two_deficient_fives_fan_exclusion/EXPECTED.json').read_text())['catalogue_corollary']['remaining_beta_profiles']
    rows = []
    removed = []
    for r in prior:
        key = (r['r'], r['a'], r['b'], tuple(r['five_counts_f0_f1_f2']))
        (removed if key == (2, 1, 2, (1, 1, 0)) else rows).append(r)
    need(len(removed) == 1 and rows == expected['catalogue_corollary']['remaining_beta_profiles'], 'all twenty-one imported necessary rows')
    return {'agent': 'six-tammes-1', 'role': 'researcher',
            'status': 'separate same-author exact finite audit; geometric proof unformalized',
            'raw_binary_neighbor_mask_pairs': 256, 'neighbor_families_compared_entrywise': len(families),
            'A_G_raw_fan_position_choices_per_case': 25,
            'distinct_role_entries_compared_per_case': 21,
            'freely_named_B_C_exchange_preserves_all_roles': True,
            'ordinary_J_alias_cases_compared': 2, 'ordinary_J_endpoint_links_compared': 2,
            'raw_undirected_five_cycle_edge_subsets': 252, 'undirected_five_cycles': 12,
            'G_equals_J_oriented_stars_compared_entrywise': len(stars), 'G_equals_J_survivors': 0,
            'three_T_G_control_stars': 4, 'unsaturated_A_control_stars': 2, 'unsaturated_Z_control_stars': 2,
            'controls_are_not_sphere_packings': True,
            'credited_exact_Bernstein_entries_compared': 3,
            'remaining_beta_profiles_compared_entrywise': len(rows)}


if __name__ == '__main__':
    print(json.dumps(main(), sort_keys=True, indent=2))
