"""Independent exact checks of the annular rooted-decomposition obstruction.

No imports from the target's verifier. Standard Python 3 only.
"""
from collections import deque
from itertools import combinations
import json
from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / 'planar_two_geodesic_rooted_decomposition_barrier'


def annulus(k):
    graph = [set() for _ in range(2*k+1)]
    def add(u, v):
        graph[u].add(v)
        graph[v].add(u)
    for i in range(k):
        b, bn = 1+i, 1+(i+1)%k
        c, cn = 1+k+i, 1+k+(i+1)%k
        for u, v in ((0,b),(b,bn),(c,cn),(b,c),(b,cn)):
            add(u,v)
    return graph


def p3(graph, triple):
    degrees = [len(graph[u] & (set(triple)-{u})) for u in triple]
    return sorted(degrees) == [1,1,2]


def p3_partition(graph, vertices):
    vertices = set(vertices)
    assert len(vertices) == 6
    for a in combinations(sorted(vertices), 3):
        if p3(graph,a) and p3(graph,vertices-set(a)):
            return a, tuple(sorted(vertices-set(a)))
    return None


def bfs(graph, start):
    dist = [-1]*len(graph)
    dist[start] = 0
    todo = deque([start])
    while todo:
        u = todo.popleft()
        for v in graph[u]:
            if dist[v] < 0:
                dist[v] = dist[u]+1
                todo.append(v)
    assert min(dist) >= 0
    return dist


def path_masks(graph):
    masks = set()
    for s in range(len(graph)):
        d = bfs(graph,s)
        def extend(u, mask):
            masks.add(mask)
            for v in graph[u]:
                if d[v] == d[u]+1:
                    extend(v,mask | (1<<v))
        extend(s,1<<s)
    return sorted(masks)


def covered(bag, paths):
    need = sum(1<<u for u in bag)
    return any(((p|q)&need)==need for i,p in enumerate(paths) for q in paths[i:])


def certificate(graph, order):
    n = len(graph)
    assert sorted(order) == list(range(n))
    positions = {v:i for i,v in enumerate(order)}
    fill = [set(x) for x in graph]
    bags, links = [], []
    for i,v in enumerate(order):
        later = {w for w in fill[v] if positions[w]>i}
        bags.append(later|{v})
        if later:
            links.append((i,min(positions[w] for w in later)))
        for x,y in combinations(later,2):
            fill[x].add(y)
            fill[y].add(x)
    assert len(links)==n-1
    tree = [set() for _ in range(n)]
    for a,b in links:
        tree[a].add(b)
        tree[b].add(a)
    for v in range(n):
        owners={i for i,bag in enumerate(bags) if v in bag}
        reached=set()
        stack=[next(iter(owners))]
        while stack:
            i=stack.pop()
            if i not in reached:
                reached.add(i)
                stack.extend((tree[i]&owners)-reached)
        assert reached==owners
    for u in range(n):
        for v in graph[u]:
            assert any(u in bag and v in bag for bag in bags)
    paths=path_masks(graph)
    assert all(covered(bag,paths) for bag in bags)
    assert any(0 not in bag for bag in bags)
    return len(bags),len(paths)


def check():
    orders=json.loads((TARGET/'orders.json').read_text())
    stats={'local_sets':0,'root_free_bags':0,'root_free_orders':0,
           'root_free_path_masks':0,'weighted_cases':0}
    for k in range(4,101):
        g=annulus(k)
        assert sum(map(len,g))//2==5*k
        assert {u for u in range(len(g)) if u not in g[0] and u!=0}==set(range(k+1,2*k+1))
        for i in range(k):
            b=1+i;c=1+k+i
            wheel=g[b]|{b}
            sun=g[c]|{c,0}
            for six in (wheel,sun):
                assert len(six)==6
                assert max(bfs(g,u)[v] for u in six for v in six)==2
                assert p3_partition(g,six) is None
                stats['local_sets']+=1
        if str(k) in orders:
            bags,paths=certificate(g,orders[str(k)])
            stats['root_free_bags']+=bags
            stats['root_free_path_masks']+=paths
            stats['root_free_orders']+=1
        for seed in range(15):
            mass=[((37*i+71*seed+13*k)%19) for i in range(len(g))]
            cols=[mass[1+i]+mass[1+k+i] for i in range(k)]
            total=sum(cols)
            chosen=[0]
            if 2*cols[0]<total:
                prefix=cols[0]
                for j in range(1,k):
                    prefix+=cols[j]
                    if 2*prefix>=total:
                        chosen.append(j)
                        break
            removed={0}
            for i in chosen:
                removed.update((1+i,1+k+i))
            unseen=set(range(len(g)))-removed
            while unseen:
                todo=[unseen.pop()]
                component=[]
                while todo:
                    u=todo.pop();component.append(u)
                    fresh=g[u]&unseen
                    todo.extend(fresh);unseen-=fresh
                assert 2*sum(mass[u] for u in component)<=sum(mass)
            stats['weighted_cases']+=1
    print(json.dumps(stats,sort_keys=True))


if __name__=='__main__':
    check()
