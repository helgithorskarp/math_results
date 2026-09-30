#!/usr/bin/env python3
"""Exact hypotheses for LINEAR_ROLL_PROOF.md; Python 3.11+ stdlib.

The hull and all support contacts are regenerated, including tied vertices.
The continuous rotation, frame and torque estimates are proved in prose.
"""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from verify import PHI, QPhi, ZERO, dot, require, vertices
from torque_certificate import cross, subtract
from cell_certificate import encode, geometry
from global_cap_certificate import check as check_previous, expect_rejection


def project(v, d):
    return tuple(x-y*dot(d,v)/dot(d,d) for x,y in zip(v,d))


def exact_hull(S, d):
    """Monotone chain in an oriented orthogonal Q(phi) chart."""
    e1 = (QPhi(1),ZERO,ZERO)
    e2 = cross(d,e1)
    require(dot(e1,d) == ZERO and dot(e2,e2) > 0, 'invalid hull chart')
    points = sorted(S, key=lambda p:(dot(p,e1),dot(p,e2)))
    def turn(p,q,r):
        a,b = subtract(q,p),subtract(r,p)
        return dot(a,e1)*dot(b,e2)-dot(a,e2)*dot(b,e1)
    def half(points):
        hull = []
        for p in points:
            while len(hull) >= 2 and turn(hull[-2],hull[-1],p) <= 0:
                hull.pop()
            hull.append(p)
        return hull
    return half(points)[:-1]+half(points[::-1])[:-1]


def validate_polygon(V, d, H):
    require(len(V) == 60, 'standard complete vertex set required')
    require(V == vertices(), 'vertex set differs from standard RID')
    S = {project(v,d) for v in V}
    N = dot(d,d)
    rho2 = QPhi(Fraction(20,3))+8*PHI
    C = {p for p in S if dot(p,p) == rho2}
    require(len(S) == 60 and len(C) == 12, 'threefold projection cardinalities')
    require(len(H) == 12 and len(set(H)) == 12 and set(H) == C,
            'hull must contain every maximum-circle vertex exactly once')
    edges, normals = [], []
    support_checks = 0
    for p,q in zip(H,H[1:]+H[:1]):
        m = cross(subtract(q,p),d)
        require(dot(m,m) > 0 and dot(m,d) == ZERO, 'degenerate edge normal')
        gaps = [dot(m,subtract(p,v)) for v in sorted(V)]
        require(all(g >= 0 for g in gaps), 'edge fails on a hidden or tied vertex')
        require(dot(m,p) > 0, 'outward edge distance must be positive')
        support_checks += len(gaps)
        h2 = dot(m,p)**2/dot(m,m)
        kp = dot(m,cross(d,p))
        kq = dot(m,cross(d,q))
        require(kp > 0 and kq < 0, 'oriented endpoint derivative signs')
        k2 = kp*kp/(N*dot(m,m))
        require(k2 == kq*kq/(N*dot(m,m)), 'unequal circular endpoint derivatives')
        require(k2 in (QPhi(1),QPhi(Fraction(5,3))), 'unexpected edge type')
        require(h2+k2 == rho2, 'edge-distance and derivative identity')
        ties = sum(g == ZERO for g in gaps)
        require(ties == (2 if k2 == QPhi(1) else 4), 'all edge ties must be checked')
        edges.append({'p':encode(p),'q':encode(q),'outward_normal':encode(m),
                      'squared_unit_support':h2.encode(),
                      'squared_unit_tangential_derivative':k2.encode(),
                      'original_vertex_ties':ties})
        normals.append(m)
    patterns = []
    witnesses = {}
    for i,p in enumerate(H):
        pattern = {}
        for m in (normals[i-1],normals[i]):
            k = dot(m,cross(d,p))
            pattern[k.sign()] = k*k/(N*dot(m,m))
            if pattern[k.sign()] == QPhi(Fraction(5,3)):
                witnesses.setdefault(k.sign(),(p,m))
        require(set(pattern) == {-1,1} and set(pattern.values()) == {
            QPhi(1),QPhi(Fraction(5,3))}, 'missing incident edge or roll sign')
        patterns.append({'p':encode(p),'negative_squared':pattern[-1].encode(),
                         'positive_squared':pattern[1].encode()})
    require(set(witnesses) == {-1,1}, 'both global roll signs need long-edge contacts')
    require(sum(e['original_vertex_ties'] == 4 for e in edges) == 6,
            'alternating long-edge count')
    require((1+2*PHI)**2 == 5+8*PHI, 'long-edge support is phi cubed')
    return {
        'projection_axis':encode(d), 'distinct_projected_vertices':len(S),
        'hull_vertices':len(H), 'hull_equals_maximum_radius_circle':True,
        'all_original_vertex_support_checks':support_checks,
        'long_edges':6, 'short_edges':6,
        'maximum_squared_radius':rho2.encode(),
        'long_edge_unit_support':(1+2*PHI).encode(),
        'long_edge_squared_unit_tangential_derivative':QPhi(Fraction(5,3)).encode(),
        'complete_oriented_edges':edges, 'incident_derivative_patterns':patterns,
        'signed_long_edge_witnesses':[
            {'sign':sgn,'vertex':encode(witnesses[sgn][0]),
             'outward_normal':encode(witnesses[sgn][1])} for sgn in (-1,1)],
    }


def check_roll_bound(slope=Fraction(3,20)):
    """Rational bounds at |alpha|=pi/6; no floating point or trig library."""
    sqrt3_lower = Fraction(433,250)
    chord_upper = Fraction(5177,10000)
    cosine_lower = Fraction(9659,10000)
    derivative_lower = Fraction(12909,10000)
    support_upper = Fraction(42361,10000)
    lower = derivative_lower*cosine_lower-support_upper*chord_upper/2
    checks = {
        'sqrt_three_lower':sqrt3_lower**2 < 3,
        'pi_over_six_roll_chord_upper':2-sqrt3_lower < chord_upper**2,
        'pi_over_twelve_cosine_lower':cosine_lower**2 < (2+sqrt3_lower)/4,
        'long_edge_derivative_lower':derivative_lower**2 < Fraction(5,3),
        'long_edge_support_upper':1+2*PHI < QPhi(support_upper),
        'global_linear_support_slope':lower > slope,
    }
    require(slope > 0 and all(checks.values()), 'global roll slope not certified')
    return {'global_support_gap_per_roll_chord_lower':str(slope),
            'roll_chord_per_one_sided_error_upper':str(1/slope),
            'maximum_reduced_roll_chord_upper':str(chord_upper),
            'cosine_half_roll_lower':str(cosine_lower),
            'long_edge_derivative_lower':str(derivative_lower),
            'long_edge_support_upper':str(support_upper),
            'endpoint_coefficient_lower':str(lower),
            'rational_and_quadratic_field_checks':checks}


def check_constants(delta=Fraction(1,7000)):
    R_upper = Fraction(9,2)
    source = Fraction(13,4)*delta
    eta = Fraction(153,8)*delta
    roll = Fraction(20,3)*eta
    angle_factor = Fraction(101,100)
    angle = angle_factor*(source+delta+roll)
    angle_upper = 134*delta
    perturbation = 27*delta
    center = Fraction(1,10)
    B = geometry()[0][0][1]
    checks = {
        'vertex_radius_less_than_nine_over_two':7+8*PHI < QPhi(R_upper**2),
        'c0_greater_than_four_over_seven':Fraction(4,7)**2 < Fraction(1,3),
        'c0_less_than_three_over_five':Fraction(1,3) < Fraction(3,5)**2,
        'receiver_axial_lower_positive':Fraction(4,7)-R_upper*delta > Fraction(1,2),
        'source_is_in_winning_region':Fraction(27,5)*delta < Fraction(1,1000),
        'source_chord_coercivity':2*Fraction(9,4)**2 < Fraction(13,4)**2,
        'all_transport_chords_less_than_one_over_fifty':max(source,delta,roll) < Fraction(1,50),
        'angle_over_chord_less_than_one_point_zero_one':
            angle_factor**2*(1-Fraction(1,100)**2) > 1,
        'full_relative_angle_upper':angle < angle_upper,
        'sum_of_angles_less_than_one':angle_upper < 1,
        'receiver_stays_in_threefold_chamber':delta < Fraction(1,100),
        'chart_bound_n_z':Fraction(4,5)-delta > Fraction(79,100),
        'chart_error_less_than_three_delta':Fraction(9,4)/Fraction(79,100) < 3,
        'receiver_stays_in_ABD':3*delta < Fraction(1,10),
        'center_chart_norm_less_than_one_point_one':dot(B,B) < QPhi(Fraction(121,100)),
        'perturbed_chart_norm_less_than_ten_over_nine':Fraction(11,10)+3*delta < Fraction(10,9),
        'support_remainder_coefficient_less_than_ten':R_upper*2*Fraction(10,9) <= 10,
        'torque_ball_remains_positive':center > perturbation,
        'torque_remainder_strictly_below_actual_ball':5*angle_upper < center-perturbation,
    }
    require(delta > 0 and all(checks.values()), 'receiver cap error bound failed')
    return {'receiver_normal_chord_radius':str(delta),
            'source_normal_chord_error_upper':str(source),
            'one_sided_shadow_error_upper':str(eta),
            'planar_roll_chord_error_upper':str(roll),
            'full_relative_angle_upper':str(angle_upper),
            'center_torque_ball_radius_lower':str(center),
            'torque_column_perturbation_upper':str(perturbation),
            'actual_torque_ball_radius_lower':str(center-perturbation),
            'support_remainder_coefficient_upper':'10',
            'maximum_linearized_torque_remainder':str(5*angle_upper),
            'strict_torque_margin_lower':str(center-perturbation-5*angle_upper),
            'rational_and_quadratic_field_checks':checks}


def check(self_test=False):
    previous = check_previous(self_test)
    path = Path(__file__).with_name('global_cap_expected.json')
    require(previous == json.loads(path.read_text()), 'inherited global certificate changed')
    V = vertices()
    d = (ZERO,QPhi(1),-PHI**2)
    H = exact_hull({project(v,d) for v in V},d)
    polygon = validate_polygon(V,d,H)
    roll = check_roll_bound()
    constants = check_constants()
    if self_test:
        expect_rejection(lambda:validate_polygon(V-{next(iter(V))},d,H))
        expect_rejection(lambda:validate_polygon(V,d,H[:-1]))
        expect_rejection(lambda:validate_polygon(V,d,H[::-1]))
        expect_rejection(lambda:validate_polygon(V,d,H[:-1]+H[:1]))
        expect_rejection(lambda:check_roll_bound(Fraction(1,5)))
        expect_rejection(lambda:check_constants(Fraction(1,6000)))
    return {'agent':'six-rupert-3','role':'researcher',
            'proof_status':'unformalized_analytic_theorem_with_exact_finite_hypotheses',
            'global_non_rupert_proved':False,
            'all_source_receiver_caps':10,
            'arbitrary_source_orientation_roll_translation_scale_ge_one':True,
            'cap_chord_radius_improvement_factor':str(Fraction(2000000,7000)),
            'exact_threefold_polygon':polygon, 'global_linear_roll_bound':roll,
            'quantitative_cap_constants':constants,
            'inherited_global_expected_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'inherited_global_graph':'bafkreih2j2cs6g7ctywh2i7du4q77rnm455nkowberfy4b333bpqkjp4pi',
            'inherited_cell_graph':'bafkreiakgi4vli7xoy5vmho5xsga7iistawcm7yhebl2flwkzu62hvewmq'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    args = parser.parse_args()
    print(json.dumps(check(args.self_test),indent=2,sort_keys=True))
