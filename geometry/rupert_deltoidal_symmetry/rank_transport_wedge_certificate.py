"""Signed rank-one tilt bounds: whole D1 angle and closed D3/4 rigidity.

Python3.11+ standard library, fixed exact witnesses, no float predicates.
Continuous proof and quantified scope: rank_transport_wedge_proof.md.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,copy,hashlib,itertools,json,resource,time
ROOT=Path(__file__).parent
if not __debug__:raise RuntimeError('verification requires assertions; do not use python -O')
import source_extrema_certificate as source
import zero_height_wedge_certificate as reference
import two_thirds_wedge_certificate as parent
import normalized_receiver_piece_certificate as H
from verify import Q5,ZERO,vec,vertices,dot,cross,sub,add,mul,project
from area_polar_certificate import audit_signs
from orientation_certificate import determinant,area_twice
from stable_certificate import orbit
from zero_height_wedge_certificate import (P,V,N,M,M2,PROBES,POINTS,DATA,
    root_upper,triangle,linear_envelopes,grid_upper,area_maximum,parse,validate_roll_cover)

SOURCE_A=F(6571,62500);SOURCE_T=F(7409521,500000)
SELECTED=list(range(1,11));TRI=triangle(F(3,4))
PINS={
    'adaptive_area_certificate.py':'41e45c7ac2183c99b65dfaa60293ab7f41c286699b3e12ef0b4bd683db41d4dc',
    'closed_cell7_certificate.py':'8dd5b363092d120c30f3538bc0b82838145eaa6ea0d341d40d033c907e6fb211',
    'normalized_cap_certificate.py':'c387e4e4ee909ce6fedaa152215ed29c2417285e58d668b4283551e18230b0d0',
    'directional_area_certificate.py':'b67dbcaf8cfd1fcd953bb9c0cc5c6d3fe1dbfe0e5c17f71741977c4b9f5b2c54',
    'area_sublevel_wedge_certificate.py':'0809a7930ed09b3f604902133c7cc7cb2f5e988780a9b25b6a5900a87cbde280',
    'selected_torque_wedge_certificate.py':'8dd0ad3d6a2b070164e4162cb256207da46e10caa812ec6a62cf29fdf7ca0784',
    'source_extrema_certificate.py':'735d46a60ef542fceb1916b1d51190ddfb066fa8f607050ae74f6f8fb95df935',
    'expected_source_extrema.json':'ebf4dc5bcef01a50e5f6831fb4a4c987f416919869b1ce603d01b3496dc65cb5',
    'zero_height_wedge_certificate.py':'2968d516344a836745bb4f8a6e1875c5db31874f3670362909a322c90397a708',
    'two_thirds_wedge_certificate.py':'b682bd9ee283bfc6c31e0c25945a064684ad21a87601a7457f2ee2670a264def',
    'normalized_receiver_piece_certificate.py':'4b64b1490df79536133f101e632e540ce21ebb153fd45a779f0a6f1bb0bd124e',
    'expected_two_thirds_wedge.json':'2697a7a5cca11d0dc137f6135439ecc95e313b7791567ce67883514c7d36f0c6',
}
# Fixed actual witnesses for BOTH domains. Wider D1 witnesses also work on D3/4.
REMOTE=((-1,'1/10','109/640',3,45),(-1,'109/640','181/640',3,45),
    (-1,'181/640','13/40',4,72),(-1,'13/40','167/320',6,4),
    (-1,'167/320','343/640',5,4),(-1,'343/640','11/20',4,63),
    (-1,'11/20','221/320',4,63),(-1,'221/320','577/640',4,4),
    (-1,'577/640','1',4,65),(1,'1/10','109/640',4,45),
    (1,'109/640','181/640',4,45),(1,'181/640','13/40',3,66),
    (1,'13/40','167/320',1,57),(1,'167/320','343/640',2,57),
    (1,'343/640','11/20',3,64),(1,'11/20','221/320',3,64),
    (1,'221/320','577/640',3,57),(1,'577/640','1',3,62))

def fixture():return json.loads((ROOT/'expected_rank_transport_wedge.json').read_text())
def pins():
    out=source.pins()
    for name,wanted in PINS.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==wanted
    return {**out,**PINS}

def chord_less(u,d):
    """Explicit NEW acute-normal scope, without changing any earlier guard."""
    assert 0<d<F(1,4)
    p=dot(M,u);assert p.sign()>0
    return (p*p-Q5((1-d*d/2)**2)*M2*dot(u,u)).sign()>0

def phase(scale):
    assert scale in (F(1),F(3,4))
    tri=triangle(scale);a=SOURCE_A
    d=max(grid_upper(lambda x:chord_less(u,x),F(1,5)) for u in tri)
    assert a<F(1,5) and d<F(1,5)
    C=vec(map(parse,P['cell_certificates'][9]['area_vector']))
    q,area=area_maximum(C,tri);assert (Q5(SOURCE_T**2)-q).sign()>0
    c=1-a*a/4;assert c>0
    envelopes=linear_envelopes(tri)
    vertex_perp=[root_upper(dot(project(v,M),project(v,M))) for v in V]
    source_perp=[root_upper(dot(project(p,M),project(p,M))) for p,_ in POINTS]
    receiver=[];records=[];comparisons=0
    for pi,p in enumerate(PROBES):
        eta,H0=p['norm_upper'],p['H'];vals=[]
        assert dot(p['mu'],M)==ZERO and Q5(eta*eta)>dot(p['mu'],p['mu'])
        for j,v in enumerate(V):
            gamma=dot(p['mu'],v);assert gamma<=H0
            correction=eta*vertex_perp[j]-gamma;assert correction.sign()>=0
            for side,xi in enumerate((envelopes[pi]['lo'],envelopes[pi]['hi'])):
                z=-dot(M,v)*xi-(H0-gamma)+d*d*correction/4
                vals.append((z,j,side));comparisons+=1
        bound=max(ZERO,*(z for z,j,side in vals))
        assert all(z<=bound for z,j,side in vals)
        receiver.append(bound)
        records.append({'probe':pi,'receiver_excess_upper':str(bound),
            'active_vertices_and_sides':[[j,side] for z,j,side in vals if z==bound],
            'corner_ratio_lower':str(envelopes[pi]['lo']),'corner_ratio_upper':str(envelopes[pi]['hi'])})
    assert comparisons==1984
    def coefficients(sg,pi,wi):
        p,row=PROBES[pi],DATA[pi][wi]
        eta,gamma,H0=p['norm_upper'],row['d'],p['H']
        assert -H0<=gamma<=H0
        assert (gamma+eta*source_perp[wi]).sign()>=0
        error=eta*row['source_height_upper']*a+a*a*eta*source_perp[wi]/4+receiver[pi]
        assert error.sign()>=0
        coef=(c*gamma-H0-error,Q5(2*c*row['tau'][sg]),-c*gamma-H0-error)
        assert coef[2].sign()<=0
        return coef
    b=F(1,10);gates=[]
    for sg,pi in ((-1,3),(1,4)):
        assert dot(M,V[45])==ZERO and DATA[pi][45]['d']==PROBES[pi]['H']
        assert DATA[pi][45]['source_height_upper']==0 and DATA[pi][45]['tau'][sg]>0
        coef=coefficients(sg,pi,45);quad=lambda x:-(coef[0]+coef[1]*x+coef[2]*x*x)
        assert quad(0).sign()>0 and quad(b).sign()<0 and coef[2].sign()<0
        up=grid_upper(lambda x:quad(x).sign()<0,b)
        assert quad(up).sign()<0 and quad(up-F(1,10**6)).sign()>=0
        gates.append({'sign':sg,'probe':pi,'point':45,'coefficients':list(map(str,coef)),
            'q_b':str(quad(b)),'receiver_excess_upper':str(receiver[pi]),
            'small_root_upper':str(up),'q_upper':str(quad(up)),
            'q_predecessor':str(quad(up-F(1,10**6))),'roll_chord_upper':str(2*up)})
    remote=[]
    for sg in (-1,1):
        rows=[r for r in REMOTE if r[0]==sg];validate_roll_cover(rows,b)
        for sign,los,his,pi,wi in rows:
            coef=coefficients(sg,pi,wi)
            margins=[coef[0]+coef[1]*x+coef[2]*x*x for x in (F(los),F(his))]
            assert all(x.sign()>0 for x in margins)
            remote.append({'sign':sg,'interval':[los,his],'probe':pi,'point':wi,
                'source_point_certificate':POINTS[wi][1],
                'strict_margins':list(map(str,margins)),'coefficients':list(map(str,coef))})
    assert len(remote)==18
    r=max(F(g['roll_chord_upper']) for g in gates)
    product=(1-a*a/4)*(1-d*d/4)*(1-r*r/4);X2=(a+d)**2+r*r
    assert r<F(1,5) and product>F(99,100)**2 and F(99,100)-a*d/4>0 and X2<=F(1,3)**2
    beta=next(F(j,1000) for j in range(1001,1020) if F(j,1000)**2*(1-X2/4)>1)
    theta=grid_upper(lambda x:Q5(x*x)>Q5(beta*beta*X2),F(1,3))
    return theta,{'receiver_scale':str(scale),'source_chord_upper':str(a),
        'receiver_chord_upper':str(d),'used_source_area_upper':str(SOURCE_T),'area':area,
        'source_tilt_factor':str(c),'receiver_vertex_side_comparisons':comparisons,
        'vertex_perpendicular_norm_uppers':list(map(str,vertex_perp)),
        'source_perpendicular_norm_uppers':list(map(str,source_perp)),
        'rank_receiver_envelopes':records,'near_zero_gates':gates,'remote_cover':remote,
        'angle':{'roll_chord_upper':str(r),'full_angle_upper':str(theta),
            'composition_squared_upper':str(X2),'quaternion_product_margin':str(product-F(99,100)**2),
            'angle_derivative_factor':str(beta),'angle_derivative_margin':str(beta*beta*(1-X2/4)-1)}}


import math
verify_fixed_refinement=parent.verify_fixed_refinement

def selected_hull(tri,theta,selected,rho):
    assert selected==SELECTED
    V=H.V;values=[];T=[];scalings=[];support_count=0
    for original_id in selected:
        aa,bb,j=H.CONTACTS[original_id];edge=H.sub(V[bb],V[aa]);muv=[H.cross(edge,u) for u in tri]
        for mu in muv:
            for v in V:
                assert H.dot(mu,H.sub(V[j],v)).sign()>=0;support_count+=1
        K2=max(H.dot(V[j],V[j])*H.dot(mu,mu)/4 for mu in muv)
        B=H.grid_upper(lambda x:(H.Q5(x*x)-K2).sign()>0,F(3));scalings.append(str(B))
        G=[H.mul(1/B,H.cross(V[j],mu)) for mu in muv];values.append(G)
        T.append([{H.UNITS[s]:G[s][k] for s in range(3) if G[s][k]!=H.ZERO} for k in range(3)])
    stress=[selected.index(i) for i in H.ORIGIN_STRESS]
    weights=H.cofactor_coefficients([values[j] for j in stress],-1)
    assert all(x.sign()>0 for row in weights for x in row)
    wp=[dict(zip(H.EXPONENTS,row)) for row in weights]
    assert all(H.sum_polys([H.pmul(wp[j],T[stress[j]][k]) for j in range(4)])=={} for k in range(3))
    sumlam={e:H.Q5(1) for e in H.UNITS};sumlam2=H.psquare(sumlam)
    counts=dict.fromkeys(['opposite','distance','degenerate','unresolved'],0);records=[];coeff=hashlib.sha256();audits=0
    audits_lam=[tuple(F(i==j) for i in range(3)) for j in range(3)]+[(F(1,2),F(1,3),F(1,6))]
    direct=[[H.vec(sum((lam[s]*G[s][k] for s in range(3)),H.ZERO) for k in range(3)) for G in values] for lam in audits_lam]
    for ids in itertools.combinations(range(len(selected)),3):
        a,b,c=[T[j] for j in ids];normal=H.pcross(H.pvsub(b,a),H.pvsub(c,a));height=H.pdot(normal,a)
        gaps=[H.psub(H.pdot(normal,t),height) for t in T]
        distance=H.psub(H.psquare(height),H.pscale(H.pmul(H.pdot(normal,normal),sumlam2),rho*rho))
        for poly in [*normal,height,*gaps,distance]:coeff.update(json.dumps(H.serialize(poly),separators=(',',':')).encode())
        for lam,actual in zip(audits_lam,direct):
            a0,b0,c0=[actual[j] for j in ids];n0=H.cross(H.sub(b0,a0),H.sub(c0,a0));h0=H.dot(n0,a0)
            assert H.vec(H.peval(p,lam) for p in normal)==n0 and H.peval(height,lam)==h0
            assert all(H.peval(p,lam)==H.dot(n0,t)-h0 for p,t in zip(gaps,actual))
            assert H.peval(distance,lam)==h0*h0-rho*rho*H.dot(n0,n0);audits+=len(selected)+3
        kinds=[]
        for face in H.FACES:
            kind,witness=H.classify(normal,gaps,distance,face);counts[kind]+=1;kinds.append([kind,list(witness)])
        records.append({'selected_triple':list(ids),'original_triple':[selected[i] for i in ids],'cases':kinds})
    assert len(records)==math.comb(len(selected),3) and sum(counts.values())==len(records)*7
    refinements=[];refhash=hashlib.sha256()
    witnesses=fixture()['hull_refinement_witnesses']
    expected=[r['selected_triple'] for r in records if any(c[0]=='unresolved' for c in r['cases'])]
    assert [r['selected_triple'] for r in witnesses]==expected
    for rec in witnesses:
        assert set(rec)=={'selected_triple','closed_leaf_paths'}
        refinements.append(verify_fixed_refinement(values,tuple(rec['selected_triple']),rho,tri,rec['closed_leaf_paths'],refhash))
    assert all(r['terminal_unresolved_strata']==0 for r in refinements)
    terminal=counts.copy()
    for rec in records:
        if rec['selected_triple'] in expected:
            for kind,_ in rec['cases']:terminal[kind]-=1
    for rec in refinements:
        for kind,num in rec['all_leaf_classifications'].items():terminal[kind]+=num
    assert terminal['unresolved']==terminal['degenerate']==0
    assert sum(terminal.values())==7*(len(records)-len(refinements)+sum(len(r['closed_leaf_paths']) for r in refinements))
    failure=None
    return {'agent':'six-rupert-1','role':'researcher','global_Rupert_property':'OPEN',
            'status':'complete D3/4 selected affine-hull hypotheses; written unformalized continuous proof',
            'selected_original_contact_ids':selected,'receiver_rays':[list(map(str,u)) for u in tri],
            'theta':str(theta),'radius':str(rho),'strict_remainder_margin':str(rho-theta),
            'denominators':scalings,'actual_support_comparisons':support_count,
            'origin_stress_original_ids':H.ORIGIN_STRESS,'positive_origin_cubic_coefficients':40,
            'all_three_origin_balance_coordinates_identically_zero':True,
            'all_potential_triples':len(records),'all_seven_faces':list(map(list,H.FACES)),
            'all_facet_strata':sum(counts.values()),'base_classifications':counts,
            'terminal_facet_strata':sum(terminal.values()),'terminal_classifications':terminal,
            'coefficient_sha256':coeff.hexdigest(),'case_sha256':H.digest(records),
            'arithmetic_audits':audits,'unresolved':[(r['original_triple'],[i for i,c in enumerate(r['cases']) if c[0]=='unresolved']) for r in records if any(c[0]=='unresolved' for c in r['cases'])],
            'refinements':refinements,'refinement_sha256':refhash.hexdigest(),'failure':failure}

def weak_inside(u,tri):
    sg=area_twice(tri).sign();assert sg!=0
    return all((cross(sub(b,a),sub(u,a))[2]*sg).sign()>=0 for a,b in zip(tri,tri[1:]+tri[:1]))

def receiver_geometry():
    full=triangle(F(1));previous=triangle(F(2,3))
    cell=[N[j] for j in P['cell_certificates'][9]['corner_indices']]
    assert all(weak_inside(u,cell) for u in full)
    assert all(weak_inside(u,full) for u in TRI)
    assert all(weak_inside(u,TRI) for u in previous)
    assert area_twice(TRI)==F(81,64)*area_twice(previous)
    weights=[F(1,10),F(1,15),F(5,6)];assert sum(weights)==1 and min(weights)>0
    witness=vec(sum((weights[j]*TRI[j][k] for j in range(3)),ZERO) for k in range(3))
    sg=area_twice(TRI).sign()
    assert all((cross(sub(b,a),sub(witness,a))[2]*sg).sign()>0 for a,b in zip(TRI,TRI[1:]+TRI[:1]))
    old=[[M,add(M,mul(F(1,8),sub(N[3],M))),add(M,mul(F(1,4),sub(N[4],M)))],
         [M,add(M,mul(F(1,4),sub(N[4],M))),N[7]],[M,N[7],N[8]],
         [M,N[8],add(M,mul(F(1,6),sub(N[10],M)))],triangle(F(2,5)),triangle(F(1,2)),previous]
    images=orbit(witness);assert len(images)==60
    for u in images:
        for a,b,c in old:
            det=determinant(a,b,c);assert det.sign()!=0
            co=[determinant(u,b,c)/det,determinant(a,u,c)/det,determinant(a,b,u)/det]
            assert not(all(x.sign()>=0 for x in co) or all(x.sign()<=0 for x in co))
    centers=orbit(M);assert len(centers)==30;c=1-F(1,50)**2/2
    for v in centers:assert (Q5(c*c)*dot(witness,witness)*dot(v,v)-dot(witness,v)**2).sign()>0
    walls=[source.reflection(w) for w in source.WALLS]
    group={source.I};pending=[source.I]
    generators=[source.mm(walls[0],walls[1]),source.mm(walls[1],walls[2])]
    while pending:
        g=pending.pop()
        for h in generators:
            q=source.mm(h,g)
            if q not in group:group.add(q);pending.append(q);assert len(group)<=60
    assert len(group)==60
    J=tuple(tuple(2*M[i]*M[j]/M2-Q5(int(i==j)) for j in range(3)) for i in range(3))
    separation=min(sum(((J[i][j]-g[i][j])**2 for i in range(3) for j in range(3)),ZERO) for g in group)
    assert separation==Q5(F(106,29),F(-36,29))
    d=F(21027,200000);assert separation>Q5(8*d*d)
    return {'closed_three_quarter_triangle_rays':[list(map(str,u)) for u in TRI],
        'whole_D1_in_actual_closed_cell9':True,'contains_entire_previous_D2_3':True,
        'unit_z_chart_area_ratio_over_previous':'81/64','spherical_area_ratio_claimed':False,
        'new_receiver_witness':list(map(str,witness)),'witness_barycentric_weights':list(map(str,weights)),
        'projective_witness_orbit':60,'old_triangular_cones_checked_per_image':7,
        'witness_images_in_old_closed_regions':0,'minimum_projective_axes_checked':30,
        'witness_chord_from_all_signed_minimum_centers_lower':'1/50 > 1/64',
        'proper_body_rotations_in_halfturn_separation':len(group),
        'receiver_halfturn_separation_squared_at_m':str(separation),
        'full_D1_halfturn_separation_margin':str(separation-Q5(8*d*d))}

def rank_transport_audits():
    """Exact Rodrigues regressions; the written algebra proves continuity."""
    base=vec((0,0,1));mu=vec((2,-3,0));eta=root_upper(dot(mu,mu));checks=0
    rank_cases=0
    planar=list(map(vec,[(0,0,0),(1,0,0),(-1,0,0),(0,1,0),(F(3,5),F(4,5),0)]))
    for x in planar:
        for y in planar:
            rx=F(int(dot(x,x)!=ZERO));ry=F(int(dot(y,y)!=ZERO));gamma=dot(x,y)
            assert dot(x,x)==Q5(rx*rx) and dot(y,y)==Q5(ry*ry)
            for e in planar[1:]:
                z=2*dot(x,e)*dot(y,e)-gamma
                assert Q5(-rx*ry)<=z<=Q5(rx*ry);rank_cases+=1
    for e in map(vec,[(1,0,0),(F(3,5),F(4,5),0)]):
        axis=cross(base,e)
        for t in (F(-1,4),F(0),F(1,4)):
            c0=(1-t*t)/(1+t*t);ss=2*t/(1+t*t);delta2=2*(1-c0)
            a=root_upper(Q5(delta2));factor=1-a*a/4;assert factor>0
            def rotation(w,sgn=1):return add(add(mul(c0,w),mul((1-c0)*dot(axis,w),axis)),mul(sgn*ss,cross(axis,w)))
            normal=rotation(base);assert normal==add(mul(c0,base),mul(ss,e))
            for roll in (F(-1,3),F(0),F(1,3)):
                cr=(1-roll*roll)/(1+roll*roll);sr=2*roll/(1+roll*roll)
                def C(w):return add(add(mul(cr,w),mul((1-cr)*dot(base,w),base)),mul(sr,cross(base,w)))
                for height in (-5,0,5):
                    p=vec((7,11,height));pp=project(p,base);rp=root_upper(dot(pp,pp))
                    actual=dot(mu,rotation(p,-1));gamma=dot(mu,p)
                    signed_linear=dot(p,base)*dot(mu,normal)
                    upper=gamma-signed_linear+delta2*(eta*rp-gamma)/4
                    assert actual<=upper;checks+=1
                    moved=project(rotation(p,-1),base)
                    rolled=dot(mu,C(moved));gamma_roll=dot(mu,C(pp))
                    lower=factor*gamma_roll-eta*abs(height)*a-a*a*eta*rp/4
                    assert rolled>=lower;checks+=1
    return {'rank_one_unit_direction_inequalities':rank_cases,
        'signed_receiver_and_rolled_source_inequalities':checks,
        'axes':2,'signed_tilts_including_zero':3,'signed_rolls_including_zero':3,
        'heights_negative_zero_positive':3,'zero_parallel_antiparallel_rank_cases_included':True,
        'ancestor_exact_Rodrigues_identities':reference.rodrigues_audits()}

def require(value):assert value

def malformed_controls():
    rejected=[]
    def reject(name,job):
        try:job()
        except AssertionError:rejected.append(name)
        else:raise AssertionError('malformed evidence accepted: '+name)
    rows=[r for r in REMOTE if r[0]==-1]
    reject('missing closed roll interval',lambda:validate_roll_cover(rows[:-1],F(1,10)))
    gap=list(rows);gap[1]=(gap[1][0],'11/64',*gap[1][2:])
    reject('gap between closed roll intervals',lambda:validate_roll_cover(gap,F(1,10)))
    reject('missing closed facet-cover child',lambda:H.validate_closed_paths(TRI,['0','1','2']))
    reject('overlapping closed facet-cover leaves',lambda:H.validate_closed_paths(TRI,['','0']))
    reject('invalid closed facet-cover digit',lambda:H.validate_closed_paths(TRI,['4']))
    reject('duplicate selected contact',lambda:require(SELECTED+[1]==sorted(set(SELECTED+[1]))))
    reject('missing positive origin contact',lambda:require(all(j in SELECTED[:-1] for j in H.ORIGIN_STRESS)))
    aa,bb,j=H.CONTACTS[SELECTED[0]];mu=cross(sub(V[aa],V[bb]),TRI[2])
    reject('reversed original support',lambda:require(all(dot(mu,sub(V[j],v)).sign()>=0 for v in V)))
    reject('obsolete fullD1 receiver chord1/10',lambda:require(chord_less(triangle(F(1))[2],F(1,10))))
    reject('zero upper for a nonzero perpendicular norm',lambda:require(dot(project(V[45],M),project(V[45],M))<=ZERO))
    # Exact minimal x-z tilt with cos=15/17, sin=8/17.
    reject('discarded receiver quadratic term',lambda:require(F(-15,17)<=F(-1)))
    reject('discarded source quadratic term',lambda:require(F(15,17)>=F(1)))
    reject('false unit angle derivative factor',lambda:require(1-F(1,10)**2/4>1))
    return rejected

def reference_checks():
    # The imported constructor already proves these support, membership and
    # norm inequalities. Reconstruct once here so recorded scope is explicit.
    probes,points,data=reference.reference()
    assert probes==PROBES and points==POINTS and data==DATA
    return {'reference_shadow_facets':len(probes),'original_body_vertices':len(V),
        'original_reference_support_comparisons':len(probes)*len(V),
        'checked_convex_zero_height_source_points':len(points)-len(V),
        'all_actual_source_points':len(points),'signed_source_torque_rows':2*len(points)*len(probes),
        'reference_sha256':H.digest([{'edge':p['edge'],'normal':list(map(str,p['mu'])),
            'support':str(p['H']),'norm_upper':str(p['norm_upper'])} for p in probes])}

def prerequisites():
    checked=pins();ancestor=source.prerequisites()
    with source.audit_signs() as qa,source.audit_radicals() as ra:actual=source.check()
    actual['independent_Q5_sign_audits']=qa;actual['independent_radical_sign_audits']=ra
    assert actual==json.loads((ROOT/'expected_source_extrema.json').read_text())
    with audit_signs() as audit:
        _,full=phase(F(1));_,three_quarter=phase(F(3,4))
        geometry=receiver_geometry();regressions=rank_transport_audits()
        original=reference_checks();controls=malformed_controls()
    return {'agent':'six-rupert-1','role':'researcher','global_Rupert_property':'OPEN',
        'all_original_global_area_hypotheses_replayed':ancestor['all_parent_fields_matched'],
        'original_support_comparisons_replayed':ancestor['parent_support_comparisons'],
        'physical_area_checks_replayed':ancestor['parent_physical_area_checks'],
        'sharp_source_extrema_all_expected_fields_matched':True,'pins':checked,
        'reference':original,'full_D1_phase':full,'D3_4_phase':three_quarter,
        'receiver_geometry':geometry,'exact_transport_regressions':regressions,
        'independent_Q5_sign_audits':audit,'malformed_controls_rejected':controls}

def hull_certificate():
    pins()
    with audit_signs() as audit:
        theta,phase_rec=phase(F(3,4))
        result=selected_hull(TRI,theta,SELECTED,theta+F(1,1000))
    result['phase_sha256']=H.digest(phase_rec);result['independent_Q5_sign_audits']=audit
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);choice=ap.add_mutually_exclusive_group(required=True)
    choice.add_argument('--prerequisites',action='store_true');choice.add_argument('--hull',action='store_true')
    args=ap.parse_args();started=time.monotonic();label='prerequisites' if args.prerequisites else 'hull'
    actual=prerequisites() if args.prerequisites else hull_certificate()
    assert json.loads(json.dumps(actual))==fixture()[label],'every expected mathematical field must match'
    print(json.dumps({'checked':label,'all_expected_fields_match':True,'global_Rupert_property':'OPEN',
        'elapsed_seconds':time.monotonic()-started,'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2))
