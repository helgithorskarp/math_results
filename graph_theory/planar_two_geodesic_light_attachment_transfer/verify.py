#!/usr/bin/env python3
"""Exact regression checks for light-attachment transfer; no census premise."""
import argparse
from heapq import heappop, heappush
import json
from pathlib import Path
import random


def require(ok, message):
    if not ok:
        raise AssertionError(message)


class Graph:
    def __init__(self, n, edges, faces):
        self.adj = [dict() for _ in range(n)]
        for u, v, length in edges:
            self.edge(u, v, length)
        self.faces = list(map(tuple, faces))
        self.pieces = []

    def edge(self, u, v, length):
        require(u != v and length > 0, 'positive simple edge')
        if v in self.adj[u]:
            require(self.adj[u][v] == length, 'shared edge agrees')
        self.adj[u][v] = self.adj[v][u] = length

    def components(self, deleted=()):
        unseen = set(range(len(self.adj))) - set(deleted)
        result = []
        while unseen:
            seen = {unseen.pop()}
            todo = list(seen)
            while todo:
                u = todo.pop()
                new = set(self.adj[u]) & unseen
                unseen -= new
                seen |= new
                todo.extend(new)
            result.append(seen)
        return result

    def distances(self):
        rows = []
        for s in range(len(self.adj)):
            d = [10**30] * len(self.adj)
            d[s] = 0
            heap = [(0, s)]
            while heap:
                cost, u = heappop(heap)
                if cost != d[u]:
                    continue
                for v, length in self.adj[u].items():
                    if cost + length < d[v]:
                        d[v] = cost + length
                        heappush(heap, (d[v], v))
            require(max(d) < 10**30, 'connected')
            rows.append(d)
        return rows

    def paths(self, source, targets, distances):
        targets = set(targets)
        def extend(path):
            u = path[-1]
            if u in targets:
                yield path
            for v, length in sorted(self.adj[u].items()):
                if distances[source][v] == distances[source][u] + length:
                    yield from extend(path + (v,))
        yield from extend((source,))

    def shortest(self, s, t, dist):
        path = [s]
        while path[-1] != t:
            u = path[-1]
            choices = [v for v, length in self.adj[u].items()
                       if length + dist[v][t] == dist[u][t]]
            path.append(min(choices))
        return tuple(path)

    def check_path(self, path, dist):
        require(path and len(path) == len(set(path)), 'simple path')
        cost = sum(self.adj[a][b] for a, b in zip(path, path[1:]))
        require(cost == dist[path[0]][path[-1]], 'ambient shortest path')

    def sphere(self):
        darts = set()
        rotation = [dict() for _ in self.adj]
        for face in self.faces:
            require(len(face) >= 3 and len(set(face)) == len(face), 'simple face')
            for i, u in enumerate(face):
                before, after = face[i-1], face[(i+1) % len(face)]
                require(after in self.adj[u] and (u, after) not in darts, 'face dart')
                require(before not in rotation[u], 'unique rotation successor')
                rotation[u][before] = after
                darts.add((u, after))
        require(darts == {(u,v) for u,row in enumerate(self.adj) for v in row}, 'all darts')
        for u, row in enumerate(rotation):
            require(set(row) == set(row.values()) == set(self.adj[u]), 'rotation domain')
            first = min(row)
            seen, v = set(), first
            while v not in seen:
                seen.add(v)
                v = row[v]
            require(v == first and seen == set(row), 'one cyclic vertex link')
        require(len(self.adj)-len(darts)//2+len(self.faces) == 2, 'sphere Euler characteristic')
        require(len(self.components()) == 1, 'connected sphere')

    def attach(self, m, interface, long_edges=1):
        # Cone over a triangle with one long alternative path on each side.
        ears = [list(range(4+j*m, 4+(j+1)*m)) for j in range(3)]
        edges = {(1,2), (2,3), (1,3)}
        faces = [(1,2,3)]
        boundary = []
        bags, tree = [{0,1,2,3}], []
        for (a,b), ear in zip(((1,2),(2,3),(3,1)), ears):
            chain = [a] + ear + [b]
            boundary.extend(chain[:-1])
            edges.update(tuple(sorted(e)) for e in zip(chain, chain[1:]))
            faces.append(tuple(chain))
            first = len(bags)
            bags.extend({0,a,chain[i],chain[i+1]} for i in range(1,len(chain)-1))
            tree.extend((i,i+1) for i in range(first,len(bags)-1))
            tree.append((len(bags)-1,0))
        edges.update((0,v) for v in boundary)
        faces.extend((0,boundary[(i+1)%len(boundary)],boundary[i]) for i in range(len(boundary)))
        r = interface[0]
        mapping = {0:r}
        if len(interface) == 2:
            mapping[1] = interface[1]
        else:
            mapping[ears[0][0]], mapping[ears[0][1]] = interface[1:]
        internal = set()
        for v in range(3*m+4):
            if v not in mapping:
                mapping[v] = len(self.adj)
                internal.add(mapping[v])
                self.adj.append({})
        for u,v in sorted(edges):
            a,b = mapping[u],mapping[v]
            if b not in self.adj[a]:
                self.edge(a,b,long_edges)
        guest = [tuple(mapping[v] for v in face) for face in faces]
        if len(interface) == 3:
            require(tuple(interface) in self.faces, 'oriented host triangle')
            self.faces.remove(tuple(interface))
            guest.remove((r,interface[2],interface[1]))
            self.faces.extend(guest)
        else:
            a = interface[1]
            def containing(fs,u,v):
                return next(face for face in fs
                            if any(x==u and y==v for x,y in zip(face,face[1:]+face[:1])))
            old = containing(self.faces,r,a)
            other = containing(guest,a,r)
            def without_edge(face,u,v):
                j=face.index(v)
                path=face[j:]+face[:j]
                require(path[-1]==u,'edge boundary path')
                return path
            merged = without_edge(old,r,a)+without_edge(other,a,r)[1:-1]
            self.faces.remove(old)
            guest.remove(other)
            self.faces.extend(guest+[merged])
        record = dict(internal=internal, boundary=set(interface),
                      bags=[{mapping[v] for v in bag} for bag in bags], tree=tree)
        self.pieces.append(record)
        return record

    def check_local_decomposition(self, piece):
        bags=piece['bags']+[set(range(len(self.adj)))-piece['internal']]
        anchor=next(i for i,b in enumerate(bags[:-1]) if piece['boundary']<=b)
        edges=piece['tree']+[(anchor,len(bags)-1)]
        tree=[set() for _ in bags]
        for a,b in edges:
            tree[a].add(b)
            tree[b].add(a)
        require(len(edges)==len(bags)-1,'decomposition tree edge count')
        for v in range(len(self.adj)):
            nodes={i for i,b in enumerate(bags) if v in b}
            require(nodes,'vertex covered')
            seen={min(nodes)}
            todo=list(seen)
            while todo:
                u=todo.pop()
                new=(tree[u]&nodes)-seen
                seen|=new
                todo.extend(new)
            require(seen==nodes,'running intersection')
        for u,row in enumerate(self.adj):
            for v in row:
                require(any({u,v}<=bag for bag in bags),'edge covered')
        require(all(len(b)<=4 for b in bags[:-1]),'local width three')


def annulus(k):
    b=lambda i:1+i%k
    c=lambda i:1+k+i%k
    edges={}
    faces=[]
    for i in range(k):
        for u,v in ((0,b(i)),(b(i),b(i+1)),(c(i),c(i+1)),(b(i),c(i)),(b(i),c(i+1))):
            edges[tuple(sorted((u,v)))]=1
        faces.extend(((0,b(i),b(i+1)),(b(i),c(i+1),b(i+1)),(b(i),c(i),c(i+1))))
    faces.append(tuple(c(i) for i in reversed(range(k))))
    return Graph(2*k+1,[(u,v,w) for (u,v),w in edges.items()],faces), set(range(k+1,2*k+1))


def support(dist, source, targets):
    return {v for v in range(len(dist)) if any(dist[source][v]+dist[v][t]==dist[source][t] for t in targets)}


def cover_bag(g, bag, dist):
    vertices=sorted(bag)
    return [g.shortest(vertices[i],vertices[min(i+1,len(vertices)-1)],dist)
            for i in range(0,len(vertices),2)]


def check_transfer(g, S, p, candidates, w, result):
    outside=g.components(S)
    proxy=[w[v] if v in S-set(p) else 0 for v in range(len(w))]
    discarded=0
    largest=0
    for part in outside:
        mass=sum(w[v] for v in part)
        largest=max(largest,mass)
        if mass==0:
            continue
        neighbors=set().union(*(set(g.adj[v]) for v in part)) & (S-set(p))
        require(len(neighbors)<=1,'one surviving support neighbor')
        require(2*mass<=sum(w),'outside component light')
        if neighbors:
            proxy[next(iter(neighbors))]+=mass
        else:
            discarded+=mass
    require(sum(proxy)==sum(w)-sum(w[v] for v in p)-discarded,'mass identity')
    for q in candidates:
        require(set(q)<=S,'second path stays in support')
        parts=g.components(set(p)|set(q))
        if all(2*sum(proxy[v] for v in part)<=sum(proxy) for part in parts):
            bound=max(sum(proxy),2*largest)
            require(all(2*sum(w[v] for v in part)<=bound for part in parts),'sharper original-mass bound')
            require(all(2*sum(w[v] for v in part)<=sum(w) for part in parts),'half balance')
            result['transfer_checks']+=1
            result['discarded_mass_checks']+=int(discarded>0)
            return
    raise AssertionError('no transfer witness')


def masses(g, rng):
    n=len(g.adj)
    yield [0]*n
    yield [1]*n
    for v in range(n):
        yield [int(i==v) for i in range(n)]
    for piece in g.pieces:
        inside=piece['internal']
        # A strict-heavy case and an exact-equality case.
        yield [2*n if i in inside else 1 for i in range(n)]
        yield [n-len(inside) if i in inside else len(inside) for i in range(n)]
    for _ in range(100):
        yield [rng.randrange(8) for _ in range(n)]


def unit_fixture(k,m,kind,result,rng):
    g,C=annulus(k)
    if kind=='single':
        g.attach(m,(0,1,2))
        chosen=1
    elif kind=='star':
        g.attach(m,(0,1,2))
        g.attach(m,(0,2,3))
        g.attach(m,(0,5))
        chosen=2
    else:
        for a in (1,3,5):
            g.attach(m,(0,a))
        chosen=None
    g.sphere()
    for piece in g.pieces:
        g.check_local_decomposition(piece)
        result['local_decompositions']+=1
    dist=g.distances()
    S=support(dist,0,C)
    active={v for v in g.adj[0] if set(g.adj[v])&C}
    require(S=={0}|active|C,'facial support identity')
    outside=g.components(S)
    require({frozenset(x) for x in outside}=={frozenset(x['internal']) for x in g.pieces},'peripheral pieces')
    candidates=list(g.paths(0,C,dist))
    for q in candidates:
        g.check_path(q,dist)
    prescribed=[p for p in candidates if chosen is None or p[1]==chosen]
    require(prescribed,'first path exists')
    result['prescribed_paths']+=len(prescribed)
    for w in masses(g,rng):
        heavy=[piece for piece in g.pieces if 2*sum(w[v] for v in piece['internal'])>sum(w)]
        if heavy:
            piece=heavy[0]
            bag=next((bag for bag in piece['bags']
                      if all(2*sum(w[v] for v in part)<=sum(w) for part in g.components(bag))),None)
            require(bag is not None,'local balanced bag')
            paths=cover_bag(g,bag,dist)
            for q in paths:
                g.check_path(q,dist)
            deleted=set().union(*map(set,paths))
            require(bag<=deleted and len(paths)<=2,'two-path bag cover')
            require(all(2*sum(w[v] for v in part)<=sum(w) for part in g.components(deleted)),'heavy witness')
            result['heavy_checks']+=1
        else:
            for p in prescribed:
                check_transfer(g,S,p,candidates,w,result)
    result['unit_fixtures']+=1
    return g,dist


def interval_fixture(m,result,rng):
    # Three equal-length s-t branches, with unequal positive edge lengths.
    edges=[(0,a,a+1) for a in (1,2,3)]+[(a,4,9-a) for a in (1,2,3)]
    g=Graph(5,edges,[(0,1,4,2),(0,2,4,3),(0,3,4,1)])
    for a in (1,2,3):
        g.attach(m,(0,a),long_edges=100)
    g.sphere()
    dist=g.distances()
    S=support(dist,0,{4})
    require(S==set(range(5)),'exact interval support')
    paths=list(g.paths(0,{4},dist))
    require(len(paths)==3,'three interval geodesics')
    for q in paths:
        g.check_path(q,dist)
    result['prescribed_paths']+=len(paths)
    for w in masses(g,rng):
        if any(2*sum(w[v] for v in part)>sum(w) for part in g.components(S)):
            continue
        for p in paths:
            check_transfer(g,S,p,paths,w,result)
    result['nonuniform_metric_fixtures']+=1


def strictness(g,dist,result):
    n=len(g.adj)
    require(n==46,'strictness fixture order')
    interval_margin=n
    face_margin=n
    for s in range(n):
        for t in range(s,n):
            S=support(dist,s,{t})
            interval_margin=min(interval_margin,n-len(S)-dist[s][t]-1)
        for face in g.faces:
            S=support(dist,s,set(face))
            face_margin=min(face_margin,n-len(S)-max(dist[s][t]+1 for t in face))
    require(interval_margin>0 and face_margin>0,'outside previous error criterion in this embedding')
    require(all(2*max(map(len,g.components(face)),default=0)>n for face in g.faces),'no facial half separator in this embedding')
    old_roots=0
    for v,row in enumerate(g.adj):
        pieces=g.components({v}|set(row))
        if all((sum(len(set(g.adj[x])&part) for x in part)//2 in
                {len(part)-1,len(part)*(len(part)-1)//2}) for part in pieces):
            old_roots+=1
    require(old_roots==0,'outside forest-or-clique nonneighbor criterion at every root')
    require(not any(len({u,v}|set(g.adj[u])|set(g.adj[v]))==n
                    for u,row in enumerate(g.adj) for v in row),'no dominating edge')
    core=set(range(n))
    while True:
        remove={v for v in core if len(set(g.adj[v])&core)<4}
        if not remove:
            break
        core-=remove
    require(len(core)==13,'nonempty four-core excludes treewidth at most three')
    result['strict_fixture_vertices']=n
    result['minimum_interval_error_deficit']=interval_margin
    result['minimum_facial_error_deficit']=face_margin
    result['four_core_order']=len(core)
    result['old_subclass_roots']=old_roots


def controls(result):
    # Verify rejection when the surviving boundary has two vertices.
    g,C=annulus(6)
    for a in (1,3,5):
        g.attach(3,(0,a,a+1))
    dist=g.distances()
    S=support(dist,0,C)
    p=(0,2,8)
    g.check_path(p,dist)
    require(any(len(set().union(*(set(g.adj[v]) for v in part))&(S-set(p)))>1
                for part in g.components(S)),'two-boundary control rejected')
    candidates=list(g.paths(0,C,dist))
    try:
        check_transfer(g,S,p,candidates,[1]*len(g.adj),result)
    except AssertionError as exc:
        require(str(exc)=='one surviving support neighbor','reject for the intended boundary reason')
    else:
        raise AssertionError('positive two-boundary control was accepted')
    check_transfer(g,S,p,candidates,[0]*len(g.adj),result)
    result['prescribed_paths']+=1
    result['rejected_boundary_controls']+=1
    # A heavy outside component cannot be removed by a second path in S.
    one,C=annulus(6)
    piece=one.attach(3,(0,1))
    dist=one.distances()
    S=support(dist,0,C)
    w=[int(v in piece['internal']) for v in range(len(one.adj))]
    require(2*sum(w[v] for v in piece['internal'])>sum(w),'heavy control rejected')
    result['rejected_mass_controls']+=1


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    result=dict(unit_fixtures=0,nonuniform_metric_fixtures=0,local_decompositions=0,
                prescribed_paths=0,transfer_checks=0,discarded_mass_checks=0,
                heavy_checks=0,rejected_boundary_controls=0,rejected_mass_controls=0)
    rng=random.Random(20260928092)
    for k,m,kind in [(6,2,'single'),(9,3,'single'),(6,2,'star'),(9,3,'star'),
                     (6,3,'edge'),(9,4,'edge')]:
        g,dist=unit_fixture(k,m,kind,result,rng)
        if (k,m,kind)==(6,3,'edge'):
            strictness(g,dist,result)
    for m in (2,3):
        interval_fixture(m,result,rng)
    controls(result)
    output=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.check:
        require(json.loads(Path(__file__).with_name('expected.json').read_text())==result,'expected output')
    print(output,end='')


if __name__=='__main__':
    main()
