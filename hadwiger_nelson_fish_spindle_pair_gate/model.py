"""One exact fixed fish--spindle Minkowski support, with complete unit graph."""
from fractions import Fraction as Q
from itertools import combinations
from math import isqrt
from hashlib import sha256
from pathlib import Path
import json

FIXED = {0:(0,0),1:(1,0),2:(0,1),5:(1,1)}

def need(ok, message):
    if not ok: raise ValueError(message)

def fish(path):
    c=json.loads(path.read_text())
    need(c['schema']=='fish-fixed-square-root-v1','schema')
    H=c['midpoint_denominator'];D=c['inverse_denominator'];rd=c['radius_denominator']
    need(all(type(z) is int and z>0 for z in (H,D,rd)),'positive integer denominators')
    r=Q(1,rd);mid=c['midpoint_numerators'];A=c['inverse_numerators'];E=list(map(tuple,c['edges']))
    need(len(mid)==23 and all(len(p)==2 and all(type(z) is int for z in p) for p in mid),'point dimensions')
    need(c['fixed_vertices']=={str(i):list(z) for i,z in FIXED.items()},'fixed square labels')
    for i,z in FIXED.items():need(mid[i]==[H*x for x in z],'fixed square coordinates')
    need(E==sorted(set(E)) and len(E)==42 and all(type(a) is int and type(b) is int and 0<=a<b<23 for a,b in E),'edge list')
    free=[i for i in range(23) if i not in FIXED];where={v:i for i,v in enumerate(free)}
    fixed_edges=[e for e in E if all(i in FIXED for i in e)]
    need(fixed_edges==[(0,1),(0,2),(1,5),(2,5)],'square edges')
    eq=[e for e in E if e not in fixed_edges];n=2*len(free)
    need(n==len(eq)==38,'square equation count')
    need(len(A)==n and all(len(row)==n and all(type(z) is int for z in row) for row in A),'inverse shape')
    J=[[0]*n for _ in range(n)];F=[]
    for k,(a,b) in enumerate(eq):
        diff=[mid[a][d]-mid[b][d] for d in range(2)]
        F.append(sum(z*z for z in diff)-H*H)
        for d in range(2):
            if a in where:J[k][2*where[a]+d]=2*diff[d]
            if b in where:J[k][2*where[b]+d]=-2*diff[d]
    B=[[int(i==j)*D*H-sum(A[i][k]*J[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    beta=Q(max(sum(abs(z) for z in row) for row in B),D*H)
    anorm=Q(max(sum(abs(z) for z in row) for row in A),D)
    afnorm=Q(max(abs(sum(A[i][k]*F[k] for k in range(n))) for i in range(n)),D*H*H)
    eta=beta+16*r*anorm;delta=afnorm+eta*r
    need(beta<1 and eta<1 and delta<r,'rational contraction and inclusion')
    points=[tuple(Q(z,H) for z in p) for p in mid]
    sep=gap=None
    for a,b in combinations(range(23),2):
        diff=[points[a][d]-points[b][d] for d in range(2)]
        d2=sum(z*z for z in diff);err=4*r*sum(abs(z) for z in diff)+8*r*r
        need(d2>err,'fish point separation')
        sep=d2-err if sep is None else min(sep,d2-err)
        if (a,b) not in E:
            need(abs(d2-1)>err,'fish nonedge gap')
            gap=abs(d2-1)-err if gap is None else min(gap,abs(d2-1)-err)
    summary={'points':23,'unit_edges':42,'root_variables':38,'radius':str(r),'beta':str(beta),'inverse_norm':str(anorm),'eta':str(eta),'self_map_displacement':str(delta),'squared_separation_lower':str(sep),'nonedge_squared_unit_gap_lower':str(gap),'certificate_sha256':sha256(path.read_bytes()).hexdigest()}
    return points,E,r,summary

# Exact real field Q(sqrt(3),sqrt(11)); mask basis (1,sqrt3,sqrt11,sqrt33).
def real(a=0,b=0,c=0,d=0):return tuple(map(Q,(a,b,c,d)))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,b):
    out=[Q(0)]*4
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i^j]+=x*y*(3 if i&j&1 else 1)*(11 if i&j&2 else 1)
    return tuple(out)
def moser():
    M=[(real(),real()),(real(1),real()),(real(Q(1,2)),real(0,Q(1,2))),
       (real(Q(3,2)),real(0,Q(1,2))),(real(Q(5,6)),real(0,0,Q(1,6))),
       (real(Q(5,12),0,0,Q(-1,12)),real(0,Q(5,12),Q(1,12))),
       (real(Q(5,4),0,0,Q(-1,12)),real(0,Q(5,12),Q(1,4)))]
    E=[]
    for i,j in combinations(range(7),2):
        dx,dy=(sub(M[i][d],M[j][d]) for d in range(2))
        if add(mul(dx,dx),mul(dy,dy))==real(1):E.append((i,j))
    need(len(E)==11,'Moser edge count')
    return M,E

def build(path):
    F,FE,r,fs=fish(path);M,ME=moser();H=10**50
    roots=[Q(1)]
    for d in (3,11,33):
        v=isqrt(d*H*H)
        need(v*v<=d*H*H<(v+1)*(v+1),'rational positive radical enclosure')
        roots.append(Q(v,H))
    mm=[tuple(sum(x*y for x,y in zip(z,roots)) for z in p) for p in M]
    # Each M coordinate midpoint has error <2/H; exact rational coefficients
    # are explicitly checked so this bound does not rely on rounding.
    need(all(sum(abs(z[i]) for i in range(1,4))<2 for p in M for z in p),'Moser enclosure error')
    R=r+Q(2,H);classes=[];raw_to_phys=[];key_to_phys={};points=[]
    for i in range(23):
        for j in range(7):
            key=(i,M[j]) if i not in FIXED else (-1,tuple(add(real(FIXED[i][d]),M[j][d]) for d in range(2)))
            if key not in key_to_phys:
                key_to_phys[key]=len(points);classes.append([])
                points.append(tuple(F[i][d]+mm[j][d] for d in range(2)))
            k=key_to_phys[key];classes[k].append(7*i+j);raw_to_phys.append(k)
    E=set()
    for a,b in FE:
        for j in range(7):E.add(tuple(sorted((raw_to_phys[7*a+j],raw_to_phys[7*b+j]))))
    for a,b in ME:
        for i in range(23):E.add(tuple(sorted((raw_to_phys[7*i+a],raw_to_phys[7*i+b]))))
    need(all(a<b for a,b in E),'no contracted unit edge')
    sep=gap=None;checks=0;nonedges=0
    for a,b in combinations(range(len(points)),2):
        diff=[points[a][d]-points[b][d] for d in range(2)]
        d2=sum(z*z for z in diff);err=4*R*sum(abs(z) for z in diff)+8*R*R
        need(d2>err,'physical point separation')
        sep=d2-err if sep is None else min(sep,d2-err);checks+=1
        if (a,b) not in E:
            need(abs(d2-1)>err,'unlisted physical unit contact')
            gap=abs(d2-1)-err if gap is None else min(gap,abs(d2-1)-err);nonedges+=1
    es=sorted(E)
    graph={'classes':classes,'edges':es}
    digest=sha256((json.dumps(graph,separators=(',',':'))+'\n').encode()).hexdigest()
    summary={'status':'EXACT FIXED FISH-SPINDLE SUPPORT VERIFIED','fish':fs,'points':len(points),'unit_edges':len(es),'physical_pair_checks':checks,'nonedges_excluded':nonedges,'collision_classes':[cl for cl in classes if len(cl)>1],'extra_noncartesian_edges':0,'squared_separation_lower':str(sep),'nonedge_squared_unit_gap_lower':str(gap),'graph_sha256':digest}
    return graph,summary

if __name__=='__main__':
    graph,summary=build(Path(__file__).with_name('geometry_certificate.json'))
    print(json.dumps(summary,indent=2))
