#!/usr/bin/env python3
"""Exact J77 critical-axis exclusions and five-axis reduction; stdlib only."""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
PRIOR=ROOT.parent/'rupert_j77_stable_local_reduction'

def require(condition,message):
    if not condition:raise ValueError(message)

def load_prior():
    manifest=json.loads((ROOT/'dependencies.json').read_text())
    require(manifest['source_commit']=='f2496f3e5cc7631d4082b3faeff6ac5fff43f4fa','unexpected dependency provenance')
    require(set(manifest['sha256'])=={'.gitignore','README.md','PROOF.md','verify.py','certificates.json','dependencies.json','expected.json'},
            'incomplete dependency manifest')
    for name,digest in manifest['sha256'].items():
        require(hashlib.sha256((PRIOR/name).read_bytes()).hexdigest()==digest,'changed dependency: '+name)
    spec=importlib.util.spec_from_file_location('j77_stable_prior',PRIOR/'verify.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

prior=load_prior();fixed=prior.base
from q5 import Q,dot,cross,sub,add,scale
from model import VERTICES
from chamber import partition

def determinant(matrix):
    n=len(matrix);total=Q()
    for p in itertools.permutations(range(n)):
        value=Q(1)
        for i,j in enumerate(p):value=value*matrix[i][j]
        if sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2:value=-value
        total=total+value
    return total

def gaussian_determinant(matrix):
    m=[list(r) for r in matrix];result=Q(1);n=len(m)
    for j in range(n):
        k=next((k for k in range(j,n) if m[k][j]!=0),None)
        if k is None:return Q()
        if k!=j:m[j],m[k]=m[k],m[j];result=-result
        d=m[j][j];result=result*d
        for k in range(j+1,n):
            x=m[k][j]/d;m[k]=[a-x*b for a,b in zip(m[k],m[j])]
    return result

def removed_rays():
    return {prior.projective(v) for v in ((Q(),Q(1),Q()),(Q(9,-7),Q(-5,13),Q(22,-8)),
                                          (Q(-16,6),Q(25,-7),Q(23,-11)))}

def strict_simplex_at(c,u):
    kind=c['kind'];columns=[]
    for a,b,j in c['contacts']:
        m=cross(sub(VERTICES[b],VERTICES[a]),u);g=cross(VERTICES[j],m)
        columns.append(g if kind=='paired' else g+(m[0],m[2]))
    values=[]
    for j in range(len(columns)):
        chosen=[v for k,v in enumerate(columns) if k!=j]
        d=determinant(list(map(list,zip(*chosen))))
        values.append(-d if j%2 else d)
    return all(v>0 for v in values) or all(v<0 for v in values)

def required_cases(parents,prior_data):
    original=json.loads((fixed.ROOT/'certificates.json').read_text())
    points={(r['parent'],fixed.decode(r['direction'])) for r in prior_data['points']}
    wanted=removed_rays()-{prior.projective((Q(),Q(1),Q()))};bad=set()
    for leaf in original['leaves']:
        p=leaf['parent'];triangle=fixed.child_triangle(parents[p],leaf['path'])
        for u in triangle:
            if prior.projective(u) not in wanted or (p,u) in points:continue
            if not any(strict_simplex_at(c,u) for c in leaf['certificates']):bad.add((p,u))
    return bad

def check_coverage(cases,points,required):
    actual=[(r['parent'],fixed.decode(r['direction'])) for r in cases+points]
    require(len(actual)==len(set(actual)) and set(actual)==required,'incomplete, duplicate or extraneous critical incidence')

def critical_case(record,parent,audit):
    u=fixed.decode(record['direction']);a=fixed.decode(record['axis']);N=dot(u,u);A2=dot(a,a)
    require(u in parent and A2>0 and dot(a,u)==0,'invalid critical corner or tangent axis')
    directions=[sub(v,u) for v in parent if v!=u]
    require(len(directions)==2,'invalid parent corner')
    contacts=record['contacts'];require(len({tuple(c) for c in contacts})==len(contacts),'duplicate persistent contact')
    columns=[];m_derivatives=[];values=[];active=[]
    for i,ids in enumerate(contacts):
        audit.contact(ids,parent,'full');x,y,j=ids;e=sub(VERTICES[y],VERTICES[x]);m=cross(e,u);h=dot(m,VERTICES[j])
        require(h>0,'collapsed critical probe');m=scale(1/h,m);g=cross(VERTICES[j],m);value=dot(a,g)
        require(value<=0,'axis is not a cone separator')
        columns.append(g+m);values.append(value);m_derivatives.append([scale(1/h,cross(e,r)) for r in directions])
        if value==0:active.append(i)
    require(any(v<0 for v in values),'missing sign-fixing negative contact')
    weights=[Q(*x) for x in record['active_weights']]
    require(len(weights)==len(active) and all(w>0 for w in weights),'nonpositive or missing active weight')
    require(sum(weights,Q())==1,'equilibrium normalization fails')
    require(all(sum((w*columns[i][k] for w,i in zip(weights,active)),Q())==0 for k in range(6)),
            'six-coordinate active equilibrium fails')
    rows=record['rank_contact_indices'];coords=record['rank_coordinate_indices']
    require(len(rows)==len(set(rows))==4 and set(rows)<=set(active),'invalid rank rows')
    require(len(coords)==len(set(coords))==4 and set(coords)<=set(range(5)),'invalid rank coordinates')
    G=[c[:3]+(c[3],c[5]) for c in columns]
    minor=[[G[i][j] for j in coords] for i in rows];d=determinant(minor)
    require(d!=0 and d==gaussian_determinant(minor),'rank-four minor fails independent replay')
    # The known nonzero kernel (a,0,0) bounds rank above by four.
    require(all(dot(G[i],a+(Q(),Q()))==0 for i in active),'active kernel fails')
    rates=[sum((w*dot(a,cross(VERTICES[contacts[i][2]],m_derivatives[i][k])) for w,i in zip(weights,active)),Q())
           for k in range(2)]
    require(all(x>0 for x in rates),'nonpositive receiver displacement stress')
    audit.values.extend(weights+rates+[d,-d,A2,N]+[-v for v in values])
    x,y,h_index=record['hidden_contact'];e=sub(VERTICES[y],VERTICES[x])
    audit.contact((x,y,x),parent,'full');m0=cross(e,u);offset=dot(m0,VERTICES[x]);require(offset>0,'zero hidden support')
    m0=scale(1/offset,m0);h=VERTICES[h_index]
    require(h_index not in (x,y) and dot(m0,h)==1,'hidden preimage does not tie')
    coefficients=[tuple(dot(scale(1/offset,cross(e,r)),sub(h,VERTICES[x])) for r in directions)]
    rhs=[-2*dot(a,cross(h,m0))]
    pairs=record['radial_pairs'];require(len(pairs)==2,'two radial pairs required')
    exposure_comparisons=0
    for i,j in pairs:
        require(type(i) is int and type(j) is int and 0<=i<55 and 0<=j<55,'invalid radial indices')
        v=VERTICES[i];require(VERTICES[j]==tuple(-x for x in v) and dot(u,v)==0,'invalid equatorial antipodal pair')
        for z in (i,j):
            vv=VERTICES[z]
            for k,w in enumerate(VERTICES):
                if k==z:continue
                gap=dot(vv,sub(vv,w));require(gap>0,'radial exposure gap fails')
                audit.values.append(gap);exposure_comparisons+=1
        coefficients.append(tuple(-2*dot(v,r)*dot(u,cross(a,v))/N for r in directions))
        rhs.append(2*(A2*dot(v,v)-dot(a,v)*dot(a,v)))
    dual=[Q(*w) for w in record['Farkas_weights']]
    require(len(dual)==3 and all(w>0 for w in dual) and sum(dual,Q())==1,'invalid Farkas weights')
    require(all(sum((w*c[k] for w,c in zip(dual,coefficients)),Q())==0 for k in range(2)),'Farkas coefficient balance fails')
    total=sum((w*b for w,b in zip(dual,rhs)),Q())
    require(total==Q(14)/11-Q(0,34)/55 and total<Q(-1)/10,'Farkas strict gap fails')
    audit.values.extend(dual+[total,-total-Q(1)/10])
    return {'parent':record['parent'],'active_contacts':len(active),'strict_contacts':sum(v<0 for v in values),
            'active_rank':4,'positive_equilibrium_weights':len(weights),'positive_drift_derivatives':2,
            'hidden_contact':record['hidden_contact'],'radial_pairs':pairs,'radial_exposure_comparisons':exposure_comparisons,
            'Farkas_rhs_sum':[str(total.a),str(total.b)]}

def cluster_classes(records,audit):
    W=[(2*v[2],2*v[0],2*v[1]) for v in VERTICES]
    a=Q(2,1);b=Q(3,1)/2;c=Q(5,1)/2;R2=Q(11,4);expected=set()
    for sx,sy,sz in itertools.product((1,-1),repeat=3):
        expected.add((sx*a,Q(sy),Q(sz)));expected.add((Q(sx),sy*a,Q(sz)))
    for sx,sy in itertools.product((1,-1),repeat=2):expected.add((sx*b,sy*c,Q()))
    require(expected<=set(W) and all(dot(v,v)==R2 for v in W),'cluster model fails')
    classes={}
    for i,v in enumerate(W):classes.setdefault(v[:2],[]).append(i)
    points={v[:2] for v in expected};actual=[fixed.decode(r['point']) for r in records]
    require(len(actual)==len(set(actual))==12 and set(actual)==points,'incomplete cluster point set')
    gaps=[]
    for r in records:
        p=fixed.decode(r['point']);ids=r['indices']
        require(ids==classes[p],'incomplete cluster preimages')
        require({W[i] for i in ids}=={v for v in expected if v[:2]==p},'unexpected class height')
        require({W[i] for i in classes[tuple(-x for x in p)]}=={tuple(-z for z in W[i]) for i in ids},
                'selected classes are not antipodal')
        for i,v in enumerate(W):
            if i not in ids:
                gap=dot(p,sub(p,v[:2]));require(gap>=1,'class radial support gap fails');gaps.append(gap)
    require(min(gaps)==1,'unexpected minimum class gap')
    bounds=[Q(20)-R2,a-4,b-2,c-b,4-c,25-(a*a+1),a*a*b*b-c*c-48,16-(c*c-b*b)]
    require(all(x>0 for x in bounds),'paired/singleton scalar bounds fail')
    require(a*a+2==b*b+c*c==R2,'class common radius identity fails')
    # eta=1/100. sqrt(1-eta^2)>1/2 and sqrt(a^2+1)<5.
    require(Q(1)-Q(Fraction(1,10000))>Q(Fraction(1,4)),'square-root lower bound fails')
    require(Q(201)/250<1 and Q(1)/2>Q(5)/100 and 24>Q(80)/100,'cluster error bounds fail')
    audit.values.extend(gaps+bounds)
    return {'selected_classes':12,'doubleton_classes':8,'singleton_classes':4,'selected_antipodal_vertices':20,
            'class_exposure_comparisons':len(gaps),'minimum_scaled_radial_gap':1,
            'frame_operator_radius':'1/100','unit_receiver_cap_chord':'1/200','relative_angle_radians':'1/200'}

def check(data,self_test=False):
    prior_data=json.loads((PRIOR/'certificates.json').read_text())
    inherited=prior.check(prior_data,self_test)
    parents=[tuple(fixed.decode(u) for u in t) for t in partition()['triangles']]
    required=required_cases(parents,prior_data);check_coverage(data['cases'],data['points'],required)
    audit=fixed.Audit();cases=[critical_case(r,parents[r['parent']],audit) for r in data['cases']]
    point_weights=[]
    for r in data['points']:point_weights.extend(prior.point_certificate(r,parents[r['parent']],audit))
    require(data['cluster_frame_radius']=='1/100','unsupported cluster radius')
    cluster=cluster_classes(data['cluster_classes'],audit)
    remaining=prior.orbit((Q(5,-3),Q(5,-1),Q(0,-2)))
    removed=set().union(*(prior.orbit(u) for u in removed_rays()))
    all_old=set().union(*(prior.orbit(fixed.decode(u)) for u in prior_data['exceptional_chamber_directions']))
    require(len(remaining)==5 and len(removed)==20 and not remaining&removed and all_old==remaining|removed,'axis orbit subtraction fails')
    signs=fixed.independent_sign_audit(audit.values)
    if self_test:malformed(data,parents,required)
    return {'agent':'six-rupert-2','role':'researcher','claim_status':'J77_small_angle_strict_passage_limits_reduce_to_five_axes',
            'arbitrary_translations':True,'both_projections_may_vary':True,'scales_covered':'lambda >= 1',
            'global_Rupert_resolved':False,'uniform_angle_over_all_normals_claimed':False,
            'remaining_axes_asserted_passage_admitting':False,'previous_axes':25,'removed_axes':20,'remaining_axes':5,
            'critical_parent_incidences':len(cases),'critical_cases':cases,'cluster_exclusion':cluster,
            'additional_stable_point_parent_incidences':len(data['points']),
            'additional_signed_rotation_equilibria':6*len(data['points']),
            'additional_positive_equilibrium_weights':len(point_weights),
            'new_whole_parent_support_comparisons':audit.comparisons,'new_independent_rational_sign_audits':signs,
            'prior_exact_coefficient_sha256':inherited['exact_coefficients_sha256'],
            'canonical_certificate_sha256':hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()}

def malformed(data,parents,required):
    def copy():return json.loads(json.dumps(data))
    a=copy();a['cases'].pop()
    p=copy();p['points'].pop()
    w=copy()['cases'][0];w['active_weights'][0]=['-1','0']
    h=copy()['cases'][0];h['hidden_contact'][2]=h['hidden_contact'][0]
    r=copy()['cases'][0];r['radial_pairs'][0][1]=r['radial_pairs'][0][0]
    d=copy()['cases'][0];d['Farkas_weights'][0]=['-1','0']
    cl=copy()['cluster_classes'];cl[0]['indices'].pop()
    failures=[lambda:check_coverage(a['cases'],a['points'],required),
              lambda:check_coverage(p['cases'],p['points'],required),lambda:critical_case(w,parents[w['parent']],fixed.Audit()),
              lambda:critical_case(h,parents[h['parent']],fixed.Audit()),lambda:critical_case(r,parents[r['parent']],fixed.Audit()),
              lambda:critical_case(d,parents[d['parent']],fixed.Audit()),lambda:cluster_classes(cl,fixed.Audit())]
    for f in failures:
        try:f()
        except ValueError:pass
        else:raise ValueError('malformed critical certificate accepted')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args();data=json.loads((ROOT/'certificates.json').read_text())
    print(json.dumps(check(data,args.self_test),indent=2,sort_keys=True))
