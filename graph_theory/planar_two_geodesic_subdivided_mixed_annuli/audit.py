#!/usr/bin/env python3
"""Separate metric/component audit and a prior-art scope control.

Imports no research implementation. This is not independent peer review.
Run with assertions enabled, Python 3.11+ standard library.
"""
from itertools import combinations
import json
from pathlib import Path


def floyd(adj):
    n=len(adj);inf=sum(sum(row.values()) for row in adj)+1
    d=[[0 if u==v else adj[u].get(v,inf) for v in range(n)] for u in range(n)]
    for k in range(n):
        for u in range(n):
            for v in range(n):
                d[u][v]=min(d[u][v],d[u][k]+d[k][v])
    return d


def components(adj,removed):
    unseen=set(range(len(adj)))-set(removed);answer=[]
    while unseen:
        start=min(unseen);unseen.remove(start);part={start};todo=[start]
        while todo:
            fresh=(set(adj[todo.pop()])&unseen)
            unseen-=fresh;part|=fresh;todo.extend(fresh)
        answer.append(part)
    return answer


def pair_ring(t,lengths,scale,attachments):
    """Direct (AD)^t ring construction, separate from staircase code."""
    A=list(range(1,2*t+1));C=list(range(2*t+1,3*t+1))
    adj=[{} for _ in range(3*t+1)]
    def edge(a,b,w):
        assert a!=b and b not in adj[a]
        adj[a][b]=adj[b][a]=w
    for i,a in enumerate(A):
        edge(0,a,scale);edge(a,A[(i+1)%(2*t)],scale)
    arcs=[]
    for j,c in enumerate(C):
        edge(c,A[2*j],scale);edge(c,A[2*j+1],scale)
        arc=[c]
        for _ in range(lengths[j]-1):
            arc.append(len(adj));adj.append({})
        arc.append(C[(j+1)%t])
        for u,v in zip(arc,arc[1:]):edge(u,v,scale)
        arcs.append(arc)
    core=set(range(len(adj)));pieces=[]
    if attachments:
        for i,a in enumerate(A):
            z=len(adj);adj.append({});pieces.append({z})
            for v in [0,a,A[(i+1)%(2*t)]]:edge(z,v,1)
    return adj,A,C,arcs,core,pieces


def check_path(adj,dist,path):
    assert len(path)==len(set(path))
    cost=sum(adj[u][v] for u,v in zip(path,path[1:]))
    assert cost==dist[path[0]][path[-1]]


geometries=0
for t in [3,4,5,7]:
    for n in range(2,13):
        for scale in [1,2]:
            sizes=[n]+[1+j%5 for j in range(1,t)]
            sizes[-1]=2
            adj,A,C,arcs,core,pieces=pair_ring(t,sizes,scale,True)
            dist=floyd(adj);original=floyd([{v:w for v,w in adj[u].items() if v in core} for u in sorted(core)])
            assert all(dist[u][v]==original[u][v] for u in core for v in core)
            a0,b0,a,b=A[:4];arc=arcs[0]
            assert dist[a0][C[1]]==3*scale and dist[b0][C[-1]]==3*scale
            p=(n+1)//2;q=(n+3)//2
            U=[a0,0,b]+list(reversed(arc[q:]))
            V=[b0]+arc[:p+1]
            for path in [U,V]:check_path(adj,dist,path)
            removed=set(U)|set(V)
            assert {0,a0,C[0]}|set(arc)<=removed
            S={a}|pieces[1]|pieces[2]
            assert S in components(adj,{0,C[1],b0,b})
            # Exact new-right support after the singleton A-step.
            L=pieces[0]|{b0}|pieces[1]|{a}|pieces[2]|set(arc[1:-1])
            M=set(range(len(adj)))-{0,a0,C[0]}
            R=M-L-{b,C[1]}
            for K in components(adj,removed):
                if K&core:assert K<=S or K<=R
                else:assert K in pieces
            old_left=pieces[0]|{b0}|pieces[1]|set(arc[1:-1])
            old_right=M-old_left-{a,C[1]}
            assert old_right&S==pieces[2]
            assert M-(old_right|S)==pieces[0]|{b0,C[1]}|set(arc[1:-1])
            geometries+=1


# The old literal control is reused as an included member, not rediscovered.
control=json.loads((Path(__file__).parent.parent/
                   'planar_two_geodesic_selected_spoke_annuli/control.json').read_text())
adj,A,C,arcs,core,pieces=pair_ring(5,[1]*5,1,False)
faces=[(0,A[i],A[(i+1)%10]) for i in range(10)]
for j,c in enumerate(C):
    a,b=A[2*j:2*j+2];d=C[(j+1)%5];nxt=A[(2*j+2)%10]
    faces.extend([(a,c,b),(b,c,d,nxt)])
faces.append(tuple(reversed(C)))
assert min(len(adj[v]) for v in core)==4
for triple in control['stack_faces']:
    face=next(f for f in faces if len(f)==3 and set(f)==set(triple))
    faces.remove(face);z=len(adj);adj.append({})
    for v in face:adj[v][z]=adj[z][v]=1
    faces.extend((face[i],face[(i+1)%3],z) for i in range(3))
n=len(adj);edges=sum(map(len,adj))//2
darts=[(f[i],f[(i+1)%len(f)]) for f in faces for i in range(len(f))]
assert len(darts)==len(set(darts))==2*edges
assert set(darts)=={(u,v) for u,row in enumerate(adj) for v in row}
assert n-edges+len(faces)==2
for v in range(n):
    rotation={}
    for f in faces:
        if v in f:
            i=f.index(v);rotation[f[i-1]]=f[(i+1)%len(f)]
    start=min(adj[v]);seen=set();u=start
    while u not in seen:seen.add(u);u=rotation[u]
    assert u==start and seen==set(adj[v])
connectivity_checks=0
for size in range(3):
    for cut in combinations(range(n),size):
        assert len(components(adj,cut))==1
        connectivity_checks+=1
weights=[0]*n
for v,w in control['positive_weights']:weights[v]=w
assert sum(weights)==37
facial_scores=[max(sum(weights[v] for v in K) for K in components(adj,f)) for f in faces]
assert all(2*score>sum(weights) for score in facial_scores)
assert n==52 and edges==143 and len(faces)==93
print(f'geometries={geometries} three_connectivity_checks={connectivity_checks} '
      f'faces={len(faces)} minimum_facial_residual={min(facial_scores)} '
      f'total_mass={sum(weights)} core_minimum_degree=4 PASS')
