"""Original-coordinate independent RID Gram/relaxation audit, six-reviewer-4.

Gift wrapping replaces the researcher's monotone hull. Exact full-shadow
common-angle tests retain all contacts and one common roll. Only this
reviewer's previously published original geometry/arithmetic is reused.
"""
import argparse
from fractions import Fraction as F
from importlib.util import module_from_spec,spec_from_file_location
from itertools import combinations,product
import hashlib,json,sys
from pathlib import Path
from circle import feasible,positive_disk_oracle,require
HERE=Path(__file__).resolve().parent

def digest(v):return hashlib.sha256((json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()
def encode(v):return [str(x) for x in v]

def geometry():
    pin=json.loads((HERE/'DEPENDENCIES.json').read_text());directory=(HERE/pin['directory']).resolve()
    require(set(pin['sha256'])=={'check.py','field.py','expected.json','REVIEW.md'},'own dependency inventory')
    for name,sha in pin['sha256'].items():require(hashlib.sha256((directory/name).read_bytes()).hexdigest()==sha,'own dependency altered:'+name)
    require('field' not in sys.modules,'premature field import');sys.path.insert(0,str(directory))
    spec=spec_from_file_location('own_rid_geometry',directory/'check.py');b=module_from_spec(spec);spec.loader.exec_module(b)
    require(Path(sys.modules['field'].__file__).resolve()==directory/'field.py','own arithmetic location')
    return b,pin

def silhouette(b,V,r):
    S,Z=b.S,b.Z;N=b.fdot(r,r)
    u=(S(1),Z,-r[0]/r[2]);v=b.fcross(r,u)
    pts={}
    for i,w in enumerate(V):pts.setdefault((b.fdot(u,w),b.fdot(v,w)),[]).append(i)
    keys=sorted(pts);start=keys[0];hull=[start]
    def turn(p,q,t):return (q[0]-p[0])*(t[1]-p[1])-(q[1]-p[1])*(t[0]-p[0])
    def length(p,q):return (p[0]-q[0])**2+(p[1]-q[1])**2
    while True:
        p=hull[-1];q=next(t for t in keys if t!=p)
        for t in keys:
            d=turn(p,q,t)
            if d<0 or (d==0 and length(p,t)>length(p,q)):q=t
        if q==start:break
        require(q not in hull and len(hull)<len(keys),'gift wrapping cycle');hull.append(q)
    require(len(hull)>=3,'two dimensional shadow')
    for p,q in zip(hull,hull[1:]+hull[:1]):require(all(turn(p,q,t)>=0 for t in keys),'complete hull support')
    ids=[pts[p][0] for p in hull];edges=[]
    for i,j in zip(ids,ids[1:]+ids[:1]):
        n=b.fcross(b.sub(V[j],V[i]),r);h=b.fdot(n,V[i])
        require(h>0 and b.fdot(n,r)==0,'physical outward edge')
        require(all(b.fdot(n,w)<=h for w in V),'all actual edge supports')
        edges.append((i,j,n,h))
    shoelace=sum((p[0]*q[1]-p[1]*q[0] for p,q in zip(hull,hull[1:]+hull[:1])),Z)
    area=shoelace**2/(4*b.fdot(u,u)*b.fdot(v,v))
    widths=[4*h*h/b.fdot(n,n) for i,j,n,h in edges]
    return {'cycle':ids,'edges':edges,'area_squared':area,'minimum_width_squared':min(widths),'all_edge_widths_squared':widths}

def rotation(b,q,improper=False):
    S,Z=b.S,b.Z
    def rot(v):return b.add(v,b.scale(2/(1+b.fdot(q,q)),b.add(b.fcross(q,v),b.fcross(q,b.fcross(q,v)))))
    R=b.transpose([rot(tuple(S(i==j) for i in range(3))) for j in range(3)])
    if improper:R=tuple(tuple(-x for x in row) for row in R)
    require(b.mmul(R,b.transpose(R))==tuple(tuple(S(i==j) for j in range(3)) for i in range(3)) and b.fdot(R[0],b.fcross(R[1],R[2]))==1,'proper source rotation')
    return R

def circle_controls():
    dirs=[(F(1),F(0)),(F(3,5),F(4,5)),(F(0),F(1)),(F(-3,5),F(4,5)),(F(-1),F(0)),(F(-3,5),F(-4,5)),(F(0),F(-1)),(F(3,5),F(-4,5))]
    targets=[tuple(scale*x for x in d) for scale in [F(1,2),F(1),F(2)] for d in dirs]
    sources=[(dirs[0],d) for d in [dirs[2],dirs[1],dirs[0],dirs[4]]]
    dot=lambda u,v:sum(x*y for x,y in zip(u,v));det=lambda u,v:u[0]*v[1]-u[1]*v[0]
    decisions=[]
    for p in sources:
        for q in product(targets,repeat=2):
            s=[dot(v,v) for v in p];t=[dot(v,v) for v in q]
            c=[(dot(p[i],q[i]),det(p[i],q[i]),s[i]) for i in range(2)]
            S=s[0]*s[1];H=dot(p[0],p[1])*dot(q[0],q[1])+det(p[0],p[1])*det(q[0],q[1]);D=S-H
            gram=min(t[i]-s[i] for i in range(2))>=0 and (D<=0 or D*D<=S*(t[0]-s[0])*(t[1]-s[1]))
            val=feasible(c)['feasible'];require(val==gram==positive_disk_oracle(c),'Gram/common-boundary/disk projection discrepancy');decisions.append(val)
    triples=[]
    for cs in combinations([(x,y,F(1)) for x,y in targets],3):
        val=feasible(cs)['feasible'];require(val==positive_disk_oracle(cs),'three-constraint convex oracle');triples.append(val)
    triple=[(F(3),F(0),F(1)),(F(-9,5),F(12,5),F(1)),(F(-9,5),F(-12,5),F(1))]
    require(all(feasible(c)['feasible'] for c in combinations(triple,2)) and not feasible(triple)['feasible'],'pairwise common-roll counterexample')
    signed=[([(F(0),F(0),F(-1))],True),([(F(0),F(0),F(1))],False),([],True),([(F(1),F(0),F(-1))],True),([(F(1),F(0),F(1))],True),([(F(1),F(0),F(1)),(F(-1),F(0),F(1))],False),([(F(1),F(0),F(-1,2)),(F(-1),F(0),F(-1,2))],True)]
    for c,val in signed:require(feasible(c)['feasible']==val,'signed/zero/equality circle control')
    return {'two_pair_controls':len(decisions),'two_pair_passing':sum(decisions),'two_pair_decisions_sha256':hashlib.sha256(bytes(decisions)).hexdigest(),'three_constraint_controls':len(triples),'three_constraint_passing':sum(triples),'three_constraint_decisions_sha256':hashlib.sha256(bytes(triples)).hexdigest(),'pairwise_feasible_global_infeasible':[[str(x) for x in c] for c in triple],'signed_zero_equality_controls':len(signed),'independent_oracle':'closest-point projections and line intersections of strictly positive halfplanes against the unit disk'}

def planar_polar(b,constraints,metric):
    """Separate exact convex-polar algorithm for negative thresholds."""
    require(all(h<0 for x,y,h in constraints),'strictly negative lower thresholds')
    points=sorted(set((x/h,y/h) for x,y,h in constraints))
    require(all((-x,-y) in points for x,y in points),'centrally symmetric dual inventory')
    def turn(p,q,t):return (q[0]-p[0])*(t[1]-p[1])-(q[1]-p[1])*(t[0]-p[0])
    chains=[]
    for seq in (points,reversed(points)):
        chain=[]
        for p in seq:
            while len(chain)>1 and turn(chain[-2],chain[-1],p)<=0:chain.pop()
            chain.append(p)
        chains.append(chain)
    hull=chains[0][:-1]+chains[1][:-1]
    require(len(hull)>=3,'full dimensional dual')
    vertices=[]
    for (x,y),(X,Y) in zip(hull,hull[1:]+hull[:1]):
        d=x*Y-y*X;require(d>0,'origin strictly inside dual polygon')
        u,v=(Y-y)/d,(x-X)/d
        require(all(a*u+c*v<=1 for a,c in points),'every primal vertex passes all halfplanes')
        vertices.append((u,v,u*u+v*v/metric))
    maximum=max(w for u,v,w in vertices)
    deficit=1-maximum;dyadic=None
    if deficit>0:
        for k in range(1,100):
            if deficit> b.q(1,2**k):dyadic=k;break
        require(dyadic is not None,'bounded exact deficit search')
    return {'distinct_dual_points':len(points),'complete_dual_vertex_count':len(hull),'complete_dual_vertices_sha256':digest([encode(p) for p in hull]),'complete_primal_vertex_count':len(vertices),'complete_primal_vertices_sha256':digest([encode(p) for p in vertices]),'maximum_physical_roll_norm_squared':str(maximum),'maximizing_primal_vertices':[encode(p) for p in vertices if p[2]==maximum],'unit_circle_feasible':maximum>=1,'strict_squared_radius_deficit':str(deficit),'strict_deficit_exceeds_two_to_minus':dyadic,'inventory_trust':'Whole dual/primal inventories computed from all constraints, validated, and fingerprinted; maxima and attaining vertices retained explicitly.'}

def construction(b,V,C,G,wrong_edge=False,wrong_root=False,improper=False):
    S,Z,P,q=b.S,b.Z,b.P,b.q;a=P**2;c=2+P;radius=7+8*P
    require(len(V)==60 and len(C)==31 and len(G)==60,'complete original hull and symmetry inventories')
    r=(q(1,25),(2+P)/125,S(1));N=b.fdot(r,r)
    require(N==(3131+P)/3125 and a*r[0]==c*r[1],'exact weighted diagonal')
    R=rotation(b,(q(12,200000),q(14,200000),q(11,200000)),improper)
    RV=[b.act(R,v) for v in V];n1=b.act(b.transpose(R),r)
    target=silhouette(b,V,r);source=silhouette(b,RV,r)
    require(len(target['cycle'])==len(source['cycle'])==16,'both full sixteen-corner shadows')
    require(target['area_squared']==b.brightness(C,r)**2/N and source['area_squared']==b.brightness(C,n1)**2/N,'both independent gift-wrapped physical areas')
    require(source['area_squared']<target['area_squared'],'strict physical area relaxation')
    require(source['minimum_width_squared']<target['minimum_width_squared'],'strict physical minimum width relaxation')
    require(target['area_squared']<q(1171,20)**2 and 940+1520*P>q(583,10)**2,'universal source area filter')
    m=P*r[0]-r[1];d=(P,S(-1),-m);h=3*P**2+P*m
    require(b.fdot(d,r)==0 and h==max(b.fdot(d,v) for v in V),'actual filter width support')
    width=4*h*h/b.fdot(d,d);limit=(20+32*P)*(1-q(10,11664))
    require(width<limit,'universal source width filter')
    E=[v for v in V if v[2]==0]
    require(set(E)=={(sx*a,sy*c,Z) for sx in (-1,1) for sy in (-1,1)},'four literal E originals')
    actual_margins=[b.fdot(b.act(R,v),v)-b.fdot(r,b.act(R,v))*b.fdot(r,v)/N-radius+b.fdot(r,b.act(R,v))**2/N for v in E]
    require(min(actual_margins)>0,'all four same-roll equatorial margins')
    height=[b.fdot(r,v)**2/N for v in V if v not in E]
    eps,sigma=q(11,20),q(24,25)
    require(q(99,100)**2*N<1 and (1-q(1,242))**2*N<1,'receiver z/chord gates')
    require(min(height)>q(9,25) and radius<20,'all56 nonequatorial heights')
    require(q(36,125)<eps**2 and q(36,125)<q(9,25),'actual radial matching margin')
    require(1-q(3,25)**2>sigma**2 and q(99,100)>sigma,'all-source E singular gates')
    require(2*a*sigma>2*eps and 2*c*sigma-2*a>2*eps and 4*eps*(a+c)+4*eps**2<4*a*c*sigma,'all label side and determinant budgets')
    lo,hi=q(1001218143501,10**12),q(1001218143502,10**12)
    if wrong_root:lo=-lo
    require(0<lo<hi and lo*lo<N<hi*hi,'positive root enclosure')
    rows=[]
    for k in (0,1):
        records=[]
        for chi in (lo,hi):
            row=[-r[k]*r[j] for j in range(2)]+[-r[k]*(chi+1)];row[k]+=N+chi
            H=max(b.fdot(row,v) for v in V);face=[v for v in V if b.fdot(row,v)==H]
            gaps=[H-b.fdot(row,v) for v in RV]
            require(min(gaps)>0,'all actual transported-row source supports')
            records.append({'root_endpoint':str(chi),'target_support_originals':[encode(v) for v in face],'target_support':str(H),'minimum_source_margin':str(min(gaps)),'all60_source_margins_sha256':digest([str(x) for x in gaps])})
        require(records[0]['target_support_originals']==records[1]['target_support_originals'],'same affine target supporter')
        rows.append({'axis':k,'endpoints':records})
    vp,vm=(a,c,Z),(a,-c,Z);Rp,Rm=b.act(R,vp),b.act(R,vm)
    s=[radius-b.fdot(n1,v)**2/N for v in (vp,vm)];t=[radius-b.fdot(r,v)**2/N for v in (vp,vm)]
    H=(a*a-c*c-a*a*n1[0]**2/N+c*c*n1[1]**2/N)*(a*a-c*c-a*a*r[0]**2/N+c*c*r[1]**2/N)+4*a*a*c*c*n1[2]*r[2]/N
    direct=(b.fdot(Rp,Rm)-b.fdot(r,Rp)*b.fdot(r,Rm)/N)*(b.fdot(vp,vm)-b.fdot(r,vp)*b.fdot(r,vm)/N)+b.fdot(r,b.fcross(Rp,Rm))*b.fdot(r,b.fcross(vp,vm))/N
    require(H==direct and min(s+t)>0,'signed physical Gram formula')
    D=s[0]*s[1]-H;require(min(t[i]-s[i] for i in (0,1))>0 and (D<=0 or D*D<=s[0]*s[1]*(t[0]-s[0])*(t[1]-s[1])),'actual normal-only Gram pass')
    memberships=[]
    for ix,g in enumerate(G):
        v=b.act(b.transpose(g),r)
        if v[2]==0:continue
        for j in (0,1):
            major=v[j]/v[2];minor=b.absolute(v[1-j]/v[2])
            if (0<=major<=q(1,12) and minor<=major/20) or (0<=major<=q(1,20) and minor<=major/2):memberships.append([ix,j])
    require(not memberships,'receiver outside every G image W union P')
    edges=target['edges'][:-1] if wrong_edge else target['edges']
    require(len(edges)==len(target['cycle']),'full receiving edge inventory')
    edge_records=[]
    for i,j,n,h in edges:
        values=[b.fdot(n,v)-h for v in RV];excess=max(values);maximizers=[V[k] for k,x in enumerate(values) if x==excess]
        scale=b.absolute(next(x for x in n if x!=0))
        edge_records.append({'from_original':encode(V[i]),'to_original':encode(V[j]),'normal':encode(b.scale(1/scale,n)),'height':str(h/scale),'maximum_source_excess':str(excess/scale),'maximizing_source_originals':[encode(v) for v in maximizers],'all60_source_excesses_sha256':digest([str(v/scale) for v in values])})
    violations=sum(b.S() < max(b.fdot(n,v)-h for v in RV) for i,j,n,h in edges)
    require(violations==10,'exactly ten of sixteen full edges fail')
    literal=((126+3*P)/125,1-26*P/25,(-6+2*P)/125);lh=(9+397*P)/125
    require(max(b.fdot(literal,v) for v in V)==lh,'literal actual receiving support')
    fail=b.fdot(literal,b.act(R,vm))-lh
    require(fail==q(390098826,1666666685875)+q(10884614,5000000057625)*P and fail>0,'literal positive original support violation')
    tests=[]
    u=(S(1),Z,-r[0]);U=b.fdot(u,u)
    reflected=[b.add(b.sub(b.scale(2*b.fdot(u,v)/U,u),v),b.scale(b.fdot(r,v)/N,r)) for v in RV]
    require(all(b.fdot(r,w)==0 and b.fdot(w,w)==b.fdot(v,v)-b.fdot(r,v)**2/N for v,w in zip(RV,reflected,strict=True)),'actual reflected-plane projection isometry')
    for parity,vertices in [('proper',RV),('reflected',reflected)]:
        cs=[];labels=[]
        for ei,(i,j,n,h) in enumerate(edges):
            for si in source['cycle']:
                v=vertices[si]
                x,y=-b.fdot(n,v),-b.fdot(r,b.fcross(v,n))/N
                require(x*x+N*y*y==(b.fdot(v,v)-b.fdot(r,v)**2/N)*b.fdot(n,n),'actual physical circle coefficient norm')
                cs.append((x,y,-h));labels.append({'edge':ei,'source_original':encode(V[si])})
        decision=feasible(cs,N)
        polar=planar_polar(b,cs,N)
        require(decision['feasible']==polar['unit_circle_feasible'],'common-angle endpoint and convex-polar disagreement')
        require(not decision['feasible'] and polar['strict_deficit_exceeds_two_to_minus']<=15,'fixed planes reject every placement with quantitative shrinkage')
        rejection=decision.pop('rejected_boundaries',[])
        decision['all_rejected_boundary_count']=len(rejection)
        decision['all_rejected_boundaries_sha256']=digest(rejection)
        tests.append({'parity':parity,'constraints':len(cs),'constraint_order':'target edge outer, source cycle position inner','constraints_sha256':digest([[str(x) for x in c] for c in cs]),'decision':decision,'independent_convex_polar':polar})
    return {'receiver_raw':encode(r),'receiver_norm_squared':str(N),'source_rotation':[encode(row) for row in R],'source_normal_raw':encode(n1),'area_target_squared':str(target['area_squared']),'area_source_squared':str(source['area_squared']),'width_target_squared':str(target['minimum_width_squared']),'width_source_squared':str(source['minimum_width_squared']),'all_target_edge_widths_squared':[str(x) for x in target['all_edge_widths_squared']],'all_source_edge_widths_squared':[str(x) for x in source['all_edge_widths_squared']],'target_cycle_originals':[encode(V[i]) for i in target['cycle']],'source_cycle_originals':[encode(V[i]) for i in source['cycle']],'receiving_width_filter_squared':str(width),'width_filter_margin':str(limit-width),'all56_nonequatorial_heights_sha256':digest([str(x) for x in height]),'minimum_nonequatorial_height_squared':str(min(height)),'label_maps':b.label_maps(),'all_four_actual_equatorial_margins':[str(x) for x in actual_margins],'actual_rows':rows,'gram':{'s':[str(x) for x in s],'t':[str(x) for x in t],'H':str(H),'D':str(D)},'all16_receiving_edge_records':edge_records,'violating_edges':violations,'literal_failed_edge':{'normal':encode(literal),'height':str(lh),'source_original':encode(vm),'excess':str(fail)},'all120_G_family_membership_tests':120,'W_union_P_memberships':memberships,'full_shadow_common_angle_tests':tests}

def build():
    b,pin=geometry();raw=b.originals();V=[b.as_fields(v,2) for v in raw]
    C,hull=b.facets(raw);G=b.proper_group(V);polar,rho0,rho5=b.polar_data(C,V,G);filt=b.width_filter(C,V,rho0,rho5)
    physical=construction(b,V,C,G);damages=[]
    for name,kw in [('missing_receiving_edge',{'wrong_edge':True}),('negative_normalization_root',{'wrong_root':True}),('improper_source_rotation',{'improper':True})]:
        try:construction(b,V,C,G,**kw)
        except ValueError:damages.append(name)
        else:raise ValueError('damaged construction accepted:'+name)
    for name,fn in [('nonpositive_plane_metric',lambda:feasible([(1,0,1)],0)),('missing_original',lambda:construction(b,V[:-1],C,G)),('wrong_positive_root_square',lambda:require(b.q(1001218143502,10**12)**2<(3131+b.P)/3125,'false upper bracket'))]:
        try:fn()
        except ValueError:damages.append(name)
        else:raise ValueError('damaged control accepted:'+name)
    square=[(F(x),F(y),F(-1)) for x,y in [(1,1),(-1,1),(-1,-1),(1,-1)]]
    pp=planar_polar(b,square,1)
    # The diamond polar has extrema of squared norm1; preserve literal equality.
    require(pp['unit_circle_feasible'] and pp['strict_squared_radius_deficit']=='0','unit-circle tangency control')
    require(feasible(square)['feasible'],'unit-circle touching support control')
    return {'actual_reviewer':'six-reviewer-4','role':'independent mathematical reviewer','dependency_commit':pin['source_commit'],'hull_sha256':digest(hull),'proper_group_size':len(G),'complete_physical_polar_sha256':digest(polar),'all_source_filter_sha256':digest(filt),'circle':circle_controls(),'physical_construction':physical,'damaged_controls_rejected':damages,'polar_unit_circle_tangency_control':pp}

def main():
    p=argparse.ArgumentParser();p.add_argument('--emit',action='store_true');a=p.parse_args()
    out=(json.dumps(build(),sort_keys=True,indent=2)+'\n').encode()
    if a.emit:sys.stdout.buffer.write(out)
    else:require(out==(HERE/'expected.json').read_bytes(),'complete independent record differs');print('PASS')
if __name__=='__main__':main()
