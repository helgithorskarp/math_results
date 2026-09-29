"""Separate full-graph audit; imports no target Python module.

Explicit adjacency and dual face orientation replace the ring generator.
Full Floyd distances and a shortest-path DAG replace cheap-leaf expansion.
All component-choice tuples replace the positive propagation trace.
Adverse metric corners with edge deletions replace the hop-route margins.
"""
from collections import deque
from fractions import Fraction
from heapq import heappop,heappush
from itertools import combinations,product
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROWS=[(1,2,3,4,5),(0,2,5,6,10),(0,1,3,6,7),(0,2,4,7,8),
      (0,3,5,8,9),(0,1,4,9,10),(1,2,7,10,11),(2,3,6,8,11),
      (3,4,7,9,11),(4,5,8,10,11),(1,5,6,9,11),(6,7,8,9,10)]


def construct(data):
    core=[set(row) for row in ROWS]
    faces=[F for F in combinations(range(12),3) if all(v in core[u] for u,v in combinations(F,2))]
    assert len(faces)==20
    edge_faces={}
    for i,F in enumerate(faces):
        for e in combinations(F,2):edge_faces.setdefault(e,[]).append(i)
    assert all(len(fs)==2 for fs in edge_faces.values())
    rotate=lambda F:min(F,F[1:]+F[:1],F[2:]+F[:2])
    oriented={0:(0,1,2)};queue=deque([0])
    while queue:
        i=queue.popleft();F=oriented[i]
        for u,v in zip(F,F[1:]+F[:1]):
            j=next(j for j in edge_faces[tuple(sorted((u,v)))] if j!=i)
            w=next(w for w in faces[j] if w not in (u,v));T=rotate((v,u,w))
            if j in oriented:assert oriented[j]==T
            else:oriented[j]=T;queue.append(j)
    cost={(u,v):w for u,v,w in data['core_edges']};assert set(cost)==set(edge_faces)
    long=sum(cost.values())+20*data['parent_length']+1;triangles=[]
    for i,F in enumerate(faces):
        z=12+i;assert data['parents'][i] in F
        for u in F:cost[u,z]=data['parent_length'] if u==data['parents'][i] else long
        a,b,c=oriented[i];triangles.extend([(a,b,z),(b,c,z),(c,a,z)])
    adj=[set() for _ in range(32)]
    for u,v in cost:adj[u].add(v);adj[v].add(u)
    darts=[(u,v) for F in triangles for u,v in zip(F,F[1:]+F[:1])]
    assert len(cost)==90 and len(triangles)==60 and len(set(darts))==180
    assert all((v,u) in darts for u,v in darts)
    for v in range(32):
        link={F[(F.index(v)+1)%3]:F[(F.index(v)+2)%3] for F in triangles if v in F}
        first=min(link);seen=set();u=first
        while u not in seen:seen.add(u);u=link[u]
        assert u==first and seen==set(link)==set(link.values())==adj[v]
    return adj,cost


def components(adj,removed):
    remaining=set(range(len(adj)))-set(removed);out=[]
    while remaining:
        start=min(remaining);remaining.remove(start);K={start};queue=deque([start])
        while queue:
            u=queue.popleft()
            for v in adj[u]:
                if v in remaining:remaining.remove(v);K.add(v);queue.append(v)
        out.append(K)
    return out


def floyd_paths(adj,cost):
    infinity=sum(cost.values())+1;n=len(adj)
    d=[[0 if u==v else infinity for v in range(n)] for u in range(n)]
    for (u,v),w in cost.items():d[u][v]=d[v][u]=w
    for k in range(n):
        for u in range(n):
            for v in range(n):d[u][v]=min(d[u][v],d[u][k]+d[k][v])
    paths=[]
    for source in range(n):
        def traverse(P):
            u=P[-1]
            if source<=u:paths.append(P)
            for v in sorted(adj[u]):
                if d[source][u]+cost[tuple(sorted((u,v)))]==d[source][v]:
                    assert v not in P;traverse(P+[v])
        traverse([source])
    return sorted(paths,key=lambda P:(P[0],P[-1],P)),d


def corner_distance(cost,source,target,forbidden):
    neighbors=[{} for _ in range(12)]
    for (u,v),w in cost.items():
        if (u,v)!=forbidden:neighbors[u][v]=neighbors[v][u]=w
    distance={source:Fraction(0)};queue=[(Fraction(0),source)]
    while queue:
        d,u=heappop(queue)
        if d!=distance[u]:continue
        if u==target:return d
        for v,w in neighbors[u].items():
            value=d+w
            if v not in distance or value<distance[v]:distance[v]=value;heappush(queue,(value,v))
    raise AssertionError('core edge deletion disconnected the core')


def run():
    data=json.loads((HERE/'certificate.json').read_text());expected=json.loads((HERE/'expected.json').read_text())['verify']
    adj,cost=construct(data);paths,d=floyd_paths(adj,cost)
    assert len(paths)==len({(P[0],P[-1]) for P in paths})==528
    digest=hashlib.sha256(json.dumps(paths,separators=(',',':')).encode()).hexdigest();assert digest==expected['catalog_sha256']
    core={(u,v):w for u,v,w in data['core_edges']};r=Fraction(data['core_box_radius']);corner_checks=0
    for P in paths:
        if P[0]>=12 or P[-1]>=12:continue
        assert all(v<12 for v in P)
        selected={tuple(sorted(e)) for e in zip(P,P[1:])}
        corner={e:Fraction(w)+(r if e in selected else -r) for e,w in core.items()}
        length=sum(corner[e] for e in selected)
        for e in selected:
            assert corner_distance(corner,P[0],P[-1],e)>length;corner_checks+=1
    decode=lambda C:{v for v in range(32) if C>>v&1}
    family=[decode(C) for C in data['family']]
    assert len(family)==56 and all(len(components(adj,set(range(32))-C))==1 for C in family)
    assert all(C&D for C,D in combinations(family,2))
    misses=[sum(1<<i for i,C in enumerate(family) if C.isdisjoint(P)) for P in paths]
    pair_checks=0
    for i,x in enumerate(misses):
        for y in misses[i:]:assert x&y;pair_checks+=1
    assert pair_checks==139656
    paths_by_tuple={tuple(P) for P in paths}|{tuple(P[::-1]) for P in paths}
    triple=data['three_path_transversal'];assert len(triple)==3 and all(tuple(P) in paths_by_tuple for P in triple)
    covered=set().union(*map(set,triple));assert all(C&covered for C in family)
    groups=[]
    for P,Q in data['positive_pairs']:
        assert tuple(P) in paths_by_tuple and tuple(Q) in paths_by_tuple
        groups.append([C for C in components(adj,set(P)|set(Q)) if len(C)>4])
    dual=[decode(C) for C in data['dual_sets']];assert len(dual)==4
    assert all(sum(v in C for C in dual)<=2 for v in range(32))
    choices=disjoint=fractional=0
    for chosen in product(*groups):
        choices+=1
        if any(C.isdisjoint(D) for C,D in combinations(chosen,2)):disjoint+=1;continue
        assert all(any(D<=C for D in chosen) for C in dual);fractional+=1
    assert choices==8192 and fractional>0
    inherited=[next(C for C in family if C<=D) for D in dual]
    assert all(sum(v in C for C in inherited)<=2 for v in range(32))
    # Corrupting one dual coefficient must violate the exact incidence bound.
    assert any(2*sum((2 if i==0 else 1) for i,C in enumerate(dual) if v in C)>5 for v in range(32))
    return {'status':'PASS','ambient_geodesics':len(paths),'ambient_pairs_with_repetition':pair_checks,
            'catalog_sha256':digest,'adverse_corner_edge_deletion_checks':corner_checks,
            'family_members':len(family),'family_pair_intersections':len(family)*(len(family)-1)//2,
            'positive_component_tuples':choices,'tuples_refuted_by_disjointness':disjoint,
            'tuples_refuted_by_fractional_dual':fractional,'family_geodesic_transversal_number':3,
            'family_four_term_dual':[sum(1<<v for v in C) for C in inherited],
            'forged_dual_rejected':True,
            'scope':'Independent full graph/catalog, complete mass-choice tuple audit, and adverse-corner verification; not independent peer review.'}


if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
