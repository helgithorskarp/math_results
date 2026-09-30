#!/usr/bin/env python3
"""Exact expanded winning triangle for EXPANDED_GLOBAL_SLACK_PROOF.md.

Python3.11+stdlib. Fully replay the original-point injection parent, pin
the separate published nonwinning review, and regenerate the expanded
actual840strata torque certificate. Written continuous bridges remain.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from verify import QPhi, PHI, ZERO, dot, vertices, require
from torque_certificate import cross, subtract
from adaptive_receiver_certificate import rational_strings
from global_cap_certificate import expect_rejection
import actual_torque_hull_certificate as hull
import winning_receiver_certificate as winning
import global_slack_certificate as original

ORIGINAL_SHA = 'a4e4fbcdb4f933368a49c3714b666dd0db93d983c93f554eb5771b4842fec8d7'
REVIEW_SHA = 'd9814ba3f397cf05387b0727a003e7fe6bf4cf0eedf329077073ef1f8e37168b'
EPSILON = F(1, 450)
Q = F(909, 2000)
BETA = (19-8*PHI)/29


def validate_review_record(data):
    require(data['agent'] == 'six-reviewer-2'
            and data['role'] == 'independent mathematical reviewer',
            'explicit separate published reviewer dependency')
    band = data['proved_refined_transport_and_band']
    require(band['closed_unit_normal_chord_cap'] == '1/480'
            and band['nonwinning_squared_height_slack'] == '1/450'
            and band['nonwinning_band_chord_upper'] == '1/486'
            and band['nonwinning_squared_diameter_slack'] == '2/225'
            and all(band['all_exact_scalar_guards'].values()),
            'complete published refined nonwinning policy')
    require(data['complete_inherited_projective_regions'] == 436
            and data['winning_regions'] == 10 and data['threshold_regions'] == 60
            and data['remaining_regions'] == 366
            and data['remaining_maximum_squared'] == '1/7',
            'complete published source region barrier')
    require(data['numerical_global_epsilon_proved'] is False
            and data['winning_receiving_region_below_beta_quantified'] is False
            and data['global_non_rupert_proved'] is False,
            'the separate review does not audit the numerical global successor')
    return band


def review_input_bytes(raw):
    require(hashlib.sha256(raw).hexdigest() == REVIEW_SHA,
            'published nonwinning review expected bytes changed')
    data = json.loads(raw)
    validate_review_record(data)
    return data


def phase_bounds(q=Q, chord=F(1, 24), raw_radius=F(1, 2), theta=F(47, 500)):
    c0, R, L = F(289, 500), F(9, 2), F(27, 25)
    E = (F(13, 15)*chord + F(3, 2)*chord**2
         + F(17, 16)*chord**2)/(1-chord**2/4)
    margin = raw_radius-R*L*theta
    checks = {
        'positive_q_below_beta_height': q > 0 and QPhi(q*q) < BETA,
        'c0_below_rational_upper': QPhi(F(1, 3)) < QPhi(c0*c0),
        'sine_bound_below_one_twentieth': (c0-q)/3 < F(1, 20),
        'acute_cosine_lower': F(399, 400) > F(199, 200)**2,
        'chord_over_sine_bound': F(101, 100)**2*F(399, 400) > 1,
        'full_source_receiver_chord_bound': F(101, 300)*(c0-q) < chord,
        'all_factor_chords_below_one_tenth': 0 < chord < F(1, 10) and E < F(1, 10),
        'balanced_error_below_complete_roll_threshold': E < F(77, 1000),
        'full_perpendicular_axis_angle_bound': F(101, 100)**2*((2*chord)**2+E*E) < theta*theta,
        'body_radius_upper': 7+8*PHI < QPhi(R*R),
        'receiver_height_upper': F(5, 3) < F(13, 10)**2,
        'reference_support_upper': PHI**3 < QPhi(F(17, 4)),
        'strict_remainder_margin_above_one_twentyfifth': margin > F(1, 25),
    }
    require(all(checks.values()), 'unsupported expanded winning phase bounds')
    return rational_strings({
        'axial_lower': q, 'c0_upper': c0,
        'source_coercivity_chord_coefficient': F(101, 300),
        'source_and_receiver_normal_chord_upper': chord,
        'balanced_support_error_upper': E,
        'full_proper_relative_angle_upper': theta, 'chart_norm_upper': L,
        'actual_torque_ball_radius': raw_radius,
        'strict_torque_remainder_margin_lower': margin, 'checks': checks})


def scalar_bounds(epsilon=EPSILON, q=Q, pair_lower=F(1), distance=F(1, 8)):
    require(epsilon > 0 and pair_lower > 0 and distance > 0,
            'positive height slack, distinct source pairs and injection distance')
    a = F(25, 27)*epsilon
    eta = F(23, 50)*a+F(9, 4)*a*a
    loss = epsilon+9*eta
    radial = (F(577, 1000)*F(199, 200)-F(23, 50))/F(9, 2)
    checks = {
        'epsilon_within_published_review_nonwinning_band': epsilon <= F(1, 450),
        'all_receiving_and_source_height_exceed_expanded_q': BETA-QPhi(epsilon) > QPhi(q*q),
        'remaining366region_barrier': BETA-QPhi(epsilon) > QPhi(F(1, 7)),
        'all_height_lower_above9over20': BETA-QPhi(epsilon) > QPhi(F(9, 20)**2),
        'c0_lower577over1000': F(577, 1000)**2 < F(1, 3),
        'beta_height_upper23over50': BETA < QPhi(F(23, 50)**2),
        'sqrt2_upper3over2': 2 < F(3, 2)**2,
        'full_threshold_disk_radius_above9over5': (39+37*PHI)/29 > QPhi(F(9, 5)**2),
        'source_coercivity_multiplier25over27': F(3, 2)/F(9, 5)*F(10, 9) == F(25, 27),
        'body_radius_below9over2': 7+8*PHI < QPhi(F(9, 2)**2),
        'winning_tangent_displacement_above1over40': radial > F(1, 40),
        'actual_threshold_source_transport_below_one1000': eta < F(1, 1000),
        'reference_beta_circle_radius_exceeds_four': 7+8*PHI-BETA > QPhi(16),
        'candidate_original_receiver_height_below_one_half': BETA+QPhi(9*eta) < QPhi(F(1, 4)),
        'candidate_height_excess_below_third_height_gap': F(10, 9)*loss < F(1, 40),
        'source_to_chosen_receiving_original_distance_bound': loss < distance*distance,
        'source_pairs_cannot_share_chosen_receiving_original': pair_lower-2*eta > 2*distance,
        'all_small_source_normal_chords_below_one10': a < F(1, 10),
        'nonactive_original_receiver_height_above17over16':
            F(5, 4)**2 < F(5, 3)
            and F(5, 4)-F(9, 2)*F(1, 24) == F(17, 16),
    }
    require(all(checks.values()), 'unsupported expanded global slack/injection bounds')
    return rational_strings({
        'numeric_global_axial_squared_slack': epsilon,
        'threshold_source_normal_chord_upper': a,
        'threshold_source_circle_original_transport_upper': eta,
        'source_to_chosen_receiving_original_squared_distance_upper': loss,
        'candidate_original_receiver_height_excess_upper': F(10, 9)*loss,
        'winning_tangent_norm_strict_lower': radial,
        'candidate_receiving_original_count_upper': 4,
        'source_original_circle_points_count': 8,
        'source_to_chosen_receiving_vertex_distance_strict_upper': distance,
        'perturbed_source_pair_distance_strict_lower': 2*distance,
        'checks': checks})


def actual_supports(probes, U):
    require(len(probes) == 10 and len(U) == 3,
            'all actual original probes and all closed receiving corners')
    supports = 0
    for u in U:
        for v, e in probes:
            m = cross(e, u)
            for w in vertices():
                require(dot(m, subtract(v, w)) >= ZERO,
                        'actual original support on whole expanded receiving triangle')
                supports += 1
    require(supports == 1800, 'complete original receiving support cover')
    return supports


def check(self_test=False, review_path=None):
    old = hull.fixture('global_slack_expected.json', ORIGINAL_SHA)
    replay = original.check(True)
    raw = (json.dumps(replay, sort_keys=True, indent=2)+'\n').encode()
    require(replay == old and hashlib.sha256(raw).hexdigest() == ORIGINAL_SHA,
            'every original injection-parent mathematical field regenerated')
    if review_path is None:
        review_path = (Path(__file__).resolve().parent.parent
                       / 'rhombicosidodecahedron_beta_cap_review2' / 'expected.json')
    review = review_input_bytes(Path(review_path).read_bytes())
    phase = phase_bounds()
    bounds = scalar_bounds()
    U, cut = winning.cut_triangle(Q)
    outer = rational_strings(winning.outer_geometry(U))
    adaptive = hull.fixture('adaptive_receiver_expected.json', hull.ADAPTIVE_SHA)
    probes, pool, facets = hull.selected_probes(adaptive)
    center = hull.center_subhull(probes, pool, facets)
    supports = actual_supports(probes, U)
    certificate = hull.certify_hull(probes, U, F(1, 2))
    require(certificate['triple_strata_certified'] == 840
            and certificate['classifications'] == {'opposite': 726, 'distance': 114, 'degenerate': 0}
            and certificate['all_triples_and_closed_boundaries_covered'],
            'complete new840strata torque proof on the expanded triangle')
    rejected = 0
    if self_test:
        bad_review = {**review, 'proved_refined_transport_and_band': {
            **review['proved_refined_transport_and_band'],
            'nonwinning_squared_height_slack': '1/600'}}
        controls = [
            lambda: phase_bounds(q=F(9, 20)),
            lambda: phase_bounds(chord=F(1, 50)),
            lambda: phase_bounds(raw_radius=F(1, 4)),
            lambda: phase_bounds(theta=F(1, 5)),
            lambda: scalar_bounds(epsilon=F(1, 400)),
            lambda: scalar_bounds(q=F(57, 125)),
            lambda: scalar_bounds(epsilon=F(0)),
            lambda: scalar_bounds(pair_lower=F(0)),
            lambda: scalar_bounds(distance=F(0)),
            lambda: scalar_bounds(distance=F(1, 20)),
            lambda: winning.cut_triangle(F(3, 5)),
            lambda: winning.cut_triangle(Q, (ZERO, ZERO, ZERO)),
            lambda: winning.outer_geometry(U[:-1]),
            lambda: hull.validate_faces(hull.FACES[:-1]),
            lambda: hull.validate_faces(hull.FACES + hull.FACES[:1]),
            lambda: review_input_bytes(b'{}'),
            lambda: validate_review_record(bad_review),
        ]
        for control in controls:
            expect_rejection(control)
            rejected += 1
    return {
        'agent': 'six-rupert-3', 'role': 'researcher',
        'proof_status': 'complete_unformalized_expanded_numeric_global_RID_receiver_slack',
        'global_RID': 'OPEN', 'global_non_rupert_proved': False,
        'numeric_global_all_receivers_axial_squared_slack': '1/450',
        'strict_passage_necessary_receiver_condition': 'f(n)^2<beta-1/450',
        'strict_receiver_squared_diameter_lower': '(736+960phi)/29+2/225',
        'conditional_winning_to_winning_source_and_receiver_height_strict_lower': '909/2000',
        'all_original_proper_Q_full_roll_translation_scale_ge_one_covered': True,
        'expanded_receiver_cut_triangle': rational_strings(cut),
        'expanded_phase_bounds': phase, 'expanded_outer_geometry': outer,
        'same_exact_center_hull_regenerated': center,
        'all_actual_original_cut_triangle_support_comparisons': supports,
        'full_expanded_actual_torque_facet_certificate': certificate,
        'all_new_global_injection_rational_bounds': bounds,
        'every_original_injection_parent_field_regenerated': True,
        'original_parent_expected_sha256': ORIGINAL_SHA,
        'original_parent_malformed_controls_rejected': replay['new_malformed_controls_rejected'],
        'new_expanded_malformed_controls_rejected': rejected,
        'published_refined_nonwinning_review_input_sha256': REVIEW_SHA,
        'published_refined_nonwinning_policy_pinned_not_rerun':
            review['proved_refined_transport_and_band'],
        'review_of_new_global_theorem_asserted': False,
        'old_full_region_cap_review_and_winning_self_tests_replayed': False,
        'new_full840strata_recomputed_including_closed_boundary_strata': True,
        'native_algorithmic_independence_or_formalization_claimed': False,
    }


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--self-test', action='store_true')
    p.add_argument('--review-input', type=Path,
                   help='Exact public review expected.json, default neighboring repository directory')
    args = p.parse_args()
    print(json.dumps(check(args.self_test, args.review_input), sort_keys=True, indent=2))
