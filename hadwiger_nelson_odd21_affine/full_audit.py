"""Exact affine-metric screen of the Ardal et al. odd-distance spindle."""
from itertools import combinations
from collections import Counter
from math import gcd
from functools import reduce
import json, time, hashlib
from pathlib import Path

D = 85
BASE = [(0,0),(16,0),(6,0),(3,3),(13,3),(10,0),
        (5,5),(11,5),(7,3),(9,3),(8,2)]

def add(x,y): return (x[0]+y[0],x[1]+y[1])
def sub(x,y): return (x[0]-y[0],x[1]-y[1])
def mul(x,y): return (x[0]*y[0]+D*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def neg(x): return (-x[0],-x[1])
def sign(x):
    a,b=x
    if not b: return (a>0)-(a<0)
    if not a or (a>0)==(b>0): return (b>0)-(b<0)
    z=a*a-D*b*b
    return ((z>0)-(z<0))*((a>0)-(a<0))

def points():
    a=[((128*x,0),(128*y,0)) for x,y in BASE]
    b=[((127*x,-3*y),(127*y,x)) for x,y in BASE[1:]]
    p=a+b
    if len(set(p))!=21: raise ValueError('collision')
    return p

def rows(p):
    out={}
    for i,j in combinations(range(len(p)),2):
        x,y=(sub(p[i][k],p[j][k]) for k in (0,1))
        xy=mul(x,y)
        r=(mul(x,x),(2*xy[0],2*xy[1]),mul(y,y))
        out.setdefault(r,[]).append((i,j))
    return sorted(out.items())

def cross(a,b):
    return (sub(mul(a[1],b[2]),mul(a[2],b[1])),
            sub(mul(a[2],b[0]),mul(a[0],b[2])),
            sub(mul(a[0],b[1]),mul(a[1],b[0])))
def dot(a,b): return add(add(mul(a[0],b[0]),mul(a[1],b[1])),mul(a[2],b[2]))

def metric(a,b,c):
    # Solve r.q=1 using the cross product of row differences.
    n=cross(subrow(b,a),subrow(c,a)); d=dot(a,n)
    if d==(0,0): return None
    if sign(n[0])*sign(d)<=0: return False
    if sign(sub(mul(n[0],n[2]),mul(n[1],n[1])))<=0: return False
    # Canonical six integer numerators and positive shared denominator.
    nn=[mul(x,(d[0],-d[1])) for x in n]
    den=d[0]*d[0]-D*d[1]*d[1]
    nums=[a for pair in nn for a in pair]
    g=reduce(gcd,nums,abs(den))
    if den<0:g=-g
    return tuple(x//g for x in nums)+(den//g,)

def subrow(a,b):return tuple(sub(x,y) for x,y in zip(a,b))

def edges_at(key,rr):
    n=tuple((key[2*i],key[2*i+1]) for i in range(3))
    return sorted(e for r,es in rr if dot(r,n)==(key[6],0) for e in es)

def greedy4(n,edges):
    adj=[set() for _ in range(n)]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    left=set(range(n)); order=[]
    while left:
        v=min(left,key=lambda v:(len(adj[v]&left),v))
        if len(adj[v]&left)>=4: return None
        left.remove(v);order.append(v)
    col=[-1]*n
    for v in reversed(order):col[v]=min(set(range(4))-{col[u] for u in adj[v]})
    return ''.join(map(str,col))

def digest(x):
    return hashlib.sha256(json.dumps(x,separators=(",",":"),sort_keys=True).encode()).hexdigest()


def full_audit():
    p=points();rr=rows(p);counts=Counter();metrics=set()
    for a,b,c in combinations([r for r,es in rr],3):
        k=metric(a,b,c)
        if k is None:counts["singular_triples"]+=1
        elif k is False:counts["nonpositive_triples"]+=1
        else:counts["positive_triples"]+=1;metrics.add(k)
    hist=Counter();stars=[];max_degree=0
    opposite={v:[(a,b) for a,b in combinations([u for u in range(21) if u!=v],2)
                 if all(add(p[a][j],p[b][j])==add(p[v][j],p[v][j]) for j in (0,1))]
              for v in range(21)}
    for k in sorted(metrics):
        es=edges_at(k,rr);w=greedy4(21,es)
        if w is None:raise ValueError("nonempty 4-core")
        if any(w[u]==w[v] for u,v in es):raise ValueError("bad full-audit word")
        adj=[set() for _ in p]
        for u,v in es:adj[u].add(v);adj[v].add(u)
        md=max(map(len,adj));max_degree=max(max_degree,md)
        if md>4:raise ValueError("degree bound failed")
        if any(len(adj[v])-sum(a in adj[v] and b in adj[v] for a,b in opposite[v])>=3 for v in range(21)):
            stars.append(k)
        hist[len(es)]+=1
    local=json.loads(Path(__file__).with_name("expected.json").read_text())
    if len(stars)!=local["positive_metrics"] or digest(stars)!=local["metrics_sha256"]:
        raise ValueError("independent star-metric comparison failed")
    return {"verified":True,"distinct_difference_rows":len(rr),
            "global_triples":sum(counts.values()),"counts":dict(sorted(counts.items())),
            "positive_metrics":len(metrics),"metrics_sha256":digest(sorted(metrics)),
            "star_metrics":len(stars),"star_metrics_sha256":digest(stars),
            "edge_histogram":dict(sorted(hist.items())),"maximum_degree":max_degree,
            "all_global_cases_three_degenerate":True}


def main():
    result=full_audit()
    expected=json.loads(Path(__file__).with_name("full_expected.json").read_text())
    if json.loads(json.dumps(result))!=expected:raise ValueError("full expected mismatch")
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":main()
