#!/usr/bin/env python3
"""Independent direct CNF generator for adding three vertices to a 40-core."""

import argparse,itertools
from pathlib import Path


def decode(s):
    vals=[ord(c)-63 for c in s.strip()];n=vals[0];bits=[]
    for x in vals[1:]:bits.extend((x>>b)&1 for b in range(5,-1,-1))
    a=[[False]*n for _ in range(n)];at=0
    for j in range(1,n):
        for i in range(j):a[i][j]=a[j][i]=bool(bits[at]);at+=1
    return a


def homogeneous(a,size,value):
    for ss in itertools.combinations(range(len(a)),size):
        if all(a[u][v]==value for u,v in itertools.combinations(ss,2)):yield ss


def main():
    p=argparse.ArgumentParser();p.add_argument('cores');p.add_argument('index',type=int);p.add_argument('output');args=p.parse_args()
    lines=Path(args.cores).read_text().splitlines();a=decode(lines[args.index]);n=len(a)
    if n!=40:raise ValueError('core order is not 40')
    if next(homogeneous(a,5,True),None)or next(homogeneous(a,5,False),None):raise ValueError('core has a homogeneous 5-set')
    def x(q,v):return 1+q*n+v
    ep={(0,1):121,(0,2):122,(1,2):123};c=[]
    k4=list(homogeneous(a,4,True));i4=list(homogeneous(a,4,False))
    k3=list(homogeneous(a,3,True));i3=list(homogeneous(a,3,False))
    k2=list(homogeneous(a,2,True));i2=list(homogeneous(a,2,False))
    for q in range(3):
        for ss in k4:c.append(tuple(-x(q,v) for v in ss))
        for ss in i4:c.append(tuple(x(q,v) for v in ss))
    for q,r in ep:
        e=ep[q,r]
        for ss in k3:c.append((-e,)+tuple(-x(q,v) for v in ss)+tuple(-x(r,v) for v in ss))
        for ss in i3:c.append((e,)+tuple(x(q,v) for v in ss)+tuple(x(r,v) for v in ss))
    for i,j in k2:c.append((-121,-122,-123)+tuple(-x(q,v) for q in range(3) for v in (i,j)))
    for i,j in i2:c.append((121,122,123)+tuple(x(q,v) for q in range(3) for v in (i,j)))
    with open(args.output,'w') as f:
        f.write(f'p cnf 123 {len(c)}\n')
        for clause in c:f.write(' '.join(map(str,clause))+' 0\n')
    print(f'index={args.index} k4={len(k4)} i4={len(i4)} k3={len(k3)} i3={len(i3)} k2={len(k2)} i2={len(i2)} clauses={len(c)}')


if __name__=='__main__':main()
