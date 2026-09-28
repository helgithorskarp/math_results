#!/usr/bin/env python3
"""Separate control audit: literal input, Floyd--Warshall, and geodesic-set DP.
Imports no research implementation. This is not independent peer review.
"""
from functools import cache
import json
from pathlib import Path

x=json.loads((Path(__file__).parent/'control.json').read_text())
assert x['block_sizes']==[2]*5
A=list(range(1,11));C=list(range(11,16));adj=[set() for _ in range(16)];faces=[]
def edge(u,v):adj[u].add(v);adj[v].add(u)
for i,a in enumerate(A):
    b=A[(i+1)%10];edge(0,a);edge(a,b);faces.append((0,a,b))
for j,c in enumerate(C):
    a,b=A[2*j:2*j+2];d=C[(j+1)%5];nxt=A[(2*j+2)%10]
    edge(c,d);edge(a,c);edge(b,c);faces.extend([(a,c,b),(b,c,d,nxt)])
faces.append(tuple(reversed(C)))
original=[set(row) for row in adj]
for triple in x['stack_faces']:
    f=next(f for f in faces if len(f)==3 and set(f)==set(triple))
    assert all(v in adj[u] for u in triple for v in triple if u!=v)
    faces.remove(f);v=len(adj);adj.append(set())
    for u in triple:edge(u,v)
    faces.extend((f[i],f[(i+1)%3],v) for i in range(3))
n=len(adj);E=sum(map(len,adj))//2
# An insertion strictly inside an existing triangular face preserves a planar
# embedding. The supplied faces also account for every directed edge once.
darts=[(f[i],f[(i+1)%len(f)]) for f in faces for i in range(len(f))]
assert len(darts)==len(set(darts))==2*E and set(darts)=={(u,v) for u in range(n) for v in adj[u]}
assert n-E+len(faces)==2

def floyd(graph):
    size=len(graph);d=[[0 if i==j else 1 if j in graph[i] else size+1 for j in range(size)] for i in range(size)]
    for k in range(size):
        for i in range(size):
            for j in range(size):d[i][j]=min(d[i][j],d[i][k]+d[k][j])
    return d
D=floyd(adj);D0=floyd(original)
assert all(D[i][j]==D0[i][j] for i in range(16) for j in range(16))
N=(1<<n)-1;neighbors=[sum(1<<v for v in row) for row in adj]

def components(mask):
    answer=[]
    while mask:
        first=mask&-mask;part=frontier=first;mask^=first
        while frontier:
            bit=frontier&-frontier;frontier^=bit
            new=neighbors[bit.bit_length()-1]&mask
            mask^=new;part|=new;frontier|=new
        answer.append(part)
    return answer
outside=components(N^((1<<16)-1))
assert sorted(K.bit_count() for K in outside)==[12,12,12]
# Reverse insertion is a width-three elimination certificate, with each
# root-clique boundary retained to the end.
for K in outside:
    vertices=[v for v in range(n) if K>>v&1]
    boundary=set().union(*(adj[v] for v in vertices))-set(vertices)
    assert 0 in boundary and len(boundary)==3
    kept=set(vertices)|boundary
    for v in sorted(vertices,reverse=True):
        nbr=adj[v]&kept
        assert len(nbr)<=3 and all(b in adj[a] for a in nbr for b in nbr if a!=b)
        kept.remove(v)
w=[0]*n
for v,value in x['positive_weights']:w[v]=value
@cache
def mass(mask):return sum(w[v] for v in range(n) if mask>>v&1)
assert sum(w)==37 and sorted(mass(K) for K in outside)==[9,14,14]

@cache
def geodesic_sets(s,t):
    if s==t:return frozenset([1<<s])
    return frozenset((1<<s)|mask for v in adj[s] if D[v][t]+1==D[s][t] for mask in geodesic_sets(v,t))
paths=set().union(*(geodesic_sets(s,t) for s in range(n) for t in range(s,n)))
def check_path(path):
    assert len(set(path))==len(path) and all(v in adj[u] for u,v in zip(path,path[1:]))
    assert D[path[0]][path[-1]]==len(path)-1
    return sum(1<<v for v in path)
P=check_path(x['prescribed_path'])
optimum=min(max(map(mass,components(N&~(P|Q))),default=0) for Q in paths)
attain=check_path([10,9,8,34])
assert max(map(mass,components(N&~(P|attain))),default=0)==optimum==19
free=0
for path in x['free_paths']:free|=check_path(path)
free_mass=max(map(mass,components(N&~free)),default=0)
assert free_mass==14 and len(paths)==3489
print(f'vertices={n} edges={E} geodesic_sets={len(paths)} total_mass={sum(w)} attachment_masses=9,14,14 fixed_optimum={optimum} free_largest={free_mass} PASS')
