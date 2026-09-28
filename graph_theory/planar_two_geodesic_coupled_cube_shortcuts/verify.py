"""Exact, solver-free replay for three coupled radial-cube shortcuts.

Python 3.11+, standard library only; run with assertions enabled.
No discovery code, solver, network access, or external input is needed.
The accompanying README supplies the reductions over continuous parameters.
"""
from collections import deque
from fractions import Fraction
from functools import reduce
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


ADJ, EDGES, CORE, FACES = fixture()
MARKS = set(range(17, 26))
VARIABLE_EDGES = [(8,15),(8,16),(10,14),(10,16),(12,14),(12,15)]
PRICE_A = [14,38,7,23,20,17,8,30,11,21,14,29,10,28,36,4,3,7,30,6,2,4,9,5]
assert all(len(ADJ[z]) == 4 for z in MARKS)
assert set(VARIABLE_EDGES) <= set(EDGES)



def floyd(prices):
    infinity = sum(prices.values()) + 1
    d = [[0 if a == b else infinity for b in range(14)] for a in range(14)]
    for (a, b), w in prices.items():
        d[a][b] = d[b][a] = w
    for k in range(14):
        for a in range(14):
            for b in range(14):
                d[a][b] = min(d[a][b], d[a][k] + d[k][b])
    return d

def catalog(prices):
    adj = {v: set() for v in range(17)}
    for a, b in list(prices) + VARIABLE_EDGES:
        adj[a].add(b)
        adj[b].add(a)
    d = floyd(prices)
    out = {(a, b): [] for a in range(17) for b in range(a, 17)}
    for source in range(17):
        def extend(path, segment_start, segment_length):
            v = path[-1]
            if v >= source:
                out[source, v].append(tuple(path))
            for u in sorted(adj[v]):
                if u in path:
                    continue
                if v < 14 and u < 14:
                    length = segment_length + prices[tuple(sorted((u, v)))]
                    assert segment_start is not None
                    if length != d[segment_start][u]:
                        continue
                    extend(path + [u], segment_start, length)
                elif u < 14:
                    extend(path + [u], u, 0)
                else:
                    extend(path + [u], None, 0)
        extend([source], source if source < 14 else None, 0)
    assert all(out.values())
    return out

def incidence(path, prices):
    result = [0] * 7
    for a, b in zip(path, path[1:]):
        e = tuple(sorted((a, b)))
        if e in prices:
            result[-1] += prices[e]
        else:
            result[VARIABLE_EDGES.index(e)] += 1
    return result

def build(data):
    prices = {(a, b): w for a, b, w in data['prices']}
    assert sorted(prices) == CORE and [prices[e] for e in CORE] == PRICE_A
    assert data['variable_edges'] == [list(e) for e in VARIABLE_EDGES]
    routes = catalog(prices)
    enc = Encoding()
    parents = {(z, p): enc.new() for z in sorted(MARKS) for p in sorted(ADJ[z])}
    for z in sorted(MARKS):
        group = [parents[z, p] for p in sorted(ADJ[z])]
        enc.add(group)
        for a, b in combinations(group, 2):
            enc.add([-a, -b])
    for i in range(6):
        vector = [0] * 7
        vector[i] = 1
        enc.add([enc.inequality(vector, True)])
    for pair in data['pairs']:
        assert len(pair) == 2
        assert all(len(K & MARKS) <= 4 for K in components(ADJ, set(pair[0]) | set(pair[1])))
        conditions = set()
        core_paths = []
        for path in pair:
            assert path and len(path) == len(set(path)) and all(v in ADJ for v in path)
            assert all(b in ADJ[a] for a, b in zip(path, path[1:]))
            assert all(v < 17 for v in path[1:-1])
            if len(path) > 1 and path[0] in MARKS:
                conditions.add((path[0], path[1]))
            if len(path) > 1 and path[-1] in MARKS:
                conditions.add((path[-1], path[-2]))
            middle = [v for v in path if v < 17]
            if not middle:
                assert len(path) == 1 and path[0] in MARKS
                continue
            if middle[0] > middle[-1]:
                middle.reverse()
            assert tuple(middle) in routes[middle[0], middle[-1]]
            core_paths.append(middle)
        clause = [-parents[z, p] for z, p in sorted(conditions)]
        for p in core_paths:
            left = incidence(p, prices)
            for other in routes[p[0], p[-1]]:
                right = incidence(other, prices)
                clause.append(enc.inequality([a - b for a, b in zip(left, right)], True))
        enc.add(clause)
    return enc, {'core_routes': sum(map(len, routes.values())), 'templates': len(data['pairs']),
                 'parent_assignments': 4 ** 9, 'base_clauses': len(enc.clauses)}

def verify_A(data):
    enc, counts = build(data)
    for index, vector in data['extra_linear_atoms']:
        assert index == enc.next and len(vector) == 7
        assert all(type(v) is int for v in vector) and normalized(vector) == tuple(vector)
        assert enc.atom(vector) == index
    for row in data['farkas']:
        assert row
        total = [Fraction(0)] * 7
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


def distances(n, costs):
    infinity = sum(costs.values()) + 1
    d = [[0 if a == b else infinity for b in range(n)] for a in range(n)]
    for (a, b), w in costs.items():
        assert w >= 0
        d[a][b] = d[b][a] = w
    for k in range(n):
        for a in range(n):
            for b in range(n):
                d[a][b] = min(d[a][b], d[a][k] + d[k][b])
    return d

def masses(pair):
    return sorted(len(K & MARKS) for K in components(ADJ, set(pair[0]) | set(pair[1])))

def static_template(template, prices):
    # An independently constructed pseudometric, with the six shortcuts
    # set to zero, is a lower bound for every positive choice of them.
    lower = distances(17, dict(prices) | {e: 0 for e in VARIABLE_EDGES})
    assert len(template['paths']) == 2
    parent = dict(template['conditions'])
    assert len(parent) == len(template['conditions'])
    assert all(z in MARKS and p in ADJ[z] for z, p in parent.items())
    for path in template['paths']:
        assert path and len(path) == len(set(path)) and all(v in ADJ for v in path)
        core = list(path)
        if core[0] in MARKS:
            assert len(core) > 1 and parent[core[0]] == core[1]
            core.pop(0)
        if core[-1] in MARKS:
            assert len(core) > 1 and parent[core[-1]] == core[-2]
            core.pop()
        assert core and all(v < 14 for v in core)
        cost = sum(prices[tuple(sorted((a, b)))] for a, b in zip(core, core[1:]))
        assert cost == lower[core[0]][core[-1]]
    assert max(masses(template['paths']), default=0) <= 4

def verify_static(data):
    assert {r['metric'] for r in data} == {'B', 'symmetric'} and len(data) == 2
    ids = {(z, p): 1 + 4 * (z - 17) + j for z in sorted(MARKS) for j, p in enumerate(sorted(ADJ[z]))}
    counts = {'metrics': 2, 'templates': 0, 'rup_additions': 0}
    for row in data:
        prices = {(a, b): w for a, b, w in row['prices']}
        assert sorted(prices) == CORE and all(w > 0 for w in prices.values())
        if row['metric'] == 'B':
            assert [prices[e] for e in CORE] == [7,10,4,8,7,11,9,6,16,14,3,23,3,16,15,16,3,10,22,9,12,3,12,7]
        else:
            assert set(prices.values()) == {1}
        clauses = []
        for z in sorted(MARKS):
            group = [ids[z, p] for p in sorted(ADJ[z])]
            clauses.append(group)
            clauses.extend([-a, -b] for a, b in combinations(group, 2))
        for template in row['templates']:
            static_template(template, prices)
            clauses.append([-ids[z, p] for z, p in template['conditions']])
            counts['templates'] += 1
        counts['rup_additions'] += rup(clauses, row['rup'], 36)
    return {'status': 'PASS', **counts}


def main():
    start = time.monotonic()
    data_A = json.loads((HERE / 'certificate_A.json').read_text())
    data_static = json.loads((HERE / 'certificate_static.json').read_text())
    exact = verify_A(data_A)
    static = verify_static(data_static)
    assert exact == {'status': 'PASS', 'core_routes': 1066, 'templates': 48,
                     'parent_assignments': 262144, 'base_clauses': 117,
                     'linear_atoms': 177, 'farkas_lemmas': 217, 'rup_additions': 28}
    assert static == {'status': 'PASS', 'metrics': 2, 'templates': 48, 'rup_additions': 4}
    hashes = {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
              for name in ('certificate_A.json', 'certificate_static.json')}
    result = {'status': 'PASS', 'vertices': 26, 'edges': 72, 'faces': 48,
              'metric_A': exact, 'zero_contraction': static,
              'certificate_sha256': hashes,
              'seconds': round(time.monotonic() - start, 6)}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
