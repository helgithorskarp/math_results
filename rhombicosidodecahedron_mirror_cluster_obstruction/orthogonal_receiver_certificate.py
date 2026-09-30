#!/usr/bin/env python3
"""Exact hypotheses for the orthogonal-composition RID receiver cover.

One invocation checks one whole closed piece. Reproduce all four pieces.
The continuous quaternion/facet/cover bridges are in the written proof;
small rational quaternion cases audit arithmetic, not parameter coverage.
Python 3.11+ standard library, explicit checks also active under -O.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F
from itertools import product

import actual_torque_hull_certificate as h
from verify import QPhi,ZERO,PHI,require
from torque_certificate import cross,subtract
from adaptive_receiver_certificate import root_bounds,rational_strings

ACTUAL_SHA='b74584ad4ed343925de777ca5b98f1217c95fdb08f073920acee28c8cd8aaaac'
RADII=[F(3,5),F(3,5),F(29,50),F(3,5)]


def padd(p,q):
    out=dict(p)
    for k,v in q.items():
        out[k]=out.get(k,F(0))+v
        if out[k]==0:del out[k]
    return out


def pscale(p,c):
    return {k:v*c for k,v in p.items() if v*c}


def pmul(p,q):
    out={}
    for k,v in p.items():
        for l,w in q.items():
            m=tuple(a+b for a,b in zip(k,l))
            out[m]=out.get(m,F(0))+v*w
    return {k:v for k,v in out.items() if v}


def psquare(p):return pmul(p,p)


def polynomial_identity():
    one={(0,0,0,0):F(1)}
    a,d,e,p=[{tuple(int(i==j) for i in range(4)):F(1)} for j in range(4)]
    a2,d2,e2=map(psquare,(a,d,e))
    ad=pmul(a,d)
    P=one
    for v in (a2,d2,e2):P=pmul(P,padd(one,pscale(v,F(-1,4))))
    lhs=padd(padd(psquare(padd(a,d)),e2),pscale(padd(one,pscale(psquare(padd(p,pscale(ad,F(-1,4)))),-1)),-4))
    rhs=padd(pscale(pmul(ad,padd(one,pscale(p,-1))),2),
             pscale(pmul(pmul(a2,d2),padd(pscale(one,8),pscale(e2,-1))),F(1,16)))
    rhs=padd(rhs,pscale(pmul(e2,padd(a2,d2)),F(1,4)))
    require(padd(lhs,pscale(rhs,-1))==pscale(padd(psquare(p),pscale(P,-1)),4),
            'general four-variable orthogonal-chord identity failed')
    record=[[[*k],str(v)] for k,v in sorted(P.items())]
    return {'identity_verified_as_polynomial':True,'product_polynomial_terms':len(P),
            'product_polynomial_sha256':hashlib.sha256(json.dumps(record,separators=(',',':')).encode()).hexdigest()}


def rdot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))


def rcross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])


def qmul(a,b):
    s,v=a[0],a[1:];t,w=b[0],b[1:]
    c=rcross(v,w)
    return (s*t-rdot(v,w),*(s*w[i]+t*v[i]+c[i] for i in range(3)))


def matrix(q):
    w,x,y,z=q
    return ((1-2*(y*y+z*z),2*(x*y-w*z),2*(x*z+w*y)),
            (2*(x*y+w*z),1-2*(x*x+z*z),2*(y*z-w*x)),
            (2*(x*z-w*y),2*(y*z+w*x),1-2*(x*x+y*y)))


def mm(a,b):return tuple(tuple(sum((a[i][k]*b[k][j] for k in range(3)),F(0)) for j in range(3)) for i in range(3))


def validate_perpendicular_axis(axis,normal):
    require(len(axis)==len(normal)==3 and rdot(axis,axis)==rdot(normal,normal)==1 and
            rdot(axis,normal)==0,'rotation axis is not a unit perpendicular axis')


def validate_small_chords(a,d,e):
    require(all(0<=x<=F(1,10) for x in (a,d,e)), 'orthogonal-composition small-chord domain failed')


def quaternion_audit():
    normal=(F(0),F(0),F(1))
    first=(F(1),F(0),F(0))
    axes=[(F(1),F(0),F(0)),(F(3,5),F(4,5),F(0)),(F(0),F(1),F(0))]
    count=0
    for t,u,v in product((F(0),F(1,100),F(-1,100)),repeat=3):
        c1,s1=(1-t*t)/(1+t*t),2*t/(1+t*t)
        c2,s2=(1-u*u)/(1+u*u),2*u/(1+u*u)
        c3,s3=(1-v*v)/(1+v*v),2*v/(1+v*v)
        for axis in axes:
            validate_perpendicular_axis(first,normal);validate_perpendicular_axis(axis,normal)
            q1=(c1,s1,F(0),F(0));q2=(c2,F(0),F(0),s2);q3=(c3,*(s3*x for x in axis))
            q=qmul(qmul(q1,q2),q3)
            require(rdot(q,q)==1 and q[0]>0, 'rational quaternion audit unit/lift failure')
            formula=c1*c2*c3-s1*s3*(c2*rdot(first,axis)+s2*rdot(rcross(first,normal),axis))
            require(q[0]==formula,'quaternion scalar product formula failed')
            M=mm(mm(matrix(q1),matrix(q2)),matrix(q3))
            require(M==matrix(q),'direct rotation matrix product differs from quaternion product')
            trace=sum((M[i][i] for i in range(3)),F(0))
            a,d,e=2*abs(s3),2*abs(s1),2*abs(s2)
            validate_small_chords(a,d,e)
            require(3-trace==4*(1-q[0]*q[0]) and 3-trace<=(a+d)**2+e**2,
                    'full rotation chord audit failed')
            count+=1
    require(count==81,'incomplete rational quaternion arithmetic audit')
    return count


def composition_hypotheses():
    # Every factor <=1/10; the principal quaternion scalar remains positive.
    require(F(399,400)**3>F(99,100)**2 and F(99,100)-F(1,400)>0,
            'positive principal quaternion lift not established')
    require(F(1,20)<F(1,16),'combined chord not below1/4')
    require(F(101,100)**2*F(63,64)>1,'full chord-to-angle factor invalid')
    require((19-8*PHI)/29>QPhi(F(4,25)) and QPhi(F(7,12))**2>QPhi(F(1,3)),
            'inherited phase prerequisites do not force source small chord')
    require(F(101,200)*(F(7,12)-F(2,5))==F(1111,12000)<F(1,10),
            'source factor domain arithmetic failed')
    return {**polynomial_identity(),'rational_quaternion_matrix_audits':quaternion_audit(),
            'audit_points_are_not_continuum_coverage':True,
            'full_rotation_chord_bound':'sqrt((a+delta)^2+E^2)',
            'angle_multiplier':'101/100','every_factor_chord_domain':'<=1/10',
            'full_chord_domain':'<1/4','principal_lift_positive':True}


def cover():
    U=h.triangle(35,7)
    def mid(a,b):return tuple((x+y)/2 for x,y in zip(a,b))
    a,b,c=U;ab=mid(a,b);ac=mid(a,c);bc=mid(b,c)
    return U,[(a,ab,ac),(ab,b,bc),(ac,bc,c),(ab,bc,ac)]


def validate_cover(pieces):
    U,expected=cover()
    require(pieces==expected and len(pieces)==4,'closed midpoint partition is incomplete or incorrect')
    full=cross(subtract(U[1],U[0]),subtract(U[2],U[0]))
    for V in pieces:
        area=cross(subtract(V[1],V[0]),subtract(V[2],V[0]))
        require(area==tuple(x/4 for x in full),'midpoint piece orientation/area mismatch')
    old=h.triangle(45,10)
    a,b,c=U;oa,ob,oc=old
    require(oa==a and ob==tuple(x+F(7,9)*(y-x) for x,y in zip(a,b)) and
            oc==tuple(x+F(7,10)*(y-x) for x,y in zip(a,c)),
            'preceding triangle is not in new closed triangle')
    oldarea=cross(subtract(ob,oa),subtract(oc,oa))
    require(full==tuple(F(90,49)*x for x in oldarea),'receiver chart-area ratio failed')
    return {'whole_closed_midpoint_partition_proved':True,'pieces':4,
            'all_piece_chart_area_fractions':'1/4','preceding_triangle_contained':True,
            'unit_z_chart_area_ratio':'90/49','spherical_area_ratio_claimed':False}


def orthogonal_patch_bounds(U,r):
    old=h.patch_bounds(U,F(1))
    a=old['source_normal_chord_upper'];d=old['all_patch_receiver_chord_upper'];e=old['directional_error_upper']
    validate_small_chords(a,d,e)
    chord2=(a+d)**2+e**2
    chord=root_bounds(QPhi(chord2))
    theta=F(101,100)*chord[1]
    require(chord[1]<F(1,4) and theta<=old['full_relative_angle_upper'],
            'orthogonal angle/domain improvement failed')
    R=root_bounds(7+8*PHI)[1]
    required=R*old['all_patch_chart_norm_upper']*theta
    require(r>required and r-required>F(2,25),'actual radius insufficient for stated piece margin')
    out=dict(old)
    out['preceding_angle_sum_upper']=old['full_relative_angle_upper']
    out['preceding_required_ball_radius_upper']=old['required_uniform_ball_radius_upper']
    out['full_rotation_chord_squared_upper']=chord2
    out['full_rotation_chord_enclosure']=chord
    out['full_relative_angle_upper']=theta
    out['required_uniform_ball_radius_upper']=required
    out['strict_all_source_torque_margin_lower']=r-required
    out['old_global_perturbation_sufficient_margin']=old['uniform_origin_interior_ball_lower']-required
    out['checks']=dict(old['checks'])
    out['checks']['actual_ball_exceeds_full_relative_torque_remainder']=True
    out['checks']['orthogonal_factor_axes_proved_in_written_frame_bridge']=True
    return out


def check(piece,self_test=False):
    require(piece in range(4),'unknown receiver-cover piece')
    actual=h.fixture('actual_torque_hull_expected.json',ACTUAL_SHA)
    adaptive=h.fixture('adaptive_receiver_expected.json',h.ADAPTIVE_SHA)
    h.fixture('directional_transport_expected.json',h.PARENT_SHA)
    require(actual['global_non_rupert_proved'] is False and actual['generic_affine_torque_hull_simplex_certificate_proved'],
            'wrong published actual-hull predecessor')
    composition=composition_hypotheses()
    U,pieces=cover();partition=validate_cover(pieces)
    probes,pool,facets=h.selected_probes(adaptive)
    center=h.center_subhull(probes,pool,facets)
    r=RADII[piece];bounds=orthogonal_patch_bounds(pieces[piece],r)
    certificate=h.certify_hull(probes,pieces[piece],r)
    # Coefficients and all cases were just directly checked. Compact evidence
    # hashes the complete generated record instead of publishing its transcript.
    full_hash=hashlib.sha256(json.dumps(certificate,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    compact={k:v for k,v in certificate.items() if k!='compressed_stratum_certificates'}
    compact['complete_stratum_record_sha256']=full_hash
    require(bounds['uniform_origin_interior_ball_lower']>F(1,3),
            'whole-piece preliminary interiority not above stated bound')
    left=h.point_enclosures(U[1],U[0],h.vertices())
    require(left['normal_chord'][0]>F(1,40),'new left-corner extent not established')
    if self_test:
        h.expect_rejection(lambda:validate_perpendicular_axis((F(0),F(0),F(1)),(F(0),F(0),F(1))))
        h.expect_rejection(lambda:validate_perpendicular_axis((F(2),F(0),F(0)),(F(0),F(0),F(1))))
        h.expect_rejection(lambda:validate_small_chords(F(1,5),F(0),F(0)))
        h.expect_rejection(lambda:validate_small_chords(F(0),F(-1,100),F(0)))
        h.expect_rejection(lambda:validate_cover(pieces[:-1]))
        bad=list(pieces);bad[2]=tuple(reversed(bad[2]))
        h.expect_rejection(lambda:validate_cover(bad))
        h.expect_rejection(lambda:orthogonal_patch_bounds(pieces[piece],F(1,10)))
        h.expect_rejection(lambda:h.verify_fixture_bytes(b'{}',ACTUAL_SHA))
    return rational_strings({'agent':'six-rupert-3','role':'researcher',
        'proof_status':'unformalized_orthogonal_composition_and_closed_piece_hull_theorem',
        'global_non_rupert_proved':False,'piece_index':piece,
        'this_whole_closed_piece_excludes_all_sources':True,
        'all_four_piece_hull_replays_required_for_complete_receiver_cover':True,
        'arbitrary_source_orientation_roll_translation_scale_ge_one':True,
        'receiver_triangle':'B; (0,phi^-2-1/35,1); (6/7)B+(1/7)D',
        'closed_piece_vertices':[h.encode(v) for v in pieces[piece]],
        'actual_ball_radius_for_this_piece':r,'strict_piece_margin_greater_than':'2/25',
        'left_corner_normal_chord_greater_than':'1/40','composition':composition,
        'midpoint_cover':partition,'persistent_probe_corner_support_checks':1800,
        'center_subhull':center,'phase_and_interior_bounds':bounds,
        'whole_piece_facet_certificate':compact,'new_malformed_controls_rejected':8 if self_test else 0,
        'pinned_actual_expected_sha256':ACTUAL_SHA,'pinned_adaptive_expected_sha256':h.ADAPTIVE_SHA,
        'pinned_directional_expected_sha256':h.PARENT_SHA,
        'full_parent_replay_is_separate_and_not_performed_here':True})


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--piece',type=int,choices=range(4),required=True)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    print(json.dumps(check(args.piece,args.self_test),indent=2,sort_keys=True))
