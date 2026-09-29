"""Separate audit: whole-graph Floyd and internally disjoint path flows.

Imports no generator or target checker. The compact certificate is an
untrusted data input. Uses only Python's standard library.
"""
from collections import deque
from itertools import combinations
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent


def parts(adj,removed):
    left=set(range(len(adj)))-set(removed);out=[]
    while left:
        s=min(left);left.remove(s);C={s};todo=deque([s])
        while todo:
            u=todo.popleft();new=adj[u]&left;left-=new;C|=new;todo.extend(new)
        out.append(C)
    return out


def five_paths(adj,s,t):
    n=len(adj);cap={}
    def edge(u,v,c):cap[u,v]=cap.get((u,v),0)+c;cap.setdefault((v,u),0)
    for v in range(n):edge(2*v,2*v+1,5 if v in (s,t) else 1)
    for u in range(n):
        for v in adj[u]:edge(2*u+1,2*v,5)
    neighbors=[set() for _ in range(2*n)]
    for u,v in cap:neighbors[u].add(v)
    source,sink=2*s+1,2*t;flow=0
    while flow<5:
        parent={source:None};todo=deque([source])
        while todo and sink not in parent:
            u=todo.popleft()
            for v in sorted(neighbors[u]):
                if cap[u,v]>0 and v not in parent:parent[v]=u;todo.append(v)
        assert sink in parent,('fewer than five internally disjoint paths',s,t)
        v=sink
        while v!=source:u=parent[v];cap[u,v]-=1;cap[v,u]+=1;v=u
        flow+=1
    return flow


def run():
    raw=(HERE/'certificate.json').read_bytes();c=json.loads(raw);n=32
    centers={(u,v):w for u,v,w in c['edge_centers']};adj=[set() for _ in range(n)]
    assert len(centers)==90
    for u,v in centers:assert 0<=u<v<n;adj[u].add(v);adj[v].add(u)
    # Directly validate the base cubic graph and the twelve pentagonal
    # neighborhoods, without using the target's triangle/rotation code.
    for v in range(20):assert len(adj[v]&set(range(20)))==3
    assert all(len(adj[v])==6 for v in range(20)) and all(len(adj[v])==5 for v in range(20,32))
    for z,F in enumerate(c['pentagons'],20):
        assert adj[z]==set(F) and all(v in adj[u] for u,v in zip(F,F[1:]+F[:1]))
    assert len(parts(adj,()))==1
    connectivity=0
    for s,t in combinations(range(n),2):
        if t in adj[s]:continue
        assert five_paths(adj,s,t)==5;connectivity+=1
    assert connectivity==406
    radius=c['radius'];assert radius==1
    distances=[]
    for pair in c['pairs']:
        for P in pair:
            assert P and len(P)==len(set(P)) and all(v in adj[u] for u,v in zip(P,P[1:]))
            selected={tuple(sorted(e)) for e in zip(P,P[1:])}
            cost={e:w+(radius if e in selected else -radius) for e,w in centers.items()}
            inf=sum(cost.values())+1;d=[[0 if u==v else inf for v in range(n)] for u in range(n)]
            for (u,v),w in cost.items():assert w>0;d[u][v]=d[v][u]=w
            for k in range(n):
                for u in range(n):
                    for v in range(n):d[u][v]=min(d[u][v],d[u][k]+d[k][v])
            length=sum(cost[e] for e in selected);assert length==d[P[0]][P[-1]];distances.append(length)
    components=[parts(adj,set(P)|set(Q)) for P,Q in c['pairs']]
    large=[[C for C in row if len(C)>4] for row in components]
    assert list(map(len,large))==[1,1,2]
    A,B=large[0][0],large[1][0]
    assert all(C.isdisjoint(A) or C.isdisjoint(B) for C in large[2])
    # The prescribed menu alone is not an all-mass theorem: vertex 1 is
    # absent from all six paths. The universal four-heavy-vertex repair
    # is a necessary case of the stated proof.
    assert all(1 not in P for pair in c['pairs'] for P in pair)
    assert all(any(1 in C for C in row) for row in components)
    # A radius just above the certified one is not asserted either safe
    # or unsafe; no optimization result or sharpness claim is used here.
    return {'status':'PASS','nonadjacent_pairs_with_five_internal_paths':connectivity,
            'adverse_corner_floyd_checks':6,'adverse_corner_path_lengths':distances,
            'residual_component_orders':[sorted(map(len,row)) for row in components],
            'prescribed_menu_alone_fails_at_vertex':1,'heavy_four_vertex_repair_checked_in_statement':True,
            'certificate_sha256':hashlib.sha256(raw).hexdigest()}


if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
