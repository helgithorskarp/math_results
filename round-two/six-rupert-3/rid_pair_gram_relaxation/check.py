#!/usr/bin/env python3
"""Exact two-pair proper-roll criterion and an RID relaxation gap.

PROOF.md supplies the continuum arguments. Ordered Q(phi), rational
positive-root brackets, and Python standard library only. No float,
solver, sampled-angle exclusion, or inferred nonexistence is used.
"""
from pathlib import Path
from fractions import Fraction as Q
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import argparse, hashlib, json, sys

HERE=Path(__file__).resolve().parent


def require(condition,message):
    if not condition:raise ValueError(message)


def replay():
    # Credit: the complete published width-filter replay in the W checker.
    pin=json.loads((HERE/'DEPENDENCIES.json').read_text())
    directory=(HERE/pin['directory']).resolve()
    require(set(pin['sha256'])=={'check.py','PROOF.md','DEPENDENCIES.json','expected.json'},'filter inventory differs')
    for name,digest in pin['sha256'].items():
        require(hashlib.sha256((directory/name).read_bytes()).hexdigest()==digest,'published filter changed:'+name)
    require('field' not in sys.modules,'arithmetic loaded before verification')
    spec=spec_from_file_location('gram_filter_dependency',directory/'check.py')
    f=module_from_spec(spec);spec.loader.exec_module(f)
    result=f.verify();output=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    require(output==(directory/'expected.json').read_bytes(),'whole filter expected record differs')
    five=json.loads((directory/'DEPENDENCIES.json').read_text())
    fold=(directory/five['directory']).resolve()
    original=json.loads((fold/'DEPENDENCIES.json').read_text())
    base=(fold/original['directory']).resolve()
    require(Path(sys.modules['field'].__file__).resolve()==base/'field.py','verified arithmetic location differs')
    for name,digest in original['sha256'].items():
        require(hashlib.sha256((base/name).read_bytes()).hexdigest()==digest,'original source changed after replay:'+name)
    spec=spec_from_file_location('gram_original_geometry',base/'verify.py')
    b=module_from_spec(spec);spec.loader.exec_module(b)
    return b,{'filter_whole_expected_bytes':len(output),'filter_whole_expected_sha256':hashlib.sha256(output).hexdigest(),
              'source_commit':pin['source_commit'],'graph':pin['graph_ref'],
              'transitive_replay':'complete filter, fivefold and original brightness records'}


def gram_decision(s,t,G):
    require(len(s)==len(t)==2 and all(x>0 for x in s+t),'nonzero pairs required')
    require(G*G<=s[0]*s[1]*t[0]*t[1],'invalid Gram data')
    losses=[t[i]-s[i] for i in [0,1]]
    if min(losses)<0:return False
    S=s[0]*s[1];L=S-G
    return L<=0 or L*L<=S*losses[0]*losses[1]


def boundary_decision(p,q):
    # Independent unit-circle endpoint test, not the Gram inequality.
    dot=lambda x,y:sum(a*b for a,b in zip(x,y))
    det=lambda x,y:x[0]*y[1]-x[1]*y[0]
    s=[dot(x,x) for x in p];t=[dot(x,x) for x in q]
    require(min(s+t)>0,'nonzero pairs required')
    if any(s[i]>t[i] for i in [0,1]):return False
    c=[(dot(p[i],q[i]),det(p[i],q[i])) for i in [0,1]]
    for i in [0,1]:
        j=1-i;A=dot(c[i],c[i]);rad=A-s[i]*s[i]
        base=s[i]*dot(c[i],c[j])-s[j]*A
        if base>=0 or base*base<=det(c[i],c[j])**2*rad:return True
    return False


def pair_data(p,q):
    dot=lambda x,y:sum(a*b for a,b in zip(x,y))
    det=lambda x,y:x[0]*y[1]-x[1]*y[0]
    s=[dot(x,x) for x in p];t=[dot(x,x) for x in q]
    G=dot(p[0],p[1])*dot(q[0],q[1])+det(p[0],p[1])*det(q[0],q[1])
    return s,t,G


def circle_controls():
    dirs=[(1,0),(Q(3,5),Q(4,5)),(0,1),(-Q(3,5),Q(4,5)),
          (-1,0),(-Q(3,5),-Q(4,5)),(0,-1),(Q(3,5),-Q(4,5))]
    targets=[tuple(Q(scale)*x for x in d) for scale in [Q(1,2),1,2] for d in dirs]
    sources=[((Q(1),Q(0)),tuple(Q(x) for x in d)) for d in [(0,1),(Q(3,5),Q(4,5)),(1,0),(-1,0)]]
    decisions=[]
    for p in sources:
        for q in product(targets,repeat=2):
            s,t,G=pair_data(p,q);v=gram_decision(s,t,G)
            require(v==boundary_decision(p,q),'Gram and arc endpoints disagree')
            decisions.append(v)
    require(len(decisions)==2304,'complete rational control inventory differs')
    p=sources[0]
    named=[('congruent',((1,0),(0,1)),True),
           ('proper_orientation_rejects_reflection',((1,0),(0,-1)),False),
           ('negative_unsquared_branch',((2,0),(0,3)),True),
           ('touching_arcs',((1,1),(1,1)),True),
           ('separated_arcs',((1,1),(1,Q(99,100))),False)]
    for name,q,expected in named:
        s,t,G=pair_data(p,q)
        require(gram_decision(s,t,G)==boundary_decision(p,q)==expected,'named circle control failed:'+name)
    s,t,G=pair_data(p,((2,0),(0,3)))
    require((s[0]*s[1]-G)**2>s[0]*s[1]*(t[0]-s[0])*(t[1]-s[1]),'unsafe squaring control ineffective')
    return {'complete_rational_controls':len(decisions),'passing_controls':sum(decisions),
            'classification_sha256':hashlib.sha256(bytes(decisions)).hexdigest(),
            'independent_algorithm':'all boundaries of both exact proper-roll arcs',
            'named_controls':{name:expected for name,_,expected in named}}


def root_bracket(b,N):
    scale=10**12;low=scale;high=2*scale
    require(b.F(1)<N<b.F(4),'normalization root coarse domain fails')
    while high-low>1:
        mid=(low+high)//2
        if b.F(Q(mid*mid,scale*scale))<=N:low=mid
        else:high=mid
    lo=Q(low,scale);hi=Q(low+1,scale)
    validate_bracket(b,N,lo,hi)
    return lo,hi


def validate_bracket(b,N,lo,hi):
    require(0<lo<hi and b.F(lo*lo)<N<b.F(hi*hi),'positive normalization bracket does not enclose root')


def proper_rotation(b,q):
    O,Z=b.ONE,b.ZERO
    def rotate(v):
        cr=b.cross(q,v);sq=b.cross(q,cr);f=b.F(2)/(O+b.dot(q,q))
        return tuple(v[i]+f*(cr[i]+sq[i]) for i in range(3))
    R=tuple(zip(*(rotate(e) for e in [(O,Z,Z),(Z,O,Z),(Z,Z,O)])))
    validate_rotation(b,R)
    return R


def validate_rotation(b,R):
    O,Z=b.ONE,b.ZERO;I=((O,Z,Z),(Z,O,Z),(Z,Z,O))
    require(tuple(tuple(b.dot(row,col) for col in R) for row in R)==I and
            b.dot(R[0],b.cross(R[1],R[2]))==O,'source rotation not proper orthogonal')


def hull_edges(b,originals,r,u,v):
    Z=b.ZERO;points={}
    for i,pt in enumerate(originals):points.setdefault((b.dot(u,pt),b.dot(v,pt)),[]).append(i)
    keys=sorted(points)
    def turn(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def half(seq):
        h=[]
        for pt in seq:
            while len(h)>=2 and turn(h[-2],h[-1],pt)<=Z:h.pop()
            h.append(pt)
        return h
    hull=half(keys)[:-1]+half(reversed(keys))[:-1]
    cycle=[points[pt][0] for pt in hull]
    edges=[]
    for i,j in zip(cycle,cycle[1:]+cycle[:1]):
        normal=b.cross(b.sub(originals[j],originals[i]),r);height=b.dot(normal,originals[i])
        if height<Z:normal=b.neg(normal);height=-height
        require(height>Z and all(b.dot(normal,x)<=height for x in originals),'full actual shadow edge invalid')
        edges.append((i,j,normal,height))
    require(len(cycle)>=3,'degenerate physical shadow')
    return cycle,edges


def edge_cover(b,cycle,edges):
    require([(i,j) for i,j,_,_ in edges]==list(zip(cycle,cycle[1:]+cycle[:1])),'receiving edge inventory incomplete')


def verify():
    b,dependency=replay();F,Z,O,p=b.F,b.ZERO,b.ONE,b.PHI
    controls=circle_controls()
    V=b.vertices();require(len(V)==60 and set(V)=={b.neg(v) for v in V},'actual original inventory differs')
    facets,fc=b.complete_facets(V);C,_,cc=b.area_generators(V,facets);Gbody=b.proper_group(V)
    require(len(facets)==62 and len(C)==31 and len(Gbody)==60,'physical hull or group inventory differs')
    r=(F(Q(1,25)),(2+p)/125,O);N=b.dot(r,r);a=p**2;c=2+p;R2=7+8*p
    require(N==(3131+p)/3125 and a*r[0]==c*r[1],'exact weighted diagonal receiver differs')
    require(all(b.dot(v,v)==R2 for v in V),'common original radius differs')
    E=sorted({(sx*a,sy*c,Z) for sx,sy in product((-1,1),repeat=2)},key=b.key)
    require(E==[v for v in V if v[2]==Z],'four actual equatorial originals differ')
    require(all(abs(v[2])>=O for v in V if v not in E),'nonequatorial heights differ')
    area=b.brightness_raw(C,r);direct,target_corners=b.direct_shadow_raw(V,r)
    require(area==direct,'independent physical receiving areas disagree')
    memberships=[]
    for g in Gbody:
        raw=b.act(tuple(zip(*g)),r)
        if raw[2]<=Z:continue
        for j in [0,1]:
            k=1-j
            if Z<=raw[j]<=raw[2]/12 and 20*abs(raw[k])<=raw[j]:memberships.append(('W',j))
            if Z<=raw[j]<=raw[2]/20 and 2*abs(raw[k])<=raw[j]:memberships.append(('P',j))
    require(not memberships,'receiver lies in previously certified W union P')
    require(area*area/N<F(Q(1171,20)**2) and 940+1520*p>F(Q(583,10)**2),'area gate of all-source filter fails')
    m=p*r[0]-r[1];d=(p,-O,-m);support=3*p**2+p*m
    require(Z<=m<=p/12 and b.dot(d,r)==Z,'actual width direction invalid')
    require(max(b.dot(d,v) for v in V)==support,'width support not verified on all originals')
    width2=4*support*support/b.dot(d,d);limit=(20+32*p)*(1-Q(10,11664))
    require(width2<limit,'width gate of all-source filter fails')
    # The original W matching proof only needs these receiver quantities,
    # not the W coordinate ratio. They are verified afresh at this point.
    eps=Q(11,20);sing=Q(24,25)
    require(F(Q(99,100)**2)*N<O and N-O<F(Q(1,11)**2),'receiver z/chord bounds fail')
    require(min(b.dot(r,v)**2/N for v in V if v not in E)>F(Q(9,25)),'actual target height separation fails')
    require(R2<F(20) and R2>F(Q(22,5)**2) and R2<F(Q(9,2)**2),'radius brackets fail')
    require(Q(36,125)<eps**2 and 1-Q(3,25)**2>sing**2,'source matching constants fail')
    require(2*a*sing>F(2*eps) and 2*c*sing-2*a>F(2*eps),'rectangle side gates fail')
    require(F(4*eps)*(a+c)+F(4*eps*eps)<4*a*c*sing,'proper matching determinant gate fails')
    q=tuple(F(Q(x,200000)) for x in [12,14,11]);R=proper_rotation(b,q)
    RV=[b.act(R,v) for v in V];n=b.act(tuple(zip(*R)),r)
    require(b.dot(n,n)==N,'source raw normal norm differs')
    source=b.brightness_raw(C,n);source_direct,source_corners=b.direct_shadow_raw(RV,r)
    require(source==source_direct and source<area,'independent physical source area or strict gap fails')
    def project(v):return tuple(v[i]-r[i]*b.dot(r,v)/N for i in range(3))
    margins=[b.dot(project(b.act(R,v)),project(v))-b.dot(project(b.act(R,v)),project(b.act(R,v))) for v in E]
    require(min(margins)>Z,'actual equatorial support inequality fails')
    lo,hi=root_bracket(b,N);rows=[]
    for k in [0,1]:
        face=[Z,Z,Z];face[k]=p**3;face[1-k]=-O;face[2]=-O;face=tuple(face)
        require(face in V,'actual shortest-row support original absent')
        tm=[];sm=[]
        for chi in [F(lo),F(hi)]:
            row=[-r[0]*r[1],-r[0]*r[1],-r[k]*(chi+O)];row[k]=N+chi-r[k]*r[k];row=tuple(row)
            h=b.dot(row,face)
            tm.extend(h-b.dot(row,v) for v in V)
            sm.extend(h-b.dot(row,v) for v in RV)
        require(min(tm)>=Z and min(sm)>Z,'actual transported-row support fails')
        rows.append({'axis':k,'target_original':b.encode(face),'target_endpoint_comparisons':120,
                     'source_endpoint_comparisons':120,'minimum_target_margin':min(tm).encode(),
                     'minimum_source_margin':min(sm).encode()})
    u=(-r[1],r[0],Z);v=b.cross(r,u)
    cycle,edges=hull_edges(b,V,r,u,v);source_cycle,source_edges=hull_edges(b,RV,r,u,v)
    edge_cover(b,cycle,edges);edge_cover(b,source_cycle,source_edges)
    require(len(cycle)==target_corners==16 and len(source_cycle)==source_corners==16,'complete shadow corner counts differ')
    target_min=min(4*h*h/b.dot(normal,normal) for _,_,normal,h in edges)
    source_min=min(4*h*h/b.dot(normal,normal) for _,_,normal,h in source_edges)
    require(source_min<target_min,'exact minimum-width inequality fails')
    violations=[]
    for i,j,normal,h in edges:
        excess,k=max((b.dot(normal,x)-h,k) for k,x in enumerate(RV))
        violations.append({'receiving_edge':[i,j],'source_maximizer':k,'excess':excess.encode(),'violates':excess>Z})
    require(sum(x['violates'] for x in violations)==10,'full noncontainment witness count differs')
    witness=next((i,j,normal,h) for i,j,normal,h in edges if max(b.dot(normal,x) for x in RV)>h)
    i,j,normal,h=witness;k=max(range(len(RV)),key=lambda k:b.dot(normal,RV[k]))
    s=[R2-(a*n[0]+sign*c*n[1])**2/N for sign in [1,-1]]
    t=[R2-(a*r[0]+sign*c*r[1])**2/N for sign in [1,-1]]
    D=a*a-c*c
    Gram=(D-a*a*n[0]**2/N+c*c*n[1]**2/N)*(D-a*a*r[0]**2/N+c*c*r[1]**2/N)+4*a*a*c*c*n[2]/N
    pp=[project(b.act(R,(a,F(sign)*c,Z))) for sign in [1,-1]]
    qq=[project((a,F(sign)*c,Z)) for sign in [1,-1]]
    direct_Gram=b.dot(pp[0],pp[1])*b.dot(qq[0],qq[1])+b.dot(b.cross(pp[0],pp[1]),b.cross(qq[0],qq[1]))
    require(Gram==direct_Gram and all(b.dot(pp[i],pp[i])==s[i] and b.dot(qq[i],qq[i])==t[i] for i in [0,1]),'normal-only Gram identities differ')
    require(gram_decision(s,t,Gram),'two-pair proper-roll criterion fails at explicit witness')
    rejected=[]
    def reject(name,f):
        try:f()
        except ValueError:rejected.append(name);return
        raise ValueError('damaged control accepted:'+name)
    reject('omitted_receiving_edge',lambda:edge_cover(b,cycle,edges[:-1]))
    reject('root_interval_below_true_normalization',lambda:validate_bracket(b,N,lo-Q(1,10**12),lo))
    reject('root_interval_above_true_normalization',lambda:validate_bracket(b,N,hi,hi+Q(1,10**12)))
    reject('improper_reflected_source_rotation',lambda:validate_rotation(b,(b.neg(R[0]),R[1],R[2])))
    reject('zero_pair',lambda:gram_decision([Q(0),Q(1)],[Q(1),Q(1)],Q(0)))
    reject('invalid_Gram_data',lambda:gram_decision([Q(1),Q(1)],[Q(1),Q(1)],Q(2)))
    return {'agent':'six-rupert-3','role':'researcher','claim':'two-pair proper-roll reduction and exact RID relaxation gap; no passage or receiver exclusion',
            'dependency_replay':dependency,'circle_controls':controls,'damaged_controls_rejected':rejected,
            'originals':len(V),'facets':len(facets),'physical_Cauchy_generators':len(C),'proper_group':len(Gbody),
            'raw_receiver':b.encode(r),'receiver_norm_squared':N.encode(),'exact_weighted_diagonal':True,
            'all_proper_W_union_P_memberships':len(memberships),'physical_receiving_area_squared':(area*area/N).encode(),
            'actual_filter_squared_directional_width':width2.encode(),'all_source_filter_and_matching_gates_pass':True,
            'Cayley_vector':b.encode(q),'proper_rotation':[[x.encode() for x in row] for row in R],
            'raw_source_normal':b.encode(n),'physical_area_raw_gap':(area-source).encode(),
            'same_original_E_support_margins':[x.encode() for x in margins],
            'positive_normalization_root_bracket':[str(lo),str(hi)],'actual_shortest_transport_rows':rows,
            'receiving_hull_cycle':cycle,'source_hull_cycle':source_cycle,
            'physical_minimum_receiving_width_squared':target_min.encode(),'physical_minimum_source_width_squared':source_min.encode(),
            'full_receiving_original_edge_comparisons':len(edges)*len(V),'violating_receiving_edges':10,'full_edge_records':violations,
            'explicit_failed_edge':{'receiving_original_indices':[i,j],'outward_normal':b.encode(normal),'target_height':h.encode(),
                                    'source_original_index':k,'source_original':b.encode(V[k]),'strict_excess':(b.dot(normal,RV[k])-h).encode()},
            'pair_source_squared_norms':[x.encode() for x in s],'pair_target_squared_norms':[x.encode() for x in t],
            'pair_squared_radius_losses':[(t[i]-s[i]).encode() for i in [0,1]],
            'oriented_Gram':Gram.encode(),'Gram_unsquared_L0':(s[0]*s[1]-Gram).encode(),
            'Gram_condition_pass':True,'independent_physical_source_and_target_areas_pass':True}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit',action='store_true',help='emit newly derived record without comparing expected.json')
    args=parser.parse_args();data=(json.dumps(verify(),indent=2,sort_keys=True)+'\n').encode()
    if not args.emit:require(data==(HERE/'expected.json').read_bytes(),'whole expected record differs')
    sys.stdout.buffer.write(data)
