#!/usr/bin/env python3
"""Exact finite hypotheses for WEIGHTED_GLOBAL_BAND_PROOF.md.

Python3.11+ standard library. New weighted moment, three original pair gates,
gap-aware whole receiving supports and complete new840-stratum triangle.
The written continuum bridges and published complete spectrum are explicit
dependencies. Global RID Rupertness remains OPEN; author checks are not review.
"""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations
import json
from pathlib import Path

from verify import PHI, QPhi, ZERO, act, dot, matmul, require, symmetry_group, vertices
from cell_certificate import decode, encode, geometry
from torque_certificate import cross, determinant, subtract
from linear_roll_certificate import project
from global_cap_certificate import canonical, expect_rejection
from adaptive_receiver_certificate import rational_strings
from threshold_receiver_certificate import (
    BETA, I, REFS, active_balance, exact_rotations, facet_coefficients, field,
    root, source_coordinates, threefold_source, validate_proper)
from contact_collar_certificate import LOW, complete_contacts, torque_hull
from expanded_global_slack_certificate import actual_supports
import actual_torque_hull_certificate as hull
import beta_cap_certificate as beta
import winning_receiver_certificate as winning
import wider_winning_band_certificate as wider
import coupled_nonwinning_certificate as coupled

EPSILON, CAP, Q = F(1, 100), F(1, 108), F(89, 200)
WINNING_CHORD, WINNING_ANGLE = F(1, 22), F(64, 625)
PAIRING = [(0, 5), (1, 3), (2, 4)]
COUPLED_SHA = '40c237c4143253e2c6df0f1c64b1d79bca0db587538198c9966f73b6efd199b9'


def record_hash(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def matrix_encode(M):
    return [encode(row) for row in M]


def scalar_bounds(epsilon=EPSILON, cap=CAP, q=Q, candidate=F(9, 40),
                  matching=F(1, 4), moment_coefficient=F(19, 5),
                  threshold_angle=F(1, 20), winning_chord=WINNING_CHORD,
                  winning_angle=WINNING_ANGLE, receiving_height=F(13, 10)):
    require(epsilon > 0 and 0 < cap < F(1, 10) and q > 0 and
            candidate > 0 and matching > 0 and moment_coefficient > 0 and
            threshold_angle > 0 and 0 < winning_chord < F(1, 10) and
            winning_angle > 0 and 0 < receiving_height < F(9, 2),
            'positive geometric parameters in declared domains')
    eta = F(23, 50)*cap+F(9, 4)*cap*cap
    loss = epsilon+9*eta
    a_win = F(101, 300)*(F(289, 500)-q)
    eta_win = F(289, 500)*a_win+F(9, 4)*a_win*a_win
    eta_receive = receiving_height*cap+F(9, 4)*cap*cap
    lx, lt = (49+45*PHI)/29, (135+195*PHI)/29
    E = (F(13, 15)*winning_chord+F(3, 2)*winning_chord**2+
         F(17, 16)*winning_chord**2)/(1-winning_chord**2/4)
    X2 = (2*winning_chord)**2+E**2
    quaternion_product = (1-winning_chord**2/4)**2*(1-E**2/4)
    phase_margin = F(1, 2)-F(9, 2)*F(27, 25)*winning_angle
    checks = {
        'cutoff_above_q_squared': BETA-QPhi(epsilon) > QPhi(q*q),
        'cutoff_above_remaining366region_maximum': BETA-QPhi(epsilon) > QPhi(F(1, 7)),
        'reference_beta_height_exceeds57over125': BETA > QPhi(F(57, 125)**2),
        'threshold_height_sum_exceeds9over10': F(57, 125)+q > F(9, 10),
        'sharp_threshold_disk_exceeds9over5': (39+37*PHI)/29 > QPhi(F(9, 5)**2),
        'sqrt2_upper3over2': 2 < F(3, 2)**2,
        'both_threshold_coercivity_chords_inside_cap': F(25, 27)*epsilon <= cap,
        'body_radius_below9over2': 7+8*PHI < QPhi(F(9, 2)**2),
        'original_long_endpoint_height_below13over10': QPhi(F(5,3)) < QPhi(F(13,10)**2),
        'original_long_support_below17over4': PHI**3 < QPhi(F(17,4)),
        'threshold_circle_height_below23over50': BETA < QPhi(F(23, 50)**2),
        'threshold_circle_radius_exceeds22over5': 7+8*PHI-BETA > QPhi(F(22, 5)**2),
        'candidate_original_absolute_height_below_one_half': BETA+QPhi(9*eta) < QPhi(F(1, 4)),
        'all52_other_threshold_originals_above_one_half': F(3, 5)-F(9, 2)*cap > F(1, 2),
        'candidate_distance_squared_clears_original_loss': candidate**2 > loss,
        'all8_source_originals_have_distinct_candidates': F(3, 2)-2*eta > 2*candidate,
        'flattened_reference_matching_inside_one4': candidate+2*eta < matching,
        'complete_matching_arcs_disjoint': 2*matching < F(3, 2),
        'all6_forbidden_shift_gaps_exceed_matching_loss': 5 > 2*matching,
        'normal_eigenvalue_below_both_tangent_values': 0 < BETA < lx < lt,
        'weighted_full_chord_coefficient': QPhi(moment_coefficient**2)*(BETA+lx) > 4*lt,
        'weighted_full_chord_below_one10': moment_coefficient*cap < F(1, 10),
        'chord_to_angle101over100': F(101, 100)**2*(1-F(1, 400)) > 1,
        'weighted_FULL_angle_below_local_one20': F(101, 100)*moment_coefficient*cap < threshold_angle,
        'winning_reference_height_upper289over500': F(1, 3) < F(289, 500)**2,
        'winning_reference_height_lower577over1000': F(577, 1000)**2 < F(1, 3),
        'winning_reference_disk_exceeds3': QPhi(F(8, 3))+4*PHI > QPhi(9),
        'winning_source_sine_below_one20': (F(289, 500)-q)/3 < F(1, 20),
        'winning_source_cosine_exceeds499over500': 1-((F(289, 500)-q)/3)**2 > F(499, 500)**2,
        'winning_chord_over_sine_multiplier': F(101, 100)**2*F(999, 1000) > 1,
        'both_winning_normal_chords_below_one22': 0 < a_win < winning_chord,
        'all12_signed_winning_active_heights_keep_their_signs': F(577, 1000)*F(499, 500)-F(9, 2)*winning_chord > 0,
        'all48_nonactive_winning_heights_above_one': F(5, 4)-F(9, 2)*winning_chord > 1,
        'three_positive_pair_means_exceed_one_half': F(577, 1000)*F(499, 500)-F(3, 2)*winning_chord > F(1, 2),
        'known_Gamma1over16_clears_NEW_actual_transports': F(1, 16)-eta_win-eta_receive > F(1, 60),
        'winning_remote_roll_gate': E < F(77, 1000),
        'winning_quaternion_scalar_branch': quaternion_product > F(99,100)**2 and F(99,100)-winning_chord**2/4 > 0,
        'winning_quaternion_chord_domain': X2 <= F(1,9),
        'winning_inverse_sine_derivative_bound': F(101,100)**2*(1-X2/4) > 1,
        'winning_full_spatial_angle_from_perpendicular_transports': F(101, 100)**2*((2*winning_chord)**2+E**2) < winning_angle**2,
        'winning_actual_torque_remainder_margin': phase_margin > F(1, 500),
    }
    require(all(checks.values()), 'unsupported weighted global-band scalar gates')
    return rational_strings(dict(epsilon=epsilon, q=q, threshold_normal_chord_cap=cap,
        both_threshold_circle_transport_upper=eta, candidate_squared_distance_upper=loss,
        original_candidate_distance_upper=candidate, flattened_matching_distance_upper=matching,
        full_rotation_chord_coefficient=moment_coefficient,
        threshold_full_principal_angle_upper=F(101, 100)*moment_coefficient*cap,
        threshold_local_rotation_angle=threshold_angle, winning_source_chord=a_win,
        winning_normal_chord_cap=winning_chord, winning_source_corner_transport_upper=eta_win,
        gap_aware_receiving_support_transport_upper=eta_receive, known_reference_Gamma=F(1, 16),
        new_actual_winning_source_support_margin=F(1, 16)-eta_win-eta_receive,
        winning_quaternion_chord_squared_upper=X2,
        winning_full_roll_error_upper=E, winning_full_principal_angle_upper=winning_angle,
        winning_raw_torque_radius=F(1, 2), winning_actual_remainder_margin=phase_margin,
        checks=checks))


def moment_certificate(n, V, supplied_weights=None, supplied_matrix=None):
    coupled.validate_vertices(V)
    N=dot(n,n);c=min(dot(v,n) for v in V if dot(v,n)>0)
    active=sorted(v for v in V if dot(v,n)==c)
    require(len(active)==4 and c*c/N==BETA, 'complete positive threshold originals')
    y=tuple(c*x/N for x in n)
    balances=[]
    for ids in combinations(range(4),3):
        a,b,d=[active[i] for i in ids];den=determinant(a,b,d)
        if den==ZERO:continue
        ws=(determinant(y,b,d)/den,determinant(a,y,d)/den,determinant(a,b,y)/den)
        if min(ws)>0:balances.append(dict(zip(ids,ws)))
    require(balances, 'positive exact original balances')
    ws=[sum((b.get(i,ZERO) for b in balances),ZERO)/len(balances) for i in range(4)]
    if supplied_weights is not None:ws=supplied_weights
    require(len(ws)==4 and min(ws)>0 and sum(ws,ZERO)==QPhi(1), 'full strictly positive original weights')
    require(tuple(sum((b*v[j] for b,v in zip(ws,active)),ZERO) for j in range(3))==y,
            'all tangent first moments cancel exactly')
    M=tuple(tuple(sum((b*v[i]*v[j] for b,v in zip(ws,active)),ZERO) for j in range(3)) for i in range(3))
    if supplied_matrix is not None:require(supplied_matrix==M, 'moment matrix equals ORIGINAL weighted outer products')
    require(act(M,n)==tuple(BETA*x for x in n), 'normal eigenvalue beta')
    tangent=(ZERO,-n[2],n[1]);xaxis=(QPhi(1),ZERO,ZERO)
    lx,lt=(49+45*PHI)/29,(135+195*PHI)/29
    require(dot(xaxis,act(M,tangent))==ZERO and M[0][0]==lx and
            dot(tangent,act(M,tangent))/N==lt, 'full exact orthogonal tangent eigenbasis')
    require(sum((M[i][i] for i in range(3)),ZERO)==7+8*PHI and 0<BETA<lx<lt,
            'positive complete three-eigenvalue spectrum')
    signed=[(v,b/2) for v,b in zip(active,ws)]+[(tuple(-x for x in v),b/2) for v,b in zip(active,ws)]
    require(len({v for v,b in signed})==8 and all(v in V for v,b in signed), 'all8 original antipodal moment points')
    record=dict(raw_reference=encode(n),positive_active_originals=[encode(v) for v in active],
                weights=[b.encode() for b in ws],moment_matrix=matrix_encode(M),
                original_antipodal_pair_weights=[(b/2).encode() for b in ws],
                normal_eigenvalue=BETA.encode(),tangent_eigenvalues=[lx.encode(),lt.encode()],
                exact_weighted_chord_coefficient_squared=(4*lt/(BETA+lx)).encode(),
                strict_rational_chord_coefficient='19/5')
    return record,M,ws


def transpose(A):return tuple(zip(*A))


def trace(A):return sum((A[i][i] for i in range(3)),ZERO)


def quaternion_rotation(axis, scale):
    b=tuple(QPhi(scale*x) for x in axis);b2=dot(b,b);den=1+b2
    skew=((ZERO,-b[2],b[1]),(b[2],ZERO,-b[0]),(-b[1],b[0],ZERO))
    A=tuple(tuple(((1-b2)*QPhi(int(i==j))+2*b[i]*b[j]+2*skew[i][j])/den
                  for j in range(3)) for i in range(3))
    validate_proper(A)
    return A,b


def moment_trace_audit(n,M):
    N=dot(n,n);records=[]
    axes=[(1,0,0),(0,1,0),(0,0,1),(1,2,-1)]
    for axis in axes:
        for scale in (F(0),F(1,100),F(-1,20),F(1)):
            A,b=quaternion_rotation(axis,scale)
            for tilt in (F(0),F(1,200),F(-1,100)):
                U,_=quaternion_rotation((1,0,0),tilt)
                nr=act(U,n);kr=act(transpose(A),nr)
                P=tuple(tuple(QPhi(int(i==j))-nr[i]*nr[j]/N for j in range(3)) for i in range(3))
                direct=trace(matmul(matmul(transpose(A),P),M))-trace(matmul(matmul(matmul(transpose(A),P),A),M))
                E=dot(kr,act(M,subtract(kr,nr)))/N
                if dot(b,b)==ZERO:cost=ZERO
                else:cost=((3-trace(A))/2)*(trace(M)-dot(b,act(M,b))/dot(b,b))
                require(direct==-cost+E, 'exact full-angle moment trace identity')
                a=root(dot(subtract(kr,n),subtract(kr,n))/N).hi
                d=root(dot(subtract(nr,n),subtract(nr,n))/N).hi
                upper=BETA*QPhi((a+d)**2/2)+((135+195*PHI)/29-BETA)*QPhi(a*(a+d))
                require(E<=upper, 'original normal-chord quadratic bound')
                records.append([axis,str(scale),str(tilt),direct.encode(),E.encode(),str(a),str(d)])
    return dict(exact_proper_rotation_regressions=len(records),
                all48_trace_and_normal_error_identities_verified=True,
                complete_regression_record_sha256=record_hash(records),
                regressions_are_not_the_continuum_proof=True)


def paired_winning_originals(V,B,active,P,pairs=PAIRING):
    require(len(active)==len(P)==6 and P==winning.validate_active(V,B,active),
            'same full six positive ORIGINAL active points')
    require(len(pairs)==3 and sorted(i for pair in pairs for i in pair)==list(range(6)) and
            all(len(pair)==2 and pair[0]!=pair[1] for pair in pairs), 'all six originals in three disjoint pairs')
    rows=[]
    for i,j in pairs:
        avg=tuple((P[i][k]+P[j][k])/2 for k in range(3))
        sq=dot(avg,avg)
        require(sq==QPhi(F(5,3)) and sq<QPhi(F(3,2)**2), 'each actual pair tangent mean norm')
        require(dot(active[i],B)==dot(active[j],B) and 3*dot(active[i],B)**2==dot(B,B),
                'both actual original pair heights equal positive c0')
        rows.append(dict(original_pair=[encode(active[i]),encode(active[j])],
                         active_indices=[i,j],tangent_average=encode(avg),squared_norm=sq.encode()))
    heights,_=wider.original_heights(V,B,active)
    return dict(pair_rows=rows,all_six_originals_covered_once=True,
                maximum_positive_original_candidates=3,maximum_signed_original_candidates=6,
                source_original_circle_points=8,full_original_height_record_sha256=record_hash(heights),
                exact_nonactive_original_squared_height_minimum=['5/3','0'])


def receiving_envelope(n,V,H,normals,cap=CAP,height_bound=F(13,10)):
    coupled.validate_vertices(V)
    require(0<cap<F(1,10) and 0<height_bound<F(9,2) and len(H)==len(normals)==16,
            'complete threshold receiving facets and declared support-envelope domain')
    N=dot(n,n);records=[];facets=[]
    for j,(p,m) in enumerate(zip(H,normals)):
        require(dot(m,m)>0 and dot(m,p)>0, 'actual nonzero positive reference support')
        norm_upper=root(dot(m,m)).hi;ties=[];positive=0;min_margin=None
        for v in sorted(V):
            gap=dot(m,subtract(p,v));require(gap>=0,'every ORIGINAL reference support')
            hs=dot(v,n)**2/N;h=root(hs).hi
            needed=max(F(0),h-height_bound)*cap
            gap_lower=field(gap).lo/norm_upper
            if gap==ZERO:
                require(h<=height_bound, 'every tied ORIGINAL satisfies the height envelope')
                ties.append(hs)
            else:
                require(gap_lower>needed, 'positive original slack clears its own excess height transport')
                positive+=1
                margin=gap_lower-needed
                min_margin=margin if min_margin is None else min(min_margin,margin)
            records.append([j,encode(v),gap.encode(),hs.encode(),str(h),str(gap_lower),str(needed)])
        facets.append(dict(facet=j,tied_originals=len(ties),strict_originals=positive,
                           max_tied_original_squared_height=max(ties).encode(),
                           minimum_strict_envelope_slack=str(min_margin)))
    require(len(records)==960, 'ALL sixteen facets and sixty original vertices')
    return dict(unit_normal_chord_cap=str(cap),uniform_tied_height_upper=str(height_bound),
                whole_original_receiving_support_error_upper=str(height_bound*cap+F(9,4)*cap*cap),
                all_original_support_envelope_comparisons=len(records),all16facets=facets,
                complete_original_envelope_record_sha256=record_hash(records),
                no_full_reference_hull_persistence_assumed=True)


def fresh_winning_outer(U,H=F(1,16),L=F(27,25)):
    require(len(U)==3 and len(set(U))==3 and 0<H<F(1,10) and L>1,
            'complete nondegenerate fresh cut triangle')
    A,B,D=geometry()[0][0]
    require(dot(cross(subtract(U[1],U[0]),subtract(U[2],U[0])),
                cross(subtract(U[1],U[0]),subtract(U[2],U[0])))>0, 'full triangle has positive area')
    for u in U:
        require(u[2]==QPhi(1),'raw unit-z chart')
        wD=u[0]/D[0];wB=(u[1]-wD*D[1])/B[1];wA=1-wB-wD
        require(min(wA,wB,wD)>=0, 'entire fresh triangle in closed ABD')
        require(dot(u,u)<QPhi(L*L) and dot(subtract(u,B),subtract(u,B))<QPhi(H*H),
                'fresh corner norm/drift bounds extend by convexity')
    interior=F(3,5)-9*H
    require(PHI-1>QPhi(F(3,5)) and interior>0, 'strict positive fresh origin-interiority')
    return rational_strings(dict(chart_norm_upper=L,chart_drift_upper=H,
        uniform_origin_interior_ball_lower=interior,corner_bounds_extend_by_convexity=True,
        inherited_outer_guard_changed=False,old_one10_interiority_comfort_not_required=True))


def new_band_witness(V,region,u):
    require(dot(u,u)>0 and all(dot(v,u)*dot(v,region)>0 for v in V),
            'all60 actual signs in the selected strict region')
    f2=min(dot(v,u)**2/dot(u,u) for v in V)
    require(BETA-QPhi(EPSILON)<=f2<BETA-QPhi(F(1,150)), 'actual height between new and old global cutoffs')
    return dict(raw_original_receiving_ray=encode(u),f_squared=f2.encode(),
                new_receiving_height_band_verified=True,all60_original_heights_checked=True,
                outside_every_old_receiver_union_claimed=False)


def check(self_test=False):
    old=hull.fixture('coupled_nonwinning_expected.json',COUPLED_SHA)
    global_data=hull.fixture('global_cap_expected.json',beta.GLOBAL_SHA)
    threshold=hull.fixture('threshold_receiver_expected.json',beta.THRESHOLD_SHA)
    win=hull.fixture('winning_receiver_expected.json',beta.WINNING_SHA)
    collar=hull.fixture('contact_collar_expected.json',beta.COLLAR_SHA)
    hull.fixture('balanced_receiver_expected.json',winning.BALANCED_SHA)
    scalar=scalar_bounds();V=vertices();G=symmetry_group(V,return_matrices=True)
    scores=global_data['diameter_and_sign_regions']['score_counts']
    values=[coupled.field_decode(x['score']) for x in scores]
    require(sum(x['regions'] for x in scores)==436 and
            sum(x['regions'] for x,v in zip(scores,values) if v==QPhi(F(1,3)))==10 and
            sum(x['regions'] for x,v in zip(scores,values) if v==BETA)==60 and
            max(v for v in values if v not in {BETA,QPhi(F(1,3))})==QPhi(F(1,7)),
            'published complete signed-region spectrum is the source/receiver reduction')
    axes={'body_projective_orbits':[dict(representative_balance=active_balance(n,V)) for n in REFS]}
    R,C,rotations=exact_rotations(G,axes)
    rays={canonical(act(g,n)) for n in REFS for g in G}
    pinned={canonical(decode(x['direction'])) for x in threshold['threshold_axis_classification']['all_sixty_axes_and_regions']}
    require(len(G)==len(rays)==60 and rays==pinned,'all60 proper symmetries and all60 threshold axes')
    for n in REFS:
        directed={act(g,n) for g in G}
        require(len(directed)==60 and all(tuple(-x for x in v) in directed for v in directed),
                'all directed threshold gauges and their reversals')
    hexagon,P,_=winning.active_hexagon()
    require(hexagon==win['complete_positive_active_tangent_hexagon'],'all positive original winning hexagon fields')
    active=[decode(v) for v in hexagon['positive_original_active_vertices']]
    B,H0,source=threefold_source(V,win)
    require(source==threshold['threefold_original_source_corner_bounds'],'every original winning source corner/preimage')
    pairs=paired_winning_originals(V,B,active,P)
    source_coords=source_coordinates(H0,B)
    references=[LOW,REFS[1]];cases=[];saved=[];covers=[]
    for j,(n,rho,ray_upper) in enumerate([(LOW,F(7,20),F(51,50)),(REFS[1],F(9,20),F(11,10))]):
        circle,ordered,originals,H=coupled.circle_geometry(n,V)
        require(circle==old['both_threshold_original_geometry_support_and_torque_certificates'][j]['complete_original_circle_geometry'],
                'every old circle-height, pair and forbidden-shift entry regenerated')
        contact,probes,T,_=complete_contacts(n,V,I)
        support=coupled.moving_support_certificate(n,V,probes,probes,cap=CAP)
        torque=torque_hull(T,rho)
        require(torque==collar['explicit_local_contact_caps'][j]['complete_center_torque_hull'],
                'every full reference torque facet and affine-rank witness regenerated')
        local=coupled.local_rotation_bounds(n,rho,ray_upper,cap=CAP,angle=F(1,20))
        moment,M,ws=moment_certificate(n,V)
        audit=moment_trace_audit(n,M)
        _,_,normals,*_=coupled.hull_data(n,V)
        envelope=receiving_envelope(n,V,H,normals)
        coeff=facet_coefficients(H,n,source_coords)
        leaves=old['both_complete_winning_source_full_roll_Bernstein_trees'][j]['all_compact_closed_leaf_witnesses']
        replay=coupled.replay_winning_cover(leaves,coeff,gamma=F(1,16))
        parent_cover=old['both_complete_winning_source_full_roll_Bernstein_trees'][j]
        require(all(replay[k]==parent_cover[k] for k in replay),'each regenerated selected known-Gamma coefficient agrees')
        covers.append(dict(known_reference_Gamma='1/16',already_proved_by_reviewer7576=True,
                           complete_closed_leaves=len(leaves),complete_tree_nodes=coupled.validate_closed_tree(leaves),
                           all_leaf_witnesses=leaves,**replay))
        support_manifest={k:v for k,v in support.items() if k!='all16actual_original_receiving_probes'}
        support_manifest['all16probe_original_endpoint_indices']=[sorted(V).index(w) for w,e in probes]
        support_manifest['complete_regenerated_support_record_sha256']=record_hash(support)
        circle_manifest={k:v for k,v in circle.items() if k not in {
            'full8ordered_original_circle_projections',
            'non_circle_original_squared_height_distribution'}}
        torque_manifest={k:v for k,v in torque.items() if k!='all_torque_facets'}
        torque_manifest['all12_facets_regenerated_and_compared_to_published_parent']=True
        torque_manifest['complete_regenerated_torque_record_sha256']=record_hash(torque)
        cases.append(dict(receiving_class=j,raw_reference=encode(n),moment=moment,trace_audit=audit,
                          full_circle_geometry=circle_manifest,selected_contact_support=support_manifest,
                          regenerated_reference_torque_hull_summary=torque_manifest,moving_torque_bounds=local,
                          gap_aware_whole_receiving_envelope=envelope))
        saved.append((n,ordered,originals,H,probes,T,M,ws,coeff))
    alignments=[]
    for si in range(2):
        for ti in range(2):
            D=I if si==ti else R;validate_proper(D)
            require({act(D,v) for v in saved[si][2]}==set(saved[ti][2]) and
                    {act(D,v) for v in saved[si][1]}==set(saved[ti][1]), 'all8 original and circle proper alignments')
            contact,probes,T,_=complete_contacts(saved[ti][0],V,D)
            require(probes==saved[ti][4] and T==saved[ti][5], 'all16 actual source/contact preimages')
            record=dict(source_class=si,receiving_class=ti,source_alignment='I' if si==ti else 'R_beta=C^5',
                        actual_shared_original_vertices=contact['original_shared_vertices'],all8actual_circle_originals_align=True,
                        original_vertex_index_convention='zero_based_lexicographic_exact_coordinate_order',
                        all16actual_original_source_contact_preimage_indices=[sorted(V).index(decode(r['original_source'])) for r in contact['actual_contact_records']])
            require(record==old['all4proper_source_receiver_original_circle_and_contact_alignments'][2*si+ti],
                    'all4 proper source contact alignment entries compared')
            alignments.append(record)
    chamber=wider.wider_chamber(G,d=WINNING_CHORD)
    U,cut=winning.cut_triangle(Q);outer=fresh_winning_outer(U)
    adaptive=hull.fixture('adaptive_receiver_expected.json',hull.ADAPTIVE_SHA)
    probes,pool,facets=hull.selected_probes(adaptive)
    center=hull.center_subhull(probes,pool,facets)
    supports=actual_supports(probes,U)
    triangle=hull.certify_hull(probes,U,F(1,2))
    require(triangle['all_triples_and_closed_boundaries_covered'] and triangle['triple_strata_certified']==840 and
            triangle['classifications']=={'opposite':726,'distance':114,'degenerate':0},
            'fresh complete winning840strata including every boundary')
    halfturns=wider.body_halfturns(G,V)
    halfturn_manifest={k:v for k,v in halfturns.items() if k!='all15_original_body_halfturn_axes'}
    halfturn_manifest['all15_original_body_halfturn_axes']=[
        {k:v for k,v in row.items() if k!='proper_body_halfturn'}
        for row in halfturns['all15_original_body_halfturn_axes']]
    halfturn_manifest['all15_proper_matrices_reconstructed_from_original_body_group']=True
    halfturn_manifest['complete_regenerated_halfturn_record_sha256']=record_hash(halfturns)
    witnesses=[new_band_witness(V,B,(ZERO,QPhi(F(87,250)),QPhi(1))),
               new_band_witness(V,LOW,(QPhi(F(7,250)),REFS[0][1],REFS[0][2]))]
    rejected=0
    if self_test:
        n,ordered,originals,H,ps,T,M,ws,coeff=saved[0]
        badM=tuple(tuple(x+(QPhi(1) if i==j==0 else ZERO) for j,x in enumerate(row)) for i,row in enumerate(M))
        badWs=ws[:];badWs[0]=ZERO
        original_shifts=cases[0]['full_circle_geometry']['complete_six_cyclic_shift_obstructions']
        badShift=json.loads(json.dumps(original_shifts))
        badShift[0]['shifted_pair']=[0,1]
        if badShift[0]['shifted_pair']==original_shifts[0]['shifted_pair']:badShift[0]['shifted_pair']=[0,2]
        leaves=old['both_complete_winning_source_full_roll_Bernstein_trees'][0]['all_compact_closed_leaf_witnesses']
        normal_rows=coupled.hull_data(n,V)[2]
        improper=tuple(tuple((-x if i==0 else x) for x in row) for i,row in enumerate(I))
        controls=[
            lambda:scalar_bounds(epsilon=F(0)),lambda:scalar_bounds(epsilon=F(1,80)),
            lambda:scalar_bounds(cap=F(1,200)),lambda:scalar_bounds(q=F(9,20)),
            lambda:scalar_bounds(candidate=F(1,5)),lambda:scalar_bounds(matching=F(1,5)),
            lambda:scalar_bounds(moment_coefficient=F(15,4)),lambda:scalar_bounds(threshold_angle=F(1,100)),
            lambda:scalar_bounds(winning_chord=F(1,23)),lambda:scalar_bounds(winning_angle=F(1,10)),
            lambda:scalar_bounds(winning_angle=F(11,100)),lambda:scalar_bounds(receiving_height=F(9,2)),
            lambda:moment_certificate(n,V,supplied_weights=badWs),
            lambda:moment_certificate(n,V,supplied_weights=ws[:-1]),
            lambda:moment_certificate(n,V,supplied_matrix=badM),
            lambda:moment_certificate(B,V),lambda:moment_certificate(n,V-{min(V)}),
            lambda:paired_winning_originals(V,B,active,P,PAIRING[:-1]),
            lambda:paired_winning_originals(V,B,active,P,[(0,5),(0,3),(2,4)]),
            lambda:paired_winning_originals(V,B,active,P,[(0,1),(2,3),(4,5)]),
            lambda:receiving_envelope(n,V,H[:-1],normal_rows),
            lambda:receiving_envelope(n,V,H,normal_rows,height_bound=F(1,2)),
            lambda:receiving_envelope(n,V,H,normal_rows,cap=F(1,2)),
            lambda:coupled.moving_support_certificate(n,V,ps[:-1],ps,cap=CAP),
            lambda:coupled.local_rotation_bounds(n,F(7,20),F(51,50),cap=CAP,angle=F(1,10)),
            lambda:coupled.validate_circle_order(n,set(ordered),ordered[:-1]),
            lambda:coupled.validate_circle_order(n,set(ordered),list(reversed(ordered))),
            lambda:coupled.validate_shift_witnesses(ordered,badShift),
            lambda:coupled.replay_winning_cover(leaves[:-1],coeff),
            lambda:coupled.replay_winning_cover(leaves+leaves[:1],coeff),
            lambda:coupled.replay_winning_cover(leaves,coeff,gamma=F(1)),
            lambda:fresh_winning_outer(U,H=F(11,200)),lambda:fresh_winning_outer(U,H=F(1,10)),
            lambda:fresh_winning_outer(U[:-1]),lambda:hull.validate_faces(hull.FACES[:-1]),
            lambda:validate_proper(improper),lambda:new_band_witness(V,B,B),
        ]
        for control in controls:expect_rejection(control);rejected+=1
    return dict(agent='six-rupert-3',role='researcher',
        proof_status='complete_written_unformalized_GLOBAL_one100_necessary_receiving_gap',
        every_strict_passage_necessary_receiving_condition='f(n)^2<beta-1/100',
        equivalent_squared_receiving_diameter_strict_lower='(736+960phi)/29+1/25',
        winning_band_closed_classification='iff lambda=1,t=0,Q in G union J_nG; exactly120proper equality orientations',
        global_RID='OPEN',global_non_rupert_proved=False,independent_review_or_formalization=False,
        unconditional_all_source_threshold_caps1over108_proved=False,
        all_new_scalar_gates=scalar,both_threshold_cases=cases,all4proper_original_alignments=alignments,
        new_three_original_winning_pair_certificate=pairs,
        known_reference_Gamma1over16_full_closed_replays=covers,
        actual_reference_winning_source_original_corner_record_sha256=record_hash(source),
        fresh_winning_proper_chamber=chamber,new_winning_cut_triangle=rational_strings(cut),
        fresh_winning_outer_triangle_bounds=outer,complete_winning_center_torque_hull=center,
        all1800_actual_winning_corner_original_support_comparisons=supports,
        full_NEW_q89over200_840stratum_torque_certificate=triangle,
        all15_original_body_halfturn_axis_facts=halfturn_manifest,actual_new_band_receiving_witnesses=witnesses,
        proper_cross_orbit_rotation_record_sha256=record_hash(rotations),
        pinned_expected_inputs=dict(coupled_nonwinning=COUPLED_SHA,global_spectrum=beta.GLOBAL_SHA,
            threshold=beta.THRESHOLD_SHA,winning_reference=beta.WINNING_SHA,contact_collar=beta.COLLAR_SHA,
            adaptive_original_supports=hull.ADAPTIVE_SHA,known_balanced_C3_hypotheses=winning.BALANCED_SHA),
        inherited436region_enumeration_rerun=False,old_rank_cones_required=False,
        inherited24_balanced_C3_moment_triples_rerun=False,
        old840stratum_certificate_used_as_new_triangle=False,
        fresh_new840strata_completely_regenerated=True,malformed_controls_rejected=rejected,
        floats_solver_private_inputs_or_sampled_continuum_used=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    output=(json.dumps(check(args.self_test),sort_keys=True,indent=2)+'\n').encode()
    expected=Path(__file__).with_name('weighted_global_band_expected.json')
    require(expected.is_file() and output==expected.read_bytes(), 'every expected mathematical byte must match')
    print(output.decode(),end='')
