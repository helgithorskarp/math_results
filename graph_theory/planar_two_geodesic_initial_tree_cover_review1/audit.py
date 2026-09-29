#!/usr/bin/env python3
"""Independent graph and deletion audit for induced-tree terminal family.

The graph is rebuilt from the stated edges, without importing the target
checker or its rotation.  Unit-edge distances are recomputed by BFS.
"""

from collections import deque
from itertools import combinations, permutations


def build(r):
    adj=[set() for _ in range(6)]
    def edge(u,v):
        assert u!=v and v not in adj[u]
        adj[u].add(v);adj[v].add(u)
    for i in range(4):
        edge(i,(i+1)%4)
        edge(4,i);edge(5,i)
    gadgets=[]
    for _ in range(r):
        names=list(range(len(adj),len(adj)+10))
        adj.extend(set() for _ in names)
        a,b,am,A,am2,A2,bm,B,bm2,B2=names
        for u,v in ((0,a),(a,b),(b,1),
                    (a,am),(am,A),(a,am2),(am2,A2),
                    (b,bm),(bm,B),(b,bm2),(bm2,B2),
                    (0,A),(1,B)):
            edge(u,v)
        gadgets.append((set(names),(A,A2,B,B2),(a,b)))
    return adj,gadgets


def edges(adj):
    return {tuple(sorted((u,v))) for u,row in enumerate(adj) for v in row}


def components(adj,subset):
    left=set(subset);out=[]
    while left:
        start=left.pop();part={start};todo=[start]
        while todo:
            new=adj[todo.pop()] & left
            left.difference_update(new);part.update(new);todo.extend(new)
        out.append(part)
    return out


def bfs(adj,start):
    dist={start:0};queue=deque([start])
    while queue:
        u=queue.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v]=dist[u]+1;queue.append(v)
    return dist


def tree_path(adj,tree,u,v):
    parent={u:None};queue=deque([u])
    while queue and v not in parent:
        x=queue.popleft()
        for y in adj[x] & tree:
            if y not in parent:parent[y]=x;queue.append(y)
    assert v in parent
    path=[v]
    while path[-1]!=u:path.append(parent[path[-1]])
    return tuple(reversed(path))


def audit_family(r):
    adj,gadgets=build(r)
    assert len(adj)==6+10*r and len(edges(adj))==12+13*r
    residual=components(adj,set(range(4,len(adj))))
    assert {frozenset(x) for x in residual} == (
        {frozenset((4,)),frozenset((5,))} |
        {frozenset(tree) for tree,_,_ in gadgets})
    for tree,(A,A2,B,B2),(a,b) in gadgets:
        internal={e for e in edges(adj) if set(e)<=tree}
        assert len(tree)==10 and len(internal)==9
        assert len(components(adj,tree))==1
        assert sum(len(adj[v]&tree)==1 for v in tree)==4
        first=tree_path(adj,tree,A,A2)
        second=tree_path(adj,tree,B,B2)
        assert len(first)==len(second)==5 and set(first)|set(second)==tree
        assert bfs(adj,A)[A2]==4 and bfs(adj,B)[B2]==4
        assert len(tree_path(adj,tree,A,B))-1==5 and bfs(adj,A)[B]==3
        # Enumerate every eligible internal geodesic and test a pair,
        # independently of the displayed leaf pairing.
        eligible=[]
        for u in sorted(tree):
            dist=bfs(adj,u)
            for v in sorted(tree):
                if u>v:continue
                path=tree_path(adj,tree,u,v)
                if len(path)-1==dist[v]:eligible.append(set(path))
        assert any(x|y==tree for x,y in combinations(eligible,2))
    return adj,gadgets


def audit_deletions(adj,gadget):
    tree,(A,A2,B,B2),(a,b)=gadget
    initial=(tree_path(adj,tree,A,A2),tree_path(adj,tree,B,B2))
    mutable=sorted(e for e in edges(adj) if set(e)&tree)
    assert len(mutable)==13
    fixed=edges(adj)-set(mutable)
    checked=0
    for mask in range(1<<13):
        surviving=fixed|{e for j,e in enumerate(mutable) if mask>>j&1}
        H=[set() for _ in adj]
        for u,v in surviving:H[u].add(v);H[v].add(u)
        for D in components(H,tree):
            pieces=[]
            for path in initial:
                indices=[j for j,v in enumerate(path) if v in D]
                if not indices:continue
                assert indices==list(range(indices[0],indices[-1]+1))
                piece=path[indices[0]:indices[-1]+1]
                assert all(v in H[u] for u,v in zip(piece,piece[1:]))
                assert bfs(H,piece[0])[piece[-1]]==len(piece)-1
                pieces.append(set(piece))
            assert set().union(*pieces)==D
            checked+=1
    assert checked==45056
    return checked


def noninduced_boundary():
    # T=0-1-2-3-4 is a G-geodesic (k=1), but chords 0-3 and 1-4
    # reconnect H[V(T)] after deleting 2-3.  No single H-geodesic
    # covers all five vertices.  The selected T-edge forest still has
    # two components, each covered by a restricted initial path.
    original={(0,1):1,(1,2):1,(2,3):1,(3,4):1,(0,3):3,(1,4):3}
    retained={e:w for e,w in original.items() if e!=(2,3)}
    def distance(edges,start):
        d={start:0};changed=True
        while changed:
            changed=False
            for (u,v),w in edges.items():
                for a,b in ((u,v),(v,u)):
                    if a in d and (b not in d or d[b]>d[a]+w):
                        d[b]=d[a]+w;changed=True
        return d
    assert distance(original,0)[4]==4
    adj=[set() for _ in range(5)]
    for a,b in retained:adj[a].add(b);adj[b].add(a)
    assert len(components(adj,range(5)))==1
    spanning=[]
    for path in permutations(range(5)):
        if all(tuple(sorted((a,b))) in retained for a,b in zip(path,path[1:])):
            cost=sum(retained[tuple(sorted((a,b)))] for a,b in zip(path,path[1:]))
            spanning.append((cost,distance(retained,path[0])[path[-1]]))
    assert len(spanning)==4 and all(cost>dist for cost,dist in spanning)
    forest=[set() for _ in range(5)]
    for a,b in ((0,1),(1,2),(3,4)):
        forest[a].add(b);forest[b].add(a)
    assert {frozenset(c) for c in components(forest,range(5))}=={
        frozenset((0,1,2)),frozenset((3,4))}
    assert distance(retained,0)[2]==2 and distance(retained,3)[4]==1
    return len(spanning)


def main():
    report=[]
    for r in (1,2,5):
        adj,gadgets=audit_family(r)
        report.append((r,len(adj),len(edges(adj)),len(edges(adj))-len(adj)+2))
        if r==1: checked=audit_deletions(adj,gadgets[0])
    boundary=noninduced_boundary()
    print(f"families={report} deletion_masks=8192 residual_components={checked} "
          f"noninduced_hamiltonian_paths={boundary} nonisometric=PASS "
          "two_internal_geodesics=PASS")


if __name__=='__main__':main()
