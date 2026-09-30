#!/usr/bin/env python3
"""Exact finite hypotheses of CONTACT_COLLAR_PROOF.md; Python3.11+ stdlib.

Regenerate two sixteen-contact original-edge/tie certificates, complete
eight-point torque hulls and explicit cap/angle margins. The global positive
axial slack is existential, via the written compactness proof, not a sampled
or numerically certified value of epsilon.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F
from itertools import combinations

from verify import PHI,QPhi,ZERO,act,dot,require,symmetry_group,vertices
from torque_certificate import cross,subtract,determinant
from cell_certificate import encode
from linear_roll_certificate import project
from global_cap_certificate import expect_rejection
from adaptive_receiver_certificate import rational_strings
import actual_torque_hull_certificate as hull
import winning_receiver_certificate as winning
from threshold_receiver_certificate import REFS,active_balance,exact_rotations,hull_data,I

WINNING_SHA='f2796de9c7123917dbd845c651179216ca595545c30e6a7cdb48ea7bf6312ba3'
THRESHOLD_SHA='5516794048036b35ce73b63b0fdf5eb1c01620b260b11f87dfc401e0e5ccfeac'
DELTA=F(1,300)
LOW=(ZERO,(2-PHI)/3,QPhi(-1))


def validate_vertices(V):
    require(V==vertices() and len(V)==60,'complete standard original body required')
    require(all(dot(v,v)==7+8*PHI and tuple(-q for q in v) in V for v in V),
            'equal radius and central symmetry of every original vertex')


def validate_probe(n,V,w,e):
    require(w in V and dot(e,e)==QPhi(4),'actual original vertex and length-two edge required')
    require(tuple(a+b for a,b in zip(w,e)) in V or subtract(w,e) in V,
            'original edge must have an actual second endpoint')
    m=cross(e,n);require(dot(m,m)>0,'nonzero actual receiving support')
    gaps=[dot(m,subtract(w,v)) for v in V]
    require(min(gaps)>=0,'every original vertex must satisfy the actual receiving support')
    ties=sorted(v for v,g in zip(V,gaps) if g==ZERO)
    require(all(cross(subtract(w,v),e)==(ZERO,ZERO,ZERO) for v in ties),
            'all zero gaps must persist identically under normal movement')
    require(len(ties)==2,'exact two-original-endpoint tie set')
    positive=min(g for g in gaps if g>0)
    return m,ties,positive


def complete_contacts(n,V,C):
    S,H,normals,_,_,circle=hull_data(n,V)
    originals=[]
    for p in H:
        vv=[v for v in V if project(v,n)==p]
        require(len(vv)==1,'unique actual receiving corner preimage');originals.append(vv[0])
    shared=V&{act(C,v) for v in V};Ct=tuple(zip(*C))
    active={v for v in V if project(v,n) in circle}
    require(len(active)==8 and active<=shared,'all eight actual circle preimages must be shared originals')
    records=[];probes=[];torques=set();minima=[]
    for j,(p,q,m,a,b) in enumerate(zip(H,H[1:]+H[:1],normals,originals,originals[1:]+originals[:1])):
        e=subtract(b,a);require(cross(e,n)==m,'original edge reproduces full receiving facet')
        for w in sorted(active):
            if dot(m,subtract(p,w))!=ZERO:continue
            exact_m,ties,positive=validate_probe(n,V,w,e);require(exact_m==m,'contact orientation')
            source=act(Ct,w);require(source in V and act(C,source)==w,'actual shared source preimage')
            T=cross(w,m);torques.add(T);minima.append(positive);probes.append((w,e))
            records.append({'receiving_facet':j,'original_receiver':encode(w),
                'original_source':encode(source),'original_edge':encode(e),
                'original_edge_squared_length':dot(e,e).encode(),
                'all_original_ties':[encode(v) for v in ties],
                'minimum_positive_raw_original_support_gap':positive.encode(),'raw_torque':encode(T)})
    require(len(records)==len(set(probes))==16 and len(torques)==8,
            'complete sixteen actual contacts and eight distinct torques required')
    require(len({r['receiving_facet'] for r in records})==10,
            'sixteen original endpoint contacts on ten selected actual receiving facets')
    require(all((tuple(-q for q in w),tuple(-q for q in e)) in probes for w,e in probes),
            'every actual support has its antipodal original support partner')
    return {'full_original_support_comparisons':960,'actual_contact_records':records,
            'complete_receiving_hull_facets_considered':16,'selected_distinct_actual_receiving_facets':10,
            'original_shared_vertices':len(shared),'active_shared_original_vertices':8,
            'minimum_positive_raw_original_gap':min(minima).encode()},probes,torques,min(minima)


def validate_complete_probes(actual,expected):
    require(len(actual)==16 and actual==expected,'complete generated original contact list required')


def torque_hull(T,rho):
    require(len(T)==8,'complete eight-torque set required')
    rank=next((a,b,c,d) for a,b,c,d in combinations(sorted(T),4)
              if determinant(subtract(b,a),subtract(c,a),subtract(d,a))!=ZERO)
    facets={};sides=0
    for a,b,c in combinations(sorted(T),3):
        m=cross(subtract(b,a),subtract(c,a))
        if dot(m,m)==ZERO:continue
        h=dot(m,a);gaps=[dot(m,t)-h for t in T];sides+=len(T)
        if all(g<=0 for g in gaps) or all(g>=0 for g in gaps):
            require(not all(g==ZERO for g in gaps),'full torque hull cannot be coplanar')
            if all(g>=0 for g in gaps):m=tuple(-q for q in m);h=-h
            first=next(q for q in m if q!=ZERO);scale=first if first>0 else -first
            facets[tuple(q/scale for q in m)]=h/scale
    require(len(facets)==12 and all(h>0 for h in facets.values()),
            'complete twelve-facet full-dimensional hull has strict origin interiority')
    distance=min(h*h/dot(m,m) for m,h in facets.items())
    require(distance>QPhi(rho*rho),'unsupported centered torque-ball radius')
    return {'raw_torque_hull_facets':12,'all_torque_triples':56,
            'full_torque_triple_side_comparisons':sides,
            'full_affine_rank_witness':[encode(t) for t in rank],
            'minimum_squared_raw_torque_hull_origin_distance':distance.encode(),
            'raw_torque_ball_radius_lower':str(rho),
            'all_torque_facets':[{'normal':encode(m),'height':h.encode(),
                                 'origin_squared_plane_distance':(h*h/dot(m,m)).encode()}
                                for m,h in sorted(facets.items())]}


def cap_bounds(n,gap,rho,theta,delta=DELTA,ray_upper=F(11,10)):
    B=F(9,2)
    require(delta>0 and rho>0 and theta>0 and ray_upper>0,'positive cap/angle parameters')
    require(dot(n,n)<QPhi(ray_upper*ray_upper),'unsupported unnormalized reference ray bound')
    require(7+8*PHI<QPhi(B*B),'strict body radius bound')
    require(gap>QPhi(18*delta*ray_upper),'positive original support gap does not clear full cap loss')
    ball=rho/ray_upper/B-2*delta
    require(ball>theta,'normalized torque ball does not clear FULL rotation angle')
    return {'receiver_unit_normal_chord_cap':str(delta),'reference_ray_norm_upper':str(ray_upper),
            'unit_original_support_gap_change_Lipschitz_upper':'18',
            'normalized_torque_movement_Lipschitz_upper':'2',
            'uniform_contact_normalization':str(B),
            'unit_normal_support_rotation_remainder_coefficient_upper':str(B),
            'full_relative_rotation_angle_upper':str(theta),
            'uniform_normalized_torque_ball_lower':str(ball),
            'strict_normalized_rotation_margin_lower':str(ball-theta)}


def winning_local_bounds(G,data):
    record,_,_=winning.active_hexagon()
    require(record==data['complete_positive_active_tangent_hexagon'],
            'entire active hexagon differs from published winning predecessor')
    adaptive=hull.fixture('adaptive_receiver_expected.json',hull.ADAPTIVE_SHA)
    probes,_,_=hull.selected_probes(adaptive)
    U,cut=winning.cut_triangle();outer=winning.outer_geometry(U)
    supports=0
    for u in U:
        for v,e in probes:
            for w in vertices():
                require(dot(cross(e,u),subtract(v,w))>=0,'actual whole-cut-triangle support');supports+=1
    phase=winning.phase_bounds();chamber=winning.chamber_geometry(G)
    q=phase['axial_lower'];ball=F(1,2)/F(27,25)/F(9,2)
    require(ball==F(25,243)>F(1,16),'winning local full-angle normalized bound')
    require(q*q<F(1,3) and QPhi(q*q)<(19-8*PHI)/29,'strict weaker winning receiver axial cut')
    require(data['complete_actual_torque_facet_certificate']['triple_strata_certified']==840,
            'published full all-facet winning certificate required')
    return rational_strings({'reference_threefold_positive_active_hexagon_every_entry_matches':True,
            'all_ten_original_probes_valid_on_closed_ABD_and_cut_triangle':True,
            'new_original_cut_triangle_support_comparisons':supports,
            'strict_winning_region_axial_lower':q,'source_or_receiver_winning_chord_upper':'1/24',
            'whole_actual_cut_triangle':cut,'outer_triangle_geometry':outer,
            'actual_closed_chamber_selection':chamber,
            'published_raw_torque_ball_radius':'1/2','uniform_unit_normalized_torque_ball_lower':str(ball),
            'full_near_body_rotation_angle_upper':'1/16',
            'strict_normalized_rotation_margin_lower':str(ball-F(1,16)),
            'published840case_whole_triangle_facet_theorem_used':True,
            'full840case_parent_self_test_replayed':False})


def check(self_test=False):
    V=vertices();validate_vertices(V);G=symmetry_group(V,return_matrices=True)
    threshold=hull.fixture('threshold_receiver_expected.json',THRESHOLD_SHA)
    win=hull.fixture('winning_receiver_expected.json',WINNING_SHA)
    require(threshold['all_receivers_f_squared_at_least_beta_excluded_for_strict_passage'] and
            threshold['threshold_axis_classification']['complete_threshold_projective_axes']==60,
            'published complete threshold closed classification required')
    axes={'body_projective_orbits':[{'representative_balance':active_balance(n,V)} for n in REFS]}
    R,C,rotations=exact_rotations(G,axes)
    cases=[];saved=[]
    for name,n,source,rho,theta in [('lower_body',LOW,I,F(7,20),F(1,16)),
                                    ('higher_body_and_36_degree',REFS[1],C,F(9,20),F(1,12))]:
        contact,probes,T,gap=complete_contacts(n,V,source)
        center=torque_hull(T,rho);cap=cap_bounds(n,gap,rho,theta)
        cases.append({'case':name,'reference_ray':encode(n),'actual_shared_contact_certificate':contact,
                      'complete_center_torque_hull':center,'entire_cap_bounds':cap})
        saved.append((n,source,probes,T,gap,rho,theta))
    local=winning_local_bounds(G,win);rejected=0
    if self_test:
        n,source,probes,T,gap,rho,theta=saved[1];w,e=probes[0]
        controls=[lambda:validate_vertices(set(sorted(V)[:-1])),
                  lambda:validate_probe(n,V,w,tuple(-q for q in e)),
                  lambda:validate_probe(n,V,w,tuple(2*q for q in e)),
                  lambda:validate_complete_probes(probes[:-1],probes),
                  lambda:torque_hull(set(sorted(T)[:-1]),rho),
                  lambda:torque_hull(T,F(1,2)),
                  lambda:cap_bounds(n,gap,rho,theta,delta=F(1,100)),
                  lambda:cap_bounds(n,gap,rho,F(1,10)),
                  lambda:cap_bounds(n,gap,rho,theta,ray_upper=F(1)),
                  lambda:cap_bounds(n,gap,rho,theta,delta=F(-1,300))]
        for control in controls:expect_rejection(control);rejected+=1
    return {'agent':'six-rupert-3','role':'researcher',
        'proof_status':'complete_unformalized_contact_rigidity_and_existential_positive_global_axial_slack',
        'global_RID':'OPEN','global_non_rupert_proved':False,
        'some_epsilon_gt_zero_excludes_every_receiver_f_squared_at_least_beta_minus_epsilon':True,
        'epsilon_numerical_value_certified':False,
        'all_sixty_nonwinning_beta_axes_have_open_all_source_excluded_neighborhoods':True,
        'uniform_receiver_sphere_collar_is_from_written_compactness_not_samples':True,
        'all_source_original_rotation_roll_translation_scale_ge_one_in_global_slack_theorem':True,
        'explicit_local_contact_caps':cases,'winning_receiver_near_body_local_bounds':local,
        'proper36degree_rotation':rotations,
        'new_malformed_controls_rejected':rejected,'pinned_threshold_expected_sha256':THRESHOLD_SHA,
        'pinned_winning_expected_sha256':WINNING_SHA,
        'full_old_threshold_global_directional_winning_self_tests_replayed':False,
        'float_or_private_diagnostic_inputs':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true');args=parser.parse_args()
    print(json.dumps(check(args.self_test),sort_keys=True,indent=2))
