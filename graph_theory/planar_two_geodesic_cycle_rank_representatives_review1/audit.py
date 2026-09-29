#!/usr/bin/env python3
"""Independent exact audit of connected-deletion representatives.

No target code is imported.  Directly enumerates ambient geodesic paths,
all connected theta representatives, all theta masks, and the K5 boundary.
"""

from collections import deque
from itertools import combinations


def adj(n,edges):
    g=[set() for _ in range(n)]
    for u,v in edges:g[u].add(v);g[v].add(u)
    return g


def components(g,vertices):
    left=set(vertices);out=[]
    while left:
        s=left.pop();part={s};todo=[s]
        while todo:
            new=g[todo.pop()]&left
            left.difference_update(new);part.update(new);todo.extend(new)
        out.append(part)
    return out


def bfs(g,s):
    d={s:0};q=deque([s])
    while q:
        u=q.popleft()
        for v in g[u]:
            if v not in d:d[v]=d[u]+1;q.append(v)
    return d


def is_bridge(n,edges,e):
    return e[1] not in bfs(adj(n,set(edges)-{e}),e[0])


def internal_paths(g,fragment,vertices):
    candidates=[]
    for s in sorted(vertices):
        d=bfs(g,s)
        def visit(path):
            v=path[-1]
            if v>=s and len(path)-1==d[v]:candidates.append(tuple(path))
            for w in fragment[v]&vertices:
                if w not in path:visit(path+[w])
        visit([s])
    return candidates


def pair_cover(n,ambient_edges,fragment_edges,vertices):
    ambient=adj(n,ambient_edges)
    fragment=adj(n,fragment_edges)
    paths=internal_paths(ambient,fragment,vertices)
    return next(((p,q) for p in paths for q in paths
                 if set(p)|set(q)==set(vertices)),None)


def theta():
    paths=((0,2,3,1),(0,4,5,1),(0,6,7,1))
    E={tuple(sorted((u,v))) for p in paths for u,v in zip(p,p[1:])}
    assert len(E)==9
    ordered=sorted(E);reps={};by_size=[0,0,0]
    for mask in range(1<<9):
        A={e for j,e in enumerate(ordered) if mask>>j&1}
        F=E-A
        if len(components(adj(8,F),range(8)))!=1:continue
        assert len(A)<=2
        pair=pair_cover(8,F,F,set(range(8)))
        assert pair is not None
        reps[frozenset(A)]=pair
        by_size[len(A)]+=1
    assert len(reps)==37 and by_size==[1,9,27]
    checked=0
    for mask in range(1<<9):
        alive={e for j,e in enumerate(ordered) if mask>>j&1}
        missing=E-alive
        chosen=set()
        while True:
            candidate=next((e for e in sorted(missing-chosen)
                            if not is_bridge(8,E-chosen,e)),None)
            if candidate is None:break
            chosen.add(candidate)
        assert frozenset(chosen) in reps
        assert all(is_bridge(8,E-chosen,e) for e in missing-chosen)
        pair=reps[frozenset(chosen)]
        H=adj(8,alive)
        for D in components(H,range(8)):
            pieces=[]
            for path in pair:
                where=[j for j,v in enumerate(path) if v in D]
                if not where:continue
                assert where==list(range(where[0],where[-1]+1))
                segment=path[where[0]:where[-1]+1]
                assert all(v in H[u] for u,v in zip(segment,segment[1:]))
                assert bfs(H,segment[0])[segment[-1]]==len(segment)-1
                pieces.append(set(segment))
            assert set().union(*pieces)==D
            checked+=1
    assert checked==1815
    return len(reps),by_size,1<<9,checked


def complete_five():
    E={tuple(p) for p in combinations(range(5),2)}
    assert len(E)==10
    assert pair_cover(5,E,E,set(range(5))) is None
    trees=0
    for chosen in combinations(sorted(E),4):
        T=set(chosen)
        if len(components(adj(5,T),range(5)))!=1:continue
        assert pair_cover(5,T,T,set(range(5))) is not None
        trees+=1
    assert trees==125
    return trees


def main():
    t=theta();k=complete_five()
    print(f"theta_reps_by_size_masks_components={t} "
          f"K5_spanning_tree_reps={k} K5_intact_two_cover=NO PASS")


if __name__=='__main__':main()
