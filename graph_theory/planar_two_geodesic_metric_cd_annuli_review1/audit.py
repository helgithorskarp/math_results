#!/usr/bin/env python3
"""Independent finite audit of the weighted D^5 metric-annulus control.

No import from the target contribution.  Rebuilds the graph, shortest
distances, candidate paths, face structure, treewidth obstruction, and
all 4^7 bounded mass profiles on seven selected vertices.
"""

from functools import lru_cache
from itertools import combinations, product

R = 0
A = tuple(range(1, 6))
C = tuple(range(6, 11))
U, V = 11, 12
K = tuple(range(13, 18))
N = 18
g = [dict() for _ in range(N)]


def add(x, y, length):
    assert x != y and length > 0 and y not in g[x]
    g[x][y] = g[y][x] = length


for i in range(5):
    add(R, A[i], 4)
    add(A[i], A[(i + 1) % 5], 4)
    add(C[i], A[i], 4)
    for endpoint in (R, A[i], A[(i + 1) % 5]):
        add(K[i], endpoint, 4)
    if i != 2:
        add(C[i], C[(i + 1) % 5], 4)
add(C[2], U, 3)
add(U, V, 2)
add(V, C[3], 3)
assert sum(map(len, g)) // 2 == 37


def distances(graph):
    n = len(graph)
    inf = 10**9
    d = [[0 if i == j else graph[i].get(j, inf) for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    return d


D = distances(g)
wheel = [dict() for _ in range(6)]
for x in range(6):
    for y, length in g[x].items():
        if y < 6:
            wheel[x][y] = length
WHEEL_D = distances(wheel)
for x in range(6):
    for y in range(6):
        assert D[x][y] == WHEEL_D[x][y]
for i in range(5):
    for x in range(6):
        assert D[C[i]][x] == 4 + WHEEL_D[A[i]][x]


def path_weight(path):
    assert path and len(path) == len(set(path))
    return sum(g[x][y] for x, y in zip(path, path[1:]))


def geodesic(path):
    assert path_weight(path) == D[path[0]][path[-1]], path


def wheel_path(s, t):
    route = [s]
    while route[-1] != t:
        x = route[-1]
        options = [y for y, w in wheel[x].items()
                   if w + WHEEL_D[y][t] == WHEEL_D[x][t]]
        route.append(min(options))
    return tuple(route)


def parts(deleted, graph=g):
    left = set(range(len(graph))) - set(deleted)
    out = []
    while left:
        s = left.pop()
        part = {s}
        todo = [s]
        while todo:
            new = set(graph[todo.pop()]) & left
            left.difference_update(new)
            part.update(new)
            todo.extend(new)
        out.append(part)
    return out


def candidates():
    anchor = (R, A[0], C[0])
    result = []
    for j in range(5):
        root = (R, A[j], C[j])
        geodesic(root)
        result.append((anchor, root))
        a, b = A[j], A[(j+1)%5]
        c, d = C[j], C[(j+1)%5]
        arc = (c, U, V, d) if j == 2 else (c, d)
        x = [0]
        for u, v in zip(arc, arc[1:]):
            x.append(x[-1]+g[u][v])
        ell = x[-1]
        ea = (C[0],) + wheel_path(A[0], a)
        eb = (C[0],) + wheel_path(A[0], b)
        delta = WHEEL_D[a][b]
        z = ell + WHEEL_D[R][b] - WHEEL_D[R][a]
        zf = ell-delta if R in ea else z
        zb = ell+delta if R in eb else z
        q = next(i for i, coord in enumerate(x) if 2*coord >= zf)
        p = max(i for i, coord in enumerate(x) if 2*coord <= zb)
        assert q <= p+1
        first = ((b,) if R in ea else wheel_path(R,b)) + tuple(reversed(arc[q:]))
        second = ((a,) if R in eb else wheel_path(R,a)) + arc[:p+1]
        for pair in ((ea, first), (eb, second)):
            assert set(anchor) <= set(pair[0]) | set(pair[1])
            for path in pair: geodesic(path)
            result.append(pair)
    result.append((anchor, anchor))
    return result


PAIRS = candidates()
assert len(PAIRS) == 16

# A zero-cost attachment edge is compatible with core isometry: r--K_0
# can cost zero while both outer incidences at K_0 still cost four.
zero_extension = [dict(row) for row in g]
zero_extension[R][K[0]] = zero_extension[K[0]][R] = 0
zero_d = distances(zero_extension)
assert all(zero_d[x][y] == D[x][y] for x in range(13) for y in range(13))
assert all(path_weight(path) == zero_d[path[0]][path[-1]]
           for pair in PAIRS for path in pair)


def max_mass(pair, masses):
    removed = set(pair[0]) | set(pair[1])
    return max((sum(masses[v] for v in part) for part in parts(removed)), default=0)


control = [0]*N
for v, value in ((A[1],2),(A[4],2),(K[2],1),(U,1),(V,1)):
    control[v] = value
assert sum(control) == 7
fixed = (R,A[0],C[0])
old = ((R,A[2],C[2],U),(R,A[3],C[3],V),
       (A[2],A[3],C[3]),(A[3],A[2],C[2]))
for path in old:
    geodesic(path)
    assert max_mass((fixed,path),control) == 4
assert [max_mass(pair,control) for pair in PAIRS[7:9]] == [2,2]


faces = []
for i in range(5):
    a,b=A[i],A[(i+1)%5]
    faces.extend(((R,a,K[i]),(a,b,K[i]),(b,R,K[i])))
    arc = (C[i],U,V,C[(i+1)%5]) if i==2 else (C[i],C[(i+1)%5])
    faces.append((a,)+arc+(b,))
faces.append(tuple(v for i in range(5) for v in
                   ((C[i],U,V) if i==2 else (C[i],)))[::-1])
darts = [(x,y) for face in faces for x,y in zip(face,face[1:]+face[:1])]
assert len(faces)==21 and len(darts)==74 and len(set(darts))==74
assert set(darts)=={(x,y) for x in range(N) for y in g[x]}
assert N-37+len(faces)==2
for v in range(N):
    successor={face[i-1]:face[(i+1)%len(face)] for face in faces for i,x in enumerate(face) if x==v}
    assert set(successor)==set(g[v])
    seen=set();x=min(successor)
    while x not in seen: seen.add(x);x=successor[x]
    assert x==min(successor) and seen==set(g[v])
assert min(max_mass((face,()),control) for face in faces)==5

suppressed = {x:{y for y in g[x] if y not in (U,V)}
              for x in range(N) if x not in (U,V)}
suppressed[C[2]].add(C[3]); suppressed[C[3]].add(C[2])
connectivity_checks=0
for size in range(3):
    for removed in combinations(suppressed,size):
        left=set(suppressed)-set(removed)
        seed=left.pop(); seen={seed};todo=[seed]
        while todo:
            for v in suppressed[todo.pop()] & left:
                left.remove(v);seen.add(v);todo.append(v)
        assert not left
        connectivity_checks+=1
assert connectivity_checks==137


simple = [set() for _ in range(11)]
for x in range(11):
    simple[x] = {y for y in g[x] if y<11}
simple[C[2]].add(C[3]);simple[C[3]].add(C[2])


@lru_cache(None)
def width_three(state):
    if not state: return True
    vertices = tuple(v for v,_ in state)
    graph = {v:set(ns) for v,ns in state}
    for v in vertices:
        near=graph[v]
        if len(near)>3: continue
        child={u:graph[u]-{v} for u in vertices if u!=v}
        for u,w in combinations(near,2):
            child[u].add(w);child[w].add(u)
        key=tuple((u,tuple(sorted(ns))) for u,ns in sorted(child.items()))
        if width_three(key): return True
    return False


start=tuple((v,tuple(sorted(simple[v]))) for v in range(11))
assert not width_three(start)


support = (A[1],A[2],A[3],A[4],K[2],U,V)
residuals = [parts(set(pair[0])|set(pair[1])) for pair in PAIRS]
profiles=0
for values in product(range(4),repeat=len(support)):
    masses=[0]*N
    for v,value in zip(support,values): masses[v]=value
    total=sum(values)
    M=total-sum(masses[v] for v in fixed)
    twice_h=max(M,2*masses[K[2]])
    assert any(all(2*sum(masses[v] for v in part)<=twice_h for part in component_list)
               for component_list in residuals)
    profiles+=1

print(f"vertices={N} edges=37 faces={len(faces)} geodesic_pairs={len(PAIRS)} "
      f"control_old_max=4 control_new_max=2 facial_min_max=5 "
      f"three_connectivity_checks={connectivity_checks} treewidth_at_least=4 "
      f"mass_profiles={profiles} zero_extension=PASS PASS")
