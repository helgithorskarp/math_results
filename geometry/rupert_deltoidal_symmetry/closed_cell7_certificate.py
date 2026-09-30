#!/usr/bin/env python3
"""Exact all-source closed receiver cell7 certificate for the deltoidal body.

Python3.11+, standard library only. Reconstructs a complete ten-piece
closed cover, actual physical area maxima, outward rational enclosures,
and strict polynomial facet-distance bounds. See closed_cell7_proof.md.
"""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from verify import Q5,ZERO,vec,vertices,dot,cross,sub,add,mul
from adaptive_area_certificate import parse
from orientation_certificate import CHAMBER,CERTIFICATES,area_twice
from directional_area_certificate import check as check_parent,tetrahedron

if not __debug__:
    raise RuntimeError('verification requires assertions; do not use python -O')

DIRECTIONAL_SHA256='e0ee007750c6dcb08d15d1222344ed22f59a13523f822c79f31ee09da8fed34c'
GRID=10**6
COERCIVITY=F(21,8)
REMAINDER=F(73,50)
MARGIN=F(1,2000)
ANGLE_FACTOR=F(1003,1000)
COMPOSITION_CHORD_GATE=F(3,20)
LEAF_PATHS=('0','10','110','111','112','113','12','13','2','3')
MAX_DEPTH=3

def digest(x):
    return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

def grid_upper(test,cap):
    """Smallest positive multiple of 10^-6 passing a monotone strict test.

    No decimal approximation enters the search or the proof decision.
    The predecessor is also tested, to audit enclosure direction.
    """
    lo,hi=0,int(cap*GRID)
    assert hi>0 and test(F(hi,GRID))
    while hi-lo>1:
        mid=(lo+hi)//2
        if test(F(mid,GRID)):hi=mid
        else:lo=mid
    upper=F(hi,GRID)
    assert test(upper) and (lo==0 or not test(F(lo,GRID)))
    return upper

def inside(p,tri):
    sign=area_twice(tri).sign()
    assert sign!=0 and p[2]==Q5(1)
    return all((cross(sub(b,a),sub(p,a))[2]*sign).sign()>0
               for a,b in zip(tri,tri[1:]+tri[:1]))

def area_maximum(C,tri):
    """Exact maximum of (C.u)^2/||u||^2 over a closed unit-z triangle.

    Enumerates corners, positive-cone edge critical points and the
    interior critical direction. Completeness is proved in the document.
    """
    assert len(tri)==3 and all(u[2]==Q5(1) for u in tri)
    assert area_twice(tri).sign()!=0
    candidates=[];edges=[]
    for i,u in enumerate(tri):
        assert dot(C,u).sign()>0
        candidates.append(('corner'+str(i),dot(C,u)**2/dot(u,u)))
    for i,(a,b) in enumerate(zip(tri,tri[1:]+tri[:1])):
        aa,bb,ab=dot(a,a),dot(b,b),dot(a,b)
        ca,cb=dot(C,a),dot(C,b)
        det=aa*bb-ab*ab;assert det.sign()>0
        alpha=(ca*bb-cb*ab)/det;beta=(cb*aa-ca*ab)/det
        included=alpha.sign()>0 and beta.sign()>0
        edges.append({'edge':i,'positive_cone_critical_point':included,
                      'alpha':str(alpha),'beta':str(beta)})
        if included:
            p=add(mul(alpha,a),mul(beta,b));assert dot(p,p).sign()>0
            candidates.append(('edge'+str(i),dot(p,p)))
    assert C[2].sign()>0
    interior=inside(mul(1/C[2],C),tri)
    if interior:candidates.append(('interior',dot(C,C)))
    q=max(x[1] for x in candidates)
    return q,{'max_squared':str(q),'active_strata':[s for s,x in candidates if x==q],
              'edge_critical_points':edges,'interior_critical_point':interior}

def gap_less(q,qmin,e):
    assert q>=qmin and qmin.sign()>0 and e>0
    left=q-qmin-e*e
    return left.sign()<=0 or left*left<4*e*e*qmin

def chord_less(M,u,d):
    assert 0<d<F(1,10)
    mp=dot(M,u);assert mp.sign()>0
    c=1-d*d/2;assert c>0
    return mp*mp>c*c*dot(M,M)*dot(u,u)

def split(tri):
    a,b,c=tri
    ab,bc,ca=[mul(F(1,2),add(x,y)) for x,y in [(a,b),(b,c),(c,a)]]
    children=[[a,ab,ca],[ab,b,bc],[ca,bc,c],[ab,bc,ca]]
    ar=area_twice(tri);assert ar.sign()!=0
    assert all(area_twice(t)==ar/4 for t in children)
    return children

def closed_cover(tri,paths):
    """Rebuild a prefix-free full quaternary subdivision, including edges."""
    assert paths and len(paths)==len(set(paths))
    assert all(len(p)<=MAX_DEPTH and set(p)<=set('0123') for p in paths)
    wanted=set(paths);leaves=[];splits=[]
    def visit(path,patch):
        if path in wanted:
            leaves.append((path,patch));return
        assert len(path)<MAX_DEPTH
        assert any(p.startswith(path) for p in wanted)
        children=split(patch);splits.append(path)
        for i,t in enumerate(children):visit(path+str(i),t)
    visit('',tri)
    assert {p for p,t in leaves}==wanted
    assert sum((F(1,4)**len(p) for p,t in leaves),F(0))==1
    return leaves,splits

def area_controls():
    """Definition-level critical-point checks, including a corner trap."""
    tri=list(map(vec,[(0,0,1),(1,0,1),(0,1,1)]))
    q,rec=area_maximum(vec((1,1,1)),tri)
    assert q==Q5(F(8,3)) and rec['active_strata']==['edge1']
    assert max(dot(vec((1,1,1)),u)**2/dot(u,u) for u in tri)==Q5(2)<q
    qr,rr=area_maximum(vec((1,1,1)),list(reversed(tri)))
    assert qr==q
    q,rec=area_maximum(vec((F(1,4),F(1,4),1)),tri)
    assert q==Q5(F(9,8)) and rec['active_strata']==['interior']
    q,rec=area_maximum(vec((0,0,1)),tri)
    assert q==Q5(1) and rec['active_strata']==['corner0']
    assert grid_upper(lambda x:Q5(x*x)>Q5(F(1,4)),F(1))==F(500001,GRID)
    return ['edge maximum 8/3 exceeds every corner2',
            'interior maximum9/8','corner maximum1',
            'reversed triangle preserves maximum',
            'strict upward grid enclosure at an exact square']

def finite(parent,*,coercivity=COERCIVITY,remainder=REMAINDER,
           margin=MARGIN,angle_factor=ANGLE_FACTOR,leaf_paths=LEAF_PATHS,
           reverse_contact=False):
    V=vertices();nodes=[vec(map(parse,x['ray'])) for x in parent['corner_areas']]
    M=nodes[9];M2=dot(M,M);qmin=parse(parent['global_minimum_area_squared'])
    assert qmin.sign()>0 and coercivity>0 and remainder>0 and margin>0
    cosine=F(2399,2601);ratio=F(51,50)
    assert 2/(1+cosine)==ratio*ratio
    cap_margins=[]
    for u in CHAMBER:
        mp=dot(M,u);assert mp.sign()>0
        cap_margin=mp*mp-cosine*cosine*M2*dot(u,u)
        assert cap_margin.sign()>0;cap_margins.append(str(cap_margin))
    corners=[]
    for j,u in enumerate(nodes):
        if j==9:continue
        q=parse(parent['corner_areas'][j]['physical_area_squared'])
        tangent2=Q5(1)-dot(M,u)**2/(M2*dot(u,u));assert tangent2.sign()>0
        d2=ratio*ratio*tangent2/(coercivity*coercivity)
        left=q-qmin-d2
        assert left.sign()>0 and left*left>4*qmin*d2
        corners.append({'corner':j,'tangent_squared':str(tangent2),
                        'root_gap_branch_left':str(left),
                        'root_gap_squared_margin':str(left*left-4*qmin*d2)})
    assert len(corners)==13
    C=vec(map(parse,parent['cell_certificates'][7]['area_vector']))
    tri=[M,nodes[7],nodes[8]]
    assert set(tri)=={nodes[j] for j in parent['cell_certificates'][7]['corner_indices']}
    assert dot(C,M).sign()>0 and dot(C,M)**2/M2==qmin
    cert=next(x for x in CERTIFICATES if x[:2]==(7,0));sign=cert[2]
    contacts=[tuple(x) for x in cert[3]]
    if reverse_contact:
        a,b,j=contacts[0];contacts[0]=(b,a,j)
    remainder_checks=[];support_count=0
    for i,u in enumerate(tri):
        for a,b,j in contacts:
            mu=cross(sub(V[b],V[a]),u)
            k2=dot(V[j],V[j])*dot(mu,mu)/4
            assert k2<Q5(remainder*remainder)
            remainder_checks.append({'corner':i,'contact':[a,b,j],
                                     'remainder_squared':str(k2)})
            for v in V:
                assert dot(mu,sub(V[j],v)).sign()>=0;support_count+=1
    assert support_count==744
    assert 0<angle_factor and angle_factor**2*(1-COMPOSITION_CHORD_GATE**2/4)>1
    leaves,splits=closed_cover(tri,leaf_paths)
    records=[];compact=[]
    for path,patch in leaves:
        q,area_record=area_maximum(C,patch)
        e=grid_upper(lambda x:gap_less(q,qmin,x),F(1,10))
        d=max(grid_upper(lambda x:chord_less(M,u,x),F(1,20)) for u in patch)
        a=coercivity*e
        E0=F(29,100)*(a+d)+F(23,20)*(a*a+d*d)
        E=F(29,100)*a+F(141,200)*d+F(23,20)*(a*a+d*d)
        b=2*E;x2=(a+d)**2+b*b
        assert d<=F(1,20) and a<=F(1,10) and E0<=F(1,28) and b<=F(1,10)
        assert x2<=COMPOSITION_CHORD_GATE**2
        theta2=angle_factor**2*x2
        theta=grid_upper(lambda x:Q5(x*x)>Q5(theta2),F(1,4))
        rho=remainder*theta+margin
        torque=tetrahedron(V,patch,contacts,sign,rho)
        record={'path':path,'rays':[list(map(str,u)) for u in patch],
                'area':area_record,'e_upper':str(e),'delta_upper':str(d),
                'source_chord_upper':str(a),'remote_radial_error_upper':str(E0),
                'roll_chord_upper':str(b),'composition_bound_squared':str(x2),
                'full_angle_upper':str(theta),'torque_ball_lower':str(rho),'torque':torque}
        records.append(record)
        compact.append({'path':path,'area_max_active_strata':area_record['active_strata'],
                        'area_excess_upper':str(e),'normal_chord_upper':str(d),
                        'full_angle_upper':str(theta),'torque_ball_lower':str(rho),
                        'degree6_coefficient_sha256':torque['degree6_coefficient_sha256']})
    result={'agent':'six-rupert-1','role':'researcher',
            'status':'exact finite hypotheses with complete written unformalized proof',
            'global_Rupert_property':'unresolved',
            'arithmetic':'Q(sqrt(5))/Fraction; standard Python3.11+; no floating proof decisions',
            'parent_directional_expected_sha256':DIRECTIONAL_SHA256,
            'global_source_normal_coercivity':str(coercivity),
            'whole_chamber_normal_cosine_lower':str(cosine),
            'chord_over_tangential_norm_upper':str(ratio),
            'chamber_corner_cap_squared_margins':cap_margins,
            'strict_source_corner_tangent_comparisons':corners,
            'whole_cell_contact_remainder_upper':str(remainder),
            'contact_remainder_corner_comparisons':remainder_checks,
            'actual_weak_support_comparisons':support_count,
            'composition_chord_gate':str(COMPOSITION_CHORD_GATE),
            'full_angle_factor':str(angle_factor),'outward_rational_grid_denominator':GRID,
            'subdivision_policy':'four closed midpoint triangles at every internal node; full prefix tree',
            'subdivision_internal_paths':splits,'max_depth':max(map(len,leaf_paths)),
            'leaf_paths':[p for p,t in leaves],'leaf_count':len(leaves),
            'closed_cover_chart_area_fraction':'1',
            'chart_area_factor_over_previous_half_cell7':'4',
            'chart_area_factor_over_mix1_20_triangle':'400',
            'receiver_domain':'entire closed cell7 conv(M,N7,N8), every proper body image and antipode',
            'source_restriction':'none; every original proper rotation, roll, translation, scale>=1',
            'closed_containment_equality_rotations':'G union J_nG; exactly120proper rotations, two disjoint LEFT cosets; lambda1,t0',
            'strict_passages_on_receiver_domain':'excluded',
            'uniform_torque_remainder_margin':str(margin),
            'largest_piece_area_excess_upper':str(max(F(r['e_upper']) for r in records)),
            'largest_piece_receiver_chord_upper':str(max(F(r['delta_upper']) for r in records)),
            'largest_piece_full_angle_upper':str(max(F(r['full_angle_upper']) for r in records)),
            'strict_positive_cubic_cofactor_coefficients':40*len(leaves),
            'identically_zero_polynomial_balance_coordinates':3*len(leaves),
            'strict_positive_degree6_facet_coefficients':112*len(leaves),
            'direct_polynomial_evaluation_audits':32*len(leaves),
            'edge_critical_points_in_positive_cones':sum(e['positive_cone_critical_point']
                for r in records for e in r['area']['edge_critical_points']),
            'leaves_with_edge_maxima':[r['path'] for r in records
                if any(s.startswith('edge') for s in r['area']['active_strata'])],
            'reconstructed_full_record_sha256':digest(records),'leaves':compact,
            'definition_level_area_and_grid_controls':area_controls()}
    return result

def negative_tests(parent):
    controls=[('unsupported source coefficient13/5',{'coercivity':F(13,5)}),
              ('unsupported contact remainder29/20',{'remainder':F(29,20)}),
              ('unsupported angle factor501/500',{'angle_factor':F(501,500)}),
              ('missing closed cover leaf',{'leaf_paths':LEAF_PATHS[:-1]}),
              ('ancestor overlaps closed cover leaves',{'leaf_paths':LEAF_PATHS+('',)}),
              ('duplicate closed cover leaf',{'leaf_paths':LEAF_PATHS+('0',)}),
              ('reversed actual weak support',{'reverse_contact':True}),
              ('unsupported uniform margin1/100',{'margin':F(1,100)})]
    rejected=[]
    for name,kwargs in controls:
        try:finite(parent,**kwargs)
        except AssertionError:rejected.append(name)
        else:raise AssertionError('malformed certificate accepted: '+name)
    return rejected

def check(self_test=False):
    root=Path(__file__).parent
    raw=(root/'expected_directional_area.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==DIRECTIONAL_SHA256
    old=json.loads(raw);assert len(old.pop('malformed_controls_rejected'))==10
    assert check_parent()==old
    parent=json.loads((root/'expected_global_area.json').read_text())
    result=finite(parent)
    if self_test:result['malformed_controls_rejected']=negative_tests(parent)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--self-test',action='store_true')
    args=p.parse_args();print(json.dumps(check(args.self_test),indent=2))
