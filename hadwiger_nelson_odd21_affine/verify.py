"""Separate star enumeration with rational quadratic-field elimination."""
from fractions import Fraction as F
from itertools import combinations
from math import lcm,gcd
from functools import reduce
from collections import Counter
from pathlib import Path
import json,time,hashlib

ZERO=(F(0),F(0));ONE=(F(1),F(0))
def plus(x,y):return (x[0]+y[0],x[1]+y[1])
def minus(x,y):return (x[0]-y[0],x[1]-y[1])
def times(x,y):return (x[0]*y[0]+85*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def divide(x,y):
    d=y[0]*y[0]-85*y[1]*y[1]
    z=times(x,(y[0],-y[1]));return (z[0]/d,z[1]/d)
def positive(x):
    a,b=x
    if b==0:return a>0
    if a==0:return b>0
    if a>0:return b>0 or a*a>85*b*b
    return b>0 and 85*b*b>a*a

def points():
    lattice=[(0,0),(8,0),(3,0),(0,3),(5,3),(5,0),
             (0,5),(3,5),(2,3),(3,3),(3,2)]
    half=[((F(256*n+128*m),F(0)),(F(128*m),F(0))) for n,m in lattice]
    c=(F(127,128),F(0));s=(F(0),F(1,128))
    return half+[(minus(times(c,x),times((F(0),F(3,128)),y)),plus(times(s,x),times(c,y))) for x,y in half[1:]]

def row(p,q):
    x,y=(minus(p[k],q[k]) for k in range(2));xy=times(x,y)
    return (times(x,x),plus(xy,xy),times(y,y))

def gaussian(rows):
    a=[list(r)+[ONE] for r in rows]
    for k in range(3):
        t=next((t for t in range(k,3) if a[t][k]!=ZERO),None)
        if t is None:return None
        a[k],a[t]=a[t],a[k]
        d=a[k][k];a[k]=[divide(x,d) for x in a[k]]
        for t in range(3):
            if t==k:continue
            d=a[t][k];a[t]=[minus(x,times(d,y)) for x,y in zip(a[t],a[k])]
    return tuple(a[k][3] for k in range(3))

def canonical(q):
    f=[z for x in q for z in x]; d=lcm(*(z.denominator for z in f))
    nums=[int(z*d) for z in f];g=reduce(gcd,nums,d)
    return tuple(x//g for x in nums)+(d//g,)

def edges(k,rr):
    # Integer expression expansion instead of Fraction dot products.
    q=[(k[2*i],k[2*i+1]) for i in range(3)];out=[]
    for ij,r in rr.items():
        a=sum(int(x[0])*y[0]+85*int(x[1])*y[1] for x,y in zip(r,q))
        b=sum(int(x[0])*y[1]+int(x[1])*y[0] for x,y in zip(r,q))
        if a==k[6] and b==0:out.append(ij)
    return out

def peel(n,es):
    a=[set() for _ in range(n)]
    for i,j in es:a[i].add(j);a[j].add(i)
    left=set(range(n));stack=[]
    while left:
        v=next((v for v in sorted(left) if len(a[v]&left)<4),None)
        if v is None:return None
        left.remove(v);stack.append(v)
    colours=[-1]*n
    for v in reversed(stack):
        colours[v]=next(c for c in range(4) if all(colours[w]!=c for w in a[v]))
    if any(colours[u]==colours[v] for u,v in es):raise ValueError('bad word')
    return colours

def digest(x):
    return hashlib.sha256(json.dumps(x,separators=(",",":"),sort_keys=True).encode()).hexdigest()


def verify():
    p=points()
    if len(set(p))!=21:raise ValueError("source collision")
    rr={(i,j):row(p[i],p[j]) for i,j in combinations(range(21),2)}
    if any(z.denominator!=1 for r in rr.values() for x in r for z in x):
        raise ValueError("nonintegral row in integer edge reconstruction")
    metrics=set();counts=Counter()
    for v in range(21):
        neighbours=[w for w in range(21) if w!=v]
        for ns in combinations(neighbours,3):
            rs=[rr[tuple(sorted((v,w)))] for w in ns]
            q=gaussian(rs)
            if q is None:counts["singular_triples"]+=1;continue
            for r in rs:
                z=ZERO
                for a,b in zip(r,q):z=plus(z,times(a,b))
                if z!=ONE:raise ValueError("linear solution residual")
            if not positive(q[0]) or not positive(minus(times(q[0],q[2]),times(q[1],q[1]))):
                counts["nonpositive_triples"]+=1;continue
            counts["positive_triples"]+=1;metrics.add(canonical(q))
    degree_hist=Counter();edge_hist=Counter();stream=hashlib.sha256()
    for k in sorted(metrics):
        es=edges(k,rr);d=Counter(x for e in es for x in e)
        md=max(d.values(),default=0)
        if md>4:raise ValueError("five points on a centred ellipse")
        word=peel(21,es)
        if word is None:raise ValueError("nonempty 4-core")
        degree_hist[md]+=1;edge_hist[len(es)]+=1
        stream.update((json.dumps([k,es,word],separators=(",",":"))+"\n").encode())
    return {"verified":True,"source_vertices":21,"star_triples":23940,
            "counts":dict(sorted(counts.items())),"positive_metrics":len(metrics),
            "metrics_sha256":digest(sorted(metrics)),
            "metric_edge_word_stream_sha256":stream.hexdigest(),
            "maximum_degree_histogram":dict(sorted(degree_hist.items())),
            "edge_histogram":dict(sorted(edge_hist.items())),
            "all_star_cases_three_degenerate":True,"affine_family_four_colourable":True}


def main():
    result=verify()
    expected=json.loads(Path(__file__).with_name("expected.json").read_text())
    if json.loads(json.dumps(result))!=expected:raise ValueError("expected result mismatch")
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":main()
