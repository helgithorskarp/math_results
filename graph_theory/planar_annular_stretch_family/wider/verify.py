#!/usr/bin/env python3
"""Exact boundary certificates and constructive witnesses; standard library only."""
from collections import deque, Counter
from copy import deepcopy
from hashlib import sha256
from heapq import heappush, heappop
import json
from pathlib import Path
import sys


def vertex(m, h, i, j):
    return 2 + (i % m) * h + j


def graph(m, h):
    if m < 6 or m % 2 or h < 1:
        raise ValueError("even circumference >=6 and positive height required")
    adj = [set() for _ in range(m*h+2)]
    vertical = set()
    def edge(a, b):
        adj[a].add(b); adj[b].add(a)
    for j in range(h):
        for i in range(m):
            v = vertex(m,h,i,j)
            edge(v,vertex(m,h,i+1,j))
            if j == 0: edge(0,v)
            if j == h-1: edge(1,v)
            if j+1 < h:
                u = vertex(m,h,i,j+1)
                edge(v,u); vertical.add(tuple(sorted((v,u))))
                if (i+j) % 2:
                    edge(vertex(m,h,i+1,j),u)
                else:
                    edge(v,vertex(m,h,i+1,j+1))
    edges = {tuple(sorted((a,b))) for a in range(len(adj)) for b in adj[a]}
    return adj, edges, vertical


def components(adj, removed):
    remaining = set(range(len(adj))) - removed
    parts = []
    while remaining:
        todo = [min(remaining)]; part = set()
        while todo:
            v = todo.pop()
            if v not in remaining: continue
            remaining.remove(v); part.add(v)
            todo.extend(adj[v] & remaining)
        parts.append(frozenset(part))
    return parts


def distances(adj, root):
    d = {root:0}; todo = deque([root])
    while todo:
        v = todo.popleft()
        for u in sorted(adj[v]):
            if u not in d: d[u] = d[v]+1; todo.append(u)
    return d


def check_kernel(data):
    m,h = data['m'],data['height']
    q,proxy = data['anchor_rows'],data['proxy']
    if (m,h,q,proxy) not in ((10,3,1,1),(12,4,2,1),(10,2,0,None)):
        raise ValueError("incorrect kernel specification")
    adj,edges,vertical = graph(m,h)
    distance = [distances(adj,v) for v in range(len(adj))]
    anchor = {0} | {vertex(m,h,i,j) for i in range(m) for j in range(q)} if q else set()
    forced = [anchor] if q else []
    distinct = set(); trace = []; completed = False
    for index,pair in enumerate(data['cuts']):
        if not 1 <= len(pair) <= 2: raise ValueError("invalid path count")
        removed = set()
        for path in pair:
            if not path or len(path) != len(set(path)):
                raise ValueError("empty or nonsimple path")
            if any(type(v) is not int or v < 0 or v >= len(adj) for v in path):
                raise ValueError("invalid path vertex")
            if proxy is not None and proxy in path: raise ValueError("proxy on path")
            used = [tuple(sorted(e)) for e in zip(path,path[1:])]
            if any(e not in edges or e in vertical for e in used):
                raise ValueError("nonedge or vertical edge")
            if len(used) != distance[path[0]][path[-1]]:
                raise ValueError("not an ambient geodesic")
            removed.update(path); distinct.add(min(tuple(path),tuple(reversed(path))))
        parts = components(adj,removed)
        possible = [c for c in parts if all(c & f for f in forced)]
        trace.append({'component_orders':[len(c) for c in parts],
                      'compatible':len(possible)})
        if not possible:
            if index != len(data['cuts'])-1: raise ValueError("unused certificate suffix")
            completed = True
        elif len(possible) != 1 or possible[0] in forced:
            raise ValueError("does not force a new heavy component")
        else:
            forced.append(possible[0])
    if not completed: raise ValueError("no contradiction")
    return {'m':m,'height':h,'vertices':len(adj),'edges':len(edges),
            'anchor_rows':q,'cuts':len(data['cuts']),
            'distinct_paths':len(distinct),'trace':trace}


def map_vertex(m,h,k,v,bottom):
    if v < 2: return 1-v if bottom else v
    i,j = divmod(v-2,h)
    if bottom:
        i = (i+(h%2 == 0)) % m; j = h-1-j
    return vertex(m,k,i,j) if j < k else 1


def lift_vertex(m,h,k,v,bottom):
    if v == 1: raise ValueError("no lift for proxy")
    if v == 0: return 1 if bottom else 0
    i,j = divmod(v-2,k)
    if bottom:
        i = (i-(h%2 == 0)) % m; j = h-1-j
    return vertex(m,h,i,j)


def is_balanced(adj,masses,paths):
    removed = {v for path in paths for v in path}
    return all(2*sum(masses[v] for v in part) <= sum(masses)
               for part in components(adj,removed))


def construct(m,h,masses,kernels):
    if not ((m == 10 and h >= 2) or (m == 12 and h >= 4)):
        raise ValueError("outside the proved range")
    total = sum(masses)
    if total == 0: return [],'zero'
    for pole in (0,1):
        if 2*masses[pole] >= total: return [[pole]],'pole'
    if m == 10 and h == 2:
        data = next(d for d in kernels if d['m']==10 and d['height']==2)
        adj,_,_ = graph(m,h)
        for pair in data['cuts']:
            if is_balanced(adj,masses,pair): return pair,'short'
        raise AssertionError("short kernel failed")
    q,k = ((1,3) if m == 10 else (2,4))
    running = masses[0]
    for j in range(h):
        running += sum(masses[vertex(m,h,i,j)] for i in range(m))
        if 2*running >= total: break
    if q <= j <= h-1-q:
        paths = [[vertex(m,h,i,j) for i in range(m//2)],
                 [vertex(m,h,i,j) for i in range(m//2,m)]]
        return paths,'row'
    bottom = j >= h-q
    data = next(d for d in kernels if d['m']==m and d['height']==k)
    weights = [0]*(m*k+2)
    for v,w in enumerate(masses): weights[map_vertex(m,h,k,v,bottom)] += w
    assert 2*(weights[0]+sum(weights[vertex(m,k,i,j)] for i in range(m) for j in range(q))) >= total
    adj,_,_ = graph(m,k)
    for pair in data['cuts']:
        if is_balanced(adj,weights,pair):
            return [[lift_vertex(m,h,k,v,bottom) for v in path] for path in pair], 'bottom' if bottom else 'top'
    raise AssertionError("boundary kernel failed")


def audit(lengths,masses,paths):
    n=len(masses); adj=[set() for _ in range(n)]; weighted=[[] for _ in range(n)]
    for (a,b),w in lengths.items():
        assert type(w) is int and w > 0
        adj[a].add(b); adj[b].add(a)
        weighted[a].append((b,w)); weighted[b].append((a,w))
    assert len(paths) <= 2
    for path in paths:
        assert path and len(set(path)) == len(path)
        cost=sum(lengths[tuple(sorted(e))] for e in zip(path,path[1:]))
        d={path[0]:0}; heap=[(0,path[0])]
        while heap:
            dv,v=heappop(heap)
            if dv != d[v]: continue
            for u,w in weighted[v]:
                if dv+w < d.get(u,dv+w+1): d[u]=dv+w; heappush(heap,(dv+w,u))
        assert cost == d[path[-1]]
    assert is_balanced(adj,masses,paths)


def fixtures(kernels):
    cases=Counter(); count=0; max_order=0; map_edges=0
    for m,heights in ((10,(2,3,4,5,7,16,33)),(12,(4,5,6,7,16,33))):
        for h in heights:
            adj,edges,vertical=graph(m,h); n=len(adj); max_order=max(max_order,n)
            weights=[[0]*n,[1]*n,[(37*v*v+17*v+11)%101 for v in range(n)]]
            for pole in (0,1):
                w=[1]*n; w[pole]=10*n; weights.append(w)
            for j in range(h):
                w=[0]*n
                for i in range(m): w[vertex(m,h,i,j)]=i+1
                weights.append(w)
            for endpoint in (0,h-1):
                w=[0]*n
                for i in range(m): w[vertex(m,h,i,endpoint)]=1
                w[1 if endpoint==0 else 0]=m
                weights.append(w)
            w=[0]*n
            for j in (0,h-1):
                for i in range(m): w[vertex(m,h,i,j)]=1
            weights.append(w)
            for mode in range(4):
                lengths={}
                for a,b in sorted(edges):
                    if (a,b) in vertical:
                        if mode==3 or (mode==2 and (a+2*b)%3==0): continue
                        lengths[a,b]=1 if mode==0 else 10**6+(3*a+b)**2
                    else: lengths[a,b]=1
                k=3 if m==10 else 4
                if h>=k:
                    _,ke,_=graph(m,k)
                    for bottom in (False,True):
                        for a,b in lengths:
                            x,y=map_vertex(m,h,k,a,bottom),map_vertex(m,h,k,b,bottom)
                            assert x==y or tuple(sorted((x,y))) in ke
                            map_edges+=1
                for w in weights:
                    paths,case=construct(m,h,w,kernels)
                    audit(lengths,w,paths); count+=1; cases[case]+=1
    return {'witnesses':count,'maximum_order':max_order,'cases':dict(sorted(cases.items())),
            'quotient_edge_checks':map_edges}


def main():
    here=Path(__file__).resolve().parent
    raw=(here/'certificate.json').read_bytes(); data=json.loads(raw)
    assert data['schema']=='wider-cylinder-kernels-v1'
    kernels=data['kernels']
    if {(d['m'],d['height']) for d in kernels}!={(10,2),(10,3),(12,4)}:
        raise ValueError("missing kernel")
    checked=[check_kernel(d) for d in kernels]
    rejected=0
    controls=[]
    d=deepcopy(kernels[0]);d['cuts'].pop();controls.append(d)
    for p in ([1],[2,3],[0,1],[0,2,0],[0,2,5]):
        d=deepcopy(kernels[0]);d['cuts'][0]=[p];controls.append(d)
    for d in controls:
        try: check_kernel(d)
        except ValueError: rejected+=1
        else: raise AssertionError("invalid control accepted")
    result={'status':'PASS','certificate_sha256':sha256(raw).hexdigest(),
            'kernels':checked,'fixtures':fixtures(kernels),'rejected_controls':rejected}
    if sys.argv[1:]==['--check']:
        assert result==json.loads((here/'expected.json').read_text())
    elif sys.argv[1:]: raise SystemExit('usage: verify.py [--check]')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__': main()
