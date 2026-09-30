#!/usr/bin/env python3
"""Exact hypotheses for WIDER_WINNING_BAND_PROOF.md; Python3.11+stdlib.

Full new torque triangle, stronger whole third-height cones, actual
original-vertex injection and all fifteen body half-turn axes. This
classifies a WINNING receiving band, not a GLOBAL1/150gap.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F

from verify import QPhi, PHI, ZERO, dot, vertices, require, symmetry_group, matmul
from cell_certificate import geometry, encode, decode
from torque_certificate import subtract
from adaptive_receiver_certificate import rational_strings
from global_cap_certificate import expect_rejection
from expanded_global_slack_certificate import actual_supports
import global_slack_certificate as original
import winning_receiver_certificate as winning
import balanced_receiver_certificate as balanced
import beta_cap_certificate as beta
import actual_torque_hull_certificate as hull

ORIGINAL_SHA = 'a4e4fbcdb4f933368a49c3714b666dd0db93d983c93f554eb5771b4842fec8d7'
EPSILON, Q, D = F(1, 150), F(449, 1000), F(1, 23)
THETA, THIRD, RECEIVER_CHORD = F(99, 1000), F(29, 20), F(1, 20)
BETA = (19-8*PHI)/29


def phase_bounds(q=Q, d=D, theta=THETA, radius=F(1, 2)):
    E = (F(13, 15)*d+F(3, 2)*d*d+F(17, 16)*d*d)/(1-d*d/4)
    sine = (F(289, 500)-q)/3
    margin = radius-F(9, 2)*F(27, 25)*theta
    checks = {
        'q_positive_above_two5': q > F(2, 5),
        'q_below_reference_beta_height': QPhi(q*q) < BETA,
        'full_cutoff_exceeds_q': BETA-QPhi(EPSILON) > QPhi(q*q),
        'center_height_upper289over500': QPhi(F(1, 3)) < QPhi(F(289, 500)**2),
        'acute_cosine_lower499over500': 1-sine*sine > F(499, 500)**2,
        'acute_chord_sine_multiplier': F(101, 100)**2*F(999, 1000) > 1,
        'both_full_winning_normal_chords_below_one23': F(101, 300)*(F(289, 500)-q) < d,
        'receiver_envelope_and_factor_chord_domain': 0 < d < F(1, 10),
        'whole_remote_roll_gate': E < F(77, 1000),
        'residual_roll_below_one10': E < F(1, 10),
        'full_perpendicular_axis_angle': F(101, 100)**2*((2*d)**2+E*E) < theta*theta,
        'original_body_radius_upper': 7+8*PHI < QPhi(F(9, 2)**2),
        'original_endpoint_height_upper': QPhi(F(5, 3)) < QPhi(F(13, 10)**2),
        'original_long_support_upper': PHI**3 < QPhi(F(17, 4)),
        'new_torque_remainder_margin_above_one100': margin > F(1, 100),
    }
    require(all(checks.values()), 'unsupported wider winning phase bounds')
    return rational_strings({
        'source_and_receiver_axial_lower': q,
        'source_and_receiver_normal_chord_upper': d,
        'balanced_support_error_upper': E,
        'full_proper_relative_angle_upper': theta,
        'raw_actual_torque_radius': radius,
        'chart_norm_upper': F(27, 25),
        'strict_rotation_margin_lower': margin,
        'checks': checks})


def injection_bounds(epsilon=EPSILON, q=Q, chord=RECEIVER_CHORD,
                     factor=THIRD, distance=F(1, 5), pair=F(1)):
    require(epsilon > 0 and q > 0 and chord > 0 and factor > 0
            and distance > 0 and pair > 0, 'positive injection parameters')
    a = F(25, 27)*epsilon
    eta = F(23, 50)*a+F(9, 4)*a*a
    loss = epsilon+9*eta
    radial = (F(577, 1000)*F(499, 500)-F(23, 50))/F(9, 2)
    third_gap, excess = factor*radial, F(10, 9)*loss
    active_lower = F(577, 1000)-F(9, 2)*chord
    other_lower = F(5, 4)-F(9, 2)*chord
    sine = (F(289, 500)-q)/3
    checks = {
        'claimed_winning_only_slack_not_exceeded': epsilon <= EPSILON,
        'cutoff_height_above449over1000': BETA-QPhi(epsilon) > QPhi(q*q),
        'complete_remaining_region_barrier': BETA-QPhi(epsilon) > QPhi(F(1, 7)),
        'center_height_lower577over1000': F(577, 1000)**2 < F(1, 3),
        'reference_beta_height_above57over125': BETA > QPhi(F(57, 125)**2),
        'source_coercivity_denominator_exceeds9over10': F(57, 125)+q > F(9, 10),
        'reference_beta_height_below23over50': BETA < QPhi(F(23, 50)**2),
        'acute_cosine_lower499over500': 1-sine*sine > F(499, 500)**2,
        'acute_chord_sine_multiplier': F(101, 100)**2*F(999, 1000) > 1,
        'actual_winning_receiver_chord_below_one20': F(101, 300)*(F(289, 500)-q) < chord,
        'receiving_all_active_signs_positive': active_lower > 0,
        'nonactive_center_height_exceeds5over4': F(5, 4)**2 < F(5, 3),
        'actual_nonactive_height_exceeds_one': other_lower > 1,
        'original_radius_below9over2': 7+8*PHI < QPhi(F(9, 2)**2),
        'whole_cone_third_gap_exceeds29over20': (60-12*PHI)/19 > QPhi(factor*factor),
        'tangent_norm_lower_positive': radial > 0,
        'full_threshold_disk_exceeds9over5': (39+37*PHI)/29 > QPhi(F(9, 5)**2),
        'source_sine_chord_multiplier': 2 < F(3, 2)**2,
        'threshold_coercivity_multiplier': F(3, 2)/F(9, 5)*F(10, 9) == F(25, 27),
        'threshold_source_chord_below_one10': a < F(1, 10),
        'circle_radius_exceeds_four': 7+8*PHI-BETA > QPhi(16),
        'transport_error_below3over1000': eta < F(3, 1000),
        'circle_points_nonzero_after_transport': eta < 4,
        'candidate_original_height_below_one2': BETA+QPhi(9*eta) < QPhi(F(1, 4)),
        'candidate_excess_below_uniform_third_gap': excess < third_gap,
        'source_to_chosen_original_distance_below_one5': loss < distance*distance,
        'different_source_points_cannot_share_original': pair-2*eta > 2*distance,
    }
    require(all(checks.values()), 'unsupported wider threshold-source injection bounds')
    return rational_strings({
        'winning_only_squared_height_slack': epsilon,
        'receiving_axial_lower': q, 'receiving_normal_chord_upper': chord,
        'acute_cosine_lower': F(499, 500),
        'all_positive_active_height_strict_lower': active_lower,
        'all_nonactive_absolute_height_strict_lower': other_lower,
        'receiving_tangent_norm_strict_lower': radial,
        'whole_third_minus_first_tangent_gap_factor': factor,
        'third_original_height_gap_strict_lower': third_gap,
        'threshold_source_normal_chord_upper': a,
        'threshold_circle_original_transport_upper': eta,
        'source_to_chosen_original_squared_distance_upper': loss,
        'candidate_original_height_excess_upper': excess,
        'positive_height_margin': third_gap-excess,
        'source_to_chosen_original_distance_strict_upper': distance,
        'source_pair_distance_strict_lower': 2*distance,
        'actual_original_receiving_candidate_limit': 4,
        'actual_original_source_circle_count': 8, 'checks': checks})


def original_heights(V, B, active):
    require(V == vertices(), 'same original RID vertices')
    P = winning.validate_active(V, B, active)
    N = dot(B, B)
    signed = set(active)|{tuple(-x for x in v) for v in active}
    others = sorted(v for v in V if v not in signed)
    require(len(signed) == 12 and len(others) == 48, 'complete original height partition')
    heights = [dot(v, B)**2/N for v in others]
    require(min(heights) == QPhi(F(5, 3)), 'sharp nonactive center height')
    return {
        'all_six_positive_active_originals': [encode(v) for v in active],
        'all48_nonactive_original_center_squared_heights': [
            {'original_vertex': encode(v), 'height_squared': h.encode()}
            for v, h in zip(others, heights)],
        'all_original_vertices_partitioned': True,
        'sharp_nonactive_height_squared': QPhi(F(5, 3)).encode()}, P


def stronger_cones(P, B, old, factor=THIRD):
    record, rays = original.order_cones(P, B)
    require(record == old, 'every original wall/cone/rank record unchanged')
    for c in record['all_closed_angular_cones']:
        original.validate_cell(P, B, rays[c['from_ray']], rays[c['to_ray']],
                               c['all_six_original_ranks'], QPhi(factor))
    return {'full_original_wall_and_closed_cone_record': record,
            'fresh_stronger_gap_factor': str(factor),
            'all18_closed_cones_both_endpoints_freshly_verified': True,
            'all_ties_and_antipodes_covered': True}, rays


def wider_chamber(G, d=D):
    cap = balanced.chamber_cap(G, d)
    A, B, C = geometry()[0][0]
    z0 = F(9, 10)
    drift = d/(z0*(z0-d))
    require(dot(B, B)*QPhi(z0*z0) < QPhi(1)
            and drift < F(1, 10) and B[1]-C[1] > QPhi(F(1, 10)),
            'whole larger winning normal band folds into ABD')
    return rational_strings({'actual_center_and_wall_checks': cap,
                              'center_normal_z_lower': z0,
                              'receiving_normal_z_lower': z0-d,
                              'raw_chart_drift_upper': drift,
                              'all_folded_wider_receivers_in_closed_ABD': True})


def body_halfturns(G, V):
    records = []
    for g in sorted(G):
        if sum((g[i][i] for i in range(3)), ZERO) != QPhi(-1):
            continue
        I = tuple(tuple(QPhi(int(i == j)) for j in range(3)) for i in range(3))
        require(matmul(g, g) == I, 'every selected proper body half-turn is an involution')
        columns = [tuple(g[i][j]+QPhi(int(i == j)) for i in range(3)) for j in range(3)]
        axis = next((c for c in columns if any(x != ZERO for x in c)), None)
        require(axis is not None and dot(axis, axis) > ZERO, 'actual body half-turn axis')
        zeros = sorted(v for v in V if dot(v, axis) == ZERO)
        require(zeros, 'every proper body half-turn axis has an original zero height')
        records.append({'proper_body_halfturn': [encode(row) for row in g],
                        'axis': encode(axis), 'zero_height_original': encode(zeros[0])})
    require(len(records) == 15, 'all fifteen proper body half-turns')
    return {'all15_original_body_halfturn_axes': records,
            'positive_f_excludes_Jn_in_body_group': True,
            'two_disjoint_left_cosets_count': 120}


def band_witness(V, B, u=None):
    if u is None:
        u = (ZERO, QPhi(F(349, 1000)), QPhi(1))
    require(dot(u, u) > ZERO and all(dot(v, u)*dot(v, B) > ZERO for v in V),
            'the actual witness is in the reference winning signed region')
    f2 = min(dot(v, u)**2/dot(u, u) for v in V)
    require(BETA-QPhi(EPSILON) <= f2 < BETA-QPhi(F(1, 450)),
            'actual new receiving band beyond the previous global height cutoff')
    require(f2 < BETA-QPhi(F(1, 445)) and f2 < QPhi(F(909, 2000)**2),
            'the witness remains beyond the independently refined global gap and old winning height domain')
    return {'raw_receiving_ray': encode(u), 'actual_f_squared': f2.encode(),
            'all60_original_signed_heights_verified': True,
            'inside_new_winning_band': True,
            'below_previous_global1over450_height_cutoff': True,
            'below_reviewed_global1over445_height_cutoff': True,
            'below_previous_conditional_winning_q909over2000': True,
            'outside_every_other_prior_receiver_piece_claimed': False}


def check(self_test=False):
    old = hull.fixture('global_slack_expected.json', ORIGINAL_SHA)
    replay = original.check(True)
    raw = (json.dumps(replay, sort_keys=True, indent=2)+'\n').encode()
    require(replay == old and hashlib.sha256(raw).hexdigest() == ORIGINAL_SHA,
            'every original finite injection-parent field regenerated')
    V, B = vertices(), geometry()[0][0][1]
    hexagon, P, _ = winning.active_hexagon()
    active = [decode(v) for v in hexagon['positive_original_active_vertices']]
    heights, P0 = original_heights(V, B, active)
    require(P == P0, 'the actual same positive tangent hexagon')
    cones, rays = stronger_cones(P, B, old['complete_winning_angular_order_and_third_height_gap'])
    circles, circle_points = [], []
    for n in beta.REFS:
        record, points = original.circle_geometry(n, V)
        circles.append(record); circle_points.append(points)
    require(circles == old['both_original_threshold_circle_preimages_and_pair_distances'],
            'every original threshold circle and all56pairs freshly regenerated')
    cap = hull.fixture('beta_cap_expected.json', original.BETACAP_SHA)
    disks = [beta.tangent_disk(n, V) for n in beta.REFS]
    require(disks == cap['both_exact_threshold_tangent_quadrilaterals'],
            'both full threshold coercivity quadrilaterals regenerated')
    phase, injection = phase_bounds(), injection_bounds()
    G = symmetry_group(V, return_matrices=True)
    chamber = wider_chamber(G)
    halfturns = body_halfturns(G, V)
    witness = band_witness(V, B)
    U, cut = winning.cut_triangle(Q)
    outer = rational_strings(winning.outer_geometry(U, H=F(11, 200)))
    adaptive = hull.fixture('adaptive_receiver_expected.json', hull.ADAPTIVE_SHA)
    probes, pool, facets = hull.selected_probes(adaptive)
    center = hull.center_subhull(probes, pool, facets)
    supports = actual_supports(probes, U)
    certificate = hull.certify_hull(probes, U, F(1, 2))
    require(certificate['triple_strata_certified'] == 840
            and certificate['classifications'] == {'opposite': 726, 'distance': 114, 'degenerate': 0}
            and certificate['all_triples_and_closed_boundaries_covered'],
            'new whole wider torque triangle with every relative face')
    rejected = 0
    if self_test:
        first = cones['full_original_wall_and_closed_cone_record']['all_closed_angular_cones'][0]
        order = first['all_six_original_ranks']
        bad = order[:]; bad[0], bad[-1] = bad[-1], bad[0]
        controls = [
            lambda: phase_bounds(q=F(2, 5)),
            lambda: phase_bounds(q=F(57, 125)),
            lambda: phase_bounds(d=F(1, 24)),
            lambda: phase_bounds(d=F(1, 5)),
            lambda: phase_bounds(theta=F(1, 5)),
            lambda: phase_bounds(radius=F(1, 4)),
            lambda: injection_bounds(epsilon=F(1, 100)),
            lambda: injection_bounds(epsilon=F(0)),
            lambda: injection_bounds(q=F(57, 125)),
            lambda: injection_bounds(chord=F(1, 24)),
            lambda: injection_bounds(chord=F(1, 2)),
            lambda: injection_bounds(factor=F(3, 2)),
            lambda: injection_bounds(factor=F(1)),
            lambda: injection_bounds(distance=F(1, 10)),
            lambda: injection_bounds(distance=F(1, 1)),
            lambda: injection_bounds(pair=F(0)),
            lambda: original_heights(V, B, active[:-1]),
            lambda: original.validate_walls(rays[:-1], P, B),
            lambda: original.validate_walls(rays+rays[:1], P, B),
            lambda: original.validate_cell(P, B, rays[0], rays[1], bad, QPhi(THIRD)),
            lambda: stronger_cones(P, B, old['complete_winning_angular_order_and_third_height_gap'], F(2)),
            lambda: original.validate_circle(beta.REFS[0], V, circle_points[0][:-1]),
            lambda: winning.outer_geometry(U, H=F(27, 500)),
            lambda: hull.validate_faces(hull.FACES[:-1]),
            lambda: body_halfturns(set(sorted(G)[:1]), V),
            lambda: band_witness(V, B, B),
        ]
        for control in controls:
            expect_rejection(control); rejected += 1
    return {
        'agent': 'six-rupert-3', 'role': 'researcher',
        'proof_status': 'complete_unformalized_all_source_wider_winning_receiving_band_and_closed_equalities',
        'winning_receiver_squared_height_slack': str(EPSILON),
        'closed_containment_on_all_winning_receivers_with_f_squared_ge_beta_minus_one150':
            'iff lambda=1,t=0,Q in G union J_n G',
        'all_original_proper_Q_full_roll_translation_scale_ge_one_covered': True,
        'global_RID': 'OPEN', 'global_non_rupert_proved': False,
        'global_epsilon1over150_proved': False,
        'nonwinning_receiving_slack_enlarged': False,
        'existing_global1over450_unchanged': True,
        'independently_reviewed_best_committed_global_gap': '1/445',
        'new_global_gap_proof_asserted': False,
        'complete_winning_positive_active_hexagon_regenerated': hexagon,
        'actual_receiving_original_height_facts': heights,
        'full_stronger_original_third_height_cone_certificate': {
            **{k: v for k, v in cones.items() if k != 'full_original_wall_and_closed_cone_record'},
            'every_parent_wall_ray_rank_and_endpoint_compared': True,
            'complete_parent_wall_record_sha256': hashlib.sha256(
                json.dumps(cones['full_original_wall_and_closed_cone_record'],
                           sort_keys=True, separators=(',', ':')).encode()).hexdigest()},
        'both_original_threshold_circle_complete_regeneration_manifests': [
            {'actual_original_preimages': len(c['all8actual_original_circle_preimages']),
             'all_original_pair_distances': len(c['all28actual_circle_pair_distances']),
             'minimum_squared_pair_distance': c['minimum_squared_pair_distance'],
             'every_parent_original_projection_preimage_and_pair_compared': True,
             'complete_original_circle_record_sha256': hashlib.sha256(
                 json.dumps(c, sort_keys=True, separators=(',', ':')).encode()).hexdigest()}
            for c in circles],
        'both_full_threshold_tangent_quadrilaterals': disks,
        'all_new_threshold_source_injection_bounds': injection,
        'all_new_winning_source_phase_bounds': phase,
        'new_larger_proper_chamber_reduction': chamber,
        'new_larger_outer_receiving_cut_triangle': rational_strings(cut),
        'new_larger_outer_geometry': outer,
        'complete_center_torque_hull_regenerated': center,
        'all1800_actual_original_receiving_support_comparisons': supports,
        'full_NEW_wider840strata_torque_certificate': certificate,
        'complete_original_proper_halfturn_and_disjoint_coset_facts': halfturns,
        'exact_actual_new_winning_receiving_band_witness': witness,
        'every_original_finite_parent_field_regenerated': True,
        'original_parent_expected_sha256': ORIGINAL_SHA,
        'original_parent_controls_rejected': replay['new_malformed_controls_rejected'],
        'new_wider_band_controls_rejected': rejected,
        'old_full_region_cap_winning_balanced_and_review_selftests_rerun': False,
        'new_independent_algorithm_review_formalization_or_priority_claimed': False,
    }


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--self-test', action='store_true')
    a = p.parse_args()
    print(json.dumps(check(a.self_test), sort_keys=True, indent=2))
