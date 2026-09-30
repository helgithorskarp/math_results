#!/usr/bin/env python3
"""Exact normalized common-support hypotheses for full all-source1/64caps.

Python3.11+, standard library, Q(sqrt(5))/Fraction. Complete continuous
geometry and quantified scope: normalized_cap_proof.md. No floating proof
decisions, sampled cap cover, solver status or hidden polyhedral corpus.
"""
import argparse,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
from verify import Q5,PHI,ZERO,vec,vertices,dot,cross,sub,add,mul,cyclic_signed
from orientation_certificate import canonical_plane,determinant,CHAMBER,area_twice
from adaptive_area_certificate import parse
from global_area_certificate import reflection,mv
from directional_area_certificate import check as check_parent
from closed_cell7_certificate import grid_upper,COERCIVITY
from stable_certificate import orbit

if not __debug__:
    raise RuntimeError('verification requires assertions; do not use python -O')

CLOSED_CELL7_SHA256='f9c4331a63cc957b0d690d7067cacee1ca645b23d546e2467f775d9da5814f2c'
CLOSED_CHECKER_SHA256='8dd5b363092d120c30f3538bc0b82838145eaa6ea0d341d40d033c907e6fb211'
CAP=F(1,64)
AREA_TANGENT=F(393,200)
TORQUE_LIPSCHITZ=F(71,10)
CENTER_BALL=F(1,4)
FULL_ANGLE=F(129,1000)
CONTACTS=((59,55,59),(59,55,55),(55,58,55),(55,58,58),(58,45,58),(58,45,45),
          (45,34,45),(45,34,34),(34,36,34),(34,36,36),(36,20,36),(36,20,20))
ORIGIN_STRESS=(1,3,8,10)
TRIPLES=tuple(itertools.combinations(range(12),3))

def digest(x):
    return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

def new_receiver_witness(parent,M,nodes):
    inds=parent['cell_certificates'][4]['corner_indices']
    center=vec(sum((nodes[j][k] for j in inds),ZERO)/len(inds) for k in range(3))
    u=add(M,mul(F(1,100),sub(center,M)))
    assert dot(sub(u,M),sub(u,M))<Q5(CAP*CAP)
    poly=[nodes[j] for j in inds];sign=area_twice(poly).sign();assert sign!=0
    assert all((cross(sub(b,a),sub(u,a))[2]*sign).sign()>0
               for a,b in zip(poly,poly[1:]+poly[:1]))
    a,b,c=M,nodes[7],nodes[8];det=determinant(a,b,c);assert det.sign()!=0
    images=orbit(u);assert len(images)==60
    for v in images:
        coordinates=(determinant(v,b,c)/det,determinant(a,v,c)/det,determinant(a,b,v)/det)
        assert not (all(x.sign()>=0 for x in coordinates) or
                    all(x.sign()<=0 for x in coordinates))
    return {'ray':list(map(str,u)),'strict_inside_cell':4,
            'cap_chord_upper_by_unit_z_normalization':'1/64',
            'complete_projective_reflection_orbit':len(images),
            'images_in_previous_closed_cell7_cone':0}

def finite(parent,*,cap=CAP,area_tangent=AREA_TANGENT,
           torque_lipschitz=TORQUE_LIPSCHITZ,center_ball=CENTER_BALL,
           full_angle=FULL_ANGLE,contacts=CONTACTS,origin_stress=ORIGIN_STRESS,
           triples=TRIPLES,omit_receiver_remainder=False):
    assert 0<cap<=F(1,20) and area_tangent>0 and torque_lipschitz>0
    assert center_ball>0 and full_angle>0
    V=vertices();nodes=[vec(map(parse,x['ray'])) for x in parent['corner_areas']]
    M=nodes[9];M2=dot(M,M);qmin=parse(parent['global_minimum_area_squared'])
    assert len(contacts)==12 and len(set(contacts))==12
    assert len(triples)==220 and set(triples)==set(TRIPLES)
    # Recheck the13new source tangent-gap comparisons from the closed-cell
    # parent, while the complete directional/global/adaptive chain is replayed.
    cosine=F(2399,2601);ratio=F(51,50);assert 2/(1+cosine)==ratio*ratio
    for u in CHAMBER:
        mp=dot(M,u);assert mp.sign()>0
        assert mp*mp>cosine*cosine*M2*dot(u,u)
    corner_margins=[]
    for j,u in enumerate(nodes):
        if j==9:continue
        q=parse(parent['corner_areas'][j]['physical_area_squared'])
        tangent2=Q5(1)-dot(M,u)**2/(M2*dot(u,u));assert tangent2.sign()>0
        d2=ratio*ratio*tangent2/(COERCIVITY*COERCIVITY)
        left=q-qmin-d2
        assert left.sign()>0 and left*left>4*qmin*d2
        corner_margins.append({'corner':j,'positive_root_branch_left':str(left),
                              'squared_margin':str(left*left-4*qmin*d2)})
    assert len(corner_margins)==13 and COERCIVITY==F(21,8)
    wall=vec((-PHI,-PHI**2,1));H=reflection(wall)
    assert dot(wall,M)==ZERO and mv(H,M)==M
    assert {mv(H,v) for v in V}==set(V)
    coordinate_margins=[]
    for x in M:
        assert x.sign()>0 and x*x>cap*cap*M2
        coordinate_margins.append(str(x*x-cap*cap*M2))
    normals=set().union(*(cyclic_signed(vec(t)) for t in
        [(1,1,PHI**3),(PHI,2*PHI,PHI**2),(0,PHI**2,2+PHI)]))
    assert len(normals)==60
    planes=sorted(set(canonical_plane(n) for n in normals));assert len(planes)==30
    through=[];nonzero=[]
    for k,w in enumerate(planes):
        p=dot(w,M)
        if p==ZERO:through.append(k);continue
        margin=p*p-cap*cap*M2*dot(w,w);assert margin.sign()>0
        nonzero.append({'plane':k,'squared_distance_margin':str(margin)})
    assert len(through)==2 and len(nonzero)==28
    witnesses=[]
    for c in parent['cell_certificates']:
        if c['cell'] in [4,7,9]:continue
        found=[i for i,w in enumerate(planes) if dot(w,M)!=ZERO and
               all((dot(w,nodes[k])*dot(w,M).sign()).sign()<=0 for k in c['corner_indices'])]
        assert found
        witnesses.append({'excluded_closed_cell':c['cell'],'separating_plane':found[0]})
    assert len(witnesses)==9
    Drecords=[];support=0
    for i in [4,7,9]:
        c=parent['cell_certificates'][i];C=vec(map(parse,c['area_vector']))
        D=sub(C,mul(dot(C,M)/M2,M))
        assert dot(D,M)==ZERO and dot(D,D)<Q5(area_tangent*area_tangent)
        assert dot(C,M).sign()>0 and dot(C,M)**2/M2==qmin
        Drecords.append({'cell':i,'tangent_squared':str(dot(D,D)),
                         'tangent_bound_squared_margin':str(Q5(area_tangent**2)-dot(D,D))})
        for k in c['corner_indices']:
            for a,b,j in contacts:
                assert a!=b and j in (a,b)
                mu=cross(sub(V[b],V[a]),nodes[k])
                for v in V:
                    assert dot(mu,sub(V[j],v)).sign()>=0;support+=1
    assert support==7440
    points=[];scalings=[]
    for a,b,j in contacts:
        edge=sub(V[b],V[a]);mu=cross(edge,M)
        K2=dot(V[j],V[j])*dot(mu,mu)/(4*M2)
        L2=dot(V[j],V[j])*dot(edge,edge)/4
        assert K2.sign()>0 and L2.sign()>0
        K=grid_upper(lambda x:Q5(x*x)>K2,F(3))
        L=grid_upper(lambda x:Q5(x*x)>L2,F(3))
        B=K+(0 if omit_receiver_remainder else L*cap)
        assert B>=K+L*cap
        torque_margin=Q5(torque_lipschitz**2*B*B)-4*L2
        assert torque_margin.sign()>0
        points.append(mul(1/B,cross(V[j],mu)))
        scalings.append({'contact':[a,b,j],'center_remainder_upper':str(K),
                         'remainder_Lipschitz_upper':str(L),'scaling_denominator':str(B),
                         'torque_Lipschitz_squared_margin':str(torque_margin)})
    assert len(set(points))==12
    assert len(origin_stress)==4 and len(set(origin_stress))==4
    T=[points[i] for i in origin_stress]
    weights=[-(-1)**j*determinant(*[T[k] for k in range(4) if k!=j]) for j in range(4)]
    assert all(x.sign()>0 for x in weights)
    assert all(sum((weights[j]*T[j][k] for j in range(4)),ZERO)==ZERO for k in range(3))
    facets={};collinear=0;side_checks=0;supporting_triples=0
    for ids in triples:
        x,y,z=[points[j] for j in ids];n=cross(sub(y,x),sub(z,x))
        if dot(n,n)==ZERO:collinear+=1;continue
        h=dot(n,x)
        if h.sign()<0:n=mul(-1,n);h=-h
        signs=[(dot(n,p)-h).sign() for p in points];side_checks+=len(points)
        if not all(s<=0 for s in signs):continue
        assert h.sign()>0
        canonical=mul(1/h,n);key=tuple(canonical)
        margin=h*h-center_ball*center_ball*M2*dot(n,n);assert margin.sign()>0
        ties=[j for j,s in enumerate(signs) if s==0];assert len(ties)>=3
        facets[key]={'vertex_indices':ties,'normal_offset_one':list(map(str,canonical)),
                     'physical_distance_squared':str(h*h/(M2*dot(n,n)))}
        supporting_triples+=1
    assert facets
    facets=[facets[k] for k in sorted(facets)]
    a=COERCIVITY*area_tangent*cap
    E0=F(29,100)*(a+cap)+F(23,20)*(a*a+cap*cap)
    E=F(29,100)*a+F(141,200)*cap+F(23,20)*(a*a+cap*cap)
    b=2*E;X2=(a+cap)**2+b*b
    assert a<=F(1,10) and E0<=F(1,28) and b<=F(1,10) and X2<=F(3,20)**2
    assert F(1003,1000)**2*(1-F(3,20)**2/4)>1
    assert F(1003,1000)**2*X2<full_angle*full_angle
    lower=center_ball-torque_lipschitz*cap;margin=lower-full_angle
    assert margin>F(1,100)
    return {'agent':'six-rupert-1','role':'researcher',
            'status':'exact finite hypotheses with complete written unformalized proof',
            'global_Rupert_property':'unresolved','independent_review':'not asserted',
            'arithmetic':'Q(sqrt(5))/Fraction, Python3.11+ standard library; no floating proof decisions',
            'parent_closed_cell7_expected_sha256':CLOSED_CELL7_SHA256,
            'cap_chord_radius':str(cap),'global_source_normal_coercivity':str(COERCIVITY),
            'receiver_tangent_area_constant':str(area_tangent),
            'receiver_cap_area_excess_upper':str(area_tangent*cap),
            'source_corner_root_gap_comparisons':corner_margins,
            'receiver_wall_reflection_vertex_permutations':62,'receiver_wall_fixes_center':True,
            'cap_coordinate_positive_squared_margins':coordinate_margins,
            'center_cutplanes_through':through,'nonzero_center_plane_comparisons':nonzero,
            'nonincident_closed_cell_witnesses':witnesses,'area_tangent_comparisons':Drecords,
            'common_actual_weak_support_comparisons':support,
            'selected_original_contacts':[list(x) for x in contacts],
            'outward_rational_grid_denominator':1000000,'support_scalings':scalings,
            'normalized_torque_Lipschitz_upper':str(torque_lipschitz),
            'positive_origin_stress_vertices':list(origin_stress),
            'positive_origin_stress_weights':list(map(str,weights)),
            'identically_zero_origin_balance_coordinates':3,
            'complete_center_triple_count':len(triples),'collinear_triples':collinear,
            'center_point_side_comparisons':side_checks,'supporting_center_triples':supporting_triples,
            'distinct_center_facet_count':len(facets),'center_facets':facets,
            'center_facet_sha256':digest(facets),'center_normalized_torque_ball_lower':str(center_ball),
            'receiver_cap_normalized_torque_ball_lower':str(lower),
            'source_chord_upper':str(a),'remote_radial_error_upper':str(E0),
            'roll_chord_upper':str(b),'composition_squared_upper':str(X2),
            'full_gauged_angle_upper':str(full_angle),'uniform_normalized_rotation_remainder_margin':str(margin),
            'closed_containment_classification':'lambda1,t0,Q in G union J_nG; exactly120proper rotations, two disjoint LEFT cosets',
            'receiver_scope':'whole closed chord1/64caps about all60directed minimizing normals/30axes; boundaries included',
            'source_scope':'every original proper rotation, full angle, roll, planar translation and scale>=1',
            'cap_radius_factor_over_original_global_caps':'312500',
            'new_receiver_outside_all_previous_cell7_images':new_receiver_witness(parent,M,nodes)}

def negative_tests(parent):
    reversed_contact=list(CONTACTS);a,b,j=reversed_contact[0];reversed_contact[0]=(b,a,j)
    controls=[('unsupported cap1/63 with fixed source envelope',{'cap':F(1,63)}),
              ('false area tangent49/25',{'area_tangent':F(49,25)}),
              ('false normalized center ball13/50',{'center_ball':F(13,50)}),
              ('false torque Lipschitz69/10',{'torque_lipschitz':F(69,10)}),
              ('missing center triple',{'triples':TRIPLES[1:]}),
              ('reversed original support',{'contacts':tuple(reversed_contact)}),
              ('repeated origin stress point',{'origin_stress':(1,3,3,10)}),
              ('missing receiver remainder increment',{'omit_receiver_remainder':True})]
    rejected=[]
    for name,kwargs in controls:
        try:finite(parent,**kwargs)
        except AssertionError:rejected.append(name)
        else:raise AssertionError('malformed certificate accepted: '+name)
    return rejected

def check(self_test=False):
    root=Path(__file__).parent
    raw=(root/'expected_closed_cell7.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==CLOSED_CELL7_SHA256
    assert hashlib.sha256((root/'closed_cell7_certificate.py').read_bytes()).hexdigest()==CLOSED_CHECKER_SHA256
    closed=json.loads(raw);assert closed['global_source_normal_coercivity']=='21/8'
    parent_directional=check_parent()
    old=json.loads((root/'expected_directional_area.json').read_text())
    assert len(old.pop('malformed_controls_rejected'))==10 and parent_directional==old
    parent=json.loads((root/'expected_global_area.json').read_text())
    result=finite(parent)
    if self_test:result['malformed_controls_rejected']=negative_tests(parent)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--self-test',action='store_true')
    args=p.parse_args();print(json.dumps(check(args.self_test),indent=2))
