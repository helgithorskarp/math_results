"""Exact, solver-free replay of two full-dimensional radial price boxes.

Python 3.11+, standard library only; assertions must be enabled.
The README supplies the strict-chamber, limiting, leaf and mass reductions.
"""
from collections import deque
from fractions import Fraction
from functools import reduce
from heapq import heappop, heappush
from itertools import combinations
from math import gcd, lcm
from pathlib import Path
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent



def components(adj,removed):
    unseen=set(adj)-removed;out=[]
    while unseen:
        K={unseen.pop()};todo=list(K)
        while todo:
            v=todo.pop();new=adj[v]&unseen;unseen-=new;K|=new;todo.extend(new)
        out.append(K)
    return out

def fixture():
    faces=[[0,4,6,2],[1,3,7,5],[0,1,5,4],[2,6,7,3],[0,2,3,1],[4,5,7,6]]
    cube=sorted({tuple(sorted((a,b))) for face in faces for a,b in zip(face,face[1:]+face[:1])})
    labels={e:14+i for i,e in enumerate(cube)};triangles=[];core=set();edges=set()
    for i,face in enumerate(faces):
        f=8+i
        for a,b in zip(face,face[1:]+face[:1]):
            z=labels[tuple(sorted((a,b)))];triangles.extend([(a,z,f),(z,b,f)])
            core.add((a,f))
    darts=set()
    for face in triangles:
        for a,b in zip(face,face[1:]+face[:1]):
            assert (a,b) not in darts;darts.add((a,b));edges.add(tuple(sorted((a,b))))
    assert all((b,a) in darts for a,b in darts)
    adj={v:set() for v in range(26)}
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    # One link cycle at each vertex, with a connected one-skeleton and
    # Euler characteristic two, certifies the supplied spherical embedding.
    for v in adj:
        rotation={}
        for face in triangles:
            if v in face:
                i=face.index(v);a,b=face[(i+1)%3],face[(i+2)%3]
                assert a not in rotation;rotation[a]=b
        assert set(rotation)==adj[v] and set(rotation.values())==adj[v]
        first=min(rotation);u=first;visited=set()
        while u not in visited:visited.add(u);u=rotation[u]
        assert u==first and visited==adj[v]
    assert len(components(adj,set()))==1
    assert len(core)==24 and len(edges)==72 and len(triangles)==48 and 26-72+48==2
    return adj,sorted(edges),sorted(core),triangles


def normalized(vector):
    q=list(map(Fraction,vector));scale=lcm(*(x.denominator for x in q))
    ints=[int(x*scale) for x in q];div=reduce(gcd,map(abs,ints))
    return tuple(x//div for x in ints) if div else tuple(ints)

class Encoding:
    def __init__(self):self.next=1;self.linear={};self.vector={};self.clauses=[]
    def new(self):
        result=self.next;self.next+=1;return result
    def atom(self,vector):
        v=normalized(vector)
        if not any(v[:-1]):return v[-1]>=0
        if v not in self.linear:
            index=self.new();self.linear[v]=index;self.vector[index]=v
        return self.linear[v]
    @staticmethod
    def negate(lit):return not lit if type(lit) is bool else -lit
    def inequality(self,vector,strict=False):
        if strict:return self.negate(self.atom([-q for q in vector]))
        return self.atom(vector)
    def add(self,clause):
        if any(x is True for x in clause):return
        c=set(x for x in clause if x is not False)
        if any(-x in c for x in c):return
        self.clauses.append(tuple(sorted(c)))

def rup(clauses,proof,variables):
    """Replay additions by reverse unit propagation; deletions are optional."""
    database=[tuple(c) for c in clauses]
    for row in proof:
        assert all(type(lit) is int and 1<=abs(lit)<=variables for lit in row)
        assert len(set(row))==len(row)
        assigned={};queue=deque(-x for x in row);conflict=False
        while True:
            while queue:
                literal=queue.popleft();v=abs(literal);value=literal>0
                if v in assigned:
                    if assigned[v]!=value:conflict=True;break
                else:assigned[v]=value
            if conflict:break
            changed=False
            for clause in database:
                open_lits=[];satisfied=False
                for literal in clause:
                    v=abs(literal)
                    if v not in assigned:open_lits.append(literal)
                    elif assigned[v]==(literal>0):satisfied=True;break
                if satisfied:continue
                if not open_lits:conflict=True;break
                if len(open_lits)==1:queue.append(open_lits[0]);changed=True
            if conflict:break
            if not changed:break
        assert conflict,'RUP addition failed'
        database.append(tuple(row))
    assert proof and proof[-1]==[],'proof must end with the empty clause'
    return len(proof)


ADJ, ALL_EDGES, RADIAL, FACES = fixture()
ACTIVE = {14, 19, 22}
MARKS = sorted(set(range(14, 26)) - ACTIVE)
CORE = sorted(set(range(14)) | ACTIVE)
SHORTCUT = [(10, 14), (10, 22), (11, 19), (12, 14), (12, 19), (13, 22)]
VARIABLE_EDGES = RADIAL + SHORTCUT
DIM = len(VARIABLE_EDGES)
PRICES = {
    'A': [14,38,7,23,20,17,8,30,11,21,14,29,10,28,36,4,3,7,30,6,2,4,9,5],
    'B': [7,10,4,8,7,11,9,6,16,14,3,23,3,16,15,16,3,10,22,9,12,3,12,7],
}
assert len(MARKS) == 9 and DIM == 30 and set(SHORTCUT) <= set(ALL_EDGES)



def incidence(path):
    vector = [0] * (DIM + 1)
    for a, b in zip(path, path[1:]):
        vector[VARIABLE_EDGES.index(tuple(sorted((a, b))))] += 1
    return vector

def radial_structure(name):
    prices = dict(zip(RADIAL, PRICES[name]))
    adj = {v: {} for v in range(14)}
    for (a, b), w in prices.items():
        adj[a][b] = adj[b][a] = w
    distances, paths = {}, {}
    for root in range(14):
        d = {root: 0}
        heap = [(0, root)]
        while heap:
            value, v = heappop(heap)
            if value != d[v]:
                continue
            for u, weight in adj[v].items():
                new = value + weight
                if u not in d or new < d[u]:
                    d[u] = new
                    heappush(heap, (new, u))
        assert len(d) == 14
        distances[root] = d
        for target in range(14):
            path = [target]
            while path[-1] != root:
                v = path[-1]
                pred = [u for u, w in adj[v].items() if d[u] + w == d[v]]
                assert len(pred) == 1, 'baseline must have unique radial geodesics'
                path.append(pred[0])
            paths[root, target] = path[::-1]
    cone = set()
    for root in range(14):
        potential = {v: incidence(paths[root, v]) for v in range(14)}
        for i, (a, b) in enumerate(RADIAL):
            for u, v in ((a, b), (b, a)):
                row = [p - q for p, q in zip(potential[u], potential[v])]
                row[i] += 1
                if any(row):
                    assert sum(p * w for p, w in zip(row, PRICES[name])) > 0
                    cone.add(tuple(row))
                else:
                    # Exactly the forward edge of this rooted shortest-path tree.
                    assert paths[root, u] + [v] == paths[root, v]
    return prices, distances, paths, sorted(cone)

def catalog(prices, distances):
    adj = {v: set() for v in CORE}
    for a, b in VARIABLE_EDGES:
        adj[a].add(b)
        adj[b].add(a)
    out = {(a, b): [] for a in CORE for b in CORE if a <= b}
    for source in CORE:
        def extend(path, start, length):
            v = path[-1]
            if v >= source:
                out[source, v].append(tuple(path))
            for u in sorted(adj[v]):
                if u in path:
                    continue
                if v < 14 and u < 14:
                    new = length + prices[tuple(sorted((u, v)))]
                    assert start is not None
                    if new != distances[start][u]:
                        continue
                    extend(path + [u], start, new)
                elif u < 14:
                    extend(path + [u], u, 0)
                else:
                    extend(path + [u], None, 0)
        extend([source], source if source < 14 else None, 0)
    assert all(out.values())
    return out

def build(data):
    name = data['metric']
    assert name in PRICES
    prices, distances, radial_paths, cone = radial_structure(name)
    routes = catalog(prices, distances)
    enc = Encoding()
    parents = {(z, p): enc.new() for z in MARKS for p in sorted(ADJ[z])}
    for z in MARKS:
        group = [parents[z, p] for p in sorted(ADJ[z])]
        enc.add(group)
        for a, b in combinations(group, 2):
            enc.add([-a, -b])
    for i in range(DIM):
        vector = [0] * (DIM + 1)
        vector[i] = 1
        enc.add([enc.inequality(vector, True)])
    for vector in cone:
        enc.add([enc.inequality(vector, True)])
    if 'relative_radius' in data:
        radius = Fraction(data['relative_radius'])
        assert 0 < radius < 1
        safe_radius = min(Fraction(sum(a * w for a, w in zip(row, PRICES[name])),
                                   sum(abs(a) * w for a, w in zip(row, PRICES[name])))
                          for row in cone)
        assert radius <= safe_radius
        for i, w in enumerate(PRICES[name]):
            lower = [0] * (DIM + 1)
            lower[i], lower[-1] = 1, -(1 - radius) * w
            upper = [0] * (DIM + 1)
            upper[i], upper[-1] = -1, (1 + radius) * w
            enc.add([enc.inequality(lower)])
            enc.add([enc.inequality(upper)])
    marked = set(MARKS)
    for pair in data['pairs']:
        assert len(pair) == 2
        assert all(len(K & marked) <= 4 for K in components(ADJ, set(pair[0]) | set(pair[1])))
        conditions = set()
        core_paths = []
        for path in pair:
            assert path and len(path) == len(set(path)) and all(type(v) is int and v in ADJ for v in path)
            assert all(b in ADJ[a] for a, b in zip(path, path[1:]))
            assert all(v in CORE for v in path[1:-1])
            if len(path) > 1 and path[0] in marked:
                conditions.add((path[0], path[1]))
            if len(path) > 1 and path[-1] in marked:
                conditions.add((path[-1], path[-2]))
            middle = [v for v in path if v in CORE]
            if not middle:
                assert len(path) == 1 and path[0] in marked
                continue
            if middle[0] > middle[-1]:
                middle.reverse()
            assert tuple(middle) in routes[middle[0], middle[-1]]
            core_paths.append(middle)
        clause = [-parents[z, p] for z, p in sorted(conditions)]
        for path in core_paths:
            left = incidence(path)
            for other in routes[path[0], path[-1]]:
                right = incidence(other)
                clause.append(enc.inequality([a - b for a, b in zip(left, right)], True))
        enc.add(clause)
    counts = {'metric': name, 'dimension': DIM, 'radial_cone_inequalities': len(cone),
              'core_routes': sum(map(len, routes.values())), 'templates': len(data['pairs']),
              'parent_assignments': 4 ** 9, 'base_clauses': len(enc.clauses)}
    if 'relative_radius' in data:
        counts['relative_radius'] = str(radius)
        counts['maximum_radial_box_radius'] = str(safe_radius)
    return enc, counts

def verify_region(data):
    enc, counts = build(data)
    for index, vector in data['extra_linear_atoms']:
        assert type(index) is int and index == enc.next and len(vector) == DIM + 1
        assert all(type(v) is int for v in vector) and normalized(vector) == tuple(vector)
        assert enc.atom(vector) == index
    for row in data['farkas']:
        assert row
        total = [Fraction(0)] * (DIM + 1)
        strict = False
        for literal, multiplier in row:
            assert type(literal) is int and abs(literal) in enc.vector
            weight = Fraction(multiplier)
            assert weight > 0
            vector = enc.vector[abs(literal)]
            sign = 1 if literal > 0 else -1
            total = [a + weight * sign * b for a, b in zip(total, vector)]
            strict |= literal < 0
        assert all(v == 0 for v in total[:-1])
        assert total[-1] < 0 or (total[-1] == 0 and strict)
        enc.add([-literal for literal, multiplier in row])
    counts.update({'linear_atoms': len(enc.linear), 'farkas_lemmas': len(data['farkas']),
                   'rup_additions': rup(enc.clauses, data['rup'], enc.next - 1)})
    return {'status': 'PASS', **counts}


def verify_unit(data):
    assert data['mark'] == 15 and len(data['templates']) == 4
    assert {row['parent'] for row in data['templates']} == ADJ[15]
    costs = {edge: 1 for edge in RADIAL} | {edge: 0 for edge in SHORTCUT}
    infinity = 1 + sum(costs.values())
    d = {a: {b: 0 if a == b else infinity for b in CORE} for a in CORE}
    for (a, b), w in costs.items():
        d[a][b] = d[b][a] = w
    for k in CORE:
        for a in CORE:
            for b in CORE:
                d[a][b] = min(d[a][b], d[a][k] + d[k][b])
    for row in data['templates']:
        parent = row['parent']
        assert type(parent) is int and parent in ADJ[15] and len(row['paths']) == 2
        for path in row['paths']:
            assert path and len(path) == len(set(path)) and all(v in ADJ for v in path)
            assert all(b in ADJ[a] for a, b in zip(path, path[1:]))
            core = list(path)
            if core[0] in MARKS:
                assert len(core) > 1 and core[0] == 15 and core[1] == parent
                core.pop(0)
            if core[-1] in MARKS:
                assert len(core) > 1 and core[-1] == 15 and core[-2] == parent
                core.pop()
            assert core and all(v < 14 for v in core)
            assert len(core) - 1 == d[core[0]][core[-1]]
        marked = set(MARKS)
        sizes = sorted(len(part & marked) for part in components(ADJ, set(row['paths'][0]) | set(row['paths'][1])))
        assert sizes == row['component_masses'] == [4, 4]
    return {'status': 'PASS', 'metric': 'U', 'templates': 4, 'mark': 15, 'parent_assignments': 4 ** 9}


def main():
    start = time.monotonic()
    results = []
    for name, radius, templates, farkas, proof_steps in [('A', '1/57', 47, 437, 48), ('B', '1/32', 67, 723, 142)]:
        data = json.loads((HERE / ('certificate_' + name + '.json')).read_text())
        assert data['metric'] == name and data['relative_radius'] == radius
        result = verify_region(data)
        assert result['templates'] == templates and result['farkas_lemmas'] == farkas
        assert result['rup_additions'] == proof_steps
        results.append(result)
    unit = verify_unit(json.loads((HERE / 'certificate_U.json').read_text()))
    hashes = {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
              for name in ('certificate_A.json', 'certificate_B.json', 'certificate_U.json')}
    print(json.dumps({'status': 'PASS', 'vertices': 26, 'edges': 72, 'faces': 48,
                      'price_boxes': results, 'unit_case': unit,
                      'certificate_sha256': hashes,
                      'seconds': round(time.monotonic() - start, 6)}, indent=2))


if __name__ == '__main__':
    main()
