"""Separate arithmetic audit: unreduced polynomials and centered Taylor signs.

Imports neither the production field/checker nor prerequisite arithmetic.
Rechecks all active-plane triples, their status, norm gaps and unit fixtures.
Does not rederive the old fourteen-point proximity argument or local stress.
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
    need(c['fixed_labels']==list(range(14)),'all fourteen inequalities')
    V=[tuple(trim([Q(x) for x in p]) for p in row) for row in c['incumbent_vectors']]
    need(len(V)==15 and all(len(v)==3 for v in V),'input vector shape')
    H=tuple(tuple(ONE if i==j else T for j in range(3)) for i in range(3))
    derivative=tuple(i*F[i] for i in range(1,6))
    # Derivative is evaluated before reducing modulo F.
    dp=[sum((derivative[k]*comb(k,j)*MID**(k-j) for k in range(j,len(derivative))),Q(0))
        for j in range(len(derivative))]
    need(eval_at(F,L)<0<eval_at(F,R) and dp[0]>sum(abs(dp[j])*RAD**j for j in range(1,len(dp))),
         'independently bracketed unique root')
    need(all(sign(sub(norm(v,H),ONE))==0 for v in V),'incumbent unit norms')
    N=[mv(H,V[i]) for i in range(14)]
    tet=(0,1,2,5)
    rows=tuple(tuple(V[tet[j]][i] for j in range(3)) for i in range(3))
    D,U=homogeneous(rows,tuple(scale(p,-1) for p in V[5]))
    sd=sign(D)
    need(sd!=0 and all(sign(p)*sd>0 for p in U),'positive origin tetrahedron')
    need(all(sign(add(dot(rows[i],U),mul(D,V[5][i])))==0 for i in range(3)),
         'origin dependence exact identity')
    expected_units=(V[14],tuple(trim([Q(x) for x in p]) for p in c['alternate_vector']))
    need(sign(sub(norm(expected_units[1],H),ONE))==0,'second completion unit')
    gap=sub(scale(ONE,2),scale(dot(expected_units[0],mv(H,expected_units[1])),2))
    need(sign(sub(gap,(Q(1,25),)))>0,'completion separation bound')
    records=[];feasible=[];unit_indices=[]
    for triple in combinations(range(14),3):
        rows=tuple(N[i] for i in triple)
        D,U=homogeneous(rows,(T,T,T));sd=sign(D)
        if not sd:
            records.append([list(triple),'singular']);continue
        need(all(sign(sub(dot(row,U),mul(T,D)))==0 for row in rows),'direct Cramer equations')
        witness=next((i for i in range(14) if sign(sub(dot(N[i],U),mul(T,D)))*sd>0),None)
        if witness is not None:
            records.append([list(triple),'infeasible',witness]);continue
        nn,square=norm(U,H),mul(D,D)
        if sign(sub(nn,square))==0:
            matches=[i for i,v in enumerate(expected_units) if all(sign(sub(U[k],mul(D,v[k])))==0 for k in range(3))]
            need(len(matches)==1,'unit vertex is one of the two advertised completions')
            unit_indices.append(matches[0]);records.append([list(triple),'unit'])
        else:
            need(sign(sub(nn,scale(square,Q(3,4))))<0,'short vertex squared norm below three quarters')
            records.append([list(triple),'short'])
        for DD,UU in feasible:
            need(any(sign(sub(mul(U[k],DD),mul(UU[k],D)))!=0 for k in range(3)),
                 'distinct feasible vertices by homogeneous cross multiplication')
        feasible.append((D,U))
    need(len(feasible)==24 and sorted(unit_indices)==[0,1],'complete feasible/short/unit counts')
    need(Q(16,1000)<=Q(1,2) and 2*(4+100)*4+2<1000,'mass and distance estimates')
    need(2030000*Q(c['near_contact_max'])<=Q(1,1000),'near-contact polytope entry')
    need(1000*2030000<2100000000,'whole-configuration bound')
    need(10*2100000000*Q(c['asymmetric_exclusion_max'])<=Q(1,400000),'old local-radius entry')
    digest=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {'status':'AUDITED','active_plane_triples':len(records),'vertices':len(feasible),
            'short_vertices':22,'unit_vertices':2,'enumeration_sha256':digest,
            'representation':'unreduced polynomial determinants; centered Taylor signs'}

if __name__=='__main__':
    print(json.dumps(verify(json.loads((HERE/'certificate.json').read_text())),sort_keys=True))
