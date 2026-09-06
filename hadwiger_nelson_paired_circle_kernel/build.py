from fractions import Fraction as F
from itertools import combinations,product
from collections import Counter
from pathlib import Path
import argparse,hashlib,json,math,time
def clean(x):
    return {r:F(v) for r,v in x.items() if v}


def plus(x, y):
    z = dict(x)
    for r,v in y.items():
        z[r] = z.get(r,F(0))+v
    return clean(z)


def neg(x):
    return {r:-v for r,v in x.items()}


def times(x, y):
    z = {}
    for r,a in x.items():
        for s,b in y.items():
            g = math.gcd(r,s)
            t = r*s//(g*g)
            z[t] = z.get(t,F(0))+g*a*b
    return clean(z)


def cadd(z, w):
    return (plus(z[0],w[0]),plus(z[1],w[1]))


def csub(z, w):
    return (plus(z[0],neg(w[0])),plus(z[1],neg(w[1])))


def cmul(z, w):
    return (plus(times(z[0],w[0]),neg(times(z[1],w[1]))),
            plus(times(z[0],w[1]),times(z[1],w[0])))


def squared(z, w):
    a,b = csub(z,w)
    return plus(times(a,a),times(b,b))


def point(a=0,b=0,c=0,d=0):
    return (clean({1:a,3:b}),clean({1:c,3:d}))


def key(z):
    return tuple(tuple(sorted(v.items())) for v in z)


UNIT={1:F(1)}
ZERO=({}, {})
ONE=point(1)
OMEGA=point(F(1,2),0,0,F(1,2))
ROOTS=[ONE]
for _ in range(5):ROOTS.append(cmul(ROOTS[-1],OMEGA))
CASES=[(m,n) for m in range(5) for n in range(5) if (m,n) not in [(0,0),(2,0),(0,2)]]
CROSS=[(0,2),(0,3),(1,2),(1,3)]

def sqrtfrac(q):
    if q==0:return {}
    if q<0:raise ValueError('negative square root')
    n=q.numerator*q.denominator;factor=1;rad=1;prime=2
    while prime*prime<=n:
        e=0
        while n%prime==0:n//=prime;e+=1
        factor*=prime**(e//2)
        if e%2:rad*=prime
        prime+=1
    return {rad*n:F(factor,q.denominator)}

def cscale(z,q):return (times(z[0],{1:q}),times(z[1],{1:q}))
def intersections(a,b):
    d=csub(b,a);q=squared(a,b)
    if any(r!=1 for r in q):raise ValueError('rational centres required')
    q=q.get(1,F(0))
    if q==0:raise ValueError('distinct centres required')
    if q>4:return []
    mid=cscale(cadd(a,b),F(1,2))
    if q==4:return [mid]
    factor=sqrtfrac((4-q)/(4*q))
    perp=(neg(d[1]),d[0])
    off=(times(perp[0],factor),times(perp[1],factor))
    return sorted([cadd(mid,off),csub(mid,off)],key=key)

def encode(z):
    return [[[r,q.numerator,q.denominator] for r,q in sorted(axis.items())] for axis in z]
def raw(data):return (json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(data):return hashlib.sha256(raw(data)).hexdigest()

def solve(lists,edges):
    adj=[set() for _ in lists]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    row={};nodes=0
    def dfs():
        nonlocal nodes
        nodes+=1
        if len(row)==len(lists):return [row[i] for i in range(len(lists))]
        options={v:[c for c in range(4) if lists[v]&(1<<c) and all(row.get(j)!=c for j in adj[v])] for v in range(len(lists)) if v not in row}
        v=min(options,key=lambda v:(len(options[v]),-len(adj[v]),v))
        for c in options[v]:
            row[v]=c
            answer=dfs()
            if answer is not None:return answer
            del row[v]
        return None
    answer=dfs()
    return answer,nodes

def build_case(m,n):
    t=point(F(m,2),0,F(n,2))
    D=[ZERO,ONE,t,cadd(t,ONE)]
    I=[intersections(D[a],D[b]) for a,b in CROSS]
    directions=[{key(r):r for r in ROOTS},{key(r):r for r in ROOTS}]
    for (a,b),points in zip(CROSS,I):
        for x in points:
            for group,centre in [(0,a),(1,b)]:
                u=csub(x,D[centre])
                for r in ROOTS:
                    z=cmul(u,r);directions[group][key(z)]=z
    ds=[sorted(v.values(),key=key) for v in directions]
    if set(map(key,ds[0]))!=set(map(key,ds[1])):raise ValueError('parallel direction identity')
    points={}
    for h,d in enumerate(D):
        for r in ds[h//2]:
            z=cadd(d,r);points[key(z)]=z
    V=sorted(points.values(),key=key);idx={key(z):i for i,z in enumerate(V)}
    centres=[idx[key(d)] for d in D]
    E=[(a,b) for a,b in combinations(range(len(V)),2) if squared(V[a],V[b])==UNIT]
    owners=[{h for h,d in enumerate(D) if squared(z,d)==UNIT} for z in V]
    masks=[]
    for i,own in enumerate(owners):
        if i in centres:allowed=1<<(2,3,0,1)[centres.index(i)]
        elif own and own<={0,1}:allowed=3
        elif own and own<={2,3}:allowed=12
        else:allowed=15
        if not own:raise ValueError('missing owner')
        masks.append(allowed)
    colour,nodes=solve(masks,E)
    if colour is None:raise ValueError(f'List condition failed at{m,n}; no full-support conclusion. Nodes={nodes}')
    return {'translation':[m,n],
            'cross_intersections':[[encode(z) for z in row] for row in I],
            'directions':[len(s) for s in ds],'vertices':len(V),'edges':len(E),
            'point_sha256':digest([encode(z) for z in V]),'edge_sha256':digest(E),
            'lists':''.join(format(a,'x') for a in masks),'colouring':''.join(map(str,colour)),
            'search_nodes':nodes}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--discover',action='store_true')
    args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=False)
    started=time.monotonic();cases=[]
    for m,n in CASES:
        case=build_case(m,n);cases.append(case)
        print(json.dumps({k:case[k] for k in ['translation','directions','vertices','edges','search_nodes']}),flush=True)
    data={'translation_denominator':2,'coordinate_encoding':'Each axis lists[positive squarefree radicand,numerator,positive denominator].','cases':cases}
    encoded=raw(data)
    if not args.discover and encoded!=(Path(__file__).parent/'certificate.json').read_bytes():raise ValueError('published bytes mismatch')
    out.joinpath('certificate.json').write_bytes(encoded)
    report={'status':'PASS','cases':len(cases),'certificate_bytes':len(encoded),'certificate_sha256':hashlib.sha256(encoded).hexdigest(),'seconds':time.monotonic()-started,'native_solver_calls':0}
    out.joinpath('build.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)
if __name__=='__main__':main()
