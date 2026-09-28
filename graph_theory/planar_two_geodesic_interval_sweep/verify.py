#!/usr/bin/env python3
"""Exact regression checks; the universal proof is the written planar sweep."""
import argparse
from collections import deque
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path
import random


HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def adjacency(n, edges):
    adj = [dict() for _ in range(n)]
    for u, v, length in edges:
        need(0 <= u < n and 0 <= v < n and u != v and length > 0, 'edge')
        need(v not in adj[u], 'duplicate edge')
        adj[u][v] = adj[v][u] = length
    return adj


def apsp(adj):
    n = len(adj)
    infinity = 1 + sum(sum(row.values()) for row in adj)
    dist = [[infinity]*n for _ in range(n)]
    for u, row in enumerate(adj):
        dist[u][u] = 0
        for v, length in row.items():
            dist[u][v] = length
    for middle in range(n):
        for u in range(n):
            for v in range(n):
                dist[u][v] = min(dist[u][v], dist[u][middle] + dist[middle][v])
    need(all(max(row) < infinity for row in dist), 'disconnected input')
    return dist


def components(adj, deleted):
    remaining = set(range(len(adj))) - set(deleted)
    answer = []
    while remaining:
        stack = [remaining.pop()]
        component = []
        while stack:
            u = stack.pop()
            component.append(u)
            for v in adj[u]:
                if v in remaining:
                    remaining.remove(v)
                    stack.append(v)
        answer.append(tuple(component))
    return answer


def check_sphere(adj, faces):
    darts = set()
    rotations = [dict() for _ in adj]
    for face in faces:
        need(len(face) >= 3 and len(set(face)) == len(face), 'face')
        for i, u in enumerate(face):
            v, prev = face[(i+1) % len(face)], face[i-1]
            need(v in adj[u] and (u, v) not in darts, 'dart')
            darts.add((u, v))
            need(prev not in rotations[u], 'rotation entry')
            rotations[u][prev] = v
    need(darts == {(u, v) for u in range(len(adj)) for v in adj[u]}, 'dart cover')
    for u, rotation in enumerate(rotations):
        need(set(rotation) == set(rotation.values()) == set(adj[u]), 'rotation')
        start = min(rotation)
        reached, v = set(), start
        while v not in reached:
            reached.add(v)
            v = rotation[v]
        need(v == start and reached == set(adj[u]), 'split vertex link')
    need(len(adj) - len(darts)//2 + len(faces) == 2, 'not spherical')
    need(len(components(adj, [])) == 1, 'disconnected embedding')


def paths_to(adj, dist, source, terminals):
    answer = set()
    for target in terminals:
        def extend(path):
            u = path[-1]
            if u == target:
                answer.add(tuple(path))
                return
            for v, length in sorted(adj[u].items()):
                if (dist[source][u] + length == dist[source][v]
                        and dist[source][v] + dist[v][target] == dist[source][target]):
                    extend(path + [v])
        extend([source])
    return sorted(answer)


def check_path(adj, dist, path):
    need(path and len(set(path)) == len(path), 'simple path')
    need(all(v in adj[u] for u, v in zip(path, path[1:])), 'path edge')
    need(sum(adj[u][v] for u, v in zip(path, path[1:]))
         == dist[path[0]][path[-1]], 'ambient shortestness')


def cut_table(adj, paths):
    return {(i, j): components(adj, set(p) | set(paths[j]))
            for i, p in enumerate(paths) for j in range(i, len(paths))}


def mass_cases(n, support, rng, exhaustive):
    support = sorted(support)
    if exhaustive:
        for bits in product((0, 1), repeat=len(support)):
            mass = [0]*n
            for v, value in zip(support, bits):
                mass[v] = value
            yield mass
    else:
        yield [int(v in support) for v in range(n)]
        yield [0]*n
    for point in support:
        yield [int(v == point) for v in range(n)]
    for _ in range(12):
        mass = [0]*n
        for v in support:
            mass[v] = rng.randrange(20)
        yield mass
    for _ in range(3):
        mass = [0]*n
        for v in support:
            mass[v] = Fraction(rng.randrange(20), rng.randrange(1, 8))
        yield mass


def check_case(n, edges, faces, source, terminals, kind, rng, result, exhaustive=False):
    adj = adjacency(n, edges)
    dist = apsp(adj)
    check_sphere(adj, faces)
    support = {v for v in range(n) if any(dist[source][v] + dist[v][z]
                                        == dist[source][z] for z in terminals)}
    paths = paths_to(adj, dist, source, terminals)
    for path in paths:
        check_path(adj, dist, path)
    result['checked_geodesics'] += len(paths)
    result['zero_mass_outside_support_vertices'] += n - len(support)
    if kind == 'face':
        need(any(set(face) == set(terminals) for face in faces), 'not a face')
        height = 1 + max(dist[source])
        augmented = adjacency(n+1, edges + [(n, z, height-dist[source][z])
                                           for z in sorted(terminals)])
        aug_dist = apsp(augmented)
        need(aug_dist[source][:n] == dist[source] and aug_dist[source][n] == height,
             'augmentation distances')
        interval = {v for v in range(n) if aug_dist[source][v] + aug_dist[v][n] == height}
        need(interval == support, 'facial interval identification')
        augmented_paths = paths_to(augmented, aug_dist, source, [n])
        need({p[:-1] for p in augmented_paths} == set(paths), 'trimming bijection')
        for path in augmented_paths:
            check_path(augmented, aug_dist, path)
        result['face_augmentations'] += 1
    cuts = cut_table(adj, paths)
    result['path_pairs_checked'] += len(cuts)
    for mass in mass_cases(n, support, rng, exhaustive):
        total = sum(mass)
        thresholds = [total - sum(mass[v] for v in p) for p in paths]
        good = set()
        for (i, j), comps in cuts.items():
            largest = max((sum(mass[v] for v in comp) for comp in comps), default=0)
            if 2*largest <= thresholds[i]:
                good.add(i)
            if 2*largest <= thresholds[j]:
                good.add(j)
        need(len(good) == len(paths), ('prescribed-path failure', kind, n, source, terminals, mass))
        result['mass_assignments'] += 1
        result['prescribed_path_mass_checks'] += len(paths)
    result[kind + '_fixtures'] += 1


def annulus(k, cap=False):
    b = lambda i: 1 + i % k
    c = lambda i: 1 + k + i % k
    edges, faces = [], []
    for i in range(k):
        edges += [(0,b(i),1), (b(i),b(i+1),1), (c(i),c(i+1),1),
                  (b(i),c(i),1), (b(i),c(i+1),1)]
        faces += [(0,b(i),b(i+1)), (b(i),c(i+1),b(i+1)), (b(i),c(i),c(i+1))]
    n = 2*k+1
    if cap:
        for i in range(k):
            edges.append((n,c(i),1))
            faces.append((n,c(i+1),c(i)))
        n += 1
    else:
        faces.append(tuple(c(i) for i in reversed(range(k))))
    return n, edges, faces


def irregular_patch(active, rng):
    gaps = [rng.randrange(1, 4) for _ in range(active)]
    positions = [sum(gaps[:i]) for i in range(active)]
    sources = [positions[i] for i in range(active) for _ in range(rng.randrange(1, 4))]
    m, k = len(sources), sum(gaps)
    b = lambda i: 1 + i % m
    c = lambda i: 1 + m + i % k
    edges = [(0,b(i),1) for i in range(m)]
    edges += [(b(i),b(i+1),rng.randrange(1, 5)) for i in range(m)]
    edges += [(b(i),c(sources[i]),1) for i in range(m)]
    edges += [(c(i),c(i+1),rng.randrange(1, 7)) for i in range(k)]
    faces = [(0,b(i),b(i+1)) for i in range(m)]
    for i in range(m):
        a, z = sources[i], sources[(i+1) % m]
        arc = [c(a)]
        while a != z:
            a = (a+1) % k
            arc.append(c(a))
        faces.append(tuple([b(i)] + arc + [b(i+1)]))
    faces.append(tuple(c(i) for i in reversed(range(k))))
    return 1+m+k, edges, faces, list(range(1+m, 1+m+k))


def grid(rows, cols, weighted=False, diagonals=False, pocket=False, rng=None):
    n = rows*cols
    level = [3*(v//cols) + 2*(v % cols) for v in range(n)]
    edges, faces = [], []
    for y in range(rows):
        for x in range(cols):
            u = y*cols+x
            for v in ([u+1] if x+1<cols else []) + ([u+cols] if y+1<rows else []):
                edges.append((u,v,abs(level[v]-level[u]) if weighted else 1))
    for y in range(rows-1):
        for x in range(cols-1):
            u = y*cols+x
            v, w, z = u+1, u+cols+1, u+cols
            if diagonals:
                edges.append((u,w,abs(level[w]-level[u])+1 if weighted else 3))
                faces += [(u,v,w), (u,w,z)]
            else:
                faces.append((u,v,w,z))
    border = list(range(cols)) + [y*cols+cols-1 for y in range(1,rows)]
    border += list(range(n-2,n-cols-1,-1)) + [y*cols for y in range(rows-2,0,-1)]
    faces.append(tuple(reversed(border)))
    if pocket:
        face = faces.pop(0)
        edges += [(n,v,100) for v in face]
        faces += [(face[i],face[(i+1) % len(face)],n) for i in range(len(face))]
        n += 1
    if rng is not None:
        edges = [(u,v,rng.randrange(1,8)) for u,v,_ in edges]
    return n, edges, faces, border


def obstruction_controls(result):
    n, edges, faces = annulus(5, cap=True)
    adj = adjacency(n, edges)
    dist = apsp(adj)
    paths = sorted({p for s in range(n) for p in paths_to(adj,dist,s,range(s,n))})
    for path in paths:
        check_path(adj,dist,path)
        need(max(map(len,components(adj,path)), default=0) > n//2, 'one path suffices')
    for v in range(n):
        rim = set(adj[v])
        need(len(rim) == 5 and all(len(set(adj[u]) & rim) == 2 for u in rim), 'wheel rim')
        target = rim | {v}
        need(all(dist[a][b] <= 2 for a in target for b in target), 'wheel metric')
        traces = {frozenset(target.intersection(path)) for path in paths}
        need(all(target != a | b for a in traces for b in traces), 'neighborhood covered')
        result['icosahedron_blocked_neighborhoods'] += 1
    triangles = {frozenset(triple) for triple in combinations(range(n),3)
                 if all(v in adj[u] for u,v in combinations(triple,2))}
    need(triangles == {frozenset(face) for face in faces}, 'unlisted triangle')
    need(all(max(map(len,components(adj,f))) > n//2 for f in faces), 'facial half separator')
    result['icosahedron_failed_single_geodesics'] = len(paths)
    # Nonplanar capped K_(6,6): every vertex lies in I(0,13), but no pair works.
    edges = [(0,1+i,1) for i in range(6)] + [(7+j,13,1) for j in range(6)]
    edges += [(1+i,7+j,1) for i in range(6) for j in range(6)]
    adj = adjacency(14,edges)
    dist = apsp(adj)
    need(all(dist[0][v]+dist[v][13] == 3 for v in range(14)), 'nonplanar interval')
    paths = paths_to(adj,dist,0,[13])
    cuts = cut_table(adj,paths)
    need(all(max(map(len,c)) > 7 for c in cuts.values()), 'nonplanar control')
    result['nonplanar_failed_pairs'] = len(cuts)
    # A positive mass outside the interval cannot be erased by interval paths.
    n,edges,faces,_ = grid(3,4,pocket=True)
    adj = adjacency(n,edges)
    dist = apsp(adj)
    need(dist[0][n-1]+dist[n-1][11] > dist[0][11], 'pocket on interval')
    paths = paths_to(adj,dist,0,[11])
    cuts = cut_table(adj,paths)
    need(all(any(n-1 in comp for comp in comps) for comps in cuts.values()), 'pocket removed')
    result['unsupported_mass_control'] = 1


def run():
    result = dict(interval_fixtures=0, face_fixtures=0, face_augmentations=0,
                  checked_geodesics=0, path_pairs_checked=0, mass_assignments=0,
                  prescribed_path_mass_checks=0, zero_mass_outside_support_vertices=0,
                  icosahedron_blocked_neighborhoods=0)
    rng = random.Random(2026092807)
    for k in range(3,9):
        n,edges,faces = annulus(k,cap=True)
        check_case(n,edges,faces,0,[n-1],'interval',rng,result,exhaustive=(n<=12))
    for rows,cols in ((2,3),(3,3),(3,4),(4,5)):
        for weighted,diagonals,pocket in ((False,False,False),(True,True,False),(True,True,True)):
            n,edges,faces,border = grid(rows,cols,weighted,diagonals,pocket)
            check_case(n,edges,faces,0,[rows*cols-1],'interval',rng,result,
                       exhaustive=(rows*cols<=12))
    for k in range(3,9):
        n,edges,faces = annulus(k)
        check_case(n,edges,faces,0,list(range(k+1,2*k+1)),'face',rng,result,
                       exhaustive=(k<=4))
    for active in range(3,9):
        for _ in range(3):
            n,edges,faces,terminals = irregular_patch(active,rng)
            check_case(n,edges,faces,0,terminals,'face',rng,result)
    for source in (0,5):
        for random_metric in (False,True):
            n,edges,faces,border = grid(3,4,True,True,True,rng if random_metric else None)
            check_case(n,edges,faces,source,border,'face',rng,result)
    obstruction_controls(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='compare expected.json')
    args = parser.parse_args()
    result = run()
    if args.check:
        need(result == json.loads((HERE/'expected.json').read_text()), 'expected output')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
