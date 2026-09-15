#!/usr/bin/env python3
"""Regenerate the small certificate using flat radical arithmetic and DSATUR.

This program does not import the verifier; geometry uses rational vectors in
1,sqrt3,sqrt11,sqrt33 separately for each Cartesian coordinate.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations
import argparse,json
BASE=Path(__file__).resolve().parent
Z=(Q(0),)*4;O=(Q(1),Q(0),Q(0),Q(0));S=(Q(0),Q(1),Q(0),Q(0));T=(Q(0),Q(0),Q(1),Q(0))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(a,s):return tuple(x*s for x in a)
def sub(a,b):return add(a,scale(b,-1))
def mul(a,b):
    r=[Q(0)]*4
    for i,x in enumerate(a):
        for j,y in enumerate(b):r[i^j]+=x*y*(3 if i&j&1 else 1)*(11 if i&j&2 else 1)
    return tuple(r)
def padd(a,b):return add(a[0],b[0]),add(a[1],b[1])
def psub(a,b):return sub(a[0],b[0]),sub(a[1],b[1])
def pmul(a,b):return sub(mul(a[0],b[0]),mul(a[1],b[1])),add(mul(a[0],b[1]),mul(a[1],b[0]))
def norm(a):return add(mul(a[0],a[0]),mul(a[1],a[1]))
def geometry():
    rho=(scale(O,Q(1,2)),scale(S,Q(1,2)));w=pmul(rho,rho)
    g=[(Z,Z),(O,Z)]
    for j in range(5):g.append(pmul(g[-1],rho))
    q=(scale(O,Q(1,6)),scale(T,Q(1,6)))
    g+=[q,pmul(w,q),pmul(pmul(w,w),q)]
    rows=[list(map(int,l.split()))[1:] for l in (BASE/'f29.tsv').read_text().splitlines() if l and not l.startswith('#')]
    f=[((Q(a,12),Q(0),Q(0),Q(b,12)),(Q(0),Q(c,12),Q(d,12),Q(0))) for a,b,c,d in rows]
    unit=psub(g[8],g[7]);f=[padd(g[7],pmul(unit,z)) for z in f]
    p=list(g)
    for z in f:
        if z not in p:p.append(z)
    e=[(a,b) for a,b in combinations(range(len(p)),2) if norm(psub(p[a],p[b]))==O]
    compact=[]
    for x,y in p:
        if x[1] or x[2] or y[0] or y[3]:raise ValueError('coordinate field')
        v=[144*t for t in (x[0],x[3],y[1],y[2])]
        if any(t.denominator!=1 for t in v):raise ValueError('denominator')
        compact.append([int(t) for t in v])
    return compact,e

def solve(n,edges,pins,enumerate_all=False):
    adj=[set() for _ in range(n)]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    c=[-1]*n
    for v,x in pins.items():c[v]=x
    if any(c[a]>=0 and c[a]==c[b] for a,b in edges):return []
    out=[]
    def walk():
        left=[v for v in range(n) if c[v]<0]
        if not left:out.append(tuple(c));return not enumerate_all
        banned={v:{c[u] for u in adj[v] if c[u]>=0} for v in left}
        v=max(left,key=lambda x:(len(banned[x]),len(adj[x]),-x))
        for x in range(4):
            if x not in banned[v]:
                c[v]=x
                if walk():return True
        c[v]=-1;return False
    walk();return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args()
    p,e=geometry();ge=[x for x in e if x[1]<10]
    source=sorted(solve(10,ge,{0:0,1:1,2:2},True));words=[]
    for w in source:
        ext=solve(len(p),e,dict(enumerate(w)))
        if not ext:raise ValueError('complete input word fails: '+str(w))
        words.append(''.join(map(str,ext[0])))
    result={'points144':p,'edges':e,'extensions':words,'proper_four':words[0],'proper_five':'4'+words[0][1:]}
    text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')
if __name__=='__main__':main()
