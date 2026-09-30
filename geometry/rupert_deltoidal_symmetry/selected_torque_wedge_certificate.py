"""Exact ten-contact closed half-wedge certificate for the deltoidal solid.

Python3.11+ stdlib. Fixed source and facet witnesses, original supports,
all simplex faces. See selected_torque_wedge_proof.md. No float predicates.
"""
import sys,json,itertools,time,resource,argparse,hashlib,copy,math
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).parent
if not __debug__:raise RuntimeError('verification requires assertions; do not use python -O')
import area_sublevel_wedge_certificate as base
import normalized_receiver_piece_certificate as H
from zero_height_wedge_certificate import (P,V,N,M,M2,QMIN,BODY,PROBES,POINTS,DATA,
 root_upper,triangle,linear_envelopes,REMOTE_COVER,validate_roll_cover,W,tW,
 vec,parse,area_maximum,grid_upper,gap_less,chord_less,Q5,ZERO,dot,sub,add,mul,cross)
from orientation_certificate import determinant,area_twice
from stable_certificate import orbit
TRI=triangle(F(1,2));SOURCE_CHORD=F(9,100);SELECTED=list(range(1,11))
PARENT_CHECKER_SHA256='0809a7930ed09b3f604902133c7cc7cb2f5e988780a9b25b6a5900a87cbde280'
PARENT_FIXTURE_SHA256='55ad9ab3fd0513f5c9b47c178d5738dc985be811111a20c5b6e87b8ca52c52ab'

def fixture():return json.loads((ROOT/'expected_selected_torque_wedge.json').read_text())

def phase(tri=TRI,a=SOURCE_CHORD):
 C=vec(map(parse,P["cell_certificates"][9]["area_vector"]));q,arec=area_maximum(C,tri);e=grid_upper(lambda x:gap_less(q,QMIN,x),F(1));T=root_upper(q);source=base.verify_source_cover(T,a,fixture()["source_cover_witnesses"])
 d=max(grid_upper(lambda x:chord_less(M,u,x),F(9,100)) for u in tri)
 assert a<=F(1,5) and d<=F(3,40)
 env=linear_envelopes(tri);gates=[];remote=[];chosen=[];b=F(1,10)
 for sg,pi in [(-1,3),(1,4)]:
  near=DATA[pi][45];probe=PROBES[pi];assert dot(M,V[45])==ZERO and near["d"]==probe["H"] and near["tau"][sg]>0
  assert env[pi]["L"]==ZERO
  E=env[pi]["L"]+probe["norm_upper"]*(near["source_height_upper"]*a+BODY/2*(a*a+d*d));H=probe["H"];tau=near["tau"][sg]
  quad=lambda x:(2*H+E)*x*x-2*tau*x+E
  assert quad(b).sign()<0 and quad(F(0)).sign()>=0
  xup=grid_upper(lambda x:quad(x).sign()<0,b);gates.append({"sign":sg,"probe":pi,"point":45,"error_upper":str(E),"tau_lower":str(tau),"b":str(b),"q_b":str(quad(b)),"small_root_upper":str(xup),"q_upper":str(quad(xup)),"q_predecessor":str(quad(xup-F(1,10**6))),"epsilon":str(2*xup)})
  selected=[r for r in REMOTE_COVER if r[0]==sg];validate_roll_cover(selected,b)
  for sign,los,his,pj,wi in selected:
   lo,hi=F(los),F(his);p=PROBES[pj];row=DATA[pj][wi];H=p["H"];dd=row["d"];tau=row["tau"][sg]
   E=env[pj]["L"]+p["norm_upper"]*(row["source_height_upper"]*a+BODY/2*(a*a+d*d))
   coef=[dd-H-E,Q5(2*tau),-dd-H-E];exact=[coef[0]+coef[1]*x+coef[2]*x*x for x in [lo,hi]]
   assert all(x.sign()>0 for x in exact) and coef[2].sign()<=0
   remote.append({"sign":sg,"interval":[los,his],"probe":pj,"point":wi,"source_point":POINTS[wi][1],
                  "coefficients":list(map(str,coef)),"strict_endpoint_margins":list(map(str,exact))})
  chosen.append((sg,len(set((r["probe"],r["point"]) for r in remote if r["sign"]==sg))))
 r=max(F(g["epsilon"]) for g in gates);product=(1-a*a/4)*(1-d*d/4)*(1-r*r/4);X2=(a+d)**2+r*r
 assert r<=F(1,5) and product>F(99,100)**2 and F(99,100)-a*d/4>0 and X2<=F(1,3)**2
 beta=next(F(j,1000) for j in range(1001,1020) if F(j,1000)**2*(1-X2/4)>1)
 theta=grid_upper(lambda x:Q5(x*x)>Q5(beta*beta*X2),F(1,3))
 return theta,{"area":arec,"source_cover":source,"area_excess_upper":str(e),"receiver_chord_upper":str(d),"source_chord_upper":str(a),"whole_receiver_signed_envelopes":[{k:([*v] if isinstance(v,list) else str(v)) for k,v in row.items()} for row in env],"near_zero_gates":gates,"remote_interval_count":len(remote),"remote_cover":remote,"remote_distinct_witnesses_per_sign":chosen,"roll_chord_upper":str(r),"composition_squared_upper":str(X2),"quaternion_product_margin":str(product-F(99,100)**2),"angle_derivative_factor":str(beta),"angle_derivative_margin":str(beta*beta*(1-X2/4)-1),"full_angle_upper":str(theta)}

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
    failure=None
    return {'agent':'six-rupert-1','role':'researcher','global_Rupert_property':'OPEN',
            'status':'complete exact selected affine-hull hypotheses; written unformalized continuous proof',
            'selected_original_contact_ids':selected,'receiver_rays':[list(map(str,u)) for u in tri],
            'theta':str(theta),'radius':str(rho),'strict_remainder_margin':str(rho-theta),
            'denominators':scalings,'actual_support_comparisons':support_count,
            'origin_stress_original_ids':H.ORIGIN_STRESS,'positive_origin_cubic_coefficients':40,
            'all_three_origin_balance_coordinates_identically_zero':True,
            'all_potential_triples':len(records),'all_seven_faces':list(map(list,H.FACES)),
            'all_facet_strata':sum(counts.values()),'base_classifications':counts,
            'coefficient_sha256':coeff.hexdigest(),'case_sha256':H.digest(records),
            'arithmetic_audits':audits,'unresolved':[(r['original_triple'],[i for i,c in enumerate(r['cases']) if c[0]=='unresolved']) for r in records if any(c[0]=='unresolved' for c in r['cases'])],
            'refinements':refinements,'refinement_sha256':refhash.hexdigest(),'failure':failure}


def verify_fixed_refinement(values,ids,rho,tri,paths,coeff):
    """Reconstruct every fixed closed patch, not the adaptive search policy."""
    H.validate_closed_paths(tri,paths)
    nodes=set()
    for path in paths:nodes.update(path[:i] for i in range(len(path)+1))
    ordered=sorted(nodes);wanted=set(paths)
    counts=dict.fromkeys(['opposite','distance','degenerate','unresolved'],0);leaf_counts=counts.copy()
    records=[];audits=0;lam=(F(1,2),F(1,3),F(1,6))
    for path in ordered:
        val=values
        for digit in path:val=[H.split_values(G)[int(digit)] for G in val]
        n,height,gaps,distance=H.facet_polynomials(val,ids,rho)
        coeff.update(json.dumps([list(ids),path],separators=(',',':')).encode())
        for poly in [*n,height,*gaps,distance]:coeff.update(json.dumps(H.serialize(poly),separators=(',',':')).encode())
        actual=[vec(sum((lam[s]*G[s][k] for s in range(3)),ZERO) for k in range(3)) for G in val]
        a,b,c=[actual[j] for j in ids];direct_n=cross(sub(b,a),sub(c,a));direct_h=dot(direct_n,a)
        assert vec(H.peval(poly,lam) for poly in n)==direct_n and H.peval(height,lam)==direct_h
        assert all(H.peval(poly,lam)==dot(direct_n,t)-direct_h for poly,t in zip(gaps,actual))
        assert H.peval(distance,lam)==direct_h*direct_h-rho*rho*dot(direct_n,direct_n)
        audits+=len(values)+3
        row=[H.classify(n,gaps,distance,f) for f in H.FACES]
        for kind,_ in row:counts[kind]+=1
        records.append([path,[[kind,list(witness)] for kind,witness in row]])
        if path in wanted:
            assert all(kind!='unresolved' for kind,_ in row),('false closed facet leaf',ids,path)
            for kind,_ in row:leaf_counts[kind]+=1
    assert leaf_counts['unresolved']==0
    return {'triple':list(ids),'nodes':len(ordered),'closed_leaf_paths':paths,'max_leaf_depth':max(map(len,paths)),
            'all_node_classifications':counts,'all_leaf_classifications':leaf_counts,
            'all7faces_checked_on_each_closed_leaf':True,'arithmetic_audits':audits,
            'terminal_unresolved_strata':0,'case_record_sha256':H.digest(records)}

def hull_certificate():
    theta,rec=phase();result=selected_hull(TRI,theta,SELECTED,theta+F(1,100))
    result['phase']=rec;return result

def receiver_geometry():
    def weak_inside(u,tri):
        sg=area_twice(tri).sign();assert sg!=0
        return all((cross(sub(b,a),sub(u,a))[2]*sg).sign()>=0 for a,b in zip(tri,tri[1:]+tri[:1]))
    assert all(weak_inside(u,[M,N[8],N[10]]) for u in TRI)
    previous=triangle(F(2,5));assert all(weak_inside(u,TRI) for u in previous)
    assert area_twice(TRI)==F(25,16)*area_twice(previous)
    weights=[F(1,10),F(1,15),F(5,6)];assert sum(weights)==1 and min(weights)>0
    witness=vec(sum((weights[j]*TRI[j][k] for j in range(3)),ZERO) for k in range(3))
    sg=area_twice(TRI).sign()
    assert all((cross(sub(b,a),sub(witness,a))[2]*sg).sign()>0 for a,b in zip(TRI,TRI[1:]+TRI[:1]))
    old=[[M,add(M,mul(F(1,8),sub(N[3],M))),add(M,mul(F(1,4),sub(N[4],M)))],
         [M,add(M,mul(F(1,4),sub(N[4],M))),N[7]],[M,N[7],N[8]],
         [M,N[8],add(M,mul(F(1,6),sub(N[10],M)))],previous]
    images=orbit(witness);assert len(images)==60
    for u in images:
        for a,b,c in old:
            det=determinant(a,b,c);assert det.sign()!=0
            co=[determinant(u,b,c)/det,determinant(a,u,c)/det,determinant(a,b,u)/det]
            assert not(all(x.sign()>=0 for x in co) or all(x.sign()<=0 for x in co))
    centers=orbit(M);assert len(centers)==30;c=1-F(1,50)**2/2
    for v in centers:assert (Q5(c*c)*dot(witness,witness)*dot(v,v)-dot(witness,v)**2).sign()>0
    return {'closed_triangle_rays':[list(map(str,u)) for u in TRI],
            'contains_entire_previous2_5_triangle':True,'unit_z_chart_area_ratio_over_previous':'25/16',
            'spherical_area_ratio_claimed':False,'new_receiver_witness':list(map(str,witness)),
            'witness_barycentric_weights':list(map(str,weights)),'projective_witness_body_orbit':60,
            'old_triangular_cones_checked_per_image':5,'witness_images_in_old_closed_receiver_regions':0,
            'minimum_projective_axes_checked':30,'witness_chord_from_all_signed_minimum_centers_lower':'1/50 > 1/64'}

def require(value):assert value

def malformed_controls():
    rejected=[]
    def reject(name,fn):
        try:fn()
        except AssertionError:rejected.append(name)
        else:raise AssertionError('malformed evidence accepted: '+name)
    cert=fixture()['source_cover_witnesses'];T=F(14788791,10**6)
    reject('missing original source triangle',lambda:base.verify_source_cover(T,SOURCE_CHORD,cert[:-1]))
    bad=copy.deepcopy(cert);idx=next(i for i,r in enumerate(bad) if len(r['leaves'])>1);bad[idx]['leaves'].pop()
    reject('missing closed source leaf',lambda:base.verify_source_cover(T,SOURCE_CHORD,bad))
    reject('obsolete source chord2/25',lambda:base.verify_source_cover(T,F(2,25),cert))
    reject('missing receiver facet-cover child',lambda:H.validate_closed_paths(TRI,['0','1','2']))
    reject('overlapping receiver facet-cover ancestor',lambda:H.validate_closed_paths(TRI,['','0']))
    reject('duplicate receiver facet-cover leaf',lambda:H.validate_closed_paths(TRI,['0','1','2','3','3']))
    reject('invalid receiver facet-cover digit',lambda:H.validate_closed_paths(TRI,['4']))
    reject('duplicate selected contact',lambda:require(SELECTED+[1]==sorted(set(SELECTED+[1]))))
    reject('missing positive origin contact',lambda:require(all(i in SELECTED[:-1] for i in H.ORIGIN_STRESS)))
    aa,bb,j=H.CONTACTS[SELECTED[0]];mu=cross(sub(V[aa],V[bb]),TRI[2])
    reject('reversed original support',lambda:require(all(dot(mu,sub(V[j],v)).sign()>=0 for v in V)))
    def false_ball():
        points=[]
        for i in SELECTED:
            aa,bb,j=H.CONTACTS[i];mu=cross(sub(V[bb],V[aa]),TRI[2]);points.append(cross(V[j],mu))
        for ids in itertools.combinations(range(10),3):
            a,b,c=[points[i] for i in ids];n=cross(sub(b,a),sub(c,a));nn=dot(n,n)
            if nn==ZERO:continue
            h=dot(n,a);gaps=[dot(n,x)-h for x in points]
            if all(x.sign()>=0 for x in gaps) or all(x.sign()<=0 for x in gaps):
                assert (h*h-Q5(10000)*nn).sign()>=0;return
        raise RuntimeError('no actual facet found for negative control')
    reject('false radius100 from plane distances',false_ball)
    reject('false unit angle-derivative factor',lambda:require(1-F(1,10)**2/4>1))
    return rejected

def prerequisites():
    parent_raw=(ROOT/'expected_area_sublevel_wedge.json').read_bytes()
    assert hashlib.sha256(parent_raw).hexdigest()==PARENT_FIXTURE_SHA256
    assert hashlib.sha256((ROOT/'area_sublevel_wedge_certificate.py').read_bytes()).hexdigest()==PARENT_CHECKER_SHA256
    parent_actual=base.prerequisites()
    assert json.loads(json.dumps(parent_actual))==json.loads(parent_raw)['prerequisites']
    theta,rec=phase();d=F(rec['receiver_chord_upper'])
    separation=Q5(F(106,29),F(-36,29));assert (separation-Q5(8*d*d)).sign()>0
    return {'agent':'six-rupert-1','role':'researcher','parent_full_prerequisites_matched':True,
            'parent_checker_sha256':PARENT_CHECKER_SHA256,'parent_fixture_sha256':PARENT_FIXTURE_SHA256,
            'new_source_and_phase':rec,'receiver_geometry':receiver_geometry(),
            'proper_source_fold_audit':base.proper_fold_audit(),'receiver_halfturn_separation_margin':str(separation-Q5(8*d*d)),
            'malformed_controls_rejected':malformed_controls()}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);choice=ap.add_mutually_exclusive_group(required=True)
    choice.add_argument('--prerequisites',action='store_true');choice.add_argument('--hull',action='store_true');args=ap.parse_args()
    start=time.monotonic();data=fixture();label='prerequisites' if args.prerequisites else 'hull'
    actual=prerequisites() if args.prerequisites else hull_certificate()
    assert json.loads(json.dumps(actual))==data[label],'every expected field must match'
    print(json.dumps({'checked':label,'all_expected_fields_match':True,'elapsed_seconds':time.monotonic()-start,
                      'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'global_Rupert_property':'OPEN'},indent=2))
