#!/usr/bin/env python3
"""Exact finite hypotheses for WIDE_THRESHOLD_SOURCE_PROOF.md.

Python 3.11+ standard library. Regenerate the complete actual receiving
rank cones, all original source-circle preimages and pairs, both tangent
quadrilaterals, and every original receiving height. The continuous
coercivity/transport/support/injection bridges are written in the proof.
This is a source-conditional theorem, not a new global receiving cutoff.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F

from verify import QPhi, PHI, ZERO, dot, vertices, require
from cell_certificate import encode, decode, geometry
from global_cap_certificate import expect_rejection
from adaptive_receiver_certificate import rational_strings
import actual_torque_hull_certificate as hull
import winning_receiver_certificate as winning
import beta_cap_certificate as beta
import global_slack_certificate as parent

ORIGINAL_SHA = 'a4e4fbcdb4f933368a49c3714b666dd0db93d983c93f554eb5771b4842fec8d7'
EPSILON = F(1, 150)
Q = F(449, 1000)
Z_LOWER = F(499, 500)
RECEIVER_CHORD = F(1, 20)
THIRD_FACTOR = F(29, 20)
DISTANCE = F(1, 5)
BETA = (19-8*PHI)/29


def scalar_bounds(epsilon=EPSILON, q=Q, z_lower=Z_LOWER,
                  receiver_chord=RECEIVER_CHORD, third_factor=THIRD_FACTOR,
                  distance=DISTANCE, pair_lower=F(1)):
    require(epsilon > 0 and q > 0 and 0 < z_lower < 1
            and 0 < receiver_chord < F(1, 10) and third_factor > 0
            and distance > 0 and pair_lower > 0,
            'positive source-conditional parameters and acute receiver branch')
    c0_lower, c0_upper, height_upper, R = F(577, 1000), F(289, 500), F(23, 50), F(9, 2)
    sine = (c0_upper-q)/3
    radial = (c0_lower*z_lower-height_upper)/R
    source_chord = F(25, 27)*epsilon
    eta = height_upper*source_chord+(R/2)*source_chord**2
    loss = epsilon+2*R*eta
    excess = F(10, 9)*loss
    third_gap = third_factor*radial
    nonactive_lower = F(5, 4)-R*receiver_chord
    active_lower = c0_lower-R*receiver_chord
    active_upper = c0_upper+R*receiver_chord
    checks = {
        'cutoff_height_strictly_above_q': BETA-QPhi(epsilon) > QPhi(q*q),
        'cutoff_above_complete_remaining366region_barrier': BETA-QPhi(epsilon) > QPhi(F(1, 7)),
        'beta_reference_height_above57over125': BETA > QPhi(F(57, 125)**2),
        'source_coercivity_height_sum_exceeds9over10': F(57, 125)+q > F(9, 10),
        'c0_lower_verified': QPhi(c0_lower*c0_lower) < QPhi(F(1, 3)),
        'c0_upper_verified': QPhi(F(1, 3)) < QPhi(c0_upper*c0_upper),
        'full_winning_tangent_disk_exceeds_three': QPhi(F(8, 3))+4*PHI > QPhi(9),
        'positive_sine_upper_below_one': 0 < sine < 1,
        'acute_cosine_strict_lower': 1-sine*sine > z_lower*z_lower,
        'acute_chord_over_sine_factor': F(101, 100)**2*(1+z_lower)/2 > 1,
        'actual_winning_receiver_chord_bound': F(101, 300)*(c0_upper-q) < receiver_chord,
        'beta_height_upper_verified': BETA < QPhi(height_upper*height_upper),
        'body_radius_strict_upper': 7+8*PHI < QPhi(R*R),
        'all_six_original_active_signs_positive': active_lower > 0,
        'original_active_heights_below_nonactive_heights': active_upper < nonactive_lower,
        'all48nonactive_original_heights_above_one_half':
            F(5, 4)**2 < F(5, 3) and nonactive_lower > F(1, 2),
        'sharp_complete_third_gap_exceeds_new_factor':
            (60-12*PHI)/19 > QPhi(third_factor*third_factor),
        'actual_receiving_tangent_norm_strict_lower_positive': radial > 0,
        'sqrt2_strict_upper': 2 < F(3, 2)**2,
        'both_full_threshold_tangent_disks_exceed9over5':
            (39+37*PHI)/29 > QPhi(F(9, 5)**2),
        'source_coercivity_multiplier_verified': F(3, 2)/F(9, 5)*F(10, 9) == F(25, 27),
        'threshold_source_chord_below_one10': source_chord < F(1, 10),
        'threshold_circle_transport_below3over1000': eta < F(3, 1000),
        'reference_beta_circle_radius_exceeds_four': 7+8*PHI-BETA > QPhi(16),
        'transported_source_radius_positive': 4-eta > 0,
        'candidate_original_receiver_height_below_one_half': BETA+QPhi(9*eta) < QPhi(F(1, 4)),
        'candidate_height_sum_exceeds9over10': F(57, 125)+q > F(9, 10),
        'candidate_height_excess_below_actual_third_gap': excess < third_gap,
        'source_to_chosen_original_squared_distance_bound': loss < distance*distance,
        'actual_source_pairs_cannot_share_a_chosen_original': pair_lower-2*eta > 2*distance,
    }
    require(all(checks.values()), 'unsupported wide threshold-source-only band or injection bounds')
    return rational_strings({
        'source_conditional_receiving_squared_height_slack': epsilon,
        'receiver_axial_height_strict_lower': q,
        'receiver_sine_strict_upper': sine,
        'receiver_acute_cosine_strict_lower': z_lower,
        'receiver_normal_chord_strict_upper': receiver_chord,
        'all_six_active_original_height_strict_lower': active_lower,
        'all_six_active_original_height_strict_upper': active_upper,
        'all48nonactive_original_height_strict_lower': nonactive_lower,
        'complete_third_height_gap_factor_strict_lower': third_factor,
        'receiver_tangent_norm_strict_lower': radial,
        'receiver_third_minus_first_height_strict_lower': third_gap,
        'threshold_source_normal_chord_strict_upper': source_chord,
        'threshold_circle_original_transport_strict_upper': eta,
        'source_to_chosen_receiving_original_squared_distance_strict_upper': loss,
        'candidate_original_height_excess_strict_upper': excess,
        'positive_height_margin': third_gap-excess,
        'source_to_chosen_receiving_original_distance_strict_upper': distance,
        'perturbed_source_pair_distance_strict_lower': 2*distance,
        'candidate_receiving_original_count_upper': 4,
        'source_original_circle_points_count': 8,
        'checks': checks,
    })


def original_receiving_heights(V, B, active):
    require(V == vertices() and B == geometry()[0][0][1],
            'the complete original RID and canonical winning axis')
    N = dot(B, B)
    expected = sorted(v for v in V if dot(v, B) > ZERO and 3*dot(v, B)**2 == N)
    require(active == expected and len(active) == 6,
            'all six distinct original positive active vertices')
    others = sorted(v for v in V if v not in active and tuple(-q for q in v) not in active)
    require(len(others) == 48 and min(dot(v, B)**2/N for v in others) == QPhi(F(5, 3)),
            'all48nonactive originals and sharp axial separation')
    return {
        'complete_original_vertex_count': len(V),
        'positive_original_active_count': len(active),
        'active_original_squared_height': ['1/3', '0'],
        'all48nonactive_original_center_heights': [
            {'original': encode(v), 'squared_height': (dot(v, B)**2/N).encode()}
            for v in others],
        'sharp_nonactive_original_squared_height': ['5/3', '0'],
    }


def strengthen_complete_cones(P, B, record, rays, factor=THIRD_FACTOR):
    require(factor > 0 and record['distinct_oriented_wall_rays'] == 18,
            'positive full18cone gap factor')
    parent.validate_walls(rays, P, B)
    cells = record['all_closed_angular_cones']
    require(len(cells) == 18 and [(c['from_ray'], c['to_ray']) for c in cells]
            == [(i, (i+1) % 18) for i in range(18)],
            'every consecutive closed cone, including the cyclic seam')
    for c in cells:
        parent.validate_cell(P, B, rays[c['from_ray']], rays[c['to_ray']],
                             c['all_six_original_ranks'], QPhi(factor))
    require((60-12*PHI)/19 > QPhi(factor*factor),
            'new uniform factor below the exact complete endpoint minimum')
    return {'whole_closed_cones': len(cells), 'closed_endpoint_rank_checks': 36,
            'every_closed_cone_strong_gap_verified': True,
            'new_third_minus_first_factor_strict_lower': str(factor),
            'complete_parent_wall_rank_record': record}


def check(self_test=False):
    old = hull.fixture('global_slack_expected.json', ORIGINAL_SHA)
    win = hull.fixture('winning_receiver_expected.json', beta.WINNING_SHA)
    cap = hull.fixture('beta_cap_expected.json', parent.BETACAP_SHA)
    spectrum = hull.fixture('global_cap_expected.json', beta.GLOBAL_SHA)
    scores = spectrum['diameter_and_sign_regions']['score_counts']
    values = [QPhi(*z['score']) for z in scores]
    require(sum(z['regions'] for z in scores) == 436
            and sum(z['regions'] for z, v in zip(scores, values) if v == QPhi(F(1, 3))) == 10
            and sum(z['regions'] for z, v in zip(scores, values) if v == BETA) == 60
            and max(v for v in values if v not in {BETA, QPhi(F(1, 3))}) == QPhi(F(1, 7)),
            'pinned complete436region source barrier and winning/threshold families')
    V = vertices()
    hexagon, P, facets = winning.active_hexagon()
    require(hexagon == win['complete_positive_active_tangent_hexagon'],
            'every actual winning active vertex, tangent and facet regenerated')
    B = geometry()[0][0][1]
    active = [decode(v) for v in hexagon['positive_original_active_vertices']]
    heights = original_receiving_heights(V, B, active)
    record, rays = parent.order_cones(P, B)
    require(record == old['complete_winning_angular_order_and_third_height_gap'],
            'every original angular wall, antipode, rank tie and endpoint regenerated')
    stronger = strengthen_complete_cones(P, B, record, rays)
    circles, points = [], []
    for n in beta.REFS:
        circle, projected = parent.circle_geometry(n, V)
        circles.append(circle)
        points.append(projected)
    require(circles == old['both_original_threshold_circle_preimages_and_pair_distances'],
            'all sixteen actual original preimages and all56exact pair distances regenerated')
    disks = [beta.tangent_disk(n, V) for n in beta.REFS]
    require(disks == cap['both_exact_threshold_tangent_quadrilaterals'],
            'both entire actual threshold active quadrilaterals and all eight facets regenerated')
    bounds = scalar_bounds()
    rejected = 0
    if self_test:
        first = record['all_closed_angular_cones'][0]
        u, v = rays[0], rays[1]
        order = first['all_six_original_ranks']
        wrong = order[:]
        wrong[0], wrong[-1] = wrong[-1], wrong[0]
        controls = [
            lambda: scalar_bounds(epsilon=F(1, 100)),
            lambda: scalar_bounds(epsilon=F(0)),
            lambda: scalar_bounds(q=F(23, 50)),
            lambda: scalar_bounds(q=F(2, 5)),
            lambda: scalar_bounds(z_lower=F(9999, 10000)),
            lambda: scalar_bounds(z_lower=F(0)),
            lambda: scalar_bounds(receiver_chord=F(1, 100)),
            lambda: scalar_bounds(receiver_chord=F(1, 5)),
            lambda: scalar_bounds(third_factor=F(3, 2)),
            lambda: scalar_bounds(third_factor=F(1)),
            lambda: scalar_bounds(third_factor=F(0)),
            lambda: scalar_bounds(distance=F(1, 10)),
            lambda: scalar_bounds(distance=F(1, 2)),
            lambda: scalar_bounds(distance=F(0)),
            lambda: scalar_bounds(pair_lower=F(0)),
            lambda: original_receiving_heights(V, B, active[:-1]),
            lambda: original_receiving_heights(V, B, active+active[:1]),
            lambda: original_receiving_heights(V-{next(iter(V))}, B, active),
            lambda: parent.validate_walls(rays[:-1], P, B),
            lambda: parent.validate_walls(list(reversed(rays)), P, B),
            lambda: parent.validate_cell(P, B, u, u, order, QPhi(THIRD_FACTOR)),
            lambda: parent.validate_cell(P, B, u, v, wrong, QPhi(THIRD_FACTOR)),
            lambda: strengthen_complete_cones(P, B, {**record,
                'all_closed_angular_cones': record['all_closed_angular_cones'][:-1]}, rays),
            lambda: strengthen_complete_cones(P, B, record, rays, F(3, 2)),
            lambda: parent.validate_circle(beta.REFS[0], V, points[0][:-1]),
            lambda: parent.validate_circle(beta.REFS[1], V, [(ZERO, ZERO, ZERO)]+points[1][1:]),
        ]
        for control in controls:
            expect_rejection(control)
            rejected += 1
    return {
        'agent': 'six-rupert-3', 'role': 'researcher',
        'proof_status': 'complete_written_unformalized_wide_threshold_source_exclusion',
        'global_RID': 'OPEN', 'global_non_rupert_proved': False,
        'theorem_receivers': 'winning signed regions with f(n)^2>=beta-1/150',
        'excluded_sources': 'both threshold signed-region families and all their proper-body/antipodal images',
        'closed_containment_translation_and_scale_ge_one_excluded': True,
        'all_original_proper_source_rotations_and_full_rolls_covered': True,
        'complete_rank_walls_cones_antipodes_and_ties_covered': True,
        'source_conditional_wider_band_gain_over_global1over450': '3',
        'global_all_receiver_epsilon1over150_proved': False,
        'winning_to_winning_exclusion_proved_by_this_standalone_source_certificate': False,
        'complete_winning_active_hexagon': hexagon,
        'actual_receiving_original_heights': heights,
        'complete_strengthened_angular_rank_certificate': stronger,
        'both_threshold_original_circle_preimages_and_pair_distances': circles,
        'both_threshold_original_tangent_quadrilaterals': disks,
        'all_new_exact_source_conditional_bounds': bounds,
        'new_malformed_controls_rejected': rejected,
        'pinned_parent_expected_sha256': {'original_injection': ORIGINAL_SHA,
            'winning_active_hexagon': beta.WINNING_SHA, 'complete_source_spectrum': beta.GLOBAL_SHA,
            'both_threshold_tangent_disks': parent.BETACAP_SHA},
        'old_global_winning_torque_nonwinning_review_and_full_region_self_tests_replayed': False,
        'new_float_solver_sampled_continuum_or_compactness_input': False,
        'new_independent_review_formalization_or_historical_priority_asserted': False,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    print(json.dumps(check(args.self_test), sort_keys=True, indent=2))
