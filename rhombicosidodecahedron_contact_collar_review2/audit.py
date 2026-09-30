#!/usr/bin/env python3
"""six-reviewer-2 independent exact contact-collar audit, stdlib only.

Imports pinned previous reviewer code only; no target Python or fixtures.
Regenerates physical contacts, persistent ties, full torque hulls and the
winning probe selection. Continuous global compactness is written in REVIEW.md.
"""
import argparse
import hashlib
import importlib.util
import json
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

PINS={'threshold_audit':'f12b78980722260e5a6b8d777ec008d1de7e5c8c4ceae6a18a652ec42e541763',
      'winning_audit':'1ce270a559c9b86582ff7bae580763490a10468d6cd5367a70927c7f269ac456',
      'winning_expected':'f1ff37922401ce54d6c5ef965acda3bb81d8f0142e1be014abd527a14db4e791'}
ZERO=(0,0);ONE=(1,0)
def require(c,msg='independent contact audit failed'):
    if not c:raise ValueError(msg)
def pin(path,key):require(hashlib.sha256(path.read_bytes()).hexdigest()==PINS[key],key+' pin changed')
def load_geometry(threshold,winning):
    pin(threshold/'audit.py','threshold_audit');pin(winning/'audit.py','winning_audit');pin(winning/'expected.json','winning_expected')
    spec=importlib.util.spec_from_file_location('reviewer2_threshold_geometry',threshold/'audit.py')
    g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);k=g.load_kernel(winning/'audit.py')
    globals().update({n:getattr(g,n) for n in ['add','sub','neg','mul','sc','div','sign','dot','va','vs','vc','cross','det','act','mm','identity','rational_ray','sum_field','PH','enc','minimum','scaled','field_vector_encode']})
    return g,k,json.loads((winning/'expected.json').read_text())
def encode_vector(v):return [enc(x) for x in v]
def canonical_probe(probe):
    w,e=probe;return min((w,e),(vc(w,-1),vc(e,-1)))

def hull_planes(points):
    points=sorted(set(points));require(len(points)>=4,'three-dimensional hull needs four points')
    rank=next((quad for quad in combinations(points,4) if det(*(vs(t,quad[0]) for t in quad[1:]))!=ZERO),None)
    require(rank is not None,'torque affine rank is below three')
    planes=set();sides=0
    for a,b,c in combinations(points,3):
        m=cross(vs(b,a),vs(c,a))
        if m==(ZERO,ZERO,ZERO):continue
        h=dot(m,a);gaps=[sign(sub(dot(m,t),h)) for t in points];sides+=len(points)
        if max(gaps)>0 and min(gaps)<0:continue
        require(min(gaps)!=max(gaps),'all torque points on a plane')
        if min(gaps)>=0:m=vc(m,-1);h=neg(h)
        require(sign(h)>0,'torque origin is not strict interior')
        normal=scaled(m,div(ONE,h));require(all(sign(sub(ONE,dot(normal,t)))>=0 for t in points),'incorrect supporting plane')
        planes.add(normal)
    require(planes,'no complete hull facets')
    distance=minimum([div(ONE,dot(m,m)) for m in planes])
    return sorted(planes),distance,sides

def actual_contacts(g,V,n,D):
    g.proper(D)
    data=g.shadow(V,n,16);H=data['hull'];circle=data['circle'];require(len(circle)==8,'complete eight-point circle')
    preimages=[]
    for p in H:
        vv=[v for v in V if g.project(v,n)==p];require(len(vv)==1,'original corner preimage is not unique');preimages.append(vv[0])
    active={v for v in V if g.project(v,n) in circle};shared=set(V)&{act(D,v) for v in V}
    require(len(active)==8 and active<=shared,'not all original active source contacts are shared')
    records=[];probes=[];facets=set();torques=set();minimum_gaps=[];Dt=tuple(zip(*D))
    for j,(p,a,b) in enumerate(zip(H,preimages,preimages[1:]+preimages[:1])):
        e=vs(b,a);m=cross(e,n)
        for w in sorted(active):
            if dot(m,vs(p,w))!=ZERO:continue
            require(w in V and dot(e,e)==(4,0) and (va(w,e) in V or vs(w,e) in V),'non-original endpoint or length-two edge')
            require(dot(m,m)!=ZERO,'zero actual support normal')
            gaps=[dot(m,vs(w,v)) for v in V];require(all(sign(x)>=0 for x in gaps),'original point outside receiving support')
            ties=[v for v,x in zip(V,gaps) if x==ZERO]
            require(len(ties)==2 and all(cross(vs(w,v),e)==(ZERO,ZERO,ZERO) for v in ties),'support ties do not persist for every normal')
            original_source=act(Dt,w);require(original_source in V and act(D,original_source)==w,'non-original proper source preimage')
            gap=minimum([x for x in gaps if sign(x)>0]);T=cross(w,m)
            probes.append((w,e));facets.add(j);torques.add(T);minimum_gaps.append(gap)
            records.append([j,encode_vector(w),encode_vector(e),encode_vector(original_source),[encode_vector(v) for v in ties],enc(gap),encode_vector(T)])
    require(len(probes)==len(set(probes))==16 and len(facets)==10 and len(torques)==8,'complete contact/facet/torque counts')
    require(all((vc(w,-1),vc(e,-1)) in probes for w,e in probes),'missing original antipodal support partner')
    planes,distance,sides=hull_planes(torques);require(len(planes)==12 and sides==448,'complete eight-point torque hull')
    stream=json.dumps({'contacts':records,'normalized_facet_planes':[encode_vector(m) for m in planes]},separators=(',',':'))
    return {'complete_original_receiving_support_comparisons':960,'contacts':16,'selected_full_receiving_facets':10,
            'distinct_torques':8,'proper_branch_shared_original_vertices':len(shared),'active_shared_original_vertices':8,
            'all_torque_triples':56,'all_torque_plane_side_checks':sides,'full_torque_facets':12,
            'minimum_positive_raw_original_gap':enc(minimum(minimum_gaps)),
            'minimum_squared_raw_torque_origin_distance':enc(distance),'generated_original_contacts_and_hull_sha256':hashlib.sha256(stream.encode()).hexdigest()},minimum(minimum_gaps),distance

def local_bound(n,gap,distance,rho,delta,theta):
    B=F(9,2);ray_upper=F(11,10)
    require(delta>0 and rho>0 and theta>0,'nonpositive local parameter')
    require(sign(sub((ray_upper**2,0),dot(n,n)))>0,'incorrect raw reference norm bound')
    require(sign(sub((B**2,0),(11,4)))>0,'incorrect original body radius bound')
    require(sign(sub(distance,(rho*rho,0)))>0,'unsupported raw torque radius')
    require(sign(sub(gap,(18*delta*ray_upper,0)))>0,'original support gap cannot cover the closed receiving cap')
    ball=rho/(ray_upper*B)-2*delta;require(ball>theta,'full relative angle cannot be covered')
    return {'unit_normal_chord_cap':str(delta),'strict_raw_torque_radius_lower':str(rho),
            'unit_support_gap_change_Lipschitz_upper':'18','normalized_torque_change_Lipschitz_upper':'2',
            'reference_ray_norm_upper':'11/10','common_support_normalization':'9/2','full_principal_angle_upper':str(theta),
            'strict_unit_normalized_torque_ball_lower':str(ball),'strict_full_angle_margin_lower':str(ball-theta)}

def winning_tail(g,k,V,G,previous):
    A,B,D,U=k.chart();N=dot(B,B);walls=((ONE,ZERO,ZERO),(ZERO,ONE,ZERO),(neg(PH),neg(mul(PH,PH)),ONE))
    centers={act(M,B) for M in G};require(len(centers)==20,'complete directed winning center orbit')
    margin=div(sub((2,0),PH),(3,0))
    for c in centers:
        if c==B:continue
        negative=[div(mul(dot(w,c),dot(w,c)),mul(dot(w,w),N)) for w in walls if sign(dot(w,c))<0]
        require(negative and all(sign(sub(x,margin))>=0 for x in negative),'another winning center can approach closed chamber')
    require(sign(sub(margin,(F(1,24)**2,0)))>0,'chamber separation does not dominate winning chord')
    for w in walls:
        reflection=tuple(tuple(sub(identity()[i][j],div(sc(mul(w[i],w[j]),2),dot(w,w))) for j in range(3)) for i in range(3))
        require({act(reflection,v) for v in V}==set(V) and tuple(tuple(neg(x) for x in row) for row in reflection) in G,'chamber fold is not an actual body symmetry')
    q=F(57,125);beta=div(sub((19,0),sc(PH,8)),(29,0));require(sign(sub(beta,(q*q,0)))>0,'no strict lower axial cut')
    c0=g.sqrt_field((F(1,3),0));s=g.sqrt_field((F(2303,2304),0))
    require(c0[1]-F(1,8)*s[0]<q,'winning f>q does not imply chord<1/24')
    hexagon,_=k.boundary_geometry([vc(v,2) for v in V])
    cut=((-1,0),(2,1),(-1,0));require(dot(cut,B)!=ZERO and sign(dot(cut,B))>0,'wrong signed original cut vertex')
    require([dot(cut,u) for u in U]==[dot(cut,B),(q,0),(q,0)],'closed cut triangle intercepts')
    require(sign(sub(dot(cut,A),(q,0)))<0 and sign(sub(dot(cut,D),(q,0)))<0,'cut does not select the B corner')
    for u in U:
        require(sign(sub((F(27,25)**2,0),dot(u,u)))>0,'winning chart norm exceeds bound')
        require(all(sign(dot(w,u))>=0 for w in walls),'cut vertex lies outside closed chamber')
    # Regenerate every admissible original length-two edge endpoint probe,
    # without consuming the author's 36-probe fixture or any target module.
    pool=[];edge_count=0
    for a,b in combinations(V,2):
        e=vs(b,a)
        if dot(e,e)!=(4,0):continue
        edge_count+=1
        for w in (a,b):
            for ee in (e,vc(e,-1)):
                if all(sign(dot(cross(ee,n),vs(w,v)))>=0 for n in (A,B,D) for v in V):pool.append((w,ee))
    require(edge_count==120 and len(pool)==36,'complete original edge/probe enumeration changed')
    center={cross(w,cross(e,B)):canonical_probe((w,e)) for w,e in pool};require(len(center)==18,'complete winning center torques')
    planes,_,_=hull_planes(center);require(len(planes)==15,'complete winning center hull facets')
    selected=[]
    for T,probe in center.items():
        incident=[m for m in planes if dot(m,T)==ONE]
        if any(det(*triple)!=ZERO for triple in combinations(incident,3)):selected.append(probe)
    require(len(selected)==10,'ten winning torque extremes not independently recovered')
    old=previous['torque_continuum'];published={canonical_probe((tuple(k.decode(x) for x in p['vertex']),tuple(k.decode(x) for x in p['edge']))) for p in old['selected_probes_phi_basis']}
    require(set(selected)==published,'reconstructed probes differ from previously certified full-triangle theorem')
    require(old['tested_stronger_radius']=='51/100' and old['stronger_radius_certified'] and old['facet_triples']==120 and old['simplex_strata']==7,'missing previously independently certified uniform torque theorem')
    supports=0
    for w,e in selected:
        for u in U:
            for v in V:require(sign(dot(cross(e,u),vs(w,v)))>=0,'original cut triangle support lost');supports+=1
    ball=F(51,100)/F(27,25)/F(9,2);require(ball==F(17,162)>F(1,10),'improved winning full-angle bound')
    return {'directed_winning_centers':20,'all_chamber_wall_body_symmetries_verified':3,'other_center_closed_chamber_separation_squared_lower':enc(margin),
            'axial_cut':'57/125','winning_region_chord_upper':'1/24','positive_active_hexagon_regenerated':hexagon,
            'actual_cut_triangle':[encode_vector(u) for u in U],'all_original_body_edges_enumerated':edge_count,
            'all_original_ABD_persistent_probes':36,'winning_center_torques':18,'winning_center_facets':15,'fresh_selected_extreme_probes':10,
            'fresh_selected_probes_match_previous_uniform51over100_theorem':True,'cut_triangle_original_support_checks':supports,
            'inherited_uniform_raw_torque_radius':'51/100','unit_normalized_torque_ball_lower':str(ball),
            'improved_full_near_body_principal_angle_upper':'1/10','strict_full_angle_margin_lower':str(ball-F(1,10)),
            'prior840case_uniform_torque_polynomial_proof_rerun':False}

def controls(g,V,n,gap,distance,C):
    rho=F(5,11);delta=F(1,240);theta=F(1,12)
    failures=[lambda:local_bound(n,gap,distance,F(1,2),delta,theta),
              lambda:local_bound(n,gap,distance,rho,F(1,100),theta),
              lambda:local_bound(n,gap,distance,rho,delta,F(1,10)),
              lambda:local_bound(n,gap,distance,rho,F(-1,240),theta),
              lambda:hull_planes([(ZERO,ZERO,ZERO),(ONE,ZERO,ZERO),(ZERO,ONE,ZERO),(ONE,ONE,ZERO)]),
              lambda:actual_contacts(g,V,n,tuple(tuple(neg(x) for x in row) for row in identity())),
              lambda:actual_contacts(g,V[:-1],n,C)]
    for f in failures:
        try:f()
        except ValueError:pass
        else:raise ValueError('malformed control accepted')
    return len(failures)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--threshold-review',type=Path,required=True);p.add_argument('--winning-review',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args()
    g,k,previous=load_geometry(a.threshold_review,a.winning_review);V=[vc(v,F(1,2)) for v in k.original_vertices()]
    require(len(V)==60 and all(dot(v,v)==(11,4) and vc(v,-1) in V for v in V),'standard original body')
    G=g.body_group(V);R,C=g.alignments(G);low=(ZERO,sc(sub((2,0),PH),F(1,3)),(-1,0));high=(ZERO,ONE,div(sub(sc(PH,3),ONE),(11,0)))
    cases=[];saved=[]
    for label,n,D,original_rho,theta,rho in [('lower',low,identity(),F(7,20),F(1,16),F(6,17)),('higher',high,C,F(9,20),F(1,12),F(5,11))]:
        record,gap,distance=actual_contacts(g,V,n,D)
        expected_gap=sc(sub((4,0),sc(PH,2)),F(1,3)) if label=='lower' else sc(add((-28,0),sc(PH,18)),F(1,11))
        expected_distance=div(add((1328,0),sc(PH,304)),(14589,0)) if label=='lower' else div(add((9692,0),sc(PH,15056)),(164681,0))
        require(gap==expected_gap and distance==expected_distance,'claimed exact original gap or torque distance differs')
        native=local_bound(n,gap,distance,original_rho,F(1,300),theta);strong=local_bound(n,gap,distance,rho,F(1,240),theta)
        cases.append({'reference_orbit':label,'reference_ray':encode_vector(n),'actual_contacts_and_full_hull':record,'confirmed_original_cap':native,'proved_larger_near_branch_cap':strong});saved.append((n,gap,distance))
    # The higher receiving contacts also apply to the body branch.
    high_body,_,_=actual_contacts(g,V,high,identity());require(high_body['proper_branch_shared_original_vertices']==60,'higher body source contacts')
    winning=winning_tail(g,k,V,G,previous);tests=controls(g,V,*saved[1],C)
    result={'agent':'six-reviewer-2','role':'independent mathematical reviewer','target_python_modules_or_fixtures_used':False,
            'arithmetic':'exact Q(sqrt5) coefficient pairs; Fraction; pinned reviewer-authored positive dyadic brackets for winning chord',
            'previous_reviewer_dependency_sha256':PINS,'full_proper_group_reconstructed':60,'reference_contact_certificates':cases,
            'higher_body_branch_same_contacts_verified':True,'winning_closed_limit_tail_audit':winning,'malformed_controls_rejected':tests,
            'global_positive_slack':'Existential, via written compactness proof in REVIEW.md; no numerical epsilon or all-source cap radius.',
            'numerical_global_epsilon_certified':False,'global_non_rupert_proved':False,'continuous_bridges_formalized':False}
    data=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if a.output:a.output.write_text(data)
    else:print(data,end='')
if __name__=='__main__':main()
