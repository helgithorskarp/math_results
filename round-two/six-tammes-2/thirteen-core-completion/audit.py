"""Separate thirteen-core cap audit using raw polynomials and Taylor signs.

Imports neither the production field/checker nor prerequisite arithmetic.
Rechecks all active-plane triples, their status, norm gaps and unit fixtures.
Adapts the raw-polynomial arithmetic from the prior fourteen-point audit;
imports no primary arithmetic or prior proof module.
"""
from fractions import Fraction as Q
from math import comb
from itertools import combinations
from pathlib import Path
import hashlib,json

HERE=Path(__file__).resolve().parent
F=tuple(map(Q,(-1,-3,2,6,-1,13)))
L=Q('0.59260590292507377809642492233275')
R=Q('0.59260590292507377809642492233276')
MID=(L+R)/2;RAD=(R-L)/2
ONE=(Q(1),);T=(Q(0),Q(1));Z=()

def need(ok,message):
    if not ok:raise ValueError(message)
def trim(p):
    p=list(p)
    while p and p[-1]==0:p.pop()
    return tuple(p)
def add(a,b):
    return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0)
                 for i in range(max(len(a),len(b)))])
def scale(p,q):return trim([q*x for x in p])
def sub(a,b):return add(a,scale(b,-1))
def mul(a,b):
    p=[Q(0)]*max(0,len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:p[i+j]+=x*y
    return trim(p)
def remainder(p):
    r=list(p)
    while len(r)>=6:
        k=len(r)-6;z=r[-1]/13
        for j,c in enumerate(F):r[k+j]-=z*c
        while r and r[-1]==0:r.pop()
    return tuple(r)
def eval_at(p,x):
    return sum((c*x**i for i,c in enumerate(p)),Q(0))
def bounds(p):
    # Exact Taylor expansion at the midpoint; bound every nonconstant term
    # by its absolute coefficient times the corresponding radius power.
    p=remainder(p)
    co=[sum((p[k]*comb(k,j)*MID**(k-j) for k in range(j,len(p))),Q(0))
        for j in range(len(p))]
    if not co:return Q(0),Q(0)
    err=sum((abs(co[j])*RAD**j for j in range(1,len(co))),Q(0))
    return co[0]-err,co[0]+err
def sign(p):
    if not remainder(p):return 0
    lo,hi=bounds(p)
    if lo>0:return 1
    if hi<0:return -1
    raise ValueError('unresolved independent Taylor sign')
def psum(seq):
    s=Z
    for p in seq:s=add(s,p)
    return s
def dot(a,b):return psum(mul(x,y) for x,y in zip(a,b))
def cross(a,b):
    return (sub(mul(a[1],b[2]),mul(a[2],b[1])),
            sub(mul(a[2],b[0]),mul(a[0],b[2])),
            sub(mul(a[0],b[1]),mul(a[1],b[0])))
def mv(M,v):return tuple(dot(row,v) for row in M)
def norm(v,H):return dot(v,mv(H,v))
def homogeneous(rows,rhs):
    # General Cramer vector from row cross products, without polynomial
    # coefficient reduction or three replaced-column determinant calls.
    c0,c1,c2=cross(rows[1],rows[2]),cross(rows[2],rows[0]),cross(rows[0],rows[1])
    return dot(rows[0],c0),tuple(psum(mul(q,c[k]) for q,c in zip(rhs,(c0,c1,c2))) for k in range(3))

def verify(c):
    core=tuple(i for i in range(15) if i not in (3,14))
    need(c['core_labels']==list(core),'thirteen prescribed core points')
    steps=((6,0,11,5),(7,0,5,11),(9,5,11,0),
           (8,2,4,1),(10,1,2,4),(12,1,10,2),(13,2,8,4))
    edges=set();errors={0:0,5:2,11:17,1:0,2:2,4:17}
    for triangle in ((0,5,11),(1,2,4)):
        edges.update(tuple(sorted(e)) for e in combinations(triangle,2))
    for n,i,j,o in steps:
        need(all(tuple(sorted(e)) in edges for e in ((i,j),(i,o),(j,o))),'core reflection antecedent')
        edges.update((tuple(sorted((n,i))),tuple(sorted((n,j)))))
        errors[n]=20+errors[i]+errors[j]+errors[o]
    edges.update(((6,8),(7,12),(9,10),(9,13)))
    need(len(edges)==24 and c['core_edges']==[list(e) for e in sorted(edges)]
         and set(errors)==set(core) and max(errors.values())<80,'complete core-only hypothesis')
    V=[tuple(trim([Q(x) for x in p]) for p in row) for row in c['incumbent_vectors']]
    need(len(V)==15 and all(len(v)==3 for v in V),'reference vector shape')
    H=tuple(tuple(ONE if i==j else T for j in range(3)) for i in range(3))
    derivative=tuple(i*F[i] for i in range(1,6))
    need(eval_at(F,L)<0<eval_at(F,R) and bounds(derivative)[0]>0,'independent root bracket')
    need(Q(1,2)<L<R<Q(3,5),'metric eigenvalue and scaling domain')
    need(all(sign(sub(norm(v,H),ONE))==0 for v in V),'all unit reference points')
    N=[mv(H,v) for v in V]
    exterior=[]
    need([x['active_labels'] for x in c['exterior_vertices']]==[[0,4,6],[0,4,7]],'exterior defining planes')
    for item in c['exterior_vertices']:
        point=tuple(trim([Q(x) for x in p]) for p in item['vector'])
        labels=item['active_labels'];D,_=homogeneous([N[i] for i in labels],(T,T,T))
        need(sign(D)!=0 and all(sign(sub(dot(N[i],point),T))==0 for i in labels),'exact exterior point')
        need(all(sign(sub(dot(N[i],point),T))<=0 for i in core),'exterior intersection feasible')
        need(sign(sub(norm(point,H),ONE))>0,'exterior squared norm')
        exterior.append(point)
    C=tuple(trim([Q(x) for x in p]) for p in c['center']);blend=Q(c['center_blend'])
    need(blend==Q(4,5) and all(sign(sub(C[k],add(add(exterior[0][k],exterior[1][k]),scale(V[3][k],blend))))==0
                               for k in range(3)),'cap center from exact exterior points')
    cut=Q(c['cap_bound']);upper=Q(c['cap_code_parameter_upper'])
    gap=sub((2*cut**2,),scale(norm(C,H),1+upper))
    need(cut>0 and upper==Q(593,1000) and sign(sub(gap,(Q(c['cap_capacity_gap_lower']),)))>0,
         'strict capacity gap above the full code strip')
    need(sign(sub(norm(C,H),(cut**2,)))>0 and sign(sub((cut,),dot(V[3],mv(H,C))))>0,
         'proper cap and isolated vertex in cut')
    constraints=[(i,N[i],T) for i in core]+[('cap',mv(H,C),(cut,))]
    tet=(0,1,2,5)
    rows=tuple(tuple(V[tet[j]][i] for j in range(3)) for i in range(3))
    D,U=homogeneous(rows,tuple(scale(p,-1) for p in V[5]));sd=sign(D)
    need(sd!=0 and all(sign(p)*sd>0 for p in U),'positive spanning origin dependence')
    need(all(sign(add(dot(rows[i],U),mul(D,V[5][i])))==0 for i in range(3)),'origin dependence identity')
    r=Q(c['short_squared_norm_upper']);need(0<r<1,'strict short norm bound')
    records=[];feasible=[];units=[]
    for inds in combinations(range(14),3):
        labels=[constraints[i][0] for i in inds]
        rows=[constraints[i][1] for i in inds];rhs=[constraints[i][2] for i in inds]
        D,U=homogeneous(rows,rhs);sd=sign(D)
        if not sd:records.append([labels,'singular']);continue
        need(all(sign(sub(dot(rows[i],U),mul(rhs[i],D)))==0 for i in range(3)),'direct Cramer equations')
        witness=next((label for label,n,b in constraints if sign(sub(dot(n,U),mul(b,D)))*sd>0),None)
        if witness is not None:records.append([labels,'infeasible',witness]);continue
        nn,square=norm(U,H),mul(D,D)
        if sign(sub(nn,square))==0:
            need(all(sign(sub(U[k],mul(D,V[3][k])))==0 for k in range(3)),'unit vertex equals missing point3')
            units.append(labels);records.append([labels,'unit'])
        else:
            need(sign(sub(nn,scale(square,r)))<0,'every other vertex strictly short')
            records.append([labels,'short'])
        for DD,UU in feasible:
            need(any(sign(sub(mul(U[k],DD),mul(UU[k],D)))!=0 for k in range(3)),
                 'distinct vertices by homogeneous cross multiplication')
        feasible.append((D,U))
    need(len(records)==364 and len(feasible)==24 and units==[[1,4,7]],'full enumeration counts')
    d=Q(c['relaxation_max']);distance=c['relaxed_isolated_distance_constant']
    need(0<d<=Q(1,1000) and distance>=2+8/(1-r),'isolated relaxed distance')
    e=Q(c['near_contact_max']);ee=Q(c['exclusion_max']);K=c['whole_configuration_constant']
    fourteen=max(2000000,distance*2030000);last=fourteen+30000
    need(0<=ee<=e<=Q(1,10**13) and 2030000*e<=d and last*e<=Q(1,1000),'both relaxed polytopes entered')
    need(K>=max(fourteen,1000*last) and K*ee<=Q(1,100) and 10*K*ee<=Q(1,400000),
         'whole-code error and both local radii')
    digest=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {'status':'AUDITED','active_plane_triples':364,'cut_vertices':24,
            'short_vertices':23,'unit_vertices':1,'enumeration_sha256':digest,
            'representation':'raw polynomial row-cross Cramer vectors; centered Taylor signs'}

if __name__=='__main__':
    print(json.dumps(verify(json.loads((HERE/'certificate.json').read_text())),sort_keys=True))
