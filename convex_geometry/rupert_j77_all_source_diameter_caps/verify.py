#!/usr/bin/env python3
"""Exact all-source J77 receiver caps; standard-library Python 3.11+."""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,importlib.util,itertools,json,sys

ROOT=Path(__file__).resolve().parent
def require(c,m):
    if not c:raise ValueError(m)
manifest=json.loads((ROOT/'dependencies.json').read_text())
required={'convex_geometry/rupert_j77_projection_diameter':'fce6fd20899e14d0e65c564f410e98518df76977',
          'convex_geometry/rupert_j77_translated_local_exclusion':'3ae881c42e58af21905e26f6cdace6215e2e8487'}
require(len(manifest['sources'])==2 and {s['source_directory']:s['source_commit'] for s in manifest['sources']}==required,
        'Invalid source dependency set')
for source in manifest['sources']:
    require(set(source['sha256'])=={'.gitignore','README.md','PROOF.md','verify.py','model.py','q5.py','expected.json'},'Incomplete dependency manifest')
    for name,digest in source['sha256'].items():
        require(hashlib.sha256((ROOT.parent.parent/source['source_directory']/name).read_bytes()).hexdigest()==digest,
                'Changed dependency: '+name)
PRIOR=ROOT.parent/'rupert_j77_translated_local_exclusion'
sys.path.insert(0,str(PRIOR))
spec=importlib.util.spec_from_file_location('j77_caps_local_dependency',PRIOR/'verify.py')
local=importlib.util.module_from_spec(spec);spec.loader.exec_module(local)
from q5 import Q,add,cross,dot,scale,sub
from model import VERTICES,cupola_construction

B=Q(65,10)/596;R2=Q(11,4)/4;D=local.DIRECTION;N=dot(D,D)
M=Q(F(51,100))
def decode(v):return tuple(Q(*x) for x in v)
def encode(v):return [[str(x.a),str(x.b)] for x in v]
def ray(v):
    first=next((x for x in v if x!=0),None)
    require(first is not None,'Zero projective direction')
    return tuple(x/first for x in v)
def cross2(a,b):return a[0]*b[1]-a[1]*b[0]
def hull(points):
    points=sorted(set(points));bottom=[];top=[]
    for stack,sequence in ((bottom,points),(top,list(reversed(points)))):
        for v in sequence:
            while len(stack)>1 and cross2(sub(stack[-1],stack[-2]),sub(v,stack[-1]))<=0:stack.pop()
            stack.append(v)
    return bottom[:-1]+top[:-1]
def candidates(a):
    for i,v in enumerate(a):yield v,['one',i]
    for i,j in itertools.combinations(range(len(a)),2):
        for s in (-1,1):yield add(a[i],scale(s,a[j])),['two',i,j,s]
    for i,j,k in itertools.combinations(range(len(a)),3):
        for s,t in itertools.product((-1,1),repeat=2):
            yield cross(sub(a[i],scale(s,a[j])),sub(a[i],scale(t,a[k]))),['three',i,j,k,s,t]
def witness(a,label):
    if len(label)==2 and label[0]=='one':
        require(type(label[1]) is int and 0<=label[1]<len(a),'Bad one-active witness');return a[label[1]]
    if len(label)==4 and label[0]=='two':
        _,i,j,s=label;require(type(i) is int and type(j) is int and 0<=i<j<len(a) and s in (-1,1),'Bad two-active witness')
        return add(a[i],scale(s,a[j]))
    if len(label)==6 and label[0]=='three':
        _,i,j,k,s,t=label
        require(all(type(x) is int for x in (i,j,k)) and 0<=i<j<k<len(a) and s in (-1,1) and t in (-1,1),'Bad three-active witness')
        return cross(sub(a[i],scale(s,a[j])),sub(a[i],scale(t,a[k])))
    raise ValueError('Invalid candidate label')
def beta_witness(a,label,beta,audit):
    d=witness(a,label);n=dot(d,d);require(n>0,'Zero runner-up witness')
    gaps=[dot(v,d)*dot(v,d)-beta*n for v in a]
    require(all(x>=0 for x in gaps) and any(x==0 for x in gaps),'Runner-up value is not attained')
    audit.extend(gaps)
def candidate_audit(a,beta,orbit,audit):
    winners=set();count=occurrences=comparisons=0;digest=hashlib.sha256()
    for d,label in candidates(a):
        count+=1;n=dot(d,d);require(n>0,'Degenerate candidate');gaps=[]
        for i,v in enumerate(a):
            p=dot(v,d);gap=p*p-beta*n;comparisons+=1;audit.append(gap)
            if gap<=0:
                digest.update((str(count)+':'+str(i)+'\n').encode());break
            gaps.append(p*p-B*n)
        else:
            require(all(x>=0 for x in gaps) and any(x==0 for x in gaps),'Unexpected intermediate or larger candidate')
            normalized=ray(d);require(normalized in orbit,'Unclassified maximizing axis')
            winners.add(normalized);occurrences+=1;audit.extend(gaps)
            digest.update((str(count)+':MAX\n').encode())
    require(count==9825 and winners==set(orbit),'Incomplete candidate count or optimizer coverage')
    return count,comparisons,occurrences,digest.hexdigest()
def reduction_controls():
    basis=[(Q(1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1))]
    for size in (1,2,3):
        a=basis[:size];scores=[]
        for d,label in candidates(a):
            n=dot(d,d)
            if n!=0:scores.append(min(dot(v,d)*dot(v,d)/n for v in a))
        require(max(scores)==Q(1)/size,'Finite reduction branch control fails')
    return 3
def full_diameters(orbit,audit):
    checks=0;active=[]
    for d in orbit:
        n=dot(d,d);hits=[]
        for i,j in itertools.combinations(range(55),2):
            v=sub(VERTICES[i],VERTICES[j]);p=dot(v,d);gap=4*(R2-B)-dot(v,v)+p*p/n
            require(gap>=0,'Full body exceeds claimed minimum diameter');audit.append(gap);checks+=1
            if gap==0:hits.append([i,j])
        require(hits,'No full-body diameter attainer');active.append(hits)
    require(checks==7425,'Incomplete full-body checks')
    return checks,active
def nonpaired_gap(audit):
    gaps=[]
    for i,j in itertools.combinations(range(55),2):
        if VERTICES[j]==scale(-1,VERTICES[i]):continue
        v=sub(VERTICES[i],VERTICES[j]);p=dot(v,D);gap=4*(R2-B)-dot(v,v)+p*p/N
        require(gap>0,'Nonantipodal pair attains minimum-view diameter');gaps.append(gap);audit.append(gap)
    require(len(gaps)==1460,'Wrong nonantipodal pair count')
    return min(gaps)
def axial_ball(ids,audit):
    active=[];height=None
    for i in ids:
        p=dot(VERTICES[i],D)
        if p*p==B*N:
            h=p if p>=0 else -p
            if height is None:height=h
            require(h==height,'Inconsistent critical heights');active.append((i,scale(p.sign(),VERTICES[i])))
    require(len(active)==4 and height*height==B*N,'Wrong active axial set')
    tangent=[sub(v,scale(height/N,D)) for i,v in active]
    project=lambda v:(v[0],D[2]*v[1]+v[2])
    points=hull(map(project,tangent));require(len(points)==4,'Wrong active tangent polygon')
    by_point={project(v):v for v in tangent};squares=[]
    for i,p in enumerate(points):
        q=points[(i+1)%4];v=by_point[p];w=by_point[q];m=cross(sub(w,v),D);offset=dot(m,v)
        if offset<0:m=scale(-1,m);offset=-offset
        require(offset>0 and all(dot(m,g)<=offset for g in tangent),'Tangent facet fails')
        square=offset*offset/dot(m,m);require(square>Q(1)/4,'Tangent inradius is not greater than 1/2')
        squares.append(square);audit.extend([offset,square-Q(1)/4])
    return [i for i,v in active],min(squares)
def reference_geometry(audit):
    cycle=local.SUPPORT_CYCLE;project=lambda v:(v[0],D[2]*v[1]+v[2])
    actual=hull(map(project,VERTICES));given=[project(VERTICES[i]) for i in cycle]
    require(len(actual)==len(given)==17 and any(given==actual[k:]+actual[:k] for k in range(17)),'Changed complete shadow cycle')
    require(all(sum(project(v)==p for v in VERTICES)==1 for p in actual),'Extreme shadow preimage is not unique')
    mirror=lambda v:(-v[0],v[1],v[2])
    require({mirror(v) for v in VERTICES}==set(VERTICES) and mirror(D)==D,'Required body mirror is invalid')
    normals=[]
    for i,j in zip(cycle,cycle[1:]+cycle[:1]):
        m=cross(sub(VERTICES[j],VERTICES[i]),D);offset=dot(m,VERTICES[i]);require(offset>0,'Reversed outer edge')
        m=scale(1/offset,m)
        require(dot(m,D)==0 and dot(m,VERTICES[j])==1,'Wrong support incidence')
        gaps=[1-dot(m,v) for v in VERTICES]
        require(all(x>=0 for x in gaps),'Reference edge is not supporting')
        require(dot(m,m)<M*M,'Reference probe norm bound fails')
        normals.append(m);audit.extend(gaps+[M*M-dot(m,m)])
    centroid=tuple(sum((p[k] for p in actual),Q())/17 for k in range(2))
    centered=[sub(p,centroid) for p in actual]
    metric=lambda v,w:v[0]*w[0]+v[1]*w[1]/N
    gram=[[metric(v,w) for w in centered] for v in centered];isometries=[]
    for sign in (1,-1):
        for shift in range(17):
            if all(gram[i][j]==gram[(shift+sign*i)%17][(shift+sign*j)%17] for i in range(17) for j in range(17)):
                isometries.append([sign,shift])
    require([x for x in isometries if x[0]==1]==[[1,0]] and len(isometries)==2,'Unexpected planar isometry group')
    return normals,isometries,centroid
def half_turn(data,normals,audit):
    ids=data['half_turn_indices'];weights=decode(data['half_turn_weights'])
    require(len(ids)==len(set(ids))==len(weights)==3 and all(type(i) is int and 0<=i<17 for i in ids),'Invalid half-turn support set')
    require(all(w>0 for w in weights) and sum(weights,Q())==1,'Invalid half-turn weights')
    require(all(sum((w*normals[i][k] for w,i in zip(weights,ids)),Q())==0 for k in range(3)),'Half-turn normals do not balance')
    gaps=[max(-dot(normals[i],v) for v in VERTICES)-1 for i in ids]
    gap=sum((w*g for w,g in zip(weights,gaps)),Q());require(gap>Q(1)/20,'Half-turn gap is too small')
    audit.extend(list(weights)+gaps+[gap-Q(1)/20])
    return gap
def cover_shape(data):
    a=F(data['roll_tangent_threshold'])
    require(len(data['covers'])==2 and {c['sign'] for c in data['covers']}=={-1,1},'Missing roll sign')
    for c in data['covers']:
        require(c['pieces'],'Empty roll cover');endpoint=a
        for piece in c['pieces']:
            lo,hi=map(F,piece['interval']);require(lo==endpoint and a<=lo<hi<=1,'Gap, overlap or invalid roll interval')
            require(type(piece['probe']) is int and 0<=piece['probe']<17 and piece['orientation'] in (-1,1),'Invalid support probe')
            pair=piece['source_pair'];require(len(pair)==2 and pair[0]!=pair[1] and all(type(i) is int and 0<=i<55 for i in pair),'Invalid difference vertex')
            endpoint=hi
        require(endpoint==1,'Closed roll endpoint omitted')
def quadratic_piece(sign,piece,normals,root_lo,root_hi,gamma,audit):
    m=scale(piece['orientation'],normals[piece['probe']]);i,j=piece['source_pair'];w=sub(VERTICES[i],VERTICES[j])
    height=max(dot(m,v) for v in VERTICES)-min(dot(m,v) for v in VERTICES)
    d=dot(m,w);S=sign*dot(m,cross(D,w));k=S/(root_hi if S>=0 else root_lo)
    p=(d-height,2*k,-d-height);lo,hi=(Q(F(x)) for x in piece['interval'])
    value=lambda x:p[0]+x*(p[1]+x*p[2])
    beta=(value(lo),value(lo)+(hi-lo)*(p[1]+2*p[2]*lo)/2,value(hi))
    # Independent power-basis identity for the three Bernstein coefficients.
    reconstructed=(beta[0],2*(beta[1]-beta[0]),beta[0]-2*beta[1]+beta[2])
    substituted=(value(lo),(hi-lo)*(p[1]+2*p[2]*lo),(hi-lo)*(hi-lo)*p[2])
    require(reconstructed==substituted,'Quadratic Bernstein identity fails')
    require(all(x>=gamma for x in beta),'Quadratic roll lower bound fails')
    audit.extend(list(beta)+[x-gamma for x in beta]+[S])
    return min(beta)
def cap_bounds(data,nonpaired,beta,audit):
    d=Q(F(data['receiver_cap_chord']));a=Q(F(data['roll_tangent_threshold']));gamma=Q(F(data['gap_numerator_lower_bound']))
    require(0<d<=Q(1)/200 and 0<a<1 and gamma>0,'Invalid cap or roll constants')
    margins=[Q(81)/16-R2,B-Q(9)/64,Q(4)/25-B,nonpaired-16*R2*d,
             B-Q(9)/5*d-beta,Q(1)/10-5*d,Q(1)/20-M*(14*d+Q(9)/4*2*a),
             gamma-4*14*d*M,Q(3)/20-(2*a+Q(101)/100*6*d)]
    require(all(x>0 for x in margins),'Cap transfer inequality fails');audit.extend(margins)
    return d,a,gamma,margins
def malformed(data,a,normals,nonpaired,beta):
    def copy():return json.loads(json.dumps(data))
    bad_beta=copy();bad_beta['beta']=encode((B,))[0]
    bad_witness=copy();bad_witness['beta_witness']=['one',0]
    bad_weight=copy();bad_weight['half_turn_weights'][0]=['-1','0']
    bad_sign=copy();bad_sign['covers'].pop()
    bad_endpoint=copy();bad_endpoint['covers'][0]['pieces'][-1]['interval'][1]='9/10'
    bad_probe=copy();bad_probe['covers'][0]['pieces'][0]['orientation']=0
    bad_root=copy();bad_root['root_N_enclosure'][0]='5'
    bad_cap=copy();bad_cap['receiver_cap_chord']='1/1000'
    def beta_config(x):
        v=Q(*x['beta']);require(0<v<B,'Invalid region-gap level')
    def root_config(x):
        lo,hi=(Q(F(v)) for v in x['root_N_enclosure'])
        require(0<lo<hi and lo*lo<N<hi*hi,'Invalid square-root enclosure')
    invalid=[lambda:beta_config(bad_beta),lambda:beta_witness(a,bad_witness['beta_witness'],beta,[]),
             lambda:half_turn(bad_weight,normals,[]),lambda:cover_shape(bad_sign),lambda:cover_shape(bad_endpoint),
             lambda:cover_shape(bad_probe),lambda:root_config(bad_root),lambda:cap_bounds(bad_cap,nonpaired,beta,[])]
    for f in invalid:
        try:f()
        except ValueError:pass
        else:raise ValueError('Malformed all-source certificate accepted')
def check(data,self_test=False):
    inherited=local.check()
    require(inherited==json.loads((PRIOR/'expected.json').read_text()),'Inherited local output mismatch')
    audit=[];beta=Q(*data['beta']);require(0<beta<B,'Invalid region-gap level')
    root_lo,root_hi=(Q(F(x)) for x in data['root_N_enclosure'])
    require(0<root_lo<root_hi and root_lo*root_lo<N<root_hi*root_hi,'Invalid square-root enclosure')
    audit.extend([N-root_lo*root_lo,root_hi*root_hi-N])
    original,core,cap,gyrated,A=cupola_construction()
    ids=[i for i,p in enumerate(VERTICES) if p in core and i<VERTICES.index(scale(-1,p))]
    require(len(ids)==25,'Wrong core pair representatives');points=[VERTICES[i] for i in ids]
    orbit=[ray(v) for v in local.check_model()]
    require(len(set(orbit))==5,'Wrong five-axis orbit')
    beta_witness(points,data['beta_witness'],beta,audit)
    count,comparisons,occurrences,digest=candidate_audit(points,beta,orbit,audit)
    diameter_checks,diameter_active=full_diameters(orbit,audit)
    nonpaired=nonpaired_gap(audit);active,rho2=axial_ball(ids,audit)
    normals,isometries,centroid=reference_geometry(audit)
    pi_gap=half_turn(data,normals,audit);cover_shape(data)
    d,a,gamma,margins=cap_bounds(data,nonpaired,beta,audit)
    minima=[quadratic_piece(c['sign'],p,normals,root_lo,root_hi,gamma,audit) for c in data['covers'] for p in c['pieces']]
    signs=sorted(set(audit),key=lambda x:(x.a,x.b))
    local.independent_sign_audit(signs)
    if self_test:local.self_test();malformed(data,points,normals,nonpaired,beta)
    return {'agent':'six-rupert-2','role':'researcher',
            'claim_status':'J77_five_explicit_all_source_receiver_caps',
            'receiver_cap_unit_chord':str(d.a),'all_source_orientations_and_rolls_covered':True,
            'arbitrary_translations':True,'scales_covered':'lambda >= 1','strict_containment_excluded':True,
            'global_Rupert_resolved':False,'full_body_diameter_minimizer_axes':5,
            'candidate_count':count,'candidate_axial_comparisons':comparisons,
            'maximizing_candidate_occurrences':occurrences,'candidate_blocker_sha256':digest,
            'region_gap_beta':encode((beta,))[0],'core_pair_count':25,'reduction_branch_controls':reduction_controls(),
            'full_body_diameter_pair_checks':diameter_checks,'full_body_diameter_equality_pairs':diameter_active,
            'nonantipodal_diameter_gap':encode((nonpaired,))[0],'nonantipodal_gap_comparisons':1460,
            'active_axial_vertices':active,'tangent_inradius_squared':encode((rho2,))[0],
            'reference_shadow_vertices':17,'proper_planar_rotation_group_order':1,'full_planar_isometry_group_order':len(isometries),
            'shadow_vertex_centroid':encode(centroid),'half_turn_balanced_probe_count':3,
            'half_turn_weighted_gap':encode((pi_gap,))[0],'probe_norm_bound':'51/100',
            'roll_tangent_threshold':str(a.a),'roll_angle_bound_radians':str(2*a.a),
            'difference_roll_gap_numerator':str(gamma.a),'closed_roll_cover_pieces':len(minima),
            'quadratic_Bernstein_coefficients':3*len(minima),'minimum_Bernstein_coefficient':encode((min(minima),))[0],
            'source_chord_bound_factor':5,'reference_shadow_error_bound_factor':14,
            'full_relative_angle_bound_radians':str(2*a.a+F(101,100)*6*d.a),
            'cap_transfer_positive_margins':[encode((x,))[0] for x in margins],
            'new_sign_inequality_records':len(audit),'independent_rational_sign_audits':len(signs)+9,
            'inherited_positive_combination_sha256':inherited['exact_positive_combination_sha256'],
            'malformed_controls_with_self_test':12,
            'canonical_certificate_sha256':hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()}
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--self-test',action='store_true');args=parser.parse_args()
    print(json.dumps(check(json.loads((ROOT/'certificates.json').read_text()),args.self_test),indent=2,sort_keys=True))
