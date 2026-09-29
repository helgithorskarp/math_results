#!/usr/bin/env python3
"""Independent exact audit of cactus representative covers and bridges.

Builds the examples from edge lists, directly enumerates ambient shortest
internal paths, and checks that representative paths restrict correctly
in every spanning edge subgraph.  Includes a noncactus bridge reduction.
"""

from collections import deque
from itertools import combinations, product


def cycle(n):
    return [tuple(sorted((i,(i+1)%n))) for i in range(n)]


def adjacency(n,edges):
    a=[set() for _ in range(n)]
    for u,v in edges:a[u].add(v);a[v].add(u)
    return a


def components(adj,vertices):
    left=set(vertices);out=[]
    while left:
        seed=left.pop();comp={seed};todo=[seed]
        while todo:
            new=adj[todo.pop()]&left
            left.difference_update(new);comp.update(new);todo.extend(new)
        out.append(comp)
    return out


def distances(adj,start):
    d={start:0};q=deque([start])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if v not in d:d[v]=d[u]+1;q.append(v)
    return d


def internal_geodesics(ambient,fragment,part):
    eligible=[]
    for s in sorted(part):
        d=distances(ambient,s)
        def visit(path):
            v=path[-1]
            if v>=s and len(path)-1==d[v]:eligible.append(tuple(path))
            for u in fragment[v]&part:
                if u not in path:visit(path+[u])
        visit([s])
    return eligible


def cover(n,ambient_edges,fragment_vertices,fragment_edges):
    ambient=adjacency(n,ambient_edges)
    fragment=adjacency(n,fragment_edges)
    solution={}
    for comp in components(fragment,fragment_vertices):
        paths=internal_geodesics(ambient,fragment,comp)
        whole=set(comp)
        found=next(((p,q) for p in paths for q in paths
                    if set(p)|set(q)==whole),None)
        solution[frozenset(comp)]=found
    return solution


def bridge(n,edges,e):
    altered=set(edges)-{e}
    a=adjacency(n,altered)
    return e[1] not in distances(a,e[0])


def check_restriction(n,original_edges,core_edges,core_vertices,cycles):
    original_edges=set(original_edges);core_edges=set(core_edges)
    templates=[]
    for choices in product(*(tuple([None]+list(z)) for z in cycles)):
        removed={e for e in choices if e is not None}
        ambient=original_edges-removed
        fragment=core_edges-removed
        assert len(components(adjacency(n,fragment),core_vertices))==1
        pair=cover(n,ambient,core_vertices,fragment)[frozenset(core_vertices)]
        assert pair is not None
        templates.append((choices,removed,pair))
    checked=0;components_seen=0
    edge_list=sorted(original_edges)
    for mask in range(1<<len(edge_list)):
        alive={e for i,e in enumerate(edge_list) if mask>>i&1}
        missing=original_edges-alive
        removed=set()
        for z in cycles:
            hit=sorted(set(z)&missing)
            if hit:removed.add(hit[0])
        representative=next((row for row in templates if row[1]==removed),None)
        assert representative is not None
        chosen,pair=representative[1],representative[2]
        F=core_edges-chosen
        assert len(components(adjacency(n,F),core_vertices))==1
        assert all(bridge(n,F,e) for e in core_edges-alive-chosen)
        H=adjacency(n,alive)
        Hcore=adjacency(n,alive&core_edges)
        for D in components(Hcore,core_vertices):
            pieces=[]
            for path in pair:
                ix=[i for i,v in enumerate(path) if v in D]
                if not ix:continue
                assert ix==list(range(ix[0],ix[-1]+1))
                segment=path[ix[0]:ix[-1]+1]
                assert all(v in H[u] for u,v in zip(segment,segment[1:]))
                assert distances(H,segment[0])[segment[-1]]==len(segment)-1
                pieces.append(set(segment))
            assert set().union(*pieces)==D
            components_seen+=1
        checked+=1
    return len(templates),checked,components_seen


def noncactus_reduction():
    # A diamond has two triangles sharing edge 0--1 and cycle rank two.
    E={(0,1),(0,2),(1,2),(0,3),(1,3)}
    beta=len(E)-4+1
    reps=set()
    for bits in range(1<<len(E)):
        missing={e for i,e in enumerate(sorted(E)) if bits>>i&1}
        chosen=set()
        while True:
            available=next((e for e in sorted(missing-chosen)
                            if not bridge(4,E-chosen,e)),None)
            if available is None:break
            chosen.add(available)
        assert len(chosen)<=beta
        assert len(components(adjacency(4,E-chosen),range(4)))==1
        assert all(bridge(4,E-chosen,e) for e in missing-chosen)
        reps.add(frozenset(chosen))
    return len(reps),1<<len(E)


def main():
    c8=cycle(8);c8_edges=set(c8)|{(0,8),(2,8),(4,8)}
    p=check_restriction(9,c8_edges,c8,set(range(8)),[c8])
    assert p==(9,2048,8200)
    c1=[(0,1),(1,2),(2,3),(0,3)]
    c2=[(0,4),(4,5),(5,6),(0,6)]
    double=check_restriction(7,set(c1)|set(c2),set(c1)|set(c2),
                             set(range(7)),[c1,c2])
    assert double==(25,256,800)
    c10=cycle(10);star=set(c10)|{(0,10),(3,10),(8,10)}
    intact=cover(11,star,set(range(10)),c10)[frozenset(range(10))]
    broken=cover(11,star-{(0,9)},set(range(10)),set(c10)-{(0,9)})[
        frozenset(range(10))]
    assert intact is not None and broken is None
    diamond=noncactus_reduction()
    print(f"cycle8_reps_masks_components={p} double4={double} "
          f"star_intact=YES star_deleted=NO diamond_reps_masks={diamond} PASS")


if __name__=='__main__':main()
