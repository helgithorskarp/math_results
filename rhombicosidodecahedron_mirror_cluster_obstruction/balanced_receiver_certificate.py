#!/usr/bin/env python3
"""Exact hypotheses for BALANCED_SUPPORT_PROOF.md, Python3.11+ stdlib.

Regenerates every C3 endpoint/gauge moment, full receiver height gaps,
proper group/chamber cap data and actual center torque hull. The continuous
averaging and support arguments are in the proof. No full parent replay.
"""
import hashlib
import json
import argparse
from fractions import Fraction as F
from pathlib import Path

from verify import PHI,QPhi,ZERO,act,dot,matmul,vertices,require,symmetry_group
from torque_certificate import cross
from cell_certificate import encode,decode
from linear_roll_certificate import project,exact_hull,validate_polygon
from directional_transport_certificate import (
    AXIS,I,axial_matrices,corner_preimages,validate_gauge,validate_long_heights)
from adaptive_receiver_certificate import rational_strings,root_bounds,check_roll_branch
import actual_torque_hull_certificate as hull
import orthogonal_receiver_certificate as orthogonal
from global_cap_certificate import canonical,expect_rejection

ORTHOGONAL_SHA='6eaaf32e88a8b46e1732c159fd062f2b6fadbe12c8925e9475ce130a20cee366'
ACTUAL_SHA='b74584ad4ed343925de777ca5b98f1217c95fdb08f073920acee28c8cd8aaaac'


def validate_equal_signed_heights(vectors,d):
    require(len(vectors)==3 and len(set(vectors))==3 and
            all(v in vertices() for v in vectors), 'three distinct original preimages required')
    height=dot(d,vectors[0])
    require(height**2/dot(d,d)==QPhi(F(1,3)) and
            all(dot(d,v)==height for v in vectors),
            'source signed axial heights do not cancel')
    return height


def validate_normal_orbit(orbit,d):
    require(len(orbit)==3 and len(set(orbit))==3, 'three distinct normals required')
    mm=dot(orbit[0],orbit[0])
    require(mm>0 and all(dot(m,m)==mm and dot(m,d)==ZERO for m in orbit),
            'normal orbit lengths/plane differ')
    require(tuple(sum((m[i] for m in orbit),ZERO) for i in range(3))==(ZERO,)*3,
            'three normals are not balanced')
    require(all(dot(orbit[i],orbit[j])==-mm/2 for i in range(3) for j in range(i)),
            'normal orbit not regular 120 degrees')


def tensor(v,w):
    return tuple(tuple(v[i]*w[j] for j in range(3)) for i in range(3))


def moment(vectors,normals):
    return tuple(tuple(sum((v[i]*m[j] for v,m in zip(vectors,normals)),ZERO)/3
                       for j in range(3)) for i in range(3))


def validate_isotropy(M,d):
    trace=sum((M[i][i] for i in range(3)),ZERO)
    require(all(M[i][j]+M[j][i]==trace*(I[i][j]-d[i]*d[j]/dot(d,d))
                for i in range(3) for j in range(3)),
            'symmetric C3 moment is not isotropic on reference plane')
    return trace


def balanced_hypotheses():
    V=vertices();d=AXIS;N=dot(d,d)
    H=exact_hull({project(v,d) for v in V},d)
    polygon=validate_polygon(V,d,H)
    edges=[e for e in polygon['complete_oriented_edges']
           if QPhi(*(F(x) for x in e['squared_unit_tangential_derivative']))==QPhi(F(5,3))]
    P=corner_preimages(V,d)
    matrices=axial_matrices(d)
    gauge=validate_gauge(V,d,P,matrices)
    heights=validate_long_heights(V,d,edges)
    G=matrices[1];powers=[I,G,matmul(G,G)]
    bynormal={decode(e['outward_normal']):e for e in edges}
    remaining=set(bynormal)
    orbits=[]
    while remaining:
        m0=min(remaining)
        orbit=[act(g,m0) for g in powers]
        require(len(set(orbit))==3 and set(orbit)<=remaining,
                'long edges do not split into complete C3 orbits')
        validate_normal_orbit(orbit,d)
        orbits.append(orbit);remaining-=set(orbit)
    require(len(orbits)==2,'complete six long-edge cover required')
    records=[]
    for orbit_index,normalorbit in enumerate(orbits):
        for roll_sign in (-1,1):
            points=[decode(bynormal[m]['p' if roll_sign==1 else 'q']) for m in normalorbit]
            require(all(points[j]==act(powers[j],points[0]) for j in range(3)),
                    'selected signed endpoints fail C3 covariance')
            support=dot(normalorbit[0],points[0])
            derivative=dot(normalorbit[0],cross(d,points[0]))
            require(support>0 and derivative.sign()==roll_sign,
                    'wrong signed edge endpoint')
            require(support**2/dot(normalorbit[0],normalorbit[0])==PHI**6 and
                    derivative**2/(N*dot(normalorbit[0],normalorbit[0]))==QPhi(F(5,3)),
                    'wrong physical h/kappa')
            for gi,g in enumerate(matrices):
                gt=tuple(zip(*g))
                for sign in (-1,1):
                    preimages=[tuple(sign*x for x in act(gt,P[p])) for p in points]
                    projected=[project(v,d) for v in preimages]
                    rotated_normals=[tuple(sign*x for x in act(gt,m)) for m in normalorbit]
                    rotated_Jnormals=[tuple(sign*x for x in act(gt,cross(d,m))) for m in normalorbit]
                    require(all(v in V and projected[j]==tuple(sign*x for x in act(gt,points[j]))
                                for j,v in enumerate(preimages)), 'incorrect original gauge preimage')
                    require(all(preimages[j]==act(powers[j],preimages[0]) for j in range(3)),
                            'gauge preimages fail C3 covariance')
                    height=validate_equal_signed_heights(preimages,d)
                    cos_moment=moment(projected,rotated_normals)
                    sin_moment=moment(projected,rotated_Jnormals)
                    cos_trace=validate_isotropy(cos_moment,d)
                    sin_trace=validate_isotropy(sin_moment,d)
                    require(cos_trace==support and sin_trace==-derivative,
                            'rolled support trace differs from h*cos+kappa*sin')
                    records.append({'long_edge_orbit':orbit_index,'residual_roll_sign':roll_sign,
                                    'proper_gauge_index':gi,'planar_halfturn_sign':sign,
                                    'common_signed_axial_dot':height.encode(),
                                    'cosine_moment':[encode(row) for row in cos_moment],
                                    'sine_over_axis_norm_moment':[encode(row) for row in sin_moment],
                                    'preimages':[encode(v) for v in preimages]})
    require(len(records)==24,'all two-orbit/two-sign/six-gauge triples required')
    data=json.dumps(records,sort_keys=True,separators=(',',':')).encode()
    return {'agent':'six-rupert-3','role':'researcher',
            'status':'exact_finite_C3_gauge_and_height_gap_hypotheses_verified',
            'global_non_rupert_proved':False,'full_parent_replay_performed':False,
            'complete_polygon':polygon,'gauge':gauge,'receiver_height_gaps':heights,
            'C3_long_edge_orbits':2,'signed_endpoint_gauge_triples':len(records),
            'all_original_endpoint_preimages_checked':3*len(records),
            'full_symmetric_tensor_entries_checked':18*len(records),
            'records_sha256':hashlib.sha256(data).hexdigest(),'records':records}


def envelope_constants():
    lower=F(399,400)
    checks={
        'h_less_than_seventeen_over_four':PHI**3<QPhi(F(17,4)),
        'R_greater_than_four':7+8*PHI>QPhi(16),
        'minimum_source_factor_denominator':1-F(1,10)**2/4==lower,
        'balanced_linear_receiver_coefficient_below_old':F(2,3)/lower<1,
        'balanced_quadratic_receiver_coefficient_below_old':F(1,3)/lower<F(1,2),
        'balanced_quadratic_source_coefficient_below_old':F(17,16)/lower<2,
        'kappa_greater_than_five_over_four':QPhi(F(5,3))>QPhi(F(25,16)),
        'new_envelope_gate_implies_receiver_chord_below_one_tenth':
            F(77,1000)*F(3,2)/F(5,4)<F(1,10),
        'receiver_chord_gate_within_height_audit':F(1,10)<F(1,2),
        'normalization_of_sharp_center_radius':dot(hull.geometry()[0][0][1],hull.geometry()[0][0][1])==3*(2-PHI),
    }
    require(all(checks.values()), 'balanced-envelope domain/inclusion constants fail')
    return {'E_balanced_formula':'[(2kappa/3)delta+(R/3)delta^2+(h/4)a^2]/(1-a^2/4)',
            'full_angle_formula':'(101/100)sqrt((a+delta)^2+E_balanced^2)',
            'preceding_entire_orthogonal_criterion_included':True,'checks':checks}


def cap_constants(delta=F(1,45),center_radius=F(4,7)):
    R=F(9,2);k=F(13,10);h=F(17,4)
    a=F(23,10)*delta
    E=(2*k*delta/3+R*delta*delta/3+h*a*a/4)/(1-a*a/4)
    chord2=(a+delta)**2+E*E
    theta=F(101,100)*root_bounds(QPhi(chord2))[1]
    ball=center_radius-2*R*delta
    B=hull.geometry()[0][0][1]
    beta=(19-8*PHI)/29
    zlower=F(4,5)-delta
    checks={
        'positive_cap':delta>0,
        'center_torque_normalized_ball_exceeds_lower':QPhi(center_radius**2)<QPhi(F(1,3)),
        'axial_lower_above_sharp_nonwinning_gap':QPhi((F(4,7)-R*delta)**2)>beta and F(4,7)-R*delta>0,
        'source_chord_coefficient':F(101,200)*R<F(23,10),
        'balanced_error_within_roll_threshold':E<=F(77,1000),
        'all_three_factor_chords_below_one_tenth':max(a,delta,E)<F(1,10),
        'center_normal_z_above_four_over_five':dot(B,B)<QPhi(F(25,16)),
        'chart_normal_z_positive':zlower>0,
        'chart_drift_less_than_three_delta':F(9,4)/zlower<3,
        'folded_receiver_stays_in_closed_ABD':3*delta<F(1,10),
        'actual_normalized_torque_ball_positive':ball>0,
        'strict_normalized_torque_margin_above_one_fiftieth':ball-R*theta>F(1,50),
    }
    require(all(checks.values()), 'closed balanced receiver-cap sufficient certificate fails')
    return {'closed_receiver_normal_chord_radius':delta,'unoriented_axes':10,
            'source_normal_chord_upper':a,'balanced_support_error_upper':E,
            'full_relative_angle_upper':theta,'normalized_center_ball_lower':center_radius,
            'uniform_normalized_actual_torque_ball_lower':ball,
            'strict_torque_margin_lower':ball-R*theta,
            'strict_margin_greater_than':'1/50','checks':checks}


def chamber_cap(G,delta):
    cells,_,_,D=hull.geometry();B=cells[0][1]
    signed=G|{tuple(tuple(-q for q in row) for row in g) for g in G}
    walls=[(QPhi(1),ZERO,ZERO),(ZERO,QPhi(1),ZERO),(-PHI,-PHI**2,QPhi(1))]
    for w in walls:
        reflection=tuple(tuple(I[i][j]-2*w[i]*w[j]/dot(w,w) for j in range(3)) for i in range(3))
        require(reflection in signed, 'chamber wall reflection absent from signed body group')
    orbit={act(g,B) for g in signed}
    require(len(orbit)==20 and canonical(B) in {canonical(act(g,AXIS)) for g in G},
            'complete threefold optimizer orbit differs')
    separations=[]
    for v in sorted(orbit):
        if v==B:continue
        defects=[dot(v,w)**2/(dot(v,v)*dot(w,w)) for w in walls if dot(v,w)<0]
        require(defects and max(defects)>QPhi(delta*delta),
                'closed cap can fold to another threefold center')
        separations.append(max(defects))
    ymax=max(u[1] for U in cells[1:] for u in U)
    require(ymax==D[1] and B[1]-ymax>QPhi(F(1,10)), 'ABD gap differs')
    return {'proper_body_rotations':len(G),'original_body_vertex_image_checks':60*len(G),
            'verified_chamber_wall_reflections':3,'directed_optimizer_centers':len(orbit),
            'other_center_wall_tests':len(separations),
            'minimum_squared_negative_unit_wall_defect':min(separations).encode(),
            'chamber_cap_radius':delta,'chart_gap_to_other_cells':(B[1]-ymax).encode()}


def halfturn_axes(G):
    records=[]
    for g in sorted(G):
        if sum((g[i][i] for i in range(3)),ZERO)!=QPhi(-1):continue
        require(matmul(g,g)==I, 'trace-minus-one proper body rotation is not a half-turn')
        axis=next(tuple(g[i][j]+I[i][j] for i in range(3)) for j in range(3)
                  if sum(((g[i][j]+I[i][j])**2 for i in range(3)),ZERO)>0)
        witness=next((v for v in sorted(vertices()) if dot(v,axis)==ZERO),None)
        require(witness is not None, 'body half-turn axis has positive axial function')
        records.append({'axis':encode(axis),'original_zero_height_vertex':encode(witness)})
    require(len(records)==15, 'complete body half-turn count differs')
    return {'proper_body_halfturn_axes':15,'every_body_halfturn_axis_has_f_zero':True,
            'F_positive_implies_two_closed_equality_cosets_disjoint':True,
            'exact_equal_shadow_proper_rotations':120,
            'axis_witness_records_sha256':hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest()}


def check(self_test=False):
    hull.fixture('orthogonal_receiver_expected.json',ORTHOGONAL_SHA)
    hull.fixture('actual_torque_hull_expected.json',ACTUAL_SHA)
    hull.fixture('directional_transport_expected.json',hull.PARENT_SHA)
    adaptive=hull.fixture('adaptive_receiver_expected.json',hull.ADAPTIVE_SHA)
    balanced=balanced_hypotheses()
    composition=orthogonal.composition_hypotheses()
    roll=check_roll_branch()
    constants=envelope_constants()
    cap=cap_constants()
    G=symmetry_group(vertices(),return_matrices=True)
    chamber=chamber_cap(G,F(1,45))
    equality=halfturn_axes(G)
    probes,pool,facets=hull.selected_probes(adaptive)
    center=hull.center_subhull(probes,pool,facets)
    rejected=0
    if self_test:
        first=balanced['records'][0]
        preimages=[decode(v) for v in first['preimages']]
        normals=[decode(e['outward_normal']) for e in balanced['complete_polygon']['complete_oriented_edges']
                 if QPhi(*(F(x) for x in e['squared_unit_tangential_derivative']))==QPhi(F(5,3))]
        G3=axial_matrices(AXIS)
        orbit=[act(g,normals[0]) for g in (I,G3[1],matmul(G3[1],G3[1]))]
        bad_preimages=[tuple(-x for x in preimages[0]),*preimages[1:]]
        expect_rejection(lambda:validate_equal_signed_heights(bad_preimages,AXIS));rejected+=1
        expect_rejection(lambda:validate_equal_signed_heights(preimages[:-1],AXIS));rejected+=1
        expect_rejection(lambda:validate_normal_orbit([orbit[0],orbit[0],orbit[2]],AXIS));rejected+=1
        M=tuple(decode(row) for row in first['cosine_moment'])
        bad_M=tuple(tuple(M[i][j]+int(i==j==0) for j in range(3)) for i in range(3))
        expect_rejection(lambda:validate_isotropy(bad_M,AXIS));rejected+=1
        V=vertices();P=corner_preimages(V,AXIS)
        expect_rejection(lambda:validate_gauge(V,AXIS,P,G3[:-1]));rejected+=1
        improper=tuple(tuple(-q for q in row) for row in I)
        expect_rejection(lambda:validate_gauge(V,AXIS,P,(I,G3[1],improper)));rejected+=1
        expect_rejection(lambda:cap_constants(F(1,40)));rejected+=1
        expect_rejection(lambda:cap_constants(center_radius=F(3,5)));rejected+=1
        expect_rejection(lambda:hull.verify_fixture_bytes(b'{}',ORTHOGONAL_SHA));rejected+=1
    # The complete moments are regenerated and checked; compact output hashes
    # them rather than requiring a separate moment-record corpus.
    compact={k:v for k,v in balanced.items() if k not in ('records','complete_polygon')}
    compact['complete_reference_polygon_support_checks']=balanced['complete_polygon']['all_original_vertex_support_checks']
    return rational_strings({'agent':'six-rupert-3','role':'researcher',
        'proof_status':'unformalized_C3_balanced_support_and_closed_all_source_receiver_cap_theorem',
        'global_non_rupert_proved':False,
        'arbitrary_source_orientation_roll_translation_scale_ge_one':True,
        'includes_entire_preceding_orthogonal_receiver_criterion':True,
        'closed_containment_classification':'lambda=1, t=0, Q in G union J_n G; J_n=2nn^T-I',
        'balanced_hypotheses':compact,'envelope_constants':constants,
        'closed_cap_constants':cap,'cap_chamber':chamber,
        'closed_equality_cosets':equality,
        'actual_center_torque_hull':center,'persistent_probe_corner_support_checks':1800,
        'composition':composition,'complete_concavity_roll_branch':roll,
        'new_malformed_controls_rejected':rejected,
        'pinned_orthogonal_expected_sha256':ORTHOGONAL_SHA,
        'pinned_actual_expected_sha256':ACTUAL_SHA,
        'pinned_directional_expected_sha256':hull.PARENT_SHA,
        'pinned_adaptive_expected_sha256':hull.ADAPTIVE_SHA,
        'full_parent_or_four_piece_replays_performed':False})


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    print(json.dumps(check(args.self_test),sort_keys=True,indent=2))
