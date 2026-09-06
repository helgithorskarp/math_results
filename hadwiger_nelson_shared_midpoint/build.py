"""Construct all antipodal-transversal colourings of the fixed midpoint kernel."""
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

def orbit(u):
    candidates=[cmul(u,z) for z in ROOTS]
    rep=min(candidates,key=key)
    k=next(k for k,z in enumerate(ROOTS) if key(cmul(rep,z))==key(u))
    return key(rep),k

def build():
    r=point(F(3,5),0,F(4,5));t=point(F(1,5),0,F(-2,5))
    D=[ZERO,ONE,t,cadd(t,r)]
    I=[intersections(D[a],D[b]) for a,b in CROSS]
    S=[{key(u):u for u in ROOTS},{key(cmul(u,r)):cmul(u,r) for u in ROOTS}]
    for (a,b),row in zip(CROSS,I):
        for x in row:
            for group,h in [(0,a),(1,b)]:
                for root in ROOTS:
                    z=cmul(csub(x,D[h]),root);S[group][key(z)]=z
    points={}
    for h,d in enumerate(D):
        for u in S[h//2].values():
            z=cadd(d,u);points[key(z)]=z
    V=sorted(points.values(),key=key);idx={key(z):i for i,z in enumerate(V)}
    ci=[idx[key(d)] for d in D]
    E=[(a,b) for a,b in combinations(range(len(V)),2) if squared(V[a],V[b])==UNIT]
    owners=[{h for h,d in enumerate(D) if squared(z,d)==UNIT} for z in V]
    mixed=sorted({idx[key(z)] for row in I for z in row})
    pairs=sorted({tuple(sorted((i,idx[key(csub(ONE,V[i]))]))) for i in mixed})
    if len(mixed)!=8 or len(pairs)!=4:raise ValueError('antipodal cross intersections')
    masks=[1<<(2,3,0,1)[ci.index(i)] if i in ci else 3 if own<={0,1} else 12 if own<={2,3} else 15 for i,own in enumerate(owners)]
    rows=[]
    for mask in range(16):
        selected={p[(mask>>j)&1] for j,p in enumerate(pairs)}
        phases=[{},{}]
        for v in mixed:
            own=owners[v];a=next(i for i in own if i<2);b=next(i for i in own if i>=2)-2
            g=0 if v in selected else 1
            h=a if g==0 else b+2
            rep,k=orbit(csub(V[v],D[h]))
            wanted=1-b if g==0 else 1-a
            alpha=(wanted+(h%2)+k)%2
            if rep in phases[g] and phases[g][rep]!=alpha:raise ValueError('phase conflict')
            phases[g][rep]=alpha
        if any(len(v)!=4 for v in phases):raise ValueError('one selected constraint per cross orbit')
        colouring=[]
        for v,z in enumerate(V):
            if v in ci:c=(2,3,0,1)[ci.index(v)]
            else:
                own=owners[v]
                g=(0 if v in selected else 1) if v in mixed else (0 if own<={0,1} else 1)
                h=next(h for h in sorted(own) if h//2==g)
                rep,k=orbit(csub(z,D[h]))
                c=2*g+(phases[g].get(rep,0)+h%2+k)%2
            colouring.append(c)
        if not all(masks[i]&(1<<c) for i,c in enumerate(colouring)):raise ValueError('list colouring')
        if not all(colouring[a]!=colouring[b] for a,b in E):raise ValueError('unit edge')
        rows.append({'transversal_mask':mask,'colouring':''.join(map(str,colouring))})
    return {'schema':1,'orientation':[[3,5],[4,5]],'translation':[[1,5],[-2,5]],
            'cross_intersections':[[encode(z) for z in row] for row in I],
            'directions':[len(s) for s in S],'vertices':len(V),'edges':len(E),
            'centres':ci,'cross_pairs':pairs,'point_sha256':digest([encode(z) for z in V]),'edge_sha256':digest(E),
            'lists':''.join(format(a,'x') for a in masks),'colourings':rows,'sharp_kernel_bound':108,'target_found':False}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--discover',action='store_true');args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    data=build();blob=raw(data)
    if not args.discover and blob!=(Path(__file__).parent/'certificate.json').read_bytes():raise ValueError('certificate bytes differ')
    out.joinpath('certificate.json').write_bytes(blob)
    r={'status':'PASS','vertices':data['vertices'],'edges':data['edges'],'colourings':len(data['colourings']),
       'certificate_bytes':len(blob),'certificate_sha256':hashlib.sha256(blob).hexdigest(),
       'seconds':time.monotonic()-start,'native_solver_calls':0,'constructive':True}
    out.joinpath('build.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
