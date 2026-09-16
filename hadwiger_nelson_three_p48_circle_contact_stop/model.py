"""Producer geometry in Q(sqrt(-3),sqrt(-11),sqrt(-35))."""
from fractions import Fraction as F
from itertools import combinations
import hashlib,json
D=336
RAD=(-3,-11,-35)
ZERO=(F(0),)*8

def scalar(v): return (F(v),)+(F(0),)*7
def root(i): return tuple(F(int(j==1<<i)) for j in range(8))
def add(x,y): return tuple(a+b for a,b in zip(x,y))
def scale(x,s): return tuple(a*s for a in x)
def mul(x,y):
    out=[0]*8
    for i,a in enumerate(x):
        if not a: continue
        for j,b in enumerate(y):
            if not b: continue
            c=a*b
            for k,r in enumerate(RAD):
                if (i&j)>>k&1: c*=r
            out[i^j]+=c
    return tuple(out)
def conj(x): return tuple(a*(-1 if i.bit_count()%2 else 1) for i,a in enumerate(x))
def norm(x): return mul(x,conj(x))
def encode(x):
    q=[a*D for a in x]
    if any(F(a).denominator!=1 for a in q): raise ValueError('bad denominator')
    return tuple(int(a) for a in q)
def hash_rows(rows): return hashlib.sha256(''.join(','.join(map(str,r))+'\n' for r in rows).encode()).hexdigest()
def geometry():
    one=scalar(1); omega=scale(add(one,root(0)),F(1,2)); r=scale(add(scalar(5),root(1)),F(1,6))
    A=add(scalar(2),omega); B=mul(r,A); delta=add(B,scale(A,-1)); v=scale(mul(delta,add(one,scale(root(2),F(1,7)))),F(1,2))
    if norm(r)!=one or norm(v)!=one or norm(delta)!=scalar(F(7,3)): raise ValueError('isometry failure')
    addresses=[(a,b) for a in range(-8,9) for b in range(-8,9) if a*a+a*b+b*b<=48]
    if len(addresses)!=169: raise ValueError('source size')
    patch=[add(scalar(a),scale(omega,b)) for a,b in addresses]
    raw=[[encode(z) for z in patch],[encode(mul(r,z)) for z in patch],[encode(add(A,mul(v,z))) for z in patch]]
    points=sorted(set(sum(raw,[]))); lookup={p:i for i,p in enumerate(points)}
    images=[[lookup[z] for z in layer] for layer in raw]
    edges=[]
    for i,j in combinations(range(len(points)),2):
        delta=tuple(a-b for a,b in zip(points[i],points[j]))
        if norm(delta)==(D*D,0,0,0,0,0,0,0): edges.append((i,j))
    special={name:lookup[encode(z)] for name,z in [('O',ZERO),('A',A),('B',B),('C',add(A,v))]}
    moser=[lookup[encode(z)] for z in [ZERO,one,omega,add(one,omega),r,mul(r,omega),mul(r,add(one,omega))]]
    return dict(denominator=D,points=points,edges=edges,images=images,addresses=addresses,special=special,moser=moser,r=encode(r),A=encode(A),v=encode(v))

def summary(g):
    ed=set(g['edges']); sets=list(map(set,g['images'])); inherited=set()
    internals=[]
    for s in sets:
        e={e for e in ed if e[0] in s and e[1] in s};internals.append(len(e));inherited|=e
    overlaps=[[i,j,len(sets[i]&sets[j])] for i,j in combinations(range(3),2)]
    cross={f'{i}-{j}':sum((a in sets[i] and b in sets[j]) or (b in sets[i] and a in sets[j]) for a,b in ed-inherited) for i,j in combinations(range(3),2)}
    return dict(vertices=len(g['points']),edges=len(ed),coordinate_sha256=hash_rows(g['points']),edge_sha256=hash_rows(g['edges']),internal_edges=internals,overlaps=overlaps,extra_edges=len(ed-inherited),extra_edges_by_pair=cross,special=g['special'],moser=g['moser'])

if __name__=='__main__': print(json.dumps(summary(geometry()),indent=2,sort_keys=True))
