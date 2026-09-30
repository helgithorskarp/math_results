#!/usr/bin/env python3
"""Exact adaptive-roll J77 criterion and a complete closed receiver cover."""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,importlib.util,itertools,json

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent.parent
def require(condition,message):
    if not condition:raise ValueError(message)
manifest=json.loads((ROOT/'dependencies.json').read_text())
require(len(manifest['sources'])==2,'Incomplete direct dependency set')
parent,composition=manifest['sources']
require(parent['source_directory']=='convex_geometry/rupert_j77_sharp_region_gap'
        and parent['source_commit']=='2def43a003a2a692571ae654c543517b1cb20e6b','Wrong J77 parent')
require(set(parent['sha256'])=={'.gitignore','README.md','PROOF.md','verify.py','certificates.json','dependencies.json','expected.json'},
        'Incomplete J77 parent pins')
require(composition['source_directory']=='rhombicosidodecahedron_mirror_cluster_obstruction'
        and composition['source_commit']=='4ccd4e7803077dacfcd993e01caeaaf001dc18d5'
        and set(composition['sha256'])=={'ORTHOGONAL_COMPOSITION_PROOF.md'},'Wrong composition dependency')
for source in manifest['sources']:
    for name,digest in source['sha256'].items():
        require(hashlib.sha256((REPO/source['source_directory']/name).read_bytes()).hexdigest()==digest,
                'Changed direct dependency: '+name)
PRIOR=REPO/parent['source_directory']
spec=importlib.util.spec_from_file_location('j77_adaptive_sharp_dependency',PRIOR/'verify.py')
sharp=importlib.util.module_from_spec(spec);spec.loader.exec_module(sharp)
old,caps,local=sharp.old,sharp.caps,sharp.local
Q,V,D,N=sharp.Q,sharp.V,sharp.D,sharp.N
dot,sub,scale,cross,add=sharp.dot,sharp.sub,sharp.scale,sharp.cross,sharp.add
encode,decode,absq,root=sharp.encode,sharp.decode,sharp.absq,sharp.root
ROLL=sharp.ROLL
G=Q(90,74)/241
B=F(57,400)

def all_dependency_pins():
    sources=[parent,composition,sharp.manifest,old.manifest,*caps.manifest['sources']]
    pins={}
    for source in sources:
        for name,digest in source['sha256'].items():
            path=source['source_directory']+'/'+name
            require(path not in pins or pins[path]==digest,'Conflicting dependency pins')
            pins[path]=digest
            require(hashlib.sha256((REPO/path).read_bytes()).hexdigest()==digest,'Changed transitive dependency: '+path)
    require(len(pins)==36,'Incomplete direct/transitive dependency boundary')
    return pins

def even_stress(normals,pi_data,claimed_G,audit):
    require([p['probe'] for p in pi_data]==[2,5,12],'Wrong even-stress probes')
    require([p['source_vertex'] for p in pi_data]==[29,31,24],'Wrong even-stress source vertices')
    weights=[p['weight'] for p in pi_data]
    require(sum(weights,Q())==1 and all(w>0 for w in weights),'Invalid even-stress weights')
    require(all(sum((p['weight']*normals[p['probe']][k] for p in pi_data),Q())==0 for k in range(3)),
            'Even-stress normals do not balance')
    cosine=sine=Q();comparisons=0
    for p in pi_data:
        m=normals[p['probe']];values=[dot(m,v) for v in V]
        i=p['source_vertex'];minimum=min(values)
        require([j for j,v in enumerate(values) if v==minimum]==[i],'Even-stress minimum is not the stated unique preimage')
        gaps=[value-minimum for value in values]
        require(all(x>=0 for x in gaps),'Even-stress source is not a minimum')
        require(dot(m,D)==0 and max(values)==1,'Incorrect even-stress reference offset')
        cosine-=p['weight']*values[i]
        sine+=p['weight']*dot(m,cross(D,V[i]))
        audit.extend(gaps+[p['weight']]);comparisons+=len(values)
        require(dot(m,m)>Q(F(1,16)),'Norm gate for entire-parent inclusion fails')
        audit.append(dot(m,m)-Q(F(1,16)))
    require(cosine==claimed_G==G and sine==0,'Even half-turn cosine/sine identity fails')
    require(Q(2)*Q(2)<caps.R2 and G<Q(F(11,10)),'Entire-parent stress comparison gates fail')
    audit.extend([caps.R2-4,Q(F(11,10))-G])
    return comparisons

def polynomial(sign,piece,normals):
    m=scale(piece['orientation'],normals[piece['probe']]);i,j=piece['source_pair']
    w=sub(V[i],V[j]);values=[dot(m,v) for v in V]
    H=max(values)-min(values);d=dot(m,w);S=sign*dot(m,cross(D,w))
    nbound=Q(F(ROLL['root_N_enclosure'][1 if S>=0 else 0]))
    require(H>=absq(d) and nbound>0,'Invalid supporting-difference polynomial')
    return d-H,2*S/nbound,-d-H

def roll_structure(data,normals,audit):
    caps.cover_shape(data)
    require(F(data['roll_tangent_threshold'])==F(1,50),'Wrong inherited roll threshold')
    require(Q(F(data['root_N_enclosure'][0]))<=Q(F(data['root_N_enclosure'][1])),'Reversed normal root interval')
    old.root_check(N,F(data['root_N_enclosure'][0]),F(data['root_N_enclosure'][1]),audit)
    first=[];remote=[]
    for cover in data['covers']:
        sign=cover['sign'];p=cover['pieces'][0]
        require(p['interval']==['1/50','57/400'] and p['orientation']==1,'Wrong first residual interval')
        require((sign,p['probe'],p['source_pair']) in [(1,11,[29,54]),(-1,13,[31,51])],
                'Wrong first signed source support')
        coeff=polynomial(sign,p,normals)
        require(coeff[0]==0 and coeff[1]>0 and coeff[2]<0,'First residual polynomial has wrong branch')
        audit.extend(coeff);first.append((sign,p,coeff[1],-coeff[2]))
        for piece in cover['pieces'][1:]:
            coeff=polynomial(sign,piece,normals)
            require(coeff[2]<=0,'Reference support polynomial is not concave')
            audit.extend(coeff);remote.append((sign,piece,coeff))
    require(len(first)==2 and len(remote)==10 and {r[0] for r in first}=={-1,1},'Incomplete reduced roll cover')
    require(first[0][2:]==first[1][2:],'Reflected residual polynomials differ')
    return first,remote

def selected_error(piece,a,delta,heights,width,nlo,rhi):
    p=width[piece['probe']];i,j=piece['source_pair']
    h=absq(heights[i]-heights[j])/nlo
    return p['norm_upper']*(h*a+p['kappa_upper']*delta+Q(rhi)*(a*a+delta*delta))

def residual_inverse(K,T,error,audit):
    require(K>0 and T>0 and error>=0,'Invalid residual inverse data')
    b=Q(B);bracket=K*b-(T+error)*b*b-error
    disc=K*K-4*(T+error)*error
    require(bracket>0 and disc>0,'First residual inverse has no certified small branch')
    dlo,dhi=root(disc,audit)
    require(K+Q(dlo)>0,'Nonpositive stable root denominator')
    lower=2*error/(K+Q(dhi));upper=2*error/(K+Q(dlo))
    require(0<=lower<=upper<b,'Invalid outward small-root enclosure')
    value=lambda x:(T+error)*x*x-K*x+error
    require(value(lower)>=0 and value(upper)<=0,'Small-root sign brackets fail')
    audit.extend([bracket,disc,upper-lower,b-upper,value(lower),-value(upper)])
    return 2*upper,bracket

def phase(flower,delta,constants,structure,audit):
    heights,width,pi,gap,rhi,c0hi,rholo,nlo=constants
    first,remote=structure
    require(flower>0 and delta>=0,'Invalid receiver parameters')
    a=Q(F(101,100))*(Q(c0hi)-flower)/rholo
    require(a>=0,'Negative source chord bound')
    margins={'sharp_regional_gap':flower*flower-Q(F(1,12)),
             'receiver_height_gap_domain':Q(F(1,20))-delta,
             'source_chord_domain':Q(F(1,10))-a,'receiver_chord_domain':Q(F(1,10))-delta}
    epsilons=[];brackets=[]
    for sign,piece,K,T in first:
        error=selected_error(piece,a,delta,heights,width,nlo,rhi)
        epsilon,bracket=residual_inverse(K,T,error,audit)
        epsilons.append(epsilon);brackets.append(bracket)
    epsilon=max(epsilons);remote_margins=[];bernstein=[]
    for sign,piece,coeff in remote:
        error=selected_error(piece,a,delta,heights,width,nlo,rhi)
        p=(coeff[0]-error,coeff[1],coeff[2]-error)
        lo,hi=[Q(F(x)) for x in piece['interval']]
        value=lambda x:p[0]+x*(p[1]+x*p[2])
        beta=(value(lo),value(lo)+(hi-lo)*(p[1]+2*p[2]*lo)/2,value(hi))
        reconstructed=(beta[0],2*(beta[1]-beta[0]),beta[0]-2*beta[1]+beta[2])
        substituted=(value(lo),(hi-lo)*(p[1]+2*p[2]*lo),(hi-lo)*(hi-lo)*p[2])
        require(reconstructed==substituted and p[2]<=0,'Coupled remote polynomial identity fails')
        margin=min(beta[0],beta[2])
        require(beta[1]>=margin and margin>0,'Closed coupled remote-roll interval is not excluded')
        audit.extend(list(beta)+[beta[1]-margin]);remote_margins.append(margin)
        bernstein.extend(beta)
    transport=sum((p['weight']*p['norm_upper']*(p['source_height_upper']*a+p['kappa_upper']*delta
                 +Q(rhi)*(a*a+delta*delta)/2) for p in pi),Q())
    margins['even_half_turn']=gap-transport-G*epsilon*epsilon/2
    _,composition_upper=root((a+delta)*(a+delta)+epsilon*epsilon,audit)
    linear=epsilon+Q(F(101,100))*(a+delta)
    perpendicular=Q(F(101,100))*composition_upper
    theta=min(linear,perpendicular)
    margins['roll_chord_domain']=Q(F(1,10))-epsilon
    torque=Q(local.C*local.M)*(delta+theta/2)
    margins['translated_torque']=1-3*torque*torque
    require(all(x>0 for x in margins.values()),'Adaptive receiver criterion fails')
    audit.extend(margins.values())
    return {'F_lower':flower,'receiver_chord_upper':delta,'source_chord_upper':a,
            'residual_angle_upper':epsilon,'full_angle_upper':theta,
            'linear_full_angle_upper':linear,'perpendicular_full_angle_upper':perpendicular,
            'minimum_coupled_remote_margin':min(remote_margins),'minimum_residual_bracket_margin':min(brackets),
            'positive_margins':margins,'remote_Bernstein_coefficients':len(bernstein)}

def midpoint_split(triangle):
    a,b,c=triangle
    mid=lambda u,v:tuple((x+y)/2 for x,y in zip(u,v))
    ab,ac,bc=mid(a,b),mid(a,c),mid(b,c)
    return [(a,ab,ac),(ab,b,bc),(ac,bc,c),(ab,bc,ac)]
def chart_area(t):
    a,b,c=t
    return ((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))/2
def closed_partition(corners,depth):
    require(type(depth) is int and 0<=depth<=2,'Unsupported closed subdivision depth')
    triangles=[tuple(corners)];parents=0
    for _ in range(depth):
        children=[]
        for t in triangles:
            parts=midpoint_split(t)
            require(all(chart_area(s)==chart_area(t)/4>0 for s in parts),'Incorrect closed midpoint partition areas')
            children.extend(parts);parents+=1
        triangles=children
    require(len(triangles)==4**depth and sum((chart_area(t) for t in triangles),Q())==chart_area(corners),
            'Closed partition loses chart area')
    return triangles,parents

def actual_torque_balances(probes,audit):
    gradients=[]
    for i,p in probes:
        require(dot(p,D)==0,'Base torque probe leaves the reference plane')
        margin=Q(local.M*local.M)-caps.R2*dot(p,p)
        require(margin>0,'Torque probe norm exceeds its bound');audit.append(margin)
        gradients.append(cross(V[i],p)+p)
    require(len(local.BASES)==6 and {(a,s) for a,s,_ in local.BASES}=={(a,s) for a in range(3) for s in (-1,1)},
            'Missing signed torque target')
    stream=[]
    for axis,sign,ids in local.BASES:
        target=[0]*6;target[axis]=sign
        weights=local.exact_solve([gradients[i] for i in ids],target)
        total=sum(weights,Q())
        require(all(w>0 for w in weights) and total<Q(local.C),'Invalid translated torque balance')
        audit.extend(weights+[Q(local.C)-total])
        stream.append([axis,sign,list(ids),[encode(w) for w in weights]])
    return hashlib.sha256(json.dumps(stream,separators=(',',':')).encode()).hexdigest()

def composition_identity():
    # Four-variable rational polynomial identity, not numerical samples.
    zero=(0,0,0,0)
    def const(c):return {zero:F(c)} if c else {}
    def plus(*polys):
        ans={}
        for p in polys:
            for e,c in p.items():ans[e]=ans.get(e,F())+c
        return {e:c for e,c in ans.items() if c}
    def times(a,b):
        ans={}
        for e,c in a.items():
            for f,d in b.items():
                k=tuple(x+y for x,y in zip(e,f));ans[k]=ans.get(k,F())+c*d
        return {e:c for e,c in ans.items() if c}
    def scalar(c,p):return {e:F(c)*v for e,v in p.items() if c*v}
    def sq(p):return times(p,p)
    a,d,e,p=[{tuple(int(i==j) for i in range(4)):F(1)} for j in range(4)]
    a2,d2,e2=sq(a),sq(d),sq(e);ad=times(a,d)
    W=plus(p,scalar(F(-1,4),ad))
    lhs=plus(sq(plus(a,d)),e2,const(-4),scalar(4,sq(W)))
    rhs=plus(scalar(2,times(ad,plus(const(1),scalar(-1,p)))),
             scalar(F(1,16),times(times(a2,d2),plus(const(8),scalar(-1,e2)))),
             scalar(F(1,4),times(e2,plus(a2,d2))))
    P=times(times(plus(const(1),scalar(F(-1,4),a2)),plus(const(1),scalar(F(-1,4),d2))),
            plus(const(1),scalar(F(-1,4),e2)))
    residual=plus(lhs,scalar(-1,rhs))
    require(residual==scalar(4,plus(sq(p),scalar(-1,P))),'Perpendicular-composition polynomial identity fails')
    require(F(399,400)**3>F(99,100)**2 and F(101,100)**2*F(63,64)>1,
            'Composition positive-lift/angle gates fail')
    return len(residual)

def frame_audits():
    # Generic exact frame/gauge audits; the continuous bridge is in PROOF.md.
    I=tuple(tuple(F(int(i==j)) for j in range(3)) for i in range(3))
    transpose=lambda a:tuple(zip(*a))
    def multiply(a,b):return tuple(tuple(sum((x*y for x,y in zip(row,col)),F()) for col in zip(*b)) for row in a)
    def mv(a,v):return tuple(sum((x*y for x,y in zip(row,v)),F()) for row in a)
    def outer(v):return tuple(tuple(x*y for y in v) for x in v)
    def difference(a,b):return tuple(tuple(x-y for x,y in zip(r,s)) for r,s in zip(a,b))
    def diagonal(a,b,c):return ((F(a),F(),F()),(F(),F(b),F()),(F(),F(),F(c)))
    def det(a):return sum((a[0][i]*(a[1][(i+1)%3]*a[2][(i+2)%3]-a[1][(i+2)%3]*a[2][(i+1)%3]) for i in range(3)),F())
    def rotation(axis,t):
        require(sum((x*x for x in axis),F())==1,'Nonunit audit rotation axis')
        c=(1-t*t)/(1+t*t);s=2*t/(1+t*t);x,y,z=axis
        skew=((F(),-z,y),(z,F(),-x),(-y,x,F()))
        return tuple(tuple(c*I[i][j]+(1-c)*axis[i]*axis[j]+s*skew[i][j] for j in range(3)) for i in range(3))
    n0=(F(),F(),F(1));count=0
    for ta,td,te,sign in itertools.product([F(),F(1,100),F(-1,100)],[F(),F(1,100),F(-1,100)],
                                          [F(),F(1,50),F(-1,50)],[-1,1]):
        source_axis=(F(3,5),F(4,5),F());receiver_axis=(F(1),F(),F())
        require(sum((x*y for x,y in zip(source_axis,n0)),F())==0
                and sum((x*y for x,y in zip(receiver_axis,n0)),F())==0,'Transport axis is not perpendicular')
        A1,A2,C=rotation(source_axis,ta),rotation(receiver_axis,td),rotation(n0,te)
        H=diagonal(1,1,sign);S=diagonal(sign,1,1)
        F2=transpose(A2);F1=multiply(C,transpose(A1))
        original=multiply(multiply(multiply(A2,H),F1),transpose(S))
        gauged=multiply(A2,F1);n=mv(A2,n0)
        nn=outer(n);projection=difference(I,nn)
        reflection=tuple(tuple(I[i][j]-2*nn[i][j] for j in range(3)) for i in range(3))
        qS=multiply(original,S)
        require(det(original)==det(gauged)==1 and multiply(transpose(original),original)==I,
                'Frame audit does not give proper rotations')
        require(gauged==(qS if sign==1 else multiply(reflection,qS)),'Improper-body proper-gauge identity fails')
        require(multiply(projection,gauged)==multiply(projection,qS),'Projection gauge identity fails')
        require(multiply(multiply(F2,original),S)[:2]==F1[:2],'Two-row frame gauge identity fails')
        b1=multiply(F2,original)[:2]
        cr=lambda a,b:(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
        source_normal=cr(*b1)
        transformed=tuple(sign*x for x in mv(transpose(S),source_normal))
        require(transformed==F1[2]==mv(A1,n0),'Determinant-sensitive cross normal identity fails')
        count+=1
    return count

def encoded_phase(result):
    return {k:({label:encode(v) for label,v in value.items()} if isinstance(value,dict)
               else encode(value) if isinstance(value,Q) else value) for k,value in result.items()}

def malformed_controls(data,corners,core,normals,constants,structure,pi):
    def criterion_at(t):
        params=[old.corner_parameters(u,core,[]) for u in t]
        return phase(min(p[0] for p in params),max(p[1] for p in params),constants,structure,[])
    bad_source=[dict(p) for p in pi];bad_source[0]['source_vertex']=0
    bad_weight=[dict(p) for p in pi];bad_weight[0]['weight']=-bad_weight[0]['weight']
    missing_sign=json.loads(json.dumps(ROLL));missing_sign['covers']=missing_sign['covers'][:1]
    missing_interval=json.loads(json.dumps(ROLL));missing_interval['covers'][0]['pieces'].pop()
    false_pair=json.loads(json.dumps(ROLL));false_pair['covers'][0]['pieces'][0]['source_pair']=[0,1]
    bad_chart=json.loads(json.dumps(data));bad_chart['triangle'][1][2]=['4','0']
    large=[D,corners[1],(Q(F(1,12)),corners[2][1],D[2])]
    big_parts,_=closed_partition(large,2)
    bad_probe=local.make_probes();bad_probe[0]=(0,bad_probe[0][1])
    tests=[lambda:even_stress(normals,pi,G+1,[]),lambda:even_stress(normals,bad_source,G,[]),
           lambda:even_stress(normals,bad_weight,G,[]),lambda:roll_structure(missing_sign,normals,[]),
           lambda:roll_structure(missing_interval,normals,[]),lambda:roll_structure(false_pair,normals,[]),
           lambda:old.root_check(Q(F(1,2)),F(1),F(1),[]),
           lambda:residual_inverse(Q(1),Q(1),Q(1),[]),lambda:closed_partition(corners,3),
           lambda:criterion_at(corners),lambda:criterion_at(big_parts[5]),
           lambda:old.whole_triangle(corners,11,bad_probe,[]),lambda:old.geometry_fixture(bad_chart)]
    for test in tests:
        try:test()
        except ValueError:pass
        else:raise ValueError('Malformed adaptive-roll evidence accepted')
    return len(tests)

def check(data,self_test=False):
    pins=all_dependency_pins();audit=[]
    require(data['height_gap_unit_chord_range']=='1/20' and data['subdivision_depth']==2,'Wrong complete-cover range/depth')
    require(decode(data['half_turn_cosine_coefficient'])==G,'Wrong fixture cosine coefficient')
    corners,critical,area=old.geometry_fixture(data)
    require(critical==11 and corners==[D,(Q(),Q(F(-13,11)),D[2]),(Q(F(1,18)),Q(F(-25,24)),D[2])],
            'Incorrect claimed macro triangle')
    require(len(V)==55 and all(dot(v,v)==caps.R2 for v in V),'Incorrect body sphere')
    require({(-v[0],v[1],v[2]) for v in V}==set(V) and {sharp.rotate(v) for v in V}==set(V),
            'Required actual body symmetries fail')
    normals=caps.reference_geometry(audit)[0]
    _,rhi=root(caps.R2,audit);_,c0hi=root(caps.B,audit)
    rholo,_=root(Q(233,-10)/596,audit);nlo,_=root(N,audit)
    heights,width,pi,gap,pair_checks,excess,single_checks,single_excess=old.transport_data(normals,Q(F(1,20)),nlo,audit)
    even_comparisons=even_stress(normals,pi,decode(data['half_turn_cosine_coefficient']),audit)
    require(gap==G-1,'Inconsistent half-turn transport gap')
    structure=roll_structure(ROLL,normals,audit)
    constants=(heights,width,pi,gap,rhi,c0hi,rholo,nlo)
    core=[v for v in V if scale(-1,v) in V];require(len(core)==50,'Wrong antipodal core')
    for v in core:
        axial=[dot(v,u) for u in corners]
        require(all(x>0 for x in axial) or all(x<0 for x in axial),'Whole macro triangle crosses an axial wall')
        audit.extend(axial)
    probes=local.make_probes();torque_digest=actual_torque_balances(probes,audit)
    triangles,parents=closed_partition(corners,data['subdivision_depth'])
    vertices=sorted({u for t in triangles for u in t},key=lambda u:tuple((x.a,x.b) for x in u))
    parameters={u:old.corner_parameters(u,core,audit) for u in vertices}
    phases=[]
    for t in triangles:
        params=[parameters[u] for u in t]
        phases.append(phase(min(p[0] for p in params),max(p[1] for p in params),constants,structure,audit))
    stream=[[[[encode(x) for x in u] for u in t],encoded_phase(result)] for t,result in zip(triangles,phases)]
    digest=hashlib.sha256(json.dumps(stream,separators=(',',':')).encode()).hexdigest()
    sc,dc,replays,smin,dmin=old.whole_triangle(corners,critical,probes,audit)
    prior_corners,_,prior_area=old.geometry_fixture(json.loads((PRIOR/'certificates.json').read_text()))
    weights=[(Q(1),Q(),Q()),(Q(F(3,14)),Q(F(11,14)),Q()),
             (Q(F(407,960)),Q(F(121,960)),Q(F(9,20)))]
    for target,ws in zip(prior_corners,weights):
        require(sum(ws,Q())==1 and all(w>=0 for w in ws),'Invalid old-triangle convex weights')
        require(tuple(sum((w*u[k] for w,u in zip(ws,corners)),Q()) for k in range(3))==target,
                'Old whole receiver triangle is not contained')
    require(area==Q(F(1,198)) and area/prior_area==Q(F(280,99)),'Incorrect closed chart-area extension')
    denlo,_=root(dot(corners[1],corners[1])*N,audit)
    beyond=2-2*dot(D,corners[1])/denlo-Q(F(1,27))*Q(F(1,27))
    require(beyond>0,'Far receiver corner does not exceed chord1/27');audit.append(beyond)
    old_threshold=Q(F(1,25));old_roll=Q(2)*old_threshold/4
    new_roll=Q(F(11,10))*old_threshold*old_threshold/2
    require(old_roll>new_roll,'Entire-parent half-turn roll-loss comparison fails')
    identity_terms=composition_identity();frames=frame_audits()
    descriptive_bounds=[min(p['F_lower'] for p in phases)-Q(F(35284,100000)),
                        Q(F(5099,100000))-max(p['source_chord_upper'] for p in phases),
                        Q(F(3729,100000))-max(p['receiver_chord_upper'] for p in phases),
                        Q(F(1136,25000))-max(p['residual_angle_upper'] for p in phases),
                        Q(F(2291,25000))-max(p['full_angle_upper'] for p in phases),
                        min(p['minimum_coupled_remote_margin'] for p in phases)-Q(F(9,50000)),
                        min(p['positive_margins']['even_half_turn'] for p in phases)-Q(F(4009,100000)),
                        min(p['positive_margins']['translated_torque'] for p in phases)-Q(F(607,25000))]
    require(all(x>0 for x in descriptive_bounds),'Advertised rational cover bounds fail')
    audit.extend(descriptive_bounds)
    rejected=malformed_controls(data,corners,core,normals,constants,structure,pi) if self_test else 13
    unique=sorted(set(audit),key=lambda x:(x.a,x.b));local.independent_sign_audit(unique)
    extrema={k:{'minimum':encode(min(p[k] for p in phases)),'maximum':encode(max(p[k] for p in phases))}
             for k in ['F_lower','receiver_chord_upper','source_chord_upper','residual_angle_upper','full_angle_upper']}
    margin_names=phases[0]['positive_margins']
    min_margins={k:encode(min(p['positive_margins'][k] for p in phases)) for k in margin_names}
    return {'agent':'six-rupert-2','role':'researcher','claim_status':'adaptive_roll_criterion_and_entire_closed_J77_receiver_triangle',
            'global_Rupert_resolved':False,'all_source_orientations_rolls_translations':True,'scales_covered':'lambda >= 1',
            'closed_equality_forms':['Q=R^k','Q=M_n X R^k'],'closed_scale':1,'closed_translation':0,
            'entire_previous_receiver_criterion_included':True,'previous_whole_triangle_contained':True,
            'whole_triangle_fixed_z_chart_area':encode(area),'previous_triangle_area_ratio':encode(area/prior_area),
            'far_corner_unit_chord_strict_lower_bound':'1/27','far_corner_squared_chord_extension_margin':encode(beyond),
            'closed_midpoint_subdivision_depth':2,'complete_closed_pieces':len(triangles),'split_parent_triangles':parents,
            'unique_cover_vertex_rays':len(vertices),'whole_triangle_common_core_signs':len(core),
            'piece_parameter_extrema':extrema,'minimum_piece_positive_margins':min_margins,
            'minimum_coupled_remote_margin':encode(min(p['minimum_coupled_remote_margin'] for p in phases)),
            'minimum_residual_bracket_margin':encode(min(p['minimum_residual_bracket_margin'] for p in phases)),
            'coupled_remote_interval_checks':len(phases)*10,'coupled_remote_Bernstein_coefficients':sum(p['remote_Bernstein_coefficients'] for p in phases),
            'residual_inverse_branch_checks':len(phases)*2,'even_half_turn_cosine_coefficient':encode(G),
            'even_half_turn_sine_coefficient':encode(Q()),'even_source_minimum_comparisons':even_comparisons,
            'whole_triangle_support_Bernstein_coefficients':sc,'whole_triangle_diameter_Bernstein_coefficients':dc,
            'whole_triangle_minimum_support_coefficient':encode(smin),'whole_triangle_minimum_diameter_coefficient':encode(dmin),
            'independent_actual_plane_barycenter_replays':replays,'difference_support_pair_checks':pair_checks,
            'difference_excess_height_checks':excess,'half_turn_support_vertex_checks':single_checks,'half_turn_excess_height_checks':single_excess,
            'signed_translated_torque_balances':6,'positive_torque_combination_sha256':torque_digest,
            'perpendicular_composition_polynomial_identity_unreduced_terms':identity_terms,'exact_proper_frame_gauge_audits':frames,
            'new_sign_records':len(audit),'new_independent_rational_sign_audits':len(unique)+9,
            'malformed_controls_with_self_test':rejected,'pinned_dependency_files':len(pins),
            'advertised_rational_cover_bounds':len(descriptive_bounds),
            'full_regional_parent_replayed_in_this_run':False,
            'pinned_regional_parent_expected_sha256':parent['sha256']['expected.json'],
            'complete_cover_bounds_sha256':digest,
            'canonical_certificate_sha256':hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--self-test',action='store_true');args=parser.parse_args()
    print(json.dumps(check(json.loads((ROOT/'certificates.json').read_text()),args.self_test),indent=2,sort_keys=True))
