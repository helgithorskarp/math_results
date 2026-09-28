"""Exact reflected product model; no axis coordinate is normalized."""
import argparse
import itertools
import math
from pathlib import Path


def axis_edges(a):
    edges=set()
    for x in range(1,a):
        for y in range(x,a):
            z=(x+y)%a
            if z:
                edges.add(tuple(sorted({min(s,a-s) for s in (x,y,z)})))
    return tuple(sorted(edges))


def encoding(a,p=7,symmetry=True):
    if a<3 or a%2!=1 or p not in (5,7,11) or math.gcd(a,p)!=1:
        raise ValueError('unsupported CRT factors')
    t=(p-1)//2;h=(a-1)//2;common=tuple(range(t,6));qlabels=(0,*common)
    E={};Q={};P={};top=0;cnf=[]
    def fresh():
        nonlocal top
        top+=1;return top
    def onehot(values):
        cnf.append(values);cnf.extend([[-u,-v] for u,v in itertools.combinations(values,2)])
    for u in range(1,h+1):
        for c in range(6):E[u,c]=fresh()
        onehot([E[u,c] for c in range(6)])
    for x in range(1,a):
        for c in qlabels:Q[x,c]=fresh()
        onehot([Q[x,c] for c in qlabels])
    for u in range(1,h+1):
        for c in common:
            P[u,c]=fresh();v=P[u,c]
            cnf.extend([[-Q[u,c],v],[-Q[a-u,c],v],[-v,Q[u,c],Q[a-u,c]]])
    for edge in axis_edges(a):
        for c in range(6):cnf.append([-E[u,c] for u in edge])
        for c in common:cnf.append([-P[u,c] for u in edge])
    for x,y in itertools.combinations(range(a),2):
        d=(y-x)%a;u=min(d,a-d)
        r=[-Q[z,0] for z in (x,y) if z]
        for c in range(t):cnf.append([*r,-E[u,c]])
        if x:
            for c in common:cnf.append([-Q[x,c],-Q[y,c],-E[u,c]])
    if symmetry:
        seen={c:[] for c in common}
        for u in range(1,h+1):
            for table,x in ((Q,u),(Q,a-u),(E,u)):
                for c in common[1:]:cnf.append([-table[x,c],*seen[c-1]])
                for c in common:seen[c].append(table[x,c])
        for u in range(1,h+1):
            for c in range(1,t):cnf.append([-E[u,c]]+[E[v,c-1] for v in range(1,u)])
    return dict(a=a,p=p,t=t,h=h,common=common,qlabels=qlabels,E=E,Q=Q,P=P,
                variables=top,symmetry=symmetry),cnf



def dimacs(a=79,p=7):
    metadata,clauses=encoding(a,p)
    header=f"p cnf {metadata['variables']} {len(clauses)}\n"
    body="".join(" ".join(map(str,clause))+" 0\n" for clause in clauses)
    return (header+body).encode("ascii")


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("output",type=Path)
    parser.add_argument("--axis-factor",type=int,default=79)
    args=parser.parse_args();args.output.write_bytes(dimacs(args.axis_factor))
