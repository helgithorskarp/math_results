#!/usr/bin/env python3
"""Exact finite hypotheses for COUPLED_NONWINNING_PROOF.md.

Python 3.11+ standard library. All original circle heights, complete
cyclic-shift obstructions, individual moving-support gaps, proper source
alignments, complete torque hulls and full winning-source Bernstein trees
are regenerated. Continuous geometric bridges and the inherited winning
receiving theorem remain written proof dependencies. Global RID is OPEN.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F
from itertools import combinations

from verify import PHI, QPhi, ZERO, act, dot, require, symmetry_group, vertices
from cell_certificate import decode, encode
from torque_certificate import cross, subtract
from linear_roll_certificate import exact_hull, project
from global_cap_certificate import canonical, expect_rejection
from adaptive_receiver_certificate import rational_strings, verify_root
from threshold_receiver_certificate import (
    BETA, I, REFS, active_balance, exact_rotations, facet_coefficients,
    hull_data, root, source_coordinates, threefold_source, validate_proper)
from contact_collar_certificate import (
    LOW, complete_contacts, torque_hull, validate_probe, validate_vertices)
import actual_torque_hull_certificate as parent
import beta_cap_certificate as beta
import winning_receiver_certificate as winning

EPSILON = F(1, 150)
CAP = F(1, 162)
Q = F(449, 1000)
GAMMA = F(1, 16)
FULL_ANGLE = F(1, 16)
MAX_DEPTH = 8
WIDER_WINNING_SHA = '2c586997ef577d18893ebb51dd23a6fc70954dae4c329451380931d93c49a4ec'


def field_decode(x):
    return QPhi(F(x[0]), F(x[1]))


def scalar_bounds(epsilon=EPSILON, cap=CAP, q=Q,
                  candidate_distance=F(37, 200), matching_distance=F(1, 5),
                  roll_chord=F(1, 22), full_angle=FULL_ANGLE):
    require(epsilon > 0 and 0 < cap < F(1, 10) and q > 0 and
            candidate_distance > 0 and matching_distance > 0 and
            0 < roll_chord < F(1, 10) and full_angle > 0,
            'positive band, chord, distance and full-angle bounds')
    source_chord = F(25, 27) * epsilon
    eta = F(23, 50) * cap + F(9, 4) * cap * cap
    loss = epsilon + 9 * eta
    a_win = F(101, 300) * (F(289, 500) - q)
    eta_win = F(289, 500) * a_win + F(9, 4) * a_win * a_win
    eta_target = F(9, 2) * cap + F(9, 4) * cap * cap
    angle = F(101, 100) * (roll_chord + 2 * cap)
    checks = {
        'cutoff_exceeds_q_squared': BETA - QPhi(epsilon) > QPhi(q*q),
        'cutoff_exceeds_remaining366region_maximum': BETA - QPhi(epsilon) > QPhi(F(1, 7)),
        'reference_beta_height_exceeds57over125': BETA > QPhi(F(57, 125)**2),
        'source_receiver_height_sum_exceeds9over10': F(57, 125) + q > F(9, 10),
        'both_threshold_tangent_disks_exceed9over5': (39+37*PHI)/29 > QPhi(F(9, 5)**2),
        'sqrt2_upper3over2': 2 < F(3, 2)**2,
        'source_receiver_coercivity_multiplier': F(3, 2)/F(9, 5)*F(10, 9) == F(25, 27),
        'both_threshold_coercivity_chords_inside_cap': source_chord <= cap,
        'body_radius_upper9over2': 7+8*PHI < QPhi(F(9, 2)**2),
        'circle_reference_height_upper23over50': BETA < QPhi(F(23, 50)**2),
        'circle_radius_exceeds22over5': 7+8*PHI-BETA > QPhi(F(22, 5)**2),
        'transported_original_circle_radius_positive': F(22, 5)-eta > 0,
        'candidate_original_height_below_one_half': BETA+QPhi(9*eta) < QPhi(F(1, 4)),
        'all_other52_moving_original_heights_above_one_half': F(3, 5)-F(9, 2)*cap > F(1, 2),
        'original_candidate_distance_squared_clears_loss': candidate_distance**2 > loss,
        'eight_distinct_source_originals_cannot_share_a_candidate': F(3, 2)-2*eta > 2*candidate_distance,
        'reference_circle_matching_distance_clears_both_transports': candidate_distance+2*eta < matching_distance,
        'reference_circle_matching_arcs_disjoint': 2*matching_distance < F(3, 2),
        'forbidden_cyclic_shift_pair_gap_clears_matching_errors': 5 > 2*matching_distance,
        'surviving_circle_roll_chord': matching_distance/F(22, 5) <= roll_chord,
        'small_chord_to_full_angle_multiplier': F(101, 100)**2*(1-F(1, 400)) > 1,
        'all_three_full_rotation_angles_below_local_bound': angle < full_angle,
        'winning_c0_upper': QPhi(F(1, 3)) < QPhi(F(289, 500)**2),
        'winning_tangent_disk_exceeds3': QPhi(F(8, 3))+4*PHI > QPhi(9),
        'winning_source_sine_below_one_twentieth': (F(289, 500)-q)/3 < F(1, 20),
        'winning_acute_cosine_exceeds499over500': 1-((F(289, 500)-q)/3)**2 > F(499, 500)**2,
        'winning_chord_over_sine_multiplier': F(101, 100)**2*(1+F(499, 500))/2 > 1,
        'winning_source_normal_chord_below_one_tenth': 0 < a_win < F(1, 10),
        'fresh_reference_winning_source_margin_clears_both_transports': GAMMA-eta_win-eta_target > F(1, 200),
    }
    require(all(checks.values()), 'unsupported coupled band, correspondence, roll or winning-source margin')
    return rational_strings({
        'global_receiver_squared_height_slack': epsilon,
        'receiving_and_source_height_strict_lower': q,
        'both_threshold_normal_chord_strict_upper': source_chord,
        'local_closed_receiver_cap': cap,
        'both_original_circle_transport_strict_upper': eta,
        'source_to_candidate_squared_distance_strict_upper': loss,
        'source_to_original_candidate_distance_strict_upper': candidate_distance,
        'reference_eight_circle_matching_distance_strict_upper': matching_distance,
        'proper_roll_chord_after_moving_halfturn_strict_upper': roll_chord,
        'full_original_near_branch_angle_strict_upper': angle,
        'local_full_rotation_angle_upper': full_angle,
        'winning_source_normal_chord_strict_upper': a_win,
        'winning_source_original_corner_transport_strict_upper': eta_win,
        'whole_original_receiver_transport_strict_upper': eta_target,
        'whole_winning_source_reference_unit_support_gap_strict_lower': GAMMA,
        'winning_source_actual_unit_support_margin_strict_lower': GAMMA-eta_win-eta_target,
        'equivalent_receiving_squared_diameter_added_strict_lower': 4*epsilon,
        'checks': checks})


def validate_circle_order(n, circle, ordered):
    require(len(circle) == len(ordered) == len(set(ordered)) == 8 and
            set(ordered) == circle, 'every original circle point occurs once in the complete cyclic order')
    radius = 7+8*PHI-BETA
    require(all(dot(p, n) == ZERO and dot(p, p) == radius for p in ordered),
            'actual reference plane and common exact original circle radius')
    for p, q in zip(ordered, ordered[1:]+ordered[:1]):
        m = cross(subtract(q, p), n)
        h = dot(m, p)
        require(h > 0 and all(dot(m, x) <= h for x in ordered),
                'complete positive oriented circle-polygon sides, including cyclic seam')
    require(all(ordered[(j+4) % 8] == tuple(-x for x in ordered[j]) for j in range(8)),
            'the fourth cyclic shift is exactly the planar half-turn')


def shift_witnesses(ordered):
    distances = {}
    for i, j in combinations(range(8), 2):
        d = subtract(ordered[i], ordered[j])
        distances[i, j] = (dot(d, d), root(dot(d, d)))
    records = []
    for shift in (1, 2, 3, 5, 6, 7):
        candidates = []
        for (i, j), (sq, bracket) in distances.items():
            a, b = sorted(((i+shift) % 8, (j+shift) % 8))
            shifted_sq, shifted_bracket = distances[a, b]
            lower = max(bracket.lo-shifted_bracket.hi, shifted_bracket.lo-bracket.hi)
            candidates.append((lower, -i, -j, [i, j], [a, b], sq, shifted_sq))
        lower, _, _, pair, moved, sq, shifted_sq = max(candidates)
        records.append({'shift': shift, 'pair': pair, 'shifted_pair': moved,
                        'first_squared_length': sq.encode(),
                        'shifted_squared_length': shifted_sq.encode(),
                        'strict_pair_length_difference_lower': str(lower)})
    return records


def validate_shift_witnesses(ordered, records, gap=F(5)):
    require(len(records) == 6 and [r['shift'] for r in records] == [1, 2, 3, 5, 6, 7],
            'all six forbidden cyclic shifts and no omitted shift')
    require(gap > 0, 'positive forbidden-shift gap')
    for r in records:
        i, j = r['pair'];s = r['shift']
        require(0 <= i < j < 8, 'actual distinct circle pair')
        moved = sorted(((i+s) % 8, (j+s) % 8))
        require(r['shifted_pair'] == moved, 'actual cyclic-shift correspondence')
        a, b = moved
        d, e = subtract(ordered[i], ordered[j]), subtract(ordered[a], ordered[b])
        first, second = dot(d, d), dot(e, e)
        require(first.encode() == r['first_squared_length'] and second.encode() == r['shifted_squared_length'],
                'both original chord lengths reconstructed exactly')
        x, y = root(first), root(second)
        lower = max(x.lo-y.hi, y.lo-x.hi)
        require(F(r['strict_pair_length_difference_lower']) == lower and lower > gap,
                'both validated square-root brackets prove the forbidden cyclic shift')


def circle_geometry(n, V):
    validate_vertices(V)
    N = dot(n, n)
    S, H, normals, _, _, circle = hull_data(n, V)
    ordered = exact_hull(circle, n)
    validate_circle_order(n, circle, ordered)
    original = [next(v for v in sorted(V) if project(v, n) == p) for p in ordered]
    require(len(set(original)) == 8 and all(dot(v, n)**2/N == BETA for v in original),
            'eight distinct actual original circle preimages with exact beta heights')
    others = sorted(V-set(original))
    require(len(others) == 52 and all(dot(v, n)**2/N > QPhi(F(3, 5)**2) for v in others),
            'all52 other original heights are strictly above3over5')
    heights = [{'original': encode(v), 'squared_height': (dot(v, n)**2/N).encode()} for v in others]
    height_counts = {}
    for h in heights:
        value = field_decode(h['squared_height'])
        height_counts[value] = height_counts.get(value, 0)+1
    height_raw = json.dumps(heights, sort_keys=True, separators=(',', ':')).encode()
    pairs = []
    for i, j in combinations(range(8), 2):
        d = subtract(ordered[i], ordered[j]);sq = dot(d, d)
        require(sq > QPhi(F(3, 2)**2), 'all28 distinct reference circle pairs exceed3over2')
        pairs.append({'pair': [i, j], 'squared_distance': sq.encode()})
    pair_raw = json.dumps(pairs, sort_keys=True, separators=(',', ':')).encode()
    shifts = shift_witnesses(ordered);validate_shift_witnesses(ordered, shifts)
    record = {
        'full_original_projections': len(S), 'full_receiving_hull_corners': len(H),
        'all8ordered_original_circle_preimages': [encode(v) for v in original],
        'full8ordered_original_circle_projections': [encode(p) for p in ordered],
        'all52_non_circle_original_squared_heights_checked': len(heights),
        'non_circle_original_squared_height_distribution': [
            {'squared_height': h.encode(), 'original_vertices': count}
            for h, count in sorted(height_counts.items())],
        'full52_original_height_record_sha256': hashlib.sha256(height_raw).hexdigest(),
        'minimum_non_circle_original_squared_height': min(field_decode(h['squared_height']) for h in heights).encode(),
        'all28_reference_circle_pair_squared_distances_checked': len(pairs),
        'full28_original_circle_pair_record_sha256': hashlib.sha256(pair_raw).hexdigest(),
        'complete_six_cyclic_shift_obstructions': shifts,
        'exact_remaining_shifts': [0, 4],
        'minimum_reference_circle_pair_squared_distance': min(field_decode(a['squared_distance']) for a in pairs).encode(),
    }
    return record, ordered, original, H


def moving_support_certificate(n, V, probes, expected_probes, cap=CAP):
    require(cap > 0 and probes == expected_probes and len(probes) == len(set(probes)) == 16,
            'complete original sixteen-contact support list and positive cap')
    N = dot(n, n);records = [];positive = [];zeros = 0
    for j, (w, e) in enumerate(probes):
        validate_probe(n, V, w, e)
        for v in sorted(V):
            a = cross(subtract(w, v), e);g = dot(n, a)
            require(g >= 0, 'oriented original receiving support')
            if g == ZERO:
                require(a == (ZERO, ZERO, ZERO), 'every tied support identity persists for all actual normals')
                zeros += 1
                records.append([j, encode(v), 'identically_zero'])
                continue
            squared = g*g/(N*dot(a, a))
            require(squared > QPhi(cap*cap), 'individual original positive support clears the whole closed cap')
            positive.append(squared)
            records.append([j, encode(v), g.encode(), dot(a, a).encode(), squared.encode()])
    require(len(records) == 960 and len(positive) == 928 and zeros == 32,
            'all960 original sides,928 positive gaps and32 persistent ties')
    raw = json.dumps(records, sort_keys=True, separators=(',', ':')).encode()
    return {
        'all_actual_original_support_comparisons': len(records),
        'strict_positive_original_supports': len(positive), 'identically_persistent_original_ties': zeros,
        'closed_unit_receiving_chord_cap': str(cap),
        'minimum_squared_unit_distance_to_positive_gap_plane': min(positive).encode(),
        'all_generated_original_support_records_sha256': hashlib.sha256(raw).hexdigest(),
        'all16actual_original_receiving_probes': [[encode(w), encode(e)] for w, e in probes]}


def local_rotation_bounds(n, rho, ray_upper, cap=CAP, angle=FULL_ANGLE):
    require(cap > 0 and angle > 0 and rho > 0 and ray_upper > 0,
            'positive local geometric bounds')
    require(dot(n, n) < QPhi(ray_upper*ray_upper), 'actual reference norm bound')
    ball = rho/(ray_upper*F(9, 2))-2*cap
    require(ball > angle, 'whole moving normalized torque ball clears the FULL spatial angle')
    return rational_strings({'reference_ray_norm_strict_upper': ray_upper,
        'raw_reference_torque_ball_radius_strict_lower': rho,
        'common_original_contact_normalization': F(9, 2),
        'normalized_torque_movement_Lipschitz_upper': F(2),
        'uniform_moving_normalized_torque_ball_strict_lower': ball,
        'full_original_relative_rotation_angle_upper': angle,
        'strict_normalized_rotation_margin': ball-angle})


def dyadic_interval(path):
    require(all(c in '01' for c in path), 'binary closed midpoint path')
    lo, hi = F(0), F(1)
    for c in path:
        mid = (lo+hi)/2
        if c == '0':hi = mid
        else:lo = mid
    return lo, hi


def validate_closed_tree(leaves, coefficient_count=192):
    require(coefficient_count == 192 and leaves, 'all16actual facets times12actual original corners')
    keys = [(q, word) for q, word, k in leaves]
    require(len(keys) == len(set(keys)) and all(0 <= q < 4 and
            all(c in '01' for c in word) and 0 <= k < coefficient_count for q, word, k in leaves),
            'unique valid closed leaf, actual quarter, binary path and original witness')
    total_nodes = 0
    for quarter in range(4):
        words = {word for q, word, k in leaves if q == quarter}
        require(words, 'every whole CLOSED circle quarter is present')
        visited = set()
        def visit(word):
            nonlocal total_nodes
            total_nodes += 1
            if word in words:
                require(not any(w.startswith(word) and w != word for w in words),
                        'no leaf may contain another leaf')
                visited.add(word)
                return
            require(any(w.startswith(word+'0') for w in words) and
                    any(w.startswith(word+'1') for w in words),
                    'every internal closed midpoint node has BOTH children')
            visit(word+'0');visit(word+'1')
        visit('')
        require(visited == words, 'all given leaves belong to the complete root tree')
    return total_nodes


def replay_winning_cover(leaves, coefficients, gamma=GAMMA):
    validate_closed_tree(leaves, len(coefficients))
    quarters = [beta.quarter_coefficients(coefficients, q) for q in range(4)]
    records = []
    for q, word, index in leaves:
        lo, hi = dyadic_interval(word)
        beta.verify_bernstein_identity(lo, hi)
        bounds = beta.lower_coefficients(quarters[q][index], lo, hi, gamma)
        require(min(bounds) > 0, 'all three actual Bernstein coefficients on every closed leaf')
        records.append([q, word, index, str(lo), str(hi), [str(x) for x in bounds]])
    raw = json.dumps(records, sort_keys=True, separators=(',', ':')).encode()
    return {'selected_actual_Bernstein_coefficients': 3*len(records),
            'minimum_selected_actual_Bernstein_coefficient': str(min(F(x) for r in records for x in r[-1])),
            'complete_selected_coefficient_record_sha256': hashlib.sha256(raw).hexdigest()}


def whole_winning_cover(H, n, source_coordinates_record, gamma=GAMMA):
    coefficients = facet_coefficients(H, n, source_coordinates_record)
    require(len(coefficients) == 192, 'complete16 by12 physical facet and original-corner coefficients')
    quarters = [beta.quarter_coefficients(coefficients, q) for q in range(4)]
    leaves = [];nodes = 0;checks = 0
    def visit(q, path, lo, hi):
        nonlocal nodes, checks
        nodes += 1
        scores = []
        for k, c in enumerate(quarters[q]):
            scores.append((min(beta.lower_coefficients(c, lo, hi, gamma)), -k));checks += 1
        value, negative_index = max(scores)
        if value > 0:
            leaves.append([q, path, -negative_index])
            return
        require(len(path) < MAX_DEPTH, 'incomplete depth-bounded cover; not a nonexistence result')
        mid = (lo+hi)/2
        visit(q, path+'0', lo, mid);visit(q, path+'1', mid, hi)
    for q in range(4):visit(q, '', F(0), F(1))
    require(validate_closed_tree(leaves) == nodes, 'generated complete tree node count')
    replay = replay_winning_cover(leaves, coefficients, gamma)
    return {'whole_closed_quarter_roots': 4, 'whole_tree_nodes': nodes,
            'whole_closed_leaves': len(leaves), 'maximum_depth': max(len(p) for q, p, k in leaves),
            'actual_unit_reference_support_gap_strict_lower': str(gamma),
            'complete_original_facet_corner_coefficients': len(coefficients),
            'all_candidate_node_witnesses_considered': checks,
            'all_compact_closed_leaf_witnesses': leaves,
            'full_generated_prefix_tree_replayed': True, **replay}, coefficients


def check(self_test=False):
    V = vertices();validate_vertices(V)
    G = symmetry_group(V, return_matrices=True)
    global_data = parent.fixture('global_cap_expected.json', beta.GLOBAL_SHA)
    threshold = parent.fixture('threshold_receiver_expected.json', beta.THRESHOLD_SHA)
    win = parent.fixture('winning_receiver_expected.json', beta.WINNING_SHA)
    collar = parent.fixture('contact_collar_expected.json', beta.COLLAR_SHA)
    wider = parent.fixture('wider_winning_band_expected.json', WIDER_WINNING_SHA)
    require(wider['winning_receiver_squared_height_slack'] == '1/150' and
            wider['closed_containment_on_all_winning_receivers_with_f_squared_ge_beta_minus_one150'] ==
            'iff lambda=1,t=0,Q in G union J_n G',
            'inherited complete winning receiving-domain theorem at the same exact cutoff')
    scores = global_data['diameter_and_sign_regions']['score_counts']
    values = [field_decode(x['score']) for x in scores]
    require(sum(x['regions'] for x in scores) == 436 and
            sum(x['regions'] for x, v in zip(scores, values) if v == QPhi(F(1, 3))) == 10 and
            sum(x['regions'] for x, v in zip(scores, values) if v == BETA) == 60 and
            max(v for v in values if v not in {BETA, QPhi(F(1, 3))}) == QPhi(F(1, 7)),
            'complete inherited source/receiver signed-region spectrum')
    axes = {'body_projective_orbits': [{'representative_balance': active_balance(n, V)} for n in REFS]}
    R, C, rotations = exact_rotations(G, axes)
    rays = {canonical(act(g, n)) for n in REFS for g in G}
    pinned = {canonical(decode(z['direction'])) for z in
              threshold['threshold_axis_classification']['all_sixty_axes_and_regions']}
    require(len(G) == len(rays) == 60 and rays == pinned,
            'all60 actual proper body rotations and all60 complete threshold axes')
    for n in REFS:
        directed = {act(g, n) for g in G}
        require(len(directed) == 60 and all(tuple(-x for x in r) in directed for r in directed),
                'all directed source/receiving threshold gauges including normal reversal')
    require(cross(LOW, REFS[0]) == (ZERO, ZERO, ZERO) and dot(LOW, REFS[0]) > 0,
            'identical directed lower raw reference')
    bound_record = scalar_bounds()
    hexagon, _, _ = winning.active_hexagon()
    require(hexagon == win['complete_positive_active_tangent_hexagon'],
            'full winning-source positive tangent hexagon regenerated')
    B, H0, source_record = threefold_source(V, win)
    require(source_record == threshold['threefold_original_source_corner_bounds'],
            'all12 actual original winning-reference corner preimages regenerated')
    reference_source_record = {
        'original_reference_corner_count': source_record['complete_center_corner_count'],
        'all_original_reference_support_comparisons': source_record['all_original_source_support_comparisons'],
        'actual_unique_original_reference_corner_preimages': source_record['actual_unique_original_corner_preimages'],
        'complete_original_reference_hull': source_record['complete_center_hull'],
        'reference_original_axial_height_squared': ['1/3', '0'],
        'old_source_record_entrywise_matches_parent': True,
        'historical1over24source_chord_and_error_are_NOT_new_proof_inputs': True,
    }
    source_coords = source_coordinates(H0, B)
    geometries = [];saved = [];covers = [];references = [LOW, REFS[1]]
    for j, (n, rho, ray_bound) in enumerate([(LOW, F(7, 20), F(51, 50)),
                                           (REFS[1], F(9, 20), F(11, 10))]):
        circle_record, ordered, originals, H = circle_geometry(n, V)
        original_contact, probes, T, gap = complete_contacts(n, V, I)
        supports = moving_support_certificate(n, V, probes, probes)
        torque = torque_hull(T, rho)
        require(torque == collar['explicit_local_contact_caps'][j]['complete_center_torque_hull'],
                'every regenerated reference torque facet and affine-rank entry matches the published parent')
        local = local_rotation_bounds(n, rho, ray_bound)
        cover, coeff = whole_winning_cover(H, n, source_coords);covers.append(cover)
        geometries.append({'receiver_class': j, 'raw_reference': encode(n),
            'complete_original_circle_geometry': circle_record,
            'complete_individual_original_support_cap': supports,
            'complete_regenerated_reference_torque_hull': torque,
            'whole_cap_full_rotation_bounds': local})
        saved.append((n, ordered, originals, H, probes, T, coeff, rho, ray_bound))
    alignments = []
    ordered_vertices = sorted(V)
    for si, ns in enumerate(references):
        for ti, nt in enumerate(references):
            D = I if si == ti else R
            source_originals = set(saved[si][2]);target_originals = set(saved[ti][2])
            require({act(D, v) for v in source_originals} == target_originals and
                    {act(D, p) for p in saved[si][1]} == set(saved[ti][1]),
                    'all8 actual spatial preimages and projected original circle points align properly')
            contact, probes, T, gap = complete_contacts(nt, V, D)
            require(probes == saved[ti][4] and T == saved[ti][5],
                    'all16 receiving contacts and torques persist in every proper source branch')
            alignments.append({'source_class': si, 'receiving_class': ti,
                'source_alignment': 'I' if si == ti else 'R_beta=C^5',
                'actual_shared_original_vertices': contact['original_shared_vertices'],
                'all8actual_circle_originals_align': True,
                'original_vertex_index_convention': 'zero_based_lexicographic_exact_coordinate_order',
                'all16actual_original_source_contact_preimage_indices':
                    [ordered_vertices.index(decode(r['original_source']))
                     for r in contact['actual_contact_records']]})
    rejected = 0
    if self_test:
        n, ordered, originals, H, probes, T, coeff, rho, ray_bound = saved[0]
        shifts = geometries[0]['complete_original_circle_geometry']['complete_six_cyclic_shift_obstructions']
        leaves = covers[0]['all_compact_closed_leaf_witnesses']
        corrupt_shift = json.loads(json.dumps(shifts));corrupt_shift[0]['shifted_pair'] = [0, 1]
        if corrupt_shift[0]['shifted_pair'] == shifts[0]['shifted_pair']:
            corrupt_shift[0]['shifted_pair'] = [1, 2]
        invalid_leaf = [list(x) for x in leaves];invalid_leaf[0][2] = 192
        improper = tuple(decode(row) for row in rotations['improper_active_alignment_matrix'])
        w, e = probes[0]
        controls = [
            lambda: circle_geometry(n, V-{min(V)}),
            lambda: circle_geometry(B, V),
            lambda: validate_circle_order(n, set(ordered), ordered[:-1]),
            lambda: validate_circle_order(n, set(ordered), list(reversed(ordered))),
            lambda: validate_shift_witnesses(ordered, shifts[:-1]),
            lambda: validate_shift_witnesses(ordered, shifts+[shifts[0]]),
            lambda: validate_shift_witnesses(ordered, corrupt_shift),
            lambda: validate_shift_witnesses(ordered, shifts, gap=F(6)),
            lambda: moving_support_certificate(n, V, probes[:-1], probes),
            lambda: moving_support_certificate(n, V, probes, probes, cap=F(1, 10)),
            lambda: validate_probe(n, V, w, tuple(-x for x in e)),
            lambda: local_rotation_bounds(n, rho, ray_bound, cap=F(1, 25)),
            lambda: local_rotation_bounds(n, rho, ray_bound, angle=F(1, 10)),
            lambda: local_rotation_bounds(n, rho, F(1)),
            lambda: scalar_bounds(epsilon=F(0)),
            lambda: scalar_bounds(epsilon=F(1, 100)),
            lambda: scalar_bounds(cap=F(1, 163)),
            lambda: scalar_bounds(candidate_distance=F(1, 10)),
            lambda: scalar_bounds(matching_distance=F(1, 10)),
            lambda: scalar_bounds(roll_chord=F(1, 23)),
            lambda: scalar_bounds(full_angle=F(1, 20)),
            lambda: validate_closed_tree([x for x in leaves if x[0] != 3]),
            lambda: validate_closed_tree(leaves[:-1]),
            lambda: validate_closed_tree(leaves+[leaves[0]]),
            lambda: validate_closed_tree(invalid_leaf),
            lambda: replay_winning_cover(leaves, coeff, gamma=F(100)),
            lambda: validate_proper(improper),
            lambda: verify_root(QPhi(5), F(3), F(4)),
        ]
        for control in controls:
            expect_rejection(control);rejected += 1
    return {'agent': 'six-rupert-3', 'role': 'researcher',
        'proof_status': 'complete_unformalized_coupled_nonwinning_band_and_explicit_global1over150_receiving_gap',
        'global_RID': 'OPEN', 'global_non_rupert_proved': False,
        'independent_new_result_review_or_formalization_claimed': False,
        'every_strict_passage_necessary_receiving_condition': 'f(n)^2<beta-1/150',
        'equivalent_squared_receiving_diameter_strict_lower': '(736+960phi)/29+2/75',
        'arbitrary_original_proper_Q_full_roll_translation_scale_ge_one_covered': True,
        'unconditional_all_source_chord_caps1over162_proved': False,
        'new_nonwinning_receiver_domain': 'nonwinning signed regions with f(n)^2>=beta-1/150',
        'inherited_winning_receiver_same_cutoff_theorem': 'source a9b869b8f81f5b97eb762497cfd2529fa4cac89e, graph7843',
        'complete_regional_spectrum_used': {'regions': 436, 'winning': 10, 'threshold': 60, 'other': 366, 'other_maximum': ['1/7', '0']},
        'all_new_coupled_original_and_angle_bounds': bound_record,
        'both_threshold_original_geometry_support_and_torque_certificates': geometries,
        'all4proper_source_receiver_original_circle_and_contact_alignments': alignments,
        'both_complete_winning_source_full_roll_Bernstein_trees': covers,
        'full_actual_winning_reference_corner_preimage_geometry_regenerated': reference_source_record,
        'proper_reference_alignment_and36degree_coset': rotations,
        'malformed_mathematical_controls_rejected': rejected,
        'pinned_expected_sha256': {'global': beta.GLOBAL_SHA, 'threshold': beta.THRESHOLD_SHA,
            'winning': beta.WINNING_SHA, 'contact_collar': beta.COLLAR_SHA,
            'wider_winning_band': WIDER_WINNING_SHA},
        'old436region_enumeration_and_wider840case_selftests_replayed': False,
        'new_full_source_rolls_and_individual_original_caps_regenerated': True,
        'floats_solver_private_inputs_or_sampled_continuum_used': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    print(json.dumps(check(args.self_test), sort_keys=True, indent=2))
