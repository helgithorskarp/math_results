"""Exact local case checks for the hand proof; six-tammes-1, researcher.
CPython>=3.11 standard library. Necessary incidences, not sphere packings.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json


def need(b, message):
    if not b:
        raise ValueError(message)


def edge(a, b):
    return tuple(sorted((a, b)))


def neighbor_families(repeat_allowed=False, f_capacity=1):
    triples = list(combinations(('A', 'B', 'C', 'F'), 3))
    return [list(map(list, (t, u))) for t in triples for u in triples
            if (repeat_allowed or t != u) and sum('F' in v for v in (t, u)) <= f_capacity]


def fan_roles(case, independence=True):
    """A/G original placements: 0=X,1=R,2=S,3=Z,4=outside.
    Both outside denotes two different originals outside the fan.
    """
    out = []
    for a, g in product(range(5), repeat=2):
        if a == g and a < 4:
            continue  # Different fixed degree/T roles cannot be one fan neighbor.
        if a in (1, 2):
            reason = 'A_one_T_cannot_be_internal'
        elif case == 'BC':
            if independence and a in (0, 3):
                reason = 'A_contacts_B_or_C_but_U_neighbor_pair_is_noncontact'
            elif not ({0, 1} & {a, g} and {2, 3} & {a, g}):
                reason = 'ordinary_pair_forces_T_at_zero_opposite'
            else:
                reason = 'RELAXED_survivor'
        else:
            need(case == 'AB', 'canonical zero-B/one-A case')
            if a != 4:
                reason = 'A_Q_opposite_of_F_is_noncontact_of_F'
            elif g not in (0, 1):
                reason = 'ordinary_XR_pair_forces_T_at_zero_B'
            elif g == 0:
                reason = 'F_and_G_cannot_be_adjacent_in_Q'
            else:
                reason = 'RETAINED_G_at_R'
        out.append({'A_position': a, 'G_position': g, 'reason': reason})
    need(len(out) == 21, 'all distinct original A/G placement choices')
    return out


def endpoint_links():
    out = []
    for p in permutations(('Z', 'C', 'K')):
        cycle = ('A',) + p
        pairs = [edge(cycle[i], cycle[(i+1) % 4]) for i in range(4)]
        for t in combinations(range(4), 2):
            ts = {pairs[i] for i in t}
            if edge('A', 'Z') not in ts or edge('A', 'C') not in pairs or edge('A', 'C') in ts:
                continue
            other = next(iter(ts - {edge('A', 'Z')}))
            if 'Z' in other:
                continue  # Z already has two Ts.
            need(other == edge('C', 'K'), 'ordinary J forces its second T at C')
            out.append({'J_neighbor_cycle': list(cycle), 'second_T_neighbors': list(other)})
    need(len(out) == 2, 'both endpoint orientations')
    return sorted(out, key=lambda x: x['J_neighbor_cycle'])


def ordinary_j():
    ts = [('F', 'X', 'G'), ('F', 'G', 'S'), ('F', 'S', 'Z'), ('Z', 'A', 'J')]
    qs = [('V', 'F', 'X', 'B'), ('V', 'A', 'Z', 'F')]
    results = []
    for alias in ('X', 'N'):
        def actual(x):
            return alias if x == 'J' else x
        adj = {p: set() for p in ('F', 'G', 'A', 'B', 'C', 'U', 'V', 'X', 'S', 'Z', 'N')}
        for face in ts + qs:
            points = tuple(map(actual, face))
            need(len(set(points)) == len(points), 'simple original face after J alias')
            for i, p in enumerate(points):
                q = points[(i+1) % len(points)]
                adj[p].add(q)
                adj[q].add(p)
        for p, neighbors in [('U', ('A', 'B', 'C')), ('V', ('F', 'A', 'B'))]:
            for q in neighbors:
                adj[p].add(q)
                adj[q].add(p)
        if alias == 'X':
            need(adj['X'] == {'F', 'G', 'B', 'Z', 'A'}, 'positive original J=X alias yields degree five at ordinary X')
            results.append({'J_alias': 'X', 'reason': 'ordinary_X_has_five_distinct_contacts', 'contacts': sorted(adj['X'])})
            continue
        need(adj['A'] == {'U', 'V', 'Z', 'N'}, 'exact four contacts at A')
        need(adj['Z'] == {'F', 'S', 'A', 'N'}, 'exact four contacts at Z')
        need(adj['V'] == {'F', 'A', 'B'}, 'complete three contacts at V')
        candidates = []
        exclusions = {}
        for p in sorted(adj['A'] - {'U'}):
            if p == 'V' and 'C' not in adj['V']:
                exclusions[p] = 'complete_degree_three_V_cannot_contact_C'
            elif p == 'Z' and 'C' not in adj['Z']:
                exclusions[p] = 'complete_degree_four_Z_cannot_contact_C'
            else:
                candidates.append(p)
        need(candidates == ['N'], 'U-A-C Q opposite is forced to be J')
        results.append({'J_alias': 'N', 'A_contacts': sorted(adj['A']), 'Z_contacts': sorted(adj['Z']),
                        'U_A_C_opposite_candidates': candidates, 'excluded_candidates': exclusions,
                        'forced_Q': ['U', 'A', 'N', 'C'],
                        'endpoint_second_T_contains_zero_C': True})
    return results


def gj_stars(tg=4, saturated=('A', 'S', 'Z')):
    required = {edge('F', 'X'), edge('F', 'S'), edge('Z', 'A')}
    out = []
    for p in permutations(('X', 'S', 'Z', 'A')):
        cycle = ('F',) + p
        pairs = [edge(cycle[i], cycle[(i+1) % 5]) for i in range(5)]
        for t in combinations(range(5), tg):
            triangles = {pairs[i] for i in t}
            if not required <= triangles:
                continue
            extra = sorted(triangles-required)
            overloaded = sorted(set(saturated) & {v for e in extra for v in e})
            out.append({'G_neighbor_cycle': list(cycle),
                        'Q_sectors': sorted(e for e in pairs if e not in triangles),
                        'additional_T_sectors': [list(e) for e in extra],
                        'overloaded_original_vertices': overloaded})
    return sorted(out, key=lambda x: (x['G_neighbor_cycle'], x['Q_sectors']))


def imported_rows():
    root = Path(__file__).resolve().parent
    deps = json.loads((root/'DEPENDENCIES.json').read_text())['files']
    for name, record in deps.items():
        need(hashlib.sha256((root.parent/name).read_bytes()).hexdigest() == record['sha256'], 'public dependency hash: '+name)
    prior = json.loads((root.parent/'tammes15_two_deficient_fives_fan_exclusion/EXPECTED.json').read_text())['catalogue_corollary']
    rows = prior['remaining_beta_profiles']
    need(prior['counts_r1_r2_r3'] == [0, 11, 11] and len(rows) == 22, 'preceding published 22-row necessary catalogue')
    removed = [r for r in rows if (r['r'], r['a'], r['b'], *r['five_counts_f0_f1_f2']) == (2, 1, 2, 1, 1, 0)]
    need(len(removed) == 1, 'precise new row occurs once')
    remaining = [r for r in rows if r not in removed]
    need(len(remaining) == 21 and [sum(r['r'] == n for r in remaining) for n in (1, 2, 3)] == [0, 10, 11], '21 necessary beta rows')
    return {'newly_excluded_row': removed[0], 'remaining_beta_profiles': remaining,
            'counts_r1_r2_r3': [0, 10, 11],
            'remaining_profile_sha256': hashlib.sha256(json.dumps(remaining, separators=(',', ':')).encode()).hexdigest(),
            'prior_catalogue_imported_not_regenerated': True,
            'guarded_dependency_sha256': {p: v['sha256'] for p, v in deps.items()}}


def main():
    families = neighbor_families()
    need(len(families) == 6, 'all six ordered families')
    bc, ab = fan_roles('BC'), fan_roles('AB')
    need(not any(x['reason'] == 'RELAXED_survivor' for x in bc), 'FBC fan contradiction complete')
    need(sum(x['reason'] == 'RETAINED_G_at_R' for x in ab) == 1, 'FAB forces exactly A outside and G at R')
    stars = gj_stars()
    need(len(stars) == 8 and all(x['overloaded_original_vertices'] for x in stars), 'all eight raw G=J stars excluded')
    # Meaningful controls relax only the indicated necessary condition.
    relaxed = gj_stars(tg=3)
    need(len(relaxed) == 4 and all(not x['overloaded_original_vertices'] for x in relaxed), 'three-T G role allows a nonempty star population')
    allow_a = [x for x in gj_stars(saturated=('S', 'Z')) if not x['overloaded_original_vertices']]
    allow_z = [x for x in gj_stars(saturated=('A', 'S')) if not x['overloaded_original_vertices']]
    need(len(allow_a) == len(allow_z) == 2, 'A/Z saturation controls reopen stars')
    relaxed_bc = [x for x in fan_roles('BC', independence=False) if x['reason'] == 'RELAXED_survivor']
    need({'A_position': 0, 'G_position': 2, 'reason': 'RELAXED_survivor'} in relaxed_bc, 'U-neighbor independence control')
    need(len(neighbor_families(repeat_allowed=True)) == 7, 'repeated ABC control')
    need(len(neighbor_families(f_capacity=2)) == 12, 'F at most one three control')
    margin = [Q(1, 2), Q(7, 20), Q(4, 25)]
    need(all(x > 0 for x in margin), 'credited y>pi-alpha exact numerator margin on [1/2,3/5]')
    return {'agent': 'six-tammes-1', 'role': 'researcher',
            'status': 'conditional hand proof plus exact local checks; independent mathematical review pending',
            'scope': 'complete connected degree3..5 simple strictly convex hemispherical cellular T/Q contact graph, N15 and nine Qs',
            'new_row_interval': 'FULL OPEN 1/2<c<3/5; no beta/H premise',
            'ordered_neighbor_families': families,
            'fan_cases': {'FBC': bc, 'FAB': ab, 'FAC': 'exact role exchange B<->C of FAB'},
            'ordinary_J_aliases_and_Q_forcing': ordinary_j(),
            'ordinary_J_endpoint_links': endpoint_links(),
            'G_equals_J_all_eight_star_obstructions': stars,
            'credited_1_plus_c_minus_4c_squared_Bernstein': list(map(str, margin)),
            'controls': {'three_T_G_stars': relaxed, 'unsaturated_A_stars': allow_a, 'unsaturated_Z_stars': allow_z,
                         'without_U_neighbor_independence_fan_survivors': relaxed_bc,
                         'repeated_neighbor_family_count': 7, 'relaxed_F_capacity_neighbor_family_count': 12,
                         'controls_are_relaxed_necessary_role_assignments_not_packings': True},
            'catalogue_corollary': imported_rows(),
            'written_geometric_and_face_point_bridges_unformalized': True,
            'global_numerical_Tammes15_bound_unchanged': True}


if __name__ == '__main__':
    print(json.dumps(main(), sort_keys=True, indent=2))
