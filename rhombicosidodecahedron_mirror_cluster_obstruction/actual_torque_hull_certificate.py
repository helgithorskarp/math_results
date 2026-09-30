#!/usr/bin/env python3
"""Exact hypotheses for ACTUAL_TORQUE_HULL_PROOF.md, Python 3.11+ stdlib.

Regenerates a ten-probe center subhull and certifies its actual torque ball
over a closed receiver triangle. Every possible facet triple is covered on
all seven simplex strata by exact homogeneous polynomial coefficients.
The source/roll reduction is the published directional parent theorem;
its full checker is a separate reproducibility command, not a hidden input.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from verify import PHI,QPhi,ZERO,dot,vertices,require
from torque_certificate import cross,subtract,determinant
from cell_certificate import geometry,decode,encode
from global_cap_certificate import expect_rejection
from adaptive_receiver_certificate import root_bounds,point_enclosures,rational_strings

PARENT_SHA='cda8f8555f21e41b412478adb776416a9161828e53f5dce77f51376adc250b33'
ADAPTIVE_SHA='53c852471e2d787b8958f01cc6f6e1b5c210ce3ee2b3a524ddbe1a59e9514e98'
FACES=[f for s in (3,2,1) for f in combinations(range(3),s)]
UNITS=[tuple(int(i==j) for i in range(3)) for j in range(3)]


def add(p,q):
    r=dict(p)
    for k,v in q.items():
        r[k]=r.get(k,ZERO)+v
        if r[k]==ZERO:
            del r[k]
    return r


def scale(p,q):
    return {k:v*q for k,v in p.items() if v*q!=ZERO}


def mul(p,q):
    r={}
    for a,x in p.items():
        for b,y in q.items():
            k=tuple(i+j for i,j in zip(a,b))
            r[k]=r.get(k,ZERO)+x*y
    return {k:v for k,v in r.items() if v!=ZERO}


def pdot(v,w):
    r={}
    for p,q in zip(v,w):
        r=add(r,mul(p,q))
    return r


def pcross(v,w):
    return tuple(add(mul(v[i],w[j]),scale(mul(v[j],w[i]),-1))
                 for i,j in ((1,2),(2,0),(0,1)))


def psub(v,w):
    return tuple(add(p,scale(q,-1)) for p,q in zip(v,w))


def evaluate(p,lam):
    result=ZERO
    for k,v in p.items():
        for j in range(3):
            v=v*(lam[j]**k[j])
        result=result+v
    return result


def validate_homogeneous(p,degree):
    require(all(len(k)==3 and all(isinstance(j,int) and j>=0 for j in k)
                and sum(k)==degree and isinstance(v,QPhi) and v!=ZERO
                for k,v in p.items()), 'invalid homogeneous Q(phi) polynomial')


def validate_faces(faces):
    require(faces==FACES and len(set(faces))==7, 'all seven canonical simplex strata required')


def restrict(p,face):
    return {k:v for k,v in p.items() if all(k[j]==0 for j in range(3) if j not in face)}


def interior_sign(p,face):
    r=restrict(p,face)
    if not r:
        return 0
    signs={v.sign() for v in r.values()}
    return next(iter(signs)) if len(signs)==1 else 0


def nonnegative(p,face):
    return all(v>=0 for v in restrict(p,face).values())


def verify_case(n,gaps,P,face,kind,witness=()):
    require(face in FACES, 'unknown simplex stratum')
    if kind=='opposite':
        require(len(witness)==2 and all(0<=j<len(gaps) for j in witness), 'invalid nonfacet witnesses')
        require(interior_sign(gaps[witness[0]],face)==1 and
                interior_sign(gaps[witness[1]],face)==-1,
                'opposite gaps are not strict throughout this relative interior')
    elif kind=='degenerate':
        require(all(not restrict(p,face) for p in n), 'triple not identically degenerate on stratum')
    elif kind=='distance':
        require(nonnegative(P,face), 'facet distance polynomial has a negative coefficient')
    else:
        raise ValueError('unknown facet-certificate case')


def classify(n,gaps,P,face):
    pos=next((j for j,p in enumerate(gaps) if interior_sign(p,face)==1),None)
    neg=next((j for j,p in enumerate(gaps) if interior_sign(p,face)==-1),None)
    if pos is not None and neg is not None:
        kind,witness='opposite',(pos,neg)
    elif all(not restrict(p,face) for p in n):
        kind,witness='degenerate',()
    elif nonnegative(P,face):
        kind,witness='distance',()
    else:
        raise ValueError('no complete facet certificate for triple/stratum')
    verify_case(n,gaps,P,face,kind,witness)
    return kind,witness


def verify_fixture_bytes(data,digest):
    require(hashlib.sha256(data).hexdigest()==digest, 'pinned parent finite output changed')


def fixture(name,digest):
    data=Path(__file__).with_name(name).read_bytes()
    verify_fixture_bytes(data,digest)
    return json.loads(data)


def selected_probes(data):
    B=geometry()[0][0][1]
    pool=[(decode(p['vertex']),decode(p['edge'])) for p in data['persistent_probes']]
    require(len(pool)==36 and len(set(pool))==36, 'complete persistent endpoint pool required')
    facets=[decode(q) for q in data['complete_center_facet_normals']]
    center={}
    for v,e in pool:
        center.setdefault(cross(v,cross(e,B)),(v,e))
    require(len(center)==18, 'center full torque cardinality changed')
    selected=[]
    for t,p in sorted(center.items()):
        active=[q for q in facets if dot(q,t)==QPhi(1)]
        if any(determinant(*triple)!=ZERO for triple in combinations(active,3)):
            selected.append(p)
    validate_probes(selected)
    return selected,pool,set(facets)


def validate_probes(probes):
    V=vertices()
    U=geometry()[0][0]
    require(len(probes)==10 and len(set(probes))==10, 'ten distinct persistent representative probes required')
    for v,e in probes:
        require(v in V and dot(e,e)==QPhi(4), 'nonstandard original vertex or edge')
        require(tuple(x+y for x,y in zip(v,e)) in V or subtract(v,e) in V,
                'support edge has no original second endpoint')
        for u in U:
            require(all(dot(cross(e,u),subtract(v,w))>=0 for w in V),
                    'representative support fails on closed ABD')


def center_subhull(probes,pool,expected_facets):
    B=geometry()[0][0][1]
    T=sorted({cross(v,cross(e,B)) for v,e in probes})
    require(len(T)==10, 'distinct center torque representatives required')
    stress=None
    for quad in combinations(T,4):
        cof=[(-1)**j*determinant(*(quad[k] for k in range(4) if k!=j)) for j in range(4)]
        if all(q>0 for q in cof) or all(q<0 for q in cof):
            if cof[0]<0:
                cof=[-q for q in cof]
            require(all(sum((cof[j]*quad[j][k] for j in range(4)),ZERO)==ZERO
                        for k in range(3)), 'center positive stress fails to balance')
            stress={'points':[encode(t) for t in quad],'positive_cofactors':[q.encode() for q in cof]}
            break
    require(stress is not None, 'center subhull origin interiority not established')
    facets=set()
    checks=0
    for a,b,c in combinations(T,3):
        n=cross(subtract(b,a),subtract(c,a))
        require(dot(n,n)>0, 'unexpected degenerate center representative triple')
        h=dot(n,a)
        gaps=[dot(n,t)-h for t in T]
        checks+=len(gaps)
        if all(g<=0 for g in gaps):
            require(h>0, 'center support contradicts positive stress')
            facets.add(tuple(q/h for q in n))
        elif all(g>=0 for g in gaps):
            require(h<0, 'reversed center support contradicts positive stress')
            facets.add(tuple(q/h for q in n))
    require(len(facets)==15 and facets==expected_facets and checks==1200,
            'center representative hull differs from the complete center hull')
    require(all(dot(q,cross(v,cross(e,B)))<=QPhi(1) for q in facets for v,e in pool),
            'center representative hull omits a persistent center torque')
    require(all(QPhi(1)/dot(q,q)>=2-PHI for q in facets), 'center ball radius overestimated')
    require((PHI,ZERO,ZERO) in facets, 'sharp center facet missing')
    return {'representative_torque_points':10,'regenerated_center_facets':15,
            'center_triples':120,'center_support_checks':checks,
            'full_pool_center_support_checks':15*36,
            'center_subhull_equals_complete_center_hull':True,
            'center_sharp_ball_radius':'phi-1','positive_interior_stress':stress}


def triangle(k=45,q=10):
    A,B,D=geometry()[0][0]
    L=(ZERO,B[1]-QPhi(F(1,k)),QPhi(1))
    C=tuple((1-F(1,q))*b+F(1,q)*d for b,d in zip(B,D))
    return B,L,C


def patch_bounds(U,r):
    require(len(U)==3 and len(set(U))==3 and r>0, 'complete nondegenerate triangle and positive ball required')
    A,B,D=geometry()[0][0]
    area=cross(subtract(U[1],U[0]),subtract(U[2],U[0]))
    require(dot(area,area)>0, 'receiver triangle has zero chart area')
    barycentric=[]
    for u in U:
        require(u[2]==QPhi(1), 'receiver corner outside unit-z chart')
        wD=u[0]/D[0]
        wB=(u[1]-wD*D[1])/B[1]
        wA=1-wB-wD
        require(min(wA,wB,wD)>=0, 'receiver triangle outside closed ABD')
        barycentric.append([q.encode() for q in (wA,wB,wD)])
    data=[point_enclosures(u,B,vertices()) for u in U]
    lower=min(p['axial_value'][0] for p in data)
    delta=max(p['normal_chord'][1] for p in data)
    chart=max(p['chart_norm'][1] for p in data)
    drift=max(p['chart_displacement'][1] for p in data)
    R=root_bounds(7+8*PHI)[1]
    c0=root_bounds(QPhi(F(1,3)))[1]
    k=root_bounds(QPhi(F(5,3)))[1]
    a=F(101,200)*(c0-lower)
    E=c0*a+k*delta+R*(a*a+delta*delta)/2
    theta=F(101,100)*(a+delta+E)
    required=R*chart*theta
    interior=root_bounds(2-PHI)[0]-2*R*drift
    checks={'corner_barycentric_coordinates_nonnegative':True,
            'common_sixty_strict_axial_signs':all(p['all_sixty_axial_signs_match_center'] for p in data),
            'axial_lower_clears_nonoptimal_region_gap':QPhi(lower*lower)>(19-8*PHI)/29,
            'source_deficit_nonnegative':a>=0,
            'positive_normal_cap_cone_coefficient':1-delta*delta/2>0,
            'receiver_chord_within_directional_height_gap_audit':delta<=F(1,2),
            'directional_error_within_roll_threshold':E<=F(77,1000),
            'all_factor_chords_below_one_tenth':max(a,delta,E)<F(1,10),
            'full_relative_angle_below_one':theta<1,
            'uniform_origin_interiority':interior>0,
            'actual_ball_exceeds_full_relative_torque_remainder':r>required}
    require(all(checks.values()), 'actual-hull receiver phase or margin criterion fails')
    return {'corners':data,'corner_barycentric_coordinates_in_ABD':barycentric,
            'all_patch_axial_value_lower':lower,'all_patch_receiver_chord_upper':delta,
            'all_patch_chart_norm_upper':chart,'all_patch_chart_drift_upper':drift,
            'source_normal_chord_upper':a,'directional_error_upper':E,
            'full_relative_angle_upper':theta,'required_uniform_ball_radius_upper':required,
            'uniform_origin_interior_ball_lower':interior,'strict_all_source_torque_margin_lower':r-required,
            'old_global_perturbation_sufficient_margin':interior-required,'checks':checks}


def polynomial_torques(probes,U):
    result=[]
    for v,e in probes:
        values=[cross(v,cross(e,u)) for u in U]
        result.append(tuple({UNITS[s]:values[s][i] for s in range(3) if values[s][i]!=ZERO}
                            for i in range(3)))
    for T in result:
        for p in T:
            validate_homogeneous(p,1)
    return result


def encode_polynomial(p):
    return [[list(k),v.encode()] for k,v in sorted(p.items())]


def certify_hull(probes,U,r,arithmetic_audit=True):
    require(r>0 and len(probes)==10 and len(U)==3, 'invalid facet-certificate inputs')
    validate_faces(FACES)
    T=polynomial_torques(probes,U)
    sumlam={k:QPhi(1) for k in UNITS}
    sumlam2=mul(sumlam,sumlam)
    nodes=[tuple(F(i==j) for i in range(3)) for j in range(3)]+[(F(1,2),F(1,3),F(1,6))]
    direct=[]
    if arithmetic_audit:
        for lam in nodes:
            u=tuple(sum((lam[j]*U[j][k] for j in range(3)),ZERO) for k in range(3))
            direct.append([cross(v,cross(e,u)) for v,e in probes])
    counts={'opposite':0,'distance':0,'degenerate':0}
    records=[]
    coefficients=hashlib.sha256()
    for triple in combinations(range(10),3):
        a,b,c=[T[j] for j in triple]
        n=pcross(psub(b,a),psub(c,a))
        h=pdot(n,a)
        gaps=[add(pdot(n,t),scale(h,-1)) for t in T]
        P=add(mul(h,h),scale(mul(pdot(n,n),sumlam2),-r*r))
        for p in n:
            validate_homogeneous(p,2)
        validate_homogeneous(h,3)
        for p in gaps:
            validate_homogeneous(p,3)
        validate_homogeneous(P,6)
        for p in (*n,h,*gaps,P):
            coefficients.update(json.dumps(encode_polynomial(p),separators=(',',':')).encode())
        if arithmetic_audit:
            for lam,actual in zip(nodes,direct):
                a0,b0,c0=[actual[j] for j in triple]
                n0=cross(subtract(b0,a0),subtract(c0,a0))
                h0=dot(n0,a0)
                require(tuple(evaluate(p,lam) for p in n)==n0 and evaluate(h,lam)==h0,
                        'coefficient construction differs from direct normal/support arithmetic')
                require(all(evaluate(p,lam)==dot(n0,t)-h0 for p,t in zip(gaps,actual)),
                        'coefficient construction differs from direct support-gap arithmetic')
                require(evaluate(P,lam)==h0*h0-r*r*dot(n0,n0),
                        'homogenized squared facet-distance identity fails')
        groups={}
        distance_mask=degenerate_mask=0
        for index,face in enumerate(FACES):
            kind,witness=classify(n,gaps,P,face)
            counts[kind]+=1
            if kind=='distance':
                distance_mask|=1<<index
            elif kind=='degenerate':
                degenerate_mask|=1<<index
            else:
                groups[witness]=groups.get(witness,0)|(1<<index)
        require((distance_mask|degenerate_mask|sum(groups.values()))==127,
                'compressed certificate does not cover all seven strata')
        records.append({'triple':triple,'distance_face_mask':distance_mask,
                        'degenerate_face_mask':degenerate_mask,
                        'opposite_gap_witnesses':[[mask,*w] for w,mask in sorted(groups.items())]})
    require(len(records)==120 and sum(counts.values())==840, 'incomplete possible-facet/stratum enumeration')
    return {'all_possible_actual_facet_triples':120,'simplex_strata':FACES,
            'triple_strata_certified':840,'classifications':counts,
            'all_triples_and_closed_boundaries_covered':True,
            'homogeneous_polynomial_coefficients_sha256':coefficients.hexdigest(),
            'arithmetic_audit_nodes':4 if arithmetic_audit else 0,
            'direct_normal_support_audits':480 if arithmetic_audit else 0,
            'direct_support_gap_audits':4800 if arithmetic_audit else 0,
            'direct_homogenized_distance_audits':480 if arithmetic_audit else 0,
            'compressed_stratum_certificates':records}


def check(self_test=False):
    parent=fixture('directional_transport_expected.json',PARENT_SHA)
    adaptive=fixture('adaptive_receiver_expected.json',ADAPTIVE_SHA)
    require(parent['inherited_adaptive_expected_sha256']==ADAPTIVE_SHA and
            parent['global_non_rupert_proved'] is False, 'wrong directional predecessor')
    probes,pool,facets=selected_probes(adaptive)
    center=center_subhull(probes,pool,facets)
    U=triangle()
    r=F(3,5)
    bounds=patch_bounds(U,r)
    certificate=certify_hull(probes,U,r)
    oldB,oldL,oldC=triangle(60,20)
    B,L,C=U
    require(oldB==B and oldL==tuple(b+F(3,4)*(l-b) for b,l in zip(B,L)) and
            oldC==tuple(b+F(1,2)*(c-b) for b,c in zip(B,C)),
            'previous receiver triangle is not inside the new triangle')
    newarea=cross(subtract(L,B),subtract(C,B))
    oldarea=cross(subtract(oldL,B),subtract(oldC,B))
    require(newarea==tuple(F(8,3)*q for q in oldarea), 'stated chart-area enlargement fails')
    require(bounds['strict_all_source_torque_margin_lower']>F(1,30) and
            bounds['corners'][1]['normal_chord'][0]>F(1,52) and
            bounds['uniform_origin_interior_ball_lower']>F(2,5) and
            bounds['old_global_perturbation_sufficient_margin']<0,
            'stated region margin, extent, interiority or prior sufficient failure fails')
    if self_test:
        expect_rejection(lambda:validate_probes(probes[:-1]))
        bad=list(probes)
        v,e=bad[0]
        bad[0]=(v,tuple(-q for q in e))
        expect_rejection(lambda:validate_probes(bad))
        bad[0]=(tuple(2*q for q in v),e)
        expect_rejection(lambda:validate_probes(bad))
        expect_rejection(lambda:validate_faces(FACES[:-1]))
        expect_rejection(lambda:validate_homogeneous({(1,0,0):QPhi(1),(0,0,0):QPhi(1)},1))
        pos={(1,0,0):QPhi(1)}
        mixed={(1,0,0):QPhi(1),(0,1,0):QPhi(-1)}
        expect_rejection(lambda:verify_case((pos,{},{}),[mixed,scale(pos,-1)],{},FACES[0],'opposite',(0,1)))
        expect_rejection(lambda:verify_case((pos,{},{}),[pos,scale(pos,-1)],{},(1,),'opposite',(0,1)))
        expect_rejection(lambda:verify_case((pos,{},{}),[],{(6,0,0):QPhi(-1)},FACES[0],'distance'))
        expect_rejection(lambda:verify_case((pos,{},{}),[],{},(0,),'degenerate'))
        expect_rejection(lambda:certify_hull(probes,U,F(7,10),False))
        expect_rejection(lambda:patch_bounds(U,F(1,10)))
        expect_rejection(lambda:patch_bounds(triangle(20,10),r))
        expect_rejection(lambda:verify_fixture_bytes(b'{}',PARENT_SHA))
    return rational_strings({
        'agent':'six-rupert-3','role':'researcher',
        'proof_status':'unformalized_analytic_theorem_with_exact_whole_simplex_facet_certificate',
        'global_non_rupert_proved':False,'whole_closed_receiver_triangle_excludes_all_sources':True,
        'arbitrary_source_orientation_roll_translation_scale_ge_one':True,
        'actual_torque_receiver_criterion_proved':True,
        'generic_affine_torque_hull_simplex_certificate_proved':True,
        'receiver_triangle':'B; (0,phi^-2-1/45,1); (9/10)B+(1/10)D',
        'certified_uniform_actual_torque_ball_radius':r,
        'contains_entire_previous_receiver_triangle':True,
        'unit_z_chart_area_ratio_to_previous_triangle':'8/3','spherical_area_ratio_claimed':False,
        'normal_at_second_corner_chord_greater_than':'1/52','strict_torque_margin_greater_than':'1/30',
        'center_representative_subhull':center,
        'persistent_representative_probes':[{'vertex':encode(v),'edge':encode(e)} for v,e in probes],
        'all_representative_original_vertex_corner_support_checks':10*3*60,
        'whole_patch_phase_and_interior_bounds':bounds,'affine_hull_facet_certificate':certificate,
        'new_malformed_controls_rejected':13 if self_test else 0,
        'full_directional_parent_replay_is_separate_command':True,
        'pinned_directional_parent_expected_sha256':PARENT_SHA,
        'pinned_adaptive_expected_sha256':ADAPTIVE_SHA,
        'parent_graph':'bafkreihl44hhtwxjrezrxurevchfwpfgkeojhbl2ctkimksjg4efia346u',
        'adaptive_graph':'bafkreicsflhs33t2yft342slfzk46vnr55unjj3uf6pnmsaxmtgum6rvz4'})


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    print(json.dumps(check(args.self_test),indent=2,sort_keys=True))
