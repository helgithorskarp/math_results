"""Exact finite encoding of the full-middle-third reflected-fibre family.

Only the Python standard library is used. The full mathematical reduction and
sound palette normalizations are described in README.md. No axis coordinate
is fixed, and no asymmetry condition is imposed.
"""
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


ELABELS=(0,1,3,4,5)
QLABELS=(0,3,4,5)


def encoding(a,symmetry=True):
    if a<7 or a%2==0 or math.gcd(a,15)!=1:raise ValueError('unsupported CRT modulus')
    h=(a-1)//2;m=(a-1)//3;top=0;E={};Q={};P={};cnf=[]
    def fresh():
        nonlocal top
        top+=1;return top
    def onehot(values):
        cnf.append(list(values));cnf.extend([[-u,-v] for u,v in itertools.combinations(values,2)])
    for u in range(1,h+1):
        for c in ELABELS:E[u,c]=fresh()
        onehot([E[u,c] for c in ELABELS])
    positions=sorted([*range(1,m+1),*range(a-m,a)])
    for x in positions:
        for c in QLABELS:Q[x,c]=fresh()
        onehot([Q[x,c] for c in QLABELS])
    for edge in axis_edges(a):
        for c in ELABELS:cnf.append([-E[u,c] for u in edge])
    for u in range(1,m+1):
        for c in (3,4,5):
            P[u,c]=fresh();p=P[u,c]
            cnf.extend([[-Q[u,c],p],[-Q[a-u,c],p],[-p,Q[u,c],Q[a-u,c]]])
    for x in range(1,m+1):
        for y in range(x,m-x+1):
            for c in (3,4,5):cnf.append(sorted({-P[x,c],-P[y,c],-P[x+y,c]}))
    for x,y in itertools.combinations([0,*positions],2):
        d=(y-x)%a;u=min(d,a-d)
        r=[-Q[z,0] for z in (x,y) if z]
        for c in (0,1):cnf.append([*r,-E[u,c]])
        if x and y:
            for c in (3,4,5):cnf.append([-Q[x,c],-Q[y,c],-E[u,c]])
    if symmetry:
        seen={3:[],4:[],5:[]}
        for u in range(1,h+1):
            nodes=([('q',u),('q',a-u)] if u<=m else [])+[('e',u)]
            for kind,x in nodes:
                table=Q if kind=='q' else E
                for c in (4,5):cnf.append([-table[x,c],*seen[c-1]])
                for c in (3,4,5):seen[c].append(table[x,c])
        for u in range(1,h+1):cnf.append([-E[u,1]]+[E[v,0] for v in range(1,u)])
    return dict(a=a,m=m,h=h,E=E,Q=Q,P=P,positions=positions,variables=top,
                symmetry_breaking=symmetry),cnf


def dimacs(a=109):
    metadata, clauses = encoding(a)
    header = f"p cnf {metadata['variables']} {len(clauses)}\n"
    body = "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return (header + body).encode("ascii")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--axis-factor", type=int, default=109)
    args = parser.parse_args()
    args.output.write_bytes(dimacs(args.axis_factor))
