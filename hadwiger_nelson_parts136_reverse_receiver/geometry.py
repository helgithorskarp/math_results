"""Exact Parts receiver, ordinary colour CNFs and complete orbit enumeration."""
from pathlib import Path
from itertools import combinations, permutations
from math import gcd
import hashlib, json
RADICALS=(1,3,5,15,11,33,55,165)
SCALE=96
SOURCE_SHA='f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50'
H=[0]+list(range(374,509))
D=list(range(1,374))
PERMS=[(0,)+p for p in permutations((1,2,3))]
def require(ok,msg):
    if not ok: raise ValueError(msg)
def read_points(path):
    raw=Path(path).read_bytes()
    require(hashlib.sha256(raw).hexdigest()==SOURCE_SHA,'coordinate source hash')
    p=[tuple(map(int,l.split())) for l in raw.decode().splitlines() if l and not l.startswith('#')]
    require(len(p)==len(set(p))==509 and all(len(v)==16 for v in p),'exact distinct points')
    return p
def norm(delta,sparse=False):
    r={}
    for axis in (delta[:8],delta[8:]):
        for i,x in enumerate(axis):
            if not x: continue
            for j,y in enumerate(axis):
                if not y: continue
                if sparse:
                    g=gcd(RADICALS[i],RADICALS[j]); k=RADICALS[i]*RADICALS[j]//(g*g)
                else:
                    g=RADICALS[i&j]; k=RADICALS[i^j]
                r[k]=r.get(k,0)+g*x*y
    return {k:v for k,v in r.items() if v}
def reconstruct(path):
    p=read_points(path); edges=[]
    for i,j in combinations(range(509),2):
        delta=[x-y for x,y in zip(p[i],p[j])]
        a=norm(delta); b=norm(delta,True)
        require(a==b,'independent distance arithmetic')
        if a=={1:SCALE*SCALE}: edges.append([i,j])
    require(len(edges)==2442,'parent complete strict graph')
    hs=set(H); ds=set(D)
    he=[e for e in edges if set(e)<=hs]
    de=[e for e in edges if set(e)<=ds]
    cross=[[a,b] if a in hs else [b,a] for a,b in edges if (a in hs)!=(b in hs)]
    B=sorted({a for a,b in cross})
    require(B==[0,430,432,434,476,478,480,481,482,483,484,485,486,487,488,489,490,491,492],'frozen boundary')
    require(len(he)==564 and len(de)==1836 and len(cross)==42,'edge split')
    require(not any(set(e)<=set(B) for e in he),'independent boundary')
    return dict(edges=edges,host_edges=he,module_edges=de,cross_edges=cross,boundary=B,
                source_sha256=SOURCE_SHA,unordered_pairs=129286,host=H,module=D,
                host_points=136,module_points=373,replacement_new_point_cap=372,total_point_cap=508)
def cnf(vertices,edges,k=4):
    idx={v:i for i,v in enumerate(vertices)}
    var=lambda v,c:k*idx[v]+c+1
    clauses=[]
    for v in vertices:
        clauses.append([var(v,c) for c in range(k)])
        clauses.extend([-var(v,c),-var(v,d)] for c,d in combinations(range(k),2))
    for a,b in edges:
        clauses.extend([-var(a,c),-var(b,c)] for c in range(k))
    return clauses,var

def dump_cnf(path,clauses,nvars):
    with Path(path).open('w') as f:
        f.write(f'p cnf {nvars} {len(clauses)}\n')
        for c in clauses: f.write(' '.join(map(str,c))+' 0\n')

def canonical(col):
    return min(tuple(p[c] for c in col) for p in PERMS)

def proper(word,vertices,edges,k=4):
    require(len(word)==len(vertices) and all(c in '0123456789'[:k] for c in word),'word domain')
    col={v:int(c) for v,c in zip(vertices,word)}
    require(all(col[a]!=col[b] for a,b in edges),'proper literal colouring')
    return col
