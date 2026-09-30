#!/usr/bin/env python3
"""Exact hypotheses for WINNING_RECEIVER_PROOF.md, Python 3.11+ stdlib.

Regenerate the full six-point active tangent hexagon, replay the complete
balanced parent's finite hypotheses, and certify the actual torque hull
over the whole cut triangle containing every folded winning receiver with
F^2>=beta, including the maximum-circle obstruction at equality.
The continuous source/coercivity/chamber/cut/rotation bridges are in prose.
"""
import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from itertools import combinations

from verify import PHI,QPhi,ZERO,dot,vertices,require,symmetry_group
from torque_certificate import cross,subtract
from cell_certificate import geometry,encode
from adaptive_receiver_certificate import rational_strings
from global_cap_certificate import expect_rejection
import actual_torque_hull_certificate as hull
import balanced_receiver_certificate as balanced

BALANCED_SHA='65561ab22beb5addc09e3f62d60eaa064d8d431ea90377365161d89e2b0fb86b'
GLOBAL_SHA='69efa7e7cc4fbc359ce5481fc7eaa82c9779a51d56464597232e520663667fa8'


def validate_active(V,B,active):
    require(V==vertices(),'standard original body required')
    N=dot(B,B)
    complete=sorted(v for v in V if dot(v,B)>0 and 3*dot(v,B)**2==N)
    require(len(complete)==6 and active==complete,'all six positive active original vertices required')
    require(all(dot(v,B)==PHI-1 for v in active),'signed active chart heights')
    P=[tuple(x-y*dot(v,B)/N for x,y in zip(v,B)) for v in active]
    require(len(set(P))==6 and all(dot(p,B)==ZERO for p in P),'six distinct tangent projections')
    radius2=7+8*PHI-QPhi(F(1,3))
    require(all(dot(p,p)==radius2 for p in P),'common active tangent circle')
    require(all(sum((p[k] for p in P),ZERO)==ZERO for k in range(3)),'positive six-point balance')
    require(dot(cross(P[0],P[1]),B)!=ZERO,'tangent polygon must span its plane')
    return P


def validate_tangent_facets(P,facets,radius2):
    require(len(P)==6 and len(facets)==6,'six active tangent facets required')
    for m in facets:
        require(all(dot(m,p)<=QPhi(1) for p in P),'invalid tangent support facet')
        require(sum(dot(m,p)==QPhi(1) for p in P)==2,'tangent facet endpoints')
        require(QPhi(1)/dot(m,m)>=radius2,'unsupported active tangent disk')


def active_hexagon():
    V=vertices();B=geometry()[0][0][1];N=dot(B,B)
    active=sorted(v for v in V if dot(v,B)>0 and 3*dot(v,B)**2==N)
    P=validate_active(V,B,active)
    facets={};comparisons=0
    for i,j in combinations(range(6),2):
        m=cross(B,subtract(P[j],P[i]));h=dot(m,P[i])
        require(dot(m,m)>0,'distinct tangent edge candidates')
        gaps=[dot(m,p)-h for p in P];comparisons+=6
        if all(g<=0 for g in gaps) or all(g>=0 for g in gaps):
            require(h!=ZERO,'tangent origin on supporting edge')
            normal=tuple(q/h for q in m)
            require(all(dot(normal,p)<=QPhi(1) for p in P),'tangent edge orientation')
            facets[normal]={'pair':[i,j],'radius_squared':QPhi(1)/dot(normal,normal)}
    sharp=QPhi(F(8,3))+4*PHI
    require(min(f['radius_squared'] for f in facets.values())==sharp and sharp>QPhi(9),
            'sharp full active tangent hexagon radius')
    levels=Counter(tuple(f['radius_squared'].encode()) for f in facets.values())
    require(levels==Counter({tuple(sharp.encode()):3,
                            tuple((QPhi(F(17,3))+8*PHI).encode()):3}),
            'complete tangent edge-distance spectrum')
    validate_tangent_facets(P,facets,sharp)
    result={'positive_original_active_vertices':[encode(v) for v in active],
            'tangent_points':[encode(p) for p in P],
            'complete_possible_edge_pairs':15,'original_tangent_support_comparisons':comparisons,
            'facet_planes':[{'normal':encode(m),'pair':f['pair'],
                            'radius_squared':f['radius_squared'].encode()} for m,f in sorted(facets.items())],
            'sharp_centered_tangent_disk_radius_squared':sharp.encode(),
            'full_tangent_disk_radius_exceeds':3,'positive_mean_balance_verified':True,
            'all_six_points_span_tangent_plane':True}
    return result,P,set(facets)


def phase_bounds(chord=F(1,24)):
    q=F(57,125);c0=F(289,500);R=F(9,2);L=F(27,25)
    E=(F(13,15)*chord+F(3,2)*chord*chord+F(17,16)*chord*chord)/(1-chord*chord/4)
    theta=F(47,500)
    margin=F(1,2)-R*L*theta
    checks={
        'q_squared_below_nonwinning_region_gap':QPhi(q*q)<(19-8*PHI)/29,
        'c0_below_rational_upper':QPhi(F(1,3))<QPhi(c0*c0),
        'sine_bound_below_one_twentieth':(c0-q)/3<F(1,20),
        'acute_cosine_lower':F(399,400)>F(199,200)**2,
        'chord_over_sine_bound':F(101,100)**2*F(399,400)>1,
        'full_source_receiver_chord_bound':F(101,300)*(c0-q)<chord,
        'all_factor_chords_below_one_tenth':0<chord<F(1,10) and E<F(1,10),
        'balanced_error_below_complete_roll_threshold':E<F(77,1000),
        'full_perpendicular_axis_angle_bound':F(101,100)**2*((2*chord)**2+E*E)<theta*theta,
        'body_radius_upper':7+8*PHI<QPhi(R*R),
        'receiver_height_upper':F(5,3)<F(13,10)**2,
        'reference_support_upper':PHI**3<QPhi(F(17,4)),
        'strict_remainder_margin_above_one_twentyfifth':margin>F(1,25),
    }
    require(all(checks.values()),'whole winning-regime phase bounds unsupported')
    return {'axial_lower':q,'c0_upper':c0,'source_coercivity_chord_coefficient':F(101,300),
            'source_and_receiver_normal_chord_upper':chord,'balanced_support_error_upper':E,
            'full_proper_relative_angle_upper':theta,'chart_norm_upper':L,
            'actual_torque_ball_radius':F(1,2),'strict_torque_remainder_margin_lower':margin,
            'checks':checks}


def cut_triangle(q=F(57,125),cut_vertex=None):
    A,B,D=geometry()[0][0]
    if cut_vertex is None:
        cut_vertex=(QPhi(-1),PHI**3,QPhi(-1))
    require(QPhi(q*q)<(19-8*PHI)/29 and q>0,'cut uses a strict rational lower axial value')
    require(cut_vertex in vertices() and dot(cut_vertex,B)==PHI-1 and
            dot(cut_vertex,A)==QPhi(-1) and dot(cut_vertex,D)==ZERO,'actual original cut vertex')
    s=(PHI-1-q)/PHI;t=(PHI-1-q)/(PHI-1)
    require(0<s<1 and 0<t<1,'cut intercepts lie on the original closed ABD edges')
    U=(B,tuple((1-s)*b+s*a for a,b in zip(A,B)),
       tuple((1-t)*b+t*d for b,d in zip(B,D)))
    require(dot(cut_vertex,U[1])==QPhi(q) and dot(cut_vertex,U[2])==QPhi(q),
            'closed outer triangle cut line')
    return U,{'q':q,'vertex':encode(cut_vertex),'s_intercept':s.encode(),'t_intercept':t.encode(),
              'corners':[encode(u) for u in U]}


def outer_geometry(U,H=F(27,500),L=F(27,25)):
    require(len(U)==3 and len(set(U))==3,'complete three-corner cut triangle required')
    A,B,D=geometry()[0][0]
    require(dot(cross(subtract(U[1],U[0]),subtract(U[2],U[0])),
                cross(subtract(U[1],U[0]),subtract(U[2],U[0])))>0,'nondegenerate cut triangle')
    for u in U:
        require(u[2]==QPhi(1),'unit-z chart required')
        wD=u[0]/D[0];wB=(u[1]-wD*D[1])/B[1];wA=1-wB-wD
        require(min(wA,wB,wD)>=0,'entire triangle inside closed ABD')
        require(dot(u,u)<QPhi(L*L),'convex whole-triangle norm bound')
        require(dot(subtract(u,B),subtract(u,B))<QPhi(H*H),'convex whole-triangle chart drift')
    interior=F(3,5)-9*H
    require(PHI-1>QPhi(F(3,5)) and interior>F(1,10),'uniform origin interiority')
    return {'chart_norm_upper':L,'chart_drift_upper':H,
            'uniform_origin_interior_ball_lower':interior,
            'corner_bounds_extend_by_convexity':True,
            'triangle_itself_is_not_claimed_all_source_excluded_without_F_squared_gap':True}


def chamber_geometry(G):
    chamber=balanced.chamber_cap(G,F(1,24))
    A,B,D=geometry()[0][0]
    lower_z=F(9,10);d=F(1,24)
    chart_drift=d/(lower_z*(lower_z-d))
    require(dot(B,B)*QPhi(lower_z*lower_z)<QPhi(1),'center normal z exceeds nine tenths')
    require(chart_drift<F(1,10) and B[1]-D[1]>QPhi(F(1,10)),
            'all high-axial folded receivers lie in closed ABD')
    return {'center_normal_z_lower':lower_z,'receiver_normal_z_lower':lower_z-d,
            'chart_drift_from_cross_product_upper':chart_drift,
            'chamber_selection':chamber,'entire_folded_winning_regime_in_ABD':True}


def boundary_multiplicity(pair_threshold=None,receiver_positive_active_limit=2):
    V=sorted(vertices());A,B,D=geometry()[0][0];N=dot(B,B)
    R2=7+8*PHI;beta=(19-8*PHI)/29
    if pair_threshold is None:
        pair_threshold=beta
    require(all(q.a.denominator==1 and q.b.denominator==1 for v in V for q in v),
            'original vertices must have integral Z[phi] coordinates')
    pair_checks=0
    for v,w in combinations(V,2):
        require((R2+dot(v,w))/2!=pair_threshold,'source level can occur with two positive active tangents')
        pair_checks+=1
    require(pair_checks==1770 and R2!=beta,'one/two-active source cases excluded')
    active=[v for v in V if dot(v,B)>0 and 3*dot(v,B)**2==N]
    others=[v for v in V if 3*dot(v,B)**2!=N]
    require(len(active)==6 and len(others)==48,'complete active/nonactive original split')
    require(min(dot(v,B)**2/N for v in others)==QPhi(F(5,3)),
            'complete receiver nonactive axial height gap')
    require(F(25,16)<F(5,3) and F(5,4)-F(9,2)*F(1,24)>F(289,500),
            'nonactive vertices cannot attain the axial minimum near the center')
    require(F(4,7)-F(9,2)*F(1,24)>0,'positive active original heights remain positive')
    cut=(QPhi(-1),PHI**3,QPhi(-1))
    ties={}
    comparisons=0
    for name,u in [('A',A),('B',B),('D',D)]:
        gaps=[dot(subtract(v,cut),u) for v in active]
        require(all(g>=0 for g in gaps),'cut vertex is not an active axial minimizer on closed ABD')
        comparisons+=len(gaps)
        ties[name]=sorted(v for v,g in zip(active,gaps) if g==ZERO)
    require(len(ties['B'])==6 and len(ties['A'])==2 and len(ties['D'])==2 and
            set(ties['A']) & set(ties['D'])=={cut},'complete active dominance/tie pattern')
    require(max(len(ties['A']),len(ties['D']))<=receiver_positive_active_limit,
            'false upper multiplicity for the receiver boundary')
    global_data=hull.fixture('global_cap_expected.json',GLOBAL_SHA)
    spectrum=global_data['diameter_and_sign_regions']['score_counts']
    count=sum(row['regions'] for row in spectrum if row['score']==beta.encode())
    require(count==60,'published beta-level regional maximum count')
    return {'original_coordinate_integrality_checks':180,
            'one_and_two_active_source_cases_at_beta_excluded':True,
            'all_distinct_original_vertex_pair_scores_checked':pair_checks,
            'all_receiver_nonactive_vertices_checked':len(others),
            'minimum_nonactive_center_squared_axial_height':[str(F(5,3)),'0'],
            'active_dominance_corner_comparisons':comparisons,
            'tie_vertices':{name:[encode(v) for v in vv] for name,vv in ties.items()},
            'nonwinning_beta_source_distinct_maximum_radius_shadow_points_at_least':6,
            'winning_beta_receiver_distinct_maximum_radius_shadow_points_at_most':4,
            'boundary_beta_sources_excluded_by_circle_multiplicity':True,
            'isolated_nonwinning_beta_receiver_unoriented_maximizers':count,
            'isolated_nonwinning_beta_receiver_directed_maximizers':2*count,
            'regional_maximum_uniqueness_requires_written_nearest_point_argument':True}


def check(self_test=False):
    parent=hull.fixture('balanced_receiver_expected.json',BALANCED_SHA)
    replay=balanced.check(True)
    raw=(json.dumps(replay,sort_keys=True,indent=2)+'\n').encode()
    require(replay==parent and hashlib.sha256(raw).hexdigest()==BALANCED_SHA,
            'complete balanced-parent finite output differs')
    hexagon,P,facets=active_hexagon()
    phase=phase_bounds()
    U,cut=cut_triangle()
    geometry_bounds=outer_geometry(U)
    G=symmetry_group(vertices(),return_matrices=True)
    chamber=chamber_geometry(G)
    boundary=boundary_multiplicity()
    adaptive=hull.fixture('adaptive_receiver_expected.json',hull.ADAPTIVE_SHA)
    probes,pool,center_facets=hull.selected_probes(adaptive)
    center=hull.center_subhull(probes,pool,center_facets)
    require(center==parent['actual_center_torque_hull'],'complete center hull differs')
    supports=0
    for u in U:
        for v,e in probes:
            m=cross(e,u)
            for w in vertices():
                require(dot(m,subtract(v,w))>=0,'actual original support at a cut-triangle corner')
                supports+=1
    certificate=hull.certify_hull(probes,U,F(1,2))
    require(certificate['triple_strata_certified']==840 and
            certificate['classifications']=={'opposite':726,'distance':114,'degenerate':0},
            'complete whole cut-triangle facet cover differs')
    rejected=0
    if self_test:
        V=vertices();B=geometry()[0][0][1]
        active=sorted(v for v in V if dot(v,B)>0 and 3*dot(v,B)**2==dot(B,B))
        expect_rejection(lambda:validate_active(V,B,active[:-1]));rejected+=1
        bad=[tuple(-q for q in active[0]),*active[1:]]
        expect_rejection(lambda:validate_active(V,B,bad));rejected+=1
        expect_rejection(lambda:validate_tangent_facets(P,facets,QPhi(F(31,10)**2)));rejected+=1
        expect_rejection(lambda:validate_tangent_facets(P,set(sorted(facets)[:-1]),QPhi(9)));rejected+=1
        expect_rejection(lambda:cut_triangle(F(3,5)));rejected+=1
        expect_rejection(lambda:cut_triangle(cut_vertex=(QPhi(1),PHI**3,QPhi(-1))));rejected+=1
        expect_rejection(lambda:outer_geometry(U[:-1]));rejected+=1
        expect_rejection(lambda:outer_geometry(U,H=F(1,25)));rejected+=1
        expect_rejection(lambda:phase_bounds(F(1,25)));rejected+=1
        expect_rejection(lambda:hull.validate_faces(hull.FACES[:-1]));rejected+=1
        sortedV=sorted(V)
        false_pair_level=(7+8*PHI+dot(sortedV[0],sortedV[1]))/2
        expect_rejection(lambda:boundary_multiplicity(pair_threshold=false_pair_level));rejected+=1
        expect_rejection(lambda:boundary_multiplicity(receiver_positive_active_limit=1));rejected+=1
    return rational_strings({'agent':'six-rupert-3','role':'researcher',
        'proof_status':'unformalized_complete_closed_winning_receiver_superlevel_theorem_including_beta_boundary',
        'global_non_rupert_proved':False,
        'every_unit_receiver_with_F_squared_strictly_above_beta_excluded':True,
        'complete_closed_winning_superlevel_components_excluded':True,
        'closed_winning_receiver_domain':'F^2>=beta and dist(n,twenty_directed_threefold_centers)<=1/24',
        'beta':((19-8*PHI)/29).encode(),
        'global_necessary_receiver_condition_for_strict_passage':'F^2<beta or an isolated nonwinning regional maximum at beta',
        'equivalent_necessary_squared_receiver_diameter_lower':((736+960*PHI)/29).encode(),
        'arbitrary_original_source_full_rotation_roll_translation_scale_ge_one':True,
        'closed_containment_classification':'lambda=1,t=0,Q in G union J_n G; exactly120proper rotations in disjoint LEFT cosets',
        'beta_boundary_of_winning_receiver_components_covered':True,
        'isolated_nonwinning_beta_receiver_maximizers_not_covered':True,
        'complete_positive_active_tangent_hexagon':hexagon,'phase_bounds':phase,
        'outer_receiver_cut_triangle':cut,'outer_triangle_geometry':geometry_bounds,
        'whole_receiver_chamber_reduction':chamber,
        'source_receiver_maximum_radius_circle_boundary_obstruction':boundary,
        'new_original_cut_triangle_support_comparisons':supports,
        'complete_actual_torque_facet_certificate':certificate,
        'new_malformed_controls_rejected':rejected,
        'full_balanced_parent_finite_hypotheses_replayed':True,
        'balanced_parent_rejected_controls_replayed':replay['new_malformed_controls_rejected'],
        'complete_balanced_parent_every_output_byte_matches':True,
        'pinned_balanced_expected_sha256':BALANCED_SHA,
        'pinned_global_expected_sha256':GLOBAL_SHA,
        'full_old_directional_global_or_four_piece_self_tests_replayed':False})


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    print(json.dumps(check(args.self_test),sort_keys=True,indent=2))
