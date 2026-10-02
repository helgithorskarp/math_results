"""Independent literal set model; six-reviewer-4, PASS35. No native imports."""
from itertools import combinations

U,V,A = 'u','v','a'
X=tuple('X'+str(i) for i in range(6))
SX=('SX0','SX1'); SY=('SY0','SY1'); T=('T0','T1','T2')
OLD=(U,V,A)+X+SX+SY+T
CYCLE=((0,4),(4,3),(3,1),(1,2),(2,5),(5,0))
TIGHT=((0,4),(0,5),(1,2),(1,3))
Q=frozenset(range(6))

def need(ok,message):
    if not ok: raise ValueError(message)

def subsets(universe,k=None):
    universe=tuple(sorted(universe))
    return [frozenset(z) for n in range(len(universe)+1) if k is None or n==k
            for z in combinations(universe,n)]

def covers():
    return [r for r in subsets(range(6)) if all(r & {i,j} for i,j in TIGHT)]

def frame(rows,r=0):
    need(set(rows)==set(SY+T),'endpoint names')
    need(r in (0,1),'actual orientation')
    g={v:set() for v in OLD}
    def edge(a,b): g[a].add(b);g[b].add(a)
    for z in (V,A)+X+SX: edge(U,z)
    edge(A,V)
    for i,j in CYCLE: edge(X[i],X[j])
    for j,pair in enumerate(((3,5),(2,4))):
        edge(A,SX[j])
        for i in pair: edge(SX[j],X[i])
    for z in SY: edge(V,z);edge(A,z)
    for z in T: edge(A,z)
    for z,ts in ((SY[0],(1,2)),(SY[1],(0,1))):
        for k in ts: edge(z,T[k])
    for j in range(2):
        for k in ((1,2),(0,2))[j ^ r]: edge(SX[j],T[k])
    for z in SY+T:
        for i in rows[z]: edge(z,X[i])
    rank={U:0,V:6,A:0,SX[0]:4,SX[1]:4,SY[0]:2,SY[1]:2,
          T[0]:3,T[1]:2,T[2]:3}
    for z in X: rank[z]=10-len(g[z])
    degrees={z:len(g[z])+rank[z] for z in OLD}
    return g,rank,degrees

def bounds(g,rank,degrees,a,b):
    red=b in g[a]
    cap=3 if red else degrees[a]+degrees[b]-14
    upper=cap-len(g[a]&g[b])
    return max(0,rank[a]+rank[b]-6),upper

def row_pair_ok(g,rank,degrees,a,qa,b,qb):
    lower,upper=bounds(g,rank,degrees,a,b)
    return lower <= len(qa&qb) <= upper

def point_failure(g,rank,rows,q):
    near={z for z in OLD if q in rows[z]}
    h=4-len(near & set(SY+T))
    if not 0<=h<=5: return ['internal_degree',h]
    dq=len(near)+h
    for a in OLD:
        red=a in near
        cap=3 if red else len(g[a])+rank[a]+dq-14
        known=len(g[a]&near)
        minimum=max(0,h+rank[a]-(6 if red else 5))
        if known+minimum>cap: return [a,red,known,minimum,cap,h,dq]
    return None

def point_ok(g,rank,rows,q):
    return point_failure(g,rank,rows,q) is None

def transport(rows,r,which):
    perm=(1,0,4,5,2,3) if which==0 else (0,1,3,2,5,4)
    dst={z:frozenset(perm[i] for i in rows[z]) for z in rows}
    oldperm={z:z for z in OLD}
    oldperm.update({X[i]:X[perm[i]] for i in range(6)})
    if which==1: oldperm.update({SX[0]:SX[1],SX[1]:SX[0]})
    return dst,r ^ which,oldperm

def canonical(obj):
    import json
    return json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n'
