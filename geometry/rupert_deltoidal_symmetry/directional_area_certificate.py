#!/usr/bin/env python3
"""Exact hypotheses for directional transports and a whole half-cell7 cover.

Python3.11+, standard library, Q(sqrt(5))/Fraction only. The continuous
geometric proof and quantified scope are in directional_area_proof.md.
"""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from verify import Q5,ZERO,vec,vertices,dot,cross,sub,add,mul
from orientation_certificate import (CHAMBER,CERTIFICATES,EXPONENTS,
                                    cofactor_coefficients,area_twice)
from adaptive_area_certificate import (parse,finite as adaptive_finite,
                                      PARENT_SHA256,ROLL_PROBES)
from global_area_certificate import check as check_parent,root_gap_greater

if not __debug__:
    raise RuntimeError('verification requires assertions; do not use python -O')

ADAPTIVE_SHA256='dde9d3de82405fb3c37c00a23bff651f960e608e3eb3511dac43880aa8f42067'
COSINE=F(2399,2601)
CHORD_OVER_TANGENT=F(51,50)
COERCIVITY=F(153,50)
DELTA_GATE=F(1,20)
RADIAL_GATE=F(1,28)
BODY_RADIUS=F(23,10)
SOURCE_HEIGHT=F(29,100)
EDGE_HEIGHT=F(141,200)
PATCH_MIX=F(1,2)
PATCH_DRIFT=F(239,10000)
PATCH_NORM_LOWER=F(21,20)
PATCH_NORM_UPPER=F(53,50)
PATCH_AREA_EXCESS=F(153,10000)
PATCH_ROLL_CHORD=F(17,250)
PATCH_FULL_ANGLE=F(1,10)
TORQUE_BALL=F(43,250)
DEGREE6=sorted((i,j,6-i-j) for i in range(7) for j in range(7-i))

def serial(v):return list(map(str,v))

# Sparse exact homogeneous polynomials. They reconstruct the finite
# certificate; hashes summarize the coefficients, not a hidden input.
def clean(p):return {e:x for e,x in p.items() if x!=ZERO}
def padd(a,b):
    out=dict(a)
    for e,x in b.items():out[e]=out.get(e,ZERO)+x
    return clean(out)
def pscale(a,x):return clean({e:y*x for e,y in a.items()})
def pmul(a,b):
    out={}
    for e,x in a.items():
        for f,y in b.items():
            assert len(e)==len(f)
            g=tuple(i+j for i,j in zip(e,f));out[g]=out.get(g,ZERO)+x*y
    return clean(out)
def psub(a,b):return padd(a,pscale(b,-1))
def psquare(a):return pmul(a,a)
def pdot(a,b):
    out={}
    for x,y in zip(a,b):out=padd(out,pmul(x,y))
    return out
def pcross(a,b):
    return [psub(pmul(a[1],b[2]),pmul(a[2],b[1])),
            psub(pmul(a[2],b[0]),pmul(a[0],b[2])),
            psub(pmul(a[0],b[1]),pmul(a[1],b[0]))]
def pvsub(a,b):return [psub(x,y) for x,y in zip(a,b)]
def peval(p,l):
    return sum((x*Q5(l[0])**e[0]*Q5(l[1])**e[1]*Q5(l[2])**e[2]
                for e,x in p.items()),ZERO)

def composition_identity():
    # Variables a,d,b,p, with p^2=(1-a^2/4)(1-d^2/4)(1-b^2/4).
    one={(0,0,0,0):Q5(1)}
    a,d,b,p=[{tuple(1 if i==j else 0 for i in range(4)):Q5(1)} for j in range(4)]
    a2,d2,b2=map(psquare,(a,d,b));ad=pmul(a,d)
    P=pmul(pmul(psub(one,pscale(a2,F(1,4))),
                 psub(one,pscale(d2,F(1,4)))),psub(one,pscale(b2,F(1,4))))
    W=psub(p,pscale(ad,F(1,4)))
    lhs=psub(padd(psquare(padd(a,d)),b2),pscale(psub(one,psquare(W)),4))
    rhs=padd(pscale(pmul(ad,psub(one,p)),2),
             padd(pscale(pmul(pmul(a2,d2),psub(pscale(one,8),b2)),F(1,16)),
                  pscale(pmul(b2,padd(a2,d2)),F(1,4))))
    assert psub(psub(lhs,rhs),pscale(psub(psquare(p),P),4))=={}
    assert F(399,400)**3>F(99,100)**2
    assert F(99,100)-F(1,400)>0
    assert F(101,100)**2*F(63,64)>1
    assert F(1,20)<F(1,16)
    return 'exact four-variable identity modulo p^2=P; positive branch and angle derivative checked'

def tetrahedron(V,patch,contacts,sign,rho):
    assert len(patch)==3 and len(contacts)==4 and sign in (-1,1) and rho>0
    G=[[cross(V[j],cross(sub(V[b],V[a]),u)) for u in patch] for a,b,j in contacts]
    weights=cofactor_coefficients(G,sign)
    assert all(x.sign()>0 for row in weights for x in row)
    wp=[dict(zip(EXPONENTS,row)) for row in weights]
    Tp=[[{tuple(1 if i==k else 0 for i in range(3)):G[j][k][d]
          for k in range(3)} for d in range(3)] for j in range(4)]
    for d in range(3):
        balance={}
        for j in range(4):balance=padd(balance,pmul(wp[j],Tp[j][d]))
        assert balance=={}
    S={(1,0,0):Q5(1),(0,1,0):Q5(1),(0,0,1):Q5(1)}
    S2=psquare(S);all_coeff=[];records=[];audits=0
    for omitted in range(4):
        inds=[j for j in range(4) if j!=omitted];a,b,c=[Tp[j] for j in inds]
        normal=pcross(pvsub(b,a),pvsub(c,a));offset=pdot(normal,a)
        assert offset==pscale(wp[omitted],sign*(-1 if omitted%2 else 1))
        poly=psub(psquare(offset),pscale(pmul(pdot(normal,normal),S2),rho*rho))
        coeff=[poly.get(e,ZERO) for e in DEGREE6]
        assert all(x.sign()>0 for x in coeff)
        all_coeff.append([[list(e),str(x)] for e,x in zip(DEGREE6,coeff)])
        distances=[]
        for lam in [(F(1),F(0),F(0)),(F(0),F(1),F(0)),
                    (F(0),F(0),F(1)),(F(1,3),)*3]:
            T=[vec(sum((Q5(lam[k])*G[j][k][d] for k in range(3)),ZERO)
                   for d in range(3)) for j in range(4)]
            av,bv,cv=[T[j] for j in inds]
            nv=cross(sub(bv,av),sub(cv,av));nsq=dot(nv,nv);assert nsq.sign()>0
            hv=dot(nv,av)
            assert peval(offset,lam)==hv
            assert peval(poly,lam)==hv*hv-Q5(rho*rho)*nsq
            distances.append(str(hv*hv/nsq));audits+=2
        records.append({'omitted_contact':omitted,'strict_positive_degree6_coefficients':len(coeff),
                        'direct_corner_and_barycenter_facet_distance_squared':distances})
    payload=json.dumps(all_coeff,separators=(',',':')).encode()
    return {'ball_lower':str(rho),'strict_positive_cubic_cofactor_coefficients':40,
            'identically_zero_polynomial_balance_coordinates':3,
            'strict_positive_degree6_facet_coefficients':4*len(DEGREE6),
            'degree6_coefficient_sha256':hashlib.sha256(payload).hexdigest(),
            'direct_polynomial_evaluation_audits':audits,'facets':records}

def finite(parent,*,delta_gate=DELTA_GATE,source_height=SOURCE_HEIGHT,
           edge_height=EDGE_HEIGHT,body_radius=BODY_RADIUS,cosine=COSINE,
           patch_mix=PATCH_MIX,torque_ball=TORQUE_BALL,roll_probes=ROLL_PROBES,
           reverse_contact=False,omit_corner=False):
    V=vertices();nodes=[vec(map(parse,x['ray'])) for x in parent['corner_areas']]
    M=nodes[9];M2=dot(M,M)
    assert 0<cosine<1 and 0<delta_gate<=F(1,10)
    assert body_radius>0 and source_height>0 and edge_height>0
    assert F(2)/(1+cosine)<=CHORD_OVER_TANGENT**2
    assert COERCIVITY==3*CHORD_OVER_TANGENT
    caps=[]
    for u in CHAMBER:
        mp=dot(M,u);assert mp.sign()>0
        margin=mp*mp-cosine*cosine*M2*dot(u,u);assert margin.sign()>0
        caps.append(str(margin))
    # The thirteen sqrt-area corner gaps were rechecked by adaptive_finite.
    # Tangential projection and the cap extend them to every whole cell.
    assert len(parent['corner_areas'])==14
    assert all(dot(v,v)<Q5(body_radius*body_radius) for v in V)
    HS=[dot(v,M)**2/M2 for v in V]
    RS=[dot(v,v)-h for v,h in zip(V,HS)]
    assert HS[57]<Q5(source_height*source_height) and source_height>0
    top=parse(parent['minimal_shadow_max_radius_squared'])
    assert top>Q5(4) and {j for j,r in enumerate(RS) if r==top}=={4,57}
    assert V[4]==mul(-1,V[57])
    root_gap_greater(top,Q5(5),RADIAL_GATE)
    radial_count=0;radial_squared_margins=[]
    for j,(r,h) in enumerate(zip(RS,HS)):
        assert r.sign()>=0 and h.sign()>=0
        if j in (4,57):continue
        left=Q5(5)-r-h*delta_gate**2
        assert left.sign()>=0 and left*left>=4*r*h*delta_gate**2
        radial_squared_margins.append(left*left-4*r*h*delta_gate**2)
        radial_count+=1
    assert radial_count==60
    assert {p[3] for p in roll_probes}=={-1,1} and len(roll_probes)==2
    height_count=0;probe_records=[]
    for a,b,j,sgn in roll_probes:
        assert j==57 and a!=b and j in (a,b)
        mu=cross(sub(V[b],V[a]),M);norm2=dot(mu,mu);assert norm2.sign()>0
        h=dot(mu,V[j]);tau=dot(M,cross(V[j],mu))
        assert h.sign()>0 and tau.sign()==sgn
        assert h*h/norm2<Q5(F(9,4)**2)
        assert tau*tau/(M2*norm2)>Q5(F(3,4)**2)
        ties=[];branches=[0,0]
        for k,hsq in enumerate(HS):
            gap=dot(mu,sub(V[j],V[k]));assert gap.sign()>=0
            if gap==ZERO:ties.append(k)
            g2=gap*gap/(delta_gate*delta_gate*norm2)
            left=hsq-edge_height*edge_height-g2
            if left.sign()>0:
                assert left*left<=4*edge_height*edge_height*g2;branches[1]+=1
            else:branches[0]+=1
            height_count+=1
        probe_records.append({'edge':[a,b],'vertex':j,'roll_sign':sgn,
                              'all_original_support_ties':ties,
                              'height_comparison_nonpositive_and_squared_branches':branches})
    assert edge_height>0 and height_count==124
    assert F(99,100)*F(3,4)-F(9,4)*F(1,10)==F(207,400)>F(1,2)
    assert RADIAL_GATE<F(1,25)
    separation=parse(parent['receiver_halfturn_Frobenius_separation_squared'])
    assert separation>Q5(8*delta_gate*delta_gate)

    old=next(x for x in CERTIFICATES if x[:2]==(7,0));sign=old[2]
    contacts=[tuple(x) for x in old[3]]
    if reverse_contact:
        a,b,j=contacts[0];contacts[0]=(b,a,j)
    assert 0<patch_mix<1
    patch=[M]+[add(M,mul(Q5(patch_mix),sub(nodes[j],M))) for j in (7,8)]
    if omit_corner:patch.pop()
    assert len(patch)==3 and area_twice(patch).sign()!=0
    assert PATCH_DRIFT<delta_gate
    assert all(dot(sub(u,M),sub(u,M))<Q5(PATCH_DRIFT**2) for u in patch)
    assert all(dot(u,u)<Q5(PATCH_NORM_UPPER**2) for u in patch)
    lower_margins=[]
    C=vec(map(parse,parent['cell_certificates'][7]['area_vector']))
    D=sub(C,mul(dot(C,M)/M2,M));assert dot(D,M)==ZERO
    assert dot(C,M).sign()>0 and dot(C,M)**2/M2==parse(parent['global_minimum_area_squared'])
    linear_area=[];support_count=0
    for u in patch:
        mp=dot(M,u);assert mp.sign()>0
        margin=mp*mp-PATCH_NORM_LOWER**2*M2;assert margin.sign()>0
        lower_margins.append(str(margin))
        slope=dot(D,sub(u,M));assert slope<Q5(PATCH_NORM_LOWER*PATCH_AREA_EXCESS)
        linear_area.append(str(slope))
        for a,b,j in contacts:
            edge=sub(V[b],V[a]);assert dot(edge,edge)<Q5(F(5,4)**2)
            mu=cross(edge,u)
            assert all(dot(mu,sub(V[j],v)).sign()>=0 for v in V)
            support_count+=len(V)
    # At these corners the same contacts are actual supports; linearity
    # extends them to the whole triangle (parent also proves whole cell7).
    assert support_count==744
    radius=tetrahedron(V,patch,contacts,sign,torque_ball)
    c=F(1)-F(1,2*50**2);mp=dot(M,patch[1]);assert mp.sign()>0
    assert c*c*M2*dot(patch[1],patch[1])>mp*mp
    a=COERCIVITY*PATCH_AREA_EXCESS;d=PATCH_DRIFT
    E0=source_height*(a+d)+body_radius/2*(a*a+d*d)
    E=source_height*a+edge_height*d+body_radius/2*(a*a+d*d)
    assert E0<RADIAL_GATE and 2*E<PATCH_ROLL_CHORD
    assert 0<a<F(1,10) and 0<d<F(1,10) and 0<PATCH_ROLL_CHORD<F(1,10)
    theta2=F(101,100)**2*((a+d)**2+PATCH_ROLL_CHORD**2)
    assert theta2<PATCH_FULL_ANGLE**2
    margin=torque_ball-(body_radius*F(5,4)/2)*PATCH_NORM_UPPER*PATCH_FULL_ANGLE
    assert margin>F(1,60)
    # This criterion includes the entire parent's sufficient domain.
    x=F(1,70)
    assert SOURCE_HEIGHT*x+BODY_RADIUS*x*x/2<RADIAL_GATE
    assert 2*(EDGE_HEIGHT+BODY_RADIUS*x/2)<5
    assert x<DELTA_GATE and 5*x<F(1,10)
    return {'agent':'six-rupert-1','role':'researcher',
            'status':'exact finite hypotheses with complete unformalized continuous proof',
            'global_Rupert_property':'unresolved','arithmetic':'Q(sqrt(5))/Fraction; standard Python3.11+',
            'parent_global_expected_sha256':PARENT_SHA256,'parent_adaptive_expected_sha256':ADAPTIVE_SHA256,
            'global_source_normal_coercivity':str(COERCIVITY),
            'whole_chamber_normal_cosine_lower':str(cosine),
            'chord_over_tangential_norm_upper':str(CHORD_OVER_TANGENT),
            'chamber_corner_cap_squared_margins':caps,'inherited_corner_root_gap_comparisons':13,
            'body_radius_upper':str(body_radius),'body_radius_vertex_comparisons':62,
            'radial_source_vertex_axial_height_upper':str(source_height),
            'signed_receiver_probe_height_upper':str(edge_height),
            'receiver_normal_chord_gate':str(delta_gate),'remote_roll_radial_error_gate':str(RADIAL_GATE),
            'radial_nonmaximum_joint_radius_height_comparisons':radial_count,
            'radial_joint_squared_zero_margins':sum(x==ZERO for x in radial_squared_margins),
            'signed_probe_all_vertex_gap_height_comparisons':height_count,'roll_probes':probe_records,
            'roll_support_gap_per_chord_lower':'207/400 > 1/2',
            'complete_reduced_roll_interval':'[-pi/2,pi/2] modulo C2; small roll derived',
            'rotation_composition_identity':composition_identity(),
            'adaptive_criterion':'a=(153/50)*(A(n)-a0), delta=||n-m||<=1/20; E0=(29/100)*(a+delta)+(23/20)*(a^2+delta^2)<=1/28; b=2*((29/100)*a+(141/200)*delta+(23/20)*(a^2+delta^2))<=1/10; a<=1/10; Theta=(101/100)*sqrt((a+delta)^2+b^2); r_cell(u)>(23/16)*||u||*Theta',
            'receiver_triangle_cell':7,'receiver_triangle_affine_mix':str(patch_mix),
            'receiver_triangle_rays':[serial(u) for u in patch],
            'receiver_triangle_chart_area_factor_over_parent':str((patch_mix/F(1,20))**2),
            'receiver_triangle_outer_normal_chord_lower':'1/50',
            'receiver_triangle_chart_drift_upper':str(PATCH_DRIFT),
            'receiver_triangle_chart_norm_lower':str(PATCH_NORM_LOWER),
            'receiver_triangle_chart_norm_upper':str(PATCH_NORM_UPPER),
            'receiver_triangle_norm_lower_squared_margins':lower_margins,
            'receiver_triangle_tangent_linear_functional_at_corners':linear_area,
            'receiver_triangle_area_excess_upper':str(PATCH_AREA_EXCESS),
            'receiver_triangle_source_chord_upper':str(a),
            'receiver_triangle_remote_radial_error_upper':str(E0),
            'receiver_triangle_signed_probe_error_upper':str(E),
            'receiver_triangle_roll_chord_upper':str(PATCH_ROLL_CHORD),
            'receiver_triangle_full_angle_upper':str(PATCH_FULL_ANGLE),
            'receiver_triangle_structured_angle_squared_upper':str(theta2),
            'receiver_triangle_actual_support_comparisons':support_count,
            'receiver_triangle_actual_torque_certificate':radius,
            'receiver_triangle_full_rotation_remainder_margin':str(margin),
            'closed_containment_equality_rotations':'G union J_nG; two disjoint LEFT cosets, exactly120proper rotations; lambda1,t0',
            'strict_passages_on_certified_receiver_domain':'excluded at every original source rotation, roll, translation and scale>=1',
            'includes_entire_parent_adaptive_sufficient_domain':True,
            'solver_or_floating_point_proof_decisions':0}

def negative_tests(parent):
    controls=[('unsupported normal gate1/10',{'delta_gate':F(1,10)}),
              ('unsupported source height7/25',{'source_height':F(7,25)}),
              ('unsupported receiver height7/10',{'edge_height':F(7,10)}),
              ('unsupported body radius9/4',{'body_radius':F(9,4)}),
              ('unsupported chamber cosine49/50',{'cosine':F(49,50)}),
              ('missing roll sign',{'roll_probes':ROLL_PROBES[:1]}),
              ('reversed actual weak support',{'reverse_contact':True}),
              ('unsupported torque ball9/50',{'torque_ball':F(9,50)}),
              ('unsupported triangle mix3/5 with fixed bounds',{'patch_mix':F(3,5)}),
              ('missing receiver corner',{'omit_corner':True})]
    rejected=[]
    for name,kwargs in controls:
        try:finite(parent,**kwargs)
        except AssertionError:rejected.append(name)
        else:raise AssertionError('malformed certificate accepted: '+name)
    return rejected

def check(self_test=False):
    root=Path(__file__).parent
    raw=(root/'expected_global_area.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==PARENT_SHA256
    old=json.loads(raw);assert len(old.pop('malformed_controls_rejected'))==5
    parent=check_parent();assert parent==old
    raw=(root/'expected_adaptive_area.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==ADAPTIVE_SHA256
    old_adaptive=json.loads(raw);assert len(old_adaptive.pop('malformed_controls_rejected'))==7
    assert adaptive_finite(parent)==old_adaptive
    result=finite(parent)
    if self_test:result['malformed_controls_rejected']=negative_tests(parent)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--self-test',action='store_true')
    args=p.parse_args();print(json.dumps(check(args.self_test),indent=2))
